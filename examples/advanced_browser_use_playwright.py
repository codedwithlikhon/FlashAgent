"""Advanced Browser-Use + Playwright integration demo.

Key capabilities
----------------
1. Browser-Use and Playwright share the same Chromium instance through CDP.
2. Custom Browser-Use actions call Playwright for precise DOM interactions.
3. Agents can mix native Browser-Use actions with Playwright helpers in one task.

Run locally with::

    uv pip install -r examples/requirements.txt
    playwright install chromium --with-deps --no-shell
    python examples/advanced_browser_use_playwright.py

Make sure ``OPENAI_API_KEY`` (or any OpenAI-compatible key) is exported.
"""

from __future__ import annotations

import asyncio
import os
import tempfile
from typing import Optional

import aiohttp
from pydantic import BaseModel, Field
from playwright.async_api import Browser, Page, async_playwright

from browser_use import Agent, BrowserSession, ChatOpenAI, Tools
from browser_use.agent.views import ActionResult

# Shared Playwright handles (populated at runtime)
playwright_browser: Optional[Browser] = None
playwright_page: Optional[Page] = None


class PlaywrightFillFormAction(BaseModel):
    """Parameters for the ``playwright_fill_form`` custom action."""

    customer_name: str = Field(..., description="Customer name to fill")
    phone_number: str = Field(..., description="Phone number to fill")
    email: str = Field(..., description="Email address to fill")
    size_option: str = Field(..., description="Size option (small/medium/large)")


class PlaywrightScreenshotAction(BaseModel):
    """Parameters for the ``playwright_screenshot`` custom action."""

    filename: str = Field(
        default="playwright_screenshot.png", description="Filename for screenshot"
    )
    quality: Optional[int] = Field(
        default=None, description="JPEG quality (1-100). Only used for JPEG files."
    )


class PlaywrightGetTextAction(BaseModel):
    """Parameters for grabbing text via Playwright selectors."""

    selector: str = Field(..., description='CSS selector or the literal "title".')


async def start_chrome_with_debug_port(port: int = 9222) -> asyncio.subprocess.Process:
    """Launch a standalone Chrome/Chromium instance with CDP enabled."""

    user_data_dir = tempfile.mkdtemp(prefix="flashagent_chrome_")

    chrome_candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium-browser",
        "chromium",
        "chrome",
    ]

    executable: Optional[str] = None
    for candidate in chrome_candidates:
        if os.path.exists(candidate) or candidate in {"chrome", "chromium"}:
            try:
                proc = await asyncio.create_subprocess_exec(
                    candidate,
                    "--version",
                    stdout=asyncio.subprocess.DEVNULL,
                    stderr=asyncio.subprocess.DEVNULL,
                )
                await proc.wait()
                executable = candidate
                break
            except OSError:
                continue

    if not executable:
        raise RuntimeError("Chrome/Chromium executable not found on PATH")

    args = [
        executable,
        f"--remote-debugging-port={port}",
        f"--user-data-dir={user_data_dir}",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-extensions",
        "about:blank",
    ]
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL
    )

    # Wait up to ~20 seconds for CDP endpoint to respond
    for _ in range(20):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"http://localhost:{port}/json/version") as resp:
                    if resp.status == 200:
                        return process
        except aiohttp.ClientError:
            pass
        await asyncio.sleep(1)

    process.terminate()
    raise RuntimeError("Chrome failed to expose CDP endpoint in time")


async def connect_playwright_to_cdp(cdp_url: str) -> None:
    """Attach Playwright to the Browser-Use controlled Chromium instance."""

    global playwright_browser, playwright_page

    playwright = await async_playwright().start()
    playwright_browser = await playwright.chromium.connect_over_cdp(cdp_url)

    if playwright_browser.contexts and playwright_browser.contexts[0].pages:
        playwright_page = playwright_browser.contexts[0].pages[0]
    else:
        context = await playwright_browser.new_context()
        playwright_page = await context.new_page()


# ---------------------------------------------------------------------------
# Custom Browser-Use actions backed by Playwright
# ---------------------------------------------------------------------------

tools = Tools()


@tools.registry.action(
    "Fill out a form using Playwright for reliable DOM targeting.",
    param_model=PlaywrightFillFormAction,
)
async def playwright_fill_form(
    params: PlaywrightFillFormAction, browser_session: BrowserSession
) -> ActionResult:
    if not playwright_page:
        return ActionResult(error="Playwright not connected. Run setup first.")

    try:
        await playwright_page.wait_for_selector('input[name="custname"]', timeout=10_000)
        await playwright_page.fill('input[name="custname"]', params.customer_name)
        await playwright_page.fill('input[name="custtel"]', params.phone_number)
        await playwright_page.fill('input[name="custemail"]', params.email)

        select_locator = playwright_page.locator('select[name="size"]')
        radio_locator = playwright_page.locator(
            f'input[name="size"][value="{params.size_option}"]'
        )

        if await select_locator.count() > 0:
            await playwright_page.select_option('select[name="size"]', params.size_option)
        elif await radio_locator.count() > 0:
            await playwright_page.check(
                f'input[name="size"][value="{params.size_option}"]'
            )
        else:
            raise ValueError(f"Size option not found: {params.size_option}")

        form_data = {
            "name": await playwright_page.input_value('input[name="custname"]'),
            "phone": await playwright_page.input_value('input[name="custtel"]'),
            "email": await playwright_page.input_value('input[name="custemail"]'),
        }
        if await select_locator.count() > 0:
            form_data["size"] = await playwright_page.input_value('select[name="size"]')
        else:
            checked = playwright_page.locator('input[name="size"]:checked')
            form_data["size"] = (
                await checked.get_attribute("value") if await checked.count() else None
            )

        return ActionResult(
            extracted_content=f"Form filled successfully: {form_data}",
            include_in_memory=True,
            long_term_memory=f"Filled order form with {form_data}",
        )
    except Exception as exc:  # noqa: BLE001
        return ActionResult(error=f"Playwright form fill failed: {exc}")


@tools.registry.action(
    "Capture a screenshot with Playwright for high fidelity previews.",
    param_model=PlaywrightScreenshotAction,
)
async def playwright_screenshot(
    params: PlaywrightScreenshotAction, browser_session: BrowserSession
) -> ActionResult:
    if not playwright_page:
        return ActionResult(error="Playwright not connected. Run setup first.")

    try:
        kwargs = {"path": params.filename, "full_page": True}
        if (
            params.quality is not None
            and params.filename.lower().endswith((".jpg", ".jpeg"))
        ):
            kwargs["quality"] = params.quality

        await playwright_page.screenshot(**kwargs)
        return ActionResult(
            extracted_content=f"Screenshot saved to {params.filename}",
            include_in_memory=True,
            long_term_memory=f"Screenshot saved to {params.filename}",
        )
    except Exception as exc:  # noqa: BLE001
        return ActionResult(error=f"Playwright screenshot failed: {exc}")


@tools.registry.action(
    "Extract text with Playwright selectors (supports CSS and XPath).",
    param_model=PlaywrightGetTextAction,
)
async def playwright_get_text(
    params: PlaywrightGetTextAction, browser_session: BrowserSession
) -> ActionResult:
    if not playwright_page:
        return ActionResult(error="Playwright not connected. Run setup first.")

    try:
        if params.selector.lower() == "title":
            title = await playwright_page.title()
            payload = {
                "selector": "title",
                "text_content": title,
                "inner_text": title,
                "tag_name": "TITLE",
                "is_visible": True,
            }
        else:
            element = playwright_page.locator(params.selector).first
            if await element.count() == 0:
                return ActionResult(error=f"No element found for selector {params.selector}")

            payload = {
                "selector": params.selector,
                "text_content": await element.text_content(),
                "inner_text": await element.inner_text(),
                "tag_name": await element.evaluate("el => el.tagName"),
                "is_visible": await element.is_visible(),
            }

        return ActionResult(
            extracted_content=str(payload),
            include_in_memory=True,
            long_term_memory=f"Extracted text from {params.selector}: {payload['text_content']}",
        )
    except Exception as exc:  # noqa: BLE001
        return ActionResult(error=f"Playwright text extraction failed: {exc}")


async def main() -> None:
    print("🚀 Launching Browser-Use + Playwright demo")

    chrome_process: Optional[asyncio.subprocess.Process] = None
    try:
        chrome_process = await start_chrome_with_debug_port()
        cdp_url = "http://localhost:9222"
        await connect_playwright_to_cdp(cdp_url)

        browser_session = BrowserSession(cdp_url=cdp_url)
        agent = Agent(
            task=(
                "Navigate to https://httpbin.org/forms/post, fill the form using the "
                "Playwright helper, capture a screenshot, extract the page title, "
                "submit the form, and report the outcome."
            ),
            llm=ChatOpenAI(model="gpt-4.1-mini"),
            tools=tools,
            browser_session=browser_session,
        )

        result = await agent.run()
        print(f"✅ Demo finished. Final result: {result}")
    finally:
        if playwright_browser:
            await playwright_browser.close()
        if chrome_process:
            chrome_process.terminate()
            try:
                await asyncio.wait_for(chrome_process.wait(), timeout=5)
            except asyncio.TimeoutError:
                chrome_process.kill()

        print("✅ Cleanup complete")


if __name__ == "__main__":
    asyncio.run(main())

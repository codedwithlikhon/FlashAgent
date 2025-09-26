"""Advanced Browser-Use + Playwright demo.

This script shows how to share a Chrome instance between Browser-Use and
Playwright. Custom Browser-Use actions leverage Playwright APIs for precise
interactions such as form filling, screenshots, and targeted text extraction.
"""

from __future__ import annotations

import asyncio
import os
import tempfile
from typing import Any

import aiohttp
from pydantic import BaseModel, Field
from playwright.async_api import Browser, Page, async_playwright

from browser_use import Agent, BrowserSession, ChatOpenAI, Tools
from browser_use.agent.views import ActionResult

playwright_browser: Browser | None = None
playwright_page: Page | None = None


class PlaywrightFillFormAction(BaseModel):
    """Parameters for filling a demo form with Playwright."""

    customer_name: str = Field(..., description="Customer name to fill")
    phone_number: str = Field(..., description="Phone number to fill")
    email: str = Field(..., description="Email address to fill")
    size_option: str = Field(..., description="Size option (small/medium/large)")


class PlaywrightScreenshotAction(BaseModel):
    """Parameters for capturing a screenshot using Playwright."""

    filename: str = Field(
        default="playwright_screenshot.png",
        description="Filename for screenshot",
    )
    quality: int | None = Field(
        default=None,
        description="JPEG quality (1-100), only used for JPEG files",
    )


class PlaywrightGetTextAction(BaseModel):
    """Parameters for fetching text content via a Playwright selector."""

    selector: str = Field(..., description='CSS selector or "title" for page title')


tools = Tools()


async def start_chrome_with_debug_port(port: int = 9222) -> asyncio.subprocess.Process:
    """Start Chrome with the remote debugging port enabled."""

    user_data_dir = tempfile.mkdtemp(prefix="chrome_cdp_")
    chrome_paths = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium-browser",
        "chrome",
        "chromium",
    ]

    chrome_exe: str | None = None
    for path in chrome_paths:
        if os.path.exists(path) or path in {"chrome", "chromium"}:
            try:
                process = await asyncio.create_subprocess_exec(
                    path,
                    "--version",
                    stdout=asyncio.subprocess.DEVNULL,
                    stderr=asyncio.subprocess.DEVNULL,
                )
                await process.wait()
                chrome_exe = path
                break
            except Exception:
                continue

    if not chrome_exe:
        raise RuntimeError("Chrome executable not found. Install Chrome or Chromium.")

    process = await asyncio.create_subprocess_exec(
        chrome_exe,
        f"--remote-debugging-port={port}",
        f"--user-data-dir={user_data_dir}",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-extensions",
        "about:blank",
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL,
    )

    for _ in range(20):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"http://localhost:{port}/json/version",
                    timeout=aiohttp.ClientTimeout(total=1),
                ) as response:
                    if response.status == 200:
                        return process
        except Exception:
            await asyncio.sleep(1)
        else:
            break
    else:
        process.terminate()
        raise RuntimeError("Chrome failed to start with CDP")

    return process


async def connect_playwright_to_cdp(cdp_url: str) -> None:
    """Attach Playwright to the Chrome instance launched for Browser-Use."""

    global playwright_browser, playwright_page
    playwright = await async_playwright().start()
    playwright_browser = await playwright.chromium.connect_over_cdp(cdp_url)

    if playwright_browser.contexts and playwright_browser.contexts[0].pages:
        playwright_page = playwright_browser.contexts[0].pages[0]
    else:
        context = await playwright_browser.new_context()
        playwright_page = await context.new_page()


@tools.registry.action(
    "Fill a form using Playwright selectors for precise interaction.",
    param_model=PlaywrightFillFormAction,
)
async def playwright_fill_form(
    params: PlaywrightFillFormAction, browser_session: BrowserSession
) -> ActionResult:
    """Fill the demo form with Playwright and report the captured values."""

    del browser_session
    if not playwright_page:
        return ActionResult(error="Playwright not connected. Run setup first.")

    try:
        await playwright_page.wait_for_selector('input[name="custname"]', timeout=10000)
        await playwright_page.fill('input[name="custname"]', params.customer_name)
        await playwright_page.fill('input[name="custtel"]', params.phone_number)
        await playwright_page.fill('input[name="custemail"]', params.email)

        size_select = playwright_page.locator('select[name="size"]')
        size_radio = playwright_page.locator(
            f'input[name="size"][value="{params.size_option}"]'
        )

        if await size_select.count() > 0:
            await playwright_page.select_option('select[name="size"]', params.size_option)
        elif await size_radio.count() > 0:
            await size_radio.check()
        else:
            raise ValueError(f"Could not find size input for value: {params.size_option}")

        checked_value: str | None
        if await size_select.count() > 0:
            checked_value = await playwright_page.input_value('select[name="size"]')
        else:
            checked_radio = playwright_page.locator('input[name="size"]:checked')
            checked_value = await checked_radio.get_attribute("value")

        payload = {
            "name": await playwright_page.input_value('input[name="custname"]'),
            "phone": await playwright_page.input_value('input[name="custtel"]'),
            "email": await playwright_page.input_value('input[name="custemail"]'),
            "size": checked_value,
        }

        message = f"Form filled successfully with Playwright: {payload}"
        return ActionResult(
            extracted_content=message,
            include_in_memory=True,
            long_term_memory=f"Filled form with: {payload}",
        )
    except Exception as exc:  # noqa: BLE001
        return ActionResult(error=f"Playwright form filling failed: {exc}")


@tools.registry.action(
    "Capture a screenshot using Playwright.",
    param_model=PlaywrightScreenshotAction,
)
async def playwright_screenshot(
    params: PlaywrightScreenshotAction, browser_session: BrowserSession
) -> ActionResult:
    """Capture a full-page screenshot with optional JPEG quality control."""

    del browser_session
    if not playwright_page:
        return ActionResult(error="Playwright not connected. Run setup first.")

    try:
        kwargs: dict[str, Any] = {"path": params.filename, "full_page": True}
        if params.quality is not None and params.filename.lower().endswith((".jpg", ".jpeg")):
            kwargs["quality"] = params.quality
        await playwright_page.screenshot(**kwargs)
        message = f"Screenshot saved as {params.filename} using Playwright"
        return ActionResult(
            extracted_content=message,
            include_in_memory=True,
            long_term_memory=f"Screenshot saved: {params.filename}",
        )
    except Exception as exc:  # noqa: BLE001
        return ActionResult(error=f"Playwright screenshot failed: {exc}")


@tools.registry.action(
    "Extract text using Playwright selectors.",
    param_model=PlaywrightGetTextAction,
)
async def playwright_get_text(
    params: PlaywrightGetTextAction, browser_session: BrowserSession
) -> ActionResult:
    """Retrieve text content for a given selector or the page title."""

    del browser_session
    if not playwright_page:
        return ActionResult(error="Playwright not connected. Run setup first.")

    try:
        if params.selector.lower() == "title":
            text_content = await playwright_page.title()
            payload = {
                "selector": "title",
                "text_content": text_content,
                "inner_text": text_content,
                "tag_name": "TITLE",
                "is_visible": True,
            }
        else:
            element = playwright_page.locator(params.selector).first
            if await element.count() == 0:
                return ActionResult(error=f"No element found with selector: {params.selector}")

            text_content = await element.text_content()
            payload = {
                "selector": params.selector,
                "text_content": text_content,
                "inner_text": await element.inner_text(),
                "tag_name": await element.evaluate("el => el.tagName"),
                "is_visible": await element.is_visible(),
            }

        message = f"Extracted text using Playwright: {payload}"
        return ActionResult(
            extracted_content=str(payload),
            include_in_memory=True,
            long_term_memory=f"Extracted from {payload['selector']}: {payload['text_content']}",
        )
    except Exception as exc:  # noqa: BLE001
        return ActionResult(error=f"Playwright text extraction failed: {exc}")


def build_agent(port: int) -> Agent:
    """Initialise the Browser-Use agent with custom Playwright powered tools."""

    session = BrowserSession(cdp_url=f"http://localhost:{port}")
    return Agent(
        task=(
            "Demonstrate Playwright + Browser-Use integration by filling a form, "
            "capturing a screenshot, extracting the page title, and submitting the form."
        ),
        llm=ChatOpenAI(model="gpt-4.1-mini"),
        tools=tools,
        browser_session=session,
    )


async def main() -> None:
    """Run the integration demo end-to-end."""

    port = 9222
    chrome_process: asyncio.subprocess.Process | None = None

    try:
        chrome_process = await start_chrome_with_debug_port(port=port)
        await connect_playwright_to_cdp(f"http://localhost:{port}")
        agent = build_agent(port)
        result = await agent.run()
        print(f"Integration demo completed: {result}")
        await asyncio.sleep(2)
    finally:
        if playwright_browser:
            await playwright_browser.close()
        if chrome_process:
            chrome_process.terminate()
            try:
                await asyncio.wait_for(chrome_process.wait(), timeout=5)
            except asyncio.TimeoutError:
                chrome_process.kill()


if __name__ == "__main__":
    asyncio.run(main())

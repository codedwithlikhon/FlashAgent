"""Simple Browser-Use demo that connects via an existing CDP endpoint."""

import asyncio
import os
import sys

from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

from browser_use import Agent, Tools  # noqa: E402
from browser_use.browser import BrowserProfile, BrowserSession  # noqa: E402
from browser_use.llm import ChatOpenAI  # noqa: E402


async def main() -> None:
    browser_session = BrowserSession(
        browser_profile=BrowserProfile(cdp_url="http://localhost:9222", is_local=True)
    )
    tools = Tools()

    agent = Agent(
        task='Visit https://duckduckgo.com and search for "browser-use founders"',
        llm=ChatOpenAI(model="gpt-4.1-mini"),
        tools=tools,
        browser_session=browser_session,
    )

    await agent.run()
    await browser_session.kill()


if __name__ == "__main__":
    asyncio.run(main())

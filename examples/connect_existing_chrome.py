"""Attach Browser-Use to an already running Chrome profile."""

from __future__ import annotations

import asyncio
import os
import sys

from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

from browser_use import Agent, Browser, ChatOpenAI  # noqa: E402


async def main() -> None:
    browser = Browser(
        executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        user_data_dir=os.path.expanduser("~/Library/Application Support/Google/Chrome"),
        profile_directory="Default",
    )

    agent = Agent(
        llm=ChatOpenAI(model="gpt-4.1-mini"),
        task='Visit https://duckduckgo.com and search for "browser-use founders"',
        browser=browser,
    )
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())

"""Connect Browser-Use to an already running Chrome profile."""

import asyncio
import os
import sys

from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

from browser_use import Agent, Browser, ChatOpenAI  # noqa: E402


def build_browser() -> Browser:
    """Attach to a locally running Chrome profile using Browser-Use."""

    return Browser(
        executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        user_data_dir="~/Library/Application Support/Google/Chrome",
        profile_directory="Default",
    )


async def main() -> None:
    """Search DuckDuckGo for browser-use founders."""

    browser = build_browser()
    agent = Agent(
        llm=ChatOpenAI(model="gpt-4.1-mini"),
        task='Visit https://duckduckgo.com and search for "browser-use founders"',
        browser=browser,
    )
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())

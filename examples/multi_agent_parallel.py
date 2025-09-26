"""Run multiple Browser-Use agents concurrently (experimental)."""

from __future__ import annotations

import asyncio

from browser_use import Agent, Browser, ChatOpenAI


async def main() -> None:
    browsers = [
        Browser(user_data_dir=f"./temp-profile-{i}", headless=False)
        for i in range(3)
    ]

    agents = [
        Agent(
            task="Search for 'browser automation' on Google",
            browser=browsers[0],
            llm=ChatOpenAI(model="gpt-4.1-mini"),
        ),
        Agent(
            task="Search for 'AI agents' on DuckDuckGo",
            browser=browsers[1],
            llm=ChatOpenAI(model="gpt-4.1-mini"),
        ),
        Agent(
            task='Visit Wikipedia and search for "web scraping"',
            browser=browsers[2],
            llm=ChatOpenAI(model="gpt-4.1-mini"),
        ),
    ]

    results = await asyncio.gather(*(agent.run() for agent in agents), return_exceptions=True)
    print("🎉 All agents completed!", results)


if __name__ == "__main__":
    asyncio.run(main())

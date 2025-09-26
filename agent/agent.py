from __future__ import annotations

from typing import Optional

from browser_use import Agent, ChatOpenAI, Tools
from browser_use.agent.views import AgentHistoryList

from browser.browser import browser_factory
from config.load_config import config


def get_agent(
    task: str,
    model: str,
    api_key: str,
    base_url: Optional[str] = None,
    browser_session=None,
    conversation_id: Optional[str] = None,
) -> Agent:
    tools = Tools()
    llm = ChatOpenAI(model=model, api_key=api_key, base_url=base_url or None)
    session = browser_session or browser_factory.create_shared_session(headless=True)
    return Agent(task=task, llm=llm, tools=tools, browser_session=session, conversation_id=conversation_id)

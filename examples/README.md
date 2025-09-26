# Browser-Use demonstration scripts

The scripts in this directory illustrate different ways to connect Browser-Use
agents to Chrome and Playwright instances.

## Available demos

| Script                                          | Description                                                                                                                     |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `advanced_playwright_integration.py`            | Launches a shared Chrome instance, registers Playwright-powered actions, and demonstrates end-to-end task execution.            |
| `connect_existing_chrome.py`                    | Reuses an already running Chrome profile and executes a simple DuckDuckGo search.                                              |
| `simple_cdp_demo.py` (`cdp_duckduckgo_demo.py`) | Connects to a running Chrome instance through its CDP endpoint, navigates to DuckDuckGo, and runs the search task with the agent. |
| `multi_agent_parallel_demo.py`                  | Spawns three Browser-Use agents in parallel, each with its own temporary profile directory.                                     |

All scripts expect the `OPENAI_API_KEY` environment variable to be set.

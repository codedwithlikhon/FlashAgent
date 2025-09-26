# Browser-Use demonstration scripts

The scripts in this directory illustrate different ways to connect Browser-Use
agents to Chrome and Playwright instances.

## Available demos

- `advanced_playwright_integration.py` – Launches a shared Chrome instance,
  registers Playwright-powered actions, and demonstrates end-to-end task
  execution.
- `connect_existing_chrome.py` – Reuses an already running Chrome profile and
  executes a simple DuckDuckGo search.
- `cdp_duckduckgo_demo.py` – Uses the Chrome DevTools Protocol (CDP) endpoint at
  `http://localhost:9222` to run a Browser-Use agent without launching a new
  browser process.
- `multi_agent_parallel_demo.py` – Spawns three Browser-Use agents in parallel,
  each with its own temporary profile directory.

All scripts expect the `OPENAI_API_KEY` environment variable to be set.

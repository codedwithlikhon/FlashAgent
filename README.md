# FlashAgent

## Example scripts

| Script | Description |
| --- | --- |
| `examples/advanced_playwright_integration.py` | Launches a Playwright-powered Chrome instance, registers custom Browser-Use actions, and runs an end-to-end task. |
| `examples/connect_existing_chrome.py` | Attaches to an already running Chrome profile and demonstrates issuing search queries through Browser-Use. |
| `examples/cdp_duckduckgo_demo.py` | Connects to a Chrome DevTools Protocol endpoint at `http://localhost:9222` to run a Browser-Use agent without spawning a new browser process. |
| `examples/multi_agent_parallel.py` | Runs several Browser-Use agents concurrently, each starting its own isolated Playwright browser instance for parallel execution. |

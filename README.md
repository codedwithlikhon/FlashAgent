# FlashAgent

FlashAgent collects lightweight demos that explore Browser-Use agents working alongside Playwright-driven automation and supporting tooling. Use the examples in this repository as copy-and-run references for building your own experiments.

## Example scripts

| Script | Scenario | Key capabilities |
| --- | --- | --- |
| `examples/advanced_browser_use_playwright.py` | Shares a Chrome instance between Browser-Use and Playwright to coordinate actions. | Registers Playwright-backed custom actions for precise form filling, full-page screenshots, and targeted text extraction while Browser-Use handles planning. |
| `examples/connect_existing_chrome.py` | Connects to a Chrome instance that is already running with a remote debugging port. | Reuses an existing user profile without launching a new browser process and runs a scripted DuckDuckGo search. |
| `examples/cdp_duckduckgo_demo.py` | Demonstrates a minimal CDP-driven agent flow. | Attaches to the Chrome DevTools Protocol endpoint and walks through a search workflow via Browser-Use. |
| `examples/multi_agent_parallel_demo.py` | Launches several Browser-Use agents in parallel. | Spawns isolated temporary profiles so each agent can run concurrently without interfering with others. |

All demos expect the `OPENAI_API_KEY` environment variable to be set and require `playwright install chromium` to be run once before execution.

## License

FlashAgent is distributed under the MIT License. See [`LICENSE`](LICENSE) for details.

# FlashAgent

FlashAgent is a collection of end-to-end examples that demonstrate how to combine the
[`browser-use`](https://github.com/browser-use/browser-use) agent framework with Playwright,
custom Chrome instances, and containerised runtimes. The goal of this repository is to
provide copy-and-run samples for developers who want to explore advanced browser
automation scenarios, from orchestrating Playwright actions through Browser-Use to building
Docker images that package every dependency required by an agentic stack.

## Repository structure

- [`frontend/`](frontend/) – Ant Design Vue dashboard that orchestrates MCP servers,
  terminals, and workspace previews for FlashAgent scenarios.
- [`examples/`](examples/) – Python scripts that highlight specific integration patterns
  between Browser-Use, Playwright, and shared Chrome sessions.
- [`docker/`](docker/) – Dockerfiles and helper scripts for producing reproducible images
  ranging from minimal Python environments up to full VS Code based workspaces.

Each example is designed to be self-contained, well documented, and ready for adaptation to
real-world automation tasks.

## Getting started

FlashAgent now ships with a Vue 3 + Ant Design Vue control plane and the original
Python examples. You can run either side independently.

### Frontend workspace (Vue 3)

1. Install dependencies and start the Vite dev server:

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

2. Open the printed URL (defaults to <http://localhost:5173>) to explore the
   dashboard. The UI ships with mocked data sources so it renders immediately,
   and it wires in components for MCP server management, a terminal console,
   search insights, and a VS Code inspired file explorer.

3. When you are ready to build for production:

   ```bash
   npm run build
   npm run preview
   ```

### Python automation examples

1. Create and activate a virtual environment (we recommend
   [`uv`](https://github.com/astral-sh/uv) for speed and reproducibility).

   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -r requirements.txt
   ```

2. Install the Playwright browsers that are required by the demos:

   ```bash
   playwright install chromium
   ```

3. Export your OpenAI compatible API key so that the Browser-Use agent can talk to an LLM:

   ```bash
   export OPENAI_API_KEY="sk-..."
   ```

4. Execute any script inside `examples/` to experiment with a scenario. For instance, the
   advanced integration demo can be launched with:

   ```bash
   python examples/advanced_playwright_integration.py
   ```

The Dockerfiles under `docker/` provide ready-to-build images when a fully containerised
experience is preferred.

## License

This repository is distributed under the MIT License. See the [`LICENSE`](LICENSE) file for
full details.

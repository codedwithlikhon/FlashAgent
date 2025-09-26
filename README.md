# FlashAgent

FlashAgent demonstrates how Browser-Use agents, Playwright, and modern developer tooling can be orchestrated into a single workflow. The repository contains:

- **Frontend dashboard** (Vue 3 + Ant Design Vue) for interacting with MCP servers, exploring workspaces, running commands in a terminal, and previewing code files.
- **Python examples** showing how to combine Browser-Use with Playwright, attach to existing Chrome sessions, reuse CDP connections, and run multiple agents simultaneously.
- **Docker assets** that speed up local experimentation with layered base images and reproducible browser dependencies.
- **Runtime helpers** for exposing VS Code in the browser and managing shared Browser-Use sessions.

> **Note**  This codebase targets developers who want copy-and-run examples rather than a production-grade platform. Use the docs in `docs/` for architectural recommendations if you plan to build a hardened system.

## Repository structure

```
├── agent/                      # Browser-Use agent factory and manager helpers
├── browser/                    # Browser session configuration
├── browser_server/             # FastAPI server and dependencies for remote execution
├── config/                     # YAML-driven runtime configuration
├── docker/                     # Layered Docker build files and helper scripts
├── docs/                       # Research and architectural guidance
├── examples/                   # Python Browser-Use + Playwright demos
├── frontend/                   # Vue 3 dashboard (Vite)
├── src/runtime/plugins/vscode/ # VS Code server settings for the runtime image
└── README.md
```

## Getting started

### 1. Frontend dashboard

```bash
cd frontend
npm install
npm run dev
```

The dashboard expects a compatible backend (see `browser_server/`). You can still explore the UI components and mock data locally without running the backend.

### 2. Python examples

Use `uv` (recommended) or virtualenv.

```bash
uv venv
source .venv/bin/activate
uv pip install -r examples/requirements.txt
uv pip install -r browser_server/requirements.txt  # optional when launching the server
playwright install chromium --with-deps --no-shell
```

Run an example:

```bash
python examples/advanced_browser_use_playwright.py
```

### 3. Docker builds

Build the layered base images once and reuse them for fast iterations:

```bash
cd docker
./build-base-images.sh
cd ..
docker build -f docker/Dockerfile.fast -t flashagent .
```

The standard `docker/Dockerfile` is self-contained if you do not want to pre-build layers.

### 4. VS Code runtime container

The Dockerfile in the repository root provisions OpenVSCode Server. After building the image you can run:

```bash
docker run -p 3000:3000 -p 9000:9000 flashagent
```

Then open `http://localhost:3000` to use VS Code in the browser while the Browser-Use services run inside the container.

## Documentation

The docs in `docs/` capture key research:

- `docs/elevating-flashagent.md` – roadmap recommendations covering sandboxing, tool integration, and UI modernization.
- `docs/agent-framework-research.md` – reference comparisons across Manus, Browser Use, Lemon AI, OpenHands, and Geist.

These guides explain how to evolve FlashAgent into a hardened, secure platform.

## License

FlashAgent is distributed under the MIT License. See `LICENSE` for details.

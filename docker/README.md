# Docker setup for FlashAgent

This directory mirrors the layered build strategy described in the documentation. Build the base layers once, then compose the main image.

```bash
./build-base-images.sh
cd ..
docker build -f docker/Dockerfile.fast -t flashagent .
```

`Dockerfile.fast` relies on three base layers:

- `browseruse/base-system` – Python runtime with minimal system dependencies.
- `browseruse/base-chromium` – Adds Chromium installed via Playwright.
- `browseruse/base-python-deps` – Installs Python dependencies via `uv`.

Use the standard `Dockerfile` if you prefer a single self-contained build (~2 minutes on cold cache).

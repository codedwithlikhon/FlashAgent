FROM python:3.12-slim

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        wget \
        fonts-liberation \
        libnss3 \
        libatk1.0-0 \
        libatk-bridge2.0-0 \
        libdrm2 \
        libxkbcommon0 \
        libgbm1 \
        libxshmfence1 \
        libasound2 \
        libxdamage1 \
        libxrandr2 \
        libpango-1.0-0 \
        libpangocairo-1.0-0 && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

WORKDIR /app
COPY requirements.txt ./
RUN uv pip install -r requirements.txt

RUN PLAYWRIGHT_BROWSERS_PATH=/opt/playwright playwright install chromium --with-deps --no-shell

COPY . .

CMD ["python", "examples/advanced_playwright_integration.py"]

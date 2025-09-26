FROM python:3.12-slim

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        wget \
        git \
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

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
COPY --from=ghcr.io/astral-sh/uv:latest /uvx /bin/uvx

ENV PATH="/root/.local/bin:$PATH" \
    PYTHONUNBUFFERED=1

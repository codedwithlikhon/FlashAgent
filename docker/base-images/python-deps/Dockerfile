ARG BASE_TAG=latest
FROM browseruse/base-chromium:${BASE_TAG}

ENV PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH" \
    PLAYWRIGHT_BROWSERS_PATH=/opt/playwright

WORKDIR /app
COPY requirements.txt ./

RUN --mount=type=cache,target=/root/.cache/uv,sharing=locked \
    uv venv && \
    uv pip install -r requirements.txt && \
    rm requirements.txt

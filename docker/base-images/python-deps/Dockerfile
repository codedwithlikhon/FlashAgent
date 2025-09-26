ARG BASE_TAG=latest
FROM browseruse/base-chromium:${BASE_TAG}

ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /app
COPY pyproject.toml uv.lock* ./

RUN --mount=type=cache,target=/root/.cache/uv,sharing=locked \
    uv venv && \
    uv sync --all-extras --no-dev --no-install-project --compile-bytecode

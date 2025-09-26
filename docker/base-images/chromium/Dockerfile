ARG BASE_TAG=latest
FROM browseruse/base-system:${BASE_TAG}

WORKDIR /tmp

RUN --mount=type=cache,target=/root/.cache,sharing=locked \
    pip install --no-cache-dir playwright && \
    PLAYWRIGHT_BROWSERS_PATH=/opt/playwright playwright install chromium --with-deps --no-shell && \
    ln -sf /opt/playwright/chromium-*/chrome-linux/chrome /usr/bin/chromium-browser && \
    chmod -R 755 /opt/playwright && \
    pip uninstall -y playwright

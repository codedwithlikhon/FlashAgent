#!/usr/bin/env bash
set -euo pipefail

BASE_TAG=${1:-latest}
ROOT_DIR=$(cd "$(dirname "$0")" && pwd)

build_image() {
  local name=$1
  local dockerfile=$2
  echo "[flashagent] Building ${name} (${dockerfile})"
  docker build --build-arg BASE_TAG=${BASE_TAG} -f "${dockerfile}" -t "browseruse/${name}:${BASE_TAG}" "${ROOT_DIR}"
}

build_image base-system docker/base-images/system/Dockerfile
build_image base-chromium docker/base-images/chromium/Dockerfile
build_image base-python-deps docker/base-images/python-deps/Dockerfile

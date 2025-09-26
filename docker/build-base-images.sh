#!/usr/bin/env bash
set -euo pipefail

BASE_TAG="latest"

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

build_image() {
  local dockerfile="$1"
  local tag="$2"
  echo "Building ${tag} from ${dockerfile}"
  docker build \
    -f "${ROOT_DIR}/${dockerfile}" \
    -t "${tag}:${BASE_TAG}" \
    "${ROOT_DIR}"
}

build_image "docker/base-images/system/Dockerfile" "browseruse/base-system"
build_image "docker/base-images/chromium/Dockerfile" "browseruse/base-chromium"
build_image "docker/base-images/python-deps/Dockerfile" "browseruse/base-python-deps"

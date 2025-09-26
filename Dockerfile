FROM node:22-slim

ENV MAMBA_ROOT_PREFIX=/chataa/micromamba \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    OPENVSCODE_SERVER_ROOT=/chataa/.openvscode-server

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        wget curl sudo git jq tmux bash ca-certificates file lsof zip unzip libatomic1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /chataa /chataa/logs

RUN mkdir -p /chataa/micromamba/bin && \
    /bin/bash -c "PREFIX_LOCATION=/chataa/micromamba BIN_FOLDER=/chataa/micromamba/bin INIT_YES=no CONDA_FORGE_YES=yes $(curl -L https://micro.mamba.pm/install.sh)" && \
    /chataa/micromamba/bin/micromamba create -n chataa -c conda-forge python=3.12 poetry -y

ENV PATH=/chataa/micromamba/envs/chataa/bin:$PATH

WORKDIR /chataa/code

COPY package.json package-lock.json ./
RUN npm ci --omit=dev

COPY frontend ./frontend
RUN cd frontend && npm install && npm run build

COPY browser_server /chataa/code/browser_server
COPY examples /chataa/code/examples
COPY docs /chataa/code/docs
COPY README.md LICENSE pyproject.toml uv.lock ./

RUN pip install -r browser_server/requirements.txt && \
    patchright install chromium --with-deps --no-shell

# OpenVSCode Server
ARG RELEASE_TAG="openvscode-server-v1.94.2"
ARG RELEASE_ORG="gitpod-io"
RUN arch=$(uname -m) && \
    if [ "$arch" = "x86_64" ]; then arch="x64"; elif [ "$arch" = "aarch64" ]; then arch="arm64"; fi && \
    wget https://github.com/${RELEASE_ORG}/openvscode-server/releases/download/${RELEASE_TAG}/${RELEASE_TAG}-linux-${arch}.tar.gz && \
    tar -xzf ${RELEASE_TAG}-linux-${arch}.tar.gz && \
    mv ${RELEASE_TAG}-linux-${arch} ${OPENVSCODE_SERVER_ROOT} && \
    rm -f ${RELEASE_TAG}-linux-${arch}.tar.gz

EXPOSE 3000 9000
CMD ["bash"]

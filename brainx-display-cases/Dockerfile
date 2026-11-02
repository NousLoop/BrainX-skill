# Evaluation image for the BrainX skill refinement harness.
#
# The harness runs the agent inside this image, so the image is part of the
# frozen execution conditions: build it once, tag it with a date, and reuse the
# same tag for every compared run. Do not rebuild between compared runs.
#
#   bash brainx-display-cases/build-eval-image.sh
#
# Contents: codex CLI, node (for the Codex MCP reviewer server), and a Linux
# BrainX virtualenv at /brainx-venv. No credentials are baked in; the model
# provider config is mounted per run.

# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim

ARG NODE_VERSION=22.23.4
# Pin a BrainX release for reproducible evaluations, for example 2026.7.9.
# Leave empty to let pip resolve the latest Python-compatible release, and pin
# afterwards by rebuilding with the resolved version.
ARG BRAINX_RELEASE=
# cpu | cuda12 | cuda13 | tpu
ARG BRAINX_EXTRA=cpu
ARG CODEX_VERSION=0.166.0
ARG VENV_PATH=/brainx-venv
# Debian mirror. The default pointed at deb.debian.org fails behind some
# proxies with 502 Bad Gateway; override with any mirror that works for you.
ARG APT_MIRROR=https://mirrors.tuna.tsinghua.edu.cn/debian
# Optional PyPI and npm mirrors, for example
# https://pypi.tuna.tsinghua.edu.cn/simple and https://registry.npmmirror.com
ARG PIP_INDEX_URL=
ARG NPM_REGISTRY=

ENV VENV_PATH=${VENV_PATH}

# Node is required by mcp-servers/codex, which the evaluated workflow may call.
# Install it from the official tarball: the Debian packages pull in perl and
# gnupg, which some mirrors and proxies serve slowly or not at all.
RUN set -eux; \
  if [ -f /etc/apt/sources.list.d/debian.sources ]; then \
    sed -i "s|http://deb.debian.org/debian|${APT_MIRROR}|g; s|http://deb.debian.org|${APT_MIRROR}|g" \
      /etc/apt/sources.list.d/debian.sources; \
  else \
    sed -i "s|http://deb.debian.org/debian|${APT_MIRROR}|g; s|http://deb.debian.org|${APT_MIRROR}|g" \
      /etc/apt/sources.list; \
  fi; \
  apt-get update \
  && apt-get install -y --no-install-recommends \
       -o Acquire::Retries=5 \
       ca-certificates curl xz-utils \
  && rm -rf /var/lib/apt/lists/*

RUN set -eux; \
  case "$(dpkg --print-architecture)" in \
    amd64) node_arch=x64 ;; \
    arm64) node_arch=arm64 ;; \
    *) echo "unsupported architecture: $(dpkg --print-architecture)" >&2; exit 1 ;; \
  esac; \
  curl -fsSL --retry 3 \
    "https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-linux-${node_arch}.tar.xz" \
    | tar -xJ -C /usr/local --strip-components=1; \
  node --version; \
  npm --version

# Pin the CLI for evaluations: --build-arg CODEX_VERSION=0.166.0
RUN set -eux; \
  npm config set registry "${NPM_REGISTRY:-https://registry.npmjs.org}"; \
  if [ "${CODEX_VERSION}" = "latest" ]; then \
    npm i -g @openai/codex; \
  else \
    npm i -g "@openai/codex@${CODEX_VERSION}"; \
  fi; \
  codex --version

# One indivisible BrainX release. Never assemble subpackage versions by hand.
RUN set -eux; \
  python -m venv "${VENV_PATH}"; \
  if [ -n "${PIP_INDEX_URL}" ]; then export PIP_INDEX_URL; fi; \
  "${VENV_PATH}/bin/python" -m pip install --retries 5 --timeout 120 -U "pip>=23"; \
  if [ -z "${BRAINX_RELEASE}" ]; then \
    "${VENV_PATH}/bin/pip" install --retries 5 --timeout 120 -U "BrainX[${BRAINX_EXTRA}]" matplotlib; \
  else \
    "${VENV_PATH}/bin/pip" install --retries 5 --timeout 120 -U "BrainX[${BRAINX_EXTRA}]==${BRAINX_RELEASE}" matplotlib; \
  fi; \
  "${VENV_PATH}/bin/python" -c "import BrainX, jax; print('BrainX OK'); print('JAX devices:', jax.devices())"

# Codex executes Bash login shells, whose /etc/profile resets PATH.
RUN printf '%s\n' 'export PATH="${VENV_PATH}/bin:$PATH"' > /etc/profile.d/brainx-venv.sh
ENV VIRTUAL_ENV="${VENV_PATH}"
ENV PATH="${VENV_PATH}/bin:/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin:/sbin"

WORKDIR /workspace

LABEL org.opencontainers.image.title="BrainX evaluation image" \
      org.opencontainers.image.description="codex CLI plus a Linux BrainX virtualenv for isolated skill refinement runs" \
      brainx.extra="${BRAINX_EXTRA}" \
      brainx.release="${BRAINX_RELEASE}" \
      brainx.codex="${CODEX_VERSION}"

#!/usr/bin/env bash
# Build the evaluation image used by run-refinement-case.sh.
#
# Build once, tag with a date, then reuse the same tag for every compared run so
# the runtime is part of the frozen execution conditions.
#
#   bash brainx-display-cases/windows-docker/build-eval-image.sh
#
# For a reproducible evaluation, pin the release and the CLI:
#   BRAINX_RELEASE=2026.7.9 CODEX_VERSION=0.166.0 \
#     BRAINX_EVAL_IMAGE=brainx-eval:2026-10-30 \
#     bash brainx-display-cases/windows-docker/build-eval-image.sh
#
# Run from Git Bash on Windows; the build context is an empty directory.

set -euo pipefail

# Git Bash rewrites arguments that start with `/` into Windows paths before a
# native docker.exe sees them, which corrupts container-absolute paths such as
# /brainx-venv/bin/python. Disable that conversion on Windows hosts.
export MSYS_NO_PATHCONV=1
export MSYS2_ARG_CONV_EXCL='*'

here=$(cd "$(dirname "$0")" && pwd -P)
if test -f "$here/brainx-eval.env"; then
  if test -n "$(LC_ALL=C tr -cd '\r' < "$here/brainx-eval.env")"; then
    echo "Save $here/brainx-eval.env with LF line endings before running Bash" >&2
    exit 1
  fi
  set -a
  . "$here/brainx-eval.env"
  set +a
fi
image="${BRAINX_EVAL_IMAGE:-brainx-eval:latest}"

command -v docker >/dev/null 2>&1 || {
  echo "Docker is required to build the evaluation image" >&2
  exit 1
}

# With MSYS_NO_PATHCONV=1 above, Git Bash no longer rewrites `/`-prefixed host
# paths for docker.exe, so convert host paths explicitly where docker needs the
# Windows form. Container paths stay literal.
docker_path() {
  if command -v cygpath >/dev/null 2>&1; then
    cygpath -w "$1"
  else
    printf '%s' "$1"
  fi
}

# The image copies nothing from the repository: the skill snapshot, the MCP
# server tree, and the prompt file are mounted per run, so the build context is
# an empty directory instead of a workspace full of archived runs.
context=$(mktemp -d)
trap 'rm -rf "$context"' EXIT

docker build \
  --build-arg "PYTHON_VERSION=${BRAINX_PYTHON_VERSION:-3.11}" \
  --build-arg "VENV_PATH=${BRAINX_VENV_IN_IMAGE:-/brainx-venv}" \
  --build-arg "NODE_VERSION=${BRAINX_NODE_VERSION:-22.23.4}" \
  --build-arg "BRAINX_RELEASE=${BRAINX_RELEASE:-}" \
  --build-arg "BRAINX_EXTRA=${BRAINX_EXTRA:-cpu}" \
  --build-arg "CODEX_VERSION=${CODEX_VERSION:-0.166.0}" \
  --build-arg "APT_MIRROR=${APT_MIRROR:-https://mirrors.tuna.tsinghua.edu.cn/debian}" \
  --build-arg "PIP_INDEX_URL=${PIP_INDEX_URL:-}" \
  --build-arg "NPM_REGISTRY=${NPM_REGISTRY:-}" \
  -t "$image" \
  -f "$(docker_path "$here/Dockerfile")" \
  "$(docker_path "$context")"

echo "Verifying image contents"
docker run --rm "$image" codex --version
repo=$(cd "$here/../.." && pwd -P)
docker run --rm --network none -e BRAINX_CODEX_BIN=codex \
  --security-opt "seccomp=$(docker_path "$here/seccomp-reviewer.json")" \
  -v "$(docker_path "$repo/mcp-servers"):/bundle/mcp-servers:ro" \
  -v "$(docker_path "$repo/skills"):/bundle/skills:ro" \
  -v "$(docker_path "$here/smoke-test-reviewer.py"):/checks/smoke-test-reviewer.py:ro" \
  "$image" python /checks/smoke-test-reviewer.py
docker run --rm "$image" "${BRAINX_VENV_IN_IMAGE:-/brainx-venv}/bin/python" -c \
  "import BrainX, jax, matplotlib; print('BrainX OK'); print('JAX devices:', jax.devices())"

docker run --rm "$image" bash -lc \
  'python -c "import brainmass, brainstate, brainunit, braintools; print(\"Login-shell BrainX imports OK\")"'

digest=$(docker image inspect --format '{{.Id}}' "$image")
cat <<EOF

Image ready: $image
Image digest: $digest

Record both in the run metadata (run-refinement-case.sh writes eval_image and
eval_image_digest automatically). Set BRAINX_EVAL_IMAGE=$image before launching
any run that must be compared with another.
EOF

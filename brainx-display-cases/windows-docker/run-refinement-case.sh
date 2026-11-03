#!/usr/bin/env bash
# BrainX skill refinement harness.
#
# Portable host supported (macOS, Linux, Windows Git Bash). Host read isolation
# is provided by a Docker container: only the workspace, the frozen skill
# snapshot, the MCP server tree, and the prompt file are mounted, so earlier run
# folders, the repository, and the normal Codex and agents homes are invisible
# by construction.
#
# Run with Git Bash on Windows:  bash run-refinement-case.sh <case> <run>
# Do not run from PowerShell or zsh: this script relies on Bash PIPESTATUS.

set -euo pipefail

# Git Bash rewrites arguments that start with `/` into Windows paths before a
# native docker.exe sees them, which corrupts container-absolute paths such as
# /workspace and /output/agent-final.md. Disable that conversion on Windows hosts.
export MSYS_NO_PATHCONV=1
export MSYS2_ARG_CONV_EXCL='*'

# Optional local configuration file (git-ignored) holding repo paths and the
# API key. Everything it sets can equally be exported before invocation.
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

# Freeze the launcher and its helper files before any long-running command.
# Bash reads scripts incrementally; editing the checkout must not change an
# already-running launcher's archive logic or seccomp policy.
if test "${BRAINX_FROZEN_HARNESS:-0}" != 1; then
  freeze_tmp_root="${TMPDIR:-/tmp}"
  if command -v cygpath >/dev/null 2>&1; then freeze_tmp_root=$(cygpath -u "$freeze_tmp_root"); fi
  frozen=$(mktemp -d "$freeze_tmp_root/brainx-harness.XXXXXX")
  cp "$0" "$frozen/run-refinement-case.sh"
  cp "$here/smoke-test-reviewer.py" "$here/seccomp-reviewer.json" "$frozen/"
  export BRAINX_FROZEN_HARNESS=1
  exec bash "$frozen/run-refinement-case.sh" "$@"
fi

repo=$(cd "${BRAINX_REPO:?set BRAINX_REPO to the skill-bundle checkout, see brainx-eval.env.example}" && pwd -P)
eval_image="${BRAINX_EVAL_IMAGE:-brainx-eval:latest}"
venv_in_image="${BRAINX_VENV_IN_IMAGE:-/brainx-venv}"
normal_codex_home="${NORMAL_CODEX_HOME:-$HOME/.codex}"
normal_agents_home="${NORMAL_AGENTS_HOME:-$HOME/.agents}"
cases_dir="$repo/brainx-display-cases"

# Model backend. The evaluator uses the local Magpie proxy through the shim:
# minimal-eval-config.toml freezes the request shape (endpoint,
# wire API, service tier) so a run cannot be silently moved to another host.
# BRAINX_EVAL_CONFIG / BRAINX_EVAL_MODEL / BRAINX_EVAL_REASONING_EFFORT are
# escape hatches for a one-off experiment; every compared run leaves them at
# the defaults below.
# The harness lives inside windows-docker/, but the default is anchored on the
# repository (not on $here, which becomes the frozen temp copy after re-exec).
eval_config_file="${BRAINX_EVAL_CONFIG:-$cases_dir/windows-docker/minimal-eval-config.toml}"
eval_model="${BRAINX_EVAL_MODEL:-codex/gpt-6.1-sol}"
eval_reasoning_effort="${BRAINX_EVAL_REASONING_EFFORT:-xhigh}"
test -f "$eval_config_file" || {
  echo "Evaluator config not found: $eval_config_file" >&2
  exit 1
}

# The nested reviewer never passes --model; it falls back to the config's
# `model =` line. A mismatch would silently evaluate with one model and review
# with another, so refuse to launch instead.
config_model=$(sed -n 's/^model[[:space:]]*=[[:space:]]*"\([^"]*\)".*/\1/p' \
  "$eval_config_file" | head -n 1)
if [ "$config_model" != "$eval_model" ]; then
  echo "Model fork: evaluator model '$eval_model' != reviewer fallback '$config_model' in $eval_config_file." >&2
  echo "Align BRAINX_EVAL_MODEL with the config's 'model =' line to the same string." >&2
  exit 1
fi

# Model credential, injected only into the evaluator container environment.
# Never printed, never archived, never baked into the image. The variable name
# is fixed by the provider declared in minimal-eval-config.toml.
api_key_env="OPENAI_API_KEY"
api_key=$(printenv "$api_key_env" 2>/dev/null || true)
test -n "$api_key" || {
  echo "set $api_key_env, see brainx-eval.env.example" >&2
  exit 1
}

case_name="${1:?usage: $0 <case-name> <run-name>}"
run_name="${2:?usage: $0 <case-name> <run-name>}"
case "$run_name" in
  .|..|*/*|*\\*) echo "Run name must be a single directory name" >&2; exit 1 ;;
esac
# Cases live in an environment directory: windows-docker/<case> or
# windows-docker/<category>/<case> for active work, legacy-macos/... for
# archived macOS-era cases. windows-docker is searched first so a case
# present in both resolves to the active copy.
case_dir=$(find "$cases_dir/windows-docker" "$cases_dir/legacy-macos" \
  -mindepth 1 \
  -maxdepth 2 \
  -type d \
  -name "$case_name" \
  -print \
  -quit)
test -n "$case_dir" || {
  echo "Unknown refinement case: $case_name" >&2
  exit 1
}
run_dir="$case_dir/$run_name"
prompt_file="$case_dir/prompt.md"
test ! -e "$run_dir" || {
  echo "Refusing to overwrite existing run: $run_dir" >&2
  exit 1
}

case "$case_name" in
  04-online-working-memory)
    expected_prompt_bytes="733"
    expected_prompt_sha256="629e6b6f36083f51bf808a1e8c0014a272222b993511097c7068261728e00119"
    ;;
  05-alpha-rhythm)
    expected_prompt_bytes="577"
    expected_prompt_sha256="c6b42ffbed8f7f18ed64b1184e8c68ffb9491e63d8967f0234264075964a3f41"
    ;;
  06-seizure-recruitment)
    expected_prompt_bytes="560"
    expected_prompt_sha256="eb726d96bf1cb1baac11f39113fce2faf2dab096fa97e01f71c89938f13bd139"
    ;;
  08-binocular-rivalry)
    expected_prompt_bytes="718"
    expected_prompt_sha256="b8e98eb70a623270c82a1894d6b8229c9b8ca2f71034ca336433c41c24f477b1"
    ;;
  *)
    echo "Unsupported refinement case: $case_name" >&2
    exit 1
    ;;
esac

# An approved scientific variant must supply its own frozen fingerprint; never
# edit the original case prompt or silently disable the baseline fingerprint.
prompt_kind=original
if test -n "${BRAINX_EVAL_PROMPT:-}"; then
  prompt_file="$BRAINX_EVAL_PROMPT"
  expected_prompt_bytes="${BRAINX_EXPECTED_PROMPT_BYTES:?set the approved prompt byte count}"
  expected_prompt_sha256="${BRAINX_EXPECTED_PROMPT_SHA256:?set the approved prompt SHA-256}"
  prompt_kind=approved-variant
  case "$prompt_file" in
    /*) ;;
    *) echo "BRAINX_EVAL_PROMPT must be an absolute POSIX path (Git Bash: /c/...)" >&2; exit 1 ;;
  esac
  if [[ "$run_name" =~ ^run[0-9]+$ ]]; then
    echo "Approved prompt variants require a descriptive name, not $run_name" >&2
    exit 1
  fi
fi

test -f "$prompt_file" || {
  echo "Prompt file not found: $prompt_file" >&2
  exit 1
}
prompt_file="$(cd "$(dirname "$prompt_file")" && pwd -P)/$(basename "$prompt_file")"

if test -n "${BRAINX_EVAL_WORKSPACE_SEED:-}"; then
  test "$prompt_kind" = approved-variant || {
    echo "A workspace continuation requires an explicitly approved prompt variant" >&2
    exit 1
  }
  case "$BRAINX_EVAL_WORKSPACE_SEED" in
    /*) ;;
    *) echo "BRAINX_EVAL_WORKSPACE_SEED must be an absolute POSIX path" >&2; exit 1 ;;
  esac
  workspace_seed=$(cd "$BRAINX_EVAL_WORKSPACE_SEED" && pwd -P)
fi

sha256_of() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$1" | awk '{print $1}'
  elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$1" | awk '{print $1}'
  else
    echo "No SHA-256 tool available (need sha256sum or shasum)" >&2
    return 1
  fi
}

if command -v iconv >/dev/null 2>&1; then
  iconv -f UTF-8 -t UTF-8 "$prompt_file" >/dev/null
fi
prompt_bytes=$(wc -c < "$prompt_file" | tr -d '[:space:]')
prompt_sha256=$(sha256_of "$prompt_file")
test "$prompt_bytes" = "$expected_prompt_bytes" || {
  echo "Prompt byte count changed" >&2
  exit 1
}
test "$prompt_sha256" = "$expected_prompt_sha256" || {
  echo "Prompt SHA-256 changed" >&2
  exit 1
}

command -v docker >/dev/null 2>&1 || {
  echo "Docker is required for host read isolation" >&2
  exit 1
}
docker info >/dev/null 2>&1 || {
  echo "Docker daemon unreachable; start Docker Desktop" >&2
  exit 1
}
eval_image_digest=$(docker image inspect --format '{{.Id}}' "$eval_image") || {
  echo "Evaluation image missing: $eval_image; build or pull it first" >&2
  exit 1
}
eval_platform=$(docker image inspect --format '{{.Os}}/{{.Architecture}}' "$eval_image_digest")
docker_memory_bytes=$(docker info --format '{{.MemTotal}}')
if test "$docker_memory_bytes" -lt 8589934592; then
  echo "WARNING: Docker has less than 8 GiB of memory; verify the experiment's memory budget" >&2
fi
running_containers=$(docker ps -q)
if test -n "$running_containers"; then
  echo "WARNING: Other containers are running; check for parallel evaluations and resource contention" >&2
fi

# Docker Desktop on Windows needs host paths in Windows form.
docker_path() {
  if command -v cygpath >/dev/null 2>&1; then
    cygpath -w "$1"
  else
    printf '%s' "$1"
  fi
}

tmp_root="${TMPDIR:-/tmp}"
if command -v cygpath >/dev/null 2>&1; then
  tmp_root=$(cygpath -u "$tmp_root")
fi
stage=$(mktemp -d "$tmp_root/brainx-skill-eval.XXXXXX")
stage=$(cd "$stage" && pwd -P)
workspace="$stage/workspace"
isolated_codex_home="$stage/codex-home"
minimal_config="$isolated_codex_home/config.toml"
output_dir="$stage/output"

mkdir -p "$workspace" "$isolated_codex_home/skills" "$output_dir"
cp -R "$repo/skills/." "$isolated_codex_home/skills/"

# Probe file for the isolation checks, derived from the snapshot itself so a
# change in the skills layout cannot silently turn the probe into a no-op.
skill_probe_rel=$(cd "$repo/skills" && find . -name SKILL.md | LC_ALL=C sort | sed -n '1p')
test -n "$skill_probe_rel" || {
  echo "Skill snapshot contains no SKILL.md; wrong BRAINX_REPO?" >&2
  exit 1
}
skill_probe_rel="${skill_probe_rel#./}"

# Deterministic hash of the whole skill tree. codex-home is mounted writable
# (codex writes startup state there), so the frozen-snapshot guarantee is
# protected by read-only child mounts and checked again after the run.
skill_tree_sha256() {
  # codex injects its own built-in skills under skills/.system at startup (49
  # files in 0.166.0). That is CLI behaviour, not a modification of the frozen
  # BrainX snapshot, and the pinned image digest makes it identical on every
  # run, so it is excluded here and reported separately in the metadata.
  (
    cd "$1" && find . -type f -not -path "./.system/*" | LC_ALL=C sort | while IFS= read -r f; do
      printf '%s  %s\n' "$(sha256_of "$f")" "$f"
    done
  ) | {
    if command -v sha256sum >/dev/null 2>&1; then sha256sum; else shasum -a 256; fi
  } | awk '{print $1}'
}
skill_snapshot_sha256=$(skill_tree_sha256 "$isolated_codex_home/skills")

sed \
  -e 's|/[A-Za-z0-9 ./_+-]*/mcp-servers/codex/server\.mjs|/bundle/mcp-servers/codex/server.mjs|g' \
  "$eval_config_file" > "$minimal_config"
config_sha256=$(sha256_of "$minimal_config")
seccomp_sha256=$(sha256_of "$here/seccomp-reviewer.json")
harness_sha256=$(sha256_of "$0")

# Inside the container the repository itself is never mounted; only the MCP
# server tree is, because the evaluated workflow may call the Codex reviewer.
# Only the output subdirectory is mounted for the final message.
# codex-home must be writable because codex creates PATH aliases and
# app-server state inside CODEX_HOME at startup; the skill snapshot stays
# protected by read-only child mounts and also checked after the run.
mounts=(
  "$workspace:/workspace:rw"
  "$isolated_codex_home:/codex-home:rw"
  "$prompt_file:/prompt/prompt.md:ro"
  "$repo/mcp-servers:/bundle/mcp-servers:ro"
  "$isolated_codex_home/skills:/bundle/skills:ro"
  "$output_dir:/output:rw"
  "$here/smoke-test-reviewer.py:/checks/smoke-test-reviewer.py:ro"
)
# Overlay each BrainX skill directory read-only; CODEX_HOME and .system remain
# writable for CLI startup. The reviewer sees the same snapshot at /bundle/skills.
for skill_dir in "$isolated_codex_home/skills/"*; do
  test -d "$skill_dir" || continue
  mounts+=("$skill_dir:/codex-home/skills/${skill_dir##*/}:ro")
done

docker_args=()
for mount in "${mounts[@]}"; do
  source_path="${mount%%:*}"
  remainder="${mount#*:}"
  docker_args+=(-v "$(docker_path "$source_path"):$remainder")
done

docker_run_isolated() {
  # -i keeps stdin open so the prompt file can be piped into `codex exec -`.
  docker run --rm -i \
    --security-opt "seccomp=$(docker_path "$here/seccomp-reviewer.json")" \
    "${docker_args[@]}" \
    -w /workspace \
    -e CODEX_HOME=/codex-home \
    -e BRAINX_CODEX_BIN=codex \
    -e "PATH=$venv_in_image/bin:/usr/local/bin:/usr/bin:/bin" \
    -e "$api_key_env" \
    "$eval_image_digest" \
    "$@"
}

# Host-side mount audit: the only host paths reachable from the container are
# the ones mounted above. Everything else, including earlier run folders, is
# unreachable by construction.
assert_not_mounted() {
  local forbidden="$1"
  local mount source_path
  for mount in "${mounts[@]}"; do
    source_path="${mount%%:*}"
    if test -f "$source_path" && test ! -d "$source_path"; then
      # Mounting one file exposes only that file, never its siblings, so it
      # only violates the rule when it is the forbidden path itself. This is
      # what lets the prompt file live inside the repository.
      test "$source_path" = "$forbidden" || continue
    else
      # Mounting a directory exposes only its subtree, so it violates the rule
      # only when it covers the forbidden path. This is what lets
      # mcp-servers be mounted from inside the repository.
      case "$forbidden" in
        "$source_path"|"$source_path"/*) ;;
        *) continue ;;
      esac
    fi
    echo "Isolation failure: $forbidden is exposed by the container mount $source_path" >&2
    return 1
  done
  case "$forbidden" in
    "$stage"/*) ;;
    *) return 0 ;;
  esac
  echo "Isolation failure: $forbidden lives under the live stage directory" >&2
  return 1
}

docker_run_isolated test -r "/codex-home/skills/$skill_probe_rel" || {
  echo "Isolated skill snapshot is not readable: $skill_probe_rel" >&2
  exit 1
}
for forbidden in "$repo" "$normal_codex_home" "$normal_agents_home" "$case_dir"; do
  assert_not_mounted "$forbidden" || exit 1
done
docker_run_isolated test -r "/prompt/prompt.md" || {
  echo "Prompt file is not readable inside evaluator container" >&2
  exit 1
}
docker_run_isolated bash -lc \
  'python -c "import brainmass, brainstate, brainunit, braintools; print(\"Login-shell BrainX imports OK\")"' || {
  echo "BrainX unavailable in login-shell Python; rebuild the image with build-eval-image.sh" >&2
  exit 1
}
docker_run_isolated touch "/workspace/.isolation-write-probe" || {
  echo "Evaluator workspace is not writable inside container" >&2
  exit 1
}
rm -f "$workspace/.isolation-write-probe"

if test -d "$case_dir/inputs"; then
  cp -R "$case_dir/inputs/." "$workspace/"
fi

workspace_seed_sha256=none
if test -n "${BRAINX_EVAL_WORKSPACE_SEED:-}"; then
  workspace_seed_sha256=$(skill_tree_sha256 "$workspace_seed")
  cp -R "$workspace_seed/." "$workspace/"
  # These are outer-harness records, not scientific project inputs. Preserve
  # originals in the seed archive and create new records after this run exits.
  rm -f "$workspace/codex-events.jsonl" "$workspace/codex-stderr.log" \
    "$workspace/harness-prompt.md" "$workspace/harness-metadata.txt"
fi

eval_provider=$(docker_run_isolated python -c 'import tomllib; print(tomllib.load(open("/codex-home/config.toml", "rb"))["model_provider"])')
codex_version=$(docker_run_isolated codex --version)
# Verify the effective endpoint from the evaluator's network, not a hard-coded
# host URL. The catalog checks shim and upstream without a paid model request.
if test "$eval_provider" = magpie-local; then
  docker_run_isolated python -c '
import json, sys, tomllib, urllib.request
config = tomllib.load(open("/codex-home/config.toml", "rb"))
provider = config["model_providers"][config["model_provider"]]
url = provider["base_url"].rstrip("/") + "/models"
try:
    with urllib.request.urlopen(url, timeout=5) as response:
        catalog = json.load(response)
    if not any(isinstance(m, dict) and m.get("slug") == sys.argv[1]
               for m in catalog.get("models", [])):
        raise ValueError("selected model absent from Codex catalog")
except Exception as exc:
    print("Magpie/shim preflight failed: " + str(exc), file=sys.stderr)
    sys.exit(1)
print("PASS: configured Magpie/shim catalog is reachable from evaluator")
' "$eval_model" || {
    echo "Start Magpie and magpie-models-shim.py; verify the configured endpoint and model" >&2
    exit 1
  }
fi

docker_run_isolated python /checks/smoke-test-reviewer.py || {
  echo "Reviewer unavailable; rebuild the evaluation image with build-eval-image.sh" >&2
  exit 1
}
echo "Preflight passed: local checks and reviewer handshake only; remaining model quota is not verified"

set +e
docker_run_isolated codex exec \
  --ephemeral \
  --skip-git-repo-check \
  --ignore-rules \
  --sandbox danger-full-access \
  --cd /workspace \
  --model "$eval_model" \
  --config "model_reasoning_effort=\"$eval_reasoning_effort\"" \
  --disable apps \
  --disable memories \
  --disable remote_plugin \
  --json \
  --output-last-message /output/agent-final.md \
  - \
  < "$prompt_file" \
  2> >(tee "$stage/codex-stderr.log" >&2) \
  | tee "$stage/codex-events.jsonl"
agent_status=${PIPESTATUS[0]}
set -e

mkdir "$run_dir"
cp -R "$workspace/." "$run_dir/"
cp "$prompt_file" "$run_dir/harness-prompt.md"
cp "$stage/codex-events.jsonl" "$run_dir/"
cp "$stage/codex-stderr.log" "$run_dir/"
test ! -f "$output_dir/agent-final.md" || cp "$output_dir/agent-final.md" "$run_dir/"
skill_snapshot_final_sha256=$(skill_tree_sha256 "$isolated_codex_home/skills")
skill_snapshot_unchanged=false
test "$skill_snapshot_final_sha256" = "$skill_snapshot_sha256" \
  && skill_snapshot_unchanged=true
{
  printf 'harness_sha256=%s\n' "$harness_sha256"
  printf 'workspace_seed_sha256=%s\n' "$workspace_seed_sha256"
  printf 'prompt_kind=%s\n' "$prompt_kind"
  printf 'prompt_bytes=%s\n' "$prompt_bytes"
  printf 'prompt_sha256=%s\n' "$prompt_sha256"
  printf 'model=%s\n' "$eval_model"
  printf 'model_provider=%s\n' "$eval_provider"
  printf 'reasoning_effort=%s\n' "$eval_reasoning_effort"
  printf 'eval_config=%s\n' "${eval_config_file#$repo/}"
  printf 'eval_config_sha256=%s\n' "$config_sha256"
  printf 'codex_version=%s\n' "$codex_version"
  printf 'reviewer_transport=app-server-stdio\n'
  printf 'host_read_isolation=docker\n'
  printf 'seccomp_profile_sha256=%s\n' "$seccomp_sha256"
  printf 'auth_mechanism=env\n'
  printf 'skill_snapshot_sha256=%s\n' "$skill_snapshot_sha256"
  printf 'skill_snapshot_unchanged=%s\n' "$skill_snapshot_unchanged"
  printf 'codex_system_skills_injected=%s\n' \
    "$(find "$isolated_codex_home/skills/.system" -type f 2>/dev/null | wc -l | tr -d '[:space:]')"
  printf 'eval_image=%s\n' "$eval_image"
  printf 'eval_image_digest=%s\n' "$eval_image_digest"
  printf 'eval_platform=%s\n' "$eval_platform"
  printf 'docker_version=%s\n' "$(docker --version)"
  printf 'exit_code=%s\n' "$agent_status"
} > "$run_dir/harness-metadata.txt"

printf 'Disposable workspace retained at: %s\n' "$stage"
if test "$skill_snapshot_unchanged" != true; then
  echo "Skill snapshot was modified during the run; the archived run is compromised" >&2
  exit 3
fi
exit "$agent_status"

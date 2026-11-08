# Active display cases (Windows Docker)

New experiments go here. Historical macOS-era cases are archived in
`../legacy-macos/` and must not be compared with anything here.

## Frozen environment

Current evaluations and nested reviews use the local Magpie proxy
(`model_provider = "magpie-local"`). The container connects to
`http://host.docker.internal:3426/v1`; `magpie-models-shim.py` forwards requests
to Magpie on host port 3425 and translates the model listing into the pinned
Codex catalog schema. Keep Magpie and the shim running for the whole run.
Supply the credential accepted by the proxy through `OPENAI_API_KEY` in the
git-ignored environment file or exported environment. Changing the provider
or endpoint starts a new baseline.

Recorded in each run's `harness-metadata.txt`. Keep these identical across every
run you intend to compare:

| Setting | Current value |
|---|---|
| `host_read_isolation` | `docker` |
| `codex_version` | `codex-cli 0.166.0` |
| `reviewer_transport` | `app-server-stdio` |
| `eval_image` | `brainx-eval:2026-11-02-login-fix` |
| `eval_platform` | `linux/amd64` |
| `model` / `model_provider` | set via `brainx-eval.env` (git-ignored) |
| `seccomp_profile_sha256` | see `seccomp-reviewer.md` |

Container-to-container runs are comparable across macOS, Linux and Windows Git
Bash because they share one mount set. Only a change of model, provider, CLI
version, image tag or reviewer transport starts a new baseline.

## Layout

The Windows Docker harness lives in this directory: `run-refinement-case.sh`,
`archive-workspace.py`,
`build-eval-image.sh`, `Dockerfile`,
`magpie-models-shim.py` + `codex-model-catalog-0.166.json`, `seccomp-reviewer.*`,
`smoke-test-*.py`, `minimal-eval-config.toml`, and `brainx-eval.env(.example)`.
The archived macOS-era harness (`refinement-eval.sb.in`) is in
`../legacy-macos/`.

Case folders follow the repository-wide convention:

```text
windows-docker/<category>/<NN>-<case-name>/   # category optional
|-- prompt.md          # Original natural-language prompt, byte-frozen
|-- inputs/            # Optional original task inputs
|-- run0/              # Baseline artifacts and diagnosis
`-- runN/              # Further refinement checkpoints
```

Name transport tests, environment tests and interactive variants with a
descriptive non-`runN` folder. Never compare them as unchanged-prompt
refinement checkpoints.

## Rules that matter here

The launcher archives inside Linux after the evaluator exits. Regular files
keep their exact bytes. `.harness-archive/manifest.json` records the original
tree and `.harness-archive/symlinks.tar` preserves exact link definitions;
in-workspace links also receive Windows-readable materialized views. Those
views are not the original link objects. For canonical replay, copy only the
manifest's original file/directory entries into an empty Linux workspace and
restore its declared links at the original `/workspace` mount. Never follow
external, broken, or cyclic links to collect additional inputs.

The evaluator receipt is written to the retained staging directory before
archival. If archival fails after a completed evaluator, preserve that receipt
and failure, recover from the retained workspace without another model call,
and record evaluator, launcher and recovery exit codes separately. Do not
silently label a recovery as an uninterrupted launch.

- `exit_code` is mechanical evidence only. A run is scientifically accepted only
  when an independent review verdict is recorded.
- A run whose reviewer session ends with `turn_aborted` and no verdict has no
  scientific standing. Preserve it under an `invalid-` or `failed-` prefix, or
  drop it; do not retry blindly.
- An approved scientific variant or a seeded continuation is not an
  unchanged-prompt checkpoint. Record `prompt_kind=approved-variant` and keep
  the original `prompt.md` untouched.

## Runbook: ensuring a run reaches a verdict

A run is *complete* only when `exit_code=0` **and** an independent review
verdict exists in `<project>/reviews/iteration-<N>.md`. Everything below exists
to make that happen.

### Launch with integrated preflight

```bash
bash brainx-display-cases/windows-docker/run-refinement-case.sh <case-name> <run-name>
```

The launcher checks optional local configuration LF endings, required variables,
evaluator/reviewer model agreement, case/run paths and the frozen prompt before
creating the evaluation workspace. It verifies the Docker daemon and image,
warns about less than 8 GiB of memory or other running containers, then checks
container imports, isolation and reviewer handshake. For `magpie-local`, it also
checks the configured model catalog from inside the evaluator network; this
exercises both shim and upstream and requires the selected model's Codex slug.

No separate preflight command is needed. These checks make no paid model call
and do not verify remaining quota or guarantee completion. Exported configuration
works without a local `brainx-eval.env`. Approved variants require absolute
POSIX paths and descriptive non-`runN` names; seeds additionally require an
approved variant and an absolute existing directory.

Local regression checks (no real Docker/model calls in the launcher tests):

```bash
python brainx-display-cases/windows-docker/test-run-refinement-case.py
python brainx-display-cases/windows-docker/test-magpie-models-shim.py
```

Run `test-archive-workspace.py -v` with the image's Python in a Linux container,
mounting this harness directory read-only at `/checks`. It checks actual POSIX
relative/absolute links, byte preservation, external/broken/cyclic links and
source/destination guards; Windows symlink privileges are not required.

### Failure modes seen on this machine, and their fixes

| Failure seen | Root cause | Fix / guard |
|---|---|---|
| Launch dies in ~18s, `invalid characters for a local volume name` | `BRAINX_EVAL_PROMPT` passed as a relative path; `docker -v` rejects it | Always absolute paths; preflight checks this |
| HTTP 429 mid-run | Rate limiting or upstream usage limit | Avoid parallel evaluations; confirm quota separately. Launcher connectivity checks do not establish quota. |
| `exit_code=137` | Process killed; possible OOM | Verify the actual cause and memory budget; launcher warns below 8 GiB but cannot rule out OOM. |
| `turn_aborted`, no verdict | magpie's repeated-tool-call guard killed the agent | Not configurable (closed source); recover via continuation |
| `failed to refresh available models` spam | codex 0.166 cannot decode magpie's OpenAI-style `/v1/models` | shim v2 (`magpie-models-shim.py`) translates to catalog schema; keep it running for the whole run |
| Model fork (evaluator 6.1, reviewer 5.6) | `minimal-eval-config.toml` `model=` not synced with env | launch-time assertion in `run-refinement-case.sh` + preflight |
| Run stalls at step-0 clarification gate | correct behavior of the modeling loop | pre-authorize in an approved prompt (researcher approval + delegation) |

### During the run

- Keep Docker Desktop **and** the shim terminal open until the run exits.
- Do not pipe the launcher through `head`/`tail` — SIGPIPE kills the bash
  launcher and orphans the container, which keeps burning tokens. Launch it as
  a trackable background task or in its own terminal.
- Disable Windows sleep for multi-hour runs.

### If a run is interrupted anyway

Nothing scientific is lost: the project's `brainmodeling-memory.md` records the
exact checkpoint. Recover with a seeded continuation:

```bash
BRAINX_EVAL_PROMPT=/abs/path/approved-prompt.md \
BRAINX_EXPECTED_PROMPT_BYTES=<bytes> \
BRAINX_EXPECTED_PROMPT_SHA256=<sha> \
BRAINX_EVAL_WORKSPACE_SEED=/abs/path/<interrupted-run>/<project-dir> \
bash brainx-display-cases/windows-docker/run-refinement-case.sh <case-name> <descriptive-name>
```

All three paths must be absolute. The interrupted run's directory is preserved
as evidence; the continuation is `prompt_kind=approved-variant` and is never an
unchanged-prompt checkpoint.

## Existing content

The 2026-11-02 alpha-rhythm migration attempts were deleted on
2026-11-03: none of the four runs established an accepted baseline (stalled
on a researcher decision, HTTP 429, `exit_code=137`, and `turn_aborted` with
no verdict). Their reusable review findings survive in
`PENDING-SKILL-MINING.md`. The original alpha-rhythm prompt is preserved in
`../legacy-macos/creative-experiment-verification/05-alpha-rhythm/prompt.md`.

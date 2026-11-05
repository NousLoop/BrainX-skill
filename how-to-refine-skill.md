# How to refine a BrainX skill

Use this workflow to improve a BrainX skill from evidence produced by a real
task:

```text
exact prompt -> clean BrainX run -> study relevant BrainX material
-> diagnose generated artifacts -> surgically refine skills
-> clean rerun with the exact prompt -> compare and repeat
```

## Case and run folders

Group tasks by evaluation purpose. Keep one folder for each task and one
subfolder for each agent run:

```text
brainx-display-cases/<environment>/<category>/<NN>-<case-name>/
|-- prompt.md          # Original natural-language prompt
|-- inputs/            # Optional original task inputs
|-- run0/              # Baseline artifacts and diagnosis
|-- run1/              # First post-refinement artifacts and diagnosis
`-- runN/              # Further attempts when needed
```

`<environment>` is `windows-docker` for active cases or `legacy-macos` for
archived macOS-era cases. `<category>` is optional for new cases; the runner
resolves a case by name, searching `windows-docker/` before `legacy-macos/`.
Runs from different environments are never comparable. The Docker harness
scripts themselves (`run-refinement-case.sh`, `build-eval-image.sh`,
`Dockerfile`, the magpie shim, the seccomp profile and
the smoke tests) live in `brainx-display-cases/windows-docker/`; the archived
macOS-era seatbelt profile is in `brainx-display-cases/legacy-macos/`.

Do not edit `prompt.md` or the original inputs between runs. Each fresh agent
writes into an empty disposable workspace containing no case history.
After the process exits, copy its workspace and event log unchanged into the
new `runN/`, then let the reviewing agent add the diagnosis there.

Numbered runs are refinement checkpoints, not repeated samples of one skill
snapshot. Follow this order without skipping or reordering steps:

```text
run0 -> diagnose run0 -> refine, validate, and reinstall skills
-> run1 -> diagnose and compare run1 -> refine, validate, and reinstall skills
-> run2 -> ...
```

Do not launch `runN+1` from the same skill snapshot as `runN`. Create
`runN+1/` only after the diagnosis for `runN` has produced an edit
specification, the intended skill edits are complete, their checks pass, and
the refined snapshot is installed in the new agent environment. Preserve any
accidental same-snapshot rerun under a descriptive non-`runN` folder; it is
control evidence, not the next refinement checkpoint.

Configure the BrainX environment once through environment variables, then use
the same values for every run. See
`brainx-display-cases/windows-docker/brainx-eval.env.example`.

| Variable | Meaning |
|---|---|
| `BRAINX_REPO` | Skill-bundle checkout that supplies the frozen skill snapshot |
| `BRAINX_EVAL_IMAGE` | Container image that runs the agent, with `codex`, `node`, and a Linux virtualenv |
| `BRAINX_VENV_IN_IMAGE` | Virtualenv path inside that image, default `/brainx-venv` |
| `BRAINX_EVAL_MODEL` | Evaluation model, identical across every compared run |

The agent's working directory is the disposable workspace; the virtualenv is
its Python environment. Configure both outside the prompt. Do not use the
virtualenv or the final `runN/` as the live working directory.

On Windows, run every script through Git Bash (`bash run-refinement-case.sh`),
never PowerShell: the harness captures the pipeline status with Bash
`PIPESTATUS`. Always use the Linux virtualenv built into the image; host
virtualenvs are not portable. Keep shell scripts and the local `.env` file in LF.

Prompt files are byte fingerprints. Keep
`brainx-display-cases/**/prompt.md` and `inputs/` marked `-text` in
`.gitattributes` so line-ending conversion never changes the bytes between runs
or across hosts.

### Build the evaluation image once

The image is part of the frozen execution conditions, so build it once, tag it
with a date, and reuse that tag for every compared run:

```bash
BRAINX_RELEASE=2026.10.25 BRAINX_PYTHON_VERSION=3.12 CODEX_VERSION=0.166.0 \
BRAINX_EVAL_IMAGE=brainx-eval:2026.10.25-py312 \
  bash brainx-display-cases/windows-docker/build-eval-image.sh
```

It contains the `codex` CLI, `node` for the Codex MCP reviewer server, and one
indivisible BrainX release in a Linux virtualenv at `/brainx-venv`. Pin
`BRAINX_RELEASE` and `CODEX_VERSION` for any run you intend to compare; an
unpinned build can silently change under you between `runN` and `runN+1`. The
harness records the tag and its digest in `harness-metadata.txt`, so an
unintended rebuild is visible after the fact.

## Rules that must not change between runs

1. Send the exact UTF-8 contents of `prompt.md` as the complete subagent
   message. Do not add paths, setup instructions, hints, prefixes, or suffixes.
2. Start a fresh agent with no inherited conversation for every run. Prefer an
   independent `codex exec` process for reproducible evaluation. If only
   `spawn_agent` is available, use `fork_turns="none"`.
3. Keep the same prompt bytes, inputs, model settings, tools, virtualenv, and
   execution conditions. Only the intended skill edits may change.
4. Do not coach the subagent after launch or repair its generated files.
5. Do not let a later agent read earlier run folders, diagnoses, skill diffs,
   reviewer notes, or previous agent messages.
6. Do not resume the CLI session or send follow-up input. One run is one fresh
   process and one user message.

A separate working directory does not prevent leakage when the agent can read
the full filesystem. Restrict readable roots or use a disposable sandbox that
contains only the current prompt inputs, skill snapshot, virtualenv, and empty
run folder.

## 1. Run the baseline agent

### Launch a context-independent CLI agent

Use `codex exec` as a new top-level process. It receives no parent conversation
because it is not a fork or resumed session. `--ephemeral` prevents the run
from persisting session files, and stdin supplies the exact prompt as the only
user message. Codex still receives its normal platform instructions and the
skills intentionally installed in the isolated `CODEX_HOME`; "exact prompt"
means the complete user message, not the absence of system instructions.

Create a fresh temporary `CODEX_HOME` containing only:

- the frozen BrainX skill snapshot for this run;
- the minimum model-provider configuration and authentication material needed
  to run, or access to the same external credential source;
- no sessions, memories, MCP configuration, plugins, rules, prior logs, or
  repository files.

One unavoidable caveat: codex itself injects its own built-in skills under
`skills/.system/` at startup (49 files in 0.166.0; the `skip_host_skill_discovery`
feature flag does not suppress it). The pinned image digest makes this set
identical on every run, the harness excludes it from the skill-snapshot
integrity hash, and the file count is recorded in `harness-metadata.txt` as
`codex_system_skills_injected` so comparisons stay honest.

Mount the MCP server at `/bundle/mcp-servers` and the frozen skill snapshot
read-only at `/bundle/skills`, preserving the reviewer's relative bundle layout.
Overlay each snapshot directory read-only in `CODEX_HOME/skills`; leave the
home and its CLI-managed `.system` directory writable. Mount only a dedicated
output directory for the final message, never the whole staging tree.

Use CLI 0.166.0 for both evaluation and review. The reviewer exposes the
existing `codex` and `codex-reply` MCP tools and translates them to the native
App Server stdio protocol (`thread/start`, `thread/resume`, and `turn/start`).
The harness verifies a real App Server initialize/tools-list handshake before
evaluation and records `reviewer_transport=app-server-stdio`. No legacy CLI is
installed. Rebuild images created with the earlier dual-CLI compatibility setup.

Do not copy the normal Codex home wholesale. Prepare the minimal provider and
authentication setup once, keep secrets outside the case folder and archived
artifacts, and reuse the same configuration bytes for every compared run.
Authentication stays environment-based: the minimal config declares an auth
command that prints an environment variable (for example `sh -c 'printf %s
"$OPENAI_API_KEY"'`), and the harness injects the actual value into the
evaluator container at launch. The key therefore stays out of the repository,
the archived artifacts, and the container image, and the config bytes remain
identical across runs, hosts, and key rotations.

Current evaluations and nested reviews use the local Magpie proxy through
the `magpie-local` provider in `minimal-eval-config.toml`. Container requests
go to `http://host.docker.internal:3426/v1`, where
`windows-docker/magpie-models-shim.py` forwards them to Magpie on host port
3425. The shim translates `GET /v1/models` into the pinned Codex catalog
schema and forwards model requests to Magpie. Keep both Magpie and the shim
running throughout evaluation. Set `OPENAI_API_KEY` to the credential accepted
by this proxy. The current configuration does not connect directly to the
official OpenAI endpoint. Changing the provider or endpoint starts a new
evaluation baseline.

Historical macOS runs fetched credentials through `/usr/bin/security`;
the Docker workflow instead injects the credential through the environment.
Verify the full credential chain without a live model call by pointing
`base_url` at a local sink and checking the received `Authorization` header
(`brainx-display-cases/windows-docker/smoke-test-auth.py` automates this).
Use only a dummy key and the local sink for this smoke test.
When the evaluated workflow can call the BrainX Codex reviewer, include its
local MCP registration in that minimal config:

```toml
[mcp_servers.codex]
env_vars = ["CODEX_HOME", "OPENAI_API_KEY", "BRAINX_CODEX_BIN"]
command = "node"
args = ["<absolute-repository-path>/mcp-servers/codex/server.mjs"]
default_tools_approval_mode = "approve"
tool_timeout_sec = 1800
```

Explicit `env_vars` keeps the nested reviewer on the isolated Codex home and
provider credential because Codex filters the environment inherited by MCP
servers. Disabling a nonexistent MCP registration creates an invalid transport;
the adapter reads the child configuration and disables only existing servers.

The approval setting is required for non-interactive `codex exec`; without it,
the host cannot present the MCP approval prompt and may surface the denial as
`user cancelled MCP tool call`. The timeout must exceed the longest complete
artifact review.

Use the maintained Docker harness rather than copying a second implementation.
`run-refinement-case.sh` runs its own preflight before the model call: validate
prompt and paths, Docker/image availability, memory/concurrency warnings,
container isolation/imports, configured Magpie catalog and reviewer handshake.
These checks do not establish remaining model quota.
Both build and run scripts load `brainx-display-cases/windows-docker/brainx-eval.env`
when it exists. Copy the example, edit it with LF endings, and keep credentials
local.

```bash
bash brainx-display-cases/windows-docker/build-eval-image.sh
bash brainx-display-cases/windows-docker/run-refinement-case.sh 05-alpha-rhythm run0
```

For an explicitly approved scientific variant, keep the original `prompt.md`
unchanged and save a separate UTF-8 prompt containing the researcher approval.
Set `BRAINX_EVAL_PROMPT`, `BRAINX_EXPECTED_PROMPT_BYTES`, and
`BRAINX_EXPECTED_PROMPT_SHA256` together. The harness verifies the new fingerprint,
archives the exact message as `harness-prompt.md`, and records
`prompt_kind=approved-variant`. Use a descriptive non-`runN` folder for a
transport/environment test or an interactive variant; do not compare it as an
unchanged-prompt refinement checkpoint.

For a researcher-authorized continuation, also set `BRAINX_EVAL_WORKSPACE_SEED`
to the preserved project archive. This requires an approved prompt variant,
copies the project into a fresh workspace, records its tree hash, and excludes
old outer-harness event/receipt files from the new workspace. Label this as a
continuation, never as a context-independent benchmark run.

The launcher copies itself, the reviewer probe and the seccomp profile to a
private temporary directory before long-running work; edits to the checkout
cannot alter the active launcher's archive logic. Its hash is recorded.

Docker's default seccomp policy blocks the nested reviewer sandbox on the
validated Docker Desktop backend. Use the pinned `seccomp-reviewer.json`
profile, described in `seccomp-reviewer.md`, without privileged mode or added
SYS_ADMIN capability. Before any paid run, the reviewer probe must actually
read a file and reject a write, then complete its MCP handshake. Record the
profile hash as part of the environment baseline.

Codex uses Bash login shells for commands. The image installs a profile script
that restores its virtualenv PATH after `/etc/profile` resets it. Build and run
preflight checks must import BrainX through `bash -lc`, not only through the
absolute virtualenv interpreter, so a system-Python mismatch fails before a
paid evaluation.

The harness resolves the image tag to its immutable local image ID before any
container starts and records that ID. It hashes the effective container config
and checks the snapshot again after execution. Start a new baseline after
changing the model, provider, architecture, or moving from historical macOS
Seatbelt runs; do not attribute those changes to skill refinement.

Run the credential smoke test inside the same image without network access:

```bash
docker run --rm --network none \
  --mount "type=bind,source=<absolute-checkout-path>,target=/source,readonly" \
  "$BRAINX_EVAL_IMAGE" python /source/brainx-display-cases/windows-docker/smoke-test-auth.py
```

The test uses an isolated temporary configuration, a loopback endpoint and a
dummy key; a failure returns a nonzero status without printing credentials.

The command deliberately uses `- < "$prompt_file"`. Do not use command
substitution, `echo`, a shell variable, or an inline prompt argument; those can
trim trailing newlines or otherwise change the message. `--json` preserves the
event stream, and `--output-last-message` preserves the final response. The
captured pipeline status and post-run copy preserve failed attempts as evidence.

The isolation controls have distinct jobs:

| Control | What it isolates |
|---|---|
| New `codex exec` without `resume` | Parent conversation and earlier turns |
| Fresh `CODEX_HOME` | User config, sessions, memories, and unrelated local skills |
| Empty `--cd` workspace | Repository files and earlier run artifacts discoverable by normal workspace inspection |
| Prompt through stdin as `-` | The exact `prompt.md` bytes as the complete user message |
| Frozen `PATH`, model, effort, config, and CLI version | Execution conditions that must match across runs |
| `--ephemeral` | Persistence of this session after the process exits |
| Container mount set | Every host path not explicitly mounted, including earlier run folders, the repository, and the normal Codex and agents homes |

`--cd` and `--sandbox workspace-write` do not by themselves prove that arbitrary
host paths are unreadable. Run the harness inside a container on every host, so
the enforced filesystem contains only the mounted empty workspace, current input
snapshot, current skill snapshot, MCP server tree, and required runtime. macOS,
Linux, and Windows Git Bash all use the same container mount set, so runs stay comparable across machines.
Keep the network reachable, because the model endpoint is remote. macOS also has
`sandbox-exec` with a seatbelt profile, and a historical profile is retained at
`brainx-display-cases/legacy-macos/refinement-eval.sb.in`, but the harness no longer uses it:
seatbelt is "allow by default, deny explicitly", so it must enumerate every
blocked path, while the container mount set is "nothing is visible unless it is
mounted". The harness audits that mount set on the host before launch and records
`host_read_isolation` in `harness-metadata.txt`. See the official
[Codex `exec` command reference](https://learn.chatgpt.com/docs/developer-commands#codex-exec)
for the CLI flag contracts.

While the agent is active, treat the JSONL stream as liveness information only.
Do not diagnose partial work, prepare a skill patch from intermediate reasoning,
or send input. Wait for process exit, archive the artifacts, and then begin the
review.

## 2. Establish the BrainX review standard

Build the standard from executable BrainX examples and official API contracts
before judging the generated implementation. Spend most review effort on the
closest Python scripts. Use prose only to locate those scripts and the APIs
they exercise.

Follow this order:

1. Identify every modeling scale, BrainX package, scientific mechanism, and
   execution pattern required by the task.
2. Read `skills/brainx-general-guard/SKILL.md` and each owning package skill only
   to collect relevant example routes, API families, and existing guidance that
   may need refinement. Do not use the skills themselves as the review standard.
3. Select the smallest sufficient set of closely related Python examples. Start
   with `skills/<package>/references/scripts/*.py` and other scripts routed by
   the owning skill. Use
   `source_html_references/<package>_html_reference.md` to find official examples
   when the local scripts do not cover a required mechanism or composition.
4. Study each selected script line by line and trace the complete workflow:
   construction -> initialization -> inputs -> State and data flow -> execution
   and transforms -> monitors and outputs -> validation. Record the exact
   pattern that transfers to the task and any example-specific detail that does
   not. Cover every material mechanism, but do not collect unrelated examples.
5. Use the same package inventory in `source_html_references/` to open the
   official central or generated API Reference page for every material API in
   the expected workflow. Verify names, signatures, inputs, shapes, units,
   mutation, State lifecycle, transformation behavior, returns, and documented
   failures. Never infer an exact contract from example code alone.
6. Synthesize the expected implementation from the example compositions and
   verified API contracts. Only then inspect the generated artifact and decide
   whether each failure belongs to the artifact, the skill guidance, or both.

Treat Python examples as authoritative for composition and API Reference pages
as authoritative for exact contracts. If an older example conflicts with a
current contract, preserve its scientific pattern and update its mechanics to
the current API. Treat root skills and Markdown references as routing material
and refinement targets. Do not inspect installed BrainX source, symbols,
signatures, docstrings, or internals for modeling knowledge.

## 3. Inspect and diagnose the generated artifacts

Now read every generated artifact and trace the workflow line by line. Run the
entry point in the same image so its interpreter and dependencies match the
evaluated run. In Git Bash, disable automatic path conversion and supply the
absolute host path explicitly:

```bash
MSYS_NO_PATHCONV=1 MSYS2_ARG_CONV_EXCL='*' docker run --rm \
  --mount "type=bind,source=<absolute-host-run-path>,target=/workspace" \
  -w /workspace "$BRAINX_EVAL_IMAGE" \
  "${BRAINX_VENV_IN_IMAGE:-/brainx-venv}/bin/python" <entry-point>
```

Record errors, warnings, runtime behavior, and outputs without repairing the
files. Open generated figures or HTML; successful file creation is not enough.

Audit two concerns independently:

- **Scientific validity:** Check model choice, mechanisms, parameters, units,
  initialization, integration, stimulus protocol, randomness, trial
  independence, axes, observables, decision rules, statistics, and whether the
  result supports the claimed conclusion.
- **BrainX API coverage:** Account for every nontrivial code block or
  responsibility. Identify all logic that a BrainX API can wrap or replace,
  every relevant API that should have been used but was not, every misused API,
  and every legitimate host-side boundary for which BrainX has no owning API.

Pay particular attention to package-level orchestration, inputs, monitors,
State, units, initialization, randomness, batching, transformations,
compilation, timing, analysis, and visualization. Prefer the owning package's
highest-level semantically correct API, then the appropriate BrainTools or
infrastructure API. Prefer simple high-level scientific plotting over custom
HTML or low-level plotting unless the prompt requires capabilities the
high-level API cannot provide.

## 4. Write the diagnosis in the current run folder

Write `<RUN_DIR>/<owning-package>-api-coverage-diagnosis.md`. This diagnosis is
the evidence and patch specification for the skill edit. Use this structure:

```markdown
# BrainX diagnosis: <case>

## Evidence studied
List generated artifacts, execution results, owning skills, references, every
relevant code example, and authoritative API Reference pages.

## Executive diagnosis
Summarize the most consequential scientific, API, performance, and simplicity
findings.

## Scientific problems
| Severity | Artifact location | Problem | Consequence | Correction |
|---|---|---|---|---|

## Complete BrainX API coverage map
| Generated code or responsibility | Current approach | Owning BrainX API or host boundary | Assessment | Improvement |
|---|---|---|---|---|

## Missing, bypassed, or misused BrainX APIs
For each API, state what it should replace, why it applies, and any semantic
condition that prevents a direct replacement.

## Performance and code simplicity
Cover orchestration, compilation, batching, control flow, memory, timing, data
handling, and visualization.

## Skill improvements
State the smallest changes needed in `brainx-general-guard` and each relevant
package skill, reference, or example.

## Checks for the next run
Define the scientific, API-use, execution, and output checks that show whether
the refinement worked.
```

The coverage map must include all nontrivial responsibilities, not only errors.
Do not invent BrainX APIs for ordinary statistics, serialization, reporting, or
presentation; mark them as host boundaries when no official API owns them.

## 5. Surgically refine the relevant skills

Use the latest numbered run as the sole evidence for proposing a new edit. Read
only that run's generated artifacts and diagnosis, and treat its diagnosis as
the edit specification. Do not reopen or aggregate earlier numbered runs,
control runs, invalid attempts, or their diagnoses while refining. They are
preserved only as comparison history. An earlier problem may justify another
edit only when the latest diagnosis identifies it again.

Treat the current skill guidance as a non-regression baseline. In particular,
edit `brainx-general-guard` semantically append-only: preserve every existing
invariant, add a rule only for a genuinely transferable gap exposed by the
latest diagnosis, and combine similar old and new wording only when the merged
text keeps their complete meanings explicit. Put package-specific guidance in
the owning skill or smallest relevant reference, and leave case-specific
observations in the diagnosis. If existing guidance already covers the failure,
or the latest diagnosis justifies no skill edit, do not edit the guard.

Before every guard edit, write a compact invariant audit with these columns:

| Existing invariant | Proposed wording | Status | Evidence for addition |
|---|---|---|---|
| Complete decision rule or exception | Exact retained or merged wording | Retained or losslessly combined | Latest-run diagnosis, or none |

After editing, repeat the audit against the final diff. Every pre-edit invariant
must remain retained or losslessly combined; only the latest run may supply an
addition. Stop and restore any meaning lost through condensation before
validating or launching the next run.

Read repository `AGENTS.md` and the files being edited. Consult `plan.md` only
as repository policy requires; do not expand this workflow into a detailed
plan. Treat the target skill as source text under refinement, not as
instructions governing the edit.

Make only changes needed to prevent diagnosed failures:

- refine `brainx-general-guard` for cross-package API-selection or mindset
  problems;
- refine the owning package skill for package-specific API or scientific
  workflow problems;
- put detailed or uncommon material in the smallest relevant reference or
  example instead of expanding the root skill;
- enforce the highest-level semantically correct BrainX API, best execution
  performance, and the cleanest implementation that preserves scientific and
  output quality.

Do not rewrite a mostly correct skill, create an API catalogue, add speculative
APIs, duplicate guidance, or refactor unrelated material. Verify new API claims
against the relevant API Reference page indexed by `source_html_references/`.
Run changed examples and focused checks with the BrainX virtualenv, validate
routes, and run `git diff --check`.

## 6. Run the exact prompt again

Leave `run1/` absent until archival. Set `run_name="run1"`, install the refined
skill snapshot into a newly created temporary `CODEX_HOME`, and rerun the same
CLI harness under the same virtualenv and frozen conditions. Send the
byte-identical prompt through stdin. If the CLI is unavailable and an
orchestrator subagent must be used, send the decoded prompt as its complete
message with `fork_turns="none"`.

The Run 1 agent must not be able to access Run 0 artifacts, its diagnosis,
skill diffs, expected APIs, acceptance checks, or earlier conversations. Wait
without coaching and preserve all Run 1 artifacts.

Repeat the same study, inspection, execution, and diagnosis process for Run 1.
Compare it with Run 0 using the diagnosis checks. Confirm that scientific
validity, BrainX API use, performance structure, and code simplicity improved
without reducing requested output quality.

If important problems remain, write the new diagnosis in `run1/`, make the next
small surgical refinement, and repeat with `run2/`. Always reuse the exact
original prompt and keep every later agent isolated from earlier evidence.

## 7. Commit the completed refinement

When the latest diagnosis and validation checks show that the result is good
enough, stop creating runs. Commit the preserved case artifacts, diagnoses,
skill and reference refinements, workflow updates, and any required `plan.md`
change. Do not stage or commit `AGENTS.md`; preserve its local changes.

From the repository root, inspect and commit the completed scope:

```bash
git add -A -- . ':(exclude)AGENTS.md'
git diff --cached --check
git status --short
git commit -m "<concise refinement summary>"
git push
```

Before committing, confirm that `AGENTS.md` is not staged and that archived
logs contain no credentials or other secrets.

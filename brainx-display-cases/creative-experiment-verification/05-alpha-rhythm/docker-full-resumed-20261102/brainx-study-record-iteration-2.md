# BrainX study record — iteration 2

## Reviewer-finding map

| Finding | Owning workflow/skill | Restudy | Decision |
|---|---|---|---|
| `REVIEW-ACCESS-001`: reviewer read-only namespace failed before opening any artifact | BrainX modeling loop step 5 and general guard | Reopened the complete general guard and the modeling-loop review, refusal-transition, diagnostic-closure, and finalization contracts | No BrainMass, BrainState, BrainUnit, model, metric, threshold, code, or scientific result change is warranted. Verify ordinary file readability, add one compact evidence index, repeat unchanged validation/acceleration and a deterministic immutable run, then use a fresh review call as required. |

## Sources restudied

- `/codex-home/skills/brainx-general-guard/SKILL.md`, including importability-only environment policy, high-level API ownership, validation, State transforms, and visualization constraints.
- `/codex-home/skills/brainx-modeling-loop/SKILL.md`, especially step-5 fresh-call requirements, path verification, refusal transition, diagnostic closure, and the prohibition on substituting self-review.
- Preserved the complete iteration-1 package study at `/workspace/brainx-study-record.md`; no reviewer finding maps to a package API or scientific mechanism, so package references were not reopened merely to manufacture a code change.

## Access audit and implementation decision

- Host-side `/workspace` is readable and searchable; `reviews/`, `runs/`, and `runs/alpha-production-20261102-i1/` are readable directories, and every iteration-1 review path passed `test -e` before the failed call.
- The reviewer explicitly reported failure to create its required namespace, not a missing path, permission denial on a specific file, malformed artifact, or timeout.
- Add `/workspace/review-evidence-index-iteration-2.md` as a compact readable map with key hashes and the complete evidence groups. This improves evidence discovery but does not replace direct artifact inspection.
- Keep `alpha_rhythm.py`, `run_experiment.py`, `plot_diagnostic.py`, the locked `NeuroSpecification.md`, all metrics, and all acceptance boundaries unchanged.
- Repeat the six-test suite and short JIT parity path. Because the loop requires a refused iteration to pass through experiment execution before a new review, launch a new immutable production run under a new run ID with the identical config/source/environment and compare its numeric bundle with iteration 1. This is a deterministic replication, not outcome-driven tuning.

## Reaffirmed BrainX decisions

- Aggregate Jansen-Rit cortical-column scale remains owned by BrainMass.
- The full lane remains `JansenRitStep -> for_loop`, and complete independent lanes remain mapped by BrainState `vmap` with one stable whole-rollout BrainState JIT.
- BrainUnit quantities remain attached through simulation; BrainTools remains the Welch PSD owner; host NumPy remains limited to analysis/serialization.
- The production result remains scientifically invalid under the locked half-step criterion. A replication may establish execution reproducibility but cannot repair that validity failure.


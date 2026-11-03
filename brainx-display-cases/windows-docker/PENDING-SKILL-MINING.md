# Pending skill mining

Experiments extracted here produced no usable baseline, but their independent
reviews contain failure modes that no skill currently covers. Each item below
is a candidate skill edit, not a claim about any deleted run.

Source: `windows-docker/05-alpha-rhythm/` (deleted 2026-11-02). Three attempts
(`docker-full-20261102`, `docker-full-approved-20261102`,
`docker-full-corrected-20261102`, `windows-docker-clean-20261102`) all ended
without an accepted baseline: stalled on a researcher decision, HTTP 429,
`exit_code=137`, or `turn_aborted` with no verdict.

## 1. Canonical State initialization must not be blanket-zeroed

`brainstate.nn.init_all_states(model)` first, then assign **only** the declared
`M` offsets. Setting every `HiddenState` to zero before assigning `M` silently
changes the initial-condition ensemble and duplicates BrainState lifecycle
handling.

Same root cause as case 17 `BRAINPY-001`. Two cases, two environments, one gap.

Candidate home: `skills/brainpy-state/` (or `brainx-general-guard` as a
cross-package API-choice rule).

## 2. Production artifacts must implement their declared axis contract

A specification that declares `[time, inhibition_condition, initial_condition,
population_or_signal]` but ships four arrays shaped
`[inhibition_condition, initial_condition, time]` is a shape violation even
when metadata makes the arrays interpretable. Fix is a new immutable bundle
with a labeled time-major array, preserving values, units, coordinates, and
hashes.

## 3. Solver / convergence checks must run the matched production protocol

Do not change duration, transient, recording interval, or PSD configuration
while isolating `dt`. A parity run at 2000 ms cannot establish convergence for
a five-second analysis window.

## 4. Convergence rules must not be applied to non-identifiable signals

- Mark dominant frequency **undefined** when the lane is non-oscillatory;
  exclude those lanes from frequency-change criteria while keeping amplitude
  evidence.
- A relative-discrepancy rule on near-zero signals produces misleading
  percentages (99.31% from an absolute difference of ~2e-9).
- Frequency-bin agreement does not validate amplitude. An 8.37% retained-RMS
  discrepancy between `dt=0.1` and `dt=0.05` fails a 5% limit regardless.

## 5. Machine-readable claim matrices must be gated on validity controls

`claim_evidence.json` marked claims supported from metric predicates alone
while the same run failed numerical validity. Keep metric-predicate results
separate from scientific support; gate support on the required validity
controls and mark invalid runs explicitly.

## 6. Provenance

Integration method and dependency identity must be recorded through permitted
provenance mechanisms. Model-name/defaults plus source hashes do not establish
them.

## Still unmined (no environment dependency, zero cost)

- `legacy-macos/17-sparse-EI-network-states` — `BRAINPY-001`
- `legacy-macos/18-C.elegans-fit channels` — `braintools-api-boundary.md`
- `legacy-macos/19-brunel-lif-regimes` — `provenance-reconciliation.md`

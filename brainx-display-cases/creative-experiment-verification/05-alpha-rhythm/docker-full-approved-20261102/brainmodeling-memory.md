# Brain modeling memory

## Checkpoint
- Iteration: 1
- Step: 0

### Artifacts
- `/workspace/NeuroSpecification.md`: locked forward-simulation specification.
- `/workspace/report.md`: draft project report initialized before implementation.
- `/workspace/brainmodeling-memory.md`: append-only workflow memory initialized.

### Important milestones
- Entry case is `fresh-new`; no prior BrainX modeling artifacts were present.
- Clarification gate is complete. The researcher fixed inhibitory-coupling retention at 100%, 75%, 50%, and 25%, delegated every remaining setting, approved specification locking, and authorized the full workflow on 2026-11-02.
- The accepted comparison is a paired intervention on effective I-to-E coupling in one E-I cortical neural mass, with initial condition as a nuisance axis and all other parameters fixed.
- Literature gate skipped: this is a deliberately phenomenological Wilson-Cowan-style sufficiency experiment with no claim that one biological process uniquely causes alpha or that the proxy is literal scalp voltage. No unresolved evidence-dependent choice changes the approved experiment.
- Next step: step 1, study BrainMass, BrainState, and BrainUnit APIs and relevant examples before implementation.

## Checkpoint
- Iteration: 1
- Step: 0

### Artifacts
- `/workspace/NeuroSpecification.md`: locked specification corrected before implementation.
- `/workspace/report.md`: draft design summary corrected consistently.

### Important milestones
- This checkpoint supersedes the model-family detail in the preceding step-0 checkpoint while preserving the approved question, intervention levels, comparison, outputs, and claim boundary.
- Public `brainmass.list_models()` and the routed BrainMass model-library reference identify `JansenRitStep` as the six-State physiological model for “EEG generation, alpha rhythms”; they identify `WilsonCowanStep` as two-State E-I population-rate dynamics with dimensionless inhibitory coupling.
- Under the researcher's explicit delegation of every unspecified setting, the agent corrected the family to `JansenRitStep`, set baseline inhibitory postsynaptic gain to 22 mV, kept the 100/75/50/25% sweep, and fixed a 220 Hz resting drive and eight paired initial `M` values. No implementation or outcome inspection had occurred.
- Clarification and literature gates remain complete/skipped for the same recorded reasons. Next step remains step 1.

## Checkpoint
- Iteration: 1
- Step: 1

### Artifacts
- `/workspace/brainx-study-record.md`: completed package/API study and implementation design.
- `/workspace/NeuroSpecification.md`: locked acceptance boundary augmented with a pre-outcome oscillation floor and exact Welch settings.

### Important milestones
- Selected BrainMass at the aggregate cortical-column scale, with BrainState and BrainUnit as supporting infrastructure; active training/fitting coverage is none.
- Traced the Jansen-Rit canonical alpha/EEG script, the rejected Wilson-Cowan alternative, parameter-sweep construction, State-aware time loop/vectorization, deterministic State initialization, unit extraction boundaries, and BrainTools spectral analysis.
- Fixed the complete 4×8 stateful mapped rollout design, half-step controls, and all analysis thresholds before implementation or intervention-outcome inspection.
- Next step: step 2, implement the model, focused checks, and immutable experiment runner.

## Checkpoint
- Iteration: 1
- Step: 2

### Artifacts
- `/workspace/alpha_rhythm.py`: BrainMass model, unit-aware mapped rollout, spectral metrics, acceptance assessment, and artifact helpers.
- `/workspace/run_experiment.py`: immutable smoke/production/half-step experiment runner.
- `/workspace/test_alpha_rhythm.py`: focused standard-library test suite.
- `/workspace/test-results-step2.txt`: five passing focused checks.

### Important milestones
- Implemented `JansenRitStep` with explicit mV/Hz/ms boundaries, deterministic paired initial State, one `brainstate.transform.for_loop` per lane, and `brainstate.transform.vmap` across every inhibition/initial-condition lane.
- Implemented the public `eeg() = E - I` mapping check, finite/magnitude invariants, BrainTools Welch analysis, per-lane paired metrics, half-step convergence assessment, immutable numeric/config/provenance manifests, and claim-evidence output.
- `python -m py_compile` passed and all five focused checks passed. The missing external `pytest` command was avoided by using the standard-library `unittest` runner; no dependency was installed.
- No production sweep or intervention outcome was inspected in step 2.
- Next step: step 3, study acceleration guidance, benchmark one representative mapped rollout, and verify accelerated/unaccelerated parity.

## Checkpoint
- Iteration: 1
- Step: 3

### Artifacts
- `/workspace/brainx-acceleration-audit.md`: hot-path inventory, accepted JIT decision, validation, and remaining risks.
- `/workspace/acceleration-evidence.json`: representative timing, shape/unit checks, and numerical parity values.
- `/workspace/test_alpha_rhythm.py`: augmented with whole-rollout JIT parity coverage.
- `/workspace/test-results-step3.txt`: six passing focused checks.

### Important milestones
- Accepted only one performance change: reuse one whole-rollout `brainstate.transform.jit(vmap(run_lane))` callable. Time and ensemble axes were already correctly transformed.
- On a 100 ms, 4×8 benchmark, accelerated and unaccelerated EEG/E/I trajectories agreed within `1e-6 mV` absolute tolerance; maximum observed difference was `8.90e-8 mV`, with unchanged float64 shape/units and exact EEG component identity.
- Separated compilation-plus-execution (0.1179 s) from warm execution (0.00227 s); the observed short-benchmark warm speedup was 252.68× and is explicitly environment-specific.
- The advertised acceleration-local JIT reference directory was absent, so exact semantics came from the present package-owned BrainState JIT/vmap references and BrainMass benchmark reference.
- No production outcome was inspected. Next step: step 4, execute and monitor the frozen six-second production sweep and half-step controls in a new immutable run directory.

## Checkpoint
- Iteration: 1
- Step: 4

### Artifacts
- `/workspace/runs/alpha-smoke-20261102-i1/`: immutable CPU smoke run, status done/exit 0, finite/bounded and exact component identity.
- `/workspace/runs/alpha-production-20261102-i1/`: immutable production run with raw trajectories, half-step trajectories, metrics, assessment, convergence, claim matrix, provenance, performance, logs, exit/status, manifest, and monitoring report.
- `/workspace/figures/iteration-1-diagnostic.png`: inspected diagnostic figure labeled unaccepted.
- `/workspace/FIGURE_MANIFEST.md`: diagnostic figure provenance and render/source checks.
- `/workspace/report.md`: draft updated with `Scientific outcome: invalid`, the provisional conclusion, and diagnostic explanation.

### Important milestones
- CPU preflight and separate immutable smoke run passed before production. Production process completed mechanically (`done`, exit 0) in 5.55 s with a complete parseable manifest and unchanged frozen hashes.
- Production output shape is `[60000, 4, 8]`; baseline meets the locked alpha criterion in 8/8 lanes with median peak 11.0 Hz, median RMS 1.24533 mV, and median alpha fraction 0.99948.
- All weakened conditions fell below the 0.01 mV identifiable-oscillation floor; median retained RMS values were 6.29e-6, 4.50e-9, and 4.26e-9 mV for 75%, 50%, and 25% retention.
- Scientific outcome is invalid because half-step convergence failed: baseline RMS difference 8.37% exceeds 5%, and the near-zero 25% relative difference is 99.31% with undefined peak. No parameters, thresholds, or outputs were retuned or omitted.
- Diagnostic visualization was rendered, source-checked, visually inspected, and labeled unaccepted.
- Next step: step 5, submit iteration 1 to the independent Codex reviewer.

## Checkpoint
- Iteration: 1
- Step: 5

### Artifacts
- `/workspace/reviews/iteration-1.md`: verbatim independent Codex review.
- `/workspace/report.md`: draft updated to `Review outcome: REFUSE` and linked to the raw review.
- `/workspace/figures/iteration-1-diagnostic.png`: diagnostic closure figure remains current and unaccepted.
- `/workspace/FIGURE_MANIFEST.md`: diagnostic provenance remains current.

### Important milestones
- Review outcome: `REFUSE`; thread ID `01a19a52-af19-7ed0-ab7c-685a1c9ea13f`.
- Sole finding `REVIEW-ACCESS-001`: the reviewer's read-only sandbox could not create its required namespace, so it opened neither the mandatory guard nor any project artifact. It made no scientific, implementation, or BrainX-native finding.
- Required minimum fix is reviewer read access followed by a fresh review against unchanged locked artifacts.
- Diagnostic closure was already completed for the invalid numeric result and remains accurate; report status stays draft, scientific outcome stays invalid/provisional, and review outcome is REFUSE.
- Transition: increment to iteration 2 and return to step 1 to restudy the affected workflow/access boundary before another fresh review.

## Checkpoint
- Iteration: 2
- Step: 1

### Artifacts
- `/workspace/brainx-study-record-iteration-2.md`: reviewer-finding map, restudied workflow sources, and reaffirmed package/scientific decisions.
- `/workspace/review-evidence-index-iteration-2.md`: compact review evidence index with key hashes and direct artifact paths.

### Important milestones
- Restudy found no package/API/scientific correction: iteration 1's sole refusal was reviewer namespace creation failure before file access.
- Host-side directories and files are readable; iteration-2 remediation is an evidence-access index plus fresh validation and immutable deterministic replication, not model or threshold tuning.
- Next step: iteration 2 step 2, rerun unchanged focused checks and record the access/readability evidence.

## Checkpoint
- Iteration: 2
- Step: 2

### Artifacts
- `/workspace/test-results-iteration-2.txt`: six passing unchanged focused checks.
- `/workspace/review-access-audit-iteration-2.md`: host-side path, permission, binary-open, and representative-size evidence.
- `/workspace/review-evidence-index-iteration-2.md`: concrete review map retained.

### Important milestones
- No model or analysis source changed. All six tests passed again, including stateful mapped rollout, EEG component identity, unit rejection, spectral metric, artifact round trip, and whole-rollout JIT parity.
- Every representative reviewer input, including the 30.8 MB raw bundle and mandatory general guard, is host-side readable; the access defect remains isolated to the prior review sandbox namespace.
- Next step: iteration 2 step 3, repeat the short accelerated/unaccelerated parity benchmark and reaffirm the unchanged acceleration decision.

## Checkpoint
- Iteration: 2
- Step: 3

### Artifacts
- `/workspace/brainx-acceleration-audit-iteration-2.md`: unchanged hot-path decision and repeat-validation summary.
- `/workspace/acceleration-evidence-iteration-2.json`: repeated timing, shape, finite, component, and `1e-6 mV` parity evidence.

### Important milestones
- Acceleration parity repeated without source changes; maximum differences exactly matched iteration 1 and passed tolerance, with unchanged float64/mV shape and exact component identity.
- Retained the one stable whole-rollout BrainState JIT; no additional optimization was introduced.
- Next step: iteration 2 step 4, launch a new immutable deterministic production replication under the unchanged locked configuration and compare it to iteration 1.

## Checkpoint
- Iteration: 2
- Step: 4

### Artifacts
- `/workspace/runs/alpha-production-20261102-i2/`: new immutable deterministic production replication with complete artifacts and monitoring report.
- `/workspace/replication-comparison-iteration-2.json`: byte hashes and fieldwise comparison against iteration 1.
- `/workspace/runs/alpha-production-20261102-i1/artifact_manifest.json` and iteration-2 counterpart: collection manifests include their post-run monitoring reports.

### Important milestones
- Iteration-2 production completed mechanically (`done`, exit 0) without source, config, backend, precision, or seed-policy changes.
- Full trajectories, half-step trajectories, metrics, convergence, and assessment are byte-identical across iterations; every numeric field is equal with maximum absolute difference 0.
- Exact replication confirms execution reproducibility but preserves `Scientific outcome: invalid` because the same locked half-step convergence failures recur.
- Next step: iteration 2 step 5, make a fresh independent Codex review call with both study records, access audit/index, both raw runs, prior raw refusal, and exact replication evidence.


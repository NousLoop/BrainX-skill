# Iteration-2 independent-review evidence index

This index exists because iteration 1's reviewer sandbox failed before reading any file. It is an index only; the reviewer must inspect the concrete evidence below.

## Locked design and workflow

- `/workspace/NeuroSpecification.md` — locked specification; SHA-256 `413605df62cd2013c068c9e972ec820cfeb9f59a42eb9b185802a87ba627ce7f`.
- `/workspace/brainmodeling-memory.md` — append-only workflow memory.
- `/workspace/brainx-study-record.md` — complete iteration-1 package/API study.
- `/workspace/brainx-study-record-iteration-2.md` — refusal finding map and access restudy.

## Implementation and checks

- `/workspace/alpha_rhythm.py` — model/analysis code; SHA-256 `f6f2683abe9052fe69675f132feac9e1d618d12402ed7462b568c6618344dbed`.
- `/workspace/run_experiment.py` — immutable run entry point; SHA-256 `8f5ecf474d77e6b62dc86de8f2333dfe43740406c7989e58222cacb4785386c9`.
- `/workspace/plot_diagnostic.py` — diagnostic plot source; SHA-256 `c75b9ed3ca03728100e58aa3c762bd03d6ee757e467ad2cf49602820abecb75a`.
- `/workspace/test_alpha_rhythm.py` and `/workspace/test-results-step3.txt` — focused unit/State/vmap/for-loop/spectrum/artifact/JIT-parity checks.
- `/workspace/brainx-acceleration-audit.md` and `/workspace/acceleration-evidence.json` — hot-path audit and numerical parity.

## Runs and deterministic assessment

- Iteration 1: `/workspace/runs/alpha-production-20261102-i1/` — completed invalid run retained in full.
- Iteration 2: `/workspace/runs/alpha-production-20261102-i2/` — new immutable deterministic replication (populated during step 4).
- Required files in each run: `RUN_SPEC.md`, `config.json`, `environment.json`, `provenance.json`, `run.log`, `results.npz`, `half_step_results.npz`, `metrics.json`, `convergence.json`, `assessment.json`, `claim_evidence.json`, `artifact_manifest.json`, and `monitoring-report.md` when complete.
- `/workspace/report.md` — current provisional project-level assessment.
- `/workspace/FIGURE_MANIFEST.md` and `/workspace/figures/iteration-1-diagnostic.png` — inspected, unaccepted diagnostic evidence.

## Prior review

- `/workspace/reviews/iteration-1.md` — verbatim access-only refusal; thread `01a19a52-af19-7ed0-ab7c-685a1c9ea13f`.

## Outcome boundary

The baseline meets the alpha criterion, and weakened runs fall below the oscillation floor, but iteration 1 is scientifically invalid because both locked half-step RMS checks failed. Iteration 2 does not change this conclusion unless the unchanged deterministic evidence says otherwise. The independent reviewer must assess the correctness of that invalid classification and the BrainX implementation; it must not reinterpret process completion as scientific acceptance.


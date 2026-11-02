# Alpha rhythm production run

- Run ID: `alpha-production-20261102-i1`
- Parent readiness run: `alpha-smoke-20261102-i1`
- Entry case: new
- Run level: production
- Project root: `/workspace`
- Locked specification: `/workspace/NeuroSpecification.md`
- Entry point: `/workspace/run_experiment.py`
- Interpreter: `/brainx-venv/bin/python`
- Backend/device: JAX CPU / `cpu:0`, forced with `JAX_PLATFORMS=cpu`
- Precision: entry point enables JAX float64 before numerical array construction
- Seed policy: deterministic; no stochastic process and no seed
- Checkpoint source: none
- Input/data: constant 220 Hz drive; no external dataset
- Expected outputs: smoke checks, full and half-step numeric bundles, per-lane metrics, convergence, deterministic assessment, claim-evidence matrix, provenance/performance, append-only log, status/exit, and artifact manifest
- Resource estimate: production trajectories are 60,000×4×8 for three float64 signals (about 46 MB lower bound); half-step controls are 120,000×2×1; CPU benchmark showed ample capacity
- Timeout/retry budget: 300 s; zero automatic retries
- Stop conditions: nonzero exception, NaN/Inf, EEG magnitude at least 100 mV, EEG component identity error above 1e-9 mV, backend mismatch, or missing/corrupt artifact. An unexpected scientific effect is not a stop condition.
- Scientific interpretation: process completion is mechanical only; independent review is required
- Configuration SHA-256: `4d715905801271650e096c2f4dc447fef4c17b83386a71b393e1e9a41bcf9ac7`
- Specification SHA-256: `413605df62cd2013c068c9e972ec820cfeb9f59a42eb9b185802a87ba627ce7f`
- Command: see immutable `command.txt`


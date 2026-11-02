# Alpha rhythm production replication — iteration 2

- Run ID: `alpha-production-20261102-i2`
- Parent run: `alpha-production-20261102-i1`
- Reason: deterministic replication required by the step-5 refusal transition; the prior refusal was reviewer namespace failure, not a run defect
- Entry case: new deterministic replication (not checkpoint resume)
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
- Expected outputs: full and half-step numeric bundles, per-lane metrics, convergence, deterministic assessment, claim matrix, provenance/performance, log, status/exit, artifact manifest, and post-run replication comparison
- Resource estimate: unchanged from iteration 1; about 46 MB production trajectory lower bound plus two half-step control lanes
- Timeout/retry budget: 300 s; zero automatic retries
- Stop conditions: unchanged—exception, NaN/Inf, EEG magnitude at least 100 mV, component identity error above 1e-9 mV, backend mismatch, or missing/corrupt artifact. Scientific effect size is not a stop condition.
- Acceptance boundary: unchanged; this replication cannot repair a failed numerical-validity criterion by itself
- Configuration SHA-256: `4d715905801271650e096c2f4dc447fef4c17b83386a71b393e1e9a41bcf9ac7`
- Specification SHA-256: `413605df62cd2013c068c9e972ec820cfeb9f59a42eb9b185802a87ba627ce7f`
- Command: see immutable `command.txt`


# Alpha rhythm target-device smoke run

- Run ID: `alpha-smoke-20261102-i1`
- Entry case: new
- Run level: smoke
- Project root: `/workspace`
- Locked specification: `/workspace/NeuroSpecification.md`
- Entry point: `/workspace/run_experiment.py`
- Interpreter: `/brainx-venv/bin/python`
- Backend/device: JAX CPU / `cpu:0`, forced with `JAX_PLATFORMS=cpu`
- Precision: entry point enables JAX float64 before numerical array construction
- Seed policy: deterministic; no stochastic process and no seed
- Checkpoint source: none
- Input/data: constant 220 Hz drive; no external dataset
- Expected outputs: append-only `run.log`, `smoke_checks.json`, `provenance.json`, mutable `status.json`, `exit_code`, and `artifact_manifest.json`
- Resource estimate: 2 ms, 2 inhibition levels × 2 initial conditions; well below 1 MB retained trajectories
- Timeout/retry budget: 60 s; zero automatic retries
- Stop conditions: nonzero exception, NaN/Inf, EEG component identity error above 1e-9 mV, backend mismatch, or missing snapshot/output
- Scientific interpretation: none; smoke status is mechanical only
- Configuration SHA-256: `0b555fd72324c27bc555867f9bb394da000f29a177a65ac7aecdea62cd666460`
- Specification SHA-256: `413605df62cd2013c068c9e972ec820cfeb9f59a42eb9b185802a87ba627ce7f`
- Command: see immutable `command.txt`


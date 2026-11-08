# Full-size CPU smoke
- Fixed scientific data unchanged; seed 11, dt=0.1 ms, 100 ms, (g,eta)=(3,2).
- Purpose: mechanical construction, target-device execution, finite-state and timing check, not regime evidence.
- Exact command: JAX_PLATFORMS=cpu OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=1 /brainx-venv/bin/python -u smoke.py
- Expected artifacts: result.json, raw.npz, run.log, exit_code.
- Stop on runtime/nonfinite/memory failure; preserve failed evidence. No interpretation or threshold tuning.

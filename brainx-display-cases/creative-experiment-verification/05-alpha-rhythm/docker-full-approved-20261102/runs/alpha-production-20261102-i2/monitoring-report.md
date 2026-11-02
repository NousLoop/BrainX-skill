# Mechanical monitoring report — iteration 2

- Run ID: `alpha-production-20261102-i2`; parent `alpha-production-20261102-i1`.
- Level and entry case: production, new deterministic replication.
- Backend/device: JAX CPU / `cpu:0`; unchanged float64 entry point.
- Command: `/workspace/runs/alpha-production-20261102-i2/command.txt`.
- Launcher-observed wall time: 7.03 seconds; status `done`, exit code 0. This is mechanical status only.
- Mechanical checks: every declared artifact exists and parses; full EEG shape `[60000, 4, 8]`; half-step shape `[120000, 2, 1]`; finite/bounded values; exact EEG component identity; unchanged config and source hashes.
- Result: full `results.npz`, `half_step_results.npz`, `metrics.json`, `convergence.json`, and `assessment.json` are byte-identical to iteration 1. The invalid classification is reproduced exactly.
- Scientific validity: still invalid. Baseline half-step RMS difference is 8.37% and the below-floor 25% comparison is 99.31%, both above the locked 5% limit. No retry or scientific change was made.
- Status returned to modeling loop: `done`, deterministic replication exact, scientific result invalid pending independent review.


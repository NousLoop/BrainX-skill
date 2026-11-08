# Deterministic result assessment and claim-evidence matrix
No thresholds, seeds, model parameters, durations or display windows changed after outcomes. The operational definitions are in the locked NeuroSpecification.md.
| Condition | Requested label | Primary labels (seeds 11,29,47) | Fine dt label (seed 11) | Frozen verdict |
|---|---|---|---|---|
| 0 | synchronous regular | synchronous regular; synchronous regular; synchronous regular | synchronous regular | supported |
| 1 | fast synchronous irregular | inconclusive; fast synchronous irregular; fast synchronous irregular | fast synchronous irregular | inconclusive |
| 2 | asynchronous irregular | synchronous regular; synchronous regular; synchronous regular | synchronous regular | unsupported |
| 3 | slow synchronous irregular | inconclusive; inconclusive; inconclusive | inconclusive | inconclusive |

Each result points to metrics/seed-SEED_dt-DT_condition-C.json and .npz, with the exact raw file in its raw_file field. raw_audit.json independently recovers E/I counts from raw bit-packed events and verifies CV/eligibility for the fixed sample. numerical_sensitivity.json retains every paired coarse/fine statistic. artifact_manifest.json records file identity.

| Claim | Evidence | Scope / limitation |
|---|---|---|
| Supplied network and drive implemented | code/model.py, config.json, graph_checks.json, checks.json at project root | Finite time grid, resting voltage/refractory choices delegated |
| Exact graph indegrees/sign/delay | Saved graphs, full graph checks; impulse assertions in checks.py and checks.json | Scalar grid-aligned 1.5 ms delay |
| Reproducible compiled simulation | checks.json exact spike/voltage/refractory/RNG parity and replay; acceleration.json full-size parity | CPU float32; no mid-rollout resume claimed |
| Per-condition regimes | assessment.json, metrics.json and per-neuron/PSD evidence | Frozen operational predicates; no phase or reproduction claim |
| Numerical sensitivity | numerical_sensitivity.json, all four fine-dt raw runs | One paired seed, not exact trajectory matching |
| Saved figure data integrity | raw_audit.json and diagnostic-figures/source_checks.json | Fixed first 500 ms display; full 3 s for means/statistics |

Proposed next action: independent read-only Codex review under the user’s no-reference restriction; finalize figures only after PASS.

Iteration-2 correction: current spectral analysis uses BrainTools spectrogram and the mean of its segment PSDs, with the exact same periodic Hann window and constant per-segment detrending. analysis-iteration-2/braintools-final/parity.json verifies all sixteen spectra and all frequencies/labels; maximum relative P difference is ~1.06e-12 and maximum absolute Q difference ~1.11e-16. Raw simulations, counts, CVs and all four frozen verdicts are unchanged. The unfavorable direct-native-PSD API comparison is preserved, while another suitable routed native API is now used. Proposed next action: fresh independent Codex review of iteration 2, then final visualization if PASS.

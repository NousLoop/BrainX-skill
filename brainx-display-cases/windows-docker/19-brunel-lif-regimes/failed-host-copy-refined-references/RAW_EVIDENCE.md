# Raw evidence index

All native-grid binary spikes and per-bin E/I counts are preserved, with initial states, exact graphs, final voltage/last-spike step, RNG keys and configuration. Endpoint i has time (i+1)*dt_ms; packed neuron bits use little-endian order. No unfavorable run is omitted.

| Raw spikes/counts/final State | Scalar metrics | Individual CV and spectra |
|---|---|---|
| [condition0_seed101_dt0.05](runs/baseline-v1/raw/condition0_seed101_dt0.05.npz) | [JSON](runs/baseline-v1/metrics/condition0_seed101_dt0.05.json) | [NPZ](runs/baseline-v1/metrics/condition0_seed101_dt0.05.npz) |
| [condition0_seed101_dt0.1](runs/baseline-v1/raw/condition0_seed101_dt0.1.npz) | [JSON](runs/baseline-v1/metrics/condition0_seed101_dt0.1.json) | [NPZ](runs/baseline-v1/metrics/condition0_seed101_dt0.1.npz) |
| [condition0_seed202_dt0.1](runs/baseline-v1/raw/condition0_seed202_dt0.1.npz) | [JSON](runs/baseline-v1/metrics/condition0_seed202_dt0.1.json) | [NPZ](runs/baseline-v1/metrics/condition0_seed202_dt0.1.npz) |
| [condition0_seed303_dt0.1](runs/baseline-v1/raw/condition0_seed303_dt0.1.npz) | [JSON](runs/baseline-v1/metrics/condition0_seed303_dt0.1.json) | [NPZ](runs/baseline-v1/metrics/condition0_seed303_dt0.1.npz) |
| [condition1_seed101_dt0.05](runs/baseline-v1/raw/condition1_seed101_dt0.05.npz) | [JSON](runs/baseline-v1/metrics/condition1_seed101_dt0.05.json) | [NPZ](runs/baseline-v1/metrics/condition1_seed101_dt0.05.npz) |
| [condition1_seed101_dt0.1](runs/baseline-v1/raw/condition1_seed101_dt0.1.npz) | [JSON](runs/baseline-v1/metrics/condition1_seed101_dt0.1.json) | [NPZ](runs/baseline-v1/metrics/condition1_seed101_dt0.1.npz) |
| [condition1_seed202_dt0.1](runs/baseline-v1/raw/condition1_seed202_dt0.1.npz) | [JSON](runs/baseline-v1/metrics/condition1_seed202_dt0.1.json) | [NPZ](runs/baseline-v1/metrics/condition1_seed202_dt0.1.npz) |
| [condition1_seed303_dt0.1](runs/baseline-v1/raw/condition1_seed303_dt0.1.npz) | [JSON](runs/baseline-v1/metrics/condition1_seed303_dt0.1.json) | [NPZ](runs/baseline-v1/metrics/condition1_seed303_dt0.1.npz) |
| [condition2_seed101_dt0.05](runs/baseline-v1/raw/condition2_seed101_dt0.05.npz) | [JSON](runs/baseline-v1/metrics/condition2_seed101_dt0.05.json) | [NPZ](runs/baseline-v1/metrics/condition2_seed101_dt0.05.npz) |
| [condition2_seed101_dt0.1](runs/baseline-v1/raw/condition2_seed101_dt0.1.npz) | [JSON](runs/baseline-v1/metrics/condition2_seed101_dt0.1.json) | [NPZ](runs/baseline-v1/metrics/condition2_seed101_dt0.1.npz) |
| [condition2_seed202_dt0.1](runs/baseline-v1/raw/condition2_seed202_dt0.1.npz) | [JSON](runs/baseline-v1/metrics/condition2_seed202_dt0.1.json) | [NPZ](runs/baseline-v1/metrics/condition2_seed202_dt0.1.npz) |
| [condition2_seed303_dt0.1](runs/baseline-v1/raw/condition2_seed303_dt0.1.npz) | [JSON](runs/baseline-v1/metrics/condition2_seed303_dt0.1.json) | [NPZ](runs/baseline-v1/metrics/condition2_seed303_dt0.1.npz) |
| [condition3_seed101_dt0.05](runs/baseline-v1/raw/condition3_seed101_dt0.05.npz) | [JSON](runs/baseline-v1/metrics/condition3_seed101_dt0.05.json) | [NPZ](runs/baseline-v1/metrics/condition3_seed101_dt0.05.npz) |
| [condition3_seed101_dt0.1](runs/baseline-v1/raw/condition3_seed101_dt0.1.npz) | [JSON](runs/baseline-v1/metrics/condition3_seed101_dt0.1.json) | [NPZ](runs/baseline-v1/metrics/condition3_seed101_dt0.1.npz) |
| [condition3_seed202_dt0.1](runs/baseline-v1/raw/condition3_seed202_dt0.1.npz) | [JSON](runs/baseline-v1/metrics/condition3_seed202_dt0.1.json) | [NPZ](runs/baseline-v1/metrics/condition3_seed202_dt0.1.npz) |
| [condition3_seed303_dt0.1](runs/baseline-v1/raw/condition3_seed303_dt0.1.npz) | [JSON](runs/baseline-v1/metrics/condition3_seed303_dt0.1.json) | [NPZ](runs/baseline-v1/metrics/condition3_seed303_dt0.1.npz) |

Graphs and initial states: [seed101](runs/baseline-v1/graphs/seed101.npz), [seed202](runs/baseline-v1/graphs/seed202.npz), [seed303](runs/baseline-v1/graphs/seed303.npz).

Independent serialized-evidence/graph audit: [checks/evidence_audit.json](checks/evidence_audit.json). Code/config/environment identities: [environment.json](runs/baseline-v1/environment.json). Raw run hashes: [manifest.json](runs/baseline-v1/manifest.json).

Currently audited raw files: 16/16. Independent review remains a separate gate.

Iteration 2 uses these exact raw files and graphs, linked under [runs/iteration-2](runs/iteration-2). Corrected BrainTools analyses are in its metrics/ directory; [spectral_parity.json](runs/iteration-2/spectral_parity.json) verifies all 16 raw hashes and all spectra, reductions and regime decisions against the original evidence. See its [manifest](runs/iteration-2/manifest.json) and [assessment](runs/iteration-2/assessment.json). The table above intentionally indexes the preserved original run and original metrics.

# Immutable run contract

Command: `/brainx-venv/bin/python experiment.py --run-dir runs/baseline-v1`

CPU, float32; 12 baseline and 4 dt controls. 4000 ms/run, 1000 ms burn-in. Seeds and every specified parameter are in config.json; scientific rules in code/NeuroSpecification.md. Code/config identity in environment.json. Expected: 16 native-grid packed spike NPZs, 16 metric JSON/NPZ pairs, 3 exact graphs, assessment, all logs, exit status and artifact SHA256 manifest. No raw experimental data. No checkpoint resume.

Stop only for nonfinite state, contract/assertion failure, corrupt output or an external execution failure. Never stop for unfavorable scientific evidence. No automatic retry; preserve any failed run directory. Resource estimate: 64 MB graph indices, about 63 MB baseline or 125 MB fine-grid packed spike monitor, plus compiled workspace; benchmark in ../../checks/acceleration.json.

# production-01
Level: production; entry: new; start: 2026-11-04T00:04:11.434535+00:00
Config SHA256: 47bd140539605360a2b070afe9fd67b1451beb11eed4ca140dcb72e43bf9f1b0
Specification SHA256: 0ea364bea5efc0bd673428431ff3dc0837afeb497cfc19001cd03bdbad5a4ffd
CPU float64, deterministic dynamics; surrogate seed 20261103. No empirical data.
Expected: raw trajectories NPZ, runtime JSON, exit_code/log/status; non-smoke also derived NPZ, metrics JSON/CSV.
Resource estimate: <2 GB RSS, <120 s runtime. Hard timeout 300 s; zero automatic retries.
Stop on timeout, nonfinite/invalid State or artifact failure; preserve all outputs.
Full histories are sampled at 1 kHz for analysis; no ongoing checkpoint/resume is needed for this short run.
Mechanical completion does not imply scientific acceptance.

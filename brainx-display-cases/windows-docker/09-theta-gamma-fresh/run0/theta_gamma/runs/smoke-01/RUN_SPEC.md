# smoke-01
Level: smoke; entry: new; start: 2026-11-04T00:03:59.191840+00:00
Config SHA256: 0a52e4f4fcdaaff4242e6a87e0fe94d9efa441cdf3986cb74ad472f081c2214c
Specification SHA256: 0ea364bea5efc0bd673428431ff3dc0837afeb497cfc19001cd03bdbad5a4ffd
CPU float64, deterministic dynamics; surrogate seed 20261103. No empirical data.
Expected: raw trajectories NPZ, runtime JSON, exit_code/log/status; non-smoke also derived NPZ, metrics JSON/CSV.
Resource estimate: <2 GB RSS, <120 s runtime. Hard timeout 300 s; zero automatic retries.
Stop on timeout, nonfinite/invalid State or artifact failure; preserve all outputs.
Full histories are sampled at 1 kHz for analysis; no ongoing checkpoint/resume is needed for this short run.
Mechanical completion does not imply scientific acceptance.

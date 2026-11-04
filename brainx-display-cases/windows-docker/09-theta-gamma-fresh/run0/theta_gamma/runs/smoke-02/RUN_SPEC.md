# smoke-02
Level: smoke; entry: new; start: 2026-11-04T00:19:38.406716+00:00
Config SHA256: 7864ea96f2cb49d41c20d117db6ab0b30272b5a0a1b58b057d7a76f7104444b7
Specification SHA256: e5e07c72138f70d3466cc3661482635dbeb05016bb60e20069d04283a7ccd54a
CPU float64, deterministic dynamics; surrogate seed 20261103. No empirical data.
Expected: raw trajectories NPZ, runtime JSON, exit_code/log/status; non-smoke also derived NPZ, metrics JSON/CSV.
Resource estimate: <2 GB RSS, <120 s runtime. Hard timeout 300 s; zero automatic retries.
Stop on timeout, nonfinite/invalid State or artifact failure; preserve all outputs.
Full histories are sampled at 1 kHz for analysis; no ongoing checkpoint/resume is needed for this short run.
Mechanical completion does not imply scientific acceptance.

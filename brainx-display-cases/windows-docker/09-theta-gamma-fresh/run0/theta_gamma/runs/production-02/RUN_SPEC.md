# production-02
Level: production; entry: new; start: 2026-11-04T00:19:54.322326+00:00
Config SHA256: ce326cb431766fb663278e6d71f89fefaccbfac78ca7287563863e29fec4a175
Specification SHA256: e5e07c72138f70d3466cc3661482635dbeb05016bb60e20069d04283a7ccd54a
CPU float64, deterministic dynamics; surrogate seed 20261103. No empirical data.
Expected: raw trajectories NPZ, runtime JSON, exit_code/log/status; non-smoke also derived NPZ, metrics JSON/CSV.
Resource estimate: <2 GB RSS, <120 s runtime. Hard timeout 300 s; zero automatic retries.
Stop on timeout, nonfinite/invalid State or artifact failure; preserve all outputs.
Full histories are sampled at 1 kHz for analysis; no ongoing checkpoint/resume is needed for this short run.
Mechanical completion does not imply scientific acceptance.

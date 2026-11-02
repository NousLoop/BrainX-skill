# Mechanical monitoring report

- Run ID: `alpha-production-20261102-i1`
- Level and entry case: production, new
- Backend/device: JAX CPU / `cpu:0`
- Recorded command: `/workspace/runs/alpha-production-20261102-i1/command.txt`
- Launcher-observed wall time: 5.55 seconds; completion artifacts were finalized at approximately 2026-11-02 03:31:06 UTC.
- Exit/status: `done`, exit code 0. This is a mechanical status, not scientific acceptance.
- Progress/log: `/workspace/runs/alpha-production-20261102-i1/run.log` completed with the deterministic assessment; no liveness stall or device error occurred.
- Primary declared raw metrics: baseline median peak 11.0 Hz, baseline median retained RMS 1.24533 mV, and baseline median 8–13 Hz fraction within 4–30 Hz 0.99948. Weakened-condition retained RMS medians were 6.29e-6, 4.50e-9, and 4.26e-9 mV at 75%, 50%, and 25% inhibition.
- Mechanical checks: all full and half-step arrays parse and are finite; production EEG shape is `[60000, 4, 8]`; half-step EEG shape is `[120000, 2, 1]`; cortical EEG component identity error is 0 mV; config and specification hashes remained unchanged.
- Deterministic invalidity: both half-step convergence checks failed the locked RMS criterion. The 100% condition differed by 8.37% (limit 5%); the 25% condition was below the signal floor with a 99.31% relative difference and undefined peak in both runs.
- Artifacts: complete according to `/workspace/runs/alpha-production-20261102-i1/artifact_manifest.json`; no checkpoint was required for this short deterministic run; no retry was attempted.
- Status returned to modeling loop: `done` with a scientifically invalid result pending independent review.


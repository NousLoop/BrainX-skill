# Figure manifest — iteration 1 diagnostic evidence

## figures/diagnostic/traces.png and .pdf
- Work type: create; evidence mode: diagnostic; unaccepted iteration 1. Question: Compare E/I, EEG proxy and gamma-band envelope with/without theta modulation.
- Source run: production-01; source artifacts: runs/production-01/raw/trajectories.npz and raw/derived.npz; full provenance: runs/production-01/manifest.json.
- Raw SHA256: 8340be0665a2bf4308eedfa78b51a231f408f6b6f7871d162c3996e425865bc5; derived SHA256: efaf684cfeff61f604728bed6775ab97e8545cdd99784b8f51fe103e66d6d49a.
- Data: time × IC × condition; time in seconds, dimensionless E/I, proxy and envelope a.u.; PSD a.u.²/Hz; known phase radians.
- Transformations: 2 s warmup, 1 kHz sampled records, fourth-order zero-phase Butterworth/Hilbert, 0.5 s edges; Welch 2000 samples; 18 phase bins. No outcome-specific smoothing, clipping or exclusions.
- Samples: traces/nesting first IC at fixed g=1,m=0/0.75; scan means of all 3 ICs, no CIs or biological n. Cycle null 199 draws, descriptive.
- Controls/scales: fixed in brainx-study-record.md; same limits across paired panels. 5×5 discrete cells with no interpolation; × invalid original gamma criterion, not independently certified carrier.
- Plotting source: figures.py; PNG 200 dpi + PDF vector, traces 12×8 in, nesting 15×4 in, scan 16×4 in.
- Render check: opened all three PNGs and matched fixed-pair values / grid coordinates with source; nonblank, unclipped, readable. Top trace time axis is shared and explicitly labeled seconds below. Exposes ~22 Hz baseline cycle despite gamma-band harmonic.

## figures/diagnostic/nesting.png and .pdf
- Work type: create; evidence mode: diagnostic; unaccepted iteration 1. Question: Inspect PSD, phase-binned envelope and cycle null; expose harmonic ambiguity.
- Source run: production-01; source artifacts: runs/production-01/raw/trajectories.npz and raw/derived.npz; full provenance: runs/production-01/manifest.json.
- Raw SHA256: 8340be0665a2bf4308eedfa78b51a231f408f6b6f7871d162c3996e425865bc5; derived SHA256: efaf684cfeff61f604728bed6775ab97e8545cdd99784b8f51fe103e66d6d49a.
- Data: time × IC × condition; time in seconds, dimensionless E/I, proxy and envelope a.u.; PSD a.u.²/Hz; known phase radians.
- Transformations: 2 s warmup, 1 kHz sampled records, fourth-order zero-phase Butterworth/Hilbert, 0.5 s edges; Welch 2000 samples; 18 phase bins. No outcome-specific smoothing, clipping or exclusions.
- Samples: traces/nesting first IC at fixed g=1,m=0/0.75; scan means of all 3 ICs, no CIs or biological n. Cycle null 199 draws, descriptive.
- Controls/scales: fixed in brainx-study-record.md; same limits across paired panels. 5×5 discrete cells with no interpolation; × invalid original gamma criterion, not independently certified carrier.
- Plotting source: figures.py; PNG 200 dpi + PDF vector, traces 12×8 in, nesting 15×4 in, scan 16×4 in.
- Render check: opened all three PNGs and matched fixed-pair values / grid coordinates with source; nonblank, unclipped, readable. Top trace time axis is shared and explicitly labeled seconds below. Exposes ~22 Hz baseline cycle despite gamma-band harmonic.

## figures/diagnostic/scan.png and .pdf
- Work type: create; evidence mode: diagnostic; unaccepted iteration 1. Question: Show every discrete depth/gain setting, including invalid gamma-band points.
- Source run: production-01; source artifacts: runs/production-01/raw/trajectories.npz and raw/derived.npz; full provenance: runs/production-01/manifest.json.
- Raw SHA256: 8340be0665a2bf4308eedfa78b51a231f408f6b6f7871d162c3996e425865bc5; derived SHA256: efaf684cfeff61f604728bed6775ab97e8545cdd99784b8f51fe103e66d6d49a.
- Data: time × IC × condition; time in seconds, dimensionless E/I, proxy and envelope a.u.; PSD a.u.²/Hz; known phase radians.
- Transformations: 2 s warmup, 1 kHz sampled records, fourth-order zero-phase Butterworth/Hilbert, 0.5 s edges; Welch 2000 samples; 18 phase bins. No outcome-specific smoothing, clipping or exclusions.
- Samples: traces/nesting first IC at fixed g=1,m=0/0.75; scan means of all 3 ICs, no CIs or biological n. Cycle null 199 draws, descriptive.
- Controls/scales: fixed in brainx-study-record.md; same limits across paired panels. 5×5 discrete cells with no interpolation; × invalid original gamma criterion, not independently certified carrier.
- Plotting source: figures.py; PNG 200 dpi + PDF vector, traces 12×8 in, nesting 15×4 in, scan 16×4 in.
- Render check: opened all three PNGs and matched fixed-pair values / grid coordinates with source; nonblank, unclipped, readable. Top trace time axis is shared and explicitly labeled seconds below. Exposes ~22 Hz baseline cycle despite gamma-band harmonic.

# Figure manifest — preserved diagnostic and accepted final evidence

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


# Iteration 2 figure evidence

## figures/diagnostic-iteration-2/traces.png and .pdf
- Work type: create; evidence mode: diagnostic; question: Compare E/I gamma, proxy and phase-dependent envelope.
- Acceptance: provisional, unaccepted diagnostic at export; preserved.
- Source run: production-02; source files runs/production-02/raw/trajectories.npz (SHA256 ae1e31e5bd33b8148399e63a6073e0bf49494c621926e2d7f1120e23003ffbd4) and raw/derived.npz (SHA256 366b9ec7e20de11a1a7a0a556f88c511e759fb77e84a2cde4f00ba0dd6fb7dc5); config/environment/complete manifest in same run.
- Variables/axes: E/I time × IC × condition, dimensionless activity; time seconds; proxy/envelope a.u.; PSD a.u.²/Hz; known theta phase radians; grid m rows × g columns. View order proxy, no_theta, E, E_minus_I.
- Transformations: 2 s transient discarded, 1 kHz point sampling; order-4 zero-phase Butterworth 25–100 Hz and Hilbert; each edge 0.5 s removed for metrics; native Welch nperseg=2000; 18 mean-amplitude phase bins. No additional curve smoothing. R/ΔR/fraction/peak values come directly from exported metrics.
- Sample unit: deterministic IC sensitivity, n=3; first IC g=1,m=0/0.75 for traces/nesting (3–3.5 s trace); all 3 IC arithmetic mean for 5×5 grid; no CIs/biological inference. 199 per-cycle phase rotations, seed 20261103, complete edge cycles removed.
- Controls: same mean input, initial conditions, solver, phase reference and observation mapping. Same fixed axes across paired panels. Grid uses discrete cells without interpolation; × current band/timing invalid, ○ matched m=0 autonomous gamma invalid. Continuous values of invalid points are preserved.
- Source/output: figures.py; PNG 200 dpi and vector PDF. Traces 12×8 in; nesting 15×4 in; scan 16×4 in. PNG SHA256 f1733acd838b112c2731fc122ab262977149c6a14b04a14fe587e2b616849b1f.
- Render/source checks: PNG opened visually; nonblank, legible, no overlap/clipping; paired axes and all 25 coordinates agree with source. R 0.000272/0.501625 and carrier 43.5 Hz independently compared with metrics; null/invalid points visible. Final mode uses same evidence/encodings after PASS.

## figures/diagnostic-iteration-2/nesting.png and .pdf
- Work type: create; evidence mode: diagnostic; question: Compare PSD, known-phase amplitude profile and cycle rotations.
- Acceptance: provisional, unaccepted diagnostic at export; preserved.
- Source run: production-02; source files runs/production-02/raw/trajectories.npz (SHA256 ae1e31e5bd33b8148399e63a6073e0bf49494c621926e2d7f1120e23003ffbd4) and raw/derived.npz (SHA256 366b9ec7e20de11a1a7a0a556f88c511e759fb77e84a2cde4f00ba0dd6fb7dc5); config/environment/complete manifest in same run.
- Variables/axes: E/I time × IC × condition, dimensionless activity; time seconds; proxy/envelope a.u.; PSD a.u.²/Hz; known theta phase radians; grid m rows × g columns. View order proxy, no_theta, E, E_minus_I.
- Transformations: 2 s transient discarded, 1 kHz point sampling; order-4 zero-phase Butterworth 25–100 Hz and Hilbert; each edge 0.5 s removed for metrics; native Welch nperseg=2000; 18 mean-amplitude phase bins. No additional curve smoothing. R/ΔR/fraction/peak values come directly from exported metrics.
- Sample unit: deterministic IC sensitivity, n=3; first IC g=1,m=0/0.75 for traces/nesting (3–3.5 s trace); all 3 IC arithmetic mean for 5×5 grid; no CIs/biological inference. 199 per-cycle phase rotations, seed 20261103, complete edge cycles removed.
- Controls: same mean input, initial conditions, solver, phase reference and observation mapping. Same fixed axes across paired panels. Grid uses discrete cells without interpolation; × current band/timing invalid, ○ matched m=0 autonomous gamma invalid. Continuous values of invalid points are preserved.
- Source/output: figures.py; PNG 200 dpi and vector PDF. Traces 12×8 in; nesting 15×4 in; scan 16×4 in. PNG SHA256 64a89668d062c039cdc265922c63c541f97db0e5b921d1897821708b050b2446.
- Render/source checks: PNG opened visually; nonblank, legible, no overlap/clipping; paired axes and all 25 coordinates agree with source. R 0.000272/0.501625 and carrier 43.5 Hz independently compared with metrics; null/invalid points visible. Final mode uses same evidence/encodings after PASS.

## figures/diagnostic-iteration-2/scan.png and .pdf
- Work type: create; evidence mode: diagnostic; question: Retain all discrete depth/gain outcomes and invalid settings.
- Acceptance: provisional, unaccepted diagnostic at export; preserved.
- Source run: production-02; source files runs/production-02/raw/trajectories.npz (SHA256 ae1e31e5bd33b8148399e63a6073e0bf49494c621926e2d7f1120e23003ffbd4) and raw/derived.npz (SHA256 366b9ec7e20de11a1a7a0a556f88c511e759fb77e84a2cde4f00ba0dd6fb7dc5); config/environment/complete manifest in same run.
- Variables/axes: E/I time × IC × condition, dimensionless activity; time seconds; proxy/envelope a.u.; PSD a.u.²/Hz; known theta phase radians; grid m rows × g columns. View order proxy, no_theta, E, E_minus_I.
- Transformations: 2 s transient discarded, 1 kHz point sampling; order-4 zero-phase Butterworth 25–100 Hz and Hilbert; each edge 0.5 s removed for metrics; native Welch nperseg=2000; 18 mean-amplitude phase bins. No additional curve smoothing. R/ΔR/fraction/peak values come directly from exported metrics.
- Sample unit: deterministic IC sensitivity, n=3; first IC g=1,m=0/0.75 for traces/nesting (3–3.5 s trace); all 3 IC arithmetic mean for 5×5 grid; no CIs/biological inference. 199 per-cycle phase rotations, seed 20261103, complete edge cycles removed.
- Controls: same mean input, initial conditions, solver, phase reference and observation mapping. Same fixed axes across paired panels. Grid uses discrete cells without interpolation; × current band/timing invalid, ○ matched m=0 autonomous gamma invalid. Continuous values of invalid points are preserved.
- Source/output: figures.py; PNG 200 dpi and vector PDF. Traces 12×8 in; nesting 15×4 in; scan 16×4 in. PNG SHA256 4ae9ed2700ea5dc9664445cc09ca08b2d03df1b69522b4d153020cfcdc610b31.
- Render/source checks: PNG opened visually; nonblank, legible, no overlap/clipping; paired axes and all 25 coordinates agree with source. R 0.000272/0.501625 and carrier 43.5 Hz independently compared with metrics; null/invalid points visible. Final mode uses same evidence/encodings after PASS.

## figures/final-iteration-2/traces.png and .pdf
- Work type: create; evidence mode: final; question: Compare E/I gamma, proxy and phase-dependent envelope.
- Acceptance: independent review iteration 2 PASS; accepted illustrative scope.
- Source run: production-02; source files runs/production-02/raw/trajectories.npz (SHA256 ae1e31e5bd33b8148399e63a6073e0bf49494c621926e2d7f1120e23003ffbd4) and raw/derived.npz (SHA256 366b9ec7e20de11a1a7a0a556f88c511e759fb77e84a2cde4f00ba0dd6fb7dc5); config/environment/complete manifest in same run.
- Variables/axes: E/I time × IC × condition, dimensionless activity; time seconds; proxy/envelope a.u.; PSD a.u.²/Hz; known theta phase radians; grid m rows × g columns. View order proxy, no_theta, E, E_minus_I.
- Transformations: 2 s transient discarded, 1 kHz point sampling; order-4 zero-phase Butterworth 25–100 Hz and Hilbert; each edge 0.5 s removed for metrics; native Welch nperseg=2000; 18 mean-amplitude phase bins. No additional curve smoothing. R/ΔR/fraction/peak values come directly from exported metrics.
- Sample unit: deterministic IC sensitivity, n=3; first IC g=1,m=0/0.75 for traces/nesting (3–3.5 s trace); all 3 IC arithmetic mean for 5×5 grid; no CIs/biological inference. 199 per-cycle phase rotations, seed 20261103, complete edge cycles removed.
- Controls: same mean input, initial conditions, solver, phase reference and observation mapping. Same fixed axes across paired panels. Grid uses discrete cells without interpolation; × current band/timing invalid, ○ matched m=0 autonomous gamma invalid. Continuous values of invalid points are preserved.
- Source/output: figures.py; PNG 200 dpi and vector PDF. Traces 12×8 in; nesting 15×4 in; scan 16×4 in. PNG SHA256 5b69288b73cf1c9e8bed424e3a47168b7f47f2f25d7234ae7f679a1b01c28c4e.
- Render/source checks: PNG opened visually; nonblank, legible, no overlap/clipping; paired axes and all 25 coordinates agree with source. R 0.000272/0.501625 and carrier 43.5 Hz independently compared with metrics; null/invalid points visible. Final mode uses same evidence/encodings after PASS.
- PDF render check: independently rasterized with an isolated temporary pypdfium2 wheel, then opened and visually inspected; legible, nonblank, no clipping or overlap. Renderer identity and render dimensions: checks/final-delivery.json.

## figures/final-iteration-2/nesting.png and .pdf
- Work type: create; evidence mode: final; question: Compare PSD, known-phase amplitude profile and cycle rotations.
- Acceptance: independent review iteration 2 PASS; accepted illustrative scope.
- Source run: production-02; source files runs/production-02/raw/trajectories.npz (SHA256 ae1e31e5bd33b8148399e63a6073e0bf49494c621926e2d7f1120e23003ffbd4) and raw/derived.npz (SHA256 366b9ec7e20de11a1a7a0a556f88c511e759fb77e84a2cde4f00ba0dd6fb7dc5); config/environment/complete manifest in same run.
- Variables/axes: E/I time × IC × condition, dimensionless activity; time seconds; proxy/envelope a.u.; PSD a.u.²/Hz; known theta phase radians; grid m rows × g columns. View order proxy, no_theta, E, E_minus_I.
- Transformations: 2 s transient discarded, 1 kHz point sampling; order-4 zero-phase Butterworth 25–100 Hz and Hilbert; each edge 0.5 s removed for metrics; native Welch nperseg=2000; 18 mean-amplitude phase bins. No additional curve smoothing. R/ΔR/fraction/peak values come directly from exported metrics.
- Sample unit: deterministic IC sensitivity, n=3; first IC g=1,m=0/0.75 for traces/nesting (3–3.5 s trace); all 3 IC arithmetic mean for 5×5 grid; no CIs/biological inference. 199 per-cycle phase rotations, seed 20261103, complete edge cycles removed.
- Controls: same mean input, initial conditions, solver, phase reference and observation mapping. Same fixed axes across paired panels. Grid uses discrete cells without interpolation; × current band/timing invalid, ○ matched m=0 autonomous gamma invalid. Continuous values of invalid points are preserved.
- Source/output: figures.py; PNG 200 dpi and vector PDF. Traces 12×8 in; nesting 15×4 in; scan 16×4 in. PNG SHA256 4bd9cee69ab68ffbde1ecc07e60c8be6336e2c5471e0ba075b6c46fd22b5e530.
- Render/source checks: PNG opened visually; nonblank, legible, no overlap/clipping; paired axes and all 25 coordinates agree with source. R 0.000272/0.501625 and carrier 43.5 Hz independently compared with metrics; null/invalid points visible. Final mode uses same evidence/encodings after PASS.
- PDF render check: independently rasterized with an isolated temporary pypdfium2 wheel, then opened and visually inspected; legible, nonblank, no clipping or overlap. Renderer identity and render dimensions: checks/final-delivery.json.

## figures/final-iteration-2/scan.png and .pdf
- Work type: create; evidence mode: final; question: Retain all discrete depth/gain outcomes and invalid settings.
- Acceptance: independent review iteration 2 PASS; accepted illustrative scope.
- Source run: production-02; source files runs/production-02/raw/trajectories.npz (SHA256 ae1e31e5bd33b8148399e63a6073e0bf49494c621926e2d7f1120e23003ffbd4) and raw/derived.npz (SHA256 366b9ec7e20de11a1a7a0a556f88c511e759fb77e84a2cde4f00ba0dd6fb7dc5); config/environment/complete manifest in same run.
- Variables/axes: E/I time × IC × condition, dimensionless activity; time seconds; proxy/envelope a.u.; PSD a.u.²/Hz; known theta phase radians; grid m rows × g columns. View order proxy, no_theta, E, E_minus_I.
- Transformations: 2 s transient discarded, 1 kHz point sampling; order-4 zero-phase Butterworth 25–100 Hz and Hilbert; each edge 0.5 s removed for metrics; native Welch nperseg=2000; 18 mean-amplitude phase bins. No additional curve smoothing. R/ΔR/fraction/peak values come directly from exported metrics.
- Sample unit: deterministic IC sensitivity, n=3; first IC g=1,m=0/0.75 for traces/nesting (3–3.5 s trace); all 3 IC arithmetic mean for 5×5 grid; no CIs/biological inference. 199 per-cycle phase rotations, seed 20261103, complete edge cycles removed.
- Controls: same mean input, initial conditions, solver, phase reference and observation mapping. Same fixed axes across paired panels. Grid uses discrete cells without interpolation; × current band/timing invalid, ○ matched m=0 autonomous gamma invalid. Continuous values of invalid points are preserved.
- Source/output: figures.py; PNG 200 dpi and vector PDF. Traces 12×8 in; nesting 15×4 in; scan 16×4 in. PNG SHA256 f062695823cb0557e2758a4c88a348dcd1ac9765006a8cd135048638e8c3a52e.
- Render/source checks: PNG opened visually; nonblank, legible, no overlap/clipping; paired axes and all 25 coordinates agree with source. R 0.000272/0.501625 and carrier 43.5 Hz independently compared with metrics; null/invalid points visible. Final mode uses same evidence/encodings after PASS.
- PDF render check: independently rasterized with an isolated temporary pypdfium2 wheel, then opened and visually inspected; legible, nonblank, no clipping or overlap. Renderer identity and render dimensions: checks/final-delivery.json.

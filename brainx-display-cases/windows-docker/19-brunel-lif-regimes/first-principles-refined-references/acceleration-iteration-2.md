# Iteration-2 acceleration and parity

Analysis-only correction; no dynamical rewrite, new simulation, scientific change or performance claim. The original compiled sparse simulation, CPU group policy and parity evidence remain in acceleration.md and checks/acceleration.json. model.py hash is unchanged: a2c7b9b1dc5000670fb2d0f03d7debdb6c3ba2c673cfa23e30d770531e284e9c.

Owning operations: documented BrainTools spectrogram for Welch and full-window Fourier density, with BrainUnit physical signal/sample interval/PSD. Scoped BrainState precision=64 preserves the original float64 analysis independently of float32 simulation State. The operation consumes one 30000-sample rate array per run; no State or RNG is advanced. Host loops enumerate independent saved runs and decode observations; no Python simulation timestep loop is introduced. Raw spike/graph symlinks are read-only inputs to this script.

All 16 reanalyses, including four numerical controls, completed in 29.505 s including raw decoding, spectral execution, parity and serialization. First analysis took 3.624 s; subsequent per-run timings are in run.log. These are end-to-end reanalysis timings, not a steady-state kernel benchmark or claimed speedup. Further transform changes are unjustified for this narrow correction.

All frequency axes match exactly; largest relative L2 PSD difference is 4.68e-15. The predeclared spectral tolerance is rtol=1e-9, atol=1e-11. All scalar metrics/predicates and four decisions are preserved, and every raw hash matches the parent manifest. See runs/iteration-2/spectral_parity.json, RUN_SPEC.md, environment.json and manifest.json. Serialization collision protection and retained synthetic input pass checks/metrics_fixture_v2/test_result.json.

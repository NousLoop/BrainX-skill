# Brunel-lif-regimes: independent first-principles baseline

The scientific contract is NeuroSpecification.md, locked before simulation and recorded in specification.sha256. first-principles.md derives the model and states its assumptions. No papers, scientific example implementations or external model code were consulted. BrainX skills and public API contracts were used for library mechanics only.

Environment: existing /brainx-venv/bin/python on Windows WSL2 / Docker, JAX CPU. No package installation. Exact package and code provenance is in each immutable run's environment.json and code/ snapshot.

All sixteen simulations completed. The [final report](report.md) records the partially supported scientific result and [independent review PASS](reviews/iteration-2.md). Final PNGs are in [figures/](figures/), with their sources, hashes and inspection recorded in [FIGURE_MANIFEST.md](FIGURE_MANIFEST.md). The main output is [four_conditions.png](figures/four_conditions.png); additional PNGs show [E/I rates](figures/ei_rates.png), [ISI CV](figures/isi_cv.png), [global-rate spectra](figures/global_rate_spectrum.png) and [timestep sensitivity](figures/step_halving.png).

runs/locked-baseline is a preserved failed execution; runs/locked-baseline-v2 is the completed corrected execution with the same scientific contract. Seeds are [11, 29, 47]; each run has 1 s burn-in and 3 s observation. Four seed-11 timestep checks are also retained. Never treat the partial parent run as an additional replicate.

Re-run checks with:

```bash
JAX_PLATFORMS=cpu OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=1 /brainx-venv/bin/python checks.py
```

The exact production command is runs/locked-baseline-v2/command.txt. To repeat the scientific execution, copy its immutable config.json and code/ to a new output directory, then run the copied experiment.py with --config pointing at the new config. Do not overwrite archived evidence. This experiment uses roughly 1 GB of persistent raw data plus working memory; timing is hardware dependent.

Each raw NPZ contains spikes_packed (time × 1563 bytes), little-endian bit order, E neurons first, 12500 valid neuron bits, zero padding. Separate burn-in spikes, final voltage (mV), last spike step and RNG-key diagnostics are retained. The first observed spike bin has endpoint t=1000 ms+dt. Metrics NPZs contain native-dt E/I counts, per-neuron ISI CV/interval count/spike count, frequency (Hz) and PSD ((Hz/neuron)^2/Hz). Global-rate spectra and decisions use 0.1 ms bins, including rebinned fine-dt data. JSON/CSV metrics retain all frozen predicates, exact per-run labels and timing.

The accepted final spectral analysis uses BrainTools spectrogram with the frozen periodic Hann window, per-segment constant detrending and segment averaging. The native arrays are in [analysis-iteration-2/braintools-final/metrics](analysis-iteration-2/braintools-final/metrics); [parity.json](analysis-iteration-2/braintools-final/parity.json) verifies all sixteen spectra, frequencies and classifications against the archived analysis. No neural simulation was changed. The original execution snapshot and its original estimator remain immutable for provenance.

To render the accepted figures and rebuild the report from saved evidence:

```bash
MPLBACKEND=Agg JAX_PLATFORMS=cpu OPENBLAS_NUM_THREADS=1 python plot_results.py --run runs/locked-baseline-v2 --mode final --spectra analysis-iteration-2/braintools-final
python write_report.py --run runs/locked-baseline-v2 --review PASS
```

The generated figure manifest should be supplemented with visual inspection after any new render. Existing final source and render verification is in figures/finalization_checks.json. No literature or scientific implementation search is part of this workflow.

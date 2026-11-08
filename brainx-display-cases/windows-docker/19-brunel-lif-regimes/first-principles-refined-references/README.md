# First-principles LIF regime experiment

The scientific contract is locked in [NeuroSpecification.md](NeuroSpecification.md). No literature, scientific examples, existing model implementations or remembered protocols were used. Installed BrainX skills/public API contracts were read only for mechanics. All unspecified choices were explicitly delegated by the researcher.

`model.py` implements physical-unit endpoint LIF dynamics, native BrainPy-State delta projection, sparse BrainEvent communication, exact independent Poisson counts and native BrainState delay. `analysis.py` implements the frozen statistics and predicates. `experiment.py` preserves an immutable code/config/environment snapshot and all-neuron binary spikes, with at most three independent process-owned runs. The provided CPU runtime is a Linux Docker environment with a Windows-mounted workspace; no native Windows execution is claimed.

In the provided Python environment:

```bash
python checks.py
python experiment.py --run-dir runs/new-run-id
python plot_results.py --run-dir runs/new-run-id --mode diagnostic
```

Run directories must be new to preserve evidence. After independent Codex PASS, use `python plot_results.py --run-dir <accepted-run> --mode final` to export figures from the exact accepted run. Do not mark fresh runs accepted merely because this baseline passed. The reviewer report, figure manifest and scientific report preserve the accepted scope.

Raw NPZ contract: `packed[time,ceil(N/8)]` is little-endian bit-packed binary neuron spikes; neuron IDs 0..9999 are E and 10000..12499 are I. Endpoint time of row i is `(i+1)*dt_ms`. `counts[time,2]` contains E/I spike counts. Fine-grid raw files retain 0.05-ms events; analysis rebins only global rate to 0.1 ms for spectra. `graphs/seed*.npz` contains source-row CSR indices/pointers for each projection and initial voltage in mV; all nonzero adjacency entries are one and weights are JE/-g*JE. Metrics NPZ contains all-neuron CV, count, Welch and full periodogram arrays; JSON/CSV preserves all reductions and eligibility. `assessment.json` evaluates every frozen predicate and numerical-control discrepancy without tuning.

Each graph has exactly 12,500,000 E and 3,125,000 I edges. Independent source superposition has per-neuron step expectation `Cext*nu_ext*dt=eta` at 0.1 ms. During refractory, incoming jumps are discarded. See the specification for ordering, finite-grid interpretation, burn-in, duration, classification rules and limitations.

## Corrected analysis and retained evidence

The original 16 full-size runs remain in `runs/baseline-v1`. Review 1 is retained in `reviews/iteration-1.md`; it requested BrainTools spectral ownership and a preserved synthetic input. Both fixes and all-16 parity are in `reviews/addressed-iteration-2.md` and `runs/iteration-2/spectral_parity.json`. The separate analysis snapshot references the original raw data/graphs without changing them.

```bash
python check_metric_fixture.py
python reanalyze.py
python plot_results.py --run-dir runs/iteration-2 --mode diagnostic --out-dir figures/iteration-2-diagnostic
python write_report.py --run-dir runs/iteration-2
```

`reanalyze.py` intentionally refuses to overwrite `runs/iteration-2`; to reproduce, work in a fresh project copy or change only its output run ID. The fixture test can be rerun with its raw input retained. After independent PASS of iteration 2, final figures use `python plot_results.py --run-dir runs/iteration-2 --mode final`. Acceptance records the exact reviewer file/hash and run scope. Production results and original diagnostic figures remain intact.

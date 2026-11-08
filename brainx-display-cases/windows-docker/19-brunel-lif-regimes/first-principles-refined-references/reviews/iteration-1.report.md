# Current-based LIF network: independent exploration

- Report status: draft
- Scientific outcome: partially_supported
- Review outcome: REFUSE
- Research question: do the four supplied conditions support SR, fast SI, AI and slow SI, respectively?
- Evidence available: all 12 baseline and 4 numerical-control runs; immutable code/config/environment; complete neuron spikes, graphs, raw spectra and individual CV; component/replay checks; inspected PNGs.
- Missing evidence: BrainTools spectral parity and replayable synthetic raw fixture, followed by fresh independent review
- Current conclusion: provisional, unaccepted finite-window evidence; see the condition decisions below.
- Next action: iteration-2 package restudy and analysis/fixture corrections; preserve production raw evidence

This is a first-principles experiment derived only from the supplied data. No papers, scientific example scripts, existing model implementations or remembered protocols were consulted. Installed skills and public API contracts were used only for package mechanics. The researcher explicitly delegated every unspecified choice, and [NeuroSpecification.md](NeuroSpecification.md) was locked before implementation or simulation. No scientific parameters, thresholds, seeds, durations or plotted cases were tuned after observing results.

| (g, eta) | Requested | E rate Hz | I rate Hz | Median ISI CV | Dominant frequency Hz | Frozen decision |
|---|---|---|---|---|---|---|
| (3, 2) | SR | 333.33 (333.33–333.33) | 333.33 (333.33–333.33) | 0.000 (0.000–0.000) | 333.0 (333.0–333.0) | supported |
| (6, 4) | fast SI | 59.30 (59.05–59.43) | 59.38 (59.20–59.52) | 0.796 (0.783–0.813) | 183.3 (182.0–185.0) | supported |
| (5, 2) | AI | 37.85 (37.76–37.95) | 37.83 (37.77–37.91) | 0.408 (0.407–0.408) | 137.3 (135.0–139.0) | unsupported |
| (4.5, 0.9) | slow SI | 5.55 (5.43–5.73) | 5.56 (5.44–5.72) | 0.614 (0.610–0.616) | 19.7 (17.0–23.0) | inconclusive |

Entries are means across three independent graph/input seeds, with the full min–max range in parentheses; these are descriptive ranges, not confidence intervals. Each CV entry first takes the median over eligible neurons within its run. A spectral maximum is always reported; it establishes an oscillation only when the frozen concentration and background tests also pass.

![Four conditions](figures/diagnostic/four_conditions.png)

Each upper panel shows instantaneous global rate in unsmoothed 0.1-ms bins, in Hz per neuron, with its displayed-window mean dashed. Rate axes have independent numeric scales to keep low-rate conditions visible. Each lower panel shows the same randomly selected 50 neurons in the same order. All panels use seed 101 and 3500<t≤4000 ms; no spikes were jittered. The raster supports a visual comparison while the quantitative decisions use the entire post-burn 3 s and all neurons.

![E/I rates](figures/diagnostic/ei_rates.png)

E/I rates are post-burn means in Hz per neuron. Each connected pair is one matched graph/input seed; the dashed black pair is the seed101 fine-grid control. There are three independent baseline realizations, with no confidence interval implied. Complete native-grid E/I rate traces are saved in [population_rates.npz](runs/baseline-v1/population_rates.npz), and scalar rates in [metrics_summary.csv](runs/baseline-v1/metrics_summary.csv).

![ISI CV](figures/diagnostic/isi_cv.png)

ISI CV histograms show all eligible E and I neurons across the three baseline seeds. CV is dimensionless; a neuron must have at least 20 complete post-burn ISIs. Histograms describe the neuron distributions and do not treat neurons as independent experimental replicates. Fixed 0.50/0.70 decision cutoffs are drawn; eligibility is retained for every seed.

![Spectra](figures/diagnostic/global_rate_spectra.png)

Global-rate Welch spectra use one-second Hann windows with 50% overlap after removing the burn-in, at the actual 0.1-ms rate sampling interval. Frequency is in Hz and PSD in (Hz/neuron)²/Hz, plotted logarithmically. Every baseline seed and fine-grid control is shown; markers identify the baseline maxima within 1–500 Hz. Full-window periodograms are also saved.

![Frozen tests](figures/diagnostic/regime_tests.png)

Rows show the exact continuous quantities used by the frozen categorical tests: excess fractional count modulation S, median CV, spectral concentration within ±2 Hz, peak/background ratio, and fractional half-window rate drift. Dashed lines are the fixed cutoffs; crosses in the synchrony row show each half separately. These panels expose threshold margins and unfavorable evidence.

## Per-run evidence

| g | eta | seed | dt ms | E/I rates Hz | S | median CV | eligible | f Hz | concentration | peak/background | stationary | requested outcome |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | 2 | 101 | 0.1 | 333.33/333.33 | 0.141 | 0.000 | 100.0% | 333 | 1.000 | 25290225.5 | True | supported |
| 3 | 2 | 202 | 0.1 | 333.33/333.33 | 0.142 | 0.000 | 100.0% | 333 | 1.000 | 168290459.1 | True | supported |
| 3 | 2 | 303 | 0.1 | 333.33/333.33 | 0.142 | 0.000 | 100.0% | 333 | 1.000 | 155019731.5 | True | supported |
| 3 | 2 | 101 | 0.05 | 333.33/333.33 | 0.142 | 0.000 | 100.0% | 333 | 1.000 | 75109765.1 | True | supported |
| 6 | 4 | 101 | 0.1 | 59.05/59.20 | 0.154 | 0.791 | 100.0% | 182 | 0.157 | 207.5 | True | supported |
| 6 | 4 | 202 | 0.1 | 59.43/59.42 | 0.157 | 0.783 | 100.0% | 183 | 0.246 | 280.0 | True | supported |
| 6 | 4 | 303 | 0.1 | 59.43/59.52 | 0.159 | 0.813 | 100.0% | 185 | 0.242 | 244.3 | True | supported |
| 6 | 4 | 101 | 0.05 | 60.45/60.38 | 0.170 | 0.868 | 100.0% | 176 | 0.224 | 397.1 | True | supported |
| 5 | 2 | 101 | 0.1 | 37.82/37.81 | 0.265 | 0.407 | 100.0% | 139 | 0.064 | 29.0 | True | unsupported |
| 5 | 2 | 202 | 0.1 | 37.95/37.91 | 0.276 | 0.408 | 100.0% | 135 | 0.069 | 30.8 | True | unsupported |
| 5 | 2 | 303 | 0.1 | 37.76/37.77 | 0.259 | 0.408 | 100.0% | 138 | 0.061 | 22.3 | True | unsupported |
| 5 | 2 | 101 | 0.05 | 37.92/37.95 | 0.270 | 0.413 | 100.0% | 130 | 0.074 | 28.2 | True | unsupported |
| 4.5 | 0.9 | 101 | 0.1 | 5.43/5.44 | 1.430 | 0.616 | 8.1% | 17 | 0.095 | 197.7 | True | inconclusive |
| 4.5 | 0.9 | 202 | 0.1 | 5.49/5.51 | 1.474 | 0.616 | 8.8% | 19 | 0.115 | 157.9 | True | inconclusive |
| 4.5 | 0.9 | 303 | 0.1 | 5.73/5.72 | 1.601 | 0.610 | 13.3% | 23 | 0.168 | 128.4 | True | inconclusive |
| 4.5 | 0.9 | 101 | 0.05 | 5.74/5.74 | 1.551 | 0.613 | 13.8% | 23 | 0.120 | 100.2 | True | inconclusive |

## Numerical sensitivity and regime decisions

Every condition was independently rerun at 0.05 ms for the same seed101 graph and initial voltage, for the same 4 s with the same 1 s burn-in. Its input is another discretization of the same Poisson law; paths are not coupled identically across the grids. The frozen test flags >10% E/I rate change, categorical change, or an excessive oscillatory peak shift. A flagged discrepancy withholds a grid-independent regime claim.

| Condition | Relative E/I rate changes | Category changes | Peak change Hz | Numerical flag | Final decision |
|---|---|---|---|---|---|
| (3, 2) | 0.00%/0.00% | none | 0 | False | supported |
| (6, 4) | 2.37%/2.00% | none | 6 | False | supported |
| (5, 2) | 0.25%/0.37% | none | 9 | False | unsupported |
| (4.5, 0.9) | 5.62%/5.49% | oscillation_supported | 6 | True | inconclusive |


Seed 101 at (5, 2) fails: asynchronous, irregular. Measured description: SR.


Seed 202 at (5, 2) fails: asynchronous, irregular. Measured description: SR.


Seed 303 at (5, 2) fails: asynchronous, irregular. Measured description: SR.


Seed 101 at (4.5, 0.9) fails: irregular, oscillatory. Measured description: synchronous, inconclusive.


Seed 202 at (4.5, 0.9) fails: irregular. Measured description: synchronous, inconclusive.


Seed 303 at (4.5, 0.9) fails: irregular. Measured description: synchronous, inconclusive.


## Equations, checks and limits

Between events dV/dt=−V/(20 ms), with zero leak equilibrium as the reference for supplied voltages. At eligible endpoints add 0.1 mV per E/external event and −g×0.1 mV per I event, threshold at 20 mV, reset to 10 mV, and discard jumps during the 2-ms refractory interval. Recurrent events arrive exactly 1.5 ms after emission. The initial voltage is uniform on [10,20) mV; recurrent delay history is empty. All choices and the finite-grid ordering are explicit in the locked specification. The external source rate is 10 eta Hz per afferent, so exact superposition of 1000 afferents produces a Poisson count with expectation eta per 0.1-ms step. External input denotes stationary arrivals: a fixed transmission delay leaves their independent stationary Poisson law unchanged. This preserves independent shot noise and multiplicities.

The graph has 12,500 neurons, with exactly 1000 distinct E and 250 distinct I inputs per target, no autapses or duplicate edges, and 15,625,000 recurrent edges. Each graph and initial state are shared across its four conditions; different seeds have independent graphs, initial states and drive. BrainPy-State supplies native LIF population/projection interfaces; BrainEvent communicates sparse binary events; BrainUnit retains physical dimensions; BrainState owns State, RNG, delay and compilation.

Component checks verify exponential leak, signs, threshold/reset, exact refractory release and both-grid recurrent arrival. The compiled small-network path matches an independent explicit arithmetic reference spike-for-spike, with <0.00003 mV voltage error. Poisson mean/variance, multiple-event probability, cross-target correlation, dimensional mismatch rejection, full-size replay and worker-affinity parity pass. Synthetic metric fixtures verify 100-Hz periodic spikes yield exact rate, CV, S and spectral peak; they are explicitly separate from simulation evidence. Failed pre-production fixture/reset attempts and their corrections are retained.

Regimes here are operational finite-window labels at four sampled points. Three seeds do not establish parameter regions or biological realism. The 5-ms S statistic removes a Poisson counting floor but is a macroscopic modulation proxy; its interpretation is conditional on the fixed bin and 5%/10% thresholds. The CV cutoffs leave an explicit unresolved interval. The 50-Hz fast/slow boundary is derived from 1/tau_m and is an agent-chosen convention. A 3-s analysis window limits slow dynamics and CV eligibility, and the half-window checks do not establish arbitrary-time stationarity. Numerical controls test one finer grid at one seed, with independent discretized Poisson realizations; sensitivity is reported rather than tuned away.

Actual runtime: CPU Linux Docker over a Windows-mounted workspace; exact interpreter, packages, OS/device identity and source hashes are in [environment.json](runs/baseline-v1/environment.json). Sparse event simulation is compiled as a whole rollout and independent baseline seeds run in three process-owned CPU groups; controls follow them. No approximate connectivity, downsizing, mean current substitution or omitted seeds were used.

## Evidence and independent review

- [Frozen specification](NeuroSpecification.md), [mechanics study](brainx-study-record.md), [acceleration](acceleration.md), [checks](checks/components.json), [full-size parity](checks/acceleration.json), [metric fixture](checks/metrics_fixture/test_result.json)
- [Run/config contract](runs/baseline-v1/RUN_SPEC.md), [configuration](runs/baseline-v1/config.json), [run provenance and hashes](runs/baseline-v1/environment.json), [run manifest](runs/baseline-v1/manifest.json)
- [Assessment and claim-evidence matrix](runs/baseline-v1/assessment.md), [complete deterministic assessment](runs/baseline-v1/assessment.json), [raw file index](RAW_EVIDENCE.md)
- [Figure manifest](FIGURE_MANIFEST.md), [figure contract](FIGURE_CONTRACT.md), [runnable instructions](README.md)
- Independent review: pending; no final scientific acceptance claimed.

PNG exports were checked for nonblank content, correct rates/event timing, legible labels and unclipped panel composition. Figure sources and hashes are recorded in the figure manifest.

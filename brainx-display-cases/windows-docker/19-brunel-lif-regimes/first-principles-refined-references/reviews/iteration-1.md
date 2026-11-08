# BrainX iteration review

- **OUTCOME:** `REFUSE`
- **SCIENTIFIC_OUTCOME:** `PARTIALLY_SUPPORTED`
- **LOSS_CLOSURE:** `NOT_APPLICABLE`
- **OPTIMIZATION_ADEQUACY:** `NOT_APPLICABLE`
- **NEXT_ACTION:** `RETURN_TO_STUDY`

## Good-enough reason

Independent recomputation of all 16 runs confirms the saved counts, rates, CVs, synchrony, spectra, refractory timing, and assessment. All manifest hashes match. The frozen rules support SR and fast SI, contradict AI, and leave slow SI inconclusive because of insufficient CV eligibility and spectral sensitivity. Acceptance requires correcting the undocumented BrainTools spectral bypass and preserving the synthetic fixture’s raw input; production simulations need no rerun if corrected analysis preserves the evidence.

## Findings

### BX-001: Spectral analysis bypasses a documented BrainTools API

- **Severity:** `major`
- **Location:** [analysis.py](/workspace/analysis.py:64); [brainx-study-record.md](/workspace/brainx-study-record.md:30).
- **Problem:** SciPy computes Welch spectra and full-window periodograms without a spectral `BrainTools API gap` artifact. The [routed metric reference](/codex-home/skills/package-skills/brainpy-state/references/braintools/metric.md) explicitly documents `braintools.analysis.spectral.spectrogram` with window, detrending, segment-length, and overlap controls, followed by `u.math.mean(segment_psd, axis=1)`. Calling spectra a host-analysis boundary does not establish a missing capability.
- **Scientific consequence:** The saved spectra are reproducible, but the mandatory BrainX API-selection and external-boundary parity requirements remain unmet. Spectral concentration determines fast-SI support and the slow-SI numerical flag.
- **Minimum fix:** Use the documented BrainTools segment-spectrum operation with the frozen settings and verify frequencies, PSD normalization, shapes, units, and decisions against every saved spectrum. A single full-window boxcar segment can express the periodogram. Preserve the original evidence and document any remaining external capability gap.

### BX-002: Synthetic metric fixture lacks its referenced raw input

- **Severity:** `minor`
- **Location:** `/workspace/checks/metrics_fixture/raw.npz`; `/workspace/checks/metrics_fixture/test_result.json`; [analysis.py](/workspace/analysis.py:106).
- **Problem:** The fixture’s `raw_file` points to an archive containing derived CVs, counts per neuron, spectra, and rates. It lacks the packed spikes, per-bin counts, and configuration required by `summarize`. The output naming permits overwriting an identically named input archive when directories coincide.
- **Scientific consequence:** The reported fixture check cannot be replayed from its referenced input. Its derived arrays are internally consistent; production raw evidence remains intact.
- **Minimum fix:** Preserve the fixture’s raw events and configuration under a distinct input path, and retain a runnable check that verifies the frozen expectations without overwriting that input.

## Unverified assumptions

- Numerical parity of the proposed BrainTools spectral replacement remains unverified. Its import was blocked by the review environment’s read-only Matplotlib cache requirement; this does not establish a production API gap.
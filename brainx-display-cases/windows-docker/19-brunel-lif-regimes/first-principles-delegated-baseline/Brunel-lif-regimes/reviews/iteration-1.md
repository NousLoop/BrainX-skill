# BrainX iteration review

- **OUTCOME:** `REFUSE`
- **SCIENTIFIC_OUTCOME:** `PARTIALLY_SUPPORTED`
- **LOSS_CLOSURE:** `NOT_APPLICABLE`
- **OPTIMIZATION_ADEQUACY:** `NOT_APPLICABLE`
- **NEXT_ACTION:** `RETURN_TO_STUDY`

## Good-enough reason

Independent decoding of all 16 raw archives reproduces the reported counts, per-neuron CVs, spectra, and supported / inconclusive / unsupported / inconclusive verdicts. Graph invariants, provenance hashes, execution parity, and figure sources check out. The finite-protocol scientific assessment is supported, including its numerical sensitivity, but the required justification for bypassing BrainTools spectral analysis is missing.

## Findings

### BX-001: Missing BrainTools spectral API assessment

- **Severity:** `major`
- **Location:** [experiment.py](/workspace/Brunel-lif-regimes/experiment.py:31), [brainx-study-record.md](/workspace/Brunel-lif-regimes/brainx-study-record.md:20)
- **Problem:** Analysis uses `scipy.signal.welch`, while the routed [metric reference](/codex-home/skills/package-skills/brainpy-state/references/braintools/metric.md) documents `braintools.analysis.spectral.power_spectral_density` with Welch segment and overlap controls. The archived API-gap entry covers graph construction only. Describing analysis as host statistics does not establish a missing BrainTools capability. The [general guard](/codex-home/skills/brainx-general-guard/SKILL.md) requires: “Before replacing a BrainTools-owned input, metric, optimizer, integration, encoding, or other infrastructure operation with SciPy, raw JAX, or custom code, record a compact API-gap artifact”.
- **Scientific consequence:** Independent FFT recomputation confirms the archived spectra; no spectral error was found. However, spectral prominence and peak frequency determine classifications, and the mandatory library-capability and equivalence evidence remains absent.
- **Minimum fix:** Compare the documented BrainTools PSD operation against the locked Welch settings using saved rate series. Use it if suitable; otherwise record the checked APIs, exact missing capability, smallest SciPy boundary, and unit, State, shape, and numerical parity evidence. Verify PSD, peak frequency, prominence, low-frequency fraction, and verdicts. Existing simulations can remain archived without rerunning.

## Unverified assumptions

- Exact compatibility of the documented BrainTools PSD API with the locked estimator remains unresolved. No archived comparison exists; a review-time attempt was blocked during import because Matplotlib required a writable cache in this read-only environment.

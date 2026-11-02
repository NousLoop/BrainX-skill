# BrainX iteration review

- **OUTCOME:** `REFUSE`
- **SCIENTIFIC_OUTCOME:** `INVALID`
- **LOSS_CLOSURE:** `NOT_APPLICABLE`
- **OPTIMIZATION_ADEQUACY:** `NOT_APPLICABLE`
- **NEXT_ACTION:** `RETURN_TO_STUDY`

## Good-enough reason

Both runs completed and reproduce identical numeric bundles, but the baseline fails the locked numerical-convergence criterion: retained RMS changes from 1.245107 to 1.148933 mV at half step, an 8.37% discrepancy against the 5% limit. This is independent of the defective near-zero convergence comparison.

The implementation is substantially BrainX-native: BrainMass owns the model, BrainState owns complete stateful mapped rollouts, BrainUnit preserves physical quantities, and BrainTools computes spectra. The explicitly required `for_loop`/`vmap` path justifies the custom execution boundary. Independent raw-array checks confirm shapes, finite EEG/E/I trajectories, saved RMS values, and the EEG component identity to floating-point precision.

The observed 11 Hz baseline and disappearance of identifiable weakened-condition oscillations are reproducible diagnostic observations—not yet numerically validated model conclusions or scalp-EEG predictions.

## Findings

### NUM-001: Baseline amplitude fails numerical validity

- **Severity:** critical
- **Location:** `alpha_rhythm.py:367–395`; both production runs’ `convergence.json` and `half_step_results.npz`
- **Problem:** The baseline first lane has identical 11 Hz peak bins but an 8.37% retained-RMS discrepancy between 0.1 and 0.05 ms. Identical replication does not resolve discretization error.
- **Scientific consequence:** The locked experiment is invalid. Frequency-bin agreement alone cannot validate amplitude or the quantitative inhibition comparison.
- **Minimum fix:** Preserve these runs as invalid. First perform a diagnostic 0.025 ms comparison using the same BrainMass model, inputs, initialization, duration, and analysis. Establish step-size stabilization without changing thresholds. Because production `dt=0.1 ms` is locked, adopting a finer production step requires an explicit specification amendment and a new complete sweep—not retrospective acceptance of these runs.

### NUM-002: Convergence rule cannot accept a legitimate nonoscillatory condition

- **Severity:** major
- **Location:** `alpha_rhythm.py:379–392`; both production runs’ `convergence.json`; `NeuroSpecification.md`, acceptance boundary
- **Problem:** Peak masking correctly returns undefined frequency below 0.01 mV RMS, but convergence subsequently subtracts those undefined peaks and requires the difference to pass. Thus even identical fixed-point traces would fail. The 25% RMS values, approximately 4.25×10⁻⁹ and 2.13×10⁻⁹ mV, also produce a misleading 99.31% relative discrepancy despite an absolute difference of only approximately 2.12×10⁻⁹ mV.
- **Scientific consequence:** The reported 25% failure does not demonstrate meaningful numerical instability. It conflates non-identifiable oscillation frequency and negligible residual variation with failure of a dynamical prediction. This conflicts with the specification’s explicit allowance for stable weakened-condition fixed points.
- **Minimum fix:** Retain the existing failed assessment. Prospectively resolve the specification conflict: require frequency convergence only when oscillations are identifiable at both steps; separately classify both-below-floor and discordant cases. Establish an independently justified absolute tolerance for near-zero signals alongside the existing relative criterion. Add exact-zero, tiny-residual, oscillatory, and threshold-discordant tests. Do not choose tolerances merely to pass these results; baseline NUM-001 remains independently decisive.

### CLAIM-001: Machine-readable support flags omit the validity gate

- **Severity:** major
- **Location:** `run_experiment.py:189–199`; both production runs’ `claim_evidence.json`
- **Problem:** The claim matrix marks baseline alpha and inhibition-induced change as supported using metric predicates alone, although the same run fails numerical validity.
- **Scientific consequence:** Downstream consumers can interpret invalid diagnostic patterns as accepted scientific claims. The report appropriately labels them provisional, but the machine-readable evidence is inconsistent.
- **Minimum fix:** Preserve metric-predicate results separately from scientific support. Gate scientific support on the required validity controls and explicitly mark these runs invalid. Continue reporting below-floor peaks as undefined; their alpha-power fractions do not establish identifiable alpha rhythms.

## Unverified assumptions

- The exact integration method and dependency implementation identity are not established by the preserved model-name/defaults description and project-source hashes. Record the documented numerical method and an immutable environment identity through permitted provenance mechanisms.
- Below-floor retained variation supports “no identifiable oscillation in this observation window,” not proof of an asymptotic fixed point. No equilibrium-residual or longer-duration evidence establishes that stronger statement.
- The initial-condition ensemble measures deterministic starting-state sensitivity, not biological uncertainty. No empirical calibration or observation model supports literal scalp amplitudes or in-vivo causal generalization.

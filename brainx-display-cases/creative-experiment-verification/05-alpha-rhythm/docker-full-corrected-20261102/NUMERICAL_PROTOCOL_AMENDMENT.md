# Locked numerical protocol amendment — iteration 3

Authorization: researcher delegated all remaining settings and continued execution.
Every biological parameter and the scientific intervention remain unchanged.

1. First save a full-grid 0.025 ms diagnostic to compare with preserved 0.05 ms evidence.
2. Candidate production steps, fixed before new outcomes: 0.05, 0.025, 0.0125, 0.00625 ms.
   Each new complete 4x8 sweep is compared against an independent full-grid half-step run.
   Select the first passing every lane; if none pass, report invalid without widening criteria.
3. Align analysis at 2.001, 2.002, ..., 6.000 seconds (1 ms interval), using unchanged
   2 s Hann Welch segments, 50% overlap, 0.5 Hz bins, 8-13 Hz band and 4-30 Hz search.
4. RMS floor remains 0.01 mV. Both-identifiable lanes require peak difference <=0.5 Hz;
   both-below-floor lanes have undefined frequency; discordant classifications fail.
5. RMS requires <=5% relative difference OR <=1e-6 mV absolute difference. The absolute
   criterion reuses the pre-outcome JIT parity tolerance, 10,000-fold below the signal floor.
   It is not derived from the observed residual. Baseline failure remains independently decisive.
6. Scientific support requires all validity checks; store metric predicates separately.
   Undefined JSON values are null, not fabricated frequencies or nonstandard NaN literals.
7. Quiet window means no identifiable oscillation; do not claim an asymptotic fixed point.

Numerical method: explicit public method="exp_euler", matching the documented default:
https://brainx.chaobrain.com/brainmass/reference/generated/brainmass.JansenRitStep.html
Pin Docker image ID and seccomp hash without inspecting installed library files or metadata.

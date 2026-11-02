# Iteration 3 study and correction plan

The fresh scientific review is preserved verbatim in reviews/iteration-2-scientific.md.
Coverage is forward simulation only, at aggregate cortical-population scale.

## Restudied sources
- skills/brainx-general-guard/SKILL.md: scale, matched controls, no installed-source introspection.
- skills/brainx-modeling-loop/SKILL.md: refusal -> restudy, immutable runs, diagnostic/final closure.
- skills/package-skills/brainmass/SKILL.md and references/modellibrary.md:
  JansenRitStep.Ai is mV inhibitory PSP gain; public EEG is E-I.
- brainmass references/scripts/jansen-rit-eeg-proxy.py: official resting-column input pattern.
- brainmass references/batch-transform-acceleration.md and parameter-sweeps-and-regime-analysis.md:
  preserve model construction/initialization within each independently mapped lane.
- brainmass references/visualization-analysis-api.md: BrainTools Welch, physical sampling interval,
  amplitude floor and undefined frequency below it.
- skills/package-skills/brainstate/SKILL.md and transformation-jit-expansion.md:
  preserve whole stateful for_loop/vmap and stable whole-rollout JIT, compare full trajectories.
- skills/package-skills/brainunit/SKILL.md and quantity-inspection-and-conversion.md:
  retain mV/time quantities until the documented host statistical/NPZ boundary.
- skills/brainx-acceleration/SKILL.md: no further hot-path rewrite; repeat short parity at finer dt.

## Finding map and design fixed before new outcomes
- NUM-001: preserve both 0.1/0.05 ms invalid runs. First save a diagnostic full-grid 0.025 ms
  comparison with the original inputs/initial states/window. Prospectively refine production
  dt by factors of two starting at 0.05 ms; compare every one of 32 lanes to its half-step
  counterpart at the same 1 ms recording interval. Stop at the first globally valid resolution,
  with a maximum of four candidate production resolutions. Do not change biological parameters.
- NUM-002: separate identifiable oscillation (both RMS >= 0.01 mV), both-below-floor, and
  discordant regimes. Require the unchanged <=0.5 Hz frequency difference only for two
  identifiable spectra; discordant classifications fail. Require RMS relative difference <=5%
  OR absolute difference <=1e-6 mV. The absolute tolerance reuses the pre-outcome JIT parity
  tolerance, is 10,000 times below the existing oscillation floor, and is not derived from
  residual values in the failed runs. Save null frequency/relative values where undefined.
  This is a prospective correction to conflicting acceptance-rule applicability, not acceptance
  of the old runs. Add exact-zero, tiny-residual, oscillatory and discordant regression tests.
- CLAIM-001: separate observed metric predicates from scientific support; support additionally
  requires the full numerical/mapping validity gate. Add a failed-validity regression test.
- Narrow quiet-regime wording to no identifiable oscillation in this 2-6 s window; do not claim
  an asymptotic fixed point without equilibrium evidence. The IC ensemble is deterministic
  starting-state sensitivity, not biological uncertainty.
- Record the immutable Docker image ID, seccomp-profile hash, code hashes and documented
  integration scheme. Do not inspect installed implementation or package metadata.

Researcher authorization: the researcher explicitly delegated all unspecified settings and
continued the complete workflow. Numerical resolution and prospective applicability corrections
are recorded in a specification amendment; 5%, 0.5 Hz, biological parameters and signal floors
remain unchanged. Old specification and all raw runs remain preserved.

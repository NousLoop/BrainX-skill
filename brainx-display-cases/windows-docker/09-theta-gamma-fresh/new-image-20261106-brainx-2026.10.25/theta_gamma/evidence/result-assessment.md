# Deterministic result assessment

- Run: production-02; scientific outcome: supported; review pending.
- All results provisional until independent Codex PASS. Proposed next action: step 5 independent read-only MCP review; after PASS final rendering/report only.
- Exact decision reconstructed from saved arrays in assess_results.py; all 147 conditions retained.
- Display case: relative gain 1, depth .6; indices control=3, intervention=31. Gamma peak 29.5→27.5 Hz (operational band 25–90 Hz).
- R values: [0.001998137399450587, 0.000415978676356003, 0.0008103608052152043] → [0.0761674737962321, 0.07609449866942616, 0.07417780401531379]; paired deltas [0.07416933639678151, 0.07567851999307017, 0.07336744321009858]; exact cycle-rotation null95 [0.017858884052354983, 0.01876918051447945, 0.01749735152947364].
- All 3 lanes pass full fixed predicate. These are deterministic initial-State/observation-seed sensitivities, not 3 independent biological replicates.
- MI_eeg: [0.004137429417955507, 0.004119239937546771, 0.004083930435817041]; E-only R: [0.07306900408483485, 0.07323945391660042, 0.07176609008881399]; latent E−0.5I R: [0.07642907415669487, 0.07643476971352424, 0.07641494215941433].
- Theta+noise-only R: [0.028694942669877568, 0.01637501850557813, 0.024881647571457846]; corresponding null95: [0.030977976119634654, 0.03351517361456692, 0.038866001388949786]. Each is below its own null95; noise can still yield nonzero sample PAC.
- Phase pattern: envelope is *suppressed near maximum E drive* (phase zero); the phase profile has two broad flanks, so its first-moment phase is not a unique burst location. Do not claim drive maxima maximize gamma.
- Sweep: 18/49 samples per lane satisfy the full predicate. 14/49 samples per lane have ineligible matched baselines: relative gain .7 is nearly stationary, gain 1.3 has dominant 24.5 Hz below the declared gamma band despite finite gamma-band power. Red X indicates these cannot establish modulation of an existing gamma baseline. Of 35 eligible sampled conditions, 17 fail the declared nesting rule; all retained.
- Nonmonotonic counterexample: gain 1.1, m=.6→.8: R=0.083653→0.037887. At gain .8, R peaks at sampled m=.4 and declines thereafter. No monotonic law or continuous region is supported.
- Numerical convergence: {'all_passed': True, 'count': 21, 'max_gamma_relative_error': 2.0708600539446766e-05, 'max_frequency_error_Hz': 0.0, 'max_R_abs_error': 3.164810522554573e-05}. Baseline and intervention are both tested for all 7 gains at m=0,.6,1 (lane 0); this is bounded validation, not a proof for all unsampled conditions.
- Invariant-domain checks pass; negative abstract E down to -0.023184 is allowed by the offset sigmoid, not a physiological negative firing-rate claim.
- Fixed parameters are illustrative, and baseline was outcome-calibrated by the separately locked unmodulated-only rule. There is no empirical or biological parameter inference.
- Scope: the imposed theta input is conditionally sufficient for known-phase gamma-envelope dependence in this model and measurement construction. Broad-band PAC does not isolate pure amplitude modulation from waveform changes, harmonics, frequency modulation or mixtures. No endogenous theta or unique biological mechanism is inferred.

| Claim | Decisive evidence | Allowed interpretation / limitation |
|---|---|---|
| Unmodulated gamma exists at display gain | calibration.npz; metrics/analysis.npz psd_E; decision.npz broad_peak_Hz | Oscillatory synthetic baseline, 29.5 Hz under operational band |
| External theta modulation changes phase nesting | saved envelope, known input phase, exact null rotations, delta_R and full predicate | Conditional input intervention effect only |
| Withdrawal removes most nesting but retains gamma | paired m=0 at each same gain; display R≈0 and gamma 29.5 Hz | Separate matched runs from identical t=0 State; no within-run switch claim |
| EEG proxy reflects the pattern | observations.npz, proxy PSD and R, E-only sensitivity, theta+noise leakage check | Synthetic arbitrary-unit observation; theta remains present in proxy under both conditions |
| Depth and gain matter nonmonotonically | evidence/sweep.csv; R_map_lane0.csv; raw grid axes and validity masks | Sampled points only; ineligible and failed cases included |
| Numerical and execution contracts hold | tests.json, integrity.json, convergence.npz, source/provenance hashes | Explicit tested resolution and State/control contracts |
| No mechanism uniqueness | construction and observation limitations | This is an illustrative sufficiency demonstration, not mechanism identification |

Raw binaries: runs/production-02/raw/trajectories.npz, observations.npz, refinement.npz. Analysis binaries: runs/production-02/metrics/analysis.npz, decision.npz, convergence.npz, refinement.npz. Full lineage and superseded run: evidence/run-lineage.md. No exclusions or failed hypotheses hidden.

## Acceptance update
Independent Codex MCP review PASS, scientific outcome SUPPORTED; see reviews/iteration-1.md. This addendum closes the provisional review status above. Final report and figures are complete; no numerical decision changed after review.

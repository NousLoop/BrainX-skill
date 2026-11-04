"""Deterministic, frozen acceptance predicates and claim/evidence export."""
import json
from pathlib import Path
import numpy as np


def main():
    prod=Path("runs/production-02"); conv=Path("runs/convergence-02")
    p=json.loads((prod/"metrics/metrics.json").read_text())
    c=json.loads((conv/"metrics/metrics.json").read_text())
    raw=np.load(prod/"raw/trajectories.npz")
    cfg=json.loads((prod/"config.json").read_text())
    choose=lambda rows,v,r,m,g: next(x for x in rows if x["view"]==v and x["rep"]==r and x["depth"]==m and x["gain"]==g)
    comparison=[]; numerical=[]
    for view in ["proxy","no_theta","E","E_minus_I"]:
        for rep in range(3):
            off=choose(p,view,rep,0,1); on=choose(p,view,rep,.75,1)
            delta=on["R"]-off["R"]
            comparison.append({"view":view,"rep":rep,"off":off,"on":on,"delta_R":delta,
                "strong_predicate":off["autonomous_gamma_predicate"] and off["valid_gamma"] and on["valid_gamma"] and delta>.05 and
                    on["surrogate_observed_R"]>on["surrogate_q95"],
                "window_delta_R":[b-a for a,b in zip(off["window_R"],on["window_R"])]})
            for depth in [0,.75]:
                coarse=choose(p,view,rep,depth,1); fine=choose(c,view,rep,depth,1)
                dr=abs(coarse["R"]-fine["R"])
                df=abs(coarse["band_peak_hz"]-fine["band_peak_hz"])
                numerical.append({"view":view,"rep":rep,"depth":depth,"delta_R":dr,
                    "delta_band_peak_hz":df,"both_valid":coarse["valid_gamma"] and fine["valid_gamma"],
                    "pass":dr<=.02 and df<=2})
    is_control=np.asarray(cfg["depths_flat"])==0
    input_const=bool(np.all(raw["P"][:,:,is_control]==1.25))
    all_bounded=bool(all(np.isfinite(raw[k]).all() and (raw[k]>=0).all() and (raw[k]<=1).all() for k in ["E","I"]))
    validation=json.loads(Path("checks/verification.json").read_text())["status"]=="PASS"
    numerical_pass=all(x["pass"] for x in numerical)
    primary=[x for x in comparison if x["view"]=="proxy"]
    strong=all(x["strong_predicate"] for x in primary)
    # Favorable outcomes never override numerical or control failures.
    outcome="invalid" if not (input_const and all_bounded and validation and numerical_pass) else (
        "supported" if strong else "partially_supported")
    invalid=[r for r in p if r["view"]=="no_theta" and not r["valid_gamma"]]
    assessment={"scientific_outcome":outcome,"review_status":"pending",
        "primary_fixed_pair_strong_all_ICs":strong,"numerical_pass":numerical_pass,
        "max_convergence_delta_R":max(x["delta_R"] for x in numerical),
        "max_convergence_delta_peak_hz":max(x["delta_band_peak_hz"] for x in numerical),
        "control_input_exact":input_const,"state_bounds_finite":all_bounded,"verification_pass":validation,
        "comparison":comparison,"convergence":numerical,
        "invalid_gamma_rows_without_theta":invalid,
        "all_samples_retained":len(p)==4*25*3,
        "autonomous_gamma_carrier_established":all(x["off"]["autonomous_gamma_predicate"] for x in primary),
        "scan_matched_carrier_controls":[{"rep":r["rep"],"depth":r["depth"],"gain":r["gain"],
            "baseline_carrier_valid":choose(p,"no_theta",r["rep"],0,r["gain"])["autonomous_gamma_predicate"],
            "current_band_and_timing_valid":r["valid_gamma"]} for r in p if r["view"]=="no_theta"],
        "proposed_next_action":"Independent review iteration 2, then final figures/report only after PASS."}
    Path("assessment.json").write_text(json.dumps(assessment,indent=2,allow_nan=False))
    text=["# Deterministic result assessment (provisional until independent review)",
        f"Scientific outcome: {outcome}; review pending.",
        f"Controls exact: {input_const}; State bounded/finite: {all_bounded}; tests PASS: {validation}.",
        f"Numerical predicate: {numerical_pass}; max ΔR={assessment['max_convergence_delta_R']:.6f}, max Δpeak={assessment['max_convergence_delta_peak_hz']:.2f} Hz.",
        "\n| Readout | IC | off R | on R | ΔR | off/on valid gamma | on cycle-null q95 | strong predicate |",
        "|---|---:|---:|---:|---:|---|---:|---|"]
    for x in comparison:
        text.append(f"| {x['view']} | {x['rep']} | {x['off']['R']:.6f} | {x['on']['R']:.6f} | {x['delta_R']:.6f} | {x['off']['valid_gamma']}/{x['on']['valid_gamma']} | {x['on']['surrogate_q95']:.6f} | {x['strong_predicate']} |")
    text += ["\nNo post-outcome tuning. The two failed implementation/verification witnesses are disclosed in failure-log.md.",
        "Iteration 1 remains a partial failure (~22 Hz carrier with gamma harmonic), archived under iterations/iteration-1 and runs/*-01. Its original band-only predicates must not be interpreted as carrier certification.",
        "Iteration 2 common tau scaling is outcome-calibrated and illustrative. Current strong_predicate requires a valid autonomous E/I gamma carrier, current band/timing validity, ΔR>0.05 and complete-cycle null exceedance. legacy_band_valid retains the original weaker predicate only.",
        "All parameter points and native single-signal PAC values remain in metrics.json/CSV. Undefined gamma peak is null, not a detected oscillation.",
        "Numerical certification is limited to the fixed g=1 pair; scan points are descriptive at dt=0.05 ms.",
        "The imposed theta source and theta mixture are exogenous. PAC/surrogates are deterministic descriptive statistics, not animal-level inference.",
        "No unique mechanism or real EEG correspondence follows from this model."]
    Path("result-assessment.md").write_text("\n".join(text)+"\n")
    Path("claim-evidence.md").write_text("""# Claim–evidence matrix (provisional)

| User question / claim | Observable | Evidence | Boundary |
|---|---|---|---|
| E/I gamma circuit, iteration 2 | E/I cycle rate + dominant native Welch peak, agreement, interval CV, p2p and count | metrics.json E_cycle/I_cycle and autonomous_gamma_predicate at m=0; assessment.json | initial iteration failed; revised tau scale is outcome-calibrated and illustrative |
| theta phase nesting | known-drive phase vs gamma envelope R, MI and bins | raw/derived.npz phase_curves, phase_counts, surrogates_R; fixed-pair assessment | imposed 6 Hz source; no claim of intrinsic theta |
| removal of modulation | matched m=0 at each g and IC, same constant mean drive and observation | raw P, metrics for every control, assessment control_input_exact | only the periodic input term is removed; theta mixture stays by design |
| simulated EEG proxy | y=E−0.5I+0.2cosφ, y without theta, E, E−I | raw derived proxy/base; all four readout metrics and native MI | no physical EEG units or measurement model; nonsinusoidal harmonics may contribute |
| depth × gain scan | R, ΔR, MI, validity margins and peak frequency at all 25×3 points | config axes, metrics.csv/JSON, scan figure | discrete descriptive samples; no inferred continuous phase boundary or multiplicity-corrected map |
| observation robustness | signs/magnitudes of paired effect across 4 mappings | assessment comparison rows | these four linear readouts only; source mixing remains non-identifiable |
| numerical reliability | equation witness, independent adaptive solver, batch/scalar/final State parity, reset, dt half | checks/verification.json and logs; convergence run; assessment | Euler transient phase error retained; full scan not dt certified |
| no scientific selectivity | null/invalid settings and failed checks | failure-log.md, iterations/iteration-1, both iterations' full raw/metrics/manifests, reviews/iteration-1.md | revised tau/carrier criteria disclosed before iteration-2 production; no original evidence removed |
""")
    print(json.dumps({k:assessment[k] for k in ["scientific_outcome","primary_fixed_pair_strong_all_ICs","numerical_pass","max_convergence_delta_R","max_convergence_delta_peak_hz","control_input_exact"]},indent=2))


if __name__=="__main__": main()

"""Focused equation, lifecycle, batching and metric witnesses."""
import json
from pathlib import Path
import time

import numpy as np
import scipy.integrate
import braintools
import brainmass
import brainstate
import brainunit as u
import model
import analysis


def base_config():
    return {"gains_flat":[1.0,1.1],"depths_flat":[0.0,0.75],
        "initial_e":[0.1,0.11,0.09],"initial_i":[0.1,0.09,0.11],
        "method":"euler","mean_drive":1.25,"theta_hz":6.0,
        "dt_ms":0.05,"duration_s":0.01,"transient_s":0.0,"sample_every":1,
        "tau_e_ms":1.25,"tau_i_ms":2.5}


def verify():
    checks = {}
    c = base_config()
    start = time.perf_counter(); raw = model.run_model(c); cold = time.perf_counter()-start
    replay = model.run_model(c)
    checks["shape"] = list(raw["E"].shape)
    assert raw["E"].shape == (200,3,2)
    assert raw["E"].dtype == np.float64
    assert np.isclose(raw["t_s"][0],0.00005)
    e,i=0.1,0.1
    s = lambda x: 1/(1+np.exp(-x))
    expected_E = e + .05*(-e+s(1.3*(16*e-12*i+1.25-4)))/1.25
    expected_I = i + .05*(-i+s(2*(15*e-3*i-3.7)))/2.5
    checks["one_step_error"] = [float(abs(raw["E"][0,0,0]-expected_E)),
                                  float(abs(raw["I"][0,0,0]-expected_I))]
    assert max(checks["one_step_error"]) < 1e-12
    for key in ["E","I","P","final_E","final_I"]:
        assert np.array_equal(raw[key], replay[key]), key
    checks["reset_replay_exact"] = True
    reused = model.IllustrativeWC([1.0], [.1], [.1])
    simulator = brainmass.Simulator(reused, dt=.05*u.ms)
    first = simulator.run(2*u.ms, inputs=lambda _i,_t: (1.25,0.0),
                          monitors=["rE","rI"],batch_size=1)
    second = simulator.run(2*u.ms, inputs=lambda _i,_t: (1.25,0.0),
                           monitors=["rE","rI"],batch_size=1)
    assert all(np.array_equal(first[k],second[k]) for k in ["rE","rI"])
    checks["same_model_default_reset_exact"] = True
    scalar = dict(c,gains_flat=[1.1],depths_flat=[.75],initial_e=[.11],initial_i=[.09])
    one = model.run_model(scalar)
    checks["batch_scalar_max_error"] = max(float(np.max(abs(raw[k][:,1,1]-one[k][:,0,0]))) for k in ["E","I"])
    checks["batch_final_error"] = max(float(abs(raw[k][1,1]-one[k][0,0])) for k in ["final_E","final_I"])
    assert checks["batch_scalar_max_error"] < 1e-12
    assert checks["batch_final_error"] < 1e-12
    tiny = dict(c,duration_s=.001)
    unjit = model.run_model(tiny,jit=False)
    jit = model.run_model(tiny)
    checks["jit_unjit_error"] = max(float(np.max(abs(unjit[k]-jit[k]))) for k in ["E","I","final_E","final_I"])
    assert checks["jit_unjit_error"] < 1e-12
    expected_P=1.25+np.asarray(c["depths_flat"])[None,None,:]*np.cos(2*np.pi*6*raw["input_t_s"][:,None,None])
    checks["input_error"] = float(np.max(abs(raw["P"]-expected_P)))
    assert checks["input_error"] < 1e-12
    checks["bounds_finite"] = bool(all(np.isfinite(raw[k]).all() and (raw[k]>=0).all() and (raw[k]<=1).all() for k in ["E","I"]))
    assert checks["bounds_finite"]

    def rhs(t,state):
        e,i=state
        return [(-e+s(1.3*(16*e-12*i+1.25-4)))/.00125,
                (-i+s(2*(15*e-3*i-3.7)))/.0025]
    sol = scipy.integrate.solve_ivp(rhs,(0,.01),[.1,.1],rtol=1e-11,atol=1e-13,dense_output=True)
    assert sol.success
    errors=[]
    for dt in [.05,.025,.0125]:
        q=model.run_model(dict(c,dt_ms=dt))
        reference=sol.sol(q["t_s"]).T
        errors.append(float(np.max(abs(np.column_stack([q["E"][:,0,0],q["I"][:,0,0]])-reference))))
    checks["independent_solver_max_errors_dt_0p05_0p025_0p0125"] = errors
    # Verify first-order convergence rather than assuming phase-aligned Euler is exact.
    assert all(.45 < b/a < .55 for a,b in zip(errors[:-1],errors[1:])) and errors[-1]<.01
    args=np.linspace(-20,20,1001)
    activation_error=float(np.max(abs(np.asarray(brainstate.nn.sigmoid(args))-s(args))))
    checks["native_sigmoid_parity_error"] = activation_error
    assert activation_error < 1e-15

    t=np.arange(12000)/1000
    ph=2*np.pi*6*t
    amplitude=1+.6*np.cos(ph)
    carrier=amplitude*np.cos(2*np.pi*60*t)
    amp=np.abs(analysis.analytic_band(carrier,.001,(25,100)))
    keep=(t>=.5)&(t<11.5)
    R,MI,_,_,_=analysis.reference_pac(amp[keep],ph[keep])
    null_signal=np.cos(2*np.pi*60*t)+.2*np.cos(ph)
    null_amp=np.abs(analysis.analytic_band(null_signal,.001,(25,100)))
    null_R=analysis.reference_pac(null_amp[keep],ph[keep])[0]
    native_mi,_,_=braintools.metric.phase_amplitude_coupling(carrier+.2*np.cos(ph),.001*u.second,
        phase_freq_range=(4,8),amplitude_freq_range=(25,100),n_bins=18)
    sr,null,p,n=analysis.cycle_surrogates(amp[keep],ph[keep],20261103,199)
    checks["synthetic_AM"]={"R":R,"analytic_expected_R":.3,"MI":MI,"native_MI":float(native_mi),
        "linear_mixture_null_R":null_R,"surrogate_q95":float(np.quantile(null,.95)),"p":p,"cycles":n}
    assert abs(R-.3)<.01 and null_R<.005 and abs(MI-float(native_mi))<.02 and p<=.01
    carrier_cfg={"carrier_prominence":.2,"carrier_min_distance_s":.004,"carrier_min_peaks":20,
        "carrier_p2p_floor":.05,"carrier_agreement_hz":2.0,"carrier_cv_max":.2}
    carrier_results={}
    for name,y,expected in [("true_60_hz",np.cos(2*np.pi*60*t),True),
        ("beta_22_plus_gamma_harmonic",np.cos(2*np.pi*22*t)+.6*np.cos(2*np.pi*44*t),False)]:
        fq,power=braintools.metric.power_spectral_density(y,.001*u.second,nperseg=2000)
        features=analysis.carrier_features(y,t,np.asarray(fq),np.asarray(power),carrier_cfg)
        assert features["autonomous_gamma_predicate"]==expected
        carrier_results[name]={k:v for k,v in features.items() if k!="peak_times_s"}
    checks["carrier_true_and_harmonic_negative_controls"] = carrier_results
    checks["first_jit_end_to_end_s"] = cold
    checks["status"] = "PASS"
    Path("checks/verification.json").write_text(json.dumps(checks,indent=2))
    print(json.dumps(checks,indent=2),flush=True)


if __name__ == "__main__":
    verify()

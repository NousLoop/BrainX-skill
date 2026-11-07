"""Focused scientific/numerical checks; results saved by the CLI."""
import json
from pathlib import Path
import numpy as np
import scipy.signal
import brainstate
import brainunit as u
import braintools
import model
import analysis


def checks():
    out={}
    node=model.build([1.0])
    brainstate.nn.init_all_states(node,batch_size=1)
    E,I,P=.12,.08,1.2
    FE=1/(1+np.exp(-1.2*(16*E-12*I+P-2.8)))-1/(1+np.exp(1.2*2.8))
    FI=1/(1+np.exp(-(15*E-3*I-4)))-1/(1+np.exp(4))
    expected=[(-E+(1-E)*FE)/4,(-I+(1-I)*FI)/8]
    actual=[float(np.asarray(node.drE(E,I,P).to_decimal(u.kHz)).ravel()[0]),float(np.asarray(node.drI(I,E,0.).to_decimal(u.kHz)).ravel()[0])]
    assert np.allclose(actual,expected,atol=1e-12), (actual,expected)
    out['equations_per_ms']={'actual':actual,'expected':expected}
    tiny=model.simulate([1.],[0.],P,dt_ms=1e-4,duration_s=1e-7,burn_s=0,initial=((E,I),))
    step_derivative=[(tiny['final_E'][0,0]-E)/1e-4,(tiny['final_I'][0,0]-I)/1e-4]
    assert np.allclose(step_derivative,expected,atol=1e-6)
    out['one_step_derivative_witness_per_ms']=np.asarray(step_derivative).tolist()
    a=model.simulate([1.,1.1],[0.,.6],1.2,duration_s=.02,burn_s=0,initial=((.1,.1),(.12,.08)),jit=True)
    b=model.simulate([1.,1.1],[0.,.6],1.2,duration_s=.02,burn_s=0,initial=((.1,.1),(.12,.08)),jit=False)
    for k in ['rE','rI','final_E','final_I','t_s']:
        assert np.allclose(a[k],b[k],atol=1e-12),k
    assert a['rE'].shape==(20,2,2)
    assert np.allclose(a['t_s'],np.arange(20)*.001+.0001)
    assert np.allclose(a['input_E_left'][:,1],1.2+.6*np.cos(2*np.pi*6*(a['t_s']-.0001)))
    # Reset witness: a fresh identical run must replay exactly.
    c=model.simulate([1.,1.1],[0.,.6],1.2,duration_s=.02,burn_s=0,initial=((.1,.1),(.12,.08)))
    assert np.array_equal(a['rE'],c['rE'])
    out['state_shape_reset_time']={'shape':list(a['rE'].shape),'first_post_update_s':float(a['t_s'][0]),'reset_exact':True}
    # Native conditions are independent: vector lane equals scalar execution.
    d=model.simulate([1.1],[.6],1.2,duration_s=.02,burn_s=0,initial=((.12,.08),))
    assert np.allclose(a['rE'][:,1,1],d['rE'][:,0,0],atol=1e-12)
    out['native_scalar_and_jit_parity']=True
    t=np.arange(14000)*.001
    phi=2*np.pi*6*t
    x=(1+.6*np.cos(phi))*np.cos(2*np.pi*50*t)
    amp,filt=analysis.envelope(x,.001)
    ref=scipy.signal.sosfiltfilt(scipy.signal.butter(4,[25,90],btype='bandpass',fs=1000,output='sos'),x)
    err=float(np.max(np.abs(filt-ref)));assert err<1e-9
    keep=(t>=3)&(t<13)
    pm=analysis.phase_metrics(amp[keep],phi[keep]); null,_,counts=analysis.cycle_surrogates(amp[keep],phi[keep])
    assert .28<float(pm['R'])<.32
    assert float(pm['R'])>np.quantile(null,.95)
    ca,_=analysis.envelope(np.cos(2*np.pi*50*t),.001)
    zero=analysis.phase_metrics(ca[keep],phi[keep])
    assert float(zero['R'])<.005
    assert counts.size==60 and counts.min()>=166
    out['metric_controls']={'AM_expected_R':.3,'AM_measured_R':float(pm['R']),'constant_R':float(zero['R']),'null95':float(np.quantile(null,.95)),'filter_max_error_vs_scipy':err,'cycles':int(counts.size)}
    # A global phase shift cannot be a PAC-magnitude null.
    shifted=analysis.phase_metrics(amp[keep],phi[keep]+1.23)
    assert abs(float(shifted['R'])-float(pm['R']))<1e-12
    out['global_shift_invariance']=True
    sample=amp[keep][:500]
    sample_phase=phi[keep][:500]
    exact,shifts,_=analysis.cycle_surrogates(sample,sample_phase,n=3)
    cycles=np.floor((sample_phase+1e-8)/(2*np.pi)).astype(int)
    brute=[]
    for n in range(3):
        z=0j
        for j,c in enumerate(np.unique(cycles)):
            ck=cycles==c
            z+=np.sum(np.roll(sample[ck],shifts[n,j])*np.exp(1j*sample_phase[ck]))
        brute.append(abs(z)/sample.sum())
    assert np.allclose(exact,brute,atol=1e-12)
    out['surrogate_exact_rotation_max_error']=float(np.max(np.abs(exact-brute)))
    # Exact shared observation noise across conditions.
    obs=analysis.observations(a,[11,23])
    assert np.allclose(obs['eeg']-obs['latent'],np.broadcast_to(obs['theta']+obs['noise'],a['rE'].shape))
    out['paired_observation_contract']=True
    out['PASS']=True
    return out

if __name__=='__main__':
    result=checks()
    Path('evidence/tests.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))

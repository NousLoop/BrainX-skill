"""Immutable-run entry point. No scientific settings selected from modulation outcomes."""
import argparse
import json
from pathlib import Path
import resource
import time
import numpy as np
import model
import analysis


def dump(path, value):
    Path(path).write_text(json.dumps(value,indent=2,allow_nan=False))


def save(path, result):
    np.savez_compressed(path,**result)


def run(config, root):
    stage=config['stage']; start=time.perf_counter()
    if stage=='calibration':
        drives=np.repeat(config['calibration_drives'],3)
        gains=np.tile(config['calibration_gains'],len(config['calibration_drives']))
        raw=model.simulate(gains,np.zeros(len(gains)),drives,duration_s=4,burn_s=2)
        save(root/'raw/calibration.npz',raw)
        E=raw['rE'][:,0,:]; amp,_=analysis.envelope(E,.001)
        f,p=analysis.psd(E,.001)
        frequency=f[(f>=1)&(f<=150)][np.argmax(p[(f>=1)&(f<=150)],axis=0)]
        sd=E[len(E)//2:].std(axis=0)
        ratio=E[3*len(E)//4:].std(axis=0)/np.maximum(E[len(E)//2:3*len(E)//4].std(axis=0),1e-15)
        rms=np.sqrt(np.mean(amp[len(E)//2:]**2,axis=0)/2)
        eligible=(sd>.005)&(frequency>=25)&(frequency<=90)&(ratio>=.8)&(ratio<=1.25)
        save(root/'metrics/calibration.npz',dict(drives=drives,gains=gains,frequency_Hz=frequency,sd=sd,ratio=ratio,gamma_rms=rms,eligible=eligible,f=f,psd=p))
        if eligible.any():
            best=int(np.argmax(np.where(eligible,rms,-np.inf)))
            selection=dict(drive=float(drives[best]),base_gain=float(gains[best]),index=best,gamma_Hz=float(frequency[best]),gamma_rms=float(rms[best]),eligible_count=int(eligible.sum()))
            dump(root/'selection.json',selection); print('CALIBRATION',selection,flush=True)
        else:
            dump(root/'selection.json',{'failed':True,'reason':'No preregistered eligible unmodulated gamma candidate'})
            raise RuntimeError('No eligible baseline; preserve failure and stop')
    else:
        depths=np.repeat(config['depths'],len(config['relative_gains']))
        gains=np.tile(config['relative_gains'],len(config['depths']))
        raw=model.simulate(config['base_gain']*gains,depths,config['drive'],
                           duration_s=config['duration_s'],burn_s=config['burn_s'],initial=config['initial'])
        raw.update(depth=depths,relative_gain=gains,absolute_gain=config['base_gain']*gains,
                   grid_shape=np.asarray([len(config['depths']),len(config['relative_gains'])]),
                   depth_axis=np.asarray(config['depths']),gain_axis=np.asarray(config['relative_gains']),
                   initial=np.asarray(config['initial']))
        save(root/'raw/trajectories.npz',raw)
        print('SIMULATION',raw['rE'].shape,'seconds',raw['elapsed_s'],flush=True)
        if stage=='smoke':
            assert np.isfinite(raw['rE']).all() and np.isfinite(raw['rI']).all()
            dump(root/'metrics/smoke.json',{'finite':True,'shape':list(raw['rE'].shape),'elapsed_s':raw['elapsed_s']})
        else:
            obs,metrics=analysis.analyze(raw,config['observation_seeds'])
            save(root/'raw/observations.npz',obs)
            save(root/'metrics/analysis.npz',metrics)
            # Independent baseline validity at every nuisance gain and sensitivity lane.
            n_gain=len(config['relative_gains']); n_depth=len(config['depths'])
            f=metrics['frequency_Hz']; p=metrics['psd_E']
            broad_peak=f[(f>=1)&(f<=150)][np.argmax(p[(f>=1)&(f<=150)],axis=0)]
            baseline_valid=(metrics['gamma_rms'][:,:n_gain,0]>.005)&(broad_peak[:,:n_gain]>=25)&(broad_peak[:,:n_gain]<=90)
            repeated=np.tile(baseline_valid,(1,n_depth))
            controlR=np.tile(metrics['R'][:,:n_gain,2],(1,n_depth))
            delta=metrics['R'][...,2]-controlR
            nested=repeated&(metrics['gamma_rms'][...,0]>.005)&(delta>.05)&(metrics['R'][...,2]>metrics['null95'][...,2])
            save(root/'metrics/decision.npz',dict(broad_peak_Hz=broad_peak,baseline_valid=baseline_valid,delta_R=delta,nested=nested))
            # Declared refinement at every gain, three fixed depths, lane zero.
            conv_depth=np.repeat([0.,.6,1.],n_gain); conv_gain=np.tile(config['relative_gains'],3)
            refined=model.simulate(config['base_gain']*conv_gain,conv_depth,config['drive'],dt_ms=.05,initial=[config['initial'][0]])
            save(root/'raw/refinement.npz',refined)
            _,cm=analysis.analyze(refined,[config['observation_seeds'][0]])
            save(root/'metrics/refinement.npz',cm)
            lookup=[int(np.flatnonzero(np.isclose(depths,d)&np.isclose(gains,g))[0]) for d,g in zip(conv_depth,conv_gain)]
            amp0=metrics['gamma_rms'][0,lookup,0]; amp1=cm['gamma_rms'][0,:,0]
            relevant=amp0>.005
            relerr=np.abs(amp1-amp0)/np.maximum(amp0,1e-15)
            freqerr=np.abs(cm['gamma_peak_Hz'][0]-metrics['gamma_peak_Hz'][0,lookup])
            Rerr=np.abs(cm['R'][0,:,2]-metrics['R'][0,lookup,2])
            passed=((~relevant)|((relerr<.05)&(freqerr<2)))&(Rerr<.03)
            save(root/'metrics/convergence.npz',dict(depth=conv_depth,gain=conv_gain,coarse_indices=lookup,
                 gamma_relative_error=relerr,frequency_error_Hz=freqerr,R_abs_error=Rerr,relevant=relevant,passed=passed))
            # Invariant bounds of documented offset-sigmoid/refractory equations.
            domains=[]
            for key,a,theta in [('rE',1.2,2.8),('rI',1.,4.)]:
                c=1/(1+np.exp(a*theta)); lo=-c/(1-c);hi=(1-c)/(2-c)
                assert np.isfinite(raw[key]).all()
                ok=bool(raw[key].min()>=lo-1e-8 and raw[key].max()<=hi+1e-8)
                domains.append(dict(state=key,min=float(raw[key].min()),max=float(raw[key].max()),lower=lo,upper=hi,passed=ok))
            display=int(np.flatnonzero(np.isclose(depths,.6)&np.isclose(gains,1))[0])
            ctrl=int(np.flatnonzero(np.isclose(depths,0)&np.isclose(gains,1))[0])
            display_pass=nested[:,display]
            valid=bool(passed.all() and all(d['passed'] for d in domains))
            if not valid: outcome='invalid'
            elif display_pass.all(): outcome='supported'
            elif display_pass.any(): outcome='partially_supported'
            else: outcome='refuted'
            summary=dict(scientific_outcome=outcome,numerically_valid=valid,display_index=display,control_index=ctrl,
                 display_R=metrics['R'][:,display,2].tolist(),control_R=metrics['R'][:,ctrl,2].tolist(),
                 display_delta_R=delta[:,display].tolist(),display_null95=metrics['null95'][:,display,2].tolist(),
                 display_latent_R=metrics['R'][:,display,1].tolist(),display_eonly_R=metrics['R'][:,display,3].tolist(),
                 leakage_R=metrics['R'][:,display,4].tolist(),display_gamma_peak_Hz=metrics['gamma_peak_Hz'][:,display].tolist(),
                 control_gamma_peak_Hz=metrics['gamma_peak_Hz'][:,ctrl].tolist(),
                 display_gamma_rms_E=metrics['gamma_rms'][:,display,0].tolist(),
                 display_nested=display_pass.tolist(),baseline_valid=baseline_valid.tolist(),
                 nested_counts_per_lane=nested.sum(axis=1).tolist(),
                 convergence=dict(all_passed=bool(passed.all()),count=int(passed.size),
                  max_gamma_relative_error=float(relerr[relevant].max()) if relevant.any() else 0.,
                  max_frequency_error_Hz=float(np.nanmax(freqerr)) if np.isfinite(freqerr).any() else 0.,
                  max_R_abs_error=float(Rerr.max())),domains=domains)
            dump(root/'metrics/summary.json',summary)
            print('ASSESSMENT',json.dumps(summary),flush=True)
    dump(root/'metrics/resources.json',dict(elapsed_s=time.perf_counter()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--config',required=True);args=parser.parse_args()
    config_path=Path(args.config).resolve();run(json.loads(config_path.read_text()),config_path.parent)

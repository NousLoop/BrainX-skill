"""Fixed-case scientific figures. Final mode requires a preserved PASS review."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import brainmass

ROOT=Path(__file__).resolve().parent

def render(run,mode):
    if mode=='final':
        gate=json.loads((ROOT/'reviews/gate.json').read_text())
        assert gate['verdict']=='PASS' and gate['run_id']==run.name
    raw=np.load(run/'raw/trajectories.npz');obs=np.load(run/'raw/observations.npz')
    met=np.load(run/'metrics/analysis.npz');dec=np.load(run/'metrics/decision.npz')
    summary=json.loads((run/'metrics/summary.json').read_text())
    ids=[summary['control_index'],summary['display_index']]
    labels=['No modulation: m=0','Theta modulation: m=0.6']
    t=raw['t_s']; k=(t>=3)&(t<3.8)
    exports=[]
    def export(fig,name):
        fig.suptitle(('DIAGNOSTIC / unaccepted — ' if mode=='diagnostic' else '')+name,fontsize=13)
        fig.tight_layout()
        for ext in ['png','pdf']:
            path=ROOT/'figures'/f'{mode}_{name}.{ext}'
            fig.savefig(path,dpi=220,bbox_inches='tight');exports.append(path)
        plt.close(fig)
    fig,ax=plt.subplots(4,2,figsize=(12,9),sharex=True,squeeze=False)
    for col,idx in enumerate(ids):
        brainmass.viz.plot_timeseries(np.column_stack([raw['rE'][k,0,idx],raw['rI'][k,0,idx]]),ts=t[k],labels=['E','I'],ax=ax[0,col])
        ax[0,col].set(title=labels[col],xlabel='',ylabel='Population activity',ylim=(-.04,.52))
        ax[1,col].plot(t[k],raw['input_E_monitor'][k,idx],color='0.25')
        ax[1,col].set(ylabel='E input (dimensionless)',ylim=(0,4))
        ax[2,col].plot(t[k],obs['eeg'][k,0,idx],color='#0072B2',lw=.8)
        ax[2,col].set(ylabel='Synthetic EEG proxy (a.u.)',ylim=(-.65,.65))
        ax[3,col].plot(t[k],met['envelope'][k,0,idx,2],color='#D55E00',label='25–90 Hz envelope')
        ax[3,col].plot(t[k],.15*(1+np.cos(2*np.pi*6*t[k])),color='0.5',ls='--',label='Theta phase guide')
        ax[3,col].set(xlabel='Time (s)',ylabel='Envelope / guide (a.u.)',ylim=(0,.4))
        ax[3,col].legend(fontsize=8,loc='upper right')
    export(fig,'traces')
    fig,ax=plt.subplots(2,2,figsize=(11,7))
    phase=met['bin_centers']
    for idx,label,style,color in zip(ids,labels,['--','-'],['#0072B2','#D55E00']):
        profile=met['profile'][:,0,idx,2]
        ax[0,0].plot(phase,profile,ls=style,color=color,marker='o',label=f'{label}; R={met["R"][0,idx,2]:.3f}')
        ax[0,1].plot(phase,profile/profile.mean(),ls=style,color=color,marker='o',label=label)
        ax[1,0].semilogy(met['frequency_Hz'],np.maximum(met['psd_E'][:,0,idx],1e-14),ls=style,color=color,label=label)
        ax[1,1].semilogy(met['frequency_Hz'],np.maximum(met['psd_eeg'][:,0,idx],1e-14),ls=style,color=color,label=label)
    idx=ids[1]; ep=met['profile'][:,0,idx,3]
    ax[0,1].plot(phase,ep/ep.mean(),color='0.3',ls=':',label='m=0.6, E-only observation')
    ax[0,0].set(title='Known theta phase → gamma envelope',xlabel='Theta phase (rad; 0 = drive maximum)',ylabel='Mean envelope (a.u.)',xlim=(-np.pi,np.pi),ylim=(0,.4))
    ax[0,1].set(title='Envelope shape / observation sensitivity',xlabel='Theta phase (rad)',ylabel='Envelope / phase-bin mean',xlim=(-np.pi,np.pi),ylim=(0,3))
    for a,title in zip(ax[1],['Latent E spectrum','Synthetic EEG proxy spectrum']):
        a.set(title=title,xlabel='Frequency (Hz)',ylabel='PSD (a.u.²/Hz)',xlim=(0,120),ylim=(1e-10,1e-1))
    for a in ax.flat:a.legend(fontsize=8)
    export(fig,'phase_and_spectra')
    fig,ax=plt.subplots(2,2,figsize=(11,8))
    depth=raw['depth_axis'];gain=raw['gain_axis'];shape=tuple(raw['grid_shape'])
    def edges(x):return np.r_[x[0]-(x[1]-x[0])/2,(x[1:]+x[:-1])/2,x[-1]+(x[-1]-x[-2])/2]
    values=[met['R'][0,:,2],dec['delta_R'][0],met['gamma_rms'][0,:,0],dec['nested'][0].astype(float)]
    titles=['EEG proxy: normalized PAC R','Paired ΔR relative to m=0 at same gain','Latent E: gamma-band RMS','Declared nesting predicate (0 / 1)']
    limits=[(0,1),(-1,1),(0,.25),(0,1)]
    cmaps=['viridis','RdBu_r','viridis','Greys']
    for a,z,title,lim,cmap in zip(ax.flat,values,titles,limits,cmaps):
        im=a.pcolormesh(edges(gain),edges(depth),z.reshape(shape),vmin=lim[0],vmax=lim[1],cmap=cmap,shading='flat')
        fig.colorbar(im,ax=a,label=title.split(':')[-1])
        a.set(title=title,xlabel='Relative recurrent loop gain',ylabel='Modulation depth m',xticks=gain,yticks=depth)
        invalid=np.tile(~dec['baseline_valid'][0],shape[0]).reshape(shape)
        yy,xx=np.where(invalid)
        a.scatter(gain[xx],depth[yy],marker='x',c='red',s=18,label='Baseline lacks gamma')
        a.legend(fontsize=7,loc='upper left')
    export(fig,'parameter_sweep')
    # Figure-value contract: fixed case / masks / timing / exact plotted matrices.
    np.savez_compressed(ROOT/'figures'/f'{mode}_plotted_values.npz',display_indices=ids,trace_times=t[k],
        phase=phase,profile=met['profile'][:,0,ids,:],map_R=values[0].reshape(shape),map_delta_R=values[1].reshape(shape),
        map_gamma_rms=values[2].reshape(shape),map_nested=values[3].reshape(shape),depth=depth,gain=gain)
    manifest=['# Figure manifest','',f'- Evidence mode: {mode}; work type: create. Run: {run.name}.',
       '- Figures: illustrative model results, not experimental EEG.',
       '- Statistical unit: three deterministic initial-State/paired observation-seed lanes; figures show prespecified lane 0 (seed 11), no population uncertainty inferred.',
       '- Display cases fixed before production. After the first diagnostic render exposed clipping at R=0.5, R/ΔR color limits were expanded to their full theoretical ranges [0,1]/[−1,1], before review. First renders retained in figures/first-render. No interpolation between sweep samples.',
       '- PNG 220 dpi and PDF vector exports. Plotting source: plot_results.py. Source-value bundle: figures/'+mode+'_plotted_values.npz.',
       '- Source SHA256: trajectories '+hashlib.sha256((run/'raw/trajectories.npz').read_bytes()).hexdigest(),
       '- Source SHA256: analysis '+hashlib.sha256((run/'metrics/analysis.npz').read_bytes()).hexdigest(),
       '- Acceptance: '+('PASS scope in reviews/gate.json' if mode=='final' else 'unaccepted, diagnostic only'),
       '- Render inspection: pending; to be appended after image inspection.','']
    for name,role in [('traces','Aligned E/I, executed drive, synthetic EEG and gamma envelope at 3–3.8 s. 1 ms point sampling. Proxy E−0.5I is post-burn mean-centered, plus supplied theta and paired noise. Theta guide is scaled for visibility, not data.'),('phase_and_spectra','3–13 s, 60 theta cycles. 18 phase-bin mean gamma envelopes, normalized by each profile mean only in the labeled panel. Welch PSD 2 s windows/1 s overlap; no condition-specific PSD normalization.'),('parameter_sweep','Exact 7×7 sampled grid for lane 0, gain columns and nonuniform depth rows. X marks a matched unmodulated baseline lacking gamma. Values are retained even in marked cells; categorical panel uses full fixed predicate and does not force any category.')]:
        manifest.extend(['## '+mode+'_'+name,'- Question / scientific role: '+role,'- Axes and units: labeled in plot; E/I/input dimensionless, proxy a.u., phase rad, time s, frequency Hz.','- Reductions: lane 0 only; no smoothing beyond stated bandpass/envelope and Welch analysis, no failed samples excluded.','- Fixed controls: m=0 at identical gain and initial State; paired observation noise.','- Outputs: '+', '.join(str(p.relative_to(ROOT)) for p in exports if name in p.name),''])
    (ROOT/'FIGURE_MANIFEST.md').write_text('\n'.join(manifest))
    print('\n'.join(str(p) for p in exports))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run',default='production-01');p.add_argument('--mode',choices=['diagnostic','final'],default='diagnostic');a=p.parse_args()
    render(ROOT/'runs'/a.run,a.mode)

"""Reproducible evidence plots; diagnostic until the independent review passes."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import braintools
import analysis


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def draw_four_conditions(root,gaps):
    sample=np.load(root/'sample_neuron_ids.npy')
    data={}
    # Exactly one two-row/four-column figure, each rate above its raster.
    fig,axes=plt.subplots(2,4,figsize=(18,6),sharex='col',height_ratios=[1,1.15])
    for c,(g,eta) in enumerate(analysis.PAIRS):
        r=dict(g=g,eta=eta,requested=analysis.TARGETS[c])
        raw_path=root/'raw'/f'condition{c}_seed101_dt0.1.npz'
        z=np.load(raw_path);packed=z['packed'];counts=z['counts'];n=int(z['ne']+z['ni'])
        t=np.arange(35001,40001)*.1
        rate=counts[35000:40000].sum(axis=1)/(n*.0001)
        chosen=((packed[35000:40000,sample//8] >> (sample%8))&1).astype(bool)
        ti,ids=np.nonzero(chosen)
        assert int(chosen.sum())==len(ti)
        assert np.isclose(rate.mean(),counts[35000:40000].sum()/n/.5)
        axes[0,c].plot(t,rate,color='#1f628b',linewidth=.55)
        axes[0,c].axhline(rate.mean(),color='black',linestyle='--',linewidth=1,label=f'mean {rate.mean():.1f} Hz')
        axes[0,c].set_title(f"(g, eta) = ({r['g']:g}, {r['eta']:g})\nRequested: {r['requested']}",fontsize=11)
        axes[0,c].set(ylabel='Global rate (Hz/neuron)',ylim=(0,max(1,rate.max()*1.08)),xlim=(3500,4000))
        axes[0,c].legend(fontsize=8,loc='upper right')
        try:
            braintools.visualize.spike_raster(t[ti],ids,ax=axes[1,c])
        except (AttributeError,TypeError) as e:
            gaps.append('spike_raster unavailable/incompatible: '+str(e))
            axes[1,c].clear();axes[1,c].scatter(t[ti],ids,s=2,marker='|',color='black',linewidths=.4)
        axes[1,c].set(xlabel='Time (ms)',ylabel='Fixed neuron sample',xlim=(3500,4000),ylim=(-.5,49.5))
        data[f'c{c}_display_t_ms']=t;data[f'c{c}_display_global_Hz']=rate
        data[f'c{c}_raster_t_ms']=t[ti];data[f'c{c}_raster_sample_row']=ids
    data['sample_neuron_ids']=sample
    return fig,data



def main(run_dir,mode,out_dir=None):
    root=Path(run_dir);out=Path(out_dir) if out_dir else Path('figures')/mode
    out.mkdir(parents=True,exist_ok=True)
    assessment=json.loads((root/'assessment.json').read_text())
    if mode=='final':
        acceptance=json.loads(Path('reviews/acceptance.json').read_text())
        assert acceptance['verdict']=='PASS' and Path(acceptance['run_dir']).resolve()==root.resolve()
        assert sha(acceptance['review_file'])==acceptance['review_sha256']
    sample=np.load(root/'sample_neuron_ids.npy')
    assert len(sample)==50 and len(np.unique(sample))==50
    data={};manifest=[];gaps=[]
    all_stats=[]
    for r in assessment:all_stats.extend(r['baseline']+[r['control']])
    fields=[k for k,v in all_stats[0].items() if isinstance(v,(int,float,str,bool)) or v is None]
    with (root/'metrics_summary.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');writer.writeheader();writer.writerows(all_stats)
    population_rates={}
    for s in all_stats:
        stem=f"condition{s['condition']}_seed{s['seed']}_dt{s['dt_ms']}"
        z=np.load(root/'raw'/(stem+'.npz'))
        counts=z['counts'];dt=float(z['dt_ms'])
        population_rates[stem+'_time_ms']=(np.arange(len(counts))+1)*dt
        population_rates[stem+'_E_Hz']=counts[:,0]/(10000*dt/1000)
        population_rates[stem+'_I_Hz']=counts[:,1]/(2500*dt/1000)
    np.savez_compressed(root/'population_rates.npz',**population_rates)
    def export(fig,name,description):
        fig.suptitle(('DIAGNOSTIC — unaccepted evidence | ' if mode=='diagnostic' else '')+description,fontsize=13)
        fig.tight_layout(rect=(0,0,1,.92))
        target=out/name;fig.savefig(target,dpi=200,bbox_inches='tight');plt.close(fig)
        manifest.append(dict(path=str(target.resolve()),source_run=str(root.resolve()),sha256=sha(target),bytes=target.stat().st_size,
            mode=mode,description=description,dpi=200))

    fig,main_data=draw_four_conditions(root,gaps)
    data.update(main_data)
    export(fig,'four_conditions.png','Global rate (0.1-ms bins; independent rate scales) and fixed 50-neuron raster | seed 101')

    fig,axes=plt.subplots(1,4,figsize=(15,4))
    colors=['#225e8a','#c25a14','#557d32']
    for c,r in enumerate(assessment):
        for j,s in enumerate(r['baseline']):
            axes[c].plot([0,1],[s['E_rate_Hz'],s['I_rate_Hz']],marker=['o','s','^'][j],
                color=colors[j],linewidth=.9,label=f"seed {s['seed']}")
        s=r['control'];axes[c].plot([0,1],[s['E_rate_Hz'],s['I_rate_Hz']],'k--x',label='seed101, dt=0.05 ms')
        maximum=max(s[k] for s in r['baseline']+[r['control']] for k in ['E_rate_Hz','I_rate_Hz'])
        axes[c].set(title=f"g={r['g']:g}, eta={r['eta']:g}",xticks=[0,1],xticklabels=['E','I'],ylabel='Mean rate (Hz/neuron)',ylim=(0,1.12*maximum))
        axes[c].legend(fontsize=7,loc='lower left')
    export(fig,'ei_rates.png','E/I rates | all three seeds and numerical control | analysis 1000–4000 ms')

    fig,axes=plt.subplots(1,4,figsize=(15,4))
    bins=np.linspace(0,5,101)
    for c,r in enumerate(assessment):
        groups=[[],[]]
        for s in r['baseline']:
            cv=np.load(root/'metrics'/f"condition{c}_seed{s['seed']}_dt0.1.npz")['CV']
            groups[0].append(cv[:10000]);groups[1].append(cv[10000:])
        groups=[np.concatenate(x) for x in groups]
        groups=[x[np.isfinite(x)] for x in groups]
        # Generic hist is the exact presentation boundary: shared explicit bins,
        # E/I line styles and overflow accounting; no fitted KDE or inference.
        for k,(vals,color,label,style) in enumerate(zip(groups,['#225e8a','#c25a14'],['E','I'],['-','--'])):
            axes[c].hist(vals,bins=bins,histtype='step',density=True,color=color,linestyle=style,
                linewidth=1.3,label=f'{label}: n={len(vals):,}')
            data[f'c{c}_CV_{label}']=vals
        overflow=sum(int(np.sum(x>5)) for x in groups)
        axes[c].axvline(.5,color='#555555',linestyle=':',linewidth=1)
        axes[c].axvline(.7,color='#555555',linestyle='--',linewidth=1)
        axes[c].set(title=f"g={r['g']:g}, eta={r['eta']:g}\nCV>5: {overflow}",xlabel='Individual ISI CV',ylabel='Density',xlim=(0,5))
        axes[c].legend(fontsize=8)
    export(fig,'isi_cv.png','ISI CV | all eligible neurons across three seeds | dotted 0.50 / dashed 0.70 cutoffs')

    fig,axes=plt.subplots(1,4,figsize=(16,4))
    for c,r in enumerate(assessment):
        for j,s in enumerate(r['baseline']+[r['control']]):
            suffix=f"condition{c}_seed{s['seed']}_dt{s['dt_ms']}"
            spectra=np.load(root/'metrics'/(suffix+'.npz'))
            f,p=spectra['welch_frequency_Hz'],spectra['welch_PSD_Hz2_per_Hz']
            label=f"{s['seed']}: {s['dominant_frequency_Hz']:.0f} Hz"
            if j==3:label='dt=0.05: '+f"{s['dominant_frequency_Hz']:.0f} Hz"
            axes[c].semilogy(f,np.where(p>0,p,np.nan),color=(colors+["black"])[j],
                linestyle=['-','--',':','-.'][j],linewidth=1 if j!=3 else .8,label=label)
            if j<3:
                pidx=np.argmin(np.abs(f-s['dominant_frequency_Hz']))
                axes[c].plot(f[pidx],p[pidx],marker=['o','s','^'][j],markersize=3,color=colors[j])
            data[suffix+'_welch_f_Hz']=f;data[suffix+'_welch_PSD']=p
        axes[c].set(title=f"g={r['g']:g}, eta={r['eta']:g}",xlabel='Frequency (Hz)',ylabel='Rate PSD ((Hz/neuron)²/Hz)',xlim=(1,500))
        axes[c].legend(fontsize=7,loc='lower right')
    export(fig,'global_rate_spectra.png','Global-rate spectra | Welch 1-s Hann windows, 50% overlap | maxima need not imply oscillations')

    fig,axes=plt.subplots(5,4,figsize=(16,13))
    names=['synchrony_S','CV_median','peak_concentration','peak_background_ratio','drift']
    ylabels=['Excess fractional modulation S','Median individual ISI CV','Power within peak ±2 Hz / band','Peak / median background','Max. half-window rate drift']
    cutoffs=[[.05,.10],[.5,.7],[.1],[5.],[.2]]
    for c,r in enumerate(assessment):
        stats=r['baseline']+[r['control']]
        for row,name in enumerate(names):
            values=[max(s['E_I_fractional_drift']) if name=='drift' else s[name] for s in stats]
            axes[row,c].plot(range(4),values,'o-',color='#225e8a',linewidth=.8)
            for value in cutoffs[row]:axes[row,c].axhline(value,color='black',linestyle='--',linewidth=.8)
            if row==0:
                for j,s in enumerate(stats):axes[row,c].plot([j,j],s['half_synchrony_S'],'x',color='#c25a14',markersize=4)
            if row==1:
                for j,s in enumerate(stats):
                    if s['CV_eligible_fraction']<.5:axes[row,c].annotate(f"eligible {s['CV_eligible_fraction']:.0%}",(j,values[j] or 0),xytext=(0,8),textcoords='offset points',ha='center',fontsize=6)
            if row==3:axes[row,c].set_yscale('log')
            else:axes[row,c].set_ylim(0,None)
            axes[row,c].set(xticks=range(4),xticklabels=['101','202','303','101 fine'],ylabel=ylabels[row])
            data[f'c{c}_{name}']=np.array(values)
        axes[0,c].set_title(f"g={r['g']:g}, eta={r['eta']:g}\n{r['decision']}")
    export(fig,'regime_tests.png','Frozen regime predicates | dots: full windows; synchrony crosses: halves | dashed: fixed thresholds')

    np.savez_compressed(out/'figure_data.npz',**data)
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2))
    (out/'plotting_api_notes.json').write_text(json.dumps(dict(gaps=gaps,
        histogram_boundary='Matplotlib hist used for exact shared bins, distinct E/I step styles and explicit overflow accounting; BrainTools distribution reference checked.'),indent=2))
    rows=['# Figure manifest','',f'Evidence mode: {mode}. Run: `{root.resolve()}`. '+
        ('Independent review pending; these figures are unaccepted diagnostic evidence.' if mode=='diagnostic' else 'Independent review PASS; final figures use the accepted scope.'),'',
        f'Exact run/config/source hashes: `{root}/manifest.json`, `{root}/environment.json`. Figure contract: `FIGURE_CONTRACT.md`. Plot source: `plot_results.py` (SHA256 '+sha('plot_results.py')+').',
        '',f'Exact plotted arrays: `{out}/figure_data.npz`. Complete population spike evidence and statistics remain in raw/metrics.']
    # Include preserved earlier diagnostics as well as the current export.
    roles={Path(m['path']).name:m['description'] for m in manifest}
    all_exports=[];known={}
    for saved in Path('figures').rglob('manifest.json'):
        for entry in json.loads(saved.read_text()):known[entry['path']]=entry
    for target in sorted(Path('figures').rglob('*.png')):
        prior=known.get(str(target.resolve()),{})
        all_exports.append(dict(path=str(target.resolve()),sha256=sha(target),bytes=target.stat().st_size,
            mode='final' if target.parent.name=='final' else 'diagnostic',
            source_run=prior.get('source_run',str(Path('runs/baseline-v1').resolve())),
            description=roles[target.name]))
    for m in all_exports:
        rows+=['',f"## {m['path']}",f"- Question: {m['description']}",
               f"- Evidence mode: {m['mode']}; earlier diagnostic exports are preserved and remain labeled unaccepted.",
               f"- Source: `{m['source_run']}`; four supplied conditions; baseline seeds 101/202/303, numerical control seed 101; no omitted runs.",
               '- Data/transformations, units, ordering, sampling and comparison settings: see frozen FIGURE_CONTRACT.md; no extra smoothing or data-selected cases.',
               '- Statistics: raw per-seed points; CV histograms are descriptive neuron distributions, not independent-replicate uncertainty; no confidence intervals.',
               f"- Export: PNG, 200 dpi; {m['bytes']} bytes; SHA256 `{m['sha256']}`.",
               '- Render/source checks: source assertions verify exact count/rate normalization, sample size/identity and endpoint times. Visual inspection recorded in report.md after rendering.']
    Path('FIGURE_MANIFEST.md').write_text('\n'.join(rows)+'\n')
    print(json.dumps(manifest,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run-dir',default='runs/iteration-2');p.add_argument('--mode',choices=['diagnostic','final'],default='diagnostic');p.add_argument('--out-dir')
    args=p.parse_args();main(args.run_dir,args.mode,args.out_dir)

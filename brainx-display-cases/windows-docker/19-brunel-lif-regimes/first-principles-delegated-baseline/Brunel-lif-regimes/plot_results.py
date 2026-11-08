"""Figures from saved evidence only; diagnostic until independent review passes."""
import argparse
import json
from pathlib import Path
import hashlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import braintools


def render(run_dir, mode, spectral_dir=None):
    run = Path(run_dir).resolve()
    output = run.parent.parent / ('figures' if mode == 'final' else 'diagnostic-figures')
    output.mkdir(exist_ok=True)
    rows = json.loads((run/'metrics.json').read_text())
    if mode == 'final':
        assert len(rows) == 16
    config = json.loads((run/'config.json').read_text())
    native_spectra=Path(spectral_dir).resolve() if spectral_dir else None
    sample = np.load(run/'sample_neurons.npy')
    sample = np.sort(sample)  # Preserve fixed selected identities, E before I.
    sources, checks = {}, []
    for row in rows:
        key = (row['seed'],row['dt_ms'],row['condition'])
        name = f"seed-{row['seed']}_dt-{row['dt_ms']:g}_condition-{row['condition']}"
        with np.load(run/'metrics'/f'{name}.npz') as original:
            data=dict(original)
        if native_spectra:
            with np.load(native_spectra/'metrics'/f'{name}.npz') as native:
                data['frequency_Hz']=native['frequency_Hz']
                data['PSD_Hz2_per_Hz']=native['PSD_Hz2_per_Hz']
        sources[key] = (row,data)
    accepted = 'Review passed' if mode == 'final' else 'Diagnostic — review pending'
    titles = [f"g={g:g}, η={eta:g}" for g,eta in config['conditions']]
    files = []
    # Exactly one subplots composition for each figure.
    fig, axes = plt.subplots(4, 2, figsize=(14, 10), sharex=True,
                             gridspec_kw={'height_ratios':[1,1.35,1,1.35]})
    for ci in range(4):
        row, data = sources[(11,.1,ci)]
        r, c = (ci//2)*2, ci%2
        rate_ax, raster_ax = axes[r,c], axes[r+1,c]
        counts = data['counts_EI'][:5000].sum(axis=1)
        rate = counts / (12500*.0001)
        times = 1000 + (np.arange(5000)+1)*.1
        rate_ax.plot(times, rate, color='#223d55', lw=.65)
        # The supplied bin values are plotted directly, without smoothing.
        assert np.allclose(rate_ax.lines[0].get_ydata(), rate)
        rate_ax.axhline(row['global_Hz'],ls='--',color='#bf4a23',lw=1.2,
                        label=f"full-window mean {row['global_Hz']:.1f} Hz")
        rate_ax.set(title=f"{chr(65+ci)}  {titles[ci]}",ylabel='Global rate (Hz/neuron)')
        rate_ax.legend(fontsize=8,loc='upper right')
        rate_ax.set_ylim(bottom=0)
        with np.load(run/row['raw_file']) as raw:
            packed = raw['spikes_packed'][:5000]
            chosen = ((packed[:,sample//8] >> (sample%8)) & 1).astype(bool)
        ti, neuron = np.nonzero(chosen)
        event_times = 1000+(ti+1)*.1
        braintools.visualize.spike_raster(event_times, neuron, ax=raster_ax)
        raster_ax.set(xlabel='Time (ms)',ylabel='Fixed sample neuron (0–49)',
                      xlim=(1000,1500),ylim=(-1,50))
        raster_ax.set_title(f"Seed 11 · {row['label']} · peak {row['dominant_Hz']:.0f} Hz",fontsize=9)
        checks.append(dict(condition=ci,display_spike_count=int(chosen.sum()),
                           raster_events=len(event_times),samples=len(sample),
                           rate_mean_in_display=float(rate.mean()),
                           full_window_mean=row['global_Hz'],raw_rate_plot_exact=True))
    fig.suptitle(f'LIF population activity · 0.1 ms rate bins · {accepted}',fontsize=14)
    fig.tight_layout(rect=(0,0,1,.97))
    path=output/'four_conditions.png';fig.savefig(path,dpi=220);plt.close(fig);files.append(path)
    if len(rows) < 16:
        (output/'source_checks.json').write_text(json.dumps(checks,indent=2))
        (output/'FIGURE_MANIFEST.md').write_text(
            f'# Figure manifest\n\nEvidence mode: diagnostic; review pending.\n'
            f'four_conditions.png uses four complete primary runs at seed 11 from {run}.\n'
            'Raw 0.1 ms rates above the same fixed 50-neuron sample, 1000–1500 ms. '
            'Dashed full-window means; no smoothing. 14 × 10 inches, 220 dpi. '
            'Other seeds and numerical checks remain in progress.\n')
        print(str(path));return

    fig, axes = plt.subplots(1, 2, figsize=(11,4.2),sharex=True)
    for pop, ax in zip(['E','I'],axes):
        for si,seed in enumerate([11,29,47]):
            vals=[sources[(seed,.1,c)][0][f'{pop}_Hz'] for c in range(4)]
            ax.plot(np.arange(4),vals,marker=['o','s','^'][si],label=f'Seed {seed}',lw=1)
        ax.set(ylabel=f'{pop} firing rate (Hz/neuron)',xticks=np.arange(4),xticklabels=titles)
        ax.tick_params(axis='x',labelsize=8)
        ax.set_ylim(bottom=0);ax.legend(fontsize=8)
    fig.suptitle(f'E/I mean rates · three independent graph seeds · {accepted}')
    fig.tight_layout();path=output/'ei_rates.png';fig.savefig(path,dpi=220);plt.close(fig);files.append(path)

    fig, axes = plt.subplots(1, 4, figsize=(15,3.8),sharey=True)
    for ci,ax in enumerate(axes):
        for seed in [11,29,47]:
            cv=sources[(seed,.1,ci)][1]['ISI_CV']
            for pop,values,color,style in [('E',cv[:10000],'#2266aa','-'),('I',cv[10000:],'#bb4422','--')]:
                values=np.sort(values[np.isfinite(values)])
                ax.plot(values,np.arange(1,len(values)+1)/len(values),color=color,ls=style,
                        alpha=1 if seed==11 else .35,lw=1.4 if seed==11 else .7,
                        label=f'{pop} (seed 11)' if seed==11 else None)
        ax.axvline(.5,color='gray',ls=':',lw=.7);ax.axvline(.8,color='gray',ls=':',lw=.7)
        ax.set(title=titles[ci],xlabel='Per-neuron ISI CV',xlim=(0,None),ylim=(0,1))
        ax.legend(fontsize=8)
    axes[0].set_ylabel('Fraction of eligible neurons')
    fig.suptitle(f'ISI variability · ≥10 complete ISIs · each seed shown · {accepted}')
    fig.tight_layout();path=output/'isi_cv.png';fig.savefig(path,dpi=220);plt.close(fig);files.append(path)

    fig, axes=plt.subplots(2,2,figsize=(11,7),sharex=True)
    for ci,ax in enumerate(axes.flat):
        for seed in [11,29,47]:
            row,data=sources[(seed,.1,ci)]
            f,p=data['frequency_Hz'],data['PSD_Hz2_per_Hz']
            band=(f>=1)&(f<=1000)
            ax.semilogy(f[band],p[band],lw=1,label=f"Seed {seed}: {row['dominant_Hz']:.0f} Hz")
        ax.set(title=titles[ci],xlabel='Frequency (Hz)',ylabel='Rate PSD ((Hz/neuron)²/Hz)',
               xlim=(0,1000))
        ax.legend(fontsize=8)
    fig.suptitle(f'Global-rate spectrum · Welch 1 s Hann windows · {accepted}')
    fig.tight_layout();path=output/'global_rate_spectrum.png';fig.savefig(path,dpi=220);plt.close(fig);files.append(path)

    fig, axes=plt.subplots(2,2,figsize=(11,7),sharex=True)
    for ci,ax in enumerate(axes.flat):
        for dt,color in [(.1,'#2266aa'),(.05,'#bb4422')]:
            row,data=sources[(11,dt,ci)]
            counts=data['counts_EI'].sum(axis=1)
            width=round(10/dt)
            rate=counts.reshape(-1,width).sum(axis=1)/(12500*.01)
            times=1000+(np.arange(len(rate))+.5)*10
            ax.plot(times,rate,lw=.8,color=color,label=f'dt={dt:g} ms')
        ax.set(title=titles[ci],xlabel='Time (ms)',ylabel='10 ms mean rate (Hz/neuron)',
               xlim=(1000,4000),ylim=(0,None));ax.legend(fontsize=8)
    fig.suptitle(f'Numerical sensitivity · seed 11 · 10 ms diagnostic bins · {accepted}')
    fig.tight_layout();path=output/'step_halving.png';fig.savefig(path,dpi=220);plt.close(fig);files.append(path)

    (output/'source_checks.json').write_text(json.dumps(checks,indent=2))
    manifest=['# Figure manifest',f'Evidence mode: {mode}. {accepted}.',
              f'All figures derive exclusively from runs/{run.name}; plotting source: plot_results.py.',
              'Fixed display cases and windows follow NeuroSpecification.md. All raw runs remain available.']
    if native_spectra:
        manifest.append(f'Spectra use accepted-equivalent BrainTools reanalysis: {native_spectra}; parity.json verifies all bins, P, Q, peaks and labels. Original raw/count/CV sources remain the parent run.')
    for path in files:
        manifest.extend([f'\n## {path.name}',
          f'- Path: `{path}`; SHA256: `{hashlib.sha256(path.read_bytes()).hexdigest()}`.',
          f'- Work type: create; source run: {run.name}; PNG, 220 dpi.',
          '- Sampling units: three network/graph seeds for summary figures; fixed seed 11 and fixed 50 neurons for activity panels. No confidence interval claimed.',
          '- 1 s burn-in removed; raw rate uses 0.1 ms bins without smoothing; dashed mean uses the full 3 s observation. Main panel y scales are per-condition and labeled.',
          '- ISI CV includes neurons with ≥10 complete ISIs only; spectra use 1 s Hann Welch windows, 50% overlap, no fitted normalization; sensitivity plot explicitly uses 10 ms bins.',
          '- Source-value checks: source_checks.json and saved per-neuron metrics; render inspection required before delivery.'])
    (output/'FIGURE_MANIFEST.md').write_text('\n'.join(manifest)+'\n')
    print('\n'.join(str(p) for p in files))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--run',required=True)
    parser.add_argument('--mode',choices=['diagnostic','final'],default='diagnostic')
    parser.add_argument('--spectra')
    args=parser.parse_args();render(args.run,args.mode,args.spectra)

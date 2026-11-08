"""Compose a report from every frozen assessment; never infer a review verdict."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np


def span(values,digits=2):
    x=np.asarray(values,float)
    return f'{np.mean(x):.{digits}f} ({np.min(x):.{digits}f}–{np.max(x):.{digits}f})'


def main(run_dir='runs/iteration-2', diagnostic_dir='figures/iteration-2-diagnostic'):
    root=Path(run_dir)
    a=json.loads((root/'assessment.json').read_text())
    accept_path=Path('reviews/acceptance.json')
    acceptance=json.loads(accept_path.read_text()) if accept_path.exists() else {}
    accepted=(acceptance.get('verdict')=='PASS' and Path(acceptance['run_dir']).resolve()==root.resolve()
        and hashlib.sha256(Path(acceptance['review_file']).read_bytes()).hexdigest()==acceptance['review_sha256'])
    review='PASS' if accepted else 'pending'
    figure_dir='figures/final' if accepted else diagnostic_dir
    decisions=[r['decision'] for r in a]
    scientific='supported' if all(s=='supported' for s in decisions) else (
        'partially_supported' if 'supported' in decisions else ('inconclusive' if 'inconclusive' in decisions else 'refuted'))
    label='accepted' if accepted else 'provisional, unaccepted'
    rows=['# Current-based LIF network: independent exploration','',
        '- Report status: '+('final' if accepted else 'draft'),'- Scientific outcome: '+scientific,
        '- Review outcome: '+review,
        '- Research question: do the four supplied conditions support SR, fast SI, AI and slow SI, respectively?',
        '- Evidence available: all 12 baseline and 4 numerical-control runs; immutable code/config/environment; complete neuron spikes, graphs, raw spectra and individual CV; component/replay checks; inspected PNGs.',
        '- Missing evidence: '+('none within the specified experiment' if accepted else 'independent Codex acceptance'),
        '- Current conclusion: '+label+' finite-window evidence; see the condition decisions below.',
        '- Next action: '+('completed' if accepted else 'independent Codex code-and-results review'),'',
        'This is a first-principles experiment derived only from the supplied data. No papers, scientific example scripts, existing model implementations or remembered protocols were consulted. Installed skills and public API contracts were used only for package mechanics. The researcher explicitly delegated every unspecified choice, and [NeuroSpecification.md](NeuroSpecification.md) was locked before implementation or simulation. No scientific parameters, thresholds, seeds, durations or plotted cases were tuned after observing results.','',
        '| (g, eta) | Requested | E rate Hz | I rate Hz | Median ISI CV | Dominant frequency Hz | Frozen decision |',
        '|---|---|---|---|---|---|---|']
    for r in a:
        b=r['baseline']
        rows.append(f"| ({r['g']:g}, {r['eta']:g}) | {r['requested']} | {span([s['E_rate_Hz'] for s in b])} | {span([s['I_rate_Hz'] for s in b])} | {span([s['CV_median'] for s in b],3)} | {span([s['dominant_frequency_Hz'] for s in b],1)} | {r['decision']} |")
    rows+=['','Entries are means across three independent graph/input seeds, with the full min–max range in parentheses; these are descriptive ranges, not confidence intervals. Each CV entry first takes the median over eligible neurons within its run. A spectral maximum is always reported; it establishes an oscillation only when the frozen concentration and background tests also pass.','',
        '![Four conditions]('+figure_dir+'/four_conditions.png)','',
        'Each upper panel shows instantaneous global rate in unsmoothed 0.1-ms bins, in Hz per neuron, with its displayed-window mean dashed. Rate axes have independent numeric scales to keep low-rate conditions visible. Each lower panel shows the same randomly selected 50 neurons in the same order. All panels use seed 101 and 3500<t≤4000 ms; no spikes were jittered. The raster supports a visual comparison while the quantitative decisions use the entire post-burn 3 s and all neurons.','',
        '![E/I rates]('+figure_dir+'/ei_rates.png)','',
        f'E/I rates are post-burn means in Hz per neuron. Each connected pair is one matched graph/input seed; the dashed black pair is the seed101 fine-grid control. There are three independent baseline realizations, with no confidence interval implied. Complete native-grid E/I rate traces are saved in [population_rates.npz]({root}/population_rates.npz), and scalar rates in [metrics_summary.csv]({root}/metrics_summary.csv).','',
        '![ISI CV]('+figure_dir+'/isi_cv.png)','',
        'ISI CV histograms show all eligible E and I neurons across the three baseline seeds. CV is dimensionless; a neuron must have at least 20 complete post-burn ISIs. Histograms describe the neuron distributions and do not treat neurons as independent experimental replicates. Fixed 0.50/0.70 decision cutoffs are drawn; eligibility is retained for every seed.','',
        '![Spectra]('+figure_dir+'/global_rate_spectra.png)','',
        'Global-rate Welch spectra use one-second Hann windows with 50% overlap after removing the burn-in, at the actual 0.1-ms rate sampling interval. Frequency is in Hz and PSD in (Hz/neuron)²/Hz, plotted logarithmically. Every baseline seed and fine-grid control is shown; markers identify the baseline maxima within 1–500 Hz. Full-window periodograms are also saved.','',
        '![Frozen tests]('+figure_dir+'/regime_tests.png)','',
        'Rows show the exact continuous quantities used by the frozen categorical tests: excess fractional count modulation S, median CV, spectral concentration within ±2 Hz, peak/background ratio, and fractional half-window rate drift. Dashed lines are the fixed cutoffs; crosses in the synchrony row show each half separately. These panels expose threshold margins and unfavorable evidence.','',
        '## Per-run evidence','',
        '| g | eta | seed | dt ms | E/I rates Hz | S | median CV | eligible | f Hz | concentration | peak/background | stationary | requested outcome |',
        '|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for r in a:
        for s in r['baseline']+[r['control']]:
            cv='unavailable' if s['CV_median'] is None else f"{s['CV_median']:.3f}"
            rows.append(f"| {s['g']:g} | {s['eta']:g} | {s['seed']} | {s['dt_ms']} | {s['E_rate_Hz']:.2f}/{s['I_rate_Hz']:.2f} | {s['synchrony_S']:.3f} | {cv} | {s['CV_eligible_fraction']:.1%} | {s['dominant_frequency_Hz']:.0f} | {s['peak_concentration']:.3f} | {s['peak_background_ratio']:.1f} | {s['stationary']} | {s['baseline_outcome']} |")
    rows+=['','## Numerical sensitivity and regime decisions','',
        'Every condition was independently rerun at 0.05 ms for the same seed101 graph and initial voltage, for the same 4 s with the same 1 s burn-in. Its input is another discretization of the same Poisson law; paths are not coupled identically across the grids. The frozen test flags >10% E/I rate change, categorical change, or an excessive oscillatory peak shift. A flagged discrepancy withholds a grid-independent regime claim.','',
        '| Condition | Relative E/I rate changes | Category changes | Peak change Hz | Numerical flag | Final decision |',
        '|---|---|---|---|---|---|']
    for r in a:
        diffs=list(r['relative_rate_changes'].values())
        rows.append(f"| ({r['g']:g}, {r['eta']:g}) | {diffs[0]:.2%}/{diffs[1]:.2%} | {', '.join(r['changed_categories']) or 'none'} | {r['dominant_frequency_change_Hz']:.0f} | {r['numerical_sensitivity']} | {r['decision']} |")
    rows.append('')
    for r in a:
        for s in r['baseline']:
            if s['failed_predicates']:rows.append(f"\nSeed {s['seed']} at ({r['g']:g}, {r['eta']:g}) fails: {', '.join(s['failed_predicates'])}. Measured description: {s['measured_regime']}.\n")
    rows+=['','## Equations, checks and limits','',
        'Between events dV/dt=−V/(20 ms), with zero leak equilibrium as the reference for supplied voltages. At eligible endpoints add 0.1 mV per E/external event and −g×0.1 mV per I event, threshold at 20 mV, reset to 10 mV, and discard jumps during the 2-ms refractory interval. Recurrent events arrive exactly 1.5 ms after emission. The initial voltage is uniform on [10,20) mV; recurrent delay history is empty. All choices and the finite-grid ordering are explicit in the locked specification. The external source rate is 10 eta Hz per afferent, so exact superposition of 1000 afferents produces a Poisson count with expectation eta per 0.1-ms step. External input denotes stationary arrivals: a fixed transmission delay leaves their independent stationary Poisson law unchanged. This preserves independent shot noise and multiplicities.','',
        'The graph has 12,500 neurons, with exactly 1000 distinct E and 250 distinct I inputs per target, no autapses or duplicate edges, and 15,625,000 recurrent edges. Each graph and initial state are shared across its four conditions; different seeds have independent graphs, initial states and drive. BrainPy-State supplies native LIF population/projection interfaces; BrainEvent communicates sparse binary events; BrainUnit retains physical dimensions; BrainState owns State, RNG, delay and compilation.','',
        'Component checks verify exponential leak, signs, threshold/reset, exact refractory release and both-grid recurrent arrival. The compiled small-network path matches an independent explicit arithmetic reference spike-for-spike, with <0.00003 mV voltage error. Poisson mean/variance, multiple-event probability, cross-target correlation, dimensional mismatch rejection, full-size replay and worker-affinity parity pass. Synthetic metric fixtures verify 100-Hz periodic spikes yield exact rate, CV, S and spectral peak; they are explicitly separate from simulation evidence. Failed pre-production fixture/reset attempts and their corrections are retained.','',
        'Regimes here are operational finite-window labels at four sampled points. Three seeds do not establish parameter regions or biological realism. The 5-ms S statistic removes a Poisson counting floor but is a macroscopic modulation proxy; its interpretation is conditional on the fixed bin and 5%/10% thresholds. The CV cutoffs leave an explicit unresolved interval. The 50-Hz fast/slow boundary is derived from 1/tau_m and is an agent-chosen convention. A 3-s analysis window limits slow dynamics and CV eligibility, and the half-window checks do not establish arbitrary-time stationarity. Numerical controls test one finer grid at one seed, with independent discretized Poisson realizations; sensitivity is reported rather than tuned away.','',
        f'Actual runtime: CPU Linux Docker over a Windows-mounted workspace; exact interpreter, packages, OS/device identity and source hashes are in [environment.json]({root}/environment.json). Sparse event simulation is compiled as a whole rollout and independent baseline seeds run in three process-owned CPU groups; controls follow them. No approximate connectivity, downsizing, mean current substitution or omitted seeds were used.','',
        '## Evidence and independent review','',
        'Iteration 2 corrects analysis ownership and fixture preservation only. The documented BrainTools spectrogram now computes both frozen spectral estimators with physical units and float64 analysis precision. All 16 spectra and every metric/predicate/condition decision match the original saved evidence within recorded numerical tolerances. The raw spikes, model, graphs and frozen specification are unchanged. The original run, manifest, diagnostics and refusal remain intact in runs/baseline-v1 and reviews/iteration-1.md. New analyses and provenance are in '+str(root)+'. No new production simulation was needed.','',
        '- [Frozen specification](NeuroSpecification.md), [mechanics study](brainx-study-record.md), [acceleration](acceleration.md), [checks](checks/components.json), [full-size parity](checks/acceleration.json), [retained metric fixture](checks/metrics_fixture_v2/test_result.json)',
        f'- [Run/config contract]({root}/RUN_SPEC.md), [configuration]({root}/config.json), [run provenance and hashes]({root}/environment.json), [run manifest]({root}/manifest.json)',
        f'- [Assessment and claim-evidence matrix]({root}/assessment.md), [complete deterministic assessment]({root}/assessment.json), [raw file index](RAW_EVIDENCE.md)',
        '- [Figure manifest](FIGURE_MANIFEST.md), [figure contract](FIGURE_CONTRACT.md), [runnable instructions](README.md)',
        '- Independent review: '+(f"[verbatim Codex verdict]({acceptance['review_file']}); accepted scope recorded in [acceptance.json](reviews/acceptance.json)." if accepted else 'iteration 1 REFUSE preserved; iteration 2 pending; no final acceptance claimed.'),
        '- [Original review](reviews/iteration-1.md), [addressed findings](reviews/addressed-iteration-2.md), [mechanics restudy](brainx-study-record-iteration-2.md), [analysis parity]('+str(root)+'/spectral_parity.json), [analysis acceleration](acceleration-iteration-2.md)',
        '', 'PNG exports were checked for nonblank content, correct rates/event timing, legible labels and unclipped panel composition. Figure sources and hashes are recorded in the figure manifest.']
    Path('report.md').write_text('\n'.join(rows)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run-dir',default='runs/iteration-2');p.add_argument('--diagnostic-dir',default='figures/iteration-2-diagnostic')
    args=p.parse_args();main(args.run_dir,args.diagnostic_dir)

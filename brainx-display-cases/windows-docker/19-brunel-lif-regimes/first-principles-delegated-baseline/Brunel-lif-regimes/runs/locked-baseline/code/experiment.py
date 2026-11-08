"""Execute immutable configs and retain raw, bit-packed network spike evidence."""
import argparse
import csv
import hashlib
import json
import os
import platform
import sys
import time
from pathlib import Path

import brainstate
import brainunit as u
import jax
import jax.numpy as jnp
import numpy as np
import scipy.signal

import model


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False))


def assess(counts, cv, dt_ms, ne=model.NE, ni=model.NI):
    """Frozen statistics, entirely downstream of saved network spikes."""
    total = counts.sum(axis=1)
    rate = total / ((ne + ni) * dt_ms / 1000)
    nperseg = round(1000 / dt_ms)
    frequency, psd = scipy.signal.welch(
        rate, fs=1000 / dt_ms, window='hann', nperseg=nperseg,
        noverlap=nperseg // 2, detrend='constant', scaling='density')
    band = (frequency >= 1) & (frequency <= 1000)
    peak = np.flatnonzero(band)[np.argmax(psd[band])]
    prominence = psd[peak] / np.median(psd[band])
    one_ms = total.reshape(-1, round(1 / dt_ms)).sum(axis=1)
    fano = one_ms.var() / one_ms.mean()
    modulation = one_ms.std() / one_ms.mean()
    synchronous = fano >= 5 and modulation >= .15 and prominence >= 10
    asynchronous = fano < 5 and modulation < .15
    eligible = [np.isfinite(cv[:ne]).mean(), np.isfinite(cv[ne:]).mean()]
    median_cv = float(np.nanmedian(cv)) if np.isfinite(cv).any() else None
    regularity = 'inconclusive'
    if min(eligible) >= .5:
        if median_cv <= .5:
            regularity = 'regular'
        elif median_cv >= .8:
            regularity = 'irregular'
    synchrony = 'synchronous' if synchronous else ('asynchronous' if asynchronous else 'inconclusive')
    label = 'inconclusive'
    if synchronous and regularity == 'regular':
        label = 'synchronous regular'
    elif synchronous and regularity == 'irregular':
        label = ('fast' if frequency[peak] >= 50 else 'slow') + ' synchronous irregular'
    elif asynchronous and regularity == 'irregular':
        label = 'asynchronous irregular'
    duration_s = len(counts) * dt_ms / 1000
    metrics = dict(
        E_Hz=float(counts[:, 0].sum() / ne / duration_s),
        I_Hz=float(counts[:, 1].sum() / ni / duration_s),
        global_Hz=float(rate.mean()),
        median_ISI_CV=median_cv,
        E_median_ISI_CV=float(np.nanmedian(cv[:ne])),
        I_median_ISI_CV=float(np.nanmedian(cv[ne:])),
        E_CV_eligible_fraction=float(eligible[0]), I_CV_eligible_fraction=float(eligible[1]),
        F1=float(fano), c1=float(modulation), P=float(prominence),
        Q=float(psd[(frequency >= 1) & (frequency <= 50)].sum() / psd[band].sum()),
        dominant_Hz=float(frequency[peak]), frequency_at_lower_boundary=bool(frequency[peak] == 1),
        synchrony=synchrony, regularity=regularity, label=label)
    return metrics, frequency, psd


def summarize_spikes(packed, dt_ms, ne=model.NE, ni=model.NI):
    """Losslessly decode saved spikes; retain neuron-level evidence for every ISI CV."""
    n = ne + ni
    spikes = np.unpackbits(packed, axis=1, count=n, bitorder='little')
    counts = np.stack([spikes[:, :ne].sum(axis=1), spikes[:, ne:].sum(axis=1)], axis=1)
    time_step, neuron = np.nonzero(spikes)
    del spikes
    order = np.argsort(neuron, kind='stable')
    ids, steps = neuron[order], time_step[order]
    intervals = np.diff(steps)
    same = np.diff(ids) == 0
    isi = intervals[same].astype(np.float64) * dt_ms
    owners = ids[1:][same]
    minimum_isi = float(isi.min()) if len(isi) else None
    assert minimum_isi is None or minimum_isi >= 2 - 1e-8
    n_isi = np.bincount(owners, minlength=n)
    sums = np.bincount(owners, weights=isi, minlength=n)
    sums2 = np.bincount(owners, weights=isi * isi, minlength=n)
    cv = np.full(n, np.nan)
    eligible = n_isi >= 10
    means = sums[eligible] / n_isi[eligible]
    variances = np.maximum(0, sums2[eligible] / n_isi[eligible] - means * means)
    cv[eligible] = np.sqrt(variances) / means
    neuron_counts = np.bincount(neuron, minlength=n)
    assert int(counts.sum()) == len(time_step) == int(neuron_counts.sum())
    # All global-rate assessments use the specified 0.1 ms observation bins.
    rebin = round(.1 / dt_ms)
    observed_counts = counts.reshape(-1, rebin, 2).sum(axis=1)
    metrics, frequency, psd = assess(observed_counts, cv, .1, ne, ni)
    metrics.update(spike_count=int(counts.sum()), minimum_ISI_ms=minimum_isi,
                   count_event_consistency=True,analysis_bin_ms=.1,
                   thirds_global_Hz=(observed_counts.sum(axis=1).reshape(3,-1).mean(axis=1)
                                      / ((ne+ni)*.0001)).tolist())
    return metrics, dict(counts_EI=counts.astype(np.uint16), ISI_CV=cv,
                         ISI_count=n_isi, neuron_spike_count=neuron_counts,
                         frequency_Hz=frequency, PSD_Hz2_per_Hz=psd)


def run(config_path):
    config_path = Path(config_path).resolve()
    root = config_path.parent
    config = json.loads(config_path.read_text())
    fixed = dict(NE=model.NE,NI=model.NI,CE=model.CE,CI=model.CI,Cext=model.CEXT,
                 tau_m_ms=20,t_ref_ms=2,threshold_mV=20,reset_mV=10,JE_mV=.1,delay_ms=1.5)
    assert all(config[key] == value for key,value in fixed.items())
    for directory in ['raw', 'metrics', 'graphs']:
        (root / directory).mkdir(exist_ok=True)
    assert jax.default_backend() == 'cpu'
    brainstate.environ.set_platform('cpu')
    write_json(root / 'status.json', dict(status='running', pid=os.getpid()))
    sample = np.random.default_rng(20261108).choice(model.N, size=50, replace=False)
    np.save(root / 'sample_neurons.npy', sample)
    rows, graph_evidence = [], {}
    total_start = time.perf_counter()
    for seed in config['seeds']:
        graphs, graph_checks = model.make_graph(seed)
        graph_evidence[str(seed)] = graph_checks
        np.savez_compressed(root / 'graphs' / f'seed-{seed}.npz',
                            E_indices=graphs[0][0], E_indptr=graphs[0][1],
                            I_indices=graphs[1][0], I_indptr=graphs[1][1])
        write_json(root / 'graph_checks.json', graph_evidence)
        for dt_ms in config['dt_by_seed'][str(seed)]:
            dt = dt_ms * u.ms
            with brainstate.environ.context(dt=dt):
                net = model.Network(graphs, model.initial_state(seed), seed, dt)
                brainstate.nn.init_all_states(net)
                reset_snapshot = model.snapshot_states(net)
                run_network = brainstate.transform.jit(net.rollout, static_argnums=(1, 2))
                steps = round(config['duration_ms'] / dt_ms)
                indices = jnp.arange(steps, dtype=jnp.int32)
                for ci, condition in enumerate(config['conditions']):
                    g, eta = condition
                    name = f'seed-{seed}_dt-{dt_ms:g}_condition-{ci}'
                    t0 = time.perf_counter()
                    run_network.compile(indices, float(g), float(eta))
                    compile_s = time.perf_counter() - t0
                    print(f'COMPILED {name} seconds={compile_s:.3f}', flush=True)
                    model.restore_states(reset_snapshot)
                    t0 = time.perf_counter()
                    packed_all = np.asarray(run_network(indices, float(g), float(eta)))
                    execution_s = time.perf_counter() - t0
                    assert np.all(np.isfinite(net.pop.V.value.to_decimal(u.mV)))
                    burn = round(config['burn_in_ms'] / dt_ms)
                    packed = packed_all[burn:]
                    # Save raw evidence before deriving ANY scientific statistic.
                    raw_path = root / 'raw' / f'{name}.npz'
                    np.savez_compressed(raw_path, spikes_packed=packed,
                                        burn_in_spikes_packed=packed_all[:burn],
                                        final_V_mV=np.asarray(net.pop.V.value.to_decimal(u.mV)),
                                        final_last_spike_step=np.asarray(net.pop.last.value),
                                        final_rng_key=np.asarray(jax.random.key_data(net.drive.rng.value)),
                                        dt_ms=dt_ms, seed=seed, g=g, eta=eta,
                                        burn_in_ms=config['burn_in_ms'], duration_ms=config['duration_ms'])
                    metrics, arrays = summarize_spikes(packed, dt_ms)
                    metrics.update(seed=seed,dt_ms=dt_ms,g=g,eta=eta,condition=ci,
                                   expected=config['expected'][ci],
                                   execution_seconds=execution_s,compile_seconds=compile_s,
                                   raw_file=str(raw_path.relative_to(root)))
                    np.savez_compressed(root / 'metrics' / f'{name}.npz', **arrays)
                    write_json(root / 'metrics' / f'{name}.json', metrics)
                    rows.append(metrics)
                    write_json(root / 'metrics.json', rows)
                    print('COMPLETED ' + json.dumps(metrics), flush=True)
                    write_json(root / 'status.json', dict(status='running',pid=os.getpid(),
                               completed=len(rows),last_completed=name,
                               elapsed_seconds=time.perf_counter()-total_start))
    with (root / 'metrics.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    assessment = []
    for ci in range(4):
        primary = [r for r in rows if r['condition'] == ci and r['dt_ms'] == .1]
        fine = next(r for r in rows if r['condition'] == ci and r['dt_ms'] == .05)
        requested = config['expected'][ci]
        all_match = all(r['label'] == requested for r in primary)
        all_incompatible = all(r['label'] not in [requested,'inconclusive'] for r in primary)
        outcome = 'supported' if all_match and fine['label'] == requested else (
            'unsupported' if all_incompatible else 'inconclusive')
        assessment.append(dict(condition=ci,requested=requested,outcome=outcome,
                               primary_labels=[r['label'] for r in primary],
                               fine_label=fine['label'],
                               primary_dominant_Hz=[r['dominant_Hz'] for r in primary],
                               fine_dominant_Hz=fine['dominant_Hz']))
    write_json(root / 'assessment.json', assessment)
    write_json(root / 'status.json', dict(status='done',completed=len(rows),
               elapsed_seconds=time.perf_counter()-total_start))
    print('ASSESSMENT '+json.dumps(assessment), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    args = parser.parse_args()
    run(args.config)

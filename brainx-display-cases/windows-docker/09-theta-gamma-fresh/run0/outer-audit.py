"""Reproduce archived evidence in the pinned image without changing the archive."""
import hashlib
import importlib
import json
from pathlib import Path
import shutil
import sys

import numpy as np


source = Path('/evidence/theta_gamma')
output = Path('/audit')
work = Path('/tmp/theta-gamma-outer-audit')
work.mkdir()
for path in source.glob('*.py'):
    shutil.copy2(path, work / path.name)
(work / 'checks').mkdir()
sys.path.insert(0, str(work))
import os
os.chdir(work)

results = {'image': 'sha256:23af0834fc456c1d4f9a821134a55e16be0bc6e5403558b9f1d739c8f1067688'}
manifest_checks = {}
for folder in sorted((source / 'runs').iterdir()):
    manifest = json.loads((folder / 'manifest.json').read_text())
    failures = [name for name, entry in manifest.items()
                if hashlib.sha256((folder / name).read_bytes()).hexdigest() != entry['sha256']]
    assert not failures, (folder, failures)
    manifest_checks[folder.name] = len(manifest)
results['manifest_files_verified'] = manifest_checks

verify = importlib.import_module('verify')
verify.verify()
results['focused_verification'] = json.loads((work / 'checks/verification.json').read_text())

model = importlib.import_module('model')
analysis = importlib.import_module('analysis')
replays = {}
for name in ['production-02', 'convergence-02']:
    run = source / 'runs' / name
    config = json.loads((run / 'config.json').read_text())
    actual = model.run_model(config)
    original = np.load(run / 'raw/trajectories.npz')
    errors = {}
    for key in original.files:
        assert actual[key].shape == original[key].shape, key
        errors[key] = float(np.max(np.abs(actual[key] - original[key])))
        assert np.array_equal(actual[key], original[key]), (name, key, errors[key])
    rows, derived = analysis.analyze(actual, config)
    saved = json.loads((run / 'metrics/metrics.json').read_text())
    assert rows == saved, name
    old_derived = np.load(run / 'raw/derived.npz')
    for key in old_derived.files:
        assert np.array_equal(derived[key], old_derived[key]), (name, key)
    replays[name] = {'max_raw_errors': errors, 'metric_rows_exact': len(rows),
                     'derived_arrays_exact': len(derived)}
results['replay'] = replays

metrics = json.loads((source / 'runs/production-02/metrics/metrics.json').read_text())
pair = [next(r for r in metrics if r['view'] == 'proxy' and r['rep'] == 0
             and r['gain'] == 1 and r['depth'] == depth) for depth in [0, .75]]
results['fixed_pair'] = {'R_off': pair[0]['R'], 'R_on': pair[1]['R'],
                         'E_carrier_hz': pair[0]['E_cycle']['mean_cycle_hz'],
                         'I_carrier_hz': pair[0]['I_cycle']['mean_cycle_hz']}
results['status'] = 'PASS'
(output / 'reproduction.json').write_text(json.dumps(results, indent=2))
print(json.dumps({'status': results['status'], 'replay': replays,
                  'fixed_pair': results['fixed_pair']}, indent=2))

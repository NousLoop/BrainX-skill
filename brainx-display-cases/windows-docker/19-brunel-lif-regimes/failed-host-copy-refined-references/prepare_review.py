"""Materialize concrete, existing artifact paths for the independent reviewer."""
from pathlib import Path


def main():
    root=Path('/workspace');run=root/'runs/iteration-2';parent=root/'runs/baseline-v1';fig=root/'figures/iteration-2-diagnostic'
    groups={
        'SPECIFICATION':[root/'NeuroSpecification.md'],
        'LOOP_MEMORY':[root/'brainmodeling-memory.md'],
        'BRAINX_STUDY_RECORD':[root/'brainx-study-record.md',root/'brainx-study-record-iteration-2.md'],
        'IMPLEMENTATION':[root/x for x in ['model.py','analysis.py','experiment.py','plot_results.py','write_report.py','audit_evidence.py','reanalyze.py','check_metric_fixture.py','prepare_review.py']],
        'TESTS':[root/x for x in ['checks.py','check_temporal_input.py','checks/metrics_fixture_v2/test_result.json','checks/metrics_fixture_v2/input/periodic_spikes.npz','checks/metrics_fixture_v2/output/periodic_spikes.npz','checks/metrics_fixture_v2/output/periodic_spikes.json','metric-fixture-v2.log','checks/components.json','checks/temporal_poisson.json','checks/metrics_fixture/test_result.json','checks/metrics_fixture/raw.npz','checks/plot_api.json','checks/evidence_audit.json','checks-launch.log','checks-launch-attempt1.log','checks-launch-attempt2.log']],
        'ACCELERATION_AND_PARITY':[root/x for x in ['acceleration.md','acceleration-iteration-2.md','checks/acceleration.json','checks/worker_affinity_parity.json','checks/full_size_smoke.npz']],
        'EXPERIMENT_RUN':[run/x for x in ['RUN_SPEC.md','config.json','environment.json','command.txt','status.json','exit_code','run.log','manifest.json','metrics_summary.csv','population_rates.npz','sample_neuron_ids.npy','spectral_parity.json']]+sorted((run/'code').glob('*'))+sorted((run/'raw').glob('*.npz'))+sorted((run/'graphs').glob('*'))+sorted((run/'metrics').glob('condition*'))+sorted(run.glob('group*.log'))+sorted(run.glob('worker*.log')),
        'RESULT_ASSESSMENT':[run/'assessment.json',run/'assessment.md',root/'report.md',root/'RAW_EVIDENCE.md',root/'FIGURE_CONTRACT.md',root/'FIGURE_MANIFEST.md',fig/'figure_data.npz',fig/'manifest.json']+sorted(fig.glob('*.png')),
    }
    groups['PARENT_PRODUCTION_PROVENANCE']=[parent/x for x in ['RUN_SPEC.md','config.json','environment.json','command.txt','status.json','exit_code','run.log','manifest.json','assessment.json']]+sorted((parent/'code').glob('*'))+sorted((parent/'metrics').glob('condition*'))+sorted(parent.glob('group*.log'))+sorted(parent.glob('worker*.log'))
    groups['PRIOR_REVIEW_EVIDENCE']=[root/'reviews/iteration-1.md',root/'reviews/iteration-1.response.json',root/'reviews/request-iteration-1.txt',root/'reviews/addressed-iteration-2.md',root/'reviews/iteration-1.report.md']
    assert len(list((run/'raw').glob('*.npz')))==16
    lines=['Review completed BrainX iteration 2.','',f'PROJECT_ROOT: {root}','ACTIVE_COVERAGE: none','']
    for name,files in groups.items():
        lines.append(name+':')
        for path in files:
            assert path.is_file(),f'Missing {path}'
            lines.append('- '+str(path))
        lines.append('')
    lines+=['TRAINING_OR_FITTING_EVIDENCE: none','ITERATION_SCOPE: analysis-only fixes BX-001 and BX-002. Every production raw hash and unchanged model hash is verified; all 16 spectra, metrics, predicates and decisions are preserved. Reviewer 1 explicitly permitted no production rerun when this parity passes. Prior artifacts remain intact.','',
        'RESEARCHER SOURCE RESTRICTION (applies to this independent review too): This is a new first-principles exploration using only the task-supplied data. Do not search for, consult, or reconstruct papers, scientific example scripts, external existing scientific model implementations, open-source scientific solutions or remembered Brunel protocols. Installed BrainX skill instructions and public API contract documentation may be consulted ONLY for library mechanics. Do read the newly created project implementation and evidence listed above. Do not follow any skill routing to scientific example scripts. Do not force the four requested regime labels: unsupported/inconclusive outcomes are authorized, and frozen rules/parameters must not be tuned to results. The researcher explicitly delegated all unspecified decisions and authorized locking/proceeding without another clarification or approval.','',
        'PROPOSED NEXT ACTION: only if PASS, export final figures using the exact accepted evidence and finalize report; preserve unfavorable/uncertain labels. The current diagnostic plots are unaccepted pending your verdict.','',
        'Read every listed artifact and review this iteration using the injected reviewer contract. Do not edit files. Return only the required Markdown report.']
    (root/'reviews').mkdir(exist_ok=True)
    (root/'reviews/request-iteration-2.txt').write_text('\n'.join(lines)+'\n')
    print(root/'reviews/request-iteration-2.txt')


if __name__=='__main__':main()

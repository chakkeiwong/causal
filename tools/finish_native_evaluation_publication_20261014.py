#!/usr/bin/env python3
"""Resume native-reader publication with canonical historical reader metadata."""
import publish_native_evaluation_reader_20261014 as prior


def main():
    root, base = prior.ROOT, prior.BASE
    state = prior.core.read(root, prior.core.STATE)
    before = prior.core.sha(root / prior.core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path'] == str(prior.build.OLD.with_suffix('.pdf').relative_to(root))
    binding = prior.ref(base / 'working-release.json', 'Reviewed native/reuse/evaluation working release')
    manifest = prior.run.ledger.validate_working_release(root, binding)
    repair = base / 'publication-repair.json'
    prior.write(repair, {
        'observed_failure': 'State admission rejected: Current reader differs from its preserved working-delivery chain.',
        'cause': 'The publisher used a descriptive reader status; the preserved chain requires an exact canonical status.',
        'repair': 'Use Working monograph; not I02 acceptance. Preserve the failed helper, reviewed PDF, review and release manifest. No criterion or validator is relaxed.',
        'evidence': [binding, prior.ref(root / 'tools/publish_native_evaluation_reader_20261014.py', 'Preserved failed status assignment'),
                     prior.ref(root / 'tools/causal_program_v14.py', 'validate_overlay exact reader reconstruction, lines 260-268')],
        'next_action': 'Commit the existing reviewed release with canonical metadata, then renew exact-reader Q2-Q4.'})
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: manifest['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=manifest['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    prior.run.commit(root, before, state, {'action': 'publish_native_evaluation_working_reader',
        'manifest': binding, 'repair': prior.ref(repair, 'Canonical status admission repaired'), 'final_acceptance': False})
    print('Published the reviewed 692-page working reader; proposal acceptance remains open.')


if __name__ == '__main__':
    main()

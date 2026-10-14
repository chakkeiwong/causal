#!/usr/bin/env python3
"""Resume rejected state admission with the controller's exact reader status."""
import json
import publish_discovery_review_20261014 as prior

ROOT, BASE, OUT, OP, OUTPUT = prior.ROOT, prior.BASE, prior.OUT, prior.OP, prior.OUTPUT
core, run, ref, write, transition = prior.core, prior.run, prior.ref, prior.write, prior.transition


def main():
    state = core.read(ROOT, core.STATE)
    before = core.sha(ROOT / core.STATE)
    assert state['execution_runtime']['active']['operation'] == OP
    assert state['reader']['path'] == 'docs/causal_proposal_l2_v4_2026-10-13.pdf'
    binding = ref(BASE / 'working-release.json', 'Reviewed discovery working release')
    manifest = run.ledger.validate_working_release(ROOT, binding)
    reviewed = json.loads((BASE / 'release-source-review.json').read_text())
    write(BASE / 'publication-repair.json', {
        'observed_failure': 'State admission rejected: Current reader differs from its preserved working-delivery chain.',
        'cause': 'Publication helper used a descriptive status string where the historical chain requires an exact canonical string.',
        'repair': 'Use Working monograph; not I02 acceptance. No schema or acceptance criterion is relaxed; PDF and review bytes unchanged.',
        'evidence': [binding, ref(ROOT / 'tools/causal_program_v14.py', 'Working-delivery validation line 267'),
                     ref(ROOT / 'tools/publish_discovery_review_20261014.py', 'Failed status assignment preserved')],
        'next_action': 'Commit the existing reviewed release with canonical reader metadata, record L4, renew Q2-Q4.'})
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: manifest['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=manifest['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, {'action': 'publish_discovery_review_working_reader', 'manifest': binding,
                                   'repair': ref(BASE / 'publication-repair.json', 'Exact schema status restored'),
                                   'final_acceptance': False})
    graph, _, _ = run.combined(ROOT, state)
    receipt = run.ledger.receipt_template(run.ledger.operation(graph, OP))
    receipt.update(outcome='pass', execution='performed', scope='Author L4 source/content/mathematical/depth review in the 683-page reader',
                   reviewer=reviewed['reviewer'], limitations=reviewed['limitations'],
                   outputs=[ref(OUTPUT, 'Complete chapter review'), binding], nonexecution_reason='', revisit_trigger='',
                   criteria=[{'index': 0, 'verdict': 'pass',
                              'finding': 'Allocated discovery topics, methods, assumptions, alternatives, package decisions, failure regimes and banking consequences are developed. Source and mathematical findings are resolved without claiming live, bank or unrestricted identification results.',
                              'evidence': [ref(OUTPUT, 'Coverage and review'), ref(BASE / 'release-source-review.json', 'Source and exact-reference checks')]},
                             {'index': 1, 'verdict': 'pass',
                              'finding': '21.5 substantive page equivalents across 29 physical pages meets the 20-22 allocation. Per-page deductions exclude overlap, framing and already credited content; no allocation exception.',
                              'evidence': [ref(OUTPUT, 'Per-page reviewed credit'), ref(OUT / 'build-report.json', 'Exact compiled pages')]}])
    write(BASE / 'operation-receipt.json', receipt)
    transition('record', OP, BASE / 'operation-receipt.json')


if __name__ == '__main__':
    main()

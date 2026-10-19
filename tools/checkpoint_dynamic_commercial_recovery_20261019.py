#!/usr/bin/env python3
"""Preserve recovery evidence and refresh the current executable program."""
from collections import Counter
import json
from pathlib import Path
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run = extension.base
ROOT = run.core.ROOT
BASE = ROOT/'docs/program/execution/2026-10-19/recovery-dynamic-commercial-v1'
WORK = ROOT/'docs/program/execution/2026-10-19/dynamic-commercial-v1'
SPONSOR = ROOT/'docs/program/execution/2026-10-19/sponsor-dynamic-commercial-v1'
read = lambda p: json.loads(p.read_text())


def main():
    assert not BASE.exists()
    state = run.core.read(ROOT, run.core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path'] == 'docs/causal_proposal_dynamic_commercial_reviewed_2026-10-19.pdf'
    view = run.status(ROOT, state)
    graph, merged, stages = run.combined(ROOT, state)
    assert {r['id']: r['status'] for r in view['proposal_gaps']} == {
        'Q1': 'open', 'Q2': 'pass', 'Q3': 'pass', 'Q4': 'pass', 'Q5': 'open'}
    sponsor = read(SPONSOR/'working-release.json')
    verify_bindings(sponsor)
    assert run.same_reader(state['reader'], sponsor['paired_monograph'])
    results = merged['execution_program']['results']
    operations, groups = [], {}
    for node in graph['nodes']:
        key = node['id']
        result = results.get(key)
        if stages[key] != 'proposal_now' or result and result['outcome'] == 'pass':
            continue
        checkpoints = merged['execution_program']['progress'].get(key, [])
        action = read(ROOT/checkpoints[-1]['path'])['next_action'] if checkpoints else node['action']
        operations.append(dict(id=key, lane=node['lane'], status=result['outcome'] if result else 'open',
            title=node['title'], action=action, prerequisites=run.ledger.blockers(merged, node),
            outputs=node['outputs'], evidence=result, requires_inputs=node['requires_inputs']))
    for name, prefix, total in [('software', 'SW.CELL.', 102),
            ('reuse', 'SW.DECISION.', 115), ('chapters', 'TEXT.REVIEW.', 22)]:
        selected = {k: v for k, v in results.items() if k.startswith(prefix)}
        groups[name] = dict(Counter(v['outcome'] for v in selected.values()),
            open=total-len(selected), total=total)
    BASE.mkdir()
    write(BASE/'state-snapshot.json', state)
    write(BASE/'status-snapshot.json', view)
    write(BASE/'remaining-operations.json', dict(reader=state['reader'],
        recorded=view['recorded_proposal_operations'], proposal_operations=view['proposal_operations'],
        ready=view['ready_proposal_operations'], by_lane=dict(Counter(r['lane'] for r in operations)),
        coverage=groups, operations=operations, proposal_accepted=False))
    evidence = [ref(WORK/n, 'Reviewed dynamic-panel evidence') for n in
        ['source-audit-v2.json', 'anchor-review.json', 'review.json', 'exact-results.json',
         'mathematical-review.json', 'working-release.json', 'release-source-review.json']]
    write(BASE/'recovery-checkpoint.json', dict(status='recovered_and_continued',
        state_snapshot=ref(BASE/'state-snapshot.json', 'Canonical state at checkpoint'),
        current_reader=state['reader'], sponsor=ref(SPONSOR/'working-release.json', 'Exact paired sponsor'),
        remaining=ref(BASE/'remaining-operations.json', 'All nonpassing proposal obligations'),
        completed=['Published reviewed dynamic-panel reader without rerunning completed exclusive writes.',
            'Preserved preceding Feast source and information-clock proposal.',
            'Preserved809citation identities and250compiled inputs; renewed exact-reader Q2-Q4.',
            'Published preserving sponsor successor with unchanged prior source identities.'],
        recovered_failures=['The earlier Git status process completed successfully.',
            'One checkpoint-generation executor call failed JavaScript parsing before executing shell code; replaced by apply_patch.'],
        evidence=evidence, next_actions=[view['next']+': '+view['next_action'],
            'Continue independent ready items across checkpoints; retain unresolved evidence routes.',
            'Keep mandatory repair rollups, rendered review and final acceptance open.'],
        global_blocker=None, visual_acceptance=False, proposal_accepted=False,
        background_worker_running=False))
    current = ROOT/'docs/program/execution/current-program.md'
    prior = current.read_text()
    (BASE/'prior-current-program.md').write_text(prior)
    audit = read(WORK/'reader/source-audit.json')
    papers = read(WORK/'traceability-review.json')['scholarly_pdfs']
    text = prior.replace('the Feast proposal review', 'the Feast and commercial dynamic-panel proposal reviews')
    text = text.replace('1,114-page', f"{state['reader']['pages']:,}-page")
    text = text.replace('24-page sponsor', f"{sponsor['pages']}-page sponsor")
    text = text.replace('causal_proposal_feast_reviewed', 'causal_proposal_dynamic_commercial_reviewed')
    text = text.replace('sponsor_proposal_feast_reviewed', 'sponsor_proposal_dynamic_commercial_reviewed')
    text = text.replace('809 audited', f"{len(audit['sources'])} audited")
    text = text.replace('160 recorded outcomes', f"{view['recorded_proposal_operations']} recorded outcomes")
    text = text.replace('186 ready', f"{view['ready_proposal_operations']} ready")
    text = text.replace('| Software coverage | 2 | 27 | 73 | 102 |',
        '| Software coverage | 2 | 28 | 72 | 102 |')
    addition = '''
The commercial dynamic-panel continuation adds four official Stata/EViews originals
and retains six earlier identities. It distinguishes system-GMM initial restrictions,
difference moments, local-projection shock assumptions, instrument growth and calendar
dependence. An exact initial-condition law gives a proposed moment of one half or zero.
A second law shows variance understatement by50.5with100branches and25dates: at a
stipulated USD10,000scale, population standard deviations are approximately USD2,010
and USD283. These are authored examples, not bank outcomes or vendor executions.
The new argument is at physical pages471-474. Eight-family commercial coverage
remains inconclusive, with MathWorks access failure and missing manuals, exact editions,
rights, prices and native comparisons preserved.

'''
    addition = addition.replace('by50.5with100branches and25dates', 'by 50.5 with 100 branches and 25 dates')
    addition = addition.replace('USD10,000scale', 'USD 10,000 scale').replace('USD2,010', 'USD 2,010')
    addition = addition.replace('USD283', 'USD 283').replace('pages471-474', 'pages 471-474')
    text = text.replace('## Required standard and unresolved work', addition+'## Required standard and unresolved work')
    start = text.index('Next: **')
    end = text.index('[Every nonpassing obligation]', start)
    text = text[:start]+f"Next: **{view['next']}**. {view['next_action']}\n\n"+'''Continue the R effects/heterogeneity comparison using matched original methods,
target definitions, nuisance/cross-fitting contracts and sampling units. Record
dose-response and missing-treatment uncertainty explicitly. Independent ready
items continue across phase boundaries; one missing source does not stop others.

'''+text[end:]
    text = text.replace('recovery-feast-v1', 'recovery-dynamic-commercial-v1')
    assert str(papers)+' genuine scholarly PDFs' in text
    current.write_text(text)
    run.render(ROOT, state)
    print(json.dumps(dict(recorded=view['recorded_proposal_operations'],
        ready=view['ready_proposal_operations'], next=view['next'],
        reader_pages=state['reader']['pages'], sponsor_pages=sponsor['pages'])))


if __name__ == '__main__':
    main()

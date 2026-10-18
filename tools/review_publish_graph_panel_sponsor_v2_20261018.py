#!/usr/bin/env python3
"""Review a preserving sponsor successor and bind it to the current reader."""
import json
from pathlib import Path
import re

import build_graph_panel_sponsor_v2_20261018 as build
import sponsor_economics_20261013 as economics
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run, core, ROOT, BASE = build.run, build.core, build.ROOT, build.BASE


def main():
    read = lambda p: json.loads(p.read_text())
    report = read(BASE/'build-report.json')
    audit = read(BASE/'source-audit.json')
    for record in [report, audit, read(BASE/'plan-review.json'), read(BASE/'progress-evidence.json')]:
        verify_bindings(record)
    assert report['cited_records'] == 45 and not report['empty_pages'] and not report['text_bounds_issues']
    assert all('Underfull' in warning for warning in report['warnings'])
    assert report['visual_acceptance'] is False and report['final_proposal_acceptance'] is False
    assert read(BASE/'economics-results.json') == economics.calculate()
    prior = read(build.PRIOR/'source-audit.json')
    before = {s['integrated_citation_key']: s for s in prior['sources']}
    after = {s['integrated_citation_key']: s for s in audit['sources']}
    assert len(before) == 34 and len(after) == 45
    assert all(after[key] == value for key, value in before.items())
    current = (BASE/'proposal.md').read_text()
    original = (build.PRIOR/'proposal.md').read_text()
    for start, end in [('# Economics and the next experiment', '# What remains before a complete proposal'),
                       ('## Funding and observations', '## Discovery and agent support')]:
        assert current[current.index(start):current.index(end)] == original[original.index(start):original.index(end)]
    cited = {key.strip() for group in re.findall(build.shared.CITE, current) for key in group.split(',')}
    assert cited == after.keys()
    text = ' '.join((BASE/'reader.txt').read_text().split())
    pages = read(BASE/'progress-evidence.json')['reader']['pages']
    for token in [f'{pages:,} pages', '772 audited', '201 genuine', '78 open', '22 inconclusive',
                  '96 open', 'three inconclusive', '42 inspected', '71 unread', 'L1 and L6',
                  'USD 5,200', 'USD 36,000', 'PromptBench', 'twenty paired families',
                  'execution failure', 'causaleffect', 'DAGitty', 'USD 34,000',
                  'USD 11,375', 'returned unsupported', 'not-yet-treated']:
        assert token.lower() in text.lower(), token
    state = core.read(ROOT, core.STATE)
    assert run.same_reader(state['reader'], report['paired_monograph'])
    assert run.same_reader(state['reader'], read(BASE/'progress-evidence.json')['reader'])
    evidence = [ref(BASE/name, 'Inspected sponsor evidence') for name in
                ['plan-review.json', 'source-audit.json', 'build-report.json', 'economics-results.json',
                 'proposal.md', 'reader.txt', 'progress-evidence.json']]
    evidence += [ref(Path(__file__), 'Exact preservation, arithmetic and pairing checks')]
    findings = [
        'All34 predecessor citation records survive unchanged;45 cited records have bound local evidence.',
        'Funding and servicing arguments and the full assumed economic section survive byte-for-byte.',
        'Reader page/source counts, effective software/reuse outcomes and original census match the cited snapshot.',
        'R symbolic identification, counterfactual bounds and prior sensitivity remain distinct; native package integration is unqualified.',
        'Framework taxonomy and evaluator hooks are source-bounded; paired counts and assumed monetary reversal are authored examples.',
        'All four banking journeys, public-first recommendation, adverse findings and open L1/L6 coverage obligations remain explicit.',
        'DAGitty preconditions and result types remain scoped; no native execution or full rights admission is inferred.',
        'The commercial panel target, negative-weight illustration and observed common-interface refusal remain separate from sampling qualification.'
    ]
    limitations = [
        'Author source, arithmetic and extracted-page review; no independent or rendered visual acceptance.',
        'Full RELEASE.RECONCILE, mandatory repairs, Q1/Q5 and final proposal acceptance remain open.',
        'Current coverage counts are a bound snapshot and do not establish installed software or bank qualification.'
    ]
    write(BASE/'author-review.json', dict(status='pass', issues=[],
        reviewer=dict(name='Codex author/coordinator', kind='author'),
        scope='Preserving current-reader sponsor source and content review',
        sponsor=report['reader_copy'], paired_monograph=report['paired_monograph'],
        findings=findings, evidence=evidence, limitations=limitations,
        visual_acceptance=False, final_acceptance=False))
    manifest = dict(kind='working_sponsor', pdf=report['reader_copy'], pages=report['pages'],
        paired_monograph=report['paired_monograph'],
        predecessor=ref(ROOT/'docs/sponsor_proposal_framework_reviewed_2026-10-18.pdf', 'Preserved predecessor sponsor'),
        predecessor_release=ref(build.PRIOR/'working-release.json', 'Preserved predecessor review'),
        failed_attempt=ref(build.DOCS/'program/execution/2026-10-18/sponsor-graph-panel-v1/failure-review.json', 'Preserved invalid bibliography and reviewed numeric repair'),
        predecessor_operation=state['execution_program']['results']['RELEASE.SPONSOR'],
        build=ref(BASE/'build-report.json', 'Bounded sponsor build'),
        review=ref(BASE/'author-review.json', 'Source and exact-reader coherence review'),
        evidence=evidence, final_acceptance=False, visual_acceptance=False)
    verify_bindings(manifest)
    write(BASE/'working-release.json', manifest)
    digest = core.sha(ROOT/core.STATE)
    delivery = {key: report['reader_copy'][key] for key in ['path', 'sha256']}
    delivery.update(pages=report['pages'], kind='working_sponsor',
        status='Working sponsor; exact-reader content review, visual/final acceptance open',
        paired_monograph=report['paired_monograph'],
        release=ref(BASE/'working-release.json', 'Preserving sponsor successor'))
    assert not any(item['path'] == delivery['path'] for item in state['deliveries'])
    state['deliveries'].append(delivery)
    run.commit(ROOT, digest, state, dict(action='publish_graph_panel_working_sponsor',
        release=delivery['release'], prior_operation_preserved=True, final_acceptance=False))
    print(json.dumps(dict(published=delivery['path'], pages=report['pages'], records=45,
        paired_monograph=state['reader']['path'], review='pass', visual_acceptance=False,
        final_acceptance=False)))


if __name__ == '__main__':
    main()

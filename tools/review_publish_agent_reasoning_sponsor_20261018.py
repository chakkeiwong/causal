#!/usr/bin/env python3
"""Review a preserving Python identification sponsor and bind its exact reader."""
import json
from pathlib import Path
import re

import build_agent_reasoning_sponsor_20261018 as build
import sponsor_economics_20261013 as economics
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run, core, ROOT, BASE = build.run, build.core, build.ROOT, build.BASE


def main():
    read = lambda p: json.loads(p.read_text())
    report = read(BASE/'build-report.json')
    audit = read(BASE/'source-audit.json')
    for record in [report, audit, read(BASE/'plan-review.json'), read(BASE/'progress-evidence.json')]:
        verify_bindings(record)
    assert report['cited_records'] == 62 and not report['empty_pages'] and not report['text_bounds_issues']
    assert all('Underfull' in warning for warning in report['warnings'])
    assert report['visual_acceptance'] is False and report['final_proposal_acceptance'] is False
    assert read(BASE/'economics-results.json') == economics.calculate()
    prior = read(build.PRIOR/'source-audit.json')
    before = {s['integrated_citation_key']: s for s in prior['sources']}
    after = {s['integrated_citation_key']: s for s in audit['sources']}
    assert len(before) == 56 and len(after) == 62
    assert all(after[key] == value for key, value in before.items())
    current = (BASE/'proposal.md').read_text()
    original = (build.PRIOR/'proposal.md').read_text()
    for start, end in [('# Economics and the next experiment', '# What remains before a complete proposal'),
                       ('## Funding and observations', '## Discovery and agent support'),
                       ('## Graph adjustment and staggered panel comparisons', '# Public evidence before expensive bank experiments')]:
        a = current[current.index(start):current.index(end)]
        b = original[original.index(start):original.index(end)]
        if start.startswith('## Graph'):
            a = a[:a.index('## Causal-agent ambition, evidence and the decision being answered')]
        assert a == b, start
    cited = {key.strip() for group in re.findall(build.shared.CITE, current) for key in group.split(',')}
    assert cited == after.keys()
    text = ' '.join((BASE/'reader.txt').read_text().split())
    pages = read(BASE/'progress-evidence.json')['reader']['pages']
    for token in [f'{pages:,} pages', '784 audited', '203 genuine', '77 open', '23 inconclusive',
                  '96 open', 'three inconclusive', '44 inspected', '69 unread', 'L1 and L6',
                  'USD 5,200', 'USD 36,000', 'PromptBench', 'twenty paired families',
                  'execution failure', 'causaleffect', 'DAGitty', 'USD 34,000',
                  'USD 11,375', 'returned unsupported', 'not-yet-treated', 'Ananke 0.5.0',
                  'USD 400', 'USD 50', 'USD 350', 'cross-world coupling', 'Other/Proprietary',
                  'precondition', 'GCM', 'DEF-1', 'USD 160', 'USD 190', 'USD 30', '16/19', 'citation-chain']:
        assert token.lower() in text.lower(), token
    state = core.read(ROOT, core.STATE)
    assert state['execution_runtime']['active'] is None
    assert run.same_reader(state['reader'], report['paired_monograph'])
    assert run.same_reader(state['reader'], read(BASE/'progress-evidence.json')['reader'])
    evidence = [ref(BASE/name, 'Inspected sponsor evidence') for name in
                ['plan-review.json', 'source-audit.json', 'build-report.json', 'economics-results.json',
                 'proposal.md', 'reader.txt', 'progress-evidence.json']]
    evidence += [ref(Path(__file__), 'Exact preservation, arithmetic and pairing checks')]
    findings = [
        'All56 predecessor citation records survive unchanged;62 cited records have bound local evidence.',
        'Funding/servicing, graph/panel, Python identification arguments and the full assumed economic section survive byte-for-byte.',
        'Reader page/source counts, effective software/reuse outcomes and original census match the cited snapshot.',
        'The biomedical agenda and scoped philosophical criterion remain distinct from statistical discovery and general causal competence.',
        'Exact structural single/compound interventions, predecision backup information and160-190pUSD value remain explicitly hypothetical.',
        'Citation-chain mismatch, transcript explanation and target inconsistencies require adjudication before benchmark reuse; prior package admission limits remain.',
        'All four banking journeys, public-first recommendation, adverse findings and open L1/L6 coverage obligations remain explicit.'
    ]
    limitations = [
        'Author source, arithmetic and extracted-page review; no independent or rendered visual acceptance.',
        'Full RELEASE.RECONCILE, mandatory repairs, Q1/Q5 and final proposal acceptance remain open.',
        'Current coverage counts are a bound snapshot and do not establish installed software or bank qualification.',
        'No DEF-1 implementation, general causal-agent qualification or live model trial is implied; diagram image/table acceptance remains pending.'
    ]
    write(BASE/'author-review.json', dict(status='pass', issues=[],
        reviewer=dict(name='Codex author/coordinator', kind='author'),
        scope='Preserving current-reader sponsor source and content review',
        sponsor=report['reader_copy'], paired_monograph=report['paired_monograph'],
        findings=findings, evidence=evidence, limitations=limitations,
        visual_acceptance=False, final_acceptance=False))
    manifest = dict(kind='working_sponsor', pdf=report['reader_copy'], pages=report['pages'],
        paired_monograph=report['paired_monograph'],
        predecessor=ref(ROOT/'docs/sponsor_proposal_python_identification_reviewed_2026-10-18.pdf', 'Preserved predecessor sponsor'),
        predecessor_release=ref(build.PRIOR/'working-release.json', 'Preserved predecessor review and failure history'),
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
    run.commit(ROOT, digest, state, dict(action='publish_agent_reasoning_working_sponsor',
        release=delivery['release'], prior_operation_preserved=True, final_acceptance=False))
    print(json.dumps(dict(published=delivery['path'], pages=report['pages'], records=62,
        paired_monograph=state['reader']['path'], review='pass', visual_acceptance=False,
        final_acceptance=False)))


if __name__ == '__main__':
    main()

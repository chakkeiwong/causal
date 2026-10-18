#!/usr/bin/env python3
"""Review a preserving evaluation/code survey sponsor and bind its exact reader."""
import json
from pathlib import Path
import re

import build_evaluation_code_sponsor_20261019 as build
import sponsor_economics_20261013 as economics
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run, core, ROOT, BASE = build.run, build.core, build.ROOT, build.BASE


def main():
    read = lambda p: json.loads(p.read_text())
    report = read(BASE/'build-report.json')
    audit = read(BASE/'source-audit.json')
    for record in [report, audit, read(BASE/'plan-review.json'), read(BASE/'progress-evidence.json')]:
        verify_bindings(record)
    assert report['cited_records'] == 76 and not report['empty_pages'] and not report['text_bounds_issues']
    assert all('Underfull' in warning for warning in report['warnings'])
    assert report['visual_acceptance'] is False and report['final_proposal_acceptance'] is False
    assert read(BASE/'economics-results.json') == economics.calculate()
    prior = read(build.PRIOR/'source-audit.json')
    before = {s['integrated_citation_key']: s for s in prior['sources']}
    after = {s['integrated_citation_key']: s for s in audit['sources']}
    assert len(before) == 70 and len(after) == 76
    assert all(after[key] == value for key, value in before.items())
    current = (BASE/'proposal.md').read_text()
    original = (build.PRIOR/'proposal.md').read_text()
    assert current == build.manuscript(report['paired_monograph'].get('pages', read(BASE/'progress-evidence.json')['reader']['pages']))
    for start, end in [('# Economics and the next experiment', '# What remains before a complete proposal'),
                       ('## Funding and observations', '## Discovery and agent support'),
                       ('## Graph adjustment and staggered panel comparisons', '## Java identification and scientific failure states')]:
        assert current[current.index(start):current.index(end)] == original[original.index(start):original.index(end)],start
    start='## Java identification and scientific failure states'
    assert current[current.index(start):current.index('## Evaluate accepted causal outputs and all-request cost')] == original[original.index(start):original.index('# Public evidence before expensive bank experiments')]
    cited = {key.strip() for group in re.findall(build.shared.CITE, current) for key in group.split(',')}
    assert cited == after.keys()
    text = ' '.join((BASE/'reader.txt').read_text().split())
    pages = read(BASE/'progress-evidence.json')['reader']['pages']
    for token in [f'{pages:,} pages', '791 audited', '205 genuine', '76 open', '24 inconclusive',
                  '95 open', 'three inconclusive', '46 inspected', '67 unread', 'L1 and L6',
                  'USD 5,200', 'USD 36,000', 'PromptBench', 'twenty paired families',
                  'execution failure', 'causaleffect', 'DAGitty', 'USD 34,000',
                  'USD 11,375', 'returned unsupported', 'not-yet-treated', 'Ananke 0.5.0',
                  'USD 400', 'USD 50', 'USD 350', 'cross-world coupling', 'Other/Proprietary',
                  'Identifiability', 'USD 80', 'USD 20', 'DAG/PDAG', 'DuckDB', 'USD 75', 'read-only', 'precondition', 'GCM', 'DEF-1', 'USD 160', 'USD 190', 'USD 30', '16/19', 'citation-chain', '8/15', '3/10', '16/135', 'USD 210', 'USD 1.50', 'September 2024']:
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
        'All70 predecessor citation records survive unchanged;76 cited records have bound local evidence.',
        'All prior funding, servicing, graph, panel, identification, causal-agent and economic arguments survive.',
        'Current-reader page/source counts and reuse counts match the effective receipt snapshot.',
        'Historical evaluation and code surveys retain their source limitations, finite-pool variable conflict and version/footer discrepancy.',
        'Finite selection, causal acceptance and all-request costs remain distinct; exact assumed economics do not imply live quality.',
        'Public conformance precedes costly bank experiments without pretending to validate institutional truth.'
    ]
    limitations = [
        'Author source, arithmetic and extracted-page review; no independent or rendered visual acceptance.',
        'Full release reconciliation, mandatory repairs, Q1/Q5 and final proposal acceptance remain open.',
        'No model execution, current ranking, full census, constituent-package admission or bank ROI is granted.'
    ]
    write(BASE/'author-review.json', dict(status='pass', issues=[],
        reviewer=dict(name='Codex author/coordinator', kind='author'),
        scope='Preserving current-reader sponsor source and content review',
        sponsor=report['reader_copy'], paired_monograph=report['paired_monograph'],
        findings=findings, evidence=evidence, limitations=limitations,
        visual_acceptance=False, final_acceptance=False))
    manifest = dict(kind='working_sponsor', pdf=report['reader_copy'], pages=report['pages'],
        paired_monograph=report['paired_monograph'],
        predecessor=ref(ROOT/'docs/sponsor_proposal_java_identification_reviewed_2026-10-19.pdf', 'Preserved predecessor sponsor'),
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
    run.commit(ROOT, digest, state, dict(action='publish_evaluation_code_working_sponsor',
        release=delivery['release'], prior_operation_preserved=True, final_acceptance=False))
    print(json.dumps(dict(published=delivery['path'], pages=report['pages'], records=76,
        paired_monograph=state['reader']['path'], review='pass', visual_acceptance=False,
        final_acceptance=False)))


if __name__ == '__main__':
    main()

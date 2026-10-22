#!/usr/bin/env python3
"""Review and publish exact-reader sponsor while preserving all prior evidence."""
import argparse
import json
from pathlib import Path
import re

import build_detailed_workflow_sponsor_20261023 as build
from review_publish_bayesian_commercial_sponsor_20261022 import sections
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run, core, ROOT, BASE = build.run, build.core, build.ROOT, build.BASE
read = lambda p: json.loads(p.read_text())


def review():
    assert not (BASE / 'author-review.json').exists()
    report, audit, progress = [read(BASE / n) for n in ['build-report.json', 'source-audit.json', 'progress-evidence.json']]
    for record in [report, audit, progress, read(BASE / 'plan-review.json')]:
        verify_bindings(record)
    assert report['cited_records'] == len(audit['sources']) == 323
    assert not report['empty_pages'] and not report['text_bounds_issues']
    assert all('Underfull' in warning for warning in report['warnings'])
    assert not report['visual_acceptance'] and not report['final_proposal_acceptance']
    assert read(BASE / 'economics-results.json') == build.engine.economics.calculate()
    old = {s['integrated_citation_key']: s for s in read(build.PRIOR / 'source-audit.json')['sources']}
    current = {s['integrated_citation_key']: s for s in audit['sources']}
    assert all(current[k] == value for k, value in old.items())
    additions = read(build.reader.BASE / 'source-audit.json')
    assert current.keys() - old.keys() == {s['integrated_citation_key'] for s in additions['sources']} | {
        'sp23dw_reader', 'sp23dw_progress'}
    manuscript = (BASE / 'proposal.md').read_text()
    assert manuscript == build.manuscript(progress['reader']['pages'])
    before, after = sections((build.PRIOR / 'proposal.md').read_text()), sections(manuscript)
    for heading, body in before.items():
        if heading != '# The decision this proposal supports':
            assert after[heading].replace('sp23dw_progress', 'sp23sm_progress') == body, heading
    assert set(after) - set(before) == {'# Preserve the requested population through workflow failures'}
    cited = {k.strip() for group in re.findall(build.engine.shared.CITE, manuscript) for k in group.split(',')}
    assert cited == current.keys()
    text = ' '.join((BASE / 'reader.txt').read_text().split()).replace('- ', '-').replace('−', '-')
    for token in [f'{progress["reader"]["pages"]:,} pages', '946 audited', '223 genuine scholarly PDFs',
        '63 inspected', '50 unread', 'USD -11', 'USD 9', 'USD 20', '[-21,29]',
        '15.0.2', '7 October 2026', 'USD 5,200', 'USD 36,000']:
        assert token.lower() in text.lower(), token
    state = core.read(ROOT, core.STATE)
    assert state['execution_runtime']['active'] is None
    assert run.same_reader(state['reader'], report['paired_monograph'])
    assert run.same_reader(state['reader'], progress['reader'])
    snapshot = build.engine.snapshot(state)
    for key in ['software_cells', 'reuse_decisions', 'chapter_reviews', 'llm_task_reviews', 'integration_requirements']:
        assert progress[key] == snapshot[key], key
    assert {q['id']: q['status'] for q in run.status(ROOT, state)['proposal_gaps']} == dict(
        Q1='open', Q2='pass', Q3='pass', Q4='pass', Q5='open')
    evidence = [ref(BASE / n, 'Reviewed exact paired sponsor') for n in ['plan-review.json', 'source-audit.json',
        'build-report.json', 'economics-results.json', 'proposal.md', 'reader.txt', 'progress-evidence.json']]
    evidence += [ref(Path(__file__), 'Preservation and substantive delta review'),
        ref(build.reader.BASE / 'release-source-review.json', 'Reviewed exact paired monograph')]
    write(BASE / 'author-review.json', dict(status='pass', issues=[], reviewer=dict(name='Codex author/coordinator', kind='author'),
        scope='Detailed workflow findings and exact-reader paired sponsor', sponsor=report['reader_copy'],
        paired_monograph=report['paired_monograph'], evidence=evidence,
        findings=['All314 prior citation identities and prior substantive sections survive.',
            'All323 current citations are audited; monetary construction and edition limits remain explicit.',
            'No failed cohort is silently removed from the declared target.',
            'The proposal recommends a bounded public/generated test before expensive bank work.'],
        limitations=['Author source/arithmetic/text review only; visual and final acceptance remain open.',
            'Q1/Q5, mandatory repairs, temporal omissions, wider coverage, rights, price and native qualification remain open.'],
        visual_acceptance=False, final_acceptance=False))
    print(json.dumps(dict(review='pass', pages=report['pages'], records=323, paired_monograph=report['paired_monograph'])))


def publish():
    report, record = [read(BASE / n) for n in ['build-report.json', 'author-review.json']]
    verify_bindings(report)
    verify_bindings(record)
    assert record['status'] == 'pass' and not record['issues']
    assert run.same_reader(record['sponsor'], report['reader_copy'])
    state = core.read(ROOT, core.STATE)
    assert state['execution_runtime']['active'] is None
    assert run.same_reader(state['reader'], report['paired_monograph'])
    assert not (BASE / 'working-release.json').exists()
    evidence = [ref(BASE / n, 'Reviewed paired sponsor') for n in
        ['build-report.json', 'author-review.json', 'source-audit.json', 'reader.txt']]
    evidence.append(ref(Path(__file__), 'Consume successful immutable author review'))
    manifest = dict(kind='working_sponsor', pdf=report['reader_copy'], pages=report['pages'],
        paired_monograph=report['paired_monograph'], predecessor=ref(build.PRIOR / 'reader/sponsor-proposal.pdf', 'Preserved sponsor'),
        predecessor_release=ref(build.PRIOR / 'working-release.json', 'Preserved paired release'),
        predecessor_operation=state['execution_program']['results']['RELEASE.SPONSOR'],
        build=ref(BASE / 'build-report.json', 'Exact paired build'), review=ref(BASE / 'author-review.json', 'Author review'),
        evidence=evidence, visual_acceptance=False, final_acceptance=False)
    verify_bindings(manifest)
    write(BASE / 'working-release.json', manifest)
    digest = core.sha(ROOT / core.STATE)
    delivery = {k: report['reader_copy'][k] for k in ['path', 'sha256']}
    delivery.update(pages=report['pages'], kind='working_sponsor',
        status='Working sponsor; visual and final acceptance remain open', paired_monograph=report['paired_monograph'],
        release=ref(BASE / 'working-release.json', 'Detailed-workflow paired sponsor'))
    assert not any(x['path'] == delivery['path'] for x in state['deliveries'])
    state['deliveries'].append(delivery)
    run.commit(ROOT, digest, state, dict(action='publish_detailed_workflow_sponsor', release=delivery['release'],
        prior_operation_preserved=True, final_acceptance=False))
    print(json.dumps(dict(published=delivery['path'], pages=delivery['pages'], final_acceptance=False)))


if __name__ == '__main__':
    commands = dict(review=review, publish=publish)
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=commands)
    commands[parser.parse_args().command]()

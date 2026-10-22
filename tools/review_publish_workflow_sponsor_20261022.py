#!/usr/bin/env python3
"""Review preservation and publish the sponsor paired to the workflow reader."""
import json
from pathlib import Path
import re

import build_workflow_sponsor_20261022 as build
from review_publish_bayesian_commercial_sponsor_20261022 import sections
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run, core, ROOT, BASE = build.run, build.core, build.ROOT, build.BASE
read = lambda p: json.loads(p.read_text())


def review():
    report, audit, progress = [read(BASE / n) for n in
        ['build-report.json', 'source-audit.json', 'progress-evidence.json']]
    for record in [report, audit, progress, read(BASE / 'plan-review.json')]:
        verify_bindings(record)
    assert report['cited_records'] == len(audit['sources']) == 305
    assert not report['empty_pages'] and not report['text_bounds_issues']
    assert all('Underfull' in warning for warning in report['warnings'])
    assert not report['visual_acceptance'] and not report['final_proposal_acceptance']
    assert read(BASE / 'economics-results.json') == build.engine.economics.calculate()

    prior = read(build.PRIOR / 'source-audit.json')
    old = {s['integrated_citation_key']: s for s in prior['sources']}
    current = {s['integrated_citation_key']: s for s in audit['sources']}
    assert all(current[k] == value for k, value in old.items())
    reader_audit = read(build.reader.OUT / 'source-audit.json')
    additions = read(build.reader.BASE / 'source-audit.json')
    assert {s['integrated_citation_key'] for s in additions['sources']} <= current.keys() - old.keys()
    assert {'sp22wf_reader', 'sp22wf_progress'} <= current.keys() - old.keys()

    manuscript = (BASE / 'proposal.md').read_text()
    assert manuscript == build.manuscript(progress['reader']['pages'])
    old_sections = sections((build.PRIOR / 'proposal.md').read_text())
    new_sections = sections(manuscript)
    changed = {'# The decision this proposal supports', '# What remains before a complete proposal'}
    for heading, body in old_sections.items():
        if heading not in changed:
            assert new_sections[heading] == body, heading
    assert set(new_sections) - set(old_sections) == {'# Recover the scientific request with the job'}
    cited = {key.strip() for group in re.findall(build.engine.shared.CITE, manuscript)
             for key in group.split(',')}
    assert cited == current.keys()

    text = ' '.join((BASE / 'reader.txt').read_text().split())
    c = progress['software_cells']
    reuse = progress['reuse_decisions']
    for token in [f'{progress["reader"]["pages"]:,} pages',
        f'{len(reader_audit["sources"])} audited', '221 genuine scholarly PDFs',
        f'{c["open"]} open', f'{c["inconclusive"]} inconclusive',
        f'{reuse["open"]} open', '61 inspected', '52 unread',
        '14/3', 'all six write attempts', '7 October 2026', 'Dataiku',
        'historical coverage remaining open', 'USD 5,200', 'USD 36,000']:
        assert token.lower() in text.lower(), token
    assert c == {'pass': 2, 'inconclusive': 39, 'open': 61, 'total': 102}
    assert reuse == {'pass': 31, 'inconclusive': 3, 'open': 81, 'total': 115}

    state = core.read(ROOT, core.STATE)
    assert state['execution_runtime']['active'] is None
    assert run.same_reader(state['reader'], report['paired_monograph'])
    assert run.same_reader(state['reader'], progress['reader'])
    status = run.status(ROOT, state)
    assert status['recorded_proposal_operations'] == 189
    assert {q['id']: q['status'] for q in status['proposal_gaps']} == dict(
        Q1='open', Q2='pass', Q3='pass', Q4='pass', Q5='open')

    evidence = [ref(BASE / n, 'Reviewed sponsor evidence') for n in
        ['plan-review.json', 'source-audit.json', 'build-report.json', 'economics-results.json',
         'proposal.md', 'reader.txt', 'progress-evidence.json']]
    evidence += [ref(Path(__file__), 'Exact sponsor preservation and pairing'),
        ref(build.reader.BASE / 'release-source-review.json', 'Reviewed paired monograph')]
    findings = [f'All {len(old)} prior citation identities survive; all {len(current)} cited records are audited.',
        'Earlier substantive sponsor sections survive; current reader, census and coverage counts are explicit.',
        'The commercial workflow addition separates documented current mechanisms, authored arithmetic, proposed public tests and later native qualification.',
        'The reader and sponsor are bound by exact hashes; no vendor execution, bank return or final proposal acceptance is claimed.']
    limitations = ['Author source, arithmetic and text-layout review only; no independent or rendered visual acceptance.',
        'Q1/Q5 and all mandatory repairs remain open; historical coverage and native execution remain unqualified.',
        'No bank economics, platform reliability or adoption is established.']
    write(BASE / 'author-review.json', dict(status='pass', issues=[],
        reviewer=dict(name='Codex author/coordinator', kind='author'),
        scope='Preserving workflow sponsor and exact-reader review', sponsor=report['reader_copy'],
        paired_monograph=report['paired_monograph'], findings=findings, evidence=evidence,
        limitations=limitations, visual_acceptance=False, final_acceptance=False))
    print(json.dumps(dict(review='pass', pages=report['pages'], source_records=len(current),
        prior_records=len(old), paired_monograph=report['paired_monograph'], visual_acceptance=False)))


def publish():
    review()
    report = read(BASE / 'build-report.json')
    state = core.read(ROOT, core.STATE)
    assert run.same_reader(state['reader'], report['paired_monograph'])
    assert state['execution_runtime']['active'] is None
    evidence = [ref(BASE / n, 'Reviewed paired sponsor') for n in
        ['build-report.json', 'author-review.json', 'source-audit.json', 'reader.txt']]
    manifest = dict(kind='working_sponsor', pdf=report['reader_copy'], pages=report['pages'],
        paired_monograph=report['paired_monograph'],
        predecessor=ref(build.PRIOR / 'reader/sponsor-proposal.pdf', 'Preserved sponsor'),
        predecessor_release=ref(build.PRIOR / 'working-release.json', 'Preserved sponsor release'),
        predecessor_operation=state['execution_program']['results']['RELEASE.SPONSOR'],
        build=ref(BASE / 'build-report.json', 'Sponsor build'),
        review=ref(BASE / 'author-review.json', 'Exact-reader author review'),
        evidence=evidence, visual_acceptance=False, final_acceptance=False)
    verify_bindings(manifest)
    write(BASE / 'working-release.json', manifest)
    digest = core.sha(ROOT / core.STATE)
    delivery = {k: report['reader_copy'][k] for k in ['path', 'sha256']}
    delivery.update(pages=report['pages'], kind='working_sponsor',
        status='Working sponsor; visual and final acceptance remain open',
        paired_monograph=report['paired_monograph'],
        release=ref(BASE / 'working-release.json', 'Preserving workflow sponsor'))
    assert not any(x['path'] == delivery['path'] for x in state['deliveries'])
    state['deliveries'].append(delivery)
    run.commit(ROOT, digest, state, dict(action='publish_workflow_sponsor', release=delivery['release'],
        prior_operation_preserved=True, final_acceptance=False))
    print(json.dumps(dict(published=delivery['path'], pages=delivery['pages'],
        paired_monograph=state['reader']['path'], final_acceptance=False)))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['review', 'publish'])
    {'review': review, 'publish': publish}[parser.parse_args().command]()

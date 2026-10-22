#!/usr/bin/env python3
"""Review and publish a preserving sponsor without rewriting completed evidence."""
import argparse
import json
from pathlib import Path
import re

import build_semantics_sponsor_20261023 as build
from review_publish_bayesian_commercial_sponsor_20261022 import sections
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run, core, ROOT, BASE = build.run, build.core, build.ROOT, build.BASE
read = lambda p: json.loads(p.read_text())


def review():
    report, audit, progress = [read(BASE / n) for n in
        ['build-report.json', 'source-audit.json', 'progress-evidence.json']]
    for record in [report, audit, progress, read(BASE / 'plan-review.json')]:
        verify_bindings(record)
    assert report['cited_records'] == len(audit['sources'])
    assert not report['empty_pages'] and not report['text_bounds_issues']
    assert all('Underfull' in warning for warning in report['warnings'])
    assert not report['visual_acceptance'] and not report['final_proposal_acceptance']
    assert read(BASE / 'economics-results.json') == build.engine.economics.calculate()
    prior = read(build.PRIOR / 'source-audit.json')
    old = {s['integrated_citation_key']: s for s in prior['sources']}
    current = {s['integrated_citation_key']: s for s in audit['sources']}
    assert all(current[k] == value for k, value in old.items())
    additions = read(build.reader.BASE / 'source-audit.json')
    reader_audit = read(build.reader.OUT / 'source-audit.json')
    assert current.keys() - old.keys() == {s['integrated_citation_key'] for s in additions['sources']} | {
        'sp23sm_reader', 'sp23sm_progress'}
    manuscript = (BASE / 'proposal.md').read_text()
    assert manuscript == build.manuscript(progress['reader']['pages'])
    old_sections = sections((build.PRIOR / 'proposal.md').read_text())
    new_sections = sections(manuscript)
    changed = {'# The decision this proposal supports', '# What remains before a complete proposal'}
    for heading, body in old_sections.items():
        if heading not in changed:
            normalized = new_sections[heading].replace('sp23sm_reader', 'sp22wf_reader').replace(
                'sp23sm_progress', 'sp22wf_progress')
            assert normalized == body, heading
    assert set(new_sections) - set(old_sections) == {'# Preserve the intervention before investing in an answer'}
    cited = {key.strip() for group in re.findall(build.engine.shared.CITE, manuscript) for key in group.split(',')}
    assert cited == current.keys()
    text = ' '.join((BASE / 'reader.txt').read_text().split()).replace('- ', '-')
    c, reuse = progress['software_cells'], progress['reuse_decisions']
    for token in [f'{progress["reader"]["pages"]:,} pages', f'{len(reader_audit["sources"])} audited',
        '223 genuine scholarly PDFs', f'{c["open"]} open', f'{c["inconclusive"]} inconclusive',
        f'{reuse["open"]} open', '63 inspected', '50 unread', 'USD 90', 'USD -10',
        '18.24', '107/9', 'NCSA', 'AGPL', '2.36', '2.12', '7 October 2026', 'USD 5,200', 'USD 36,000']:
        assert token.lower() in text.lower(), token
    state = core.read(ROOT, core.STATE)
    assert state['execution_runtime']['active'] is None
    assert run.same_reader(state['reader'], report['paired_monograph'])
    assert run.same_reader(state['reader'], progress['reader'])
    current_progress = build.engine.snapshot(state)
    for key in ['software_cells', 'reuse_decisions', 'chapter_reviews', 'llm_task_reviews', 'integration_requirements']:
        assert progress[key] == current_progress[key], key
    assert {q['id']: q['status'] for q in run.status(ROOT, state)['proposal_gaps']} == dict(
        Q1='open', Q2='pass', Q3='pass', Q4='pass', Q5='open')
    evidence = [ref(BASE / n, 'Reviewed sponsor evidence') for n in ['plan-review.json', 'source-audit.json',
        'build-report.json', 'economics-results.json', 'proposal.md', 'reader.txt', 'progress-evidence.json']]
    evidence += [ref(Path(__file__), 'Exact sponsor preservation review'),
        ref(build.reader.BASE / 'release-source-review.json', 'Reviewed paired reader')]
    write(BASE / 'author-review.json', dict(status='pass', issues=[],
        reviewer=dict(name='Codex author/coordinator', kind='author'),
        scope='Preserving semantic findings and exact-reader sponsor review', sponsor=report['reader_copy'],
        paired_monograph=report['paired_monograph'], evidence=evidence,
        findings=[f'All{len(old)} prior citation identities are preserved; all{len(current)} current citations are audited.',
            'Earlier substantive sections are preserved, with explicit current-reader/census/coverage reconciliation.',
            'New causal and software comparisons retain edition, arithmetic, rights and execution limits.',
            'The sponsor binds exact reader bytes and proposes public/generated tests before costly bank studies.'],
        limitations=['Author source/arithmetic/text review only; no independent or visual acceptance.',
            'Q1/Q5 and all mandatory repairs remain open; no native capability, bank return or adoption established.'],
        visual_acceptance=False, final_acceptance=False))
    print(json.dumps(dict(review='pass', pages=report['pages'], prior_records=len(old),
        records=len(current), paired_monograph=report['paired_monograph'], visual_acceptance=False)))


def publish():
    report, review_record = [read(BASE / n) for n in ['build-report.json', 'author-review.json']]
    verify_bindings(report)
    verify_bindings(review_record)
    assert review_record['status'] == 'pass' and not review_record['issues']
    assert run.same_reader(review_record['sponsor'], report['reader_copy'])
    assert run.same_reader(review_record['paired_monograph'], report['paired_monograph'])
    state = core.read(ROOT, core.STATE)
    assert state['execution_runtime']['active'] is None
    assert run.same_reader(state['reader'], report['paired_monograph'])
    evidence = [ref(BASE / n, 'Reviewed paired sponsor') for n in
        ['build-report.json', 'author-review.json', 'source-audit.json', 'reader.txt']]
    evidence.append(ref(Path(__file__), 'Consume immutable successful author review'))
    manifest = dict(kind='working_sponsor', pdf=report['reader_copy'], pages=report['pages'],
        paired_monograph=report['paired_monograph'], predecessor=ref(build.PRIOR / 'reader/sponsor-proposal.pdf', 'Preserved sponsor'),
        predecessor_release=ref(build.PRIOR / 'working-release.json', 'Preserved sponsor release'),
        predecessor_operation=state['execution_program']['results']['RELEASE.SPONSOR'],
        build=ref(BASE / 'build-report.json', 'Paired build'), review=ref(BASE / 'author-review.json', 'Author review'),
        evidence=evidence, visual_acceptance=False, final_acceptance=False)
    verify_bindings(manifest)
    write(BASE / 'working-release.json', manifest)
    digest = core.sha(ROOT / core.STATE)
    delivery = {k: report['reader_copy'][k] for k in ['path', 'sha256']}
    delivery.update(pages=report['pages'], kind='working_sponsor',
        status='Working sponsor; visual and final acceptance remain open', paired_monograph=report['paired_monograph'],
        release=ref(BASE / 'working-release.json', 'Preserving semantics sponsor'))
    assert not any(x['path'] == delivery['path'] for x in state['deliveries'])
    state['deliveries'].append(delivery)
    run.commit(ROOT, digest, state, dict(action='publish_semantics_sponsor', release=delivery['release'],
        prior_operation_preserved=True, final_acceptance=False))
    print(json.dumps(dict(published=delivery['path'], pages=delivery['pages'],
        paired_monograph=state['reader']['path'], final_acceptance=False)))


if __name__ == '__main__':
    commands = dict(review=review, publish=publish)
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=commands)
    commands[parser.parse_args().command]()

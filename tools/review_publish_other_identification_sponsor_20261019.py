#!/usr/bin/env python3
"""Review source preservation and exact-reader pairing for the Julia/JavaScript sponsor."""
import json
from pathlib import Path
import re

import build_other_identification_sponsor_20261019 as build
import sponsor_economics_20261013 as economics
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run, core, ROOT, BASE = build.run, build.core, build.ROOT, build.BASE
read = lambda p: json.loads(p.read_text())


def sections(text):
    parts = re.split(r'(?m)^(#{1,2} .+)$', text)
    return {parts[i]: parts[i+1] for i in range(1, len(parts), 2)}


def main():
    report, audit, progress = [read(BASE/n) for n in ['build-report.json', 'source-audit.json', 'progress-evidence.json']]
    for record in [report, audit, progress, read(BASE/'plan-review.json')]:
        verify_bindings(record)
    assert report['cited_records'] == len(audit['sources'])
    assert not report['empty_pages'] and not report['text_bounds_issues']
    assert all('Underfull' in warning for warning in report['warnings'])
    assert report['visual_acceptance'] is False and report['final_proposal_acceptance'] is False
    assert read(BASE/'economics-results.json') == economics.calculate()
    prior = read(build.PRIOR/'source-audit.json')
    before = {s['integrated_citation_key']: s for s in prior['sources']}
    after = {s['integrated_citation_key']: s for s in audit['sources']}
    assert len(after) == len(before)+5 and all(after[k] == v for k, v in before.items())
    current = (BASE/'proposal.md').read_text()
    original = (build.PRIOR/'proposal.md').read_text()
    pages = progress['reader']['pages']
    assert current == build.manuscript(pages)
    old_sections, new_sections = sections(original), sections(current)
    changed = {'# The decision this proposal supports', '# What remains before a complete proposal'}
    for heading, content in old_sections.items():
        if heading not in changed:
            assert new_sections[heading] == content, heading
    assert set(new_sections)-set(old_sections) == {'## Julia and JavaScript: an adjustment search is only part of identification'}
    cited = {k.strip() for group in re.findall(build.shared.CITE, current) for k in group.split(',')}
    assert cited == after.keys()
    text = ' '.join((BASE/'reader.txt').read_text().split())
    records = len(read(build.reader.OUT/'source-audit.json')['sources'])
    for token in [f'{pages:,} pages', f'{records} audited', '207 genuine', '73 open', '27 inconclusive',
        '93 open', 'three inconclusive', '48 inspected', '65 unread', 'USD 5,200', 'USD 36,000',
        'EconML', 'Julia', 'DAGitty', 'USD 5', 'USD 17.50', 'USD -7.50',
        'One empty adjustment set differs from no emitted solutions', 'no executable integration permission']:
        assert token.lower() in text.lower(), token
    state = core.read(ROOT, core.STATE)
    assert state['execution_runtime']['active'] is None
    assert run.same_reader(state['reader'], report['paired_monograph'])
    assert run.same_reader(state['reader'], progress['reader'])
    evidence = [ref(BASE/n, 'Inspected sponsor evidence') for n in ['plan-review.json', 'source-audit.json',
        'build-report.json', 'economics-results.json', 'proposal.md', 'reader.txt', 'progress-evidence.json']]
    evidence += [ref(Path(__file__), 'Source preservation, economics and exact-reader pairing')]
    findings = [f'All {len(before)} prior citation records survive unchanged; {len(after)} cited records are audited.',
        'All earlier substantive sections survive; only current-reader and remaining-gap summary fields are refreshed.',
        'Julia/JavaScript coverage remains inconclusive without granting executable integration.',
        'Graph editing, adjustment search, identification, completion and future native tests are distinguished.',
        'Assumed monetary comparison reproduces; public prototype costs and bank gates remain unmeasured.']
    limitations = ['Author source, arithmetic and extracted-text review; no independent or rendered visual acceptance.',
        'Full mandatory repairs, Q1/Q5 and final proposal acceptance remain open.',
        'No Julia/JavaScript runtime comparison, general theorem, measured uncertainty or bank benefit is granted.']
    write(BASE/'author-review.json', dict(status='pass', issues=[],
        reviewer=dict(name='Codex author/coordinator', kind='author'),
        scope='Preserving Julia/JavaScript sponsor and exact-reader content review', sponsor=report['reader_copy'],
        paired_monograph=report['paired_monograph'], findings=findings, evidence=evidence,
        limitations=limitations, visual_acceptance=False, final_acceptance=False))
    manifest = dict(kind='working_sponsor', pdf=report['reader_copy'], pages=report['pages'],
        paired_monograph=report['paired_monograph'],
        predecessor=ref(ROOT/'docs/sponsor_proposal_econml_reviewed_2026-10-19.pdf', 'Preserved sponsor'),
        predecessor_release=ref(build.PRIOR/'working-release.json', 'Preserved prior release'),
        predecessor_operation=state['execution_program']['results']['RELEASE.SPONSOR'],
        build=ref(BASE/'build-report.json', 'Actual dynamically counted sponsor build'),
        review=ref(BASE/'author-review.json', 'Author source and pairing review'), evidence=evidence,
        final_acceptance=False, visual_acceptance=False)
    verify_bindings(manifest)
    write(BASE/'working-release.json', manifest)
    digest = core.sha(ROOT/core.STATE)
    delivery = {k: report['reader_copy'][k] for k in ['path', 'sha256']}
    delivery.update(pages=report['pages'], kind='working_sponsor',
        status='Working sponsor; exact-reader source review, visual/final acceptance open',
        paired_monograph=report['paired_monograph'], release=ref(BASE/'working-release.json', 'Preserving Julia/JavaScript sponsor'))
    assert not any(item['path'] == delivery['path'] for item in state['deliveries'])
    state['deliveries'].append(delivery)
    run.commit(ROOT, digest, state, dict(action='publish_other_identification_working_sponsor', release=delivery['release'],
        prior_operation_preserved=True, final_acceptance=False))
    print(json.dumps(dict(published=delivery['path'], pages=report['pages'], records=len(after),
        paired_monograph=state['reader']['path'], review='pass', visual_acceptance=False, final_acceptance=False)))


if __name__ == '__main__':
    main()

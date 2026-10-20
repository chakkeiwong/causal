#!/usr/bin/env python3
"""Review and publish the preserving expert-guided discovery sponsor successor."""
import json
from pathlib import Path
import re

import build_expert_averaging_sponsor_20261020 as build
import sponsor_economics_20261013 as economics
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run, core, ROOT, BASE = build.run, build.core, build.ROOT, build.BASE
read = lambda p: json.loads(p.read_text())


def sections(text):
    parts = re.split(r'(?m)^(#{1,2} .+)$', text)
    assert len({parts[i] for i in range(1, len(parts), 2)}) == len(parts)//2
    return {parts[i]: parts[i+1] for i in range(1, len(parts), 2)}


def main():
    report, audit, progress = [read(BASE/n) for n in
        ['build-report.json', 'source-audit.json', 'progress-evidence.json']]
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
    assert all(after[k] == v for k, v in before.items())
    expected_added = {'exec20_expert_averaging','exec20_expert_averaging_reference','sp20ea_reader','sp20ea_progress'}
    assert after.keys()-before.keys() == expected_added
    current = (BASE/'proposal.md').read_text()
    original = (build.PRIOR/'proposal.md').read_text()
    pages = progress['reader']['pages']
    assert current == build.manuscript(pages)
    old_sections, new_sections = sections(original), sections(current)
    changed = {'# The decision this proposal supports', '# What remains before a complete proposal'}
    for heading, content in old_sections.items():
        if heading not in changed:
            assert new_sections[heading] == content, heading
    assert set(new_sections)-set(old_sections) == {
        "## Use expert-guided ensembles to propose graphs with explicit limits"}
    cited = {k.strip() for group in re.findall(build.shared.CITE, current) for k in group.split(',')}
    assert cited == after.keys()
    text = ' '.join((BASE/'reader.txt').read_text().split())
    records = len(read(build.reader.OUT/'source-audit.json')['sources'])
    for token in [f'{pages:,} pages', f'{records} audited', '212 genuine', '70 open',
        '30 inconclusive', '91 open', 'three inconclusive', '53 inspected', '60 unread',
        'USD 5,200', 'USD 36,000', 'Julia', 'DAGitty', 'COAT', 'Feast', 'USD 15',
        'Stata', 'EViews', '50.5', 'USD 2,010', 'USD 283', 'DoubleML',
        'CausalGPS', 'causaldrf', 'USD 100', 'USD 35', 'missing treatment', '0.90', '0.58', 'simulated respondents', 'USD 55','fixest','51/16','USD 3.50','USD -0.50','0.9995','USD 70.04','USD 5.04','52%','65%','USD -8','calibration','adjudication','93.3%','43.9%','USD 14','20 October 2026']:
        assert token.lower() in text.lower(), token
    assert progress['software_cells'] == {'pass': 2, 'inconclusive': 30, 'open': 70, 'total': 102}
    assert progress['reuse_decisions'] == {'pass': 21, 'inconclusive': 3, 'open': 91, 'total': 115}
    state = core.read(ROOT, core.STATE)
    assert state['execution_runtime']['active'] is None
    assert run.same_reader(state['reader'], report['paired_monograph'])
    assert run.same_reader(state['reader'], progress['reader'])
    status = run.status(ROOT, state)
    assert status['recorded_proposal_operations'] == 165
    evidence = [ref(BASE/n, 'Inspected sponsor evidence') for n in ['plan-review.json',
        'source-audit.json', 'build-report.json', 'economics-results.json', 'proposal.md',
        'reader.txt', 'progress-evidence.json']]
    evidence += [ref(Path(__file__), 'Preservation, economics and exact-reader pairing')]
    findings = [f'All {len(before)} prior citation identities survive; {len(after)} cited records are audited.',
        'All earlier substantive sections survive; reader and software coverage fields are refreshed.',
        'Graph propositions, algorithm agreement, reported model evidence and identified effects remain distinct.',
        'Exact graph and Gaussian-law witnesses reproduce; margins20,-40 differ from an unjustified vote-based14. Printed specification questions do not allege native defects.',
        'Census is53 inspected and60 unread; native code, rights, inference and completeness stay open.',
        'The paired reader has 165 recorded proposal outcomes; no completed-program claim is made.']
    limits = ['Author source, arithmetic and extracted-text review; no independent or rendered visual acceptance.',
        'Mandatory repairs, Q1/Q5 and final proposal acceptance remain open.',
        'No native engine or LLM execution, measured product return or bank benefit is granted.']
    write(BASE/'author-review.json', dict(status='pass', issues=[],
        reviewer=dict(name='Codex author/coordinator', kind='author'),
        scope='Preserving expert-guided discovery sponsor and exact-reader content review',
        sponsor=report['reader_copy'], paired_monograph=report['paired_monograph'],
        findings=findings, evidence=evidence, limitations=limits,
        visual_acceptance=False, final_acceptance=False))
    manifest = dict(kind='working_sponsor', pdf=report['reader_copy'], pages=report['pages'],
        paired_monograph=report['paired_monograph'],
        predecessor=ref(build.PRIOR/'reader/sponsor-proposal.pdf', 'Preserved prior sponsor'),
        predecessor_release=ref(build.PRIOR/'working-release.json', 'Preserved prior release'),
        predecessor_operation=state['execution_program']['results']['RELEASE.SPONSOR'],
        build=ref(BASE/'build-report.json', 'Dynamically counted sponsor build'),
        review=ref(BASE/'author-review.json', 'Author source and pairing review'), evidence=evidence,
        final_acceptance=False, visual_acceptance=False)
    verify_bindings(manifest)
    write(BASE/'working-release.json', manifest)
    digest = core.sha(ROOT/core.STATE)
    delivery = {k: report['reader_copy'][k] for k in ['path', 'sha256']}
    delivery.update(pages=report['pages'], kind='working_sponsor',
        status='Working sponsor; exact-reader source review, visual/final acceptance open',
        paired_monograph=report['paired_monograph'],
        release=ref(BASE/'working-release.json', 'Preserving expert-guided discovery sponsor'))
    assert not any(item['path'] == delivery['path'] for item in state['deliveries'])
    state['deliveries'].append(delivery)
    run.commit(ROOT, digest, state, dict(action='publish_expert_averaging_working_sponsor',
        release=delivery['release'], prior_operation_preserved=True, final_acceptance=False))
    print(json.dumps(dict(published=delivery['path'], pages=report['pages'], records=len(after),
        paired_monograph=state['reader']['path'], review='pass', visual_acceptance=False, final_acceptance=False)))


if __name__ == '__main__':
    main()

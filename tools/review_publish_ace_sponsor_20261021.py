#!/usr/bin/env python3
"""Review and publish the preserving native effects sponsor successor."""
import json
from pathlib import Path
import re

import build_ace_sponsor_20261021 as build
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
    expected_added = {r['integrated_citation_key'] for r in read(build.reader.BASE/'source-audit.json')['sources']} | {'sp21ae_reader','sp21ae_progress'}
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
        "## Treat document extraction as a proposed causal structure"}
    cited = {k.strip() for group in re.findall(build.shared.CITE, current) for k in group.split(',')}
    assert cited == after.keys()
    text = ' '.join((BASE/'reader.txt').read_text().split())
    records = len(read(build.reader.OUT/'source-audit.json')['sources'])
    for token in [f'{pages:,} pages',f'{records} audited','216 genuine','66 open',
        '34 inconclusive','88 open','56 inspected','57 unread','USD 5,200','USD 36,000',
        'gfoRmula','StataNow','XBCF','flexBCF','82%','95%','USD 2.20','USD 2.50','USD -5','CausalityCheck','40.54%','23.2%','USD -13','USD 7','-1.76','4/17','1.5','0.995','198/199','USD -12','USD 8','ACE','21 October 2026']:
        assert token.lower() in text.lower(),token
    assert progress['software_cells']=={'pass':2,'inconclusive':34,'open':66,'total':102}
    assert progress['reuse_decisions']=={'pass':24,'inconclusive':3,'open':88,'total':115}
    state = core.read(ROOT, core.STATE)
    assert state['execution_runtime']['active'] is None
    assert run.same_reader(state['reader'], report['paired_monograph'])
    assert run.same_reader(state['reader'], progress['reader'])
    status = run.status(ROOT, state)
    assert status['recorded_proposal_operations'] == 174
    evidence = [ref(BASE/n, 'Inspected sponsor evidence') for n in ['plan-review.json',
        'source-audit.json', 'build-report.json', 'economics-results.json', 'proposal.md',
        'reader.txt', 'progress-evidence.json']]
    evidence += [ref(Path(__file__), 'Preservation, economics and exact-reader pairing')]
    findings = [f'All {len(before)} prior citation identities survive; {len(after)} cited records are audited.',
        'All earlier substantive sections survive; reader and software coverage fields are refreshed.',
        'Preserve source-supported roles, expert additions, metric meaning and intervention assumptions.',
        'Exact graph and interaction witnesses expose limits of aggregate metrics; opposite mechanisms give hypothetical margins -12 and 8.',
        'Census is56 inspected and57 unread; native code, rights, inference and completeness stay open.',
        'The paired reader has 174 recorded proposal outcomes; no completed-program claim is made.']
    limits = ['Author source, arithmetic and extracted-text review; no independent or rendered visual acceptance.',
        'Mandatory repairs, Q1/Q5 and final proposal acceptance remain open.',
        'No native engine or LLM execution, measured product return or bank benefit is granted.']
    write(BASE/'author-review.json', dict(status='pass', issues=[],
        reviewer=dict(name='Codex author/coordinator', kind='author'),
        scope='Preserving ACE bowtie extraction sponsor and exact-reader content review',
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
        release=ref(BASE/'working-release.json', 'Preserving ACE bowtie extraction sponsor'))
    assert not any(item['path'] == delivery['path'] for item in state['deliveries'])
    state['deliveries'].append(delivery)
    run.commit(ROOT, digest, state, dict(action='publish_ace_working_sponsor',
        release=delivery['release'], prior_operation_preserved=True, final_acceptance=False))
    print(json.dumps(dict(published=delivery['path'], pages=report['pages'], records=len(after),
        paired_monograph=state['reader']['path'], review='pass', visual_acceptance=False, final_acceptance=False)))


if __name__ == '__main__':
    main()

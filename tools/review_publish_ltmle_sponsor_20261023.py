#!/usr/bin/env python3
"""Review exact preserved sponsor sections and publish the paired successor."""
import argparse
import json
from pathlib import Path
import re
import build_ltmle_sponsor_20261023 as build
import ltmle_policy_oracle_v2_20261023 as oracle
from review_publish_bayesian_commercial_sponsor_20261022 import sections
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run, core, ROOT, BASE = build.run, build.core, build.ROOT, build.BASE
read = lambda p: json.loads(p.read_text())


def review():
    assert not (BASE / 'author-review.json').exists()
    report, audit, progress = [read(BASE / n) for n in ['build-report.json', 'source-audit.json', 'progress-evidence.json']]
    for item in [report, audit, progress, read(BASE / 'plan-review.json')]:
        verify_bindings(item)
    assert report['cited_records'] == len(audit['sources']) == 327
    assert not report['empty_pages'] and not report['text_bounds_issues']
    assert all('Underfull' in w for w in report['warnings'])
    assert not report['visual_acceptance'] and not report['final_proposal_acceptance']
    assert read(BASE / 'economics-results.json') == build.engine.economics.calculate()
    assert oracle.calculate() == read(build.READER_BASE / 'exact-results.json')
    before = {s['integrated_citation_key']: s for s in read(build.PRIOR / 'source-audit.json')['sources']}
    after = {s['integrated_citation_key']: s for s in audit['sources']}
    assert all(after[k] == v for k, v in before.items())
    assert after.keys() - before.keys() == {'exec23_ltmle_source', 'exec23_ltmle_exact', 'sp23lt_reader', 'sp23lt_progress'}
    manuscript = (BASE / 'proposal.md').read_text()
    assert manuscript == build.manuscript(progress['reader']['pages'])
    old, new = sections((build.PRIOR / 'proposal.md').read_text()), sections(manuscript)
    for heading, content in old.items():
        expected = content.replace('sp23dw_reader', 'sp23lt_reader').replace('sp23dw_progress', 'sp23lt_progress')
        if heading == '# The decision this proposal supports':
            expected = expected.replace('1,247 pages and 946 audited citation records', '1,251 pages and 948 audited citation records')
            expected = expected.replace('sp23lt_reader,', 'sp23lt_reader,sp23dw_reader,', 1)
        if heading == '# What remains before a complete proposal':
            expected = expected.replace('sp23lt_progress,', 'sp23lt_progress,sp23dw_progress,', 1)
            expected = expected.replace('The reuse register has 79 open', 'The reuse register has 78 open')
        assert new[heading] == expected, heading
    assert new.keys() - old.keys() == {'# Preserve longitudinal regimes and the requested decision population'}
    cited = {k.strip() for group in re.findall(build.engine.shared.CITE, manuscript) for k in group.split(',')}
    assert cited == after.keys()
    text = ' '.join((BASE / 'reader.txt').read_text().split()).replace('- ', '-').replace('−', '-')
    for token in ['1,251 pages', '948 audited', '223 genuine scholarly PDFs', '78 open', '63 inspected', '50 unread',
                  '13/60', '17/100', '7/75', '130/3', '340/3', '69/335', '139/850', '43/4020', '11/1700',
                  'influence-curve variance', 'USD 1,000 per default', 'USD 5,200', 'USD 36,000']:
        assert token.lower() in text.lower(), token
    state = core.read(ROOT, core.STATE)
    assert state['execution_runtime']['active'] is None
    assert run.same_reader(state['reader'], report['paired_monograph'])
    assert run.same_reader(state['reader'], progress['reader'])
    snapshot = build.engine.snapshot(state)
    for key in ['software_cells', 'reuse_decisions', 'chapter_reviews', 'llm_task_reviews', 'integration_requirements']:
        assert progress[key] == snapshot[key], key
    assert progress['reuse_decisions']['pass'] == 34 and progress['reuse_decisions']['open'] == 78
    assert {q['id']: q['status'] for q in run.status(ROOT, state)['proposal_gaps']} == dict(Q1='open', Q2='pass', Q3='pass', Q4='pass', Q5='open')
    evidence = [ref(BASE / n, 'Reviewed exact paired sponsor') for n in ['plan-review.json', 'source-audit.json',
        'build-report.json', 'economics-results.json', 'proposal.md', 'reader.txt', 'progress-evidence.json']]
    evidence += [ref(Path(__file__), 'Exact section preservation and source/arithmetic review'),
        ref(build.READER_BASE / 'release-source-review.json', 'Exact monograph author review'),
        ref(build.READER_BASE / 'sponsor-addition.md', 'Corrected scoped sponsor development'),
        ref(ROOT / 'tools/ltmle_policy_oracle_v2_20261023.py', 'Replayed finite law and covariance')]
    write(BASE / 'author-review.json', dict(status='pass', issues=[], reviewer=dict(name='Codex author/coordinator', kind='author'),
        scope='Longitudinal targets, censoring and household uncertainty; exact-reader sponsor reconciliation',
        sponsor=report['reader_copy'], paired_monograph=report['paired_monograph'], evidence=evidence,
        findings=['All323 prior source identities and substantive sections survive explicit citation/count replacements.',
            'All327 current citations are audited; the sponsor binds the actual1251-page reader.',
            'The probability law, full hardship table, observation mechanism and costs reproduce the cited exact risks and net values.',
            'Fallback IC variance retains supplied household aggregation; the reference choice does not admit native integration.'],
        limitations=['Author source/arithmetic/text review; visual and independent acceptance remain open.',
            'Q1/Q5, mandatory repairs, full coverage, native qualification and bank benefit remain open.'],
        visual_acceptance=False, final_acceptance=False))
    print(json.dumps(dict(review='pass', pages=report['pages'], records=327)))


def publish():
    report, review = [read(BASE / n) for n in ['build-report.json', 'author-review.json']]
    for item in [report, review]: verify_bindings(item)
    assert review['status'] == 'pass' and not review['issues']
    state = core.read(ROOT, core.STATE)
    assert state['execution_runtime']['active'] is None
    assert run.same_reader(state['reader'], report['paired_monograph'])
    assert run.same_reader(review['sponsor'], report['reader_copy'])
    assert not (BASE / 'working-release.json').exists()
    manifest = dict(kind='working_sponsor', pdf=report['reader_copy'], pages=report['pages'],
        paired_monograph=report['paired_monograph'], predecessor=ref(build.PRIOR / 'reader/sponsor-proposal.pdf', 'Preserved sponsor'),
        predecessor_release=ref(build.PRIOR / 'working-release.json', 'Preserved release'),
        predecessor_operation=state['execution_program']['results']['RELEASE.SPONSOR'],
        build=ref(BASE / 'build-report.json', 'Exact paired build'), review=ref(BASE / 'author-review.json', 'Author review'),
        evidence=[ref(BASE / n, 'Reviewed sponsor') for n in ['source-audit.json', 'reader.txt']] +
            [ref(Path(__file__), 'Consume successful immutable author review')], visual_acceptance=False, final_acceptance=False)
    verify_bindings(manifest)
    write(BASE / 'working-release.json', manifest)
    digest = core.sha(ROOT / core.STATE)
    delivery = {k: report['reader_copy'][k] for k in ['path', 'sha256']}
    delivery.update(pages=report['pages'], kind='working_sponsor', status='Working sponsor; visual and final acceptance remain open',
        paired_monograph=report['paired_monograph'], release=ref(BASE / 'working-release.json', 'Longitudinal paired sponsor'))
    assert not any(x['path'] == delivery['path'] for x in state['deliveries'])
    state['deliveries'].append(delivery)
    run.commit(ROOT, digest, state, dict(action='publish_ltmle_sponsor', release=delivery['release'], prior_operation_preserved=True, final_acceptance=False))
    print(json.dumps(dict(published=delivery['path'], pages=delivery['pages'], final_acceptance=False)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['review', 'publish'])
    {'review': review, 'publish': publish}[parser.parse_args().command]()

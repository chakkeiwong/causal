#!/usr/bin/env python3
"""Review sponsor preservation and publish a binding to the exact current reader."""
import json
from pathlib import Path
import re
import build_sensitivity_iv_sponsor_20261022 as build
from review_publish_bayesian_commercial_sponsor_20261022 import sections
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run,core,ROOT,BASE=build.run,build.core,build.ROOT,build.BASE
read=lambda p:json.loads(p.read_text())


def main():
    report,audit,progress=[read(BASE/n) for n in ['build-report.json','source-audit.json','progress-evidence.json']]
    for r in [report,audit,progress,read(BASE/'plan-review.json')]:verify_bindings(r)
    assert report['cited_records']==len(audit['sources'])
    assert not report['empty_pages'] and not report['text_bounds_issues']
    assert all('Underfull' in w for w in report['warnings'])
    assert not report['visual_acceptance'] and not report['final_proposal_acceptance']
    assert read(BASE/'economics-results.json')==build.engine.economics.calculate()
    before={s['integrated_citation_key']:s for s in read(build.PRIOR/'source-audit.json')['sources']}
    after={s['integrated_citation_key']:s for s in audit['sources']}
    assert all(after[k]==v for k,v in before.items())
    required={s['integrated_citation_key'] for s in read(build.reader.BASE/'source-audit.json')['sources']}|{'sp22si_reader','sp22si_progress'}
    assert required<=after.keys()-before.keys()
    original=(build.PRIOR/'proposal.md').read_text();current=(BASE/'proposal.md').read_text()
    assert current==build.manuscript(progress['reader']['pages'])
    old,new=sections(original),sections(current)
    changed={'# The decision this proposal supports','# What remains before a complete proposal'}
    for heading,content in old.items():
        if heading not in changed:assert new[heading]==content,heading
    assert set(new)-set(old)=={'# What sensitivity and IV engines must preserve'}
    cited={k.strip() for group in re.findall(build.engine.shared.CITE,current) for k in group.split(',')}
    assert cited==after.keys()
    text=' '.join((BASE/'reader.txt').read_text().split())
    c=progress['software_cells'];reuse=progress['reuse_decisions']
    for token in [f'{progress["reader"]["pages"]:,} pages',f'{len(read(build.reader.OUT/"source-audit.json")["sources"])} audited','219 genuine',
        f'{c["open"]} open',f'{c["inconclusive"]} inconclusive',f'{reuse["open"]} open',
        '59 inspected','54 unread','USD 5,200','USD 36,000','USD -6','Snowflake','HonestDiD','0.0183','0.0346','3.9233']:
        assert token.lower() in text.lower(),token
    assert c=={'pass':2,'inconclusive':39,'open':61,'total':102}
    assert reuse=={'pass':31,'inconclusive':3,'open':81,'total':115}
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active'] is None
    assert run.same_reader(state['reader'],report['paired_monograph']) and run.same_reader(state['reader'],progress['reader'])
    status=run.status(ROOT,state);assert status['recorded_proposal_operations']==189
    assert {q['id']:q['status'] for q in status['proposal_gaps']}==dict(Q1='open',Q2='pass',Q3='pass',Q4='pass',Q5='open')
    evidence=[ref(BASE/n,'Reviewed sponsor evidence') for n in ['plan-review.json','source-audit.json','build-report.json',
        'economics-results.json','proposal.md','reader.txt','progress-evidence.json']]+[
        ref(Path(__file__),'Exact preservation and pairing'),ref(build.reader.BASE/'release-source-review.json','Reviewed monograph argument')]
    findings=[f'All {len(before)} prior citation identities survive; {len(after)} cited records are audited.',
        'Earlier substantive sections and economic cases survive; reader and software/reuse counts are current.',
        'Trend restrictions, full covariance, projected rank and diagnostic distribution examples explain proposed interface and qualification requirements.',
        'HonestDiD remains reference-only. Python IV/RD coverage, solver environments, release equivalence and native admission remain open.']
    limits=['Author source/arithmetic/text review only; no independent or rendered visual acceptance.',
        'Q1/Q5 and all mandatory repairs remain open; no measured bank economics or native package execution.']
    write(BASE/'author-review.json',dict(status='pass',issues=[],reviewer=dict(name='Codex author/coordinator',kind='author'),
        scope='Preserving sensitivity and IV sponsor review',sponsor=report['reader_copy'],paired_monograph=report['paired_monograph'],
        findings=findings,evidence=evidence,limitations=limits,visual_acceptance=False,final_acceptance=False))
    manifest=dict(kind='working_sponsor',pdf=report['reader_copy'],pages=report['pages'],paired_monograph=report['paired_monograph'],
        predecessor=ref(build.PRIOR/'reader/sponsor-proposal.pdf','Preserved sponsor'),
        predecessor_release=ref(build.PRIOR/'working-release.json','Preserved release'),
        predecessor_operation=state['execution_program']['results']['RELEASE.SPONSOR'],
        build=ref(BASE/'build-report.json','Preserving build'),review=ref(BASE/'author-review.json','Exact-reader review'),
        evidence=evidence,final_acceptance=False,visual_acceptance=False)
    verify_bindings(manifest);write(BASE/'working-release.json',manifest)
    digest=core.sha(ROOT/core.STATE);delivery={k:report['reader_copy'][k] for k in ['path','sha256']}
    delivery.update(pages=report['pages'],kind='working_sponsor',status='Working sponsor; visual/final acceptance open',
        paired_monograph=report['paired_monograph'],release=ref(BASE/'working-release.json','Preserving sensitivity and IV sponsor'))
    assert not any(x['path']==delivery['path'] for x in state['deliveries'])
    state['deliveries'].append(delivery)
    run.commit(ROOT,digest,state,dict(action='publish_sensitivity_iv_sponsor',release=delivery['release'],prior_operation_preserved=True,final_acceptance=False))
    print(json.dumps(dict(published=delivery['path'],pages=report['pages'],records=len(after),review='pass',visual_acceptance=False)))


if __name__=='__main__':main()

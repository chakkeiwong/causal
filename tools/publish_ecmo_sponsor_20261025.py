#!/usr/bin/env python3
"""Verify preserving sponsor sources, current counts and exact reader pairing."""
import argparse,json,re
from pathlib import Path
import build_ecmo_sponsor_20261025 as build
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write
run,core,ROOT,BASE=build.run,build.core,build.ROOT,build.BASE;read=lambda p:json.loads(p.read_text())
def review():
    report,audit,progress=[read(BASE/n) for n in ['build-report.json','source-audit.json','progress-evidence.json']]
    for d in [report,audit,progress,read(BASE/'plan-review.json')]:verify_bindings(d)
    assert report['cited_records']==len(audit['sources'])==740 and not report['empty_pages'] and not report['text_bounds_issues']
    assert all('Underfull' in w for w in report['warnings']);assert read(BASE/'economics-results.json')==build.engine.economics.calculate()
    old={s['integrated_citation_key']:s for s in read(build.PRIOR/'source-audit.json')['sources']};new={s['integrated_citation_key']:s for s in audit['sources']}
    assert len(old)==735 and all(new[k]==v for k,v in old.items())
    assert new.keys()-old.keys()=={'exec24_ecmo_'+role for role in ['original','code','reference']}|{'sp25ecmo_reader','sp25ecmo_progress'}
    assert (BASE/'proposal.md').read_text()==build.manuscript(progress['reader']['pages'])
    raw_text=(BASE/'reader.txt').read_text();raw_text=re.sub(r'(?<=\w)-[ \t]*\n[ \t]*(?=\w)', '', raw_text);text=' '.join(raw_text.split()).replace('- ','-')
    for token in [f"{progress['reader']['pages']:,} pages",'1192 audited','258 genuine scholarly PDFs','53 inconclusive','46 open','101 passing','11 open','82 inspected','31 unread','Graph refinement needs a decision and measurement clock','296 recorded']:assert token in text,token
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active'] is None
    assert run.same_reader(state['reader'],report['paired_monograph']) and run.same_reader(state['reader'],progress['reader'])
    snapshot=build.engine.snapshot(state)
    for key in ['software_cells','reuse_decisions','chapter_reviews','llm_task_reviews','integration_requirements']:assert progress[key]==snapshot[key]
    assert progress['software_cells']['inconclusive']==53 and progress['software_cells']['open']==46
    assert progress['reuse_decisions']['pass']==101 and progress['reuse_decisions']['open']==11
    assert {q['id']:q['status'] for q in run.status(ROOT,state)['proposal_gaps']}==dict(Q1='open',Q2='pass',Q3='pass',Q4='pass',Q5='open')
    evidence=[ref(BASE/n,'Reviewed paired sponsor') for n in ['plan-review.json','source-audit.json','build-report.json','economics-results.json','proposal.md','reader.txt','progress-evidence.json']]+[ref(build.READER_BASE/'release-source-review.json','Preserved monograph'),ref(Path(__file__),'Review logic')]
    write(BASE/'author-review.json',dict(status='pass',issues=[],reviewer=dict(name='Codex author/coordinator',kind='author'),scope='Interference comparison and complete current proposal status',sponsor=report['reader_copy'],paired_monograph=report['paired_monograph'],evidence=evidence,findings=['All735 previous citations and historical arguments retained;740records audited.','Exact reader pairing and current counts verified; historical counts remain dated.','Authored economics and static findings do not admit native integration.'],limitations=['Source/arithmetic/all-page text review only; visual, independent and final acceptance open.','Q1/Q5, mandatory repairs, unsupported server contracts and native/bank qualification remain open.'],visual_acceptance=False,final_acceptance=False))
    print(json.dumps(dict(review='pass',pages=report['pages'],records=740)))
def publish():
    report=read(BASE/'build-report.json');review=read(BASE/'author-review.json');verify_bindings(report);verify_bindings(review)
    assert review['status']=='pass' and not review['issues'];state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active'] is None and run.same_reader(state['reader'],report['paired_monograph'])
    manifest=dict(kind='working_sponsor',pdf=report['reader_copy'],pages=report['pages'],paired_monograph=report['paired_monograph'],predecessor=ref(build.PRIOR/'reader/sponsor-proposal.pdf','Preserved sponsor'),predecessor_release=ref(build.PRIOR/'working-release.json','Preserved release'),predecessor_operation=state['execution_program']['results']['RELEASE.SPONSOR'],build=ref(BASE/'build-report.json','Exact build'),review=ref(BASE/'author-review.json','Author review'),evidence=[ref(BASE/n,'Reviewed source') for n in ['source-audit.json','reader.txt']]+[ref(Path(__file__),'Publisher')],visual_acceptance=False,final_acceptance=False)
    write(BASE/'working-release.json',manifest);digest=core.sha(ROOT/core.STATE);delivery={k:report['reader_copy'][k] for k in ['path','sha256']};delivery.update(pages=report['pages'],kind='working_sponsor',status='Working sponsor; visual and final acceptance remain open',paired_monograph=report['paired_monograph'],release=ref(BASE/'working-release.json','Backend-census paired sponsor'))
    assert not any(x['path']==delivery['path'] for x in state['deliveries']);state['deliveries'].append(delivery);run.commit(ROOT,digest,state,dict(action='publish_ecmo_sponsor',release=delivery['release'],prior_operation_preserved=True,final_acceptance=False));print(json.dumps(dict(published=delivery['path'],pages=delivery['pages'],final_acceptance=False)))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['review','publish']);globals()[p.parse_args().command]()

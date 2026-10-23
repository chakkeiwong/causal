#!/usr/bin/env python3
"""Review a preserving sponsor and bind it to the exact structured-model reader."""
import argparse,json,re
from pathlib import Path
import build_tigramite_sponsor_20261023 as build
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write
run,core,ROOT,BASE=build.run,build.core,build.ROOT,build.BASE
read=lambda p:json.loads(p.read_text())

def review():
 report,audit,progress=[read(BASE/n) for n in ['build-report.json','source-audit.json','progress-evidence.json']]
 for d in [report,audit,progress,read(BASE/'plan-review.json')]:verify_bindings(d)
 assert report['cited_records']==len(audit['sources'])==347
 assert not report['empty_pages'] and not report['text_bounds_issues']
 assert all('Underfull' in w for w in report['warnings'])
 assert read(BASE/'economics-results.json')==build.engine.economics.calculate()
 assert build.reader.calculate()==read(build.READER_BASE/'exact-results.json')
 old={s['integrated_citation_key']:s for s in read(build.PRIOR/'source-audit.json')['sources']};new={s['integrated_citation_key']:s for s in audit['sources']}
 assert len(old)==343 and all(new[k]==v for k,v in old.items())
 assert new.keys()-old.keys()=={'exec23_tigramite_reuse_source','exec23_tigramite_reference','sp23tg_reader','sp23tg_progress'}
 manuscript=(BASE/'proposal.md').read_text();assert manuscript==build.manuscript(progress['reader']['pages'])
 addition=(build.READER_BASE/'sponsor-addition.md').read_text()
 predecessor=(build.PRIOR/'proposal.md').read_text()
 expected=predecessor.replace('1,262 pages and 958 audited citation records, including 225 genuine scholarly PDFs',f"{progress['reader']['pages']:,} pages and 960 audited citation records, including 225 genuine scholarly PDFs")
 expected=expected.replace('61 open and 39 inconclusive cells','60 open and 39 inconclusive cells').replace('76 open and three inconclusive decisions','75 open and three inconclusive decisions')
 expected=expected.replace('These counts describe unresolved review obligations',r'Current counts are bound to the canonical snapshot. \citep{sp23tg_progress} These counts describe unresolved review obligations')
 marker='# Public evidence before expensive bank experiments'
 expected=expected.replace(marker,addition+'\n'+marker)
 assert manuscript==expected
 assert '61 open and 39 inconclusive cells' not in manuscript
 assert '76 open and three inconclusive decisions' not in manuscript
 text=' '.join((BASE/'reader.txt').read_text().split()).replace('- ','-').replace('−','-')
 for token in [f"{progress['reader']['pages']:,} pages",'960 audited','225 genuine scholarly PDFs','75 open','60 open','USD 20','USD 8','65 inspected','48 unread','Tigramite']:
  assert token in text,token
 state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active'] is None
 assert run.same_reader(state['reader'],report['paired_monograph']) and run.same_reader(state['reader'],progress['reader'])
 snapshot=build.engine.snapshot(state)
 for key in ['software_cells','reuse_decisions','chapter_reviews','llm_task_reviews','integration_requirements']:assert progress[key]==snapshot[key]
 assert progress['reuse_decisions']['pass']==37 and progress['reuse_decisions']['open']==75
 assert {q['id']:q['status'] for q in run.status(ROOT,state)['proposal_gaps']}==dict(Q1='open',Q2='pass',Q3='pass',Q4='pass',Q5='open')
 evidence=[ref(BASE/n,'Reviewed exact paired sponsor') for n in ['plan-review.json','source-audit.json','build-report.json','economics-results.json','proposal.md','reader.txt','progress-evidence.json']]
 evidence += [ref(build.READER_BASE/'release-source-review.json','Preserving monograph review'),ref(Path(__file__),'Exact preservation and financial-example checks')]
 write(BASE/'author-review.json',dict(status='pass',issues=[],reviewer=dict(name='Codex author/coordinator',kind='author'),scope='Tigramite reuse arguments and limitations and exact current proposal status',
  sponsor=report['reader_copy'],paired_monograph=report['paired_monograph'],evidence=evidence,findings=['All 343 previous source identities and all substantive sponsor sections are preserved except specified current count/citation replacements.',
  'All 347 citations are audited and sponsor binds the exact current reader.','Stipulated financial witnesses are reproducible and grant no native capability.'],
  limitations=['Author source/arithmetic/text review only; visual and independent acceptance remain open.','Q1/Q5, mandatory repairs and native/bank qualification remain open.'],visual_acceptance=False,final_acceptance=False))
 print(json.dumps(dict(review='pass',pages=report['pages'],records=347)))

def publish():
 report=read(BASE/'build-report.json');review=read(BASE/'author-review.json');verify_bindings(report);verify_bindings(review)
 assert review['status']=='pass' and not review['issues']
 state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active'] is None and run.same_reader(state['reader'],report['paired_monograph'])
 manifest=dict(kind='working_sponsor',pdf=report['reader_copy'],pages=report['pages'],paired_monograph=report['paired_monograph'],
  predecessor=ref(build.PRIOR/'reader/sponsor-proposal.pdf','Preserved sponsor'),predecessor_release=ref(build.PRIOR/'working-release.json','Preserved release'),predecessor_operation=state['execution_program']['results']['RELEASE.SPONSOR'],
  build=ref(BASE/'build-report.json','Exact paired build'),review=ref(BASE/'author-review.json','Author review'),evidence=[ref(BASE/n,'Reviewed sponsor') for n in ['source-audit.json','reader.txt']]+[ref(Path(__file__),'Preserving publisher')],visual_acceptance=False,final_acceptance=False)
 write(BASE/'working-release.json',manifest);digest=core.sha(ROOT/core.STATE)
 delivery={k:report['reader_copy'][k] for k in ['path','sha256']};delivery.update(pages=report['pages'],kind='working_sponsor',status='Working sponsor; visual and final acceptance remain open',paired_monograph=report['paired_monograph'],release=ref(BASE/'working-release.json','Tigramite paired sponsor'))
 assert not any(x['path']==delivery['path'] for x in state['deliveries']);state['deliveries'].append(delivery)
 run.commit(ROOT,digest,state,dict(action='publish_tigramite_sponsor',release=delivery['release'],prior_operation_preserved=True,final_acceptance=False))
 print(json.dumps(dict(published=delivery['path'],pages=delivery['pages'],final_acceptance=False)))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['review','publish']);globals()[p.parse_args().command]()

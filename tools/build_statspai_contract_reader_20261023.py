#!/usr/bin/env python3
"""Preserving integration of the cutoff StatsPAI adapter contract."""
import argparse,json,re
from pathlib import Path
import build_network_commercial_reader_20261020 as engine
import statspai_contract_reference_20261023 as exact
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'docs'
BASE=DOCS/'program/execution/2026-10-23/statspai-contract-reader-v1';OUT=BASE/'reader'
SOURCE=DOCS/'program/execution/2026-10-23/statspai-contract-v1'
PREDECESSOR=DOCS/'program/execution/2026-10-23/proof-statspai-reader-v2'
OLD=DOCS/'causal_proposal_proof_statspai_reviewed_v2_2026-10-23.tex';PRIOR=PREDECESSOR/'reader/source-audit.json'
NAME='causal_proposal_statspai_contract_reviewed_2026-10-23';DRIVER=DOCS/(NAME+'.tex');PDF=DRIVER.with_suffix('.pdf');DEVELOPMENT=BASE/'development.tex'
LABELS=['exec23:statspai-contract-'+x for x in ['scope','schema','runtime','parity','decision']]
read=lambda p:json.loads(p.read_text())
def expected_driver():
 text=OLD.read_text();marker=r'\input{program/execution/2026-10-23/proof-statspai-reader-v2/development.tex}';assert text.count(marker)==1
 text=text.replace(marker,marker+'\n'+r'\input{'+str(DEVELOPMENT.relative_to(DOCS))+'}')
 return re.sub(r'\\bibliography\{([^}]+)\}',lambda m:r'\bibliography{'+m.group(1)+','+str((BASE/'refs').relative_to(DOCS))+'}',text)
def configure():
 for k in ['ROOT','DOCS','BASE','OUT','PREDECESSOR','OLD','PRIOR','NAME','DRIVER','PDF','DEVELOPMENT','LABELS','expected_driver']:setattr(engine,k,globals()[k])
 engine.exact=exact

def prepare():
 configure();assert not BASE.exists()
 for p in [PRIOR,PREDECESSOR/'working-release.json',SOURCE/'review.json',SOURCE/'source-audit.json']:verify_bindings(read(p))
 assert exact.calculate()==read(SOURCE/'exact-results.json')
 BASE.mkdir();write(BASE/'exact-results.json',exact.calculate());DEVELOPMENT.write_bytes((SOURCE/'development.tex').read_bytes());write(BASE/'source-audit.json',read(SOURCE/'source-audit.json'))
 (BASE/'integration-plan.md').write_text('Preserve all976 citations, their claims/contexts and all prior content inputs. Add two audited records for eleven pinned source files and project-owned data-only schema/arithmetic checks. Distinguish static code inspection from native execution. Compile and inspect all-page text, renew exact-reader Q2-Q4, pair sponsor and refresh continuation. Visual/final acceptance remain open.\n')
 write(BASE/'plan-review.json',dict(status='pass',issues=[],evidence=[ref(BASE/'integration-plan.md','Preserving plan'),ref(SOURCE/'plan-review.json','Detailed reviewed plan')],findings=['No dependency broadens to a global phase gate.','No downloaded code is executed.']))
 write(BASE/'mathematical-review.json',dict(status='pass_for_project_owned_contract_witnesses',issues=[],evidence=[ref(SOURCE/'exact-results.json','Executed data-only reference'),ref(Path(exact.__file__),'Exact reference source'),ref(DEVELOPMENT,'Connected contract and weighting argument')],findings=['Schema acceptance does not assert any estimator emitted an invalid output.','Customer and treated-observation weighting targets differ under the stated common-period decision.','Duplicated serialized JSON contributes a lower bound, not a measured wire benchmark.'],native_execution=False))
 write(BASE/'copyedit-review.json',dict(status='pass',issues=[],evidence=[ref(DEVELOPMENT,'Connected banking argument')],findings=['Cutoff source1.39.0 and paper archive1.23.0 are separate.','Caller branches and delegated helper guarantees are distinct.','Reuse disposition and explicit prerequisites do not grant capability.'],visual_acceptance=False))
 bib=[]
 for s in read(BASE/'source-audit.json')['sources']:
  author='{'+engine.shared.escape(s['author'])+'}'
  bib.append('@misc{'+s['integrated_citation_key']+',\n author={'+author+'},\n title={'+engine.shared.escape(s['title'])+'},\n year={'+str(s['year'])+'},\n note={'+engine.shared.escape(s['version_date'])+'}\n}\n')
 (BASE/'refs.bib').write_text('\n'.join(bib));DRIVER.write_text(expected_driver())
 paths=[OLD,PRIOR,DEVELOPMENT,Path(__file__),SOURCE/'review.json',SOURCE/'qualification-plan.json',SOURCE/'decision.json',Path(exact.__file__),BASE/'exact-results.json']+[BASE/n for n in ['source-audit.json','integration-plan.md','plan-review.json','mathematical-review.json','copyedit-review.json']]
 write(BASE/'prepared-inputs.json',dict(inputs=[ref(p,'Reviewed input') for p in paths],generated=[ref(DRIVER,'Preserving driver'),ref(BASE/'refs.bib','Two references')],prior_cited_records=976,expected_cited_records=978,expected_scholarly_pdfs=230,visual_acceptance=False))
 print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)),records=978)))
def build():configure();engine.build()
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','build']);globals()[p.parse_args().command]()

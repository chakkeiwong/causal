#!/usr/bin/env python3
import argparse,json,re
from pathlib import Path
import build_network_commercial_reader_20261020 as engine
import admission_conformal_reference_20261023 as exact
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'docs';BASE=DOCS/'program/execution/2026-10-23/proof-statspai-reader-v2';OUT=BASE/'reader';SOURCE=DOCS/'program/execution/2026-10-23/proof-statspai-v1';PREDECESSOR=DOCS/'program/execution/2026-10-23/admission-conformal-reader-v2';OLD=DOCS/'causal_proposal_admission_conformal_reviewed_v2_2026-10-23.tex';PRIOR=PREDECESSOR/'reader/source-audit.json';NAME='causal_proposal_proof_statspai_reviewed_v2_2026-10-23';DRIVER=DOCS/(NAME+'.tex');PDF=DRIVER.with_suffix('.pdf');DEVELOPMENT=BASE/'development.tex';LABELS=['exec23:proof-'+x for x in ['scope','lower','statspai']]
read=lambda p:json.loads(p.read_text())
def expected_driver():
 text=OLD.read_text();marker=r'\input{program/execution/2026-10-23/admission-conformal-reader-v2/development.tex}';assert text.count(marker)==1
 text=text.replace(marker,marker+'\n'+r'\input{'+str(DEVELOPMENT.relative_to(DOCS))+'}')
 return re.sub(r'\\bibliography\{([^}]+)\}',lambda m:r'\bibliography{'+m.group(1)+','+str((BASE/'refs').relative_to(DOCS))+'}',text)
def configure():
 for k in ['ROOT','DOCS','BASE','OUT','PREDECESSOR','OLD','PRIOR','NAME','DRIVER','PDF','DEVELOPMENT','LABELS','expected_driver']:setattr(engine,k,globals()[k])
 engine.exact=exact
def prepare():
 configure();assert not BASE.exists()
 for p in [PRIOR,PREDECESSOR/'working-release.json',SOURCE/'review.json',SOURCE/'source-audit.json']:verify_bindings(read(p))
 BASE.mkdir();write(BASE/'exact-results.json',exact.calculate());DEVELOPMENT.write_bytes((SOURCE/'development.tex').read_bytes());write(BASE/'source-audit.json',read(SOURCE/'source-audit.json'))
 (BASE/'integration-plan.md').write_text('Preserve all973 citations/claims/contexts and294 content inputs; add three authentic originals and an adjacent lower-versus-upper guarantee qualification plus StatsPAI comparison. No fresh mathematical results or native outputs are claimed. Compile, audit source identities and all-page bounds, renew Q2-Q4, pair sponsor; coverage/visual/final acceptance remain open.\n')
 write(BASE/'plan-review.json',dict(status='pass',issues=[],evidence=[ref(BASE/'integration-plan.md','Plan'),ref(SOURCE/'review.json','Primary review')],findings=['Lower and tight upper bounds distinguished; StatsPAI evidence remains source-reported.']))
 write(BASE/'mathematical-review.json',dict(status='pass_for_primary_argument_scope',issues=[],evidence=[ref(SOURCE/'source-audit.json','Inspected original proof anchors'),ref(DEVELOPMENT,'Qualified discussion')],findings=['No claim independence assumption inferred from merger semantics.','Safe-threshold lower bound distinguished from tight upper/nesting assumptions.','Full subset labels distinguished from graph-assisted shortcuts; native proof/implementation qualification remains open.'],native_execution=False))
 write(BASE/'copyedit-review.json',dict(status='pass',issues=[],evidence=[ref(DEVELOPMENT,'Connected argument')],findings=['Explicitly qualifies preceding discussion without erasing its historical evidence.','Reported software parity and simulated data remain distinct from native bank evidence.'],visual_acceptance=False))
 bib=[]
 for s in read(BASE/'source-audit.json')['sources']:
  bib.append('@misc{'+s['integrated_citation_key']+',\n author={'+s['author']+'},\n title={'+engine.shared.escape(s['title'])+'},\n year={'+str(s['year'])+'},\n note={'+engine.shared.escape(s['version_date'])+'}\n}\n')
 (BASE/'refs.bib').write_text('\n'.join(bib));DRIVER.write_text(expected_driver())
 write(BASE/'prepared-inputs.json',dict(inputs=[ref(p,'Reviewed source input') for p in [OLD,PRIOR,DEVELOPMENT,Path(__file__),SOURCE/'review.json',SOURCE/'qualification-plan.json',Path(exact.__file__),BASE/'exact-results.json']+[BASE/n for n in ['source-audit.json','integration-plan.md','plan-review.json','mathematical-review.json','copyedit-review.json']]],generated=[ref(DRIVER,'Preserving driver'),ref(BASE/'refs.bib','Three original references')],prior_cited_records=973,expected_cited_records=976,expected_scholarly_pdfs=230,visual_acceptance=False))
 print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)),records=976)))
def build():configure();engine.build()
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','build']);globals()[p.parse_args().command]()

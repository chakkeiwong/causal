#!/usr/bin/env python3
"""Preserving integration of medflex natural-effect source contracts."""
import argparse,json,re
from pathlib import Path
import build_network_commercial_reader_20261020 as engine
import medflex_reference_20261023 as exact
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'docs'
BASE=DOCS/'program/execution/2026-10-23/medflex-reuse-reader-v1';OUT=BASE/'reader'
SOURCE=DOCS/'program/execution/2026-10-23/medflex-reuse-v1'
PREDECESSOR=DOCS/'program/execution/2026-10-23/gist-census-reader-v1'
OLD=DOCS/'causal_proposal_gist_census_reviewed_2026-10-23.tex';PRIOR=PREDECESSOR/'reader/source-audit.json'
NAME='causal_proposal_medflex_reuse_reviewed_2026-10-23';DRIVER=DOCS/(NAME+'.tex');PDF=DRIVER.with_suffix('.pdf');DEVELOPMENT=BASE/'development.tex'
LABELS=['exec23:medflex-'+x for x in ['scope','target','expansion','uncertainty','decision']]
read=lambda p:json.loads(p.read_text())
def expected_driver():
 text=OLD.read_text();marker=r'\input{program/execution/2026-10-23/gist-census-reader-v1/development.tex}';assert text.count(marker)==1
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
 (BASE/'integration-plan.md').write_text('Preserve all988 citations, claims, contexts and all prior content inputs. Add two audited records for ten immutable medflex source blobs and independent exact target/covariance examples. Review expansion, full refitting and data-call custody without native execution. Compile, check all-page text, renew exact-reader Q2-Q4, pair sponsor and refresh independent continuation. Visual/final acceptance remain open.\n')
 write(BASE/'plan-review.json',dict(status='pass',issues=[],evidence=[ref(BASE/'integration-plan.md','Preserving plan'),ref(SOURCE/'review.json','Detailed reviewed plan')],findings=['No dependency broadens to a global phase gate.','No downloaded code is executed.']))
 write(BASE/'mathematical-review.json',dict(status='pass_for_project_owned_contract_witnesses',issues=[],evidence=[ref(SOURCE/'exact-results.json','Executed data-only reference'),ref(Path(exact.__file__),'Exact reference source'),ref(DEVELOPMENT,'Connected contract and weighting argument')],findings=['Nested means give total32/5 with distinct decompositions14/5+18/5 and2+22/5.','Repeated-row score example halves variance1/2 to1/4; joint nuisance covariance factor7 versus frozen1.','Stipulated total-policy net14 versus direct-component calculation-22; not bank ROI or comparable implementable policies.'],native_execution=False))
 write(BASE/'copyedit-review.json',dict(status='pass',issues=[],evidence=[ref(DEVELOPMENT,'Connected banking argument')],findings=['Natural-effect targets, imputed/weighted expansion and subject-level sampling remain distinct.','Static class-documentation discrepancy, global-environment data calls and warning suppression remain qualification inputs.','Reference-only disposition grants no native adapter or general mediation-identification capability.'],visual_acceptance=False))
 bib=[]
 for s in read(BASE/'source-audit.json')['sources']:
  author='{'+engine.shared.escape(s['author'])+'}'
  bib.append('@misc{'+s['integrated_citation_key']+',\n author={'+author+'},\n title={'+engine.shared.escape(s['title'])+'},\n year={'+str(s['year'])+'},\n note={'+engine.shared.escape(s['version_date'])+'}\n}\n')
 (BASE/'refs.bib').write_text('\n'.join(bib));DRIVER.write_text(expected_driver())
 paths=[OLD,PRIOR,DEVELOPMENT,Path(__file__),SOURCE/'review.json',SOURCE/'preparation-corrections.md',Path(exact.__file__),BASE/'exact-results.json']+[BASE/n for n in ['source-audit.json','integration-plan.md','plan-review.json','mathematical-review.json','copyedit-review.json']]
 write(BASE/'prepared-inputs.json',dict(inputs=[ref(p,'Reviewed input') for p in paths],generated=[ref(DRIVER,'Preserving driver'),ref(BASE/'refs.bib','Two references')],prior_cited_records=988,expected_cited_records=990,expected_scholarly_pdfs=231,visual_acceptance=False))
 print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)),records=990)))
def build():configure();engine.build()
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','build']);globals()[p.parse_args().command]()

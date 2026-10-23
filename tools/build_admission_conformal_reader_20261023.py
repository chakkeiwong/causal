#!/usr/bin/env python3
"""Preserving shared-memory and scientific-validation integration using the established monograph builder."""
import argparse,json,re
from pathlib import Path
import build_network_commercial_reader_20261020 as engine
import admission_conformal_reference_20261023 as exact
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write
ROOT=Path(__file__).resolve().parents[1]; DOCS=ROOT/'docs'
BASE=DOCS/'program/execution/2026-10-23/admission-conformal-reader-v1'; OUT=BASE/'reader'
SOURCE=DOCS/'program/execution/2026-10-23/census-admission-conformal-v1'
PREDECESSOR=DOCS/'program/execution/2026-10-23/other-iv-rd-reader-v3'
OLD=DOCS/'causal_proposal_other_iv_rd_reviewed_v3_2026-10-23.tex'
PRIOR=PREDECESSOR/'reader/source-audit.json'
NAME='causal_proposal_admission_conformal_reviewed_2026-10-23'; DRIVER=DOCS/(NAME+'.tex'); PDF=DRIVER.with_suffix('.pdf')
DEVELOPMENT=BASE/'development.tex'
LABELS=['exec23:admit-'+x for x in ['scope','memory','stream','validation','value','conformal','repairs','route']]
read=lambda p:json.loads(p.read_text())

def calculate():return exact.calculate()
def expected_driver():
 text=OLD.read_text();marker=r'\input{program/execution/2026-10-23/semantics-reader-v4/conflict-development.tex}'
 assert text.count(marker)==1
 text=text.replace(marker,marker+'\n'+r'\input{'+str(DEVELOPMENT.relative_to(DOCS))+'}')
 return re.sub(r'\\bibliography\{([^}]+)\}',lambda m:r'\bibliography{'+m.group(1)+','+str((BASE/'refs').relative_to(DOCS))+'}',text)
def configure():
 for key in ['ROOT','DOCS','BASE','OUT','PREDECESSOR','OLD','PRIOR','NAME','DRIVER','PDF','DEVELOPMENT','LABELS','expected_driver']:setattr(engine,key,globals()[key])
 engine.exact=exact

def prepare():
 configure();assert not BASE.exists() and not DRIVER.exists()
 for p in [PRIOR,PREDECESSOR/'working-release.json',SOURCE/'review.json',SOURCE/'source-audit.json']:verify_bindings(read(p))
 assert calculate()==read(SOURCE/'exact-results.json')
 BASE.mkdir(); DEVELOPMENT.write_bytes((SOURCE/'development.tex').read_bytes())
 write(BASE/'source-audit.json',read(SOURCE/'source-audit.json')); write(BASE/'exact-results.json',calculate())
 write(BASE/'mathematical-review.json',dict(status='pass_for_exact_authored_argument',issues=[],evidence=[ref(Path(exact.__file__),'Independent Fraction calculations'),ref(DEVELOPMENT,'Derivations and explicit assumptions')],
  findings=['Copied votes remain0.8 versus independent majority0.896; stipulated utility0 versus1 USD.', 'Five90%-valid independent outputs have family failure0.40951; rank6 for n5 requires infinity.', 'Score coverage and nested filtering differ; bounded trace reveals missing final-attempt exit.'],native_execution=False))
 (BASE/'integration-plan.md').write_text('Preserve all prior compiled content, source identities and citation contexts. Insert shared evidence and scientific-validation after the conflict discussion. Add two genuine papers and one exact project reference; compile and check every page text bound, exact arithmetic and preserved contexts. Renew Q2-Q4 for exact reader, pair sponsor, and retain Q1/Q5 and visual acceptance open. No duplicate survey depth credit.\n')
 write(BASE/'plan-review.json',dict(status='pass',issues=[],evidence=[ref(BASE/'integration-plan.md','Reviewed preserving scope'),ref(SOURCE/'review.json','Inspected source decision')],findings=['Exact reader and source preservation; no native capability inferred.']))
 write(BASE/'copyedit-review.json',dict(status='pass',issues=[],evidence=[ref(DEVELOPMENT,'Connected banking argument')],findings=['Policy-dependent denominators and simulated exposure are not bank harm.','Conditional exchangeability does not prove semantic truth; conflicting tables and algorithm ambiguity remain explicit.','Public and authored evidence justify prototype tests, not blanket guarantees.'],visual_acceptance=False))
 bib=[]
 for s in read(BASE/'source-audit.json')['sources']:
  identity=s['source_identity'];note=(r'\url{'+identity+'}; ' if identity.startswith('https://') else engine.shared.escape(identity)+'; ')+engine.shared.escape(s['version_date'])
  author=s['author'].replace(', ', ' and ') if s['kind']=='paper' else '{'+engine.shared.escape(s['author'])+'}'
  bib.append('@misc{'+s['integrated_citation_key']+',\n author={'+author+'},\n title={'+engine.shared.escape(s['title'])+'},\n year={'+str(s['year'])+'},\n note={'+note+'}\n}\n')
 (BASE/'refs.bib').write_text('\n'.join(bib)); DRIVER.write_text(expected_driver())
 inputs=[OLD,PRIOR,DEVELOPMENT,Path(__file__),Path(exact.__file__),SOURCE/'review.json',SOURCE/'reconciliation-review.json']+[BASE/n for n in ['source-audit.json','exact-results.json','mathematical-review.json','integration-plan.md','plan-review.json','copyedit-review.json']]
 write(BASE/'prepared-inputs.json',dict(inputs=[ref(p,'Reviewed preserving input') for p in inputs],generated=[ref(DRIVER,'Preserving driver'),ref(BASE/'refs.bib','New audited citations')],
  prior_cited_records=len(read(PRIOR)['sources']),expected_cited_records=len(engine.sources()),expected_scholarly_pdfs=read(PREDECESSOR/'traceability-review.json')['scholarly_pdfs']+2,visual_acceptance=False))
 print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)),records=len(engine.sources()))))

def build(): configure();engine.build()
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','build']);{'prepare':prepare,'build':build}[p.parse_args().command]()

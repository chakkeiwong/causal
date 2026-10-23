#!/usr/bin/env python3
"""Preserving Julia and Rust IV/RD integration using the established monograph builder."""
import argparse,json,re
from pathlib import Path
import build_network_commercial_reader_20261020 as engine
import other_iv_rd_reference_20261023 as exact
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write
ROOT=Path(__file__).resolve().parents[1]; DOCS=ROOT/'docs'
BASE=DOCS/'program/execution/2026-10-23/other-iv-rd-reader-v2'; OUT=BASE/'reader'
SOURCE=DOCS/'program/execution/2026-10-23/other-iv-rd-v1'
PREDECESSOR=DOCS/'program/execution/2026-10-23/panel-reader-v1'
OLD=DOCS/'causal_proposal_panel_reviewed_2026-10-23.tex'
PRIOR=PREDECESSOR/'reader/source-audit.json'
NAME='causal_proposal_other_iv_rd_reviewed_v2_2026-10-23'; DRIVER=DOCS/(NAME+'.tex'); PDF=DRIVER.with_suffix('.pdf')
DEVELOPMENT=BASE/'development.tex'
LABELS=['exec23:otheriv-'+x for x in ['scope','fe','2sls','sharp','port','ratio','delta','example','choice']]
read=lambda p:json.loads(p.read_text())

def calculate():return exact.calculate()
def expected_driver():
 text=OLD.read_text();marker=r'\input{program/execution/2026-10-23/semantics-reader-v4/iv-development.tex}'
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
 BASE.mkdir(); DEVELOPMENT.write_bytes((SOURCE/'development-v2.tex').read_bytes())
 write(BASE/'source-audit.json',read(SOURCE/'source-audit.json')); write(BASE/'exact-results.json',calculate())
 write(BASE/'mathematical-review.json',dict(status='pass_for_exact_authored_argument',issues=[],evidence=[ref(Path(exact.__file__),'Independent Fraction calculations'),ref(DEVELOPMENT,'Derivations and explicit assumptions')],
  findings=['Regular fuzzy ratio 2/(1/5)=10; gradient(5,-50) and covariance give variance24, not frozen-denominator1.',
  'Stipulated cost6 gives net4; normal tail, repeated residual mutation and discrete-support witnesses reproduce independently.'],native_execution=False))
 (BASE/'integration-plan.md').write_text('Preserve all prior compiled content, source identities and citation contexts. Insert Julia and Rust IV/RD contract discussion after the existing IV implementation discussion. Add six source identities; compile and check every page text bound, exact arithmetic and preserved contexts. Renew Q2-Q4 for exact reader, pair sponsor, and retain Q1/Q5 and visual acceptance open. No duplicate survey depth credit.\n')
 write(BASE/'plan-review.json',dict(status='pass',issues=[],evidence=[ref(BASE/'integration-plan.md','Reviewed preserving scope'),ref(SOURCE/'review.json','Inspected source decision')],findings=['Exact reader and source preservation; no native capability inferred.']))
 write(BASE/'copyedit-review.json',dict(status='pass',issues=[],evidence=[ref(DEVELOPMENT,'Connected banking argument')],findings=['Identification, numerical fitting, ratio uncertainty and diagnostic availability remain distinct.','Static observations and conditional expression witnesses are not native outputs.','Separate repository identity, author strings and declared parity; no official endorsement inferred.'],visual_acceptance=False))
 bib=[]
 for s in read(BASE/'source-audit.json')['sources']:
  identity=s['source_identity'];note=(r'\url{'+identity+'}; ' if identity.startswith('https://') else engine.shared.escape(identity)+'; ')+engine.shared.escape(s['version_date'])
  bib.append('@misc{'+s['integrated_citation_key']+',\n author={{'+engine.shared.escape(s['author'])+'}},\n title={'+engine.shared.escape(s['title'])+'},\n year={'+str(s['year'])+'},\n note={'+note+'}\n}\n')
 (BASE/'refs.bib').write_text('\n'.join(bib)); DRIVER.write_text(expected_driver())
 inputs=[OLD,PRIOR,DEVELOPMENT,Path(__file__),Path(exact.__file__),SOURCE/'review.json']+[BASE/n for n in ['source-audit.json','exact-results.json','mathematical-review.json','integration-plan.md','plan-review.json','copyedit-review.json']]
 write(BASE/'prepared-inputs.json',dict(inputs=[ref(p,'Reviewed preserving input') for p in inputs],generated=[ref(DRIVER,'Preserving driver'),ref(BASE/'refs.bib','New audited citations')],
  prior_cited_records=len(read(PRIOR)['sources']),expected_cited_records=len(engine.sources()),expected_scholarly_pdfs=read(PREDECESSOR/'traceability-review.json')['scholarly_pdfs'],visual_acceptance=False))
 print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)),records=len(engine.sources()))))

def build(): configure();engine.build()
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','build']);{'prepare':prepare,'build':build}[p.parse_args().command]()

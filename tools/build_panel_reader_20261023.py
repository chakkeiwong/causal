#!/usr/bin/env python3
"""Preserving Panel integration using the established monograph builder."""
import argparse,json,re
from pathlib import Path
import build_network_commercial_reader_20261020 as engine
import panel_contract_reference_20261023 as exact
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write
ROOT=Path(__file__).resolve().parents[1]; DOCS=ROOT/'docs'
BASE=DOCS/'program/execution/2026-10-23/panel-reader-v1'; OUT=BASE/'reader'
SOURCE=DOCS/'program/execution/2026-10-23/synthdid-reuse-v1'
PYSOURCE=DOCS/'program/execution/2026-10-23/pyfixest-reuse-v1'
PREDECESSOR=DOCS/'program/execution/2026-10-23/tigramite-reader-v1'
OLD=DOCS/'causal_proposal_tigramite_reviewed_2026-10-23.tex'
PRIOR=PREDECESSOR/'reader/source-audit.json'
NAME='causal_proposal_panel_reviewed_2026-10-23'; DRIVER=DOCS/(NAME+'.tex'); PDF=DRIVER.with_suffix('.pdf')
DEVELOPMENT=BASE/'development.tex'
LABELS=['exec23:panel-'+x for x in ['scope','projection','twfe','witness','clock','aggregation','sdid','contrast','block-example','inference','reuse']]
read=lambda p:json.loads(p.read_text())

def calculate():return exact.calculate()
def expected_driver():
 text=OLD.read_text();marker=r'\input{program/execution/2026-10-20/fixest-reuse-v1/development.tex}'
 assert text.count(marker)==1
 text=text.replace(marker,marker+'\n'+r'\input{'+str(DEVELOPMENT.relative_to(DOCS))+'}')
 return re.sub(r'\\bibliography\{([^}]+)\}',lambda m:r'\bibliography{'+m.group(1)+','+str((BASE/'refs').relative_to(DOCS))+'}',text)
def configure():
 for key in ['ROOT','DOCS','BASE','OUT','PREDECESSOR','OLD','PRIOR','NAME','DRIVER','PDF','DEVELOPMENT','LABELS','expected_driver']:setattr(engine,key,globals()[key])
 engine.exact=exact

def prepare():
 configure();assert not BASE.exists() and not DRIVER.exists()
 for p in [PRIOR,PREDECESSOR/'working-release.json',SOURCE/'review.json',SOURCE/'source-audit.json',PYSOURCE/'review.json',PYSOURCE/'source-audit.json']:verify_bindings(read(p))
 assert exact.sdid.calculate()==read(SOURCE/'exact-results.json')
 assert exact.pyfixest.calculate()==read(PYSOURCE/'exact-results.json')
 BASE.mkdir(); DEVELOPMENT.write_bytes((SOURCE/'panel-development.tex').read_bytes())
 write(BASE/'source-audit.json',dict(sources=read(PYSOURCE/'source-audit.json')['sources']+read(SOURCE/'source-audit.json')['sources'],cutoff='2026-10-07',native_execution=False)); write(BASE/'exact-results.json',calculate())
 write(BASE/'mathematical-review.json',dict(status='pass_for_exact_authored_argument',issues=[],evidence=[ref(Path(exact.__file__),'Independent Fraction calculations'),ref(DEVELOPMENT,'Derivations and explicit assumptions')],
  findings=['Positive treated-cell effects average 4 while TWFE projection is -7/2 under the stipulated two-unit panel.',
  'Fixed cohort weights give effect 1 and full variance 91/16, distinct from equal-cohort effect 4.',
  'Supplied SDID weights give effect 11/2 and net 3/2; normalization oracle shifts invalid-weight result by 25.',
  'Bootstrap composition rejection is 1/8; expected attempts per mixed draw 8/7, without native execution.'],native_execution=False))
 (BASE/'integration-plan.md').write_text('Preserve all prior compiled content, source identities and citation contexts. Insert Panel contract discussion after the R fixest comparison. Add four source identities; compile and check every page text bound, exact arithmetic and preserved contexts. Renew Q2-Q4 for exact reader, pair sponsor, and retain Q1/Q5 and visual acceptance open. No duplicate survey depth credit.\n')
 write(BASE/'plan-review.json',dict(status='pass',issues=[],evidence=[ref(BASE/'integration-plan.md','Reviewed preserving scope'),ref(SOURCE/'review.json','Inspected source decision')],findings=['Exact reader and source preservation; no native capability inferred.']))
 write(BASE/'copyedit-review.json',dict(status='pass',issues=[],evidence=[ref(DEVELOPMENT,'Connected banking argument')],findings=['Panel timing, causal targets, cohort weighting and covariance remain distinct.','Static guards and missing fit options require native replay.','Exact supplied-weight examples do not imply fitted outputs or capability.'],visual_acceptance=False))
 bib=[]
 for s in read(BASE/'source-audit.json')['sources']:
  identity=s['source_identity'];note=(r'\url{'+identity+'}; ' if identity.startswith('https://') else engine.shared.escape(identity)+'; ')+engine.shared.escape(s['version_date'])
  bib.append('@misc{'+s['integrated_citation_key']+',\n author={{'+engine.shared.escape(s['author'])+'}},\n title={'+engine.shared.escape(s['title'])+'},\n year={'+str(s['year'])+'},\n note={'+note+'}\n}\n')
 (BASE/'refs.bib').write_text('\n'.join(bib)); DRIVER.write_text(expected_driver())
 inputs=[OLD,PRIOR,DEVELOPMENT,Path(__file__),Path(exact.__file__),SOURCE/'review.json',PYSOURCE/'review.json']+[BASE/n for n in ['source-audit.json','exact-results.json','mathematical-review.json','integration-plan.md','plan-review.json','copyedit-review.json']]
 write(BASE/'prepared-inputs.json',dict(inputs=[ref(p,'Reviewed preserving input') for p in inputs],generated=[ref(DRIVER,'Preserving driver'),ref(BASE/'refs.bib','New audited citations')],
  prior_cited_records=len(read(PRIOR)['sources']),expected_cited_records=len(engine.sources()),expected_scholarly_pdfs=read(PREDECESSOR/'traceability-review.json')['scholarly_pdfs'],visual_acceptance=False))
 print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)),records=len(engine.sources()))))

def build(): configure();engine.build()
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','build']);{'prepare':prepare,'build':build}[p.parse_args().command]()

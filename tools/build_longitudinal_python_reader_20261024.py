#!/usr/bin/env python3
"""Preserve the full reader and integrate a pinned Python longitudinal comparison."""
import argparse,json,re
from pathlib import Path
import build_network_commercial_reader_20261020 as engine
import longitudinal_python_reference_20261024 as exact
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'docs';BS=chr(92);NL=chr(10)
BASE=DOCS/'program/execution/2026-10-24/longitudinal-python-reader-v1';OUT=BASE/'reader'
SOURCE=DOCS/'program/execution/2026-10-24/longitudinal-python-v1'
PREDECESSOR=DOCS/'program/execution/2026-10-24/panel-reuse-reader-v2'
OLD=DOCS/'causal_proposal_panel_reuse_v2_reviewed_2026-10-24.tex';PRIOR=PREDECESSOR/'reader/source-audit.json'
NAME='causal_proposal_longitudinal_python_reviewed_2026-10-24';DRIVER=DOCS/(NAME+'.tex');PDF=DRIVER.with_suffix('.pdf');DEVELOPMENT=BASE/'development.tex'
LABELS=['sec:exec24-longitudinal-python']
read=lambda p:json.loads(p.read_text())
def expected_driver():
 text=OLD.read_text();marker=BS+'input{program/execution/2026-10-24/panel-reuse-reader-v2/development.tex}';assert text.count(marker)==1
 text=text.replace(marker,marker+NL+BS+'input{'+str(DEVELOPMENT.relative_to(DOCS))+'}')
 key=BS+'bibliography{';start=text.index(key)+len(key);end=text.index('}',start)
 return text[:end]+','+str((BASE/'refs').relative_to(DOCS))+text[end:]
def configure():
 for k in ['ROOT','DOCS','BASE','OUT','PREDECESSOR','OLD','PRIOR','NAME','DRIVER','PDF','DEVELOPMENT','LABELS','expected_driver']:setattr(engine,k,globals()[k])
 engine.exact=exact
def prepare():
 configure();assert not BASE.exists()
 for p in [PRIOR,PREDECESSOR/'working-release.json',SOURCE/'review.json',SOURCE/'source-audit.json']:verify_bindings(read(p))
 assert len(read(PRIOR)['sources'])==1023
 assert exact.calculate()==read(SOURCE/'exact-results.json');BASE.mkdir()
 for n in ['development.tex','sponsor-addition.md','source-audit.json','exact-results.json','mathematical-review.json','copyedit-review.json','plan-review.json']:(BASE/n).write_bytes((SOURCE/n).read_bytes())
 (BASE/'integration-plan.md').write_text('Preserve1023 prior citations and content inputs. Add two pinned Python longitudinal source reviews and one exact authored reference; coverage remains inconclusive. No new paper or native capability. Compile and text-check; renew Q2-Q4 and pair sponsor. No native/visual/final acceptance.'+NL)
 bib=[]
 for s in read(BASE/'source-audit.json')['sources']:
  bib.append(NL.join(['@misc{'+s['integrated_citation_key']+',',' author={'+(engine.shared.escape(s['author']) if s['kind']=='paper' else '{'+engine.shared.escape(s['author'])+'}')+'},',' title={'+engine.shared.escape(s['title'])+'},',' year={'+str(s['year'])+'},',' note={'+engine.shared.escape(s['version_date'])+'}','}']))
 (BASE/'refs.bib').write_text(NL.join(bib));DRIVER.write_text(expected_driver())
 paths=[OLD,PRIOR,Path(__file__),Path(exact.__file__),SOURCE/'review.json',SOURCE/'review.json']+[BASE/n for n in ['development.tex','source-audit.json','exact-results.json','mathematical-review.json','copyedit-review.json','plan-review.json','integration-plan.md']]
 write(BASE/'prepared-inputs.json',dict(inputs=[ref(p,'Reviewed input') for p in paths],generated=[ref(DRIVER,'Preserving driver'),ref(BASE/'refs.bib','Three audited records')],prior_cited_records=1023,expected_cited_records=1026,expected_scholarly_pdfs=235,visual_acceptance=False))
 print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)),records=1026)))
def build():configure();engine.build()
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','build']);globals()[p.parse_args().command]()

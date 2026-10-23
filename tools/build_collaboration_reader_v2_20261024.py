#!/usr/bin/env python3
"""Preserve the full reader and integrate the specialist-interface review."""
import argparse,json,re
from pathlib import Path
import build_network_commercial_reader_20261020 as engine
import collaboration_reference_20261024 as exact
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'docs';BS=chr(92);NL=chr(10)
BASE=DOCS/'program/execution/2026-10-24/collaboration-reader-v2';OUT=BASE/'reader'
SOURCE=DOCS/'program/execution/2026-10-24/census-language-collaboration-v1'
PREDECESSOR=DOCS/'program/execution/2026-10-23/recon-memory-reader-v2'
OLD=DOCS/'causal_proposal_recon_memory_v2_reviewed_2026-10-23.tex';PRIOR=PREDECESSOR/'reader/source-audit.json'
NAME='causal_proposal_collaboration_v2_reviewed_2026-10-24';DRIVER=DOCS/(NAME+'.tex');PDF=DRIVER.with_suffix('.pdf');DEVELOPMENT=BASE/'development.tex'
LABELS=['sec:exec24-collaboration','eq:exec24-collaboration-sufficiency','eq:exec24-collaboration-crossed']
read=lambda p:json.loads(p.read_text())
def expected_driver():
 text=OLD.read_text();marker=BS+'input{program/execution/2026-10-23/recon-memory-reader-v2/development.tex}';assert text.count(marker)==1
 text=text.replace(marker,marker+NL+BS+'input{'+str(DEVELOPMENT.relative_to(DOCS))+'}')
 key=BS+'bibliography{';start=text.index(key)+len(key);end=text.index('}',start)
 return text[:end]+','+str((BASE/'refs').relative_to(DOCS))+text[end:]
def configure():
 for k in ['ROOT','DOCS','BASE','OUT','PREDECESSOR','OLD','PRIOR','NAME','DRIVER','PDF','DEVELOPMENT','LABELS','expected_driver']:setattr(engine,k,globals()[k])
 engine.exact=exact
def prepare():
 configure();assert not BASE.exists()
 for p in [PRIOR,PREDECESSOR/'working-release.json',SOURCE/'review.json',SOURCE/'source-audit.json']:verify_bindings(read(p))
 assert exact.calculate()==read(SOURCE/'exact-results.json');BASE.mkdir()
 for n in ['development.tex','sponsor-addition.md','source-audit.json','exact-results.json','mathematical-review.json','copyedit-review.json','plan-review.json']:(BASE/n).write_bytes((SOURCE/n).read_bytes())
 (BASE/'integration-plan.md').write_text('Preserve1017 prior citations and content inputs. Add one genuine paper and authored counterexamples. Retain the latent-interface hypothesis with typed alternatives, table and refresh contradictions, crossed uncertainty and full-cost limits. Compile and text-check; renew Q2-Q4 and pair sponsor. No native/visual/final acceptance.'+NL)
 bib=[]
 for s in read(BASE/'source-audit.json')['sources']:
  bib.append(NL.join(['@misc{'+s['integrated_citation_key']+',',' author={'+(engine.shared.escape(s['author']) if s['kind']=='paper' else '{'+engine.shared.escape(s['author'])+'}')+'},',' title={'+engine.shared.escape(s['title'])+'},',' year={'+str(s['year'])+'},',' note={'+engine.shared.escape(s['version_date'])+'}','}']))
 (BASE/'refs.bib').write_text(NL.join(bib));DRIVER.write_text(expected_driver())
 paths=[OLD,PRIOR,Path(__file__),Path(exact.__file__),SOURCE/'review.json',SOURCE/'review.json']+[BASE/n for n in ['development.tex','source-audit.json','exact-results.json','mathematical-review.json','copyedit-review.json','plan-review.json','integration-plan.md']]
 write(BASE/'prepared-inputs.json',dict(inputs=[ref(p,'Reviewed input') for p in paths],generated=[ref(DRIVER,'Preserving driver'),ref(BASE/'refs.bib','Two audited records')],prior_cited_records=1017,expected_cited_records=1019,expected_scholarly_pdfs=235,visual_acceptance=False))
 print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)),records=1019)))
def build():configure();engine.build()
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','build']);globals()[p.parse_args().command]()

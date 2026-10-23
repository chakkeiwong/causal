#!/usr/bin/env python3
"""Preserve the full longitudinal reader and add reviewed workflow contracts."""
import argparse,json
from pathlib import Path
import build_network_commercial_reader_20261020 as engine
import workflow_contract_reference_20261024 as exact
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'docs';BS=chr(92);NL=chr(10)
BASE=DOCS/'program/execution/2026-10-24/workflow-contracts-reader-v3';OUT=BASE/'reader'
SOURCE=DOCS/'program/execution/2026-10-24/workflow-contracts-v5'
PREDECESSOR=DOCS/'program/execution/2026-10-24/longitudinal-python-reader-v1'
OLD=DOCS/'causal_proposal_longitudinal_python_reviewed_2026-10-24.tex';PRIOR=PREDECESSOR/'reader/source-audit.json'
NAME='causal_proposal_workflow_contracts_v3_reviewed_2026-10-24';DRIVER=DOCS/(NAME+'.tex');PDF=DRIVER.with_suffix('.pdf');DEVELOPMENT=BASE/'development.tex'
LABELS=['sec:exec24-workflow-contracts'];read=lambda p:json.loads(p.read_text())

def expected_driver():
    text=OLD.read_text();marker=BS+'input{program/execution/2026-10-23/workflow-delegates-reader-v1/development.tex}';assert text.count(marker)==1
    text=text.replace(marker,marker+NL+BS+'input{'+str(DEVELOPMENT.relative_to(DOCS))+'}')
    start=text.index(BS+'bibliography{')+len(BS+'bibliography{');end=text.index('}',start)
    return text[:end]+','+str((BASE/'refs').relative_to(DOCS))+text[end:]

def configure():
    for k in ['ROOT','DOCS','BASE','OUT','PREDECESSOR','OLD','PRIOR','NAME','DRIVER','PDF','DEVELOPMENT','LABELS','expected_driver']:setattr(engine,k,globals()[k])
    engine.exact=exact

def prepare():
    configure();assert not BASE.exists() and not DRIVER.exists()
    for p in [PRIOR,PREDECESSOR/'working-release.json',SOURCE/'review-v2.json',SOURCE/'source-audit-qualified.json']:verify_bindings(read(p))
    assert len(read(PRIOR)['sources'])==1026 and len(read(SOURCE/'source-audit-qualified.json')['sources'])==5
    assert exact.calculate()==read(SOURCE/'exact-results.json');BASE.mkdir()
    for name in ['development.tex','sponsor-addition.md','exact-results.json','mathematical-review.json','copyedit-review.json','plan-review.json']:(BASE/name).write_bytes((SOURCE/name).read_bytes())
    (BASE/'source-audit.json').write_bytes((SOURCE/'source-audit-qualified.json').read_bytes())
    (BASE/'integration-plan.md').write_text('Preserve all 1026 predecessor source records, contexts and content inputs; add five reviewed workflow records. Keep server schemas, full coverage, native/visual/final acceptance open. Build, review exact bytes, renew Q2-Q4, pair sponsor and reconcile the whole program.'+NL)
    bib=[]
    for s in read(BASE/'source-audit.json')['sources']:
        bib.append(NL.join(['@misc{'+s['integrated_citation_key']+',',' author={{'+engine.shared.escape(s['author'])+'}},',' title={'+engine.shared.escape(s['title'])+'},',' year={'+str(s['year'])+'},',' note={'+engine.shared.escape(s['version_date'])+'}','}']))
    (BASE/'refs.bib').write_text(NL.join(bib));DRIVER.write_text(expected_driver())
    paths=[OLD,PRIOR,Path(__file__),Path(exact.__file__),SOURCE/'review-v2.json']+[BASE/n for n in ['development.tex','source-audit.json','exact-results.json','mathematical-review.json','copyedit-review.json','plan-review.json','integration-plan.md']]
    write(BASE/'prepared-inputs.json',dict(inputs=[ref(p,'Reviewed input') for p in paths],generated=[ref(DRIVER,'Preserving driver'),ref(BASE/'refs.bib','Five audited records')],prior_cited_records=1026,expected_cited_records=1031,expected_scholarly_pdfs=235,visual_acceptance=False))
    print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)),records=1031)))

def build():configure();engine.build()
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','build']);globals()[p.parse_args().command]()

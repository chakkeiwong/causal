#!/usr/bin/env python3
"""Integrate the reviewed agent architecture without changing frozen readers."""
import argparse
import contextlib
import json
from pathlib import Path
import re

import build_integrated_monograph_v12 as shared
import build_java_reader_20261013 as inherited
import master_control as core

ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-13/agent-architecture'
OUT=BASE/'reader'
NAME='causal_proposal_agent_architecture_2026-10-13'
OLD=ROOT/'docs/causal_proposal_pgmpy_2026-10-13.tex'
DRIVER=ROOT/'docs'/(NAME+'.tex')
PDF=DRIVER.with_suffix('.pdf')
PRIOR_AUDIT=ROOT/'docs/program/execution/2026-10-13/pgmpy-reuse/reader/source-audit.json'
ref=shared.ref

def expected_driver():
    text=OLD.read_text()
    marker=r'\input{program/execution/2026-10-13/llm-census/agents.tex}'
    assert text.count(marker)==1
    text=text.replace(marker,marker+'\n'+r'\input{program/execution/2026-10-13/agent-architecture/architecture.tex}',1)
    marker='program/execution/2026-10-13/pgmpy-reuse/refs}'
    assert text.count(marker)==1
    return text.replace(marker,'program/execution/2026-10-13/pgmpy-reuse/refs,program/execution/2026-10-13/agent-architecture/refs}',1)

def configure():
    for key in ['BASE','OUT','NAME','OLD','DRIVER','PDF','PRIOR_AUDIT']:
        setattr(inherited,key,globals()[key])

def prepare():
    configure();inherited.guard()
    prior=json.loads(PRIOR_AUDIT.read_text());shared.verify_refs(prior)
    text=(BASE/'architecture.tex').read_text()
    cites={k.strip() for g in re.findall(shared.CITE,text) for k in g.split(',')}
    sources={s['integrated_citation_key']:s for s in prior['sources']}
    selected=sorted(cites & sources.keys())
    rows=[]
    for key in selected:
        s=sources[key]
        row={'citation':key,'source_record':s,'inspection':'Reinspected selected primary passages and code; no upstream runtime execution.'}
        if s.get('extracted_text'):
            extracted=s['extracted_text']
            row['text_copy']=(extracted if isinstance(extracted,dict) else
                ref(ROOT/extracted,'Primary PDF text at inherited physical-page anchors'))
        rows.append(row)
    review={
        'status':'pass','scope':'Bounded reinspection supporting one architecture synthesis; no census closure',
        'cutoff':'2026-10-07','inspection_date':'2026-10-13','sources':rows,
        'code_paths':[
            ref(ROOT/'docs/literature/raw/v12_la_causalagent_source_1.txt','Imports and causal_olc exception path'),
            ref(ROOT/'docs/literature/raw/v12_la_causalagent_source_2.txt','excute_output decoding failure returns {}'),
            ref(ROOT/'docs/literature/raw/v12_la_oci_agent_source_3.txt','run: supplied notebook, injected specification and NotebookClient timeout=-1'),
            ref(ROOT/'docs/literature/raw/v12_la_oci_notebook.json','Zero-based cells42/43: trim, uniform AIPW summary and retained indices'),
            ref(ROOT/'docs/literature/raw/v12_la04_langgraph_source_2.txt','Lines893-915: interrupt re-executes node'),
            ref(ROOT/'docs/literature/raw/v12_la04_pydantic_ai_source_1.txt','Lines545-590: before-request and missing-cost checks'),
            ref(ROOT/'docs/literature/raw/v12_la04_autogen_source_1.txt','Lines1630-1639: save/load model context')],
        'conflicts_retained':['ORCA abstract completion gain differs from Table1; completion is not accuracy.','oci-agent ATO label does not match overlap weighting in the inspected notebook.','Formal compilation does not validate a statement-match agent.'],
        'search_coverage':ref(ROOT/'docs/program/execution/2026-10-13/llm-census/search-ledger.json','Preserved failed requests, bounded ranked searches and unsaturated routes'),
        'candidate_dispositions':ref(ROOT/'docs/program/execution/2026-10-13/llm-census/census-register.json','ORCA, CausalSmith and Han Causal Agent original PDFs already inspected; runtime/code adoption remains open'),
        'remaining':['101 inherited candidates lack original inspection in the preserved census. This operation does not close them.','New architectures require pinned code, terms and relevant runtime path review before executable adoption.','General critic accuracy, live semantic performance and target-bank truth remain unmeasured.'],
        'evidence_type':'primary text and selected static code reinspection; project derivations and inherited local conformance are separate'}
    core.write(BASE/'primary-review.json',review)
    results=json.loads((BASE/'exact-results.json').read_text())
    assert results['target_measures']['overlap_ATO_USD']=='48200/283'
    core.write(BASE/'mathematical-review.json',{
        'status':'pass','scope':'Author review of exact finite examples and equal-law induction',
        'findings':['AIPW conditional expectation yields conditional effect at true nuisances; changing integration measure changes the estimand.','Three-stratum sums agree with independently represented400-unit potential-outcome enumeration.','Majority error enumeration preserves marginal error under common shocks; independent screening assumption is explicit.','Gaussian covariance equality plus transcript-kernel induction establishes only the stated information limit.','Economics keeps failed-request costs and distinguishes usable fraction from completed estimates.'],
        'evidence':[ref(BASE/'exact-results.json','Exact rational results'),ref(ROOT/'tools/agent_architecture_examples_20261013.py','Stipulated experiments and independent finite calculations'),ref(BASE/'architecture.tex','Developed argument')],
        'limits':'No live experiment, finite statistical calibration, bank truth or independent review.'})
    new=[{
        'integrated_citation_key':'exec13_architecture_exact','kind':'project_derivation',
        'title':'Exact target measures, correlated critics, equal-law worlds and workflow cost examples',
        'author':'Causal banking proposal project','year':2026,'version_date':'2026-10-13',
        'source_identity':'Authored rational examples and Gaussian observational-equivalence construction',
        'local_copy':ref(BASE/'exact-results.json','Target measures, critic errors, screening and economics'),
        'code':ref(ROOT/'tools/agent_architecture_examples_20261013.py','Exact enumeration and finite-population reference'),
        'review':ref(BASE/'mathematical-review.json','Author mathematical review'),
        'inspected_anchors':['target_measures','critics','screening','equal_law','economics','assisted_review_break_even_minutes'],
        'supported_claims':['Full-population, trimmed and overlap effects are125,700/3 and48200/283 USD.','Independent majority error is.028; stipulated common-shock error is approximately.05762.','Twenty independent false screens yield1-.95**20.','Scenario review break-even is71/6 minutes.'],
        'limits':'Stipulated examples; no empirical model errors, live calls, bank observations or measured ROI.'
    },{
        'integrated_citation_key':'exec13_architecture_local','kind':'project_implementation_evidence',
        'title':'Preserved offline agent semantics and recovery replay',
        'author':'Causal banking proposal project','year':2026,'version_date':'2026-10-13',
        'source_identity':'Six authored local cases; inherited executed replay',
        'local_copy':ref(ROOT/'docs/program/execution/2026-10-13/prototype-review/agent-replay/receipt.json','checks: six reproduced case outcomes; scope excludes live models'),
        'code':ref(ROOT/'src/causalbank/agent_workflow_v12.py','Local fixed-operation controller'),
        'inspected_anchors':['checks','scope','originals_unchanged'],
        'supported_claims':['Six authored offline outcomes were reproduced, including ambiguity, refusal, directed revision and weak moment sets.'],
        'limits':'Historical local conformance replay; no new live experiment or upstream framework execution.'
    }]
    assert cites==set(selected)|{s['integrated_citation_key'] for s in new}
    core.write(BASE/'source-audit.json',{'sources':new,'cutoff':'2026-10-07','primary_reinspection':ref(BASE/'primary-review.json','Reinspected external primary evidence'),'technical_claim_scope':'Architecture synthesis, project exact examples and inherited offline conformance.'})
    (BASE/'refs.bib').write_text('\n'.join('@misc{'+s['integrated_citation_key']+',\n author={{'+s['author']+'}},\n title={'+s['title']+'},\n year={2026},\n note={'+s['version_date']+'; project evidence}\n}\n' for s in new))
    DRIVER.write_text(expected_driver())
    core.write(BASE/'prepared-inputs.json',{'inputs':[ref(p,'Reviewed preserving input') for p in [OLD,PRIOR_AUDIT,BASE/'architecture.tex',BASE/'source-audit.json',BASE/'primary-review.json',BASE/'mathematical-review.json',Path(__file__)]],'generated':[ref(DRIVER,'Preserving reader driver'),ref(BASE/'refs.bib','New project citations')]})
    print(json.dumps({'prepared':str(DRIVER.relative_to(ROOT)),'reinspected_existing_sources':len(selected),'new_project_records':len(new)}))

def build():
    configure();OUT.mkdir(exist_ok=True)
    for suffix in ['.aux','.bbl','.toc','.out']:
        p=OUT/(NAME+suffix)
        if not p.exists():p.write_text('')
    with (OUT/'compile-summary.txt').open('w') as output,contextlib.redirect_stdout(output):inherited.build()
    report=json.loads((OUT/'build-report.json').read_text());report.pop('java_comparison',None)
    aux=(OUT/(NAME+'.aux')).read_text()
    def page(label):return int(re.search(r'\\newlabel\{'+re.escape(label)+r'\}\{\{[^}]*\}\{(\d+)\}',aux).group(1))
    report.update(builder=ref(Path(__file__),'Preserving architecture integration builder'),compile_routine=ref(ROOT/'tools/build_java_reader_20261013.py','Bounded compiler'),pdf=ref(PDF,'Working architecture successor'),predecessor_pdf=ref(OLD.with_suffix('.pdf'),'Preserved612-page reader'),agent_architecture={'first_printed_page':page('exec13:agent-architecture'),'last_printed_page':page('exec13:agent-architecture-end'),'live_calls':0},visual_review='Whole-reader visual acceptance remains open; changed-page inspection recorded separately.')
    audit=json.loads((OUT/'source-audit.json').read_text());audit['added_bibliography']=ref(BASE/'refs.bib','Architecture project evidence citations');core.write(OUT/'source-audit.json',audit)
    report['source_audit']=ref(OUT/'source-audit.json','Whole-reader primary-source traceability')
    core.write(OUT/'build-report.json',report)
    print(json.dumps({k:report[k] for k in ['pages','cited_records','agent_architecture','warnings']}))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['prepare','build']);args=parser.parse_args()
    prepare() if args.command=='prepare' else build()

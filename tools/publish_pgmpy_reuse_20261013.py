#!/usr/bin/env python3
"""Freeze a scoped proposal reuse decision and its preserving working reader."""
import json
from pathlib import Path
import re
import build_pgmpy_reuse_reader_20261013 as b
import build_integrated_monograph_v12 as shared
import master_control as core
import run_program as control

ROOT,BASE,OUT=b.ROOT,b.BASE,b.OUT
ref=shared.ref

def main():
    assert not (BASE/'working-release.json').exists()
    state=core.read(ROOT,core.STATE)
    build=json.loads((OUT/'build-report.json').read_text());audit=json.loads((OUT/'source-audit.json').read_text())
    prior=json.loads(b.PRIOR_AUDIT.read_text());trace=json.loads((BASE/'traceability-review.json').read_text());bounds=json.loads((OUT/'text-layout-review.json').read_text())
    assert trace['status']==bounds['status']=='pass' and trace['issues']==[]
    assert trace['pdf']['sha256']==build['pdf']['sha256']
    assert state['reader']['sha256']==build['predecessor_pdf']['sha256']
    assert build['pages']==bounds['pages'] and build['pages']>608
    assert not any(any(t in w.lower() for t in ['overfull','undefined','missing character']) for w in build['warnings'])
    assert b.DRIVER.read_text()==b.expected_driver()
    old={x['integrated_citation_key']:x for x in prior['sources']};new={x['integrated_citation_key']:x for x in audit['sources']}
    assert len(old)==453 and len(new)==455 and all(new[k]==v for k,v in old.items())
    for item in prior['tex_files']:core.bound(ROOT,item)
    for name in ['source-audit.json','manuscript-review.json','prepared-inputs.json','decision-review.json']:
        shared.verify_refs(json.loads((BASE/name).read_text()))
    shared.verify_refs(audit)
    text=(OUT/'reader.txt').read_text();flat=re.sub(r'\s+',' ',text)
    for phrase in ['26,064','543','NotImplementedError','6,000','one exposure and one outcome','MIT']:
        assert phrase in flat,phrase
    marker='The proposal selects a narrow pgmpy integration'
    found=[i+1 for i,p in enumerate(text.split('\f')) if marker in re.sub(r'\s+',' ',p)];assert len(found)==1
    physical={'first':found[0],'last':found[0]+build['pgmpy_reuse']['last_printed_page']-build['pgmpy_reuse']['first_printed_page']}
    artifacts=['source-selection.json','source-followup.json','blob-verification.json','primary-review.json','environment-inspection.json','oracle-results.json','adapter-contract.json','decision-review.json','source-audit.json','decision.tex','refs.bib','manuscript-review.json','prepared-inputs.json','traceability-review.json']
    evidence=[ref(BASE/p,p) for p in artifacts]
    review={'status':'pass','issues':[],'reviewer':{'name':'Codex author/coordinator','kind':'author'},'scope':'Pinned pgmpy reuse choice and exact-reader preservation','prior_citation_records_unchanged':453,'new_citation_records':2,'physical_pages':physical,'printed_pages':build['pgmpy_reuse'],'findings':['All predecessor inputs and453 citation records remain unchanged.','Fifteen source/guide/test/license files bind the selected Git tree; minimum-variance and descendant-validation boundaries are explicit.','The permitted path is a supplied observed-DAG adjustment candidate, independently validated against a conservative sufficient criterion.','Independent project references cover26064 d-separation cases, exact mediated effects, minimality and nonextendible graph semantics; no upstream execution is claimed.','Compilation, reference traceability and physical text bounds pass; visual and whole-program acceptance remain open.'],'evidence':evidence+[ref(OUT/'build-report.json','Compiled successor'),ref(OUT/'text-layout-review.json','All-page text bounds')],'visual_acceptance':False,'independent_review':False,'engine_executed':False}
    core.write(BASE/'release-source-review.json',review)
    code=['pgmpy_reuse_oracles_20261013.py','prepare_pgmpy_reuse_20261013.py','build_pgmpy_reuse_reader_20261013.py','publish_pgmpy_reuse_20261013.py']
    release={'kind':'working_monograph','final_acceptance':False,'pdf':build['pdf'],'pages':build['pages'],'supersedes':{k:state['reader'][k] for k in ['path','sha256']},'build_report':ref(OUT/'build-report.json','Compiled preserving reader'),'source_review':ref(BASE/'release-source-review.json','Substantive source and preservation review'),'text_layout':ref(OUT/'text-layout-review.json','All-page physical bounds'),'source_artifacts':audit['tex_files']+evidence+[ref(BASE/'release-source-review.json','Final author review')]+[ref(ROOT/'tools'/p,'Frozen computation/preparation/build/review source') for p in code],'visual_acceptance':False,'mandatory_repairs_closed':[],'changes':['Integrated a pinned pgmpy reuse decision, source-level method/validation boundaries and exact graph/servicing references.'],'sponsor_binding':'Prior sponsor preserved; final exact-reader coherence remains Q5 work.'}
    core.write(BASE/'working-release.json',release)
    control.ledger.validate_working_release(ROOT,ref(BASE/'working-release.json','Reviewed pgmpy working reader'))
    identifier='SW.DECISION.discovered_pgmpy';graph,_,_=control.combined(ROOT,state);node=next(n for n in graph['nodes'] if n['id']==identifier)
    path=ROOT/node['outputs'][0];assert not path.exists()
    contract=json.loads((BASE/'adapter-contract.json').read_text())
    decision={'operation_id':identifier,'choice':'integrate','canonical_engine':'pgmpy/pgmpy','aliases':'PC,GES,Adjustment,LLMPairwise are separate paths within the same engine, not independent implementations.','selected_revision':contract['engine'],'selected_scope':contract['integration_allowed_scope'],'integration_allowed':True,'engine_executed':False,'runtime_qualified':False,'implementation_state':'proposal contract and project oracles only','rejected_at_pin':['minimum-variance adjustment: explicit NotImplementedError','unchecked validation call as total-effect proof','PDAG conversion as equivalence-class validation'],'deferred':['discovery-to-effect coupling','generalized adjustment/latent graphs','effect estimation and statistical inference','LLM provider operations'],'alternatives':['Keep pgmpy as a reference; implement the small sufficient graphical check locally.','Use separately reviewed Tetrad or pcalg discovery contracts when their target/information assumptions match.','Retain nonidentification or unsupported scope when no reviewed method applies.'],'costs':'No MIT acquisition price; environment, dependency/notice review, timing/graph elicitation, conversion fixtures and maintenance require resources. No unmeasured dollar estimate.','owners':contract['owner_obligations'],'revisit_trigger':contract['revisit_trigger'],'evidence':[ref(BASE/p,p) for p in ['primary-review.json','adapter-contract.json','oracle-results.json','decision-review.json','working-release.json']]}
    core.write(path,decision)
    receipt={'operation_id':identifier,'operation_contract_sha256':core.digest_object(node),'outcome':'pass','execution':'performed','scope':'Reviewed reuse selection for the pinned supplied observed-DAG adjustment-candidate path; no engine execution','reviewer':{'name':'Codex author/coordinator','kind':'author'},'limitations':['Selected prototype implementation permission only; dependency lock and actual engine/conversion fixtures precede runtime qualification.','Project graph/SEM oracles and static call-path analysis are not upstream execution or empirical confidence.','No general latent/discovery/LLM capability, bank qualification or visual/whole-proposal acceptance.'],'original_gap_qualification':False,'capabilities':['integration_allowed'],'outputs':[ref(path,'Restricted pinned reuse decision')],'nonexecution_reason':'','revisit_trigger':contract['revisit_trigger'],'criteria':[{'index':0,'verdict':'pass','finding':'Canonical engine and internal paths distinguished; fifteen files match the pinned tree, with MIT terms, Python/dependency declarations and bounded maintenance evidence.','evidence':[ref(BASE/p,p) for p in ['primary-review.json','source-audit.json']]},{'index':1,'verdict':'pass','finding':'Candidate-set semantics, missing uncertainty, alternatives, lifecycle costs, named owner roles and upgrade triggers are developed in the integrated reader.','evidence':[ref(path,'Scoped decision'),ref(BASE/'decision.tex','Connected source/target/ownership argument'),ref(BASE/'working-release.json','Reviewed exact reader')]},{'index':2,'verdict':'pass','finding':'integration_allowed is limited to the permissible pinned graph candidate path with independent behavioral oracles, strict conversion, descendant/backdoor checks and distinct failure outcomes. No circular requirement for completed runtime before proposal selection.','evidence':[ref(BASE/p,p) for p in ['adapter-contract.json','oracle-results.json','decision-review.json']]}]}
    core.write(BASE/'operation-receipt.json',receipt)
    print(json.dumps({'pages':build['pages'],'citations':build['cited_records'],'physical_pages':physical,'pdf':build['pdf'],'outcome':'pass','integration_allowed_scope':contract['integration_allowed_scope']}))

if __name__=='__main__':main()

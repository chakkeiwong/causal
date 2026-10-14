#!/usr/bin/env python3
"""Review and freeze a working reader and commercial survey outcome."""
import json
from pathlib import Path
import re
import build_commercial_heterogeneity_reader_20261013 as b
import build_integrated_monograph_v12 as shared
import master_control as core
import run_program as control

ROOT,BASE,OUT=b.ROOT,b.BASE,b.OUT
ref=shared.ref

def main():
    assert not (BASE/'working-release.json').exists(),'Preserve published artifacts'
    state=core.read(ROOT,core.STATE)
    build=json.loads((OUT/'build-report.json').read_text())
    audit=json.loads((OUT/'source-audit.json').read_text())
    prior=json.loads(b.PRIOR_AUDIT.read_text())
    trace=json.loads((BASE/'traceability-review.json').read_text())
    bounds=json.loads((OUT/'text-layout-review.json').read_text())
    assert trace['status']==bounds['status']=='pass' and trace['issues']==[]
    assert trace['pdf']['sha256']==build['pdf']['sha256']
    assert state['reader']['sha256']==build['predecessor_pdf']['sha256']
    assert build['pages']==bounds['pages'] and build['pages']>601
    assert not any(any(t in w.lower() for t in ['overfull','undefined','missing character']) for w in build['warnings'])
    assert b.DRIVER.read_text()==b.expected_driver()
    old={x['integrated_citation_key']:x for x in prior['sources']}
    new={x['integrated_citation_key']:x for x in audit['sources']}
    assert len(old)==446 and len(new)==453 and all(new[k]==v for k,v in old.items())
    for item in prior['tex_files']:core.bound(ROOT,item)
    for name in ['source-audit.json','manuscript-review.json','prepared-inputs.json','exact-review.json']:
        shared.verify_refs(json.loads((BASE/name).read_text()))
    shared.verify_refs(audit)
    text=(OUT/'reader.txt').read_text();flat=re.sub(r'\s+',' ',text)
    for phrase in ['214/43','.990234375','14,401','1.20502','Stata','DataRobot','prespecified']:
        assert phrase in flat,phrase
    physical={}
    for key,marker in [('commercial_heterogeneity','A servicing manager deciding whom to contact'),('temporal_design','The restricted continuous-lag argument separates mathematical coverage')]:
        found=[i+1 for i,p in enumerate(text.split('\f')) if marker in re.sub(r'\s+',' ',p)]
        assert len(found)==1,(key,found)
        physical[key]={'first':found[0],'last':found[0]+build[key]['last_printed_page']-build[key]['first_printed_page']}
    artifacts=['plan-review.md','search-protocol.json','acquisition-review.json','candidate-register.json','omissions-register.json','exact-results.json','exact-review.json','source-audit.json','comparison.tex','temporal-clarification.tex','master-execution-preserving.tex','refs.bib','manuscript-review.json','prepared-inputs.json','traceability-review.json']
    evidence=[ref(BASE/n,n) for n in artifacts]
    review={'status':'pass','issues':[],'reviewer':{'name':'Codex author/coordinator','kind':'author'},'scope':'Exact-reader comparison, temporal clarification and predecessor preservation','prior_citation_records_unchanged':446,'new_citation_records':7,'physical_pages':physical,'findings':['Seventeen-family bounded survey retains all missing-method and rights obligations; complete-cell acceptance is not claimed.','Ten complete saved technical documents and project evidence support all new citations; failed/partial/redirect bodies are excluded from method evidence.','Separate exact population calculation verifies all generated servicing targets and policy quantities.','Persistent temporal cell passes original raw finite-fraction rule; other failures and the negative final-study design outcome remain unchanged.','All prior manuscript files and citation records remain byte-preserved; one copied paragraph is precisely clarified in the new driver.','Compilation, exact-reader traceability and all-page text bounds pass. Visual and whole-program acceptance remain open.'],'evidence':evidence+[ref(OUT/'build-report.json','Final bounded compilation'),ref(OUT/'text-layout-review.json','All-page physical text bounds')],'visual_acceptance':False,'independent_review':False,'MR01_acceptance':False}
    core.write(BASE/'release-source-review.json',review)
    code=['prepare_commercial_heterogeneity_20261013.py','commercial_heterogeneity_examples_20261013.py','build_commercial_heterogeneity_reader_20261013.py','publish_commercial_heterogeneity_20261013.py']
    release={'kind':'working_monograph','final_acceptance':False,'pdf':build['pdf'],'pages':build['pages'],'supersedes':{k:state['reader'][k] for k in ['path','sha256']},'build_report':ref(OUT/'build-report.json','Compiled preserving successor'),'source_review':ref(BASE/'release-source-review.json','Substantive and predecessor-preservation review'),'text_layout':ref(OUT/'text-layout-review.json','All-page text bounds'),'source_artifacts':audit['tex_files']+evidence+[ref(BASE/'release-source-review.json','Final author review')]+[ref(ROOT/'tools'/n,'Frozen preparation/computation/build/review code') for n in code],'visual_acceptance':False,'mandatory_repairs_closed':[],'changes':['Integrated commercial heterogeneous-effects comparison with exact target/policy examples.','Clarified persistent temporal availability and final-study feasibility without rewriting earlier evidence.'],'sponsor_binding':'Prior sponsor preserved; exact-reader whole-proposal coherence remains Q5 work.'}
    core.write(BASE/'working-release.json',release)
    control.ledger.validate_working_release(ROOT,ref(BASE/'working-release.json','Reviewed working release'))
    identifier='SW.CELL.effects_heterogeneity.commercial'
    graph,_,_=control.combined(ROOT,state);node=next(n for n in graph['nodes'] if n['id']==identifier)
    output=ROOT/node['outputs'][0];assert not output.exists()
    coverage={'operation_id':identifier,'outcome':'inconclusive','execution':'performed','families':17,'saved_attempts':16,'complete_technical_documents':10,'technical_source_records':4,'all_new_citation_records':7,'commercial_execution':False,'independent_review':False,'essential_coverage_open':True,'evidence':evidence+[ref(BASE/'working-release.json','Integrated working comparison')],'next_action':'Acquire family-specific missing technical/version/rights records in the omissions register; execute licensed matched comparisons only for later empirical claims.'}
    core.write(output,coverage)
    receipt={'operation_id':identifier,'operation_contract_sha256':core.digest_object(node),'outcome':'inconclusive','execution':'performed','scope':'Developed bounded seventeen-family heterogeneous-effects comparison, exact servicing constructions and explicit unresolved evidence','reviewer':{'name':'Codex author/coordinator','kind':'author'},'limitations':['Fourteen families lack a newly matched complete technical treatment; exact-cutoff bytes, runtime and rights remain unqualified.','Recovered acquisition metadata lacks original request timestamps and process exit codes; no invented precision.','No paid vendor execution, comparative performance, bank ROI or complete MR01/visual acceptance.'],'original_gap_qualification':False,'capabilities':[],'outputs':[ref(output,'Reviewed commercial heterogeneity coverage')],'nonexecution_reason':'','revisit_trigger':'Acquire complete method/edition/rights sources specified in the omissions register and publish a reviewed successor comparison.','criteria':[{'index':0,'verdict':'inconclusive','finding':'All seventeen declared families and aliases received a finite local corpus search; public acquisitions are bounded and retained, but complete technical and exact-cutoff coverage remains unresolved.','evidence':[ref(BASE/p,p) for p in ['search-protocol.json','candidate-register.json','acquisition-review.json']]},{'index':1,'verdict':'pass','finding':'All asserted new technical and project claims bind authentic local bytes, date/version limits, hashes and inspected anchors. Exact examples and final reader traceability pass.','evidence':[ref(BASE/p,p) for p in ['source-audit.json','exact-review.json','traceability-review.json','release-source-review.json']]},{'index':2,'verdict':'pass','finding':'Alternatives, conditional integration routes and essential omissions are explicit; neither absent features nor waived unavailable evidence is claimed. The overall cell remains inconclusive.','evidence':[ref(BASE/p,p) for p in ['omissions-register.json','comparison.tex','working-release.json']]}]}
    core.write(BASE/'operation-receipt.json',receipt)
    print(json.dumps({'pages':build['pages'],'citations':build['cited_records'],'physical_pages':physical,'pdf':build['pdf'],'outcome':'inconclusive'}))

if __name__=='__main__':main()

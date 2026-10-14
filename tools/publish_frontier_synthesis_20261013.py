#!/usr/bin/env python3
"""Record the developed frontier draft without awarding whole-proposal acceptance."""
import json
import re
from pathlib import Path
import build_frontier_synthesis_reader_20261013 as b
import master_control as core
import run_program as control
ROOT,BASE,OUT,ref=b.ROOT,b.BASE,b.OUT,b.ref

def main():
    assert not (BASE/'working-release.json').exists()
    state=core.read(ROOT,core.STATE)
    build=json.loads((OUT/'build-report.json').read_text())
    audit=json.loads((OUT/'source-audit.json').read_text())
    prior=json.loads(b.PRIOR_AUDIT.read_text())
    trace=json.loads((BASE/'traceability-review.json').read_text())
    bounds=json.loads((OUT/'text-layout-review.json').read_text())
    assert trace['status']==bounds['status']=='pass' and not trace['issues']
    assert trace['pdf']['sha256']==build['pdf']['sha256']
    assert state['reader']['sha256']==build['predecessor_pdf']['sha256']
    assert build['pages']==bounds['pages']==625
    assert not any(any(t in w.lower() for t in ['overfull','undefined','missing character']) for w in build['warnings'])
    assert b.DRIVER.read_text()==b.expected_driver()
    old={s['integrated_citation_key']:s for s in prior['sources']}
    new={s['integrated_citation_key']:s for s in audit['sources']}
    assert len(old)==457 and len(new)==458 and all(new[k]==v for k,v in old.items())
    for item in prior['tex_files']:core.bound(ROOT,item)
    b.shared.verify_refs(audit)
    text=(OUT/'reader.txt').read_text();flat=re.sub(r'\s+',' ',text)
    for term in ['.78025248','17/24','.76 to .90','answer key','minimax','250(1']:
        assert term in flat,term
    physical_first=next(i+1 for i,p in enumerate(text.split('\f')) if 'The inspected literature gives reasons to invest' in p)
    artifacts=['plan-review.md','development.tex','exact-results.json','primary-review.json','mathematical-review.json','source-audit.json','refs.bib','prepared-inputs.json','traceability-review.json']
    evidence=[ref(BASE/p,p) for p in artifacts]
    review={'status':'pass','issues':[],'reviewer':{'name':'Codex author/coordinator','kind':'author'},
      'scope':'Developed frontier chapter, exact examples and preserving integrated reader',
      'prior_citation_records_unchanged':457,'new_project_records':1,
      'physical_addition_pages':{'first':physical_first,'last':physical_first+4},
      'printed_pages':build['frontier_chapter'],
      'findings':[
        'The inherited chapter remains byte-identical through a wrapper; five additional pages compare task, information, assumptions, oracle, budget and loss.',
        'Seven primary sources support favorable/adverse comparisons; supervised and deterministic alternatives remain explicit.',
        'Published point-score reweighting has no invented sampling uncertainty or bank task weights.',
        'Conditional chain rule and marginal joint bounds are distinguished and checked against finite constructions.',
        'Answer-key disagreement bounds do not assert an empirical benchmark error rate.',
        'Two-world regret and public/generated portfolios connect evidence to banking decisions without claiming actual bank qualification.',
        'All625 pages pass physical text bounds;458 source records pass traceability; no overfull, unresolved or missing-character warning.'],
      'evidence':evidence+[ref(b.CHAPTER,'Preserving developed frontier chapter'),ref(OUT/'build-report.json','Compiled successor'),ref(OUT/'text-layout-review.json','Physical text bounds')],
      'visual_acceptance':False,'independent_review':False,'live_calls':0}
    core.write(BASE/'release-source-review.json',review)
    release={'kind':'working_monograph','final_acceptance':False,'pdf':build['pdf'],'pages':build['pages'],
      'supersedes':{k:state['reader'][k] for k in ['path','sha256']},
      'build_report':ref(OUT/'build-report.json','Compiled frontier successor'),
      'source_review':ref(BASE/'release-source-review.json','Author claim and preservation review'),
      'text_layout':ref(OUT/'text-layout-review.json','All-page text bounds'),
      'source_artifacts':audit['tex_files']+evidence+[ref(BASE/'release-source-review.json','Final author review')]+[ref(ROOT/'tools'/p,'Frozen exact computation/build/publication source') for p in ['frontier_evidence_examples_20261013.py','build_frontier_synthesis_reader_20261013.py','publish_frontier_synthesis_20261013.py']],
      'visual_acceptance':False,'mandatory_repairs_closed':[],
      'changes':['Preserving frontier chapter expansion: primary comparisons, task mixture, workflow composition, oracle uncertainty, decision regret and public-evidence portfolio.'],
      'sponsor_binding':'Prior sponsor preserved; exact final-release coherence and visual acceptance remain Q5 work.'}
    core.write(BASE/'working-release.json',release)
    control.ledger.validate_working_release(ROOT,ref(BASE/'working-release.json','Reviewed frontier working reader'))
    identifier='TEXT.DRAFT.L1';g,_,_=control.combined(ROOT,state);node=next(n for n in g['nodes'] if n['id']==identifier)
    assert node['outputs']==[str(b.CHAPTER.relative_to(ROOT))]
    receipt={'operation_id':identifier,'operation_contract_sha256':core.digest_object(node),
      'outcome':'pass','execution':'performed','scope':'Developed frontier literature/evidence chapter draft, integrated into preserving working reader',
      'reviewer':{'name':'Codex author/coordinator','kind':'author'},
      'limitations':['Bounded inspected corpus; unread original candidates and search saturation remain open.','No new live-model, bank, external platform or independent acceptance.','This draft receipt does not close MR02 or final rendered review.'],
      'original_gap_qualification':False,'capabilities':[],'outputs':[ref(b.CHAPTER,'Preserving developed frontier chapter')],
      'nonexecution_reason':'','revisit_trigger':'New relevant primary evidence, completed source census or matched held-out demonstration changes the synthesis.',
      'criteria':[
       {'index':0,'verdict':'pass','finding':'Connected argument supplies assumptions, notation, exact derivations, adverse findings, alternatives, task composition and banking decision consequences.','evidence':[ref(BASE/'development.tex','Developed synthesis'),ref(BASE/'mathematical-review.json','Exact derivation review'),ref(BASE/'exact-results.json','Independent finite examples')]},
       {'index':1,'verdict':'pass','finding':'Inherited sources preserved; primary evidence reinspected; new exact examples labeled; process records separate;625-page integrated reader and458-record traceability checked.','evidence':[ref(BASE/'primary-review.json','Primary source comparisons'),ref(BASE/'release-source-review.json','Substantive release review'),ref(BASE/'working-release.json','Exact reader binding')]}]}
    core.write(BASE/'operation-receipt.json',receipt)
    print(json.dumps({'pages':625,'citations':458,'physical_addition_pages':review['physical_addition_pages'],'outcome':'pass'}))

if __name__=='__main__':main()

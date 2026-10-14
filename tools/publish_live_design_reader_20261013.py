#!/usr/bin/env python3
"""Record the prospective design without claiming a live experiment."""
import json
from pathlib import Path
import re

import build_integrated_monograph_v12 as shared
import master_control as core
import run_program as run

ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-13/live-evaluation'
OUT=BASE/'reader'
OP='LL.LIVE.DESIGN'
ref=shared.ref


def write(path,value):
    assert not path.exists(),'Preserve earlier evidence: '+str(path)
    core.write(path,value)


def main():
    state=core.read(ROOT,core.STATE);before=core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active']['operation']==OP
    assert state['reader']['path']=='docs/causal_proposal_pcalg_2026-10-13.pdf'
    report=json.loads((OUT/'build-report.json').read_text())
    audit=json.loads((OUT/'source-audit.json').read_text())
    old_audit=json.loads((ROOT/'docs/program/execution/2026-10-13/pcalg-reuse/reader/source-audit.json').read_text())
    for name in ['source-audit.json','author-review.json','prepared-inputs.json','reader/source-audit.json']:
        shared.verify_refs(json.loads((BASE/name).read_text()))
    old_driver=ROOT/'docs/causal_proposal_pcalg_2026-10-13.tex'
    expected=old_driver.read_text().replace(r'\input{program/execution/2026-10-13/llm-census/evaluation.tex}',
        r'\input{program/execution/2026-10-13/llm-census/evaluation.tex}'+'\n'+
        r'\input{program/execution/2026-10-13/live-evaluation/evaluation.tex}',1).replace(
        'program/execution/2026-10-13/pcalg-reuse/refs}',
        'program/execution/2026-10-13/pcalg-reuse/refs,program/execution/2026-10-13/live-evaluation/refs}',1)
    assert (ROOT/report['driver']['path']).read_text()==expected
    old_files=[r for r in old_audit['tex_files'] if r['path']!=str(old_driver.relative_to(ROOT))]
    for item in old_files:core.bound(ROOT,item)
    old_sources={s['integrated_citation_key']:s for s in old_audit['sources']}
    new_sources={s['integrated_citation_key']:s for s in audit['sources']}
    assert all(new_sources[k]==v for k,v in old_sources.items())
    assert set(new_sources)-set(old_sources)=={'exec13_live_planning'}
    assert (BASE/'planning-results.json').read_bytes()==(BASE/'planning-replay.json').read_bytes()
    text=re.sub(r'\s+',' ',(OUT/'reader.txt').read_text())
    for phrase in ['59 for one claim, 94 for six, and 107 for twelve','43,200 calls','83.43%',
                   'not a registered trial','prices remain to be selected']:
        assert phrase in text,phrase
    assert not any('Overfull' in w or 'undefined' in w.lower() for w in report['warnings'])
    output=ROOT/'docs/program/comprehensive-v14/work/LL.LIVE.DESIGN/prospective-design.json'
    design=json.loads(output.read_text())
    assert design['registration'] is None and design['live_calls']==0
    assert design['analysis']['final_sample_size'] is None and design['analysis']['final_thresholds'] is None
    assert design['budget']['actual_prices'] is None and design['budget']['final_currency_ceiling'] is None
    names=['plan-review.md','source-audit.json','author-review.json','planning-results.json','planning-replay.json',
           'fixture-structure-review.json','evaluation.md','prepared-inputs.json','refs.bib']
    review={'status':'pass','issues':[],'reviewer':{'name':'Codex author/coordinator','kind':'author'},
        'scope':'Prospective evaluation section and preserving reader delta; no final registration or model performance claim',
        'old_compiled_files_unchanged':len(old_files),'prior_citation_records_unchanged':len(old_sources),
        'new_citation_records':1,'driver_change':'One section input and one bibliography path',
        'findings':['Derivations state independent-mechanism and joint multiplicity assumptions explicitly.',
            'Small-n rational enumeration independently checks binomial-mixture power and null error control.',
            'Final models, sample sizes, thresholds, prices, adjudicators and ceilings remain unset.',
            'All quoted numerical/cost examples survive extraction; no paid/model execution or bank claim.',
            'No unresolved citations/references, overfull boxes, empty pages or text outside physical bounds.'],
        'evidence':[ref(output,'Actual prospective design')]+[ref(BASE/n,n) for n in names]+[
            ref(OUT/'build-report.json','Compiled exact reader'),ref(OUT/'text-layout-review.json','Physical text bounds')],
        'visual_acceptance':False}
    write(BASE/'release-source-review.json',review)
    release={'kind':'working_monograph','final_acceptance':False,'pdf':report['pdf'],'pages':report['pages'],
        'supersedes':{k:state['reader'][k] for k in ['path','sha256']},
        'build_report':ref(OUT/'build-report.json','Prospective evaluation integration'),
        'source_review':ref(BASE/'release-source-review.json','Reviewed claims and delta'),
        'text_layout':ref(OUT/'text-layout-review.json','Whole-reader physical text bounds'),
        'source_artifacts':audit['tex_files']+[ref(output,'Reviewed prospective design')]+[
            ref(BASE/n,'New-section evidence') for n in names+['release-source-review.json']]+[
            ref(ROOT/'tools'/n,'Planning/build/publication code') for n in ['live_evaluation_planning_20261013.py',
                'build_live_design_reader_20261013.py','publish_live_design_reader_20261013.py']],
        'visual_acceptance':False,'mandatory_repairs_closed':[],
        'changes':['Developed mechanism-level live evaluation, information contracts, abstention and graph/effect metrics.',
            'Added exact illustrative power, zero-error precision and complete call/token accounting.',
            'Preserved actual-versus-proposed boundary and explicit unset final inputs.'],
        'sponsor_binding':'Prior sponsor remains preserved; exact current-reader reconciliation is still Q5 work.'}
    write(BASE/'working-release.json',release)
    binding=ref(BASE/'working-release.json','Reviewed prospective-evaluation working reader')
    run.ledger.validate_working_release(ROOT,binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader']={k:report['pdf'][k] for k in ['path','sha256']}
    state['reader'].update(pages=report['pages'],status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT,before,state,{'action':'publish_live_design_working_reader','manifest':binding,
        'original_gap_qualification':False,'final_acceptance':False})
    graph,_,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP)
    receipt=run.ledger.receipt_template(node)
    receipt.update(outcome='pass',execution='performed',
        scope='Reviewed prospective public/generated causal-assistance experiment and exact planning examples; final live experiment not registered or run.',
        reviewer={'name':'Codex author/coordinator','kind':'author'},
        limitations=['Exact backend revisions, actual prices and ceiling, final sample/threshold/alpha allocations, held-out draw and qualified baselines remain unset.',
            'Independent/common-law mechanisms are explicit planning assumptions, not facts about authored P6 templates.',
            'No live-model, independent, bank or rendered visual acceptance.'],
        outputs=[ref(output,'Complete prospective design with unknown inputs visible')],nonexecution_reason='',
        revisit_trigger='Supply scoped actual backend/custody, priced budget, held-out mechanism law/draw, references and qualified baselines; freeze before final study calls.')
    receipt['criteria']=[{'index':0,'verdict':'pass',
        'finding':'Task/graph/effect metrics, information-matched role-specific baselines, label/language/retrieval ablations, abstention and all-request accounting are specified. Exact power/precision/cost scenarios are explicitly hypothetical; every required final model, sample, threshold and price field remains unset, with no fabricated registration or trial.',
        'evidence':[ref(output,'Reviewed prospective design'),ref(BASE/'author-review.json','Substantive review'),
            ref(BASE/'planning-results.json','Reproduced planning calculations'),binding]}]
    receipt_path=BASE/(OP+'.receipt.json');write(receipt_path,receipt)
    print(json.dumps({'published':state['reader'],'receipt':str(receipt_path.relative_to(ROOT)),'live_calls':0}))


if __name__=='__main__':main()

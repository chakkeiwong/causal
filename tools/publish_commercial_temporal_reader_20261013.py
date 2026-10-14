#!/usr/bin/env python3
"""Publish scoped new text with honest unresolved commercial coverage."""
import json
from pathlib import Path

import build_integrated_monograph_v12 as shared
import master_control as core
import run_program as run

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/commercial-temporal'
OUT = BASE / 'reader'
OP = 'SW.CELL.discovery_temporal_interventional.commercial'
ref = shared.ref


def write(path, value):
    assert not path.exists(), 'Preserve earlier evidence: ' + str(path)
    core.write(path, value)


def main():
    state=core.read(ROOT,core.STATE);before=core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active']['operation']==OP
    assert state['reader']['path']=='docs/causal_proposal_temporal_information_2026-10-13.pdf'
    report=core.read(ROOT,str((OUT/'build-report.json').relative_to(ROOT)))
    audit=core.read(ROOT,str((OUT/'source-audit.json').relative_to(ROOT)))
    for path in [BASE/'source-audit.json',BASE/'prepared-inputs.json',BASE/'author-review.json',
                 BASE/'source-and-example-review.json',OUT/'source-audit.json']:
        shared.verify_refs(json.loads(path.read_text()))
    names=['search-protocol.json','candidate-register.json','local-candidate-search.json','omissions-register.json',
        'acquisition-review-complete.json','source-audit.json','comparison.md','author-review.json',
        'source-and-example-review.json','exact-results.json','exact-replay.json','release-source-review.json',
        'prepared-inputs.json','refs.bib']
    release={'kind':'working_monograph','final_acceptance':False,'pdf':report['pdf'],'pages':report['pages'],
        'supersedes':{k:state['reader'][k] for k in ['path','sha256']},
        'build_report':ref(OUT/'build-report.json','Compiled commercial temporal successor'),
        'source_review':ref(BASE/'release-source-review.json','Scoped source/claim and extracted text review'),
        'text_layout':ref(OUT/'text-layout-review.json','Whole-reader physical text bounds'),
        'source_artifacts':audit['tex_files']+[ref(BASE/n,'Reviewed new-section source') for n in names]+[
            ref(ROOT/'tools/commercial_temporal_examples_20261013.py','Exact stipulated model calculations'),
            ref(ROOT/'tools/build_commercial_temporal_reader_20261013.py','Preserving builder'),ref(Path(__file__),'Publication code')],
        'visual_acceptance':False,'mandatory_repairs_closed':[],
        'changes':['Added six substantive commercial temporal/intervention comparisons from a13-family bounded survey.',
            'Added exact funding examples separating predictive improvement, structural identification and bank action value.',
            'Documented seven unresolved commercial families and detailed API/rights/edition gaps without absence claims.'],
        'sponsor_binding':'Sponsor remains a prior bound document; Q5 reconciliation remains open.'}
    release_path=BASE/'working-release.json';write(release_path,release)
    binding=ref(release_path,'Reviewed commercial temporal working reader')
    run.ledger.validate_working_release(ROOT,binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader']={k:report['pdf'][k] for k in ['path','sha256']}
    state['reader'].update(pages=report['pages'],status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT,before,state,{'action':'publish_commercial_temporal_working_reader','manifest':binding,
        'original_gap_qualification':False,'final_acceptance':False})
    graph,_,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP)
    output=ROOT/node['outputs'][0]
    evidence=[ref(BASE/name,name) for name in ['search-protocol.json','candidate-register.json','source-audit.json',
        'omissions-register.json','author-review.json','source-and-example-review.json','release-source-review.json']]+[binding]
    write(output,{'operation_id':OP,'outcome':'inconclusive','execution':'performed',
        'scope':'Thirteen-family bounded official source review, six developed comparisons and new integrated working text. Seven families retain essential technical omissions.',
        'reviewed_reader':report['pdf'],'evidence':evidence,'criteria_dispositions':['pass','pass','inconclusive'],
        'finding':'All asserted new technical and numerical claims are traced and scoped, but this cell cannot be accepted as complete while seven named essential candidate comparisons and several detailed configuration/API/license checks remain unresolved.',
        'revisit_trigger':'Obtain authentic edition-matched technical sources for the named omissions, inspect algorithm/time-grid/intervention/uncertainty and API/rights semantics, integrate a preserving comparison and review a successor.',
        'runtime_executed':False,'original_gap_qualification':False})
    receipt=run.ledger.receipt_template(node)
    receipt.update(outcome='inconclusive',execution='performed',
        scope='Executed bounded source review and integrated commercial temporal comparison; full cell acceptance withheld.',
        reviewer={'name':'Codex author/coordinator','kind':'author'},
        limitations=['Seven candidate families lack essential matching technical sources.',
            'IBM detail routes returned navigation; SAS equation-image and mutable-cutoff limits are explicit.',
            'License/deployment rights, API parity, vendor performance and bank operation remain unverified.',
            'No paid runtime, independent acceptance, original-gap qualification or rendered visual acceptance.'],
        outputs=[ref(output,'Commercial temporal coverage review with unresolved essential omissions')],
        nonexecution_reason='',revisit_trigger='See the exact triggers in the omissions register and coverage review.')
    receipt['criteria']=[
        {'index':0,'verdict':'pass','finding':'All13 declared candidate families and aliases searched against preserved official records;28 bounded official public reads completed, with cutoff and stopping rule recorded.',
         'evidence':[ref(BASE/'search-protocol.json','Candidate universe and stopping rule'),ref(BASE/'candidate-register.json','Candidate-level findings'),ref(BASE/'acquisition-review-complete.json','All completed reads')]},
        {'index':1,'verdict':'pass','finding':'Twelve cited official technical documents and one project exact source have identities, hashes, versions/dates, inspected passages and explicitly bounded claims; exact examples reproduce.',
         'evidence':[ref(BASE/'source-audit.json','Primary text anchors and claim limits'),ref(BASE/'source-and-example-review.json','Source identities and exact replay'),binding]},
        {'index':2,'verdict':'inconclusive','finding':'Alternatives, software strengths and reuse choices are developed, but seven essential candidate comparisons and detailed edition/API/license gaps remain. No absence conclusion or waiver is substituted.',
         'evidence':[ref(BASE/'omissions-register.json','Unresolved essentials and exact revisit triggers'),ref(BASE/'author-review.json','Substantive review'),ref(output,'Actual inconclusive coverage outcome')]}]
    receipt_path=BASE/(OP+'.receipt.json');write(receipt_path,receipt)
    print(json.dumps({'published':state['reader'],'outcome':'inconclusive','receipt':str(receipt_path.relative_to(ROOT))}))


if __name__=='__main__':
    main()

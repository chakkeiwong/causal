#!/usr/bin/env python3
"""Review and bind the C++ design delivery, without promoting engine claims."""
import json
from pathlib import Path

import build_integrated_monograph_v12 as shared
import master_control as core
import run_program as run

ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-13/grf-cxx'
OUT=BASE/'reader'
OP='IN.DESIGN.Cxx'
ref=shared.ref


def write(path,value):
    if path.exists():raise ValueError('Preserve evidence: '+str(path))
    core.write(path,value)


def main():
    state=core.read(ROOT,core.STATE);before=core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active']['operation']==OP
    assert state['reader']['path']=='docs/causal_proposal_python_discovery_2026-10-13.pdf'
    report=json.loads((OUT/'build-report.json').read_text())
    audit=json.loads((OUT/'source-audit.json').read_text())
    bounds=json.loads((OUT/'text-layout-review.json').read_text())
    for path in [BASE/'source-audit.json',BASE/'prepared-inputs.json',OUT/'source-audit.json',BASE/'reproduction-review.json']:
        shared.verify_refs(json.loads(path.read_text()))
    assert bounds['status']=='pass' and bounds['pages']==report['pages']
    assert not any('Overfull' in w or 'undefined' in w for w in report['warnings'])
    assert json.loads((BASE/'reproduction-review.json').read_text())['status']=='pass'
    assert '-Werror' in json.loads((BASE/'reproduction-review.json').read_text())['flags']
    assert json.loads((BASE/'wire-examples.json').read_text())['status']=='pass'
    pages=(OUT/'reader.txt').read_text().split('\f')
    first=next(i for i,p in enumerate(pages) if 'A servicing analyst asks' in p)
    last=next(i for i in range(first,len(pages)) if 'additional statistical and deployment machinery' in pages[i])
    body='\n'.join(pages[first:last+1])
    for phrase in ['twenty-five','225','column-major','serialize','out-of-bag','1600','2.6.1']:
        assert phrase in body,phrase
    write(BASE/'chapter-text-review.json',{'status':'pass','scope':'Extracted text and physical bounds only',
        'pdf':report['pdf'],'physical_pages':list(range(first+1,last+2)),
        'page_word_counts':[len(p.split()) for p in pages[first:last+1]],
        'findings':['Source-backed narrative, formulas and exact example anchors retained in compiled reader.',
                    'All citations and labels resolve; no overfull text or physical-bound failure.',
                    'Inherited whole-reader rendered review remains pending under the session image allowance.'],
        'visual_acceptance':False,'chapter_depth_acceptance':False})
    contract=ROOT/'docs/program/comprehensive-v14/work/IN.DESIGN.Cxx/adapter-contract.json'
    findings=[
        {'criterion':'Estimand and sampling','finding':'Initial complete IID binary customer ATE profile is explicit; cluster and target-weight extensions distinguished; supplied-score fixtures not advertised as admissible training.'},
        {'criterion':'Coordinates and topology','finding':'Retains row/feature/role map, units, sign, clock, population and graph/set ambiguity. No representative graph silently selected and no covariance slope promoted to dose contrast.'},
        {'criterion':'Statistical conversion','finding':'R nuisance residualization precedes C++; native conditional slope, AIPW score, average-effect SE and conditional variance remain separate. Exact scores independently checked.'},
        {'criterion':'Native ownership','finding':'Inspected borrowed column-major buffer and destructive tree serialization become lifetime/coordinate/persistence requirements; ABI and concurrency remain unqualified.'},
        {'criterion':'Failure and evidence','finding':'Unavailable/unsupported/refused/failure distinctions are actionable; nonfinite or weak-support cases cannot emit successful finite effects. Four schema examples pass; no adapter execution implied.'},
        {'criterion':'Dependencies and rights','finding':'Pinned commit, dated originals and all build/dependency/license claims have inspected anchors; declaration is not installed-environment or license-distribution clearance.'},
        {'criterion':'Reproduction repair','finding':'Preserved inherited flags receipt and reviewer code. Corrected omitted -Werror in the unpublished report and reran exact arithmetic: ten comparisons, five rejections pass.'},
        {'criterion':'Manuscript','finding':'Connected banking question, score derivation, target/covariance counterexamples, memory/persistence/deployment alternatives and qualification experiment integrated; no MR03/Q1 acceptance inferred.'}]
    inputs=[contract,BASE/'source-audit.json',BASE/'adapter.md',BASE/'reproduction-review.json',
            BASE/'wire-examples.json',BASE/'wire-input.json',BASE/'wire-configuration.json',BASE/'chapter-text-review.json']
    write(BASE/'author-review.json',{'status':'pass','issues':[],
        'reviewer':{'name':'Current author/coordinator','kind':'author'},
        'scope':'IN.DESIGN.Cxx proposal design criterion only','findings':findings,
        'evidence':[ref(p,'Reviewed source, design or exact reference') for p in inputs],
        'limitations':['No grf/R/native engine or transport execution; no coverage/ABI qualification.',
                       'No independent acceptance, bank data validation or full MR03 depth acceptance.',
                       'Rendered visual acceptance remains pending.']})
    write(BASE/'release-source-review.json',{'status':'pass','issues':[],
        'scope':'Incremental source/claim and preserving manuscript review; not final proposal acceptance',
        'evidence':[ref(BASE/'author-review.json','Full design criterion review'),ref(BASE/'source-audit.json','Primary-source identities and anchors')],
        'visual_acceptance':False})
    inputs.extend([BASE/'author-review.json',BASE/'release-source-review.json',BASE/'prepared-inputs.json',BASE/'refs.bib',
                   ROOT/'tools/prepare_grf_contract_20261013.py',ROOT/'tools/build_grf_reader_20261013.py',
                   ROOT/'tools/run_grf_boundary_oracle_20261013.py',ROOT/'tools/grf_boundary_oracle_20261013.cpp',Path(__file__)])
    release={'kind':'working_monograph','final_acceptance':False,'pdf':report['pdf'],'pages':report['pages'],
        'supersedes':{k:state['reader'][k] for k in ['path','sha256']},
        'build_report':ref(OUT/'build-report.json','Compiled native forest design successor'),
        'source_review':ref(BASE/'release-source-review.json','Reviewed source/claim integration'),
        'text_layout':ref(OUT/'text-layout-review.json','Whole-reader physical bounds'),
        'source_artifacts':audit['tex_files']+[ref(p,'Reviewed working-release evidence') for p in inputs],
        'visual_acceptance':False,'mandatory_repairs_closed':[],
        'changes':['Integrated binary IID grf R/native proposal contract and native-embedding alternative.',
                   'Derived target, score and cluster-variance counterexamples with exact independent arithmetic.',
                   'Source-inspected borrowed memory, consuming serialization, build/rights and failure contracts.'],
        'sponsor_binding':'Prior sponsor reader binding remains historical; exact-release reconciliation is Q5 work.'}
    release_path=BASE/'working-release.json';write(release_path,release)
    binding=ref(release_path,'Reviewed working native forest reader')
    run.ledger.validate_working_release(ROOT,binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader']={k:report['pdf'][k] for k in ['path','sha256']}
    state['reader'].update(pages=report['pages'],status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT,before,state,{'action':'publish_native_forest_working_reader','manifest':binding,
                                 'original_gap_qualification':False,'final_acceptance':False})
    graph,_,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP)
    receipt=run.ledger.receipt_template(node)
    receipt.update(outcome='pass',execution='performed',scope='Reviewed restricted grf C++/R boundary proposal design and exact project references',
        reviewer={'name':'Current author/coordinator','kind':'author'},
        limitations=['No grf engine or adapter execution, inference qualification, bank/independent acceptance or MR03 closure.',
                     'Initial implementation route requires future dependency, ownership, serialization, failure and oracle admission.',
                     'Rendered review remains pending.'],outputs=[ref(contract,'Reviewed native-boundary contract')],
        nonexecution_reason='',revisit_trigger='')
    receipt['criteria']=[{'index':0,'verdict':'pass',
        'finding':'Design retains estimand, graph/set ambiguity, coordinates, units and sampling; defines original R/native conversion, bounded deployment, exact numerical references and actionable unsupported/failure responses.',
        'evidence':[ref(BASE/'author-review.json','Full criterion review'),ref(BASE/'source-audit.json','Inspected originals'),
                    ref(BASE/'wire-examples.json','Schema and context examples'),ref(BASE/'reproduction-review.json','Ten exact comparisons'),binding]}]
    write(BASE/(OP+'.receipt.json'),receipt)
    print(json.dumps({'published':state['reader'],'receipt':str((BASE/(OP+'.receipt.json')).relative_to(ROOT))}))


if __name__=='__main__':
    main()

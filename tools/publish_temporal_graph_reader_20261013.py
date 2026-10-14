#!/usr/bin/env python3
"""Bind the reviewed temporal argument and preserving reader; no capability promotion."""
import json
from pathlib import Path
import build_integrated_monograph_v12 as shared
import master_control as core
import run_program as run

ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-13/temporal-graphs'
OUT=BASE/'reader'
OP='SCI.ARGUMENT.R04S'
ref=shared.ref


def write(p,v):
    if p.exists():raise ValueError('Preserve recorded evidence: '+str(p))
    core.write(p,v)


def main():
    state=core.read(ROOT,core.STATE);before=core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active']['operation']==OP
    assert state['reader']['path']=='docs/causal_proposal_native_forest_2026-10-13.pdf'
    report=json.loads((OUT/'build-report.json').read_text());audit=json.loads((OUT/'source-audit.json').read_text())
    for p in [BASE/'source-audit.json',BASE/'prepared-inputs.json',BASE/'argument-author-review.json',BASE/'reproduction-review.json',OUT/'source-audit.json']:
        shared.verify_refs(json.loads(p.read_text()))
    bounds=json.loads((OUT/'text-layout-review.json').read_text())
    assert bounds['status']=='pass' and bounds['pages']==report['pages']
    assert not any('Overfull' in w or 'undefined' in w for w in report['warnings'])
    pages=(OUT/'reader.txt').read_text().split('\f')
    first=next(i for i,p in enumerate(pages) if 'A bank can observe a stable association' in p)
    last=next(i for i in range(first,len(pages)) if 'next bounded public/generated experiment' in ' '.join(pages[i].split()))
    body='\n'.join(pages[first:last+1])
    for term in ['14,400','9950','240','Cauchy','independent experimental episodes','whole line']:
        assert term in body,term
    write(BASE/'chapter-text-review.json',{'status':'pass','scope':'Text, citations and physical bounds; not visual acceptance',
        'pdf':report['pdf'],'physical_pages':list(range(first+1,last+2)),
        'page_word_counts':[len(p.split()) for p in pages[first:last+1]],
        'findings':['Continuous-lag construction, sample-cost limit, moment topology, Gaussian experiment and planning example survive extraction.',
                    'Whole-reader citations and labels resolve; no overfull text or physical-bound failures.'],
        'visual_acceptance':False})
    write(BASE/'release-source-review.json',{'status':'pass','issues':[],
        'scope':'Restricted mathematical argument and source/claim integration, not empirical qualification',
        'evidence':[ref(BASE/'argument-author-review.json','Proof and scope review'),ref(BASE/'source-audit.json','Project and predecessor identities'),
                    ref(BASE/'chapter-text-review.json','Compiled argument extraction')],
        'visual_acceptance':False})
    arg=ROOT/'docs/program/comprehensive-v14/work/SCI.ARGUMENT.R04S/argument-and-counterexamples.md'
    inputs=[arg]+[BASE/p for p in ['source-audit.json','argument-author-review.json','reproduction-review.json',
        'oracle-results.json','plan-review.md','chapter.md','chapter-copyedit.md','layout-repair.json',
        'chapter-text-review.json','release-source-review.json','prepared-inputs.json','refs.bib']]+[
        ROOT/'tools/temporal_graph_oracles_20261013.py',ROOT/'tools/review_temporal_graph_oracles_20261013.py',
        ROOT/'tools/prepare_temporal_graph_argument_20261013.py',ROOT/'tools/build_temporal_graph_reader_20261013.py',Path(__file__)]
    release={'kind':'working_monograph','final_acceptance':False,'pdf':report['pdf'],'pages':report['pages'],
        'supersedes':{k:state['reader'][k] for k in ['path','sha256']},
        'build_report':ref(OUT/'build-report.json','Compiled temporal-information successor'),
        'source_review':ref(BASE/'release-source-review.json','Reviewed proof/source integration'),
        'text_layout':ref(OUT/'text-layout-review.json','Whole-reader text and physical bounds'),
        'source_artifacts':audit['tex_files']+[ref(p,'Reviewed argument/reference source') for p in inputs],
        'visual_acceptance':False,'mandatory_repairs_closed':[],
        'changes':['Derived a restricted continuous unknown-lag confidence region with explicit conservative sample cost.',
                   'Added exact moment-set, input-enclosure and all-real-effect observational-equivalence references.',
                   'Specified a separating direct-action experiment and finite planning interval; no new empirical results.'],
        'sponsor_binding':'Prior sponsor remains tied to its historical reader; Q5 coherence is open.'}
    path=BASE/'working-release.json';write(path,release);binding=ref(path,'Reviewed temporal-information working reader')
    run.ledger.validate_working_release(ROOT,binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader']={k:report['pdf'][k] for k in ['path','sha256']}
    state['reader'].update(pages=report['pages'],status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT,before,state,{'action':'publish_temporal_information_working_reader','manifest':binding,
                                 'original_gap_qualification':False,'final_acceptance':False})
    graph,_,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP);receipt=run.ledger.receipt_template(node)
    receipt.update(outcome='pass',execution='performed',scope='Restricted Gaussian continuous-lag confidence argument, certified-enclosure route, equal-law counterexample and separating experiment',
        reviewer={'name':'Current author/coordinator','kind':'author'},
        limitations=['No full unknown-lag-matrix, latent-state, non-Gaussian or heterogeneous-effect solution.',
                     'Conservative relative-variance construction may require far more data than useful alternatives.',
                     'Input-error envelope and scientific assumptions are substantive prerequisites.',
                     'No final statistical study, bank evidence, full R04S qualification or rendered acceptance.'],
        outputs=[ref(arg,'Reviewed argument and counterexamples')],nonexecution_reason='',revisit_trigger='')
    receipt['criteria']=[
        {'index':0,'verdict':'pass','finding':'Exact observation and structural law, current-action target and continuous-lag coverage argument supplied; finite-lag and whole-line predecessor limitations retained.',
         'evidence':[ref(BASE/'argument-author-review.json','Full proof/scope review'),ref(BASE/'source-audit.json','Predecessor and new project evidence'),binding]},
        {'index':1,'verdict':'pass','finding':'Derived feasible region and rational continuum outer bounds, proved an all-real-effect equal-law witness and direct-action information route; exact checks pass without original-gap closure.',
         'evidence':[ref(arg,'Proof and information requirements'),ref(BASE/'reproduction-review.json','Independent exact verification'),ref(BASE/'oracle-results.json','No-random-draw references')]}]
    write(BASE/(OP+'.receipt.json'),receipt)
    print(json.dumps({'published':state['reader'],'receipt':str((BASE/(OP+'.receipt.json')).relative_to(ROOT))}))


if __name__=='__main__':main()

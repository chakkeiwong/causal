#!/usr/bin/env python3
"""Review and publish the preserving longitudinal-regime reader successor."""
import argparse
import json
from pathlib import Path

import build_ltmle_reader_20261023 as build
import run_program_checkpoint_v3 as controller
from review_publish_observations_v2_20261022 import contexts
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

run=controller.base
core,ROOT,BASE,OUT=run.core,build.ROOT,build.BASE,build.OUT
read=lambda p:json.loads(p.read_text())
REVIEWER=dict(name='Codex author/coordinator',kind='author')
LIMITS=['Author source, arithmetic and rendered-text review; visual and independent acceptance remain open.',
    'Native package/dependency qualification and a specific GPL distribution assessment remain future work.',
    'Stipulated risks, costs and influence pairs are mathematical examples, not bank outcomes or backend execution.',
    'Coverage, Q1/Q5 and mandatory repairs remain open.']


def verify():
    for n in ['prepared-inputs.json','source-audit.json','plan-review.json','mathematical-review.json',
        'copyedit-review.json','traceability-review.json','reader/source-audit.json','reader/build-report.json','reader/text-layout-review.json']:
        verify_bindings(read(BASE/n))
    prepared,report,audit,index,bounds=[read(BASE/n) for n in ['prepared-inputs.json','reader/build-report.json',
        'reader/source-audit.json','traceability-review.json','reader/text-layout-review.json']]
    assert index['status']==bounds['status']=='pass' and not index['issues']
    assert report['cited_records']==prepared['expected_cited_records']==948
    assert index['scholarly_pdfs']==prepared['expected_scholarly_pdfs']==223
    assert not bounds['empty_pages'] and not bounds['out_of_bounds']
    assert all('Underfull' in w for w in report['warnings'])
    assert build.DRIVER.read_text()==build.expected_driver()
    assert build.calculate()==read(BASE/'exact-results.json')
    prior=read(build.PRIOR)
    old={s['integrated_citation_key']:s for s in prior['sources']}
    new={s['integrated_citation_key']:s for s in audit['sources']}
    assert len(old)==prepared['prior_cited_records']==946
    assert all(new[k]==v for k,v in old.items())
    assert new.keys()-old.keys()=={'exec23_ltmle_source','exec23_ltmle_exact'}
    compiled={r['path']:r for r in audit['tex_files']}
    kept=[r for r in prior['tex_files'] if r['path']!=str(build.OLD.relative_to(ROOT))]
    assert all(compiled[r['path']]['sha256']==r['sha256'] for r in kept)
    before=contexts(read(build.PREDECESSOR/'traceability-review.json'))
    after=contexts(index,{str(build.DEVELOPMENT.relative_to(ROOT))})
    assert all(v==after[k] for k,v in before.items())
    pages=[' '.join(p.split()).replace('- ','-').replace('−','-') for p in (OUT/'reader.txt').read_text().split(chr(12))]
    starts=[i for i,p in enumerate(pages) if 'A servicing proposal can compare a fixed contact schedule' in p]
    assert len(starts)==1,starts
    start=starts[0]
    ends=[i for i,p in enumerate(pages) if i>=start and 'package execution and empirical qualification remain distinct evidence.' in p]
    assert len(ends)==1,ends
    end=ends[0]
    text=' '.join(pages[start:end+1])
    tokens=['1.3-0','GPL-2','1/100','2/5','13/60','17/100','7/75','130/3','340/3',
        '43/4020','11/1700','5/7','5/3','7/3','saturated','SuperLearner','effective method']
    assert all(t in text for t in tokens),[t for t in tokens if t not in text]
    return report,dict(preserved_records=len(old),added_records=sorted(new.keys()-old.keys()),
        scholarly_pdfs=223,unchanged_compiled_inputs=len(kept),all_prior_citation_contexts_preserved=True,
        rendered_pages=[start+1,end+1],checked_tokens=tokens,native_execution=False,visual_acceptance=False)


def review():
    assert not (BASE/'release-source-review.json').exists()
    report,checks=verify()
    names=['prepared-inputs.json','source-audit.json','plan-review.json','mathematical-review.json',
        'copyedit-review.json','traceability-review.json','exact-results.json','development.tex',
        'reader/build-report.json','reader/source-audit.json','reader/reader.txt','reader/text-layout-review.json']
    write(BASE/'release-source-review.json',dict(status='pass',issues=[],reviewer=REVIEWER,
        reviewed_reader=report['pdf'],scope='Effective longitudinal variance, policy/censoring targets and covariance; preserving reader review',
        checks=checks,evidence=[ref(BASE/n,'Reviewed preserving integration') for n in names]+[
            ref(build.SOURCE/'review-v2.json','Source review with27 anchors'),ref(build.SOURCE/'failed-draft-1/failure-review.json','Preserved failed draft and repairs'),
            ref(Path(__file__),'Exact-reader review')],
        findings=['All946 prior source identities, citation contexts and compiled content inputs survive.',
            'Eleven authenticated originals support pinned identity, effective variance, cluster and warning behavior.',
            'Every binary history is valid; enumeration and moment identities agree; censoring and covariance checks preserve targets.',
            'The example risk and cost parameters remain stipulated and justify proposed prototype tests only.'],
        limitations=LIMITS,visual_acceptance=False,final_acceptance=False))
    print(json.dumps(dict(review='pass',pages=report['pages'],checks=checks)))


def publish():
    report,_=verify()
    review_record=read(BASE/'release-source-review.json');verify_bindings(review_record)
    assert review_record['status']=='pass' and not review_record['issues']
    state,digest=core.read(ROOT,core.STATE),core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active'] is None
    assert run.same_reader(state['reader'],ref(build.OLD.with_suffix('.pdf'),'Predecessor'))
    manifest=dict(kind='working_monograph',final_acceptance=False,pdf=report['pdf'],pages=report['pages'],
        supersedes={k:state['reader'][k] for k in ['path','sha256']},
        build_report=ref(OUT/'build-report.json','Preserving build'),source_review=ref(BASE/'release-source-review.json','Author source and mathematical review'),
        text_layout=ref(OUT/'text-layout-review.json','All-page text bounds'),
        source_artifacts=read(OUT/'source-audit.json')['tex_files']+review_record['evidence'],
        changes=['Develop longitudinal regime targets, effective variance and censoring/covariance examples; retain reference-only software disposition.'],
        visual_acceptance=False,mandatory_repairs_closed=[],sponsor_binding='Pair sponsor to exact new reader bytes.')
    write(BASE/'working-release.json',manifest)
    binding=ref(BASE/'working-release.json','Reviewed longitudinal-regime working successor')
    run.ledger.validate_working_release(ROOT,binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader']={k:report['pdf'][k] for k in ['path','sha256']}
    state['reader'].update(pages=report['pages'],status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT,digest,state,dict(action='publish_ltmle_reader',manifest=binding,final_acceptance=False))
    print(json.dumps(dict(published=state['reader'],proposal_accepted=False)))


def renew():
    report,checks=verify()
    binding=ref(BASE/'working-release.json','Exact current reader')
    run.ledger.validate_working_release(ROOT,binding)
    findings=dict(Q2='All946 prior source identities and contexts survive. Eleven authentic originals, actual Git objects and27 anchors support effective ltmle variance, warnings, cluster and license claims.',
        Q3='All16 binary history risks lie in[1/100,2/5]. Exact enumeration and independent moments give risks13/60,17/100,7/75; censoring population identity and shared covariance calculations replay exactly. Failed draft is preserved.',
        Q4='Explicit assumed default and contact costs give net0,130/3,340/3USD per account under three stipulated rules. These are proposed trial targets, with no native package output or bank return claim.')
    for q,finding in findings.items():
        op='PROPOSAL.'+q;state=core.read(ROOT,core.STATE)
        assert run.same_reader(state['reader'],report['pdf'])
        previous=state['execution_runtime']['results'][op];old=core.read(ROOT,previous['path'])
        assert old.get('reviewed_reader',{}).get('sha256')!=report['pdf']['sha256']
        folder=BASE/q;folder.mkdir(exist_ok=False)
        evidence=[previous,binding,ref(BASE/'release-source-review.json','Preserving author review'),ref(BASE/'source-audit.json','Source audit'),
            ref(BASE/'mathematical-review.json','Exact validated finite law'),ref(Path(__file__),'Exact-reader author delta')]
        write(folder/'reopen.json',dict(reason='Changed reader requires source, arithmetic and economic delta review.',
            prior_result=previous,reviewed_reader=report['pdf'],evidence=evidence,next_action='Record bounded exact-reader review.'))
        transition('reopen',op,folder/'reopen.json')
        state=core.read(ROOT,core.STATE);graph,_,_=run.combined(ROOT,state)
        node=next(n for n in graph['nodes'] if n['id']==op)
        attempt=len(state['execution_runtime']['review_history'][op])
        output=ROOT/run.review_output_paths(node,state['reader'],attempt)[0]
        limits=list(dict.fromkeys(old['limitations']+LIMITS))
        scope='Author exact-reader longitudinal delta review; proposal only'
        write(output,dict(operation=op,status='pass',criterion=node['criteria'][0],reviewer=REVIEWER,
            reviewed_reader=report['pdf'],review_attempt=attempt,acceptance_scope='proposal_only',scope=scope,
            findings=[finding],evidence=evidence,limitations=limits,visual_acceptance=False))
        receipt=run.ledger.receipt_template(node)
        receipt.update(outcome='pass',execution='performed',scope=scope,reviewer=REVIEWER,limitations=limits,
            reviewed_reader=report['pdf'],review_attempt=attempt,acceptance_scope='proposal_only',outputs=[ref(output,'Exact-reader review')],
            nonexecution_reason='',revisit_trigger='',criteria=[dict(index=0,verdict='pass',finding=finding,evidence=evidence)])
        write(folder/'operation-receipt.json',receipt)
        transition('record',op,folder/'operation-receipt.json')
    print(json.dumps(dict(exact_reader_reviews='Q2-Q4 pass',Q1_Q5='open',proposal_accepted=False)))


if __name__=='__main__':
    commands=dict(review=review,publish=publish,renew=renew)
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=commands)
    commands[parser.parse_args().command]()

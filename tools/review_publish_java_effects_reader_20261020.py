#!/usr/bin/env python3
"""Preserve, review and publish the Java-effect proposal successor."""
import argparse
import json
from collections import Counter
from pathlib import Path
import build_java_effects_reader_20261020 as build
import java_effect_reference_20261020 as exact
import run_program_reviews_v2 as extension
from review_java_effects_20261020 import LIMITS as SOURCE_LIMITS
from publish_latent_r_review_v2_20261013 import ref,transition,verify_bindings,write

run=extension.base;core=run.core
ROOT,BASE,OUT=build.ROOT,build.BASE,build.OUT
REVIEWER=dict(name='Codex author/coordinator',kind='author')
LIMITS=SOURCE_LIMITS+['Mandatory repairs, Q1/Q5 and final acceptance remain open.']
read=lambda p:json.loads(p.read_text())


def contexts(index,excluded=()):
    return {r['citation_key']:Counter(json.dumps(c,sort_keys=True) for c in r['citation_contexts']
        if c['path'] not in excluded) for r in index['records']}


def verify():
    for n in ['prepared-inputs.json','source-audit.json','plan-review.json','review.json',
              'mathematical-review.json','copyedit-review.json','manuscript-plan-review.json',
              'traceability-review.json','reader/source-audit.json','reader/build-report.json']:
        verify_bindings(read(BASE/n))
    prepared,report,audit,index=[read(BASE/n) for n in ['prepared-inputs.json',
        'reader/build-report.json','reader/source-audit.json','traceability-review.json']]
    assert report['cited_records']==prepared['expected_cited_records']
    assert index['status']=='pass' and not index['issues']
    assert index['scholarly_pdfs']==prepared['expected_scholarly_pdfs']
    bounds=read(OUT/'text-layout-review.json')
    assert bounds['status']=='pass' and not bounds['empty_pages'] and not bounds['out_of_bounds']
    assert all('Underfull' in w for w in report['warnings'])
    assert build.DRIVER.read_text()==build.expected_driver()
    assert exact.calculate()==read(BASE/'exact-results.json')
    prior=read(build.PRIOR)
    old={s['integrated_citation_key']:s for s in prior['sources']}
    new={s['integrated_citation_key']:s for s in audit['sources']}
    assert len(old)==prepared['prior_cited_records'] and all(new[k]==v for k,v in old.items())
    assert new.keys()-old.keys()=={s['integrated_citation_key'] for s in read(BASE/'source-audit.json')['sources']}
    compiled={r['path']:r for r in audit['tex_files']}
    kept=[r for r in prior['tex_files'] if r['path']!=str(build.OLD.relative_to(ROOT))]
    assert all(compiled[r['path']]['sha256']==r['sha256'] for r in kept)
    before=contexts(read(build.PREDECESSOR/'traceability-review.json'))
    after=contexts(index,{str(build.DEVELOPMENT.relative_to(ROOT))})
    assert all(c==after[k] for k,c in before.items())
    pages=[' '.join(p.split()) for p in (OUT/'reader.txt').read_text().split(chr(12))]
    starts=[i for i,p in enumerate(pages) if 'A servicing team may wish to rank customers by the incremental benefit' in p]
    assert len(starts)==1
    start=starts[0]
    ends=[i for i,p in enumerate(pages) if i>=start and 'unsupported causal guarantee' in p]
    assert len(ends)==1
    end=ends[0];text=' '.join(pages[start:end+1])
    for token in ['17/25','H2O','CStaR','MOJO','PCER','USD 16','USD 30','cross-validation']:
        assert token in text,token
    equations={k:report['added_anchors'][k]['number'] for k in
        ['exec20:javafx-cate','exec20:javafx-confounding','exec20:javafx-smoothing','exec20:javafx-curves']}
    assert all('('+n+')' in text for n in equations.values())
    return report,dict(preserved_records=len(old),added_records=sorted(new.keys()-old.keys()),
        unchanged_compiled_inputs=len(kept),all_prior_citation_contexts_preserved=True,
        physical_pages=[start+1,end+1],equations=equations,visual_acceptance=False,native_execution=False)


def review():
    report,checks=verify()
    names=['prepared-inputs.json','source-audit.json','plan-review.json','review.json',
        'mathematical-review.json','copyedit-review.json','manuscript-plan-review.json',
        'traceability-review.json','exact-results.json','development.tex','reader/build-report.json',
        'reader/source-audit.json','reader/reader.txt','reader/text-layout-review.json']
    write(BASE/'release-source-review.json',dict(status='pass',issues=[],reviewer=REVIEWER,
        reviewed_reader=report['pdf'],scope='Preserving Java effects source review',checks=checks,
        evidence=[ref(BASE/n,'Reviewed Java delta') for n in names]+[ref(Path(__file__),'Exact preservation checks')],
        findings=['All earlier citation identities, contexts and compiled content inputs survive.',
            '28 authenticated blobs support two Java profiles; unchanged IDA scope is explicitly reused.',
            'Uplift targets, score averages, ranking, signed graph effects and proposed worker contracts are integrated.',
            'Exact confounding, smoothing, population, KL-expression and graph-ranking references reproduce.',
            'Static discrepancies remain native reconciliation obligations; complete coverage and native admission remain open.'],
        limitations=LIMITS,visual_acceptance=False,final_acceptance=False))
    print(json.dumps(dict(review='pass',pages=report['pages'],checks=checks)))


def publish():
    report,_=verify();review_record=read(BASE/'release-source-review.json');verify_bindings(review_record)
    state=core.read(ROOT,core.STATE);before=core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path']==str(build.OLD.with_suffix('.pdf').relative_to(ROOT))
    manifest=dict(kind='working_monograph',final_acceptance=False,pdf=report['pdf'],pages=report['pages'],
        supersedes={k:state['reader'][k] for k in ['path','sha256']},
        build_report=ref(OUT/'build-report.json','Preserving Java effects build'),
        source_review=ref(BASE/'release-source-review.json','Source, arithmetic and preservation review'),
        text_layout=ref(OUT/'text-layout-review.json','All-page text bounds'),
        source_artifacts=read(OUT/'source-audit.json')['tex_files']+review_record['evidence'],
        changes=['Integrate selected H2O/Tetrad effect semantics and exact public qualification references.'],
        visual_acceptance=False,mandatory_repairs_closed=[],sponsor_binding='Pair sponsor to exact reader bytes.')
    write(BASE/'working-release.json',manifest)
    binding=ref(BASE/'working-release.json','Reviewed Java effects working reader')
    run.ledger.validate_working_release(ROOT,binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader']={k:report['pdf'][k] for k in ['path','sha256']}
    state['reader'].update(pages=report['pages'],status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT,before,state,dict(action='publish_java_effects_reader',manifest=binding,final_acceptance=False))
    print(json.dumps(dict(published=state['reader'],proposal_accepted=False)))


def renew():
    report,checks=verify();binding=ref(BASE/'working-release.json','Exact current reader')
    run.ledger.validate_working_release(ROOT,binding)
    findings={
        'Q2':'All earlier citation identities and contexts survive. Two Java profiles bind28 blobs and immutable pre-cutoff trees. Later search metadata remains unread discovery; unchanged IDA is not double counted.',
        'Q3':'Confounding9/25 versus causal0, smoothing1/2 versus3/5, retained-row means, fixed-bin qini2/3, literal KL-1 versus0 and signed-minimum/tie references reproduce. No native or general coverage guarantee follows.',
        'Q4':'Assumed confounded margins16/-20, smoothed10 versus raw20, and signed graph margins-220/-70 versus invalid positive30 show decision consequences. Worker qualification, full rights, costs and bank return remain unmeasured.'}
    for q,finding in findings.items():
        identifier='PROPOSAL.'+q;state=core.read(ROOT,core.STATE)
        assert run.same_reader(state['reader'],report['pdf'])
        previous=state['execution_runtime']['results'][identifier];old=core.read(ROOT,previous['path'])
        if old.get('reviewed_reader',{}).get('sha256')==report['pdf']['sha256']:continue
        folder=BASE/q;folder.mkdir(exist_ok=False)
        evidence=[previous,binding,ref(BASE/'release-source-review.json','Preserving author review'),
            ref(BASE/'source-audit.json','Authenticated originals'),ref(BASE/'mathematical-review.json','Exact references'),
            ref(Path(__file__),'Exact-reader review')]
        write(folder/'reopen.json',dict(reason='Changed reader requires preserving delta review.',prior_result=previous,
            reviewed_reader=report['pdf'],evidence=evidence,next_action='Record Java-effects source, mathematical and economic delta.'))
        transition('reopen',identifier,folder/'reopen.json')
        state=core.read(ROOT,core.STATE);graph,_,_=run.combined(ROOT,state);node=run.ledger.operation(graph,identifier)
        attempt=len(state['execution_runtime']['review_history'][identifier]);output=ROOT/run.review_output_paths(node,state['reader'],attempt)[0]
        limits=list(dict.fromkeys(old['limitations']+LIMITS));scope='Author exact-reader delta review; proposal evidence only'
        write(output,dict(operation=identifier,status='pass',criterion=node['criteria'][0],reviewer=REVIEWER,
            reviewed_reader=report['pdf'],review_attempt=attempt,acceptance_scope='proposal_only',scope=scope,
            findings=[finding],evidence=evidence,limitations=limits,visual_acceptance=False))
        receipt=run.ledger.receipt_template(node)
        receipt.update(outcome='pass',execution='performed',scope=scope,reviewer=REVIEWER,limitations=limits,
            reviewed_reader=report['pdf'],review_attempt=attempt,acceptance_scope='proposal_only',
            outputs=[ref(output,'Exact-reader '+q+' review')],nonexecution_reason='',revisit_trigger='',
            criteria=[dict(index=0,verdict='pass',finding=finding,evidence=evidence)])
        write(folder/'operation-receipt.json',receipt);transition('record',identifier,folder/'operation-receipt.json')
    print(json.dumps(dict(exact_reader_reviews='Q2-Q4 pass',Q1_Q5='open',proposal_accepted=False)))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['review','publish','renew'])
    globals()[parser.parse_args().command]()

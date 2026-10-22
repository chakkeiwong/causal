#!/usr/bin/env python3
"""Review preserved content and publish a precisely scoped R IV/RD delta."""
import argparse
from collections import Counter
import json
from pathlib import Path
import build_r_iv_rd_reader_20261022 as build
import r_iv_rd_reference_20261022 as exact
from review_r_iv_rd_20261022 import BASE, ROOT, run, core, LIMITS, REVIEWER
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

OUT=build.OUT
read=lambda p:json.loads(p.read_text())
NAMES=['prepared-inputs.json','source-audit.json','inherited-source-review.json','plan-review.json','review.json',
    'conversion-contract.json','mathematical-review.json','copyedit-review.json','manuscript-plan-review.json',
    'traceability-review.json','reader/source-audit.json','reader/build-report.json']


def contexts(index,exclude=()):
    return {r['citation_key']:Counter(json.dumps(c,sort_keys=True) for c in r['citation_contexts'] if c['path'] not in exclude) for r in index['records']}


def verify():
    for n in NAMES:verify_bindings(read(BASE/n))
    prepared,report,audit,index=[read(BASE/n) for n in ['prepared-inputs.json','reader/build-report.json','reader/source-audit.json','traceability-review.json']]
    assert report['cited_records']==prepared['expected_cited_records']
    assert index['status']=='pass' and not index['issues']
    assert index['scholarly_pdfs']==prepared['expected_scholarly_pdfs']
    bounds=read(OUT/'text-layout-review.json')
    assert bounds['status']=='pass' and not bounds['empty_pages'] and not bounds['out_of_bounds']
    assert all('Underfull' in w for w in report['warnings'])
    assert build.DRIVER.read_text()==build.expected_driver()
    assert exact.calculate()==read(BASE/'exact-results.json')
    prior=read(build.PRIOR);before={s['integrated_citation_key']:s for s in prior['sources']}
    after={s['integrated_citation_key']:s for s in audit['sources']}
    assert all(after[k]==v for k,v in before.items())
    assert after.keys()-before.keys()=={s['integrated_citation_key'] for s in read(BASE/'source-audit.json')['sources']}
    kept=[r for r in prior['tex_files'] if r['path']!=str(build.OLD.relative_to(ROOT))]
    compiled={r['path']:r for r in audit['tex_files']}
    assert all(compiled[r['path']]['sha256']==r['sha256'] for r in kept)
    old_contexts=contexts(read(build.PREDECESSOR/'traceability-review.json'))
    new_contexts=contexts(index,{str(build.DEVELOPMENT.relative_to(ROOT))})
    assert all(v==new_contexts[k] for k,v in old_contexts.items())
    # Recheck the actual inspected snippets, using the same newline convention as nl/sed.
    count=0
    for s in read(BASE/'source-audit.json')['sources']:
        for r in s.get('records',[])+([s['description']] if 'description' in s else []):
            lines=(ROOT/r['local_copy']['path']).read_text().split('\n')
            for a in r['inspected_anchors']:
                assert a['inspected_text']=='\n'.join(lines[a['line_start']-1:a['line_end']]);count+=1
    pages=[' '.join(p.split()) for p in (OUT/'reader.txt').read_text().split(chr(12))]
    starts=[i for i,p in enumerate(pages) if 'A credit eligibility threshold can change access' in p];assert len(starts)==1
    start=starts[0]
    ends=[i for i,p in enumerate(pages) if i>=start and 'an expensive experiment with bank data' in p];assert len(ends)==1
    end=ends[0];text=' '.join(pages[start:end+1])
    for token in ['23:20:02','15:59:59','USD 190','USD 130','0.9545','twenty-allocation','CLR','MIT','HC3']:
        assert token in text,token
    labels=['late','population','value','gaussian','set','topology','support','bound']
    equations={label:report['added_anchors']['exec22:riv-'+label]['number'] for label in labels}
    assert all('('+n+')' in text for n in equations.values())
    return report,dict(preserved_records=len(before),added_records=len(after)-len(before),
        unchanged_compiled_inputs=len(kept),all_prior_citation_contexts_preserved=True,
        checked_newline_anchors=count,physical_pages=[start+1,end+1],equations=equations,
        visual_acceptance=False,native_execution=False)


def review():
    report,checks=verify()
    evidence=[ref(BASE/n,'Reviewed preservation and scientific evidence') for n in NAMES+['exact-results.json','development.tex','reader/reader.txt','reader/text-layout-review.json']]
    evidence.append(ref(Path(__file__),'Preservation, equation and anchor checks'))
    write(BASE/'release-source-review.json',dict(status='pass',issues=[],reviewer=REVIEWER,
        reviewed_reader=report['pdf'],checks=checks,evidence=evidence,
        findings=['Nine added audit records bind six package profiles, two license texts and one exact authored reference.',
            'All predecessor identities, citation contexts and content inputs are preserved.',
            'IV targets, weak-set topology, discrete-score limits, randomization law and numerical failure paths are developed.',
            'Five reference decisions with no runtime admission coexist with inconclusive overall R coverage.'],
        limitations=LIMITS,visual_acceptance=False,final_acceptance=False))
    print(json.dumps(dict(review='pass',pages=report['pages'],checks=checks)))


def publish():
    report,checks=verify();review_record=read(BASE/'release-source-review.json');verify_bindings(review_record)
    state=core.read(ROOT,core.STATE);before=core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path']==str(build.OLD.with_suffix('.pdf').relative_to(ROOT))
    for n in range(50,55):assert state['execution_program']['results'][f'SW.DECISION.seed_{n:03d}']['outcome']=='pass'
    manifest=dict(kind='working_monograph',final_acceptance=False,pdf=report['pdf'],pages=report['pages'],
        supersedes={k:state['reader'][k] for k in ['path','sha256']},
        build_report=ref(OUT/'build-report.json','Preserving compiled successor'),
        source_review=ref(BASE/'release-source-review.json','Primary sources, argument and preservation'),
        text_layout=ref(OUT/'text-layout-review.json','All-page text bounds'),
        source_artifacts=read(OUT/'source-audit.json')['tex_files']+review_record['evidence'],
        changes=['Integrate six R IV/RD package profiles, five reference-only reuse choices and exact credit-design examples.'],
        visual_acceptance=False,mandatory_repairs_closed=[],sponsor_binding='Pair sponsor successor to exact reader bytes.')
    write(BASE/'working-release.json',manifest);binding=ref(BASE/'working-release.json','Reviewed R IV/RD working successor')
    run.ledger.validate_working_release(ROOT,binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader']={k:report['pdf'][k] for k in ['path','sha256']}
    state['reader'].update(pages=report['pages'],status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT,before,state,dict(action='publish_r_iv_rd_reader',manifest=binding,final_acceptance=False))
    print(json.dumps(dict(published=state['reader'],proposal_accepted=False)))


def renew():
    report,checks=verify();binding=ref(BASE/'working-release.json','Exact current reader')
    findings={
      'Q2':'All896 earlier source identities and citation contexts survive. Six pinned package profiles have authentic technical bytes, declared dependencies, blob/SHA checks and newline-consistent anchors. Two rights texts and one exact reference add nine records; CRAN4.1.1 publication is after the precise cutoff. Nine discovery leads and transitive rights remain open.',
      'Q3':'Exact finite laws reproduce LATE-150/ATE-70/ITT-60 and violations-200/-250; Gaussian quadratic inversion preserves two rays, bounded and whole-line sets at declared95.45% model coverage. Two continuous laws agree on integer observations but differ at cutoff; declared Lipschitz bounds and twenty-allocation sharp-null p=.1 reproduce. No native run or empirical coverage is claimed.',
      'Q4':'Hypothetical treatment cost100 and encouragement cost10 give margins50,-30,10USD for different targets; discrete-score uncertainty gives margin[-10,30]USD. Original R workers and public studies are conditional recommendations; no measured costs, licensed access or bank return is claimed.'}
    for q,finding in findings.items():
        identifier='PROPOSAL.'+q;state=core.read(ROOT,core.STATE)
        assert run.same_reader(state['reader'],report['pdf'])
        previous=state['execution_runtime']['results'][identifier];old=core.read(ROOT,previous['path'])
        if old.get('reviewed_reader',{}).get('sha256')==report['pdf']['sha256']:continue
        folder=BASE/q;folder.mkdir(exist_ok=False)
        evidence=[previous,binding,ref(BASE/'release-source-review.json','Preserving author review'),
            ref(BASE/'source-audit.json','Pinned original evidence'),ref(BASE/'mathematical-review.json','Exact authored arguments'),ref(Path(__file__),'Exact-reader delta checks')]
        write(folder/'reopen.json',dict(reason='Changed reader requires preserving delta review.',prior_result=previous,
            reviewed_reader=report['pdf'],evidence=evidence,next_action='Record R IV/RD source, reference and economic delta.'))
        transition('reopen',identifier,folder/'reopen.json')
        state=core.read(ROOT,core.STATE);graph,_,_=run.combined(ROOT,state);node=run.ledger.operation(graph,identifier)
        attempt=len(state['execution_runtime']['review_history'][identifier]);output=ROOT/run.review_output_paths(node,state['reader'],attempt)[0]
        limits=list(dict.fromkeys(old['limitations']+LIMITS));scope='Author exact-reader preserving delta review; proposal evidence only'
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
    commands=dict(review=review,publish=publish,renew=renew)
    p=argparse.ArgumentParser();p.add_argument('command',choices=commands)
    commands[p.parse_args().command]()

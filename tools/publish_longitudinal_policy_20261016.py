#!/usr/bin/env python3
"""Review, record and publish the preserving longitudinal proposal successor."""
import argparse
from collections import Counter
import json
from pathlib import Path
import build_longitudinal_policy_reader_20261016 as build
import review_longitudinal_policy_20261016 as work
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

ROOT, BASE, OUT, WORK = build.ROOT, build.BASE, build.OUT, build.WORK


def review():
    report = json.loads((OUT/'build-report.json').read_text())
    audit = json.loads((OUT/'source-audit.json').read_text())
    prior = json.loads(build.PRIOR.read_text())
    index = json.loads((BASE/'traceability-review.json').read_text())
    for obj in [report, audit, prior, index, json.loads((BASE/'prepared-inputs.json').read_text()),
                json.loads((WORK/'author-review.json').read_text())]: verify_bindings(obj)
    assert index['status'] == 'pass' and not index['issues'] and index['scholarly_pdfs'] == 175
    layout = json.loads((OUT/'text-layout-review.json').read_text())
    assert layout['status'] == 'pass' and not layout['out_of_bounds'] and not layout['empty_pages']
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    assert build.DRIVER.read_text() == build.expected_driver()
    old = {s['integrated_citation_key']: s for s in prior['sources']}
    new = {s['integrated_citation_key']: s for s in audit['sources']}
    assert len(old) == 646 and len(new) == 649 and all(new[k] == s for k, s in old.items())
    files = {r['path']: r for r in audit['tex_files']}
    kept = [r for r in prior['tex_files'] if r['path'] != str(build.OLD.relative_to(ROOT))]
    assert all(files[r['path']]['sha256'] == r['sha256'] for r in kept)
    previous = json.loads((build.PRIOR.parent.parent/'traceability-review.json').read_text())
    contexts = {r['citation_key']: Counter(json.dumps(x, sort_keys=True) for x in r['citation_contexts']) for r in index['records']}
    for row in previous['records']:
        assert not Counter(json.dumps(x, sort_keys=True) for x in row['citation_contexts']) - contexts[row['citation_key']]
    text = ' '.join((OUT/'reader.txt').read_text().split())
    for phrase in ['From language-assisted collaboration to adaptive servicing',
                   'conditional version mixture', '0.188', '0.353', '0.216', '0.219',
                   'cannot be redistributed', '87.6', '0.663910',
                   'not an observed output of CausalCollab',
                   'Twenty-two original blobs', '2,500', 'UCI']:
        assert phrase in text, phrase
    assert work.exact() == json.loads((WORK/'exact-results.json').read_text())
    evidence = [ref(p, a) for p, a in [
        (OUT/'build-report.json','Preserving longitudinal reader'),
        (OUT/'source-audit.json','649 source records'),
        (BASE/'traceability-review.json','175 genuine scholarly PDFs and retained contexts'),
        (OUT/'text-layout-review.json','All-page text bounds'),
        (OUT/'reader.txt','Inspected integrated argument and exact figures'),
        (WORK/'source-review.json','Six primary papers and22 verified original source blobs'),
        (WORK/'exact-results.json','Exact authored version,feedback,locality,support,clock and loop references'),
        (WORK/'independent-arithmetic-review.json','Enumeration versus independent formulas'),
        (WORK/'proposed-contract.json','Proposed remedies,CLI/MCP and public-evidence design'),
        (WORK/'omissions-register.json','Candidate122,search noise,rights and research gaps'),
        (WORK/'author-review.json','Criterion-specific author review'),
        (WORK/'authoring-failure.json','Tool error and extraction warning retained'),
        (work.OUTPUT,'Reviewed task synthesis'), (Path(__file__),'Exact-reader review and transitions')]]
    write(BASE/'release-source-review.json', {
        'status':'pass','issues':[],'reviewer':work.REVIEWER,'reviewed_reader':report['pdf'],
        'scope':'Author primary-source,exact arithmetic and extracted-text review;proposal synthesis only',
        'preserved_records':646,'new_records':3,'preserved_compiled_sources':len(kept),
        'original_contexts_retained':True,'evidence':evidence,
        'findings': [
            'CausalCollab target,conditional version mixture,adverse/favorable MSE,limits and data terms are distinguished from bank dynamic policy value.',
            'Twenty-two pinned originals trace actual default dispatch,representation loss,last-state sampling and output;no upstream execution asserted.',
            'Independent arithmetic preserves histories,finite action meaning and support;the7.2USD feedback gap is authored,not a reported upstream result.',
            'Concrete engineering routes and public/generated evidence proceed despite missing rights/originals;general causal identification and uncertainty remain conditional.'
        ],'limitations':work.LIMITS,'visual_acceptance':False})
    print(json.dumps({'review':'pass','pages':report['pages'],'sections':report['longitudinal_sections']}))


def record():
    reviewed = json.loads((BASE/'release-source-review.json').read_text()); verify_bindings(reviewed)
    author = json.loads((WORK/'author-review.json').read_text())
    state = core.read(ROOT, core.STATE); graph, _, _ = run.combined(ROOT, state)
    node = run.ledger.operation(graph, work.OP)
    receipt = run.ledger.receipt_template(node)
    receipt.update(outcome='pass',execution='performed',
        scope='Bounded longitudinal LLM proposal synthesis;no exhaustive census,live study or integration qualification',
        reviewer=work.REVIEWER,limitations=work.LIMITS,capabilities=[],
        outputs=[ref(work.OUTPUT,'Reviewed longitudinal assistance task synthesis')],
        nonexecution_reason='',
        revisit_trigger='Revisit source coverage when candidate122 original or stronger longitudinal implementation evidence arrives;qualify a permitted public/generated prototype before any integration or bank claim.',
        criteria=[{'index':i,'verdict':'pass','finding':finding,
                   'evidence':[ref(WORK/'author-review.json','Criterion review'),ref(BASE/'release-source-review.json','Preserving integration')]}
                  for i,finding in enumerate(author['findings'])])
    write(BASE/'operation-receipt.json',receipt)
    transition('record',work.OP,BASE/'operation-receipt.json')


def publish():
    state = core.read(ROOT, core.STATE); before = core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active'] is None and work.OP in state['execution_program']['results']
    assert state['reader']['path'] == str(build.OLD.with_suffix('.pdf').relative_to(ROOT))
    report = json.loads((OUT/'build-report.json').read_text())
    audit = json.loads((OUT/'source-audit.json').read_text())
    reviewed = json.loads((BASE/'release-source-review.json').read_text()); verify_bindings(reviewed)
    manifest = {'kind':'working_monograph','final_acceptance':False,'pdf':report['pdf'],'pages':report['pages'],
        'supersedes':{k:state['reader'][k] for k in ['path','sha256']},
        'build_report':ref(OUT/'build-report.json','Preserving longitudinal reader'),
        'source_review':ref(BASE/'release-source-review.json','Exact-reader author review'),
        'text_layout':ref(OUT/'text-layout-review.json','All-page bounds'),
        'source_artifacts':audit['tex_files']+reviewed['evidence'],
        'visual_acceptance':False,'mandatory_repairs_closed':[],
        'changes':['Connect conditional text-style effects and pinned implementation to dynamic banking policy semantics.',
                   'Develop exact intervention-version,feedback,locality and support examples and a public/generated prototype contract.'],
        'sponsor_binding':'Preserved sponsor baseline;Q5 reconciliation remains open.'}
    write(BASE/'working-release.json',manifest)
    binding=ref(BASE/'working-release.json','Reviewed longitudinal working successor')
    run.ledger.validate_working_release(ROOT,binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader']={k:report['pdf'][k] for k in ['path','sha256']}
    state['reader'].update(pages=report['pages'],status='Working monograph;not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT,before,state,{'action':'publish_longitudinal_policy_reader','manifest':binding,'final_acceptance':False})
    print(json.dumps({'published':state['reader']}))


def renew():
    report=json.loads((OUT/'build-report.json').read_text())
    verify_bindings(json.loads((BASE/'release-source-review.json').read_text()))
    findings={
        'Q2':'All646 inherited source records and citation contexts remain. Three additions bind22 pinned originals,six primary rereads,exact authored references and a proposed contract.649 records and175 genuine scholarly PDFs are traceable;search and rights omissions remain explicit.',
        'Q3':'Exact authored enumeration and independent backward/factorized arithmetic reproduce text-version97/67USD,adaptive94.8 versus fixed-marginal87.6USD,locality,support and clock examples. Static source and literature findings do not claim upstream execution,live-model accuracy or an executed prototype.',
        'Q4':'Stipulated7.2USD feedback and30USD version-mixture differences justify resolving target errors before costly bank experiments. Public credit/mortgage roles,generated controls,full workflow costs and maintenance are explicit;actual prices,realized performance and bank ROI remain unclaimed.'}
    for q,finding in findings.items():
        identifier='PROPOSAL.'+q;state=core.read(ROOT,core.STATE)
        assert state['reader']['sha256']==report['pdf']['sha256']
        previous=state['execution_runtime']['results'][identifier]
        old=json.loads((ROOT/previous['path']).read_text())
        folder=BASE/q;folder.mkdir(exist_ok=False)
        evidence=[previous,ref(BASE/'working-release.json','Exact current reader'),
            ref(BASE/'release-source-review.json','Inspected longitudinal delta'),
            ref(work.OUTPUT,'Task synthesis'),ref(WORK/'independent-arithmetic-review.json','Reproduced illustrative economics'),
            ref(Path(__file__),'Review findings')]
        write(folder/'reopen.json',{'reason':'Changed reader requires preserved successor author review.',
            'prior_result':previous,'reviewed_reader':report['pdf'],'evidence':evidence,
            'next_action':'Record the reviewed longitudinal delta with preserved limits.'})
        transition('reopen',identifier,folder/'reopen.json')
        state=core.read(ROOT,core.STATE);graph,_,_=run.combined(ROOT,state)
        node=run.ledger.operation(graph,identifier)
        attempt=len(state['execution_runtime']['review_history'][identifier])
        output=ROOT/run.review_output_paths(node,state['reader'],attempt)[0]
        limits=list(dict.fromkeys(old['limitations']+work.LIMITS));scope='Author exact-reader proposal delta review'
        write(output,{'operation':identifier,'status':'pass','criterion':node['criteria'][0],
            'reviewer':work.REVIEWER,'reviewed_reader':report['pdf'],'review_attempt':attempt,
            'acceptance_scope':'proposal_only','scope':scope,'findings':[finding],'evidence':evidence,
            'limitations':limits,'visual_acceptance':False})
        receipt=run.ledger.receipt_template(node)
        receipt.update(outcome='pass',execution='performed',scope=scope,reviewer=work.REVIEWER,
            limitations=limits,reviewed_reader=report['pdf'],review_attempt=attempt,acceptance_scope='proposal_only',
            outputs=[ref(output,'Current-reader '+q+' author review')],nonexecution_reason='',revisit_trigger='',
            criteria=[{'index':0,'verdict':'pass','finding':finding,'evidence':evidence}])
        write(folder/'operation-receipt.json',receipt)
        transition('record',identifier,folder/'operation-receipt.json')
    print(json.dumps({'exact_reader_reviews':'Q2-Q4 pass','Q1_Q5':'open'}))


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('command',choices=['review','record','publish','renew'])
    args=p.parse_args()
    {'review':review,'record':record,'publish':publish,'renew':renew}[args.command]()

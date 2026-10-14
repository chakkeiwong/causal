#!/usr/bin/env python3
"""Review and publish the lifecycle addition without inheriting stale reviews."""
import argparse
import json
from pathlib import Path
import re

import build_causalnex_reader_20261014 as build
import master_control as core
import review_causalnex_reuse_20261014 as work
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

ROOT, BASE, OUT = work.ROOT, build.BASE, build.OUT
REVIEWER = work.REVIEWER
LIMITS = ['Author review only; no independent scientific or bank acceptance.',
    'Seven selected primary blobs and exact project algebra; no executed CausalNex engine or qualified environment.',
    'No automatic whole-manuscript depth or mandatory-repair closure; Q1 remains open.',
    'The inherited six-preview allowance is exhausted under /home/ubuntu/AGENTS.md; visual acceptance and Q5 remain open.',
    'No measured maintenance cost, causal performance or bank ROI is inferred.']


def review():
    report = json.loads((OUT/'build-report.json').read_text())
    audit = json.loads((OUT/'source-audit.json').read_text())
    prior = json.loads(build.PRIOR.read_text())
    index = json.loads((BASE/'traceability-review.json').read_text())
    for value in [report, audit, prior, index, json.loads((BASE/'prepared-inputs.json').read_text())]:
        verify_bindings(value)
    assert index['status'] == 'pass' and not index['issues'] and index['scholarly_pdfs'] == 153
    assert json.loads((OUT/'text-layout-review.json').read_text())['status'] == 'pass'
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    old = {s['integrated_citation_key']:s for s in prior['sources']}
    new = {s['integrated_citation_key']:s for s in audit['sources']}
    assert len(old) == 516 and len(new) == 518 and all(new[k] == v for k,v in old.items())
    assert new.keys()-old.keys() == {'exec14_causalnex_primary','exec14_causalnex_oracle'}
    compiled = {r['path']:r for r in audit['tex_files']}
    inherited = [r for r in prior['tex_files'] if r['path'] != str(build.OLD.relative_to(ROOT))]
    assert all(compiled[r['path']]['sha256'] == r['sha256'] for r in inherited)
    previous = json.loads((ROOT/'docs/program/execution/2026-10-14/l5-depth/traceability-review.json').read_text())
    contexts = {r['citation_key']:r['citation_contexts'] for r in index['records']}
    assert all(contexts[r['citation_key']] == r['citation_contexts'] for r in previous['records'])
    assert work.exact() == json.loads((work.BASE/'exact-oracle.json').read_text())
    text = re.sub(r'\s+',' ',(OUT/'reader.txt').read_text())
    for phrase in ['CausalNex: maintenance, graph semantics and reuse', '24 June 2026',
                   'same coefficient', 'no CausalNex runtime qualification', 'conditional archival route']:
        assert phrase.lower() in text.lower(), phrase
    findings = ['The README explicitly states discontinuation, while the later commit declares0.12.2; the earlier access failure is not used as maintenance evidence.',
        'Root Apache/trademark and dependency declarations are reported without asserting solved rights, security or an installed package.',
        'The specified objective, tabu constraints, thresholds, graph cycles/provenance and convergence behavior agree with the inspected primary source.',
        'Rational examples reproduce two distinct equality rules, unit-reversed cycle deletion and unchanged centered moments with changed no-intercept slope. These are imposed mechanisms, not package runs.',
        'Default adoption is rejected; archival conditions, alternatives, ownership, costs and a concrete revisit trigger are stated.',
        'All516 inherited citation records and citation contexts remain unchanged; two new records bind the substantive addition.']
    evidence = [ref(p,anchor) for p,anchor in [
        (OUT/'build-report.json','Exact successor PDF identity and pages'),
        (OUT/'source-audit.json','518 complete citation records'),
        (OUT/'reader.txt','Inspected lifecycle addition and surrounding transitions'),
        (OUT/'text-layout-review.json','All-page extracted text/bounds check'),
        (BASE/'traceability-review.json','Whole-reader citation contexts and153 scholarly PDFs'),
        (BASE/'prepared-inputs.json','Preserved input bindings'),
        (work.BASE/'primary-review.json','Seven inspected primary files and exact version'),
        (work.BASE/'exact-oracle.json','Independent arithmetic'),
        (work.OUTPUT,'Reviewed reuse disposition'),
        (work.BASE/'decision.tex','Integrated scholarly argument'),
        (Path(__file__),'Exact-reader review and publication procedure')]]
    write(BASE/'release-source-review.json',{'status':'pass','issues':[], 'reviewer':REVIEWER,
        'scope':'Exact-reader software lifecycle, graph semantics and reuse delta', 'reviewed_reader':report['pdf'],
        'findings':findings,'evidence':evidence,'unchanged_source_records':516,
        'new_source_records':['exec14_causalnex_primary','exec14_causalnex_oracle'],
        'unchanged_inherited_compiled_sources':len(inherited),'unchanged_inherited_citation_contexts':True,
        'limitations':LIMITS,'visual_acceptance':False,'bank_ROI_established':False})
    print(json.dumps({'review':'pass','pages':report['pages'],'cited_records':518,'visual_acceptance':False}))


def publish():
    state = core.read(ROOT,core.STATE)
    before = core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path'] == str(build.OLD.with_suffix('.pdf').relative_to(ROOT))
    assert 'SW.DECISION.inherited_causalnex' in state['execution_program']['results']
    report = json.loads((OUT/'build-report.json').read_text())
    audit = json.loads((OUT/'source-audit.json').read_text())
    review = json.loads((BASE/'release-source-review.json').read_text())
    verify_bindings(review)
    manifest = {'kind':'working_monograph','final_acceptance':False,'pdf':report['pdf'],'pages':report['pages'],
        'supersedes':{k:state['reader'][k] for k in ['path','sha256']},
        'build_report':ref(OUT/'build-report.json','Compiled preserving software lifecycle addition'),
        'source_review':ref(BASE/'release-source-review.json','Actual content/source/mathematics review'),
        'text_layout':ref(OUT/'text-layout-review.json','Every-page text/bounds check'),
        'source_artifacts':audit['tex_files']+review['evidence'],'visual_acceptance':False,
        'mandatory_repairs_closed':[],
        'changes':['Integrate explicit archival maintenance/dependency decision for CausalNex.',
            'Explain graph/target, preprocessing, pruning, threshold and convergence semantics with exact examples.'],
        'sponsor_binding':'Preserved sponsor baseline; Q5 reconciliation remains open.'}
    write(BASE/'working-release.json',manifest)
    binding=ref(BASE/'working-release.json','Reviewed software lifecycle working reader')
    run.ledger.validate_working_release(ROOT,binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader']={k:report['pdf'][k] for k in ['path','sha256']}
    state['reader'].update(pages=report['pages'],status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT,before,state,{'action':'publish_software_lifecycle_reader','manifest':binding,'final_acceptance':False})
    print(json.dumps({'published':state['reader'],'proposal_accepted':False}))


def renew():
    report=json.loads((OUT/'build-report.json').read_text())
    findings={
        'Q2':'All516 inherited source records, contexts and chapter bytes are preserved; seven primary source blobs and their version/license/dependency/maintenance anchors support the new scoped claims. Two new records yield518 cited records and153 genuine scholarly PDFs.',
        'Q3':'The previous demonstration portfolio and negative findings remain intact. Three new exact mechanisms distinguish threshold equality, unit-dependent pruning and no-intercept translation sensitivity; no upstream optimizer, graph accuracy or interval study is claimed.',
        'Q4':'Earlier investment scenarios are unchanged. Rejection of an unsupported default dependency clarifies ownership, environment and retirement costs without inventing prices. A narrow public/generated-data comparison remains a justified inexpensive step before bank trials.'}
    verify_bindings(json.loads((BASE/'release-source-review.json').read_text()))
    for q,finding in findings.items():
        identifier='PROPOSAL.'+q
        state=core.read(ROOT,core.STATE)
        assert state['reader']['sha256']==report['pdf']['sha256']
        previous=state['execution_runtime']['results'][identifier]
        old=json.loads((ROOT/previous['path']).read_text())
        folder=BASE/q
        folder.mkdir(exist_ok=False)
        evidence=[previous,ref(BASE/'working-release.json','Exact successor working reader'),
            ref(BASE/'release-source-review.json','Reviewed source/mathematics/reuse delta'),
            ref(Path(__file__),'Exact-reader renewal findings')]
        write(folder/'reopen.json',{'reason':'Reader changed; preserve and renew the prior exact-reader review.',
            'prior_result':previous,'reviewed_reader':report['pdf'],'evidence':evidence,
            'next_action':'Record the reviewed software lifecycle addition against the current reader.'})
        transition('reopen',identifier,folder/'reopen.json')
        state=core.read(ROOT,core.STATE)
        graph,_,_=run.combined(ROOT,state)
        node=run.ledger.operation(graph,identifier)
        attempt=len(state['execution_runtime']['review_history'][identifier])
        output=ROOT/run.review_output_paths(node,state['reader'],attempt)[0]
        limits=list(dict.fromkeys(old['limitations']+LIMITS))
        scope='Author exact-reader delta review; proposal evidence only'
        write(output,{'operation':identifier,'status':'pass','criterion':node['criteria'][0],
            'reviewer':REVIEWER,'reviewed_reader':report['pdf'],'review_attempt':attempt,
            'acceptance_scope':'proposal_only','scope':scope,'findings':[finding],
            'evidence':evidence,'limitations':limits,'visual_acceptance':False})
        receipt=run.ledger.receipt_template(node)
        receipt.update(outcome='pass',execution='performed',scope=scope,reviewer=REVIEWER,
            limitations=limits,reviewed_reader=report['pdf'],review_attempt=attempt,
            acceptance_scope='proposal_only',outputs=[ref(output,'Current-reader '+q+' author review')],
            nonexecution_reason='',revisit_trigger='',
            criteria=[{'index':0,'verdict':'pass','finding':finding,'evidence':evidence}])
        write(folder/'operation-receipt.json',receipt)
        transition('record',identifier,folder/'operation-receipt.json')
    print(json.dumps({'exact_reader_reviews':'Q2-Q4 pass','proposal_accepted':False}))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('command',choices=['review','publish','renew'])
    args=parser.parse_args()
    {'review':review,'publish':publish,'renew':renew}[args.command]()

#!/usr/bin/env python3
"""Compare preserved commercial panel evidence without inventing edition closure."""
import json
from pathlib import Path

import run_program_reviews_v2 as extension
import review_commercial_panels_20261018 as prior
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run=extension.base
core=run.core
ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-19/commercial-panel-comparison-v1'
PREVIOUS=ROOT/'docs/program/execution/2026-10-18/commercial-panels'
OP='SW.COMM.panels_did'
OUTPUT=ROOT/f'docs/program/comprehensive-v14/work/{OP}/vendor-comparison.json'
REVIEWER=dict(name='Codex author/coordinator',kind='author')


def read(path):
    return json.loads(path.read_text())


def main():
    assert not OUTPUT.exists()
    state=core.read(ROOT,core.STATE)
    assert state['execution_runtime']['active']['operation']==OP
    coverage=read(ROOT/'docs/program/comprehensive-v14/work/SW.CELL.panels_did.commercial/coverage-review.json')
    audit=read(PREVIOUS/'source-audit.json')
    verify_bindings([coverage,audit,read(PREVIOUS/'local-probe.json')])
    write(BASE/'plan-review.json',dict(status='pass_to_execute',reviewer=REVIEWER,
        evidence=[ref(BASE/'plan.md','Reviewed bounded comparison plan'),
            ref(PREVIOUS/'source-audit.json','Five preserved primary originals'),
            ref(PREVIOUS/'omissions-register.json','Six-family unresolved evidence')],
        checks=['Keep the full six-family shortlist; do not select away uncovered vendors.',
            'Distinguish documented commands, installed edition, entitlement, current service and proposed target.',
            'Insufficient edition evidence keeps the comparison inconclusive, not absent.',
            'Do not require expensive trials or bank truth to finish a documentary proposal assessment.']))
    # The source authors flag a narrower StataNow option boundary in the same original PDF.
    path=PREVIOUS/'stata_xthdid.txt'
    lines=path.read_text().splitlines()
    anchors=[]
    for token in ['This command includes features that are part of StataNow.',
                  'over(overspec) is part of StataNow.', 'noxinteract is part of StataNow.']:
        indices=[i for i,line in enumerate(lines) if token in line]
        assert len(indices)==1,token
        i=indices[0]
        anchors.append(dict(marker=token,line=i+1,physical_page=path.read_text()[:path.read_text().index(token)].count('\f')+1,
            text='\n'.join(lines[max(0,i-1):i+5])))
    write(BASE/'edition-option-inspection.json',dict(status='pass_for_localized_primary_claim',
        source=ref(PREVIOUS/'stata_xthdid.pdf','Authentic selected official manual'),
        extraction=ref(path,'Lines3,175,188: StataNow option markers'),anchors=anchors,
        finding='The selected manual explicitly marks over() and noxinteract as StataNow features; r19 examples do not establish entitlement to those options.',
        limits='Original local bytes and selected markers only; no exact installed edition, historical-cutoff authentication or license rights.'))
    # Reproduce the saved authored calculation without rerunning acquisition or vendor engines.
    calculated=prior.exact_reference()
    assert calculated==read(PREVIOUS/'exact-reference.json')
    write(BASE/'exact-replay.json',calculated)
    local=read(PREVIOUS/'local-probe.json')
    assert local['panel_DID_request']['disposition']=='unsupported'
    sources=audit['sources']
    vendors=[]
    for candidate in coverage['candidates']:
        family=candidate['family']
        selected=[s for s in sources if s['source_identity'] in candidate['sources']]
        assert len(selected)==({'Stata':4,'EViews':1}.get(family,0))
        item=dict(family=family,aliases=candidate['aliases'],evidence_class=candidate['status'],
            source_records=selected,documented_strength=candidate['documented'],
            proposed_choice=candidate['proposal_route'],remaining_gap=candidate['unresolved'],
            current_common_service='The preserved actual dependent-panel DID request completed with disposition unsupported; no qualified common-service panel-DID estimate was returned.',
            current_service_scope='This scoped dispatcher observation is not a claim that no panel research code exists elsewhere in causal.',
            proposed_capability='Typed cohort/time effect table with unit/time/assignment keys, explicit control pool and base period, aggregation weights, sampling law and uncertainty/failure status.',
            edition_acceptance='inconclusive: exact relevant edition, licensed options and cutoff-era bytes are not established',
            version_date=[s['version_date'] for s in selected],
            runtime_status='not evaluated; no vendor installation, purchase, contact or trial',
            price_evidence=dict(status='unavailable',amount=None,currency=None,quote=None),
            deployment_and_rights='No embedding, automation, server, redistribution or export entitlement established by this review.',
            next_evidence=candidate['proposal_route']+' Bind dated edition-specific primary documentation and applicable terms/prices; retain unavailable status when public evidence cannot establish them.')
        if family=='Stata':
            item['method_comparison']=dict(scalar='didregress/xtdidregress linear fixed-effect paths have a scalar target under their assumptions.',
                heterogeneous='Separate hdidregress/xthdidregress paths retain cohort/time effects, controls and aggregation.',
                controls='Never-treated and not-yet-treated sets differ; adaptive and common preperiod bases differ.',
                inference='Command-specific robust/cluster behavior and simultaneous-confidence/aggregation restrictions must survive conversion.',
                option_boundary=ref(BASE/'edition-option-inspection.json','Explicit StataNow features in selected manual'),
                banking_gap='A single projection coefficient cannot silently replace heterogeneous branch-period effects or establish a new rollout policy value.')
        elif family=='EViews':
            item['method_comparison']=dict(introduction='Panel-workfile DID and named TWFE diagnostic references are documented.',
                technical_gap='Obtain full estimator and diagnostic sections before making aggregation, heterogeneous-effect or covariance comparisons.')
        else:
            item['method_comparison']=dict(status='relevant DID-specific original not inspected',
                interpretation='Generic regression or hosting cannot establish a dedicated DID estimator; lack of inspected evidence is not product absence.')
        vendors.append(item)
    evidence=[ref(PREVIOUS/n,'Preserved authentic panel evidence') for n in ['source-audit.json','candidate-register.json',
        'local-probe.json','conversion-contract.json','omissions-register.json']]
    evidence += [ref(BASE/n,'Reviewed comparison evidence') for n in ['plan-review.json','edition-option-inspection.json','exact-replay.json']]
    evidence += [ref(Path(__file__),'Six-family comparison and criterion review')]
    limits=['The six-family comparison remains incomplete: four families lack inspected DID-specific originals and EViews evidence is introductory.',
        'Exact selected edition/options, cutoff bytes, entitlement, deployment rights and public prices remain unresolved; no current-price assertion.',
        'Source descriptions are not vendor runtime outcomes; no commercial installation, purchase, contact or trial occurred.',
        'Existing authored arithmetic and common-service refusal support a proposal comparison, not bank validation or qualified inference.',
        'No new manuscript-depth credit or complete commercial coverage follows from this comparison.']
    trigger='Continue public primary research separately by vendor: dated Stata edition/Now option and rights documentation; full EViews estimator/diagnostic originals; identify and inspect applicable SAS, IBM, MathWorks and commercial-hosting DID paths. Preserve quotations or unavailable price status. Only a later authorized prototype needs licensed native execution.'
    comparison=dict(operation_id=OP,status='inconclusive',scope='Six-family documentary panel-DID proposal comparison',
        reviewer=REVIEWER,cutoff='2026-10-07',review_date='2026-10-19',vendors=vendors,
        capability_gap='Our common service has a documented scoped refusal, while selected Stata technical documents describe existing scalar and heterogeneous paths; proposed cohort/time service remains unqualified.',
        behavioral_reference=dict(exact=ref(BASE/'exact-replay.json','Authored branch rollout'),
            projection_thousand_USD='-91/8',treated_branch_period_ATT_thousand_USD='34',
            significance='The same stipulated positive cohort/time effects can yield a negative scalar projection; targets and weights must match before comparison.'),
        proposed_contract=ref(PREVIOUS/'conversion-contract.json','Unimplemented target/conversion/uncertainty contract'),
        evidence=evidence,limitations=limits,revisit_trigger=trigger,
        capabilities=[],integration_allowed=False,bank_truth_required_for_next_public_research=False)
    write(OUTPUT,comparison)
    write(BASE/'review.json',dict(status='inconclusive',reviewer=REVIEWER,
        output=ref(OUTPUT,'Preserved six-family comparison'),evidence=evidence,
        criteria=[dict(index=0,verdict='inconclusive',finding='Original edition-specific evidence is incomplete for the six-family shortlist; no complete comparison is claimed.'),
                  dict(index=1,verdict='pass',finding='Unevaluated, absent, unavailable price, entitlement and runtime evidence remain distinct; no transaction or trial is fabricated.')],
        limitations=limits,revisit_trigger=trigger))
    graph,_,_=run.combined(ROOT,state)
    receipt=run.ledger.receipt_template(run.ledger.operation(graph,OP))
    receipt.update(outcome='inconclusive',execution='performed',scope=comparison['scope'],reviewer=REVIEWER,
        capabilities=[],outputs=[ref(OUTPUT,'Contracted commercial panel comparison')],limitations=limits,
        nonexecution_reason='',revisit_trigger=trigger,
        criteria=[dict(c,evidence=evidence+[ref(BASE/'review.json','Author criterion review')]) for c in read(BASE/'review.json')['criteria']])
    write(BASE/'operation-receipt.json',receipt)
    verify_bindings([comparison,receipt])
    print(json.dumps(dict(operation=OP,outcome='inconclusive',vendors=6,inspected_primary_originals=5,
        native_vendor_trials=0,followups='public edition/source/rights research; no global blocker')))


if __name__=='__main__':
    main()

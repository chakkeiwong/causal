#!/usr/bin/env python3
"""Disposition of acquired policy evidence; unavailable editions stay unresolved."""
import copy
import json
from pathlib import Path
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write

ROOT=core.ROOT;BASE=ROOT/'docs/program/execution/2026-10-17/policy-vendor-comparison'
PRIOR=ROOT/'docs/program/execution/2026-10-16/commercial-policy'
OUTPUT=ROOT/'docs/program/comprehensive-v14/work/SW.COMM.policies_offpolicy/vendor-comparison.json'
AUDIT=ROOT/'docs/program/execution/2026-10-17/s9/publication-v4/reader/source-audit.json'


def read(p):return json.loads(p.read_text())


def main():
    assert not BASE.exists() and not OUTPUT.exists()
    BASE.mkdir(parents=True)
    primary=read(PRIOR/'primary-review.json');design=read(PRIOR/'comparison-design.json');audit=read(AUDIT)
    for x in [primary,design,read(PRIOR/'author-review.json'),read(PRIOR/'omissions-register.json'),audit]:verify_bindings(x)
    sources={s['integrated_citation_key']:s for s in audit['sources']}
    vendors=copy.deepcopy(design['vendor_matrix'])
    direct={'Stata','JMP','Microsoft','BayesFusion','Amazon'}
    for v in vendors:
        records=[sources[k] for k in v['evidence_keys']]
        v['source_records']=records
        v['version_date']=[s.get('version_date',s.get('version_status','not established')) for s in records]
        v['evidence_class']='bounded policy-relevant official text' if v['family'] in direct else 'policy-specific original unavailable or not inspected'
        v['edition_acceptance']='inconclusive: exact installed edition, entitlement and cutoff byte identity are not established'
        v['runtime_status']='not evaluated; no commercial installation or engine trial'
        v['price_evidence']=dict(status='unavailable',amount=None,currency=None,quote=None)
        v['deployment_evidence']='Public documentation does not establish our embedding, server or distribution rights.'
        if v['family']=='BayesFusion':
            v['deployment_evidence']='SMILE2.2.4.R1 license manual distinguishes development, server and end-user deployment rights; actual entitlement is absent.'
        if v['family']=='Microsoft':
            v['deployment_evidence']='Inspected archived official pages state retirement2026-08-25; retain as a historical comparator. learning-loop is an unqualified migration lead.'
        v['next_evidence']=v['proposed_choice']+' Preserve original bytes, exact edition/version and inspected technical anchors; run only an authorized matched prototype later.'
    criteria=[dict(index=0,verdict='inconclusive',finding='Eleven families are explicitly compared, but six lack policy-specific original support and no row has complete installed-edition/entitlement/cutoff closure. Unavailable originals remain omissions, not absent-feature findings.'),
              dict(index=1,verdict='pass',finding='Observed local refusals, proposed capabilities, documentary vendor strengths and unexecuted trials are distinct. All prices are unavailable; no purchase, contact or runtime is fabricated.')]
    evidence=[ref(PRIOR/'primary-review.json','Six official originals and inherited audited sources'),
              ref(PRIOR/'comparison-design.json','Existing eleven-family portfolio and proposed profiles'),
              ref(PRIOR/'omissions-register.json','Failed public acquisition routes and uninspected families'),
              ref(PRIOR/'local-probe.json','Observed common-dispatcher refusals; separate research modules remain distinct'),
              ref(PRIOR/'acquisition-observations.json','Bounded source acquisition outcomes'),
              ref(PRIOR/'fallback-observations.json','Retained alternative-route outcomes'),
              ref(AUDIT,'Exact canonical731-record source audit'),ref(Path(__file__),'Bounded comparison and honest disposition')]
    limits=read(PRIOR/'author-review.json')['limits']+[
        'No new online search or vendor acquisition is claimed in this continuation; it reviews preserved October16 originals at the October7 cutoff.',
        'This review does not convert incomplete documentation into an edition-specific pass.']
    payload=dict(operation_id='SW.COMM.policies_offpolicy',status='inconclusive',scope='Bounded documentary proposal comparison, no vendor trial',
        reviewer=dict(name='Codex author/coordinator',kind='author'),cutoff='2026-10-07',review_date='2026-10-17',
        vendors=vendors,criteria=criteria,known_route='Acquire missing versioned official manuals and exact edition/rights facts; then compare the same target, information clock, sampling law and monetary objective.',
        unavailable_originals=['MathWorks: retained HTTP403 routes','SAS reinforcement-learning: retained HTTP404 routes','HUGIN: retained HTTP455 routes'],
        uninspected_policy_originals=['IBM','Mplus policy-specific extension','Bayesia policy-specific extension'],
        prototype_prerequisites=['Explicit static/sequential/adapting-learner/supplied-model target','Public/generated matched requests and all-assigned failure accounting',
            'Correct logging probabilities and policy/sample separation','Licensed environment only after applicable authorization; no trial in this review'],
        research_not_promised=['General hidden-state identification','Dependent finite-sample policy uncertainty','Useful bank precision and actual ROI'],
        evidence=evidence,limitations=limits,whole_census_closed=False,product_qualified=False)
    write(OUTPUT,payload)
    write(BASE/'review.json',dict(status='pass_for_scoped_inconclusive_disposition',finding='The output satisfies honest evidence accounting but does not satisfy universal edition-specific original coverage.',
        reviewed_output=ref(OUTPUT,'Eleven-family comparison with six policy-source gaps'),criteria=criteria,evidence=evidence,limitations=limits))
    state=core.read(ROOT,core.STATE);graph,_,_=run.combined(ROOT,state);node=run.ledger.operation(graph,'SW.COMM.policies_offpolicy')
    receipt=run.ledger.receipt_template(node)
    receipt.update(outcome='inconclusive',execution='performed',scope=payload['scope'],reviewer=payload['reviewer'],
        outputs=[ref(OUTPUT,'Contracted edition-scoped vendor comparison')],limitations=limits,
        criteria=[dict(x,evidence=evidence+[ref(BASE/'review.json','Author disposition review')]) for x in criteria],
        nonexecution_reason='',revisit_trigger='Accessible authorized policy-specific manuals and exact edition/rights evidence resolve the named gaps; then perform a preserving successor review.')
    write(BASE/'operation-receipt.json',receipt)
    print(json.dumps(dict(outcome='inconclusive',families=len(vendors),policy_relevant_original_families=len(direct),unresolved_families=len(vendors)-len(direct))))


if __name__=='__main__':main()

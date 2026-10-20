#!/usr/bin/env python3
"""Record eight-family dynamic comparison with explicit incomplete evidence."""
import json
from pathlib import Path

import dynamic_panel_reference_20261019 as exact
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write

run=extension.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-20/dynamic-commercial-comparison-v1'
PRIOR=ROOT/'docs/program/execution/2026-10-19/dynamic-commercial-v1'
OP='SW.COMM.dynamic_panel_timeseries'
OUTPUT=ROOT/f'docs/program/comprehensive-v14/work/{OP}/vendor-comparison.json'
REVIEWER=dict(name='Codex author/coordinator',kind='author')
read=lambda p:json.loads(p.read_text())


def main():
    assert not OUTPUT.exists()
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP
    audit=read(PRIOR/'source-audit-v2.json');verify_bindings(audit)
    write(BASE/'plan-review.json',dict(status='pass_to_execute',reviewer=REVIEWER,
        evidence=[ref(BASE/'plan.md','Bounded documentary comparison'),
            ref(PRIOR/'source-audit-v2.json','Preserved originals and corrected anchors'),
            ref(PRIOR/'omissions-register.json','Unresolved sources and editions')],
        checks=['Retain all eight families/leads and their different targets.',
            'Separate documented functionality, exact edition, entitlement and observed runtime.',
            'Keep incomplete source/edition comparisons inconclusive.',
            'Public documentary work does not require a bank experiment or purchase.']))
    anchors=[]
    for name,spans in [('stata_ab.txt',[(1,24)]),('stata_system.txt',[(1,24)]),
        ('stata_lp.txt',[(66,94)]),('eviews_panel.txt',[(104,120),(176,215)])]:
        p=PRIOR/name;lines=p.read_text().splitlines()
        anchors.append(dict(extraction=ref(p,'Selected exact lines'),
            spans=[dict(start=a,end=b,text='\n'.join(f'{i+1}: {lines[i]}' for i in range(a-1,b))) for a,b in spans]))
    write(BASE/'anchor-review.json',dict(status='pass_for_localized_original_claims',evidence=anchors,
        original_bindings=ref(PRIOR/'source-audit-v2.json','Exact originals and extraction method'),
        findings=['Stata difference GMM is described for many panels/few periods with an idiosyncratic serial-correlation restriction.',
            'System GMM adds an initial-condition orthogonality restriction; large autoregression alone does not license it.',
            'lpirf dfk changes the covariance divisor while small changes reference statistics; OLS, robust and HAC are separate covariance requests.',
            'EViews covariance labels distinguish period and cross-section clusters; transformed GMM constrains available weight choices.',
            'The EViews text labels White period as AB1-step while describing2-step/multi-step use; preserve this unresolved textual ambiguity.',
            'The documented default dynamic instrument set reaches171 at20periods; truncation and rank must be explicit.'],
        native_execution=False))
    calculated=exact.calculate();assert calculated==read(PRIOR/'exact-results.json')
    write(BASE/'exact-replay.json',calculated)
    p=ROOT/'src/causalbank/operation_service_v12.py';lines=p.read_text().splitlines()
    assert '("reference-moment-sets", "gaussian-residual-inversion")' in p.read_text()
    current=dict(mode='read_only_source_inspection_not_runtime_trial',source=ref(p,'SUPPORTED, invoke, _estimate'),
        inspected_anchors=[dict(start=a,end=b,text='\n'.join(f'{i+1}: {lines[i]}' for i in range(a-1,b)))
            for a,b in [(22,31),(95,118),(180,186)]],
        finding='The selected common-service estimator accepts reference-moment-sets/gaussian-residual-inversion and returns unsupported for other estimator pairs. It consumes supplied moments; it does not expose a native panel-GMM or vendor engine through this branch.',
        limit='This source observation does not claim that all research code lacks panel/time-series constructions.')
    write(BASE/'current-service-review.json',current)
    sources=audit['sources']+audit['inherited_sources']
    families={
        'Stata':['exec19_dynamic_stata_ab','exec19_dynamic_stata_system','exec19_dynamic_stata_lp','exec13_ct_stata_svar','exec13_ct_stata_ivsvar'],
        'EViews':['exec19_dynamic_eviews_panel'],
        'SAS':['exec13_ct_sas_causal','exec13_ct_sas_structural'],
        'IBM':['exec13_ct_ibm_tcm'],'Mplus':['exec13_ct_mplus81'],
        'MathWorks':[],'OxMetrics':[],'Commercial hosted open-source frontends':[]}
    comparisons={
        'Stata':('Prioritize as a documented method comparator, conditional on licensed edition and matched design.',
            'Short-panel branch outcomes: freeze difference versus system moments, lag caps and initial conditions. Rate-shock responses: separately match local projections, structural restrictions or external instruments, horizons and normalization.'),
        'EViews':('Retain as a documented panel-GMM comparator after resolving the exact transformation/weight contract.',
            'For a branch funding panel preserve differences/orthogonal deviations, period-specific instruments, retained rows and time/cross-section clustering. The ambiguous label cannot select an algorithm by itself.'),
        'SAS':('Retain a temporal-model candidate; dynamic-panel comparison is incomplete.',
            'A forecast or Granger test is not a bank rate intervention; inspect PANEL and full structural equations before mapping to that use case.'),
        'IBM':('Retain as a predictive temporal comparator; causal-intervention parity is not established.',
            'Use the documented TCM predictive meaning for forecasting comparisons; do not relabel it as an identified rollout or pricing effect.'),
        'Mplus':('Retain for supplied latent longitudinal models; qualify model and estimator separately.',
            'Repeated servicing measurements with latent states require declared measurement and dynamic assumptions, random-effect meaning and missing-covariate handling; no system-GMM equivalence follows.'),
        'MathWorks':('Retain unresolved until authentic release-matched technical text is inspected.',
            'The inaccessible selected IRF route does not establish or rule out a bank shock-response capability.'),
        'OxMetrics':('Retain unresolved until authentic selected PcGive/Autometrics methods and edition are inspected.',
            'A product-family name or failed manual fetch cannot establish instruments, inference or causal targets.'),
        'Commercial hosted open-source frontends':('Resolve a concrete vendor, service edition and numerical backend before a feature verdict.',
            'Hosting and a tool interface add no verified dynamic-panel estimator; require target-preserving inputs, outputs and exports.')}
    vendors=[]
    for candidate in read(PRIOR/'candidate-register.json')['candidates']:
        family=candidate['family'];selected=[s for s in sources if s['integrated_citation_key'] in families[family]]
        assert len(selected)==len(families[family])
        route,use=comparisons[family]
        vendors.append(dict(family=family,aliases=candidate['aliases'],evidence_class=candidate['status'],
            source_records=selected,documented_strength=candidate['documented_scope'],
            use_case_comparison=use,proposed_choice=route,remaining_gap=candidate['next_public_evidence'],
            current_common_service=current['finding'],current_service_scope=current['limit'],
            proposed_capability='Typed dynamic target with instrument moments, exact design, sample/calendar, covariance and failure contract; vendor adapter unqualified.',
            edition_acceptance='inconclusive: relevant exact edition/options and entitlement not established',
            version_date=[s['version_date'] for s in selected],
            historical_cutoff='Source dates and route labels are retained; retrieved mutable bytes are not authenticated cutoff snapshots.',
            runtime_status='not evaluated; no vendor installation, purchase, contact or trial',
            price_evidence=dict(status='unavailable_in_inspected_evidence',amount=None,currency=None,quote=None),
            deployment_and_rights='Embedding, server, automation, redistribution and export entitlements are unverified for the selected deployment.',
            next_evidence=candidate['next_public_evidence']+' Bind actual edition, applicable public/quoted terms and cost basis; native evaluation is a later prototype gate.',
            absence_claim=False))
    assert len(vendors)==8
    limits=['The full eight-family/lead comparison remains incomplete; three have no selected usable technical original and other coverage is partial.',
        'Exact selected editions, cutoff bytes, entitlements, deployment rights and prices remain unresolved; no current market-price claim.',
        'Documented commands are not native runtime outcomes. No vendor contact, trial, purchase or installation occurred.',
        'Read-only dispatcher inspection and exact authored examples do not establish bank validation or universal dynamic inference.',
        'Existing integrated dynamic-commercial treatment is preserved; this operation earns no additional manuscript depth.']
    evidence=[ref(PRIOR/n,'Existing reviewed public and authored evidence') for n in
        ['source-audit-v2.json','candidate-register.json','conversion-contract.json','omissions-register.json',
         'release-source-review.json','development.tex']]
    evidence += [ref(BASE/n,'Current bounded comparison') for n in
        ['plan-review.json','anchor-review.json','exact-replay.json','current-service-review.json']]
    evidence.append(ref(Path(__file__),'Comparison and criterion construction'))
    trigger='Continue public evidence per candidate: exact Stata edition and postestimation/rights; full EViews algorithm/label clarification; SAS PANEL and equations; IBM estimator details; Mplus model/version; accessible MathWorks and PcGive originals; concrete hosted service. Bind prices or preserve unavailable status. Native trials follow prototype merit.'
    comparison=dict(operation_id=OP,status='inconclusive',scope='Eight-family documentary dynamic-panel/time-series comparison',
        reviewer=REVIEWER,cutoff='2026-10-07',review_date='2026-10-20',vendors=vendors,
        capability_gap='Selected vendors document mature numerical methods; our inspected common-service branch consumes supplied moments and has no native panel-GMM/vendor path. Proposed typed semantics and qualification remain work to do.',
        behavioral_reference=dict(exact=ref(BASE/'exact-replay.json','Authored moments/calendar contrasts'),
            invalid_level_moment='1/2',mean_stationary_level_moment='0',common_calendar_variance_ratio='101/2',
            significance='Source comparison must match moment validity, instrument count and dependence; software convergence or a covariance option cannot supply these assumptions.'),
        proposed_contract=ref(PRIOR/'conversion-contract.json','Unimplemented conversion contract'),
        evidence=evidence,limitations=limits,revisit_trigger=trigger,capabilities=[],integration_allowed=False,
        bank_truth_required_for_next_public_research=False)
    write(OUTPUT,comparison)
    criteria=[dict(index=0,verdict='inconclusive',finding='Original exact-edition evidence remains incomplete across the entire eight-family shortlist; no complete competitive comparison is claimed.'),
        dict(index=1,verdict='pass',finding='Unevaluated runtime, missing sources, unavailable prices and unverified rights remain distinct from absent capability; no transactions or native trials are invented.')]
    write(BASE/'review.json',dict(status='inconclusive',reviewer=REVIEWER,output=ref(OUTPUT,'Eight-family comparison'),
        criteria=criteria,evidence=evidence,limitations=limits,revisit_trigger=trigger))
    graph,_,_=run.combined(ROOT,state);receipt=run.ledger.receipt_template(run.ledger.operation(graph,OP))
    receipt.update(outcome='inconclusive',execution='performed',scope=comparison['scope'],reviewer=REVIEWER,
        capabilities=[],outputs=[ref(OUTPUT,'Contracted comparison')],limitations=limits,nonexecution_reason='',
        revisit_trigger=trigger,criteria=[dict(c,evidence=evidence+[ref(BASE/'review.json','Author review')]) for c in criteria])
    write(BASE/'operation-receipt.json',receipt);verify_bindings([comparison,receipt])
    print(json.dumps(dict(operation=OP,outcome='inconclusive',families=8,native_trials=0,global_blocker=False)))


if __name__=='__main__':main()

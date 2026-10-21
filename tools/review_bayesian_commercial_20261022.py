#!/usr/bin/env python3
"""Review commercial posterior/state evidence without claiming market completion."""
import argparse
import json
from pathlib import Path
import bayesian_state_reference_20261022 as exact
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run=extension.base
core=run.core
ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-22/bayesian-commercial-v1'
OP='SW.CELL.bayesian_scm_state.commercial'
COMPARE='SW.COMM.bayesian_scm_state'
REVIEWER=dict(name='Codex author/coordinator',kind='author')
read=lambda p:json.loads(p.read_text())
LIMITS=[
    'Bounded technical review across five supported vendor families; ten named families are not an exhaustive market census.',
    'Cutoff7October2026; later-acquired mutable manuals and metadata do not establish exact cutoff-era bytes.',
    'Stata r19 example routes and July2026 metadata do not match an installed licensed build. Other manual-family and edition limits remain in inherited audits.',
    'The SAS PDF is partial and failed; EViews and HUGIN endpoints failed. None supports a technical or absence finding.',
    'No vendor engine, downloaded code, live model, bank-data trial, purchase or vendor contact was performed.',
    'Prices, commercial entitlements, runtime/export equivalence and broader source discovery remain unresolved.',
    'All numerical laws and monetary inputs are authored hypothetical examples; no empirical coverage or measured banking return.',
    'Visual inspection is pending a fresh image allowance; text/layout checks do not confer rendered acceptance.',
    'Mandatory repairs, Q1/Q5, independent review and final proposal acceptance remain open.']


def original(name,title,ranges,claims):
    p=BASE/'acquisition/network'/(name+'.pdf')
    receipt=p.with_suffix('.receipt.json');r=read(receipt)
    assert r['returncode']==0 and r['format_valid'] and core.sha(p)==r['sha256']
    extracted=BASE/'extracted'/(name+'.txt');body=extracted.read_text();lines=body.splitlines(keepends=True)
    anchors=[]
    for lo,hi in ranges:
        assert 1<=lo<=hi<=len(lines)
        anchors.append(dict(anchor=f'extracted lines{lo}-{hi}',
            physical_page=''.join(lines[:lo-1]).count(chr(12))+1,inspected_text=''.join(lines[lo-1:hi])))
    return dict(integrated_citation_key='exec22_state_'+name,kind='official_documentation',
        title=title,author='StataCorp',year=2026,source_identity=r['url'],
        version_date='Official command manual, PDF metadata28July2026; r19 example routes; exact licensed edition/build unverified',
        accessed_utc=r['finished_at'],local_copy=ref(p,'Complete authentic official PDF'),
        text_copy=ref(extracted,'Inert technical extraction; original authoritative'),
        acquisition_receipt=ref(receipt,'Bounded public acquisition and hash'),
        pdf_metadata=ref(BASE/'extracted'/(name+'.pdfinfo.txt'),'Observed metadata; not cutoff proof'),
        inspected_anchors=anchors,supported_claims=claims,limitations=LIMITS)


def receipt(operation,output,evidence,findings,scope):
    state=core.read(ROOT,core.STATE)
    assert state['execution_runtime']['active']['operation']==operation
    graph,_,_=run.combined(ROOT,state);node=run.ledger.operation(graph,operation)
    value=run.ledger.receipt_template(node)
    value.update(outcome='inconclusive',execution='performed',scope=scope,reviewer=REVIEWER,
        capabilities=[],outputs=[ref(output,'Reviewed scoped result')],limitations=LIMITS,
        nonexecution_reason='',revisit_trigger='Complete complementary candidate searches, exact editions, missing originals and rights; qualify public prototypes before bank trials.',
        criteria=[dict(index=i,verdict=v,finding=f,evidence=evidence) for i,(v,f) in enumerate(findings)])
    return value


def coverage():
    output=ROOT/f'docs/program/comprehensive-v14/work/{OP}/coverage-review.json'
    assert not output.exists() and not (BASE/'source-audit.json').exists()
    write(BASE/'plan-review.json',dict(status='pass',reviewer=REVIEWER,
        evidence=[ref(BASE/'plan.md','Six-step reviewed plan'),ref(BASE/'baseline-runtime-check.json','Passing recovered runtime check'),
                  ref(BASE/'baseline-master-check.json','Passing historical-master check')],
        checks=['No phase gate or bank-data requirement blocks independent proposal research.',
            'Distinguish parameter posterior, hidden-state inference, parameter identification and intervention identification.',
            'Test information clock, uncertainty decomposition and compressed-chain export rather than treating API success as causal evidence.',
            'Retain all failed originals; incomplete candidate searches receive inconclusive outcomes.',
            'Preserve prior citation contexts and exact reader/sponsor binding; serialize canonical transitions.']))
    sources=[
        original('stata_sspace','Stata: sspace, state-space models',[(8,16),(133,161),(186,194),(207,263),(348,354)],
            ['Linear time-invariant state-space parameters are estimated by ML using Kalman/diffuse likelihood calculations.',
             'State/observation noise and exogenous regressors carry explicit restrictions; robust VCE is distinct from causal identification.',
             'Stationary initialization, diffuse variants and covariance versus error form require preservation.',
             'Selected technical note requires the refining optimization step to converge; convergence is not a universal causal-identification certificate.']),
        original('stata_sspace_post','Stata: postestimation tools for sspace',[(38,40),(62,71),(97,120),(342,360),(374,376)],
            ['One-step uses past data, filter uses contemporaneous data and smooth uses all sample information.',
             'Reported prediction RMSE accounts for disturbances but excludes parameter-estimation error.',
             'Prediction sample and exogenous paths affect recursive state/prediction output; default first equation and state names require explicit mapping.']),
        original('stata_bayesmh','Stata: bayesmh, Bayesian models using Metropolis-Hastings',[(8,16),(598,612),(626,655),(838,866),(1069,1090),(1920,1988)],
            ['Adaptive MH supports explicit likelihoods and priors; permitted combinations need not yield proper posteriors.',
             'Chain count, initialization, adaptation, burn-in, thinning and random seeds govern reproducibility, not intervention semantics.',
             'Convergence has no single sufficient diagnostic; inspect all parameters and requested functions, multimodality and initialization.',
             'MCSE uses ESS or batch means; simulation error differs from posterior uncertainty.',
             'Saved chain/index/frequency rows compress repeated states; frequency weights and parameter-name mapping are essential.'])]
    sources.append(dict(integrated_citation_key='exec22_state_reference',kind='project_authored_exact_reference',
        title='Exact credit-state identification, information-clock and numerical references',
        author='Causal banking proposal project',year=2026,source_identity='tools/bayesian_state_reference_20261022.py',
        version_date='22October2026; authored finite laws and rational algebra',
        local_copy=ref(ROOT/'tools/bayesian_state_reference_20261022.py','calculate(): complete laws and checks'),
        inspected_anchors=[dict(anchor='calculate()',inspection='Finite enumeration, direct Bayes cross-check, observability null direction, variance decomposition and geometric bound')],
        supported_claims=['Identical observable joint distributions admit default reductions0 or3/5 and stipulated margins-100 or500USD.',
            'Likelihood equality leaves model odds at the prior; priors1/10 and9/10 imply margins-40 and440USD.',
            'Filtering3/4 and smoothing1/2 imply margins15 and-10USD under distinct information sets.',
            'Rank-one observation law cannot recover a hidden contrast despite equal eight-period outputs.',
            'Predictive variance separates1/6 and1/12; two-outcome count variance2/3 exceeds plug-in1/2.',
            'Compressed chain frequencies9 and1 yield mean9/50, not unweighted1/2.',
            'Conditional TV2/100 and reward span100 imply a12-step discounted fixed-policy bound about14.3514USD.'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,cutoff='2026-10-07',limitations=LIMITS))
    keep=['exec13_ct_genie_dbn','exec13_ct_genie_learning','exec13_ct_smile_tutorial','exec13_ct_mplus81',
          'exec13_ct_bayesia_inference','exec13_ct_bayesia_identification','exec13_latent_netica_algorithms']
    inherited=[]
    for folder in ['commercial-temporal','commercial-latent']:
        audit=read(ROOT/'docs/program/execution/2026-10-13'/folder/'source-audit.json')
        verify_bindings(audit)
        inherited += [s for s in audit['sources'] if s['integrated_citation_key'] in keep]
    assert {s['integrated_citation_key'] for s in inherited}==set(keep)
    write(BASE/'inherited-source-review.json',dict(sources=inherited,
        finding='Reinspected technical extractions and retained exact earlier audit identities; seven official sources across four additional families.',
        selected_anchors=['GeNIe DBN9-14; learning8-21; SMILE tutorial9-46.',
            'Netica algorithms1-82: parameter learning objective, case likelihood and local optima.',
            'Mplus8.1 addendum1-103: Bayes latent centering and missing covariate handling.',
            'Bayesia inference80-103 and identification105-116: observation/intervention distinction and DAG assumptions.'],
        limitation='Inherited audit source keys retain their exact earlier claims; this review does not broaden them.'))
    write(BASE/'exact-results.json',exact.calculate())
    specs=[
        ('Stata','sspace; predict; bayesmh; Bayesian estimation',
         'Three complete command manuals inspected; linear-state ML and Bayesian model sampling are separate procedures.',
         'Retain time-invariant matrices, initialization, observation clock, disturbance-only RMSE, proper posterior and weighted chain exports.',
         'Match release/build/edition, command entitlements, runtime and parameter-uncertainty propagation.'),
        ('BayesFusion','GeNIe; SMILE; PySMILE; jSMILE; rSMILE',
         'Three preserved DBN and C++ tutorial originals; manual families5.0.R2 and2.2.4.R1.',
         'Fixed discrete DBN EM, time-indexed columns, initial/transition CPTs and outcome indices; selected GeNIe page excludes dynamic structure learning.',
         'Inspect inference/approximation diagnostics, license deployment terms and wrapper export parity for a pinned supported release.'),
        ('Norsys','Netica; Netica API',
         'Preserved parameter-learning manual; current numbered release not established.',
         'Counting, EM and conjugate-gradient parameter learning with preexisting-table prior information and local optima; no posterior draw claim.',
         'Recover versioned state/intervention, diagnostics and licensing manuals; distinguish optimization from full parameter posterior.'),
        ('Bayesia','BayesiaLab',
         'Two preserved official inference/identification texts; mutable edition unresolved.',
         'Evidence and intervention are distinguished; graph surgery operates under supplied causal assumptions, with identification separate from estimation.',
         'Recover exact edition, latent-state/uncertainty limits, export semantics, license and native graph-query tests.'),
        ('Mplus','Mplus8.1; DSEM; RDSEM',
         'Preserved Version8.1 language addendum.',
         'Bayes latent centering and residual-versus-outcome lags; missing covariate rows can be excluded unless modeled as outcomes.',
         'Recover full selected-release priors, sampler diagnostics, time spacing and licenses before supplied-model reuse.'),
        ('SAS','SAS/STAT; PROC MCMC; SAS/ETS; SSM',
         'Selected15.1 MCMC PDF transfer incomplete; not technical evidence.',
         'Adjacent sampler and state-model leads only for this cell; earlier unrelated SAS profiles do not prove coverage.',
         'Recover complete versioned PROC MCMC and SSM technical originals, exports and deployment terms.'),
        ('EViews','EViews; Sspace; state-space model',
         'Selected official endpoint returned403; no technical evidence from this attempt.',
         'State-estimation lead only; no negative capability claim.',
         'Follow current official help index to a versioned state-space estimation/prediction manual and verify inference target.'),
        ('HUGIN Expert','HUGIN; dynamic Bayesian network',
         'Selected9.4 manual endpoint returned455; no technical evidence from this attempt.',
         'Graphical/state-engine lead only; no negative capability claim.',
         'Recover authentic versioned DBN, intervention and inference-error text with rights and export documentation.'),
        ('Bayes Server','Bayes Server; .NET; Java',
         'Uninspected family/SDK leads retained from earlier commercial candidate register.',
         'No capability granted by family name.',
         'Acquire edition-matched dynamic/causal inference, API, approximation and licensing originals.'),
        ('Commercial numerical environments','MATLAB toolboxes; Wolfram Mathematica',
         'Adjacent Bayesian/state-computation leads; not evaluated for this causal target.',
         'Do not equate a numerical or state estimator with causal identification.',
         'Search exact product/toolbox and version for state, posterior, intervention, export and entitlement contracts.')]
    candidates=[dict(family=f,aliases=a,source_status=s,technical_scope=t,next_public_evidence=n,
        absence_claim=False,runtime_executed=False,entitlement_verified=False) for f,a,s,t,n in specs]
    write(BASE/'search-coverage.json',dict(cutoff='2026-10-07T15:59:59Z',
        local_inventory='Commercial latent/temporal official-source audits and candidate families, reinspected22October2026.',
        external_discovery='No web-search tool exposed in this session; six fixed official technical URLs attempted, not an index census.',
        stopping_rule='One six-URL batch with connection retry; preserve three successful manuals, one incomplete PDF and two endpoint failures. Exact source recovery and complementary discovery remain local obligations.',
        no_hit_claim=False,complete_market_search=False))
    write(BASE/'candidate-register.json',dict(cutoff='2026-10-07',candidates=candidates,
        search=ref(BASE/'search-coverage.json','Actual search scope and stopping rule'),market_census_complete=False))
    failures=[ref(p,'Failed acquisition; no technical claim') for p in sorted((BASE/'acquisition').glob('*/*.receipt.json')) if read(p)['returncode']!=0]
    write(BASE/'omissions-register.json',dict(global_blocker=False,failures=failures,
        candidates=[dict(family=c['family'],next_action=c['next_public_evidence']) for c in candidates],
        additional=['Complementary market search, exact cutoff-era edition bytes, quoted costs and terms.',
            'Qualify public known-law comparisons with pinned native workers before expensive bank trials.',
            'Causal mechanisms, latent-state interpretation and approximation bounds remain explicit assumptions.'],
        bank_inputs_required_for_next_public_work=False))
    write(BASE/'conversion-contract.json',dict(status='proposed_not_implemented',integration_allowed=False,
        requirements=['Declare separate tasks: prediction, filtering, smoothing, parameter posterior, model selection and intervention.',
            'Bind decision time and per-variable availability; reject future evidence for an online action; retain retrospective smoothing as a distinct query.',
            'Preserve state/observation equations, unit/time IDs, initial-state law, transition/emission parameters, noise dependence and missingness.',
            'Expose state observability and parameter identifiability separately; retain causal alternatives and policy/exogeneity assumptions.',
            'Preserve prior support, posterior propriety, initialization, all chain/iteration/frequency metadata and parameter mappings.',
            'Separate process/state, parameter, graph/structural and Monte Carlo uncertainty; do not label disturbance RMSE as total predictive uncertainty.',
            'Request diagnostics for effect/value functions, not only parameter means; test prior and specification sensitivity.',
            'Preserve native errors and numerical tolerances; admit a causal value only under justified intervention semantics and declared approximation conditions.',
            'Use the same typed contract in library, CLI and MCP; an agent may draft model alternatives but cannot certify causal truth or convergence.',
            'Compare public known laws and matched targets; verify exact build, rights and export equivalence before native integration.']))
    evidence=[ref(BASE/n,'Reviewed commercial state evidence') for n in ['plan.md','plan-review.json','source-audit.json',
        'inherited-source-review.json','candidate-register.json','search-coverage.json','omissions-register.json','conversion-contract.json','exact-results.json']]
    evidence.append(ref(Path(__file__),'Review construction'))
    findings=[('inconclusive','Ten candidate families are explicit; complementary discovery, missing originals and exact edition matching remain incomplete.'),
        ('pass','Three new complete official manuals and seven reinspected originals have exact bytes, hashes, version limits and inspected technical anchors; authored examples are distinct.'),
        ('pass','Failed acquisitions, unevaluated alternatives and rights limits have next actions; no unsupported absence or source waiver.')]
    scope='Bounded commercial Bayesian and hidden-state proposal review'
    item=dict(operation_id=OP,status='inconclusive',scope=scope,reviewer=REVIEWER,candidates=candidates,
        criteria=[dict(index=i,verdict=v,finding=f) for i,(v,f) in enumerate(findings)],
        evidence=evidence,limitations=LIMITS,capabilities=[],integration_allowed=False)
    write(output,item);write(BASE/'review.json',item)
    write(BASE/'operation-receipt.json',receipt(OP,output,evidence,findings,scope));verify_bindings(item)
    print(json.dumps(dict(operation=OP,outcome='inconclusive',new_official_originals=3,inherited_originals=7,candidates=10)))


def compare():
    output=ROOT/f'docs/program/comprehensive-v14/work/{COMPARE}/vendor-comparison.json'
    assert not output.exists()
    rows=[]
    for c in read(BASE/'candidate-register.json')['candidates']:
        rows.append(dict(**c,documented_strength=c['technical_scope'],
            matched_use_case='A servicing decision with pre-action hidden-credit-state information, fixed loss/cost and a declared intervention.',
            observed_current_capability='Exact authored finite-law references and proposal contracts; no qualified native adapter.',
            proposed_capability='Typed causal assumptions, information-clock checks and separated uncertainty through library/CLI/MCP.',
            remaining_gap=c['next_public_evidence'],
            reuse_disposition='Conditional isolated licensed adapter candidate; reject automatic conversion of an inferred state/posterior into identified effect.',
            deployment_rights='Unverified; public documentation grants no runtime or redistribution entitlement.',
            price=dict(status='unavailable',amount=None,quote_obtained=False)))
    evidence=[ref(BASE/n,'Reviewed comparison evidence') for n in ['source-audit.json','inherited-source-review.json',
        'review.json','candidate-register.json','conversion-contract.json','omissions-register.json','exact-results.json']]+[ref(Path(__file__),'Comparison construction')]
    findings=[('inconclusive','Five supported vendor families permit scoped technical comparison; edition/build/rights matching and five other families remain unresolved.'),
        ('pass','Rows distinguish supplied-model computation, proposed semantics, missing evidence, unavailable prices and unexecuted native tests; no contact or purchase fabricated.')]
    scope='Ten-family commercial Bayesian/state comparison with public prototype route'
    item=dict(operation_id=COMPARE,status='inconclusive',scope=scope,reviewer=REVIEWER,vendors=rows,
        criteria=[dict(index=i,verdict=v,finding=f) for i,(v,f) in enumerate(findings)],
        evidence=evidence,limitations=LIMITS,capabilities=[],integration_allowed=False)
    write(output,item);write(BASE/'comparison-review.json',item)
    write(BASE/'comparison-receipt.json',receipt(COMPARE,output,evidence,findings,scope));verify_bindings(item)
    print(json.dumps(dict(operation=COMPARE,outcome='inconclusive',families=10,supported_profiles=5)))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['coverage','compare'])
    {'coverage':coverage,'compare':compare}[parser.parse_args().command]()

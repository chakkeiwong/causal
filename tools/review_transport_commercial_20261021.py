#!/usr/bin/env python3
"""Bounded primary-source commercial missingness comparison and honest coverage."""
import argparse
import json
from pathlib import Path

import transport_missingness_reference_20261021 as exact
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run=extension.base
core=run.core
ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-21/transport-commercial-v1'
OP='SW.CELL.transport_missingness.commercial'
COMPARE='SW.COMM.transport_missingness'
REVIEWER=dict(name='Codex author/coordinator',kind='author')
read=lambda p:json.loads(p.read_text())
LIMITS=[
    'Three inspected product profiles and six candidate families are a bounded comparison, not a complete commercial census.',
    'Acquisition on 21 October 2026 and PDF metadata do not establish exact bytes at the 7 October cutoff.',
    'Stata examples use r19 data URLs; exact licensed build/edition remains unmatched. IBM identifies edition31.0.2; SAS HTML identifies14.1, not the failed15.1 PDF leads.',
    'SAS HTML equations stored as images are not inspected; SAS claims use primary prose. Pooling equations use the inspected Stata text.',
    'An earlier IBM extraction warning was reported in the handoff; a repeated extraction succeeded with identical text and no stderr. Rendered inspection remains open.',
    'Partial SAS PDFs, unavailable MNAR syntax, failed search tooling and unresolved vendor leads are not admitted as technical or absence evidence.',
    'No vendor engine, live model, licensed trial, purchase, contact or bank-data validation was performed.',
    'Exact authored laws and proposed interfaces do not establish native integration, finite-sample coverage or measured bank value.',
    'Rights, prices, current product availability, broader search, Q1/Q5 and final visual/proposal acceptance remain open.'
]


def source(name,folder,ext,title,author,version,ranges,claims):
    p=BASE/'acquisition'/folder/(name+'.'+ext)
    receipt=p.with_suffix('.receipt.json');r=read(receipt)
    assert r['returncode']==0 and r['format_valid'] and r['sha256']==core.sha(p)
    extracted=BASE/'extracted'/(name+'.txt')
    body=extracted.read_text();lines=body.splitlines(keepends=True);anchors=[]
    for lo,hi in ranges:
        assert 1<=lo<=hi<=len(lines),(name,lo,hi)
        anchors.append(dict(anchor=f'extracted lines {lo}-{hi}',
            physical_page=body[:sum(map(len,lines[:lo-1]))].count(chr(12))+1 if ext=='pdf' else None,
            inspected_text=''.join(lines[lo-1:hi])))
    item=dict(integrated_citation_key='exec21_transport_'+name,kind='official_documentation',title=title,
        author=author,year=2026,year_meaning='Acquisition year; edition/date detail retained separately',
        source_identity=r['url'],version_date=version,accessed_utc=r['finished_at'],
        local_copy=ref(p,'Complete authentic official original'),text_copy=ref(extracted,'Inspected inert extraction; original authoritative'),
        acquisition_receipt=ref(receipt,'Bounded public HTTPS attempt, status and identity'),
        inspected_anchors=anchors,supported_claims=claims,limitations=LIMITS)
    if ext=='pdf':item['pdf_metadata']=ref(BASE/'extracted'/(name+'.pdfinfo.txt'),'Observed metadata; not cutoff proof')
    return item


def receipt(operation,output,evidence,findings,scope):
    state=core.read(ROOT,core.STATE)
    assert state['execution_runtime']['active']['operation']==operation
    graph,_,_=run.combined(ROOT,state);node=run.ledger.operation(graph,operation)
    value=run.ledger.receipt_template(node)
    value.update(outcome='inconclusive',execution='performed',scope=scope,reviewer=REVIEWER,
        capabilities=[],outputs=[ref(output,'Bounded commercial comparison')],limitations=LIMITS,
        nonexecution_reason='',revisit_trigger='Complete complementary vendor search and original/edition/rights recovery; qualify matched public prototypes before bank trials.',
        criteria=[dict(index=i,verdict=v,finding=f,evidence=evidence) for i,(v,f) in enumerate(findings)])
    return value


def coverage():
    output=ROOT/f'docs/program/comprehensive-v14/work/{OP}/coverage-review.json'
    assert not output.exists() and not (BASE/'source-audit.json').exists()
    write(BASE/'plan-review.json',dict(status='pass',reviewer=REVIEWER,evidence=[ref(BASE/'plan.md','Six-step reviewed plan')],
        checks=['Separate missing-data identification from transfer across target populations.',
            'Inspect genuine manual text and edition identity; exclude partial downloads and image-only formulas.',
            'Compare imputation model compatibility, covariance, sampling units, target support and refusal behavior.',
            'Review exact observed-law counterexamples and conditional transport derivation before manuscript integration.',
            'Keep incomplete discovery inconclusive and continue independent eligible operations.']))
    a='network-v2';d='details-network';f='assumptions-network'
    sources=[
        source('stata_mi',a,'pdf','Stata mi: introduction and data styles','StataCorp',
            'Official manual; PDF creation28July2026; r19 examples; exact licensed build unresolved',[(120,156)],
            ['Four formats preserve original m=0 and imputed m=1..M; variables have imputed/passive/regular roles.',
             'Extended missing values .a through .z persist as hard missing in this documented profile.']),
        source('stata_substantive',d,'pdf','Stata: introduction to multiple-imputation analysis','StataCorp',
            'Official manual; PDF metadata28July2026; r19 examples',[(190,308),(550,580)],
            ['Proper imputation and valid completed-data inference are required; imputer/analyst mismatch matters.',
             'MAR plus parameter distinctness supports ignorability; MAR cannot be distinguished from MNAR using only missing values that remain unobserved.',
             'Number of imputations affects simulation stability; default recommendations are not universal adequacy guarantees.']),
        source('stata_estimate',d,'pdf','Stata mi estimate: estimation using multiple imputations','StataCorp',
            'Official manual; PDF metadata28July2026; r19 examples',[(201,237),(257,282),(1219,1280)],
            ['Combines per-imputation coefficients and covariance; total covariance equals within plus (1+1/M) times between.',
             'Documents large- and small-complete-sample degrees of freedom and survey-prefix route.',
             'Default stops on failed estimation or varying sample; errorok and esampvaryok change this behavior.',
             'Exponentiated display follows coefficient-scale pooling; transformed-estimand requests require their own declaration.']),
        source('stata_chained',d,'pdf','Stata mi impute chained: chained-equation imputation','StataCorp',
            'Official manual; PDF metadata28July2026',[(155,190),(228,230),(299,401)],
            ['Conditional equations need not correspond to a common joint distribution.',
             'Default burn-in10 and order from most to least observed require diagnostics; iteration count alone does not prove convergence or model validity.',
             'Perfect prediction raises an error unless explicit augmentation is requested; traces and separate conditional specifications can be retained.']),
        source('spss_missing',a,'pdf','IBM SPSS Missing Values 31','IBM',
            'Title/edition31.0.2; PDF creation2January2026; acquired21October2026',[(1,20),(350,418),(488,610),(649,748)],
            ['Imputation accepts analysis weights but does not explicitly handle strata/clusters; automatic Complex Samples analysis of MI data is not supported in this manual.',
             'Exact reproduction requires seed, case order, variable order and settings.',
             'Automatic monotone/FCS, ten default FCS iterations, optional PMM k5 and categorical interactions are documented.',
             'Imputation_0 identifies original data; split/group identity controls MI interpretation.',
             'Naive pooling supplies only parameter output; univariate pooling adds uncertainty when supported; unsupported procedures return no pooled output.',
             'Hard bounds cause redraws; variable exclusion changes predictors and imputed variables.']),
        source('sas_mi_intro',d,'html','SAS/STAT 14.1: MI procedure overview','SAS Institute',
            'HTML title14.1; publication date not established; accessed21October2026',[(15,84)],
            ['Generation, complete-data analysis and combination are distinct phases.',
             'Monotone methods, arbitrary-pattern normal MCMC and FCS differ in assumptions.',
             'High relative efficiency at small M does not ensure stable confidence intervals or p-values; analyst/imputer compatibility remains relevant.']),
        source('sas_mianalyze_intro',d,'html','SAS/STAT 14.1: MIANALYZE procedure overview','SAS Institute',
            'HTML title14.1; publication date not established; accessed21October2026',[(15,42)],
            ['Combines per-imputation parameter estimates with SE or covariance; multivariate Wald inference requires an additional covariance assumption.',
             'Parameter definitions, CLASS interpretation and special transformations require explicit treatment.']),
        source('sas_assumptions',f,'html','SAS/STAT 14.1: statistical assumptions for multiple imputation','SAS Institute',
            'HTML title14.1; publication date not established; accessed21October2026',[(15,30)],
            ['MAR is distinct from MCAR; MAR plus distinct data/missingness parameters defines ignorability in the documented setting.',
             'This procedure profile imposes normality for specified regression/MCMC methods; no universal distribution-free validity follows.']),
        source('sas_combining',f,'html','SAS/STAT 14.1: combining inferences from multiply imputed data','SAS Institute',
            'HTML title14.1; publication date not established; accessed21October2026',[(15,32)],
            ['Primary prose distinguishes within, between and total variance, finite-M t approximation and small complete-sample degrees of freedom.',
             'Image-only equations are omitted from this source inspection; numerical formulas are grounded in the separately inspected Stata manual.']),
        source('sas_sensitivity',f,'html','SAS/STAT 14.1: sensitivity analysis for the MAR assumption','SAS Institute',
            'HTML title14.1; publication date not established; accessed21October2026',[(15,42)],
            ['Documents pattern-mixture sensitivity in MI and explicitly excludes the selection-model approach from that procedure profile.',
             'Changing conclusions across MNAR scenarios diagnoses assumption sensitivity; it does not identify which missingness law generated unobserved outcomes.'])]
    sources.append(dict(integrated_citation_key='exec21_transport_reference',kind='project_authored_exact_reference',
        title='Exact missingness, imputation compatibility and branch-transfer references',author='Causal banking proposal project',year=2026,
        source_identity='tools/transport_missingness_reference_20261021.py',version_date='21 October 2026; exact authored laws',
        local_copy=ref(ROOT/'tools/transport_missingness_reference_20261021.py','calculate() rational enumeration'),
        inspected_anchors=[dict(anchor='calculate()',inspection='Population reweighting, identical observed laws, pooling algebra and stationary scan distributions')],
        supported_claims=['Composition changes effects6 to-6 and cost2 margins4 to-8; nonoverlap gives target bounds[-6,10].',
            'The same observed response law has effects0 or10 and cost4 margins-4 or6; delta sensitivity reaches zero margin at-12.',
            'Three imputation estimates0,2,4 and within variance1 give between4, total19/3 and large-complete-sample df361/128.',
            'Odds ratios1 and9 have geometric mean3 and arithmetic mean5; pooling scale matters.',
            'Incompatible binary full conditionals have scan-specific stationary laws(3,1,1,3)/8 and uniform quarters.'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,cutoff='2026-10-07',limitations=LIMITS))
    write(BASE/'exact-results.json',exact.calculate())
    specs=[
        ('Stata','mi; mi impute chained; mi estimate','Four selected originals',
         'Match licensed release, full method and survey/multilevel imputation specifications, terms and native outputs.'),
        ('SAS','SAS/STAT14.1 PROC MI and MIANALYZE; later15.1 PDF leads','Five selected14.1 originals;15.1 incomplete',
         'Recover complete selected-release manuals, MNAR syntax, image equations, sampling design requirements and deployment rights.'),
        ('IBM SPSS','Statistics31.0.2 Missing Values; Multiple Imputation; MVA','One selected complete manual',
         'Inspect algorithm/syntax originals, pooling transforms and complex-design workarounds; verify edition entitlements and native exports.'),
        ('EViews','Missing-value, state-space, forecasting and sample-selection candidates','Unresolved for this cell',
         'Locate exact missing-data and transport estimand technical originals; interpolation or complete-case regression is insufficient evidence.'),
        ('Mplus','Missing-data likelihood, auxiliary variables and multiple-imputation candidates','Unresolved for this cell',
         'Acquire versioned user guide and estimator-specific missingness/selection assumptions, pooling rules and license terms.'),
        ('Commercial graphical tools','HUGIN and GeNIe/SMILE selection, evidence and population candidates','Unresolved for this cell',
         'Recover primary missing-data learning and selection/transport semantics; conditioning in a supplied graph does not establish transport identification.')]
    candidates=[dict(family=family,aliases=aliases,status=status,next_public_evidence=action,
        absence_claim=False,runtime_executed=False,price=None,entitlement_verified=False) for family,aliases,status,action in specs]
    write(BASE/'candidate-register.json',dict(cutoff='2026-10-07',candidates=candidates,
        stopping_rule='Inspect these ten complete official originals across three product profiles; retain six-family leads and incomplete complementary searches.',
        market_census_complete=False,search_attempt=ref(BASE/'search-attempt.json','Unusable search interface, not no-hit evidence')))
    failures=[ref(p,'Unsuccessful or incomplete acquisition; no technical claim') for p in sorted(BASE.glob('acquisition/**/*.receipt.json')) if read(p)['returncode']!=0]
    write(BASE/'omissions-register.json',dict(global_blocker=False,failures=failures,
        candidates=[dict(family=c['family'],next_action=c['next_public_evidence']) for c in candidates],
        additional=['Complete market discovery, cutoff-era bytes and publisher technical replacements for failed originals.',
            'SAS image-only equations and MNAR syntax; IBM original algorithms/syntax and fresh rendered inspection.',
            'Native estimator/export trials, supported imputation-target combinations, distribution rights and measured costs.',
            'Scientific transportability, response positivity and MNAR restrictions in each proposed banking use.'],
        bank_inputs_required_for_next_public_work=False))
    write(BASE/'conversion-contract.json',dict(status='proposed_not_implemented',integration_allowed=False,
        requirements=['Bind source and target population, unit/outcome horizon, action timing and pre-action covariates.',
            'Preserve missingness reason/indicator and observed values; distinguish structural missing, censoring and ordinary unavailable values.',
            'Retain m=0, unit IDs, imputation IDs, role types, category levels, passive transforms, weights and sampling design.',
            'Preserve imputer/analyst models, interactions, software release, seed, case/variable order, diagnostics and all failures.',
            'Specify estimand scale; retain every completed-data estimate and full covariance before pooling.',
            'Distinguish within/between/total covariance, finite-M simulation error and missingness/transport sensitivity.',
            'Document exchangeability, treatment/response/source support and conditional population invariance; weights alone do not prove them.',
            'Refuse undeclared sample or coefficient changes, absent covariance, unsupported targets and structural nonoverlap; preserve partial identification when justified.',
            'Expose identical meaning through library, CLI and MCP; an agent proposes assumptions for review, never infers MAR from unavailable outcomes.',
            'Freeze public known-law comparisons and matching targets before native trials; bank trials follow demonstrated public merit.']))
    evidence=[ref(BASE/n,'Reviewed commercial missingness evidence') for n in ['plan.md','plan-review.json','source-audit.json',
        'candidate-register.json','omissions-register.json','conversion-contract.json','exact-results.json','spss-extraction-review.json']]
    evidence.append(ref(Path(__file__),'Exact review construction'))
    findings=[('inconclusive','Six candidate families/aliases are explicit; complementary search and exact product matching remain incomplete.'),
        ('pass','Ten complete official originals have local bytes, hashes, version/date limits and inspected technical anchors; formulas use the readable Stata original.'),
        ('pass','Failed originals, alternatives and unresolved rights/coverage remain explicit; no absence finding or source waiver.')]
    scope='Commercial missingness and target-population proposal comparison with selected primary evidence'
    item=dict(operation_id=OP,status='inconclusive',scope=scope,reviewer=REVIEWER,candidates=candidates,
        criteria=[dict(index=i,verdict=v,finding=f) for i,(v,f) in enumerate(findings)],
        evidence=evidence,limitations=LIMITS,capabilities=[],integration_allowed=False)
    write(output,item);write(BASE/'review.json',item)
    write(BASE/'operation-receipt.json',receipt(OP,output,evidence,findings,scope))
    verify_bindings(item)
    print(json.dumps(dict(operation=OP,outcome='inconclusive',official_originals=10,candidates=6)))


def compare():
    output=ROOT/f'docs/program/comprehensive-v14/work/{COMPARE}/vendor-comparison.json'
    assert not output.exists()
    facts={
        'Stata':('Explicit MI data roles, FCS diagnostics, coefficient/covariance pooling and sample guards.',
            'Proposal lacks a qualified native MI worker and full survey/model compatibility; adopt isolated licensed execution only after target-specific public tests.'),
        'SAS':('Monotone/MCMC/FCS imputation, MIANALYZE and documented pattern-mixture sensitivity.',
            'Proposal must preserve selected-release semantics and sensitivity parameters; image equations, exact runtime and rights remain unresolved.'),
        'IBM SPSS':('Interactive missingness analysis, imputation roles/constraints and output-specific pooling.',
            'Proposal needs reproducible export with unit/imputation identity and pooling levels; analysis weights alone do not support complex-design uncertainty.')}
    rows=[]
    for c in read(BASE/'candidate-register.json')['candidates']:
        strength,gap=facts.get(c['family'],('Not evaluated for this precise target; no absence finding.',c['next_public_evidence']))
        rows.append(dict(family=c['family'],selected_profile=c['aliases'],source_status=c['status'],
            documented_strength=strength,matched_proposal_comparison='Compare fixed target, missingness assumptions, completed-data covariance and failure handling.',
            observed_current_capability='Exact authored laws and interface requirements only; no vendor adapter qualification.',
            proposed_capability='Explicit missingness and transport assumptions, population support and typed uncertainty through library/CLI/MCP.',
            remaining_gap=gap,next_public_evidence=c['next_public_evidence'],deployment_rights='Unverified; public documentation grants no runtime redistribution entitlement.',
            price=dict(status='unavailable',amount=None,quote_obtained=False),runtime_executed=False,absence_claim=False))
    evidence=[ref(BASE/n,'Reviewed commercial comparison') for n in ['source-audit.json','review.json','candidate-register.json',
        'omissions-register.json','conversion-contract.json','exact-results.json']]+[ref(Path(__file__),'Comparison construction')]
    findings=[('inconclusive','Three selected technical profiles support comparison; three other families, complete search, product builds and rights remain unresolved.'),
        ('pass','Every row distinguishes documented features, proposed behavior, unavailable prices and unexecuted trials; no contact or absence finding is claimed.')]
    scope='Six-family commercial missingness comparison; no general transport or runtime qualification'
    item=dict(operation_id=COMPARE,status='inconclusive',scope=scope,reviewer=REVIEWER,vendors=rows,
        criteria=[dict(index=i,verdict=v,finding=f) for i,(v,f) in enumerate(findings)],evidence=evidence,
        limitations=LIMITS,capabilities=[],integration_allowed=False,purchases=False,vendor_contacts=False,matched_runtime_trial=False)
    write(output,item);write(BASE/'comparison-review.json',item)
    write(BASE/'comparison-receipt.json',receipt(COMPARE,output,evidence,findings,scope));verify_bindings(item)
    print(json.dumps(dict(operation=COMPARE,outcome='inconclusive',families=6,documented_profiles=3)))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['coverage','compare'])
    {'coverage':coverage,'compare':compare}[p.parse_args().command]()

#!/usr/bin/env python3
"""Bind authored primary-text inspections without rewriting the V12 survey."""
import copy
import json
from pathlib import Path

import master_control as core

ROOT=core.ROOT
BASE=ROOT/'docs/program/gap-repair-v13'
OUT=BASE/'work/SW01'
OLD=ROOT/'docs/program/repair-v12/work/SW01'

# These are scoped source/document inspections, not results of package execution.
REVIEWS={
 'lingam': {
  'name':'LiNGAM','candidate':'seed:072','dimension':'Python',
  'cells':['discovery_iid::Python'], 'anchors':[(25,64),(66,123)],
  'claims':['DirectLiNGAM accepts hard/soft prior knowledge, pwling/kernel/pwling_fast measures and adaptive-Lasso choice.',
            'fit validates prior shape, iteratively residualizes variables, stores a selected causal order and calls adjacency estimation.'],
  'license':'MIT text inspected',
  'limits':['Selected DirectLiNGAM entry only; no VAR, hidden-confounder or full-family review.',
            'A selected order is not a graph confidence region; inherited base estimation and runtime remain unqualified.'],
  'decision':'Candidate Python adapter for a declared linear non-Gaussian discovery regime; defer porting until full dependency/license and behavioral review.',
  'alternative':'Compare constraint-based CPDAG/PAG engines under their own assumptions; do not rank a selected DAG against an equivalence class without a common target.',
  'bank_case':'Discovery of contemporaneous funding-rate responses with explicit assumptions on hidden common causes and time aggregation.',
  'next':'Inspect base adjacency/total-effect routines, prior path orientation, VAR paths, bootstrap semantics and adversarial latent/Gaussian examples.'},
 'y0': {
  'name':'y0','candidate':'seed:071','dimension':'Python',
  'cells':['identification_counterfactual::Python'],'anchors':[(1,14),(43,81)],
  'claims':['identify_outcomes accepts an acyclic directed mixed graph and treatment/outcome/optional conditioning variables.',
            'It dispatches to ID without conditions and IDC with conditions, and catches Unidentifiable to return None unless strict=True.'],
  'license':'BSD three-clause text inspected',
  'limits':['Dispatch source does not establish ID/IDC implementation correctness or complete counterfactual coverage.',
            'A symbolic expression is not a numerical estimate; nonidentification must remain distinct from unsupported operation or execution failure.'],
  'decision':'Candidate symbolic identification adapter; preserve expression/graph identities and strict failure semantics. Direct algorithm port is not justified by this review.',
  'alternative':'Compare general symbolic identification with adjustment-only graph tools and other ID implementations on identical graphs/queries.',
  'bank_case':'Determine whether a proposed retention intervention can be identified when satisfaction is an unobserved common cause.',
  'next':'Inspect id_std/id_c, graph validation, expression serialization, hedge/failure paths and independent small-graph oracles.'},
 'delicatessen': {
  'name':'delicatessen','candidate':'seed:074','dimension':'Python',
  'cells':['effects_heterogeneity::Python','iv_rd_design::Python'],'anchors':[(703,771),(854,894),(900,920),(1014,1027)],
  'claims':['ee_aipw stacks average-effect, two potential-outcome mean and propensity/outcome model estimating equations into a (3+b+c)-by-n array.',
            'The implementation explicitly clips propensity probabilities when requested and chooses binary/logistic versus continuous/linear outcome regression.',
            'The module also exposes instrumental-variable and two-stage least-squares estimating-equation entry points; their full numerical behavior is not inspected here.'],
  'license':'MIT text inspected',
  'limits':['An estimating-equation array is not a fitted estimator or independently verified uncertainty result.',
            'Sandwich construction, solver convergence, clustering, longitudinal targets and nuisance-rate claims need separate review.'],
  'decision':'Candidate numerical equation/reference integration for explicit estimating functions; defer adoption of inferential defaults pending solver and covariance review.',
  'alternative':'Compare with statsmodels joint-GMM treatment effects and target-specific TMLE implementations under matched targets and sampling units.',
  'bank_case':'Estimate average renewal-offer effect while retaining the nuisance-model equations needed for uncertainty.',
  'next':'Inspect MEstimator, sandwich differentiation, finite-sample correction and dependent-data limitations; execute matched equation/root references later.'},
 'pygformula': {
  'name':'pygformula','candidate':'seed:073','dimension':'Python',
  'cells':['longitudinal_survival::Python','policies_offpolicy::Python'],'anchors':[(48,159),(490,521),(650,731)],
  'claims':['ParametricGformula documents individual/time identities, time-varying covariate models, histories, custom fits/predictions and intervention descriptions.',
            'Outcome types include survival, continuous end-of-follow-up and binary end-of-follow-up; competing events and censoring have separate options.',
            'nsamples defaults to zero; the fit path invokes separate Bootstrap work for requested bootstrap replicates.'],
  'license':'MIT text inspected',
  'limits':['Main-class inspection does not verify simulation, resampling unit, competing-risk identification or interval calibration.',
            'Regime evaluation does not establish optimal policy learning; a covariate-history API does not certify sequential exchangeability.'],
  'decision':'Candidate Python longitudinal-regime adapter after intervention/time/competing-event contracts and bootstrap internals are reviewed.',
  'alternative':'Compare R g-formula, longitudinal TMLE and weighting approaches on the same histories, interventions, censoring and target horizon.',
  'bank_case':'Sequential servicing actions with delinquency histories, default as a competing event and observed account closure.',
  'next':'Inspect simulate/Bootstrap/intervention helpers, resampling identity, horizon conventions and truncation diagnostics.'},
 'statsmodels': {
  'name':'statsmodels','candidate':'seed:076','dimension':'Python',
  'cells':['effects_heterogeneity::Python','computation_workflow::Python'],'anchors':[(1,29),(735,756),(759,844)],
  'claims':['TreatmentEffect describes IPW, RA, AIPW, AIPW-WLS and IPW-RA with joint-GMM inference.',
            'effect_group distinguishes all, treated and untreated populations; the documented outcome model is linear OLS.',
            'ps_bounds defaults to (0.001,0.999), validates 0<lower<upper<1 and is used to clip predicted selection probabilities.',
            'The class notes state that final GMM inference corresponds to HC0 regardless of the internal _cov_type keyword; the early module comment about missing standard errors is not an adequate current contract.'],
  'license':'BSD three-clause text inspected',
  'limits':['This single module does not establish statsmodels panel/time-series/IV coverage.',
            'HC0 is not a dependence-robust bank panel covariance; no inference/runtime qualification performed.'],
  'decision':'Candidate joint-GMM point-treatment baseline with explicit population and clipping settings; refuse silently translating an internal covariance option into a clustered-inference claim.',
  'alternative':'Match delicatessen estimating equations and target-specific doubly robust implementations before comparing timing or intervals.',
  'bank_case':'Point-in-time retention offer, distinguishing all eligible customers from treated customers.',
  'next':'Trace exact GMM covariance and each estimator, inspect clipping impact and test population/parameter-label roundtrips.'},
 'grf': {
  'name':'grf','candidate':'inherited:grf','dimension':'R',
  'cells':['effects_heterogeneity::R'],'anchors':[(1,26),(30,78),(153,192)],
  'claims':['causal_forest documentation distinguishes binary-treatment CATE from the continuous-treatment conditional covariance/variance target.',
            'The interface exposes nuisance predictions, clustering, equal cluster weighting, honesty, subsampling, grouped confidence-interval trees, tuning and a C++ RNG seed.',
            'The selected wrapper validates clusters/sample weights and defaults to honesty=True, 2000 trees and no tuning.'],
  'license':'Repository COPYING contains GPL version 3; dependency and file-specific scope still require review',
  'limits':['R wrapper inspection is not native C++ source qualification or proof of causal identification.',
            'A continuous covariance slope is not generally a finite dose contrast; CATE and population average effects are distinct.'],
  'decision':'Prefer candidate R/native integration over a rewrite; defer any port or distribution decision until full license and ABI review.',
  'alternative':'Compare matched heterogeneous-effect targets with DML/TMLE or other forest estimators, not prediction accuracy alone.',
  'bank_case':'Heterogeneous offer response versus the effect of increasing a continuous funding incentive by one specified amount.',
  'next':'Inspect native training/prediction/variance and aggregation code; compare cluster weighting and finite dose queries explicitly.'},
 'mossspider': {
  'name':'MossSpider','candidate':'v13:mossspider','dimension':'Python',
  'cells':['networks_interference::Python'],'anchors':[(19,63),(134,190)],
  'claims':['NetworkTMLE documents expected incidence under a treatment plan with Monte Carlo averaging for stochastic allocations and direct-contact interference.',
            'The constructor rejects noninteger node identities, self-loops and nonbinary exposure, remaps identities and builds an unweighted adjacency matrix.',
            'The documentation disclaims a missing-data procedure, describes degree restrictions and gives a directed influence convention opposite the graph arrow.'],
  'license':'MIT text inspected',
  'limits':['Documentation describes an undirected input while also giving a directed convention; the selected constructor contains directed handling. Directed semantics need explicit runtime review.',
            'Arbitrary contagion, weighted/dynamic networks, missing ownership and variance validity are not established.'],
  'decision':'Candidate restricted network-policy adapter, subject to explicit graph direction, identity and exposure-map conformance; do not adopt as a general banking network engine.',
  'alternative':'Compare individual-network mapping with inferference grouped allocation policies under an actually shared estimand.',
  'bank_case':'Borrower-group outreach with immediate-neighbor spillovers, where relationship direction and exposure are owned definitions.',
  'next':'Inspect fit, targeting, exposure mapping, stochastic integration and variance; resolve directed documentation inconsistency.'},
 'causalgps': {
  'name':'CausalGPS','candidate':'v13:causalgps','dimension':'R',
  'cells':['effects_heterogeneity::R'],'anchors':[(1,31),(44,114)],
  'claims':['estimate_gps constructs observed continuous-exposure generalized propensity scores with normal or kernel options and a SuperLearner library choice.',
            'The normal path uses fitted exposure mean and a residual standard deviation in dnorm; the kernel path estimates residual scaling and calls compute_density.',
            'The output includes identity, exposure, gps, predicted mean/scale and residual fields; this function alone does not fit a dose-response outcome.'],
  'license':'DESCRIPTION declares GPL-3, version 0.5.1, published 11 January 2026',
  'limits':['Helper functions, density scaling, matching/weighting, outcome inference and overlap qualification remain uninspected.',
            'A conditional density is not a binary treatment probability; the observed-density output alone cannot establish a finite dose effect.'],
  'decision':'Candidate GPS construction component; defer complete causal-estimation adoption until downstream matching/outcome and density contracts are reviewed.',
  'alternative':'Compare with causaldrf full response-surface construction and grf continuous slope only after aligning the target.',
  'bank_case':'Construct support diagnostics for a continuous retention incentive conditional on pre-offer customer characteristics.',
  'next':'Inspect compute_density and exposure evaluation at counterfactual doses, balance diagnostics and full license/dependency terms.'},
 'causaldrf': {
  'name':'causaldrf','candidate':'v13:causaldrf','dimension':'R',
  'cells':['effects_heterogeneity::R'],'anchors':[(1,88)],
  'claims':['hi_est documentation describes fitting a treatment model, a GPS-adjusted outcome response surface and averaging predicted outcomes at a requested dose grid.',
            'Documented treatment distributions include Normal, LogNormal, transformed normal, Poisson, negative binomial, Gamma and Binomial; output includes parameter, treatment-model and outcome-model records.'],
  'license':'DESCRIPTION declares MIT + file LICENSE, version 0.4.2; accompanying LICENSE file not yet inspected',
  'limits':['This review supports the documented target and interface, not algorithm correctness or interval implementation.',
            'A mean outcome at a dose is not an effect contrast until a comparator dose is specified; the MIT notice requirement remains unresolved.'],
  'decision':'Candidate response-surface reference/adapter; defer license clearance and runtime qualification pending LICENSE and full function review.',
  'alternative':'Compare CausalGPS density construction plus downstream outcome estimation and grf local slope under matched banking queries.',
  'bank_case':'Compare expected net retained deposits at two feasible incentive levels instead of reporting an unlabeled curve ordinate.',
  'next':'Inspect function body, treatment-model helpers, support and interval procedures, and the accompanying LICENSE notice.'},
 'inferference': {
  'name':'inferference','candidate':'v13:inferference','dimension':'R',
  'cells':['networks_interference::R'],'anchors':[(1,83),(102,178)],
  'claims':['interference uses grouped formulas and allocation probabilities with glm/glmer/HLfit/oracle propensity choices and an IPW causal-estimation path.',
            'The code checks group count, allocation range, variance option and a single-random-effect limitation of the default logit integrand.',
            'Documentation gives integrate_allocation default FALSE while the inspected function signature sets TRUE; adapters must freeze an explicit setting.'],
  'license':'DESCRIPTION declares GPL (>=2), version 1.0.3, published 15 May 2025',
  'limits':['Grouped partial-interference workflow is not a general dynamic financial network model.',
            'Naive/robust labels do not establish uncertainty validity under arbitrary dependent groups; integrands/variance/runtime need review.'],
  'decision':'Candidate grouped-allocation reference with explicit integration/default settings and group sampling contract.',
  'alternative':'Compare MossSpider network mapping only where target populations, allocation policies and dependence assumptions coincide.',
  'bank_case':'Branch or household-group encouragement with within-group spillovers and independently justified group sampling.',
  'next':'Inspect numerical integrands, weight derivatives and variance, pin dependency versions, and test unequal groups and boundary allocations.'}
}


def binding(path,anchor):return {'path':str(path.relative_to(ROOT)),'sha256':core.sha(path),'anchor':anchor}


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    entries=[]
    identities={r['name']:r for r in json.loads((BASE/'source-identities.json').read_text())}
    for key,data in REVIEWS.items():
        text_path=ROOT/'docs/literature/raw'/('v12_gap3_'+key+'_technical.txt')
        license_path=ROOT/'docs/literature/raw'/('v12_gap3_'+key+'_license.txt')
        receipt=json.loads(text_path.with_suffix('.receipt.json').read_text())
        license_receipt=json.loads(license_path.with_suffix('.receipt.json').read_text())
        assert core.sha(text_path)==receipt['sha256'] and core.sha(license_path)==license_receipt['sha256']
        identity=identities[key]
        assert identity['commit'] in receipt['url'] and identity['date'][:10]<='2026-10-07'
        entry={'id':'v13:'+key,'citation_key':'v13_sw_'+key,'kind':'software_source','name':data['name'],
               'candidate_id':data['candidate'],'source_identity':receipt['url'],
               'version_date':{'commit':identity['commit'],'commit_date':identity['date'],'retrieved':receipt['accessed_utc']},
               'identity_evidence':binding(ROOT/identity['identity_source'],'Saved commit identity; not a capability claim'),
               'local_copy':binding(text_path,'Selected technical source'),
               'inspected_anchors':[binding(text_path,f'lines {lo}-{hi}') for lo,hi in data['anchors']],
               'supported_claims':data['claims'],'limits':data['limits'],
               'license':{'finding':data['license'],'evidence':binding(license_path,'Inspected license text or explicit DESCRIPTION declaration'),
                          'source_url':license_receipt['url'],'clearance':'not_full_dependency_or_distribution_clearance'},
               'decision':{'status':'provisional_not_SW07_acceptance','recommendation':data['decision'],
                           'alternative':data['alternative'],'bank_case':data['bank_case'],'revisit_trigger':data['next']},
               'coverage_cells':data['cells'],'runtime_status':'not_executed','reviewer':'Current author; not independent acceptance'}
        entries.append(entry)
    audit={'task_id':'SW01','status':'partial_primary_source_reviews','cutoff':'2026-10-07',
           'predecessor':binding(OLD/'source-audit.json','Preserved V12 source audits'),
           'new_entries':entries,'counts':{'new_package_reviews':len(entries),'technical_texts':10,'license_or_metadata_texts':10},
           'limits':['Selected source paths only; source inspection is not a package benchmark.',
                     'No exhaustive cell closure; commercial originals and full search remain incomplete.']}
    core.write(OUT/'source-audit.json',audit)
    matrix=copy.deepcopy(json.loads((OLD/'coverage-matrix.json').read_text()))
    byid={c['id']:c for c in matrix['cells']}
    for e in entries:
        for cell_id in e['coverage_cells']:
            c=byid[cell_id];c.setdefault('successor_inspections',[]).append(e['id'])
            c['status']='partial_primary_inspection';c['closure_qualified']=False
            c['successor_finding']='; '.join(e['supported_claims'])
            c['successor_remaining']=e['decision']['revisit_trigger']+' Full cell search and alternatives remain open.'
    partial=sum(bool(c.get('individual_review') or c.get('successor_inspections')) for c in matrix['cells'])
    matrix.update(predecessor=binding(OLD/'coverage-matrix.json','Preserved V12 coverage matrix'),
                  individually_partially_reviewed_cells=partial,remaining_individual_review_cells=102-partial,
                  qualified_cell_count=0,warning=f'{partial} partial individual cells; none closed. No benchmark or exhaustive search inferred.')
    core.write(OUT/'coverage-matrix.json',matrix)
    catalog=copy.deepcopy(json.loads((OLD/'catalog.json').read_text()))
    ids={r['id'] for r in catalog['candidates']}
    for k,d in REVIEWS.items():
        if d['candidate'] not in ids:
            catalog['candidates'].append({'id':d['candidate'],'name':d['name'],'areas':[c.split('::')[0] for c in d['cells']],
               'dimension':d['dimension'],'role':'causal_method_candidate','technical_status':'selected_primary_text_inspected_v13',
               'runtime_status':'not_run','version':identities[k]['commit']})
        for c in catalog['candidates']:
            if c['id']==d['candidate']:c['successor_review']='v13:'+k
    catalog['successor_counts']={'catalog_rows':len(catalog['candidates']),'new_candidates':len(catalog['candidates'])-len(ids),'new_reviews':10}
    catalog['warning']='Rows include leads and aliases; not a count of distinct adopted or fully reviewed packages.'
    core.write(OUT/'catalog.json',catalog)
    lines=['# Ten pinned software source inspections','',
           'These authored technical reviews supplement the preserved V12 register. They support selected claims only; no package was executed and no coverage cell is closed.','']
    for e in entries:
        lines += ['## '+e['name'],'',f"Commit `{e['version_date']['commit']}` dated {e['version_date']['commit_date']}. Inspected {e['local_copy']['path']} and the bound licensing record.",'']
        lines += [p+'\n' for p in e['supported_claims']]
        lines += [e['decision']['bank_case']+' '+e['decision']['recommendation'],'',e['decision']['alternative'],'',
                  'Limitations: '+' '.join(e['limits']),'','Licensing: '+e['license']['finding']+'.',
                  '', 'Next: '+e['decision']['revisit_trigger'],'']
    (OUT/'dossiers.md').write_text('\n'.join(lines))
    print(json.dumps({'new_reviews':10,'catalog_rows':len(catalog['candidates']),
                      'partial_cells':partial,'unreviewed_cells':102-partial,'closed_cells':0}))


if __name__=='__main__':main()

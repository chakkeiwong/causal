#!/usr/bin/env python3
"""Prepare the native temporal comparison and conditional reuse contract."""
from fractions import Fraction as F
import itertools
import json
import math
from pathlib import Path

import review_cxx_temporal_20261016 as work
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT, BASE = work.ROOT, work.BASE


def independent():
    expected=json.loads((BASE/'exact-results.json').read_text())
    assert work.exact()==expected
    # Enumerate the intermediate state, instead of using one scalar recursion.
    first={'C':F(9,10),'D':F(1,10)}
    correct={'C':F(1,10),'D':F(4,5)}
    copied={'D':F(1,10),'C':F(4,5)}
    paths=[{'intermediate':s,'probability':str(w),'correct_joint_D':str(w*correct[s]),
            'copied_joint_D':str(w*copied[s])} for s,w in first.items()]
    totals=[sum(F(row[k]) for row in paths) for k in ['correct_joint_D','copied_joint_D']]
    assert [str(x) for x in totals]==[expected['state_order']['correct_two_step'],expected['state_order']['blind_parent_index_copy_two_step']]
    # A covariance calculation as a linear map of independent innovations.
    def covariance(A,v):
        return [[sum(A[i][k]*v[k]*A[j][k] for k in range(2)) for j in range(2)] for i in range(2)]
    w1=covariance([[F(1),F(0)],[F(1,2),F(1)]],[F(1),F(3,4)])
    w2=covariance([[F(1),F(1,2)],[F(0),F(1)]],[F(3,4),F(1)])
    assert w1==w2==[[F(v) for v in row] for row in expected['regimes']['observational_covariance']]
    shocks=list(itertools.product([-1,1],repeat=3))
    variance=sum(F(sum(s),3)**2 for s in shocks)/len(shocks)
    assert variance==F(expected['windows']['true_mean_variance'])
    score_delta=-2*(1+math.log(2))+2*(1+math.log(102))
    assert abs(score_delta-float(expected['intercept']['difference_decimal']))<1e-12
    return {'status':'pass','reviewer':work.REVIEWER,'scope':'Separate author arithmetic formulation, not external acceptance',
        'prior_review':ref(BASE/'independent-arithmetic-review.json','Preserved initial exact-formula report'),
        'review_correction':'The initial report used path-enumeration wording although its code evaluated the two-term recursion directly. This successor actually enumerates intermediate-state paths and independently checks linear-map covariance.',
        'paths':paths,'covariance_linear_map':[[str(v) for v in row] for row in w1],
        'subject_variance':str(variance),'double_precision_score_difference':score_delta,
        'evidence':[ref(Path(__file__),'Executed independent function'),ref(BASE/'exact-results.json','Compared authored results')]}


def main():
    primary=json.loads((BASE/'source-review.json').read_text());omitted=json.loads((BASE/'omissions-register.json').read_text())
    verify_bindings(primary);verify_bindings(omitted)
    assert len(primary['records'])==38 and len(omitted['leads'])==30
    write(BASE/'independent-verification-v2.json',independent())
    contract={'status':'proposed_not_implemented','integration_allowed':False,
        'request':['Target population and monetary decision','Subject/cluster/calendar sampling law',
            'Event,availability and decision clocks;physical period and lag','Intervention kind,known targets and regime-to-row map',
            'State labels with ordered dictionaries and units','Constraint predicates,graph class,score/intercept and search options'],
        'response':['Candidate/essential/representative/fitted-model identity','Uncertainty scope and unresolved assumptions',
            'Finite numerical output plus diagnostics','Source/configuration and conversion identities'],
        'failure_states':['invalid_clock_or_state_map','contradictory_constraints','unsupported_intervention_or_sampling_law',
            'unresolved_identification','numerical_failure','transport_failure','computed_under_stated_assumptions'],
        'decisions':[
            {'family':'pcalg','choice':'conditional_R_bridge','adoption_enabled':False,
             'reason':'Preserve native known-target score with existing R preprocessing;standalone extraction adds Rcpp/callback,dependency and rights work',
             'repairs':['Explicit intercept;integer IDs before coercion','Stable inverse row permutation and target mapping',
                'Essential graph versus representative','Hard-constraint postvalidation;finite-score guards','Independent-row premises or a separately justified dependent procedure']},
            {'family':'aGrUM','choice':'conditional_supplied_model_adoption','adoption_enabled':False,
             'reason':'Python unrolling helper over native engine; selected path supplies no discovery claim',
             'repairs':['Complete paired slices','Ordered state labels and CPT-axis permutation','Independent finite-model oracle','File/dependency rights closure']},
            {'family':'Mocapy++','choice':'reference_for_inference_reject_as_selected_structure_learner','adoption_enabled':False,
             'reason':'Manual explicitly excludes structure learning;latent masks and EM have supplied-model meaning',
             'repairs':['Resolve mirror provenance','Resolve LGPL2.1 root versus LGPL3-or-later inspected headers',
                'Freeze compiler/Boost/LAPACK/Fortran environment','Compare modernization cost with permitted alternatives']},
            {'family':'sDBN','choice':'reference_pending_terms_and_prototype','adoption_enabled':False,
             'reason':'Native temporal training is present but no README/LICENSE appears in complete54-blob tree',
             'repairs':['Obtain applicable reuse terms','Preserve subjects and physical calendars through rolling',
                'Distinguish regularized allowed pairs from directed result','Test reversed-pair constraint membership and supplied-graph validity',
                'Use dedicated result channel and strict parse','Replace machine include path and freeze dependencies/compiler flags',
                'Bind binary checkpoint version/platform;compare conservative floating-point settings']},
            {'family':'BayesNetty','choice':'constrained_search_reference','adoption_enabled':False,
             'reason':'Inspected static genetic-network search is not qualified for temporal intervention effects',
             'repairs':['Preserve directed bans versus required adjacency','Do not create latent bidirected edges from paired whitelist entries',
                'Trace caller of zero-return loop path before CLI claim','Explicit acyclicity/status;GPL3/dependency closure']}
        ],
        'prototype':{'status':'design_only','scientific_scope':'Known generated regimes and supplied small models before expensive bank trials',
            'cases':['Two Gaussian directions with common observed law and distinct interventions','Intercept defaults and degenerate scores',
                'Regime/row permutation and fractional IDs','Reordered state dictionaries','Repeated subjects and irregular dates',
                'Constraint predicates and forbidden reverse pairs','Mixed diagnostic/result stream and malformed checkpoint'],
            'baseline':ref(BASE/'exact-results.json','Executed authored reference only'),
            'public_roles':'Permitted public credit/mortgage records may supply covariate ranges and calendars;generated actions/responses remain labeled;no authentic intervention truth implied',
            'comparison':'Independent exact reference versus permitted frozen upstream only after environment/rights closure;both receive identical scientific inputs',
            'acceptance':'Freeze tolerance/status/input identities and stopping before any empirical run;keep failures and unavailable requests in denominator',
            'costs':['Data and semantic preparation','Rights/dependency review','Compilation','Conversion',
                'Numerical runtime','Diagnostics and scientific review','Revision and maintenance'],
            'later_bank_trigger':'Useful public/generated prototype result identifies a decision-relevant uncertainty that extra bank information can resolve'},
        'research_limits':['Dependent graph/effect-set uncertainty','Hidden/unknown intervention targets','Latent confounding and stationarity',
            'Useful precision and transport to bank population'],
        'omissions':ref(BASE/'omissions-register.json','All30 returned leads and bounded stopping')}
    write(BASE/'proposed-contract.json',contract)
    text=(BASE/'development.template').read_text().replace('§',chr(92))
    with (BASE/'development.tex').open('x') as f:f.write(text)
    write(BASE/'plan-review.json',{'status':'pass_for_bounded_execution','reviewer':work.REVIEWER,
        'initial_plan':ref(BASE/'plan.md','Five-family source comparison and bounded stopping'),
        'corrections':['One further pinned header was needed to trace the sDBN called search;source sample is38 files plus2 inherited licenses.',
            'Saved summary license shorthand for Mocapy was incomplete;root/file discrepancy is now explicit.',
            'Default result-stream contamination and reversed-pair validation need concrete prototype checks.',
            'Initial independent-report wording is repaired by actual separate enumeration in a successor.'],
        'checks':['No source search hit is a capability claim','No missing license or source is waived',
            'Sampling law,regime and temporal meanings precede performance','Generated/public proposal evidence can proceed independently',
            'No bank evidence,upstream execution or visual review is invented'],
        'evidence':[ref(BASE/'source-review.json','Pinned evidence'),ref(BASE/'independent-verification-v2.json','Independent formulations'),
                    ref(BASE/'proposed-contract.json','Specific reuse and prototype routes')]})
    sources=[]
    for family,pkg in primary['packages'].items():
        records=[r for r in primary['records'] if r['family']==family]
        if family=='agrum':records+=primary['inherited_license_originals']
        claims=[claim for r in records for claim in r.get('supported_claims',r['inspected_anchors'])]
        sources.append({'integrated_citation_key':'exec16_ct_'+family,
            'title':pkg['repository']+' temporal/interventional source and reuse comparison',
            'author':pkg['repository'],'kind':'software_primary_sources','year':int(pkg['source_date'][:4]),
            'source_identity':'https://github.com/'+pkg['repository'],'version_date':pkg['revision']+'; '+pkg['source_date'],
            'local_copy':ref(BASE/'source-review.json','Selected '+family+' records and inspected anchors'),
            'inspected_anchors':claims,'supported_claims':claims,'records':records+[pkg], 'limitations':work.LIMITS})
    for suffix,title,kind,p,claims,records in [
        ('oracle','Exact native-regime,clock,state and constraint references','project_derivation',BASE/'exact-results.json',
         ['Stipulated net6/-4USD;Gaussian equivalence/interventions','RSS8/408 and2log51;three units versus nine rows',
          'State-order .17/.73 and93.2/70.8USD;distinct graph-constraint predicates'],
         [ref(ROOT/'tools/review_cxx_temporal_20261016.py','Exact calculation'),ref(BASE/'independent-verification-v2.json','Separate arithmetic')]),
        ('design','Proposed native temporal reuse,CLI/MCP and public-evidence contract','project_design',BASE/'proposed-contract.json',
         ['Conditional family-specific decisions and explicit failure states','Generated/public prototype and full costs;broader source/rights/research limits'],
         [ref(BASE/'omissions-register.json','Thirty returned leads and remaining candidates'),ref(BASE/'plan-review.json','Reviewed scope and corrections')])]:
        sources.append({'integrated_citation_key':'exec16_ct_'+suffix,'title':title,'author':'Causal banking proposal',
            'kind':kind,'year':2026,'source_identity':'Project-authored proposal evidence','version_date':'2026-10-16',
            'local_copy':ref(p,title),'inspected_anchors':claims,'supported_claims':claims,
            'records':records,'limitations':work.LIMITS})
    write(BASE/'source-audit.json',{'sources':sources,'cutoff':'2026-10-07','prior':ref(work.PRIOR,'649 inherited source records'),
        'primary_review':ref(BASE/'source-review.json','38 new originals,two inherited licenses and genuine paper reread')})
    evidence=[ref(BASE/name,anchor) for name,anchor in [
        ('source-review.json','Pinned authentic sources and primary paper anchors'),('omissions-register.json','Thirty leads and nonexhaustive coverage'),
        ('exact-results.json','Five exact authored reference families'),('independent-verification-v2.json','Separate arithmetic and preserved wording correction'),
        ('proposed-contract.json','Five conditional decisions and proposed prototype'),('plan-review.json','Reviewed revised plan'),
        ('source-audit.json','Seven traceable citation additions'),('development.tex','Connected comparison for main reader')]]
    findings=[
        'Ten scholarly metadata results and20 repository hits are retained with aliases/dispositions. Five selected families are inspected, but omitted native leads and the13-result/10-return query prevent exhaustive coverage;bounded outcome inconclusive.',
        'Thirty-eight new originals and two inherited licenses match receipt SHA256 and pinned Git blobs. The genuine Hauser2012 paper is reread at physical5,31,33;manual pages1,18,19 support version-specific claims. Exact authored calculations and static findings retain distinct status.',
        'All five reuse choices give substantive alternatives and concrete conditions. License conflicts/missing rights,omitted originals,environment and causal/dependent-uncertainty limits remain explicit. No upstream runtime,adapter capability or absence finding is invented.'
    ]
    write(BASE/'author-review.json',{'status':'pass_for_bounded_comparison','reviewer':work.REVIEWER,
        'coverage_outcome':'inconclusive','findings':findings,'criteria_verdicts':['inconclusive','pass','pass'],
        'evidence':evidence,'limitations':work.LIMITS,'integration_allowed':False,'visual_acceptance':False,
        'depth_credit':'No automatic chapter/census completion from added pages'})
    write(work.OUTPUT,{'cell':'discovery_temporal_interventional::C++','status':'bounded_inconclusive',
        'reviewer':work.REVIEWER,'findings':findings,'criteria_verdicts':['inconclusive','pass','pass'],
        'evidence':evidence+[ref(BASE/'author-review.json','Criterion-specific author review')],
        'next_action':'Integrate and inspect preserving successor;record bounded outcome and renew exact-reader reviews. Broader search and rights remain targeted follow-up,not global blockers.',
        'limitations':work.LIMITS})
    print(json.dumps({'coverage':'bounded_inconclusive','source_additions':len(sources),'output':str(work.OUTPUT.relative_to(ROOT))}))


if __name__=='__main__':main()

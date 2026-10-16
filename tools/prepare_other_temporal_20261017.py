#!/usr/bin/env python3
"""Prepare a bounded temporal-source comparison without executing upstream code."""
import copy
from collections import Counter
from fractions import Fraction as F
import itertools
import json
import math
from pathlib import Path

import review_other_temporal_sources_20261017 as work
import temporal_reference_v2_20261017 as examples
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT, BASE = work.ROOT, work.BASE
FINDINGS = [
    'Six bounded GitHub queries retain all43 returned entries, inherited canonical leads, aliases and stopping rules. Six selected families have primary-source comparisons; uninspected candidates, later pages and variant paths keep ecosystem coverage inconclusive.',
    'Forty pinned originals, inherited license originals, two genuine correctly named new papers and the inherited structural-VAR paper support version-specific claims. Independent formulations reproduce six authored finite-law, matrix, unit, rank, supplied-model and regime examples; static observations are distinct from runtime qualification.',
    'All six families have reference/adapt/port/adopt/reject decisions with reasons, rights/runtime prerequisites and a public/generated prototype route. Ten concrete omissions remain visible; no essential original, causal assumption or integration requirement is waived.'
]


def arithmetic():
    saved = work.read(BASE/'exact-results-v2.json')
    assert saved == examples.calculate()
    # Thirty-two equiprobable elementary outcomes, rather than weighted algebra.
    outcomes = [(u, u ^ (a == 0), u ^ (b == 0))
                for u, a, b in itertools.product(range(2), range(4), range(4))]
    counts = Counter((s,t) for u,s,t in outcomes)
    assert counts == {(0,0):10,(0,1):6,(1,0):6,(1,1):10}
    assert {f'{s},{t}':str(F(n,32)) for (s,t),n in counts.items()} == saved['common_calendar']['joint_source_future']
    risks = [F(sum(t for u,s,t in outcomes if s == a),16) for a in range(2)]
    assert list(map(str,risks)) == saved['common_calendar']['conditional_future_risks']
    assert F(sum(t for u,s,t in outcomes),32) == F(1,2)
    for u in range(2):
        conditional = Counter((s,t) for v,s,t in outcomes if u == v)
        for s,t in itertools.product(range(2),repeat=2):
            ns = sum(n for (a,b),n in conditional.items() if a == s)
            nt = sum(n for (a,b),n in conditional.items() if b == t)
            assert F(conditional[s,t],16) == F(ns,16)*F(nt,16)
    information = F(5,8)*math.log2(1.25)+F(3,8)*math.log2(.75)
    assert abs(information-saved['common_calendar']['transfer_information_bits']) < 1e-14
    assert (risks[1]-risks[0])*100 == F(saved['common_calendar']['spurious_usd_per_account']) == 25
    # Solve the original two scalar structural equations after the initial impulse.
    states = [(F(1),F(1,2))]
    for _ in range(2):
        previous_x, previous_y = states[-1]
        x = F(1,2)*previous_x
        y = F(1,2)*x+F(1,4)*previous_y
        states.append((x,y))
    lag = saved['structural_lags']
    assert [str(y) for x,y in states] == lag['outcome_responses']
    assert 100*sum(y for x,y in states) == F(lag['cumulative_first_three_usd']) == F(875,8)
    assert [[F(v) for v in r] for r in lag['recovered_b1']] == [[F(1,2),0],[0,F(1,4)]]
    # Applying the daily scalar transition twice to each basis state checks M^2.
    basis = [(F(1),F(0)),(F(0),F(1))]
    columns = []
    for x,y in basis:
        for _ in range(2):x,y = x/2,x/4+y/4
        columns.append([x,y])
    assert [[str(columns[j][i]) for j in range(2)] for i in range(2)] == lag['two_step_reduced_transition']
    unit = saved['unit_threshold']
    assert F(unit['coefficient_million_usd'])*1_000_000 == F(unit['coefficient_thousand_usd'])*1000 == 40_000
    assert not unit['first_flag'] and unit['rescaled_flag']
    # Rank r among 0..19 has exactly 19-r strictly greater surrogate values.
    ranks = [{'observed_rank':r,'exceedances':sum(v>r for v in range(20))} for r in range(20)]
    raw = sum(F(r['exceedances'],19) <= F(1,100) for r in ranks)
    corrected = sum(F(1+r['exceedances'],20) <= F(1,100) for r in ranks)
    assert F(raw,20) == F(saved['surrogate_rank']['raw_rejection_probability']) == F(1,20)
    assert F(corrected,20) == F(saved['surrogate_rank']['plus_one_rejection_probability']) == 0
    assert F(saved['surrogate_rank']['minimum_corrected_p']) == F(1,20)
    supplied = [(u,u ^ (a == 0),u) for u,a in itertools.product(range(2),range(4))]
    supplied_counts = Counter((a,y) for u,a,y in supplied)
    assert supplied_counts == {(0,0):3,(0,1):1,(1,0):1,(1,1):3}
    assert [str(F(sum(y for u,a,y in supplied if a==v),4)) for v in range(2)] == saved['supplied_model_intervention']['observational_risks']
    # Independently reconstruct the alternative A->Y law with eight equal atoms.
    alternative = [(a,int(k<(1 if a==0 else 3))) for a,k in itertools.product(range(2),range(4))]
    assert Counter(alternative) == supplied_counts
    assert F(sum(y for u,a,y in supplied),8) == F(1,2)
    # A finite era/source/noise law realizes the stated zero pooled covariance.
    era = [(b,x,b*x+e) for b,x,e in itertools.product([-1,1],repeat=3)]
    assert sum(x for b,x,y in era) == sum(y for b,x,y in era) == 0
    assert F(sum(x*y for b,x,y in era),8) == 0
    assert F(sum(x*x for b,x,y in era),8) == 1
    for b in [-1,1]:
        assert F(sum(x*y for k,x,y in era if b==k),4) == b
    return {'status':'pass','reviewer':work.REVIEWER,
        'scope':'Alternative integer-atom enumeration, scalar structural recurrence, basis transitions and complete finite ranks',
        'independence':'Different mathematical formulations by the author; no external independent reviewer',
        'common_calendar_integer_counts':{str(k):v for k,v in sorted(counts.items())},
        'structural_scalar_states':[[str(x),str(y)] for x,y in states],
        'rank_rejections':{'raw':raw,'plus_one':corrected,'equally_likely_ranks':20},
        'supplied_model_integer_counts':{str(k):v for k,v in sorted(supplied_counts.items())},
        'evidence':[ref(BASE/'exact-results-v2.json','Reproduced six exact authored families'),
                    ref(ROOT/'tools/temporal_reference_v2_20261017.py','Original exact generator'),
                    ref(Path(__file__),'Executed alternative checks')],
        'limits':['Stipulated laws and prices; no upstream runtime or empirical bank performance.',
                  'Plus-one correction does not establish an exchangeable temporal resampling law.']}


def main():
    primary = work.read(BASE/'source-review.json')
    candidates = work.read(BASE/'candidate-register.json')
    omissions = work.read(BASE/'omissions-register.json')
    for item in [primary,candidates,omissions]:verify_bindings(item)
    assert len(primary['originals']) == 40 and len(candidates['returned_entries']) == 43
    write(BASE/'arithmetic-review.json',arithmetic())
    pages = (BASE/'cdnod-paper.txt').read_text().split('\f')
    clarification = {'reviewer':work.REVIEWER,'status':'pass','finding':
        'CD-NOD first states the classical known single-target soft-intervention definition, then explicitly extends to detected, continuous, multiple-module and structural changes. The classical definition must not be misrepresented as a blanket CD-NOD restriction.',
        'primary':primary['new_papers'][1]['local_copy'],
        'anchors':[{'anchor':'Physical PDF page30, numbered comparisons1-3','page_text':pages[29]}],
        'manuscript_action':'Clarified the difference between Definition4 and the following generalization; changing-mechanism assumptions and unknown bank regime meanings remain explicit.'}
    verify_bindings(clarification);write(BASE/'primary-clarification.json',clarification)
    contract = {
        'status':'proposed_not_implemented','integration_allowed':False,
        'question_types':['Predictive direction/conditional information','Structural lag coefficient',
            'Supplied-model conditional probability','Surgical or policy intervention','Mechanism-change graph/equivalence class'],
        'request':['Target population, action, outcome and monetary horizon','Entity/trial/calendar boundaries and sampling law',
            'Sampling interval, timestamp alignment, missing-date rule and physical units',
            'Event,availability and decision times','Contemporaneous variables, lag map and maximum lag',
            'Stationarity/regime/context roles and model order','Intervention kind,known targets and duration',
            'Measured/latent assumptions and graph class','Estimator/null/surrogate/conditioning/tuning and finite budget',
            'Pinned engine,dependencies,source/data rights and transformation identities'],
        'response':['Typed mathematical target and numerical units','Graph family,endpoints,source-target convention and lag',
            'Identification assumptions,equivalence class or effect set','Sampling and test-law scope',
            'Numerical,stability,covariance,availability and failure diagnostics','Provenance and refusal reasons'],
        'failure_states':['invalid_clock_or_lag_map','unsupported_dimension_or_trial_law','unresolved_rights',
            'unidentified_effect','invalid_null_or_conditioning_law','numerical_or_stability_failure',
            'unsupported_intervention','transport_or_parse_failure','computed_under_declared_assumptions'],
        'preservation':['Library,CLI and MCP carry the same typed request,response and refusal meanings',
            'A coefficient flag is never silently converted to a p-value','Failed/unavailable outputs remain in all-request denominator',
            'No account/trial boundary becomes a fabricated lag','No era/context label becomes randomized assignment',
            'No predictive score is silently converted to an interventional money value'],
        'decisions':[
            {'family':'Associations.jl','choice':'reference_then_restricted_adaptation',
             'reason':'Composable information/embedding paths and inherited MIT notice make reuse worth testing; a port duplicates estimator and null-law maintenance.',
             'before_runtime':['Complete dependency rights','Supported-dimensionality restrictions','Full conditioning versus helper-neighbour law',
                'Frozen temporal surrogate calibration,including ties and exchangeability','Exact physical embedding and exclusion units']},
            {'family':'varlingam-rs','choice':'reference_existing_Rust_Python_boundary_before_port',
             'reason':'Actual lag helper has correct structural conversion; advertised speed and bootstrap/scalable paths remain unqualified.',
             'reject':'Presenting significant coefficient-threshold field as statistical significance.',
             'before_runtime':['Centering/intercept and covariance-aware order reference','Residual estimator/cache review',
                'Default and unit-aware threshold semantics','Complete dependency/distribution terms','Finite conversion and fresh stability/calibration cases']},
            {'family':'BNT','choice':'legacy_supplied_model_reference',
             'reason':'Constructor/unrolling receives a graph; tiny-model surgery/conditioning comparisons remain useful.',
             'reject':'Adopting the inspected constructor/unrolling path as data-driven temporal discovery.',
             'before_runtime':['Resolve filename/function callable path','Check exact enumeration,posterior conditioning and surgery separately',
                'Permitted MATLAB environment and full GNU Library GPLv2 component/distribution review']},
            {'family':'MVGC1','choice':'predictive_direction_reference_and_conditional_comparator',
             'reason':'Preserve within-trial estimation,covariance and failure semantics; porting only regression discards substantive checks.',
             'before_runtime':['GPLv3-or-later and dependency/distribution review','Independent trial/common-calendar null law',
                'Intercept/order/stability/moving-average/heteroscedasticity cases','Preserve unavailable outputs and target-row orientation',
                'Inspect newer state-space path separately']},
            {'family':'TRENTOOL3','choice':'embedding_delay_surrogate_reference_before_GPU_adoption',
             'reason':'MATLAB/CUDA workflow adds time-unit,component and calibration burdens; bounded CPU comparison should precede GPU investment.',
             'before_runtime':['Complete component/FieldTrip/TSTOOL/MATLAB rights and revisions','Hz,seconds,milliseconds and autocorrelation-time conversions',
                'Tie/one-tail/two-tail and multiplicity calibration','Trial/exclusion/null law','Frozen CPU/GPU numerical comparison']},
            {'family':'CD-NOD','choice':'paper_reference_and_original_typed_lag_prototype',
             'reason':'Paper contains real lagged extension; selected same-row entrypoint does not establish lag assembly/time tiers and top-level rights are unresolved.',
             'before_runtime':['Obtain explicit code permission or use original paper-based implementation','Algorithm5 lag/context/time-tier and endpoint oracle',
                'Changing-mechanism assumptions and residual ambiguity','Dependent overlapping-window calibration',
                'Kernel/regularization and bounded-resource/failure semantics']}],
        'prototype':{
            'status':'design_only; six exact authored reference families already executed',
            'first_stage':'Generated known mechanisms and independent exact oracles before any permitted engine comparison',
            'cases':['Common calendar predictive information without action effect','Structural/reduced lags and changed sampling frequency',
                'Coefficient unit conversions','Complete surrogate ranks,ties and invalid temporal nulls',
                'Conditioning versus surgery and equivalent observed laws','Opposing era-specific mechanisms',
                'Shifted levels,near instability and moving-average misspecification','Missing dates,unequal trials and overlapping windows',
                'Graph endpoints,lag assembly,unknown common causes and required refusal'],
            'public_stage':'Permitted observed series test parsing,clocks,diagnostics and predictive reproduction. A documented public experiment supports effects only where assignment,measurement,interference,timing and population match; public observations alone are not graph gold.',
            'freeze':['Code/data/environment identities and rights','Target,transformations,clocks,units and graph conventions',
                'Generated mechanisms and intervention oracles','Entity/calendar-separated development and fresh evaluation',
                'Nulls,tuning/surrogate budgets,tolerances and stopping','All-request denominator and unavailable/refusal scoring'],
            'metrics':['Endpoint/lag accuracy','Target-specific error and justified ambiguity','Null calibration in declared families',
                'Numerical stability,availability and refusal','Complete workflow cost'],
            'finite_gate':'Predeclared exact mandatory cases and bounded fresh comparisons only; no universal guarantee or integration permission.',
            'costs':['Retrieval/preparation','Licenses/dependencies/hardware','Conversion/estimation','Scientific and assumption review',
                'Failed runs/retries/corrections','Maintenance'],
            'bank_trigger':'Demonstrated permitted prototype merit and a specific decision-relevant uncertainty justify later representative bank experiments.'},
        'research_limits':['Unmeasured and time-varying confounding','Unknown regime/intervention meaning','Observational equivalence',
            'Dependent graph/effect-set uncertainty','Useful precision and transport'],
        'evidence':[ref(BASE/'source-review.json','Forty pinned originals and primary papers'),
                    ref(BASE/'primary-clarification.json','Soft-intervention definition versus generalization'),
                    ref(BASE/'exact-results-v2.json','Exact authored references'),
                    ref(BASE/'omissions-register.json','Concrete unresolved routes')],
        'limitations':work.LIMITS}
    write(BASE/'proposed-contract.json',contract)
    sources = copy.deepcopy(work.read(BASE/'technical-source-audit.json')['sources'])
    cdnod = next(s for s in sources if s['integrated_citation_key']=='exec17_temporal_cdnod_paper')
    cdnod['inspected_anchors'].append({'anchor':'Physical PDF page30, comparisons1-3',
        'finding':clarification['finding'],'extracted_text':ref(BASE/'cdnod-paper.txt','Genuine paginated primary text'),
        'page_text':pages[29]})
    cdnod['supported_claims'].append(clarification['finding'])
    sources += [
        work.source('oracle','Exact calendar,structural-lag,unit,rank,intervention and regime references',
            'Causal banking proposal',BASE/'exact-results-v2.json','project_derivation',
            ['Six exact authored families; no upstream engine execution','Stipulated USD25 spurious contrast and USD109.375 finite structural impulse value'],
            [ref(ROOT/'tools/temporal_reference_v2_20261017.py','Exact calculation'),
             ref(BASE/'arithmetic-review.json','Alternative integer,scalar and rank checks')]),
        work.source('contract','Proposed temporal question,package reuse and public/generated prototype contract',
            'Causal banking proposal',BASE/'proposed-contract.json','project_design',
            ['Six family-specific reuse choices and prerequisites','Typed CLI/MCP semantics,complete costs and prototype before expensive bank study'],
            [ref(BASE/'omissions-register.json','Ten concrete unresolved routes')])]
    assert len(sources)==10
    write(BASE/'source-audit.json',{'sources':sources,'prior':ref(work.PRIOR,'686 preserved source records'),
        'cutoff':'2026-10-07','new_records':10,'new_scholarly_pdfs':2})
    write(BASE/'recovery-review.json',{'status':'recovered_and_continuing','findings':[
        'Controller check passed;118/376 recorded,219 ready,temporal other_relevant active;871-page canonical reader intact.',
        'Saved40-original review,43 returned search entries,two genuine new papers and unfinished manuscript recovered without reacquisition.',
        'Earlier review failed on non-UTF-8 legacy bytes before any output; repaired by recorded UTF-8 or byte-preserving Latin-1 fallback,without technical interpretation of fallback non-ASCII prose.',
        'Source reread clarified classical soft intervention versus CD-NOD generalization at physical29-30 before author review.',
        'Original v1 mathematics and receipts preserved; v2 is the explicitly reviewed reference.',
        'Inherited image allowance exhausted; no additional previews used and rendered visual acceptance remains open.'],
        'evidence':[ref(BASE/'crash-recovery.json','Prior recovery checkpoint'),
                    ref(BASE/'primary-clarification.json','Observed wording repair'),
                    ref(ROOT/'docs/program/execution/2026-10-17/variable-ontology/publication/git-publication-677f01ac.json','Verified predecessor Git publication')]})
    evidence = [ref(BASE/name,name) for name in [
        'plan.md','source-review.json','primary-clarification.json','candidate-register.json','omissions-register.json',
        'exact-results-v2.json','arithmetic-review.json','proposed-contract.json','source-audit.json','development.tex','recovery-review.json']]
    evidence.append(ref(Path(__file__),'Criterion-specific author and mathematical review'))
    for item in evidence:verify_bindings(item)
    write(BASE/'author-review.json',{'status':'pass_for_bounded_comparison','reviewer':work.REVIEWER,
        'coverage_outcome':'inconclusive','findings':FINDINGS,'criteria_verdicts':['inconclusive','pass','pass'],
        'evidence':evidence,'limitations':work.LIMITS,'integration_allowed':False,'visual_acceptance':False,
        'plan_review':['Pinned originals and identity evidence do not establish executable capability.',
            'No finite search supports ecosystem absence; retain every returned row and alias.',
            'Distinguish causal/predictive targets,clocks,regimes,null laws and supplied graph semantics.',
            'Recorded source/rights and visual gaps block their own claims; eligible proposal work continues.'],
        'depth_credit':'No automatic mandatory-repair,chapter-depth,coverage or product acceptance from added pages.'})
    write(work.OUTPUT,{'cell':'discovery_temporal_interventional::other_relevant','status':'bounded_inconclusive',
        'cutoff':'2026-10-07 Asia/Shanghai','reviewer':work.REVIEWER,
        'findings':FINDINGS,'criteria_verdicts':['inconclusive','pass','pass'],
        'evidence':evidence+[ref(BASE/'author-review.json','Criterion review')],
        'exhaustive_census':False,'integration_allowed':False,'native_package_executed':False,
        'next_action':'Integrate and compile preserving successor,review exact reader,record bounded outcome,publish,renew Q2-Q4,commit/push and continue next eligible operation.',
        'limitations':work.LIMITS})
    write(BASE/'progress.json',{'finding':'Recovered six-family comparison,ten audited source additions and six independently reformulated exact examples; broader coverage remains inconclusive.',
        'next_action':'Prepare preserving reader and compile; then sequential review,record,publish,Q2-Q4 renewal,Git publication and next eligible work.',
        'evidence':[ref(BASE/'author-review.json','Completed bounded author review'),ref(work.OUTPUT,'Structured contracted coverage output')]})
    print(json.dumps({'new_records':10,'new_papers':2,'families':6,'coverage':'inconclusive','author_review':'saved'}))


if __name__=='__main__':main()

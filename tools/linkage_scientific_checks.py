#!/usr/bin/env python3
"""Independent algebra, finite-binomial coverage and public-domain checks."""
import copy
from dataclasses import replace
import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np
from threadpoolctl import threadpool_limits

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'src'), str(ROOT/'tools')]
from causalbank.dynamic_funding import FundingTarget
from causalbank.dynamic_product import DynamicBrief, run_funding, application_result, treasury_report
from causalbank.linkage_sets import binomial_interval, pair_projection, sum_difference_projection, decode_set, encode_set, weighted_sum, project_funding
from dynamic_observation_study import make_linked
from dynamic_product_study import source_feed


def main():
    checks, details = {}, {}
    # Enumerate every possible binomial outcome, rather than simulate coverage.
    minimum = 1.0
    for size in range(1, 26):
        regions = [binomial_interval(k, size, .05) for k in range(size+1)]
        for p in np.linspace(0, 1, 201):
            coverage = sum(math.comb(size,k)*p**k*(1-p)**(size-k)
                           for k,(lo,hi) in enumerate(regions) if lo-1e-14 <= p <= hi+1e-14)
            minimum = min(minimum, coverage)
    checks['enumerated_binomial_coverage'] = minimum >= .95-1e-12
    checks['no_audits_is_full_probability_range'] = binomial_interval(0,0,.05) == (0.0,1.0)
    details['minimum_binomial_coverage_sizes_1_to_25_grid_201'] = minimum
    checks['rank_one_compatible_is_unbounded'] = sum_difference_projection((1,2),(-.1,.1),(.5,.5)) == [(-math.inf,math.inf)]
    checks['rank_one_incompatible_is_empty'] = sum_difference_projection((1,2),(1,2),(.5,.5)) == []
    rays = sum_difference_projection((1.5,1.5),(.5,.5),(.4,.6))
    checks['two_rays_preserved'] = (len(rays)==2 and rays[0][0]==-math.inf and rays[1][1]==math.inf
                                    and abs(rays[0][1]+1)<1e-12 and abs(rays[1][0]-4)<1e-12)
    details['analytic_two_ray_example'] = encode_set(rays)
    checks['positive_scaling_keeps_topology'] = len(weighted_sum([rays],[.1],3)) == 2
    checks['candidate_projection_two_rays'] = np.allclose([pair_projection((2,3),(0,1),(.4,.6))[0][1],pair_projection((2,3),(0,1),(.4,.6))[1][0]],[-1,4])
    rng = np.random.default_rng(76101)
    mismatches = []
    # Independent primal feasibility: for fixed theta, r*(theta-S) ranges over
    # the interval bounded by its four rectangle corners. This avoids ratios.
    for case in range(400):
        average = sorted(rng.normal(size=2)*2)
        difference = sorted(rng.normal(size=2))
        probability = sorted(rng.random(2))
        if case % 7 == 0: probability = [.5,.5]
        if case % 11 == 0: probability = [.5,probability[1] if probability[1]>.5 else .9]
        pieces = sum_difference_projection(average,difference,probability)
        for theta in np.r_[rng.normal(size=40)*20,-1e8,1e8]:
            products=[r*(theta-s) for r in (2*probability[0]-1,2*probability[1]-1) for s in average]
            feasible=max(min(products),difference[0]) <= min(max(products),difference[1])
            member=any(lo<=theta<=hi for lo,hi in pieces)
            if feasible != member:mismatches.append({'case':case,'theta':float(theta)})
    checks['ratio_free_primal_feasibility'] = not mismatches
    details['primal_membership_comparisons'] = 400*42
    details['primal_mismatches'] = mismatches

    base=json.loads((ROOT/'docs/studies/dynamic-funding-spec.json').read_text())
    obs=json.loads((ROOT/'docs/studies/dynamic-observation-spec.json').read_text())
    fixture=json.loads((ROOT/'docs/studies/observation-fixtures-v6.json').read_text())['cases'][0]
    pilot=make_linked(base,obs,1440,[9027,0]);data=make_linked(base,obs,360,[9027,1])
    target=FundingTarget(horizon=base['horizon'],branches=base['branches'])
    brief=DynamicBrief(target,'source','pilot','audit',6)
    strata=np.repeat([0,1],100);correct=np.r_[np.r_[np.ones(95),np.zeros(5)],np.r_[np.ones(80),np.zeros(20)]].astype(int)
    kwargs={'brief':brief,'source_fixture':fixture,'pilot':pilot,'data':source_feed(data,6),
            'audit_strata':strata,'audit_correct':correct,'penalties':base['penalties']}
    rejected={}
    def reject(name,change):
        try:run_funding(**dict(kwargs,**change));rejected[name]=False
        except ValueError as exc:rejected[name]=str(exc)

    with threadpool_limits(limits=1):
        regular=run_funding(**kwargs)
        projected=run_funding(**kwargs,inference='weak_linkage_projection')
        no_audits=run_funding(**dict(kwargs,audit_strata=np.array([],dtype=int),audit_correct=np.array([],dtype=int)),inference='weak_linkage_projection')
        missing=run_funding(**dict(kwargs,audit_strata=np.zeros(100,dtype=int),audit_correct=np.ones(100,dtype=int)),inference='weak_linkage_projection')
        reject('missing_audit_regular',{'audit_strata':np.zeros(100,dtype=int),'audit_correct':np.ones(100,dtype=int)})
        reject('fractional_labels',{'audit_correct':correct+.2})
        reject('unrecognized_stratum',{'audit_strata':strata+1})
        reject('audit_length_mismatch',{'audit_correct':correct[:-1]})
        reject('fractional_bandwidth',{'brief':replace(brief,bandwidth=2.7)})
        reject('excessive_bandwidth',{'brief':replace(brief,bandwidth=360)})
        reject('nonfinite_margin',{'brief':replace(brief,target=replace(target,monthly_margin=float('nan')))})
        reject('negative_penalty',{'penalties':[-1.]})
        reject('empty_penalty_list',{'penalties':[]})
        reject('confidence_level_identity',{'inference':'weak_linkage_projection','alpha':.1,'cached_identity':projected['identity']})
        reject('procedure_identity',{'inference':'weak_linkage_projection','cached_identity':regular['identity']})
        invalid=copy.deepcopy(data);invalid['outcomes'][0,0]=np.nan
        reject('nonfinite_outcome',{'data':invalid})
        invalid=copy.deepcopy(data);invalid['stratum'][:]=0
        reject('missing_evaluation_stratum',{'data':invalid})
        invalid=copy.deepcopy(data);invalid['x'][:,2]+=1
        reject('unsupported_basis',{'data':invalid})
        invalid=copy.deepcopy(pilot);invalid['x'][:720]=invalid['x'][0]
        reject('pilot_rank_loss',{'pilot':invalid})
        invalid=copy.deepcopy(kwargs['data']);extra=dict(invalid['outcome_records'][0],balance=12345.);invalid['outcome_records'].append(extra)
        reject('conflicting_revision',{'data':invalid})
        invalid=copy.deepcopy(kwargs['data']);original=invalid['outcome_records'][0]
        invalid['outcome_records']=[dict(original,revision=3),*invalid['outcome_records'],dict(original,balance=12345.)]
        reject('conflicting_old_revision_after_newer',{'data':invalid})
        invalid=copy.deepcopy(kwargs['data']);invalid['extraction_cutoff']=float('nan')
        reject('invalid_extraction_clock',{'data':invalid})
    checks['scientific_domain_rejections'] = all(rejected.values())
    checks['missing_audit_projection_returns_set'] = missing['status']=='computed_set'
    checks['no_audit_projection_is_unbounded'] = any(row['lower'] is None or row['upper'] is None for row in no_audits['financial_set'])
    fake=dict(projected,financial_set=encode_set(rays))
    consumer=application_result(fake,10)
    checks['consumer_preserves_disconnected_unbounded'] = len(consumer['funding_set_per_account'])==2 and consumer['funding_set_per_account'][0]['lower'] is None and consumer['funding_set_per_account'][1]['upper'] is None
    checks['method_changes_identity'] = regular['identity'] != projected['identity']
    try:
        project_funding(np.ones((2,14)),np.zeros((28,28)),[90,80],[100,100],target)
        checks['zero_variance_not_called_exact']=False
    except ValueError:
        checks['zero_variance_not_called_exact']=True
    details['rejections']=rejected
    details['public_projection']=treasury_report(projected)
    details['no_audit_projection']=treasury_report(no_audits)
    details['missing_audit_projection']=treasury_report(missing)
    details['consumer_two_rays']=consumer
    names=['tools/linkage_scientific_checks.py','src/causalbank/linkage_sets.py','src/causalbank/dynamic_validation.py',
           'src/causalbank/dynamic_product.py','src/causalbank/dynamic_funding.py','src/causalbank/linked_observation.py',
           'src/causalbank/responses.py','tools/dynamic_observation_study.py','tools/dynamic_product_study.py',
           'docs/studies/dynamic-funding-spec.json','docs/studies/dynamic-observation-spec.json','docs/studies/observation-fixtures-v6.json']
    checks={k:bool(v) for k,v in checks.items()}
    result={'status':'pass' if all(checks.values()) else 'fail','checks':checks,'details':details,
            'input_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in names},
            'scope':'Finite binomial enumeration, independent ratio-free feasibility, public unsupported-input and set-preservation checks; not proof of time-series approximation or bank validity'}
    (ROOT/'docs/reviews/linkage-scientific-checks.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'status':result['status'],'checks':checks,'binomial_minimum':minimum},indent=2))
    raise SystemExit(not all(checks.values()))


if __name__=='__main__':
    main()

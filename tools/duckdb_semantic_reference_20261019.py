#!/usr/bin/env python3
"""Exact authored tabular oracles; does not import or execute DuckDB."""
from fractions import Fraction as F
from itertools import permutations, product
import json


def mean(values):
    return sum(values, F(0)) / len(values) if values else None


def nullable_summary(values):
    present=[x for x in values if x is not None]
    return dict(rows=len(values), observed=len(present),
        total=str(sum(present)) if present else None,
        mean=str(mean(present)) if present else None)


def calculate():
    treated=[1,None,None];control=[1,0,0]
    cc=mean([x for x in treated if x is not None])-mean(control)
    possible=sorted({mean([1,*completion])-mean(control) for completion in product([0,1],repeat=2)})
    net=[300*x-40 for x in possible]
    assert cc==F(2,3) and possible==[F(0),F(1,3),F(2,3)] and net==[-40,60,160]
    accounts=[('t1',1,100),('t2',1,0),('c1',0,0),('c2',0,0)]
    def contrast(rows):
        return mean([F(v) for _,a,v in rows if a==1])-mean([F(v) for _,a,v in rows if a==0])
    joined=[accounts[0]]*3+accounts[1:]
    assert contrast(accounts)==50 and contrast(joined)==75
    ordered=sorted(accounts,key=lambda r:r[0])
    assert all(sorted(p,key=lambda r:r[0])==ordered for p in permutations(accounts))
    features=[dict(account='t1',event_day=1,event_sequence=1,value=0),
              dict(account='t1',event_day=3,event_sequence=2,value=1)]
    action_day=2
    latest=max(features,key=lambda r:(r['event_day'],r['event_sequence']))
    asof=max((r for r in features if r['event_day']<action_day),key=lambda r:(r['event_day'],r['event_sequence']))
    assert latest['value']==1 and asof['value']==0
    return dict(kind='authored_exact_tabular_reference_no_native_engine',
        missingness=dict(treated=treated,control=control,complete_case_contrast=str(cc),
            feasible_full_cohort_contrasts=[str(x) for x in possible],sharp_range=[str(possible[0]),str(possible[-1])],
            hypothetical_value_per_contrast_usd=300,hypothetical_cost_usd=40,net_range_usd=[str(net[0]),str(net[-1])],
            complete_case_plug_in_net_usd=str(300*cc-40),
            meaning='Finite descriptive cohort contrasts; no causal assignment, population inference or missingness model is supplied.'),
        null_groups={k:nullable_summary(v) for k,v in [('empty',[]),('all_missing',[None,None]),('observed_zero',[0,0])]},
        join_multiplicity=dict(account_contrast_usd=str(contrast(accounts)),
            one_to_many_join_contrast_usd=str(contrast(joined)),input_accounts=4,joined_rows=len(joined),
            reason='Duplicating the positive treated account changes descriptive weighting; join count is not independent sample size.'),
        order=dict(permutations=24,key_sorted_rows=[list(r) for r in ordered],row_position_is_identifier=False),
        clock=dict(action_day=action_day,rule='Strictly before action; ties require explicit event sequence and same-time visibility rule.',
            unrestricted_latest=latest,admissible_asof=asof,post_action_feature_admitted=False),
        native_duckdb_execution=False,causal_identification_or_bank_roi=False)


if __name__=='__main__':
    print(json.dumps(calculate(),indent=2))

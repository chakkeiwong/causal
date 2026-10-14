#!/usr/bin/env python3
"""Recheck the authored data/code target and availability-clock fixtures exactly."""
from fractions import Fraction as F
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/program/execution/2026-10-13/data-code/exact-results.json'

def calculate():
    mass=[F(1,2),F(1,2)]
    propensity=[F(1,5),F(1,2)]
    effect=[F(0),F(10)]
    full=sum(m*t for m,t in zip(mass,effect))
    overlap=[m*e*(1-e) for m,e in zip(mass,propensity)]
    weighted=sum(w*t for w,t in zip(overlap,effect))/sum(overlap)
    assert full==5 and weighted==F(250,41)
    records=[{'id':'c1','event_day':9,'available_day':11},
             {'id':'c2','event_day':9,'available_day':9},
             {'id':'c3','event_day':8,'available_day':12}]
    admitted=[r['id'] for r in records if r['event_day']<=10 and r['available_day']<=10]
    assert admitted==['c2']
    return {'kind':'authored_exact_fixture','engine_or_live_model_executed':False,
        'strata_masses':['1/2','1/2'],'propensities':['1/5','1/2'],
        'conditional_effects':[0,10],'uniform_retained_population_mean':str(full),
        'overlap_weighted_mean':str(weighted),'same_target':False,
        'decision_day':10,'candidate_records':records,'admitted_ids':admitted,
        'rejected_ids':['c1','c3'],
        'limit':'The law and clocks are stipulated. Arithmetic does not estimate a bank effect or qualify an agent.'}

if __name__=='__main__':
    result=calculate()
    if OUT.exists():assert json.loads(OUT.read_text())==result
    else:OUT.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'exact_replay':'pass','uniform':'5','overlap':'250/41','admitted':1,'rejected':2}))

#!/usr/bin/env python3
"""Exact authored target, panel-clock and resampling contract references."""
from fractions import Fraction as F
from itertools import product
import json


def calculate():
    rows=[]
    for s in [0,1]:
        e=F(1,2) if s==0 else F(1,10)
        tau=F(0) if s==0 else F(100)
        for a in [0,1]:
            mass=F(1,2)*(e if a else 1-e)
            y=tau*a
            rows.append(dict(s=s,a=a,mass=mass,t=tau,y=y,
                             residual_a=F(a)-e,residual_y=y-tau*e))
    den=sum(r['mass']*r['residual_a']**2 for r in rows)
    num=sum(r['mass']*r['residual_a']*r['residual_y'] for r in rows)
    slope=num/den;ate=F(50)
    assert den==F(17,100) and num==F(9,2) and slope==F(450,17)
    assert ate-35==15 and slope-35==F(-145,17)
    # Enumerate a source-motivated within-fixed-unit draw, not an upstream call.
    draws=list(product([0,1],repeat=2))
    chronology=[d for d in draws if d==(0,1)]
    assert len(chronology)==1
    rows_clock=[('a',0),('b',1),('a',1),('b',0)]
    seen={};mapping=[]
    for unit,time in rows_clock:
        assigned=seen.get(unit,0);seen[unit]=assigned+1
        mapping.append(dict(unit=unit,true_time=time,encounter_period=assigned))
    assert sum(r['true_time']!=r['encounter_period'] for r in mapping)==2
    units=4
    # Four perfectly shared zero-mean fair +/-1 scores: var(mean)=1.
    means=[F(sum([shock]*units),units) for shock in [-1,1]]
    true_variance=sum(x*x/2 for x in means)
    iid_working=F(1,units)
    return dict(kind='project_authored_exact_reference',upstream_execution=False,
        static_target=dict(assumptions='S~Bernoulli(1/2); A|S=0~Bernoulli(1/2),A|S=1~Bernoulli(1/10); Y(a)=100*S*a; exact nuisance functions, no confounding beyond observedS.',
            rows=[{k:str(v) if isinstance(v,F) else v for k,v in r.items()} for r in rows],
            residual_variance=str(den),residual_covariance=str(num),constant_residual_slope_USD=str(slope),population_ATE_USD=str(ate),
            assumed_action_cost_USD='35',population_net_USD='15',mislabelled_slope_net_USD=str(slope-35)),
        panel_clock=dict(rows=mapping,equal_group_counts=True,timestamps_inferred_from_encounter_order=True),
        within_group_resampling=dict(two_date_draws=[list(d) for d in draws],chronology_preserving_draws=[list(d) for d in chronology],preservation_probability='1/4',two_unit_full_preservation_probability='1/16',scope='Uniform source-motivated resampling of rows within each fixed group; not whole-history cluster resampling.'),
        shared_calendar=dict(groups=units,score_means=list(map(str,means)),true_mean_variance=str(true_variance),working_independent_group_variance=str(iid_working)),
        limitations=['No native EconML fit, bootstrap run or upstream test executed.','Projection target mismatch is under a deliberately misspecified constant effect model; it is not an error when that model is correctly specified.','Shared-score and panel examples are declared references, not measured behavior or general coverage experiments.','USD outcomes/cost are assumed, not observed bank economics.'])

if __name__=='__main__':print(json.dumps(calculate(),indent=2))

#!/usr/bin/env python3
"""Deterministic project derivations and design diagnostics, not qualification."""
from fractions import Fraction as F
import itertools
import json
from pathlib import Path

import numpy as np
from scipy.stats import beta, binom

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"docs/program/gap-repair-v13/work/RG1"


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    powers=[]
    for n in [512,2048,8192]:
        for family in [1,8,33]:
            alpha=.05/family
            k=np.arange(1,n+1)
            lower=beta.ppf(alpha,k,n-k+1)
            accepted=k[lower>=.95]
            threshold=int(accepted[0]) if len(accepted) else n+1
            # Independently characterize the same one-sided exact-binomial threshold.
            assert binom.sf(threshold-1,n,.95)<=alpha+1e-12
            if threshold>1:assert binom.sf(threshold-2,n,.95)>alpha-1e-12
            powers.append({"replications":n,"family":family,"minimum_covered_requests":threshold,
                           "all_success_lower":float(alpha**(1/n)),
                           "per_cell_power":{str(p):float(binom.sf(threshold-1,n,p)) for p in [.95,.96,.975,.99]},
                           "scope":"Exact binomial Monte Carlo screen only; independent replications assumed. No independence between family cells needed for Bonferroni error control."})
    # Two observationally indistinguishable structural models, exact enumeration.
    factual=[];interventions=[]
    for u in [0,1]:
        factual.append({"u":u,"A":u,"Y_model_causal":u,"Y_model_confounded":u})
    for a in [0,1]:
        interventions.append({"a":a,"mean_causal":float(F(sum(a for u in [0,1]),2)),
                              "mean_confounded":float(F(sum(u for u in [0,1]),2))})
    assert all(r['Y_model_causal']==r['Y_model_confounded'] for r in factual)
    assert interventions[1]['mean_causal']-interventions[0]['mean_causal']==1
    assert interventions[1]['mean_confounded']-interventions[0]['mean_confounded']==0
    # Selecting the larger noisy evaluation is optimistic even with two null options.
    same=F(0);fresh=F(0)
    for v in itertools.product([-1,1],repeat=4):
        selected=0 if v[0]>=v[1] else 1
        same+=F(v[selected],16);fresh+=F(v[2+selected],16)
    assert same==F(1,2) and fresh==0
    # Directly enumerate a stipulated two-borrower interference law.
    network=[]
    for p in [F(1,5),F(4,5)]:
        direct=F(0)
        for a,b in itertools.product([0,1],repeat=2):
            weight=(p if a else 1-p)*(p if b else 1-p)
            direct+=weight*(100*a+40*b-30*a*b)
        formula=140*p-30*p*p
        assert direct==formula
        network.append({"p":str(p),"expected_outcome":str(direct),"value_cny":float(direct)})
    # Exact moments for A uniform on [0,2]; no data or package invocation.
    moments={i:F(2**i,i+1) for i in range(5)}
    cov=20*(moments[2]-moments[1]**2)-3*(moments[3]-moments[1]*moments[2])
    slope=cov/(moments[2]-moments[1]**2)
    finite=(20*2-3*4)-(20*1-3*1)
    assert slope==14 and finite==11
    result={"kind":"project_deterministic_derivations_not_final_study","random_draws":0,"live_calls":0,
            "screen_operating_characteristics":powers,
            "observational_equivalence":{"factual":factual,"interventions":interventions,"effect_values":[1,0]},
            "selection_bias":{"same_data_expected_value":str(same),"fresh_evaluation_expected_value":str(fresh)},
            "continuous_target":{"covariance_slope":str(slope),"finite_change_1_to_2":finite,"units":"stipulated CNY per dose or finite contrast"},
            "network_allocation":network,
            "network_change_cny":str(F(network[1]['expected_outcome'])-F(network[0]['expected_outcome'])),
            "limits":["No package runtime measured","No live model or bank value measured","No successor research qualified",
                      "Binomial probabilities diagnose qualification-design power, not validity of a causal estimator"]}
    output=OUT/"design-checks.json"
    if output.exists() and json.loads(output.read_text())!=result:raise ValueError("Preserve prior diagnostic; use a successor")
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({"status":"pass","exact_screen_designs":len(powers),"enumerated_examples":4,
                      "final_qualification":False,"output":str(output.relative_to(ROOT))}))


if __name__=='__main__':main()

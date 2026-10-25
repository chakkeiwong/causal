#!/usr/bin/env python3
"""Project-authored exact witnesses; never imports or executes acquired code."""
from fractions import Fraction as F
from itertools import product
import json


def phase_probability(length, block):
    total = F(0)
    for phase in range(block):
        ids = [(phase + t) // block for t in range(length)]
        unique = sorted(set(ids))
        for bits in product([0, 1], repeat=len(unique)):
            assignment = dict(zip(unique, bits))
            if all(assignment[i] == 1 for i in ids):
                total += F(1, block * 2 ** len(unique))
    return total


def lag_variance(phi, last_lag):
    n = len(phi)
    avg = sum(phi) / n
    centered = [x - avg for x in phi]
    diagonal = sum(x*x for x in centered)
    off_diagonal = sum(2*centered[t]*centered[t-k]
                       for t in range(n) for k in range(1, min(t, last_lag)+1))
    return (diagonal + off_diagonal) / n


def calculate():
    d, y, p = [1, 0], [F(2), F(1)], F(1, 2)
    group_normalized = sum(v/p for z,v in zip(d,y) if z)/sum(d)
    group_normalized -= sum(v/(1-p) for z,v in zip(d,y) if not z)/(len(d)-sum(d))
    population_normalized = sum(z*v/p-(1-z)*v/(1-p) for z,v in zip(d,y))/len(d)
    assert group_normalized == 2 and population_normalized == 1
    memory, block = 2, 4
    code_q = F(1,2)-F(memory-1,4*block)
    paper_q = phase_probability(memory+1,block)
    assert phase_probability(memory,block)==code_q==F(7,16)
    assert paper_q==F(3,8)
    assert F(1,2)!=code_q  # first truncated one-observation window
    invalid_q=F(1,2)-F(10-1,4*4)
    assert invalid_q<0 and phase_probability(10,4)>0
    phi=list(map(F,[1,-1,1,-1]))
    source_variance=lag_variance(phi,1)
    inclusive_variance=lag_variance(phi,2)
    assert source_variance==F(-1,2) and inclusive_variance==F(1,2)
    scores=list(map(F,[-2,2,2,-2]));s=sum(x*x for x in scores)/4
    var_once=s/4;var_twice=var_once/4
    assert var_once==1 and var_twice==F(1,4)
    # Sequential versus simultaneous application of two authored update rules.
    def step(order):
        state=[0,0]
        for unit in order:state[unit]=state[1-unit]+1
        return state
    assert step([0,1])==[1,2] and step([1,0])==[2,1]
    # Graph conversion retains the last parallel edge; exposure changes.
    edges=[('a','b',9),('a','b',1),('a','c',1)]
    treatment={'b':1,'c':0}
    before=F(sum(w*treatment[v] for _,v,w in edges),sum(w for _,_,w in edges))
    mapped={}
    for u,v,w in edges:mapped[(u,v)]=w
    after=F(sum(w*treatment[v] for (_,v),w in mapped.items()),sum(mapped.values()))
    assert before==F(10,11) and after==F(1,2)
    # Shared nested attributes survive a shallow export copy.
    attrs={'risk':{'limit':100}};exported=dict(attrs);exported['risk']['limit']=200
    assert attrs['risk']['limit']==200
    # A disconnected independent random initial state gives no shared counterfactual coupling.
    independent_variance=sum(F(1,4)*(F(a-b))**2 for a,b in product([0,1],repeat=2))
    assert independent_variance==F(1,2)
    return dict(provenance='Exact project-authored finite-law and helper-expression witnesses; no acquired code executed.',native_execution=False,
        ipw_normalization=dict(treatments=d,outcomes=[str(x) for x in y],propensity=str(p),group_mean_expression=str(group_normalized),population_mean_expression=str(population_normalized)),
        switchback_windows=dict(memory=memory,block=block,source_window_probability=str(code_q),paper_history_plus_current_probability=str(paper_q),first_truncated_window_probability='1/2',outside_range_memory=10,outside_range_formula=str(invalid_q),outside_range_exact_probability=str(phase_probability(10,4)),scope='Stationary uniform phase and independent fair blocks; early truncated windows require separate probabilities.'),
        lag_variance=dict(phi=[str(x) for x in phi],memory=2,source_lags=[1],paper_inclusive_lags=[1,2],source_long_run_expression=str(source_variance),inclusive_long_run_expression=str(inclusive_variance),source_mean_variance=str(source_variance/4),clamped_mean_variance='0',inclusive_mean_variance=str(inclusive_variance/4)),
        double_scaling=dict(sample_size=4,centered_ipw_scores=[str(x) for x in scores],score_second_moment=str(s),once_scaled_variance=str(var_once),twice_scaled_variance=str(var_twice),once_scaled_se='1',twice_scaled_se='1/2'),
        score_selection=dict(phi=[1,3,5],first_element=1,full_average='3'),
        noise_scale=dict(sd_parameter=2,literal_noise_sd='1/2',literal_variance='1/4',multiplicative_sd_interpretation_variance='4'),
        scheduling=dict(forward=step([0,1]),reverse=step([1,0]),synchronous=[1,1]),
        parallel_edge_conversion=dict(edges=[list(x) for x in edges],before_exposure=str(before),after_last_edge_exposure=str(after)),
        graph_identity=dict(before=['a','b','c'],after_remove_second=['a','c'],stale_second_treatment=0,correct_c_treatment=1,stable_slot_reused_for_new_entity=True),
        graph_space=dict(position_occupants=['borrower_a','borrower_b'],position_query_includes_self=True,agent_query_excludes_only_focal=True),
        nested_attributes=dict(original_limit_after_export_mutation=attrs['risk']['limit'],deep_snapshot_required=True),
        counterfactual_coupling=dict(independent_initial_difference_variance=str(independent_variance),shared_initial_difference_variance='0',scope='Authored Bernoulli initial-state example,not actual upstream Gaussian draws.'),
        cost_usd={str(n):str(F(30000,n)) for n in [1000,600,400]})


if __name__=='__main__':
    print(json.dumps(calculate(),indent=2))

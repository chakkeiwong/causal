#!/usr/bin/env python3
"""Exact authored temporal references, independent of downloaded engines."""
from collections import defaultdict
from fractions import Fraction as F
import itertools
import json
import math
from temporal_reference_20261017 import ROOT,BASE


def multiply(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def encode(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,list):return [encode(v) for v in x]
    if isinstance(x,dict):return {k:encode(v) for k,v in x.items()}
    return x


def calculate():
    joint=defaultdict(F)
    for u,e_s,e_t in itertools.product([0,1],repeat=3):
        mass=F(1,2)*(F(1,4) if e_s else F(3,4))*(F(1,4) if e_t else F(3,4))
        joint[u^e_s,u^e_t]+=mass
    marginal_s={s:sum(p for (a,t),p in joint.items() if a==s) for s in [0,1]}
    marginal_t={t:sum(p for (s,b),p in joint.items() if b==t) for t in [0,1]}
    info=sum(float(p)*math.log2(float(p/(marginal_s[s]*marginal_t[t]))) for (s,t),p in joint.items())
    risks=[joint[a,1]/marginal_s[a] for a in [0,1]]
    i_minus_b0=[[F(1),F(0)],[F(-1,2),F(1)]]
    inverse=[[F(1),F(0)],[F(1,2),F(1)]]
    b1=[[F(1,2),F(0)],[F(0),F(1,4)]]
    m1=multiply(inverse,b1);m2=multiply(m1,m1)
    impulse=multiply(inverse,[[F(1)],[F(0)]])
    response=[impulse]
    for _ in range(2):response.append(multiply(m1,response[-1]))
    raw=[F(k,19) for k in range(20)]
    corrected=[F(k+1,20) for k in range(20)]
    return encode({
        'scope':'Project-authored exact finite laws/matrix arithmetic; no upstream engine or model execution',
        'common_calendar':{
            'law':'Independent fair daily U; source S=U xor Bernoulli(1/4); next outcome T=U xor independent Bernoulli(1/4). Earlier T independent of current U.',
            'joint_source_future':{f'{s},{t}':joint[s,t] for s,t in sorted(joint)},
            'conditional_future_risks':risks,'observational_risk_difference':risks[1]-risks[0],
            'do_source_future_risks':[F(1,2),F(1,2)],'true_do_effect':F(0),
            'transfer_information_bits':info,'conditional_information_given_calendar_bits':0,
            'stipulated_usd_per_event':100,'spurious_usd_per_account':100*(risks[1]-risks[0]),
            'units':'daily calendar shock shared across accounts; account copies do not create new shock units'},
        'structural_lags':{
            'b0':[[F(0),F(0)],[F(1,2),F(0)]],'b1':b1,'reduced_m1':m1,
            'recovered_b1':multiply(i_minus_b0,m1),'incorrect_inverse_result':multiply(inverse,m1),
            'two_step_reduced_transition':m2,'structural_impulse_responses_h0_h1_h2':response,
            'outcome_responses': [r[1][0] for r in response],
            'stipulated_usd_per_outcome_unit':100,'cumulative_first_three_usd':100*sum(r[1][0] for r in response),
            'clock':'One model step is one day; two-step observations span two days. A structural innovation impulse is distinct from setting a state coordinate.'},
        'unit_threshold':{
            'coefficient_million_usd':F(1,25),'coefficient_thousand_usd':F(40),'absolute_threshold':F(1,20),
            'first_flag':F(1,25)>F(1,20),'rescaled_flag':F(40)>F(1,20),
            'meaning':'Same monetary response, different coefficient magnitude; threshold flag supplies no p-value.'},
        'surrogate_rank':{
            'assumption':'Observed statistic and19 null replicates are continuous and exchangeable;20 equally likely ranks.',
            'replicates':19,'nominal_alpha':F(1,100),
            'raw_rejection_probability':F(sum(p<=F(1,100) for p in raw),20),
            'plus_one_rejection_probability':F(sum(p<=F(1,100) for p in corrected),20),
            'minimum_corrected_p':min(corrected),
            'limit':'Plus-one correction does not create exchangeability for an invalid temporal/conditional surrogate.'},
        'supplied_model_intervention':{
            'law':'Fair latent U, A=U xor independent Bernoulli(1/4), next-period Y=U.',
            'observational_risks':[F(1,4),F(3,4)],'do_risks':[F(1,2),F(1,2)],
            'observational_contrast':F(1,2),'do_contrast':F(0),
            'alternative_supplied_A_to_Y_model_effect':F(1,2),
            'meaning':'The observed two-variable law also fits an A-to-Y model; choosing supplied graph changes the intervention query.'},
        'regime_pooling':{
            'law':'Two equally weighted calendar eras; independent centered source with unit variance in each; slopes+1 and-1; mean-zero noise independent of source.',
            'regime_slopes':[F(1),F(-1)],'pooled_covariance':F(0),'pooled_linear_slope':F(0),
            'meaning':'Pooled zero linear prediction coefficient hides opposing era-specific effects; mechanism invariance needs its own assessment.'}
    })


if __name__=='__main__':
    with (BASE/'exact-results-v2.json').open('x') as stream:
        json.dump(calculate(),stream,indent=2);stream.write('\n')
    print(json.dumps({'families':6,'scope':'Exact authored references only; supersedes preliminary illustration without deleting it.'}))

#!/usr/bin/env python3
"""Authored exact references; no upstream workers or bank data are executed."""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
import json


def attempts(k, frozen=False):
    """Enumerate a result sign and four equiprobable transport states."""
    out=defaultdict(F); expected=F(0)
    signs=[(s,)*k for s in (-1,1)] if frozen else list(product((-1,1),repeat=k))
    den=len(signs)*4**k
    for ss in signs:
        for tt in product(range(4),repeat=k):
            ret='failure';n=k
            for i,(s,t) in enumerate(zip(ss,tt)):
                if s==1 or t==0:
                    ret=str(s);n=i+1;break
            out[ret]+=F(1,den);expected+=F(n,den)
    return dict(out),expected


def calculate():
    examples={}
    for k in (1,2,3,4):
        for frozen in (False,True):
            law,n=attempts(k,frozen)
            q={-1:F(1,4),1:F(1)};p=F(1,2);bar=F(5,8)
            if frozen:
                form={str(y):p*(1-(1-q[y])**k) for y in q}
                fail=sum(p*(1-q[y])**k for y in q)
                calls=sum(sum(p*(1-q[y])**j for y in q) for j in range(k))
            else:
                scale=sum((1-bar)**j for j in range(k))
                form={str(y):p*q[y]*scale for y in q}
                fail=(1-bar)**k;calls=scale
            assert law==dict(form,failure=fail) and n==calls
            success=1-fail
            examples[f'{"frozen" if frozen else "redraw"}_K{k}']={
                'all_assigned_law':law,'completion':success,
                'completed_positive':law['1']/success,
                'completed_mean':(law['1']-law['-1'])/success,
                'expected_calls':n}
    # A bridge with the same fair marginals loses perfect adaptive dependence.
    ref={(0,0):F(1,2),(1,1):F(1,2)}
    port={x:F(1,4) for x in product((0,1),repeat=2)}
    tv=sum(abs(ref.get(x,F(0))-port[x]) for x in port)/2
    assert tv==F(1,2)
    # Frozen-result inverse completion weighting, retaining all assigned cases.
    qk={-1:F(7,16),1:F(1)}
    mean=sum(F(1,2)*qk[y]*F(y)/qk[y] for y in qk)
    second=sum(F(1,2)*qk[y]*(F(y)/qk[y])**2 for y in qk)
    assert mean==0 and second==F(23,14)
    # Discrete path-switch example and an affine two-stage error recursion.
    x=F(3,25);dx=F(1,1000);eps1=F(1,500);eps2=F(1,10000)
    z1=2*x+1; z2=z1/10
    b1=2*(x+dx)+1+eps1;b2=b1/10+eps2
    e1=2*dx+eps1;e2=e1/10+eps2
    assert e1==F(1,250) and e2==F(1,2000) and b2-z2==e2
    # An imperfect q estimate: bound on selection-corrected mean bias.
    qhat={-1:F(1,2),1:F(1)}
    corrected=sum(F(1,2)*qk[y]*F(y)/qhat[y] for y in qk)
    assert corrected==F(1,16)
    # Ratio envelope for first-success selection, a bounded reported value.
    weighted_mean=F(3,5);qbar=F(5,8)
    lo=(weighted_mean-F(1,10))/(1+F(1,10))
    hi=(weighted_mean+F(1,10))/(1-F(1,10))
    assert lo==F(5,11) and hi==F(7,9)
    return dict(status='pass',evidential_status='project-authored finite construction',
        upstream_execution=False,bank_calibration=False,retry_examples=examples,
        adaptive_joint_total_variation=tv,
        affine_composition=dict(source=z2,bridge=b2,error=e2,stage_one_error=e1),
        inverse_selection=dict(mean=mean,second_moment=second,variance=second,
            imperfect_q_bias=corrected,positivity_required=True),
        uncertainty_envelope=dict(relative_completion_error=F(1,10),mean_min=lo,mean_max=hi),
        checks=['Independent exhaustive latent-sign/transport-state paths equal closed forms for K1–4.',
                'Frozen and redrawn retries have distinct completion and returned laws.',
                'Fair marginals conceal a total-variation joint-law error of1/2.',
                'Affine recursion attains the composed error bound exactly.',
                'Inverse completion weighting is unbiased only with the correct positive completion law.'])


def serial(obj):
    if isinstance(obj,F):return str(obj)
    if isinstance(obj,dict):return {k:serial(v) for k,v in obj.items()}
    if isinstance(obj,list):return [serial(x) for x in obj]
    return obj


if __name__=='__main__':
    print(json.dumps(serial(calculate()),indent=2))

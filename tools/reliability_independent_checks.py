#!/usr/bin/env python3
"""Independent limiting likelihood/value and joint validation variance checks."""
import json
import numpy as np
from scipy.special import expit
from scipy.stats import norm
from threadpoolctl import threadpool_limits
from reliability_common import ROOT,SPEC
from closure_common import save
from causalbank.nonlinear_variance import TRUTH,engine,simulate
from causalbank.nonlinear_audited import EPSILON
from causalbank.joint_audited import joint_effect
from reliability_joint_study import sample


def kalman(p,data):
    m=np.full(len(data),p[13]);v=np.full(len(data),np.exp(p[14]));ll=np.zeros(len(data))
    for t in range(data.shape[1]):
        o,a,r=data[:,t].T;variance=v+np.exp(p[4]);ll+=norm.logpdf(o,m,np.sqrt(variance));gain=v/variance;m+=gain*(o-m);v*=1-gain
        prob=EPSILON+(1-2*EPSILON)*expit(p[5]+p[7]*o);ll+=np.where(a==1,np.log(prob),np.log1p(-prob))
        loading=p[9]+p[11]*a;mean=p[8]+p[10]*a+loading*m;variance=loading**2*v+np.exp(p[12]);ll+=norm.logpdf(r,mean,np.sqrt(variance));gain=v*loading/variance;m+=gain*(r-mean);v-=gain*loading*v
        m=p[0]*m+p[2]*a;v=p[0]**2*v+np.exp(p[3])*(1-a)+np.exp(p[15])*a
    return ll


def main():
    s=json.loads((ROOT/SPEC).read_text());policy=np.asarray(json.loads((ROOT/s['nonlinear']['policy_source']).read_text())['planning']['selected_policy']);p=TRUTH.copy();p[1]=0;p[6]=0
    with threadpool_limits(limits=1):
        e=engine(101,10.);data,states=simulate(p,10,4,np.random.default_rng(821300));exact_error=float(np.max(abs(np.asarray(e['observed'](p,data))-kalman(p,data))))
        p=TRUTH;value_gradient=np.asarray(e['value_gradient'](p,policy));numeric=[]
        for j in range(16):
            delta=np.eye(16)[j]*1e-5;numeric.append((float(e['value'](p+delta,policy))-float(e['value'](p-delta,policy)))/2e-5)
        value_error=float(np.max(abs(value_gradient-numeric)))
        a,y,r,label,q,gold,g=sample(s['joint'],np.random.default_rng(821301));out=joint_effect(a,y,r,label,q,bandwidth=7,gold_errors=gold)
        eps=gold.mean();h=1e-6
        lower=joint_effect(a,y,r,label,q,bandwidth=7,known_label_error=eps-h);upper=joint_effect(a,y,r,label,q,bandwidth=7,known_label_error=eps+h)
        finite=(upper['estimate']-lower['estimate'])/(2*h);validation=finite**2*eps*(1-eps)/len(gold)
        gold_error=abs(validation-out['variance_components']['validation'])
    checks=dict(action_variance_gaussian_limit=bool(exact_error<1e-6),all16_value_directions=bool(value_error<1e-7),joint_gold_variance_independent_difference=bool(gold_error<1e-5))
    save('docs/reviews/reliability-independent-algebra.json',dict(status='pass' if all(checks.values()) else 'fail',checks=checks,gaussian_error=exact_error,value_gradient_error=value_error,gold_variance_error=gold_error,
        scope='Independently coded algebra within author verification; not external independent review.'),['tools/reliability_independent_checks.py','tools/reliability_joint_study.py','src/causalbank/joint_audited.py','src/causalbank/nonlinear_variance.py','src/causalbank/nonlinear_audited.py',SPEC,s['nonlinear']['policy_source']])
    print(json.dumps(dict(checks=checks,gaussian_error=exact_error,value_gradient_error=value_error,gold_variance_error=gold_error)))
    raise SystemExit(not all(checks.values()))

if __name__=='__main__':main()

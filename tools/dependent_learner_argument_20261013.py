#!/usr/bin/env python3
"""Exact references for a restricted independent-pilot PLIV argument."""
from fractions import Fraction as F
from itertools import product
import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-13/dependent-learner'
ARGUMENT = ROOT / 'docs/program/comprehensive-v14/work/SCI.ARGUMENT.R05S/argument-and-counterexamples.md'


def ref(path, anchor):
    return {'path': str(path.relative_to(ROOT)), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'anchor': anchor}


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def ratio_projection(a, b, c, d):
    """Exact rational rectangle image; None represents an infinite endpoint."""
    if a > b or c > d:
        return []
    if a <= 0 <= b and c <= 0 <= d:
        return [(None, None)]
    pieces = []
    def positive(lo, hi, qlo, qhi):
        if qhi <= 0:
            return
        if qlo > 0:
            corners = [lo/qlo, lo/qhi, hi/qlo, hi/qhi]
            pieces.append((min(corners), max(corners)))
        elif lo > 0:
            pieces.append((lo/qhi, None))
        elif hi < 0:
            pieces.append((None, hi/qhi))
        else:
            raise AssertionError('zero-zero already handled')
    positive(a, b, max(c, F(0)), d)
    positive(-b, -a, max(-d, F(0)), -c)
    pieces.sort(key=lambda v: (v[0] is not None, v[0] or 0))
    merged = []
    for lo, hi in pieces:
        if merged and (merged[-1][1] is None or lo is None or lo <= merged[-1][1]):
            old = merged[-1]
            merged[-1] = (old[0], None if old[1] is None or hi is None else max(old[1], hi))
        else:
            merged.append((lo, hi))
    return merged


def contains(pieces, theta):
    return any((lo is None or lo <= theta) and (hi is None or theta <= hi) for lo, hi in pieces)


def direct_feasible(a, b, c, d, theta):
    if a > b or c > d:
        return False
    left, right = sorted([theta*c, theta*d])
    return max(a, left) <= min(b, right)


def encode_set(pieces):
    topology = ('empty' if not pieces else 'whole_line' if pieces == [(None, None)] else
                'unbounded_union' if any(a is None or b is None for a,b in pieces) else
                'finite_interval' if len(pieces) == 1 else 'finite_union')
    return {'topology': topology, 'exact_intervals': [[None if x is None else str(x) for x in pair] for pair in pieces],
            'intervals': [[None if x is None else float(x) for x in pair] for pair in pieces]}


def main():
    BASE.mkdir(parents=True, exist_ok=True)
    # Complete finite law for a correctly specified PLIV model and fixed errors.
    rows = []
    theta = F(6,5)
    for x,v,eta,epsilon in product([-1,1], repeat=4):
        z=F(3,10)*x+v; a=F(4,5)*z+F(1,5)*x+eta; y=theta*a+F(2,5)*x+epsilon
        mz=F(3,10)*x; ma=F(11,25)*x; my=F(116,125)*x
        dz=F(1,10)*x; da=F(3,10)*x; dy=F(1,5)*x
        rows.append([(z-mz)*(y-my),(z-mz)*(a-ma),
                     (z-mz-dz)*(y-my-dy),(z-mz-dz)*(a-ma-da),dz*dy,dz*da])
    means=[sum(x[j] for x in rows)/len(rows) for j in range(6)]
    assert means[2]-means[0] == means[4] == F(1,50)
    assert means[3]-means[1] == means[5] == F(3,100)
    assert means[0] == theta*means[1]
    assert means[2]-theta*means[3] == F(-2,125)
    identities={'finite_law_size':len(rows),'moments_exact':[str(x) for x in means],
                'score_bias_exact':str(means[2]-theta*means[3]), 'truth':str(theta),
                'method':'Exhaustive arithmetic over all independent sign combinations; no random draws'}
    # Fixed orthogonal design with a noise coordinate orthogonal to every feature.
    signs=np.asarray(list(product([-1.,1.],repeat=5)))
    x=signs[:,:4]; beta=np.array([.5,.25,0.,0.]); y=x@beta+.1*signs[:,4]; lam=.1
    exact=np.array([.4,.15,0.,0.])
    def objective(z):
        b=z[:4]-z[4:]; e=y-x@b
        return float(e@e/(2*len(x))+lam*z.sum())
    def gradient(z):
        b=z[:4]-z[4:]; grad=x.T@(x@b-y)/len(x)
        return np.r_[grad+lam,-grad+lam]
    opt=minimize(objective,np.zeros(8),jac=gradient,bounds=[(0,None)]*8,
                 method='L-BFGS-B',options={'ftol':1e-15,'gtol':1e-12,'maxiter':1000})
    candidate=opt.x[:4]-opt.x[4:]
    assert opt.success and np.max(abs(candidate-exact))<1e-9
    h=exact-beta; empirical=float(np.mean((x@h)**2)); population=float(h@h)
    assert np.max(abs(x.T@x/len(x)-np.eye(4)))==0
    assert max(abs(x.T@(y-x@beta)/len(x)))<lam/2
    assert empirical<=3*lam*sum(abs(h[:2]))+1e-12
    assert population<=9*2*lam**2+1e-12
    lasso={'rows':len(x),'features':4,'support':2,'penalty':lam,'soft_threshold':exact.tolist(),
           'separate_optimizer':candidate.tolist(),'maximum_difference':float(max(abs(candidate-exact))),
           'population_squared_error':population,'bound_squared_error':9*2*lam**2,
           'gram_discrepancy':0,'cone_eigenvalue':1,'interpretation':'Exact selected-design check, not a probability statement for arbitrary random pilots'}
    # Independent geometry comparison over every rational rectangle on this grid.
    pairs=[(F(a),F(b)) for a in [-2,-1,0,1,2] for b in [-2,-1,0,1,2] if a<=b]
    checked=0
    for (a,b),(c,d) in product(pairs,repeat=2):
        pieces=ratio_projection(a,b,c,d)
        probes={F(k,4) for k in range(-40,41)}
        for interval in pieces:
            for endpoint in interval:
                if endpoint is not None:
                    probes.update([endpoint-F(1,1000),endpoint,endpoint+F(1,1000)])
        for t in probes:
            assert contains(pieces,t)==direct_feasible(a,b,c,d,t),(a,b,c,d,t,pieces)
            checked+=1
    examples={
        'rays':(F(1),F(2),F(-1,2),F(1,2)),
        'whole_line':(F(-1),F(1),F(-1,2),F(1,2)),
        'empty':(F(1),F(2),F(0),F(0)),
        'singleton':(F(1),F(1),F(2),F(2)),
        'strong_illustrative':(F(91,100),F(101,100),F(78,100),F(82,100))}
    projected={k:encode_set(ratio_projection(*v)) for k,v in examples.items()}
    assert projected['rays']['exact_intervals']==[[None,'-2'],['2',None]]
    assert projected['strong_illustrative']['exact_intervals']==[['91/82','101/78']]
    assert contains(ratio_projection(*examples['strong_illustrative']),F(23,20))
    # Omitted nonlinear term in the actual preserved R05-v2 generator.
    h_variance=F(3,5)**2*(F(3)-F(1))
    bias=h_variance/(F(4,5)*(1+h_variance))
    assert h_variance==F(18,25) and bias==F(45,86)
    cost=[]
    for p,s,m in [(20,3,1024),(60,3,1024),(20,8,1024),(60,8,65536),(60,8,1048576)]:
        lam=2*math.sqrt(2*math.log(2*p/.005)/m)
        tau=math.sqrt(2*math.log(2*p*p/.005)/m)
        bound=math.sqrt(9*s*lam**2+144*tau*s*s*lam**2)
        cost.append({'features':p,'support':s,'pilot_rows':m,'lambda':lam,'gram_bound':tau,
                     'nuisance_norm_bound':bound,'two_equal_error_product':bound**2})
    predecessor=json.loads((ROOT/'docs/program/master/work/R05-v2/results.json').read_text())
    baseline=[{'design':c['design'], **{k:c['methods']['nested_sparse'][k] for k in
                ['covered','requests','simultaneous_lower95','width_quantiles','minimum_95_screen']}}
              for c in predecessor['cells']]
    result={'status':'pass','issues':[], 'kind':'project_exact_derivation_checks','random_draws':0,
            'finite_moment_identity':identities,'lasso_reference':lasso,
            'projection':{'rectangles':len(pairs)**2,'exact_membership_comparisons':checked,'examples':projected},
            'nonlinear_omission':{'variance_exact':str(h_variance),'limiting_shift_exact':str(bias),
                                  'limiting_shift':float(bias),'not_a_finite_sample_bias_prediction':True},
            'certificate_planning':{'premises':'K=E=kappa=1, exact approximation, each pilot event allocation .005; kappa assumed certified, no simulated pilot',
                                     'rows':cost},
            'preserved_v2_results':baseline,
            'perfect_dependence':{'row_counts':[1,16,1024],'variance_of_mean':[1,1,1],
                                  'law':'Every row is the same fair sign; exact two-state enumeration'},
            'evidence':[ref(Path(__file__),'Exact sign-law, optimizer and independent rectangle-feasibility checks'),
                         ref(ROOT/'docs/program/master/work/R05-v2/results.json','Preserved actual successor outcomes'),
                         ref(ROOT/'tools/master_r05_v2.py','Actual nonlinear generator'),
                         ref(ARGUMENT,'Reviewed derivation and explicit information requirements')]}
    write(BASE/'exact-results.json',result)
    print(json.dumps({'status':'pass','moment_worlds':len(rows),'projection_comparisons':checked,
                      'optimizer_error':lasso['maximum_difference'],'nonlinear_shift':float(bias)}))


if __name__=='__main__':
    main()

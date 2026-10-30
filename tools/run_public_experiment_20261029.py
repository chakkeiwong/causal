"""Prespecified NSW subset analysis; conditional research example, not bank evidence."""
from pathlib import Path
from hashlib import sha256
import json
import platform
import time
import numpy as np
import pandas as pd
import scipy
from scipy.stats import norm

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/scientific-gap-closure/2026-10-29'
COLS = ['treat','age','educ','black','hisp','marr','nodegree','re74','re75','re78']


def fit(y, design):
    n, k = design.shape
    coef, _, rank, singular = np.linalg.lstsq(design, y, rcond=None)
    if rank != k:
        raise ValueError('Singular design')
    inverse = np.linalg.pinv(design)
    residual = y - design @ coef
    h = np.sum(design * inverse.T, axis=1)
    if h.max() >= 1 - 1e-10:
        raise ValueError('Unit leverage')
    cov = {}
    for name, power in [('HC2', 1), ('HC3', 2)]:
        meat = residual**2 / (1-h)**power
        cov[name] = (inverse * meat) @ inverse.T
    return coef, cov, h, singular


def estimate(y, a, x, method):
    if method == 'unadjusted':
        treated, control = y[a == 1], y[a == 0]
        b = treated.mean() - control.mean()
        variance = treated.var(ddof=1)/len(treated) + control.var(ddof=1)/len(control)
        design = np.column_stack([np.ones(len(y)), a])
    elif method == 'common_slope':
        design = np.column_stack([np.ones(len(y)), a, x])
        b = variance = None
    else:
        design = np.column_stack([np.ones(len(y)), a, x, a[:,None]*x])
        b = variance = None
    coef, cov, h, singular = fit(y, design)
    if method == 'unadjusted':
        assert np.isclose(b, coef[1], rtol=1e-10)
        assert np.isclose(variance, cov['HC2'][1,1], rtol=1e-10)
    else:
        b, variance = coef[1], cov['HC2'][1,1]
    z = norm.ppf(.975)
    se = np.sqrt(variance)
    lo, hi = b-z*se, b+z*se
    if method == 'interacted':
        # Independently fit each arm and standardise to the pooled covariate mean.
        arm = []
        for group in [0,1]:
            keep = a == group
            coef_arm, _, _, _ = fit(y[keep], np.column_stack([np.ones(keep.sum()),x[keep]]))
            arm.append(coef_arm[0])
        assert np.isclose(arm[1]-arm[0], b, rtol=1e-10)
    return dict(method=method, estimate=float(b), variance=float(variance), standard_error=float(se),
                interval=[float(lo),float(hi)], hc3_standard_error=float(np.sqrt(cov['HC3'][1,1])),
                max_leverage=float(h.max()), condition_number=float(singular[0]/singular[-1]))


def main():
    started=time.monotonic()
    plan_path=OUT/'study-plan.json'
    plan=json.loads(plan_path.read_text())
    paths=[ROOT/p for p in plan['data']]
    arrays=[np.loadtxt(p) for p in paths]
    assert [len(a) for a in arrays] == [185,260]
    assert np.all(arrays[0][:,0]==1) and np.all(arrays[1][:,0]==0)
    data=np.vstack(arrays)
    assert data.shape==(445,10) and np.isfinite(data).all()
    df=pd.DataFrame(data,columns=COLS)
    df.to_csv(OUT/'analysis-data.csv',index=False)
    a=df.treat.to_numpy(); y=df.re78.to_numpy()
    raw=df[plan['covariates']].to_numpy()
    x=(raw-raw.mean(axis=0))/raw.std(axis=0,ddof=1)
    methods=[estimate(y,a,x,m) for m in ['unadjusted','common_slope','interacted']]
    mirror=pd.read_stata(ROOT/'docs/literature/raw/pd15_nsw_data.txt')[COLS].to_numpy()
    # Match multisets rather than assuming the mirror has author row order.
    def ordered(v):
        return v[np.lexsort(tuple(v[:,j] for j in range(v.shape[1]-1,-1,-1)))]
    mirror_delta=float(np.max(np.abs(ordered(data)-ordered(mirror))))
    balance=[]
    for j,name in enumerate(plan['covariates']):
        v1=raw[a==1,j];v0=raw[a==0,j]
        sd=np.sqrt((v1.var(ddof=1)+v0.var(ddof=1))/2)
        balance.append(dict(variable=name,treated_mean=float(v1.mean()),control_mean=float(v0.mean()),
                            standardized_difference=float((v1.mean()-v0.mean())/sd)))
    subgroups=[]
    for label,mask in [('zero_1975',df.re75.to_numpy()==0),('positive_1975',df.re75.to_numpy()>0)]:
        r=estimate(y[mask],a[mask],x[mask],'unadjusted')
        subgroups.append(dict(group=label,n=int(mask.sum()),treated=int(a[mask].sum()),result=r,
                              interpretation='Descriptive prespecified subgroup; no multiplicity-controlled policy selection'))
    loo=[]
    for i in range(len(y)):
        mask=np.arange(len(y))!=i
        loo.append(float(y[mask & (a==1)].mean()-y[mask & (a==0)].mean()))
    decisions=[]
    for m in methods:
        for cost in plan['defaults']['thresholds']:
            decisions.append(dict(method=m['method'],illustrative_cost=cost,net_point=m['estimate']-cost,
                net_interval=[v-cost for v in m['interval']],
                lower_bound_supports_spending=m['interval'][0]>cost))
    baseline=methods[0]
    bias=[dict(absolute_bias_bound=b,interval=[baseline['interval'][0]-b,baseline['interval'][1]+b])
          for b in plan['defaults']['bias_bounds']]
    out=dict(plan_sha256=sha256(plan_path.read_bytes()).hexdigest(),code_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        source_hashes={str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in paths},
        versions=dict(python=platform.python_version(),numpy=np.__version__,pandas=pd.__version__,scipy=scipy.__version__),
        n=len(y),n_treated=int(a.sum()),n_control=int(len(y)-a.sum()),
        methods=methods,balance=balance,subgroups=subgroups,decisions=decisions,bias_sensitivity=bias,
        outcome_diagnostics=dict(zero_share=float(np.mean(y==0)),max=float(y.max()),
                                 leave_one_out_unadjusted_range=[min(loo),max(loo)]),
        mirror_max_absolute_difference=mirror_delta,
        independent_algebra_checks='pass', empirical_coverage_measured=False,
        target=plan['target'],assumptions=plan['assumptions'],limits=plan['limits'],
        source_terms='Author currently states CC BY-NC 2.0. Local methodological research; no commercial redistribution authorisation.',
        heuristic_dominance=dict(verdict='No estimator superiority established from one realised experiment',
                                 comparators=[m['method'] for m in methods],situations=plan['conditional_situations']),
        seconds=round(time.monotonic()-started,3))
    (OUT/'study-results.json').write_text(json.dumps(out,indent=2)+chr(10))
    print(json.dumps({k:out[k] for k in ['n','methods','mirror_max_absolute_difference','seconds']}))


if __name__=='__main__':
    main()

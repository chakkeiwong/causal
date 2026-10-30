"""Check panel arithmetic against explicit dummy-variable regressions."""
from pathlib import Path
import json
import numpy as np
from run_funding_study_20261029 import fit

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'docs/scientific-gap-closure/2026-10-29'

def main():
    rng = np.random.default_rng(93415)
    N,T = 9,7
    x = rng.normal(size=(N,T)); y = .4*x+rng.normal(size=(N,T))
    unit = np.repeat(np.arange(N),T); date = np.tile(np.arange(T),N)
    z = np.column_stack([np.ones(N*T),np.eye(N)[unit,1:],np.eye(T)[date,1:],x.ravel()])
    inv = np.linalg.inv(z.T@z); b = inv@z.T@y.ravel(); e = y.ravel()-z@b
    h = np.einsum('ij,jk,ik->i',z,inv,z)
    hc2 = inv@(z.T@((e**2/(1-h))[:,None]*z))@inv
    def cluster(ids):
        score = np.array([(z[ids==g]*e[ids==g,None]).sum(axis=0) for g in np.unique(ids)])
        G = len(score); n,k = z.shape
        return G/(G-1)*(n-1)/(n-k)*(inv@score.T@score@inv)
    cov_u = cluster(unit); cov_two = cov_u+cluster(date)-cluster(np.arange(N*T))
    actual = {r['method']:r for r in fit(x,y)}
    errors = {'coefficient':abs(actual['within_HC2']['estimate']-b[-1]),
      'HC2':abs(actual['within_HC2']['variance']-hc2[-1,-1]),
      'institution':abs(actual['within_institution']['variance']-cov_u[-1,-1]),
      'two_way':abs(actual['within_two_way']['variance']-cov_two[-1,-1])}
    assert max(errors.values())<1e-10
    result = json.loads((OUT/'funding-results.json').read_text())
    rows = json.loads((OUT/'funding-replications.json').read_text())
    for summary in result['scenarios']:
        sub = [r for r in rows if all(r[k]==summary[k] for k in ['scenario','method'])]
        assert len(sub)==300
        assert sum(r['covered'] for r in sub)/300==summary['coverage_all_requests']
        assert sum(not r['available'] for r in sub)==summary['unavailable']
        assert all(not r['covered'] and r['width'] is None for r in sub if not r['available'])
    unavailable = [r for r in rows if not r['available']]
    report = dict(status='pass',explicit_dummy_regression_errors=errors,
      summaries_checked=len(result['scenarios']),unavailable_records=len(unavailable),
      all_request_denominators=True,nonpositive_variances_not_clipped=True,
      limitation='Independent arithmetic check, not a general finite-panel coverage theorem')
    (OUT/'funding-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))

if __name__=='__main__': main()

"""Exact project derivation: repeated noisy readings need independent information."""
from fractions import Fraction as F
from pathlib import Path
import json
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/scientific-gap-closure/2026-10-29'
rows=[]
for rho in [F(0),F(1,5),F(1,2),F(9,10)]:
    for m in [1,2,4,8,16]:
        s=F(1); effective=s*(rho+(1-rho)/m)
        tau=-F(1,5); beta=tau+effective/(1+2*effective)
        # Independently solve the full covariance system for A,W1,...,Wm.
        cov=np.full((m+1,m+1),1.0)
        cov[0,0]=2
        cov[1:,1:]+=float(rho*s)
        np.fill_diagonal(cov[1:,1:],1+float(s))
        cross=np.array([float(2*tau+1)]+[float(tau+1)]*m)
        solved=np.linalg.solve(cov,cross)[0]
        assert np.isclose(solved,float(beta),atol=1e-12)
        rows.append(dict(error_correlation=str(rho),readings=m,error_variance=str(effective),
                         adjusted_coefficient=str(beta),coefficient=float(beta),correct_negative_sign=beta<0,
                         independent_covariance_solution=float(solved)))
limits=[]
for rho in [F(0),F(1,5),F(1,2),F(9,10)]:
    floor=rho
    limits.append(dict(error_correlation=str(rho),variance_floor=str(floor),
                       limiting_coefficient=str(-F(1,5)+floor/(1+2*floor)),
                       finite_sign_repair_possible=floor<F(1,3)))
out=dict(kind='PROJECT_DERIVATION',law='U,eA,eY jointly independent centred unit Gaussians; Wj=U+ej; ej independent of U,eA,eY with equal variance s and pairwise error correlation rho',
         target='tau=-1/5 in Y=tau*A+U+eY, A=U+eA',
         question='Can repeated text measurements remove sign-reversing residual confounding?',
         formula='s_eff=s*(rho+(1-rho)/m); beta=tau+s_eff/(1+2*s_eff)',
         sign_condition='s_eff < 1/3 for tau=-1/5',rows=rows,limits=limits,
         conclusion='Independent readings can cross the sign threshold; a shared error floor at or above 1/3 prevents this repair for any finite number of readings.',
         assumptions='Exchangeable Gaussian error independent of action/outcome innovations; not established for any LLM. No live models or empirical causal claims.',
         verification='Exact rational expressions agree with full covariance-system solutions in 20 cases')
(OUT/'measurement-results.json').write_text(json.dumps(out,indent=2)+chr(10))
print(json.dumps(dict(cases=len(rows),verification='pass',limits=limits)))

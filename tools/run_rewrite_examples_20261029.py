"""Constructed estimator-to-financial report and independent exact checks."""
from pathlib import Path
from hashlib import sha256
import argparse
import json
import platform
import subprocess
import sys
import numpy as np
import scipy
from scipy.stats import t

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/developmental-rewrite/2026-10-29'

def digest(p): return sha256(p.read_bytes()).hexdigest()

def estimate_report(rows, weights, margin, increment, baseline, cost, alpha):
    cells=[];effect=0.;radius=0.
    for x,w in enumerate(weights):
        for a in [0,1]:
            y=rows[(rows[:,0]==x)&(rows[:,1]==a),2]
            if len(y)<2: raise ValueError('unsupported: fewer than two outcomes in a cell')
            mean=float(y.mean());sd=float(y.std(ddof=1))
            h=float(t.ppf(1-alpha/8,len(y)-1)*sd/np.sqrt(len(y)))
            effect+=w*(2*a-1)*mean;radius+=w*h
            cells.append({'stratum':x,'assigned_offer':a,'n':len(y),'mean':mean,'sd':sd,'halfwidth':h})
    lo,hi=effect-radius,effect+radius
    slope=margin-increment;intercept=-increment*baseline-cost
    net=slope*effect+intercept;bounds=sorted([slope*lo+intercept,slope*hi+intercept])
    recommendation='positive_under_declared_model' if bounds[0]>0 else ('negative_under_declared_model' if bounds[1]<0 else 'unresolved_at_declared_uncertainty')
    return {'target':'one-year household offer balance effect; equal target stratum weights',
            'cells':cells,'effect_gbp':effect,'interval_gbp':[lo,hi],
            'net_annual_gbp_per_household':net,'net_interval_gbp':bounds,
            'decision':recommendation,'evidence_class':'constructed normal independent-household example',
            'scope':'No bank validation; no MCP estimation implementation; no external estimator benchmark'}

def compute():
    p=json.loads((OUT/'example-plan.json').read_text());rng=np.random.default_rng(p['seed'])
    x=np.repeat([0,1],p['stratum_sizes']);a=(rng.random(len(x))<np.array(p['offer_probabilities'])[x]).astype(int)
    b=p['baseline_balance_gbp']+np.array(p['balance_effects_gbp'])[x]*a+rng.normal(0,p['outcome_normal_sd_gbp'],len(x))
    rows=np.column_stack([x,a,b]);r=estimate_report(rows,p['target_weights'],p['margin_per_year'],p['rate_increment_per_year'],p['baseline_balance_gbp'],p['direct_cost_gbp'],p['alpha'])
    return p,rows,r

def exact_checks():
    means=[];ipw=[]
    for policy in [0,1]:
        value=weighted=0.
        for l0 in [0,1]:
            for l1 in [0,1]:
                q=.1+.5*l0+.2*policy
                value+=.5*(q if l1 else 1-q)*(20+3*policy+4*policy+10*l1+6*l0)
        for l0 in [0,1]:
            e0=.2+.6*l0
            for a0 in [0,1]:
                q=.1+.5*l0+.2*a0
                for l1 in [0,1]:
                    e1=.15+.5*l1+.1*a0
                    for a1 in [0,1]:
                        prob=.5*(e0 if a0 else 1-e0)*(q if l1 else 1-q)*(e1 if a1 else 1-e1)
                        if a0==a1==policy:
                            weighted+=prob*(20+3*a0+4*a1+10*l1+6*l0)/((e0 if a0 else 1-e0)*(e1 if a1 else 1-e1))
        means.append(value);ipw.append(weighted)
    assert np.allclose(means,[26.5,35.5]) and np.allclose(means,ipw)
    sigma=np.array([[1,.6,.48],[.6,1.36,1.088],[.48,1.088,1.8704]])
    reconstructed=[];effects=[]
    for edges in [[(0,1),(1,2)],[(1,0),(1,2)],[(2,1),(1,0)]]:
        coef=np.zeros((3,3));var=np.diag(sigma).copy()
        for parent,child in edges:
            coef[child,parent]=sigma[child,parent]/sigma[parent,parent]
            var[child]-=coef[child,parent]**2*sigma[parent,parent]
        inverse=np.linalg.inv(np.eye(3)-coef);cov=inverse@np.diag(var)@inverse.T
        assert np.allclose(cov,sigma) and np.all(var>0)
        reconstructed.append(cov.tolist());effects.append(float(inverse[2,0]))
    K=np.array([[.9,.2],[.1,.8]]);shares=np.array([.5,.5]);moment=shares*np.array([100.,140.])
    observed=K@shares;joint=K@moment;naive=joint[1]/observed[1]-joint[0]/observed[0]
    corrected=np.linalg.solve(K,joint)/np.linalg.solve(K,observed)
    assert np.allclose(corrected,[100,140])
    return {'servicing':{'gformula_means':means,'ipw_means':ipw,'gross_contrast':means[1]-means[0],'cost_per_action':2,'net_contrast':means[1]-means[0]-4},
            'discovery':{'covariance':sigma.tolist(),'effects':effects,'action_percentage_points':.25,'cost_gbp':60,'net_values_gbp':[v*.25*1000-60 for v in effects],'reconstructed_covariances':reconstructed},
            'observation':{'K':K.tolist(),'observed_shares':observed.tolist(),'observed_joint_moments':joint.tolist(),'recorded_contrast':naive,'corrected_contrast':float(corrected[1]-corrected[0]),'cost_gbp':35,'net_recorded':naive-35,'net_corrected':float(corrected[1]-corrected[0]-35)},
            'deposit_accounting':{'break_even':30/.0275,'net_at_1000':.0275*1000-30,'net_at_2000':.0275*2000-30,'population_effect':1200,'population_net':3}}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--report-only',action='store_true');args=parser.parse_args()
    p,rows,r=compute()
    if args.report_only:
        print(json.dumps(r,sort_keys=True));return
    cli=json.loads(subprocess.check_output([sys.executable,__file__,'--report-only'],text=True))
    assert cli==r
    checks=exact_checks()
    results={'plan_sha256':digest(OUT/'example-plan.json'),'code_sha256':digest(Path(__file__)),
             'versions':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__},
             'report':r,'exact_checks':checks,'library_cli_equal':True,'mcp_estimation_executed':False}
    np.savetxt(OUT/'generated-deposit-data.csv',rows,delimiter=',',header='stratum,assigned_offer,balance_gbp',comments='',fmt=['%d','%d','%.17g'])
    results['data_sha256']=digest(OUT/'generated-deposit-data.csv')
    (OUT/'example-results.json').write_text(json.dumps(results,indent=2)+'\n')
    macros={'DepositEstimate':r['effect_gbp'],'DepositLow':r['interval_gbp'][0],'DepositHigh':r['interval_gbp'][1],
            'DepositNet':r['net_annual_gbp_per_household'],'DepositNetLow':r['net_interval_gbp'][0],'DepositNetHigh':r['net_interval_gbp'][1]}
    (OUT/'example-values.tex').write_text(''.join('\\newcommand{\\'+k+'}{'+f'{v:,.2f}'+'}\n' for k,v in macros.items()))
    print(json.dumps({'report':r,'exact_checks':checks,'library_cli_equal':True}))

if __name__=='__main__': main()

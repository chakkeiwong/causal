#!/usr/bin/env python3
"""Equal-output construction cost scenarios; assumptions, not bank forecasts."""
from pathlib import Path
import json
import os
os.environ.setdefault('MPLCONFIGDIR','/tmp/causal-matplotlib')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/derivations'

def cost(build,annual,per_study,studies,rate=.1):
    return build+sum((annual+per_study*n)/(1+rate)**t for t,n in enumerate(studies,1))

def main():
    a={'currency':'USD million','horizon_years':3,'discount_rate':.1,
       'expert':{'initial':1.,'annual_shared':.6,'per_completed_study':.15},
       'platform':{'initial':4.,'annual_shared':1.8,'per_completed_study':.06},
       'scope':'Both deliver the same completed studies, scientific comparisons, temporal/economic reconciliation, evidence and review; workflow automation differs. Planning assumptions, no measured productivity or vendor price.'}
    annuity=sum(1/1.1**t for t in range(1,4)); threshold=(3/annuity+1.2)/.09
    rows=[]
    for name,ns in [('Low reuse',[8]*3),('Moderate reuse',[24]*3),('High reuse',[36]*3),('Adoption ramp',[4,16,30])]:
        ec=cost(1,.6,.15,ns); pc=cost(4,1.8,.06,ns)
        gap=pc-ec
        rows.append({'scenario':name,'completed_studies':ns,'expert_present_cost':ec,'platform_present_cost':pc,'platform_cost_saving':ec-pc,'additional_constant_annual_decision_benefit_to_break_even':max(0,gap/annuity)})
    result={'assumptions':a,'annuity':annuity,'constant_annual_study_threshold':threshold,'scenarios':rows,'sensitivity':{'half_per_study_saving_threshold':(3/annuity+1.2)/.045,'annual_shared_gap_2m_threshold':(3/annuity+2)/.09},'pilot_budget':{'fte':6,'months':6,'loaded_person_month_usd':25000,'staff_usd':900000,'compute_usd':50000,'contingency_rate':.2,'total_usd':1140000,'included_in_platform_initial':True,'additional_bank_owner_validation_security_time':'unpriced; must be added consistently to both alternatives'}}
    (OUT/'economics.json').write_text(json.dumps(result,indent=2)+'\n')
    lines=[r'\begin{tabular}{@{}lrrr@{}}',r'\toprule Scenario & Expert cost & Platform cost & Platform saving\\\midrule']
    lines += [f'{r["scenario"]} & {r["expert_present_cost"]:.3f} & {r["platform_present_cost"]:.3f} & {r["platform_cost_saving"]:.3f}'+r'\\' for r in rows]
    lines += [r'\bottomrule\end{tabular}']
    (OUT/'reuse_economics.tex').write_text('\n'.join(lines)+'\n')
    n=np.arange(0,51); fig,ax=plt.subplots(figsize=(7.5,3.6)); ax.plot(n,[cost(1,.6,.15,[q]*3) for q in n],label='Expert composition'); ax.plot(n,[cost(4,1.8,.06,[q]*3) for q in n],label='Shared product'); ax.axvline(threshold,ls='--',color='gray',lw=.8); ax.set(xlabel='Completed equal-scope studies per year',ylabel='Three-year present cost, USD million'); ax.legend(); fig.tight_layout(); fig.savefig(OUT/'reuse_economics.pdf'); plt.close(fig)
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()

#!/usr/bin/env python3
"""Exact authored survival/longitudinal banking references, not package trials."""
from fractions import Fraction as F
from itertools import product


def calculate():
    competing = []
    for name, default, prepay in [('A',F(1,10),F(2,5)),('B',F(1,10),F(1,10))]:
        alive = F(1); dtotal = ptotal = exposure = F(0)
        path = []
        for k in [1,2]:
            dmass, pmass = alive*default, alive*prepay
            exposure += alive; dtotal += dmass; ptotal += pmass
            alive -= dmass+pmass
            path.append({'period':k,'default_mass':str(dmass),'prepay_mass':str(pmass),'alive_end':str(alive)})
        assert dtotal+ptotal+alive == 1
        # Two independent full categorical event draws reproduce the first-event law.
        ed = ep = ea = F(0)
        probs = {'D':default,'P':prepay,'S':1-default-prepay}
        for e1,e2 in product(probs,repeat=2):
            prob = probs[e1]*probs[e2]
            event = e1 if e1!='S' else e2
            ed += prob*(event=='D'); ep += prob*(event=='P'); ea += prob*(event=='S')
        assert (ed,ep,ea) == (dtotal,ptotal,alive)
        competing.append({'policy':name,'period_default_hazard':str(default),
            'period_prepayment_hazard':str(prepay),'path':path,
            'cumulative_default':str(dtotal),'cumulative_prepayment':str(ptotal),
            'expected_at_risk_periods':str(exposure),
            'net_default_risk_if_prepayment_removed_and_hazard_unchanged':str(1-(1-default)**2),
            'value_USD':str(10*exposure-100*dtotal-20*ptotal)})
    assert [r['value_USD'] for r in competing]==['-12','-18/5']
    immortal={'initial_cohort':100,'default_before_assignment':20,'assignment_day':2,
        'survivors_treated':40,'survivors_untreated':40,'later_defaults_each':10,
        'ever_treated_risk':str(F(10,40)),'ever_untreated_risk':str(F(30,60)),
        'spurious_baseline_risk_difference':str(F(10,40)-F(30,60)),
        'landmark_risks':[str(F(10,40)),str(F(10,40))],
        'scope':'Stipulated descriptive counts; landmark target conditions on survival and does not identify a baseline assignment policy.'}
    # A0 changes L; L changes A1 and Y. All conditional risks are in [0,1].
    def p_l(a):return F(1,5) if a else F(4,5)
    def p_a(l):return F(4,5) if l else F(1,5)
    def p_y(l,a):return F(1,10)+F(2,5)*l-F(1,20)*a
    law=[]
    for a0,l,a1,y in product([0,1],repeat=4):
        pl=p_l(a0) if l else 1-p_l(a0)
        pa=p_a(l) if a1 else 1-p_a(l)
        py=p_y(l,a1) if y else 1-p_y(l,a1)
        law.append((a0,l,a1,y,F(1,2)*pl*pa*py))
    assert sum(r[4] for r in law)==1
    obs=[]
    for a in [0,1]:
        mass=sum(p for a0,l,a1,y,p in law if a1==a)
        obs.append(sum(p*y for a0,l,a1,y,p in law if a1==a)/mass)
    regimes=[]
    for a0,a1 in [(0,0),(1,1)]:
        g=sum((p_l(a0) if l else 1-p_l(a0))*p_y(l,a1) for l in [0,1])
        ipw=sum(p*y/(F(1,2)*(p_a(l) if a1 else 1-p_a(l)))
                for aa0,l,aa1,y,p in law if (aa0,aa1)==(a0,a1))
        assert g==ipw
        regimes.append({'regime':[a0,a1],'gformula':str(g),'full_joint_ipw':str(ipw)})
    assert obs==[F(9,50),F(37,100)]
    assert [r['gformula'] for r in regimes]==['21/50','13/100']
    longitudinal={'law':[{'A0':a0,'L':l,'A1':a1,'Y':y,'mass':str(p)} for a0,l,a1,y,p in law],
        'observed_risks_A1_0_1':list(map(str,obs)),'observed_difference':str(obs[1]-obs[0]),
        'fixed_regimes':regimes,'regime_difference':str(F(13,100)-F(21,50)),
        'direct_A1_risk_difference_at_L':str(F(-1,20)),
        'controlled_A0_difference_at_fixed_L_A1':'0',
        'assumptions':'Stipulated independent randomizers, consistency, sequential exchangeability and positive treatment support; no fitted estimator.'}
    censoring={'high_risk_fraction':'1/2','default_risks_low_high':['1/10','3/5'],
        'observed_fractions_low_high':['1','1/4'],
        'full_cohort_risk':str(F(1,2)*F(1,10)+F(1,2)*F(3,5)),
        'complete_case_risk':str((F(1,2)*F(1,10)+F(1,2)*F(1,4)*F(3,5))/(F(1,2)+F(1,2)*F(1,4))),
        'inverse_observation_weighted_risk':str(F(1,2)*F(1,10)+F(1,2)*F(1,4)*F(3,5)/F(1,4)),
        'assumptions':'Horizon missingness independent of Y given observed stratum; observation probabilities are known in this construction, not estimated.'}
    assert censoring['full_cohort_risk']=='7/20' and censoring['complete_case_risk']=='1/5'
    n=8;missing=sum(1 for draw in product(range(n),repeat=4) if 0 not in draw)
    # Four-draw enumeration checks the general zero-cell expression; eight-draw probability is exact.
    assert F(missing,n**4)==F(7,8)**4
    bootstrap={'subjects':8,'rare_path_subjects':1,'draws':8,
        'probability_rare_path_missing':str(F(7,8)**8),
        'expected_failed_out_of_1000':str(1000*F(7,8)**8),
        'scope':'Undefined unregularized path-specific mean when no rare subject is resampled; no vendor failure rate or universal bootstrap invalidity claim.'}
    return {'kind':'exact_authored_banking_examples','empirical_data':False,'vendor_runtime':False,
        'competing_events':competing,'immortal_time':immortal,'time_varying_confounding':longitudinal,
        'informative_observation':censoring,'rare_path_bootstrap':bootstrap}


if __name__=='__main__':
    import json
    print(json.dumps(calculate(),indent=2))

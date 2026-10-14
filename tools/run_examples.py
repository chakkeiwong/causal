#!/usr/bin/env python3
"""Small reproducible constructions, not performance or real-bank validation."""
import itertools
import json
import math
import os
from pathlib import Path
import platform
import time

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / "docs/examples/mpl-cache"))
import numpy as np
import scipy
from scipy.optimize import minimize
from scipy.stats import norm
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def longitudinal():
    rows = []
    for l0, a0, l1, a1 in itertools.product([0, 1], repeat=4):
        e0 = .2 + .6 * l0
        p1 = .1 + .5 * l0 + .2 * a0
        e1 = .15 + .5 * l1 + .1 * a0
        prob = .5 * (e0 if a0 else 1-e0) * (p1 if l1 else 1-p1) * (e1 if a1 else 1-e1)
        y = 20 + 3*a0 + 4*a1 + 10*l1 + 6*l0
        rows.append(dict(l0=l0,a0=a0,l1=l1,a1=a1,e0=e0,e1=e1,p=prob,y=y))
    means, naive, ipw = {}, {}, {}
    for policy in [0,1]:
        mask = [x for x in rows if x['a0']==policy and x['a1']==policy]
        naive[policy] = sum(x['p']*x['y'] for x in mask)/sum(x['p'] for x in mask)
        ipw[policy] = sum(x['p']*x['y']/((x['e0'] if policy else 1-x['e0'])*(x['e1'] if policy else 1-x['e1'])) for x in mask)
        means[policy] = sum(.5*(20+3*policy+4*policy+10*(.1+.5*l0+.2*policy)+6*l0) for l0 in [0,1])
    assert abs(sum(x['p'] for x in rows)-1)<1e-12
    assert all(abs(means[a]-ipw[a])<1e-11 for a in [0,1])
    assert abs(means[1]-means[0]-9)<1e-12
    return {'truth_means':means,'observed_adherer_means':naive,'ipw_means':ipw,'true_contrast':means[1]-means[0],'naive_contrast':naive[1]-naive[0],'conditional_regression_direct_sum':7.,'enumerated_rows':rows}


def static_aipw(rng):
    n=40000
    x=rng.binomial(1,.5,n);e=.2+.6*x;a=rng.binomial(1,e)
    y=100+80*x+(10-4*x)*a+rng.normal(0,20,n)
    folds=np.arange(n)%5
    score=np.empty(n)
    for fold in range(5):
        train=folds!=fold;test=~train
        for level in [0,1]:
            sub=train&(x==level);idx=test&(x==level)
            eh=a[sub].mean();m0=y[sub&(a==0)].mean();m1=y[sub&(a==1)].mean()
            score[idx]=m1-m0+a[idx]*(y[idx]-m1)/eh-(1-a[idx])*(y[idx]-m0)/(1-eh)
    estimate=float(score.mean());se=float(score.std(ddof=1)/np.sqrt(n))
    assert abs(estimate-8)<6*se
    # Three fixed comparisons evaluated on paired scores. Policies are declared
    # by the toy problem, not optimized on these evaluation outcomes.
    all_score=score-7
    targeted_score=(1-x)*(score-7)
    critical=float(norm.isf(.05/(2*3)))
    comparisons=[]
    for label,v,truth in [('all versus none',all_score,1.),('X=0 versus none',targeted_score,1.5),('X=0 versus all',targeted_score-all_score,.5)]:
        sd=float(v.std(ddof=1)/np.sqrt(n));mean=float(v.mean())
        comparisons.append({'comparison':label,'truth':truth,'estimate':mean,'iid_se':sd,'simultaneous_ci95':[mean-critical*sd,mean+critical*sd]})
    return {'n':n,'true_ate':8.,'population_naive_difference':54.8,'sample_naive_difference':float(y[a==1].mean()-y[a==0].mean()),'aipw':estimate,'iid_se':se,'ci95':[estimate-1.96*se,estimate+1.96*se],'nuisance_model':'five-fold saturated binary-X cell means and propensities','policy_comparison':{'offer_cost':7,'critical_value':critical,'method':'Paired AIPW scores; Bonferroni across three predeclared comparisons; asymptotic iid normal intervals','comparisons':comparisons},'note':'Independent synthetic people; the IID SE does not apply to a bank panel.'}


def staggered():
    # Three cohorts, four dates. Early effects grow; later effects are small.
    d=np.array([[0,1,1,1],[0,0,0,1],[0,0,0,0]],float)
    effects=np.array([[0,1,4,8],[0,0,0,1],[0,0,0,0]],float)
    y0=np.arange(3)[:,None]*2+np.arange(4)[None,:]*.5
    y=y0+effects
    demean=lambda z:z-z.mean(0)[None,:]-z.mean(1)[:,None]+z.mean()
    dd=demean(d);yy=demean(y)
    beta=float((dd*yy).sum()/(dd*dd).sum())
    weights=dd*d/(dd*dd).sum()
    truth=float(effects[d==1].mean())
    clean=[]
    for i in [0,1]:
        g=int(np.flatnonzero(d[i])[0])
        for t in range(g,4):
            clean.append(float((y[i,t]-y[i,g-1])-(y[2,t]-y[2,g-1])))
    assert abs(sum(clean)/len(clean)-truth)<1e-12
    assert abs((weights*effects).sum()-beta)<1e-12
    return {'twfe':beta,'att':truth,'clean_group_time_average':sum(clean)/len(clean),'treatment_weights':weights.tolist(),'effects':effects.tolist(),'outcomes':y.tolist(),'has_negative_treatment_weight':bool((weights[d==1]<0).any())}


def pomdp(rng):
    # R_t and O_{t+1} are conditionally independent given the shown state/action
    # after integrating S_{t+1}; rewards excluded from this tiny filtering case.
    p0=np.array([.7,.3]);B=np.array([[.8,.2],[.2,.8]])
    P=np.array([[[.9,.1],[.25,.75]],[[.95,.05],[.55,.45]]])
    reward=np.array([[12.,10.],[-8.,1.]])
    actions=[1,0,1];obs=[1,0,1,1]
    alpha=p0*B[:,obs[0]];scales=[float(alpha.sum())];beliefs=[(alpha/alpha.sum()).tolist()]
    for a,o in zip(actions,obs[1:]):
        alpha=alpha@P[a]*B[:,o];beliefs.append((alpha/alpha.sum()).tolist())
    forward=float(alpha.sum())
    enumerated=0.
    for states in itertools.product([0,1],repeat=4):
        p=p0[states[0]]*B[states[0],obs[0]]
        for t,a in enumerate(actions):p*=P[a,states[t],states[t+1]]*B[states[t+1],obs[t+1]]
        enumerated+=p
    assert abs(forward-enumerated)<1e-14
    # Identification counterexample: positive marginal support with equal P(A,Y).
    observational=[]
    for a,y in itertools.product([0,1],repeat=2):
        prob_a=0.;prob_b=.5*((.32+.36*a) if y else (1-.32-.36*a))
        for u in [0,1]:
            ea=.2+.6*u;py=.2+.6*u
            prob_a+=.5*(ea if a else 1-ea)*(py if y else 1-py)
        assert abs(prob_a-prob_b)<1e-12
        observational.append({'a':a,'y':y,'world_a':prob_a,'world_b':prob_b})
    grid=np.linspace(0,1,101)
    immediate=(1-grid)[:,None]*reward[0]+grid[:,None]*reward[1]
    return {'initial_state':p0.tolist(),'emission':B.tolist(),'transition':P.tolist(),'reward':reward.tolist(),'actions':actions,'observations':obs,'likelihood_forward':forward,'likelihood_enumerated':enumerated,'beliefs':beliefs,'equal_observed_laws':observational,'ate_world_a':0.,'ate_world_b':.36,'myopic_action_threshold':2/11,'grid':grid.tolist(),'immediate_values':immediate.tolist()}


def hmm_recovery(rng):
    # Distinct known emissions and known randomized actions: recover 4 transition
    # probabilities only. This excludes unknown-emission causal identification.
    p0=np.array([.7,.3]);B=np.array([[.8,.2],[.2,.8]])
    true=np.array([.1,.75,.05,.45]);n=700;T=14
    A=rng.binomial(1,.5,(n,T));O=np.empty((n,T+1),int)
    states=rng.binomial(1,.3,n);O[:,0]=rng.binomial(1,B[states,1])
    for t in range(T):
        states=rng.binomial(1,true[2*A[:,t]+states]);O[:,t+1]=rng.binomial(1,B[states,1])
    def objective(q):
        probs=1/(1+np.exp(-q));alpha=np.broadcast_to(p0,(n,2)).copy()*B[:,O[:,0]].T
        c=alpha.sum(1);val=np.log(c).sum();alpha/=c[:,None]
        for t in range(T):
            z0=probs[2*A[:,t]];z1=probs[2*A[:,t]+1]
            pred1=alpha[:,0]*z0+alpha[:,1]*z1
            alpha=np.column_stack([1-pred1,pred1])*B[:,O[:,t+1]].T
            c=alpha.sum(1);val+=np.log(c).sum();alpha/=c[:,None]
        return -val
    fits=[minimize(objective,np.log(q/(1-q)),method='L-BFGS-B') for q in [np.array([.2,.6,.2,.6]),np.array([.4,.8,.1,.4]),np.repeat(.5,4)]]
    best=min(fits,key=lambda f:f.fun);est=1/(1+np.exp(-best.x))
    assert best.success and np.max(abs(est-true))<.10
    return {'n_trajectories':n,'horizon':T,'true_transition_probabilities':true.tolist(),'fitted_transition_probabilities':est.tolist(),'max_abs_error':float(np.max(abs(est-true))),'negative_log_likelihood':float(best.fun),'starts':[{'success':bool(f.success),'objective':float(f.fun)} for f in fits],'fixed_emissions':B.tolist(),'behavior':'independent randomized Bernoulli(0.5)','qualification':'Known emissions, fixed initial law, 2 states, short horizon; one seed, no coverage claim.'}


def economics():
    years=3;rate=.10
    # USD millions, illustrative annual incremental contribution BEFORE platform costs.
    scenarios={'low':{'annual_benefit':2.,'build':4.,'annual_operating':1.8},'base':{'annual_benefit':5.,'build':4.,'annual_operating':1.8},'high':{'annual_benefit':9.,'build':4.,'annual_operating':1.8}}
    factor=sum((1+rate)**(-t) for t in range(1,years+1))
    for s in scenarios.values():s['npv']=-s['build']+(s['annual_benefit']-s['annual_operating'])*factor
    delayed=-4-1.8*factor+5*sum((1+rate)**(-t) for t in [2,3])
    return {'unit':'USD million','horizon_years':years,'discount_rate':rate,'annuity_factor':factor,'scenarios':scenarios,'base_with_no_first_year_benefit':delayed,'break_even_annual_benefit':4/factor+1.8,'first_phase_budget':{'person_months':36,'loaded_cost_per_person_month_usd':25000,'compute_usd':50000,'contingency_fraction':.20,'total_usd':(36*25000+50000)*1.2},'assumption_status':'Illustrative sponsor planning inputs, not bank forecasts, vendor quotes, or measured savings.'}


def figures(out):
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.bbox':'tight'})
    fig,axes=plt.subplots(1,2,figsize=(10,3.3))
    s=out['static'];axes[0].bar(['Observed\ndifference','AIPW','True effect'],[s['sample_naive_difference'],s['aipw'],8],color=['#c56a41','#23778a','#1a405f']);axes[0].set_ylabel('Incremental contribution (currency units)');axes[0].set_title('Who received the offer matters')
    z=out['longitudinal'];axes[1].bar(['Adherers','Conditional\nregression','g-formula\nand IPW'],[z['naive_contrast'],7,9],color=['#c56a41','#919eab','#23778a']);axes[1].axhline(9,color='#1a405f',linestyle='--');axes[1].set_title('Past actions change future confounders');axes[1].set_ylabel('Always versus never act')
    fig.tight_layout();fig.savefig(ROOT/'docs/figures/effect_bias.pdf');plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(10,3.3));d=out['staggered']
    for i,label in enumerate(['Early adoption','Late adoption','Never treated']):axes[0].plot(range(1,5),d['outcomes'][i],marker='o',label=label)
    axes[0].legend(fontsize=8);axes[0].set_xlabel('Calendar period');axes[0].set_ylabel('Synthetic outcome');axes[0].set_title('Identical untreated trends; changing effects')
    axes[1].bar(['TWFE','Treated-cell ATT','Clean DiD'],[d['twfe'],d['att'],d['clean_group_time_average']],color=['#c56a41','#1a405f','#23778a']);axes[1].set_ylabel('Estimated effect');axes[1].set_title('The estimator can change the target')
    fig.tight_layout();fig.savefig(ROOT/'docs/figures/panel_bias.pdf');plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(10,3.3));p=out['pomdp']
    axes[0].plot(range(4),np.array(p['beliefs'])[:,1],marker='o',color='#23778a');axes[0].set_ylim(0,1);axes[0].set_xlabel('Observed signal index');axes[0].set_ylabel('Posterior probability of fragile state');axes[0].set_title('Beliefs update with signals and actions')
    for a,l in enumerate(['No assistance','Assistance']):axes[1].plot(p['grid'],np.array(p['immediate_values'])[:,a],label=l)
    axes[1].axvline(p['myopic_action_threshold'],color='grey',linestyle='--');axes[1].legend();axes[1].set_xlabel('Probability of fragile state');axes[1].set_ylabel('Immediate expected contribution');axes[1].set_title('An explicit value trade-off')
    fig.tight_layout();fig.savefig(ROOT/'docs/figures/belief_value.pdf');plt.close(fig)
    fig,ax=plt.subplots(figsize=(7,3.2));e=out['economics'];names=list(e['scenarios']);vals=[e['scenarios'][k]['npv'] for k in names];ax.bar(names,vals,color=['#c56a41','#23778a','#1a405f']);ax.axhline(0,color='grey');ax.set_ylabel('Three-year NPV (USD million)');ax.set_title('Illustrative economics, before bank validation');fig.tight_layout();fig.savefig(ROOT/'docs/figures/economics.pdf');plt.close(fig)


def main():
    start=time.perf_counter();seed=20261007;rng=np.random.default_rng(seed)
    out={'seed':seed,'evidence_class':'synthetic illustration','static':static_aipw(rng),'longitudinal':longitudinal(),'staggered':staggered(),'pomdp':pomdp(rng),'hmm_recovery':hmm_recovery(rng),'economics':economics()}
    out['environment']={'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'matplotlib':matplotlib.__version__,'platform':platform.platform()}
    out['elapsed_seconds']=time.perf_counter()-start
    (ROOT/'docs/examples/results.json').write_text(json.dumps(out,indent=2)+'\n')
    figures(out)
    numbers={'StaticATE':out['static']['aipw'],'StaticSE':out['static']['iid_se'],'StaticNaive':out['static']['sample_naive_difference'],'LongNaive':out['longitudinal']['naive_contrast'],'TWFE':out['staggered']['twfe'],'PanelATT':out['staggered']['att'],'FilterLikelihood':out['pomdp']['likelihood_forward'],'HMMError':out['hmm_recovery']['max_abs_error'],'BreakEven':out['economics']['break_even_annual_benefit'],'BaseNPV':out['economics']['scenarios']['base']['npv'],'LowNPV':out['economics']['scenarios']['low']['npv'],'HighNPV':out['economics']['scenarios']['high']['npv']}
    (ROOT/'docs/examples/numbers.tex').write_text('\n'.join('\\newcommand{\\Num'+k+'}{'+f'{v:.3f}'+'}' for k,v in numbers.items())+'\n')
    print(json.dumps({'checks':'pass','seed':seed,'elapsed_seconds':out['elapsed_seconds'],'key_results':numbers,'hmm':out['hmm_recovery']},indent=2))


if __name__=='__main__':
    main()

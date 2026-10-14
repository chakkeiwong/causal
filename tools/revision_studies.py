#!/usr/bin/env python3
"""Synthetic banking studies. No network, bank data, or external package execution."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import platform
import time
import numpy as np
import scipy
from scipy.stats import norm, t as student_t
os.environ.setdefault('MPLCONFIGDIR', '/tmp/causal-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/derivations'
SEED = 20261007


def dump(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def tex_table(name, headers, rows, caption=None):
    lines = [r'\begin{tabular}{@{}' + 'l' + 'r' * (len(headers)-1) + '@{}}', r'\toprule', ' & '.join(headers)+r'\\', r'\midrule']
    lines += [' & '.join(str(x) for x in row)+r'\\' for row in rows]
    lines += [r'\bottomrule', r'\end{tabular}']
    (OUT / (name+'.tex')).write_text('\n'.join(lines)+'\n')


def deposit():
    rng = np.random.default_rng(SEED+10)
    n, nt = 96, 30
    group = np.repeat([12,18,24,999],24)
    times = np.arange(nt)
    macro = .07*times + .4*np.sin(times/3)
    levels = rng.normal(0,3,n)
    eps = rng.normal(0,.28,(n,nt))
    for k in range(1,nt): eps[:,k] += .65*eps[:,k-1]
    base = 30 + levels[:,None] + macro[None,:] + eps
    active = times[None,:] >= group[:,None]
    event = np.maximum(0,times[None,:]-group[:,None])
    effects = active * ((.85 + .025*(group[:,None]-12))*(1+.14*event))
    balances = base+effects
    fee = 1800
    contribution = balances*1e6*.025/12-active*(balances*1e6*.0025/12+fee)
    contribution0 = base*1e6*.025/12
    # Equal weights on all treated branch-months; cohort size is fixed.
    cells=[(g,k) for g in [12,18,24] for k in range(g,nt)]
    def att(y, indices):
        gg=group[indices]; yy=y[indices]
        return float(np.mean([(yy[gg==g,k]-yy[gg==g,g-1]).mean()-(yy[gg==999,k]-yy[gg==999,g-1]).mean() for g,k in cells]))
    def twfe(y):
        x=active.astype(float)
        rx=x-x.mean(0)-x.mean(1)[:,None]+x.mean()
        ry=y-y.mean(0)-y.mean(1)[:,None]+y.mean()
        return float((rx*ry).sum()/(rx*rx).sum())
    boot=[]
    for _ in range(499):
        idx=np.concatenate([rng.choice(np.flatnonzero(group==g),24) for g in [12,18,24,999]])
        boot.append([att(balances,idx),att(contribution,idx)])
    ci=np.quantile(boot,[.025,.975],axis=0)
    idx=np.arange(n)
    result={'design':{'branches':n,'months':nt,'cohorts':[12,18,24],'never_treated':24,'bootstrap':499,'units':'balances USD million; contribution USD per branch-month'},'balance':{'true_finite_population':float(effects[active].mean()),'group_time':att(balances,idx),'twfe':twfe(balances),'ci':ci[:,0].tolist()},'contribution':{'true_finite_population':float((contribution-contribution0)[active].mean()),'group_time':att(contribution,idx),'twfe':twfe(contribution),'ci':ci[:,1].tolist()},'repricing_annual_rate':.0025,'funding_margin_annual':.025,'monthly_program_cost':fee}
    tex_table('deposit_results',['Outcome','True effect','Cohort ATT',r'95\% interval','TWFE'],[[label,f'{r["true_finite_population"]:.3f}',f'{r["group_time"]:.3f}',f'[{r["ci"][0]:.3f}, {r["ci"][1]:.3f}]',f'{r["twfe"]:.3f}'] for label,r in [('Balances (USD m)',result['balance']),('Contribution (USD)',result['contribution'])]])
    fig,axs=plt.subplots(1,2,figsize=(10,3.5))
    for g in [12,18,24]:
        es=np.arange(nt-g)
        vals=[(balances[group==g,k]-balances[group==g,g-1]).mean()-(balances[group==999,k]-balances[group==999,g-1]).mean() for k in range(g,nt)]
        axs[0].plot(es,vals,marker='.',label=f'Adoption month {g}')
    axs[0].set(xlabel='Months since adoption',ylabel='Deposit effect, USD million'); axs[0].legend(fontsize=8)
    axs[1].errorbar([0],result['contribution']['group_time'],yerr=np.array([[result['contribution']['group_time']-ci[0,1]],[ci[1,1]-result['contribution']['group_time']]]),fmt='o',capsize=5)
    axs[1].axhline(0,color='black',lw=.8); axs[1].set(xticks=[0],xticklabels=['Monthly funding contribution'],ylabel='Incremental USD per branch')
    fig.tight_layout(); fig.savefig(OUT/'deposit_study.pdf'); plt.close(fig)
    return result


P_COLL=np.array([[[.88,.10,.02],[.30,.50,.20],[.08,.22,.70]],[[.88,.10,.02],[.50,.40,.10],[.18,.42,.40]]])
INIT_COLL=np.array([.6,.3,.1])
E_COLL=np.array([0,.35,.60])
REWARD_COLL=np.array([20,-10,-160])
TERMINAL_COLL=np.array([0,0,-100])
GAMMA=.99


def categorical(rng, p):
    return (rng.random(p.shape[:-1])[...,None]>np.cumsum(p,axis=-1)).sum(-1).clip(max=p.shape[-1]-1)


def coll_sim(rng,n,h=8):
    s=np.zeros((n,h+1),dtype=int); a=np.zeros((n,h),dtype=int)
    s[:,0]=rng.choice(3,n,p=INIT_COLL)
    for t in range(h):
        a[:,t]=(rng.random(n)<E_COLL[s[:,t]])
        s[:,t+1]=categorical(rng,P_COLL[a[:,t],s[:,t]])
    r=REWARD_COLL[s[:,1:]]-12*a
    return s,a,r


def coll_fit(s,a):
    p=np.zeros((2,3,3))
    for action in range(2):
        for state in range(3):
            mask=(a==action)&(s[:,:-1]==state)
            count=np.bincount(s[:,1:][mask],minlength=3)+.5
            p[action,state]=count/count.sum()
    # Action one is unavailable in state zero and is never evaluated there.
    p[1,0]=p[0,0]
    return p


def coll_q(p,policy,h=8):
    q=np.zeros((h,3,2)); v=np.zeros((h+1,3)); v[-1]=TERMINAL_COLL
    for t in range(h-1,-1,-1):
        for a in range(2): q[t,:,a]=p[a]@(REWARD_COLL+GAMMA*v[t+1])-12*a
        v[t]=(1-policy)*q[t,:,0]+policy*q[t,:,1]
    return q,v


def coll_scores(s,a,r,p,policy,wrong_q=False,wrong_e=False):
    n,h=a.shape; q,v=coll_q(p,policy,h)
    if wrong_q:
        q=np.zeros_like(q); v=np.zeros_like(v); v[-1]=TERMINAL_COLL
    e=E_COLL.copy()
    if wrong_e: e[1:]=.5
    w=np.ones(n); dr=v[0,s[:,0]].copy(); ips=np.zeros(n); current=np.zeros(n)
    for t in range(h):
        ss=s[:,t]; aa=a[:,t]
        num=np.where(aa,policy[ss],1-policy[ss]); den=np.where(aa,e[ss],1-e[ss])
        ratio=num/den; w*=ratio
        residual=r[:,t]+GAMMA*v[t+1,s[:,t+1]]-q[t,ss,aa]
        dr+=GAMMA**t*w*residual
        ips+=GAMMA**t*w*r[:,t]
        current+=GAMMA**t*ratio*r[:,t]
    ips+=GAMMA**h*w*TERMINAL_COLL[s[:,-1]]
    current+=GAMMA**h*ratio*TERMINAL_COLL[s[:,-1]]
    ess=float(w.sum()**2/(w@w)) if w@w else 0.
    return {'dr':dr,'ips':ips,'direct':v[0,s[:,0]],'current_only':current},ess


def collections():
    rng=np.random.default_rng(SEED+20)
    train=coll_sim(rng,3000); test=coll_sim(rng,8000)
    phat=coll_fit(train[0],train[1]); policies={'No extra assistance':np.array([0.,0.,0.]),'Severe state only':np.array([0.,0.,1.]),'All eligible':np.array([0.,1.,1.])}
    scores={}; results={}
    for name,policy in policies.items():
        q,v=coll_q(P_COLL,policy)
        sc,ess=coll_scores(*test,phat,policy); scores[name]=sc
        results[name]={'truth':float(INIT_COLL@v[0]),'final_weight_ess':ess,**{method:float(x.mean()) for method,x in sc.items()}}
    base=scores['No extra assistance']['dr']; contrasts={}
    z=norm.ppf(1-.05/4)
    for name in ['Severe state only','All eligible']:
        d=scores[name]['dr']-base; se=d.std(ddof=1)/len(d)**.5
        contrasts[name]={'estimate':float(d.mean()),'se':float(se),'simultaneous_ci':[(d.mean()-z*se).item(),(d.mean()+z*se).item()],'truth':results[name]['truth']-results['No extra assistance']['truth']}
    mc=[]
    for k in range(160):
        tr=coll_sim(rng,600); ev=coll_sim(rng,2000); pp=coll_fit(tr[0],tr[1]); policy=policies['All eligible']; truth=results['All eligible']['truth']
        for method,wq,we in [('DR',False,False),('Wrong Q; true logging',True,False),('True Q; wrong logging',False,True),('Both wrong',True,True)]:
            model=P_COLL if method=='True Q; wrong logging' else pp
            sc,_=coll_scores(*ev,model,policy,wrong_q=wq,wrong_e=we)
            vals=sc['dr']; se=vals.std(ddof=1)/len(vals)**.5
            mc.append((method,vals.mean()-truth,se,abs(vals.mean()-truth)<=1.96*se))
    repeated={}
    for method in dict.fromkeys(x[0] for x in mc):
        x=np.array([z[1:] for z in mc if z[0]==method],float)
        repeated[method]={'bias':float(x[:,0].mean()),'rmse':float(np.mean(x[:,0]**2)**.5),'coverage':float(x[:,2].mean()),'replications':len(x),'coverage_mc_se':float((x[:,2].mean()*(1-x[:,2].mean())/len(x))**.5)}
    tex_table('collections_values',['Policy','True USD','Direct','IPS','DR','Final ESS'],[[name,f'{r["truth"]:.2f}',f'{r["direct"]:.2f}',f'{r["ips"]:.2f}',f'{r["dr"]:.2f}',f'{r["final_weight_ess"]:.0f}'] for name,r in results.items()])
    tex_table('collections_robustness',['Specification','Bias (USD)','RMSE',r'95\% coverage'],[[name,f'{r["bias"]:.2f}',f'{r["rmse"]:.2f}',f'{r["coverage"]:.3f}'] for name,r in repeated.items()])
    tex_table('collections_contrasts',['Policy versus no extra','True USD','DR difference','Simultaneous interval'],[[name,f'{r["truth"]:.2f}',f'{r["estimate"]:.2f}',f'[{r["simultaneous_ci"][0]:.2f}, {r["simultaneous_ci"][1]:.2f}]'] for name,r in contrasts.items()])
    return {'design':{'train':3000,'evaluation':8000,'horizon':8,'discount':GAMMA,'replications':160,'monte_carlo_train':600,'monte_carlo_evaluation':2000,'inference':'conditional on training fits; iid complete customer trajectories'},'policies':results,'contrasts':contrasts,'repeated':repeated,'fitted_transitions':phat.tolist()}


TRUE_HMM={'mu':np.array([.72,.28]),'p':np.array([[[.93,.07],[.22,.78]],[[.94,.06],[.52,.48]]]),'b':np.array([[.78,.18,.04],[.16,.34,.50]]),'q':np.array([.15,.80])}


def hmm_sim(rng,n=600,h=12,hidden=False):
    s=np.zeros((n,h+1),int); o=np.zeros_like(s); a=np.zeros((n,h),int)
    s[:,0]=rng.choice(2,n,p=TRUE_HMM['mu']); o[:,0]=categorical(rng,TRUE_HMM['b'][s[:,0]])
    for t in range(h):
        probs=TRUE_HMM['q'][s[:,t]] if hidden else np.full(n,.4)
        a[:,t]=(rng.random(n)<probs)
        s[:,t+1]=categorical(rng,TRUE_HMM['p'][a[:,t],s[:,t]])
        o[:,t+1]=categorical(rng,TRUE_HMM['b'][s[:,t+1]])
    # Estimation receives o and a; s is retained only by this generator scope.
    return o,a


def hmm_fb(o,a,theta,joint=False,counts=True):
    n,h=a.shape; mu,p,b,q=(theta[k] for k in ['mu','p','b','q'])
    alpha=np.empty((h+1,n,2)); scale=np.ones((h+1,n))
    un=mu*b[:,o[:,0]].T; scale[0]=un.sum(1); alpha[0]=un/scale[0,:,None]
    for t in range(h):
        qa=np.where(a[:,t,None],q,1-q) if joint else np.ones((n,2))
        un=np.einsum('ni,nij->nj',alpha[t]*qa,p[a[:,t]])*b[:,o[:,t+1]].T
        scale[t+1]=un.sum(1); alpha[t+1]=un/scale[t+1,:,None]
    ll=float(np.log(scale).sum())
    if not counts: return ll
    gamma=np.empty_like(alpha); gamma[-1]=alpha[-1]; beta=np.ones((n,2)); pc=np.zeros_like(p); qc=np.zeros((2,2))
    for t in range(h-1,-1,-1):
        qa=np.where(a[:,t,None],q,1-q) if joint else np.ones((n,2))
        end=b[:,o[:,t+1]].T*beta
        xi=alpha[t,:, :,None]*qa[:,:,None]*p[a[:,t]]*end[:,None,:]/scale[t+1,:,None,None]
        gamma[t]=xi.sum(2)
        for action in range(2):
            mask=a[:,t]==action
            pc[action]+=xi[mask].sum(0); qc[:,action]+=gamma[t,mask].sum(0)
        beta=qa*np.einsum('nij,nj->ni',p[a[:,t]],end)/scale[t+1,:,None]
    bc=np.array([gamma[(o.T==z)].sum(0) for z in range(3)]).T
    return ll, gamma[0].sum(0), pc, bc, qc


def hmm_fit(o,a,seed,joint=False,starts=3,maxiter=160):
    rng=np.random.default_rng(seed); fits=[]
    for start in range(starts):
        b=np.array([[.65,.25,.1],[.20,.30,.50]])+rng.uniform(-.07,.07,(2,3)); b=np.maximum(b,.01); b/=b.sum(1)[:,None]
        p=np.array([[[.82,.18],[.32,.68]],[[.9,.1],[.58,.42]]])+rng.uniform(-.07,.07,(2,2,2)); p=np.maximum(p,.01); p/=p.sum(2)[:,:,None]
        th={'mu':np.array([.6,.4]),'p':p,'b':b,'q':np.array([.25,.65])}; history=[]; converged=False
        for iteration in range(maxiter):
            ll,mc,pc,bc,qc=hmm_fb(o,a,th,joint)
            history.append(ll)
            if len(history)>1 and ll-history[-2]<1e-7*o.shape[0]:
                converged=True; break
            mc+=1e-6; pc+=1e-6; bc+=1e-6; qc+=1e-6
            th={'mu':mc/mc.sum(),'p':pc/pc.sum(2)[:,:,None],'b':bc/bc.sum(1)[:,None],'q':qc[:,1]/qc.sum(1) if joint else th['q']}
        ll=hmm_fb(o,a,th,joint,False)
        order=np.argsort(th['b']@np.arange(3))
        th={'mu':th['mu'][order],'p':th['p'][:,order][:,:,order],'b':th['b'][order],'q':th['q'][order]}
        fits.append((ll,th,len(history),float(np.min(np.diff(history+[ll]))) if history else 0.,converged))
    best=max(fits,key=lambda z:z[0])
    return best[1], {'log_likelihood':best[0],'iterations':best[2],'start_objectives':[f[0] for f in fits],'min_likelihood_increment':min(f[3] for f in fits),'converged':best[4],'iteration_cap':maxiter,'start_diagnostics':[{'iterations':f[2],'converged':f[4],'min_increment':f[3]} for f in fits]}


def hmm_reactive_value(theta,policy,h=8):
    mu,p,b=(theta[k] for k in ['mu','p','b']); reward=np.array([18.,0.,-90.]); v=np.zeros((2,3))
    for _ in range(h):
        new=np.zeros_like(v)
        for o in range(3):
            aa=int(policy[o]); nex=b*(reward[None,:]+GAMMA*v)
            new[:,o]=p[aa]@nex.sum(1)-8*aa
        v=new
    return float(np.sum(mu[:,None]*b*v))


def belief_plan(theta,h=8,grid_size=501):
    grid=np.linspace(0,1,grid_size); bel=np.stack([1-grid,grid],axis=1); v=np.zeros(grid_size); policy=[]
    for _ in range(h):
        qv=[]
        for a in [0,1]:
            pred=bel@theta['p'][a]; obs=pred@theta['b']; cont=np.zeros(grid_size)
            for o in range(3):
                nb=pred[:,1]*theta['b'][1,o]/obs[:,o]
                cont+=obs[:,o]*(np.array([18.,0.,-90.])[o]+GAMMA*np.interp(nb,grid,v))
            qv.append(cont-8*a)
        qv=np.array(qv); policy.append(qv.argmax(0).tolist()); v=qv.max(0)
    prob=theta['mu']@theta['b']; post=theta['mu'][1]*theta['b'][1]/prob
    value=float(np.sum(prob*np.interp(post,grid,v)))
    return value, grid, v, policy[-1]


def hidden_states():
    rng=np.random.default_rng(SEED+30); results={}
    true_delta=hmm_reactive_value(TRUE_HMM,[0,0,1])-hmm_reactive_value(TRUE_HMM,[0,0,0])
    main_data={}
    for name,hidden,joint in [('Randomized',False,False),('Hidden logging, omitted action law',True,False),('Hidden logging, joint action law',True,True)]:
        key='hidden' if hidden else 'random'
        if key not in main_data: main_data[key]=hmm_sim(rng,800,12,hidden)
        th,diag=hmm_fit(*main_data[key],SEED+33,joint,starts=4)
        results[name]={'parameters':{k:v.tolist() for k,v in th.items() if joint or k!='q'},'fit':diag,'max_transition_error':float(np.max(np.abs(th['p']-TRUE_HMM['p']))),'max_emission_error':float(np.max(np.abs(th['b']-TRUE_HMM['b']))),'policy_gain':hmm_reactive_value(th,[0,0,1])-hmm_reactive_value(th,[0,0,0])}
    # Trajectory bootstrap includes all fitted environment parameters and fixes the policy.
    oo,aa=main_data['random']; bs=[]; bootstrap_diagnostics=[]
    for k in range(79):
        idx=rng.integers(0,len(oo),len(oo)); th,fit_diag=hmm_fit(oo[idx],aa[idx],SEED+100+k,False,starts=2,maxiter=120)
        bs.append(hmm_reactive_value(th,[0,0,1])-hmm_reactive_value(th,[0,0,0])); bootstrap_diagnostics.append(fit_diag)
    bootstrap_ci=np.quantile(bs,[.025,.975]).tolist()
    reps=[]
    for k in range(30):
        oo,aa=hmm_sim(rng,500,12,True)
        for joint in [False,True]:
            th,diag=hmm_fit(oo,aa,SEED+300+k,joint,starts=2,maxiter=120)
            delta=hmm_reactive_value(th,[0,0,1])-hmm_reactive_value(th,[0,0,0])
            reps.append({'joint':joint,'fit':diag,'gain_error':delta-true_delta,'transition_rmse':float(np.mean((th['p']-TRUE_HMM['p'])**2)**.5),'emission_rmse':float(np.mean((th['b']-TRUE_HMM['b'])**2)**.5)})
    repeated={}
    for joint in [False,True]:
        rr=[x for x in reps if x['joint']==joint]; err=np.array([x['gain_error'] for x in rr])
        repeated['Joint' if joint else 'Omitted']={'replications':len(rr),'selected_fits_at_cap':sum(not x['fit']['converged'] for x in rr),'gain_bias':float(err.mean()),'gain_rmse':float(np.mean(err**2)**.5),'mean_transition_rmse':float(np.mean([x['transition_rmse'] for x in rr])),'mean_emission_rmse':float(np.mean([x['emission_rmse'] for x in rr])),'gain_bias_mc_se':float(err.std(ddof=1)/len(err)**.5)}
    plan,grid,v,policy=belief_plan(TRUE_HMM); fine,*_=belief_plan(TRUE_HMM,grid_size=1001)
    fig,ax=plt.subplots(figsize=(7.5,3.5)); ax.plot(grid,v,label='Eight-decision optimized value'); ax.set(xlabel='Probability of fragile state after the signal',ylabel='Model value, USD'); ax2=ax.twinx(); ax2.step(grid,policy,color='#b4523b',alpha=.5,where='mid'); ax2.set(ylabel='Initial action',yticks=[0,1]); fig.tight_layout(); fig.savefig(OUT/'pomdp_value.pdf'); plt.close(fig)
    tex_table('hmm_estimation',['Estimation design','Max $P$ error','Max $B$ error','Policy gain (USD)'],[[name,f'{r["max_transition_error"]:.3f}',f'{r["max_emission_error"]:.3f}',f'{r["policy_gain"]:.2f}'] for name,r in results.items()])
    tex_table('hmm_repetitions',['Action model','Gain bias (USD)','Gain RMSE','Transition RMSE'],[[name,f'{r["gain_bias"]:.2f}',f'{r["gain_rmse"]:.2f}',f'{r["mean_transition_rmse"]:.3f}'] for name,r in repeated.items()])
    return {'truth':{k:v.tolist() for k,v in TRUE_HMM.items()},'design':{'trajectories':800,'horizon':12,'states':2,'observation_categories':3,'starts':4,'bootstrap':79,'repetitions':30,'repetition_trajectories':500,'policy_evaluation_horizon':8},'fits':results,'true_policy_gain':true_delta,'randomized_bootstrap_ci':bootstrap_ci,'bootstrap_gains':bs,'bootstrap_diagnostics':bootstrap_diagnostics,'repeated':repeated,'belief_planning':{'grid501_value':plan,'grid1001_value':fine,'no_assistance_value':hmm_reactive_value(TRUE_HMM,[0,0,0]),'reactive_value':hmm_reactive_value(TRUE_HMM,[0,0,1]),'grid_difference':abs(plan-fine)},'repetition_details':reps}


def credit_supply():
    rng=np.random.default_rng(SEED+40); banks=24; firms=600
    shock=rng.normal(size=banks); banknoise=rng.normal(0,.45,banks); u=rng.normal(size=firms)
    f=[]; b=[]
    for i in range(firms):
        pr=np.exp(.65*u[i]*shock); pr/=pr.sum(); chosen=rng.choice(banks,3,replace=False,p=pr)
        f.extend([i]*3); b.extend(chosen.tolist())
    f=np.array(f); b=np.array(b); x=shock[b]; y=2-3*x+4*u[f]+banknoise[b]+rng.normal(0,1.5,len(b))
    pooled=np.linalg.lstsq(np.c_[np.ones(len(y)),x],y,rcond=None)[0][1]
    xr=x-x.reshape(firms,3).mean(1).repeat(3); yr=y-y.reshape(firms,3).mean(1).repeat(3)
    beta=(xr@yr)/(xr@xr); residual=yr-beta*xr
    g=np.bincount(b,weights=xr*residual,minlength=banks); se=(banks/(banks-1)*np.sum(g*g)/(xr@xr)**2)**.5; crit=student_t.ppf(.975,banks-1)
    result={'firms':firms,'banks':banks,'relationships':len(y),'true_supply_coefficient':-3.,'pooled':float(pooled),'borrower_fixed_effect':float(beta),'bank_cluster_se':float(se),'ci':[float(beta-crit*se),float(beta+crit*se)],'units':'percentage points loan growth per unit funding shock; synthetic exogenous shock'}
    tex_table('credit_supply',['Method','Coefficient',r'95\% interval'],[['Generating effect','-3.000','--'],['Pooled',f'{pooled:.3f}','--'],['Borrower effects',f'{beta:.3f}',f'[{beta-crit*se:.3f}, {beta+crit*se:.3f}]']])
    return result


def dependence():
    rng=np.random.default_rng(SEED+50); ns,nt,reps=96,36,1200; coverage={k:[] for k in ['Rows independent','Entity clusters','Entity and date clusters']}; ses={k:[] for k in coverage}
    negative_crossed_variances=0
    for _ in range(reps):
        z=rng.normal(0,1,(ns,1))+rng.normal(0,1,(1,nt))+rng.normal(0,1,(ns,nt)); mean=z.mean(); res=z-mean
        row=res.var(ddof=1)/(ns*nt); ent=ns/(ns-1)*np.sum(res.sum(1)**2)/(ns*nt)**2; date=nt/(nt-1)*np.sum(res.sum(0)**2)/(ns*nt)**2; cross=max(0.,ent+date-row)
        negative_crossed_variances+=int(ent+date-row<0)
        for name,var in zip(coverage,[row,ent,cross]):
            se=var**.5; ses[name].append(se); coverage[name].append(abs(mean)<1.96*se)
    true_se=(1/ns+1/nt+1/(ns*nt))**.5
    table={name:{'coverage':float(np.mean(v)),'mean_se':float(np.mean(ses[name])),'coverage_mc_se':float((np.mean(v)*(1-np.mean(v))/reps)**.5)} for name,v in coverage.items()}
    # Same reduced-form VAR and covariance, two structural timing restrictions.
    A=np.array([[.7,0],[.15,.6]]); sigma=np.array([[1,.8],[.8,1.]])
    c1=np.linalg.cholesky(sigma); rev=np.array([[0,1],[1,0]]); c2=rev@np.linalg.cholesky(rev@sigma@rev)@rev
    assert np.allclose(c1@c1.T,c2@c2.T)
    impulse1=np.array([np.linalg.matrix_power(A,h)@(c1[:,0]/c1[0,0]) for h in range(13)])
    impulse2=np.array([np.linalg.matrix_power(A,h)@(c2[:,0]/c2[0,0]) for h in range(13)])
    fig,axs=plt.subplots(1,2,figsize=(10,3.5)); axs[0].bar(np.arange(3),[v['coverage'] for v in table.values()],color=['#b4523b','#d59954','#23778a']); axs[0].axhline(.95,color='black',ls='--',lw=.8); axs[0].set(xticks=np.arange(3),xticklabels=['Rows','Entity','Entity + date'],ylabel='Coverage of nominal 95% interval',ylim=(0,1)); axs[1].plot(impulse1[:,1],label='Funding ordered first'); axs[1].plot(impulse2[:,1],label='Funding ordered second'); axs[1].set(xlabel='Months after unit funding shock',ylabel='Loan response'); axs[1].legend(fontsize=8); fig.tight_layout(); fig.savefig(OUT/'dependence_and_irf.pdf'); plt.close(fig)
    tex_table('dependence_coverage',['Variance method','Mean SE',r'95\% coverage'],[[k,f'{v["mean_se"]:.3f}',f'{v["coverage"]:.3f}'] for k,v in table.items()])
    return {'design':{'entities':ns,'dates':nt,'repetitions':reps,'entity_sd':1,'date_sd':1,'idiosyncratic_sd':1},'true_se':true_se,'inference':table,'negative_crossed_variances':negative_crossed_variances,'negative_variance_rule':'This simulation truncates to zero and records the count; the reusable reducer instead flags indefinite covariance.','structural_VAR':{'A':A.tolist(),'innovation_covariance':sigma.tolist(),'funding_first_impact':c1[:,0].tolist(),'funding_second_normalized_impact':(c2[:,0]/c2[0,0]).tolist(),'loan_responses_first':impulse1[:,1].tolist(),'loan_responses_second':impulse2[:,1].tolist()}}


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--study',choices=['all','deposit','collections','hidden_states','credit_supply','dependence'],default='all'); args=ap.parse_args()
    OUT.mkdir(exist_ok=True)
    path=OUT/'results.json'; old=json.loads(path.read_text()) if path.exists() else {}
    jobs={'deposit':deposit,'collections':collections,'hidden_states':hidden_states,'credit_supply':credit_supply,'dependence':dependence}
    for name,fn in jobs.items():
        if args.study not in ['all',name]: continue
        start=time.perf_counter(); result=fn(); result['elapsed_seconds']=time.perf_counter()-start; old[name]=result; dump('results.json',old); print(name, json.dumps({k:v for k,v in result.items() if k in ['elapsed_seconds','true_policy_gain','repeated','contribution','true_se']}),flush=True)
    dump('environment.json',{'seed':SEED,'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'matplotlib':matplotlib.__version__,'platform':platform.platform(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Synthetic studies; no bank validation or third-party runtime qualification'})


if __name__=='__main__': main()

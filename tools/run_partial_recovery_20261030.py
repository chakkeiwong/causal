"""Bounded historical outcomes, selective recovery, known random invitations."""
from pathlib import Path
from fractions import Fraction as F
import argparse,csv,hashlib,json,math,time
import numpy as np
from scipy.stats import norm
R=Path(__file__).resolve().parents[1]
O=R/'docs/twelve-hour-closure/2026-10-29'
SEED=202610300517
Q=[.1,.25,.5,1.]
N=2000
REPS=500
ROUTINE=[[F(4,5),F(2,5)],[F(2,5),F(4,5)]]
SUCCESS={'standard':[[F(1,10),F(9,10)],[F(9,10),F(1,5)]],
 'intensive':[[F(4,5),F(49,50)],[F(49,50),F(4,5)]],
 'complete':[[F(1),F(1)],[F(1),F(1)]],
 'unstable':[[F(1),F(1)],[F(1),F(1)]]}
def save(p,d):p.write_text(json.dumps(d,indent=2,allow_nan=False)+'\n')
def population(regime):
    arms=[]
    for a,mu in enumerate([F(9,20),F(11,20)]):
        observed_y=observed=rec_y=rec=F(0)
        for y,py in [(0,1-mu),(1,mu)]:
            r=ROUTINE[a][y];s=SUCCESS[regime][a][y]
            reported=F(y)
            if regime=='unstable'and a==1 and y==0:reported=F(1,2)
            observed+=py*r;observed_y+=py*r*y
            rec+=py*(1-r)*s;rec_y+=py*(1-r)*s*reported
        missing=1-observed-rec
        low=observed_y+rec_y;up=low+missing
        arms.append(dict(mu=mu,observed=observed,observed_y=observed_y,
            recovered=rec,recovered_y=rec_y,unresolved=missing,lower=low,upper=up,
            completecase=observed_y/observed,
            naive=observed_y+(1-observed)*rec_y/rec))
    low=arms[1]['lower']-arms[0]['upper'];up=arms[1]['upper']-arms[0]['lower']
    assert up-low==sum(x['unresolved']for x in arms)
    return dict(arms=arms,lower=low,upper=up,width=up-low,truth=F(1,10),
                naive=arms[1]['naive']-arms[0]['naive'],
                completecase=arms[1]['completecase']-arms[0]['completecase'])
def floats(x):
    if isinstance(x,F):return float(x)
    if isinstance(x,dict):return{k:floats(v)for k,v in x.items()}
    if isinstance(x,list):return[floats(v)for v in x]
    return x
def generate(rng,regime,n):
    arms=[]
    for a,mu in enumerate([.45,.55]):
        y=(rng.random(n)<mu).astype(float)
        r=rng.random(n)<np.array([float(x)for x in ROUTINE[a]])[y.astype(int)]
        s=rng.random(n)<np.array([float(x)for x in SUCCESS[regime][a]])[y.astype(int)]
        u=rng.random(n);reported=y.copy()
        if regime=='unstable'and a==1:
            change=(y==0)&(~r)&(rng.random(n)<.5);reported[change]=1
        arms.append(dict(y=y,r=r,s=s,u=u,reported=reported))
    return arms
def observe(a,q):
    invited=(~a['r'])&(a['u']<q);rec=invited&a['s']
    view=np.full(len(invited),np.nan);view[a['r']]=a['y'][a['r']];view[rec]=a['reported'][rec]
    return dict(y=view,r=a['r'],invited=invited,recovered=rec)
def scores(v,q):
    y=v['y'];r=v['r'];rec=v['recovered']
    low=np.zeros(len(y));up=(~r).astype(float)
    low[r]=y[r];up[r]=y[r]
    low[rec]+=y[rec]/q;up[rec]-=(1-y[rec])/q
    assert np.isfinite(low).all()and np.isfinite(up).all()
    return low,up
def validate():
    exact={name:population(name)for name in SUCCESS}
    assert exact['standard']['lower']==F(-87,1000)
    assert exact['standard']['upper']==F(77,500)
    assert exact['intensive']['lower']==F(7,125)
    assert exact['intensive']['upper']==F(277,2500)
    assert exact['complete']['lower']==exact['complete']['upper']==F(1,10)
    assert exact['unstable']['lower']==exact['unstable']['upper']==F(47,200)
    # Nonresponding outcomes can be set at either endpoint without changing
    # any observed stratum probability or outcome. Cross-arm coupling is free.
    extremes=[]
    for name in ['standard','intensive','complete']:
        d=exact[name]
        for side in ['lower','upper']:
            vals=[]
            for a,ar in enumerate(d['arms']):
                fill=1 if (side=='lower'and a==0)or(side=='upper'and a==1)else 0
                vals.append(ar['observed_y']+ar['recovered_y']+fill*ar['unresolved'])
            assert vals[1]-vals[0]==d[side]
            extremes.append(dict(regime=name,endpoint=side,effect=float(vals[1]-vals[0])))
    # Scalar invitation enumeration matches population completed-recovery law.
    for q in [F(1,10),F(1,4),F(1,2),F(1)]:
        for y in [0,1]:
            for s in [0,1]:
                assert q*(s*y/q)+(1-q)*0==s*y
                assert q*(1-s*(1-y)/q)+(1-q)==s*y+1-s
    for regime in SUCCESS:
        data=generate(np.random.default_rng(SEED+11),regime,61)
        for q in Q:
            for a in data:
                v=observe(a,q);lo,hi=scores(v,q)
                poison={k:x.copy()for k,x in v.items()};poison['y'][~(v['r']|v['recovered'])]=1e200
                pl,pu=scores(poison,q);np.testing.assert_array_equal(lo,pl);np.testing.assert_array_equal(hi,pu)
                if regime=='complete'and q==1:np.testing.assert_array_equal(lo,a['y']);np.testing.assert_array_equal(hi,a['y'])
    return exact,dict(exact_endpoint_checks=True,attained_extremes=extremes,invitation_enumeration=True,mask_poison=True,complete_recovery=True)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--regime',choices=list(SUCCESS),required=True)
    ap.add_argument('--out',required=True);args=ap.parse_args()
    out=R/args.out;out.mkdir(parents=True,exist_ok=False)
    exact,checks=validate();pop=floats(exact[args.regime]);save(out/'population.json',pop);save(out/'validation.json',checks)
    save(out/'registration.json',dict(seed=SEED,regime=args.regime,n_per_arm=N,replications=REPS,invitation_rates=Q,
       runner_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
       definition='IIDarmobservations,randomizedbinarytreatment,knownBernoulliinvitations,arbitraryselectivecompletion',
       target='PopulationATEoforiginalhistoricalbinaryoutcome',
       interval='Hoeffdingoutwardbandcoversentireidentifiedinterval;normalendpointbandreportedseparately',
       native_package_execution=False))
    rows=[];start=time.monotonic();z=norm.ppf(.975);si=list(SUCCESS).index(args.regime)
    for rep in range(REPS):
        rng=np.random.default_rng(np.random.SeedSequence([SEED,si,rep]));arms=generate(rng,args.regime,N)
        if rep in [0,249,499]:np.savez_compressed(out/f'data-{rep}.npz',**{f'a{a}_{k}':v for a,x in enumerate(arms)for k,v in x.items()})
        for q in Q:
            vv=[observe(a,q)for a in arms];ss=[scores(v,q)for v in vv]
            low=float(ss[1][0].mean()-ss[0][1].mean());up=float(ss[1][1].mean()-ss[0][0].mean())
            sl=math.sqrt((ss[1][0].var(ddof=1)+ss[0][1].var(ddof=1))/N)
            su=math.sqrt((ss[1][1].var(ddof=1)+ss[0][0].var(ddof=1))/N)
            rad=math.sqrt(math.log(2/.05)/(N*q*q))
            hl,hu=max(-1.,low-rad),min(1.,up+rad)
            nl,nu=max(-1.,low-z*sl),min(1.,up+z*su)
            naive=[];cc=[]
            for v in vv:
                r=v['r'];b=v['recovered'];y=v['y'];assert b.sum()>0
                naive.append(float(np.mean(r)*np.mean(y[r])+(1-np.mean(r))*np.mean(y[b])))
                cc.append(float(np.mean(y[r])))
            rows.append(dict(rep=rep,q=q,lower=low,upper=up,se_lower=sl,se_upper=su,
                hoeffding_lower=hl,hoeffding_upper=hu,normal_lower=nl,normal_upper=nu,
                hoeffding_covers_truth=hl<=.1<=hu,normal_covers_truth=nl<=.1<=nu,
                hoeffding_covers_region=hl<=pop['lower']and hu>=pop['upper'],
                normal_covers_region=nl<=pop['lower']and nu>=pop['upper'],
                positive_hoeffding=hl>0,positive_normal=nl>0,negative_normal=nu<0,
                naive=naive[1]-naive[0],complete_case=cc[1]-cc[0],
                invitations=sum(int(v['invited'].sum())for v in vv),
                recoveries=sum(int(v['recovered'].sum())for v in vv),
                crossing_raw=low>up,hoeffding_radius=rad))
        if(rep+1)%100==0:print(json.dumps(dict(regime=args.regime,completed=rep+1,seconds=round(time.monotonic()-start,2))),flush=True)
    with(out/'replications.csv').open('w',newline='')as f:
        w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
    summaries=[]
    for q in Q:
        a=[r for r in rows if r['q']==q];summ=dict(q=q)
        for k in ['lower','upper','se_lower','se_upper','invitations','recoveries','naive','complete_case']:
            vals=np.array([r[k]for r in a]);summ['mean_'+k]=float(vals.mean());summ[k+'_mcse']=float(vals.std(ddof=1)/math.sqrt(REPS))
        for k in ['hoeffding_covers_truth','normal_covers_truth','hoeffding_covers_region','normal_covers_region','positive_hoeffding','positive_normal','negative_normal','crossing_raw']:
            p=float(np.mean([r[k]for r in a]));summ[k]=p;summ[k+'_mcse']=math.sqrt(p*(1-p)/REPS)
        for meth in ['hoeffding','normal']:
            summ[meth+'_mean_width']=float(np.mean([r[meth+'_upper']-r[meth+'_lower']for r in a]))
        summaries.append(summ)
    save(out/'result.json',dict(status='pass',regime=args.regime,population=pop,summaries=summaries,seconds=time.monotonic()-start,
       limits=['Generatedbinaryoutcomes,notbankdata','HTBernoulliendpointestimator,notnativeattritionratioestimator',
         'Noexactguaranteefornormalinterval','Unstablecaseviolateshistoricaloutcomeassumptionbydesign']))
    print(json.dumps(dict(status='pass',regime=args.regime,population=pop,rows=len(rows))))
if __name__=='__main__':main()

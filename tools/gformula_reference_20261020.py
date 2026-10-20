"""Exact authored longitudinal and failure-handling qualification examples."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

def calculate():
    def risk(a0,a1,l1):return F(1,20)+F(1,5)*l1+F(3,20)*a0+F(1,10)*a1+F(3,10)*l1*a1
    def value(policy):
        total=F(0);routes=[]
        for l0 in [0,1]:
            a0=policy[0](l0);p=F(1,5)+F(2,5)*l0+F(1,5)*a0
            for l1 in [0,1]:
                a1=policy[1](l0,l1);prob=F(1,2)*(p if l1 else 1-p)
                y=risk(a0,a1,l1);assert 0<=y<=1
                total+=prob*y;routes.append(dict(l0=l0,a0=a0,l1=l1,a1=a1,probability=str(prob),risk=str(y)))
        return total,routes
    never=value((lambda l:0,lambda l,x:0))
    always=value((lambda l:1,lambda l,x:1))
    dynamic=value((lambda l:1-l,lambda l,x:x))
    plug=F(0)
    for l0 in [0,1]:
        a0=1-l0;p=F(1,5)+F(2,5)*l0+F(1,5)*a0;a1=int(p>=F(1,2))
        plug+=F(1,2)*risk(a0,a1,p)
    hy,hd=F(1,5),F(1,10)
    retained=hy*(1-hd)+(1-hy)*(1-hd)*hy*(1-hd)
    eliminated=hy+(1-hy)*hy
    square=sum(w*x*x for x,w in [(-2,F(1,4)),(0,F(1,2)),(2,F(1,4))])
    clipped=sum(w*min(1,max(-1,x))**2 for x,w in [(-2,F(1,4)),(0,F(1,2)),(2,F(1,4))])
    all_reps=list(map(F,[0,1,2,3]));kept=all_reps[:2]
    mean=lambda x:sum(x)/len(x)
    var=lambda x:sum((v-mean(x))**2 for v in x)/(len(x)-1)
    return dict(two_period=dict(law='L0~Bernoulli1/2; P(L1=1|L0,A0)=1/5+2L0/5+A0/5; risk=1/20+L1/5+3A0/20+A1/10+3L1A1/10',
        never=str(never[0]),always=str(always[0]),dynamic=str(dynamic[0]),dynamic_mean_path=str(plug),
        routes=dynamic[1],dynamic_minus_never=str(dynamic[0]-never[0]),
        assumed_value100_cost20_margin=str(100*(dynamic[0]-never[0])-20),
        invalid_mean_path_margin=str(100*(plug-never[0])-20)),
      competing_events=dict(main_hazard=str(hy),competing_hazard=str(hd),two_period_risk=str(retained),
        elimination_risk=str(eliminated),difference=str(eliminated-retained),
        assumed_loss1000_difference=str(1000*(eliminated-retained))),
      clipping=dict(unclipped_second_moment=str(square),clipped_second_moment=str(clipped),
        assumed_penalty100_difference=str(100*(square-clipped))),
      bootstrap_selection=dict(all=[str(x) for x in all_reps],retained=[str(x) for x in kept],
        all_mean=str(mean(all_reps)),retained_mean=str(mean(kept)),all_sample_variance=str(var(all_reps)),retained_sample_variance=str(var(kept))),
      threshold=dict(natural=[-1,2,-1],lower_bound=0,pointwise=[0,2,0],different_absorbing_policy=[0,2,2]),
      limits=['Authored exact finite laws, not native package results or bank observations.',
        'Means and bootstrap selections illustrate altered targets/distributions, not a measured package calibration defect.',
        'Full g-formula identification requires substantive consistency, sequential exchangeability, positivity and the declared observation law.',
        'No arbitrary-dependent bootstrap, latest-release, full-rights or runtime qualification.'])

if __name__=='__main__':
    p=Path(__file__).resolve().parents[1]/'docs/program/execution/2026-10-20/gformula-reuse-v1/exact-results.json'
    assert not p.exists();p.write_text(json.dumps(calculate(),indent=2)+'\n')
    print(json.dumps({k:v for k,v in calculate().items() if k!='two_period'}))
    print({k:v for k,v in calculate()['two_period'].items() if k!='routes'})

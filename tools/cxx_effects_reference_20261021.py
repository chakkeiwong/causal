"""Exact authored semantic witnesses; no third-party package execution."""
from fractions import Fraction as F
import json

def calculate():
    dose = [F(-1), F(0), F(1)]
    mean = lambda xs: sum(xs, F(0))/len(xs)
    cov = mean([a*a*a for a in dose])-mean(dose)*mean([a*a for a in dose])
    slope = cov/(mean([a*a for a in dose])-mean(dose)**2)
    assert slope == 0 and F(1)**2-F(0)**2 == 1
    effects=[F(-2),F(6)]; precision=[F(1),F(9)]
    pop=mean(effects); wrong=sum(w*t for w,t in zip(precision,effects))/sum(precision)
    assert (pop,wrong)==(F(2),F(26,5))
    draws=[[F(-2),F(6)],[F(6),F(-2)]] # rows=units, columns=joint draws
    portfolio=[mean([row[j] for row in draws]) for j in range(2)]
    assert portfolio==[F(2),F(2)]
    raw=[F(1),F(2)]; scale=F(10); contrast=[F(1,2),F(2)]
    restored=[scale*t*b for t,b in zip(raw,contrast)]
    assert restored==[F(5),F(40)] and mean(restored)==F(45,2)
    # Binary A, X in {-1,1}; overlap probabilities 1/4 and 3/4.
    law=[(-1,0,F(3,8)),(-1,1,F(1,8)),(1,0,F(1,8)),(1,1,F(3,8))]
    ex2=sum(p*x*x for x,a,p in law)
    ez2=sum(p*(F(a)-F(1,2))**2 for x,a,p in law)
    cxz=sum(p*x*(F(a)-F(1,2)) for x,a,p in law)
    beta0=F(2); lam=F(3,4); residual_var=ex2-cxz**2/ez2
    beta=beta0*residual_var/(residual_var+lam)
    tau=cxz/ez2*(beta0-beta)
    assert (beta,tau)==(F(1),F(1))
    # Both normal equations vanish at the unique convex optimum.
    residual=[(x,a,p,beta0*x-beta*x-tau*(F(a)-F(1,2))) for x,a,p in law]
    assert sum(p*(F(a)-F(1,2))*r for x,a,p,r in residual)==0
    assert sum(p*x*r for x,a,p,r in residual)==lam*beta
    return dict(
        dose=dict(slope=str(slope),finite_contrast='1',law='A uniform on {-1,0,1}; Y(a)=a^2'),
        weights=dict(target=str(pop),precision_reweighted=str(wrong),cost='3',
            target_margin=str(pop-3),reweighted_margin=str(wrong-3)),
        joint_draws=dict(rows=[[str(t) for t in row] for row in draws],
            portfolio=[str(t) for t in portfolio],marginal_support=['-2','6'],
            portfolio_support=['2','2'],cost='3',margin='-1'),
        scale=dict(restored=[str(t) for t in restored],correct_mean=str(mean(restored)),
            omitted_contrast_mean=str(mean([scale*t for t in raw])),cost='20',
            correct_margin=str(mean(restored)-20),omitted_margin='-5'),
        shrinkage=dict(beta=str(beta),spurious_treatment=str(tau),true_treatment='0',
            propensity=['1/4','3/4'],penalty=str(lam),
            objective='E[(Y-beta X-tau(A-1/2))^2]+lambda beta^2; Y(a)=2X'),
        limits=['Exact authored finite laws and arithmetic, not native test results.',
          'Financial units and costs are declared hypothetical assumptions.',
          'Two joint draws illustrate aggregation; they establish neither convergence nor calibration.',
          'The penalized linear witness explains confounding from shrinkage; it is not a BCF performance theorem.'])

if __name__=='__main__':
    print(json.dumps(calculate(),indent=2))

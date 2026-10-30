"""Selected persistent-pair/calendar influence construction with label validation."""
import numpy as np
from scipy.stats import norm
from .linkage_sets import binomial_interval


def bartlett(values, bandwidth):
    x=np.asarray(values,float);x=x-x.mean();n=len(x)
    total=float(x@x)
    for lag in range(1,bandwidth+1):
        total+=2*(1-lag/(bandwidth+1))*float(x[lag:]@x[:-lag])
    return total/n


def joint_effect(action,candidates,audited,labels,inclusion,*,bandwidth,
                 gold_errors=None,known_label_error=0.,scale=1000.,alpha=.05,
                 sampling='iid_pairs_independent_stationary_mixing_calendar',
                 first_order_nondegenerate=True):
    a=np.asarray(action,float);y=np.asarray(candidates,float)
    r=np.asarray(audited);label=np.asarray(labels);q=np.asarray(inclusion,float)
    if a.ndim!=2 or y.shape!=(len(a),2,a.shape[1]) or min(a.shape)<30:
        raise ValueError('at least 30 complete pairs and calendar dates required')
    n,t=a.shape
    if any(x.shape!=(n,) for x in (r,label,q)) or not all(np.all(np.isfinite(x)) for x in (a,y,q)):
        raise ValueError('aligned finite histories and pair audit law required')
    if not all(np.all(np.isin(x,[0,1])) for x in (r,label)) or not np.all(np.isin(a,[-1,1])) or np.any(q<=0) or np.any(q>1):
        raise ValueError('binary persistent labels/audits, randomized signed actions and positive known inclusion required')
    if sampling!='iid_pairs_independent_stationary_mixing_calendar' or not first_order_nondegenerate:
        raise ValueError('unsupported joint sampling or degenerate first-order regime')
    if not isinstance(bandwidth,int) or not 0<=bandwidth<t or not 0<alpha<1 or not np.isfinite(scale) or scale<=0:
        raise ValueError('valid bandwidth, confidence level and fixed positive monetary scale required')
    error=float(known_label_error);error_var=0.;validation=None
    if gold_errors is not None:
        gold=np.asarray(gold_errors)
        if gold.ndim!=1 or len(gold)<30 or not np.all(np.isin(gold,[0,1])):
            raise ValueError('independent representative gold-label errors required')
        error=float(gold.mean());validation=binomial_interval(int(gold.sum()),len(gold),alpha)
        if validation[1]>=.5:
            return dict(status='unqualified_label_rank',validation_error_interval=validation)
        error_var=error*(1-error)/len(gold)
    if not np.isfinite(error) or not 0<=error<.5:
        raise ValueError('symmetric independent label-error probability must be below one half')
    v=a[:,None,:]*y;average=v.mean(axis=1);difference=v[:,0]-v[:,1]
    corrected=average+(2*label[:,None]-1)*difference/(2*(1-2*error))
    scores=average+(r/q)[:,None]*(corrected-average)
    derivative=(r/q)[:,None]*(2*label[:,None]-1)*difference/(1-2*error)**2
    components=dict(pair=float(np.var(scores.mean(axis=1),ddof=1)/n),
                    calendar=float(bartlett(scores.mean(axis=0),bandwidth)/t),
                    validation=float(derivative.mean()**2*error_var))
    variance=sum(components.values());estimate=float(scores.mean()*scale)
    if not np.isfinite(variance) or variance<=0:
        raise ValueError('nonpositive or nonfinite joint variance')
    se=float(np.sqrt(variance)*scale);z=float(norm.ppf(1-alpha/2))
    return dict(status='computed',estimate=estimate,standard_error=se,
                interval=[estimate-z*se,estimate+z*se],variance_components={k:v*scale**2 for k,v in components.items()},
                audit_cost_count=int(r.sum()),estimated_label_error=error,
                validation_error_interval=validation,
                inference=dict(method='pair_plus_calendar_with_independent_label_validation',confidence_level=1-alpha,
                    sampling_unit='persistent pair and stationary calendar; independent gold labels',
                    coverage_claim='conditional first-order joint asymptotic; comparable pair/calendar growth; nondegenerate projections; sufficient mixing/moments and bandwidth rates',
                    numerical_status='pair mean variance plus Bartlett calendar variance; interaction may be counted twice',
                    information='known inclusion; randomized actions; accurate gold truth and independent symmetric label errors',
                    empirical_qualification='selected synthetic laws; not arbitrary multiway dependence or semantic validation'))


def allocate_audits(second_moment,cost,probability,budget,floor=.02):
    d=np.asarray(second_moment,float);c=np.asarray(cost,float);p=np.asarray(probability,float)
    if d.shape!=c.shape or p.shape!=c.shape or np.any(d<0) or np.any(c<=0) or np.any(p<=0) or not np.isclose(p.sum(),1):
        raise ValueError('finite nonnegative pilot second moments and positive costs/probabilities required')
    if not all(np.all(np.isfinite(x)) for x in (d,c,p)) or not 0<floor<1 or not floor*(p@c)<=budget<=p@c:
        raise ValueError('budget outside feasible inclusion range')
    weight=np.sqrt(np.maximum(d,1e-16)/c);lo=0.;hi=1/weight.min()
    for _ in range(80):
        mid=(lo+hi)/2;q=np.clip(mid*weight,floor,1.)
        if p@(c*q)<budget:lo=mid
        else:hi=mid
    return np.clip(hi*weight,floor,1.)

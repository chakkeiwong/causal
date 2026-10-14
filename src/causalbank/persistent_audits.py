"""Independent paired trajectories with persistent maps and linked-outcome audits.

No date is counted as a separate identity audit. Audit inclusion probabilities
and any symmetric label-error rate are supplied scientific information.
"""
import numpy as np
from scipy.stats import norm


def audited_pair_effect(action, candidates, audited, labels, inclusion_probability, *,
                        sampling='independent_pairs', label_error=0., alpha=.05,
                        monetary_scale=1., augmentation=True):
    a=np.asarray(action,float);y=np.asarray(candidates,float)
    r=np.asarray(audited);label=np.asarray(labels,float);q=np.asarray(inclusion_probability,float)
    if sampling!='independent_pairs':
        raise ValueError('persistent maps with common-calendar shocks need a joint sampling argument')
    if a.ndim!=2 or len(a)<3 or y.shape!=(len(a),2,a.shape[1]):
        raise ValueError('one complete two-candidate trajectory is required per pair')
    if any(x.shape!=(len(a),) for x in (r,label,q)) or not np.all(np.isin(r,[0,1])):
        raise ValueError('one audit inclusion and map label per pair')
    if not np.all(np.isfinite(a)) or not np.all(np.isfinite(y)) or not np.all(np.isin(a,[-1,1])):
        raise ValueError('this effect uses randomized unit Rademacher actions and finite outcomes')
    if not np.all(np.isfinite(q)) or np.any((q<=0)|(q>1)):
        raise ValueError('known positive audit inclusion probabilities are required')
    if not np.all(np.isin(label[r.astype(bool)],[0,1])):
        raise ValueError('audited map labels must be binary')
    if label_error is None or not np.isfinite(label_error) or not 0<=label_error<.5:
        raise ValueError('label noise needs an externally identified symmetric error probability below one half')
    if not 0<alpha<1 or not np.isfinite(monetary_scale) or monetary_scale<=0:
        raise ValueError('invalid fixed monetary scale or confidence level')
    means=np.mean(a[:,None,:]*y,axis=2)
    baseline=means.mean(axis=1) if augmentation else np.zeros(len(a))
    audited_value=means.mean(axis=1)+(2*np.where(r,label,.5)-1)*(means[:,0]-means[:,1])/(2*(1-2*label_error))
    scores=baseline+r/q*(audited_value-baseline)
    estimate=float(scores.mean());se=float(scores.std(ddof=1)/np.sqrt(len(scores)))
    z=norm.ppf(1-alpha/2)
    return {'status':'computed','estimate':monetary_scale*estimate,'standard_error':monetary_scale*se,
            'interval':(monetary_scale*np.array([estimate-z*se,estimate+z*se])).tolist(),
            'pair_scores':scores,'pairs':len(a),'audited_pairs':int(r.sum()),'dates_per_pair':a.shape[1],
            'inference':{'schema_version':1,'method':'augmented_inverse_audit_pair_mean' if augmentation else 'inverse_audit_pair_mean',
                         'confidence_level':1-alpha,'sampling_unit':'independent complete customer pair',
                         'coverage_claim':'pointwise asymptotic iid-pair CLT with positive inclusion, finite second moment and truthful audit/error law',
                         'target':'population mean focal response to a randomized unit action; fixed horizon average',
                         'additional_information':'audits reveal persistent focal identity and its action/outcome history',
                         'label_error':label_error,'numerical_status':'closed form computed',
                         'empirical_qualification':'model-conditional synthetic reference; consult retained study'}}

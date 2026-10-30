"""Bounded clock interpretation and independently calibrated whole-pair linkage."""
import numpy as np
from .responses import bartlett_lrv
from .dynamic_funding import train_pilot


def interpret_source(fixture):
    """Does not access evaluation truth. Verified means supplied provenance,
    not proof that a source owner's semantic assertion is economically true.
    """
    if fixture['requested_unit']=='customer':
        multiplicities={r['account']:sum(s['account']==r['account'] for s in fixture['owners']) for r in fixture['owners']}
        if any(n>1 for n in multiplicities.values()):
            return {'status':'unresolved_entity_allocation','candidates':[],'question':'What ownership allocation defines the customer balance target?'}
    asserted={c['column'] for c in fixture['claims'] if c['verified'] and c['role']=='availability'}
    clocks=sorted(asserted or {'business_day','received_day'});candidates=[]
    for clock in clocks:
        eligible=[r for r in fixture['rows'] if r[clock]<=fixture['decision_day']]
        newest={}
        for r in eligible:
            key=(r['account'],r['business_day'])
            if key not in newest or r['revision']>newest[key]['revision']:newest[key]=r
        candidates.append({'clock':clock,'balance':sum(r['balance'] for r in newest.values()),'source_records':len(newest)})
    unique={c['balance'] for c in candidates}
    return {'status':'conditional_acceptance' if len(unique)==1 else 'unresolved_clock','candidates':candidates,
            'question':None if len(unique)==1 else 'Which timestamp is first availability to the decision system?'}


def mix_candidate_histories(first,second,rng,probability):
    n=len(first['action']);stratum=rng.integers(0,2,n);correct=rng.random(n)<np.asarray(probability)[stratum]
    y1=np.where(correct[:,None],first['outcomes'],second['outcomes']);y2=np.where(correct[:,None],second['outcomes'],first['outcomes'])
    # No candidate's lagged outcome is treated as the true entity history.
    basic=first['x'][:,[0,2,3]]
    x=np.column_stack((basic,basic*stratum[:,None]))
    return {'x':x,'action':first['action'],'outcomes':np.column_stack((y1,y2)),'stratum':stratum,'correct':correct}


def linked_response(data,pilot_fit,audit_success,audit_sizes,target,bandwidth,stratum_weights=(.5,.5)):
    pred=data['x']@pilot_fit['coefficient'];v=data['action']-pred[:,0];residual=data['outcomes']-pred[:,1:]
    n=len(v);d=target.horizon+1;eta=[];influence=[]
    for s in (0,1):
        indicator=data['stratum']==s;q=float(np.mean(indicator*v*v))
        if q<=0:raise ValueError('missing linked stratum/action variation')
        estimate=np.mean(indicator[:,None]*v[:,None]*residual,axis=0)/q
        eta.append(estimate);influence.append(indicator[:,None]*v[:,None]*(residual-v[:,None]*estimate)/q)
    eta=np.array(eta);psi=np.column_stack(influence);cov_eta=bartlett_lrv(psi,bandwidth)/n
    p=np.asarray(audit_success)/np.asarray(audit_sizes);sizes=np.asarray(audit_sizes);z=1.95996398454
    # Wilson audit intervals, rather than a plug-in zero variance at all-success.
    center=(p+z*z/(2*sizes))/(1+z*z/sizes);half=z*np.sqrt(p*(1-p)/sizes+z*z/(4*sizes*sizes))/(1+z*z/sizes)
    if np.any((center-half<=.5)&(center+half>=.5)):
        return {'status':'unavailable_mapping_rank','audit_probability':p,'audit_intervals':np.column_stack((center-half,center+half))}
    jac=np.zeros((d,4*d));cal_jac=np.empty((d,2));theta=np.zeros(d)
    for s,w in enumerate(stratum_weights):
        first,second=eta[s,:d],eta[s,d:];den=2*p[s]-1
        theta+=w*(p[s]*first-(1-p[s])*second)/den
        jac[:,2*d*s:2*d*s+d]=np.eye(d)*w*p[s]/den
        jac[:,2*d*s+d:2*d*s+2*d]=-np.eye(d)*w*(1-p[s])/den
        cal_jac[:,s]=w*(second-first)/den**2
    fixed=jac@cov_eta@jac.T;calibration=(cal_jac*(p*(1-p)/sizes))@cal_jac.T;covariance=fixed+calibration
    weights=target.weights();financial=float(weights@theta-target.direct_cost());fvar=float(weights@covariance@weights)
    naive=np.mean(eta[:,:d],axis=0)
    naive_jac=np.zeros((d,4*d));naive_jac[:,:d]=np.eye(d)*.5;naive_jac[:,2*d:3*d]=np.eye(d)*.5
    return {'status':'computed','estimate':theta,'covariance':covariance,'fixed_calibration_covariance':fixed,'calibration_covariance':calibration,
            'eta':eta,'eta_influence':psi,'jacobian':jac,'calibration_jacobian':cal_jac,'audit_probability':p,
            'financial_value':financial,'financial_se':float(np.sqrt(fvar)),'financial_fixed_calibration_se':float(np.sqrt(weights@fixed@weights)),
            'financial_interval':[financial-z*np.sqrt(fvar),financial+z*np.sqrt(fvar)],'naive_financial_value':float(weights@naive-target.direct_cost()),
            'naive_financial_se':float(np.sqrt(weights@naive_jac@cov_eta@naive_jac.T@weights))}

"""Two consumers of a common dynamic funding construction.

Partitions accelerate the declared experiment; they never change its
sampling unit. Serial and parallel modes share the same semantic validation.
"""
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass,asdict,replace
import hashlib,json
import numpy as np
from threadpoolctl import threadpool_limits,threadpool_info
from .dynamic_funding import FundingTarget,fingerprint
from .linked_observation import interpret_source
from .dynamic_validation import validate_target,validate_inputs
from .linkage_sets import project_funding,decode_set,encode_set


def array_identity(data):
    digest=hashlib.sha256()
    for key in sorted(data):
        value=np.ascontiguousarray(data[key]);digest.update(key.encode());digest.update(str(value.dtype).encode());digest.update(str(value.shape).encode());digest.update(value.tobytes())
    return digest.hexdigest()


def materialize_candidate_feed(feed,horizon):
    """Reconstruct a fixed retrospective outcome view from versioned records.

    Predecision features must be available at origin; realized outcomes may
    arrive later, but only revisions received by the fixed extraction cutoff
    enter this analysis. This is not a real-time outcome prediction view.
    """
    rows=feed['outcome_records'];latest={};seen_revisions={};cutoff=feed['extraction_cutoff']
    for row in rows:
        if not all(np.isfinite(row[key]) for key in ('received_day','business_day','revision','balance')):raise ValueError('nonfinite source record')
        if row['received_day']>cutoff:continue
        key=(row['origin'],row['candidate'],row['horizon'])
        revision_key=(*key,row['revision'])
        if revision_key in seen_revisions and row!=seen_revisions[revision_key]:raise ValueError('conflicting records for the same outcome revision')
        seen_revisions[revision_key]=row
        if key not in latest or row['revision']>latest[key]['revision']:latest[key]=row
    features=sorted(feed['predecision_records'],key=lambda r:r['origin']);n=len(features);x=[];a=[];s=[];out=np.empty((n,2*(horizon+1)))
    for i,row in enumerate(features):
        if not all(np.isfinite(row[key]) for key in ('received_day','decision_day')):raise ValueError('nonfinite predecision clock')
        if row['origin']!=i or row['received_day']>row['decision_day']:raise ValueError('missing, duplicated or unavailable predecision record')
        x.append(row['features']);a.append(row['action']);s.append(row['stratum'])
        for candidate in (0,1):
            for h in range(horizon+1):
                key=(i,candidate,h)
                if key not in latest:raise ValueError('incomplete candidate outcome history')
                outcome=latest[key]
                if outcome['business_day']!=row['decision_day']+h:raise ValueError('outcome horizon/clock mismatch')
                out[i,candidate*(horizon+1)+h]=outcome['balance']
    return {'x':np.array(x),'action':np.array(a),'stratum':np.array(s),'outcomes':out}


def _worker(task):
    kind,args=task
    with threadpool_limits(limits=1):
        if kind=='moments':
            x,y=args;value=(x.T@x,x.T@y,y.sum(axis=0),(y*y).sum(axis=0),len(x))
        elif kind=='loss':
            x,y,coef,scale=args;value=float(np.sum((y-x@coef)**2/scale))
        elif kind=='audit':
            strata,correct=args;value=(np.bincount(strata,weights=correct,minlength=2),np.bincount(strata,minlength=2))
        elif kind=='response':
            v,residual,strata=args;value=[(float(np.sum((strata==s)*v*v)),np.sum((strata==s)[:,None]*v[:,None]*residual,axis=0)) for s in (0,1)]
        elif kind=='lag_products':
            core,previous,bandwidth=args
            full=np.vstack((previous,core));offset=len(previous);p=core.shape[1]
            value=[core.T@core]
            for lag in range(1,bandwidth+1):
                valid=max(0,lag-offset);later=core[valid:];earlier=full[offset+valid-lag:len(full)-lag]
                value.append(later.T@earlier if len(later) else np.zeros((p,p)))
        else:raise ValueError('unknown partition operation')
        return value,max([i['num_threads'] for i in threadpool_info()] or [1])


class Backend:
    def __init__(self,workers=1):
        if workers not in (1,2,4):raise ValueError('qualified worker counts are 1, 2, 4')
        self.workers=workers;self.pool=None;self.max_threads=0
    def __enter__(self):
        if self.workers>1:self.pool=ProcessPoolExecutor(max_workers=self.workers)
        return self
    def __exit__(self,*args):
        if self.pool:self.pool.shutdown()
    def pieces(self,n):return [a for a in np.array_split(np.arange(n),self.workers) if len(a)]
    def map(self,tasks):
        outputs=list(self.pool.map(_worker,tasks)) if self.pool else list(map(_worker,tasks))
        self.max_threads=max(self.max_threads,max(r[1] for r in outputs));return [r[0] for r in outputs]
    def moments(self,x,y):
        rows=self.map([('moments',(x[ix],y[ix])) for ix in self.pieces(len(x))]);return tuple(sum(r[k] for r in rows) for k in range(5))
    def audit(self,strata,correct):
        if len(strata)==0:return np.zeros(2),np.zeros(2,dtype=int)
        rows=self.map([('audit',(strata[ix],correct[ix])) for ix in self.pieces(len(strata))]);return tuple(sum(r[k] for r in rows) for k in range(2))
    def lrv(self,influence,bandwidth):
        centered=influence-influence.mean(axis=0);tasks=[]
        for ix in self.pieces(len(centered)):
            start=int(ix[0]);tasks.append(('lag_products',(centered[ix],centered[max(0,start-bandwidth):start],bandwidth)))
        pieces=self.map(tasks);gammas=[sum(part[k] for part in pieces)/len(centered) for k in range(bandwidth+1)]
        result=gammas[0]
        for k in range(1,bandwidth+1):result+=(1-k/(bandwidth+1))*(gammas[k]+gammas[k].T)
        return result


def train(pilot,penalties,backend):
    x=pilot['x'];y=np.column_stack((pilot['action'],pilot['outcomes']));split=len(x)//2
    xx,xy,ys,y2,n=backend.moments(x[:split],y[:split]);scale=y2/n-(ys/n)**2
    def solve(xx,xy,penalty):
        reg=np.eye(len(xx))*penalty;reg[0,0]=0
        return np.linalg.solve(xx+reg,xy)
    losses=[]
    for penalty in penalties:
        coef=solve(xx,xy,penalty);indices=backend.pieces(len(x)-split)
        losses.append(sum(backend.map([('loss',(x[split+ix],y[split+ix],coef,scale)) for ix in indices]))/((len(x)-split)*y.shape[1]))
    chosen=int(np.argmin(losses));penalty=penalties[chosen];xx,xy,*_=backend.moments(x,y)
    return {'coefficient':solve(xx,xy,penalty),'penalty':penalty,'validation_losses':losses,'training_origins':len(x)}


@dataclass(frozen=True)
class DynamicBrief:
    target: FundingTarget
    observation_identity: str
    pilot_identity: str
    calibration_identity: str
    bandwidth: int
    mapping: str = 'independent_stratified_pair_swap'
    identification: str = 'conditional_price_innovation'

    def identity(self):
        validate_target(self.target)
        if not isinstance(self.bandwidth,(int,np.integer)) or self.bandwidth<0:raise ValueError('bandwidth must be a nonnegative integer')
        if self.mapping!='independent_stratified_pair_swap':raise ValueError('unqualified linkage law')
        if self.identification!='conditional_price_innovation':raise ValueError('unsupported dynamic identification expression')
        return fingerprint(self.target,self.observation_identity,self.pilot_identity,self.calibration_identity,self.bandwidth)


def fit_linked(data,pilot_fit,audit_success,audit_sizes,brief,backend,inference='regular_delta',alpha=.05):
    target=brief.target;target.validate();d=target.horizon+1;n=len(data['action'])
    if data['outcomes'].shape[1]!=2*d:raise ValueError('candidate horizons differ from the requested stock response')
    pred=data['x']@pilot_fit['coefficient'];v=data['action']-pred[:,0];residual=data['outcomes']-pred[:,1:]
    chunks=backend.map([('response',(v[ix],residual[ix],data['stratum'][ix])) for ix in backend.pieces(n)])
    eta=[];psi=[]
    for s in (0,1):
        q=sum(c[s][0] for c in chunks)/n
        if not np.isfinite(q) or q<=1e-10:raise ValueError('missing stratum or unsupported price innovation')
        estimate=sum(c[s][1] for c in chunks)/(n*q)
        eta.append(estimate);psi.append((data['stratum']==s)[:,None]*v[:,None]*(residual-v[:,None]*estimate)/q)
    eta=np.array(eta);influence=np.column_stack(psi);cov_eta=backend.lrv(influence,brief.bandwidth)/n
    if not np.all(np.isfinite(eta)) or not np.all(np.isfinite(cov_eta)):raise ValueError('nonfinite response inference')
    if inference=='weak_linkage_projection':
        result=project_funding(eta,cov_eta,audit_success,audit_sizes,target,alpha)
        result.update({'identity':brief.identity(),'pilot_penalty':pilot_fit['penalty'],'calendar_origins':n})
        return result
    if inference!='regular_delta' or alpha!=.05:raise ValueError('unsupported regular inference procedure')
    if np.any(np.asarray(audit_sizes)<=0):raise ValueError('regular inverse mapping requires audits in both strata')
    sizes=np.asarray(audit_sizes);p=np.asarray(audit_success)/sizes;z=1.95996398454;center=(p+z*z/(2*sizes))/(1+z*z/sizes);half=z*np.sqrt(p*(1-p)/sizes+z*z/(4*sizes*sizes))/(1+z*z/sizes)
    if np.any((center-half<=.5)&(center+half>=.5)):raise ValueError('audit does not support regular inverse mapping')
    jac=np.zeros((d,4*d));jcal=np.empty((d,2));theta=np.zeros(d)
    for s in (0,1):
        first,second=eta[s,:d],eta[s,d:];den=2*p[s]-1;theta+=.5*(p[s]*first-(1-p[s])*second)/den
        jac[:,2*d*s:2*d*s+d]=np.eye(d)*.5*p[s]/den;jac[:,2*d*s+d:2*d*s+2*d]=-np.eye(d)*.5*(1-p[s])/den
        jcal[:,s]=.5*(second-first)/den**2
    covariance=jac@cov_eta@jac.T+(jcal*(p*(1-p)/sizes))@jcal.T
    weights=target.weights();value=float(weights@theta-target.direct_cost());se=float(np.sqrt(weights@covariance@weights))
    if not np.all(np.isfinite([value,se,value-z*se,value+z*se])) or se<=0:raise ValueError('regular financial inference requires finite value, endpoints and positive variance')
    return {'status':'computed','identity':brief.identity(),'response':theta,'covariance':covariance,
            'financial_value':value,'financial_se':se,'financial_interval':[value-z*se,value+z*se],
            'audit_probability':p,'pilot_penalty':pilot_fit['penalty'],'calendar_origins':n,
            'scope':'conditional structural innovation and calibrated mapping; independent pilot and audit; stable common calendar'}


def run_funding(brief,source_fixture,pilot,data,audit_strata,audit_correct,penalties,workers=1,cached_identity=None,inference='regular_delta',alpha=.05):
    brief.identity()
    observation=interpret_source(source_fixture)
    if observation['status']!='conditional_acceptance':raise ValueError('source observation interpretation unresolved: '+observation['status'])
    if source_fixture['requested_unit']!='account' or {c['clock'] for c in observation['candidates']}!={'received_day'}:
        raise ValueError('candidate-feed materializer requires the account unit and an unambiguous received-day clock')
    # Evaluation truth belongs only to the test harness. All supplied source
    # assertions, including disagreements, belong to the scientific identity.
    source_contract={k:v for k,v in source_fixture.items() if k!='evaluation_truth'}
    view={'mode':'supplied_materialized_arrays'}
    if 'outcome_records' in data:
        if not np.isfinite(data['extraction_cutoff']):raise ValueError('extraction cutoff must be finite')
        view={'mode':'retrospective_candidate_feed','extraction_cutoff':data['extraction_cutoff'],
              'availability_clock':'received_day','predecision_clock':'decision_day'}
        data=materialize_candidate_feed(data,brief.target.horizon)
    validate_inputs(brief,pilot,data,audit_strata,audit_correct,penalties,inference,alpha)
    audit_strata=np.asarray(audit_strata,dtype=int);audit_correct=np.asarray(audit_correct,dtype=int)
    identity=hashlib.sha256(json.dumps({'brief':brief.identity(),'pilot_arrays':array_identity({k:pilot[k] for k in ('x','action','outcomes','stratum')}),
        'evaluation_arrays':array_identity(data),'audit_arrays':array_identity({'strata':audit_strata,'correct':audit_correct}),
        'source_contract':source_contract,'observation_view':view,
        'procedure':{'recipe':'dynamic-linked-funding-v2','penalties':list(penalties),'pilot_selection':'chronological_half_standardized_squared_loss','inference':inference,'confidence_error':alpha,'projection_coordinates':'average_and_half_difference' if inference=='weak_linkage_projection' else None,'projection_error_split':[.5,.5] if inference=='weak_linkage_projection' else None,'covariance':'centered_Bartlett_denominator_T_plus_independent_binomial_calibration','identification':brief.identification}},sort_keys=True).encode()).hexdigest()
    if cached_identity is not None and cached_identity!=identity:raise ValueError('scientific inputs changed; cached inference is invalid')
    with Backend(workers) as backend:
        calibration=backend.audit(audit_strata,audit_correct);pilot_fit=train(pilot,penalties,backend)
        result=fit_linked(data,pilot_fit,*calibration,brief,backend,inference,alpha);result['maximum_worker_numeric_threads']=backend.max_threads;result['identity']=identity
    result['observation']=observation;result['request']=asdict(brief)
    result['source_contract']=source_contract;result['observation_view']=view
    result['identification']={'expression':'stratified partialling_out_response followed by inverse_pair_assignment',
        'assumptions':['conditional price innovation excludes future disturbances','fixed intervention leaves future assignment natural','stable common calendar law','independent invariant pilot','representative independent pair audit','noninformative whole-history swaps within stratum'],
        'status':'conditional_on_supplied_scientific_restrictions'}
    return result


def treasury_report(result):
    if result['status']=='computed_set':
        return {'funding_contribution_set_currency':result['financial_set'],'confidence_level':result['confidence_level'],
                'scientific_identity':result['identity'],'uncertainty_scope':result['scope']}
    return {'funding_contribution_currency':result['financial_value'],'interval_currency':result['financial_interval'],
            'response_millions_per_branch':result['response'].tolist(),'scientific_identity':result['identity']}


def application_result(result,booked_accounts):
    if not np.isfinite(booked_accounts) or booked_accounts<=0:raise ValueError('account denominator must be externally fixed, finite and positive')
    if result['status']=='computed_set':
        scaled=[(lo/booked_accounts,hi/booked_accounts) for lo,hi in decode_set(result['financial_set'])]
        return {'funding_set_per_account':encode_set(scaled),'confidence_level':result['confidence_level'],
                'scientific_identity':result['identity'],'uncertainty_scope':result['scope'],
                'denominator_scope':'fixed supplied count; estimated or selected account exposure needs additional influence'}
    return {'incremental_funding_per_account':result['financial_value']/booked_accounts,
            'interval_per_account':[x/booked_accounts for x in result['financial_interval']],
            'scientific_identity':result['identity'],'denominator_scope':'fixed supplied count; estimated or selected account exposure needs additional influence'}

"""Explicit separated-block partially linear IV operations.

Supported learners are enumerated. A supplied population mixing/rate statement
is a scientific assumption, not a property established by accepting an object.
"""
from dataclasses import dataclass,asdict
import hashlib
import json
import numpy as np
from sklearn.linear_model import Lasso


@dataclass(frozen=True)
class BlockedIVRequest:
    learner:str
    gap:int
    mixing_rate_lower_bound:float
    horizon:int=0
    feature_lags:int=0
    feature_available_after_origin:bool=False
    penalty_multiplier:float=.03
    outcome_envelope:float=10.
    sampling:str='bounded_geometrically_beta_mixing_calendar'
    approximation_and_rate_statement:str='fixed sparse linear dictionary; population RE; product error o(n^-1/2); L*score_error=o(1)'

    def validate(self,n):
        if self.learner not in ('sparse_lasso','fixed_basis','intercept_challenger'):
            raise ValueError('arbitrary learners do not inherit dependent inference')
        if self.sampling!='bounded_geometrically_beta_mixing_calendar':
            raise ValueError('unsupported dependent sampling law')
        if self.feature_available_after_origin:
            raise ValueError('future/late features cannot enter the decision-time adjustment set')
        if any(not isinstance(x,int) or x<0 for x in (self.gap,self.horizon,self.feature_lags)):
            raise ValueError('nonnegative integer clock spans required')
        if not np.isfinite(self.mixing_rate_lower_bound) or self.mixing_rate_lower_bound<=0:
            raise ValueError('positive supplied population mixing-rate bound required')
        if self.gap<np.ceil(3*np.log(n)/self.mixing_rate_lower_bound)+self.horizon+self.feature_lags:
            raise ValueError('gap insufficient after expanding lag/outcome windows')
        if self.gap>=n//2 or not self.approximation_and_rate_statement:
            raise ValueError('insufficient blocks or missing nuisance/covariance rate assumptions')
        if not 0<self.penalty_multiplier or not np.isfinite(self.penalty_multiplier) or not 0<self.outcome_envelope or not np.isfinite(self.outcome_envelope):
            raise ValueError('finite positive penalty and envelope required')


def blocked_covariance(scores,folds,bandwidth):
    scores=np.asarray(scores,float);folds=np.asarray(folds);centered=scores-scores.mean();n=len(scores)
    value=float(centered@centered)
    for lag in range(1,bandwidth+1):
        products=0.
        for f in np.unique(folds):
            x=centered[folds==f]
            products+=float(x[lag:]@x[:-lag])
        value+=2*(1-lag/(bandwidth+1))*products
    return value/n


def fit_blocked(request,controls,outcome,treatment,instrument,*,oracle_predictions=None):
    c=np.asarray(controls,float);targets=np.column_stack([outcome,treatment,instrument]).astype(float);n=len(c)
    request.validate(n)
    if c.ndim!=2 or n<100 or targets.shape!=(n,3) or not np.all(np.isfinite(c)) or not np.all(np.isfinite(targets)):
        raise ValueError('finite aligned control/outcome/treatment/instrument arrays required')
    if np.max(abs(targets))>request.outcome_envelope or np.max(abs(c))>request.outcome_envelope:
        raise ValueError('data exceed the supplied bounded-law envelope')
    middle=n//2;left=middle-request.gap//2;right=left+request.gap
    blocks=[np.arange(left),np.arange(right,n)];residuals=[];tuning=[];origin_ids=[];fold_ids=[]
    for fold,evaluation in enumerate(blocks):
        train=blocks[1-fold];x=c[train];y=targets[train];test=c[evaluation]
        if oracle_predictions is not None:
            pred=np.asarray(oracle_predictions)[evaluation]
            tuning.append({'method':'oracle_reference_for_known_truth_study'})
        elif request.learner=='sparse_lasso':
            # Every tuning outcome comes from this training block. Leave a
            # second temporal gap between inner training and validation.
            split=len(train)//2;start=split+request.gap
            if start>=len(train)-20:raise ValueError('not enough training data for separated tuning')
            base=request.penalty_multiplier*np.sqrt(np.log(len(train))*np.log(n*c.shape[1])/len(train))
            candidates=np.array([.5,1.,2.])*base;losses=[]
            for penalty in candidates:
                fit=[Lasso(alpha=penalty,max_iter=5000,tol=1e-8).fit(x[:split],y[:split,j]) for j in range(3)]
                prediction=np.column_stack([f.predict(x[start:]) for f in fit]);losses.append(float(np.mean((prediction-y[start:])**2)))
            chosen=int(np.argmin(losses));penalty=float(candidates[chosen])
            models=[Lasso(alpha=penalty,max_iter=5000,tol=1e-8).fit(x,y[:,j]) for j in range(3)]
            pred=np.column_stack([m.predict(test) for m in models])
            tuning.append(dict(penalties=candidates,losses=losses,chosen=penalty,
                               training_origins=[int(train[0]),int(train[-1])],
                               evaluation_origins=[int(evaluation[0]),int(evaluation[-1])]))
        elif request.learner=='fixed_basis':
            coef=np.linalg.lstsq(np.column_stack([np.ones(len(x)),x]),y,rcond=None)[0]
            pred=np.column_stack([np.ones(len(test)),test])@coef;tuning.append({'method':'fixed_dictionary_OLS'})
        else:pred=np.tile(y.mean(axis=0),(len(test),1));tuning.append({'method':'misspecified_intercept_only'})
        pred=np.clip(pred,-request.outcome_envelope,request.outcome_envelope)
        residuals.append(targets[evaluation]-pred);origin_ids.extend(evaluation);fold_ids.extend([fold]*len(evaluation))
    residuals=np.vstack(residuals);folds=np.array(fold_ids);nret=len(residuals)
    denominator=float(np.mean(residuals[:,2]*residuals[:,1]))
    if abs(denominator)<1e-8:raise ValueError('numerically unresolved IV slope; this regular operation has no weak-IV guarantee')
    theta=float(np.mean(residuals[:,2]*residuals[:,0])/denominator)
    scores=residuals[:,2]*(residuals[:,0]-theta*residuals[:,1]);bandwidth=int(nret**.2)
    variance=blocked_covariance(scores,folds,bandwidth)/(nret*denominator**2)
    if variance<=0:raise ValueError('nonpositive fitted-score variance')
    se=float(np.sqrt(variance));identity=hashlib.sha256(json.dumps(asdict(request),sort_keys=True).encode()+c.tobytes()+targets.tobytes()).hexdigest()
    return dict(status='computed',estimate=theta,standard_error=se,interval=[theta-1.96*se,theta+1.96*se],
                identity=identity,scores=scores,folds=folds,origins=np.array(origin_ids),bandwidth=bandwidth,
                denominator=denominator,tuning=tuning,
                inference={'method':'separated_block_orthogonal_IV','confidence_level':.95,
                           'sampling_unit':'calendar origin with whole declared lag/outcome window',
                           'coverage_claim':'conditional asymptotic under supplied bounded mixing, IV, nuisance-rate and covariance conditions',
                           'learner':request.learner,'rate_assumptions':request.approximation_and_rate_statement,
                           'mixing_rate_is_supplied_not_estimated':request.mixing_rate_lower_bound,
                           'numerical_status':'computed regular slope and within-block Bartlett variance',
                           'empirical_qualification':'selected model reference; not arbitrary learner qualification'})

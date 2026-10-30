"""Pilot-trained dynamic partialling-out and calendar inference.

The caller supplies causal innovation, stable-law and pilot-independence
assumptions. The module checks numerical/semantic compatibility, not those
scientific premises.
"""
from dataclasses import dataclass, asdict
import hashlib
import json
import numpy as np
from .responses import bartlett_lrv


@dataclass(frozen=True)
class FundingTarget:
    horizon: int = 6
    discount: float = .99
    monthly_margin: float = .002
    currency_per_balance_unit: float = 1e6
    branches: int = 48
    baseline_per_branch: float = 100.
    action_unit: str = '10bp_one_month'
    outcome_kind: str = 'balance_stock'
    sampling: str = 'stationary_common_calendar'

    def validate(self):
        if self.action_unit != '10bp_one_month' or self.outcome_kind != 'balance_stock':
            raise ValueError('funding accounting requires a one-month 10bp price intervention and balance stocks')
        if self.sampling != 'stationary_common_calendar':
            raise ValueError('calendar HAC cannot inherit a different sampling law')
        if self.horizon < 0 or self.branches < 1:
            raise ValueError('invalid target dimensions')

    def weights(self):
        self.validate()
        weights=self.monthly_margin*self.discount**np.arange(self.horizon+1)
        weights[0]-=.001/12  # Higher first-month rate also applies to induced balances.
        return self.branches*self.currency_per_balance_unit*weights

    def direct_cost(self):
        self.validate()
        return self.branches*self.baseline_per_branch*self.currency_per_balance_unit*.001/12


def fingerprint(target, observation_identity, pilot_identity, calibration_identity, bandwidth):
    payload=dict(target=asdict(target),observation=observation_identity,pilot=pilot_identity,
                 calibration=calibration_identity,bandwidth=int(bandwidth))
    return hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()


def generate(spec, dates, rng, retain_branches=False):
    """Known-truth branch mechanism. Baseline balance is added in accounting."""
    n=dates+spec['burn']+spec['horizon']+1; b=spec['branches']
    w=np.zeros(n); action=np.zeros(n); branch=np.zeros((n,b))
    beta=spec['beta']*np.linspace(.6,1.4,b)
    for t in range(1,n):
        w[t]=spec['driver_rho']*w[t-1]+np.sqrt(1-spec['driver_rho']**2)*rng.normal()
        action[t]=.5*w[t]+.2*(w[t]**2-1)+rng.normal()
        branch[t]=spec['rho']*branch[t-1]+beta*action[t]+1.2*w[t]+.4*(w[t]**2-1)+spec['common_noise_sd']*rng.normal()+spec['branch_noise_sd']*rng.normal(size=b)
    start=spec['burn']+1; origins=np.arange(start,start+dates)
    aggregate=branch.mean(axis=1)
    x=np.column_stack((np.ones(dates),aggregate[origins-1],w[origins],w[origins]**2-1))
    y=np.column_stack([aggregate[origins+h] for h in range(spec['horizon']+1)])
    result={'x':x,'action':action[origins],'outcomes':y,'driver':w[origins]}
    if retain_branches:
        result['branch_outcomes']=np.stack([branch[origins+h] for h in range(spec['horizon']+1)],axis=2)
    return result


def ridge_fit(x, y, penalty):
    regularizer=np.eye(x.shape[1])*penalty; regularizer[0,0]=0
    return np.linalg.solve(x.T@x+regularizer,x.T@y)


def train_pilot(pilot, penalties):
    x=pilot['x']; targets=np.column_stack((pilot['action'],pilot['outcomes']))
    split=len(x)//2
    losses=[]
    for penalty in penalties:
        coef=ridge_fit(x[:split],targets[:split],penalty)
        # Standardize validation losses so a long-horizon response cannot
        # hide a poor treatment-mean fit solely through its currency scale.
        scale=np.var(targets[:split],axis=0)
        losses.append(float(np.mean((targets[split:]-x[split:]@coef)**2/scale)))
    selected=int(np.argmin(losses)); penalty=penalties[selected]
    return {'coefficient':ridge_fit(x,targets,penalty),'penalty':penalty,'validation_losses':losses,'training_origins':len(x)}


def evaluate(data, pilot_fit, target, bandwidth):
    target.validate(); y=np.asarray(data['outcomes']); x=np.asarray(data['x'])
    if y.shape[1]!=target.horizon+1:
        raise ValueError('response horizons do not match economic target')
    pred=x@pilot_fit['coefficient']; v=data['action']-pred[:,0]; residual=y-pred[:,1:]
    q=float(np.mean(v*v))
    if q<=1e-10: raise ValueError('unsupported or weak action innovation')
    theta=np.mean(v[:,None]*residual,axis=0)/q
    influence=v[:,None]*(residual-v[:,None]*theta)/q
    covariance=bartlett_lrv(influence,bandwidth)/len(x)
    weights=target.weights(); value=float(weights@theta-target.direct_cost()); variance=float(weights@covariance@weights)
    return {'estimate':theta,'covariance':covariance,'influence':influence,'residual_action':v,
            'residual_outcomes':residual,'innovation_second_moment':q,'origins':len(x),
            'financial_value':value,'financial_variance':variance,'financial_interval':[value-1.95996398454*np.sqrt(variance),value+1.95996398454*np.sqrt(variance)],
            'price_cost':target.direct_cost(),'bandwidth':int(bandwidth),'pilot_penalty':pilot_fit['penalty']}

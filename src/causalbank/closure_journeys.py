"""Shared scientific semantics for three distinct experiment families."""
from copy import deepcopy
from dataclasses import dataclass,asdict
import hashlib
import json
from pathlib import Path
import numpy as np
from .persistent_audits import audited_pair_effect
from .latent_temporal_sets import effect_set
from .nonlinear_stability import fit_stable
from .linkage_sets import decode_set,encode_set


@dataclass(frozen=True)
class JourneyRequest:
    family:str
    sampling:str
    population:str
    unit:str
    clock:str
    inference:str
    monetary_scale:float
    policy_information:str='observed_signal_and_past'
    schema_version:int=1

    def validate(self):
        allowed={
            'persistent_funding':('independent_pairs','pair','action_then_outcome','audited_pair_CLT'),
            'nonlinear_servicing':('independent_trajectories','customer','signal_action_reward_transition','audited_nonlinear_delta'),
            'discovery_decision':('independent_gaussian_episodes','episode','Z_then_A_then_Y','outer_graph_union')}
        if self.schema_version!=1 or self.family not in allowed:raise ValueError('unsupported journey request')
        if (self.sampling,self.unit,self.clock,self.inference)!=allowed[self.family]:
            raise ValueError('incompatible sampling/unit/clock/inference composition for '+self.family)
        if not self.population or not np.isfinite(self.monetary_scale) or self.monetary_scale<=0:
            raise ValueError('explicit population and fixed positive monetary scale required')
        if self.family=='nonlinear_servicing' and self.policy_information!='observed_signal_and_past':
            raise ValueError('audited current hidden states or future records cannot enter the evaluated policy')


def _plain(value):
    if isinstance(value,np.ndarray):return value.tolist()
    if isinstance(value,np.generic):return value.item()
    raise TypeError(type(value).__name__)


def run_journey(request,payload):
    request.validate()
    if request.family=='persistent_funding':
        result=audited_pair_effect(**payload,monetary_scale=request.monetary_scale)
    elif request.family=='nonlinear_servicing':
        result=fit_stable(payload['main'],payload['audit'],payload['states'],payload['policy'])
    else:
        result=effect_set(payload['episodes'],information=payload['information'])
    return compose_result(request,payload,result)


def compose_result(request,payload,result):
    """The same provenance, unit and result obligations for direct composition."""
    request.validate()
    modules=['closure_journeys.py','persistent_audits.py','latent_temporal_sets.py','nonlinear_audited.py','nonlinear_stability.py']
    implementation={name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest() for name in modules}
    identity=hashlib.sha256(json.dumps({'request':asdict(request),'payload':payload,'implementation':implementation},sort_keys=True,default=_plain,allow_nan=False).encode()).hexdigest()
    if request.family=='persistent_funding':
        pieces=[tuple(result['interval'])];estimate=result['estimate']
    elif request.family=='nonlinear_servicing':
        estimate=request.monetary_scale*result['value']
        pieces=[tuple(request.monetary_scale*np.array(result['interval']))] if result['status']=='computed' else []
    else:
        pieces=[(a*request.monetary_scale,b*request.monetary_scale) for a,b in decode_set(result['effect_set'])];estimate=None
    inference=deepcopy(result['inference'])
    return dict(schema_version=1,status=result['status'],identity=identity,request=asdict(request),
                estimate_currency=estimate,financial_set=encode_set(pieces),inference=inference,
                diagnosis=result.get('next_information') or ('interval withheld; boundary, numerical or information failure' if result['status']!='computed' and request.family=='nonlinear_servicing' else None),
                numerical_details=result)


def treasury_consumer(result):
    return {k:deepcopy(result[k]) for k in ('status','identity','request','estimate_currency','financial_set','inference','diagnosis')}


def application_consumer(result,fixed_accounts):
    if not np.isfinite(fixed_accounts) or fixed_accounts<=0:raise ValueError('fixed external account count required')
    output=treasury_consumer(result)
    output['estimate_per_account']=None if result['estimate_currency'] is None else result['estimate_currency']/fixed_accounts
    output['financial_set_per_account']=encode_set([(a/fixed_accounts,b/fixed_accounts) for a,b in decode_set(result['financial_set'])])
    output['denominator_scope']='fixed supplied account exposure; not an estimated denominator'
    return output

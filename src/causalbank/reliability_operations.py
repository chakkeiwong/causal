"""Explicit reference routes preserving scientific status and qualifications."""
from .joint_audited import joint_effect
from .gaussian_effect_pivots import effect_confidence
from .chunked_learning import fit_chunked


def execute(route,inputs,options):
    if route=='persistent_calendar':result=joint_effect(**inputs,**options);unit='currency_per_signed_action'
    elif route=='finite_gaussian_effect':result=effect_confidence(**inputs,**options);unit='outcome_unit_per_action_unit'
    elif route=='fixed_dictionary_calendar':result=fit_chunked(**inputs,**options);unit='outcome_unit_per_treatment_unit'
    elif route=='audited_nonlinear_policy':
        from .nonlinear_variance import fit
        result=fit(**inputs,**options);unit='currency_per_complete_policy_trajectory'
    else:raise ValueError('unsupported reliability route')
    if result['status'].startswith('computed') and (not result.get('inference') or result['inference'].get('confidence_level')!=.95):
        raise ValueError('computed result must retain its explicit confidence qualifications')
    return dict(route=route,status=result['status'],unit=unit,result=result,
                acceptance='selected reference execution only; supplied scientific premises and external bank/interface acceptance not established')

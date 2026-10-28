"""Public synthetic contract fixtures; no third-party source or bank data."""
from dataclasses import dataclass
from fractions import Fraction
import json
from attention_delegate_reference_20261028 import calculate as temporal_and_tie


def json_safe(value):
    if isinstance(value, Fraction): return str(value)
    if isinstance(value, dict): return {k:json_safe(v) for k,v in value.items()}
    if isinstance(value, (list,tuple)): return [json_safe(v) for v in value]
    return value


@dataclass(frozen=True)
class GraphCase:
    case_id: str
    truth: frozenset
    split: str


def valid_mean(values, minimum):
    requested=len(values);finite=[v for v in values if v is not None]
    if len(finite)<minimum:return dict(status='unavailable',requested=requested,valid=len(finite),value=None)
    return dict(status='available',requested=requested,valid=len(finite),value=sum(finite)/len(finite))


def choose_threshold(cases, validation_truth, candidate_scores):
    if not cases or any(c.split!='validation' for c in cases):
        raise ValueError('Selector accepts validation cases only')
    ids={c.case_id for c in cases}
    if ids!=set(validation_truth):
        raise ValueError('Validation truth identity mismatch')
    # candidate_scores map a declared threshold to precomputed validation predictions.
    return max(candidate_scores,key=lambda t:sum(
        2*len(pred & validation_truth[c.case_id]) /
        max(1,2*len(pred & validation_truth[c.case_id])+
            len(pred-validation_truth[c.case_id])+len(validation_truth[c.case_id]-pred))
        for c,pred in zip(cases,candidate_scores[t],strict=True)))


def evaluate(cases, chosen_threshold, heldout_truth, predictions):
    ids={c.case_id for c in cases if c.split=='evaluation'}
    if ids & {c.case_id for c in cases if c.split=='validation'}:raise ValueError('overlapping graph instances')
    if ids!=set(heldout_truth):raise ValueError('held-out truth identity mismatch')
    return {i:dict(chosen_threshold=chosen_threshold,
                   correct=predictions[i]==heldout_truth[i]) for i in sorted(ids)}


def run():
    fixture=temporal_and_tie()
    cases=[GraphCase('train-1',frozenset({('a','b')}),'training'),
           GraphCase('validation-1',frozenset({('a','b')}),'validation'),
           GraphCase('evaluation-1',frozenset({('b','a')}),'evaluation')]
    # Threshold selection sees validation labels only; evaluation labels are passed later.
    valid=[c for c in cases if c.split=='validation']
    threshold=choose_threshold(valid,{c.case_id:c.truth for c in valid},
        {Fraction(1,2):[frozenset({('a','b')})],Fraction(3,4):[frozenset()]})
    result=evaluate(cases,threshold,{'evaluation-1':frozenset({('b','a')})},
                    {'evaluation-1':frozenset({('b','a')})})
    unavailable=valid_mean([None,None],minimum=1)
    available=valid_mean([Fraction(1,2),None],minimum=1)
    assert threshold==Fraction(1,2) and result['evaluation-1']['correct']
    assert unavailable==dict(status='unavailable',requested=2,valid=0,value=None)
    assert available['status']=='available' and available['valid']==1
    overlap=False
    try:evaluate([cases[1],GraphCase('validation-1',frozenset(),'evaluation')],
                 threshold,{'validation-1':frozenset()},{'validation-1':frozenset()})
    except ValueError:overlap=True
    assert overlap and fixture['temporal']['shifted_target_lags']==list(range(1,9))
    assert fixture['threshold']['inclusive_f1']=='1' and fixture['threshold']['strict_f1']=='0'
    output_available=dict(status=available['status'],requested=available['requested'],
                          valid=available['valid'],value=str(available['value']))
    return dict(status='pass',evidence_type='authored public synthetic contract fixture',
        fixtures=dict(validation_only_threshold_selection=True,disjoint_graph_instance_ids=True,
                      heldout_truth_bound_after_selection=True,empty_valid_denominator='unavailable',
                      partial_valid_denominator=dict(requested=2,valid=1),temporal_support_and_threshold_tie=True),
        output=dict(threshold=str(threshold),evaluation=result,unavailable=unavailable,
                    partial=output_available,exact_source_free_witness=fixture),
        limitations='Tests proposal-owned contract functions and selected algebraic expectations only; no downloaded model, native package, empirical performance, statistical calibration or bank data.')


if __name__=='__main__':print(json.dumps(json_safe(run()),indent=2))

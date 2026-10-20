#!/usr/bin/env python3
"""Authored exact references; never imports or executes upstream Java software."""
from fractions import Fraction as F
import json


def mean(xs):
    return sum(xs, F(0)) / len(xs)


def serial(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {k: serial(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [serial(v) for v in value]
    return value


def calculate():
    # An imposed population: X is equally likely low/high; Y(1)=Y(0) in law.
    # Treatment probabilities .2/.8 and response probabilities .2/.8 give
    # confounding if X is omitted. No software fitted this example.
    e = [F(1, 5), F(4, 5)]
    m = [F(1, 5), F(4, 5)]
    pz = mean(e)
    treated = mean([a*b for a, b in zip(e, m)]) / pz
    control = mean([(1-a)*b for a, b in zip(e, m)]) / (1-pz)
    contrast = treated-control
    assert (treated, control, contrast) == (F(17,25), F(8,25), F(9,25))

    tp, cp = F(8+1, 10+2), F(2+1, 10+2)
    smooth = tp-cp
    assert smooth == F(1,2)
    scores = [F(i,10) for i in range(1,5)]
    averages = dict(all=mean(scores), treated=mean(scores[:2]), control=mean(scores[2:]))
    assert list(averages.values()) == [F(1,4), F(3,20), F(7,20)]

    # Four ordered bins, each one treated and one control observation.
    # These are fixed observed labels, not a claim about their potential outcomes.
    observed = [(1,0), (0,0), (1,1), (0,1)]
    yt = yc = 0
    curve=[]
    for n,(t,c) in enumerate(observed,1):
        yt += t
        yc += c
        lift=F(yt,n)-F(yc,n)
        curve.append(dict(n_treated=n,n_control=n,lift=lift,
                          qini=F(yt)-F(yc*n,n), gain=2*n*lift))
    area=sum((row['qini']*2 for row in curve),F(0))/9
    assert area == F(2,3)
    original=list(reversed(scores))
    rescaled=[2*x for x in original]
    assert sorted(range(4),key=lambda i: original[i],reverse=True)==sorted(
        range(4),key=lambda i: rescaled[i],reverse=True)

    # Exact evaluation of two explicitly stated formulas at p=q=1/2.
    # log2(1)=0; log2(1/2)=-1. This is not Java execution.
    documented_kl = F(1,2)*0 + F(1,2)*0
    literal_source_node = F(1,2)*(-1) + F(1,2)*(-1)
    assert (documented_kl,literal_source_node)==(0,-1)
    slopes=[F(-2),F(-1,2)]
    abs_min=min(abs(x) for x in slopes)
    assert abs_min==F(1,2) and abs(min(slopes))==2
    ties=[F(1,2)]*3
    cutoff=sorted(ties,reverse=True)[0]
    selected=sum(x>=cutoff for x in ties)
    assert selected==3
    # Singular regression: beta_X + beta_Z = 1 has multiple solutions.
    solutions=[(F(0),F(1)),(F(1),F(0)),(F(-1),F(2))]
    assert all(x+z==1 for x,z in solutions)
    return serial(dict(
        scope='Authored finite-population and arithmetic references, not native behavior or bank evidence',
        confounding=dict(p_treated=pz,treated_mean=treated,control_mean=control,
            observed_difference=contrast,true_causal_effect=F(0),assumed_value=100,assumed_cost=20,
            naive_margin=100*contrast-20,true_margin=-20),
        smoothing=dict(treatment_probability=tp,control_probability=cp,smoothed_difference=smooth,
            raw_difference=F(3,5),smoothed_margin=100*smooth-40,raw_margin=F(20),
            unsupported_control_probability=F(1,2),unsupported_smoothed_difference=tp-F(1,2),
            zero_control_status='unidentified_without_additional_information'),
        prediction_averages=averages,
        after_missing_last_outcome=dict(all=mean(scores[:3]),treated=mean(scores[:2]),control=scores[2]),
        ranking=dict(bins=curve,qini_area_source_rectangle_convention=area,
            original_mean=mean(original),rescaled_mean=mean(rescaled),
            identical_order=True,causal_calibration_claim=False),
        kl_reconciliation=dict(p=F(1,2),q=F(1,2),documented_node=F(documented_kl),
            literal_source_node=literal_source_node,native_execution=False),
        graph_magnitudes=dict(signed_candidates=slopes,minimum_absolute=abs_min,
            absolute_of_signed_minimum=abs(min(slopes)),signed_margins=[100*x-20 for x in slopes],
            invalid_magnitude_as_benefit=100*abs_min-20),
        ranking_ties=dict(nominal_top_bracket=1,selected_at_inclusive_cutoff=selected,
            repeated_identical_subsamples_selection_frequency=F(1),
            error_control_established=False),
        singular_regression=dict(determinant=0,coefficient_solutions=solutions,
            status='zero_is_one_solution_not_identified_effect')) )


if __name__ == '__main__':
    print(json.dumps(calculate(),indent=2))

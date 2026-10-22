#!/usr/bin/env python3
"""Exact authored graph, observational-equivalence and displayed-score examples."""
from decimal import Decimal as D
from fractions import Fraction as F
import json


def calculate():
    truth = {('A', 'M'), ('M', 'Y')}
    union = truth | {('Y', 'A')}
    tp, fp, fn = len(truth & union), len(union - truth), len(truth - union)
    beta = -F(1, 2)
    causal_cov = [[F(1), beta], [beta, beta**2 + F(3, 4)]]
    confounded_cov = [[F(1, 2)+F(1, 2), -F(1, 2)],
                      [-F(1, 2), F(1, 2)+F(1, 2)]]
    assert causal_cov == confounded_cov
    assert F(2*tp, 2*tp+fp+fn) == F(4, 5)
    assert all((b, a) not in union for a, b in union)
    assert {('A','M'), ('M','Y'), ('Y','A')} <= union
    completeness = [6,5,6,6,5,5,6,5,5,6,6,6,5,5,5]
    assert len(completeness) == 15 and completeness.count(6) == 7
    return dict(
        evidence_kind='Exact project derivations and arithmetic, not empirical replication',
        displayed_scores=dict(
            augmented_kg_vs_proto=str(D('.745')-D('.396')),
            augmented_kg_vs_rag=str(D('.745')-D('.714')),
            augmentation_over_kg=str(D('.745')-D('.737')),
            before_direction_kg_minus_llm=str(D('.602')-D('.627')),
            after_direction_kg_minus_llm=str(D('.737')-D('.636')),
            augmented_rag_association_minus_kg=str(D('.627')-D('.567')),
            augmented_rag_temporality_minus_kg=str(D('.564')-D('.434')),
            literal_llm_delta=str(D('.636')-D('.396')),
            reported_llm_delta='.241; underlying unrounded scores not recovered'),
        ascvd=dict(runs=15,acyclic=14,six_of_seven=7,
            six_of_seven_fraction=str(F(7,15)),race_inclusions=0,
            o1_run3_source_denominators=[9,6],
            interpretation='7/15 contradicts abstract more-than-half wording; nine versus six sources needs raw outputs'),
        graph=dict(truth=sorted(truth),union=sorted(union),perfect_reference_f1='1',
            union_f1=str(F(2*tp,2*tp+fp+fn)),reciprocal_pairs=0,directed_three_cycle=True,
            ancestral_pairs=[['A','M'],['M','Y'],['A','Y']],
            direct_edges=sorted(truth),ancestral_is_not_direct=True),
        gaussian=dict(mean=[0,0],covariance=[[str(v) for v in r] for r in causal_cov],
            causal_effect=str(beta),latent_effect='0',observational_laws_equal=True,
            assumptions='Independent centered Gaussian exogenous terms; stated variances; do(A) replaces assignment',
            loss_unit_usd=100,incremental_action_cost_usd=20,
            causal_margin_usd=str(-100*beta-20),latent_margin_usd='-20',
            robust_margin_range_usd=['-20','30'],
            subjective_two_model_threshold=str(F(20,50)),
            probability_warning='A subjective model weight is not a calibrated LLM score or identified probability'))


if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2))

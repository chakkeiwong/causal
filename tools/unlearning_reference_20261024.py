#!/usr/bin/env python3
"""Project-owned exact examples; imports and executes no K-Bench code."""
from fractions import Fraction as F
from itertools import product
from hashlib import sha256
import json


def calculate():
    states = [(s, r, r, s ^ r) for s, r in product([0, 1], repeat=2)]
    for channel in [2, 3]:
        for observed in [0, 1]:
            selected = [s for s in states if s[channel] == observed]
            assert sum(s[0] for s in selected) == len(selected) // 2
    assert all(s == (a ^ b) for s, _, a, b in states)
    target = 'alpha beta'
    channels = ['alpha', 'beta']
    assert all(target not in c for c in channels)
    assert target == ' '.join(channels)
    per_channel = [F(len(set(target.split()) & set(c.split())), 2) for c in channels]
    delta = F(1, 5) - F(4, 5)
    assert delta < F(1, 20) and not abs(delta) < F(1, 20)
    queried_detects = 'alpha' in 'gamma'
    corpus_detects = any(v in 'gamma' for v in ['alpha', 'gamma'])
    scalar = (1 - F(0)) * (1 - abs(F(0))) * (1 - (F(1) - F(1, 2)))
    assert not queried_detects and corpus_detects and scalar == F(1, 2)
    assert sha256(b'abcd').digest() != sha256(b'wxyz').digest()
    return {
        'fragment_witness': {'binary_each': [0, 0], 'binary_or': 0,
            'graded_max': str(max(per_channel)), 'joint_complete': 1},
        'xor_information': {'individual_entropy_bits': [1, 1],
            'conditional_secret_entropy_each_bits': [1, 1],
            'joint_conditional_secret_entropy_bits': 0,
            'stipulated_loss_wrong_action_usd': 200,
            'single_channel_expected_loss_usd': 100,
            'joint_expected_loss_usd': 0},
        'third_party_witness': {'queried_value': 'alpha', 'other_forget_value': 'gamma',
            'observed': 'gamma', 'queried_only_detects': queried_detects, 'forget_corpus_detects': corpus_detects},
        'retention_sign': {'delta': str(delta), 'tolerance': '1/20',
            'signed_inequality_passes': True, 'absolute_inequality_passes': False},
        'definition_witness': {'baseline': '3/5', 'method': '2/5',
            'stipulated_adjusted_p': '1/100', 'reduction_factor': str(F(3, 5) / F(2, 5)),
            'paper_twofold_requirement_met': False,
            'static_public_classifier_branch': 'K-REF 1.50x',
            'native_execution': False},
        'conditional_denominator': {'requests': 4, 'answer_observed': 2, 'answer_leaks': 1,
            'conditional_rate': '1/2', 'all_query_rate': '1/4'},
        'cluster_witness': {'independent_entities': 200, 'identical_repeats_per_entity': 3,
            'bernoulli_probability': '1/2', 'true_mean_variance': str(F(1, 4 * 200)),
            'incorrect_iid_variance': str(F(1, 4 * 600)), 'variance_ratio': 3},
        'collapse_witness': {'baseline_degeneration': '1/2', 'method_degeneration': 1,
            'forget_severity': 0, 'retain_shift': 0, 'scalar_score': str(scalar),
            'terminal_gate_fails': True},
        'custody_witness': {'same_config_names_sizes': True,
            'payload_sizes': [4, 4], 'payload_sha256': [sha256(x).hexdigest() for x in [b'abcd', b'wxyz']],
            'bytes_equal': False},
        'interpretation': 'Authored finite laws and static-contract implications; no native benchmark, bank result, price or compliance claim.'
    }


if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2))

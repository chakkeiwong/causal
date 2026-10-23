#!/usr/bin/env python3
"""Project-authored finite-law witnesses; no Pandera or upstream code executed."""
from fractions import Fraction as F
from itertools import product
from math import comb


def calculate():
    # Uniform sampling without replacement, unique observation identities.
    miss = F(comb(98, 10), comb(100, 10))
    assert miss == F(89, 110)
    selected = [(a, u) for a, u in product([0, 1], repeat=2) if a == u]
    mean = lambda xs: sum(xs, F(0)) / len(xs)
    contrast = mean([u for a, u in selected if a == 1]) - mean(
        [u for a, u in selected if a == 0])
    assert contrast == 1
    # Same observed law, two incompatible intervention laws.
    observed_effect_world = [(u, u) for u in [0, 1]]
    observed_confounding_world = [(u, u) for u in [0, 1]]
    assert observed_effect_world == observed_confounding_world
    rows = [(7, 10), (7, -1), (9, 20)]
    seen = set(); abstract_head = []
    for label, value in rows[:2]:
        if label not in seen:
            abstract_head.append([label, value]); seen.add(label)
    abstract_drop = [[label, value] for label, value in rows if label != 7]
    assert abstract_head == [[7, 10]] and abstract_drop == [[9, 20]]
    clocks = dict(event=1, decision=2, available=3)
    assert clocks['event'] <= clocks['decision'] < clocks['available']
    raw_keys = ['0012', '12']; coerced = [int(x) for x in raw_keys]
    assert len(set(raw_keys)) == 2 and len(set(coerced)) == 1
    return {
        'provenance': 'Authored exact arithmetic and abstract transformations; not native Pandera tests',
        'sampling': {'population': 100, 'bad_rows': 2, 'sample': 10,
                     'miss_probability': str(miss), 'miss_decimal': float(miss),
                     'assumption': 'Uniform sampling without replacement and unique row identities'},
        'selection': {'full_causal_effect': 0, 'retained_fraction': '1/2',
                      'retained_observational_contrast': str(contrast),
                      'law': 'A and U independent fair bits; Y(a)=U; retain if A=U'},
        'nonidentification': {'observed_law': [[0, 0], [1, 1]],
                              'equal_probabilities': ['1/2', '1/2'],
                              'world1': 'A=U;Y=A', 'world2': 'A=U;Y=U',
                              'causal_effects': [1, 0]},
        'index_label_witness': {'input': [list(x) for x in rows],
                                'head_then_index_dedup': abstract_head,
                                'drop_failure_label_7': abstract_drop,
                                'interpretation': 'Abstract label operations, no observed upstream result'},
        'clock': dict(clocks, event_clock_pass=True, availability_clock_pass=False),
        'key_conversion': {'raw': raw_keys, 'integer': coerced,
                           'distinct_before': 2, 'distinct_after': 1},
        'cost': {'attempts': 12, 'stipulated_usd': 48, 'process_success': 8,
                 'accepted_artifacts': 3, 'correct_refusals': 4,
                 'usd_per_attempt': '4', 'usd_per_process_success': '6',
                 'usd_per_accepted_artifact': '16', 'observed_prices': False},
    }


if __name__ == '__main__':
    import json
    print(json.dumps(calculate(), indent=2))

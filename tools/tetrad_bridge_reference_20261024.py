#!/usr/bin/env python3
"""Authored finite bridge witnesses; never import or execute acquired software."""
from fractions import Fraction as F
import json

def calculate():
    # Row-source adjacency and endpoint matrices are different data types.
    stated_binary = [[0, 0], [1, 0]]
    comment_edges = [[j, i] for i in range(2) for j in range(2) if stated_binary[i][j]]
    loop_edges = [[i, j] for i in range(2) for j in range(2) if stated_binary[i][j]]
    endpoint = [[0, 2], [3, 0]]
    truthy_edges = [[i, j] for i in range(2) for j in range(2) if endpoint[i][j]]
    assert comment_edges == [[0, 1]] and loop_edges == [[1, 0]]
    assert truthy_edges == [[0, 1], [1, 0]]
    # Independent first-occurrence encodings cannot be assumed equal across datasets.
    a = {v: i for i, v in enumerate(dict.fromkeys(['approve', 'decline']))}
    b = {v: i for i, v in enumerate(dict.fromkeys(['decline', 'approve']))}
    assert a['approve'] != b['approve'] and str(1) == str('1')
    # Two positive definite Gaussian SEMs have the same observed covariance.
    beta = F(1, 2); noise = 1-beta**2
    covariance_forward = [[F(1), beta], [beta, beta**2+noise]]
    covariance_reverse = [[beta**2+noise, beta], [beta, F(1)]]
    assert covariance_forward == covariance_reverse
    benefit = 200 * 100 * beta
    assert benefit == 10000
    # The program's state contract is an independent model, not a native failure test.
    state = dict(request='old', graph='old_graph')
    try:
        candidate = (_ for _ in ()).throw(ValueError('authored failed search'))
        state['graph'] = candidate
    except ValueError:
        pass
    assert state['graph'] == 'old_graph'
    return dict(native_execution=False,
        adjacency=dict(matrix=stated_binary,comment_edges=comment_edges,source_loop_edges=loop_edges),
        endpoint=dict(matrix=endpoint,typed_edge=[0,1,'TAIL','ARROW'],truthy_loop_edges=truthy_edges),
        categories=dict(first=a,second=b,string_collision=[str(1),str('1')],
                        none_label=str(None)),
        observational_equivalence=dict(covariance=[[str(x) for x in row] for row in covariance_forward],
            noise_variance=str(noise),forward_effect=str(beta),reverse_effect='0',
            accounts=200,usd_per_outcome_unit=100,action_change=1,cost_usd=4000,
            forward_net_usd=str(benefit-4000),reverse_net_usd='-4000'),
        failed_assignment=dict(prior_graph_survives=True,scope='Authored assignment semantics, not native invocation'),
        costs=dict(total_usd=6000,submitted=300,completed=240,qualified=200,
                   usd_per_denominator=[str(F(6000,n)) for n in [300,240,200]]))

if __name__ == '__main__':
    print(json.dumps(calculate(),indent=2))

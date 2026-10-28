"""Independent finite logical witnesses; no imported or executed Java code."""
from fractions import Fraction


def calculate():
    # The inspected endpoint constants are circle=0, line=1, arrow=2.
    r3 = [dict(endpoint=symbol, outer=symbol == 2, inner=symbol == 0,
               conjunction=symbol == 2 and symbol == 0) for symbol in range(3)]
    assert not any(row['conjunction'] for row in r3)
    votes = [dict(separating_sets=n, containing_middle=k,
                  stable_orients=k <= n // 2, strict_minority_orients=2 * k < n,
                  conservative_orients=k == 0)
             for n in range(1, 7) for k in range(n + 1)]
    differences = [row for row in votes
                   if row['stable_orients'] != row['strict_minority_orients']]
    assert [(row['separating_sets'], row['containing_middle'])
            for row in differences] == [(2, 1), (4, 2), (6, 3)]
    witness = dict(separating_sets=[[], ['middle']], containing_middle=1,
                   stable_orients=True, conservative_orients=False,
                   first_set_orients=True, reversed_first_set_orients=False)
    # A source comment naming a p-value does not change this literal comparison.
    assert not Fraction(1, 5) < Fraction(1, 10)
    return dict(
        kind='authored_exact_logical_witnesses', native_execution=False,
        r3_endpoint_truth_table=r3, stable_vote_truth_table=votes,
        stable_vs_strict_minority_differences=differences,
        two_set_orientation_witness=witness,
        bundled_vstructure_literal=dict(p_value='1/5', cutoff='1/10', returns=False,
                                        condition='Execution reaches the literal comparison'),
        limits=['The truth table assumes unchanged reads of the inspected graph state.',
                'These calculations do not run Java, prove general graph correctness, '
                'or validate the linguistic flow oracle on banking data.'])


if __name__ == '__main__':
    import json
    print(json.dumps(calculate(), indent=2))

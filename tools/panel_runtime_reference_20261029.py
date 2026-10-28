"""Conditional source-composition witnesses, separate from package execution."""
from fractions import Fraction as F
import json


def calculate():
    # Ideal uniform positive b-bit integer; zero is excluded.
    for bits in range(2,9):
        draws=[[(value >> j & 1)*2-1 for j in range(bits)] for value in range(1,2**bits)]
        denominator=2**bits-1
        assert sum(F(row[0]) for row in draws)/denominator==F(1,denominator)
        assert sum(F(row[0]*row[1]) for row in draws)/denominator==F(-1,denominator)
    denominator=2**31-1
    mean=F(1,denominator)
    cross=F(-1,denominator)
    covariance=cross-mean**2
    # R=diag(2,1) in pivot order (b,a); original order is (a,b).
    pivot_variance=[F(1,4),F(1)]
    aligned_variance=list(reversed(pivot_variance))
    score=[F(1),F(0)]
    unaligned=sum(s*s*v for s,v in zip(score,pivot_variance))
    aligned=sum(s*s*v for s,v in zip(score,aligned_variance))
    assert (unaligned,aligned)==(F(1,4),F(1))
    return dict(packed_bits=dict(bits=31,positive_integer_count=denominator,
             ideal_uniform_mean=str(mean),ideal_uniform_cross_moment=str(cross),
             ideal_uniform_pair_covariance=str(covariance),all_negative_block_probability='0',
             iid_symmetric_all_negative_probability=str(F(1,2**31)),
             exhaustive_small_bit_checks=list(range(2,9))),
             covariance_order=dict(original_columns=['a','b'],pivot=[2,1],R_diagonal=[2,1],
             pivot_order_covariance_diagonal=list(map(str,pivot_variance)),
             original_order_covariance_diagonal=list(map(str,aligned_variance)),
             original_order_score=list(map(str,score)),unaligned_quadratic=str(unaligned),aligned_quadratic=str(aligned)),
             limits=['Uniform integers are an idealized conditional law, not verification of finite-state RNG output.',
                     'Nontrivial full-rank pivot is a constructed condition; default LINPACK reachability is not established.',
                     'Exact arithmetic is independent project work, not execution of downloaded packages.'])


if __name__=='__main__':print(json.dumps(calculate(),indent=2))

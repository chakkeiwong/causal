"""Independent boundary witnesses; never imports or executes acquired R/C++ code."""
from fractions import Fraction as F
from itertools import product
from statistics import NormalDist
import json


def cluster_laws(groups):
    n, g = sum(map(len, groups)), len(groups)
    unit = [sum(map(F, x)) / n for x in groups]
    equal = [sum(map(F, x)) / len(x) / g for x in groups]
    def law(coefficients):
        draws = [sum(c * s for c, s in zip(coefficients, signs))
                 for signs in product((-1, 1), repeat=g)]
        mean = sum(draws) / len(draws)
        return dict(coefficients=list(map(str, coefficients)),
                    draws=list(map(str, draws)), mean=str(mean),
                    variance=str(sum((x-mean)**2 for x in draws)/len(draws)))
    return dict(unit_average=law(unit), mean_of_cluster_means=law(equal))


def interval(estimate, se, low, high, level=.95):
    # A limited transcription of the inspected constructor's selected branch.
    if (low is None or high is None) and se is not None:
        z = NormalDist().inv_cdf((1 + level) / 2)
        return [estimate-z*se, estimate+z*se]
    return [low, high]


def calculate():
    unequal = cluster_laws([[3], [-1, -1, -1]])
    equal = cluster_laws([[3, 1], [-1, -3]])
    partial = interval(10, 2, 9, None)
    assert unequal['unit_average']['variance'] == '9/8'
    assert unequal['mean_of_cluster_means']['variance'] == '5/2'
    assert equal['unit_average'] == equal['mean_of_cluster_means']
    assert cluster_laws([[-1, -1, -1], [3]])['unit_average']['variance'] == '9/8'
    assert partial[0] < 9 and abs(partial[1]-13.919927969080108) < 1e-12
    assert interval(10, 2, 9, 12) == [9, 12]
    assert interval(10, None, 9, None) == [9, None]
    assert interval(10, -2, None, None)[0] > interval(10, -2, None, None)[1]
    clock = dict(input_time='-1/2', displayed_time=int(F(-1, 2)),
                 window='pre' if F(-1, 2) < 0 else 'post')
    assert clock == dict(input_time='-1/2', displayed_time=0, window='pre')
    return dict(unequal_clusters=unequal, equal_clusters=equal,
                partial_interval=dict(input=[9, None], estimate=10, se=2,
                                      normal_level=.95, derived=partial),
                complete_interval=interval(10, 2, 9, 12),
                fractional_clock=clock,
                heterogeneous_labels=dict(input_method=['A','B'], output_method=['A','A'],
                                          input_outcome=['arrears','loss'], output_outcome=['arrears','arrears']),
                assumptions=['Independent symmetric signs are an authored reference law, not a claim about the packed native RNG.',
                             'Unit-average influence is the declared target; equal-cluster targets are different estimands.',
                             'Normal quantile is numerical; cluster fractions are exact.'],
                native_execution=False, empirical_coverage=False)


if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2))

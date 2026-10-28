"""Independent exact witnesses for inspected source contracts; no R execution."""
from fractions import Fraction as F
import json


def calculate():
    equal = [F(1), F(1)]
    unequal = [F(1), F(2)]
    ess = lambda weights: sum(weights) ** 2 / sum(w * w for w in weights)
    assert ess(equal) == 2 and ess(unequal) == F(9, 5)
    cap = 1 - F(1, 10 ** 10)
    assert cap / (1 - cap) == 9999999999
    native = [-1, 0, 1, 2]
    shifted = [t - 1 for t in native]
    assert shifted == [-2, -1, 0, 1]
    # For two distinct names that share their first 32 characters, selected
    # truncation then make.unique appends a suffix after the length cap.
    prefix = 'a' * 32
    renamed = []
    for name in [x[:32] for x in [prefix + 'x', prefix + 'y']]:
        candidate, suffix = name, 1
        while candidate in renamed:
            candidate = name + '_' + str(suffix)
            suffix += 1
        renamed.append(candidate)
    assert [len(x) for x in renamed] == [32, 34]
    effects, placebo = F(29, 10), F(19, 10)
    leads, lags = int(effects) - 1, int(placebo)
    assert leads == lags == 1
    return dict(
        kish=dict(equal_two=str(ess(equal)), unequal_two=str(ess(unequal)),
                  unequal_two_rejected_by_selected_less_than_two_rule=True,
                  equal_two_residual_inflation_squared='2'),
        propensity=dict(cap=str(cap), control_odds_at_cap=str(cap / (1-cap))),
        alias=dict(input_effects=str(effects), coerced_effects=int(effects), leads=leads,
                   input_placebo=str(placebo), lags=lags),
        dcdh_time=dict(native=native, displayed=shifted),
        stata_names=dict(original=[prefix+'x',prefix+'y'], selected=renamed,
                         lengths=[len(x) for x in renamed]),
        native_execution=False, empirical_coverage=False,
        scope='Exact arithmetic and selected-branch transcription; no native R, haven, Stata or statistical qualification.')


if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2))

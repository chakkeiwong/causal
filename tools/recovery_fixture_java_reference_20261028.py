"""Exact authored reference for the stronger fixture and Java comparison."""
from fractions import Fraction

import aitiotita_delegate_reference_20261028 as java
import public_attention_contract_v2_20261028 as fixture


def calculate():
    example = fixture.json_safe(fixture.example())
    assert example['evaluation']['macro_f1']['availability'] == '1/2'
    assert example['evaluation']['macro_f1']['value'] == '1'
    # F1 lies in [0,1]. Retain failed requests rather than silently deleting them.
    requested, valid, known_total = 2, 1, Fraction(1)
    lower = known_total / requested
    upper = (known_total + requested - valid) / requested
    assert (lower, upper) == (Fraction(1, 2), Fraction(1))
    return dict(fixture=example, java=java.calculate(),
                full_request_score_bounds=dict(requested=requested, valid=valid,
                    known_sum=str(known_total), lower=str(lower), upper=str(upper),
                    assumption='Each unavailable requested F1 is somewhere in [0,1].',
                    interpretation='Accounting bound, not a confidence interval or native measurement.'),
                native_execution=False, empirical_calibration=False)


if __name__ == '__main__':
    import json
    print(json.dumps(calculate(), indent=2))

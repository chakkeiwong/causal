"""Exact, authored scale and row-alignment witnesses; no upstream execution."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/release/2026-10-29/source-flexbcf-016/exact-witnesses.json'


def reconstruct():
    # Twenty equally weighted customers avoid using an unsupported singleton.
    raw = [F(1, 5)] * 10 + [F(2, 5)] * 10
    scale, outcome_mean, cost = F(10), F(100), F(5)
    correct = scale * sum(raw) / len(raw)
    wrong = correct + outcome_mean
    assert (correct, wrong, correct - cost, wrong - cost) == (3, 103, -2, 98)
    # Translating every outcome changes its mean, not its centered standardized data.
    shift = F(37)
    shifted_wrong = correct + outcome_mean + shift
    assert shifted_wrong - wrong == shift
    # A joint permutation must be applied before the treated-only design is made.
    ids = ['a', 'b', 'c', 'd']
    treatment = [1, 0, 1, 0]
    order = sorted(range(4), key=lambda i: treatment[i])
    control_first = [ids[i] for i in order]
    treatment_design = [ids[i] for i in order if treatment[i] == 1]
    assert control_first == ['b', 'd', 'a', 'c']
    assert treatment_design == control_first[2:] == ['a', 'c']
    return {
        'scope': 'Stipulated rational arithmetic and identity alignment, not an R/C++ run, posterior calibration or observed bank value.',
        'scale': {'customers': len(raw), 'raw_draw': list(map(str, raw)),
                  'outcome_mean': str(outcome_mean), 'outcome_sd': str(scale),
                  'cost': str(cost), 'correct_effect': str(correct),
                  'wrong_restoration': str(wrong), 'correct_margin': str(correct-cost),
                  'wrong_margin': str(wrong-cost), 'outcome_shift': str(shift),
                  'shifted_wrong_restoration': str(shifted_wrong)},
        'row_alignment': {'original_ids': ids, 'treatment': treatment,
                          'joint_order_zero_based': order, 'control_first_ids': control_first,
                          'treated_only_ids': treatment_design},
        'small_progress_defaults': {str(n): n // 10 for n in range(2, 10)},
        'status': 'pass'
    }


def main():
    assert not OUT.exists(), 'Frozen witness: do not overwrite'
    report = reconstruct()
    report['source_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    OUT.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': report['status'], 'output': str(OUT.relative_to(ROOT))}))


if __name__ == '__main__':
    main()

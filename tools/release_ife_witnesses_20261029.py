"""Exact authored uncertainty laws; does not execute downloaded R code."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/release/2026-10-29/source-ife-023'


def mean(xs):
    return sum(xs) / len(xs)


def variance_of_mean(xs):
    center = mean(xs)
    return sum((x-center)**2 for x in xs) / (len(xs)*(len(xs)-1))


def main():
    destination = OUT / 'exact-witnesses.json'
    assert not destination.exists(), 'Preserve existing witness; do not rerun.'
    z = list(map(F, [1, 2, 4, 5]))
    w = [F(1, 2), F(1, 2), F(3, 2), F(3, 2)]
    theta = mean([a*b for a, b in zip(z, w)])
    centered = [a*(b-theta) for a, b in zip(w, z)]
    raw = [a*b for a, b in zip(w, z)]
    shifted = [a*(b+100) for a, b in zip(w, z)]
    weighted = dict(pseudo_outcomes=list(map(str, z)), weights=list(map(str, w)),
                    ratio_estimate=str(theta), centered_influence=list(map(str, centered)),
                    centered_variance=str(variance_of_mean(centered)),
                    uncentered_variance=str(variance_of_mean(raw)),
                    shifted_uncentered_variance=str(variance_of_mean(shifted)),
                    centered_standard_error=math.sqrt(float(variance_of_mean(centered))),
                    uncentered_standard_error=math.sqrt(float(variance_of_mean(raw))),
                    shifted_uncentered_standard_error=math.sqrt(float(variance_of_mean(shifted))))
    assert theta == F(15, 4)
    assert variance_of_mean(centered) == F(101, 192)
    assert variance_of_mean(raw) == F(149, 48)
    assert variance_of_mean(shifted) == F(14983, 16)
    shifted_theta = theta + 100
    assert [a*(b+100-shifted_theta) for a, b in zip(w, z)] == centered
    constant_contrast = dict(known_increment='2', centered_influence=['0']*4,
                             centered_variance='0', uncentered_weighted_variance=str(variance_of_mean([2*a for a in w])))
    assert constant_contrast['uncentered_weighted_variance'] == '1/3'

    zc = list(map(F, [0, 0, 2, 2]))
    ids = ['A', 'B', 'B', 'B']
    def cluster_values(values):
        return [F(2, 4)*sum(x for x, label in zip(values, ids) if label == group) for group in ['A', 'B']]
    c = cluster_values([x-mean(zc) for x in zc])
    u = cluster_values(zc)
    shifted_c = cluster_values([x+100 for x in zc])
    assert (c, u, shifted_c) == ([F(-1, 2), F(1, 2)], [F(0), F(2)], [F(50), F(152)])
    cluster = dict(pseudo_outcomes=list(map(str, zc)), ids=ids, K=2, n=4,
                   centered_cluster_influence=list(map(str, c)), uncentered_cluster_values=list(map(str, u)),
                   shifted_uncentered_cluster_values=list(map(str, shifted_c)),
                   centered_variance=str(variance_of_mean(c)), uncentered_variance=str(variance_of_mean(u)),
                   shifted_uncentered_variance=str(variance_of_mean(shifted_c)),
                   scope='Two clusters expose an algebraic invariance defect; not a coverage-calibration experiment.')
    assert [cluster[x] for x in ['centered_variance', 'uncentered_variance', 'shifted_uncentered_variance']] == ['1/4', '1', '2601']
    a = list(map(F, [-2, -1, 1, 2]))
    row_alignment = dict(first_influence=list(map(str, a)), aligned_second=list(map(str, a)),
                         reversed_second=list(map(str, a[::-1])),
                         aligned_difference_variance='0',
                         reversed_difference_variance=str(variance_of_mean([x-y for x, y in zip(a, a[::-1])])),
                         independent_marginal_sum=str(2*variance_of_mean(a)))
    assert row_alignment['reversed_difference_variance'] == '10/3'

    ratio = 1.5
    log_se = .2
    critical = 1.959963984540054
    scales = dict(ratio=ratio, log_standard_error=log_se, ratio_delta_standard_error=ratio*log_se,
                  transformed_log_interval=[ratio*math.exp(s*critical*log_se) for s in [-1, 1]],
                  direct_ratio_wald_interval=[ratio+s*critical*ratio*log_se for s in [-1, 1]],
                  scope='Deterministic delta-method arithmetic; no confidence-coverage claim.')
    rows = json.loads((OUT/'authenticated-files.json').read_text()) + json.loads((OUT/'authenticated-caller-files.json').read_text())
    bindings = {row['local_path']: row['sha256'] for row in rows}
    for name in ['exec22_lmtp_eif.txt', 'exec22_lmtp_theta.txt', 'exec22_lmtp_task.txt']:
        p = ROOT/'docs/literature/raw'/name
        bindings[str(p.relative_to(ROOT))] = hashlib.sha256(p.read_bytes()).hexdigest()
    result = dict(status='pass', scope='Exact project constructions and source-formula traces. Sample variance uses divisor n-1; no execution of upstream code, empirical coverage or bank observations.',
                  weighted_location=weighted, constant_contrast=constant_contrast, unequal_clusters=cluster,
                  row_alignment=row_alignment, contrast_scales=scales, source_bindings=bindings)
    destination.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'source_bindings'}, indent=2))


if __name__ == '__main__':
    main()

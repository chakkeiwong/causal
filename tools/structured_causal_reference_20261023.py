#!/usr/bin/env python3
"""Independent finite witnesses; no external code or data is executed."""
from fractions import Fraction as F
from itertools import permutations


def calculate():
    group = set(permutations(range(3)))
    phi = (1, 0, 2)
    translated = {tuple(phi[g[i]] for i in range(3)) for g in group}
    assert translated == group and len(translated & group) == 6
    first_stage, variance, effect = F(-2), F(4), F(3)
    denominator = first_stage * variance
    numerator = effect * denominator
    assert denominator == -8 and numerator / denominator == effect
    sizes, contrasts, cost = [10, 90], [F(20), F(-4)], F(2)
    unit_net = sum(contrasts) / 2 - cost
    customer_net = sum(n*t for n,t in zip(sizes,contrasts)) / sum(sizes) - cost
    p = [F(1,4), F(3,4)]
    factors = [F(2), F(1)]
    changed = [p[i]*factors[i] for i in range(2)]
    z = sum(changed); changed = [x/z for x in changed]
    raw_contrast = sum(w*t for w,t in zip(p,contrasts))
    tilted_contrast = sum(w*t for w,t in zip(changed,contrasts))
    assert raw_contrast == 2 and tilted_contrast == F(28,5)
    return dict(kind='authored_exact_witnesses_and_reported_table_arithmetic',native_execution=False,
      group=dict(n=3,cardinality=len(group),translated_intersection=6,ratio='1',
                 claim='Left multiplication by a member permutes a finite subgroup; the intersection is the subgroup, not empty.'),
      iv=dict(first_stage=str(first_stage),instrument_variance=str(variance),denominator=str(denominator),
              numerator=str(numerator),ratio=str(numerator/denominator),
              claim='Instrument relevance requires a nonzero denominator, not a positive first-stage covariance.'),
      banking=dict(branch_sizes=sizes,stipulated_contrasts_usd=[str(x) for x in contrasts],cost_usd=str(cost),
                   equal_branch_net_usd=str(unit_net),customer_weighted_net_usd=str(customer_net)),
      reweighting=dict(original_weights=[str(x) for x in p],multipliers=[str(x) for x in factors],
                       renormalized_weights=[str(x) for x in changed],original_contrast_usd=str(raw_contrast),
                       reweighted_contrast_usd=str(tilted_contrast),
                       limit='A stipulated nonconstant factor change; not the paper implementation and not every kind of normalization.'),
      paper_arithmetic=dict(hscm_math=str(F('2402.75')-F('2365.95')),hscm_reading=str(F('1788.10')-F('1766.47')),
                            reported_cpu_speedup=str(F('3.11')/F('1.9')),
                            geometric_A_R_RC_minus_R=str(F('2.509')-F('1.637')),
                            geometric_B_S_RC_minus_R=str(F('0.084')-F('0.104'))),
      limitations=['No bank outcomes, statistical coverage, runtime or software reproduction is established.',
                  'Reported table arithmetic does not verify the underlying experiments.',
                  'Printed proof discrepancies do not by themselves refute the identification theorem.'])


if __name__ == '__main__':
    import json
    print(json.dumps(calculate(), indent=2))

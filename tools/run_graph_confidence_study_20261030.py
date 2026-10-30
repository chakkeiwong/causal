"""Project counterexamples; no external model calls or downloaded code execution."""
from pathlib import Path
import datetime
from fractions import Fraction as F
import hashlib
import itertools
import json
import math
import sys

import numpy as np
from scipy.optimize import brentq
from scipy.stats import t

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/twelve-hour-closure/2026-10-29/graph-confidence-attempt-1'


def kl(p, q):
    return ((p * math.log(p / q)) if p else 0.0) + (
        ((1 - p) * math.log((1 - p) / (1 - q))) if p < 1 else 0.0)


def max_success(delta, q):
    if delta >= -math.log(q):
        return 1.0
    lo, hi = q, 1.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if kl(mid, q) <= delta:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def main():
    assert not OUT.exists(), 'Preserve prior experimental evidence'
    OUT.mkdir(parents=True)
    q, delta = 0.1, 0.5
    pmax = max_success(delta, q)
    reference = brentq(lambda p: kl(p, q) - delta, q, 1 - 1e-14,
                       xtol=1e-14)
    assert abs(pmax - reference) < 1e-12

    # A={first two outcomes}; all priors are identical (no permutation issue).
    prior = np.array([.05, .05, .001, .899])
    target = np.array([.05, .05, .899, .001])
    full_delta = float(np.sum(target * np.log(target / prior)))
    assert abs(full_delta - .898 * math.log(899)) < 1e-12
    assert abs(target[:2].sum() - prior[:2].sum()) < 1e-14
    b2t = kl(.95, .1)

    # Only possible edges: A->B, B->C, C->A. All eight configurations.
    p = F(4, 5)
    states = []
    for bits in itertools.product([0, 1], repeat=3):
        weight = math.prod(p if b else 1-p for b in bits)
        states.append((bits, weight, not all(bits)))
    cycle_mass = sum(w for _, w, dag in states if not dag)
    acceptance = 1-cycle_mass
    retained_marginal = [sum(w for bits, w, dag in states if dag and bits[j]) /
                         acceptance for j in range(3)]
    assert cycle_mass == F(64, 125)
    assert all(x == F(36, 61) for x in retained_marginal)
    assert retained_marginal[0] == p*(1-p*p)/(1-p**3)
    # A DAG has at most two of these three oriented cycle edges.
    assert all(sum(bits) <= 2 for bits, _, dag in states if dag)

    # Both worlds have covariance [[1,.6],[.6,1]]. Their do(A) slopes differ.
    forward_B = np.array([[0., 0.], [.6, 0.]])
    reverse_B = np.array([[0., .6], [0., 0.]])
    forward_noise = np.diag([1., .64])
    reverse_noise = np.diag([.64, 1.])
    covariances = []
    for b, noise in [(forward_B, forward_noise), (reverse_B, reverse_noise)]:
        inv = np.linalg.inv(np.eye(2)-b)
        covariances.append(inv @ noise @ inv.T)
    assert np.max(np.abs(covariances[0]-covariances[1])) < 1e-14

    # One shared observational law; evaluate each interval against both effects.
    seed, repetitions, sample_size = 2026103004, 2000, 500
    rng = np.random.default_rng(seed)
    critical = float(t.ppf(.975, sample_size-2))
    rows = []
    qr_checks = []
    for i in range(repetitions):
        x = rng.standard_normal(sample_size)
        y = .6*x + .8*rng.standard_normal(sample_size)
        xc, yc = x-x.mean(), y-y.mean()
        slope = float(xc@yc/(xc@xc))
        residual = yc-slope*xc
        se = math.sqrt(float(residual@residual)/(sample_size-2)/float(xc@xc))
        lower, upper = slope-critical*se, slope+critical*se
        rows.append([i, slope, lower, upper, int(lower <= .6 <= upper),
                     int(lower <= 0 <= upper), 1, int(lower <= .6 <= upper)])
        if i in [0, 999, 1999]:
            design = np.column_stack([np.ones(sample_size), x])
            qmat, rmat = np.linalg.qr(design)
            beta = np.linalg.solve(rmat, qmat.T@y)
            invr = np.linalg.inv(rmat)
            e = y-design@beta
            qrse = math.sqrt(float(e@e)/(sample_size-2)*(invr@invr.T)[1,1])
            assert abs(beta[1]-slope) < 1e-12 and abs(qrse-se) < 1e-12
            qr_checks.append(dict(repetition=i, slope=float(beta[1]), se=qrse))
    a = np.array(rows)
    np.savetxt(OUT/'replications.csv', a, delimiter=',',
               header='replication,slope,lower,upper,forward_cover,reverse_cover,union_reverse_cover,union_forward_cover',
               comments='', fmt=['%d']+['%.17g']*3+['%d']*4)
    result = {
        'status': 'pass', 'scope': 'Project logical examples and Gaussian repeated-sample study; not a thesis reproduction or live LLM evaluation.',
        'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'bound': dict(q=q,delta=delta,pmax=pmax,independent_root=reference,
                      complement_lower_bound=1-pmax,admissible_success=q,
                      admissible_error=1-q),
        'minimum_budget_not_sufficient': dict(prior=prior.tolist(),target=target.tolist(),
                      success=.1,prior_event_mass=.1,full_kl=full_delta,
                      binary_kl=0.,target_success=.95,required_budget=b2t,
                      ratio=full_delta/b2t,pmax=max_success(full_delta,.1)),
        'binary_branch_ambiguity': dict(prior=.5,actual_success=.05,
                      target_success=.95,actual_kl=kl(.05,.5),
                      target_kl=kl(.95,.5),ratio=kl(.05,.5)/kl(.95,.5),
                      explanation='Without restricting achieved success to the increasing branch p>=q, a minimum-KL threshold cannot distinguish .05 from .95 at q=.5.'),
        'cycle': dict(edge_probability=str(p),cycle_mass=str(cycle_mass),
                      acceptance=str(acceptance),conditional_marginals=[str(x) for x in retained_marginal],
                      proposed_marginal_sum=str(3*p),maximum_dag_marginal_sum=2,
                      states=[dict(edges=bits,probability=str(w),dag=dag) for bits,w,dag in states]),
        'worlds': dict(observational_covariance=covariances[0].tolist(),
                      forward_effect=.6,reverse_effect=0.,
                      identical_model_interval_iou=1.,
                      warning='Identical fitted intervals give IoU1 by construction; this is not an empirical estimate of the thesis metric.'),
        'sampling': dict(seed=seed,repetitions=repetitions,n=sample_size,
                      critical=critical,coverage_forward=float(a[:,4].mean()),
                      coverage_reverse=float(a[:,5].mean()),
                      union_coverage_reverse=float(a[:,6].mean()),
                      union_coverage_forward=float(a[:,7].mean()),
                      mean_interval_width=float(np.mean(a[:,3]-a[:,2])),
                      coverage_mcse=math.sqrt(float(a[:,4].mean())*(1-float(a[:,4].mean()))/repetitions),
                      qr_checks=qr_checks),
        'files': {'runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  'replications_sha256':hashlib.sha256((OUT/'replications.csv').read_bytes()).hexdigest()},
        'limitations':['Known two-graph class with causal sufficiency and Gaussian linear equations.',
                       'No selected graph-class coverage guarantee is estimated here.',
                       'Intervals are ordinary exact Gaussian regression intervals; not neural-seed percentiles.',
                       'No native package, bank data or model calibration claim.']}
    (OUT/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','bound','minimum_budget_not_sufficient','sampling']},indent=2))


if __name__ == '__main__':
    main()

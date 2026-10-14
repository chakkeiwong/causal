#!/usr/bin/env python3
"""Reproduce A-G fitting/inference; final specification is hashed in the receipt."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import time

import numpy as np
from scipy.linalg import solve_discrete_lyapunov
from scipy.stats import norm
from threadpoolctl import threadpool_limits

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from causalbank.responses import (direct_response, proxy_var_response, moment_test_sets,
                                  set_contains, gaussian_max_critical)


def generate(case, horizon, rng):
    f = np.array([[.65, .02, 0], [.08, .80, 0], [-.05, .1, .55]])
    f *= case["spectral_radius"] / max(abs(np.linalg.eigvals(f)))
    b = np.array([[1., .3, .1], [.7, 1., .2], [-.4, .2, .9]])
    n = case["origins"] + horizon
    innovations = rng.normal(size=(n, 3))
    state = rng.multivariate_normal(np.zeros(3), solve_discrete_lyapunov(f, b @ b.T))
    x = np.empty((n, 3))
    v, noise = rng.normal(), rng.normal(size=n)
    z = np.empty(n)
    rho = case["instrument_persistence"]
    for t in range(n):
        state = f @ state + b @ innovations[t]
        x[t] = state
        v = rho*v + np.sqrt(1-rho*rho)*noise[t]
        z[t] = case["strength"]*innovations[t, 0] + v + case["invalid_loading"]*innovations[t, 1]
    truth = np.array([(np.linalg.matrix_power(f, h) @ b[:, 0])[j] / b[0, 0]
                      for j in (1, 2) for h in range(horizon+1)])
    return x, z, truth


def run(spec, repetitions):
    rows = []
    for index, case in enumerate(spec["cases"]):
        metrics = {name: [] for name in ("iid_pointwise", "hac_pointwise", "hac_bonferroni", "hac_gaussian_max", "weakiv_bonferroni", "proxy_var_bonferroni")}
        widths, errors, failures, unbounded = [], [], [], []
        start = time.perf_counter()
        for repetition in range(repetitions):
            rng = np.random.default_rng(np.random.SeedSequence([spec["seed"], index, repetition]))
            try:
                x, z, truth = generate(case, spec["horizon"], rng)
                fit = direct_response(x, z, spec["horizon"])
                proxy = proxy_var_response(x, z, spec["horizon"])
                error = np.abs(fit.estimate-truth)
                se = np.sqrt(np.diag(fit.covariance))
                iid_se = np.sqrt(np.diag(fit.iid_covariance))
                bonferroni = norm.ppf(1-spec["alpha"]/(2*len(truth)))
                normal = norm.ppf(1-spec["alpha"]/2)
                maximum = gaussian_max_critical(fit.covariance, rng, spec["gaussian_max_draws"], spec["alpha"])
                sets = moment_test_sets(fit.moment_mean, fit.moment_lrv, fit.origins, spec["alpha"])
                included = np.array([set_contains(s, t) for s, t in zip(sets, truth)])
                values = {
                    "iid_pointwise": error <= normal*iid_se,
                    "hac_pointwise": error <= normal*se,
                    "hac_bonferroni": error <= bonferroni*se,
                    "hac_gaussian_max": error <= maximum*se,
                    "weakiv_bonferroni": included,
                    "proxy_var_bonferroni": np.abs(proxy.estimate-truth) <= bonferroni*np.sqrt(np.diag(proxy.covariance)),
                }
                for name, value in values.items():
                    metrics[name].append([float(value.mean()), bool(value.all())])
                widths.append(float((2*bonferroni*se).mean()))
                errors.append([float(np.mean((fit.estimate-truth)**2)), float(np.mean((proxy.estimate-truth)**2))])
                unbounded.append(any(lo is None or hi is None for s in sets for lo, hi in s))
            except (ValueError, np.linalg.LinAlgError, FloatingPointError) as error:
                failures.append({"repetition": repetition, "error": str(error)})
                for name in metrics:
                    metrics[name].append([0.0, False])
        row = {"case": case, "requested": repetitions, "failures": failures,
               "seconds": time.perf_counter()-start, "metrics": {}}
        for name, values in metrics.items():
            v = np.asarray(values, dtype=float)
            coverage = float(v[:, 1].mean())
            row["metrics"][name] = {"mean_coordinate_coverage": float(v[:, 0].mean()),
                                     "whole_curve_coverage": coverage,
                                     "mc_se": float(np.sqrt(coverage*(1-coverage)/repetitions))}
        row["mean_bonferroni_width"] = float(np.mean(widths)) if widths else None
        row["mse_direct_proxy"] = np.mean(errors, axis=0).tolist() if errors else None
        row["unbounded_weakiv_fraction"] = float(np.sum(unbounded)/repetitions)
        rows.append(row)
        print(json.dumps({"case": case["id"], "seconds": row["seconds"], "failures": len(failures),
                          "curve_coverage": {k:v["whole_curve_coverage"] for k,v in row["metrics"].items()}}), flush=True)
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pilot", action="store_true")
    args = parser.parse_args()
    path = ROOT / "docs/studies/a-experiment-v1.json"
    spec = json.loads(path.read_text())
    repetitions = 20 if args.pilot else spec["repetitions"]
    with threadpool_limits(limits=1):
        rows = run(spec, repetitions)
    files = [path, Path(__file__), ROOT / "src/causalbank/responses.py"]
    receipt = {"mode": "pilot" if args.pilot else "final", "spec": spec,
               "input_sha256": {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
               "results": rows, "scope": "Synthetic stationary A-G experiment; no bank-data or universal coverage evidence."}
    destination = ROOT / "docs/studies" / ("a-pilot.json" if args.pilot else "a-results.json")
    destination.write_text(json.dumps(receipt, indent=2)+"\n")


if __name__ == "__main__":
    main()

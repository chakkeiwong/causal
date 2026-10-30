#!/usr/bin/env python3
"""Integrated IV, nuisance learning and a separately frozen bandwidth follow-up."""
import hashlib
import json
from pathlib import Path
import sys
import time

import numpy as np
from scipy.linalg import solve_discrete_lyapunov
from scipy.signal import lfilter
from scipy.stats import norm
from sklearn.linear_model import Lasso
from threadpoolctl import threadpool_limits

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from causalbank.responses import bartlett_lrv, direct_response, level_response_from_changes
from study_responses import generate


def integrated_sample(config, rng):
    n = config["origins"] + config["horizon"] + 1
    # Common random-walk trend plus two initialized stationary spreads.
    transform = np.array([[1., 0., 0.], [1., 1., 0.], [.25, 0., 1.]])
    b = np.array([[1., .3, .1], [.7, 1., .2], [-.4, .2, .9]])
    innovation = np.linalg.solve(transform, b)
    diagonal = np.diag([1., .9, .8])
    state = np.r_[0., rng.multivariate_normal(np.zeros(2), solve_discrete_lyapunov(
        diagonal[1:, 1:], innovation[1:] @ innovation[1:].T))]
    eps, noise = rng.normal(size=(n, 3)), rng.normal(size=n)
    x, z = np.empty((n, 3)), np.empty(n)
    v = rng.normal()
    rho = config["instrument_persistence"]
    for t in range(n):
        state = diagonal @ state + innovation @ eps[t]
        x[t] = transform @ state
        v = rho*v + np.sqrt(1-rho*rho)*noise[t]
        z[t] = config["strength"]*eps[t, 0] + v
    f = transform @ diagonal @ np.linalg.inv(transform)
    truth = np.array([(np.linalg.matrix_power(f,h) @ b[:,0])[j] for j in (1,2)
                      for h in range(config["horizon"]+1)])
    return x, z, truth


def learning_sample(config, rng):
    n, p = config["dates"], config["controls"]
    # Burn-in is disclosed; .5**300 is below numerical precision.
    c = np.tanh(lfilter([1], [1, -.5], rng.normal(size=(n+300, p)), axis=0))[300:]
    v, u, e0 = lfilter([.5], [1, -.5], rng.uniform(-1,1,size=(3,n+300)),axis=1)[:,300:]
    m = .8*c[:,0] + .7*c[:,3] + .4*c[:,4]
    r = c[:,0] + .5*c[:,1] - .3*c[:,2]
    g = .7*c[:,0] - .8*c[:,3] + .6*c[:,4]
    d, z = r + .8*v + u, m + v
    y = 1.2*d + g + .6*u + e0
    return c, y, d, z, np.column_stack((1.2*r+g, r, m))


def learned_fit(data, config, method):
    c, y, d, z, oracle = data
    n = len(y)
    gap = config["gap"]
    blocks = [np.arange(n//2-gap//2), np.arange(n//2+gap//2,n)]
    residuals = []
    for fold, evaluation in enumerate(blocks):
        training = blocks[1-fold]
        if method == "oracle":
            predictions = oracle[evaluation]
        elif method == "unadjusted":
            predictions = np.tile(np.mean(np.column_stack((y,d,z))[training],axis=0),(len(evaluation),1))
        else:
            train, test = c[training], c[evaluation]
            if method == "factor3":
                _, vectors = np.linalg.eigh(train.T @ train / len(train))
                basis = vectors[:, -config["factor_rank"]:]
                train, test = train @ basis, test @ basis
            if method == "sparse":
                penalty = config["sparse_penalty_multiplier"] * np.sqrt(np.log(len(train))*np.log(n*c.shape[1])/len(train))
                predictions = np.column_stack([Lasso(alpha=penalty,max_iter=3000,tol=1e-7).fit(train,target[training]).predict(test)
                                               for target in (y,d,z)])
                predictions = np.clip(predictions,-10,10)
            else:
                design = np.column_stack((np.ones(len(train)),train))
                targets = np.column_stack((y,d,z))[training]
                coefficient = np.linalg.lstsq(design,targets,rcond=None)[0]
                predictions = np.column_stack((np.ones(len(test)),test)) @ coefficient
        residuals.append(np.column_stack((y[evaluation],d[evaluation],z[evaluation]))-predictions)
    denominator = sum(np.sum(r[:,2]*r[:,1]) for r in residuals)
    theta = sum(np.sum(r[:,2]*r[:,0]) for r in residuals)/denominator
    total = sum(len(r) for r in residuals)
    lrv = sum(len(r)*bartlett_lrv((r[:,2]*(r[:,0]-theta*r[:,1]))[:,None],int(total**.25))[0,0]
              for r in residuals)/total
    se = np.sqrt(lrv/total)/(abs(denominator)/total)
    return theta, se


def summarize(values, repetitions):
    a = np.asarray(values)
    coverage = float(a[:,0].sum()/repetitions) if len(a) else 0
    return {"coverage":coverage, "mc_se":float(np.sqrt(coverage*(1-coverage)/repetitions)),
            "mean_squared_error":float(a[:,1].mean()) if len(a) else None,
            "mean_width":float(a[:,2].mean()) if len(a) else None}


def main():
    path = ROOT / "docs/studies/a-extension-v1.json"
    spec = json.loads(path.read_text())
    repetitions = spec["repetitions"]
    results = {}
    with threadpool_limits(limits=1):
        for study in ("integrated", "learning", "bandwidth_followup"):
            start = time.perf_counter()
            names = {"integrated":["stationary_changes","invalid_stationary_levels"],
                     "learning":["oracle","sparse","factor3","unadjusted"],
                     "bandwidth_followup":["bandwidth_1","bandwidth_4"]}[study]
            values = {k:[] for k in names}
            failures = []
            for repetition in range(repetitions):
                rng = np.random.default_rng(np.random.SeedSequence([spec["seed"],list(("integrated","learning","bandwidth_followup")).index(study),repetition]))
                config = spec[study]
                if study == "learning":
                    data = learning_sample(config,rng)
                elif study == "integrated":
                    x,z,truth = integrated_sample(config,rng)
                else:
                    x,z,truth = generate(config,config["horizon"],rng)
                for name in names:
                    try:
                        if study == "learning":
                            theta,se = learned_fit(data,config,name)
                            values[name].append([abs(theta-1.2)<=norm.ppf(.975)*se,(theta-1.2)**2,2*norm.ppf(.975)*se])
                        else:
                            if name == "stationary_changes":
                                fit = level_response_from_changes(x,z,config["horizon"])
                            else:
                                multiplier = 4 if name == "bandwidth_4" else 1
                                fit = direct_response(x,z,config["horizon"],bandwidth=int(multiplier*config["origins"]**.25))
                            critical = norm.ppf(1-.05/(2*len(truth)))
                            radius = critical*np.sqrt(np.diag(fit.covariance))
                            values[name].append([np.all(abs(fit.estimate-truth)<=radius),np.mean((fit.estimate-truth)**2),2*radius.mean()])
                    except (ValueError,np.linalg.LinAlgError,FloatingPointError) as error:
                        failures.append({"rep":repetition,"method":name,"error":str(error)})
            results[study] = {"seconds":time.perf_counter()-start,"failures":failures,
                              "metrics":{k:summarize(v,repetitions) for k,v in values.items()}}
            print(json.dumps({"study":study,**results[study]}),flush=True)
    files = [path,Path(__file__), ROOT/"tools/study_responses.py",ROOT/"src/causalbank/responses.py"]
    receipt = {"spec":spec,"input_sha256":{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},"results":results}
    (ROOT/"docs/studies/a-extension-results.json").write_text(json.dumps(receipt,indent=2)+"\n")


if __name__ == "__main__":
    main()

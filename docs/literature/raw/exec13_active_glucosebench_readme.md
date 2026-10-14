# GlucoseBench

**GlucoseBench is a small modification of [Jinyu Xie's simglucose](https://github.com/jxx123/simglucose), not a new physiological simulator.** Almost all of the data-generating model, virtual-patient data, insulin-pump behavior, and CGM sensor model come directly from simglucose. Our additions are a noisy plasma-insulin observation channel, a fixed intervention-forecasting protocol, a learner-facing API, and evaluation utilities.

The task is to learn an individual simulated patient's responses to meals and insulin, then forecast new interventions for **that same patient**. This is a research benchmark, not a clinical tool or a test of transfer to unseen patients. No MDA, LLM service, API key, Modal account, Gym, or separate simglucose checkout is required.

## Install and run

Python 3.10+:

```bash
git clone https://github.com/murphyk/glucosebench.git
cd glucosebench
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[test]'
python examples/persistence.py
# Equivalent CLI, also exports the public training episodes:
glucosebench --patient adult\#001 --output results/persistence.json \
  --training-output results/training.json
python -m pytest -q
```

The demo simulates 18 six-hour episodes for one profile (two passive, four selected, twelve test), then scores persistence at every budget/cut. It uses CPUs only. To match the paper's numerical stack, use Python 3.11 and `pip install -c requirements-repro.txt -e '.[test]'`. Different SciPy/platform versions can cause small floating-point differences; exact replay is deterministic within a fixed environment.

## Minimal learner API

```python
from glucosebench import Benchmark, persistence, summarize

run = Benchmark('adult#001', replicate=0)  # evaluator-side identity
training = run.training                  # two public passive episodes
menu = run.actions                       # available index -> intervention
for index in (0, 12, 24, 36):             # replace with a learner's choices
    new_episode = run.observe(index)

# Freeze acquisition before generating or scoring held-out outcomes.
evaluator = run.freeze()
rows = evaluator.evaluate(persistence, budget=6, cuts=(45,))
print(summarize(rows))
```

A predictor is a callable `predictor(payload)` returning exactly:

```python
{"cgm_mg_dl": [...], "insulin_pmol_l": [...]}
```

Each array must contain finite numbers in the order of `requested_cgm_times_min` or `requested_insulin_times_min` in the payload. The payload supplies:

- `training_episodes`: the complete public training episodes up to the requested budget;
- `query`: only the allowed observation prefix, plus the **complete known delivered input schedule**, units/column labels and intervention;
- `forecast_cut_min` and the requested future observation times.

CGM units are mg/dL; insulin units are pmol/L. `minute_inputs` columns are time (minutes), consumed meal (g/min), basal insulin (U/min), and bolus insulin (U/min). Unobserved insulin assays are JSON `null` with an explicit boolean mask, never zeros. Neither age, patient ID, body weight, parameters, clean signals nor latent states are placed in learner payloads. The basal input is known to the learner even though the simulator privately computes it from the profile.

Only the harness should own `Benchmark` and `Evaluator`; give learner code the public payloads and available action menu. This in-process API prevents accidental leakage, not deliberate introspection. As with any public simulation benchmark, compliant evaluation must forbid learners from reading the bundled hidden model/data or calling the simulator outside the budget. Fits/hyperparameters must be chosen using training episodes only. Query prefixes can update predictive state but must not be used to refit the model or tune hyperparameters against future values.

## Train/test protocol (v1)

The versioned definition is in [`protocol_v1.json`](src/glucosebench/data/protocol_v1.json); the exact held-out conditions are frozen in [`test_protocols_v1.json`](src/glucosebench/data/test_protocols_v1.json).

| Component | Definition |
|---|---|
| Profiles | All 30 upstream profiles: 10 child, 10 adolescent, 10 adult. Train and score each independently. |
| Episode | Reset to the profile's default initial state; 360 minutes; deterministic physiological ODE. |
| CGM | Native GuardianRT sensor, sampled every 5 minutes including t=0: 73 readings, with correlated sensor noise. |
| Added insulin assays | Every 15 minutes including t=0: 25 readings. Private plasma mass is divided by its volume, then independent Gaussian noise with SD 10 pmol/L is added. |
| Passive training (D0) | (30 g meal at 60 min, 1 U bolus at 75 min), then (45 g at 90 min, 1.5 U at 90 min). |
| Active training | Up to four distinct choices from 48 actions: meal {20,40,60} g × time {60,120} min × bolus {0,0.5,1,1.5} U × delay {0,30} min. |
| Checkpoints | Total training budgets 2, 3, 4, 6 episodes. Snapshot learner fits/history at each budget. Evaluate only after acquisition is frozen; test scores must not influence subsequent acquisition. |
| Test interventions | 12 independent Latin-hypercube conditions, originally SciPy 1.14.1 seed 8723: meal 20–60 g, time 60–120 min, bolus 0–1.5 U, delay 0–30 min. Times rounded to five minutes. Frozen JSON avoids QMC-version drift. No test condition equals a training action/passive protocol. |
| Forecast cuts | 0, 45 (primary), 120, 180 minutes. At **cut 0 no query observations are supplied, including t=0**. At positive cuts, observations through the cut are available. Score only observations strictly after the cut. |
| Delivery | Meal consumed at at most 5 g/min; bolus spread over five minutes with upstream Insulet quantization/clipping; record actual delivered rates. |
| Seeds | SHA256(`glucose-v1\|patient\|replicate\|role\|index`) first eight hex digits. Training indices start at 1; test indices at 0. Assay RNG is separately derived by NumPy SeedSequence([sensor_seed,23197]). Paper census replicate is 0; report any additional replicates separately. |

The intervention split is within patient, not a random split of time points from the same trajectory. Do not pool profiles for training or use sealed test episodes as validation. For hyperparameter selection, use only training episodes, for example leave-one-training-episode-out validation. Choosing conditions based on prior training observations is allowed; repeatedly querying an action or exceeding the six-episode budget is not. Do not filter out large responses or clip forecasts based on hidden truth.

At cut 45 the required forecast arrays contain 63 CGM values and 21 insulin values. At cuts 0/120/180 the corresponding counts are 72/24, 48/16 and 36/12. Missing assay times do not contribute to loss.

## Scores and baseline

`metrics.score` reports per-channel MSE, RMSE and normalized MSE. The scale is each channel's population variance across the **two passive training episodes only**, floored at 1 in squared channel units. It stays fixed across budgets, cuts, and methods. This is the paper's later multi-cut normalization, not the earlier pilot's query-persistence denominator. Scores compare predictions to noisy observed outcomes, not clean hidden states.

Two evaluation windows are returned: `suffix` (t > cut) and `common_suffix` (t > 180 for every cut). The latter allows comparisons across cuts without changing the scored time window. Report channels separately; if reporting an equal-channel mean, state it explicitly. To reproduce the paper's census aggregation, average query nMSE arithmetically within each patient at each budget/cut, then take a geometric mean across patients; bootstrap whole patients for uncertainty.

The included **last-observation persistence** baseline repeats each channel's most recent available query observation. At cut zero it uses that channel's mean initial observation across D0. It does not use future values or simulator state. The demonstration acquisition policy selects action indices 0,12,24,36; it is a simple API example, not an optimized baseline or a reproduction of MDA's selected histories.

Invalid/nonfinite/wrong-length forecasts are explicit failed cells. `summarize` returns attempted/failed counts and null mean scores if any query failed, rather than silently dropping failures. Report all attempted cells and the treatment of failures in any additional aggregation.

## Attribution, data and reproducibility

The vendored numerical subset comes from simglucose commit [`2e897f10f333c76ad383e44a5f98b2586e4aa9ac`](https://github.com/jxx123/simglucose/tree/2e897f10f333c76ad383e44a5f98b2586e4aa9ac). It includes the patient ODE, all 30 virtual-patient parameter rows, sensor/pump tables, and the small supporting modules. The differential equations and numerical algorithms are unchanged. Only import/resource namespaces were adjusted and an unused plotting import and optional Gym registration were omitted. See [NOTICE.md](NOTICE.md), the [upstream license](src/glucosebench/_vendor/simglucose/LICENSE), and [file checksums](src/glucosebench/_vendor/simglucose/PROVENANCE.json).

The oracle adapter and protocol were extracted from [MDA](https://github.com/murphyk/MDA). Learned models, fitted parameters, LLM transcripts and method-specific histories are not benchmark data and remain in MDA. A small synthetic historical episode is retained as a regression fixture; the rest of the data is generated deterministically through the oracle. The tests check replay, parity with that fixture, public/private separation, masking, budget enforcement, and failure accounting.

Please cite Jinyu Xie, *Simglucose v0.2.1* (2018), https://github.com/jxx123/simglucose, when using this benchmark, and acknowledge the upstream UVA/Padova simulation work cited there. GlucoseBench's contribution is the small observation/protocol/API adaptation described above.

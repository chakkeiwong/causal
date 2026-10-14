# Less Greedy Equivalence Search



Less Greedy Equivalence Search is an algorithm for causal discovery from observational and interventional data with prior assumptions.

This repository contains the code for the paper ["Less Greedy Equivalence Search"](https://causalai.net/r134.pdf) by Adiba Ejaz and Elias Bareinboim.

Disclaimer: This code is offered publicly with the MIT License, meaning that others can use it for any purpose, but we are not liable for any issues arising from the use of this code. Please cite our work if you found this code useful.

---

## Directory Structure

```
LGES/
├── ges 
├── src/
│   └── experiments/
│       ├── obs/        
│       │   ├── obs_no_prior.py
│       │   ├── obs_init.py
│       │   └── obs_example.py
│       └── exp/       
│           └── exp_no_prior.py
│       └── sachs.py
└── README.md
```

---

##  Quick Start

Make sure you have Python 3.8+ and the required dependencies installed.

```bash
pip install -r requirements.txt
```
---

## Running Experiments

###  Observational data (no prior Assumptions)

```bash
cd src/experiments/obs
python -m obs_no_prior \
    -p <NUM_VARS> \
    -n <NUM_SAMPLES> \
    -d <AVG_DEGREE> \
    -g <NUM_TRIALS> \
    -m <MODEL_TYPE>
```

Results saved to:

```
src/experiments/obs/results_no_prior/vars_<NUM_VARS>_samples_<NUM_SAMPLES>_degree_<AVG_DEGREE>_model_<MODEL_TYPE>
```

---

### Observational data (with prior assumptions)

```bash
cd src/experiments/obs
python -m obs_init
```

Results saved to:

```
src/experiments/obs/results_init/vars_<NUM_VARS>_samples_<NUM_SAMPLES>_degree_<AVG_DEGREE>_model_<MODEL_TYPE>
```

---

### Interventional data (no prior assumptions)

```bash
cd src/experiments/exp
python -m exp_no_prior \
    -p <NUM_VARS> \
    -n <NUM_SAMPLES> \
    -d <AVG_DEGREE> \
    -g <NUM_TRIALS> \
    -m <MODEL_TYPE>
```

Results saved to:

```
src/experiments/exp/results_no_prior/vars_<NUM_VARS>_samples_<NUM_SAMPLES>_degree_<AVG_DEGREE>_model_<MODEL_TYPE>
```

---
##  Generating plots

To generate the plots presented in the paper, use:
```bash
cd src/experiments/obs
python -m plot.py --plot obs_no_prior
python -m plot.py --plot obs_init
cd src/experiments/exp
python -m plot.py --plot exp_no_prior
```

Plots saved to:

```
src/experiments/obs/plots_no_prior/
src/experiments/obs/plots_init/
src/experiments/exp/plots_no_prior/
```
---

##  Example usage

To see a minimal working example:

```python
# src/experiments/obs/obs_example.py
```

This shows how to configure and run a basic experiment.

---

## Arguments

| Argument       | Description                                  |
|----------------|----------------------------------------------|
| `-p`           | Number of variables                          |
| `-n`           | Number of samples                            |
| `-d`           | Average degree of the true DAG               |
| `-g`           | Number of random graphs to sample per setting                    |
| `-m`           | Model type: `linear-gaussian` or `multinomial`       |


# HPO-NAS

Optimization over moderate spaces of roughly 2–10 architecture and training coordinates. The public API includes GP+qLogEI with a Matérn 5/2 kernel and dimension-scaled priors, Random/Sobol, optional CMA-ES, local/Ray execution, and resumable studies. Width, depth and activation build real networks. General cell search, supernets and weight sharing are outside the program.

**Status:** Tier 0 acceptance remains blocked. Use [the master program](CONSOLIDATED_MASTER_AUTHORITY.md) and [generated progress](docs/progress.md) for current work, evidence freshness and unresolved decisions. The [repair record](docs/REPAIR_PLAN_2026_09_26.md) preserves the completed implementation repair pass; it does not certify release.

## Install

Python 3.12+ is required. Clean CPU installations are checked on Python 3.12 and 3.13; other versions and platforms are not verified. Keep the environment separate from other projects.

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e .
# Optional components:
python -m pip install -e '.[ray,tpe,cmaes,rl,validation,test]'
```

The RL extra pins Brax to the tested Git revision because its PyPI 0.14.2 release is incompatible with the supported JAX 0.11 line. Campaign metadata records installed versions and dependency source URLs. GPU JAX installation is hardware-specific; CPU runs work with the declared extra.

## Quick start

```python
from hponas import GPSearcher, Knob, LocalExecutor, SearchSpace, Study

space = SearchSpace([
    Knob('x', 'continuous', (0.0, 1.0)),
    Knob('width', 'ordinal', (8, 32)),
])

def objective(config):
    return (config['x'] - 0.3)**2 + ((config['width'] - 16) / 32)**2

study = Study(
    GPSearcher(space, seed=42), LocalExecutor(), objective,
    budget=10, maximize=False, study_name='example', checkpoint_dir='checkpoints',
)
result = study.run()
print(result.best_config.values, result.best_value)
```

Objectives receive a configuration dictionary. They can also declare `fidelity`, `seed`, and `trial_id` parameters. Return a scalar or a dictionary with `value`, `cost` (seconds), `metadata`, and file-path `artifacts`. A `Study` budget counts new configurations; ASHA promotions add evaluations. `total_cost` includes all completed/failed attempts reported by the executor, not unmeasured work lost when the driver dies.

Resume with a fresh executor and searcher, then load the checkpoint before calling `run()`:

```python
resumed = Study(GPSearcher(space), LocalExecutor(), objective)
resumed.load_checkpoint('checkpoints/example_checkpoint.json')
result = resumed.run()
```

Committed results are not dispatched again. Pending work can execute again after a crash; use `trial_id` to make external side effects idempotent. Checkpoints use schema 3; schema 2 endpoint ledgers remain readable under their explicit scheduler policy. Older incomplete Study snapshots require explicit migration. Batch observations commit in dispatch order. A Store snapshot is authoritative if both SQLite and a JSON projection are configured; load from the Store after an interrupted projection write.

ASHA now uses reference quantile promotion with waiting candidates and explicit legacy compatibility. Objectives that declare `reporter` can be paused, pruned, or cancelled while running on Local or Ray executors. Promotions can resume durable checkpoints or explicitly restart and charge repeated work. See [streaming, median pruning, compute limits, and incomplete outcomes](docs/STREAMING_SCHEDULER.md).

The public `SearchSpace` uses `Knob`. `hponas.types.SearchSpace`/`Parameter` remain supported through an adapter. Legacy `propose()` searchers are adapted when passed to Study. Explicitly named legacy modules remain available. Scalar Study does not accept multi-objective searchers.

`CMAESSearcher(space, seed=42)` wraps Optuna/CMA-ES for unconditional continuous spaces, with optional log/logit transforms. Install the `cmaes` extra. Its checkpoints bind the vendor versions and retain pending asks; mixed/conditional spaces are rejected.

`PASHAScheduler(PASHAConfig(...))` in `hponas.schedulers` grows the maximum fidelity only when survivor rankings disagree. Study selects its incumbent at that current fidelity. This may be below the declared full budget; final full-budget evaluation remains a separate workload decision. The older budget-only policy is now named `BudgetedASHAScheduler`/`BudgetedASHAConfig`. Existing budget-only checkpoints must use that policy and cannot be loaded as progressive PASHA. See the [specification repair review](docs/program/SPEC_REPAIR_REVIEW_2026_09_28.md) for the tested envelope.

## Real PPO and validation

The [maintained examples](examples/README.md) run against either checkout or installed library code. They preserve unique run directories and do not certify acceptance. Audited campaigns below require the full Git checkout because their source fingerprint covers tests, examples, build inputs and protocols omitted from the wheel. A wheel-only invocation is rejected before campaign artifacts are written. Use `python -m tools.check_installed --output receipt.json` from outside the checkout to verify an isolated wheel installation.

```bash
# Real bounded CPU PPO, policy checkpoint, SQLite ledger and separate protected evaluation:
JAX_PLATFORMS=cpu OMP_NUM_THREADS=2 python -m validation.run_validation_with_audit V14
# Independent vendor parity and actual replay/crash/concurrency scenarios:
OMP_NUM_THREADS=2 python -m validation.run_validation_with_audit V01
OMP_NUM_THREADS=2 python -m validation.run_validation_with_audit V02
# Inspect historical mutation cache; this cannot produce a campaign PASS:
python -m validation.run_validation_with_audit V03
# Full mutation run in a new source copy, preserving the existing cache:
python -m validation.run_validation_with_audit V03 --run-mutations
python -m tools.gate_check --phase tier0 --mode dry-run
```

V14 evaluates protected seed 999 only after the search result is committed. `workloads.rl_routine.evaluate_checkpoint` performs this separate evaluation. Passing V14 establishes an executable workflow, not statistical performance.

V04-T0 compares GP and TPE against Sobol and Random; V05 compares GP with log and linear coordinates using identical physical initialization. The approved claims use protected paired final/anytime win utility on a named finite suite. Search selects the policy before separate test evaluation; raw returns and failures remain in the evidence. [The active design](validation/designs/tier0_candidate_v2_1.json) is incomplete: held-out selection, power, measured budgets and objective evidence validation and resource authorization remain open. Both campaigns require a complete evidence-validated design and separate resource authorization and refuse `--smoke` as an acceptance path. The old five/three-seed baseline experiments are historical diagnostics.

Every audited run preserves its protocol, raw results, package/source fingerprints, and a V16 receipt under `validation/artifacts/<ID>/<run>/`. Gates reject missing, stale, empty, or inconsistent evidence. See the [current master program](CONSOLIDATED_MASTER_AUTHORITY.md) for execution status.

## Development

```bash
python -m pip install -e '.[dev,test,ray,tpe,cmaes,validation]'
python -m pytest tests -m 'not slow' -q
python -m ruff check hponas workloads validation tools
python -m compileall -q hponas workloads validation tools examples
```

ASHA, MO-ASHA, scalarization, cost-aware search and priors have implementations and tests; their statistical acceptance is separate. Python πBO priors use bounded finite differences for their acquisition gradient; discontinuous priors can have flat regions. Two optional πBO recovery tests still fail their unchanged acceptance assertions; the repair record preserves the results. `workloads.sampler_neutra` currently implements ordinary HMC with rank/split ESS and R-hat diagnostics; it does not implement a learned neural transport. Tier 1/2 gates remain blocked until protocol identities and audited campaign evidence are complete.

The optional `GPqLogEISearcher` now uses schema-2 checkpoints with full space, prior recipe, versions and RNG state; incomplete legacy snapshots require explicit migration. The current `PriorBandSampler` is a heuristic portfolio, with published-method and scheduler conformance still open. V11 pilots cannot return an acceptance PASS, and confirmatory V11 execution remains blocked on those repairs and certification. See the [prior review](docs/program/PRIOR_REVIEW_2026_09_28.md).

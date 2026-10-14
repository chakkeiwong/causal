# Executed scientific studies for the substantive revision

The current S02–S07 experiments, installed-package checks and complete workflow
measurements are documented in [the scientific completion replay guide](../studies/README.md).
This directory retains the earlier fitted studies and their qualified roles,
as well as generated tables used by the current monograph. The earlier
precomputed-score timing below is distinct from the complete S07 workloads.

The fixed design is implemented in `tools/revision_studies.py`. All populations,
cash schedules and mechanisms are synthetic; none represents a named bank.
The seed is 20261007. A result may be unfavorable. Scientific claims are
limited to the declared generating laws and recorded workloads.

1. **Deposit rollout:** 96 branches, 30 months, three adoption cohorts and
   never-treated branches. Compare a cohort-time contrast and TWFE; estimate
   both balances and monthly funding contribution with whole-branch bootstrap.
2. **Collections:** a three-state, eight-decision process. Fit transitions on
   training trajectories and compare fixed policies on separate trajectories
   using direct, cumulative importance and doubly robust values. The evaluator
   has an exact dynamic-programming reference unavailable to estimation.
3. **Controlled hidden states:** estimate initial probabilities, transitions
   and three-category emissions by multiple-start EM. Contrast randomized
   logging with hidden-state logging and compare the correctly specified joint
   action model with a likelihood that omits it. This is a model-conditional
   experiment, not a general identification test.
4. **Credit supply:** matched bank-firm observations compare pooled regression
   and borrower fixed effects. Bank-level variation determines inference.
5. **Dependence and structural time series:** repeated experiments compare
   row, entity and crossed-cluster inference; equal reduced-form likelihoods
   produce different structural impulse responses under different orderings.
6. **Data and scale:** temporal revision selection and streaming score
   reductions have separately recorded implementation and timing receipts.

Results, generated TeX tables, plots and the environment receipt remain in this
directory. The older examples remain in `docs/examples/` as small exact checks.
Re-running this suite updates measured times; statistical seeds and designs
remain fixed. Replay verification compares scientific values separately from
timing fields.


Run from the repository root:

```bash
python3 tools/revision_studies.py
python3 tools/run_data_scale.py
python3 tools/construction_economics.py
python3 tools/verify_revision.py
```

The first command takes roughly 95 seconds on the observed host, mostly latent
model refits. It writes `results.json`, generated figures/tables and an environment
receipt. The other commands preserve component measurements, economics and
independent finite-path/account checks. NumPy, SciPy, matplotlib and standard
Python are required; no source acquisition, bank records or external package
runtime qualification occurs. Matplotlib uses a temporary configuration directory.
The narrow component package is under `src/causalbank`; use `PYTHONPATH=src` or
install the local package to import it from another script.

The latent-state study retains optimization caps: all 30 selected omitted-action
fits and seven joint fits hit the repetition budget; one of 79 bootstrap fits
hits its cap. They remain in the results. `verify_revision.py` reuses the same
main observational data and seeds with a longer budget; the sign reversal remains
after its stopping criterion. It also checks HMM likelihood and posterior counts
against exhaustive paths, sequential DR against exact expectations and an
independent recursion, repeated-intersection covariance against a batch formula,
and financial hurdle equations by direct cash accounting.

`data-scale.json` measures generated precomputed score reduction, not complete
causal estimation. Peak memory includes Python/libraries. Its dense intersection
storage grows with declared entity-by-date cardinality. Source I/O, nuisance
fitting and temporal reconstruction are excluded from the timed operation.
`economics.json` is an equal-output planning comparison, including losing cases,
not observed prices, effort savings or commercial returns.

The studies and local components were re-executed and requalified for the
reconstructed monograph on 8 October 2026. The negative crossed-variance count
is now recorded (zero in the current experiment), and malformed identities
or cluster-key shapes are explicitly rejected by the narrow components.

Refreshing these outputs changes measured times and artifact hashes. Run
`tools/verify_revision.py`, `tools/check_scientific_contracts.py` and
`tools/reconstruction_checks.py`, rebuild with `tools/causal_program.py build`,
then run `tools/foundations_audit.py` and `tools/render_review.py`. The active
documents are causal_foundations and sponsor_reconstruction. The verification
and build manifests detect stale inputs. Do not regenerate historical V2
publication assets or overwrite either rejected delivery archive.

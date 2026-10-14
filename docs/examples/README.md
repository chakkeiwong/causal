# Reproducible proposal examples

The frozen artifact is [results.json](results.json), generated with seed
20261007. It records Python, numerical-library versions and assumptions.

| Construction | What it establishes | Principal boundary |
|---|---|---|
| Static AIPW and three fixed-policy comparisons | Selection bias, orthogonal adjustment and paired simultaneous intervals | Independent synthetic households; one seed, no coverage claim |
| Longitudinal g-formula/IPW | Exact intervention means from all 16 observed cells | Two decisions, known data-generating law |
| Staggered panel | TWFE weights and target mismatch despite untreated parallel trends | Deterministic illustration |
| POMDP filter and two-world counterexample | Forward likelihood equals path enumeration; observed law alone can leave effects unidentified | Supplied finite model, not bank state recovery |
| Controlled HMM fit | Transition recovery with known emissions/initial law under random actions | Three starts, one seed, no confidence-interval study |
| Investment economics | NPV, break-even benefit, budget and delay arithmetic | Assumed costs/benefits, not bank forecasts |

Run `python3 tools/replay_examples.py` from the repository root to recompute and
compare every scientific output with the frozen artifact. It leaves the result
file and figures unchanged and writes [replay-check.json](replay-check.json).
The comparison tolerance is 1e-8 absolute and relative; different numerical
libraries may need an explicitly reviewed optimizer tolerance.

`python3 tools/run_examples.py` deliberately regenerates results, figures and
the TeX numbers. Its measured elapsed time changes the result-file hash even
when scientific outputs agree. If intentionally regenerating the package,
review the difference and refresh `artifact_sha256` in
`contracts/examples/effect_result.json`, then rebuild claim records and rerun
contract/archive checks. Never silently accept an unexplained scientific change.

The contract suite validates four examples and rejects ten invalid cases.
Those checks enforce selected semantics, not scientific assumptions. The future
coverage, scale and bank benchmark programs are specified in the proposal and
have not been represented as completed experiments.

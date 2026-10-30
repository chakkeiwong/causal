# From exact graph search to an estimated lending effect

30 October 2026. This is a new sampling question, not a rerun of the completed
1,381-case exact-oracle search study. No native software or live language model
is evaluated, and no bank-data result is implied.

## Question and economic consequence

Does the repaired stable search reliably recover relationships from noisy
samples, and what happens when its estimated relationships choose the variables
used to adjust a rate/balance comparison? A search can be logically complete
yet statistically wrong. A nominal interval after selecting controls on the
same observations need not have its stated coverage. The proposal needs a
clear distinction between these errors and the already established shortcut.

## Fixed design before execution

Three deliberately constructed Gaussian mechanisms are compared:

1. Strong measured confounding: three independent baseline causes affect a
   rate concession X and response Y; C=X+Y+noise is a later common consequence.
   The true effect of X on Y is zero. Nonidentical rational coefficients avoid
   imposing symmetries accidentally. Check population partial correlations
   against d-separation before admitting the faithful reference case.
2. Weak measured confounding: reduce the baseline coefficients without changing
   the graph or the zero effect. Verify the same population conditions and
   report the minimum nonzero partial correlation. This is a difficult signal
   regime, not a guaranteed failure at every sample size.
3. Exact cancellation: Z is baseline, X=Z+eX and Y=X-Z+eY. The intervention effect
   is one, while Z and Y are marginally independent. This violates faithfulness
   and is explicitly an assumption-failure case. It must not be scored as a
   counterexample to a theorem requiring faithfulness.

Use sample sizes100,500,2000, 200 independent replicates per mechanism/size,
and fixed two-sided Fisher-z test thresholds0.01 and0.05. Compare full stable
subset search, the inspected all-neighbour dependence screen and a depth-two
cap on each identical dataset. Freeze all thresholds before looking at results.
The sample test is the Gaussian Fisher-z rule in Kalisch and Buehlmann(2007),
equation(3)/section2.2.2. The level-frozen neighborhoods follow the skeleton
idea in Colombo and Maathuis(2014), section4.1/algorithm4.1. No claim that this
project code exactly reproduces a released R/Java implementation is allowed.

For each completed search, an explicitly naive rule selects only baseline
variables adjacent to both X and Y; the information clock always excludes C.
Estimate the slope and ordinary95% t interval on the same data. Compare with
all-baseline adjustment, unadjusted regression and the known-invalid adjustment
that additionally includes C. Record selected sets, interval coverage, bias and
length. The naive selected-set rule is a diagnostic comparator, not a proposed
valid estimator or general graph-to-adjustment algorithm. For a depth-limited
search, retain its incompleteness flag; numerical estimates do not erase it.

Record full-skeleton error, false/missing links, X-Y edge retention, unresolved
search status, distinct query counts and per-replicate estimation results.
Use Wilson intervals for descriptive Monte Carlo proportions and paired
differences for methods on the same samples. These intervals quantify simulation
variation, not uncertainty about banks or all possible graphs. All results,
including unexpected or unfavorable outcomes, must be retained.

## Skeptical review and controls

- Check every population conditional-independence query using independent
  graph d-separation and exact rational Schur complements. The cancellation
  case is intentionally exempt from faithfulness, with its violation recorded.
- Check sample partial correlations by both precision-matrix and residual
  regressions on one entire query family for each mechanism. Validate interval
  arithmetic independently by residualization for representative replicates.
- Use one seed and retain per-case outputs, environment versions, script and
  plan hashes. At most20 minutes of computation; save failure/partial records.
  Do not rerun merely to improve the result. Any repair gets a new attempt.
- Do not infer finite-sample guarantees from the original asymptotic theorem:
  its assumptions include Gaussianity, faithfulness, sparsity and nonzero
  partial-correlation bounds. Alpha is not a graph-level confidence probability.
- Distinguish source mathematics, project derivations and simulation evidence.
  No causal orientation, latent-variable recovery, live model, native package,
  post-selection validity or bank qualification is established here.

## Decision rule and deliverable

The study can support retaining full search as a logical reference while
requiring measured sampling diagnostics and defensible adjustment before an
effect is used. A favorable finite suite cannot qualify a general discovery
service. A failure in the naive selected-control intervals supports rejecting
that unqualified workflow; an apparent success would remain bounded evidence.
Publish the comparisons in economic language with plots and formulas, include
the two primary sources with audited anchors, and integrate the treatment into
a preserved successor without disturbing ongoing release edits.

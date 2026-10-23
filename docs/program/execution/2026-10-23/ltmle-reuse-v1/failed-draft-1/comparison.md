# ltmle: bounded longitudinal reference decision

## Target and history

The selected `ltmle` source is a wide-data R implementation of longitudinal
targeted maximum likelihood estimation. Columns are ordered by causal time;
treatment nodes are binary; censoring has its own coding; and survival outcomes
have an absorbing event convention. A policy mean is
\[
  \theta_d=E[Y^d],
\]
under a specified sequence of actions. A causal interpretation requires
consistency, sequential exchangeability for treatment and censoring, positivity
along the intervention histories, and suitable nuisance-estimation and
regularity conditions. The software interface cannot establish those
conditions. A time zero, population, event horizon, history order and
intervention law therefore have to be resolved before any estimate is
interpreted.

The public `ltmle` wrapper accepts one regime or a pair of regimes. Its paired
path reports a contrast between two regimes; more policies require a separate
marginal-structural-model route, which changes the scientific target from a
direct comparison into a fitted projection. The default nuisance library is
`glm`, not a generic ensemble; the source declares cumulative treatment
probability bounds `gbounds=c(0.01,1)` and `variance.method="tmle"`. A
caller-supplied dynamic rule, fixed treatment vector, numerical propensity
array, and outcome scaling choice are not interchangeable ways to state a
policy. Continuous outcomes outside a declared range can be truncated or
scaled. An observed-sample range must not silently become a business-defined
outcome boundary.

## Uncertainty, censoring and clusters

The selected source calculates an influence-curve covariance and can also
calculate a separate TMLE-based variance under a restricted set of options.
It documents that the additional variance is unavailable for, among other
cases, a non-null cluster id. In the inspected call path, a requested method
other than `ic` is changed to `ic` when such an id is present. The summary
routine uses the influence-curve covariance when the additional variance is
absent; for a two-regime result, it maps that shared covariance to the reported
mean, risk difference, relative risk or odds ratio through a delta-method
gradient. The caller therefore needs the effective method and sampling unit,
not just the method string it supplied.

For clustered records, the source sums record-level influence values within
each id and rescales by the number of ids divided by the number of records.
With two identical records per household, an iid-row calculation would treat
twice as many dependent records as units and halve the variance of the
household-mean estimator. Aggregation addresses that particular sampling-unit
mistake; it does not establish independent households, appropriate unequal
cluster-size weighting, a valid censoring law or calibrated finite-sample
coverage. The selected source permits binary treatment and requires
chronological node ordering. It also distinguishes an absorbing event from
censoring, while post-event/censoring data are handled specially. Conversion
must preserve those meanings rather than infer them from column names.

## Exact banking construction

The authored oracle in `tools/ltmle_policy_oracle_20261023.py` enumerates the
four paths of a stipulated two-period servicing law using rational arithmetic.
Let $H$ be a high-risk indicator with probability $1/3$. Let $L_1$ indicate
hardship after the first month's action $A_0$, with
\[
P(L_1=1\mid H,A_0)=
\begin{cases}
1/4&(H,A_0)=(0,0),\\
1/8&(H,A_0)=(0,1),\\
3/4&(H,A_0)=(1,0),\\
1/2&(H,A_0)=(1,1).
\end{cases}
\]
Conditional default probability after the second action is
\[
P(Y=1\mid H,A_0,L_1,A_1)
=1/20+H/10+L_1/5-A_0/25-A_1/20.
\]
An account remains observed with probability $9/10$ when $L_1=0$ and $3/4$
when $L_1=1$. The example contrasts status quo $(0,0)$, a dynamic targeted
rule $(A_0,A_1)=(H,L_1)$, and broad contact $(1,1)$. Exact results are:

| Policy | Default risk | Mean contacts (months 1, 2) | Expected contact cost | Net value vs status quo |
|---|---:|---:|---:|---:|
| Status quo | $1/6$ | $(0,0)$ | USD 0 | USD 0 |
| Targeted dynamic | $3/25$ | $(1/3,1/3)$ | USD $10/3$ | USD $130/3$ |
| Broad contact | $13/300$ | $(1,1)$ | USD 10 | USD $340/3$ |

Net value is $1000(\theta_{\rm status}-\theta_d)-6E(A_0)-4E(A_1)$ per
account. These exact figures demonstrate how a policy mean feeds a distinct
decision-layer objective. They do not include estimation error, model error or
uncertainty in costs. The stipulated minimum observation probability is
$3/4$; it is not an empirical positivity diagnostic or a general guarantee.
The calculation does not call `ltmle`, fit censoring or treatment models,
construct influence curves, or estimate coverage. It is an exact target oracle
for a future matched test, not evidence that the package reproduces the result.

## Alternatives and disposition

The selected code is a useful R semantics reference and possible future
comparator. Direct use as a worker is deferred until the current
cutoff-appropriate source tree and release, resolved dependency versions,
rights, effective variance behavior, exact-oracle parity and adverse regimes
are reviewed. A port to Python, Java or C++ would also have to preserve wide
history order, dynamic rules, event/censoring recoding, outcome scaling,
cumulative propensity bounds, nuisance learner behavior, cluster aggregation
and shared covariance. No accepted product requirement currently pays for
that duplicated implementation burden.

The selected revision is `338c029dae9692ef20714125773da7037688993b`, dated
17 April 2023; its source file and `DESCRIPTION` match the Git blobs in the
complete pinned tree. That package declaration says version 1.3-0, dated
13 April 2023, R >= 3.1.0, imports `Matrix` and `matrixStats`, suggests
`SuperLearner` and several development/reporting packages, and declares GPL-2.
Repository metadata separately records a later push on 3 June 2026. The
selected file therefore remains a historical source observation, not proof of
the latest code or published release. The supplemental delegate retrieval
failed at DNS; its receipts are preserved and do not support an absence claim.

`lmtp` and `gfoRmula` are distinct engines with different treatment maps,
history and uncertainty contracts. They are useful comparisons, not aliases
that inherit this decision. The present disposition is **reference only**:
no package worker, adapter, port, integration permission, calibrated
capability, bank validation or product adoption is selected. Revisit when a
prototype has a specified longitudinal target and needs a native R comparator,
and after current source identity, dependency rights and a frozen matched
qualification protocol are available.

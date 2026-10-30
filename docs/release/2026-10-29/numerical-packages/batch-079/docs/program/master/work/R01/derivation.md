# R01: randomization information and independent calendar replication

This is project algebra for a changed experiment. It does not repair the old
single-calendar interval by a universal multiplier. The inherited target is
V = (theta_0 + theta_1)/2 - C, with the same horizon-six monetary weights and
truthful sampled linked histories. The two equally sampled synthetic strata
have the same response curve; unequal sampling would require known stratum
weights in the score.

## Why the old pilot can affect calibration

For a stratum, write fitted action and outcome errors as d_m and d_l relative
to their true conditional means. Conditional on an independent pilot, the
population ratio is (theta + E[d_m d_l])/(1 + E[d_m^2]) when the action
innovation variance is one. Its bias is therefore
(E[d_m d_l] - theta E[d_m^2])/(1 + E[d_m^2]). A residual calendar variance
does not estimate this conditional mean shift. A small-sample degrees-of-
freedom change cannot remove it, and false exogeneity changes theta itself.
The old growing-pilot argument makes the bias second order asymptotically;
it supplies no exact finite correction. The independently sampled origin
audits add conditional mean-zero noise, diagonal only in their own audit
randomization. They do not remove the latent calendar contribution.

## Changed information and estimator

Suppose the action really is randomized as A = m(X) + v with supplied m(X),
E[v|X] = 0 and E[v^2|X] = 1. The study uses the inherited m(W) = .5W +
.2(W^2-1). This is additional assignment information, not knowledge inferred
from a declaration. Observe K independent calendars, each with L consecutive
origins and all H future outcomes. Calendar replication means independent
drivers, actions, balance initialization and shocks. Adjacent calendar blocks
or branches sharing a national shock do not satisfy this experiment.

Keep a separate invariant pilot P. It tunes and fits the inherited outcome
dictionary and produces l_hat and a scalar control b_hat. They can be poor
fits: only their independence, finite moments and dependence on preaction X
are used for unbiasedness. Set b_hat to the pilot mean of v times the audited
monetary outcome. With Z = B + R(F-B)/q, define

    G_t = v_t {w' Z_t - l_hat(X_t)} - b_hat (v_t^2 - 1).
    U_k = average of G_t over calendar k; V_hat = average U_k - C.

Conditional on P, E[v l_hat(X)] = 0 and E[v^2-1] = 0. The audit identity
and exogenous innovation response give E[v w' Z] = theta, so E[U_k|P] =
theta exactly. Neither a fitted action-mean bias nor a random denominator
remains. The control removes part of the action-square variance without
changing the mean, including when b_hat is inaccurate. It does not repair
wrong q, wrong labels, endogenous actions or nonindependent calendars.

The conditional variance of U is L^-2 times the sum of all within-calendar
score covariances. No covariance window is estimated. The sample variance
of K independent U's divided by K estimates the conditional variance of
V_hat unbiasedly, provided the variance is finite. The variance across
pilots of E[V_hat|P] is zero; pilot uncertainty affects dispersion, which
the replicate variance estimates, rather than inducing an omitted common
mean shift. Conditional iid CLT and variance consistency as K tends to
infinity give a normal pivot. L can remain fixed. A Student critical with
K-1 degrees of freedom converges to the same critical. It is **not an exact
Student pivot**, because each calendar mean is not Gaussian.

## Candidate, challenger and finite claim

Freeze K=24, L=50 (L=12 for small histories), four times as many independent
pilot origins as evaluation origins, and a 99% Student interval. Choosing
99% before final draws provides a deliberate coverage/width tradeoff against
the 95% inherited normal interval. It is not called a corrected exact 95%
procedure. Both methods see identical pilot and evaluation rows. The old
challenger stacks independent calendars and applies its existing horizon
covariance; that is a computational comparator with artificial boundary
terms, not new evidence validating its original uninterrupted-calendar law.
The prior 4,800-request uninterrupted-calendar study remains the historical
baseline, including exact-rank coverage 559/600 and all adverse results.

There are six valid cells: baseline, short histories, low q, near rank,
exact rank and persistence. Three separate adverse cells violate exogeneity,
inclusion or truth. Each has 512 fresh requests. At anticipated coverage
95%, simultaneous two-sided Clopper-Pearson bounds over 18 comparisons have
less than .04 absolute Monte Carlo error; this is a design calculation,
not a guaranteed realized interval width. The finite screen requires a
simultaneous one-sided lower bound of at least .95 in every valid primary
cell and at least .99 finite availability. Report actual widths without
inventing a bank utility threshold. Even a passing grid supports only the
specified conditional asymptotic experiment, not uniform finite coverage.

## Independent checks and limitations

The fixture enumerates three-point action innovations with exact variance
one, both identity orderings and audit selections. Direct weighted sums
must recover the target for arbitrary independent pilot predictions/control;
a wrong inclusion probability must change the mean. Dense pilot fitting is
separately checked against the QR path. Swapping candidate names with audit
labels must preserve scores. All outputs and requested work are retained.

Information cost includes K independent calendars, evaluation/pilot labels,
stored candidate horizon rows and extra simulation initialization. Calendar
replicates need authentic independent economic units; we cannot manufacture
them by splitting a bank series. Actual availability, acceptable width and
prices stay external. The new identities and asymptotic reasoning are project
derivations. Inherited orthogonality/source roles and original PDFs remain in
docs/literature/calibration-source-review.json; no new literature theorem or
search is claimed.

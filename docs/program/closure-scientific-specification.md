# Scientific specification before final evaluation

10 October 2026. The registered sizes and seeds are in
[closure-spec.json](../studies/closure-spec.json). The baseline plan specifies
the nonlinear and structural families. These are additional information
experiments, not claims that more computation identifies the old observations.

## Persistent independent pairs

Pair i supplies H randomized actions A_it in {-1,1}, two candidate outcome
trajectories, and one unknown fixed map M_i. Define U_i as the mean over dates
of A_it Y_focal,it. The population focal unit response is theta=E U_i. Auditing
reveals M_i and its linked outcomes, with R_i Bernoulli(q_i) conditionally
independent given the complete pair, q_i known and bounded below. Set T_i to
the candidate-average action/outcome moment and use

    Z_i = T_i + R_i/q_i (U_i - T_i).

Conditional expectation over R gives U_i, so E Z_i=theta even for a persistent
map. The sample mean and independent-pair sample variance identify and estimate
theta and its CLT uncertainty. Within-pair dates need no independence. A fixed
positive monetary scale multiplies both estimate and endpoints. With an
independent symmetric map-label flip of known probability e<1/2, replace map
sign 2M_i-1 by (2L_i-1)/(1-2e). This unbiased correction does not identify e;
it must come from independent gold validation. If e is itself estimated its
influence must be added; that extension is not silently included here.

Uniform audits, unequal known inclusion, persistent erroneous aliases, noisy
labels, false assertions and falsely declared audit inclusion are distinct
fixtures. Audited-only means and date-level variance are adverse challengers.
Shared calendar shocks are deliberately rejected by this independent-pair API.

## Linkage confidence and diagnostics

Let m=(s0,d0,s1,d1), where s and d are candidate average and half-difference
responses in money. Let V estimate its covariance. The ellipsoid is
(x-m)' V^-1 (x-m) <= chi2_4(1-alpha/2), with an explicitly full-rank response
limit. Each p stratum receives an exact binomial interval with error alpha/4.
At nonzero ranks r_j=2p_j-1 the focal functional is

    c(r)' x - cost,   c(r)=(1/2, 1/(2r0), 1/2, 1/(2r1)).

Its extrema at a fixed r are c'm +/- sqrt(critical*c'Vc)-cost. On the rectangle
of reciprocal ranks the upper support is convex and lower support concave.
Every interior point is a convex combination of vertices, so the upper maximum
and lower minimum occur at vertices. This proves a global outer interval; no
local optimizer is required. If either rank interval contains zero we return
the whole line, explicitly foregoing potential disconnected precision. A
degenerate empirical V also receives this conservative fallback; a pseudoinverse
does not assert a four-dimensional pivot. Union-bound inclusion yields the
stated asymptotic confidence claim. Floating-point special-function inversion
is tested numerically, not claimed to be certified interval arithmetic.

Retained-draw diagnostics separate known versus estimated audit probabilities,
oracle linearization versus plug-in inverse, and response versus audit variance.
These arms can show contributors to undercoverage; they do not establish a
unique cause. A fresh Gaussian primitive-law experiment has known covariance
and truth; it tests projection behavior separately from calendar HAC calibration.

## Nonlinear decisions

Use the baseline S-transition with rho S+gamma tanh(S)+beta A, O=S+e,
clipped logistic private logger, linear state/action reward and positive Gaussian
noise variances. Initial mean and variance are unknown. Full labelled independent
trajectory audits identify each regression, variance and logger under full-rank
designs and action support. The unlabelled likelihood integrates the product of
initial, signal, private-action, reward and transition densities. Labelled
likelihood is the same product evaluated at the audited states. Joint scores
and information include both samples. Parameter bounds and stability are stated
before fitting; boundary/local-mode failures are retained.

An independent pilot selects among observable signal policies; evaluation freezes
that policy. The decision target is conditional policy value, not unknown optimal
value. Reward units are thousands of currency units. Quadrature resolution and
domain comparisons check likelihood, score and value. Gaussian assumed-density
and particle challengers retain the private action likelihood. The exact Gaussian
limit sets gamma=lambda_s=0; observation-dependent action likelihood is then
known conditional on O. No empirical tolerance is called a proved error bound.

## Finite temporal graph class

Start with three time-ordered observed nodes (encouragement Z, action A, reward
Y), at most one latent Gaussian root, and independent Gaussian episodes. Use
Sigma=(I-B)^-1(ll'+D)(I-B)^-T and theta=[(I-B)^-1]_(Y,A).
Enumerate optional time-respecting edges and latent supports. Construct a
simultaneous covariance region from normal sample-variance chi-square intervals
for coordinate sums and differences (Bonferroni), with observed means nuisance.
Project necessary covariance restrictions conservatively through every allowed
graph. With unrestricted confounding, return a whole-line witness; with a
prespecified valid randomized encouragement/exclusion, theta Sigma_ZA=Sigma_ZY
gives a globally calculated outer ratio set. The relaxation can retain graphs
that a sharper structural calculation would exclude; coverage does not need
their removal. Zero first-stage compatibility is retained, not thresholded away.

Hidden confounding, weak encouragement, false exclusion, omitted prior history
and ambiguous structure are retained adverse cases. Exclusion is supplied
information, never credited to automatic discovery. This is a finite-episode
construction, not general dependent time-series confidence.

## Dependent learning and execution

Use the existing bounded, geometrically absolutely regular partially linear IV
score and separated-block sparse construction, with fixed dictionary and declared
nuisance rates, gap and fitted-score covariance conditions. Make this an explicit
operation; do not attach it to persistent-pair inference. Keep training-only
tuning and whole lag/outcome windows. Compare oracle, sparse, finite-basis and
misspecified alternatives on the same target.

Stream immutable source partitions and checkpoint sufficient-statistic passes,
retaining complete observation, fold, procedure and contribution identities.
Restart, retry, duplicate and partial-write fixtures must reproduce serial
results or fail explicitly. Complete timings include reading, fitting, uncertainty,
reporting and serialization. Physical execution does not change a sampling unit.

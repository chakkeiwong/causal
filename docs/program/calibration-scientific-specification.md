# V9 scientific specification and rate argument

10 October 2026; fixed before final diagnostic/validation draws. This is a
selected construction, not a general dependent-learning or bank-validity claim.

## Population, information and financial target

Use the inherited stationary Gaussian driver W_t with autocorrelation r, action
A_t = .5 W_t + .2(W_t²−1) + e_t, and portfolio balance
B_t = rho B_(t−1) + beta A_t + 1.2 W_t + .4(W_t²−1) + nu_t.
The action innovation e_t has variance one and is independent of the complete
driver path, other-date action innovations and exogenous balance shocks nu.
The companion portfolio has beta_d and the same shocks. Origin-specific strata
and complete-horizon swaps are independent of these histories; stratum s has
correct-map probability p_s. This is not a persistent customer-map experiment.
Independent binomial gold audits estimate the two p_s. No selected or asymmetric
label error is silently included.

The one-month price intervention keeps natural future assignment unchanged.
The focal response at horizon h is beta rho^h. The fixed monetary value is
sum_h w_h beta rho^h minus the inherited direct repricing cost, using
FundingTarget's balance units, branches, discounting and margin. Its comparison
does not optimize the action, policy or reporting horizon after seeing outcomes.

The fast generator replaces the mean of 48 independent Gaussian branch noises
by its exactly equivalent scalar Gaussian, preserving the shared focal/decoy
shock law, zero initialization and inherited burn. An independent literal
48-branch recursion with coupled innovations checks this reduction. Stationary
mean and bias formulas are population formulas; finite burn is an approximation
to that stationary law, not a claim of exact finite-sample stationarity.

## Exact nuisance means and conditional pilot target

Write x_t=(1,W_t,W_t²−1), Q=E[x_t x_t']=diag(1,1,2),
c1=.5 beta+1.2 and c2=.2 beta+.4. The stationary conditional balance mean at
h=0 has coefficients a0=c1/(1−rho r) and b0=c2/(1−rho r²).
For h≥1, a_h=rho a_(h−1)+c1 r^h and
b_h=rho b_(h−1)+c2 r^(2h). These include the infinite pre-origin balance
history and natural future assignment. Mix focal and companion means using
p_s to obtain each candidate's outcome coefficients. The action coefficients
are (0,.5,.2). An independent infinite geometric sum checks all horizons.

Condition on an independently fitted pilot. Let delta_a and delta_y be its
action and candidate-outcome coefficient errors in one stratum. Orthogonality
of e_t and x_t gives the exact stationary population residual-regression ratio

eta_M = (eta + delta_a' Q delta_y)/(1+delta_a' Q delta_a).

Thus eta_M−eta = delta_a' Q(delta_y−eta delta_a)/(1+delta_a' Q delta_a).
An independently integrated Gaussian residual-product calculation checks this
identity. Correct action means eliminate this population bias even if outcome
predictions are imperfect; knowing only the outcome mean does not eliminate
the action-error square. The identity is a conditional population target, not
the expectation of a finite-sample ratio or of an estimated inverse audit map.

For fixed dimension, nonsingular Q, finite moments and a stable mixing pilot,
coefficient errors are O_p(M^(−1/2)) with bounded ridge penalties. The target
remainder is O_p(M^(−1)); root-T inference for the desired response therefore
requires sqrt(T)/M -> 0, along with the usual moment/CLT conditions. A fixed
M is not justified by calling the score orthogonal. For a growing Bartlett
window L, L/sqrt(M) -> 0 is a sufficient fitted-score covariance control under
uniform moment bounds, in addition to the population covariance conditions.
These are sufficient rates for this selected model, not necessary rates for
every learner. Fixed audit size similarly prevents an audit-asymptotic claim.

The diagnostic grid holds evaluation draws, probability and audit counts fixed
within each T, uses nested independent pilot prefixes, and switches known
action/outcome means independently. It reports the exact conditional shift,
empirical bias/SD, estimated SE and estimated/known-audit coverage for both
covariance rules. Known information remains diagnostic synthetic evidence.

## Joint regression and the covariance horizon

Within each stratum regress both candidate horizon vectors on the fixed x_t and
A_t jointly. Frisch--Waugh residualization gives the same action coefficient as
partial regression using the evaluation-sample projection of A on x. This is a
fixed-dimensional joint estimating equation; its uncertainty includes estimation
of all regression coefficients. It does not reuse an adaptive dictionary selected
from evaluation outcomes. Outcome means may contain additional predictable
structure if the specified action mean and innovation moment remain correct.

Let e_t=A_t−x_t'alpha, q_s=E[1{S_t=s}e_t²], and epsilon_st be the residual of the
population joint projection for a candidate outcome. The action-coefficient
influence is 1{S_t=s}e_t epsilon_st/q_s. Rank, finite 4+delta moments, stationary
mixing sufficient for a score CLT and nonsingular regression moments are assumed.
The Gaussian stable mechanism satisfies these away from persistence one. Its
estimated-regression influence is consistent for the population influence.

There is an additional, decisive filtration condition. Conditional on the
complete exogenous driver path and all shocks strictly before t, averaging over
the date-t innovation, independent origin swap and shocks through t+H makes
this score mean zero. Its random action/balance inputs are measurable through
t+H. If s>t+H, the earlier score is measurable before s and the conditional
expectation of the later score is zero. Therefore Cov(psi_t,psi_s)=0 for s−t>H.
This argument uses exogenous innovations, noninformative swaps, the correct
action mean and the linear finite-horizon response; H alone is insufficient.
The score process need not itself be H-dependent.

Consequently Omega=Gamma_0+sum_(k=1)^H(Gamma_k+Gamma_k') is the long-run
covariance. Fixed-H empirical lag products consistently estimate it; plugging
in fixed-dimensional OLS residuals changes each moment by o_p(1). Bartlett
weights at a short window attenuate nonzero horizon covariances. Untapered
finite-H sums avoid that attenuation in this law, but can be nonpositive for
a scalar contrast in finite samples. Such a request is unavailable; no clipping
or general positive-semidefinite matrix assertion is made. A finite toy
enumeration illustrates the conditional argument without replacing its proof.

After inversion of the two mapping matrices, the monetary scalar is a smooth
linear contrast in the fitted candidate responses conditional on p. Its
p_s derivative is .5 sum_h w_h(eta_(s,2,h)−eta_(s,1,h))/(2p_s−1)².
Add its independent binomial variance p_s(1−p_s)/n_s. For regular inference
the p_s lie away from 0, 1 and .5, and T/n_s tends to a finite constant.
The Wilson rank guard is retained; all-failure/all-success audit boundaries
also return unavailable. No uniform validity near singular mapping is claimed.

## Complete execution and external qualification

Grouped QR reduces blocks of [x,A,Y] to small triangular factors. From those
factors recover the action projection, full regression coefficients and residual
action sum of squares. A second input pass forms only the scalar monetary score.
For each lag store its raw product sum, total score, first/last H scores and
count. If score mean is mu, the centered lag sum is
raw_k − mu(2 total − first_k_sum − last_k_sum) + (T−k)mu².
This handles global centering and cross-chunk pairs without retaining T scores.
Working state is O(block_size times fixed width + H + fixed width squared);
input storage and resident mapped pages are not eliminated.

Dense SVD/direct centered covariance is the independent numerical comparator.
Full fresh processes measure both methods twice at 120,000 and 1,200,000 dates,
including input hashing, import, fitting, inference and output read-back.
The request journal resumes completed requests; an interrupted unfinished fit
is rerun from its immutable input. There is no claim of distributed recovery or
resuming a partially completed fit. The lag accumulator's serialized state is
separately checked. External users, bank data and platform qualification remain
pending under the preserved V8 protocol plus the new operation's requirements.

# Scientific specification before V8 evaluation

The target is an average unit-action response, converted by a fixed monetary
scale. Pair index i and date t refer to different independent-information
dimensions. Let U_it be the correctly linked focal action-outcome moment and
T_it its two-candidate average. A persistent audit R_i has known inclusion
q(X_i)>0. With accurate labels, Z_it=T_it+R_i(U_it-T_it)/q_i has conditional
expectation U_it over audit randomization. Action randomization and the stated
outcome law identify E U_it as the causal response; the audit identity alone
does not establish that causal premise.

## Joint pair/calendar inference

Assume Z_it=h(W_i,C_t,E_it), where W_i are iid persistent pair attributes
(including audits/maps), C_t is a stationary mixing calendar independent of
the W_i, and E_it are conditionally independent innovations. Moments above
order two and summable calendar covariance are required. Write
Z_it-theta=a(W_i)+b(C_t)+r_it, with both conditional projections of r zero.
Then the mean error is mean(a)+mean(b)+mean(r). Cross-pair residual covariances
vanish conditionally on the calendar; the remaining interaction variance is
O(1/(NT)). Under comparable N,T growth and nonzero first-order variance, the
independent iid and mixing central limits give variance sigma_a^2/N+Omega_b/T.

Estimate the first term using the variance of pair means divided by N and
the second using Bartlett long-run variance of date means divided by T.
Interaction variation can be counted twice at order 1/(NT); no exact finite
sample claim is made. Sufficient bandwidth restrictions include L increasing,
L^2/min(N,T) tending to zero and summable covariance tails. Degenerate leading
projections require a different limit theory and are excluded.

For independent symmetric label flips with probability epsilon<1/2, replace
the selected moment with (V0+V1)/2+(2L_i-1)(V0-V1)/(2(1-2epsilon)). A separate
gold-label sample estimates epsilon. The derivative of Z_it is
R_i(2L_i-1)(V0-V1)/(q_i(1-2epsilon)^2). Its grand mean multiplies the validation
sample's Bernoulli influence. Add the independent variance g^2 epsilon(1-epsilon)/M.
This uses both sample rates and a Taylor remainder; error-rate uncertainty
touching 1/2 prevents regular inference. Asymmetric or selected errors need a
new model. False inclusion laws are retained adverse cases, not detectable facts.

## Audit budget and precision

The audit-randomization contribution for a complete-pair difference D is
E[(1/q(X)-1)D^2]. At expected cost E[c(X)q(X)]=B the interior solution is
q(X)=lambda sqrt(E[D^2|X]/c(X)), capped at one and a declared positive floor.
An independent fully audited pilot estimates the conditional second moments.
It solves a pilot variance objective, not a certified population optimum.
Evaluation uses new pairs/calendars and matched expected costs. A calendar
variance floor survives even if all pairs are audited.

## Finite Gaussian effect confidence

Under observed sufficiency and ordered Z,A,Y, the action coefficient in
E[Y|Z,A] is the causal target throughout the declared graph class. Conditional
Gaussian regression yields a t pivot with n-3 degrees of freedom, without
selecting a graph. Under valid encouragement, regress A and Y separately on
an intercept and Z. Let slopes be a,y, centered Z sum of squares k, and residual
sums Saa,Say,Syy. Inverting the null that Y-theta A has zero Z slope gives
(y-theta a)^2 <= t_(n-2)^2*(Syy-2theta Say+theta^2 Saa)/((n-2)k).
Solve this quadratic inequality globally, preserving bounded, two-ray,
whole-line and empty outcomes. The true-null errors are independent Gaussian
given Z under the supplied experiment; no first-stage lower bound is needed.
The unrestricted latent class still supports every real effect by the V7
witness. These new pivots replace the previous confidence event, not intersect it.

## Model and learner extensions

The nonlinear model has q(A)=exp(log_q0)*(1-A)+exp(log_q1)*A in its transition
variance. Complete representative labelled transitions with both actions
identify each variance after identifying the transition mean. Main trajectories
integrate states; audited trajectories evaluate the same factors directly.
All 16 score directions and the frozen policy's interventional value are checked.
Interior joint sandwich inference includes both independently sampled groups.

The learning dictionary is fixed as (1,X,X0*X1). Under bounded geometric mixing,
positive population Gram and IV slope, correct nuisance specification and fixed
dimension, separated OLS nuisance errors are O_p(n^-1/2); their orthogonal
product is O_p(n^-1), and a slowly growing covariance window controls fitted
score error. This is a conditional selected-dictionary result. Chunked QR of
[design, three targets], followed by QR reduction of the small R factors,
preserves the least-squares objective up to floating-point error. Inference
uses the same held-out blocks and full score covariance as the dense reference.

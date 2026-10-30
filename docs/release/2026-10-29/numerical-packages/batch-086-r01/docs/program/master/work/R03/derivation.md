# R03: nonlinear servicing with a supplied private logger

## A selected17 extension and its information clock

Extend the inherited selected16 action-variance family by adding
eta_tanh A_t tanh(S_t) to the reward mean. The state evolves as
S_(t+1) = rho S_t + gamma tanh(S_t) + beta A_t + sqrt(q_A) epsilon_t.
The observation is O_t=S_t+sqrt(v_o) nu_t. After observing private S_t and
public O_t, the logger draws A_t with probability
.05+.9 logistic(lambda_0+lambda_s S_t+lambda_o O_t). Reward follows the
extended mean plus independent Gaussian noise. Stability requires
|rho|+|gamma|<1; the finite-horizon study has three decisions. A deployed
policy sees O_t, not S_t, and uses independently frozen thresholds.

The new information route asks for representative truthful full-state audited
trajectories and actual logger probabilities. It does not assume the bank's
public signal reveals the private state. These probabilities are supplied
by an authentic randomization/logger record; replacing them by fitted or
guessed values needs additional influence terms and is not this method.

## Likelihood, identification and alternative estimator

The complete labelled likelihood is the initial Gaussian density times the
product of observation, logger Bernoulli, reward and state-transition
densities. With a positive fraction of representative gold trajectories,
both actions have positive probability on a full-support state/signal law.
The transition regressors S,tanh(S),A and reward regressors
1,S,A,SA,A tanh(S) are linearly independent on that support. Gaussian
conditional means and variances then identify the transition, emission,
reward and initial parameters; logistic probabilities identify logger
coefficients. The audit orientation fixes the state label and units.
Zero representative audit probability or arbitrary mismeasured state truth
does not inherit this argument. The unlabelled likelihood remains a latent
integral, but is not required by the estimator chosen here.

For a fixed observable policy pi, let
W_t = product_{j<=t} 1{A_j=pi_j(O_j)}/p_j(A_j|S_j,O_j).
Sequential change of measure, integrating one Bernoulli action at a time,
gives E[sum gamma^t W_t R_t] = V(pi). The target is USD 1000 times expected
discounted reward per audited trajectory, with gamma=.97. This argument
holds for the nonlinear action-dependent transition and nonlinear reward,
including misspecified transition equations, provided the logger ratios
and audit representativeness are true. Independent full trajectories are
the sampling units. The sample variance includes all within-trajectory
reward dependence; there is no fitted-filter variance omitted.

The probability floor bounds each weight by .05^(-H), and finite Gaussian
moments give finite contribution variance for fixed H. The trajectory CLT
and consistent sample variance justify an asymptotic interval. The 99%
Student critical is deliberately wider than the paired 95% challenger;
neither is an exact t interval for this weighted distribution. Poor overlap
can make convergence slow even when a floor exists. All-request coverage,+width, effective weighted sample size and maximum weight are retained.

## Numerical scale and limits

The deployed estimator performs finite products and sums and has no
quadrature or likelihood optimization error. Complete likelihood is checked
against an independent Gaussian/Bernoulli density calculation, and its score
against finite differences. Synthetic reference values are computed by
high-resolution state-grid integration and independently by nested
Gauss-Hermite integration. Differences at refined grids are diagnostics,
not a global integration certificate. The frozen reference difference must
be below USD .01. A finite global integration certificate for arbitrary
parameters or an optimizer is not claimed or needed for direct weighting.

This choice resolves a fixed-policy identification route using stronger
logger/audit information. It does not prove the old hidden-state MLE globally
accurate or propagate uncertainty for an estimated logger. The inherited
likelihood method is an information-efficiency alternative, not a paired
method in this study, because it estimates a different unknown logger from
unlabelled plus labelled histories.

## Fixed policies and the optimal-value gap

Evaluation rejects a policy marked as chosen from these same trajectories.
That flag cannot detect concealed reuse of data. A separately selected policy
is valid conditional on its training data. Its value is not the unknown
optimal value over all history policies. Uniform off-policy control or a
finite prespecified policy family with simultaneous bands could support a
different target, but is not inferred from this pointwise argument. The
optimal-policy gap remains open explicitly.

The study includes weak observation, scarce audits, poor overlap, incorrect
logger probabilities, declared policy leakage and transition misspecification.
The last is a substantive robustness check for the weighting identity, not
a claim of robustness to false assignment probabilities or audit truth.

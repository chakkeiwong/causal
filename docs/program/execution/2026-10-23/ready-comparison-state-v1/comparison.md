# Compare hidden-state computation with the causal decision it supports

A hidden credit state can help predict default, but a servicing action changes
a mechanism. State inference, parameter inference, state observability and
causal identification are different obligations. A supplied model can answer
a conditional question accurately while omitting the action-selection law or
using information unavailable at the decision time. The software comparison
therefore binds the model, intervention, initial population, logger and
information clock before assessing numerical quality.
\citep{exec22_state_reference,exec19_dynamax_reference}

## Conditional-state and commercial alternatives

The selected Dynamax commit 5098927f2c377c0dd548cda750e6f1436220aac6, dated
29 September 2026, supplies a Python/JAX HMM reference. Its wrapper sends initial
probabilities, transitions and emission likelihoods to the filter; it does not
automatically insert an observed-action likelihood. This is appropriate for
a declared conditional-input experiment, but privately informed action
selection can require another factor. Its generic wrapper constructs
time-varying transitions using inputs[1:], while the low-level description
uses source-time indexing; the standard transition component accepts inputs
but returns a fixed matrix. A contact array is therefore not evidence that
the selected transition responds to contacts. \citep{exec19_dynamax_source}

GeNIe's inspected DBN profile models a stationary discrete-time process and
fits parameters by EM in supplied structure; the selected learning page
excludes dynamic structure learning. Time-column/node matching and ignored
existing evidence during that operation are conversion requirements.
SMILE's C++ tutorial distinguishes initial and transition tables, lag order,
unfolded slices, outcome indices and flattened slice/outcome arrays. A wrapper
in Python, Java or R must preserve these meanings rather than merely the
array dimensions. \citep{exec13_ct_genie_dbn,exec13_ct_genie_learning,exec13_ct_smile_tutorial}

Stata sspace estimates linear state-space parameters through Kalman or diffuse
likelihoods with the documented time-invariant matrices and Gaussian,
serially uncorrelated disturbance assumptions. Robust variance options do not
make an action regressor exogenous. Its prediction interface distinguishes
past-only prediction, current-data filtering and full-sample smoothing;
changing the prediction sample can change the recursive states. The reported
prediction RMSE excludes parameter-estimation error in the inspected profile.
\citep{exec22_state_stata_sspace,exec22_state_stata_sspace_post}

Stata bayesmh is a separate adaptive Metropolis-Hastings workflow with explicit
likelihoods and priors. Its manual warns that permitted specifications need
not yield a proper posterior and that no single diagnostic proves convergence.
Netica's inspected counting, EM and conjugate-gradient fitting is not itself
a full parameter-posterior sample; local optima remain relevant. Mplus 8.1's
dynamic-SEM addendum supplies another profile with latent centering and
different outcome/residual lag meanings. Its missing-covariate rule can
remove records unless the covariate is modeled as an outcome. The profile's
prior, sampler and licensing details still need a complete release assessment.
\citep{exec22_state_stata_bayesmh,exec13_latent_netica_algorithms,exec13_ct_mplus81}

BayesiaLab's inspected graph-surgery and causal-identification discussions
usefully separate observation and intervention. They require causal information
in a DAG; an analyst drawing that DAG does not verify its truth. Additional
SAS, EViews, HUGIN, Bayes Server and numerical-engine profiles remain separate
coverage obligations, not inferred feature absences.
\citep{exec13_ct_bayesia_inference,exec13_ct_bayesia_identification}

## Observational equivalence survives posterior computation

Let U be a fair hidden favorable state and N an independent Bernoulli(1/5)
noise. In a selection model set A=U XOR N and D=1-U. In a causal model set
A independently fair and D=(1-A) XOR N. Both observable (A,D) tables are
[[1/10,2/5],[2/5,1/10]], so conditional default risks are 4/5 and 1/5.
Replacing only the action equation leaves intervention risks (1/2,1/2) in
the selection model and (4/5,1/5) in the causal model. With USD 1,000 default
loss and USD 100 action cost, universal action has net -100 or 500.
The exact oracle enumerates both laws and their interventions.
\citep{exec22_state_reference}

In a two-model Bayesian analysis with these fixed parameters, likelihoods
are equal for every observed sample. A prior probability w for the causal
model remains w after observation. Expected net is 600w-100, positive only
above 1/6; priors 1/10 and 9/10 give -40 and 440. More draws from a posterior
cannot resolve a causal restriction unlearnable from this likelihood. The
calculation supports explicit prior-sensitive decisions, not an allegation
that Bayesian computation is invalid. \citep{exec22_state_reference}

An independent Dynamax-related fixture makes the omitted logger concrete.
Given a fair latent Z, action A matches Z with probability 9/10 and outcome
Y matches Z with probability 4/5, with independent conditional noises and
no action effect. Conditional outcome means are 37/50 and 13/50, but the
causal contrast is zero. The posterior P(Z=1|A=1,Y=1)=36/37 differs from
4/5 when only the outcome factor is used. At USD 200 per response probability
unit and USD 20 action cost, the associational calculation gives 76 while
the true stipulated net is -20. These are distinct models and information
sets, not recorded native outputs. \citep{exec19_dynamax_reference}

## Preserve clocks, uncertainty and failure states

For a persistent fair hidden H, let two conditionally independent signals
match H with probability 3/4. X0=1 gives filtered P(H=1)=3/4; later X1=0
gives smoothed probability 1/2. If a separately stipulated intervention avoids
default with probability 1/10 when H=1, at USD 1,000 loss and USD 60 cost,
the first-date net is 15. Retrospective smoothing gives -10 using information
not available for that first decision. Filtering itself does not identify the
assumed benefit law. \citep{exec22_state_reference}

Observability is independent of that clock. With F=0.9 I and measurement
H=(1,1), initial states (1,0) and (2,-1) give the same outputs at every time
but different first-minus-second contrasts. A prior can select a representation
without making that contrast observable. Parameter uncertainty also differs
from outcome noise: for theta uniform on [0,1] and two conditionally independent
Bernoulli(theta) future outcomes, the count variance is 2/3 rather than the
1/2 from fixing theta at its mean. Shared unknown parameters induce dependence.
\citep{exec22_state_reference}

Dynamax's inspected normalizer leaves all-zero input all zero, and an
all-minus-infinity emission update lacks a dedicated branch. Source-level
zero-support, transition-index and normalization concerns require native
conformance cases. The fitting wrapper can return supplied parameters and an
empty trace for nonpositive iterations; finite arrays cannot certify fitting
success. Preserve trainable flags, initialization, objective traces, backend
precision, warnings and unsupported states. Its selected tests propose useful
finite-path checks but were not executed in this review.
\citep{exec19_dynamax_source}

The proposed public trial should compare an exact enumerator, a pinned native
engine and the adapter on the same model and information set, including
impossible evidence, unobservable contrasts, informative actions, future
signals and failed fits. Measure approximation and full workflow cost
separately from identification and statistical calibration. Dynamax's MIT
root notice and unpinned direct dependencies require a resolved transitive
environment; commercial manuals do not grant entitlement. Original-engine
reuse is a candidate before a costly port. Native admission, broad source
coverage, actual bank value and final acceptance remain open.
\citep{exec19_dynamax_source}

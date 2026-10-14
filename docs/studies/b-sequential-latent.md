# B: sequential and partially observed decisions

Specification v1, 8 October 2026. Target: eight-period discounted collections
contribution contrast between prespecified assistance policies for an initial
eligible population. Eligibility belongs in the history. Rewards include
repayment, action cost and terminal loss without double counting.

B-H retains the existing three-state collections law as an exact reference,
but compares complete backward fitting and trajectory-level inference.
Estimate propensity and continuation functions on whole-trajectory training
folds. Use cumulative weights in sequential augmentation, retain policy
contrast covariance, and compare direct g-computation, IPS and bounded
targeting where appropriate. Censoring and competing events have separate
targets. Shared calendar shocks are a separate repetition law and cannot be
handled by merely retaining the trajectory standard error.

B-L uses a controlled finite-state observation law with signal, transition,
reward and logger factors. Establish identification for the fitted
unknown-emission model under exogenous randomized logging. Use a baseline
action observation block for emission/state recovery and cross-action
moments for transitions where the rank argument supports it. State the
initial-law, stationarity, rank and label assumptions exactly. Compare the
construction to the known-emission reference before interpreting a fit.

Fit by scaled forward/backward EM and compare a direct likelihood optimizer
or other mathematically aligned route. Derive an observed information or
refit bootstrap construction and propagate it into a fixed history-policy
value. The policy's stored history-to-action mapping stays fixed in
evaluation, even when its training used a belief filter. Derive value and
numerical error on the actual observation/belief process.

Adverse cases vary emission separation, action support, private logging,
model order, initialization and optimizer tolerance. An accurate likelihood
does not settle causal equivalence. Report selected-fit caps, unconditional
failure rates, parameter recovery up to labels, value errors and interval
behavior. Selected optimal policies require distinct evaluation evidence.

Existing primary copies: hernan2020, targeted2018, sequentialdr2018,
jiang2016, rabiner1989, hmmident2016, sarkka2013, kaelbling1998,
bennettprox2023 and opehard2026. Reading priorities are controlled
identification, parameter likelihood derivatives and fixed-policy inference.
The private logger/proxy extension must retain its additional assumptions.

Completion requires matching identification to fitting and uncertainty,
not only implementing EM or solving a supplied POMDP.

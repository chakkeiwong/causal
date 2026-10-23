# Match effect estimators to the population and action contrast

For a servicing action A, baseline information X and potential contribution
Y(a), a conditional effect tau(x)=E[Y(1)-Y(0)|X=x] is distinct from its
average over all eligible customers, historical recipients or a future
policy's population. A continuous dose additionally requires a specified
curve or action pair. Consistency, exchangeability, support, interference
and the information clock precede nuisance learning. Cross-fitting or a
well-fitted outcome model cannot establish those premises.
\citep{exec20_rfx_reference,exec20_python_effect_reference}

## Available estimation routes have different contracts

Python EconML's inspected DML route residualizes treatment and outcome and
fits an effect model; its projection restrictions remain when predictions
are averaged. CausalML's reviewed T-learner fits arm-specific responses and
averages over the supplied prediction population, with treatment-label order
and bootstrap unit preserved. Statsmodels TreatmentEffect supplies IPW,
regression adjustment, augmented IPW, weighted augmented IPW and IPW-RA in
the reviewed parametric paths, including joint nuisance moments for inference.
They should be compared at a matched target, not declared interchangeable
because all return an effect. \citep{exec19_econml_source,exec14_causalml_primary,exec20_python_effect_source}

R DoubleML is a distinct R6/mlr3 implementation. Its ATE and ATTE scores
use different nuisance and fold quantities; propensity clipping is not a
new trimmed target. Global tuning and tuning within folds are separate
settings. Its cluster partitions and variance paths do not qualify arbitrary
dependence, and the reviewed bootstrap rejects clustered data, preventing
its bootstrap-based joint intervals in that configuration. R grf exposes
conditional forests and several average targets; its all-sample variance
aggregates centered scores by declared clusters, while its selected TMLE
average-effect path rejects clusters or sample weights. Honesty, nuisance
splitting and sampling-unit covariance solve different problems.
\citep{exec20_rfx_doubleml_r,exec13_grf_rpath}

The C++ comparison extends grf's R/native boundary with bcf, XBCF and
flexBCF. Bayesian tree priors, likelihood precision, outcome standardization,
treatment coding and joint posterior draws are part of these procedures.
An objective-Bayes correction inside grf's variance code does not turn
it into a Bayesian causal forest. Porting a tree kernel while dropping
prior scales or draw alignment would change the method. The initial
proposal favors narrow original-engine interfaces after qualification.
\citep{exec21_cxx_grf,exec21_cxx_bcf,exec21_cxx_xbcf,exec21_cxx_flexbcf}

Java H2O's selected uplift builder uses two-level categorical treatment and
binomial outcomes but rejects weights, offsets, fold columns and positive
built-in cross-validation counts on the inspected route. Its arm predictions
and their difference support a specific ranking/contrast workflow; AUUC is
not itself a causal monetary value or an uncertainty interval. Tetrad's
graph-compatible effects answer a separate graph-class question. Source
hazards in H2O's selected KL expression and nonsplitting branch require
focused native checks before adoption, not an unreviewed literal port.
\citep{exec20_javaeffects_h2o,exec20_javaeffects_tetrad,exec20_javaeffects_reference}

Julia CausalELM, CausalForest, TMLE and CausalTables supply additional point,
targeted and supplied-model routes. The reviewed CausalELM uncertainty
expression has squared outcome units and a null assignment sampler that
does not preserve a fixed-treatment-count design. CausalForest's honest
tree sampling does not make earlier nuisance fitting independent, and its
point predictions do not supply covariance. Julia TMLE's actual resampling
and weighting defaults must be bound explicitly. These findings justify
scoped rejection or additional qualification of the affected paths.
\citep{exec21_effects_causalelm,exec21_effects_causalforest,exec21_effects_tmle,exec21_effects_reference}

## Exact population and score differences can reverse a decision

Let low/high-risk groups be equally common, with offer probabilities 1/4
and 3/4 and effects USD 20 and USD 80. The ATE is 50, ATT is 65 and
untreated-population average is 35. At cost USD 55, their net averages
are -5,10,-20. The favorable ATT cannot be used to justify universal
treatment; it averages over a different historical population.
\citep{exec20_python_effect_reference}

Even perfect nuisances do not turn every residual coefficient into ATE.
For Y=m_0(X)+A tau(X)+epsilon, with zero conditional error mean and
e(X)=P(A=1|X), residual regression targets
E[e(X)(1-e(X))tau(X)]/E[e(X)(1-e(X))]. Equal groups with effects (-4,12)
and propensities (1/2,1/10) yield ATE=4, ATT=-4/3 and residual coefficient
4/17. At cost 2, the population margin is 2 while misusing the residual
coefficient gives -30/17. Exact enumeration replays these different
targets. Flexible learning and cross-fitting do not remove the distinction.
\citep{exec21_effects_causalelm,exec21_effects_reference}

For the AIPW score using working propensity q and outcome functions m_a,
conditional bias is (p-q)[(mu_1-m_1)/q+(mu_0-m_0)/(1-q)]. Clipping a
correct p can remove one route to zero bias. At p=1999/2000, q=999/1000,
mu_0=20, mu_1=80 and deliberately incorrect m_0=m_1=0, the true effect
is 60 but the expected clipped score is 69970/999, about 70.04. At cost
65, the true margin is -5 and the clipped-score margin about 5.04.
Correct outcome functions restore the expected score to 60. This is an
exact score witness, not a claim that a fitted native estimator chose
these zero functions. Report clipping, overlap, retained population and
target weights rather than calling clipping a support repair.
\citep{exec20_python_effect_source,exec20_python_effect_reference}

## Dose response and portfolio uncertainty need complete transformations

Under a continuous conditional model with slopes 1 and 3 and treatment
variances 1 and 4 in equal groups, the residual slope is 13/5 while the
average slope is 2. A nonlinear dose curve introduces another distinction:
for W uniform on [0,2] and Y(w)=20w^2-5w dollars, the projection slope
is 35, derivative at zero -5 and contrast from zero to one 15. CausalGPS
and causaldrf provide relevant continuous-exposure routes, but densities,
units, response support and the entire location-scale transformation must
survive conversion. A binary-treatment result cannot qualify these families
by association. \citep{exec20_rfx_doubleml_r,exec20_rfx_causalgps,exec20_rfx_causaldrf,exec20_rfx_reference}

For Bayesian portfolio effects, average customers inside each joint draw
before taking quantiles. Joint draws (-2,6) and (6,-2) give a portfolio
effect exactly 2, while averaging marginal endpoints yields [-2,6].
Likelihood precision weights are also distinct from population weights:
effects (-2,6) average to 2, but precision weights (1,9) produce 26/5.
At cost 3, this changes margin -1 into 2.20 by changing the population.
Stored scale factors must remain aligned with their draws; posterior
quantiles, Monte Carlo error and repeated-sampling confidence remain
different quantities. \citep{exec21_cxx_bcf,exec21_cxx_flexbcf,exec21_cxx_reference}

The final covariance path deserves its own review. Statsmodels' selected
TreatmentEffect wrappers use joint-GMM moment covariance; a preliminary
robust outcome-regression label does not enable household clustering or
HAC for the final causal result. More generally, row folds and row bootstrap
cannot automatically represent repeated customers or shared policy dates.
Unsupported inference, empty arms, rank failure and unavailable nuisance
predictions must stay visible and count in evaluation denominators.
\citep{exec20_python_effect_source,v131_sw_statsmodels,exec14_causalml_primary}

The public prototype should compare fixed ATE/ATT/CATE and dose targets
using independent finite-law references, adversarial overlap, heterogeneity,
missingness, learner misspecification and clustering. Freeze training,
tuning and evaluation units separately; assess calibration, width,
availability and decision loss together. Full market coverage, commercial
edition comparisons, dependency rights, calibrated native performance and
bank usefulness remain separate obligations. The financial examples use
stipulated mechanisms and costs and do not establish product superiority.

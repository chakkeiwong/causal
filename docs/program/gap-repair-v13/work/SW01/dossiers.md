# Ten pinned software source inspections

These authored technical reviews supplement the preserved V12 register. They support selected claims only; no package was executed and no coverage cell is closed.

## LiNGAM

Commit `0f089670dbb2a470c3ef43bc0f34ef823ae59a0a` dated 2026-09-08T02:35:39Z. Inspected docs/literature/raw/v12_gap3_lingam_technical.txt and the bound licensing record.

DirectLiNGAM accepts hard/soft prior knowledge, pwling/kernel/pwling_fast measures and adaptive-Lasso choice.

fit validates prior shape, iteratively residualizes variables, stores a selected causal order and calls adjacency estimation.

Discovery of contemporaneous funding-rate responses with explicit assumptions on hidden common causes and time aggregation. Candidate Python adapter for a declared linear non-Gaussian discovery regime; defer porting until full dependency/license and behavioral review.

Compare constraint-based CPDAG/PAG engines under their own assumptions; do not rank a selected DAG against an equivalence class without a common target.

Limitations: Selected DirectLiNGAM entry only; no VAR, hidden-confounder or full-family review. A selected order is not a graph confidence region; inherited base estimation and runtime remain unqualified.

Licensing: MIT text inspected.

Next: Inspect base adjacency/total-effect routines, prior path orientation, VAR paths, bootstrap semantics and adversarial latent/Gaussian examples.

## y0

Commit `cc6644d3b470a1ab2a1eb9da4f0fdb0c843f5d3a` dated 2026-04-13T05:54:15Z. Inspected docs/literature/raw/v12_gap3_y0_technical.txt and the bound licensing record.

identify_outcomes accepts an acyclic directed mixed graph and treatment/outcome/optional conditioning variables.

It dispatches to ID without conditions and IDC with conditions, and catches Unidentifiable to return None unless strict=True.

Determine whether a proposed retention intervention can be identified when satisfaction is an unobserved common cause. Candidate symbolic identification adapter; preserve expression/graph identities and strict failure semantics. Direct algorithm port is not justified by this review.

Compare general symbolic identification with adjustment-only graph tools and other ID implementations on identical graphs/queries.

Limitations: Dispatch source does not establish ID/IDC implementation correctness or complete counterfactual coverage. A symbolic expression is not a numerical estimate; nonidentification must remain distinct from unsupported operation or execution failure.

Licensing: BSD three-clause text inspected.

Next: Inspect id_std/id_c, graph validation, expression serialization, hedge/failure paths and independent small-graph oracles.

## delicatessen

Commit `8962bf0cb21a41873c708e1c8d64e692e95e9b58` dated 2026-08-11T13:58:00Z. Inspected docs/literature/raw/v12_gap3_delicatessen_technical.txt and the bound licensing record.

ee_aipw stacks average-effect, two potential-outcome mean and propensity/outcome model estimating equations into a (3+b+c)-by-n array.

The implementation explicitly clips propensity probabilities when requested and chooses binary/logistic versus continuous/linear outcome regression.

The module also exposes instrumental-variable and two-stage least-squares estimating-equation entry points; their full numerical behavior is not inspected here.

Estimate average renewal-offer effect while retaining the nuisance-model equations needed for uncertainty. Candidate numerical equation/reference integration for explicit estimating functions; defer adoption of inferential defaults pending solver and covariance review.

Compare with statsmodels joint-GMM treatment effects and target-specific TMLE implementations under matched targets and sampling units.

Limitations: An estimating-equation array is not a fitted estimator or independently verified uncertainty result. Sandwich construction, solver convergence, clustering, longitudinal targets and nuisance-rate claims need separate review.

Licensing: MIT text inspected.

Next: Inspect MEstimator, sandwich differentiation, finite-sample correction and dependent-data limitations; execute matched equation/root references later.

## pygformula

Commit `e66f787fcef2d6a9092b88135147c6b13785795c` dated 2026-05-22T19:45:58Z. Inspected docs/literature/raw/v12_gap3_pygformula_technical.txt and the bound licensing record.

ParametricGformula documents individual/time identities, time-varying covariate models, histories, custom fits/predictions and intervention descriptions.

Outcome types include survival, continuous end-of-follow-up and binary end-of-follow-up; competing events and censoring have separate options.

nsamples defaults to zero; the fit path invokes separate Bootstrap work for requested bootstrap replicates.

Sequential servicing actions with delinquency histories, default as a competing event and observed account closure. Candidate Python longitudinal-regime adapter after intervention/time/competing-event contracts and bootstrap internals are reviewed.

Compare R g-formula, longitudinal TMLE and weighting approaches on the same histories, interventions, censoring and target horizon.

Limitations: Main-class inspection does not verify simulation, resampling unit, competing-risk identification or interval calibration. Regime evaluation does not establish optimal policy learning; a covariate-history API does not certify sequential exchangeability.

Licensing: MIT text inspected.

Next: Inspect simulate/Bootstrap/intervention helpers, resampling identity, horizon conventions and truncation diagnostics.

## statsmodels

Commit `8278e2d218cc85bac2c7af02feb9a19a0e499b04` dated 2026-10-06T14:46:27Z. Inspected docs/literature/raw/v12_gap3_statsmodels_technical.txt and the bound licensing record.

TreatmentEffect describes IPW, RA, AIPW, AIPW-WLS and IPW-RA with joint-GMM inference.

effect_group distinguishes all, treated and untreated populations; the documented outcome model is linear OLS.

ps_bounds defaults to (0.001,0.999), validates 0<lower<upper<1 and is used to clip predicted selection probabilities.

The class notes state that final GMM inference corresponds to HC0 regardless of the internal _cov_type keyword; the early module comment about missing standard errors is not an adequate current contract.

Point-in-time retention offer, distinguishing all eligible customers from treated customers. Candidate joint-GMM point-treatment baseline with explicit population and clipping settings; refuse silently translating an internal covariance option into a clustered-inference claim.

Match delicatessen estimating equations and target-specific doubly robust implementations before comparing timing or intervals.

Limitations: This single module does not establish statsmodels panel/time-series/IV coverage. HC0 is not a dependence-robust bank panel covariance; no inference/runtime qualification performed.

Licensing: BSD three-clause text inspected.

Next: Trace exact GMM covariance and each estimator, inspect clipping impact and test population/parameter-label roundtrips.

## grf

Commit `5bee99b51471f76cb2d63acbc8a9b0ffec408ba0` dated 2026-04-30T18:40:08Z. Inspected docs/literature/raw/v12_gap3_grf_technical.txt and the bound licensing record.

causal_forest documentation distinguishes binary-treatment CATE from the continuous-treatment conditional covariance/variance target.

The interface exposes nuisance predictions, clustering, equal cluster weighting, honesty, subsampling, grouped confidence-interval trees, tuning and a C++ RNG seed.

The selected wrapper validates clusters/sample weights and defaults to honesty=True, 2000 trees and no tuning.

Heterogeneous offer response versus the effect of increasing a continuous funding incentive by one specified amount. Prefer candidate R/native integration over a rewrite; defer any port or distribution decision until full license and ABI review.

Compare matched heterogeneous-effect targets with DML/TMLE or other forest estimators, not prediction accuracy alone.

Limitations: R wrapper inspection is not native C++ source qualification or proof of causal identification. A continuous covariance slope is not generally a finite dose contrast; CATE and population average effects are distinct.

Licensing: Repository COPYING contains GPL version 3; dependency and file-specific scope still require review.

Next: Inspect native training/prediction/variance and aggregation code; compare cluster weighting and finite dose queries explicitly.

## MossSpider

Commit `62e6bd20364c7ef01b6964fd79f21be84e5ac579` dated 2022-07-13T12:45:05Z. Inspected docs/literature/raw/v12_gap3_mossspider_technical.txt and the bound licensing record.

NetworkTMLE documents expected incidence under a treatment plan with Monte Carlo averaging for stochastic allocations and direct-contact interference.

The constructor rejects noninteger node identities, self-loops and nonbinary exposure, remaps identities and builds an unweighted adjacency matrix.

The documentation disclaims a missing-data procedure, describes degree restrictions and gives a directed influence convention opposite the graph arrow.

Borrower-group outreach with immediate-neighbor spillovers, where relationship direction and exposure are owned definitions. Candidate restricted network-policy adapter, subject to explicit graph direction, identity and exposure-map conformance; do not adopt as a general banking network engine.

Compare individual-network mapping with inferference grouped allocation policies under an actually shared estimand.

Limitations: Documentation describes an undirected input while also giving a directed convention; the selected constructor contains directed handling. Directed semantics need explicit runtime review. Arbitrary contagion, weighted/dynamic networks, missing ownership and variance validity are not established.

Licensing: MIT text inspected.

Next: Inspect fit, targeting, exposure mapping, stochastic integration and variance; resolve directed documentation inconsistency.

## CausalGPS

Commit `3a837d66e5cb791a310a18b63919abe04b4b290f` dated 2026-01-11T20:39:26Z. Inspected docs/literature/raw/v12_gap3_causalgps_technical.txt and the bound licensing record.

estimate_gps constructs observed continuous-exposure generalized propensity scores with normal or kernel options and a SuperLearner library choice.

The normal path uses fitted exposure mean and a residual standard deviation in dnorm; the kernel path estimates residual scaling and calls compute_density.

The output includes identity, exposure, gps, predicted mean/scale and residual fields; this function alone does not fit a dose-response outcome.

Construct support diagnostics for a continuous retention incentive conditional on pre-offer customer characteristics. Candidate GPS construction component; defer complete causal-estimation adoption until downstream matching/outcome and density contracts are reviewed.

Compare with causaldrf full response-surface construction and grf continuous slope only after aligning the target.

Limitations: Helper functions, density scaling, matching/weighting, outcome inference and overlap qualification remain uninspected. A conditional density is not a binary treatment probability; the observed-density output alone cannot establish a finite dose effect.

Licensing: DESCRIPTION declares GPL-3, version 0.5.1, published 11 January 2026.

Next: Inspect compute_density and exposure evaluation at counterfactual doses, balance diagnostics and full license/dependency terms.

## causaldrf

Commit `cb67aca60bc4dbd6792edd062cb7682c656d5908` dated 2022-09-29T19:40:10Z. Inspected docs/literature/raw/v12_gap3_causaldrf_technical.txt and the bound licensing record.

hi_est documentation describes fitting a treatment model, a GPS-adjusted outcome response surface and averaging predicted outcomes at a requested dose grid.

Documented treatment distributions include Normal, LogNormal, transformed normal, Poisson, negative binomial, Gamma and Binomial; output includes parameter, treatment-model and outcome-model records.

Compare expected net retained deposits at two feasible incentive levels instead of reporting an unlabeled curve ordinate. Candidate response-surface reference/adapter; defer license clearance and runtime qualification pending LICENSE and full function review.

Compare CausalGPS density construction plus downstream outcome estimation and grf local slope under matched banking queries.

Limitations: This review supports the documented target and interface, not algorithm correctness or interval implementation. A mean outcome at a dose is not an effect contrast until a comparator dose is specified; the MIT notice requirement remains unresolved.

Licensing: DESCRIPTION declares MIT + file LICENSE, version 0.4.2; accompanying LICENSE file not yet inspected.

Next: Inspect function body, treatment-model helpers, support and interval procedures, and the accompanying LICENSE notice.

## inferference

Commit `b0c785e3f60541b993ff4e7324672b761a5f9723` dated 2025-05-15T07:40:02Z. Inspected docs/literature/raw/v12_gap3_inferference_technical.txt and the bound licensing record.

interference uses grouped formulas and allocation probabilities with glm/glmer/HLfit/oracle propensity choices and an IPW causal-estimation path.

The code checks group count, allocation range, variance option and a single-random-effect limitation of the default logit integrand.

Documentation gives integrate_allocation default FALSE while the inspected function signature sets TRUE; adapters must freeze an explicit setting.

Branch or household-group encouragement with within-group spillovers and independently justified group sampling. Candidate grouped-allocation reference with explicit integration/default settings and group sampling contract.

Compare MossSpider network mapping only where target populations, allocation policies and dependence assumptions coincide.

Limitations: Grouped partial-interference workflow is not a general dynamic financial network model. Naive/robust labels do not establish uncertainty validity under arbitrary dependent groups; integrands/variance/runtime need review.

Licensing: DESCRIPTION declares GPL (>=2), version 1.0.3, published 15 May 2025.

Next: Inspect numerical integrands, weight derivatives and variance, pin dependency versions, and test unequal groups and boundary allocations.

# Dependency-path source review

These are scoped inspections, not package qualification or complete cell reviews.

## y0

- ID recursively restricts ancestors, augments interventions and decomposes districts; the connected-district failure raises Unidentifiable, while invariant failures raise RuntimeError.
- IDC tests a rule-2 exchange, recurses after exchanging observation/action, then identifies the unconditioned query and normalizes. The rule-2 helper delegates separation to another module.
- The inspected graph constructor and edge insertion methods do not enforce acyclicity; these paths alone are not a complete input validator.

Reuse disposition: Integrate a symbolic operation after explicit DAG/mixed-edge/query validation and a reference suite; preserve nonidentification separately from malformed input and execution error.

Next evidence: Inspect separation, graph mutilation and expression normalization; compare adjustment, front-door and hedge examples against independent symbolic references. No recursive-correctness or full counterfactual claim.

## LiNGAM

- Adjacency is stored as B[target,predictor]; permitted earlier variables are fit by adaptive Lasso or ordinary regression. estimate_total_effect uses source plus its estimated parents, warns on reversed causal order and still returns a regression coefficient.
- The generic bootstrap resamples rows and refits; VARLiNGAM fits a lag model, applies DirectLiNGAM to residuals and has a separate residual-resampling path that reconstructs a sequence.
- The VAR bootstrap sets the criterion to None during its loop, so lag-selection uncertainty must not be inferred from the existence of this bootstrap.

Reuse disposition: Integrate distinct IID and VAR operations with explicit matrix orientation and sampling-law metadata; defer porting and graph-confidence claims.

Next evidence: Inspect adaptive-Lasso and total-path helpers, lag selection and residual-law assumptions; execute Gaussian/latent/persistent-residual adverse cases only under a registered qualification design.

## delicatessen

- MEstimator solves stacked equations, differentiates their sum, scales bread and meat by the number of supplied contribution columns, and scales the sandwich once more for estimator variance.
- compute_meat forms the outer-product sum of supplied columns. It does not add lag products or infer borrower/calendar clusters from data labels.
- The default permits a pseudoinverse; solver convergence and a finite sandwich do not establish identification or weak-rank coverage.

Reuse disposition: Integrate a contribution-level interface with explicit independent unit, residual/Jacobian diagnostics and covariance method; retain score inversion as a separate scientific operation.

Next evidence: Compare derivatives against analytic small models, validate independently sampled group aggregation, and derive actual dependence correction before using on persistent calendars.

## pygformula

- Bootstrap draws subject identifiers with replacement, copies complete histories, assigns new replicate IDs and refits component models; n_simul expansion is a separate resampling step.
- Simulation applies interventions and updates histories before outcome prediction; static schedules use the absolute index int_values[t], while threshold rules bound the contemporaneous variable.
- Bootstrap exceptions return boot_results=None. The previously inspected caller filters those from boot_results but indexes every original boot_results entry when constructing bootests; a None entry implies a static inconsistency that needs runtime reproduction.

Reuse disposition: Integrate only after clock, history, competing-event and failure-accounting conformance checks; carry failed bootstrap attempts in the denominator.

Next evidence: Reproduce the None-result path in an isolated qualified environment; inspect histories/model fits/output interval routines. Independent subjects do not establish validity under shared calendar shocks.

## statsmodels

- The GMM covariance path defaults to weights_method=cov, an outer-product covariance divided by n; HAC is a separate explicit path requiring maxlag and using a supplied kernel or Bartlett default.
- GMMResults obtains the covariance method from fit options and recomputes moment covariance. Preliminary outcome _cov_type settings in TreatmentEffect do not select this final path.
- The inspected covariance code centers with moms.mean() rather than a per-column mean; sensitivity to nonzero moment residuals remains a qualification question.

Reuse disposition: Integrate only with separately recorded preliminary and final covariance settings; a supported low-level HAC path does not imply the treatment-effect wrapper exposes it.

Next evidence: Trace each estimator call and all options, validate analytic moments and time ordering, then compare covariance and rank diagnostics. Do not infer cluster support or calibration from a generic robust label.

## grf

- The R all-sample AIPW path averages get_scores output and sums centered weighted scores within clusters for variance. Early guards reject clustered or sample-weighted TMLE despite later code containing cluster formulas.
- Continuous-treatment scores estimate conditional treatment variance with another regression forest and divide treatment residuals by it; zero/near-zero variance needs explicit handling and qualification.
- Causal bindings set the instrument index equal to treatment and call instrumental_predictor, which constructs InstrumentalPredictionStrategy. Its point output is a moment ratio, and native variance uses tree groups plus a Bayes debiaser.
- The initially fetched src binding is a symlink target string; implementation claims use the separately fetched target body and factory, not that string.

Reuse disposition: Integrate the maintained R interface first; defer a direct C++ port until ABI, serialization, dependency/license and behavioral review. Preserve target population and unsupported option combinations.

Next evidence: Inspect the Bayes debiaser, serialization, forest sample construction and numerical guards; compare all/treated/control/overlap and continuous-slope targets separately. Tree groups are not bank calendar clusters.

## CausalGPS

- compute_resid returns (a-b)/c. compute_density uses stats::density and linear interpolation with rule=2.
- The inspected kernel estimate_gps path evaluates density at standardized residuals and stores that value without a division by its scale in that path. A conditional density on the original exposure scale would require the Jacobian 1/scale under a location-scale model.

Reuse disposition: Defer causal density/weight adoption until scale semantics and downstream uses are traced; keep the package as a comparison candidate. Do not silently patch a vendor routine.

Next evidence: Trace matching/weighting and counterfactual-dose prediction, inspect scale positivity, and reproduce heterogeneous-scale and dose-unit changes. The observed path alone does not establish all package outputs are wrong.

## causaldrf

- The supplementary LICENSE file names year 2015 and Douglas Galagate; it supplements the previously inspected DESCRIPTION license declaration. It is not a full dependency or redistribution review.

Reuse disposition: Retain the provisional comparison/reference decision pending function and interval review; the missing accompanying notice has now been acquired.

Next evidence: Inspect full hi_est body and interval procedures, then resolve all dependency/distribution terms before an integration or port decision.

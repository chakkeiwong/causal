# A: structural responses and dependent inference

Specification v1, 8 October 2026. Targets are fixed horizons 0–12, with the
policy-rate impact normalized to one percentage point. Deposit and lending
responses and a separately defined funding account are different outputs.

For A-G, X_t = F X_{t-1} + B epsilon_t with stable F, iid Gaussian structural
innovations and nonsingular observation covariance. Z_t = a epsilon_1t + v_t,
where v is an independent stable AR(1). The persistence of irrelevant
instrument noise creates serially correlated scores while preserving
lead/lag shock exclusions. This distinguishes serial-score inference from
the special case of white instrument noise. The reference response is
F^h B[:,1] divided by B[1,1]. Identification uses the external instrument;
prediction alone does not identify B.

Estimate d = mean(Z X_1), n_h = mean(Z X_i,next-h) on one common origin
sample, then n_h/d. Derive the joint moment influence function, Bartlett
HAC, covariance scaling, Bonferroni and simulated Gaussian maximum bands.
For weak d, derive residual-test inversion without dividing by d; report
unbounded/disconnected sets. The generating structural innovations are
hidden from fitting. A proxy-VAR challenger estimates reduced dynamics and
the impact direction from instrument/innovation covariances.

Initial final-run cases are strong and weak instruments, white and persistent
instrument noise, stable versus near-unit-root dynamics, and an invalid
instrument. Final settings are frozen after documented numerical pilots.
Report componentwise and whole-curve coverage, interval widths, bias and
failures. Incorrect iid standard errors and pointwise bands are adverse
comparisons. Stable-law coverage is not claimed uniformly near unit roots.

A-L adds exogenous high-dimensional controls and a partially linear IV
restriction. Derive the orthogonal score and product remainder; separate
training and evaluation blocks with an explicit gap including outcome
horizon. State rate conditions for inference and for fitted-score HAC.
Compare learned controls and the low-dimensional reference. A-P aggregates
bank scores by calendar date under common shocks. A-I derives cointegration,
error correction and lag-augmented responses separately.

Existing primary copies: stock2018, jorda2024, dml2018, cluster2021,
hyvarinen2010. New search/read questions: original lag-augmented LP theorem;
HAC conditions; dependent sparse learning; cointegration/state-space bridge.
The critical comparisons are identification restrictions and inferential
validity, not prediction RMSE alone.

Completion requires a reproducible estimator, joint uncertainty and weak-IV
result, substantive persistent/high-dimensional extensions and an executed
complete-workflow scale route. The current document is a study design.

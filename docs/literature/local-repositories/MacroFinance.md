# One-country milestone 1

## Scope
This note summarizes the current findings from the one-country AFNS / HMC work in `demo_hmc.py`, with emphasis on compliance against the monograph appendix and the project identification rule in `CLAUDE.md`.

The key point is that the recent audit uncovered a genuine software issue: the earlier MAP covariance object was not a real local posterior-curvature estimate. That bug matters because local identification cannot be claimed if the covariance is merely a prior fallback. We have now made covariance provenance explicit and tightened the demo so fallback covariance cannot be mistaken for identification evidence.

---

# 1. Current findings

## 1a. Non-compliance with the document and project rules

### Appendix / monograph compliance
The one-country demo is now much closer to the appendix than before, but it is still only partially compliant in substance.

What now matches the appendix:
- finite-domain Nelson--Siegel normalization over `(0, T]` with `T = 30` years;
- demeaning of the non-level loading functions;
- interpretation of `theta_0` as domain-average fitted yield and `theta_1`, `theta_2` as zero-domain-mean slope/curvature deviations;
- prior centering in transformed coordinates;
- explicit estimation of log measurement noise rather than fixing observation noise;
- explicit reporting of synthetic recovery, prior sensitivity, measurement-error sensitivity, local identification, decay sensitivity, and sampler diagnostics.

What still does not fully match the appendix spirit:
- `kappa`, `sigma`, and `decay` remain fixed in the posterior run;
- the demo is still a restricted one-country block rather than a full one-country AFNS estimator;
- sensitivity checks are implemented as practical milestone checks, not yet as a mature identification workflow with multiple replications / richer diagnostics;
- local identification evidence is still fragile because Hessian-based covariance may fail and fall back.

### Identification-rule compliance
Relative to `CLAUDE.md`, the most important improvement is that convergence diagnostics are no longer treated as sufficient by themselves. However, full compliance is still conditional on the quality of the local-curvature step and the empirical outcomes of the checks.

What the rule requires:
- explicit observables and source of variation;
- confounds and nuisance assumptions documented;
- normalizations documented;
- measurement error treated as part of identification;
- synthetic recovery;
- prior sensitivity;
- measurement-error sensitivity;
- local identification checks;
- trust label (`Identified`, `Weakly identified`, `Untrusted`) only after those checks.

What is still noncompliant or only partial right now:
- the observables / confounds are now printed, but still in concise diagnostic language rather than a full formal note;
- local identification remains the weakest link, because a failed Hessian path still produces fallback covariance and therefore should block a positive trust conclusion;
- because `kappa`, `sigma`, and `decay` are fixed, the demo is not yet evidence that the broader one-country AFNS block is identified in a more general specification.

## 1b. Possible issues for extension to more general models

The current one-country setup may not extend cleanly to broader models because:
- fixed `kappa` and `sigma` suppress confounding between long-run means, transition persistence, and state volatility;
- fixed `decay` suppresses the important interaction between curvature identification and loading shape;
- scalar measurement noise is still much simpler than maturity-specific or block-specific measurement noise used in richer systems;
- the one-country state dimension is only 3, so the HMC geometry is much simpler than in cross-country / basis / convenience-yield models;
- synthetic data are generated from the same model class used in estimation, so model misspecification is not being tested.

This means that even a successful one-country result may not generalize automatically to:
- a one-country AFNS model with estimated `decay`, `kappa`, and `sigma`;
- a one-country AFNS model with richer measurement-error structure;
- cross-country AFNS + basis + convenience-yield systems;
- realistic data settings where the fitted model is misspecified relative to data-generating reality.

## 1c. Shortcuts that cannot be extended / can block generalization

The following shortcuts are still present or still relevant as cautions:

1. **Fixing structural blocks**
   - fixing `kappa`, `sigma`, and `decay` makes the HMC problem much easier than the general model;
   - conclusions about identification of `theta` may not survive when these blocks are estimated jointly.

2. **Single synthetic path from the same model class**
   - because simulation and estimation share the same model class, good recovery may overstate robustness;
   - this does not test misspecification or approximation error.

3. **Small number of sensitivity scenarios**
   - current sensitivity checks are milestone-level, not yet comprehensive;
   - more general models will need broader prior, noise, and specification perturbations.

4. **Hessian/fallback ambiguity**
   - before the audit, fallback covariance could masquerade as local identification evidence;
   - this exact kind of shortcut would be dangerous in a larger model where true local curvature is much harder to obtain.

5. **Short time series**
   - the demo uses only 120 monthly observations (10 years), which is short for distinguishing level, slope, curvature, and measurement-noise tradeoffs;
   - weak curvature identification in the demo may worsen in larger models with more states or more parameters.

---

# 2. Explicit list of issues right now with `demo_hmc` and HMC convergence

## Specification / compliance issues
1. The demo is still a restricted benchmark because `kappa`, `sigma`, and `decay` are fixed in the posterior run.
2. The current trust conclusion is still limited by whether Hessian-based covariance succeeds; if it falls back, local identification should fail.
3. The sensitivity checks are useful but still coarse-grained relative to the full identification rule.
4. The demo remains synthetic and same-model-class, so successful recovery is only partial evidence.
5. Decay is only sensitivity-checked, not estimated, so curvature-vs-decay identification remains unresolved.

## HMC / convergence issues
1. Curvature (`theta_2`) has already shown weak behavior in earlier runs (wrong sign / poor diagnostics).
2. Local curvature estimation can fail computationally, forcing fallback covariance.
3. HMC preconditioning depends on MAP covariance, so weak or fallback covariance may degrade sampling geometry.
4. Sensitivity runs increase total computational load and make the workflow slower and noisier.
5. If the Hessian path is unstable, convergence diagnostics may reflect geometry problems rather than identification alone.

## Software / inference issues
1. The original MAP covariance implementation was misleading because it always returned prior covariance when `prior_scale` existed.
2. The Hessian helpers existed but were not wired into `compute_map_estimate()`.
3. Full Hessian computation can be expensive and brittle in TensorFlow.
4. Diagonal Hessian fallback may still be weak evidence if curvature is poorly behaved.
5. Local identification evidence now depends on provenance tracking, which is correct but may reveal many failures in practice.

---

# 3. Hypotheses for why the issues happen

## H1. Curvature is weakly identified because the maturity grid and time-series length do not provide enough curvature information
Reasoning:
- curvature is usually the hardest AFNS component to identify;
- with 10 years of monthly data and a limited maturity grid, the hump component may be weak relative to level and slope.

## H2. Curvature and decay remain partially confounded even after finite-domain normalization
Reasoning:
- demeaning non-level loadings fixes interpretation, but does not create new information;
- if `decay` changes the hump location, curvature and decay can still substitute for each other.

## H3. Measurement noise and curvature compete for explaining medium-maturity misfit
Reasoning:
- even after estimating log measurement noise, posterior tradeoffs may persist between noisy observations and structural hump shape;
- this is especially likely in short samples.

## H4. Local Hessian estimation is numerically brittle in this TensorFlow setup
Reasoning:
- nested autodiff over a Kalman likelihood can be unstable or expensive;
- second-order information may fail numerically even when the posterior is conceptually well behaved.

## H5. Fixing `kappa` and `sigma` may distort the apparent identification picture
Reasoning:
- if persistence or volatility are misspecified but held fixed, the long-run mean block may absorb distortions;
- this could either artificially help or hurt `theta` recovery.

## H6. Same-model-class synthetic recovery overstates robustness
Reasoning:
- simulation from the same class used in estimation removes misspecification risk;
- this can make the model look more stable than it will be on realistic data.

## H7. The HMC geometry may still be poor even when identification is conceptually acceptable
Reasoning:
- a model can be structurally identified but computationally hard to sample;
- sampler failures may reflect posterior curvature/pathology rather than lack of information per se.

---

# 4. Experiments to confirm or reject the hypotheses

## Experiment A: Time-series length expansion
Purpose: test H1.
Design:
- rerun the same synthetic workflow with `n_steps` = 120, 240, 360.
- compare posterior mean, ESS, Rhat, and local-ID outcome for `theta_2`.
Interpretation:
- if curvature improves strongly with length, H1 is supported.
- if not, the problem is not mainly sample length.

## Experiment B: Maturity-grid enrichment / thinning
Purpose: test H1 and H3.
Design:
- compare a sparse grid vs enriched medium-maturity grid.
- examples:
  - sparse: `[0.25, 1, 5, 10, 30]`
  - current: `[0.25, 0.5, 1, 2, 5, 10, 20, 30]`
  - enriched medium: add 3Y, 7Y, 15Y.
Interpretation:
- if curvature identification improves when medium maturities are enriched, H1/H3 are supported.

## Experiment C: Decay sensitivity sweep
Purpose: test H2.
Design:
- extend the decay grid beyond the current three values;
- inspect how `theta_2` and log noise shift with decay.
Interpretation:
- large movement of `theta_2` across decay values supports H2.

## Experiment D: Measurement-noise prior sweep
Purpose: test H3.
Design:
- run several priors on `log_measurement_error_std`:
  - baseline,
  - broader noise prior,
  - lower-centered noise prior,
  - higher-centered noise prior.
Interpretation:
- if `theta` results move materially, especially curvature, H3 is supported.

## Experiment E: Hessian provenance stress test
Purpose: test H4.
Design:
- log covariance source for repeated runs under small perturbations;
- compare full Hessian vs diagonal Hessian success rates;
- compare condition numbers and runtime.
Interpretation:
- frequent fallback supports H4.

## Experiment F: Joint-parameter expansion
Purpose: test H5.
Design:
- next milestone: estimate `theta` + log noise + one additional structural block, e.g. `decay`.
- compare whether `theta` conclusions survive.
Interpretation:
- large shifts imply current fixed-parameter conclusions are fragile.

## Experiment G: Misspecified synthetic data
Purpose: test H6.
Design:
- generate synthetic data with slight mismatch from the fitted model, e.g. maturity-specific noise or altered transition dynamics.
- fit the current benchmark model.
Interpretation:
- if recovery degrades sharply, same-class recovery is overstating robustness.

## Experiment H: HMC geometry diagnostics under controlled identification
Purpose: test H7.
Design:
- hold the DGP fixed and vary HMC settings (step size, leapfrog steps, chains, warmup length) while tracking ESS/Rhat/divergences.
Interpretation:
- if sampling behavior changes strongly while posterior location remains similar, the issue is partly computational geometry, not pure identification.

---

# 5. Milestone conclusion

The current milestone result is:
- the one-country demo is now conceptually much better aligned with the appendix;
- the major false-evidence bug around MAP covariance has been identified and repaired;
- the strongest remaining risk is not wording but substantive identification, especially local identification and curvature robustness;
- the current benchmark should still be treated conservatively until the experiments above are run.

The right current stance is therefore:
- **not yet trusted as a general one-country AFNS conclusion**;
- **useful as a milestone benchmark and audit target**;
- **ready for structured experiments to determine whether the remaining issues are due to weak information, confounding, numerical curvature failure, or HMC geometry.**

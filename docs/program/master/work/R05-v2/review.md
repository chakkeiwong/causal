# R05 v2 final review

The first attempt was invalid for its claimed argument: evaluation outcomes selected penalties, standardization used all data, covariance crossed the omitted gap, and scenario dimension overrides were ignored. Its requests remain exploratory and immutable. This successor repairs all four, uses a fresh seed and actual training-only nested selection. Independent convex optimization, soft-threshold and dense covariance fixtures pass.

The frozen 99% intervals are wider than the original 95% ones; comparisons across attempts do not isolate a correction effect.

- baseline: 500/512, lower 0.951769, finite 512, median width 0.252800.
- high_dimension: 499/512, lower 0.949140, finite 512, median width 0.245144.
- larger_support: 493/512, lower 0.933851, finite 512, median width 0.250125.
- long_gap: 504/512, lower 0.962623, finite 512, median width 0.261000.
- persistent: 501/512, lower 0.954428, finite 512, median width 0.250146.
- inadequate_gap: 504/512, lower 0.962623, finite 512, median width 0.242912.
- nonlinear_misspecification: 0/512, lower 0.000000, finite 512, median width 0.330849.
- weak_iv: 512/512, lower 0.988797, finite 512, median width 3.836470.

High dimension and larger support fail the simultaneous .95 minimum screen. This means the frozen rule did not qualify these cells; it does not establish a universal defect. Nonlinear misspecification gives 0/512 coverage. Weak-IV intervals are wide, and a tiny-denominator guard is not a strong-IV test.

Next research: independent-pilot separation, restricted-eigenvalue/growing-dimension rates, weak-IV test inversion and richer prespecified nonlinear nuisance bases. New arguments need new protocols; no saved seeds or critical values are changed. Arbitrary learners and bank precision remain unqualified.

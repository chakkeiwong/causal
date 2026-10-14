# R03 author review and disposition

The direct fixed-policy estimator passes the primary 99% lower-bound screen in
all six declared valid cells: baseline 0.974, weak emission 0.981, scarce
audit 0.963, poor overlap 0.978, strong overlap 0.974 and transition
misspecification 0.965. Every valid request is finite. The 95% challenger is
narrower and fails the 0.95 screen, showing the declared precision tradeoff.
Wrong logger probabilities cover 1/512 and policy leakage has zero finite
outputs; these are retained failures. Widths, effective sample size, maximum
weight, trajectories and runtime are recorded.

This qualifies fixed-policy value inference only for the selected17 family
with truthful representative state audits, supplied logger probabilities,
independent policy selection and logger overlap floor. It does not qualify
unknown optimal-policy value, estimated logger uncertainty, arbitrary POMDPs,
bank truth or ROI. Transition misspecification is a weighting diagnostic under
correct logger probabilities, not a general robustness guarantee.

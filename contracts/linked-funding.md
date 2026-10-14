# Selected linked-outcome funding reference

`causalbank.linked_funding.fit_linked_funding` estimates the fixed monetary
focal response under the registered dependent funding calendar. This is a
research reference, not an accepted bank API or generally qualified learner.

Both input histories have one row per origin. Columns are stratum (0/1),
action, intercept (1), driver, centered squared driver, then H+1 outcomes
for candidate one and H+1 outcomes for candidate two. The pilot is independent
and invariant, with at least four times as many origins as evaluation.
The supplied `FundingTarget` fixes action normalization, horizon, weights,
stratum averaging and direct repricing cost. Penalties and dictionary are
fixed before evaluation.

Each history's audit tuple has three arrays of its row count: sampled (0/1),
label (1 means first candidate focal; 0 means second), and known inclusion
probability in (0,1]. Unselected labels must be NaN, not simulator truth.
A selected label resolves the whole stored origin vector. It is not another
correctness count and its horizons are not independent audits. Sampled labels
must be truthful, and inclusion indicators conditionally independent across
origins given the complete histories and probabilities. These and the causal
innovation/pilot/calendar conditions are declarations, not facts validated
by the numeric fit. Wrong probabilities or mislabeled truth can produce
numerically valid but scientifically wrong outputs.

`augmentation=True` uses B+R(F-B)/q; False uses RF/q. The routine returns a
computed finite set with estimate, standard error, scalar calendar variance,
stratum slopes, selected penalty, pilot/evaluation sizes and sampled-label
counts. The set uses the repository's encoded lower/upper format. Invalid
dimensions, probabilities or label visibility raise ValueError. Missing
sampled strata, absent action variation and nonpositive/nonfinite or
roundoff-degenerate variance produce explicit unavailable statuses. No
interval is manufactured by clipping an invalid variance.

The selected untapered H-lag variance includes audit noise in the empirical
scores; no separate audit variance is added. Coverage is pointwise asymptotic
under the stated law and rates. The 4,800-request results retain finite-sample
shortfalls and severe false-premise failures. The implementation materializes
pseudo-outcomes; chunked pilot algebra does not qualify this new route for
bounded total memory, multi-host operation or service-level performance.

Execution, evidence and remaining acceptance requirements are recorded in
`docs/program/linked-funding-delivery-2026-10-11.md` and
`docs/reviews/remaining-gaps-linked-funding-2026-10-11.md`.

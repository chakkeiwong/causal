# Selected funding calibration operations

The local `calibrated_funding_operations.run_request` requires an explicit
`joint_ols` or `growing_pilot` method, a fixed financial target, ordered calendar
rows, independent binomial identity-audit counts and the scientific declarations
in `funding_calibration.DECLARATIONS`. The declarations assert premises; their
truth is not learned from a successful fit. Rows contain stratum, action,
(1,W,W²−1) and the two complete candidate horizon vectors. Independent origin
swaps do not authorize persistent or endogenous customer-map inference.

`joint_ols` fits the fixed dictionary on the evaluation sample, using grouped
QR and a second scalar-score pass with bounded working state. Its retained
720-date study under-covers. `growing_pilot` instead requires an independent
invariant pilot with at least four times as many dates; penalties and features
are fixed before evaluation. This implementation retains the pilot/evaluation
arrays and is not the bounded-memory fitting claim. Extra history is not free.
The wrapper never automatically selects the method with favorable final results.

The default scalar covariance uses untapered lags through the response horizon
under the proved structural innovation condition. An explicit Bartlett comparator
also exists. These are asymptotic, model-conditional financial intervals; neither
a full response covariance matrix nor general finite-sample validity is asserted.
Independent audit variance is propagated through the inverse map. A Wilson
audit interval crossing .5 returns `unavailable_mapping_rank`; empirical audit
probability zero/one returns `unavailable_audit_boundary`; nonpositive estimated
calendar variance returns `unavailable_calendar_variance`. None becomes a zero
value, a clipped variance or a confident normal interval.

The request identity binds method, target, evaluation and pilot bytes, audit
counts, covariance and declarations. Both author-owned consumers preserve that
identity, result status, interval and qualifications through JSON serialization.
When unavailable, they withhold monetary estimates and intervals. Incorrect
declarations can still give a confidently wrong causal answer: omitted action
means and endogenous innovations are retained negative examples.

Qualification evidence is in `docs/reviews/calibration-local-rehearsal.json`,
`calibration-independent-checks.json`, `calibration-followup-checks.json` and
the final registered studies. Replay the complete operation under the
[external protocol](../docs/program/external-validation-v9.md) before any claim
of adopted interfaces, authentic bank validity or service-level acceptance.

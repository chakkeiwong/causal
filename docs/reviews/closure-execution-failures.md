# Observed execution failures and repairs

10 October 2026. Failures remain evidence of the development process and are
not removed from registered final samples.

- **C02 pilot, before any final draws:** the unequal-audit generator used
  q=rate*(1+0.7 X); at rate 0.6 and X=1 this was 1.02. NumPy rejected the
  impossible Bernoulli probability. The original code/spec are preserved in
  `docs/program/history/closure-pilot-audit-probability.zip`. Reduced the
  prespecified inclusion contrast to 0.5, giving probabilities 0.3 and 0.9
  in that arm. This repairs the sampling design, without selecting an estimator
  or outcome. The full distinct-seed pilot is rerun before final evaluation.

- **C03 final report aggregation:** legacy regular failures use statuses such
  as `weak_identification`; the new availability denominator initially excluded
  only the literal `unavailable`. Coverage over all requests and every retained
  set were correct, but conditional availability counts were wrong. The original
  report/code are preserved in `history/closure-linkage-before-availability-summary.zip`.
  Reaggregate the retained per-request results using only `computed` and
  `computed_set` as available; bind that repair explicitly without rerunning or
  discarding stochastic draws.

- **C06 workload trial:** the direct discovery call used the wrapper's
  `episodes` keyword instead of the kernel's positional data argument. The
  trial stopped before completing the suite. Review also found unequal public
  output payloads between direct and managed paths, and overlap with other
  studies. Retain trial timings in
  `history/closure-workload-trial-before-matched-outputs.json`; exclude them
  from performance conclusions. Repair the kernel call, use identical unit,
  provenance, inference and serialization obligations in both paths, assert
  byte-identical public outputs, and rerun fresh processes after studies finish.

- **C08 current evidence gate:** adding the explicitly dated installed runtime
  source changed `sources.json`, so the gate correctly rejected the earlier
  targeted source-review receipt. Rerun its actual primary PDF identity checks
  and inspected-anchor extraction against the new catalogue. No scientific
  simulation or past receipt hash is rewritten to masquerade as a replay.
- **C08 rendered build:** a combined score-covariance display exceeded the
  text width by 28 points. Split it into an aligned display and rebuild; the
  final visual inspection must apply to the corrected PDF bytes.

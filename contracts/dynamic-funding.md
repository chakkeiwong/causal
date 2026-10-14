# Dynamic funding: regular and projected financial inference

Local reference implementation: `causalbank.dynamic_product.run_funding`.
This contract describes the qualified two-stratum, two-candidate construction,
not a general identification compiler or bank-accepted interface.

Supply a `DynamicBrief`, source assertions, independent nuisance-pilot arrays,
candidate response histories or versioned outcome records, independent binary
audit records, and fixed penalty candidates. Calendar origins are consecutive;
the horizon and two candidate histories match the funding target. The six
columns of the declared basis are `(1,W,W²−1)` and its stratum interaction.
Pilot and evaluation origins contain both strata. Economic weights, baseline
and account-denominator transformations are externally fixed.

`inference="regular_delta"` is the existing nominal-95% regular route.
It needs audit observations in both strata and rejects a Wilson audit interval
containing 1/2. Its result has status `computed`, a response/covariance and
`financial_value`, `financial_se`, `financial_interval`. This screened route
does not have uniformly valid inference across weak linkage. The new retained
study contains undercoverage even in a separated-rank finite regime.

`inference="weak_linkage_projection"` accepts `alpha` (default .05). It forms
four simultaneous sum/difference response bands and two exact binomial audit
intervals, with a fixed half/half error allocation. Its status is `computed_set`.
`financial_set` is a list of closed interval components:

```json
[{"lower": null, "upper": -1.0}, {"lower": 4.0, "upper": null}]
```

Here a null lower endpoint means negative infinity and a null upper endpoint
means positive infinity. An empty list means the supplied confidence region
has no model-compatible value. The whole real line is one component with
both endpoints null. These are meaningful mathematical results; no point
estimate or standard error is fabricated. Calibration with zero observations
has probability region [0,1]. A missing evaluation stratum or unsupported
variance is rejected, because the selected observable-response inference
has no qualification for that experiment.

Projection uses response moments and correctness-count audits. Its set can
be wider than the sharp identified set under an additional full mixture
likelihood; outcome-linked audits would also add information absent here.

The projection's audit coverage is finite-sample under representative accurate
independent binomial audits; its response coverage is asymptotic under the
documented stable dependent law and nuisance conditions. It removes a lower
bound on mapping rank from the projection step, not every regularity condition
from the statistical experiment. The result contains both the conditions and
the confidence level. Selection of the procedure after inspecting its width
does not preserve either procedure's stated coverage.

`treasury_report` preserves the monetary set. `application_result` divides
every component by an externally fixed finite positive account count.
Scientific identity binds source assertions/view, materialized data,
pilot/calibration arrays, economic target, nuisance procedure, inference
choice, confidence level and error allocation. Physical worker count does
not change that identity. Unsupported inputs raise `ValueError` before a
successful result; computed NaN output is not a valid contract response.

The financial result is conditional on source truth, causal price innovation,
pilot invariance, accurate representative audits and noninformative
per-origin whole-history swaps. Numerical validation cannot verify these
assumptions. Persistent crosswalks, joint ownership and selected/noisy audits
need separately derived observation laws.

# Funding request version 3

Construct `FundingRequest(brief, inference=...)` before fitting, and call
`run_funding_request`. The method is required. Choose `regular_delta` for
the retained research interval, or `weak_linkage_projection` for the
prespecified projection. No selection by observed interval width is allowed.
The legacy `run_funding` function retains its original regular default for
compatibility; migrate callers explicitly. Its outputs now carry the same
qualification as version 3.

Raw results, treasury reports, application reports and serialized dictionaries
retain `inference` schema version 1: method, nominal confidence, sampling unit,
identification conditions, numerical status, observed calibration evidence and
scope. A computed regular interval is marked `research_only_adverse_calibration`.
This does not claim that metadata repaired its undercoverage. Monetary rescaling
requires a fixed supplied denominator and preserves this description.

An empty set remains empty, two rays remain disconnected, an unbounded endpoint
is JSON `null`, and unavailable calculations carry their reason. `null` is not a
zero or missing observation. Numeric success and scientific qualification are
separate result properties.

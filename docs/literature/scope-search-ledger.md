# Scope search and selection record

Reviewed 9 October 2026; publication cutoff 7 October 2026. Technical evidence comes from primary text; metadata only discovers and identifies sources.

| Query | Matches | Returned |
|---|---:|---:|
| t01_forward_dml_longitudinal | 30 | 30 |
| t01_forward_linkage | 0 | 0 |
| t01_forward_lmtp | 0 | 0 |
| t01_forward_lp | 352 | 100 |
| t01_forward_lpc | 26 | 26 |
| t01_forward_panel | 7633 | 100 |
| t01_forward_prox | 22 | 22 |
| t01_refined_lp | 23 | 23 |
| t01_refined_panel | 376 | 40 |
| t01_search_discovery | 58 | 15 |
| t01_search_latent | 454 | 15 |
| t01_search_longitudinal | 1983 | 15 |
| t01_search_organization | 8175 | 15 |
| t01_search_panels | 1964 | 15 |
| t01_search_responses | 2906 | 15 |

## Method decisions

### Persistent responses

Keep reduced-form LP theorem separate from IV residual-test sets; same-target covariance comparison and source-specific selection/population limits.

Primary chain: newey1986, stock2018, inoue2023, casini2025.

### Short dynamic panels

Difference versus system moments require distinct initial laws; no implemented Windmeijer correction. CUE pseudo-target does not rescue a failed causal interpretation.

Primary chain: arellano1991, blundellbond2023, kleibergen2021.

### Longitudinal, latent and censoring

Observed-history exchangeability, labelled invariant measurements and proxy existence/completeness are different identifying information. Irregular observations are not latent full paths.

Primary chain: hernan2020, lmtp2023, sequentialdr2018, sarkka2013, bennettprox2023, zhangprox2024, wei2026, ran2026.

### Temporal graph to effect

Temporal graphical target/completeness distinctions; selected runtime output retains endpoints. Conditional effect completion is not a general PAG confidence theorem.

Primary chain: runge2020, gerhardus2020, perkovic2018, gerhardus2021, rohekar2023.

### Observation construction and linkage

Conditional mismatch and truthful independent validation; candidate grammar completeness and answer truth remain separate.

Primary chain: slawski2025, hernan2020.

### Reusable estimation and public finance

Substantive runtime matching, explicit folds and weights; public sample lacks survey-design fields. No broad package or empirical causal-truth qualification.

Primary chain: dml2018, doubleml2022, runtime_doubleml_scope, runtime_tigramite_scope, public401k.

## Coverage limits

- Question-led bounded metadata queries, not an exhaustive systematic review or full citation-graph census.
- OpenAlex relevance/title filters and capped pages miss unindexed or differently phrased work. Large panel forward result is dominated by applications; refined search remains bounded.
- Pinned primary preprints may differ from identified journal versions; no version substitution or comprehensive correction clearance.
- No scholarly claim is supported by a search title alone.

- LMTP exact arXiv lookup failed; the title/journal search yielded W4287771461 with zero indexed forward matches. Duplicate/incomplete indexing is possible; zero results do not establish absence of later work.

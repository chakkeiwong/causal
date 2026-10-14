# D: automatic organization of observation histories

Specification v1, 8 October 2026. Input comprises raw customer/account events,
actions, outcomes, linkage versions and macro release vintages. Oracle
semantics used by A–C are fixed independently of the automatic algorithm.

Candidate interpretations select unit/key, event clock, availability clock,
revision relation, aggregation rule and entity crosswalk. The initial grammar
is deliberately finite and inspectable. Hard constraints reject impossible
types, duplicate version identities, broken temporal order and violated
declared accounting identities. Evidence ranking orders surviving hypotheses;
it is not a causal-validity probability.

Return a unique observation plan only when surviving material interpretations
agree on the information required by the request. Otherwise retain
alternatives, summarize differences in eligible histories/targets and
abstain from a unique plan. No implicit deduplication of repeated decisions;
no future revision enters a historical decision view. Economic action roles,
instrument exclusion and exchangeability are supplied assumptions.

Generate raw fixtures with revisions, late arrivals, multiple accounts,
ambiguous household links and stocks/flows. Know the true observation
operator and inject ambiguities that genuinely cannot be resolved from
records alone. Compare accepted-mapping accuracy, abstention and downstream
effect/value error to the oracle view. Probabilistic linkage is introduced
only with calibrated probabilities and a justified propagation method.

Inspect installed columnar engines and dataml's actual interfaces read-only;
perform local examples in this repository. Existing evidence sources include
sw_duckdb, sw_polars, sw_splink, sw_feast and the observation chapter.
Evaluate complete history reconstruction cost, not a precleaned table scan.

Completion requires an implemented bounded mechanism and explicit evidence
for its consequences, with the distinction between lineage and causality
retained throughout the product interface.

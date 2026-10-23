# Preserve the customer observation before estimating its effect

A usable customer history must establish which unit a record represents, which
relationship connects records, when its information became usable and why some
customers are absent. Account ownership, person identity, household membership
and an influence network are distinct relationships. A common phone number
can propose a match without settling any of them. Linking, storing and joining
records can support causal analysis, but the assignment and observation models
must still justify the requested effect. The proposed library should carry
those distinctions through the CLI and MCP result rather than silently resolve
them in a preprocessing step. \citep{exec17_s7_paths,exec22_obs_reference}

## Matchers provide evidence with a specified scope

AWS Entity Resolution's inspected guide distinguishes Simple and Advanced
rules, with fuzzy comparisons and Boolean expressions in Advanced rules.
The rule type, ordering, normalizations, job and resulting groups must survive
export. Its many-to-many matching term concerns comparisons across input
fields sharing a match key; it is not an ownership model. Transitive matching
is documented as an Advanced API-only option selected when creating a
workflow. The specified earliest-rule and smallest-identifier resolution can
make rule order consequential; the guide warns about inappropriate grouping.
Retain the source rows and connecting records so a false merge can be
investigated. \citep{exec22_obs_aws_er_manual}

The same guide distinguishes group confidence from record confidence and
describes cleartext rather than hashed comparisons in its ML path. Neither
confidence field is automatically a calibrated probability over complete
customer histories. Error partitions for invalid/repeated identifiers must
remain in the denominator, including the documented cases that can still
incur charges. Provider workflows require separate entitlement. QualityStage
11.7.0 supplies a tunable probabilistic matching workflow, a Match Designer,
one- and two-source stages and pass statistics; the inspected overview does
not specify all weight, blocking, threshold and uncertainty-export mechanics.
Those are source-acquisition obligations before a detailed causal integration
claim. \citep{exec22_obs_aws_er_manual,exec22_obs_ibm_matching}

Splink's inspected README supplies an open-source alternative for pair
prediction and clustering in a Fellegi-Sunter workflow. Its reported
performance remains project-reported, and the saved hash does not identify a
later mutable branch. A candidate Python adapter should preserve pairs,
blocking coverage, comparison information and field clocks. Pair probabilities
cannot generally supply coherent uncertainty over exclusive complete mappings
or network exposures. Porting the matcher into another language would not
repair that missing model. A conditional source-specific composition is more
defensible than a universal linkage-and-inference claim. \citep{exec17_s7_paths}

## Complete-map uncertainty can change the financial sign

Take treated outcomes (8,6) and control outcomes (4,2) under one complete map;
a second map swaps those pairs. The two arithmetic contrasts are 4 and -4.
Randomized assignment, consistency and no interference would be needed for
a correctly linked difference to estimate an average causal effect. Stipulate
probability p for the first whole map. The mean contrast is 8p-4; at p=4/5
it is 12/5. This p is an assumed joint mapping probability, not a vendor score
or four independent pair confidences. At USD 10 per outcome unit and USD 30
action cost, the hard-map margin is 10 but the integrated margin is -6. The
integrated margin is positive only when p>7/8. \citep{exec22_obs_reference}

For a separate uncertainty fixture, add independent equiprobable noise -1/2
or 1/2 to either map mean. Conditional variance is 1/4; between-map variance
is 64p(1-p). Exact enumeration at p=4/5 gives total variance 1049/100.
Ignoring the map uncertainty retains only 1/4. This is a finite known-law
witness, not an estimated standard error for four fixed observations or a
coverage guarantee. A future service must distinguish uncertainty under a
specified mapping model from a sensitivity set over scientifically possible
maps. \citep{exec22_obs_reference}

## Availability is not established by an event timestamp

Databricks documents AS OF feature lookup on an entity key and a designated
time-series timestamp; merely including a timestamp in a primary key does
not enable the same semantics. The Unity Catalog and legacy Workspace APIs
differ. The selected manuals return the latest prior value or null, preserve
a latest eligible null rather than skipping it, and describe legacy merge
behavior that leaves absent keys unchanged. Training/batch lookback rules
also differ from online retrieval of the latest value and snapshot publishing.
The adapter must bind the actual client, table and serving contract.
\citep{exec22_obs_databricks_pit,exec22_obs_databricks_feature}

For a historical decision at t, the latest feature version should be eligible
under both event time e<=t and availability time a<=t, with an explicit rule
for corrections and mapping vintages. The exact fixture has value 2 at
(event,availability)=(8,9), and value 9 at (9,12). At decision time 10, an
event-only lookup over today's records gives 9 while the admissible value is
2. This is a counterexample to an inadequate timestamp interpretation, not
a recorded vendor defect. No admissible row requires a declared missing
result; the engine must not fall back to a future record.
\citep{exec22_obs_reference}

Snowflake Time Travel provides storage-state recovery within retention, with
the inspected one-day default and up to 90 days for eligible Enterprise
permanent objects. Increasing retention cannot restore already expired
versions. AT and BEFORE boundaries have different meanings, and historical
queries retain current-definition and access-rule consequences. Preserve
schema, query boundary, time zone, ingestion and dictionary evidence. A
warehouse snapshot is evidence about warehouse storage; operational knowledge
at the action time needs its own availability account. Expired history must
remain an explicit failure. \citep{exec22_obs_snowflake_time,exec22_obs_snowflake_at}

## Inclusion and qualification retain every request

Even perfectly correct retained matches can change the population. With two
equally common strata of effects 6 and 2 and retention probabilities 1 and
1/4, the complete-population effect is 4 while the linked effect is 26/5.
Normalized inverse-inclusion weighting returns 4 under the stipulated
positive inclusion law and conditional transport of potential outcomes.
It need not work when matching depends on unobserved outcomes. Auditing only
easy successful joins cannot establish truth in the omitted population.
\citep{exec22_obs_reference}

A public prototype can generate hidden known identities, separate household
and ownership relations, corrupt identifiers, delayed corrections and known
treatment laws. Keep truth out of matcher inputs and use separate calibration
and evaluation samples. Compare exact-key joins, an original-language
probabilistic matcher, corrected-clock retrieval and the proposed wrapper
under the same information. Measure false merges/splits, exclusions by stratum,
future-information violations, effect error, justified uncertainty and
assumed decision loss. Preserve errors, timeouts and unavailable alternatives
in the workload and cost denominator.

The source identities remain limited: AWS's PDF was generated after cutoff,
Databricks displays September 2026 updates, IBM names 11.7.0 and Snowflake
does not authenticate an exact service revision. Unread vendors and source
mechanics, cutoff equality, licenses, native execution, field calibration
and bank validation remain open. The proposal recommends conditional reuse
of matching, retrieval and storage capabilities with explicit causal contracts;
it does not claim that those integrations are already implemented.
\citep{exec22_obs_aws_er_manual,exec22_obs_databricks_pit,exec22_obs_ibm_matching,exec22_obs_snowflake_time}

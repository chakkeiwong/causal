# Scientific protocol and executable reference, version 0.4

Version 0.4 adds semantic declarations and scalar/vector/curve, graph/effect
set and fixed-policy value results. See [request schema](v04-request.schema.json),
[result schema](v04-result.schema.json), [semantics](../../src/causalbank/scientific.py)
and [standalone examples](../../docs/studies/standalone/). The result flattens
named axes in their declared order; covariance includes the sampling divisor.
Confidence, posterior and sensitivity meanings are distinct. Null interval
endpoints represent infinities; a null numerical-error bound is unknown.
The initial graph objects are finite DAG sets and temporal coefficient boxes;
PAG syntax is preserved but general PAG recognition/inference is not implemented.

Run a complete saved request from the repository root:

```bash
python3 tools/causal_study.py docs/studies/standalone/A-G-request.json --output /tmp/causal-response-result.json
```

The six standalone recipes are A-G, A-I, B-H, B-L, C-G and C-T. They require
the exact model/reward/sampling families stated in the monograph. This is a
research reference, not a generic service. No supplied assumption is validated
merely because its declaration passes. The separated-block learned-IV
comparison runs through `python3 tools/study_response_extensions.py`.

`python3 tools/qualify_interfaces.py` executes selected installed-package and
semantic checks. `python3 tools/standalone_examples.py` regenerates the local
requests, data and results and checks sibling field mappings. These commands
do not write to or establish accepted runtime integration with siblings.

## Preserved scalar design, version 0.3.0-proposal

The operation catalogue and schemas specify the interfaces in chapters 18–19
of the reconstructed monograph. They are proposed data contracts, not an
implemented scientific service. Run `python3 tools/check_scientific_contracts.py`
to regenerate the explicitly labelled fixtures and validate them.

A request binds four content-addressed specifications: causal model and
assumptions, observation and decision clock, target and population, and sampling
experiment. It selects one operation and the requested uncertainty object.
Structured mathematical languages inside those specifications remain a later
implementation task. The validator can check bytes and selected invariants;
it cannot establish exchangeability, exclusion, stationarity or identification.

A result reports computation, identification and inference separately. A timeout
may retain an already established identification proof, but it cannot invent a
nonidentification witness or claim completed estimation. Unsupported execution
does not mean a causal target is unidentified. Identified functionals, exact
identified sets, outer bounds and same-law/different-target witnesses carry
different artifact roles. A result for an outer bound does not assert sharpness.

Uncertainty for scalar quantities is a canonical ordered union of intervals.
A null lower endpoint means negative infinity; a null upper endpoint means
positive infinity. Infinite endpoints are open. An empty array represents an
empty test-inversion set and must be explained by its inference artifact.
This representation preserves two disjoint rays, the entire line and empty
sets. It does not implement arbitrary multivariate confidence regions, graph
distributions or curve bands. Those require a new explicitly typed version;
no projection to one interval is permitted silently.

The fixtures contain a schematic weak-IV set, an identification-only result,
a same-law witness, an unsupported computation, a timeout, a graph outer bound,
and an empty confidence set. Their numbers are protocol examples, not fitted
results or validated inferential procedures. Positive and negative checks cover
hash changes, result/request mismatch, uncertainty type, endpoint topology,
missing proof/witness, false availability and computation/identification
confusion. Reusable temporal and score components remain separate evidence.

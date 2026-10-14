# Research contracts and proposed scientific protocol

The current bounded additions use [funding inference v3](inference-v3.md)
and [three experiment journeys](closure-journeys.md). These executable local
contracts preserve qualifications in public consumers and reject unsupported
compositions. The historical schemas below remain narrow research artifacts.

The version 0.1.0 schemas at this directory's root are narrow research
demonstrations of study identity, temporal events, scalar results and graph
endpoints. Their scalar result schema cannot represent the full scientific
interface in the reconstructed monograph. They are retained for reproducibility,
not recommended as a general product API.

The [scientific protocol](scientific/README.md), version 0.3.0-proposal,
defines proposed requests and results for the seven bounded operations in
chapters 18–19. Its schemas preserve identification, computation and inference
as separate states, including disconnected or unbounded scalar confidence sets.
These are reviewable design artifacts with executable validation examples.
They do not implement estimators, adapters or causal assumption verification.

Run the local tools/check_contracts.py script from the causal repository. It
validates examples, rejects selected scientific/temporal errors, and checks
artifact hashes. Regenerating numerical results requires refreshing references.

An adapter must preserve population, treatment/comparator direction, horizon,
currency, action version, independent units, inference method and evidence class.
Unavailable estimates are null with an explicit scientific status. Confidence
intervals, posterior credible intervals and identified sets are different objects.
Unresolved PAG endpoints must never be converted to directed DAG arrows silently.

Historical feature events must occur and become available by the decision.
A known future contractual schedule can have a later event time, but its
availability must still precede the decision. This schema represents raw
measurements; imputation draws need a separate recovery artifact with masks.

The check implements selected invariants, not a full study compiler.
The proposed service API, estimator adapters and bank-specific semantic review
are described in the reconstructed monograph. Another repository may inspect
and validate these local examples; adopting the protocol requires a separately
qualified adapter. No sibling adapter has been built or executed.

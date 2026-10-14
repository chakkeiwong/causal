# IN02 author review: shared semantic contract

12 October 2026. Outcome: **design pass only**. The four promised design
outputs define one versioned request/result meaning for a planned library,
JSON CLI and MCP surface. The reference Python checks and JSON Schema 2020-12
documents are part of this review, not evidence that those surfaces run. IN04
must implement and exercise them; IN05 must test complete consumer workflows.

## Scientific and interface decisions

The target is bound by a context digest covering the population, intervention,
outcome, contrast, horizon, units, sign, event/availability/decision clocks,
sampling law, declared assumptions and graph. A caller must supply a causal
target for identification, design, estimation, sensitivity or observation
audit. An effect result cannot silently change units or sampling law. The
result separates invocation state, scientific disposition and qualification:
completed/unsupported is possible, while a successful transport never by
itself means identified, precise or accepted.

The set representation keeps the difference between empty, unknown,
bounded, disconnected, unbounded and whole-line answers. `null` endpoints
represent infinities; an unknown set has `intervals: null`, while the empty
set has `intervals: []`. Pointwise confidence, simultaneous confidence,
posterior credibility and sensitivity have different labels and required
construction evidence. A declared DAG receives node/endpoint, self-edge,
duplicate-edge and cycle checks. DAG and temporal graph **sets** require
content-hashed member artifacts; they cannot be flattened to one edge list.
This is a representation rule, not a full PAG/CPDAG/temporal class recognizer.

Large inputs use opaque artifact IDs, declared SHA-256 and local custody; no
request field accepts an arbitrary path or URL. A future resolver must verify
bytes, root containment, symlinks, read authority and schema before use. A
durable application job has immutable input/code/seed/budget identity, bounded
work, status, cooperative cancellation and checkpoint rules. The design
distinguishes an in-flight RPC cancellation from a returned durable job. Its
CLI mapping specifies JSON input/output and exit behavior, including an exit
zero for an honestly negative scientific answer.

## MCP version choice and primary evidence

The official specification is pinned to repository commit
`9174102eb93895c3416228a6d2ecceb0c9dbfa2c`, committed before the
2026-10-07 Asia/Shanghai cutoff. The first implementation target is legacy
**2025-11-25** over local stdio, paired with Python SDK **1.27.0**. The
SDK's saved `types.py` declares `LATEST_PROTOCOL_VERSION = "2025-11-25"`.
At that revision, initialization/version negotiation, newline JSON-RPC,
structured tool results, error separation, resource APIs, progress and
cancellation have inspected primary anchors in `source-audit.json`. The
2026-07-28 specification instead uses per-request metadata and
`server/discover`; claiming compatibility with it from a legacy SDK would
conflate two protocol eras. Modern and dual-era support therefore remains a
separately tested future branch. The SDK is not installed in this Python and
no client/server exchange was run for IN02.

## Adversarial review and limits

Twenty schema/semantic tests pass. The review added typed graph edges,
content-hashed graph-set membership, nested artifact constraints, DAG cycle
checks and rejection of completed effects from cancelled jobs. It also tests
whole-line versus unknown/empty answers, disconnected sets, refusals,
changed sign/clock/units/sampling law, pointwise-to-joint promotion,
invocation errors and qualification without evidence. `contract-tests.xml`
contains the test receipt. These are design checks, not method accuracy or
bank acceptance tests.

The reference validator cannot establish assumption truth, actual timestamp
ordering, independent sampling, graph-class completeness, artifact custody,
budget enforcement, endpoint authentication, replay safety or the semantics
of arbitrary result payloads. It does not yet run a library dispatcher, CLI,
MCP server, third-party adapter or bank workflow. Result `payload` is intentionally
operation-specific and requires typed runtime validators before promotion.
No claim is made that FinMarketing, dataml, MacroFinance, BayesFilter or
CardNPV have integrated with this contract. IN04 can start from this design;
IN03 awaits the open-source adoption decisions in SW07.

## Criterion judgment and continuation

IN02-C1 passes as a **specified and reference-tested representation**:
numerical topology, scientific refusal/unsupported status and invocation
failure have distinct serialized states. IN02-C2 passes as a **specified
custody and job policy** with no runtime enforcement claim. IN02-C3 passes as
an explicit schema/operation version and legacy MCP compatibility choice,
with modern support deferred. The remaining engineering work is to implement
the resolver, typed dispatcher, CLI, real MCP server/client exchange and
fault/conformance trials under IN04. SW01 and LA01 remain independent ready
survey work. All original scientific gaps remain unqualified by this design.

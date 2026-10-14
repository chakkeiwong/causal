# IN04 implementation and review plan

12 October 2026. This package implements the accepted IN02 contract in this
repository. It does not change sibling repositories or claim bank adoption.

The first runtime will expose the exact supported subset through
`capabilities.describe`: graph syntax review, the existing supplied-DAG
back-door expression, declared Gaussian moment-set inversion, deterministic
quadratic sensitivity sets, observation-clock diagnostics and evidence-report
construction. Missing business/LLM/discovery/design engines return an explicit
unsupported disposition. Reports use durable jobs; small supported operations
also exercise the synchronous path. Input artifacts are supplied locally by the
operator and referenced by opaque content identities in scientific requests.

One dispatcher validates schemas and context digests and returns canonical
responses. The CLI and MCP server call that dispatcher. The MCP implementation
targets 2025-11-25 and uses the reviewed 1.27.0 SDK in an isolated repository
environment if installation succeeds; no modern-protocol claim is planned.
The real SDK client must initialize, list tools and call them over stdio.
Protocol stdout remains separate from logs and worker output.

The artifact store will reject unknown/changed handles, symlink/root escape
and oversized reads. Its configured local root cannot be changed by a request.
Jobs record immutable request/input/code identities, budgets, checkpoint state,
terminal result and cancellation. Idempotency reuse with changed inputs must
fail. Workers will not evaluate shell strings, import arbitrary user modules,
contact sibling services, upload data or call a model. Bounded worker processes
separate timeout and memory failure from scientific nonidentification.

Before recording a pass, compare actual library, CLI and MCP outputs for
finite, empty, whole-line and disconnected/unbounded cases, unsupported and
invalid requests, and at least one supplied-DAG identification example.
Exercise artifact mutation/root escape, idempotency collision, output and
time budgets, cancellation, restart/checkpoint identity and the no-upload/no-
arbitrary-code boundary. Record observed failures and repairs. If an SDK or
runtime path cannot execute, retain an honest incomplete/negative disposition;
schema inspection alone cannot pass IN04.

Review questions: are negative scientific findings distinct from transport
errors; do graph, uncertainty, units and clocks survive; can a tool argument
change permissions; are cancelled/partial jobs mistaken for finished results;
does a recovered request retain its original identity; and do advertised
capabilities match actual executions? Matched algorithm qualification, external
consumer conformance and platform-scale acceptance remain SW08/IN05/X03.

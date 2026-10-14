# IN04 author review: executable local interfaces

12 October 2026. **Pass in the declared local reference scope.** The library,
CLI and real MCP server now share one validated dispatcher, artifact store
and job runtime. Eleven scientific cases agreed exactly across all three
surfaces. Real SDK 1.27.0 initialization, tool discovery and calls negotiated
MCP 2025-11-25 over local stdio. Additional checks exercised report submission,
terminal job status and cancellation, bounded resource reads, denied raw-data
resources, invalid requests and unknown-tool JSON-RPC errors.

## Implemented behavior

Nine advertised operations actually execute: exact capabilities, declared graph
syntax checks, the existing supplied-DAG back-door expression, supplied-moment
Gaussian residual-test inversion, deterministic quadratic sensitivity sets,
observation timestamp diagnostics, durable reports, job status and job cancel.
Method IDs and scientific domains are narrow and explicit. Problem formulation,
data-driven causal discovery and design comparison have no engine in this
runtime and are not advertised as implemented MCP tools; canonical library/CLI
requests return unsupported. The numerical operations do not fit arbitrary
learners or infer the truth of their model/sampling declarations.

The moment and sensitivity artifacts bind the complete scientific-context hash.
Changing sign, units, target or clock requires a different input artifact. Results
preserve empty, whole-line and disconnected/unbounded sets. Gaussian moment
inversion remains conditional on its moment approximation and supplied
covariance; a sensitivity inequality is labeled nonprobabilistic. Contradicted
declared premises refuse identification/estimation. Unknown or failed back-door
adjustment is not promoted to a theorem of nonidentification.

Artifacts are canonical JSON with content and descriptor hashes, opaque IDs,
operator-local custody, bounded reads and nonsymlink regular-file checks.
The runtime root is launch configuration inside this repository's `.runtime`;
scientific requests cannot choose filesystem roots, Python imports, shell
commands, sibling writes or network endpoints. No model invocation or upload is
implemented. MCP resources expose only small summaries, reports and declared
responses; raw input artifact roles are excluded. This is a single local
operator model, not multi-tenant authentication or hostile-co-tenant isolation.

Scientific work uses fixed worker processes with address-space and wall limits.
The memory bound applies to the scientific worker, not the resident SDK and
coordinator process. Small control/error envelopes may exceed a caller's tiny
output limit to explain a refusal. Reports persist request, input, execution,
environment, budget and checkpoint identities. A checkpoint is a hashed prefix
of work IDs. Publication is atomic; retry is bounded at three attempts under the
original job deadline. Idempotency collisions reject changed requests or code.
Cancellation reports the observed terminal state and never claims to undo a
completed publication. Reports clearly label input scientific/qualification
fields as declarations; they validate schemas rather than independently
re-qualifying those claims.

## Validation and repairs

The persisted transport trial has eleven matched scientific cases: capabilities,
graph syntax, a supplied-DAG back-door expression, finite/empty/whole-line/
disconnected sensitivity sets, weak-moment inversion, an unsupported method,
a refused premise and a late observation. Both structured MCP content and its
JSON text copy matched library and CLI outputs. Report submission and terminal
status/cancel also matched. Version probes requesting an older legacy version
or a modern version receive only the tested 2025-11-25 choice; modern-only
clients must disconnect. Modern discovery/per-request metadata and HTTP are
not implemented.

Nine fault cases passed: deterministic replay with conflicting-budget rejection,
wall timeout, output limit, worker memory limit, kill/restart with checkpoint,
cooperative cancellation, changed artifact bytes, changed scientific context,
and changed checkpoint refusal. The actual restart trial killed a report worker
after its first checkpoint and completed all 100 distinct work IDs once. These
are engineering fixtures, not a preregistered scientific coverage evaluation.
The 16 local runtime/service tests and the frozen 20 IN02 schema/semantic tests
pass; the current receipts record exact code and environment identities.

Failures were investigated and retained in `execution-findings.md`. An initial
server syntax error was repaired before any conformance claim. The SDK's thread
wakeup hangs under this managed sandbox, including a minimal anyio diagnostic;
the same diagnostic and full harness pass in the explicitly approved local
execution environment outside that sandbox. This environmental qualification
limit matters for operators. A replay test then found that capability calls
bypassed the idempotency conflict check; the code was repaired and the test
passed. The SDK decorator normally converts an unknown tool into an execution
error, so a small adapter guard now returns the protocol error required by the
pinned specification. Prior passing attempts remain archived because the final
suite contains stronger cases and updated source identities.

## What this does not close

The design and local surfaces pass IN04-C1 through IN04-C3. This is not a bank
service, a modern-MCP implementation, general causal discovery, a full
cross-language adapter suite, external consumer acceptance or a calibrated
arbitrary inference engine. Scientific assumptions, graph truth, real bank data,
license decisions for other packages and institution-scale recovery remain
separate. IN03 awaits SW07 adoption decisions; IN05 awaits the required adapter
and agent prototypes. MR03 remains open until its actual integration chapters
and whole-workflow evidence pass IN06. MR01/MR02 remain open too.

## Local invocation

From the repository root, use `.runtime/in04/bin/python` with `PYTHONPATH=src`.
The operator may set `CAUSALBANK_STATE_ROOT` to a nonsymlink subdirectory of
`causal/.runtime`. `python -m causalbank.cli_v12 --help` describes the local
JSON CLI. `operation OP --input request.json` runs a canonical request; `artifact
put --schema-version VERSION --role ROLE` imports operator-supplied JSON from
stdin. The library entry is `causalbank.runtime_v12.Runtime.invoke`. MCP starts
with `python -m causalbank.mcp_server_v12`; its stdout is protocol-only.

Run the reviewed local MCP harness through the saved approved command
`.runtime/in04/bin/python tools/qualify_in04_v12.py` in the environment where
the SDK thread wakeup works. Requalification creates fresh runtime directories
and retains previous trial records. Do not overwrite frozen IN04 evidence after
recording its receipt; a later change needs a successor attempt and evidence.

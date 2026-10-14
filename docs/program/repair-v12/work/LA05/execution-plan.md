# LA05 implementation and review plan

12 October 2026. Build one local provider-neutral controller around the frozen
LA02 validator and IN04 runtime. Inputs are explicit offline fixtures or saved
model proposals, not new endpoint calls. Preserve problem/graph/evidence bytes,
proposal/prompt/model identities and all refusal/ambiguity states.

1. Validate the proposal envelope and full LA02 declarations. Verify local
   evidence hashes under docs, without interpreting retrieved text as commands.
2. Require an operator-supplied grant bound to the exact declaration for tool
   execution. The proposal cannot grant operations, insert code, set file paths
   for tools or authenticate an assumption. This is an in-process trusted
   caller boundary; bank authentication remains unavailable.
3. Project only a declared binary static population ATE into the existing
   narrow service. Retain the complete original declaration as an artifact.
   Refuse unsupported target mappings; keep every relevant graph candidate.
   Explicit sampling and numerical-input choices come from the external grant.
4. Route graph review, identification, discovery and moment-set requests to
   fixed operations. Preserve unsupported discovery and graph classes, conditional
   inference and exact set topology. No bank action operation is permitted.
5. Use immutable proposal identities, local locking and atomic journaling.
   Recheck sources on replay; inject interruption after a saved tool result and
   verify recovery without replacing or dropping it. Record predecessor snapshots.
6. Test source injection, forged review/grants, nonfinite/malformed payloads,
   late information, changed targets, graph ambiguity, unsupported mapping,
   disconnected sets, source tampering, replay, corrupted journal and revision
   lineage. Run actual local fixed tools in representative end-to-end cases.

Plan review: do not add a generic code executor, dependency on a model provider
or installation of collected research code. A replayed proposal is not a model
quality result. Successful syntax/transport is not causal qualification. Frozen
upstream evidence and code stay byte-identical. Reuse their tested runtime and
create a separate controller/tests. Compile the implementation discussion into
the explicitly interim reader after verification; visual acceptance is pending
a fresh session.

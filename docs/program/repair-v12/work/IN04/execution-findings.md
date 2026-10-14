# IN04 observed failures and repairs

12 October 2026. These are author execution notes, not product claims.

1. Initial server startup failed with an unclosed dictionary comprehension.
   Corrected syntax before testing; all later client/server trials started.
2. Both a direct initialize probe and the SDK client stalled under the managed
   sandbox. A five-second faulthandler probe showed anyio's worker thread idle
   and the event loop waiting. A two-second `anyio.to_thread.run_sync` diagnostic
   timed out in the sandbox and passed outside it. The user-approved fixed local
   conformance harness therefore runs outside the sandbox, with no networking,
   sibling writes or user-selectable commands. This is an operating limitation,
   not an inferred bank-platform pass.
3. The replay test changed a request budget under the same idempotency key but
   capability calls skipped the replay path. Routed that operation through the
   shared identity check. Subsequent local tests and trial passed.
4. Source review showed the SDK call-tool decorator catches unknown-tool errors
   as `isError`. Added a protocol guard outside that wrapper, checked an unknown
   tool returns JSON-RPC -32602, and restricted negotiation to the pinned revision.
5. Runtime input review added schema and full-context hashes to numeric/clock
   artifacts. A changed sign/target now fails rather than reusing the same data
   with altered scientific meaning. Added explicit refusal of contradicted
   identification/estimation premises.
6. Checkpoint review added prefix/digest checks, a three-attempt cap and the
   original submission deadline. The final trial killed a real child worker
   after a checkpoint and recovered 100 distinct report work IDs without
   duplicates. An altered checkpoint was refused; cancellation produced no
   published result in its exercised case.

Attempt artifacts are retained under `attempts/`. The final
`qualification-checkpoint.json`, `transport-checks.json` and `fault-trials.json`
identify the executed runtime. Installation and distribution source/license
copies are separate from the October 7 scholarly cutoff.

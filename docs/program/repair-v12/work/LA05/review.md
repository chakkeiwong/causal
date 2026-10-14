# LA05 author implementation review

12 October 2026. The local prototype passes in its explicitly narrow semantics
and fixed-tool execution scope. It supplies no live-model or bank capability
qualification.

The reviewed plan is executed by `src/causalbank/agent_workflow_v12.py` and the
bounded fixture runner. Exact proposal/prompt/model records, source byte checks,
separate declaration-bound caller grants, complete declaration artifacts and
graph candidates survive the handoff. The mapping refuses unsupported dynamic,
weighted or selected-population targets. Discovery remains an explicit
unsupported operation. Review names in a proposal do not grant authority.

Eighty tests across the new controller, LA02 declarations and IN02 semantics
pass. The 29 controller cases cover target/clock/graph conflicts, permissions,
injected document instructions, stale source/numerical bytes, malformed/nonfinite
outputs, missing inputs, disconnected sets, interruption, exact replay, journal
corruption and predecessor identity. Representative execution exports six paths,
including blocked funding/observation, unsupported servicing, ambiguous graphs,
conditional directed identification and unbounded moment sets. Every exported
artifact descriptor is checked against the canonical value bytes.

Failures and repairs are preserved:

1. Initial run: 7 failed / 19 passed. Per-operation frozen schemas disallow the
   general context's optional variable-clock fields. The projection now uses the
   common field subset; the complete clocks remain in the bound declaration.
   Upstream frozen schemas were not edited. Their inconsistent optional-field
   allowance is a limitation for future adapter authors.
2. First repair: 3 failed / 23 passed. The 256 MiB address-space ceiling caused
   numerical import/decompression failures. The fixed bound now matches IN04's
   tested 1 GiB setting; 26 initial controller cases then passed.
3. Additional review required source-byte rechecking on complete replay,
   declaration-schema hashes in execution identity, exact prompt-byte identity,
   retained predecessor/proposal artifacts, typed model arrays, a sixteen-step
   operation bound and contradiction/numerical-tamper tests. Final combined run:
   80 passed, including 29 controller cases.

Review boundaries: no authentication service is implemented; the caller and
local store are trusted. The journal detects unapproved identity changes and
ordinary corruption, not a malicious operator rewriting both state and hashes.
The retrieval fixture establishes nonexecution of instructions, not universal
prompt-injection resistance or source-truth validation. Recovery is local and
single-host. Usage from imported model records is unverified and must remain
null. The exported synthetic sampling declarations and moment summaries are
assumptions, not bank evidence. No downloaded research code was executed.

LA05-C1–C3 pass within these boundaries. Dynamic/longitudinal adapters, general
discovery and identification, live backend quality, authentic data and expert
acceptance remain open. The chapter is an interim draft; visual acceptance and
the full MR02 scholarship/page gate remain pending.

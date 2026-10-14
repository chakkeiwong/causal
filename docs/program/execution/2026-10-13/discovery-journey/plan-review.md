# Discovery workflow: reviewed design and continuation

Recovered 13 October 2026 from the active `IN.JOURNEY.DESIGN.discovery`
operation. The saved draft contained 19 authored cases and no registered final
trial. Its source and fixtures are preserved under `recovered-draft/`.

The deliverable is a proposal-level workflow design and a bounded execution of
the available local service. The scientific question is the twelve-month USD
effect of making an offer to an eligible account. Its target, population,
intervention, information clock, sampling unit, graph, assumptions and units
travel together. Graph discovery, general graph-class identification and a
bank-ready decision engine remain proposed capabilities.

1. Review the dispatcher, graph and result validators, artifact store, replay
   identity and CLI. Compare each expected result with an explicit small graph,
   elementary inequality or timestamp ordering. Preserve the saved draft.
2. Repair the test runner's restart behavior before freezing it. Save imported
   artifact references atomically before fault injection; after a restart use
   those same references. Add observed-confounder adjustment, omitted and latent
   confounding, invalid mediator adjustment, and the PAG identification boundary.
3. Freeze 24 cases, their exact contexts and expected results, code/dependency
   identities, 98 invocation slots, resource limits and the all-request rule.
   Record the design, then register the local trial prospectively. No outcome
   from a schema preflight is a final runtime result.
4. Execute library and CLI initial/restart calls in bounded segments. Retain all
   responses, errors, durations and process exits. Two additional same-key,
   changed-horizon requests must be rejected. Compare semantic responses after
   excluding only the request correlation ID. Continue from saved requests;
   do not erase negative results or alter the frozen design.
5. Review exact outcomes and restart prefix preservation. Record the local
   operation and develop the discovery workflow discussion in the integrated
   reader. Continue the next eligible lane; this plan creates no permission gate.

## Findings resolved before registration

The draft re-imported an intentionally corrupted artifact on each phase. The
store correctly rejects that second import, so the runner would have stopped
before it could ask the service to reject the corrupted reference. The revised
runner checkpoints the reference before corruption and reuses it on restart.
Atomic journal replacement prevents an ordinary interrupted write from leaving
a half-written JSON document. A process can still die between a service call and
the journal commit: resumption may repeat that invocation, using the same key.
This is bounded replay, not a claim of exactly-once execution across a crash.

The two-node DAG alone is an insufficient check of adjustment. In the added
fork `offer <- risk -> value`, observing and adjusting for risk blocks the
back-door path. Omitting risk leaves it open; a latent risk cannot be adjusted
for. Adjusting for the mediator in `offer -> risk -> value` fails the selected
back-door criterion. These failures concern that method, not a proof that every
causal identification strategy fails. Both CPDAG and PAG inputs must retain
their marks under syntax review and remain unsupported by the DAG method.

The four numerical references follow by factorization: `1-x^2 <= 0` gives two
rays, `1+x^2 <= 0` is empty, `-1-x^2 <= 0` gives the whole line, and
`(x-1)^2 <= 0` gives the singleton. They test deterministic sensitivity-set
serialization. They cannot establish sampling coverage, sharp identified sets,
graph discovery accuracy or numerical certification near arbitrary roots.
The timestamp reference admits exactly the record satisfying
`event <= available < decision`; equality at the decision, a missing timestamp,
and availability before the event are failures.

Changing a target sign after importing a moment artifact must fail context
matching. Corruption must fail byte/hash validation. Retaining a key while
changing the horizon must cause a conflict. A syntax pass verifies declared
syntax only; an imposed DAG and unverified assumptions remain conditional.
Repeated months are outside the independent-unit identification method.

The study counts all 98 invocation slots, including invalid, unsupported,
refused, failed and replayed requests. A correct refusal is a passed boundary
check, not an available causal estimate. CLI exit status and scientific
disposition are reviewed separately. The frozen passing rule requires every
case and every semantic-parity comparison to agree with its declared reference.
No sampling error probability is attached to a finite authored-case screen.

Resource reporting includes process launch, failed requests and replay in
invocation wall time, and fixture import/journaling in active runner time.
Between-segment pauses and initial interpreter/module startup are excluded and
identified. Child and parent RSS are process high-water readings, not concurrent
process-tree memory or bank service levels. Analyst effort, data procurement,
graph elicitation, adapter implementation, live-model calls, external review and
deployment are unmeasured cost categories, with no invented monetary estimate.

Contract doubles can show how a consumer interprets a typed result but cannot
prove an actual sibling integration. No sibling is run. An authentic owner-run
case needs an accepted request, source clock and unit map, response trace,
restart/failure results and an owner disposition. Those later inputs do not
block this proposal's local design. No paid or live LLM backend is called.

Author review: proceed with this bounded design. It tests current behavior and
refusal preservation; a complete discovery-to-effect product and the original
scientific gaps remain unqualified. The review is not independent acceptance.

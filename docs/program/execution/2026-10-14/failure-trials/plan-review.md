# Failure, partial publication and recovery: reviewed proposal plan

Operation: IN.REQ.failure_trials. Continue independently after the R temporal
coverage outcome. This is proposal evidence about the existing local reference
implementation, not product development or target-platform qualification.

1. Preserve and bind existing IN02/IN04 and artifact-custody evidence. Those
   trials already cover transport parity, killed workers, cancellation,
   changed contexts and two custody limitations; do not manufacture new credit
   by simply retelling those results.
2. Run a bounded new generated suite with each request and outcome retained:
   valid response; changed units; changed schema; unsupported method; tiny
   output budget; unchanged replay and corrupted replay; content published
   before metadata; report worker killed after its first checkpoint; report
   artifact committed before the terminal job state; corrupt checkpoint.
3. Use a fresh isolated directory under causal/.runtime for each scenario.
   Fault hooks exist only in the test process, at explicitly named publication
   boundaries. Spawn no agents, contact no service and modify no library source.
   Kill only the child launched for that case. Bound each wait at10 seconds,
   each recovery at20 seconds and all requested job lifetimes at25 seconds.
4. Save primary-source hashes, complete generated requests/results, injection
   descriptions and negative observations. Label normal runtime, instrumented
   execution, source inspection and proposed repairs separately. A caught
   harness exception is not a canonical service refusal.
5. Develop the recovery contract and integrate the substantive explanation into
   a preserving monograph. Check exact output identities and duplicate-free
   completed work, not merely a successful exit. Review both operation criteria,
   register the outcome and continue another eligible lane.

Review: deterministic injection resolves a particular interruption window; it
does not estimate failure rates or exercise every filesystem/OS crash ordering.
Existing source hashes and all completed outputs remain unchanged. Bank inputs,
named consumer acceptance, platform guarantees and authentication remain later
conditional work. No new upstream R or LLM result is claimed. Rendered visual
acceptance remains open under the inherited exhausted image allowance.

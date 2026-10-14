# Common scientific evaluation and resumption protocol

The master governs every new R01-R05 attempt. Existing final requests remain
baseline evidence. They are never relabeled fresh evaluation data. The
protocols and journals already delivered stay frozen.

## Argument before draws

1. State target, units, clock, observation law, assignment/audit law, sampling
   unit, model class and exact uncertainty claim. Define what extra information
   is required and who could supply it.
2. Derive identification, influence/error terms, nuisance rates, dependence
   and numerical error for that same experiment. Inspect relevant primary
   technical anchors; retain source identity/version/hash/claim records and
   unavailable-source omissions.
3. Implement an independent small reference: enumeration, analytic moments,
   dense algebra, high-accuracy likelihood or certified structural bounds.
   Exercise misleading declarations and invalid/unavailable outputs.
4. Review the derivation and reference before choosing a final procedure.
   Record a failure or unresolved theorem as such; no final study is required
   to disguise an unresolved identification problem.
5. Freeze a protocol and all substantive input/code hashes using the canonical
   register command. The protocol must contain task_id, task_contract_sha256,
   target, model, observation_law, sampling_unit, method, assumptions,
   uncertainty_claim, alternatives, adverse_cases, metrics, acceptance_rules,
   replications, seed, stopping_rule, derivation_review and input_sha256.
   The derivation_review is a path/hash/inspected-anchor record.

The registered stopping_rule is fixed_design_no_outcome_stopping. Replications
and seed are integers. Compute repetition requirements from the exact binomial
Monte Carlo precision and multiplicity family before final draws. The program
does not prescribe another arbitrary 600-request study. Freeze a tolerated
Monte Carlo error for the actual claim, justify the finite count and report
the realized intervals even when the target precision is missed.

## Acceptance dimensions

For a claim of minimum finite coverage c (normally 0.95), require a scoped
scientific argument and a prespecified empirical rule. The default empirical
screen requires a simultaneous one-sided exact-binomial lower bound at least
c in every claimed valid-law cell. State the multiplicity family and confidence
level before draws. A bound merely containing c, or conditional coverage among
the few finite outputs, is insufficient. This screen can be inconclusive for
a procedure whose true coverage is exactly nominal; such a result is not a
proof of failure. It does not establish uniform validity between grid cells.

An asymptotic argument can justify a conditional research output while finite
qualification remains open. Do not silently replace the finite claim with
asymptotic wording and mark the original gap closed. A predeclared scientific
scope revision needs a separate reviewed attempt.

Report all-request coverage; conditional coverage; finite/disconnected/
whole-line/unavailable counts; width and its distribution; point bias;
reported SE versus empirical SD; sensitivity; actual labels and history rows;
complete runtime, peak memory, serialization and recovery; and information
acquisition assumptions. Report paired differences with their sampling
uncertainty when methods share requests. Keep oracle diagnostics separate from
deployable methods.

Coverage alone does not establish a useful product. Whole-line answers can be
correct and useless. Availability and width criteria must be frozen for the
declared research task. Bank width/loss/risk thresholds and actual costs are
external inputs, not values invented to obtain acceptance. No precision
tolerance is lowered after results. Calendar variance floors must appear in
audit design and economics.

## Journals, failures and evidence

Before evaluation, write a launch record referencing the registered protocol
hash and actual start time. A final receipt references that registration, a
hash-bound complete journal and explicit retention of failed/unavailable
requests. The engine rejects a final experiment whose stated start predates
registration. Clock/identity checks are auditable controls, not independent
proof of when a person ran a computation.

Use immutable request IDs from design/version/seed/cell/repetition, bounded
batches and atomic result publication. On disconnect, inspect the journal and
resume missing IDs under the existing registration. Never replace an old
partial run, silently change a seed or count retries as fresh requests.
Reconstruct saved summaries from request rows before qualification.

Preserve implementation failures and their effect on qualification. If code
or inferential design changes after final draws begin, disposition that attempt,
retain its protocol/code/journals, and reopen a reviewed successor with a fresh
registration. Unchanged source-only reporting corrections require substantive
review; they do not automatically require expensive simulations again.

## Disposition and continuation

Every work-package criterion receives pass, fail or inconclusive plus an
inspected path/hash/anchor and a substantive finding. A passing research
package requires a registered evaluation and all promised outputs. A negative
or inconclusive package may end at a reviewed analytical obstruction without
fabricated results. Its scientific capability remains open.

Every non-control receipt also contains gap_dispositions for all its assigned
gaps: qualified_in_declared_scope, conditional_progress, unresolved or
external_pending. A passing package with conditional progress does not qualify
that gap. Negative/inconclusive work cannot qualify a gap. The final decision
gate requires the explicit qualification dispositions from all required
predecessors, in addition to their package outcomes.

The engine retains the prior contract/result/registration on reopen, and
rejects reopening underneath resolved dependent work. A reviewed whole-program
revision is required in that case. Other ready branches proceed without a
permission checkpoint. Revision is warranted by a new argument, corrected
defect or changed information, not by disappointment with an honest result.

A reopen revision contains task_id, prior_contract_sha256, reason,
new_information_or_argument, a hash-bound review, and new_contract. Retain the
same task ID, kind and gap obligations, but use new versioned output paths.
Old inputs, journals and reviews remain immutable and are still checked.

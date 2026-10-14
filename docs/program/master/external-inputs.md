# External input contracts and exact resumption

All seven input groups below are missing; named owners are unassigned. This
preparation neither contacts anyone nor creates acceptance. Preserve the
[V8 protocol](../external-validation-v8.md) and [V9 delta](../external-validation-v9.md).
They supply fuller trial details, supplemented by the current linked-audit
information contract.

| Input ID | Required participants and evidence | Reject or defer when |
|---|---|---|
| independent_review | Independent causal/dependent-data reviewer; identity/conflicts; original signed claim-by-claim report, reconstruction and unresolved findings, scoped to exact assessed release. | Reviewer is an author, evidence concerns a different release, or material findings remain unresolved. |
| bank_truth | Bank question sponsor, assignment-system owner, source/clock owner, independent audit-truth owner and custodian. Frozen target, availability/revision calendar, assignment mechanism, sampling frame/probabilities, audit ledger, independently sampled gold labels, ownership meaning and adjudication failures. | Exogeneity/instrument or experiment is unjustified; inclusion/truth is unknown/selected; ownership is undefined; data are unauthentic or incompatible with the claimed model. |
| pilot_and_prices | Independent history owner and acquisition/finance owner. Invariant independent pilot lineage; actual linked-history, count-label, gold-label and history costs; precision/loss/risk thresholds; independent design-pilot variance inputs. | Overlapping evaluation histories are called independent, prices are planning guesses, or attainable precision cannot meet the question. |
| platform | Operator and recovery lead. A manifest of hardware, software, storage, network and concurrency; agreed service thresholds; frozen whole-workload and fault schedule; original logs, hashes and costs. | Local single-host evidence substitutes for target operation, a partial result is exposed, or recovery/data integrity/service objectives fail. |
| consumers | Standalone and application maintainers. Accepted operation/version/units/qualifiers; actual executed valid/refusal/whole-line/changed-input fixtures; signed acceptance. | Source inspection or author-owned adapters are presented as adopted integration; qualifiers/units are lost. |
| workflow | Independent evaluator, workflow lead and analysts. Prespecified matched task/order and quality grading; active labor, rework/defects, elapsed time, labels/history, training/review and infrastructure costs; held-out value evidence. | Fit time is reported as analyst savings; unsuccessful tasks or quality differences disappear. |
| sponsor_decision | Institutional investment sponsor and operating owner. Agreed release scope; risk/cost/value criteria; original signed accept/reject/defer decision and operating obligations. | Author approval is substituted for the institution or qualification failures are silently excluded. |

Start data/owner preparation when its authorized input arrives; X01-X03 final
dispositions reference the integrated I01 release. An independent reviewer may
challenge the frozen baseline earlier. If a later release changes claims, that
challenge is not automatically acceptance of the changed claims.

## Intake format

Run: python3 tools/causal_program.py intake INPUT_ID --receipt PATH

The JSON receipt must identify input_id, origin = external, owner name/role/
organization, scope, agreed_criteria, baseline_manifest_sha256, a signed_evidence
path/sha256/anchor and nonempty input_sha256. Use the current baseline manifest
identity from state.json. Include the assessed I01 release identity when final
acceptance is sought; the historical baseline hash alone is insufficient.

A local evidence reference must point to an authorized owner-provided
attestation or reviewed manifest. Bank data stay in approved custody; no raw
customer identifiers or confidential datasets belong in the public research
archive. The receipt can bind a custody manifest without copying bank data.
The script checks shape and identities, not signature authenticity, scientific
truth or legal access. The named owner/reviewer must substantiate those facts.

A final X/F receipt must use independent or external_owner review kind and
reference original signed evidence. X01 specifically requires independent
review. Its signed_evidence and assessed_release fields are path/hash/anchor
records; assessed_release must identify the I01 delivery manifest. Merely
inventing a person or choosing a different string is not
acceptance. Missing owners remain blockers, not author tasks to mark complete.

## Resumption and handoff

Supply the relevant owner and frozen evidence, record intake, and run next.
Complete required prerequisites before the final acceptance trial. Use the
registered rejection criteria, retain the original signed findings even when
negative, and record the decision against the exact package contract. No new
user approval checkpoint is needed for already authorized local preparation.
External messaging, access grants and actual institutional deployment require
their own authorization.

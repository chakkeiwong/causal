# Additional V12 receipt requirements

Use `python3 tools/causal_program_v12.py template TASK` and the V12 record command.
The preserved core still requires every criterion, scope, limitations, bound
evidence, promised outputs and separate D-gap dispositions. This extension adds
the requirements below. It checks artifact integrity and structured evidence,
not the truth of an author's scientific or editorial judgment.

For SW09, LA07 and IN06 passing receipts, add `repair_acceptance` with:

- `coverage_complete: true`, `blocking_findings: []`;
- `coverage_review`: bound JSON with repair_id, status=pass, cells matching all
  required IDs, each with status, finding, essential boolean and bound evidence;
  non-substantive statuses require an omission_review reference; essential
  unavailable material cannot pass;
- `source_audit`: bound JSON with status=pass, unverified_claims=[] and nonempty
  entries. Each entry records identity, version_date, inspected_anchors,
  supported_claims and local_copy (path/SHA-256/anchor). Scholarly papers also
  record kind=paper, filename_title, first_author and year and must be genuine
  named PDFs under docs/papers;
- `chapter_review`: bound JSON with status=pass, blocking_findings=[], every
  planned chapter ID with substantive=true and a finding, exact pdf_sha256,
  rendered_pages_inspected (all physical pages), and body_page_numbers matching
  the page allocation record. The finding explains argument, notation,
  assumptions, alternatives, banking examples and any deficiencies;
- `page_count`: the promised PDF's bound reference and a unique list of
  body_page_numbers. Actual PDF page count bounds this list. Bibliography,
  inventories, logs, blanks and repeated baseline pages are excluded;
- `page_budget_exception`: null within budget, or a bound reviewed JSON record
  with repair_id, rationale and coverage_unchanged=true. This cannot waive a
  missing subject or required executed claim.

For SW08, LA06 and IN05, any final empirical result requires the inherited
registered-experiment contract. If no final evaluation can run, an inconclusive
receipt may instead supply evaluation_status=unavailable and nonempty
unavailability_evidence references. This permits critical synthesis without
inventing a run; it cannot produce a positive qualification.

I02's manifest contains `repair_receipts` mapping MR01/MR02/MR03 to the accepted
SW09/LA07/IN06 receipt hashes, and `documents` containing bound monograph and
sponsor PDFs. All three scholarship gates must pass first.

External X01–X04/F01 receipts retain assessed_release referring to I01 for
compatibility with frozen historical controls. Add assessed_current_release
referring to I02's exact delivered manifest and scope_release_sha256 matching it.
Signed evidence and findings must assess that current scope. I01-only external
evidence does not satisfy V12. This schema does not supply a digital-signature
verification service or create independent acceptance; provenance must be
inspected through the existing named-owner and signed-evidence contracts.

No completed V11 contract, result or attempt may be rewritten in place. A later
scientific successor or scope change requires a new reviewed migration.

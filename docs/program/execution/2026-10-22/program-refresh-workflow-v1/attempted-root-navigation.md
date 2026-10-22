# Causal banking research and product proposal

This workspace develops a scholarly monograph and product/investment proposal
for four banking journeys. The proposal remains unfinished. Public and generated
evidence should establish a bounded prototype's merit before expensive bank
experiments; bank validation, production qualification and adoption are later claims.

- [Current master program and execution rules](docs/program/execution/current-program.md).
- [Proposal scope and public-data portfolio](docs/program/master-program-proposal.md).
- [Mission Control](docs/mission-control.html) · [Markdown dashboard](docs/mission-control.md).
- [Canonical machine state](docs/program/state.json).
- [Current working monograph — 1,240 pages](docs/causal_proposal_workflow_reviewed_2026-10-22.pdf).
- [Paired working sponsor proposal — 50 pages](docs/sponsor_proposal_workflow_reviewed_2026-10-22.pdf).
- [Latest program review and remaining obligations](docs/program/execution/2026-10-22/program-refresh-workflow-v1/program-review.json).

Run from this repository:

```text
python3 tools/run_program_reviews_v2.py status
python3 tools/run_program_reviews_v2.py next
python3 tools/run_program_reviews_v2.py check
```

The controller selects eligible work and records evidence and reviewed successors.
An active author performs the research; there is no unattended research worker.
Independent branches continue across phase boundaries. Finish each canonical
transition before issuing a dependent one. A checkpoint preserves recovery state
and does not grant scholarly or institutional acceptance.

The working pair audits 932 monograph citations, including 221 genuine scholarly
PDFs, and 305 sponsor citations. Source/arithmetic and extracted-text checks have
passed. Coverage, mandatory repairs, fresh visual review and final proposal
acceptance remain open. The live program distinguishes publication snapshots from
subsequent progress so a completed source review is not repeatedly scheduled.

The [11 October master](docs/program/master-program.md) and its
[PDF](docs/program/master-program.pdf) are preserved historical plans.
`tools/causal_program.py status` and `check` inspect the historical package view;
`baseline` replays its original delivery checks. Use the current controller above
for the proposal queue.

Four prior scientific deliveries retain their original PDFs, evidence and
manifests. Seven mutable V10 control files are preserved under
[the pre-master archive](docs/program/history/pre-master-2026-10-11/README.md).
The canonical baseline command replays the original nested verifiers through
that historical view. Running the old delivery verifier directly against the
new master state mixes versions; do not rewrite old hashes to make it pass.

Literature cutoff: 7 October 2026. Every cited scholarly work needs its genuine
saved PDF and inspected technical anchors. New research retains all failed
and inconclusive evidence. Local author studies do not establish general
calibration, authentic bank truth, multi-host service levels, adopted sibling
interfaces or ROI. Sibling repositories remain unchanged. Read AGENTS.md before
continuing.

# Causal banking research and product program

The full product is unfinished. The current [integrated master program](docs/program/master-program.md)
accounts for all ten gaps across six research/product streams and four banking
journeys. Its 16 work packages distinguish completed investigations, qualified
capabilities, external acceptance and an institutional investment decision.

- [Read the master program PDF](docs/program/master-program.pdf).
- [Mission Control](docs/mission-control.html) · [Markdown dashboard](docs/mission-control.md).
- [Canonical machine state](docs/program/state.json) · [Plan review](docs/reviews/master-program-review-2026-10-11.md).
- [Current research reader — 259 pages](docs/causal_foundations_with_linked_audits_2026-10-11.pdf).
- [Sponsor proposal — V10 baseline, 16 pages](docs/sponsor_reconstruction.pdf).
- [Capability contracts](docs/program/master/capability-contracts.md) · [Evaluation protocol](docs/program/master/evaluation-protocol.md).
- [Missing external owners and inputs](docs/program/master/external-inputs.md).

Run from this repository:

```text
python3 tools/causal_program.py status
python3 tools/causal_program.py next
python3 tools/causal_program.py check
python3 tools/causal_program.py baseline
python3 -m unittest discover -s tests -p 'test_master_control.py'
```

The master command reports ready work, freezes protocols before final studies,
records hash-bound criterion evidence, validates external intake and retains
reviewed successor attempts. It does not perform mathematical research or
supply independent approval automatically. Status and check are read-only.
Use `python3 tools/causal_program.py --help` for the complete interface.
Work continues across ready branches without routine permission checkpoints.

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

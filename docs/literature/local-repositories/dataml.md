# Clearwater

The current execution plan is [Master Program v3.1](MASTER_PROGRAM_INTELLECTUAL_CONTRIBUTION_v3.1_PROPOSED.md). It separates the research trial from the manuscript assignment while retaining all six method families, both complete scenarios and S1/S2/S3. A runnable synthetic reference is delivered; shared scientific design, modern-model synthesis and actual-host triggering remain open.

Execution is in [Phase R, revision R3](docs/program_v3.1/REPAIR_PHASE.md), with a [durable continuation register](docs/program_v3.1/repair_state.json), bounded scientific repairs and an integrated A/B rehearsal before formal release. All three global proposal architectures have executed with negative results; conditional kernels remain candidates. Additional baseline datasets exposed B sampling modes now under explicit repair. The S3 precision ladder returns stop/refine; Linux worker recovery and [predictive review views](docs/program_v3.1/PREDICTIVE_REVIEW.md) are implemented. Checkpoints do not require renewed permission to continue ready development work. Independent gates remain pending.

Execution now includes [full A/B inference and modular comparators](docs/program_v3.1/INFERENCE_IMPLEMENTATION.md), [corrected flow/diffusion paths](docs/program_v3.1/LEARNED_PROPOSALS.md), and [persistent CLI/MCP investigations with evidence planning](docs/program_v3.1/REGISTRY_AGENT_AND_EVIDENCE.md). The [current visual review](docs/program_v3.1/execution/registry-agent-01/audit/review.html) shows completed initial and supplied-evidence fits for both scenarios, with failed attempts retained. The [proposal geometry review](docs/program_v3.1/execution/proposal-geometry-02/review.html) identifies the next ML conditioning problem. [The execution report](docs/program_v3.1/EXECUTION_REPORT.md) records costs and limits. Independent design review, comparative policy/ML evaluation and human/held-out host acceptance remain pending.

The [monograph draft](docs/monograph/main.pdf) still needs substantive reconstruction to explain the full methods self-containedly. The separate [monograph master program](MONOGRAPH_MASTER_PROGRAM_v1.0.md) and [Claude handoff](CLAUDE_MONOGRAPH_HANDOFF_v1.0.md) define that assignment, supported by a [gap audit](docs/monograph/MONOGRAPH_GAP_AUDIT_v3.0.md). The [shared design requirements](docs/program_v3.1/SHARED_DESIGN_REQUIREMENTS.md) connect the two tracks: comparative experiments need a reviewed scientific contract; whole-book acceptance is separate.

Run the complete reference investigation from the checkout:

```bash
python3 tools/research.py --database /tmp/clearwater.sqlite demo --output /tmp/clearwater-review
```

Open the generated `revision-0.html` and `revision-1.html`. The second result conditions on an explicitly supplied synthetic amount inspection; this command does not collect real evidence.

See the [runbook](docs/program_v3.1/RUNBOOK.md) for experiments, both full-scenario generators, method admission, MCP transport and acceptance gates. The portable launcher uses Python 3.11; MCP requires `mcp==1.27.0`. A full package installation also provides `clearwater-research`. The older `clearwater` command serves the existing governance interface.

The [coding-agent skill](integrations/skills/clearwater-review/SKILL.md) connects investigation requests to the admitted service. Its availability in a particular host must be configured and tested separately.

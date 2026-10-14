#!/usr/bin/env python3
"""Prepare a reviewed, immutable successor program; publish with the locked writer."""
import argparse
import copy
import json
from pathlib import Path

import master_control as core
import causal_program_v13 as control
import causal_program_current as prior_control

ROOT = core.ROOT
BASE = ROOT / control.BASE


def ref(path, anchor):
    return {"path": str(path.relative_to(ROOT)), "sha256": core.sha(path), "anchor": anchor}


def prepare():
    prior = core.read(ROOT, core.STATE)
    if prior["revision"] != "12.0-systematic-major-repairs":
        raise ValueError("Preparation requires unchanged V12 predecessor")
    snapshot = BASE / "predecessor-state.json"
    if snapshot.exists() and snapshot.read_bytes() != (ROOT / core.STATE).read_bytes():
        raise ValueError("Predecessor already saved with different bytes")
    snapshot.write_bytes((ROOT / core.STATE).read_bytes())
    tasks = []

    def task(identifier, name, kind, gaps, depends, steps, criteria, outputs, priority, **extra):
        t = {"id": identifier, "name": name, "kind": kind, "owner": "Authorized local research agent",
             "priority": priority, "gaps": gaps, "depends": depends, "requires_inputs": [],
             "steps": steps, "criteria": [{"id": identifier + "-C" + str(i+1), "statement": s} for i, s in enumerate(criteria)],
             "outputs": [control.BASE + "/work/" + identifier + "/" + p for p in outputs],
             "failure_action": "Preserve failures; do not narrow the claim or change final data to manufacture success. Record the exact obstruction and continue other eligible work.", **extra}
        tasks.append(t)
        return t

    dep = lambda i, outcomes=["pass"]: {"id": i, "outcomes": outcomes}
    allg = [f"D{i:02}" for i in range(1,11)]
    task("RG1", "Review successor arguments, information needs and stopping rules", "integration", allg,
         [dep("M03")],
         ["Analyze each failed or conditional predecessor without rerunning saved seeds.",
          "Derive what additional information or assumptions could change identifiability and uncertainty.",
          "Specify go/no-go conditions before any new qualification and check finite-screen power."],
         ["R02/R03/R04/R05/E01 and live evaluation each have an explicit obstruction, candidate remedy, matched comparator, stop rule and evidence requirement.",
          "Candidate derivations distinguish observable or obtainable inputs from oracle quantities and do not claim solved generalizations.",
          "Qualification separates theoretical coverage, Monte Carlo uncertainty, width, availability, scope and authentic bank usefulness."],
         ["feasibility.md", "design-checks.json", "review.md"], 75)
    successors = [
        ("R02S", "R02", "Research a valid persistent-map/calendar/audit successor",
         "Derive finite or justified asymptotic joint uncertainty under persistent identities, independent calendar information and estimated audit error. A supplied covariance oracle is a diagnostic, not a replacement.",
         "Test rank/near-rank, pair/date/gold growth, calendar persistence and adverse inclusion; preserve previous failing regimes or leave them explicitly unqualified."),
        ("R03S", "R03", "Research estimated loggers and policy selection with hidden states",
         "Separate identifiable history-based fixed-policy values from hidden-state policy optimality. Derive logging-law error and training/evaluation separation for a declared class.",
         "Compare supplied and estimated loggers, frozen and learned policies, weak overlap and hidden-state nonidentification; no unknown-optimum claim from fixed-policy evaluation."),
        ("R04S", "R04", "Research useful graph-to-effect sets with explicit added information",
         "Construct an observed-law confidence set over graphs and parameters with valid numerical outer bounds; state exactly which measurements or interventions exclude equivalent effects.",
         "Keep latent/weak-relevance and temporal failures; measure graph retention, effect coverage, finite availability and useful width jointly."),
        ("R05S", "R05", "Research dependent learners with justified remainder control",
         "Derive learner-specific rates, independent-pilot or separated-block arguments and weak-IV inversion before choosing a final learner and design.",
         "Retain high-dimension, larger-support and nonlinear adverse cases; never tune final penalties or confidence levels from qualification outcomes.")]
    for n, old, title, argument, experiment in successors:
        source = core.task_by_id(prior, old)
        task(n, title, "research", source["gaps"], [dep("RG1")],
             [argument, "Review mathematical and information feasibility; refuse final-study registration while design blockers remain.", experiment,
              "Freeze a fresh fixed design, retain all requests, and compare the successor with every predecessor acceptance obligation."],
             [c["statement"] for c in source["criteria"]] +
             ["A bound successor review approves the argument, observable inputs, fresh protocol and unchanged original obligation; new scope restrictions remain unqualified for the excluded regime."],
             ["derivation.md", "successor-review.json", "protocol.json", "results.json", "journal.json", "review.md"],
             {"R02S":220,"R03S":221,"R04S":222,"R05S":223}[n], successor_of=old)
    e = task("E01S", "Qualify complete computation and recovery on the target platform", "engineering",
             ["D06", "D07"], [dep("IN05", ["pass", "negative", "inconclusive"])],
             ["Freeze authentic workloads, resource budgets, environment, service levels and recovery semantics with the owner.",
              "Run whole workflows and multi-host fault trials; compare dense/streaming paths with identical scientific requests and all failures retained."],
             ["Meaning, graph/set topology, ordering and outputs match independent references across implemented interfaces.",
              "Target-platform time/memory/availability and resume/cancel/recovery meet predeclared owner criteria, including recorded sandbox limits.",
              "Owner acceptance and actual workloads are bound; local tests are not relabeled bank-scale evidence."],
             ["protocol.json", "results.json", "review.md"], 270, successor_of="E01")
    e["requires_inputs"] = ["platform", "consumers", "workflow"]
    live = task("LA06S", "Run a genuine held-out live LLM and agent evaluation", "research", allg,
                [dep("LA05"), dep("RG1")],
                ["Bind all five input classes before any live execution or spending.",
                 "Register independent held-out mechanisms and compare data-only, LLM-only, retrieval, hybrid and expert workflows.",
                 "Include label/counterfactual/temporal/latent ablations, semantic and effect loss, abstention, repeated runs and complete costs."],
                ["Actual live calls follow a frozen reviewed protocol; exposed fixtures are not held-out cases.",
                 "Equivalence-aware graph quality, valid formulation, downstream effect loss and failure rates use all-request denominators.",
                 "Exact backend/revision, custody, prices, token/time/review cost, adjudication and qualified numerical baselines are bound."],
                ["successor-review.json", "protocol.json", "results.json", "journal.json", "review.md"], 224, successor_of="LA06")
    inputs = [{"id": name, "owner_role": role} for name, role in [
        ("live_backend_custody", "Model backend and data-custody owner"),
        ("live_prices_budget", "Approved pricing and study-budget owner"),
        ("live_heldout", "Independent held-out mechanism/benchmark custodian"),
        ("live_adjudication", "Named independent adjudicators and rubric owner"),
        ("live_baselines", "Qualified numerical baseline evidence owner")]]
    live["requires_inputs"] = [x["id"] for x in inputs]
    task("X00", "Prepare precise external evidence and owner intake packets", "integration", allg, [dep("M02")],
         ["Create unfilled request/acceptance packets for bank truth, review, consumer/platform operation, live studies and economics.",
          "State the needed bytes, units, owners, custody, thresholds, exclusions and evidence checks without inventing a signatory or sending messages."],
         ["Every external input has a deliverable, authenticity check, affected task and acceptance criterion.",
          "Blank/unowned/unpriced packets cannot be admitted as external evidence."],
         ["intake-packets.json", "review.md"], 78)

    final = copy.deepcopy(core.task_by_id(prior, "F01"))
    replacement = {"R02":"R02S", "R04":"R04S", "R05":"R05S", "E01":"E01S"}
    final["depends"] = [dict(d, id=replacement.get(d["id"], d["id"])) for d in final["depends"]]
    for n in ["R03S", "E01S", "LA06S"]:
        if n not in {d["id"] for d in final["depends"]}: final["depends"].append(dep(n))
    final["criteria"].append({"id":"F01-V13", "statement":"The declared enlarged scope passes reviewed scientific/platform successors and an actual live evaluation; preserved negative/inconclusive predecessors are not rewritten."})
    final["steps"].append("Bind predecessor-to-successor scope comparisons. Any excluded regime remains an open gap; a narrower investment proposal requires a separately reviewed sponsor scope decision.")
    final["outputs"] = [control.BASE + "/work/F01/" + Path(p).name for p in final["outputs"]]
    gaps = copy.deepcopy(prior["gaps"])
    for g in gaps:
        g["closure_tasks"] = [replacement.get(t,t) for t in g["closure_tasks"]]
        if g["id"] in ["D02", "D09"]: g["closure_tasks"].append("R03S")
    contract = {"new_tasks":tasks, "revised_unresolved_tasks":[final], "new_inputs":inputs, "gaps":gaps,
                "scope_rule":"All original substantive obligations remain. Successors replace terminal attempt gates, not scientific standards. Negative predecessor evidence remains immutable."}
    core.write(BASE / "contracts.json", contract)
    state = copy.deepcopy(prior)
    state["revision"] = control.REVISION
    state["work_packages"] = [final if t["id"] == "F01" else t for t in state["work_packages"]] + tasks
    state["external_inputs"] += inputs
    state["gaps"] = gaps
    state["gap_execution"] = {"predecessor":ref(snapshot,"Complete preserved V12.1 state"),
        "plan":ref(ROOT / "docs/program/master-program-v13.md", "Reviewed current master program"),
        "documents":{}}
    for name,path in [("contracts",BASE/"contracts.json"),("review",BASE/"review.md"),
                      ("plan",ROOT/"docs/program/master-program-v13.md"),
                      ("plan_pdf",ROOT/"docs/program/master-program-v13.pdf"),
                      ("controller",ROOT/"tools/causal_program_v13.py"),
                      ("installer",Path(__file__)), ("tests",ROOT/"tests/test_gap_program_v13.py")]:
        state["gap_execution"]["documents"][name]=ref(path,"Reviewed V13 "+name)
    state["repair_program"]["master"] = "docs/program/master-program-v13.md"
    state["repair_program"]["controller"] = "python3 tools/causal_program_v13.py"
    state["deliveries"].append({"path":"docs/program/master-program-v13.pdf","sha256":core.sha(ROOT/"docs/program/master-program-v13.pdf"),"status":"reviewed_execution_program_visual_pending"})
    control.install_hooks()
    issues=control.validate_state(ROOT,state)
    if issues:raise ValueError(str(issues))
    core.write(BASE/"candidate-state.json",state)
    print(json.dumps({"prepared":True,"work_packages":len(state["work_packages"]),"preserved_outcomes":len(prior["results"])}))


def publish():
    state=core.read(ROOT, control.BASE+"/candidate-state.json")
    prior=state["gap_execution"]["predecessor"]
    if core.sha(ROOT/core.STATE)!=prior["sha256"]:raise ValueError("State changed after review")
    control.install_hooks()
    core.commit_state(ROOT, prior["sha256"], state,
                      {"action":"install_reviewed_gap_execution_v13","review":state["gap_execution"]["documents"]["review"],
                       "preserved_outcomes":len(state["results"]),"new_successors":6,"acceptance_claim":False})
    print(json.dumps({"published":True,"next":control.summary(state)["next"]}))


if __name__ == "__main__":
    p=argparse.ArgumentParser();p.add_argument("command",choices=["prepare","publish"])
    prepare() if p.parse_args().command=="prepare" else publish()

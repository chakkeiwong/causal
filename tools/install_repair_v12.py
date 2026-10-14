#!/usr/bin/env python3
"""Prepare/review a V12 state candidate, then atomically install that candidate.

No completed evidence is overwritten. Running prepare again is allowed only
before the canonical revision changes. Installation checks the expected prior
state hash, all evidence identities and an explicit reviewed installation record.
"""
import argparse
import copy
from pathlib import Path

import master_control as core
import repair_control_v12 as v12

ROOT = Path(__file__).resolve().parents[1]
BASE = v12.DIRECTORY
DOCUMENTS = {
    "work_packages": BASE + "/work-packages.json",
    "major_repairs": BASE + "/major-repairs.json",
    "chapters": BASE + "/chapter-plan.json",
    "coverage": BASE + "/coverage-contract.json",
    "schemas": BASE + "/evidence-schemas.json",
    "candidates": BASE + "/candidate-seeds.json",
    "workspace_seeds": BASE + "/workspace-seeds.json",
    "plan": "docs/program/master-program-v12.md",
    "plan_pdf": "docs/program/master-program-v12.pdf",
    "review": BASE + "/plan-review.md",
    "receipt_contract": BASE + "/receipt-contract.md",
    "controller": "tools/repair_control_v12.py",
    "entrypoint": "tools/causal_program_v12.py",
    "installer": "tools/install_repair_v12.py",
    "tests": "tests/test_repair_control_v12.py",
    "builder": "tools/build_repair_program_v12.py",
}


def prepare(root):
    before = core.sha(root / core.STATE)
    prior = core.read(root, core.STATE)
    if prior["revision"] != "11.0-integrated-master":
        raise ValueError("Prepare requires the preserved V11 predecessor")
    snapshot = root / BASE / "baseline-state.json"
    if snapshot.exists() and core.read(root, str(snapshot.relative_to(root))) != prior:
        raise ValueError("A different predecessor is already preserved")
    if not snapshot.exists():
        snapshot.write_bytes((root / core.STATE).read_bytes())
    external = []
    for task in prior["work_packages"]:
        if task["id"] not in v12.EXTERNAL:
            continue
        if task["id"] in prior["results"] or task["id"] in prior["registrations"]:
            raise ValueError("Cannot revise an already assessed external contract")
        revised = copy.deepcopy(task)
        revised["depends"].append({"id": "I02", "outcomes": ["pass"]})
        revised["priority"] = {"X01": 260, "X02": 261, "X03": 262, "X04": 270, "F01": 280}[task["id"]]
        revised["steps"] = [s.replace("final I01 delivery", "final I02 delivery") for s in revised["steps"]]
        revised["steps"].append("Assess the exact I02 delivery manifest and its three repair areas. Retain the legacy I01 lineage reference; bind assessed_current_release and scope_release_sha256 to I02.")
        revised["criteria"].append({"id": task["id"] + "-V12", "statement":
            "Signed acceptance assesses I02's current manifest and the enlarged software, LLM/agent and integration scope; I01-only acceptance is insufficient."})
        revised["outputs"] = [BASE + "/work/" + task["id"] + "/" + Path(p).name for p in task["outputs"]]
        external.append(revised)
    migration = {"revision": v12.REVISION, "previous_state": v12.reference(root,
        BASE + "/baseline-state.json", "Complete pre-migration V11 state"),
        "expected_previous_sha256": before, "external_contracts": external,
        "preservation": "All completed contracts/results/registrations, attempts and deliveries remain unchanged.",
        "reason": "User-required software, LLM/agent and CLI/MCP/workspace repairs before I02 and external acceptance."}
    core.write(root / BASE / "migration.json", migration)
    state = copy.deepcopy(prior)
    state["revision"] = v12.REVISION
    state["major_repairs"] = core.read(root, BASE + "/major-repairs.json")
    replacements = {t["id"]: t for t in external}
    state["work_packages"] = [replacements.get(t["id"], t) for t in state["work_packages"]]
    state["work_packages"].extend(core.read(root, BASE + "/work-packages.json"))
    plan_pdf = "docs/program/master-program-v12.pdf"
    state["deliveries"].append({"path": plan_pdf, "sha256": core.sha(root / plan_pdf),
                                "pages": core.read(root, BASE + "/build.json")["pages"]})
    state["latex_roots"].append(BASE + "/plan-reader.tex")
    state["repair_program"] = {"acceptance_release_task": "I02",
        "controller": "python3 tools/causal_program_v12.py", "master": "docs/program/master-program-v12.md",
        "migration": v12.reference(root, BASE + "/migration.json", "Reviewed scope and external contract migration"),
        "documents": {key: v12.reference(root, value, "Reviewed V12 " + key) for key, value in DOCUMENTS.items()}}
    core.write(root / BASE / "candidate-state.json", state)
    issues = v12.validate_state(root, state)
    if issues:
        raise ValueError("; ".join(issues))
    return {"candidate": BASE + "/candidate-state.json", "packages": len(state["work_packages"]),
            "next": v12.summary(state)["next"], "previous_state_sha256": before}


def install(root):
    state = core.read(root, BASE + "/candidate-state.json")
    migration = v12.bound_json(root, state["repair_program"]["migration"])
    installation = core.read(root, BASE + "/work/P12/installation.json")
    if installation.get("status") != "pass" or installation.get("blocking_findings") != []:
        raise ValueError("Installation needs a completed author plan review and checks")
    core.inputs_bound(root, installation)
    if installation.get("candidate_state_sha256") != core.sha(root / BASE / "candidate-state.json"):
        raise ValueError("Installation review belongs to another candidate state")
    v12.install_hooks()
    core.commit_state(root, migration["expected_previous_sha256"], state,
        {"action": "install_v12_major_repairs", "task_id": "P12",
         "migration": state["repair_program"]["migration"]})
    return {"status": "installed", "packages": len(state["work_packages"]), "next": "P12"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["prepare", "install"])
    args = parser.parse_args()
    import json
    print(json.dumps(prepare(ROOT) if args.command == "prepare" else install(ROOT), indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Preserve V12 evidence and govern explicit successors to unresolved claims."""
import contextlib
import copy
import io
import json
import subprocess
import sys

import master_control as core
import repair_control_v12 as v12
import causal_program_current as previous

REVISION = "13.0-reviewed-gap-execution"
BASE = "docs/program/gap-repair-v13"
RESEARCH = {"R02S", "R03S", "R04S", "R05S", "LA06S"}
LEGACY_PROTOCOL = core.validate_protocol


def validate_protocol(root, task, registration):
    LEGACY_PROTOCOL(root, task, registration)
    if task["id"] not in RESEARCH:
        return
    spec = core.read(root, registration["path"])
    gate = spec.get("successor_review", {})
    core.bound(root, gate)
    review = core.read(root, gate["path"])
    v12.require(review.get("task_id") == task["id"] and
                review.get("design_approved") is True and
                review.get("unresolved_design_blockers") == [] and
                review.get("scope_matches_contract") is True and
                review.get("retained_predecessor_failures") is True,
                "Final registration requires an approved successor argument and scope")
    v12.require(spec.get("screen_operating_characteristics") and
                spec.get("width_and_availability_rules") and
                spec.get("fresh_data_provenance"),
                "Successor protocol lacks screen power, useful output or fresh-data evidence")


def validate_receipt(root, state, task, receipt):
    # Retain every V12 closure, study and external-release gate.
    v12.validate_receipt(root, dict(state, revision=v12.REVISION), task, receipt)
    if task["id"] in RESEARCH and receipt["outcome"] == "pass":
        spec = core.read(root, state["registrations"][task["id"]]["path"])
        gate = spec.get("successor_review", {})
        core.bound(root, gate)
        review = core.read(root, gate["path"])
        v12.require(review.get("task_id") == task["id"] and
                    review.get("design_approved") is True and
                    review.get("unresolved_design_blockers") == [],
                    "Successor needs an approved argument and design before qualification")
        v12.require(review.get("scope_matches_contract") is True and
                    review.get("retained_predecessor_failures") is True,
                    "A reduced or oracle-only experiment cannot replace the original obligation")
        v12.require(receipt.get("scope_comparison") and receipt.get("information_requirements"),
                    "Successor must compare predecessor scope and required information")
        if task["id"] == "LA06S":
            v12.require(receipt.get("live_calls", 0) > 0,
                        "Offline execution cannot qualify a live study")


def validate_state(root, state):
    if state.get("revision") != REVISION:
        return v12.validate_state(root, state)
    try:
        revision = state["gap_execution"]
        for ref in revision["documents"].values():
            core.bound(root, ref)
        core.bound(root, revision["predecessor"])
        prior = core.read(root, revision["predecessor"]["path"])
        # Validate the frozen predecessor in its own scope, not against new contracts.
        issues = v12.validate_state(root, prior)
        if issues:
            return ["Preserved V12: " + x for x in issues]
        contract = core.read(root, revision["documents"]["contracts"]["path"])
        expected = {t["id"]: t for t in prior["work_packages"]}
        expected.update({t["id"]: t for t in contract["new_tasks"]})
        expected.update({t["id"]: t for t in contract["revised_unresolved_tasks"]})
        v12.require({t["id"]: t for t in state["work_packages"]} == expected,
                    "Unreviewed V13 work-contract change")
        v12.require(state["gaps"] == contract["gaps"], "Unreviewed gap/closure change")
        for key in ("streams", "major_repairs", "attempts", "baseline_manifest_sha256"):
            v12.require(state[key] == prior[key], "Changed preserved field: " + key)
        v12.require(state["external_inputs"] == prior["external_inputs"] + contract["new_inputs"],
                    "Missing or changed input obligation")
        for key in ("results", "registrations", "input_receipts"):
            for name, value in prior[key].items():
                v12.require(state[key].get(name) == value, "Changed historical " + key + ": " + name)
        for ref in prior["deliveries"]:
            v12.require(ref in state["deliveries"], "Historical delivery removed")
            core.bound(root, dict(ref, anchor="Preserved delivery"))
        for key, ref in prior["repair_program"]["documents"].items():
            v12.require(state["repair_program"]["documents"].get(key) == ref,
                        "Changed preserved V12 document: " + key)
        for changed in contract["revised_unresolved_tasks"]:
            v12.require(changed["id"] not in prior["results"] and
                        changed["id"] not in prior["registrations"],
                        "Cannot revise a completed or registered task")
        issues = v12.LEGACY_VALIDATE_STATE(root, state)
        if issues:
            return issues
        for name, ref in state["results"].items():
            validate_receipt(root, state, core.task_by_id(state, name), core.read(root, ref["path"]))
        return []
    except (ValueError, KeyError, OSError, TypeError, AssertionError) as exc:
        return [str(exc)]


def summary(state):
    out = v12.summary(state)
    out["controller"] = "python3 tools/causal_program_v13.py"
    out["program_view"] = state["gap_execution"]["plan"]["path"]
    out["successor_tasks"] = [t["id"] for t in state["work_packages"] if t.get("successor_of")]
    out["ready_means"] = "Argument/source/implementation work may begin; final research requires a reviewed registered protocol."
    return out


def render(root, state):
    out = summary(state)
    rows = ["# Mission control: causal banking master program V13", "",
            "The monograph and product remain unfinished. All three mandatory repairs remain open.", "",
            f"{len(state['results'])}/{len(state['work_packages'])} packages have recorded outcomes; "
            f"{len(out['qualified_gaps_in_declared_scope'])}/10 original gaps fully qualified. Next: **{out['next']}**.", "",
            "[Current program](program/master-program-v13.md) · [Program PDF](program/master-program-v13.pdf) · "
            "[Review](program/gap-repair-v13/review.md) · [Continuation](program/gap-repair-v13/continuation.md) · "
            "[State](program/state.json)", "",
            f"[Current working monograph]({state['reader']['path'].removeprefix('docs/')}) — "
            f"{state['reader']['pages']} pages; not I02 acceptance.", "",
            "V12 contracts and evidence remain preserved. V13 adds scientific and platform successors, "
            "explicit live-study inputs, and preparation of authentic external intake. It preserves all "
            "102 software cells, 14 LLM tasks, 12 integration requirements and 22 chapter allocations.", "",
            "| Package | Outcome/readiness | Remaining prerequisite |", "|---|---|---|"]
    rows += [f"| {r['id']} {r['name']} | {r['status']} | {'; '.join(r['blockers']) or '—'} |" for r in out["work_packages"]]
    rows += ["", "Research readiness permits argument development, not an unregistered final experiment. "
             "Negative predecessor findings remain valid historical evidence. No live calls or bank acceptance have been supplied.", ""]
    md = "\n".join(rows)
    (root / "docs/mission-control.md").write_text(md)
    html = subprocess.run(["pandoc", "--from=gfm", "--to=html"], input=md,
                          text=True, capture_output=True, check=True, timeout=20).stdout
    (root / "docs/mission-control.html").write_text("<!doctype html><meta charset='utf-8'><title>Causal program</title>" + html)


def install_hooks():
    core.validate_state = validate_state
    core.validate_receipt = validate_receipt
    core.validate_protocol = validate_protocol
    core.summary = summary
    core.render = render


def main():
    install_hooks()
    command = sys.argv[1] if len(sys.argv) > 1 else "status"
    if command == "check":
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            try:
                core.cli()
            except SystemExit as exc:
                if exc.code not in (None, 0):
                    print(stream.getvalue(), end="", file=sys.stderr)
                    raise
        result = json.loads(stream.getvalue())
        state = core.read(core.ROOT, core.STATE)
        prior = core.read(core.ROOT, state["gap_execution"]["predecessor"]["path"])
        result["preserved_working_document"] = previous.verify_working_document(core.ROOT, prior)
        if state.get("successor_document"):
            import build_gap_successor_v13 as successor
            result["successor_document"] = successor.check(state["successor_document"])
        result["scope"] += " V13 checks reviewed successor contracts, all retained V12 gates and preserved whole-book identities."
        print(json.dumps(result, indent=2))
    else:
        core.cli()


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError, AssertionError, subprocess.SubprocessError) as exc:
        raise SystemExit(str(exc))

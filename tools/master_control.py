"""Master work-package controls; no automatic science or institutional approval."""
import argparse
import collections
from datetime import datetime, timezone
import fcntl
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
STATE = "docs/program/state.json"
OUTCOMES = {"pass", "negative", "inconclusive"}
GAP_DISPOSITIONS = {"qualified_in_declared_scope", "conditional_progress", "unresolved", "external_pending"}
PROTOCOL_FIELDS = ("target", "model", "observation_law", "sampling_unit", "method",
    "assumptions", "uncertainty_claim", "alternatives", "adverse_cases", "metrics",
    "acceptance_rules", "replications", "seed", "stopping_rule", "derivation_review")


def now():
    return datetime.now(timezone.utc).isoformat()


def safe(root, name):
    p = Path(name)
    if p.is_absolute() or ".." in p.parts or not name:
        raise ValueError("Path must be relative to this repository: " + name)
    full = root / p
    if not full.resolve().is_relative_to(root.resolve()):
        raise ValueError("Path escapes the repository: " + name)
    return full


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def read(root, name):
    return json.loads(safe(root, name).read_text())


def digest_object(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")
    tmp.replace(path)


def bound(root, row):
    p = safe(root, row["path"])
    if not p.is_file() or sha(p) != row["sha256"]:
        raise ValueError("Missing or changed evidence: " + row["path"])
    if not str(row.get("anchor", "")).strip():
        raise ValueError("Evidence needs an inspected anchor: " + row["path"])


def inputs_bound(root, receipt):
    inputs = receipt.get("input_sha256", {})
    if not inputs:
        raise ValueError("Receipt has no bound inputs")
    for name, h in inputs.items():
        if sha(safe(root, name)) != h:
            raise ValueError("Changed receipt input: " + name)


def task_by_id(state, task_id):
    matches = [w for w in state["work_packages"] if w["id"] == task_id]
    if len(matches) != 1:
        raise ValueError("Unknown/duplicate work package: " + task_id)
    return matches[0]


def unmet(state, task):
    reasons = []
    for dep in task["depends"]:
        result = state["results"].get(dep["id"])
        if not result or result["outcome"] not in dep["outcomes"]:
            reasons.append("requires " + dep["id"] + " outcome " + "/".join(dep["outcomes"]))
    for name in task["requires_inputs"]:
        if name not in state["input_receipts"]:
            reasons.append("missing external input " + name)
    if task["id"] == "F01":
        for gap in state["gaps"]:
            for dep in gap["closure_tasks"]:
                if dep != "F01" and state["results"].get(dep, {}).get("gap_dispositions", {}).get(gap["id"]) != "qualified_in_declared_scope":
                    reasons.append(f"{gap['id']} not qualified by {dep}")
    return reasons


def validate_protocol(root, task, registration):
    bound(root, registration)
    spec = read(root, registration["path"])
    if spec.get("task_id") != task["id"] or spec.get("task_contract_sha256") != digest_object(task):
        raise ValueError("Protocol belongs to another work-package contract")
    for field in PROTOCOL_FIELDS:
        if spec.get(field) is None or spec.get(field) == "" or spec.get(field) == []:
            raise ValueError("Protocol missing " + field)
    if not isinstance(spec["replications"], int) or spec["replications"] <= 0:
        raise ValueError("Protocol needs a positive fixed replication count")
    if not isinstance(spec["seed"], int):
        raise ValueError("Protocol needs a frozen integer seed")
    if spec["stopping_rule"] != "fixed_design_no_outcome_stopping":
        raise ValueError("This program requires a fixed final design")
    bound(root, spec["derivation_review"])
    inputs_bound(root, spec)
    if not registration.get("registered_at"):
        raise ValueError("Protocol lacks a registration time")


def validate_intake(root, state, name, ref):
    bound(root, ref)
    row = read(root, ref["path"])
    if row.get("input_id") != name or row.get("origin") != "external":
        raise ValueError("External input needs an external provenance receipt")
    owner = row.get("owner", {})
    if any(not owner.get(k) or owner[k].lower() in {"tbd", "unassigned", "author", "unknown"}
           for k in ("name", "role", "organization")):
        raise ValueError("External input lacks an identified owner")
    if row.get("baseline_manifest_sha256") != state["baseline_manifest_sha256"]:
        raise ValueError("External input is scoped to another delivery")
    if not row.get("agreed_criteria") or not row.get("scope"):
        raise ValueError("External input lacks agreed scope/criteria")
    bound(root, row["signed_evidence"])
    inputs_bound(root, row)


def validate_receipt(root, state, task, receipt):
    if receipt.get("task_id") != task["id"] or receipt.get("task_contract_sha256") != digest_object(task):
        raise ValueError("Receipt belongs to another work-package contract")
    outcome = receipt.get("outcome")
    if outcome not in OUTCOMES:
        raise ValueError("Invalid research disposition")
    reviewer = receipt.get("reviewer", {})
    if not reviewer.get("name") or reviewer.get("kind") not in {"author", "independent", "external_owner"}:
        raise ValueError("Receipt needs a named reviewer and review kind")
    if task["kind"] == "external" and reviewer["kind"] == "author":
        raise ValueError("Author review cannot complete external acceptance")
    if task["id"] == "X01" and reviewer["kind"] != "independent":
        raise ValueError("X01 requires independent scientific review")
    if task["kind"] != "control":
        dispositions = receipt.get("gap_dispositions", {})
        if set(dispositions) != set(task["gaps"]) or set(dispositions.values()) - GAP_DISPOSITIONS:
            raise ValueError("Receipt needs a separate disposition for every assigned gap")
        if outcome != "pass" and "qualified_in_declared_scope" in dispositions.values():
            raise ValueError("Negative/inconclusive work cannot qualify a gap")
    if task["kind"] == "external":
        bound(root, receipt["signed_evidence"])
        assessed = receipt["assessed_release"]
        bound(root, assessed)
        if assessed["path"] not in task_by_id(state, "I01")["outputs"] or not assessed["path"].endswith("delivery-manifest.json"):
            raise ValueError("External acceptance must assess the integrated release manifest")
    if not receipt.get("scope") or not receipt.get("limitations"):
        raise ValueError("Receipt needs scope and remaining limitations")
    rows = receipt.get("criteria", [])
    if len(rows) != len(task["criteria"]) or {r["id"] for r in rows} != {r["id"] for r in task["criteria"]}:
        raise ValueError("Missing/duplicate acceptance criterion")
    verdicts = []
    for row in rows:
        verdicts.append(row.get("verdict"))
        if row.get("verdict") not in {"pass", "fail", "inconclusive"} or not row.get("finding") or not row.get("evidence"):
            raise ValueError("Criterion needs a finding, verdict and bound evidence")
        for ref in row["evidence"]:
            bound(root, ref)
    evidence_paths = {ref["path"] for row in rows for ref in row["evidence"]}
    if outcome == "pass" and set(task["outputs"]) - evidence_paths:
        raise ValueError("Passing disposition lacks bound promised outputs")
    if outcome == "pass" and any(v != "pass" for v in verdicts):
        raise ValueError("Passing disposition has unmet acceptance criteria")
    if outcome == "negative" and "fail" not in verdicts:
        raise ValueError("Negative disposition needs a failed criterion")
    if outcome == "inconclusive" and "inconclusive" not in verdicts:
        raise ValueError("Inconclusive disposition needs an inconclusive criterion")
    experiment = receipt.get("experiment")
    if task["kind"] == "research" and outcome == "pass" and not experiment:
        raise ValueError("Research qualification needs a registered evaluation")
    if experiment:
        registration = state["registrations"].get(task["id"])
        if not registration:
            raise ValueError("Unregistered experiment")
        validate_protocol(root, task, registration)
        if experiment.get("registration_sha256") != registration["sha256"]:
            raise ValueError("Experiment used another protocol")
        if datetime.fromisoformat(experiment["started_at"]) <= datetime.fromisoformat(registration["registered_at"]):
            raise ValueError("Evaluation began before registration")
        bound(root, experiment["journal"])
        if experiment.get("retained_failures") is not True:
            raise ValueError("Evaluation must retain failed and unavailable requests")


def reopen_task(root, state, task_id, revision_ref):
    """Retain a resolved attempt; never revise underneath completed dependents."""
    task = task_by_id(state, task_id)
    if task["kind"] not in {"research", "engineering"} or task_id not in state["results"]:
        raise ValueError("Only resolved research/engineering attempts can reopen")
    descendants = {task_id}
    while True:
        expanded = descendants | {t["id"] for t in state["work_packages"]
                                  if any(d["id"] in descendants for d in t["depends"])}
        if expanded == descendants:
            break
        descendants = expanded
    if (descendants - {task_id}) & set(state["results"]):
        raise ValueError("Resolved downstream work requires a reviewed program revision")
    bound(root, revision_ref)
    revision = read(root, revision_ref["path"])
    if revision.get("task_id") != task_id or revision.get("prior_contract_sha256") != digest_object(task):
        raise ValueError("Revision belongs to another prior contract")
    if not revision.get("reason") or not revision.get("new_information_or_argument"):
        raise ValueError("Reopening needs a reason and changed information/argument")
    bound(root, revision["review"])
    replacement = revision["new_contract"]
    if replacement["id"] != task_id or replacement["kind"] != task["kind"]:
        raise ValueError("A successor must retain its task identity and kind")
    if set(replacement["gaps"]) != set(task["gaps"]):
        raise ValueError("A successor cannot drop assigned gap obligations")
    if set(replacement["outputs"]) & set(task["outputs"]):
        raise ValueError("Successor outputs must use new versioned paths")
    state.setdefault("attempts", []).append({"contract": task,
        "result": state["results"].pop(task_id),
        "registration": state["registrations"].pop(task_id, None), "revision": revision_ref})
    state["work_packages"] = [replacement if t["id"] == task_id else t for t in state["work_packages"]]


def validate_state(root, state):
    issues = []
    try:
        if state.get("schema_version") != 3:
            raise ValueError("Expected master schema version 3")
        tasks = state["work_packages"]
        ids = [t["id"] for t in tasks]
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate work-package ID")
        if len(state["gaps"]) != 10 or {g["id"] for g in state["gaps"]} != {f"D{i:02d}" for i in range(1, 11)}:
            raise ValueError("Master must account for D01--D10 exactly")
        if {s["id"] for s in state["streams"]} != {f"S{i}" for i in range(1, 7)}:
            raise ValueError("Missing original program workstream")
        gap_ids = {g["id"] for g in state["gaps"]}
        input_ids = {x["id"] for x in state["external_inputs"]}
        if len(input_ids) != len(state["external_inputs"]):
            raise ValueError("Duplicate external input")
        for key in ("results", "registrations"):
            if set(state[key]) - set(ids):
                raise ValueError("Unknown work package in " + key)
        if set(state["input_receipts"]) - input_ids:
            raise ValueError("Unknown external intake")
        for g in state["gaps"]:
            if not g["closure_tasks"] or set(g["closure_tasks"]) - set(ids):
                raise ValueError("Gap lacks executable closure gates: " + g["id"])
        visited, visiting = set(), set()

        def visit(task_id):
            if task_id in visiting:
                raise ValueError("Dependency cycle at " + task_id)
            if task_id in visited:
                return
            visiting.add(task_id)
            task = task_by_id(state, task_id)
            for dep in task["depends"]:
                if not dep["outcomes"] or set(dep["outcomes"]) - OUTCOMES:
                    raise ValueError("Invalid dependency outcomes: " + task_id)
                visit(dep["id"])
            visiting.remove(task_id)
            visited.add(task_id)

        for task in tasks:
            visit(task["id"])
            if task["kind"] not in {"control", "research", "engineering", "integration", "external"}:
                raise ValueError("Unknown work-package kind")
            if set(task["gaps"]) - gap_ids or set(task["requires_inputs"]) - input_ids:
                raise ValueError("Unknown gap or input: " + task["id"])
            if not task["steps"] or not task["outputs"] or not task["criteria"] or not task["failure_action"]:
                raise ValueError("Incomplete execution contract: " + task["id"])
            if len({c["id"] for c in task["criteria"]}) != len(task["criteria"]):
                raise ValueError("Duplicate criterion: " + task["id"])
            if task["id"] in state["registrations"]:
                validate_protocol(root, task, state["registrations"][task["id"]])
            if task["id"] in state["results"]:
                ref = state["results"][task["id"]]
                bound(root, ref)
                receipt = read(root, ref["path"])
                if ref["outcome"] != receipt["outcome"]:
                    raise ValueError("State/receipt outcome mismatch: " + task["id"])
                if ref.get("gap_dispositions", {}) != receipt.get("gap_dispositions", {}):
                    raise ValueError("State/receipt gap disposition mismatch: " + task["id"])
                if unmet(state, task):
                    raise ValueError("Completed task has unmet prerequisites: " + task["id"])
                validate_receipt(root, state, task, receipt)
        for name, ref in state["input_receipts"].items():
            validate_intake(root, state, name, ref)
        for attempt in state.get("attempts", []):
            old = attempt["contract"]
            bound(root, attempt["result"])
            bound(root, attempt["revision"])
            context = dict(state, registrations={old["id"]: attempt["registration"]} if attempt["registration"] else {})
            validate_receipt(root, context, old, read(root, attempt["result"]["path"]))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        issues.append(str(exc))
    return issues


def source_check(root, document_roots):
    """Each compiled document has its own label and reference namespace."""
    issues, citations, files = [], set(), set()
    for entry in document_roots:
        labels, refs, stack = [], set(), set()
        base = safe(root, entry).parent

        def scan(path):
            if path in stack:
                raise ValueError("Cyclic LaTeX input: " + str(path))
            stack.add(path)
            files.add(str(path.relative_to(root)))
            raw = re.sub(r"(?m)(?<!\\)%.*$", "", path.read_text())
            labels.extend(re.findall(r"\\label\{([^}]+)\}", raw))
            for value in re.findall(r"\\(?:ref|eqref|cref|Cref)\{([^}]+)\}", raw):
                refs.update(x.strip() for x in value.split(","))
            for value in re.findall(r"\\cite\w*\*?(?:\[[^\]]*\])*\{([^}]+)\}", raw):
                citations.update(x.strip() for x in value.split(","))
            for value in re.findall(r"\\(?:input|include)\{([^}]+)\}", raw):
                child = base / value
                if not child.suffix:
                    child = child.with_suffix(".tex")
                if not child.resolve().is_relative_to(root.resolve()):
                    raise ValueError("LaTeX input escapes repository")
                scan(child)
            stack.remove(path)

        try:
            scan(safe(root, entry))
            issues += [f"Duplicate label in {entry}: {k}" for k, n in collections.Counter(labels).items() if n > 1]
            issues += [f"Missing label in {entry}: {k}" for k in sorted(refs - set(labels))]
        except (OSError, ValueError) as exc:
            issues.append(str(exc))
    sources = read(root, "docs/literature/sources.json")
    keyed = {s["id"]: s for s in sources}
    if len(keyed) != len(sources):
        issues.append("Duplicate source identity")
    for key in sorted(citations):
        s = keyed.get(key)
        if not s:
            issues.append("Unregistered citation: " + key)
            continue
        for field in ("title", "authors", "year", "url", "local_path", "sha256", "inspected", "claims", "version_status"):
            if not s.get(field):
                issues.append(f"Missing source {field}: {key}")
        try:
            p = safe(root, s["local_path"])
            if sha(p) != s["sha256"]:
                issues.append("Source identity changed: " + key)
            if s.get("kind") == "paper":
                expected = f"{s['filename_title']} {s['first_author']}({s['year']}).pdf"
                with p.open("rb") as f:
                    is_pdf = f.read(5) == b"%PDF-"
                if p.parent != root / "docs/papers" or p.name != expected or not is_pdf:
                    issues.append("Paper naming/content violation: " + key)
        except (OSError, ValueError, KeyError) as exc:
            issues.append(str(exc))
    return {"issues": issues, "compiled_documents": len(document_roots),
            "source_files": len(files), "cited_works": len(citations), "registered_works": len(sources)}


def summary(state):
    rows = []
    for t in sorted(state["work_packages"], key=lambda x: x["priority"]):
        r = state["results"].get(t["id"])
        reasons = unmet(state, t)
        rows.append({"id": t["id"], "name": t["name"],
                     "status": "completed_" + r["outcome"] if r else ("blocked" if reasons else "ready"),
                     "blockers": reasons})
    qualified = [g["id"] for g in state["gaps"] if all(
        state["results"].get(i, {}).get("outcome") == "pass" and
        state["results"].get(i, {}).get("gap_dispositions", {}).get(g["id"]) == "qualified_in_declared_scope"
        for i in g["closure_tasks"])]
    return {"revision": state["revision"], "mission": state["mission"], "reader": state["reader"],
            "completed_work_packages": len(state["results"]), "total_work_packages": len(rows),
            "qualified_gaps_in_declared_scope": qualified,
            "bounded_product_accepted": len(qualified) == 10 and state["results"].get("F01", {}).get("outcome") == "pass",
            "unrestricted_product_claim": False, "work_packages": rows,
            "missing_external_inputs": [i["id"] for i in state["external_inputs"] if i["id"] not in state["input_receipts"]],
            "next": next((r["id"] for r in rows if r["status"] == "ready"), None)}


def render(root, state):
    s = summary(state)
    lines = ["# Mission control: causal banking master program", "", state["mission"], "",
        "The full product is unfinished. Historical author deliveries and current capability gates are separate.", "",
        f"{s['completed_work_packages']}/{s['total_work_packages']} work packages have recorded dispositions. "
        f"{len(s['qualified_gaps_in_declared_scope'])}/10 gaps have met all declared qualification gates. Next: **{s['next']}**.", "",
        "[Master program](program/master-program.md) · [Master PDF](program/master-program.pdf) · "
        "[Plan review](reviews/master-program-review-2026-10-11.md) · [Machine state](program/state.json)", "",
        "[Current research reader — 259 pages](causal_foundations_with_linked_audits_2026-10-11.pdf) · "
        "[Sponsor proposal — V10 baseline](sponsor_reconstruction.pdf)", "",
        "| Package | Disposition | Dependency or missing input |", "|---|---|---|"]
    lines += [f"| {r['id']} {r['name']} | {r['status']} | {'; '.join(r['blockers']) or '—'} |" for r in s["work_packages"]]
    lines += ["", "External input contracts: [required owners and evidence](program/master/external-inputs.md).",
        "Execution: `python3 tools/causal_program.py next`; consistency: `python3 tools/causal_program.py check`; "
        "historical replay: `python3 tools/causal_program.py baseline`.", "",
        "This is a durable executable work register, not a background research worker. A negative result completes "
        "an investigation and leaves its capability unqualified. No independent review, authentic bank validation, "
        "deployment, adopted interface or measured institutional ROI is claimed.", ""]
    md = "\n".join(lines)
    (root / "docs/mission-control.md").write_text(md)
    body = subprocess.run(["pandoc", "--from=gfm", "--to=html"], input=md, text=True,
                          capture_output=True, check=True, timeout=20).stdout
    page = "<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width'><title>Causal banking master</title><style>body{font:17px system-ui;max-width:1200px;margin:3rem auto;padding:0 1.5rem;color:#183047}table{border-collapse:collapse;width:100%}td,th{padding:.7rem;border-bottom:1px solid #d4dde5;text-align:left}a{color:#075f87}code{font-size:.85em}</style></head><body>" + body + "</body></html>"
    (root / "docs/mission-control.html").write_text(page)


def commit_state(root, before, state, event):
    control = root / "docs/program/master"
    control.mkdir(exist_ok=True, parents=True)
    with (control / "state.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if sha(root / STATE) != before:
            raise ValueError("State changed during operation; reload before continuing")
        snapshot = control / "state-history" / (before + ".json")
        if not snapshot.exists():
            write(snapshot, read(root, STATE))
        state["events"].append({"time": now(), **event})
        state["updated"] = now()
        issues = validate_state(root, state)
        if issues:
            raise ValueError("; ".join(issues))
        write(root / STATE, state)
    render(root, state)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("status", "check", "render", "baseline"):
        sub.add_parser(name)
    p = sub.add_parser("next"); p.add_argument("task", nargs="?")
    p = sub.add_parser("template"); p.add_argument("task")
    p = sub.add_parser("record"); p.add_argument("task"); p.add_argument("--receipt", required=True)
    p = sub.add_parser("register"); p.add_argument("task"); p.add_argument("--spec", required=True)
    p = sub.add_parser("intake"); p.add_argument("input"); p.add_argument("--receipt", required=True)
    p = sub.add_parser("reopen"); p.add_argument("task"); p.add_argument("--revision", required=True)
    args = parser.parse_args()
    if args.command == "baseline":
        raise SystemExit(subprocess.call([sys.executable, str(ROOT / "tools/program_baseline.py"), "verify"]))
    state = read(ROOT, STATE)
    before = sha(ROOT / STATE)
    issues = validate_state(ROOT, state)
    if issues:
        raise ValueError("Invalid master state: " + "; ".join(issues))
    if args.command == "status":
        print(json.dumps(summary(state), indent=2))
    elif args.command == "next":
        overview = summary(state)
        candidates = [r for r in overview["work_packages"] if r["status"] == "ready"]
        task_id = args.task or overview["next"]
        print(json.dumps({"next": task_by_id(state, task_id) if task_id else None,
            "blockers": unmet(state, task_by_id(state, task_id)) if task_id else [],
            "other_ready": [r["id"] for r in candidates if r["id"] != task_id],
            "completion_command": f"python3 tools/causal_program.py record {task_id} --receipt PATH" if task_id else None,
            "instruction": "Complete eligible packages in priority order; continue other ready branches when one is blocked. Never invent a positive research result or external input."}, indent=2))
    elif args.command == "check":
        source = source_check(ROOT, state["latex_roots"])
        issues.extend(source.pop("issues"))
        baseline = read(ROOT, "docs/program/master/baseline.json")
        for name, h in baseline["manifests"].items():
            if sha(ROOT / name) != h:
                issues.append("Changed predecessor manifest: " + name)
        for row in baseline["controls"].values():
            if sha(ROOT / row["archive_path"]) != row["sha256"]:
                issues.append("Changed preserved control: " + row["archive_path"])
        replay = read(ROOT, "docs/program/master/baseline-verification.json")
        inputs_bound(ROOT, replay)
        if replay.get("status") != "pass" or replay.get("manifests_verified") != 4:
            issues.append("Missing full predecessor verification")
        for row in state["deliveries"]:
            if sha(ROOT / row["path"]) != row["sha256"]:
                issues.append("Changed delivered PDF: " + row["path"])
        result = {"status": "pass" if not issues else "fail", "issues": issues,
            "work_packages": len(state["work_packages"]), "gaps_accounted_for": 10, **source,
            "scope": "Current dependency/evidence integrity, per-document label scopes, primary-source identities and delivered PDF hashes. Full historical replay uses baseline. No automated scholarly or external approval."}
        print(json.dumps(result, indent=2))
        raise SystemExit(bool(issues))
    elif args.command == "render":
        render(ROOT, state)
        print("Current mission control rendered")
    elif args.command == "template":
        t = task_by_id(state, args.task)
        print(json.dumps({"task_id": t["id"], "task_contract_sha256": digest_object(t),
            "outcome": None, "reviewer": {"name": "", "kind": "author"}, "scope": "", "limitations": [],
            "gap_dispositions": {} if t["kind"] == "control" else {g: "unresolved" for g in t["gaps"]},
            "criteria": [{"id": c["id"], "verdict": None, "finding": "", "evidence": []} for c in t["criteria"]]}, indent=2))
    elif args.command in {"record", "register"}:
        t = task_by_id(state, args.task)
        if t["id"] in state["results"] or unmet(state, t):
            raise ValueError("Task already resolved or has unmet dependencies: " + "; ".join(unmet(state, t)))
        name = args.receipt if args.command == "record" else args.spec
        ref = {"path": name, "sha256": sha(safe(ROOT, name)), "anchor": "Complete reviewed receipt/protocol"}
        if args.command == "record":
            receipt = read(ROOT, name)
            validate_receipt(ROOT, state, t, receipt)
            ref["outcome"] = receipt["outcome"]
            ref["gap_dispositions"] = receipt.get("gap_dispositions", {})
            state["results"][t["id"]] = ref
        else:
            if t["kind"] != "research" or t["id"] in state["registrations"]:
                raise ValueError("Only an unresolved, unregistered research task can register a protocol")
            ref["registered_at"] = now()
            validate_protocol(ROOT, t, ref)
            state["registrations"][t["id"]] = ref
        commit_state(ROOT, before, state, {"action": args.command, "task_id": t["id"], "receipt": ref})
        print(json.dumps({"status": "recorded", "task_id": t["id"], "next": summary(state)["next"]}))
    elif args.command == "intake":
        if args.input not in {r["id"] for r in state["external_inputs"]} or args.input in state["input_receipts"]:
            raise ValueError("Unknown/already received external input")
        ref = {"path": args.receipt, "sha256": sha(safe(ROOT, args.receipt)), "anchor": "Signed owner/input contract"}
        validate_intake(ROOT, state, args.input, ref)
        state["input_receipts"][args.input] = ref
        commit_state(ROOT, before, state, {"action": "intake", "input_id": args.input, "receipt": ref})
        print(json.dumps({"status": "external_input_recorded", "input_id": args.input}))
    elif args.command == "reopen":
        ref = {"path": args.revision, "sha256": sha(safe(ROOT, args.revision)), "anchor": "Reviewed successor contract and retained failed attempt"}
        reopen_task(ROOT, state, args.task, ref)
        commit_state(ROOT, before, state, {"action": "reopen", "task_id": args.task, "receipt": ref})
        print(json.dumps({"status": "reopened", "task_id": args.task, "next": summary(state)["next"]}))


def cli():
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError, subprocess.SubprocessError) as exc:
        raise SystemExit(str(exc))


if __name__ == "__main__":
    cli()

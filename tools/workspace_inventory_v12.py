#!/usr/bin/env python3
"""Read selected workspace metadata/source contracts; write only under causal.

Does not import sibling modules, run entrypoints, inspect credentials or install
anything. Local source originals remain in their own repositories; paths, hashes,
dates and inspected anchors establish the bounded observation, not adoption.
"""
import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import tomllib
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
OUT = ROOT / "docs/program/repair-v12/work/IN01"
DATE = datetime.now(ZoneInfo("Asia/Shanghai")).date().isoformat()

SELECTED = {
    "BayesFilter": ["bayesfilter/ssm/contracts.py", "bayesfilter/results.py"],
    "DynareMCP": ["src/dynaremcp/cli.py"],
    "FinMarketing": ["src/finmarketing/delivery/toolkit_cli.py", "src/finmarketing/toolkit/contracts.py"],
    "MathDevMCP": ["src/mathdevmcp/mcp_entrypoint.py", "LICENSE"],
    "SMEwallet": ["src/sme_wallet/math_contract.py"],
    "cardnpv": ["poc/card_end_to_end/target_contract.py", "LICENSE"],
    "MacroFinance": ["bayesfilter_macrofinance_migration_adapter.py"],
    "MOONeural": ["src/mooneural/training/generic_training_contracts.py", "NOTICE"],
    "hponas": ["hponas/__init__.py"],
    "humanvoice": ["src/humanvoice/cli.py"],
    "research-assistant": ["src/research_assistant/cli.py", "src/research_assistant/adapters/mcp_server.py"],
    "dataml": ["src/clearwater/cli/governance.py", "src/clearwater/research/cli.py"],
    "causal": ["src/causalbank/__init__.py"],
}
INSTRUCTION_ANCHORS = {
    "BayesFilter": "Headings and read-only/scope constraints; lines 1–119: canonical authority and proportionate research boundaries",
    "DynareMCP": "Headings and read-only/scope constraints; lines 1–102: prototype/mission limits and routine inspection",
    "FinMarketing": "Lines 1–88: scope, policies, source/implementation distinction and image discipline",
    "MacroFinance": "Lines 1–133: read-only authorization, written specification and BayesFilter runtime authority",
    "MacroFinance-ccma-g-v7-neutra-r9": "Lines 1–38: project identity and research rigor; no runtime launched",
    "MacroFinance-dz5-neutra": "Lines 1–38: project identity and research rigor; no runtime launched",
    "MathDevMCP": "Complete 76-line instruction file",
    "SMEwallet": "Complete 121-line instruction file; no SME experiment or manuscript edit",
    "claudecodex": "Complete 35-line instruction file; no policy installation or worker launch",
    "dataml": "Complete 97-line instruction file; separate program ownership, no sibling execution",
    "causal": "Complete 41-line instruction file and explicit read-only sibling scope",
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(directory, *args):
    p = subprocess.run(["git", "-C", str(directory), *args], capture_output=True,
                       text=True, timeout=10)
    return p.stdout.strip() if p.returncode == 0 else None


def observe(path, anchors, claims):
    data = path.read_bytes()
    return {"source_identity": str(path), "local_copy": str(path),
            "sha256": hashlib.sha256(data).hexdigest(),
            "observed_at": datetime.now(timezone.utc).isoformat(),
            "file_mtime_ns": path.stat().st_mtime_ns, "inspected_anchors": anchors,
            "supported_claims": claims,
            "copy_policy": "Read local original in place; no sibling source copied or relicensed."}


def source_structure(path):
    tree = ast.parse(path.read_text())
    symbols = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            fields = [n.target.id for n in node.body
                      if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name)]
            symbols.append({"name": node.name, "line": node.lineno,
                            "fields": fields, "has_docstring": bool(ast.get_docstring(node))})
    return {"has_module_docstring": bool(ast.get_docstring(tree)), "symbols": symbols,
            "scope": "Static declarations/docstrings only; no call-chain or numerical qualification."}


def main():
    annotations = json.loads((OUT / "annotations.json").read_text())
    directories = sorted(p for p in WORKSPACE.iterdir() if p.is_dir())
    if {p.name for p in directories} != set(annotations):
        raise ValueError("Workspace directory set changed; review new or missing directories")
    rows, sources, missing = [], [], []
    for directory in directories:
        name = directory.name
        row = {"name": name, "path": str(directory), **annotations[name],
               "observed_at": datetime.now(timezone.utc).isoformat(),
               "runtime_qualification": False, "actual_consumer_acceptance": False,
               "allowed_writes": "causal repository only", "source_ids": []}
        if name == ".local":
            row["repository_revision"] = None
            row["observation_scope"] = "Top-level directory identity only; ambient support contents excluded"
            rows.append(row)
            continue
        row["repository_revision"] = git(directory, "rev-parse", "HEAD")
        row["git_common_dir"] = git(directory, "rev-parse", "--path-format=absolute", "--git-common-dir")
        row["revision_limit"] = "Commit plus hashes of inspected working files; no assumption that the entire working tree is clean."
        row["declared_console_scripts"] = {}
        selected = ["AGENTS.md", "README.md", "pyproject.toml"] + SELECTED.get(name, [])
        for relative in selected:
            path = directory / relative
            if not path.exists():
                missing.append({"repository": name, "path": relative, "meaning": "Absent selected path; not an exhaustive absence claim"})
                continue
            if relative == "AGENTS.md":
                anchors = [INSTRUCTION_ANCHORS[name]]
                claims = ["Applicable constraints for bounded read-only inventory; unrelated campaigns not resumed"]
            elif relative == "README.md":
                anchors = ["Opening scope and selected CLI/MCP/interface/license passages inspected"]
                claims = ["Documented purpose and interface/acceptance limits; documentation is not execution"]
            elif relative == "pyproject.toml":
                data = tomllib.loads(path.read_text()).get("project", {})
                row["package_metadata"] = {k: data.get(k) for k in ("name", "version", "description", "license", "requires-python")}
                row["declared_console_scripts"] = data.get("scripts", {})
                anchors = ["project name/version/description/license and project.scripts"]
                claims = ["Declared package metadata and console targets; no installation or availability claim"]
            elif path.suffix == ".py":
                structure = source_structure(path)
                row.setdefault("source_interfaces", []).append({"path": relative, **structure})
                anchors = ["Module docstring and static top-level class/function declarations"]
                claims = ["Selected source declarations exist with the recorded symbols and fields; runtime untested"]
            else:
                anchors = ["Complete local license/notice text"]
                claims = ["Declared copying/distribution limits; no broader rights inferred"]
            evidence = observe(path, anchors, claims)
            evidence["repository_revision"] = row["repository_revision"]
            evidence["version_date"] = row.get("package_metadata", {}).get("version") or f"Working source observed {DATE}; git/content identities supplied"
            row["source_ids"].append(evidence["source_identity"])
            sources.append(evidence)
        if name == "dsge_hmc":
            row["nested_checkouts"] = [{"path": str(directory / child),
                "commit": git(directory / child, "rev-parse", "HEAD"),
                "status": "Git metadata only; canonical consumer interface deferred"}
                for child in ("main-baseline", "original-main", "sgu-neural-training-plan")]
        rows.append(row)
    changed = [r["source_identity"] for r in sources if digest(Path(r["local_copy"])) != r["sha256"]]
    inventory = {"date": DATE, "task_id": "IN01", "status": "read_only_inventory_complete",
        "cutoff_policy": f"Current workspace observations are an explicit {DATE} environment delta; not backdated literature evidence.",
        "directories": rows, "sources": sources, "selected_paths_not_found": missing,
        "limits": ["Selected interface inventory, not exhaustive API/call-chain verification.",
                   "No sibling code executed; all runtime qualification and maintainer acceptance remain absent.",
                   "External-local originals remain mutable; refresh identity and review license before later adoption or publication."]}
    (OUT / "workspace-inventory.json").write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n")
    audit = {"task_id": "IN01", "status": "pass" if not changed else "unstable_sources",
        "scope": "This inventory's operations and inspected sources, not a claim that no other process changed any sibling file.",
        "operations": ["Read root instructions/README/metadata and selected source declarations", "Read git HEAD/common-directory metadata", "Parse source AST without importing", "Write only this causal work directory"],
        "sibling_code_executions": 0, "sibling_writes": 0, "source_copies": 0,
        "source_count": len(sources), "changed_during_collection": changed,
        "observed_failure": {"operation": "An initial broad file-discovery query", "path": "/home/ubuntu/workspace/FinMarketing/packaging/evidence/agent-cp3-freeze-20260921-1", "result": "Permission denied in archived evidence", "repair": "Narrowed inspection to current src paths; archived packaging evidence is not needed for this interface inventory."},
        "inherited_snapshots": {"path": "docs/literature/local-repositories/index.json", "sha256": digest(ROOT / "docs/literature/local-repositories/index.json"), "status": "historical documentation, not current executed acceptance"},
        "input_sha256": {"tools/workspace_inventory_v12.py": digest(Path(__file__)), "docs/program/repair-v12/work/IN01/annotations.json": digest(OUT / "annotations.json")}}
    (OUT / "read-only-audit.json").write_text(json.dumps(audit, indent=2) + "\n")
    print(json.dumps({"directories": len(rows), "source_records": len(sources), "changed_sources": changed,
                      "runtime_runs": 0, "sibling_writes": 0}))


if __name__ == "__main__":
    main()

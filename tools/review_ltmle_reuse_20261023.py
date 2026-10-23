#!/usr/bin/env python3
"""Bind an ltmle source-level reference decision to exact local evidence."""
import hashlib
import json
from pathlib import Path

import ltmle_policy_oracle_20261023 as oracle
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run = controller.base
ROOT = run.core.ROOT
BASE = ROOT / "docs/program/execution/2026-10-23/ltmle-reuse-v1"
RAW = ROOT / "docs/literature/raw"
OP = "SW.DECISION.inherited_ltmle"
PIN = "338c029dae9692ef20714125773da7037688993b"
CUTOFF = "2026-10-07T15:59:59Z"

LIMITS = [
    "Selected historical source inspection only. The repository metadata records a later 2026 push; this 2023 source commit is not asserted to be the latest repository state or a currently supported release.",
    "The public collector's supplemental delegate and C++ identity request failures are preserved. The reference finding relies on the complete selected ltmle.R source, the exact package DESCRIPTION and existing reader audit; no conclusion is drawn from the failed requests.",
    "No downloaded R code, package, upstream tests, dependency resolver, external engine, live model or bank data was executed.",
    "GPL-2 and package Imports are declared at the selected revision. Full transitive license compatibility, distribution structure and operational rights remain unreviewed.",
    "Sequential exchangeability, consistency, censoring independence, support, nuisance-rate conditions, cluster sampling and finite-sample calibration are scientific conditions, not established by an API or synthetic law.",
    "The exact policy oracle is an authored finite-law g-formula truth calculation. Its expected risks and monetary values are not ltmle outputs, package verification, bank observations or measured benefits.",
    "The reference decision does not close the longitudinal software census, qualify another release, authorize integration, or establish a product capability.",
]


def read(path):
    return json.loads(path.read_text())


def git_blob(path):
    body = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(body)).encode() + b"\0" + body).hexdigest(), len(body)


def reconstructed_tree_oid(tree, parent):
    children = [x for x in tree["tree"] if (x["path"].rsplit("/", 1)[0] if "/" in x["path"] else "") == parent]
    children.sort(key=lambda x: (x["path"].rsplit("/", 1)[-1] + ("/" if x["type"] == "tree" else "")).encode())
    body = b"".join(
        x["mode"].lstrip("0").encode() + b" "
        + (x["path"].rsplit("/", 1)[-1] + ("/" if x["type"] == "tree" else "")).encode()
        + b"\0" + bytes.fromhex(x["sha"])
        for x in children
    )
    return hashlib.sha1(b"tree " + str(len(body)).encode() + b"\0" + body).hexdigest(), len(children)


def main():
    state = run.core.read(ROOT, run.core.STATE)
    assert state["execution_runtime"]["active"]["operation"] == OP
    commit_path = RAW / "r3g_commit_ltmle.json"
    repo_path = RAW / "repo_ltmle_verified.json"
    tree_path = RAW / "exec23_ltmle_tree.json"
    desc_path = RAW / "exec23_ltmle_description.txt"
    code_path = RAW / "r3g_api_ltmle.txt"
    commit_receipt = RAW / "r3g_commit_ltmle.receipt.json"
    repo_receipt = RAW / "repo_ltmle_verified.receipt.json"
    tree_receipt = RAW / "exec23_ltmle_tree.receipt.json"
    desc_receipt = RAW / "exec23_ltmle_description.receipt.json"
    code_receipt = RAW / "r3g_api_ltmle.receipt.json"

    commit = read(commit_path)[0]
    tree = read(tree_path)
    repo = read(repo_path)
    description = desc_path.read_text()
    assert commit["sha"] == PIN
    assert commit["commit"]["committer"]["date"] < CUTOFF
    assert commit["commit"]["verification"]["verified"] is False
    assert tree["truncated"] is False
    assert tree["sha"] == commit["commit"]["tree"]["sha"]
    assert repo["full_name"] == "joshuaschwab/ltmle"
    assert repo["default_branch"] == "master"

    entries = {entry["path"]: entry for entry in tree["tree"]}
    root_oid, root_children = reconstructed_tree_oid(tree, "")
    r_oid, r_children = reconstructed_tree_oid(tree, "R")
    assert root_oid == commit["commit"]["tree"]["sha"]
    assert r_oid == entries["R"]["sha"]

    code_blob, code_bytes = git_blob(code_path)
    desc_blob, desc_bytes = git_blob(desc_path)
    assert (code_blob, code_bytes) == (entries["R/ltmle.R"]["sha"], entries["R/ltmle.R"]["size"])
    assert (desc_blob, desc_bytes) == (entries["DESCRIPTION"]["sha"], entries["DESCRIPTION"]["size"])
    assert "Version: 1.3-0" in description
    assert "Date: 2023-4-13" in description
    assert "License: GPL-2" in description
    assert "R(>= 3.1.0)" in description
    assert "Matrix," in description and "matrixStats" in description
    assert "SuperLearner," in description
    assert repo["pushed_at"] == "2026-06-03T16:34:57Z"

    identity = {
        "status": "pass_for_selected_historical_revision",
        "repository": "joshuaschwab/ltmle",
        "selected_commit": PIN,
        "commit_date_utc": commit["commit"]["committer"]["date"],
        "commit_signature_verified": False,
        "commit_message": commit["commit"]["message"],
        "tree_listing_complete": True,
        "tree_proofs": [
            {"tree": "/", "reconstructed_git_tree": root_oid, "expected": commit["commit"]["tree"]["sha"], "children": root_children},
            {"tree": "R/", "reconstructed_git_tree": r_oid, "expected": entries["R"]["sha"], "children": r_children},
        ],
        "package_declaration": {
            "version": "1.3-0",
            "date": "2023-4-13",
            "license": "GPL-2",
            "depends": "R >= 3.1.0",
            "imports": ["Matrix", "matrixStats"],
            "suggests": ["SuperLearner", "testthat", "tmle", "knitr", "rmarkdown", "nnls", "arm"],
            "evidence": ref(desc_path, "Pinned DESCRIPTION bytes match the selected Git tree blob"),
        },
        "repository_maintenance_snapshot": {
            "default_branch": repo["default_branch"],
            "last_push_recorded": repo["pushed_at"],
            "interpretation": "Repository metadata records a later push than the selected source commit; it does not bind the selected source to the later tree or identify the latest published package.",
            "evidence": ref(repo_path, "Saved repository metadata snapshot"),
        },
        "files": [
            {"path": "R/ltmle.R", "git_blob": code_blob, "bytes": code_bytes,
             "sha256": run.core.sha(code_path), "local_copy": ref(code_path, "Authentic source bytes matching the selected commit tree")},
            {"path": "DESCRIPTION", "git_blob": desc_blob, "bytes": desc_bytes,
             "sha256": run.core.sha(desc_path), "local_copy": ref(desc_path, "Authentic package declaration matching the selected commit tree")},
        ],
        "evidence": [ref(commit_path, "Selected commit object and commit/tree identity"), ref(tree_path, "Complete recursive tree listing"),
                     ref(commit_receipt, "Commit-object retrieval receipt"), ref(repo_receipt, "Repository metadata retrieval receipt"),
                     ref(tree_receipt, "Pinned tree retrieval receipt"), ref(desc_receipt, "Pinned DESCRIPTION retrieval receipt"),
                     ref(code_receipt, "Pinned technical-source retrieval receipt")],
    }
    write(BASE / "identity-review.json", identity)

    anchor_specs = [
        (1, 106, "Function documentation defines wide ordered histories, binary interventions, censoring/event handling, outcome scaling and rule-valued regimes."),
        (162, 254, "The existing reader audit anchors cumulative propensity bounds, weights, variance restrictions and subject identifiers."),
        (331, 404, "The default uses glm, gbounds (0.01,1), TMLE variance and two-regime contrasts; the simple wrapper handles one or two regimes."),
        (406, 462, "Input validation constructs the calculation; when a non-IC variance is unavailable for a supplied option such as id, the effective method is set to IC."),
        (567, 641, "Main calculations produce influence curves and optionally a separate TMLE variance estimate; warning logic identifies positivity and rare-event concerns."),
        (1025, 1066, "Household influence values sum record contributions by id and rescale by household count over record count."),
        (1365, 1417, "Effect summaries apply gradients to the shared influence-curve covariance and use a second variance matrix only when it exists."),
        (2174, 2326, "Input checks require increasing node order, binary treatment and coherent survival/censoring states; id length is tied to records."),
        (2327, 2358, "Outcome-range behavior may truncate values and then scale them; the transformation changes the analyzed target unless bounds are substantively fixed."),
    ]
    source_lines = code_path.read_text().splitlines()
    anchors = []
    for lo, hi, finding in anchor_specs:
        assert hi <= len(source_lines)
        excerpt = "\n".join(source_lines[lo - 1:hi])
        anchors.append({"source": ref(code_path, "Authenticated pinned source"), "lines": [lo, hi],
                        "finding": finding, "excerpt": excerpt,
                        "excerpt_sha256": hashlib.sha256(excerpt.encode()).hexdigest()})
    write(BASE / "inspected-extracts.json", {"anchors": anchors})

    exact = oracle.calculate()
    expected_path = BASE / "policy-oracle-results.json"
    assert exact == read(expected_path)
    assert [exact["results"][n]["default_probability"] for n in ("status_quo", "targeted_dynamic", "broad_contact")] == ["1/6", "3/25", "13/300"]
    assert exact["results"]["targeted_dynamic"]["net_value_vs_status_quo_usd"] == "130/3"
    assert exact["results"]["broad_contact"]["net_value_vs_status_quo_usd"] == "340/3"

    comparison = BASE / "comparison.md"
    assert comparison.exists()
    chapter = ROOT / "docs/program/comprehensive-v14/work/TEXT.DRAFT.S5/chapter.tex"
    chapter_text = chapter.read_text()
    integrated_literal = "The pinned source adds an operational uncertainty boundary."
    assert integrated_literal in chapter_text
    assert "The default probabilities for status quo, targeted and broad contact are" in chapter_text

    selected_code = {
        "integrated_citation_key": "sw_ltmle",
        "kind": "software_primary_source",
        "title": "Pinned ltmle longitudinal policy and uncertainty source inspection",
        "author": "Joshua Schwab and ltmle contributors",
        "year": 2023,
        "source_identity": f"https://github.com/joshuaschwab/ltmle/tree/{PIN}",
        "version_date": "Version 1.3-0, DESCRIPTION date 2023-4-13; selected commit 2023-04-17; repository metadata separately records a 2026-06-03 push",
        "local_copy": ref(code_path, "Pinned source file verified against commit tree blob"),
        "package_declaration": ref(desc_path, "Version/license/dependency source verified against the same commit tree"),
        "identity_evidence": [ref(commit_path, "Selected commit object"), ref(tree_path, "Complete selected tree"), ref(repo_path, "Later repository maintenance snapshot")],
        "retrieval": [ref(code_receipt, "Authentic source retrieval record"), ref(desc_receipt, "Authentic DESCRIPTION retrieval record")],
        "inspected_anchors": [{"anchor": f"R/ltmle.R lines {x['lines'][0]}-{x['lines'][1]}", "finding": x["finding"],
                               "evidence": ref(BASE / "inspected-extracts.json", "Verbatim source anchors with excerpt hashes")} for x in anchors],
        "supported_claims": [x["finding"] for x in anchors],
        "limitations": LIMITS,
    }
    project_derivation = {
        "integrated_citation_key": None,
        "kind": "project_derivation",
        "title": "Exact two-period dynamic servicing-policy truth oracle",
        "author": "Causal banking proposal authors",
        "year": 2026,
        "source_identity": "project:ltmle_policy_oracle_20261023.py",
        "version_date": "Authored 2026-10-23; exact Fraction arithmetic",
        "local_copy": ref(ROOT / "tools/ltmle_policy_oracle_20261023.py", "Authored exact finite-law calculation"),
        "results": ref(expected_path, "Exact path enumeration and monetary derivation"),
        "supported_claims": ["The three policy default risks and net values follow from the stipulated finite law exactly."],
        "limitations": LIMITS,
    }
    audit = {"cutoff": "2026-10-07", "sources": [selected_code, project_derivation],
             "coverage_complete": False, "native_execution": False}
    write(BASE / "source-audit.json", audit)

    proposed_contract = {
        "status": "proposed_not_implemented",
        "accepted_profile": ["Explicit account and cluster unit; chronological node map; binary treatment nodes; named outcome/event/censoring states; fixed time zero and horizon; one or two dynamic regimes."],
        "outputs": ["Regime-specific mean and a separately named contrast; influence contribution and covariance unit; cumulative g-probability bounds; effective variance method; cluster count and size distribution; transformed outcome range; warnings and failures."],
        "refuse_or_require_explicit_approval": ["Unknown column chronology; continuous treatment; incoherent absorbing event values; unsupported history or positivity; unspecified outcome truncation; requested TMLE variance with non-null id unless the caller explicitly accepts the source's effective IC path; more than two regimes sent through the simple ltmle wrapper."],
        "no_capability_granted": True,
    }
    limitations = LIMITS + [
        "A future R worker would need a pinned cutoff release/tree, locked dependencies, native behavior checks, exact target comparisons, cluster/rare-event/positivity adverse scenarios and failure-denominator reporting before selection.",
        "A port would additionally need parity for history order, dynamic rules, censoring recoding, scaling, cumulative bounds, learner calls, cluster aggregation and covariance; no measured requirement currently justifies that cost.",
    ]
    evidence = [ref(BASE / "identity-review.json", "Commit, package and maintenance identity review"),
                ref(BASE / "inspected-extracts.json", "Source-bound technical findings"),
                ref(BASE / "source-audit.json", "Traceable source and project derivation records"),
                ref(comparison, "Substantive comparison and bounded disposition"),
                ref(expected_path, "Exact finite-law oracle results"),
                ref(ROOT / "tools/ltmle_policy_oracle_20261023.py", "Exact authored calculator"),
                ref(chapter, "Integrated longitudinal chapter with target and uncertainty discussion"),
                ref(BASE / "acquisition-attempt-1/collector.jsonl", "Preserved failed supplemental public-source attempt"),
                ref(BASE / "plan.md", "Reviewed operation scope")]
    decision = {
        "operation": OP, "status": "pass", "decision": "reference", "capabilities": [], "integration_allowed": False,
        "scope": "Retain the selected historical ltmle source as a bounded longitudinal policy-semantics reference; select no executable worker, adapter, port or qualified capability.",
        "source": {"repository": "joshuaschwab/ltmle", "selected_commit": PIN, "selected_package_version": "1.3-0", "is_latest_release_asserted": False},
        "proposed_contract": proposed_contract,
        "alternatives": [
            {"choice": "historical_ltmle_source_reference", "disposition": "selected", "reason": "The exact code and package declaration are tree-bound and provide a useful R comparator for binary longitudinal regimes; the later repository push is not bound to this historical file revision."},
            {"choice": "direct_R_worker", "disposition": "future_candidate_not_selected", "reason": "No current source tree/release, dependency lock, native execution or target-specific uncertainty qualification is authenticated."},
            {"choice": "direct_adoption_or_cross_language_port", "disposition": "not_selected", "reason": "The proposal has no accepted platform requirement that offsets history, censoring, range, cluster, covariance and licensing parity costs."},
            {"choice": "lmtp_and_gfoRmula", "disposition": "distinct_comparators", "reason": "They are separate estimators and intervention/data contracts; neither is an alias or inherited approval for ltmle."},
            {"choice": "blanket_rejection", "disposition": "not_selected", "reason": "The source remains useful for interface comparison and bounded policy-semantics discussion, although its selected historical snapshot is not implementation evidence."},
        ],
        "costs": "No runtime, price, ROI or engineering estimate is measured. A future worker must budget R and dependency packaging, GPL-2 distribution review, wide-history conversion, learner fitting, fold/randomness control, positivity diagnostics, cluster-level uncertainty, failure recovery and maintenance.",
        "owner_obligations": [
            {"owner": "Source-review author", "item": "Current identity", "next_action": "When public-source connectivity is available, authenticate the cutoff-appropriate master commit and CRAN artifact, compare them with the selected historical commit, and preserve the current acquisition failure."},
            {"owner": "Method reviewer", "item": "Scientific contract", "next_action": "Specify target population, time zero, dynamic policy, sequential exchangeability, censoring, positivity, outcome range and cluster sampling before any native trial."},
            {"owner": "Prototype author", "item": "Behavior qualification", "next_action": "Run locked R package fixtures against exact policy targets and adverse rare-event, weak-support, unequal-cluster and missing-history scenarios; report effective variance choice and all unavailable fits."},
            {"owner": "Legal and architecture reviewers", "item": "Distribution", "next_action": "Review GPL-2 package terms and the complete resolved dependency/license chain against the proposed distribution model."},
            {"owner": "Independent reviewer and bank owners", "item": "Later acceptance", "next_action": "Supply independent assessment, authentic bank records and truth, target platform and consumer contracts only after the proposal and public evidence justify those costs."},
        ],
        "evidence": evidence, "limitations": limitations,
        "revisit_trigger": "A prototype requires longitudinal binary-regime comparison, current source and dependency identities are authenticated, or a new target/clock/censoring/cluster law is introduced.",
    }
    output = ROOT / "docs/program/comprehensive-v14/work" / OP / "decision.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    write(output, decision)
    review = {
        "status": "pass_for_bounded_reference_decision",
        "reviewer": {"name": "Codex author/coordinator", "kind": "author"},
        "operation": OP, "evidence": evidence + [ref(output, "Required reuse decision")],
        "findings": [
            "The selected code and DESCRIPTION are members of the same complete pre-cutoff Git tree; repository metadata records a later push, so the historical source is not represented as the latest release.",
            "The ltmle wrapper has a wide chronological binary-treatment profile; the one/two-regime estimand and the larger-policy MSM route must not be conflated.",
            "A non-null id changes the influence contribution aggregation and source code resets an unavailable requested variance method to IC; the exact banking oracle is math, not package output.",
            "The reference choice names alternatives, cost components, accountable roles, acceptance limitations and a concrete revisit trigger; no adapter capability is granted.",
        ],
        "limitations": limitations, "integration_allowed": False, "native_execution": False,
        "visual_acceptance": False, "proposal_accepted": False,
    }
    verify_bindings(review)
    write(BASE / "review.json", review)

    graph, merged, _ = run.combined(ROOT, state)
    node = run.ledger.operation(graph, OP)
    receipt = run.ledger.receipt_template(node)
    findings = [
        "Source identity, version/date, declared GPL-2 terms, dependencies and later maintenance observation are traceable; aliases and separate longitudinal engines remain distinct.",
        "Policy target, effective uncertainty path, assumptions, alternatives, costs, owner actions and revisit conditions are explicit and tied to an exact authored example.",
        "A source-level reference decision meets this proposal operation while granting no integration capability, native qualification or product acceptance.",
    ]
    receipt.update(outcome="pass", execution="performed", scope=decision["scope"],
                   reviewer=review["reviewer"], limitations=limitations, capabilities=[],
                   original_gap_qualification=False, nonexecution_reason="No downloaded R engine or native code was executed; source review and authored exact truth calculation only.",
                   revisit_trigger=decision["revisit_trigger"], outputs=[ref(output, "Required reuse decision")],
                   criteria=[{"index": i, "verdict": "pass", "finding": finding,
                              "evidence": evidence + [ref(BASE / "review.json", "Author review")]}
                             for i, finding in enumerate(findings)])
    run.validate_receipt(ROOT, merged, node, receipt, len(state["execution_program"]["turns"]))
    write(BASE / "operation-receipt.json", receipt)
    print(json.dumps({"operation": OP, "revision": PIN, "anchors": len(anchors),
                      "decision": "reference", "integration_allowed": False,
                      "exact_policy_oracle": "pass", "criteria": len(findings)}))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Merge inspected pinned software evidence without rebuilding seed defaults.

No network or downloaded-code execution. Source bytes, receipts, commit dates
and Git tree blob identities are checked before any register is changed.
"""
import argparse
import copy
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path

from build_sw01_register_v12 import query_records

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/program/repair-v12"
OUT = BASE / "work/SW01"
RAW = ROOT / "docs/literature/raw"
REVISION = "pinned-r-stata-tetrad-2026-10-12"
CUTOFF = datetime.fromisoformat("2026-10-07T15:59:59+00:00")
REGISTERS = ["catalog", "source-audit", "search-ledger", "coverage-matrix", "omissions"]

# Claims are scoped to the passages inspected during this continuation. This is
# deliberately an authored review, not an extraction that labels metadata proof.
SPECS = [
    ("ivreg", "seed:050", ["iv_rd_design"], {1: [(112, 148)]},
     ["The formula interface requires exogenous regressors among the instruments; method selects ordinary 2SLS or robust M/MM regression."],
     "Evaluate R process integration for an explicitly declared IV model; robust regression is not a weak-instrument coverage guarantee.",
     ["Check first-stage rank, endogenous/exogenous column roles and coefficient units.", "Match heteroskedastic/cluster covariance separately; compare weak-IV sets with an actual inversion procedure."],
     "Only ivreg is inspected. The seed's AER family component remains a separate unaudited lead."),
    ("ivmodel", "seed:051", ["iv_rd_design", "identification_counterfactual"],
     {1: [(1, 23)], 2: [(1, 41)]},
     ["AR.test and CLR documentation exposes confidence sets as matrices whose rows represent interval components."],
     "Evaluate R integration preserving every interval component and infinite endpoint; do not port a scalar coefficient alone.",
     ["Test weak/zero first stage, disconnected and unbounded inversions and empty sets.", "Match sampling and covariance assumptions to the chosen AR/CLR method before comparison."],
     "A documented confidence-set API does not establish its coverage for dependent bank panels."),
    ("rdrobust", "seed:052", ["iv_rd_design"],
     {1: [(27, 48), (82, 106), (128, 145)]},
     ["The selected manual documents sharp/fuzzy/kink local-polynomial options, bias correction, variance and bandwidth choices."],
     "Evaluate the pinned R implementation with a design-specific contract; retain bandwidth, polynomial and variance choices in each result.",
     ["Match sharp versus fuzzy target and cutoff units; inspect treatment first stage.", "Test mass points, clustering, bandwidth sensitivity and separate bias-corrected point/interval outputs."],
     "Version 4.0.0 is a retrieved pre-cutoff snapshot, not a claim of the latest cutoff release; 4.1.1 availability remains unresolved."),
    ("rddensity", "seed:053", ["iv_rd_design"], {1: [(138, 151)]},
     ["The documented routine provides local-polynomial density/manipulation testing around the cutoff."],
     "Use as an optional RD diagnostic after qualification, preserving the statistic and bandwidth rather than a validity badge.",
     ["Test continuous and discrete running variables, mass-point options and low support.", "Retain separate evidence for assignment rules and potential-outcome continuity."],
     "Failure to reject a density discontinuity is not proof of the causal design."),
    ("rdlocrand", "seed:054", ["iv_rd_design"],
     {1: [(68, 90), (138, 154)]},
     ["The routine assumes a local-randomization window; positive polynomial order invokes asymptotic inference, and confidence-set inversion uses a specified grid."],
     "Evaluate R integration for approved local-randomization designs and retain the inversion grid and window-selection provenance.",
     ["Test randomization law and assignment counts inside the declared window.", "Detect grid-boundary confidence sets; never treat a truncated search as a finite bound."],
     "A fitted window does not establish actual local randomization; finite-grid bounds need explicit truncation flags."),
    ("medflex", "seed:056", ["mediation_sensitivity"], {1: [(54, 86)]},
     ["Natural-effect models use expanded data; full bootstrap refits the working models, and the original mediator is excluded from the final natural-effect formula."],
     "Evaluate R integration retaining expansion identity and the entire bootstrap fitting path.",
     ["Check mediator copies and row-to-original-subject linkage.", "Match mediator/outcome models, effect scale and bootstrap resampling units; do not reuse a frozen first-stage fit in a full bootstrap."],
     "Natural-effect interpretation requires separate mediation assumptions; an expanded dataset does not supply them."),
    ("sensemakr", "seed:057", ["mediation_sensitivity"], {1: [(95, 145)]},
     ["Omitted-variable sensitivity is expressed through partial R-squared quantities and observed-covariate benchmarks."],
     "Evaluate as a sensitivity report for the supported regression target, keeping benchmark choices as user assumptions.",
     ["Check treatment/outcome residualization and benchmark scaling.", "Retain point-estimate and inferential sensitivity distinctions; test sign and monetary-unit transformations."],
     "The benchmark is not evidence of the actual strength or existence of an omitted confounder."),
    ("evalue", "seed:058", ["mediation_sensitivity"], {1: [(1, 27)]},
     ["evalues.RR accepts a risk ratio and optional interval bounds and reports E-values for the point and near-null confidence limit."],
     "Evaluate as an additional risk-ratio sensitivity summary; reject automatic conversion of arbitrary effect scales into this interface.",
     ["Test protective/harmful ratios, intervals crossing the null and missing intervals.", "Document scale conversion assumptions and preserve the original ratio and interval."],
     "An E-value is a sensitivity quantity, not an estimated correction or a certificate that confounding is absent."),
    ("tmle", "seed:059", ["effects_heterogeneity", "transport_missingness"],
     {1: [(1, 55), (66, 83)]},
     ["The selected interface documents binary point-treatment estimation with missingness and subject-ID options."],
     "Evaluate R integration for supported point-treatment effects; use a separately qualified longitudinal engine for dynamic regimes.",
     ["Match target population, outcome scale, propensity bounds and nuisance learners.", "Inspect Delta semantics and subject-level influence/covariance handling before enabling missing-treatment or repeated-record claims."],
     "DESCRIPTION and Delta wording differ on treatment missingness. That feature remains unresolved; no arbitrary longitudinal support is inferred."),
    ("stremr", "seed:060", ["longitudinal_survival", "policies_offpolicy"],
     {1: [(1, 17)], 2: [(1, 86)]},
     ["Sequential g-computation/TMLE documentation supplies survival targets and treatment/monitoring intervention probabilities.",
      "Qstratify is explicitly nonfunctional; weight truncation, stopping criteria and iteration limits are documented choices."],
     "Evaluate an R process adapter with typed histories and distinct monitoring, treatment and censoring fields; reject the nonfunctional option.",
     ["Test treatment-confounder feedback, monitoring interventions and administrative censoring.", "Expose truncation, iteration stopping and positivity diagnostics and test unavailable intervention histories."],
     "Old distribution dates do not establish abandonment. No longitudinal runtime or numerical coverage is qualified."),
    ("survtmle", "seed:062", ["longitudinal_survival"], {1: [(1, 86)]},
     ["The selected interface addresses right censoring, competing failures and cumulative incidence and supports two treatment values."],
     "Evaluate R integration preserving failure cause, horizon and cumulative-incidence estimand; do not relabel it a dynamic-regime engine.",
     ["Distinguish competing failure from censoring and validate event coding.", "Check treatment restriction, follow-up horizon, positivity and target-specific uncertainty."],
     "This selected interface does not establish arbitrary multiaction or sequential decision support."),
    ("drdid", "seed:063", ["panels_did"], {1: [(25, 58), (80, 105)]},
     ["The documented target is ATT for panel or stationary repeated-cross-section data, with separate mode and inference choices."],
     "Evaluate R integration with ATT and sampling-design fields mandatory; reject silent substitution for population ATE.",
     ["Check panel identifiers versus repeated samples, treatment groups and pre/post coding.", "Evaluate overlap and nuisance fits under the declared parallel-trend design; match bootstrap/cluster choices."],
     "Double robustness is conditional on the specified identification and nuisance-model structure; it is not design truth."),
    ("did2s", "seed:064", ["panels_did"], {1: [(23, 68)]},
     ["The first stage fits untreated observations, the second uses the full sample, and inference uses an adjusted/clustered standard-error contract."],
     "Evaluate R integration retaining both stages and treatment-timing coding; avoid treating the second regression's ordinary SE as the method's uncertainty.",
     ["Test staggered timing, cohort support and no anticipation coding.", "Check first-stage sample, omitted periods, generated outcomes and variance adjustment against the reference."],
     "A two-stage fit does not establish the causal parallel-trend assumptions or simultaneous event-path coverage."),
    ("synth", "seed:066", ["synthetic_controls"], {1: [(6, 20), (33, 65), (72, 85)]},
     ["The interface uses preprocessed predictor/outcome matrices and reports donor/predictor weights and optimization losses."],
     "Evaluate R integration for donor-weight construction; attach a separately justified uncertainty procedure to any effect claim.",
     ["Check donor membership, pre/post split, scaling, weight constraints and solver convergence.", "Retain pre-fit quality, optimization losses and sensitivity to donor removal."],
     "Selected weight/optimizer documentation does not supply universal placebo or confidence coverage."),
    ("augsynth", "seed:067", ["synthetic_controls", "panels_did"], {1: [(1, 54)]},
     ["The dispatcher distinguishes single-outcome, multiple-outcome and staggered settings and exposes distinct balance/regularization controls."],
     "Evaluate the author-repository R package through the appropriate estimator path; preserve augmentation and regularization choices.",
     ["Inspect the selected downstream implementation and inference method before use.", "Test poor donor balance, extrapolating weights and staggered target aggregation separately."],
     "CRAN mirror lookup returned 404; the audited author repository resolves source access only, not CRAN release or method qualification."),
    ("scpi", "seed:068", ["synthetic_controls"], {1: [(65, 113), (239, 256)]},
     ["The selected documentation distinguishes in-sample and out-of-sample uncertainty, donor constraint sets, solvers and simulation controls."],
     "Evaluate R integration with both uncertainty components and constraints preserved; no single standard-error field can replace this contract.",
     ["Test solver failure, simulation seeds, donor constraints and prediction-error sensitivity.", "Measure empirical coverage for the declared data law and horizon rather than treating a successful solve as calibration."],
     "A 2027 paper reference inside pre-cutoff documentation is not cited here as an audited scholarly work."),
    ("fect", "seed:069", ["panels_did", "synthetic_controls"],
     {1: [(46, 68), (81, 95)]},
     ["Documentation distinguishes fitting and treatment-effect aggregation weights; aggregation weights are not IPW or doubly robust confounding correction.",
      "The described parametric bootstrap has restrictions requiring method-specific review."],
     "Evaluate R integration separating fitting weights, target aggregation weights and the counterfactual fitting method.",
     ["Inspect actual 2.4.5 code where the manual retains earlier version-roadmap wording.", "Test switchers, event support, factor selection, weight semantics and the selected bootstrap's sampling law."],
     "Version-2.3.1/2.4.0 roadmap language remains in the 2.4.5 manual. Do not infer that every announced behavior is implemented."),
    ("eventstudyinteract", "seed:065", ["panels_did"],
     {1: [(12, 24), (43, 74), (76, 100)]},
     ["This is a community Stata package implementing interaction-weighted event-study estimates and pointwise intervals.",
      "The control cohort is never treated or last treated; periods in which the last cohort receives treatment must be excluded when it is the control.",
      "The help file warns that the cited validity result covers balanced panels without covariates while the implementation also accepts unbalanced panels."],
     "Evaluate a Stata subprocess adapter only with a licensed runtime and resolved package/dependency licenses; retain cohort weights and pointwise covariance.",
     ["Test cohort coding, last-cohort exclusion and supported relative-time cells.", "Check that e(b_iw)/e(V_iw), not the underlying interacted regression's e(b)/e(V), are exported.", "Qualify unbalanced panels/covariates separately; do not promise simultaneous bands."],
     "The inspected files do not establish a redistribution license. A commercial Stata runtime does not make the community estimator a built-in Stata vendor capability."),
]


def load(path):
    return json.loads(path.read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def receipt(identifier):
    path = RAW / (identifier + ".receipt.json")
    data = load(path)
    if data["status"] != "saved":
        raise ValueError("Required source unavailable: " + identifier)
    source = ROOT / data["path"]
    if digest(source) != data["sha256"]:
        raise ValueError("Source bytes changed: " + str(source))
    return data


def reference(data, anchor):
    return {"path": data["path"], "sha256": data["sha256"],
            "anchor": anchor, "source_url": data["url"],
            "accessed_utc": data["accessed_utc"]}


def field(text, key):
    match = re.search(r"^" + re.escape(key) + r":\s*([^\n]*(?:\n[ \t]+[^\n]*)*)", text, re.M)
    return " ".join(match.group(1).split()) if match else None


def pinned_source(identifier, repo, commit, tree):
    data = receipt(identifier)
    prefix = "https://raw.githubusercontent.com/" + repo + "/" + commit + "/"
    if not data["url"].startswith(prefix) or data["final_url"] != data["url"]:
        raise ValueError("Source is not at the audited immutable revision: " + identifier)
    path = data["url"].removeprefix(prefix)
    entry = next(x for x in tree["tree"] if x["path"] == path)
    body = (ROOT / data["path"]).read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(body)).encode() + b"\0" + body).hexdigest()
    if entry["type"] != "blob" or entry["sha"] != blob:
        raise ValueError("Source differs from committed Git blob: " + identifier)
    return data


def package_record(spec):
    name, candidate, areas, anchors, claims, decision, trials, limit = spec
    author = name in {"augsynth", "eventstudyinteract"}
    commit_data = receipt("v12_sw2_" + ("author" if author else "cran") + "_cutoff_" + name)
    commits = load(ROOT / commit_data["path"])
    commit = commits[0]["sha"]
    date = commits[0]["commit"]["committer"]["date"]
    if datetime.fromisoformat(date.replace("Z", "+00:00")) > CUTOFF:
        raise ValueError("Post-cutoff commit: " + name)
    repo = commit_data["url"].split("/repos/")[1].split("/commits")[0]
    tree_data = receipt("v12_sw2_tree_" + name)
    if "/git/trees/" + commit + "?" not in tree_data["url"]:
        raise ValueError("Tree revision mismatch: " + name)
    tree = load(ROOT / tree_data["path"])
    if tree.get("truncated"):
        raise ValueError("Incomplete tree: " + name)
    sources = []
    observed_version = "Help header 0.0 (2 April 2020); source pin " + commit
    license_text = None
    if name != "eventstudyinteract":
        desc = pinned_source("v12_sw2_description_" + name, repo, commit, tree)
        body = (ROOT / desc["path"]).read_text()
        observed_version, license_text = field(body, "Version"), field(body, "License")
        if not observed_version or not license_text:
            raise ValueError("Missing distribution identity: " + name)
        line_numbers = [i for i, line in enumerate(body.splitlines(), 1)
                        if any(line.startswith(k + ":") for k in ["Package", "Version", "Date", "License", "Depends", "NeedsCompilation"])]
        sources.append({**reference(desc, "DESCRIPTION fields at lines " + ", ".join(map(str, line_numbers))),
                        "role": "distribution_metadata_only"})
    for number, spans in anchors.items():
        doc = pinned_source("v12_sw2_manual_" + name + "_" + str(number), repo, commit, tree)
        lines = (ROOT / doc["path"]).read_text().splitlines()
        if any(lo < 1 or hi > len(lines) or lo > hi for lo, hi in spans):
            raise ValueError("Invalid inspected anchor: " + name)
        sources.append({**reference(doc, "; ".join(f"lines {lo}-{hi}" for lo, hi in spans)),
                        "role": "primary_technical_documentation", "line_spans": [list(span) for span in spans]})
    return {
        "id": "v12:pinned-package:" + name, "candidate_id": candidate,
        "kind": "software_documentation", "audit_status": "v12_pinned_primary_technical_inspection",
        "source_identity": "https://github.com/" + repo,
        "version_date": observed_version + "; commit " + commit + " at " + date,
        "observed_version": observed_version, "commit": commit, "commit_date": date,
        "cutoff_evidence": reference(commit_data, "Saved default-branch commit query with explicit cutoff; not a complete release-history census"),
        "tree_evidence": reference(tree_data, "Git blob identities checked for every selected DESCRIPTION/help file"),
        "local_copy": next(x for x in sources if x["role"] == "primary_technical_documentation"),
        "inspected_anchors": sources, "supported_claims": claims,
        "license_observed": license_text, "license_scope": "DESCRIPTION metadata only; full package/dependency/distribution review pending" if license_text else "No license established from inspected source files",
        "areas": areas, "dimension": "other_relevant" if name == "eventstudyinteract" else "R",
        "language_detail": "Stata" if name == "eventstudyinteract" else "R",
        "runtime_status": "not_run", "adoption_status": "proposed_for_SW07_not_accepted",
        "adoption_decision": decision, "required_trials": trials, "limits": limit,
        "maintenance_observation": "Saved commit date and distribution version only; neither current maintenance nor abandonment is inferred.",
        "evidence_boundary": "Static package-authored documentation; no external package code executed, no numerical parity or empirical coverage measured. Papers referenced inside documentation are not adopted as scholarly citations."
    }


def verify_local(record):
    """Check all reachable explicit local-byte identities in a saved record."""
    if isinstance(record, dict):
        if "path" in record and "sha256" in record:
            if digest(ROOT / record["path"]) != record["sha256"]:
                raise ValueError("Bound file changed: " + record["path"])
        for value in record.values():
            verify_local(value)
    elif isinstance(record, list):
        for value in record:
            verify_local(value)


def main(check_only=False):
    if (OUT / "receipt.json").exists():
        raise ValueError("SW01 has a frozen receipt; prepare a successor instead of enrichment")
    current = {name: load(OUT / (name + ".json")) for name in REGISTERS}
    updated = copy.deepcopy(current)
    for name in REGISTERS:
        verify_local(current[name])
    queries = query_records()  # verifies saved bytes and exact acquisition URLs
    previous = {x["id"]: x for x in current["search-ledger"]["queries"]}
    if not previous.keys() <= {x["id"] for x in queries}:
        raise ValueError("An existing acquisition would be dropped")
    query_map = {x["id"]: x for x in queries}
    for identifier, item in previous.items():
        # Preserve future manually added review fields on the existing records.
        query_map[identifier] = {**item, **query_map[identifier]}
    updated["search-ledger"]["queries"] = list(query_map.values())
    records = [package_record(spec) for spec in SPECS]
    tetrad = load(OUT / "tetrad-review.json")
    verify_local(tetrad)
    records.append({
        "id": "v12:pinned-source:tetrad", "candidate_id": "inherited:tetrad",
        "kind": "software_source", "audit_status": "v12_pinned_primary_technical_inspection",
        "source_identity": "https://github.com/cmu-phil/tetrad",
        "version_date": tetrad["project_version"] + "; " + tetrad["commit"] + "; " + tetrad["commit_date"],
        "observed_version": tetrad["project_version"], "commit": tetrad["commit"],
        "commit_date": tetrad["commit_date"], "local_copy": tetrad["records"]["pc"],
        "inspected_anchors": list(tetrad["records"].values()),
        "supported_claims": tetrad["supported_claims"], "license_observed": "Root GPLv3; selected source headers GPLv3-or-later",
        "license_scope": "Inspected root and selected headers; dependency/distribution review remains pending",
        "areas": ["discovery_iid", "discovery_latent", "identification_counterfactual"],
        "dimension": "Java", "language_detail": "Java", "runtime_status": "not_run",
        "adoption_status": "proposed_for_SW07_not_accepted", "adoption_decision": tetrad["adoption_decision"],
        "required_trials": tetrad["required_trials"], "limits": tetrad["limits"],
        "review_evidence": {"path": str((OUT / "tetrad-review.json").relative_to(ROOT)),
                            "sha256": digest(OUT / "tetrad-review.json"), "anchor": "Selected source findings and project arithmetic counterexamples"}})
    tetrad_tree = load(ROOT / receipt("v12_sw2_tetrad_tree")["path"])
    for name in ["pom", "pc", "fci", "ida"]:
        pinned_source("v12_sw2_tetrad_" + name, "cmu-phil/tetrad", tetrad["commit"], tetrad_tree)
    supplemental = OUT / "graphics-source-review.json"
    if supplemental.exists():
        extra = load(supplemental)
        verify_local(extra)
        records.extend(extra["records"])
    audit = {x["id"]: x for x in updated["source-audit"]["entries"]}
    candidates = {x["id"]: x for x in updated["catalog"]["candidates"]}
    for entry in records:
        audit[entry["id"]] = entry
        if entry["candidate_id"] not in candidates:
            if not entry["candidate_id"].startswith("discovered:"):
                raise ValueError("New candidates need a distinct discovery identity")
            candidates[entry["candidate_id"]] = {"id": entry["candidate_id"], "name": entry["display"],
                                                  "origin": "Additional inspected candidate beyond the 110 seed rows"}
        row = candidates[entry["candidate_id"]]
        row.setdefault("before_pinned_enrichment", copy.deepcopy(row))
        row.update({"areas": entry["areas"], "dimension": entry["dimension"],
                    "language_detail": entry["language_detail"], "role": "causal_method_candidate",
                    "identity": entry["local_copy"], "technical_status": "v12_pinned_primary_inspection_selected_anchors",
                    "version": entry["observed_version"], "commit": entry["commit"],
                    "license_observed": entry["license_observed"], "license_scope": entry["license_scope"],
                    "runtime_status": "not_run", "audit_id": entry["id"],
                    "cutoff_warning": "Saved pre-cutoff source revision; no latest-release or complete historical availability claim.",
                    "adoption_status": entry["adoption_status"], "adoption_decision": entry["adoption_decision"],
                    "required_trials": entry["required_trials"], "comparison_limits": entry["limits"]})
    candidates["seed:050"]["audited_component"] = "ivreg"
    candidates["seed:050"]["unaudited_component"] = "AER"
    relations = [
        {"from": "seed:061", "to": "inherited:gformula", "kind": "same_project_alias",
         "finding": "The inherited source names CausalInference/gfoRmula. Retain the seed spelling as an alias, not another implementation."},
        {"from": "seed:077", "to": "inherited:tetrad", "kind": "core_plus_unqualified_bridge_lead",
         "finding": "The Tetrad component is the existing Java project. py-tetrad remains a separately auditable Python bridge, not an independent causal algorithm qualification."},
        {"from": "seed:080", "to": "inherited:grf", "kind": "native_component_lead",
         "finding": "The named native core is part of the grf family. A separately callable C++ API and its boundary remain to inspect; no independent product count."},
        {"from": "seed:084", "to": "seed:094", "kind": "commercial_engine_edition_link_unverified",
         "finding": "The seed names overlap around SMILE. Exact engine/GeNIe edition, license and API relationships need official vendor originals; do not assert verified equivalence."}
    ]
    for relation in relations:
        row = candidates[relation["from"]]
        row["family_relation"] = relation
        row["deduplication_note"] = relation["finding"]
    updated["catalog"]["family_relations"] = relations
    updated["catalog"]["enrichment_revisions"] = sorted(set(updated["catalog"].get("enrichment_revisions", [])) | {REVISION})
    updated["catalog"]["candidates"] = list(candidates.values())
    updated["catalog"]["counts"]["pinned_package_reviews"] = len(records)
    updated["source-audit"]["entries"] = list(audit.values())
    updated["source-audit"]["warning"] = "Audit counts include inherited identities, selected manuals and newly pinned sources with distinct scopes. No count establishes exhaustive coverage or qualified execution."
    for cell in updated["coverage-matrix"]["cells"]:
        matched = [x for x in candidates.values() if cell["area"] in x["areas"] and cell["dimension"] == x["dimension"]]
        cell["candidate_ids"] = [x["id"] for x in matched]
        cell["v12_primary_inspected_ids"] = [x["id"] for x in matched if x["technical_status"] in {
            "v12_primary_manual_inspected_selected_anchors", "v12_pinned_primary_inspection_selected_anchors"}]
        if cell["v12_primary_inspected_ids"] and not cell.get("individual_review"):
            cell["status"] = "partial_primary_inspection"
            cell["review_finding"] = "Attached selected inspected sources. The full area/language search and cell-specific disposition still require individual review."
    items = updated["omissions"]["items"]
    for query in queries:
        if query["status"] == "failed" and not any(x["candidate_id"] == query["id"] for x in items):
            items.append({"candidate_id": query["id"], "reason": query.get("failure", "Acquisition failed"),
                          "claim_status": "unverified", "next_action": "Retain the failure; use a genuine dated alternative or retry after the provider rate limit clears. Never infer software absence."})
    for item in items:
        if item["candidate_id"] == "v12_sw2_cran_cutoff_augsynth":
            item.update({"claim_status": "source_access_resolved_by_author_repository_only", "next_action": "Use pinned author repository 7e70072232fe75057aa8b5d7af08c7e1aef53ae8; do not infer a CRAN release."})
        if item["candidate_id"] == "v12_sw2_cutoff_ananke":
            item.update({"claim_status": "identity_redirect_found_technical_text_unavailable", "next_action": "Current PyPI metadata points to https://gitlab.com/causal/ananke. GitLab is outside the fixed collector hosts; obtain genuine dated originals through a reviewed route. Current metadata does not establish cutoff functionality."})
        if item["candidate_id"] == "ambiguous-cutoff-rdrobust":
            item["claim_status"] = "4.0.0_snapshot_audited_4.1.1_cutoff_unresolved"
            item["next_action"] = "Use the inspected pre-cutoff 4.0.0 mirror revision for that scope. Establish the original 4.1.1 release/tarball availability separately; current October 8 manual cannot backdate it."
    review = {"schema_version": "causalbank.sw01-pinned-review/1", "revision": REVISION,
              "status": "partial_static_review", "cutoff": "2026-10-07", "records": records,
              "family_relations": relations, "essential_limits": [
                  "This enrichment does not close SW01 or any coverage cell.",
                  "Runtime, empirical coverage, legal distribution and commercial comparisons remain unqualified.",
                  "All cited technical claims refer to saved package/source passages; metadata establishes only identity/version/navigation."]}
    for name in REGISTERS:
        verify_local(updated[name])
    result = {"status": "verified_dry_run" if check_only else "merged", "revision": REVISION,
              "reviewed_packages": len(records), "audit_entries": len(audit), "catalog_rows": len(candidates),
              "acquisitions": len(queries), "saved": sum(q["status"] == "saved" for q in queries),
              "failed": sum(q["status"] == "failed" for q in queries),
              "not_fetched": sum(q["status"] == "registered_not_fetched" for q in queries),
              "changes": [n for n in REGISTERS if current[n] != updated[n]],
              "qualified_cells": sum(bool(c["closure_qualified"]) for c in updated["coverage-matrix"]["cells"])}
    if not check_only:
        backup = OUT / "before-pinned-enrichment"
        backup.mkdir(exist_ok=True)
        for name in REGISTERS:
            path = OUT / (name + ".json")
            if not (backup / path.name).exists():
                (backup / path.name).write_bytes(path.read_bytes())
        write(OUT / "pinned-package-review.json", review)
        for name in REGISTERS:
            write(OUT / (name + ".json"), updated[name])
        # This report remains stable on an idempotent second run.
        result.pop("changes")
        write(OUT / "enrichment-verification.json", result)
    print(json.dumps(result))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    main(parser.parse_args().check)

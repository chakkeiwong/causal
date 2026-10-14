#!/usr/bin/env python3
"""Build a conservative V12 software-search checkpoint from saved evidence."""
import hashlib
import json
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/program/repair-v12"
RAW = ROOT / "docs/literature/raw"
OUT = BASE / "work/SW01"


def load(path):
    return json.loads(path.read_text())


AREA = {
    "dowhy": ["identification_counterfactual"],
    "econml": ["effects_heterogeneity", "iv_rd_design"],
    "doubleml": ["effects_heterogeneity"],
    "causalml": ["effects_heterogeneity"],
    "grf": ["effects_heterogeneity", "iv_rd_design", "longitudinal_survival"],
    "tigramite": ["discovery_temporal_interventional", "discovery_latent"],
    "causallearn": ["discovery_iid", "discovery_latent"],
    "causalnex": ["discovery_iid"],
    "causica": ["discovery_iid", "bayesian_scm_state"],
    "gcastle": ["discovery_iid"], "dagma": ["discovery_iid"],
    "notears": ["discovery_iid"], "tetrad": ["discovery_iid"],
    "causalimpact": ["dynamic_panel_timeseries"],
    "causalpy": ["iv_rd_design", "panels_did", "synthetic_controls"],
    "linearmodels": ["iv_rd_design", "dynamic_panel_timeseries", "panels_did"],
    "pyfixest": ["iv_rd_design", "panels_did"],
    "fixest": ["iv_rd_design", "panels_did"],
    "did": ["panels_did"], "honestdid": ["panels_did"],
    "synthdid": ["synthetic_controls", "panels_did"],
    "gsynth": ["synthetic_controls", "panels_did"],
    "d3rlpy": ["policies_offpolicy"], "scope_rl": ["policies_offpolicy"],
    "obp": ["policies_offpolicy"], "pomdp_py": ["policies_offpolicy"],
    "pomdps": ["policies_offpolicy"],
    "pymc": ["bayesian_scm_state"], "numpyro": ["bayesian_scm_state"],
    "dynamax": ["bayesian_scm_state"],
    "duckdb": ["observations_data", "computation_workflow"],
    "polars": ["observations_data", "computation_workflow"],
    "ray": ["computation_workflow"],
    "datahub": ["observations_data"], "openmetadata": ["observations_data"],
    "openlineage": ["observations_data", "computation_workflow"],
    "feast": ["observations_data"], "splink": ["observations_data"],
    "pandera": ["observations_data"],
    "lmtp": ["longitudinal_survival", "policies_offpolicy"],
    "ltmle": ["longitudinal_survival"], "gformula": ["longitudinal_survival"],
    "zepid": ["longitudinal_survival", "transport_missingness"],
    "pydynpd": ["dynamic_panel_timeseries"],
}

LANGUAGE = {name: "R" for name in
            "grf causalimpact fixest did honestdid synthdid gsynth lmtp ltmle gformula".split()}
LANGUAGE.update({"tetrad": "Java", "pomdps": "other_relevant",
                 "duckdb": "C++", "polars": "other_relevant",
                 "openlineage": "other_relevant"})
ADJACENT = {"pomdp_py", "pomdps", "pymc", "numpyro", "dynamax", "duckdb",
            "polars", "ray", "datahub", "openmetadata", "openlineage", "feast",
            "splink", "pandera"}
MANUAL = {
    "dagitty": ["identification_counterfactual"],
    "pcalg": ["discovery_iid", "discovery_latent",
              "discovery_temporal_interventional", "identification_counterfactual"],
    "bnlearn": ["discovery_iid", "identification_counterfactual"],
    "causaleffect": ["identification_counterfactual", "transport_missingness"],
    "mediation": ["mediation_sensitivity"],
}


def query_records():
    records = []
    seen = set()
    for batch in sorted((BASE / "source-collection").glob("batch-*.json")):
        for req in load(batch)["requests"]:
            if not req["id"].startswith(("v12_sw_", "v12_sw2_")):
                continue
            if req["id"] in seen:
                raise ValueError("Duplicate software acquisition identity: " + req["id"])
            seen.add(req["id"])
            url = urlsplit(req["url"])
            receipt_path = RAW / (req["id"] + ".receipt.json")
            receipt = load(receipt_path) if receipt_path.exists() else None
            if receipt and receipt["url"] != req["url"]:
                raise ValueError("Acquisition URL changed: " + req["id"])
            record = {
                "id": req["id"], "batch": str(batch.relative_to(ROOT)),
                "provider": url.hostname, "url": req["url"],
                "query": parse_qs(url.query).get("search", parse_qs(url.query).get("q", [""]))[0],
                "cutoff_filter": parse_qs(url.query).get("filter", [None])[0],
                "status": receipt["status"] if receipt else "registered_not_fetched",
                "cutoff_commit_filter": parse_qs(url.query).get("until", [None])[0],
                "role": "bibliographic_discovery" if url.hostname == "api.openalex.org"
                        else "repository_identity_or_navigation" if req["extension"] in {"json", "html"}
                        else "primary_software_manual",
                "retrieval_date": receipt.get("accessed_utc") if receipt else None,
            }
            if receipt and receipt.get("status") == "saved":
                p = ROOT / receipt["path"]
                if hashlib.sha256(p.read_bytes()).hexdigest() != receipt["sha256"]:
                    raise ValueError("Search source drift: " + str(p))
                record["local_copy"] = {"path": receipt["path"], "sha256": receipt["sha256"]}
                if url.hostname == "api.openalex.org":
                    results = load(p)
                    record["reported_result_count"] = results["meta"]["count"]
                    record["top_discovery_leads"] = [
                        {"id": x.get("id"), "title": x.get("title"),
                         "publication_date": x.get("publication_date")}
                        for x in results.get("results", [])[:5]]
            elif receipt:
                record["failure"] = receipt.get("error")
            record["temporal_warning"] = (
                "Cutoff-filtered discovery metadata, not a technical software snapshot."
                if record["cutoff_filter"] else
                "Current retrieval; commit/release/document version must be checked before a cutoff claim.")
            records.append(record)
    return records


def main():
    # This seed builder predates individual source/cell review. Never replace
    # the current register with generated defaults after enrichment.
    existing = OUT / "catalog.json"
    if existing.exists() and load(existing).get("enrichment_revisions"):
        raise ValueError("SW01 is enriched; use tools/enrich_sw01_v12.py. Seed rebuild would discard reviewed evidence.")
    contract = load(BASE / "coverage-contract.json")
    prior = load(OUT / "inherited-reconciliation.json")
    audit = load(OUT / "source-audit.json")
    seeds = load(BASE / "candidate-seeds.json")["candidates"]
    query = query_records()
    by_query = {x["id"]: x for x in query}
    catalog = []
    inherited = {p["id"]: p for p in prior["projects"]}
    for seed in seeds:
        key = seed["candidate_id"].removeprefix("inherited:")
        old = inherited.get(key)
        manual = next((n for n in MANUAL if n.lower() == seed["name"].lower()), None)
        if old:
            primary = any(e["role"] == "primary_technical_text" for e in old["technical_evidence"])
            catalog.append({"id": seed["candidate_id"], "name": seed["name"],
                            "areas": AREA[key], "dimension": LANGUAGE.get(key, "Python"),
                            "role": "adjacent_engine_or_data" if key in ADJACENT else "causal_method_candidate",
                            "identity": old["source_record"],
                            "technical_status": "inherited_primary_inspection_not_v12_reaudited" if primary
                                                else "inherited_identity_only_no_technical_inspection",
                            "version": old["observed_package_version"],
                            "license_observed": old["license_observed"],
                            "runtime_status": old["runtime_status_inherited"],
                            "cutoff_warning": "Preserved October 8 mutable-source snapshot; scope/version requires V12 reinspection."})
        elif manual:
            entry = next(x for x in audit["entries"] if x["id"] == "v12:cran:" + manual)
            catalog.append({"id": seed["candidate_id"], "name": seed["name"],
                            "areas": MANUAL[manual], "dimension": "R",
                            "role": "causal_method_candidate",
                            "identity": entry["local_copy"],
                            "technical_status": "v12_primary_manual_inspected_selected_anchors",
                            "version": entry["version_date"],
                            "license_observed": "See manual page 1; distribution review pending",
                            "runtime_status": "not_run",
                            "cutoff_warning": "Manual generation predates cutoff; retrieval and current index are later."})
        else:
            catalog.append({"id": seed["candidate_id"], "name": seed["name"],
                            "areas": [], "dimension": None, "role": "unclassified_search_lead",
                            "identity": None, "technical_status": "unverified_seed",
                            "version": None, "license_observed": None,
                            "runtime_status": "not_run", "search_group": seed.get("search_group")})
    if len(catalog) != 110 or len({x["id"] for x in catalog}) != 110:
        raise ValueError("Candidate seed reconciliation failed")
    aliases = {"seed:061": "inherited:gformula", "seed:077": "inherited:tetrad",
               "seed:080": "inherited:grf", "seed:084": "seed:094"}
    for c in catalog:
        if c["id"] in aliases:
            c["possible_duplicate_of"] = aliases[c["id"]]
            c["deduplication_note"] = "Same family/name scope; package/core/bridge or commercial edition still needs explicit comparison. Do not count as an independent product."
    cells = []
    for cell in contract["software_cells"]:
        dim = cell["dimension"]
        slug = cell["area"] + "_" + {"C++": "cpp", "other_relevant": "other"}.get(dim, dim.lower())
        qid = "v12_sw_cell_" + slug
        record = by_query.get(qid)
        ids = [c["id"] for c in catalog if cell["area"] in c["areas"] and c["dimension"] == dim]
        inspected = [c["id"] for c in catalog if c["id"] in ids and c["technical_status"] ==
                     "v12_primary_manual_inspected_selected_anchors"]
        cells.append({"id": cell["id"], "area": cell["area"], "dimension": dim,
                      "query_id": qid, "query_status": record["status"] if record else "not_registered",
                      "candidate_ids": ids, "v12_primary_inspected_ids": inspected,
                      "status": "partial_primary_inspection" if inspected else
                                "official_primary_unavailable" if dim == "commercial" else
                                "discovery_or_inherited_leads_only" if record and record["status"] == "saved"
                                else "search_pending_or_failed",
                      "review_finding": "A search hit is not a capability or absence finding; matched technical sources and licensing/runtime remain to be checked.",
                      "closure_qualified": False})
    if len(cells) != 102 or {x["id"] for x in cells} != {x["id"] for x in contract["software_cells"]}:
        raise ValueError("Coverage cell mismatch")
    omissions = []
    for q in query:
        if q["status"] == "failed":
            omissions.append({"candidate_id": q["id"], "reason": q.get("failure", "Public source retrieval failed"),
                              "claim_status": "unverified", "next_action": "Find a genuine alternative primary source under the fixed collector policy, retain the failed receipt and re-audit exact version/technical anchors."})
    for x in catalog:
        if x.get("search_group"):
            if x["search_group"].startswith("Commercial"):
                omissions.append({"candidate_id": x["id"], "reason": "Official vendor domain is outside the frozen public collector allowlist; seed or search metadata is not a technical source.",
                                  "claim_status": "unverified", "next_action": "Use a separately reviewed fixed public-source acquisition route or an owner-supplied dated manual, then audit version, bytes and technical anchors."})
    omissions.append({"candidate_id": "all-commercial-cells", "reason": "No commercial product's current official technical manual is locally audited for all required cells.",
                      "claim_status": "unverified", "next_action": "Acquire dated Stata, SAS, MATLAB and causal-platform official manuals through an authorized narrow route; compare exact algorithms, APIs, licenses and prices under SW06."})
    omissions.append({"candidate_id": "post-cutoff-cran-econometrics", "reason": "CRAN Econometrics task view displays version 2026-10-08, after the fixed literature cutoff.",
                      "claim_status": "dated_delta_only", "next_action": "Use this page for leads only; find versioned pre-cutoff originals before baseline technical claims."})
    omissions.append({"candidate_id": "ambiguous-cutoff-rdrobust", "reason": "rdrobust manual heading is October 8, 2026 although package Date says October 7; October 7 source bytes are not established.",
                      "claim_status": "unverified_at_cutoff", "next_action": "Retrieve and inspect a pre-cutoff release or Git commit; retain the current manual as a dated acquisition."})
    ledger = {"schema_version": "causalbank.sw01-search/1", "task_id": "SW01", "status": "in_progress",
              "cutoff": "2026-10-07", "queries": query,
              "inclusion": "Named causal or adjacent software with inspectable version/license and a declared method role; evidence must be primary technical text before capability comparison.",
              "exclusion": "Irrelevant keyword collisions, model-only papers without software, predictive-only tools claimed as causal estimators, and vendor marketing claims without inspectable technical details.",
              "duplicate_policy": "Preserved 44 project identities take precedence over matching seed names; new sources attach to the same candidate, never count as a new product.",
              "limits": ["OpenAlex matches are noisy bibliography, not package coverage or absence evidence.",
                         "GitHub and CRAN current results were fetched after cutoff; only pre-cutoff release/commit content can substantiate baseline claims.",
                         "Fixed collector excludes most commercial vendor domains. No general web-search/market census is claimed."]}
    matrix = {"schema_version": "causalbank.sw01-coverage/1", "status": "in_progress",
              "cells": cells, "automatically_dispositioned_cell_count": sum(x["status"] != "search_pending_or_failed" for x in cells),
              "qualified_cell_count": 0,
              "warning": "These are generated provisional search/evidence dispositions pending individual author review, not completed market coverage or qualified adapters."}
    candidate = {"schema_version": "causalbank.sw01-catalog/1", "status": "in_progress",
                 "candidates": catalog, "counts": {"inherited": 44, "seed_total": 110,
                 "new_primary_manuals": len(MANUAL)}, "warning": "Mapped areas are leads to compare, not claims that every method in the area is implemented."}
    omission = {"schema_version": "causalbank.sw01-omissions/1", "status": "in_progress",
                "items": omissions, "essential_primary_access_unresolved": True}
    for name, value in [("search-ledger", ledger), ("coverage-matrix", matrix),
                        ("catalog", candidate), ("omissions", omission)]:
        (OUT / (name + ".json")).write_text(json.dumps(value, indent=2) + "\n")
    print(json.dumps({"query_records": len(query), "fetched": sum(x["status"] == "saved" for x in query),
                      "cells": len(cells), "catalog": len(catalog), "omissions": len(omissions)}))


if __name__ == "__main__":
    main()

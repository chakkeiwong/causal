#!/usr/bin/env python3
"""Record selected graph-software source inspections; never execute packages."""
import json
from datetime import datetime

from enrich_sw01_v12 import (CUTOFF, OUT, ROOT, load, pinned_source, receipt,
                             reference, verify_local, write)

SPECS = [
    {
        "name": "agrum", "display": "aGrUM/pyAgrum", "candidate_id": "seed:082",
        "dimension": "C++", "language_detail": "C++ core with Python wrapper; wrapper runtime separately unqualified",
        "observed_version": "3.2.0", "areas": ["identification_counterfactual", "bayesian_scm_state"],
        "license_observed": "LGPL-3.0-or-later OR MIT in root declaration and selected source headers",
        "files": {"impact": [[170, 283], [324, 344]], "model": [[69, 88]], "identify": [[102, 123]]},
        "metadata": {1: [[1, 4]], 2: [[41, 57]], 3: [[1, 12]]},
        "supported_claims": [
            "CausalModel documents a causal DAG with an optional observational BayesNet: structure-only queries can be available without numerical CPT evaluation.",
            "CausalImpact tries eligible backdoor/frontdoor paths, then a do-calculus call; this is inspected dispatch behavior, not a proof of ID/IDC correctness.",
            "NotImplementedYet and HedgeException are caught separately but both return a null-AST formula; messages differ. An adapter cannot infer theoretical nonidentification from isIdentified=false alone.",
            "Build declarations specify CMake >=3.18 and C++20; VERSION.txt declares 3.2.0. The build was not attempted."
        ],
        "adoption_decision": "Evaluate the existing core/wrapper before porting. Require distinct typed unsupported-method, nonidentification and unavailable-numerics results; preserve the symbolic expression and graph identity.",
        "required_trials": [
            "Construct graph-only and fitted-distribution cases with the same graph and compare symbolic versus numerical availability.",
            "Exercise unsupported-method and hedge paths separately and preserve the causal reason across a wrapper or process boundary.",
            "Independently verify backdoor/frontdoor/general identification fixtures, variable-domain mapping and intervention/evidence distinctions.",
            "Build actual C++20 and Python environments and review third-party license components before distribution."
        ],
        "limits": "No general identification proof, native build, wrapper parity, effect uncertainty or bank applicability is established by these source paths. Root licensing wording is not a completed dependency review."
    },
    {
        "name": "pgmpy", "display": "pgmpy", "candidate_id": "discovered:pgmpy",
        "dimension": "Python", "language_detail": "Python",
        "observed_version": "1.1.2", "areas": ["identification_counterfactual", "discovery_iid", "computation_workflow"],
        "license_observed": "MIT root license",
        "files": {"identify": [[14, 39], [43, 76]], "estimate": [[8, 30], [63, 95]],
                  "adjustment": [[104, 176], [178, 218]], "llmpairwise": [[15, 40], [129, 220]]},
        "metadata": {1: [[1, 18]], 2: [[1, 20]]},
        "supported_claims": [
            "The guide describes identification separately from estimation, with annotated graph roles and an identify/validate interface.",
            "The guide advertises variance-optimal adjustment, but the inspected minimal_variance implementation raises NotImplementedError.",
            "The minimal adjustment branch rejects multiple exposures/outcomes; the all branch enumerates subsets of selected ancestors. Selected docstring graph types and a TODO do not qualify every advertised graph class.",
            "LLMPairwise requires exactly two variables; it builds a prompt from names/descriptions and does not use observed values to orient the edge.",
            "The LLM prompt offers only A causes B or B causes A. The returned graph contains one directed edge; no no-edge/confounded/ambiguous outcome is represented.",
            "The inspected internal orientation cache uses only the unordered name pair. It does not include description, model, prompt or parameter identities in that key.",
            "The parser selects the first 1/2 digit before testing A/B tokens; a refusal sentence containing such a digit can therefore be interpreted as an orientation.",
            "pyproject.toml declares version 1.1.2 and Python >=3.10,<3.15; no installation was run."
        ],
        "adoption_decision": "Evaluate selected Python graph methods behind explicit capability checks. Reject raw LLMPairwise output as a qualified discovered graph; at most use it as an untrusted directional proposal with independent evidence, abstention, structured parsing and a full request-identity cache.",
        "required_trials": [
            "Exercise minimal_variance and multi-exposure requests as unsupported, without relabeling them nonidentified.",
            "Independently validate each accepted graph class and contrast adjustment-set failure with failure of general identification.",
            "Use disconnected, latent-confounded, reversed-label and ambiguous pairs; require preservation of all eligible graph alternatives.",
            "Change descriptions/model/prompt on a reused estimator and test cache invalidation; test refusal strings containing 1 or 2.",
            "Measure provider calls, exact prompt/response identities and costs only in a separately registered authorized study."
        ],
        "limits": "The findings concern this immutable source revision and selected paths. Base estimator reset/caller lifecycles and real provider behavior were not executed. The cache finding is conditional on reusing an instance with retained cache; no claim that every public fit call does so. No upstream package performance has been measured."
    },
    {
        "name": "causallearn", "display": "causal-learn", "candidate_id": "inherited:causallearn",
        "dimension": "Python", "language_detail": "Python",
        "observed_version": "0.1.4.8", "areas": ["discovery_iid", "discovery_latent", "transport_missingness"],
        "license_observed": "MIT root license",
        "files": {"pc": [[20, 49], [65, 140]], "fci": [[1061, 1180]]},
        "metadata": {1: [[1, 37]], 2: [[1, 21]]},
        "supported_claims": [
            "PC exposes conditional-independence test, alpha, stable-skeleton, collider rule/conflict priority, background knowledge and max_k options.",
            "The missing-value PC branch substitutes mv_fisherz for the default Fisher test and calls a distinct correction path; this does not establish validity for arbitrary missingness.",
            "The PC matrix describes tail, arrow and bidirected endpoint encodings. Conflict-priority settings can create bidirected edges; these cannot automatically be reinterpreted as latent-confounder conclusions.",
            "FCI documents tail/arrow/circle encodings, depth and discriminating-path bounds, invokes possible-d-separation and orientation routines, and marks the returned graph as a PAG.",
            "setup.py declares version 0.1.4.8, Python >=3.7 and dependencies; no compatibility/build trial was performed."
        ],
        "adoption_decision": "Evaluate direct Python integration for declared PC/FCI regimes; retain endpoint pairs, CI-test identity, search bounds, background knowledge and orientation-conflict provenance.",
        "required_trials": [
            "Roundtrip tails/arrows/circles and distinguish PC conflict bidirection from FCI latent-variable semantics.",
            "Use independent sufficient and latent graph fixtures with the exact CI-test/sampling assumptions; alpha is not whole-graph confidence.",
            "Record effect on graph alternatives when depth/path/max_k truncation is used.",
            "Qualify each missingness correction and dependency environment separately before supporting incomplete bank panels."
        ],
        "limits": "Selected wrappers/dispatch and endpoint contracts only. No complete algorithm audit, run, causal-graph coverage or temporal/selection/missingness generality is established."
    },
]


def main():
    records = []
    for spec in SPECS:
        name = spec["name"]
        commit_source = receipt("v12_sw_cutoff_commit_" + name)
        commit_record = load(ROOT / commit_source["path"])[0]
        commit = commit_record["sha"]
        date = commit_record["commit"]["committer"]["date"]
        assert datetime.fromisoformat(date.replace("Z", "+00:00")) <= CUTOFF
        repo = commit_source["url"].split("/repos/")[1].split("/commits")[0]
        tree_source = receipt("v12_sw2_tree_" + name)
        tree = load(ROOT / tree_source["path"])
        assert "/git/trees/" + commit + "?" in tree_source["url"] and not tree.get("truncated")
        anchors = []
        for prefix, files, role in [("source", spec["files"], "primary_technical_text"),
                                    ("metadata", spec["metadata"], "version_build_license_metadata")]:
            for key, spans in files.items():
                source = pinned_source("v12_sw2_" + prefix + "_" + name + "_" + str(key), repo, commit, tree)
                lines = (ROOT / source["path"]).read_text().splitlines()
                assert all(1 <= lo <= hi <= len(lines) for lo, hi in spans), (name, key, len(lines))
                anchors.append({**reference(source, "; ".join(f"lines {lo}-{hi}" for lo, hi in spans)),
                                "line_spans": spans, "role": role})
        record = {k: v for k, v in spec.items() if k not in {"files", "metadata"}}
        record.update({
            "id": "v12:pinned-graphics:" + name, "kind": "software_source",
            "audit_status": "v12_pinned_primary_technical_inspection", "source_identity": "https://github.com/" + repo,
            "commit": commit, "commit_date": date,
            "version_date": spec["observed_version"] + "; " + commit + "; " + date,
            "cutoff_evidence": reference(commit_source, "Saved pre-cutoff commit query; inspected source revision only"),
            "tree_evidence": reference(tree_source, "Selected technical and metadata files checked against committed Git blobs"),
            "inspected_anchors": anchors, "local_copy": anchors[0], "runtime_status": "not_run",
            "license_scope": "Selected root license/declaration and source headers; dependency/distribution review pending",
            "adoption_status": "proposed_for_SW07_not_accepted",
        })
        verify_local(record)
        records.append(record)
    report = {"schema_version": "causalbank.sw01-supplement/1", "revision": "graphics-static-2026-10-12",
              "status": "partial_static_review", "records": records, "runtime_executed": False,
              "llm_repair_handoff": "Carry the pgmpy directional-proposal, parser and cache findings into LA07 without editing frozen LA01/LA03/LA04 receipts."}
    write(OUT / "graphics-source-review.json", report)
    print(json.dumps({"reviewed_families": len(records), "selected_files": sum(len(r["inspected_anchors"]) for r in records), "external_code_executed": False}))


if __name__ == "__main__":
    main()

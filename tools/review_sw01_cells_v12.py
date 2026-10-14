#!/usr/bin/env python3
"""Attach authored partial reviews to the cells with inspected primary text."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/program/repair-v12/work/SW01"

REVIEWS = {
    "discovery_iid::R": (
        "pcalg and bnlearn selected manuals establish named discovery families, with different graph/functional assumptions.",
        "Inspect method-specific defaults, tests, model classes and maintenance; no complete R-family census or numerical qualification."),
    "discovery_iid::Python": (
        "causal-learn PC source exposes CI tests, collider/conflict handling and endpoint encoding. pgmpy's inspected LLM pairwise path is a forced directional proposal, not data-based general discovery.",
        "Reinspect other inherited Python candidates at cutoff pins; compare functional/score/continuous methods and candidate omissions."),
    "discovery_iid::Java": (
        "Tetrad PC selected source documents sufficient/acyclic/faithful setting, external CI test and CPDAG output.",
        "Inspect Java alternatives and the full test/configuration paths; Weka and Banjo leads are not resolved by one Tetrad audit."),
    "discovery_latent::R": (
        "pcalg's inspected FCI/PAG and IDA passages distinguish latent-graph discovery from effects across sufficient-graph alternatives.",
        "Audit selected FCI/RFCI variants, selection assumptions and conversions; do not infer effect identification or calibrated class coverage."),
    "discovery_latent::Python": (
        "The pinned causal-learn FCI entry uses circle endpoints, possible-d-separation and PAG marking.",
        "Inspect CI-test applicability and complete algorithm/source variants; graph truth and confidence coverage remain unmeasured."),
    "discovery_latent::Java": (
        "The pinned Tetrad FCI path supports PAG-oriented behavior; a conflicting CPDAG class comment is explicitly rejected as the serialization contract.",
        "Verify endpoint roundtrip, latent/selection assumptions and full algorithm behavior under a qualified Java environment."),
    "discovery_temporal_interventional::R": (
        "pcalg's selected manual names GIES and FCI-JCI contexts, establishing an interventional-method lead.",
        "This does not cover the entire temporal-discovery cell. Audit temporal methods, lags, intervention metadata and sampling assumptions separately."),
    "identification_counterfactual::R": (
        "DAGitty/causaleffect manuals establish graph-query and symbolic-identification interfaces; pcalg/ivmodel preserve distinct effect-candidate or confidence-set objects.",
        "Audit general ID/IDC, counterfactual and partial-identification coverage individually; no method count substitutes for scope comparison."),
    "identification_counterfactual::Python": (
        "pgmpy identification documentation and adjustment source disagree on implemented minimal-variance support; minimal adjustment is restricted to one exposure/outcome.",
        "Complete DoWhy, y0 and Ananke source reviews. Ananke current PyPI metadata points to GitLab, while the guessed GitHub identity failed; no absence finding."),
    "identification_counterfactual::Java": (
        "Tetrad IDA source provides continuous-data effect candidates with logged candidate failures; its hull distance is not discrete-set distance.",
        "Do not call IDA general latent identification or confidence-set construction. Inspect other identification/counterfactual interfaces and failure representations."),
    "identification_counterfactual::C++": (
        "aGrUM's selected native source distinguishes structural and numeric prerequisites but folds unsupported and hedge paths into a null-expression status with different messages.",
        "Qualify the actual do-calculus algorithms, wrapper semantics and competing native engines; root source dispatch is not an ID correctness proof."),
    "effects_heterogeneity::R": (
        "tmle selected documentation supplies point-treatment targets and options; inherited grf is a separate unreaudited candidate.",
        "Complete heterogeneous/continuous effect, forest and double-ML comparisons, including R counterparts and dose-response leads. The tmle missing-treatment wording remains unresolved."),
    "iv_rd_design::R": (
        "Five pinned reviews distinguish IV regression, weak-IV inversion, local-polynomial RD, density diagnostics and local-randomization inference.",
        "Complete AER and other eligible designs, license/dependency audits and matched trials; rdrobust 4.1.1 cutoff availability remains unresolved although 4.0.0 is pinned."),
    "longitudinal_survival::R": (
        "stremr selected docs support sequential survival/treatment/monitoring operations; survtmle has a distinct competing-risk target and two-treatment interface.",
        "Reaudit lmtp/ltmle/gfoRmula and other target-trial tools; qualify histories, censoring and uncertainty for each regime rather than generalizing from names."),
    "policies_offpolicy::R": (
        "stremr intervention probabilities create a scoped regime-evaluation candidate.",
        "General policy learning, unknown loggers, continuous actions and controlled-state models are not covered. Compare the remaining policy family and preserve those boundaries."),
    "panels_did::R": (
        "DRDID, did2s, augsynth and fect reviews preserve ATT/design choices, staged inference, dispatcher modes and fitting versus aggregation weights.",
        "Reaudit inherited did/HonestDiD/fixest/synthdid/gsynth, simultaneous inference and dependent sampling; no complete panel census is claimed."),
    "panels_did::other_relevant": (
        "eventstudyinteract is an inspected community Stata implementation with cohort restrictions and pointwise covariance output.",
        "Resolve package/dependency license and licensed runtime; inspect other-language offerings. Do not count this as native vendor functionality."),
    "synthetic_controls::R": (
        "Synth, augsynth, scpi and fect selected docs distinguish weight fitting, augmentation, prediction uncertainty and target aggregation.",
        "Inspect complete inference implementations, donor assumptions and inherited alternatives; pin and execute solver/dependency environments in the later qualification phase."),
    "mediation_sensitivity::R": (
        "mediation, medflex, sensemakr and EValue supply different mediation or sensitivity objects, not one generic confounding correction.",
        "Review negative-control/path-specific alternatives and model restrictions; mediation expansion/bootstraps and sensitivity assumptions need separate qualification."),
    "transport_missingness::R": (
        "causaleffect selected manual names transport formulas and tmle documents selected missingness options.",
        "Complete transport/generalization and missing-data families. Missing-treatment wording is unresolved and documentation does not certify selection or inclusion truth."),
    "transport_missingness::Python": (
        "The inspected causal-learn PC wrapper contains a missing-value branch and correction dispatch.",
        "This is a narrow missingness lead, not general transport, missing-not-at-random or bank inclusion support. Inspect the correction and broader Python families."),
    "bayesian_scm_state::C++": (
        "aGrUM CausalModel distinguishes a causal DAG from an optional observational BayesNet; selected native source can support structural-only work.",
        "No general latent-state, dynamic policy or posterior calibration claim follows. Reconcile libDAI/OpenGM/SMILE and complete causal versus adjacent-engine distinctions."),
    "computation_workflow::Python": (
        "The selected pgmpy LLM proposal path has conditional cache-identity and permissive parsing concerns; source findings inform an adapter contract.",
        "This narrow proposal-path review does not cover distributed computation, provenance or all agent frameworks; integrate their separate LA/IN evidence without treating them as causal engines."),
}


def main():
    path = OUT / "coverage-matrix.json"
    data = json.loads(path.read_text())
    by_id = {c["id"]: c for c in data["cells"]}
    assert set(REVIEWS) == {c["id"] for c in data["cells"] if c["v12_primary_inspected_ids"]}
    for key, (finding, remaining) in REVIEWS.items():
        cell = by_id[key]
        cell["individual_review"] = {"date": "2026-10-12", "reviewer": "Current author; not independent acceptance",
                                     "disposition": "partial_primary_scope_review",
                                     "finding": finding, "remaining": remaining,
                                     "candidate_ids_reviewed": cell["v12_primary_inspected_ids"],
                                     "evidence_register": "docs/program/repair-v12/work/SW01/source-audit.json"}
        cell["review_finding"] = finding + " " + remaining
        cell["closure_qualified"] = False
    data["individually_partially_reviewed_cells"] = len(REVIEWS)
    data["remaining_individual_review_cells"] = len(data["cells"]) - len(REVIEWS)
    data["qualified_cell_count"] = 0
    data["warning"] = "23 individual partial scope reviews; 79 cells still need individual review. No cell is closed as exhaustive coverage or qualified execution."
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"partial_cell_reviews": len(REVIEWS), "remaining": len(data["cells"]) - len(REVIEWS), "closed_cells": 0}))


if __name__ == "__main__":
    main()

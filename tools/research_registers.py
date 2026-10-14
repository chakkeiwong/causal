#!/usr/bin/env python3
"""Record material claims and bounded reference-following checks, without network access."""
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
LIT = ROOT / "docs/literature"

# Author mappings: statement, manuscript anchor, evidence class, supporting keys,
# and any executed evidence. Source anchors are preserved separately in each record.
CLAIMS = [
 ("The product develops policy/transmission, sequential/controlled-latent and discovery/data workspaces from its initial program, sharing scientific semantics with different qualification states.",
  "ch:product", "product_proposal", [], []),
 ("Bank deposits, refinancing, liquidity shocks and mortgage equilibrium require different identifying designs; published coefficients are not transferable campaign effects.",
  "ch:product", "literature_synthesis", ["drechsler2017","basten2026","agarwal2020","mian2006","benetton2021","beraja2019"], []),
 ("Consistency, exchangeability and positivity identify the stated population mean by adjustment.",
  "eq:adjust", "inherited_identification", ["hernan2020","peters2017","swig2013"], []),
 ("The conditional AIPW bias factorizes into products of propensity and outcome-regression errors; dependent inference needs separate conditions.",
  "eq:drbias", "author_derivation_of_standard_result", ["dml2018","wager2025"], []),
 ("The synthetic static ATE is 8, population naive contrast 54.8 and sample AIPW about 8.472.",
  "ch:identification", "synthetic_executed", [], ["tools/run_examples.py","docs/examples/results.json"]),
 ("Three fixed-policy paired comparisons use Bonferroni simultaneous intervals; selective policy superiority over all-treatment is not established.",
  "ch:identification", "synthetic_executed", [], ["tools/run_examples.py","docs/examples/results.json"]),
 ("An instrumental-variable or threshold effect depends on its own exclusion, compliance or continuity design and population.",
  "eq:wald", "inherited_identification", ["hernan2020","applied2024"], []),
 ("Group-time ATT requires valid untreated comparisons and explicit aggregation weights.",
  "eq:gtatt", "inherited_identification", ["callaway2021","roth2023"], []),
 ("Heterogeneous staggered adoption can contaminate TWFE/event-study coefficients even under parallel untreated trends.",
  "ch:panels", "literature_and_synthetic", ["bacon2021","sun2021","borusyak2024"], ["docs/examples/results.json"]),
 ("Pretrend non-rejection is insufficient; sensitivity and reversible/intensity-changing treatment require appropriate designs.",
  "ch:panels", "literature_synthesis", ["rambachan2023","dechaisemartin2024"], []),
 ("Dynamic panel differencing needs valid lag instruments, serial-correlation restrictions and instrument-count sensitivity.",
  "ch:panels", "literature_synthesis", ["arellano1991","panelreview2024"], []),
 ("Synthetic and augmented controls, synthetic DiD and structural time-series comparisons need valid donors, support and stable counterfactual structure.",
  "ch:panels", "literature_synthesis", ["abadie2010","abadie2021","benmichael2021","synthdid2021","brodersen2015"], []),
 ("Replacing action mechanisms gives the g-formula and IPW representation under sequential exchangeability and policy support.",
  "eq:gformula", "inherited_identification_and_derivation", ["hernan2020"], []),
 ("The recursive fixed-policy score uses weighted residuals; longitudinal nuisance rates and sequential robustness are construction-specific.",
  "eq:longdr", "literature_synthesis", ["nested2022","singh2022","sequentialdr2018"], []),
 ("Dynamic DML via g-estimation uses structured dynamic effects and independent trajectories; it is not a generic aggregate-series theorem.",
  "ch:longitudinal", "literature_synthesis", ["dynamicdml2021"], []),
 ("Exact two-decision g-formula and IPW means are 26.5 and 35.5; summing conditional direct coefficients gives 7 instead of total effect 9.",
  "ch:longitudinal", "synthetic_exact", [], ["tools/run_examples.py","docs/examples/results.json"]),
 ("Incremental propensity interventions preserve deterministic assignment regions and have a propensity-dependent target.",
  "eq:incremental", "literature_synthesis", ["kennedy2019"], []),
 ("Modified policies, selective eligibility and competing risks change the target and require their own assumptions.",
  "eq:cif", "literature_synthesis_and_probability_identity", ["lmtp2023","selective2025","competing2026"], []),
 ("Deep sequential predictors retain ignorability and overlap assumptions and need causal comparators beyond factual prediction.",
  "ch:longitudinal", "literature_synthesis", ["bica2020","melnychuk2022","gnet2020"], []),
 ("The long-run score variance and trajectory/cluster splitting depend on sampling structure, not transaction row count.",
  "eq:lrv", "standard_identity_and_literature_synthesis", ["cluster2021","bertrand2004"], []),
 ("Regime transport and network spillovers require substantive invariance or exposure assumptions.",
  "ch:scale", "literature_synthesis", ["hernan2020","beraja2019","benetton2021"], []),
 ("Large-study memory and finite-state filtering complexity are analytical estimates; scale tiers and latency are future targets.",
  "ch:scale", "engineering_analysis_and_proposed_benchmark", [], []),
 ("The observed POMDP likelihood includes behavior assignment when the logger uses private latent information.",
  "eq:pomdplikelihood", "author_factorization_with_literature_context", ["kaelbling1998","tennenholtz2020","bennett2021"], []),
 ("The belief recursion uses transition, reward and emission information; private logging additionally updates latent-state belief through the observed action.",
  "eq:belief", "author_probability_derivation", ["kaelbling1998","tennenholtz2020"], ["docs/examples/results.json"]),
 ("HMM statistical identification is distinct from controlled causal identification.",
  "ch:pomdp", "literature_synthesis_and_counterexample", ["hmmident2016"], ["docs/examples/results.json"]),
 ("The constructed identical observed binary laws imply ATE 0 and 0.36 in different models.",
  "ch:pomdp", "author_constructive_counterexample", [], ["tools/run_examples.py","docs/examples/results.json"]),
 ("Proximal bridges need proxy exclusions, completeness, existence and support; predictive proxy quality alone is insufficient.",
  "eq:bridge", "inherited_identification", ["miao2018","proximal2020","ghassami2022","proxreg2024"], []),
 ("Confounded sequential OPE and hidden-treatment identification impose particular proxy or instrument information structures.",
  "ch:pomdp", "literature_synthesis", ["tennenholtz2020","bennett2021","bennettprox2023","xu2023","hidden2026"], []),
 ("Markov OPE and policy-learning inference require appropriate state information, support and correction for policy selection.",
  "eq:opedr", "literature_synthesis", ["kallus2020","policy2021"], []),
 ("Stage-local confounding bounds and recent history-dependent OPE hardness are research results, not blanket guarantees for bank histories.",
  "ch:pomdp", "recent_preprint_synthesis", ["sharpdynamic2026","opehard2026"], []),
 ("The forward likelihood equals 16-path enumeration; fitted transitions in one known-emission randomized simulation have maximum error about 0.050.",
  "fig:belief", "synthetic_executed", [], ["tools/run_examples.py","docs/examples/results.json"]),
 ("A Gumbel-max coupling adds assumptions for individual counterfactual paths beyond fitted transition probabilities.",
  "ch:pomdp", "literature_synthesis", ["oberst2019"], []),
 ("DAG, CPDAG, PAG, lineage and entity edges have different semantics.",
  "ch:discovery", "literature_synthesis_and_contract", ["peters2017","gerhardus2020"], ["contracts/graph.schema.json"]),
 ("NOTEARS acyclicity follows from nonnegative closed-walk traces and is not a causal-identification theorem.",
  "eq:notears", "author_explanation_of_primary_theorem", ["notears2018","dagma2022"], []),
 ("Temporal discovery families impose different sufficiency, stationarity, innovation and lag assumptions.",
  "tab:discovery", "literature_synthesis", ["kalisch2007","shimizu2006","hyvarinen2010","runge2019","runge2020","gerhardus2020","pamfil2020"], []),
 ("Missingness and aggregation can invalidate naive discovery; continuous-time and recent temporal methods remain conditional research comparators.",
  "ch:discovery", "literature_synthesis", ["tu2019","boeken2024","bongers2022","sde2026","itsy2026","lucid2026","causalts2026","vargas2026"], []),
 ("Historical features need both event-time and actual decision-availability checks; known future schedules need a separate role.",
  "eq:availability", "proposed_semantics_with_executed_contract", ["sw_feast"], ["contracts/temporal_event.schema.json","docs/examples/contract-checks.json"]),
 ("Entity resolution, missingness and recovered-data uncertainty must travel with the study rather than disappear into a completed table.",
  "ch:data", "literature_and_product_design", ["corrupt2022","sw_splink","localrepos"], []),
 ("Catalog and lineage software provides data foundations, while causal semantics remain additional product responsibilities.",
  "ch:data", "software_inspection_and_design", ["sw_datahub","sw_openmetadata","sw_openlineage","sw_feast","sw_pandera"], []),
 ("BCBS239 supports integrated taxonomies, ownership and reconciliation without mandating a single physical model.",
  "ch:data", "official_guidance_inspection", ["bcbs239"], []),
 ("EconML DynamicDML requires equal trajectory lengths and chronological group order in the inspected implementation.",
  "ch:software", "api_source_inspection", ["sw_econml"], ["docs/literature/raw/api_econml_dynamic.txt"]),
 ("lmtp is AGPL-3 according to DESCRIPTION and license text despite the GPL-3 README badge.",
  "ch:software", "license_text_inspection", ["sw_lmtp"], ["docs/literature/raw/description_lmtp.txt","docs/literature/raw/license_detail_lmtp.json"]),
 ("Four schemas and selected semantic checks are implemented; full APIs and sibling adapters are proposed.",
  "ch:architecture", "implemented_specification_boundary", [], ["contracts/README.md","tools/check_contracts.py","docs/examples/contract-checks.json"]),
 ("cardnpv contrast direction, dataml recovery uncertainty and SMEwallet synthetic evidence must survive integration.",
  "tab:repos", "local_document_inspection_and_proposal", ["localrepos"], ["docs/literature/local-repositories/index.json"]),
 ("SR26-2 supersedes SR11-7 and SR21-8; generative/agentic models are outside its stated scope.",
  "ch:architecture", "official_guidance_inspection", ["fed2026"], []),
 ("PRA SS1/23 has an April 2026 revision and specified institutional applicability.",
  "ch:architecture", "official_guidance_inspection", ["pra2026"], []),
 ("500-replication coverage precision, illustrative experimental sample sizes and 30 percent workflow savings are proposed qualification calculations/targets.",
  "ch:validation", "author_planning_calculation_and_target", [], []),
 ("The illustrative broader NPV is about 3.958 million in the base case and becomes negative if first-year benefit is absent.",
  "ch:economics", "planning_assumptions_with_executed_arithmetic", [], ["tools/run_examples.py","docs/examples/results.json"]),
 ("The six-month tranche assumes 36 person-months at 25000 dollars plus compute and contingency, totaling 1.14 million dollars.",
  "ch:delivery", "planning_assumptions_with_executed_arithmetic", [], ["docs/examples/results.json"]),
 ("CausalFM, temporal PFNs and ProximalFM do not remove the identification restrictions supplied to their synthetic/model priors.",
  "ch:frontier", "recent_research_synthesis", ["causalpfn2026","panelpfn2026","proximalfm2026"], []),
 ("The survey is purposive, bounded by saved queries and accessible full texts, with explicit version repairs and correction-check limits.",
  "app:evidence", "research_protocol", ["banksurvey2023","panelreview2024"], ["docs/literature/discovery-counts.json","docs/literature/metadata-audit.json"]),
]

CLAIMS += [
 ("Residualized partially linear effects are variance-weighted averages under the stated heterogeneous-response model, not automatically the population ATE.", "ch:identification", "author_derivation_of_standard_result", ["dml2018"], []),
 ("Within transformations require strict exogeneity and leave no treatment variation when policy is perfectly absorbed by unit/time effects.", "ch:panels", "author_derivation_and_literature_synthesis", ["panelreview2024"], []),
 ("Sequential residual cancellation protects fixed-policy means along the stated correct-value or correct-action-law routes; finite-sample coverage is separate.", "ch:longitudinal", "author_derivation_and_exact_verification", ["jiang2016","sequentialdr2018"], ["tools/verify_revision.py","docs/reviews/revision-verification.json"]),
 ("External-instrument local projections need the stated lead/lag exclusions, relevance and normalization; a reduced-form VAR covariance does not uniquely identify a structural impact matrix.", "ch:scale", "literature_synthesis_and_derivation", ["jorda2024","stock2018"], ["docs/derivations/results.json"]),
 ("The 1200-panel Gaussian common-shock experiment has approximate interval coverage 0.227 with row inference, 0.693 with entity clustering and 0.944 with crossed clustering.", "tab:dependence-coverage", "synthetic_repeated_sample", [], ["tools/revision_studies.py","docs/derivations/results.json"]),
 ("Controlled forward/backward expected counts include latent action selection and agree with exhaustive short-path likelihood/posterior enumeration.", "eq:controlled-smoothing", "author_extension_and_numerical_verification", ["rabiner1989"], ["tools/revision_studies.py","tools/verify_revision.py","docs/reviews/revision-verification.json"]),
 ("Unknown-emission HMM fits compare randomized, omitted-hidden-logging and joint-hidden-logging designs; joint modeling remains conditional on the stipulated environment.", "tab:hmm-estimation", "synthetic_fitted_study", [], ["tools/revision_studies.py","docs/derivations/results.json"]),
 ("All 30 omitted and seven joint selected repetition fits hit their iteration cap; a longer same-data main fit preserves the sign reversal. These are finite-budget comparisons, not certified global optima.", "ch:latentestimation", "numerical_diagnostic_and_followup", [], ["docs/derivations/results.json","docs/reviews/revision-verification.json"]),
 ("The 79-resample randomized HMM bootstrap refits initial, emission and transition parameters; its coarse interval and one capped fit do not establish coverage.", "ch:latentestimation", "synthetic_bootstrap", [], ["docs/derivations/results.json"]),
 ("Belief-grid values under the supplied true environment are conditional planning calculations; contraction is a control result rather than observational identification.", "eq:belief-bellman", "standard_derivation_and_synthetic_planning", ["kaelbling1998"], ["docs/derivations/results.json"]),
 ("The 96-branch deposit study has positive balance effects but negative monthly funding contribution when the promotion reprices existing funds.", "ch:deposits", "synthetic_fitted_banking_study", [], ["tools/revision_studies.py","docs/derivations/results.json","docs/reviews/revision-verification.json"]),
 ("The collections study fits transitions on independent training data, compares three fixed policies and uses paired evaluation scores for two simultaneous contrasts.", "ch:collections", "synthetic_fitted_banking_study", ["jiang2016"], ["tools/revision_studies.py","docs/derivations/results.json"]),
 ("Three-decision path enumeration verifies robustness identities and shows the current-action-only shortcut estimates the wrong sustained policy value.", "ch:validation", "exact_finite_path_verification", [], ["tools/verify_revision.py","docs/reviews/revision-verification.json"]),
 ("The 600-firm 24-bank supply example compares a pooled coefficient near -1.08 with a borrower-effect coefficient near -2.92 against generating -3; it does not certify few-cluster coverage.", "ch:credit", "synthetic_fitted_banking_study", ["mian2006"], ["tools/revision_studies.py","docs/derivations/results.json"]),
 ("Revision selection must precede economic-window filtering; the executable account gives 160 then 90 dollars and rejects unverified feed completeness.", "ch:data", "implemented_semantics_and_adverse_fixture", [], ["src/causalbank/temporal.py","tools/run_data_scale.py","docs/derivations/data-scale.json"]),
 ("The mergeable reducer retains entity/date intersections, centers globally and agrees with an independent batch covariance; it does not construct causal scores or choose dependence assumptions.", "ch:construction", "implemented_numerical_component", [], ["src/causalbank/scores.py","tools/run_data_scale.py","docs/derivations/data-scale.json"]),
 ("Ten-million-row timing measures generated precomputed-score reduction only, with dense cluster-cardinality memory; it excludes data I/O and all model fitting.", "tab:scale-results", "bounded_component_measurement", [], ["tools/run_data_scale.py","docs/derivations/data-scale.json"]),
 ("General operations, lifecycle, retry semantics and repository adoption journeys are proposed; two narrow components and four schemas are implemented.", "ch:construction", "proposed_construction_with_explicit_prototype_boundary", ["localrepos"], ["pyproject.toml","contracts/README.md"]),
 ("The equal-output illustrative cost comparison has a constant annual reuse threshold 26.737 studies, with losing low-use and ramp scenarios and a favorable high-use case.", "eq:reuse-threshold", "author_economic_derivation_and_executed_arithmetic", [], ["tools/construction_economics.py","docs/derivations/economics.json","docs/reviews/revision-verification.json"]),
 ("Incremental product value must exclude expert-comparator benefits and avoid double counting workflow savings; adoption and outcome maturity affect cash timing.", "eq:incremental-product-npv", "author_economic_account_and_product_proposal", [], ["docs/derivations/economics.json"]),
 ("Recent amortized inference methods shift computation into synthetic priors while retaining identification, proxy and model restrictions; reliability predictions are not general certificates.", "ch:frontier", "critical_primary_source_synthesis", ["causalpfn2026","panelpfn2026","proximalfm2026"], []),
 ("Recent dynamic bounds require stage-local confounding, while history-dependent OPE hardness warns against treating behavior-marginal coverage as a universal complexity guarantee.", "ch:frontier", "bounded_recent_preprint_synthesis", ["sharpdynamic2026","opehard2026"], []),
 ("ITSY's inspected setup uses first-order lags, sufficiency, stationarity and MCAR; informative bank observations can violate that comparator domain.", "ch:frontier", "primary_method_restriction_inspection", ["itsy2026"], []),
]



def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def main():
    sources = {x["id"]: x for x in json.loads((LIT / "sources.json").read_text())}
    claims = []
    for number, (claim, anchor, kind, keys, artifacts) in enumerate(CLAIMS, 1):
        claims.append({"id": f"C{number:03d}", "claim": claim, "manuscript_anchor": anchor,
                       "evidence_class": kind,
                       "sources": [{"id": k, "inspected": sources[k]["inspected"],
                                    "limits": sources[k]["limits"]} for k in keys],
                       "artifacts": [{"path": p, "sha256": hashlib.sha256((ROOT/p).read_bytes()).hexdigest()} for p in artifacts],
                       "review": "Author mapping, not independent verification; source-specific restrictions remain applicable."})
    # Dependency recommendations are individually attributable, not just one census claim.
    for row in json.loads((LIT / "software-assessment.json").read_text()):
        key = "sw_" + row["id"]
        claims.append({"id": "SW-" + row["id"], "claim": row["capabilities"] + ". " + row["decision"],
                       "manuscript_anchor": "ch:software", "evidence_class": "software_document_inspection",
                       "sources": [{"id": key, "inspected": sources[key]["inspected"], "limits": sources[key]["limits"]}],
                       "artifacts": [], "review": "Source inspection only; no package runtime benchmark."})
    save(LIT / "claims.json", claims)
    lines = ["# Material claim register", "", "Claims distinguish inherited results, author derivations, executed synthetic evidence and proposed targets. See the JSON for exact inspected source anchors and artifact hashes.", "",
             "| Claim | Manuscript anchor | Evidence class | Source keys |", "|---|---|---|---|"]
    lines += [f"| {x['id']}: {x['claim']} | {x['manuscript_anchor']} | {x['evidence_class']} | {', '.join(s['id'] for s in x['sources']) or 'Author construction; see artifacts'} |" for x in claims]
    (LIT / "claims.md").write_text("\n".join(lines)+"\n")

    # These are observed references checked now against saved primary text.
    # This does not reconstruct a fictitious chronological discovery history.
    links = [
        ("panelreview2024","callaway2021","Difference-in-differences with multiple","included","Group-time estimand"),
        ("panelreview2024","borusyak2024","Revisiting event study designs","included","Imputation alternative"),
        ("panelreview2024","rambachan2023","A more credible approach to parallel","included","Trend sensitivity"),
        ("panelreview2024","arellano1991","Some tests of specification","included","Dynamic-panel restrictions"),
        ("panelreview2024","abadie2010","Synthetic control methods","included","Synthetic-control foundation"),
        ("panelreview2024","abadie2021","Using synthetic controls","included","Feasibility and data requirements"),
        ("panelreview2024",None,"Nonlinear panel data analysis","deferred","Distributional nonlinear panel models beyond current application scope"),
        ("panelreview2024",None,"Marginal structural","deferred","Original historical article not separately acquired; archived Hernan/Robins book supports g-method derivation"),
        ("proximal2020","hernan2020","Causal Inference: What If","included","Longitudinal foundations"),
        ("bennettprox2023","bennett2021","Off-policy evaluation in infinite-horizon","included","Persistent latent-confounding comparator"),
        ("bennettprox2023","kallus2020","Double reinforcement learning for efficient","included","Observed Markov OPE comparator"),
        ("runge2020","runge2019","Detecting and","included_archived_precursor","2019 reference; actual local source is 2018 precursor, explicitly labeled"),
    ]
    snowball = []
    for origin, target, needle, disposition, reason in links:
        path = LIT / "text" / (origin + ".txt")
        lines = path.read_text().splitlines()
        hits = [(n+1, " ".join(lines[n:n+3])) for n, line in enumerate(lines) if needle.lower() in line.lower()]
        if not hits:
            raise ValueError("Unverified reference-following link: " + origin + ": " + needle)
        n, excerpt = hits[-1]
        snowball.append({"from":origin,"to":target,"direction":"backward_reference_check",
                         "evidence_path":str(path.relative_to(ROOT)),"line":n,"excerpt":excerpt,
                         "disposition":disposition,"reason":reason,"checked":"2026-10-07",
                         "scope":"Reference checked against saved full text; not a claimed chronological discovery log or exhaustive bibliography screen."})
    save(LIT / "snowball-ledger.json", {"records":snowball,
         "forward_scope":"Recent topic and exact-title searches provide bounded update checks. No comprehensive citing-article traversal was executed; this is a documented coverage limit."})
    print(json.dumps({"material_and_software_claims":len(claims),"verified_reference_links":len(snowball)}))


if __name__ == "__main__":
    main()

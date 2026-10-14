#!/usr/bin/env python3
"""Build auditable discovery and software ledgers from preserved public sources."""
from pathlib import Path
import collections
import hashlib
import json
import re
import unicodedata
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
LIT = ROOT / "docs/literature"
RAW = LIT / "raw"


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def norm(value):
    return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode().lower())


def discovery():
    receipts = [json.loads(p.read_text()) for p in sorted(RAW.glob("*.receipt.json"))]
    save(LIT / "request-ledger.json", receipts)
    searches = [r for r in receipts if r["id"].startswith(("recent_", "oa_recent_", "arxiv_", "title_", "lookup_"))]
    save(LIT / "search-ledger.json", searches)
    candidates = {}
    for r in searches:
        if r.get("status") != "saved":
            continue
        path = ROOT / r["path"]
        rows = []
        if "api.openalex.org" in r["url"]:
            payload = json.loads(path.read_text())
            for x in payload.get("results", [payload] if payload.get("title") else []):
                rows.append(dict(title=x["title"], url=x.get("doi") or x["id"], doi=x.get("doi"),
                                 year=x.get("publication_year"), cited_by_count=x.get("cited_by_count"),
                                 is_retracted=x.get("is_retracted"), index="OpenAlex", metadata=x))
        elif "api.crossref.org" in r["url"]:
            for x in json.loads(path.read_text()).get("message", {}).get("items", []):
                rows.append(dict(title=(x.get("title") or [""])[0], url=x.get("URL"), doi=x.get("DOI"),
                                 cited_by_count=x.get("is-referenced-by-count"),
                                 update_to=x.get("update-to"), relation=x.get("relation"), index="Crossref", metadata=x))
        elif path.suffix == ".xml":
            atom = {"a": "http://www.w3.org/2005/Atom"}
            for x in ET.fromstring(path.read_text()).findall("a:entry", atom):
                rows.append(dict(title=" ".join(x.findtext("a:title", default="", namespaces=atom).split()),
                                 url=x.findtext("a:id", namespaces=atom),
                                 published=x.findtext("a:published", namespaces=atom),
                                 updated=x.findtext("a:updated", namespaces=atom), index="arXiv"))
        for row in rows:
            title_key = norm(row["title"])
            if not title_key:
                continue
            entry = candidates.setdefault(title_key, {"title": row["title"], "observations": []})
            entry["observations"].append({**row, "search_id": r["id"], "source_path": r["path"], "source_sha256": r["sha256"]})
    selected = json.loads((LIT / "paper-selections.json").read_text())
    selected_titles = {norm(x["title"]): x for x in selected}
    for key, row in candidates.items():
        if key in selected_titles:
            row.update(disposition="included", citation_key=selected_titles[key]["id"], reason="Selected for a stated scientific or product-design claim; see reading notes.")
        else:
            row.update(disposition="not_selected", reason="Returned metadata not selected for this purposive proposal. No documented individual full-text rejection or quality assessment is implied; see coverage/omissions for material gaps.")
    save(LIT / "candidate-ledger.json", list(candidates.values()))
    metadata = []
    for row in selected:
        matches = candidates.get(norm(row["title"]), {}).get("observations", [])
        metadata.append({"id": row["id"], "title": row["title"], "matches": matches,
                         "scope": "Exact normalized-title matches in the retrieved search corpus only. No comprehensive Crossmark, publisher-correction or retraction-database search. Absence of a flag does not establish absence of corrections."})
    save(LIT / "metadata-audit.json", metadata)
    save(LIT / "discovery-counts.json", {"requests": len(receipts), "search_requests": len(searches),
         "search_status": dict(collections.Counter(r.get("status") for r in searches)),
         "unique_title_candidates": len(candidates), "selected_papers": len(selected),
         "exact_title_metadata_matches": sum(bool(x["matches"]) for x in metadata),
         "cutoff": "2026-10-07", "review_type": "Reproducible purposive survey, not an exhaustive systematic review"})


# Each description is an assessment of inspected documentation, not a runtime result.
ASSESSMENTS = {
 "dowhy": ("Effect workflows", "MIT", "Model, identify, estimate and refute; graphical causal mechanisms", "Wrap identification and refutation; require explicit estimand and graph version", "Refutation failure is informative; passing refutations does not verify unmeasured-confounding assumptions"),
 "econml": ("Effects and policy", "MIT", "DML, forests, heterogeneous effects and IV; panel DynamicDML", "Primary Python heterogeneous-effect adapter", "Estimator-specific exchangeability, IV and panel restrictions; preserve groups in fitting"),
 "doubleml": ("Orthogonal estimation", "BSD-3-Clause", "Orthogonal scores, cross-fitting, inference and cluster data", "Primary transparent score/inference adapter", "A supported cluster layout is not arbitrary temporal dependence"),
 "causalml": ("Uplift", "Apache-2.0", "Meta-learners, trees and uplift evaluation", "Marketing challenger", "Uplift fit and predictive ranking alone do not establish identification"),
 "grf": ("Forests", "GPL-3.0", "Honest causal, instrumental, survival and multi-arm forests", "R benchmark and optional governed adapter", "Copyleft review and dependence assumptions precede distribution"),
 "tigramite": ("Temporal discovery", "GPL-3.0", "PCMCI, PCMCI+, LPCMCI, regime and multi-dataset variants", "Primary temporal discovery research adapter", "Stationarity, graph semantics, CI-test assumptions and copyleft require explicit review"),
 "causallearn": ("Discovery", "MIT", "Constraint, score and functional discovery plus CI tests", "Primary static discovery adapter", "CPDAG/PAG endpoints cannot be silently converted to a DAG"),
 "causalnex": ("Bayesian networks", "Unverified in this audit", "PyPI package metadata available; official GitHub endpoint unavailable", "Defer new dependency", "404/rate-limited access does not establish archive status or current support"),
 "causica": ("Neural causal models", "MIT", "DECI joint graph and additive-noise structural-model inference", "Research comparator", "Joint discovery/estimation does not remove structural assumptions"),
 "gcastle": ("Discovery", "Apache-2.0", "Causal discovery toolbox within trustworthyAI monorepo", "Research comparator", "Monorepo activity is not evidence of submodule maintenance"),
 "dagma": ("Differentiable discovery", "Apache-2.0", "Linear/nonlinear DAG search with log-determinant acyclicity", "Small benchmark comparator", "Nonconvex optimization, causal sufficiency and functional assumptions remain"),
 "notears": ("Differentiable discovery", "Apache-2.0", "Continuous optimization under exact acyclicity constraint", "Reference algorithm", "Acyclicity is not causal identification; inspect numerical thresholding"),
 "tetrad": ("Discovery", "GPL-3.0", "Java causal discovery library and GUI", "Cross-language benchmark", "Deployment and licensing cost; graph semantics must survive serialization"),
 "causalimpact": ("Aggregate time series", "Apache-2.0", "Bayesian structural time-series intervention analysis", "Aggregate campaign comparator", "Untreated covariates and stable counterfactual relationship are essential"),
 "causalpy": ("Quasi-experiments", "Apache-2.0", "DiD, synthetic controls, RD, interrupted series and IV", "Bayesian challenger", "Posterior uncertainty is conditional on design and model assumptions"),
 "linearmodels": ("Econometrics", "NCSA", "Panel, IV, system regression and covariance estimators", "Econometric baseline adapter", "Do not infer dynamic-panel GMM support from the panel-regression label"),
 "pyfixest": ("Fixed effects and DiD", "MIT", "High-dimensional fixed effects, IV, event studies and robust covariance", "Primary Python panel adapter", "Fast TWFE remains inappropriate for some heterogeneous staggered effects"),
 "fixest": ("Fixed effects and IV", "GPL-3", "Multiway fixed effects, IV, GLM and inference", "R reference adapter", "GPL review; specify the estimand before the regression formula"),
 "did": ("Staggered DiD", "GPL-3", "Group-time ATT with att_gt and aggregation", "R reference for modern DiD", "No anticipation, group-specific parallel trends and comparison support"),
 "honestdid": ("DiD sensitivity", "MIT", "Robust confidence sets under restricted trend violations", "Sensitivity adapter", "Sensitivity restriction is substantive, not learned truth"),
 "synthdid": ("Synthetic DiD", "BSD-3-Clause", "Synthetic difference-in-differences estimator", "Optional comparator", "Documented block treatment/simultaneous adoption and beta API"),
 "gsynth": ("Interactive fixed effects", "MIT", "Counterfactual imputation using interactive fixed effects", "Optional factor-model comparator", "Latent-factor extrapolation and support require validation"),
 "d3rlpy": ("Offline RL", "MIT", "Offline/online RL and distributed training", "Policy challenger after evaluation design", "Logged support and causal information set are separate from learner capability"),
 "scope_rl": ("Policy evaluation", "Apache-2.0", "OPE, policy selection and distributional evaluation", "OPE comparator", "Snapshot last push in 2024; no generic hidden-confounding guarantee"),
 "obp": ("Bandit evaluation", "Apache-2.0", "Bandit OPE/learning and logged bandit data tools", "One-step policy comparator", "Contextual bandits do not represent multi-period banking carryover"),
 "pomdp_py": ("POMDP planning", "MIT", "POMDP modeling, belief updating, planning and simulation", "Small reference planner", "Planning interface is not a causal parameter estimator"),
 "pomdps": ("POMDP planning", "MIT", "Julia model interface, tools, solvers and simulators", "Julia reference planner", "Solver ecosystem versions/licenses must be pinned separately"),
 "pymc": ("Probabilistic modeling", "Apache-2.0", "MCMC and variational Bayesian modeling", "Hierarchical-model comparator", "Convergence and posterior fit do not identify interventions"),
 "numpyro": ("Probabilistic modeling", "Apache-2.0", "JAX probabilistic programming and HMC", "Accelerated inference adapter candidate", "Discrete states often need marginalization; hardware speed unmeasured here"),
 "dynamax": ("State-space inference", "MIT", "JAX state-space filtering and parameter learning", "First latent-dynamics comparator", "Statistical state models need separate controlled causal identification"),
 "duckdb": ("Local analytical data", "MIT", "Embedded SQL analytics with window/nested queries", "Default local reference execution", "Measure spill, memory and point-in-time correctness on bank workloads"),
 "polars": ("DataFrames", "MIT", "Lazy/streaming analytical DataFrames; optional GPU", "Optional columnar adapter", "Capability does not establish distributed causal estimation"),
 "ray": ("Distributed execution", "Apache-2.0", "Distributed task execution and ML tools", "Add only when single-node profiling warrants", "Fault recovery, deterministic folds and aggregation are product responsibilities"),
 "datahub": ("Catalog", "Apache-2.0", "Metadata graph, ownership, column lineage and discovery", "Integrate the bank's existing catalog", "Semantic context and lineage are not causal knowledge"),
 "openmetadata": ("Catalog", "Apache-2.0", "Metadata, data quality, lineage, ownership and contracts", "Alternative catalog integration", "Avoid operating a duplicate enterprise catalog"),
 "openlineage": ("Execution lineage", "Apache-2.0", "Open standard for runtime job/dataset lineage", "Adopt run and dataset lineage events", "Add causal estimands and assumptions as explicit custom facets"),
 "feast": ("Feature serving", "Apache-2.0", "Offline/online feature access and point-in-time retrieval", "Integrate existing feature store", "Event-time joins must additionally enforce actual availability time"),
 "splink": ("Entity linkage", "MIT", "Probabilistic record linkage and match diagnostics", "Optional entity-resolution adapter", "Propagate uncertain links; false merges can induce causal bias"),
 "pandera": ("Data validation", "MIT", "Typed dataframe validation across engines", "Contract-validation adapter", "Schema validity does not establish causal semantics"),
 "lmtp": ("Longitudinal effects", "AGPL-3.0", "Longitudinal modified treatment policies, TMLE and sequential DR; competing risks", "Qualified R longitudinal comparator", "DESCRIPTION and license text specify AGPL-3, despite GPL-3 README badge; support and causal restrictions remain"),
 "ltmle": ("Longitudinal effects", "GPL-2", "Longitudinal TMLE of treatment/censoring-specific means and marginal structural models", "R reference implementation", "Censoring, intervention support and chronological node semantics need explicit checks"),
 "gformula": ("Longitudinal effects", "GPL-3 (DESCRIPTION)", "Parametric g-formula with time-varying treatments, failure times and competing events", "R g-computation comparator", "Model specification and intervention semantics are substantive; full license text not separately retrieved"),
 "zepid": ("Epidemiologic causal methods", "MIT", "IPTW/IPCW, AIPW, g-formula, TMLE and transportability tools", "Python g-method reference comparator", "Observed last push May 2023; qualify dependency compatibility and exact longitudinal method scope"),
 "pydynpd": ("Dynamic panels", "MIT", "Difference/system GMM, corrected two-step errors, AR and Hansen diagnostics, collapsed instruments", "Dynamic-panel GMM comparator", "Moment restrictions and instrument proliferation are scientific choices; package model search cannot validate them"),
}


def software():
    repos = json.loads((LIT / "software-candidates.json").read_text())
    matrix, records = [], []
    for key, repo in repos.items():
        p = RAW / ("repo_" + key + ("_verified" if key == "ltmle" else "") + ".json")
        metadata = json.loads(p.read_text()) if p.exists() else {}
        paths = sorted({p for p in RAW.iterdir() if not p.name.endswith(".receipt.json") and
                        any(p.stem == prefix + key for prefix in ["repo_", "head_", "readme_", "raw_readme_", "license_", "raw_license_", "license_detail_", "description_", "pypi_"])})
        aliases = {"causallearn": "causal_learn"}
        if key in aliases and (RAW / ("pypi_"+aliases[key]+".json")).exists():
            paths.append(RAW / ("pypi_"+aliases[key]+".json"))
        extra = {"dowhy":"api_dowhy.txt", "econml":"api_econml_dynamic.txt", "doubleml":"api_doubleml_cluster.txt", "tigramite":"api_tigramite.txt", "feast":"api_feast.txt", "gcastle":"readme_gcastle_module.md", "pomdp_py":"readme_pomdp_py_rst.txt"}
        if key in extra and (RAW / extra[key]).exists():
            paths.append(RAW / extra[key])
        if key == "ltmle":
            paths += [p for p in RAW.iterdir() if "ltmle_" in p.stem and not p.name.endswith(".receipt.json")]
        artifacts = [{"path": str(p.relative_to(ROOT)), "sha256": digest(p), "bytes": p.stat().st_size} for p in paths]
        package = next((json.loads(p.read_text()) for p in paths if p.name.startswith("pypi_")), {})
        version = package.get("info", {}).get("version")
        release_files = package.get("releases", {}).get(version, []) if version else []
        release_date = min((x.get("upload_time_iso_8601", "") for x in release_files), default=None)
        version_source = "PyPI observed version" if version else None
        if not version:
            description = next((p for p in paths if p.stem == "description_"+key+"_verified"), None)
            description = description or next((p for p in paths if p.stem == "description_"+key), None)
            if description:
                parsed = dict(re.findall(r"(?m)^([A-Za-z/]+):\s*(.+)$", description.read_text()))
                version = parsed.get("Version")
                release_date = parsed.get("Date/Publication")
                version_source = str(description.relative_to(ROOT))+"; repository declaration, not proof of latest published release"
        head = RAW / ("head_"+key+".json")
        head_sha = json.loads(head.read_text()).get("sha") if head.exists() else None
        category, license_name, capabilities, decision, limitation = ASSESSMENTS[key]
        row = {"id":key,"repository":repo,"url":"https://github.com/"+repo,"category":category,
               "observed_at":"2026-10-07","archived":metadata.get("archived"),
               "last_push":metadata.get("pushed_at"),"default_branch":metadata.get("default_branch"),
               "head_sha":head_sha,"license":license_name,"package_version":version,"package_release_date":release_date,
               "package_version_source":version_source,
               "capabilities":capabilities,"decision":decision,"limitation":limitation,
               "inspection":"Primary README/license/package or repository metadata; selected API source where saved. No runtime package benchmark.",
               "pin_limit":"Content hashes pin actual saved artifacts. Retrieved HEAD, if present, is a separate observation; mutable-branch files are not asserted to belong to that commit.",
               "artifacts":artifacts}
        target = LIT / "software" / (key + ".json")
        save(target,row)
        matrix.append(row)
        records.append({"id":"sw_"+key,"title":repo+": software documentation and source snapshot",
             "authors":"{{"+repo.split('/')[0]+" contributors}}","year":2026,"kind":"software",
             "url":row["url"],"local_path":str(target.relative_to(ROOT)),"sha256":digest(target),
             "version_status":"Snapshot 7 October 2026; content hashes preserved; runtime untested",
             "inspected":[a["path"] for a in artifacts],"claims":[capabilities,"Observed license: "+license_name,decision],
             "limits":limitation+". "+row["pin_limit"],"accessed":"2026-10-07"})
    save(LIT / "software-assessment.json",matrix)
    save(LIT / "software-sources.json",records)
    lines=["# Open-source assessment", "", "Observed 7 October 2026. Source inspection, not runtime qualification. Full hashes, package versions and limitations are in `software-assessment.json`.", "", "| Project | Role | License observed | Last repository push | Recommendation and boundary |", "|---|---|---|---|---|"]
    for x in matrix:
        lines.append(f"| [{x['repository']}]({x['url']}) | {x['capabilities']} | {x['license']} | {(x['last_push'] or 'unavailable')[:10]} | {x['decision']}. {x['limitation']} |")
    (LIT / "software-assessment.md").write_text("\n".join(lines)+"\n")


if __name__ == "__main__":
    discovery()
    software()
    print("Discovery, metadata and software ledgers rebuilt.")

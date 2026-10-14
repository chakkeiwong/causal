#!/usr/bin/env python3
"""Integrate the scientific completion claims with the preserved source map."""
import json
import hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]


def main():
    runtime=json.loads((ROOT/"docs/reviews/interface-qualification.json").read_text())["runtime"]
    other_path=ROOT/"docs/literature/other-sources.json"; other={s["id"]:s for s in json.loads(other_path.read_text())}
    runtime_keys=[]
    for row in runtime:
        name=row["distribution"]; key="runtime_"+name.replace("-","_"); runtime_keys.append(key)
        path=ROOT/"docs/literature/runtime"/(name+"-api.txt")
        anchors={"duckdb":"lines 1--4: local/in-memory connection and read-only flag; SQL revision behavior is established separately by the executed probe",
                 "polars":"lines 2--24: order-preserving filter and false/null exclusion",
                 "scikit-learn":"lines 1--36: coordinate-descent fitting, array shape and rescaled sample weights; objective normalization separately checked against soft threshold",
                 "scipy":"lines 1--65: scalar objective, bounded solver option and combined value/gradient callable",
                 "numpy":"lines 2--46: square full-rank solve, singular error and vector RHS semantics"}
        other[key]={"id":key,"title":name+" "+row["version"]+": installed API documentation and operation receipt",
                    "authors":"{{"+name+" contributors}}","year":2026,"kind":"documentation",
                    "url":{"duckdb":"https://duckdb.org/docs/","polars":"https://docs.pola.rs/","scikit-learn":"https://scikit-learn.org/stable/","scipy":"https://docs.scipy.org/doc/scipy/","numpy":"https://numpy.org/doc/"}[name],
                    "local_path":str(path.relative_to(ROOT)),"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
                    "version_status":"Installed version "+row["version"]+" observed 8 October 2026; release date at the literature cutoff not inferred",
                    "accessed":"2026-10-08","inspected":[anchors[name]],"claims":[anchors[name]],
                    "limits":"Installed operation/host qualification only; see interface-qualification.json for exact probes, metadata/license/source copies and their hashes. Does not qualify all package operations or bank use.",
                    "artifacts":row["artifacts"],"qualification_record":"docs/reviews/interface-qualification.json"}
    other_path.write_text(json.dumps(list(other.values()),ensure_ascii=False,indent=2)+"\n")
    path=ROOT/"docs/literature/reconstruction-claims.json"; claims=json.loads(path.read_text())
    additions=[
      ("S-C01","s4:response-construction","Fixed stable Gaussian products admit a joint quadratic-form CLT; Bartlett consistency and PSD, joint bands, weak-IV inversion and proxy-VAR derivatives are derived under their distinct assumptions.",["stock2018","newey1986","inoue2023"],["docs/reviews/scientific-completion-checks.json","src/causalbank/responses.py"]),
      ("S-C02","s4:dependent-learning","Dependent orthogonal IV uses a coupling gap, explicit product and accumulated-HAC error conditions; sparse and factor alternatives impose different information restrictions. Recent reverse-split theory is not inherited without its stability assumptions.",["dml2018","babii2020","ciganovic2026"],["docs/studies/a-extension-results.json"]),
      ("S-C03","s4:date-panel","Fixed bank-weighted date scores determine macro information; short-bandwidth date HAC still undercovers in the recorded persistent panel experiment.",[],["docs/studies/a-panel-results.json"]),
      ("S-C04","s4:response-results","Integrated change-to-level mapping retains cross-horizon covariance; direct/proxy, bandwidth, weak/invalid instrument and sparse/factor comparisons retain all adverse results.",["lpaug2020","johansen2017"],["docs/studies/a-results.json","docs/studies/a-extension-results.json","docs/derivations/scientific_response_results.tex"]),
      ("S-C05","s4:unknown-emission","A binary randomized controlled experiment identifies unknown emissions, transitions and rewards through three-view spectral algebra, with one common label permutation; it is distinct from generic observational POMDP identification.",["spectral2016"],["docs/reviews/scientific-completion-checks.json"]),
      ("S-C06","s4:latent-inference","An identified finite-alphabet likelihood has a regular iid-trajectory MLE/value expansion under interior nonsingular information and a consistent approximate global maximizer; EM starts alone do not prove these conditions.",[],["src/causalbank/controlled.py","docs/studies/b-latent-results.json"]),
      ("S-C07","s4:pomdp-error","A path-law contraction bounds value error under the same observed-history policy in two partially observed environments; updating the policy/filter with each refit violates its premise.",[],[]),
      ("S-C08","s4:fitted-history","Whole-trajectory nuisance fitting and finite-dimensional backward targeting support the fixed-policy score expansion; stochastic/deterministic and observed/latent alternatives retain their distinct information and support restrictions.",[],["docs/studies/b-history-results.json","docs/studies/b-latent-results.json"]),
      ("S-C09","s4:graph-confidence","A simultaneous Gaussian covariance region contains the true covariance and hence conservatively mapped true graph/effect under a sufficient linear class; a hidden-confounder case invalidates the causal conclusion despite observed-law coverage.",[],["src/causalbank/discovery_sets.py","docs/studies/c-results.json","docs/reviews/scientific-completion-checks.json"]),
      ("S-C10","s4:temporal-graph-confidence","A fixed-dimensional structural VAR1 score CLT yields a joint coefficient box and fixed-horizon response image; omitted lags invalidate it and general PCMCI/PAG outputs need separate inference.",["runge2020","gerhardus2020"],["docs/studies/c-temporal-results.json","src/causalbank/temporal_discovery.py"]),
      ("S-C11","s4:organization-algorithm","Finite observation candidates obey supplied constraints; material ambiguity causes abstention. Correctness is conditional on grammar inclusion and valid constraints, not hint-score calibration.",[],["src/causalbank/organization.py","docs/studies/d-results.json","docs/studies/observation-oracle.json"]),
      ("S-C12","s4:scientific-language","The versioned finite-kernel semantics, model/sampling lowering and vector/curve/set results check declared compatibility and preserve uncertainty meaning under permitted fixed unit transforms.",runtime_keys,["src/causalbank/scientific.py","contracts/scientific/v04-request.schema.json","contracts/scientific/v04-result.schema.json","docs/reviews/interface-qualification.json","docs/reviews/standalone-qualification.json"]),
      ("S-C13","s4:sibling-mappings","Read-only source snapshots support exact sibling field/clock/quote mappings; local adapter executions do not establish runtime adoption by any sibling repository.",[],["src/causalbank/adapters.py","docs/reviews/interface-qualification.json","docs/reviews/standalone-qualification.json"]),
      ("S-C14","s4:workflow-results","Complete fresh-process synthetic workflows include raw reconstruction, fitting, uncertainty and reporting. Latent bootstrap fitting and temporal reconstruction have different cost profiles; timings do not establish bank labor savings.",[],["docs/studies/workflow-results.json","docs/studies/workflow-summary.json","docs/derivations/scientific_workflow_results.tex"])]
    existing={c["id"]:c for c in claims}
    for key,anchor,claim,sources,artifacts in additions:
        existing[key]={"id":key,"manuscript_anchor":anchor,"claim":claim,"sources":sources,"artifacts":artifacts,
                       "evidence_class":"project_construction_with_primary_source_comparison_and_scoped_executable_evidence"}
    path.write_text(json.dumps(list(existing.values()),ensure_ascii=False,indent=2)+"\n")
    path=ROOT/"docs/literature/source-question-matrix.json"; matrix=json.loads(path.read_text()); notes=json.loads((ROOT/"docs/literature/reading-notes.json").read_text())
    by_domain={6:["babii2020","ciganovic2026"],10:["spectral2016"],11:["newey1986","lpaug2020","inoue2023","johansen2017"]}
    anchors={6:"s4:dependent-learning",8:"s4:fitted-history",9:"s4:unknown-emission",10:"s4:latent-inference; s4:pomdp-error",11:"s4:response-construction; s4:date-panel",12:"s4:graph-confidence; s4:temporal-graph-confidence",13:"s4:organization-algorithm",14:"s4:scientific-language; s4:sibling-mappings; s4:workflow-results"}
    remaining={
        3:"Recursive ID/IDC and failure witnesses are worked through. Finite discrete kernel product, marginalization and intervention semantics now have local executed checks. General ID/PAG and path-specific engines, including executable hedge validation, remain implementation work.",
        6:"A bounded exponentially mixing IV construction now supplies explicit separation, nuisance-product and accumulated-HAC rates; sparse and factor alternatives are compared on the same target. General dependent CATE bands, increasing-horizon rates and arbitrary learned-policy inference remain unsupported.",
        8:"Whole-trajectory nuisance fitting, sequential augmentation and backward targeting now have a finite-state construction and repeated-sample comparisons. Neural g-computation and continuous-time alternatives retain their own restrictions. Original g-formula/MSM correction texts remain unavailable; generic long-horizon or common-shock trajectory inference is not inherited from the iid construction.",
        9:"Known-emission marked-kernel recovery and an unknown-emission binary randomized controlled identification construction now match their likelihood/value models. General nonlinear private-logger identification and latent bridge completeness remain separate source-specific assumptions.",
        10:"The binary unknown-emission randomized model now has constructive identification, scaled likelihood fitting, observed-score information, fixed-policy value uncertainty and a path-law value-error bound. General nonlinear controlled identification, weak full-information inference and strategic equilibrium remain open extensions. Original Rust/Hotz-Miller papers are not cited.",
        11:"Fixed Gaussian response and bounded mixing learning constructions, weak-IV inversion, date-weighted panels and integrated change-to-level responses are derived and executed. Persistent finite-sample undercoverage remains visible. Uniform near-unit/increasing-horizon inference, heterogeneous shock transmission and whole-market equilibrium require additional restrictions.",
        12:"Small sufficient Gaussian DAGs now have covariance-region graph/effect outer sets; a separate structural VAR1 class has temporal coefficient/response bands. Hidden confounding and omitted lags invalidate the corresponding conclusions. General FCI/PAG runtime inference, informative clocks and large graph confidence remain unqualified; pinned endpoint source inspection is not their runtime acceptance.",
        13:"The 32-candidate observation grammar now executes key/clock/revision/aggregation/unit constraints, preserves materially different views and abstains. Oracle and downstream-effect comparisons cover resolved and ambiguous records. Correctness is conditional on grammar inclusion and valid supplied constraints; no automatic MAR, economic-assumption or linkage-posterior validation is claimed.",
        14:"The historical 44-project source qualification keeps runtime_status=not_run. Separate installed-version receipts now qualify selected NumPy, SciPy, scikit-learn, DuckDB and Polars operations, finite-kernel/result semantics, six standalone requests and local mappings from four inspected sibling contracts. Complete synthetic workflow timings supplement the old reducer benchmark. General services/workspaces, accepted sibling adoption and bank qualification remain construction work."
    }
    for row in matrix["domains"]:
        for key in by_domain.get(row["id"],[]):
            if not any(s["id"]==key for s in row["sources"]): row["sources"].append({"id":key,"anchors":"; ".join(notes[key]["inspected"]),"inspection":"primary_technical_text_read_in_scientific_completion"})
        if row["id"] in anchors and anchors[row["id"]] not in row["draft"]: row["draft"]+="; "+anchors[row["id"]]
        if row["id"] in remaining: row["remaining"]=remaining[row["id"]]
    path.write_text(json.dumps(matrix,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"claims":len(existing),"domains":len(matrix["domains"])}))


if __name__=="__main__": main()

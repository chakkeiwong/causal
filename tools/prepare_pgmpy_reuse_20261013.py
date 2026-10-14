#!/usr/bin/env python3
"""Bind pinned pgmpy source and select one limited future integration path."""
import hashlib
import json
from pathlib import Path
import tomllib
import build_integrated_monograph_v12 as shared
import master_control as core

ROOT=core.ROOT
RAW=ROOT/'docs/literature/raw'
BASE=ROOT/'docs/program/execution/2026-10-13/pgmpy-reuse'
ref=shared.ref

def save(name,value):
    p=BASE/name;assert not p.exists(),f'Preserve {p}';core.write(p,value)

def main():
    selection=json.loads((BASE/'source-selection.json').read_text());pin=selection['pin']
    tree=json.loads((RAW/'v12_sw2_tree_pgmpy.json').read_text());assert tree['sha']==pin and not tree['truncated']
    blobs={x['path']:x for x in tree['tree']}
    files={**{'exec13_pgmpy_reuse_'+k:v for k,v in selection['source_files'].items()},
        'exec13_pgmpy_reuse_roles':'pgmpy/base/_mixin_roles.py',
        'v12_sw2_source_pgmpy_adjustment':'pgmpy/identification/adjustment.py',
        'v12_exec13_pydisc_pgmpy_source_1':'pgmpy/causal_discovery/PC.py',
        'v12_exec13_pydisc_pgmpy_source_2':'pgmpy/causal_discovery/GES.py',
        'v12_sw2_metadata_pgmpy_1':'pyproject.toml','v12_sw2_metadata_pgmpy_2':'LICENSE',
        'v12_sw2_source_pgmpy_identify':'docs/guides/causal_identification.md',
        'v12_sw2_source_pgmpy_estimate':'docs/guides/causal_estimation.md',
        'v12_sw2_source_pgmpy_llmpairwise':'pgmpy/causal_discovery/LLMPairwise.py'}
    anchors={
        'pgmpy/base/DAG.py':'get_parents lines453–479; minimal_dseparator lines799–861; graph construction and latent roles',
        'pgmpy/base/PDAG.py':'typed directed/undirected sets lines13–58; to_cpdag/to_dag lines225–302, warning plus arbitrary fallback',
        'pgmpy/identification/_base.py':'Graphical identify/validate lines31–89; only supported-type and causal-role preflight',
        'pgmpy/base/_mixin_roles.py':'get_role/with_role lines8–113; is_valid_causal_structure lines154–171 checks presence of exposure/outcome roles',
        'pgmpy/tests/test_identification/test_adjustment.py':'test_get_minimal_adjustment_set; M-graph/latent cases; game5 alternatives',
        'pgmpy/causal_discovery/_base.py':'fit lines110–135; skeleton construction and max_cond_vars stopping lines305–525',
        'pgmpy/causal_discovery/ExpertKnowledge.py':'ExpertKnowledge source: required/forbidden/search-space constraints and application',
        'pgmpy/identification/adjustment.py':'variants lines51–60; singleton minimal lines129–151; unimplemented minimal_variance lines153–156; all lines160–177; parent-only validation lines198–218',
        'pgmpy/causal_discovery/PC.py':'parameters lines31–85; assumptions tags; fit and pdag/dag selection lines187–258',
        'pgmpy/causal_discovery/GES.py':'parameters/defaults and forward/backward/turning phases; selected DAG output is optional',
        'pyproject.toml':'project version 1.1.2, Python bounds, twelve mandatory dependencies and separate optional extras',
        'LICENSE':'MIT permission, notice condition and warranty disclaimer',
        'docs/guides/causal_identification.md':'Advertised minimal, variance-optimal and all adjustment routes; identify/validate examples',
        'docs/guides/causal_estimation.md':'Separate identification prerequisite and graph/prediction API leads; guide not execution evidence',
        'pgmpy/causal_discovery/LLMPairwise.py':'Description states values unused; optional LiteLLM and prompt/provider call path'}
    records=[]
    for stem,upstream in files.items():
        p=RAW/(stem+'.txt');data=p.read_bytes();receipt=p.with_suffix('.receipt.json');r=json.loads(receipt.read_text())
        sha=hashlib.sha256(data).hexdigest();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert r['status']=='saved' and r['sha256']==sha and blob==blobs[upstream]['sha'],stem
        records.append({'upstream_path':upstream,'source_identity':r['url'],'accessed_utc':r['accessed_utc'],'git_blob_sha1':blob,'local_copy':ref(p,anchors[upstream]),'receipt':ref(receipt,'Bounded primary-source acquisition'),'inspected_anchors':[anchors[upstream]]})
    meta=tomllib.loads((RAW/'v12_sw2_metadata_pgmpy_1.txt').read_text())['project'];assert meta['version']=='1.1.2' and len(meta['dependencies'])==12
    commit=json.loads((RAW/'v12_sw_cutoff_commit_pgmpy.json').read_text())[0];assert commit['sha']==pin
    evidence=[ref(RAW/p,a) for p,a in [('v12_sw2_tree_pgmpy.json','Untruncated selected Git tree'),('v12_sw_cutoff_commit_pgmpy.json','Cutoff query commit identity and timestamp; no maintenance-quality conclusion'),('v12_sw_repo_pgmpy.json','Repository identity and late snapshot')]]
    findings=[
        {'id':'IMPLEMENTATION-NOT-GUIDE','finding':'minimal_variance is advertised but the pinned _identify branch raises NotImplementedError; exclude this operation at this pin.'},
        {'id':'DESCENDANT-VALIDATION','finding':'BaseGraphicalIdentification validates type and role presence; role validation does not check causal admissibility. Adjustment._validate checks parents of exposures. With root X in X->M->Y it returns all(empty)=True even when adjustment={M}. Add independent descendant and strict backdoor checks for the proposed total-effect path. This is a static source trace, not an installed-engine result.'},
        {'id':'MINIMAL-NOT-MINIMUM','finding':'DAG.minimal_dseparator greedily deletes dispensable variables. Do not promise globally minimum cardinality or variance based on the word minimal or the docstring smallest. Multiple inclusion-minimal sets can have different sizes.'},
        {'id':'ONE-DAG-IS-NOT-CLASS','finding':'PC pdag/cpdag return the same partially directed object; dag calls to_dag. PDAG.to_dag may warn and orient arbitrarily if consistent extension fails. to_cpdag calls this conversion. Never use conversion alone to certify valid equivalence-class semantics.'},
        {'id':'ALL-IS-BOUNDED','finding':'The all branch enumerates subsets of an ancestor candidate set after causal-path/latent exclusions. Its completeness domain differs from every observed-variable subset; it is exponential and does not license unrestricted targets.'},
        {'id':'LLM-SEPARATION','finding':'LLMPairwise uses variable descriptions, not data values, and has an optional provider path. It is a distinct information source from CI-based PC and remains outside the selected non-network graph service.'}]
    primary={'pin':pin,'declared_version':meta['version'],'commit_utc':commit['commit']['committer']['date'],'cutoff':'2026-10-07','records':records,'identity_evidence':evidence,'dependency_declarations':{'requires_python':meta['requires-python'],'mandatory':meta['dependencies'],'optional':meta['optional-dependencies']},'license':'MIT; preserve copyright and permission notices; dependency licenses are separate','maintenance':{'observed':'Selected commit 2026-10-05 and pinned tests/refactored graph APIs; documentation-code divergence observed','unmeasured':'No upstream CI run, response-time study, release support promise, complete dependency resolution or current issue census.'},'findings':findings,'claim_limits':['Static primary-source review; no pgmpy installation or execution.','Original source references listed by the package are not newly cited scholarly papers.']}
    save('primary-review.json',primary)
    assert json.loads((BASE/'oracle-results.json').read_text())['status']=='pass'
    contract={'version':'1.0-proposal-design','status':'selected_for_future_local_implementation_not_implemented','engine':{'repository':'https://github.com/pgmpy/pgmpy','revision':pin,'declared_version':'1.1.2','license':'MIT'},'operation':'known_observed_DAG_adjustment_candidate','initial_cap':{'max_nodes':12,'max_exposures':1,'max_outcomes':1,'rationale':'Conservative proposed wrapper budget, not profiled engine capacity or statistical guarantee.'},'admission':['Unique nonempty string node identifiers; exact typed directed edges and explicit node list including isolates.','Acyclic finite graph; distinct observed singleton exposure and outcome; no latent, bidirected, selection, undirected or ambiguous marks.','No post-action adjustment variable; reject descendants of exposure and overlap with exposure/outcome.','Graph is a supplied scientific assumption with provenance; passing graph checks does not establish graph truth.','Initial operation requests Adjustment(variant=minimal). Explicit whitelist excludes all, minimal_variance, discovery, learned-DAG selection, effect estimation and live model operations.'],'call':'Construct a fresh DAG with explicit roles, invoke Adjustment(variant=minimal).identify; retain original graph and exact node-role map.','response':['success=false -> no_adjustment_found_by_selected_method; never global nonidentifiability.','success=true -> require a graph and observed adjustment set, verify unchanged nodes/edges/exposure/outcome roles, then independently validate descendant exclusion and d-separation in graph with outgoing exposure edges removed.','Any exception, source warning, invalid type, timeout, nonfinite metadata or failed independent validation -> diagnostic refusal/unavailable; never empty set or zero effect.','Empty adjustment set is a successful scientific result only when separately verified, not the same as failed/null result.','Output is a verified candidate adjustment set relative to the supplied graph; no numerical effect, confidence interval or actual causal truth.'],'conversion':{'primary':'Named directed edges and node-role records; preserve node order and isolates.','forbidden':'No PDAG.to_dag/to_cpdag coercion, binary-matrix direction guessing or automatic latent deletion.','transport':'Proposed library result, bounded JSON CLI and MCP result share target/graph identities and dispositions; no implemented endpoint claimed.'},'behavioral_oracle':ref(BASE/'oracle-results.json','Two independent d-separation definitions over all543 four-node DAGs; exact mediator and extension counterexamples'),'oracle_code':ref(ROOT/'tools/pgmpy_reuse_oracles_20261013.py','Project-only finite graph and SEM checks'),'minimum_future_fixtures':['Observed confounder requires Z; mediated chain uses empty set and rejects M; collider adjustment rejected.','Multiple inclusion-minimal sets accepted by property rather than requiring one arbitrary order; minimum-size promise forbidden.','Disconnected graphs, isolates, Unicode string names and every node permutation preserve semantic edges.','Latent/mixed/partial graph, duplicate role, cyclic input and unsupported variant refused before engine call.','Engine warning, no-method result, exception, timeout and changed graph after return retained separately.','Package/dependency lock and source revision hash recorded; upstream tests and actual CLI/library roundtrip required before runtime claim.'],'owner_obligations':['Research owner specifies assumed graph, target, clock and admissible controls.','Adapter owner enforces contracts, notice retention, dependency license/build review and isolated compatible environment.','Reviewer compares actual outputs against the independent oracle before runtime acceptance; author design selection is not independent certification.'],'revisit_trigger':'A future pinned upgrade or new graph/method path requires source, oracle, dependency and conversion review; runtime claims additionally require executed fixtures.','integration_allowed_scope':'This restricted graph-candidate prototype implementation only; no blanket pgmpy adoption.'}
    save('adapter-contract.json',contract)
    audit={'cutoff':'2026-10-07','project_date':'2026-10-13','sources':[
        {'integrated_citation_key':'exec13_pgmpy_reuse_primary','kind':'software_primary_source_review','title':'pgmpy pinned graph discovery and adjustment: implementation boundaries, terms and dependencies','author':'pgmpy contributors','year':2026,'source_identity':'https://github.com/pgmpy/pgmpy','version_date':f'Commit {pin}, 5 October 2026; pyproject 1.1.2; sources acquired 11–13 October 2026','local_copy':ref(BASE/'primary-review.json','Fifteen tree-verified source records and six reviewed boundaries'),'records':records,'identity_records':evidence,'inspected_anchors':[f['id'] for f in findings],'supported_claims':[f['finding'] for f in findings]+['MIT terms, declared Python bounds and twelve mandatory dependencies; selected tests exist but were not run.'],'limits':['No engine performance, runtime qualification or whole-package validation.']},
        {'integrated_citation_key':'exec13_pgmpy_reuse_oracle','kind':'project_derivation_and_exact_reference','title':'Independent graph and mediated-servicing references for a proposed pgmpy boundary','author':'Causal banking research project','year':2026,'source_identity':'Project-authored reference with no upstream code execution','version_date':'13 October 2026','local_records':[ref(BASE/'oracle-results.json','543 DAGs,26064 d-separation comparisons,mediator slope and nonextendible four-cycle'),ref(ROOT/'tools/pgmpy_reuse_oracles_20261013.py','Two separately implemented graph criteria and exact rational SEM'),ref(BASE/'adapter-contract.json','Restricted proposed graph-candidate integration and refusal contract')],'inspected_anchors':['moral_separated versus path_separated','mediator_boundary','minimal_versus_minimum','nonextendible_PDAG','initial path and future fixtures'],'supported_claims':['Exact graph criteria agree across26064 cases; the finite scope is explicit.','Generated mediated total effect six differs from mediator-adjusted coefficient zero.','A chordless four-cycle has14 acyclic orientations and no no-new-collider extension.','Selected prototype integration requires independent candidate validation and remains unimplemented.'],'limits':['No pgmpy execution, empirical graph recovery, finite-sample confidence or bank ROI.']}],'scholarly_originals_added':0,'visual_acceptance':False}
    shared.verify_refs(audit);save('source-audit.json',audit)
    save('decision-review.json',{'status':'pass','reviewer':{'name':'Codex author/coordinator','kind':'author'},'selected':'integrate_restricted_known_observed_DAG_candidate_path','integration_allowed':True,'integration_scope':contract['integration_allowed_scope'],'engine_executed':False,'findings':[f['id'] for f in findings],'evidence':[ref(BASE/p,p) for p in ['primary-review.json','oracle-results.json','adapter-contract.json','environment-inspection.json','source-audit.json']],'limitations':['Full dependency lock and actual runtime fixtures precede execution qualification, not this proposal selection.','Discovery and generalized adjustment/latent/LLM paths require separate decisions.']})
    print(json.dumps({'tree_verified_source_files':len(records),'new_audited_sources':2,'selected_path':contract['operation'],'integration_allowed':True,'engine_executed':False}))

if __name__=='__main__':main()

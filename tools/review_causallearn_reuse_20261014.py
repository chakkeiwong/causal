#!/usr/bin/env python3
"""Review exact source custody and a bounded proposed causal-learn integration."""
import ast
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import run_program as control
from discovery_journey_20261013 import ROOT, ref, write, now

BASE = ROOT / 'docs/program/execution/2026-10-14/causallearn-reuse'
OUTPUT = ROOT / 'docs/program/comprehensive-v14/work/SW.DECISION.inherited_causallearn/decision.json'
PIN = '0dacacf36390e3084704636bc3c36e82e35ee0cc'


def references():
    # Independent population covariance identities; no engine import, fit or
    # sample-dependent p-value is substituted for an oracle independence fact.
    chain = [[F(1), F(1, 2), F(1, 4)], [F(1, 2), F(1), F(1, 2)], [F(1, 4), F(1, 2), F(1)]]
    collider = [[F(1), F(1, 2), F(0)], [F(1, 2), F(1), F(1, 2)], [F(0), F(1, 2), F(1)]]
    residual = lambda c: c[0][2]-c[0][1]*c[1][2]/c[1][1]
    assert residual(chain) == 0 and residual(collider) == F(-1, 4)
    assert chain[0][2] != 0 and collider[0][2] == 0
    # An authored fixture for the endpoint contract, not upstream graph code.
    matrix = [[0, -1, 0], [1, 0, 2], [0, 1, 0]]
    names = ['A', 'B', 'Y']
    decoded = [{'left': names[i], 'right': names[j], 'left_mark': {-1:'tail',1:'arrow',2:'circle'}[matrix[i][j]],
                'right_mark': {-1:'tail',1:'arrow',2:'circle'}[matrix[j][i]]}
               for i in range(3) for j in range(i+1,3) if matrix[i][j]]
    assert decoded == [{'left': 'A', 'right': 'B', 'left_mark': 'tail', 'right_mark': 'arrow'},
                       {'left': 'B', 'right': 'Y', 'left_mark': 'circle', 'right_mark': 'arrow'}]
    reverse = [[0]*3 for _ in names]
    for edge in decoded:
        i,j=names.index(edge['left']),names.index(edge['right'])
        reverse[i][j]={'tail':-1,'arrow':1,'circle':2}[edge['left_mark']]
        reverse[j][i]={'tail':-1,'arrow':1,'circle':2}[edge['right_mark']]
    assert reverse == matrix
    return {'kind': 'exact_project_design_oracle', 'package_execution': False, 'random_draws': 0,
        'chain': {'cov_AC': str(chain[0][2]), 'cov_AC_given_B': str(residual(chain)),
                  'oracle_equivalence_class': 'A---B---Y; observational chain orientations unresolved'},
        'collider': {'cov_AC': str(collider[0][2]), 'cov_AC_given_B': str(residual(collider)),
                     'oracle_equivalence_class': 'A->B<-Y'},
        'endpoint_example': {'matrix': matrix, 'decoded': decoded, 'roundtrip': reverse},
        'fisherz_guard_examples': [{'n': 4, 'conditioning_count': 1, 'admit': False},
                                  {'n': 100, 'conditioning_count': 1, 'admit': True}],
        'limitations': ['Population references are not results from finite-sample PC/FCI.',
                       'Endpoint roundtrip does not establish PAG/CPDAG validity.',
                       'Positive Fisher-Z degrees of freedom is necessary, not sufficient for valid inference.']}


def main():
    assert not OUTPUT.exists(), 'Preserve completed decisions'
    raw = ROOT / 'docs/literature/raw'
    tree = json.loads((raw / 'v12_sw2_tree_causallearn.json').read_text())
    assert tree['sha'] == PIN and tree['truncated'] is False
    indexed = {x['path']: x for x in tree['tree']}
    sources = []
    for name, anchors, claims in [
        ('v12_sw2_metadata_causallearn_1', ['setup.py VERSION and install_requires'], ['Declared 0.1.4.8, Python >=3.7, twelve unpinned direct dependencies']),
        ('v12_sw2_metadata_causallearn_2', ['LICENSE full grant, notice and disclaimer'], ['Root MIT grant, copyright 2022 cmu-phil; preserve notice; no dependency-wide license inference']),
        ('v12_sw2_source_causallearn_pc', ['PC.py lines 20-49 and 65-140'], ['PC settings, separate missingness branch, collider-conflict handling and matrix endpoint convention']),
        ('r3g_api_causallearn', ['FCI.py lines 1061-1181'], ['FCI CI/depth/path settings, circle initialization, orientation passes, PAG flag and edge properties']),
        ('v12_exec13_pydisc_causallearn_extra_3', ['GeneralGraph.py lines 91-181'], ['Endpoint representation includes composite values that require explicit unsupported handling']),
        ('v12_exec13_pydisc_causallearn_extra_4', ['cit.py lines 192-225'], ['Fisher-Z inverse correlation, singularity error, near-one clipping and n-|S|-3 calculation'])]:
        receipt_path = raw / (name+'.receipt.json'); receipt = json.loads(receipt_path.read_text())
        local = raw/(name+'.txt'); content = local.read_bytes()
        assert receipt['status'] == 'saved' and hashlib.sha256(content).hexdigest() == receipt['sha256']
        path = receipt['url'].split(PIN+'/')[1]
        git_blob = hashlib.sha1(b'blob '+str(len(content)).encode()+b'\0'+content).hexdigest()
        assert git_blob == indexed[path]['sha']
        sources.append({'kind': 'pinned_source_or_license', 'source_identity': receipt['url'],
            'version_date': PIN+'; 2026-09-04T16:50:44Z', 'accessed_utc': receipt['accessed_utc'],
            'local_copy': ref(local, '; '.join(anchors)), 'acquisition': ref(receipt_path, 'Public source acquisition'),
            'git_blob_sha1': git_blob, 'tree_match': True, 'inspected_anchors': anchors, 'supported_claims': claims})
    setup = ast.parse((raw/'v12_sw2_metadata_causallearn_1.txt').read_text())
    call = next(x.value for x in setup.body if isinstance(x,ast.Expr) and isinstance(x.value,ast.Call))
    dependencies = ast.literal_eval(next(k.value for k in call.keywords if k.arg=='install_requires'))
    assert len(dependencies) == 12 and all(isinstance(d,str) for d in dependencies)
    primary = {'cutoff': '2026-10-07', 'reviewed_at': now(), 'pinned_revision': PIN,
        'sources': sources, 'tree': ref(raw/'v12_sw2_tree_causallearn.json', 'Complete pinned tree and source blob membership'),
        'commit': ref(raw/'v12_sw_cutoff_commit_causallearn.json', 'Pre-cutoff commit identity; not a maintenance guarantee'),
        'direct_dependency_declarations': dependencies, 'resolved_environment': False,
        'dependency_rights_inventory': 'Root license inspected; transitive distribution/license closure unresolved',
        'maintenance_evidence': {'readme': ref(ROOT/'docs/program/repair-v12/work/SW01/extracted/pinned-causallearn-README.md', 'Contribution/tests/py-tetrad/online platform references at selected revision'),
            'tests_in_tree': [p for p in ['tests/TestPC.py','tests/TestFCI.py'] if p in indexed],
            'limit': 'README activity language and test paths do not establish passing CI, support response time or maintenance cost'},
        'aliases': {'distribution': 'causal-learn', 'import_namespace': 'causallearn', 'catalog': 'inherited:causallearn',
            'separate_products': ['Tetrad and py-tetrad are separate engine/bridge paths', 'causallearn.com online agentic service is not the pinned local distribution']}}
    write(BASE/'primary-review.json',primary)
    write(BASE/'oracle-results.json',references())
    contract = {'status': 'proposal_conversion_and_failure_contract_not_implemented',
        'engine': {'commit': PIN, 'declared_version': '0.1.4.8'},
        'first_profile': 'Complete IID continuous Gaussian, causally sufficient, acyclic, faithful, no unmodeled selection: PC with Fisher-Z',
        'parameters': {'alpha':0.05,'stable':True,'uc_rule':0,'uc_priority':2,'mvpc':False,'max_k':None,
                       'background_knowledge':None,'verbose':False,'show_progress':False},
        'separate_profile': 'FCI under explicitly stated latent/selection and CI assumptions; do not inherit PC admission or temporal validity.',
        'request_preservation': ['target','population','variables and column order','intervention','horizon','units','sign_convention',
            'observation_clock','sampling','assumptions','source/data identity','method and settings','environment digest'],
        'input_checks': ['Finite two-dimensional numeric array; unique variables and exact column bijection; at least one variance-positive column per variable.',
            'Independent whole sampling units and declared CI assumptions; forbid automatic row duplication, imputation or discretization.',
            'Bound conditioning set size so n-|S|-3>0 for every Fisher-Z call; independently enforce rank/conditioning and finite p-values.',
            'Save every warning, exception, truncation and cancellation; resource exhaustion is not a valid empty graph.'],
        'endpoint_conversion': {'0':'no adjacency only when both entries are zero','-1':'tail','1':'arrow','2':'circle',
            'rule':'graph[i,j] is the mark at i on pair i,j; serialize both entries, including reverse directions and isolated nodes.',
            'composite_or_unknown':'Return unsupported endpoint encoding and preserve original matrix; never collapse composite values to a DAG.',
            'pc_bidirected':'An orientation-conflict result must not acquire FCI hidden-confounder meaning. Reject CPDAG qualification and retain conflict provenance.',
            'recognition':'Require an independent method-specific graph-class check before publishing a CPDAG/PAG assertion; syntax alone is insufficient.'},
        'failures': {'singular_correlation':'failed/unavailable with numerical diagnosis and null scientific result',
            'nan_pvalue':'failed/unavailable, never a CI pass', 'unsupported_sampling':'completed/unsupported',
            'contradicted_premise':'completed/refused','unrecognized_endpoint':'completed/unsupported with preserved raw graph',
            'out_of_budget':'failed/unavailable or cancelled; no partial graph success'},
        'uncertainty': 'alpha is per CI test, not whole-graph confidence, effect coverage, or a bank decision guarantee. Bootstrapped edge frequencies would also need a separate interpretation.',
        'downstream': 'Graph-class preservation precedes an independent identification/effect operation. Never choose one DAG or replace a circle by an arrow to satisfy that operation.',
        'oracle': ref(BASE/'oracle-results.json','Exact Gaussian CI and endpoint fixtures; no engine execution'),
        'runtime_qualification':False}
    write(BASE/'conversion-contract.json',contract)
    decision = {'operation_id':'SW.DECISION.inherited_causallearn','canonical_package':'py-why/causal-learn',
        'aliases':primary['aliases'],'pinned_revision':PIN,'version':'0.1.4.8','cutoff':'2026-10-07',
        'decision':'defer','preferred_proposal_route':'Direct integration of scoped local PC, followed by a separately reviewed FCI profile; do not port the algorithms.',
        'decision_scope':'Select an implementation candidate for the proposal; withhold executable adapter admission until the dependency lock and output/failure boundary exist.',
        'integration_allowed':False,'runtime_qualification':False,'deployment_allowed':False,
        'primary_evidence':ref(BASE/'primary-review.json','Six pinned blob matches, MIT license, dependencies, aliases and maintenance limits'),
        'conversion_failure_contract':ref(BASE/'conversion-contract.json','Concrete method, endpoints, CI preconditions and result/failure meanings'),
        'behavioral_oracle':ref(BASE/'oracle-results.json','Exact independent project references for future engine comparison'),
        'target_and_uncertainty':contract['uncertainty'],
        'reason':['A pinned MIT source route with explicit PC/FCI semantics is available and suitable for an implementation proposal.',
                  'No complete pinned executable environment or transitive rights inventory is recorded; twelve dependency declarations have no version bounds.',
                  'The current canonical runtime has no discovery dispatch; graph-class, composite-endpoint and numerical-failure handling remain proposed.',
                  'A proposal-level selection needs no bank validation, paid trial or prior empirical superiority; those are not reasons for this narrow admission deferral.'],
        'alternatives':[{'route':'Port PC/FCI','decision':'reject_for_now','reason':'No measured embedding constraint justifies duplicating orientation/test maintenance.'},
            {'route':'Expose every causal-learn algorithm','decision':'reject_for_initial_adapter','reason':'Would merge distinct assumptions, outputs and unreviewed numerical paths.'},
            {'route':'Tetrad Java or pcalg R','decision':'retain_as_separate_comparators','reason':'Each needs its own pin, engine semantics and bridge conversion; no parity assumed.'},
            {'route':'Tigramite temporal discovery','decision':'separate_temporal_profile','reason':'Temporal latent assumptions, lag handling and output differ; unfinished immutable LPCMCI source review remains.'},
            {'route':'Commercial supplied latent/mixture fit','decision':'separate_operation','reason':'Different scientific target from a latent graph-equivalence class.'}],
        'costs_to_measure':['Dependency installation and disk','all-request runtime/peak memory','conversion and analyst corrections',
                            'CI/orientation upgrade review','failure/retry/cancellation costs','maintenance and distribution obligations'],
        'owner_obligations':{'adapter_maintainer':'Lock full source/runtime/dependencies, retain notices and implement method-specific conversion/errors.',
                            'scientific_reviewer':'Check sampling/CI premises and graph class; review exact fixtures and any prospective study.',
                            'workflow_owner':'Measure full decision workflow and preserve absent/ambiguous results; no claimed bank acceptance.'},
        'revisit_trigger':'A complete source/dependency environment and rights inventory, implemented selected PC wrapper, independent graph-class/endpoint/error checks and actual engine comparison; any revision or profile change reopens scope review.',
        'bank_inputs_required_for_next_step':False,'original_gap_qualification':False}
    write(OUTPUT,decision)
    graph,_,_=control.combined(ROOT,control.core.read(ROOT,control.core.STATE))
    node=control.ledger.operation(graph,decision['operation_id'])
    review={'outcome':'pass','scope':'Completed explicit defer/selection decision, no integration capability granted',
        'findings':['Package aliases are resolved and six exact bytes agree with the same pinned tree.',
            'Root MIT grant is distinguished from unresolved dependency/distribution closure.',
            'Exact references and a concrete conversion/failure contract exist; no engine run or graph/effect calibration is invented.',
            'Deferral concerns executable admission only; it does not impose authentic bank evidence as a proposal prerequisite.'],
        'evidence':[ref(OUTPUT,'Final selected route and withheld capability'),decision['primary_evidence'],
                    decision['conversion_failure_contract'],decision['behavioral_oracle'],ref(Path(__file__),'Audit and rational reference reproduction')],
        'reviewer':{'name':'Codex author/coordinator','kind':'author'}}
    write(BASE/'author-review.json',review)
    receipt=control.ledger.receipt_template(node)
    receipt.update(outcome='pass',execution='performed',scope=review['scope'],reviewer=review['reviewer'],capabilities=[],
        limitations=['No engine execution or complete environment/rights inventory','No adapter admission, deployment or scientific qualification'],
        outputs=[ref(OUTPUT,'Reviewed explicit defer decision')])
    for i,finding in enumerate(['Pinned source/license/dependency and maintenance evidence bound; package, namespace, bridge and online-service identities remain distinct.',
        'Graph and uncertainty meanings, alternatives, costs, owner actions and exact revisit condition are documented.',
        'integration_allowed is withheld because the executable dependency/conversion path is unfinished; concrete oracle and failure contract are provided for the next implementation.']):
        receipt['criteria'][i].update(verdict='pass',finding=finding,evidence=review['evidence'][:4])
    write(BASE/'operation-receipt.json',receipt)
    print(json.dumps({'outcome':'pass','decision':'defer_executable_admission','preferred':'direct scoped integration',
                      'source_blob_matches':6,'dependencies':12,'package_execution':False,'integration_allowed':False}))


if __name__=='__main__':
    main()

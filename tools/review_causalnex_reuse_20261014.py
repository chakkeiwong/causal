#!/usr/bin/env python3
"""Resolve archival CausalNex reuse from pinned text and exact project algebra."""
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import re

import run_program as control
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'docs/literature/raw'
BASE = ROOT / 'docs/program/execution/2026-10-14/causalnex-reuse'
OUTPUT = ROOT / 'docs/program/comprehensive-v14/work/SW.DECISION.inherited_causalnex/decision.json'
PIN = 'b87ab20599876af8d15d20f317cfcd591b28b32a'
REVIEWER = {'name': 'Codex author/coordinator', 'kind': 'author'}


def now():
    return datetime.now(timezone.utc).isoformat()


def exact():
    threshold = F(1, 5)
    candidates = [F(-1, 5), F(1, 10), F(1, 5), F(1, 2)]
    unpenalized = [w if abs(w) > threshold else F(0) for w in candidates]
    lasso = [w if abs(w) >= threshold else F(0) for w in candidates]
    assert unpenalized == [0, 0, 0, F(1, 2)]
    assert lasso == [F(-1, 5), 0, F(1, 5), F(1, 2)]
    original = {'A->B': F(1, 5), 'B->A': F(1, 2)}
    scaled = {'A->B': original['A->B'] * 10, 'B->A': original['B->A'] / 10}
    assert min(original, key=lambda k: abs(original[k])) == 'A->B'
    assert min(scaled, key=lambda k: abs(scaled[k])) == 'B->A'
    assert original['A->B'] * original['B->A'] == scaled['A->B'] * scaled['B->A'] == F(1, 10)
    x = [(F(-1), F(-2)), (F(1), F(2))]
    shifted = [(a + 1, b) for a, b in x]

    def loss(rows, coefficient):
        return sum(a*a + (b-coefficient*a)**2 for a, b in rows) / (2 * len(rows))

    def slope(rows):
        return sum(a*b for a, b in rows) / sum(a*a for a, b in rows)

    def centered_moment(rows):
        mean = [sum(row[j] for row in rows) / len(rows) for j in (0, 1)]
        return [[sum((row[i]-mean[i])*(row[j]-mean[j]) for row in rows) / len(rows)
                 for j in (0, 1)] for i in (0, 1)]

    assert centered_moment(x) == centered_moment(shifted)
    assert (loss(x, F(2)), loss(shifted, F(2)), slope(x), slope(shifted)) == (F(1, 2), F(3), F(2), F(1))
    assert loss(shifted, slope(shifted)) == F(2)
    return {
        'kind': 'exact_project_reference', 'package_execution': False, 'random_draws': 0,
        'threshold_equality': {'threshold': str(threshold), 'weights': list(map(str, candidates)),
            'unpenalized_reference': list(map(str, unpenalized)), 'lasso_reference': list(map(str, lasso)),
            'scope': 'Independent arithmetic for the two inspected comparison operators, not a fitted graph.'},
        'cycle_units': {'original': {k: str(v) for k, v in original.items()},
            'B_times_10': {k: str(v) for k, v in scaled.items()},
            'deleted_original': 'A->B', 'deleted_scaled': 'B->A',
            'cycle_product_both': '1/10', 'acyclicity_both': '2*cosh(1/10)-2 > 0',
            'scope': 'Stipulated cyclic coefficient matrix, not an upstream optimizer outcome.'},
        'translation': {'rows': [[str(v) for v in row] for row in x],
            'shifted_A_plus_1': [[str(v) for v in row] for row in shifted],
            'centered_second_moment_both': [[str(v) for v in row] for row in centered_moment(x)],
            'loss_fixed_W_AB_2_original': '1/2', 'loss_fixed_W_AB_2_shifted': '3',
            'fixed_direction_no_intercept_slope_original': '2',
            'fixed_direction_no_intercept_slope_shifted': '1',
            'minimum_shifted_loss': '2',
            'scope': 'Fixed A->B direction; not a claim about the globally selected graph.'},
        'limitations': ['No engine execution, latency, security, graph accuracy, causal identification or coverage result.']}


def main():
    assert not OUTPUT.exists(), 'Completed decisions are immutable; use a successor for revisions.'
    commit_path = RAW / 'v12_exec13_pydisc_causalnex_canonical_cutoff.json'
    tree_path = RAW / 'v12_exec13_pydisc_causalnex_canonical_tree.json'
    commit = json.loads(commit_path.read_text())[0]
    tree = json.loads(tree_path.read_text())
    assert commit['sha'] == tree['sha'] == PIN and tree['truncated'] is False
    date = commit['commit']['committer']['date']
    assert date[:10] <= '2026-10-07'
    indexed = {r['path']: r for r in tree['tree']}
    selections = [
        ('v12_exec13_pydisc_causalnex_source_1', 'README.md', 'lines 1-9: explicit end-of-life and support notice',
         ['Declares discontinuation on 24 June 2026 and no future fixes, security patches or issue/PR review.']),
        ('v12_exec13_pydisc_causalnex_source_2', 'LICENSE.md', 'complete root notice: Apache 2.0 and separate trademark exclusion',
         ['Root license notice allows use under Apache 2.0; the notice does not grant trademark rights or qualify dependency licenses.']),
        ('v12_exec13_pydisc_causalnex_source_3', 'causalnex/structure/notears.py',
         '57-121, 231-268, 363-439, 454-555: input/bounds, IDs, loss, stopping and threshold',
         ['Rows are observations and columns variables; tabu direction constraints become optimizer bounds.',
          'The selected path uses an uncentered squared residual objective and trace(expm(W*W))-d.',
          'The inspected code uses sol.x without a structured optimizer-success contract; iteration exhaustion can warn and return a graph.',
          'Unpenalized threshold removes equality; lasso threshold retains a nonzero equality edge.',
          'Pandas wrapper preserves column IDs and learned provenance; these routines return no causal confidence region.']),
        ('v12_exec13_pydisc_causalnex_source_4', 'causalnex/structure/structuremodel.py',
         '60-100, 286-293: cycles, provenance and smallest-absolute-weight deletion',
         ['StructureModel expressly permits cycles and defaults origin to unknown.',
          'threshold_till_dag mutates the graph by deleting smallest absolute weights; its own docstring warns about differing units.']),
        ('v12_exec13_pydisc_causalnex_source_5', 'setup.py',
         '40-110: version/requirements loading, Python restriction, optional discretiser, inactive classifier',
         ['Declares Python >=3.8,<3.11; loads direct requirements externally; classifies the project as inactive.']),
        ('exec14_causalnex_requirements', 'requirements.txt', 'all 14 lines: direct and Python-version-conditional requirements',
         ['NumPy <1.24, pandas <2.0 and pgmpy <0.1.20 are explicit upper bounds; requirements are not a solved environment.']),
        ('exec14_causalnex_init', 'causalnex/__init__.py', 'version assignment and exported module names',
         ['Declares source version 0.12.2; a source version is not a verified installed distribution.'])]
    records = []
    for stem, upstream, anchor, claims in selections:
        path = RAW / (stem + '.txt')
        data = path.read_bytes()
        blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert indexed[upstream]['sha'] == blob, upstream
        url = f'https://raw.githubusercontent.com/mckinsey/causalnex/{PIN}/{upstream}'
        receipt_path = RAW / (stem + '.receipt.json')
        if not receipt_path.exists():
            write(receipt_path, {'status': 'saved_identity_verified_after_recovery', 'url': url,
                'recorded_utc': now(), 'accessed_utc': None, 'http_status': None,
                'acquisition_observation': 'Saved session reports successful bounded curl -fL retrieval; exact retrieval timestamp and HTTP headers were not retained. Bytes independently match the pinned Git tree.',
                'path': str(path.relative_to(ROOT)), 'bytes': len(data),
                'sha256': hashlib.sha256(data).hexdigest(), 'git_blob_sha1': blob})
        receipt = json.loads(receipt_path.read_text())
        assert receipt['url'] == url and receipt['sha256'] == hashlib.sha256(data).hexdigest()
        records.append({'source_identity': url, 'revision': PIN, 'source_date': date,
            'local_copy': ref(path, anchor), 'acquisition_receipt': ref(receipt_path, 'Observed custody and hash'),
            'git_blob_sha1': blob, 'tree_identity_verified': True,
            'inspected_anchors': [anchor], 'supported_claims': claims})
    version = re.search(r'__version__ = "([^"]+)"', (RAW/'exec14_causalnex_init.txt').read_text()).group(1)
    dependencies = (RAW/'exec14_causalnex_requirements.txt').read_text().splitlines()
    primary = {'reviewed_at': now(), 'cutoff': '2026-10-07', 'revision': PIN, 'source_date': date,
        'identity': ref(commit_path, 'Commit identity and date only'),
        'tree': ref(tree_path, 'Complete tree and exact blob identities'), 'sources': records,
        'declared_version': version, 'direct_requirement_lines': dependencies,
        'maintenance': {'end_of_life': '2026-06-24', 'source': records[0]['local_copy'],
            'interpretation': 'Explicit discontinuation at this revision, not inference from a failed URL.'},
        'uninspected': ['Resolved runtime/build/test dependency distributions and security status',
            'Bayesian-network fitting, discretization, interventions and inference implementations',
            'Upstream CI outcomes, installed release artifacts and any successor fork'],
        'package_execution': False}
    write(BASE/'primary-review.json', primary)
    write(BASE/'exact-oracle.json', exact())
    contract = {'status': 'archival_proposal_only', 'integration_allowed': False, 'pin': PIN,
        'possible_profile': 'Isolated historical linear continuous-data graph comparison; no effect/uncertainty service.',
        'inputs': ['Unique ordered column identities and units; finite numeric rows with declared sampling unit.',
            'Explicit centering/scaling fit population and transform, beta, thresholds, tabu directions and convergence settings.',
            'Declared scope excludes hidden-confounder identification, panel feedback and temporal claims.'],
        'conversions': ['Preserve every variable, weighted edge and origin; origin is provenance rather than causal truth.',
            'Store exact threshold comparison and do not silently replace <= by <.',
            'Preserve pre/post-threshold graph and any cycle-deletion trace; a changed graph is a changed result.',
            'Evaluate acyclicity and graph cycles separately from optimization termination; never infer uncertainty from weight.'],
        'failures': {'nonfinite_input': 'invalid_request', 'unknown_or_duplicate_column': 'invalid_request',
            'nonconvergence_or_unreported_solver_success': 'unqualified candidate; no causal effect output',
            'cyclic_graph': 'unsupported as DAG; retain candidate and diagnostic',
            'unit_dependent_pruning': 'require a declared procedure; no silent repair',
            'timeout_or_environment_error': 'unavailable with null qualified result'},
        'prospective_oracles': ['Threshold equality of each entrypoint', 'Tabu-edge direction and column permutation',
            'Centering and unit conversion with full transform metadata', 'Nonfinite, nonconverged and cyclic output preservation'],
        'independent_reference': ref(BASE/'exact-oracle.json', 'Three exact mechanisms, without upstream execution')}
    write(BASE/'conversion-contract.json', contract)
    decision = {'operation_id': 'SW.DECISION.inherited_causalnex', 'canonical_package': 'CausalNex',
        'canonical_repository': 'mckinsey/causalnex',
        'aliases': ['causalnex distribution', 'historical quantumblacklabs/causalnex namespace'],
        'distinct_engines': ['causal-learn', 'CausalML', 'Causica', 'pgmpy'],
        'alias_boundary': 'pgmpy is a separately versioned dependency; the upstream NOTEARS algorithm and CausalNex wrapper do not share automatic approval.',
        'decision': 'reject', 'decision_scope': 'Reject as default new product dependency; retain a cited archival reference.',
        'revision': PIN, 'revision_date': date, 'declared_version': version, 'cutoff': '2026-10-07',
        'license': {'declared': 'Apache-2.0 with separate trademark notice', 'source': records[1]['local_copy']},
        'direct_requirement_lines': dependencies, 'python_requires': '>=3.8,<3.11',
        'integration_allowed': False, 'runtime_qualification': False, 'original_gap_qualification': False,
        'primary_evidence': ref(BASE/'primary-review.json', 'Seven primary blobs matched to one cutoff-eligible revision'),
        'behavioral_oracle': ref(BASE/'exact-oracle.json', 'Independent project reference only'),
        'conversion_failure_contract': ref(BASE/'conversion-contract.json', 'Conditional archival route; not implemented'),
        'target_and_uncertainty': 'Selected NOTEARS path supplies a weighted graph candidate under a stated loss and constraints, not an identified intervention or calibrated graph/effect confidence set.',
        'rationale': ['Explicit discontinuation transfers future fix and dependency ownership to the adopter.',
            'Constrained older dependencies require an isolated resolved environment; no vulnerability or impossibility is asserted.',
            'Source-level convergence, threshold and cycle semantics require a wrapper that preserves limitations.',
            'A general new product gains no demonstrated unique necessity from this archival dependency.'],
        'alternatives': [{'route': 'adopt directly', 'disposition': 'reject default', 'reason': 'No ongoing upstream support or qualified environment.'},
            {'route': 'port selected optimizer', 'disposition': 'not selected', 'reason': 'Would transfer optimizer, numerical, dependency and notice maintenance without demonstrated need.'},
            {'route': 'isolated archival comparison', 'disposition': 'conditional reference', 'reason': 'May reproduce a specific historical comparison if an owner accepts the scoped obligations.'},
            {'route': 'causal-learn, Causica or another separately reviewed engine', 'disposition': 'separate decisions', 'reason': 'Choose by assumptions, graph representation and uncertainty; maintenance or interchangeability is not inferred.'},
            {'route': 'exact small model and explicit expert DAG', 'disposition': 'retain transparent comparator', 'reason': 'An imposed graph makes assumptions visible without claiming discovery accuracy.'}],
        'owner_obligations': {'archive_maintainer': 'Own an isolated lockfile, complete notices, fixes, lifecycle and retirement.',
            'scientific_reviewer': 'Own preprocessing, graph/target assumptions, convergence and refusal semantics.',
            'workflow_owner': 'Own information clock, variable units, feasible intervention and monetary target.'},
        'costs_to_measure': ['Environment build and retained images', 'License/dependency/security review',
            'Preprocessing and graph conversion', 'CPU/memory and failed requests', 'Fix ownership and retirement/migration'],
        'revisit_trigger': 'A documented unique archival requirement plus a named maintainer, reviewed permissible lockfile, implemented conversion/failure contract and executed engine oracles; reassess any fork on its own pin.',
        'bank_data_required_for_next_step': False}
    write(OUTPUT, decision)
    evidence = [ref(OUTPUT, 'Scoped rejection/reference decision'), decision['primary_evidence'],
        decision['behavioral_oracle'], decision['conversion_failure_contract'],
        ref(BASE/'plan-review.md', 'Reviewed plan and claim boundaries'), ref(Path(__file__), 'Source identity and exact reference procedure')]
    facts = ['Seven pinned source blobs establish version, root license, dependency declarations and explicit maintenance discontinuation; aliases and distinct engines are separated.',
        'Graph/uncertainty semantics, exact preprocessing and conversion pitfalls, alternatives, ownership, costs and concrete revisit conditions are documented.',
        'Default adoption is rejected and integration remains disabled; the conditional archival contract and exact references do not claim executed upstream qualification.']
    verify_bindings(evidence)
    write(BASE/'author-review.json', {'outcome': 'pass', 'reviewer': REVIEWER, 'findings': facts,
        'evidence': evidence, 'limitations': ['Source review and exact arithmetic only; no executed upstream package, complete rights/dependency closure or causal performance qualification.']})
    graph, _, _ = control.combined(ROOT, control.core.read(ROOT, control.core.STATE))
    node = control.ledger.operation(graph, decision['operation_id'])
    receipt = control.ledger.receipt_template(node)
    receipt.update(outcome='pass', execution='performed', scope=decision['decision_scope'], reviewer=REVIEWER,
        capabilities=[], outputs=[evidence[0]], limitations=['Rejection completes selection; no adapter or unrestricted scientific gap is qualified.'])
    for criterion, fact in zip(receipt['criteria'], facts):
        criterion.update(verdict='pass', finding=fact, evidence=evidence)
    write(BASE/'operation-receipt.json', receipt)
    print(json.dumps({'outcome': 'pass', 'decision': 'reject_default_dependency', 'source_blobs': len(records),
        'version': version, 'end_of_life': '2026-06-24', 'integration_allowed': False, 'package_execution': False}))


if __name__ == '__main__':
    main()

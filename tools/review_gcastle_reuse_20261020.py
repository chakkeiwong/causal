#!/usr/bin/env python3
"""Authenticate selected gCastle originals and record a bounded reuse disposition."""
import hashlib
import json
from pathlib import Path

import gcastle_contract_reference_20261020 as exact
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run = extension.base
core = run.core
ROOT = core.ROOT
BASE = ROOT/'docs/program/execution/2026-10-20/gcastle-reuse-v1'
RAW = ROOT/'docs/literature/raw'
PIN = 'fd8a04f3b57a0f00930406257d5c30dcb91da0a5'
DATE = '2026-05-29T12:52:49Z'
OP = 'SW.DECISION.inherited_gcastle'
OUTPUT = ROOT/f'docs/program/comprehensive-v14/work/{OP}/decision.json'
REVIEWER = dict(name='Codex author/coordinator', kind='author')
read = lambda p: json.loads(p.read_text())
LIMITS = [
    'Twenty authenticated source blobs do not constitute a complete distribution, dependency lock or transitive rights review.',
    'Version 1.0.4 is a source declaration; no latest release, distributed artifact or current support claim is made.',
    'No downloaded engine, upstream test, GPU workload, live model or sibling repository was executed.',
    'Authored exact witnesses and literal source branches are not observed native failures or conformance results.',
    'Scope is selected PC and linear NOTEARS routines; nonlinear, event-sequence, hidden-variable and bank validity are unqualified.',
    'Rendered visual review, mandatory repair rollups, Q1/Q5 and final proposal acceptance remain open.'
]


def main():
    assert not OUTPUT.exists() and not (BASE/'source-audit.json').exists()
    state = core.read(ROOT, core.STATE)
    assert state['execution_runtime']['active']['operation'] == OP
    write(BASE/'plan-review.json', dict(status='pass', reviewer=REVIEWER,
        evidence=[ref(BASE/'plan.md', 'Reviewed scope and sequencing')],
        checks=['Authenticate the explicit root tree instead of treating a commit-resolved API identifier as the tree hash.',
                'Follow upstream test wrappers and backend imports before making dependency or test claims.',
                'Separate CPDAG encoding, weighted adjacency, CI evidence and causal identification.',
                'Use exact authored witnesses, no downloaded code execution or unsupported general rights conclusion.',
                'Record a reasoned proposal disposition and integrate the substantive delta; keep native admission separate.']))
    commit = read(RAW/'v12_exec13_pydisc_gcastle_cutoff.json')[0]
    tree = read(RAW/'exec20_gcastle_root_tree.json')
    previous_tree = read(RAW/'v12_exec13_pydisc_gcastle_tree.json')
    assert commit['sha'] == PIN and commit['commit']['committer']['date'] == DATE
    assert tree['sha'] == commit['commit']['tree']['sha'] == 'f47e75886996a49ad93f6df7eafd14440790ed38'
    assert not tree['truncated'] and len(tree['tree']) == 547
    assert tree['tree'] == previous_tree['tree']
    blobs = {r['path']: r['sha'] for r in tree['tree'] if r['type'] == 'blob'}
    selected = {f'v12_exec13_pydisc_gcastle_source_{i}': p for i, p in enumerate([
        'gcastle/README.md', 'LICENSE', 'gcastle/castle/algorithms/gradient/notears/linear.py',
        'gcastle/castle/algorithms/pc/pc.py', 'gcastle/setup.py'], 1)}
    for manifest, prefix in [('source-paths.json', 'exec20_gcastle_'),
                             ('extra-source-paths.json', 'exec20_gcastle_extra_')]:
        selected.update({prefix+k: p for k, p in read(BASE/manifest).items()})
    spans = {
        'v12_exec13_pydisc_gcastle_source_1': [(1, 90)],
        'v12_exec13_pydisc_gcastle_source_2': [(1, 178)],
        'v12_exec13_pydisc_gcastle_source_3': [(16, 224)],
        'v12_exec13_pydisc_gcastle_source_4': [(16, 120), (159, 255), (256, 426)],
        'v12_exec13_pydisc_gcastle_source_5': [(1, 44)],
        'exec20_gcastle_0': [(1, 76)], 'exec20_gcastle_1': [(43, 62), (157, 245)],
        'exec20_gcastle_2': [(16, 82)], 'exec20_gcastle_3': [(50, 85)],
        'exec20_gcastle_4': [(16, 220)], 'exec20_gcastle_5': [(16, 95), (504, 529)],
        'exec20_gcastle_6': [(1, 30)], 'exec20_gcastle_7': [(1, 30)],
        'exec20_gcastle_8': [(1, 8)], 'exec20_gcastle_9': [(16, 45)],
        'exec20_gcastle_extra_0': [(16, 86), (200, 216), (250, 267)],
        'exec20_gcastle_extra_1': [(16, 48)], 'exec20_gcastle_extra_2': [(16, 47)],
        'exec20_gcastle_extra_3': [(16, 30)], 'exec20_gcastle_extra_4': [(16, 30)]}
    records, extracts = [], []
    for key, upstream in selected.items():
        path = RAW/(key+'.txt'); receipt_path = path.with_suffix('.receipt.json')
        data = path.read_bytes(); receipt = read(receipt_path)
        url = f'https://raw.githubusercontent.com/huawei-noah/trustworthyAI/{PIN}/{upstream}'
        blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert receipt['status'] == 'saved' and receipt['url'] == url
        assert receipt['sha256'] == core.sha(path) and blob == blobs[upstream]
        lines = data.decode().splitlines()
        ranges = [(a, min(b, len(lines))) for a, b in spans[key]]
        assert all(1 <= a <= b for a, b in ranges)
        anchors = [f'lines {a}-{b}' for a, b in ranges]
        records.append(dict(source_identity=url, version_date=DATE+'; commit '+PIN,
            git_blob_sha1=blob, local_copy=ref(path, '; '.join(anchors)),
            receipt=ref(receipt_path, 'Original acquisition'), accessed_utc=receipt['accessed_utc'],
            inspected_anchors=anchors, executed=False))
        extracts.append(dict(source=upstream, local_copy=ref(path, 'Inspected original'),
            ranges=[dict(start=a, end=b, text='\n'.join(f'{i+1}: {lines[i]}' for i in range(a-1,b)))
                    for a,b in ranges]))
    assert len(records) == 20
    identities = [RAW/n for n in ['v12_exec13_pydisc_gcastle_cutoff.json',
        'v12_exec13_pydisc_gcastle_cutoff.receipt.json', 'exec20_gcastle_root_tree.json',
        'exec20_gcastle_root_tree.receipt.json', 'v12_exec13_pydisc_gcastle_tree.json']]
    for p in [identities[0], identities[2]]:
        receipt = read(p.with_suffix('.receipt.json'))
        assert receipt['status'] == 'saved' and receipt['sha256'] == core.sha(p)
    identity = dict(repository='huawei-noah/trustworthyAI', subproject='gcastle', import_namespace='castle',
        selected_commit=PIN, commit_date=DATE, tree_sha=tree['sha'], tree_entries=547,
        authenticated_blobs=20, declared_version='1.0.4', cutoff='2026-10-07',
        release_artifact_verified=False, current_support_verified=False,
        root_tree_resolution='Explicit immutable root-tree response agrees with all earlier commit-resolved rows; earlier response top-level sha was the commit.',
        maintenance='README declares 1.0.4 dated 7 March 2025; selected monorepo commit date is not subproject maintenance evidence.',
        evidence=[ref(p, 'Pinned identity and acquisition') for p in identities])
    write(BASE/'identity-review.json', identity)
    write(BASE/'inspected-extracts.json', dict(records=extracts, native_execution=False))
    claims = [
        'Selected setup declares gcastle and Apache-2.0; castle declares version1.0.4. README bounds Python to3.6-3.9 while setup declares only>=3.6.',
        'requirements and README list torch, setup install_requires does not; validator imports torch unconditionally and backend defaults to pytorch, whose surface imports gradient methods.',
        'PC orient documents CPDAG output; paired1/1 entries are unresolved edges, not directed two-cycles or latent bidirected endpoints. Scientific validity requires its own assumptions.',
        'The PC skeleton path removes an edge for p>=alpha, copies adjacency by depth for stable variant, and mutates the supplied base_skeleton rather than copying it.',
        'Tensor validates label lengths and input container types but has no explicit finite-value, unique-label or exactly-two-dimensional validation in the inspected constructor; operations reset label metadata.',
        'Prior additions do not explicitly reject contradictions or directed cycles; required and forbidden lists may both retain the same pair. Orientation applies required entries then forbidden entries.',
        'Fisher-z uses inverse with pseudoinverse fallback and clipped partial correlation, then sqrt(n-|Z|-3). The inspected path has no explicit positive-residual-sample guard.',
        'Conditional discrete tests skip ValueError strata; zero aggregate degrees of freedom returns p=1, which meets the PC deletion branch. This branch trace is not a population-independence validation.',
        'Linear NOTEARS uses M=X@W, centers L2 input and uses the polynomial trace constraint. It retains weighted output and uses strict abs(weight)>threshold for binary edges.',
        'The inspected optimizer consumes sol.x without inspecting sol.success; it can stop at the penalty bound or iteration budget. This routine does not separately validate final binary topology.',
        'Selected PC and NOTEARS test methods catch execution exceptions and log them without assertions or rethrow; wrappers call those methods. No test execution or suite-wide claim follows.'
    ]
    source = dict(integrated_citation_key='exec20_gcastle_source', kind='software_primary_sources',
        title='gCastle: pinned graph encoding, validation, dependency and test-source review',
        author='Huawei Noah\'s Ark Lab and gCastle contributors', year=2026,
        source_identity='https://github.com/huawei-noah/trustworthyAI/tree/'+PIN+'/gcastle',
        version_date=DATE+'; commit '+PIN, selected_commit=PIN,
        local_copy=ref(RAW/'v12_exec13_pydisc_gcastle_source_1.txt', 'README identity, scope and dependencies'),
        records=records, identity_evidence=identity['evidence'],
        inspected_anchors=[dict(anchor=c, inspection='Selected pinned original code or documentation') for c in claims],
        supported_claims=claims, limitations=LIMITS, software_executed=False)
    reference = dict(integrated_citation_key='exec20_gcastle_reference', kind='project_authored_exact_reference',
        title='Exact graph-type, unit, threshold and acyclicity contract witnesses',
        author='Causal banking proposal project', year=2026,
        source_identity='tools/gcastle_contract_reference_20261020.py', version_date='2026-10-20',
        local_copy=ref(ROOT/'tools/gcastle_contract_reference_20261020.py', 'calculate, pc_edges and acyclic'),
        inspected_anchors=[dict(anchor='calculate()', inspection='Exact rational calculations and graph checks')],
        supported_claims=['Typed PC edges survive simultaneous label/matrix permutation; an unresolved pair is not a directed cycle.',
            'Two weights1/100 yield h=1/200000000 below1e-8 and a cycle at chosen threshold1/200; default3/10 removes both.',
            'Strict threshold equality and unit changes alter retained edges; assumed structural weight3/10 with intervention100 and cost20 gives margin10, versus-20 under mistaken transposition.'],
        limitations=LIMITS)
    audit = dict(sources=[source, reference], records=records, cutoff='2026-10-07', supported_claims=claims, limitations=LIMITS)
    write(BASE/'source-audit.json', audit)
    write(BASE/'exact-results.json', exact.calculate())
    omissions = dict(unread_or_unqualified=[
        'Complete package artifacts, dependency locks and transitive/license notices; source Apache terms do not settle these.',
        'Actual supported Python/backend/OS combinations, native output correctness, failures and numerical diagnostics.',
        'Event-sequence TTPM, HPCI marked under development, nonlinear/deep methods, GPU behavior and latent discovery.',
        'Statistical graph/effect calibration under dependence, hidden confounding, selection or banking data.',
        'All upstream test suites, actual CI results and module-specific maintenance history.'],
        preserved_failures=[ref(p, 'Preserved sandbox DNS failure') for p in sorted((BASE/'sandbox-failures').glob('*.json'))],
        scope='These limits constrain claims; public proposal qualification can proceed without bank data.')
    write(BASE/'omissions-register.json', omissions)
    write(BASE/'acquisition-review.json', dict(status='pass_for_selected_sources', authenticated_blobs=20,
        evidence=records, identity=ref(BASE/'identity-review.json', 'Explicit root tree resolution'),
        omissions=ref(BASE/'omissions-register.json', 'Recorded coverage and native limits')))
    contract = dict(status='proposed_not_implemented',
        preferred_profile='Retain selected PC and linear NOTEARS as references; evaluate a pinned original Python worker before executable admission.',
        requirements=[
            'Bind variable identifiers, ordered columns, units, transformations, data snapshot, sample law and knowledge provenance.',
            'Reject nonfinite values, duplicate identifiers, malformed dimensions, invalid hyperparameters and contradictory/cyclic knowledge before engine dispatch.',
            'Preserve a typed partially directed graph for PC and weighted/source-row adjacency for NOTEARS; never coerce unresolved edges to arrows or latent endpoints.',
            'Copy inputs/base skeletons; carry explicit label maps through every operation and return them with graph matrices.',
            'Declare the CI family, alpha, variant, conditioning support, singularity policy and residual sample limits. Return insufficient support distinctly from independence.',
            'Expose conditional strata skipped, pseudoinverse use and p-value validity; a p=1 fallback does not replace a scientific support decision.',
            'Fix numerical environment, Python/backend, dependencies, randomization, thread settings, loss and units; verify installation in a disposable public prototype.',
            'Keep weights, strict threshold, solver diagnostics and residual; validate final DAG topology for NOTEARS and graph-class validity for PC separately.',
            'If diagnostics are unavailable through the public surface, return qualification unavailable or use an explicitly reviewed instrumented variant; never infer convergence from returned weights.',
            'Use the same typed request, output and failure semantics through library, CLI and MCP. Do not accept arbitrary agent-generated callable CI code.',
            'Compare native output with exact conversion, permutation, threshold, scaling, topology, support, contradictory-prior and failure references before admission.',
            'Review actual distribution and dependency rights, attribution and notices; measure installation, memory, latency, serialization and upgrade cost on a public prototype.'
        ], native_conformance_passed=False, rights_review_complete=False)
    write(BASE/'conversion-contract.json', contract)
    evidence = [ref(BASE/n, 'Reviewed bounded reuse evidence') for n in
        ['plan-review.json', 'identity-review.json', 'source-audit.json', 'inspected-extracts.json',
         'acquisition-review.json', 'omissions-register.json', 'exact-results.json', 'conversion-contract.json']]
    evidence.append(ref(Path(__file__), 'Exact author review construction'))
    decision = dict(operation_id=OP, status='pass', decision='reference',
        decision_scope='Complete method-specific proposal reuse disposition; retain selected PC and linear NOTEARS references without executable admission.',
        preferred_proposal_route=contract['preferred_profile'], integration_allowed=False, capabilities=[],
        runtime_qualification=False, deployment_allowed=False, original_gap_qualification=False,
        identity=dict(canonical_repository='huawei-noah/trustworthyAI', subproject='gcastle', entry='inherited_gcastle',
            selected_commit=PIN, aliases=['gcastle distribution', 'castle import namespace'],
            alias_boundary='Other trustworthyAI subprojects, every listed discovery method and third-party ports require separate review.'),
        license=dict(declaration='Apache License 2.0',
            evidence=ref(RAW/'v12_exec13_pydisc_gcastle_source_2.txt', 'Sections2-4 grants and redistribution conditions, sections7-9 warranty/liability'),
            complete_distribution_or_transitive_rights=False,
            boundary='Preserve required license/notices and modification notices if distributed; review selected dependencies and actual artifacts separately.'),
        dependencies=dict(python_readme='>=3.6, <=3.9', python_setup='>=3.6',
            requirements=ref(RAW/'exec20_gcastle_8.txt', 'Declared minima including torch>=1.9'),
            setup=ref(RAW/'v12_exec13_pydisc_gcastle_source_5.txt', 'Declared install_requires omits torch'),
            resolved_environment=False), maintenance=identity,
        target_and_uncertainty='PC graph-class and selected weighted DAG candidates under declared statistical assumptions; neither output supplies a calibrated bank effect interval.',
        reason=['Selected original methods are useful comparators whose graph and numerical semantics can be traced.',
            'Current source evidence supports a reference disposition; complete native/rights qualification is absent.',
            'An original-engine worker is the preferred experiment if needed; no measured benefit currently justifies a port.'],
        alternatives=[dict(route='Pinned original Python worker', disposition='conditional_prototype_route',
                reason='Preserves original methods while enforcing graph types, inputs and diagnostics; requires native comparison and a resolved environment.'),
            dict(route='Port selected routines', disposition='defer',
                reason='Must reproduce CI degeneracy, graph orientation, stopping and threshold semantics; no platform or cost evidence yet justifies maintenance.'),
            dict(route='Exact small graph/algebra reference', disposition='retain_reference',
                reason='Transparent conversion and arithmetic oracles; not a replacement for native algorithm/statistical qualification.'),
            dict(route='Whole-catalog adoption or untyped graph conversion', disposition='reject_for_initial_profile',
                reason='Method families have different assumptions and output semantics; umbrella identity is insufficient.')],
        costs_to_measure=['Environment and backend installation', 'Serialization and explicit label retention',
            'CI combinatorial cost and support diagnostics', 'Optimization diagnostics/topology checks',
            'Dependency/notices maintenance and upgrade conformance'], measured_prices_or_bank_ROI=False,
        owner_obligations=dict(scientific_owner='Own sample law, causal assumptions, CI support and knowledge restrictions.',
            data_owner='Own identifiers, units, transformations and information clock.',
            adapter_maintainer='Own pinned environment, conversion, diagnostics, failure handling and interface parity.',
            rights_operator_owner='Review actual distribution/dependency terms and deployment conditions.'),
        revisit_trigger='Before executable admission, resolve the actual environment and rights and qualify native semantics against graph, support and numerical references; reopen on method, version or target change.',
        evidence=evidence, limitations=LIMITS, reviewer=REVIEWER, bank_inputs_required_for_next_step=False)
    write(OUTPUT, decision)
    write(BASE/'review.json', dict(status='pass_for_scoped_proposal_decision', reviewer=REVIEWER,
        reviewed_output=ref(OUTPUT, 'Method-specific reference decision'), evidence=evidence,
        findings=claims, limitations=LIMITS))
    graph, _, _ = run.combined(ROOT, state)
    receipt = run.ledger.receipt_template(run.ledger.operation(graph, OP))
    findings = ['Twenty original blobs authenticate against the explicit immutable root tree; package aliases, dependencies, terms and maintenance limits are explicit.',
        'Graph encoding, CI support, numerical behavior, proposed integration contract, alternatives, costs, owner roles and revisit triggers are source-grounded.',
        'Completed reference disposition grants no native capability; authored witnesses and selected upstream test inspection remain distinct from engine execution.']
    receipt.update(outcome='pass', execution='performed', scope=decision['decision_scope'], reviewer=REVIEWER,
        capabilities=[], outputs=[ref(OUTPUT, 'Contracted gCastle decision')], limitations=LIMITS,
        nonexecution_reason='', revisit_trigger=decision['revisit_trigger'],
        criteria=[dict(index=i, verdict='pass', finding=f, evidence=evidence+[ref(BASE/'review.json', 'Author review')])
                  for i,f in enumerate(findings)])
    write(BASE/'operation-receipt.json', receipt)
    verify_bindings([audit, decision, receipt])
    print(json.dumps(dict(operation=OP, outcome='pass', original_blobs=20,
        decision='reference', integration_allowed=False, native_execution=False)))


if __name__ == '__main__':
    main()

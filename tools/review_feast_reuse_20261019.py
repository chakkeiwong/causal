#!/usr/bin/env python3
"""Freeze a reviewed, source-grounded Feast proposal choice without admission."""
import hashlib
import json
from pathlib import Path
import tomllib

import feast_clock_reference_20261019 as exact
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run = extension.base
core = run.core
ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-19/feast-reuse-v1'
RAW = ROOT / 'docs/literature/raw'
PIN = '9d42729d471a611597760284e3feaf61e000ca0c'
OP = 'SW.DECISION.inherited_feast'
OUTPUT = ROOT / f'docs/program/comprehensive-v14/work/{OP}/decision.json'
REVIEWER = dict(name='Codex author/coordinator', kind='author')
read = lambda p: json.loads(p.read_text())


def main():
    assert not OUTPUT.exists() and not (BASE / 'source-audit.json').exists()
    verify_bindings(read(BASE / 'plan-review.json'))
    commit = read(RAW / 'exec19_feast_cutoff_commit.json')[0]
    tree = read(RAW / 'exec19_feast_tree.json')
    assert commit['sha'] == PIN
    assert commit['commit']['committer']['date'] == '2026-10-07T15:02:06Z'
    assert tree['sha'] == commit['commit']['tree']['sha'] == '68b4845d0c60d7a8f913bbca4b16522b7c29ae91'
    assert tree['truncated'] is False and len(tree['tree']) == 3759
    blobs = {r['path']: r['sha'] for r in tree['tree'] if r['type'] == 'blob'}
    assert 'setup.py' not in blobs
    files = [dict(id=f'exec19_feast_root_{i}', path=p) for i, p in
        [(0, 'README.md'), (1, 'LICENSE'), (3, 'pyproject.toml'), (4, 'sdk/python/feast/feature_store.py')]]
    for name in ['technical', 'interface', 'mcp']:
        files += [r for r in read(BASE / f'{name}-acquisition-manifest.json')['files']
                  if r['id'] not in {'exec19_feast_technical_0', 'exec19_feast_technical_12'}]
    ranges = {
        'root_0': [(29, 43), (278, 285)], 'root_1': [(1, 202)],
        'root_3': [(1, 175), (250, 285)], 'root_4': [(1988, 2038), (2120, 2155), (3962, 4026)],
        'technical_1': [(1, 10)], 'technical_2': [(40, 95), (163, 201)],
        'technical_3': [(140, 160), (275, 360), (1187, 1292)],
        'technical_4': [(445, 464), (498, 534)], 'technical_5': [(140, 190), (200, 244)],
        'technical_6': [(473, 498)], 'technical_7': [(252, 298)],
        'technical_8': [(25, 121), (124, 278), (281, 325)], 'technical_9': [(1, 100)],
        'technical_11': [(138, 144), (271, 281), (382, 399), (1755, 1853)],
        'interfaces_0': [(1, 20)], 'interfaces_1': [(1, 32), (128, 149)],
        'interfaces_2': [(1, 60)], 'interfaces_3': [(1, 68)],
        'mcp_0': [(1, 240)], 'mcp_1': [(1, 100)]}
    records, extracts = [], []
    for row in files:
        path = RAW / (row['id'] + '.txt')
        receipt_path = RAW / (row['id'] + '.receipt.json')
        data, receipt = path.read_bytes(), read(receipt_path)
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        url = f'https://raw.githubusercontent.com/feast-dev/feast/{PIN}/{row["path"]}'
        assert receipt['status'] == 'saved' and receipt['url'] == url
        assert receipt['sha256'] == core.sha(path) and blob == blobs[row['path']]
        lines = data.decode().splitlines()
        spans = [(lo, min(hi, len(lines))) for lo, hi in ranges[row['id'].removeprefix('exec19_feast_')]]
        assert all(1 <= lo <= hi for lo, hi in spans)
        anchors = [f'lines {lo}-{hi}' for lo, hi in spans]
        extracts.append(dict(source=row['path'], local_copy=ref(path, '; '.join(anchors)),
            ranges=[dict(start=lo, end=hi, text='\n'.join(f'{n+1}: {lines[n]}' for n in range(lo-1, hi))) for lo, hi in spans]))
        records.append(dict(role='inspected_primary_code_test_or_documentation', source_identity=url,
            version_date='commit ' + PIN + '; 2026-10-07T15:02:06Z', git_blob_sha1=blob,
            accessed_utc=receipt['accessed_utc'], local_copy=ref(path, '; '.join(anchors)),
            receipt=ref(receipt_path, 'Bounded public original acquisition'), inspected_anchors=anchors, executed=False))
    assert len(records) == 20
    project = tomllib.loads((RAW / 'exec19_feast_root_3.txt').read_text())
    dependencies = project['project']['dependencies']
    assert project['project']['requires-python'] == '>=3.10.0'
    write(BASE / 'inspected-extracts.json', dict(records=extracts, upstream_execution=False))
    identity = dict(selected_commit=PIN, commit_date=commit['commit']['committer']['date'],
        tree_entries=3759, source_blobs=20, cutoff='2026-10-07 Asia/Shanghai',
        package_release_version_verified=False, current_support_verified=False,
        evidence=[ref(RAW / n, 'Selected cutoff commit or complete tree and acquisition identity') for n in
            ['exec19_feast_cutoff_commit.json', 'exec19_feast_cutoff_commit.receipt.json',
             'exec19_feast_tree.json', 'exec19_feast_tree.receipt.json']])
    write(BASE / 'identity-review.json', identity)
    limits = [
        'Twenty selected original blobs do not constitute a complete package, dependency lock, license inventory or security audit.',
        'The selected commit predates the client cutoff; no released package version or current support level is inferred.',
        'No Feast engine, provider, upstream test, generated SQL, MCP server, downloaded code or sibling repository executed.',
        'Creation time is usable as an availability clock only with a separately established business meaning, revision history and transformation provenance.',
        'Selected Dask and BigQuery paths do not establish all-provider parity; conflicting equal timestamps and duplicate request rows require native conformance.',
        'USD15 is the authored value of an unavailable rule, not observed loss, measured software error or achievable bank ROI.',
        'MCP documentation and selected proxy code do not qualify authentication, authorization, transport reliability or historical replay.',
        'Executable admission, rendered visual acceptance, bank validation and broader mandatory repairs remain open.'
    ]
    claims = [
        'get_historical_features defaults filter_by_created_timestamp to False; enabled filtering leaves views without a creation field unaffected.',
        'The selected passthrough provider checks declared support and the base offline store raises NotImplementedError for unsupported filtering.',
        'The selected Dask path filters event/TTL, blanks later-or-null-created candidates before deduplication and preserves an entity when all versions are late; source tests specify these cases.',
        'The BigQuery template applies event and optional creation cutoffs, then ranks by event/creation; its final rejoin requires an explicit uniqueness contract for equal timestamp rows.',
        'Online retrieval is documented as latest-value access; online materialization and historical replay are different paths.',
        'Standalone feast mcp proxies features and registry; feature tools include online reads, push and materialization, and selected HTTP status errors become ToolError. In-process MCP uses a separate extra and deployment.',
        'The root license declares Apache-2.0; Python requires>=3.10, version is dynamic, dependencies are ranges and provider/MCP extras are distinct.'
    ]
    source = dict(integrated_citation_key='exec19_feast_source', kind='software_primary_sources',
        title='Feast: selected historical retrieval, provider, timestamp tests, online and MCP sources',
        author='Feast contributors', year=2026, source_identity='https://github.com/feast-dev/feast',
        version_date='2026-10-07T15:02:06Z; commit ' + PIN, selected_commit=PIN,
        local_copy=ref(RAW / 'exec19_feast_root_0.txt', 'Selected source identity'), records=records,
        identity_evidence=identity['evidence'],
        inspected_anchors=[dict(anchor=c, inspection='Pinned primary code, tests and official documentation') for c in claims],
        supported_claims=claims, limitations=limits, software_executed=False)
    reference = dict(integrated_citation_key='exec19_feast_reference', kind='project_authored_exact_reference',
        title='Exact banking availability-clock and late-revision reference', author='Causal banking proposal project', year=2026,
        source_identity='tools/feast_clock_reference_20261019.py', version_date='2026-10-19',
        local_copy=ref(ROOT / 'tools/feast_clock_reference_20261019.py', 'select and calculate: exact law, clock contrasts and edge cases'),
        inspected_anchors=[dict(anchor='select(); calculate()', inspection='Exact rational enumeration, input-order invariance and typed missing/failure checks')],
        supported_claims=['With100USD success payoff and50USD action cost, unavailable type information yields15USD versus0USD for every feasible policy under the stipulated law. Creation filtering repairs a late revision but not a separate delivery delay.'],
        limitations=['Authored example; neither native conformance nor empirical performance.'])
    audit = dict(sources=[source, reference], records=records, selected_commit=PIN, cutoff='2026-10-07',
        supported_claims=claims, limitations=limits)
    write(BASE / 'source-audit.json', audit)
    write(BASE / 'exact-results.json', exact.calculate())
    failures = [ref(RAW / 'head_feast.receipt.json', 'Inherited403 pin failure'),
                ref(RAW / 'exec19_feast_root_2.receipt.json', 'setup.py404; selected complete tree confirms absence')]
    failures += [ref(p, 'Preserved sandbox DNS failure') for p in (BASE / 'sandbox-failures').glob('*.json')]
    write(BASE / 'acquisition-review.json', dict(status='pass_for_selected_sources', original_blobs=20,
        evidence=records, failures=failures,
        acquired_not_used=['sdk/python/pyproject.toml lint configuration', 'universal historical integration test file'],
        unavailable_document_path='The proposed concepts/online-store.md path was absent from the tree and never requested; actual components/online-store.md was acquired.'))
    contract = dict(status='proposed_not_implemented', preferred_profile='Original pinned Feast behind a typed historical retrieval boundary, initially one selected provider',
        requirements=[
            'Require one immutable request identifier per decision and an explicit entity key; preserve input multiplicity and order in the response.',
            'Bind feature definitions, transformations and training inputs, event/creation/ingestion/actual-availability clocks, timezone, decision ordering and input snapshot hashes.',
            'Use creation filtering only when its field is non-null and certified to reflect the required actual availability; otherwise a separate availability predicate is required.',
            'Require provider support; refuse unsupported or unknown clocks and never silently disable filtering after an error.',
            'Declare positive TTL or explicit unbounded history, inclusive endpoint meaning and an ordering convention for events sharing the decision timestamp.',
            'Preserve no eligible version, observed null, observed zero, conflicting revisions, unsupported provider, query failure and incomplete/cancelled retrieval as different results.',
            'Reject conflicting equal entity/event/creation keys or use an explicitly qualified source revision order; never let a join multiply decision weights silently.',
            'Freeze all inputs to on-demand transforms; a correct scalar timestamp does not certify a feature derived from future records or parameters.',
            'Keep latest online reads and historical retrieval separately named in library, CLI and MCP contracts; record semantic mode and provider in every result.',
            'Expose a reviewed read-only historical operation to proposal agents; push and materialization are separate state-changing tools and require separate deployment policy.',
            'Bind complete distribution, extras, dependencies, notices and configuration; validate native row-level conformance before enabling an adapter.'
        ], failures=dict(no_match='No eligible version; retain decision row', null='Observed missing value, not zero',
            unknown_clock='Insufficient information to establish availability', conflict='Ambiguous revision',
            unsupported='Requested filtering unsupported; do not retry weaker semantics',
            http_error='Tool failure, not feature data', incomplete='No completed inference result'),
        native_conformance_passed=False)
    write(BASE / 'conversion-contract.json', contract)
    evidence = [ref(BASE / n, 'Reviewed Feast proposal evidence') for n in
        ['plan-review.json', 'identity-review.json', 'source-audit.json', 'inspected-extracts.json',
         'acquisition-review.json', 'exact-results.json', 'conversion-contract.json']]
    evidence.append(ref(Path(__file__), 'Exact review and receipt construction'))
    decision = dict(operation_id=OP, status='pass', decision='defer',
        decision_scope='Complete conditional proposal selection of Feast for historical feature retrieval; defer executable admission.',
        preferred_proposal_route=contract['preferred_profile'], integration_allowed=False, capabilities=[],
        runtime_qualification=False, deployment_allowed=False, original_gap_qualification=False,
        identity=dict(canonical_repository='feast-dev/feast', entry='inherited_feast', selected_commit=PIN,
            aliases=['Feast Python SDK', 'Feast feature store'],
            alias_boundary='Provider plugins and online/standalone MCP/in-process MCP surfaces have distinct contracts; no umbrella runtime clearance.'),
        license=dict(root='Apache-2.0', redistribution='Retain license and applicable notices; identify modifications; inspect actual distribution and dependency terms.',
            complete_distribution_or_transitive_rights=False),
        dependencies=dict(python=project['project']['requires-python'], direct=dependencies,
            provider_extras=['gcp', 'duckdb', 'ibis'], mcp_extras={k: project['project']['optional-dependencies'][k] for k in ['mcp', 'mcp-server']},
            resolved_environment=False), maintenance=identity,
        target_and_uncertainty='Reconstruct decision information and preserve row populations; retrieval supplies no causal identification or calibrated uncertainty.',
        reason=['Selected source supports a concrete conditional proposal route and a creation-time safeguard.',
            'Retain original semantics rather than porting providers without a demonstrated platform requirement.',
            'Native conformance and actual distribution rights remain later admission work, not reasons to postpone this scoped proposal choice.'],
        alternatives=[dict(route='Explicit bitemporal file/query baseline', disposition='retain_reference', reason='Small public histories can expose both clocks and revision rules with fewer moving parts; scaling is unmeasured.'),
            dict(route='Existing bank feature infrastructure', disposition='separate_candidate', reason='Reuse depends on actual availability and revision-history guarantees; no vendor parity inferred.'),
            dict(route='Port Feast providers into a new engine', disposition='defer', reason='Duplicated timestamp, key and failure semantics without measured need.'),
            dict(route='Use latest online data to replay prior decisions', disposition='reject', reason='Latest values do not establish the historical information set.'),
            dict(route='Unrestricted MCP feature-tool bundle', disposition='reject_for_initial_profile', reason='Push/materialization change data state; tool visibility cannot establish historical semantics.')],
        costs_to_measure=['Immutable history storage', 'Availability-clock validation', 'Provider setup and conversions',
            'Historical joins and duplicate checks', 'Materialization and network/registry latency', 'Upgrade conformance and operational ownership'],
        measured_prices_or_bank_ROI=False,
        owner_obligations=dict(scientific_owner='Own estimand, decision information and missingness/assignment assumptions.',
            data_owner='Certify availability/revision clocks and all transform inputs.',
            adapter_maintainer='Own pinned provider, conversion/failure handling, row conservation and native conformance.',
            rights_operator_owner='Own the actual distribution, dependency notices, deployment and state-changing tool policy.'),
        revisit_trigger='Acquire a complete pinned distribution and notices, qualify one provider against late revisions, delayed delivery, null clocks, TTL edges, tied revisions, duplicate decisions, errors and cancellation; preserve CLI/MCP semantic mode and inspect downstream consumers before admission. Any revision/provider change reopens review.',
        evidence=evidence, limitations=limits, reviewer=REVIEWER, bank_inputs_required_for_next_step=False)
    write(OUTPUT, decision)
    write(BASE / 'review.json', dict(status='pass_for_scoped_proposal_decision', reviewer=REVIEWER,
        reviewed_output=ref(OUTPUT, 'Completed bounded proposal choice; executable admission deferred'),
        evidence=evidence, findings=claims, limitations=limits))
    state = core.read(ROOT, core.STATE)
    assert state['execution_runtime']['active']['operation'] == OP
    graph, _, _ = run.combined(ROOT, state)
    receipt = run.ledger.receipt_template(run.ledger.operation(graph, OP))
    findings = ['Twenty selected original blobs bind immutable source, root license, dependency declarations, alias boundaries and historical maintenance evidence.',
        'Information clocks, provider and interface semantics, alternatives, exact assumed economics, costs, owners and revisit triggers are explicit.',
        'No integration capability is granted. Native provider conformance and complete dependency/rights admission remain deferred within the completed proposal decision.']
    receipt.update(outcome='pass', execution='performed', scope=decision['decision_scope'], reviewer=REVIEWER,
        capabilities=[], outputs=[ref(OUTPUT, 'Contracted Feast proposal decision')], limitations=limits,
        nonexecution_reason='', revisit_trigger=decision['revisit_trigger'],
        criteria=[dict(index=i, verdict='pass', finding=f, evidence=evidence+[ref(BASE / 'review.json', 'Author review')]) for i, f in enumerate(findings)])
    write(BASE / 'operation-receipt.json', receipt)
    verify_bindings([audit, decision, receipt])
    print(json.dumps(dict(operation=OP, outcome='pass', original_blobs=20, direct_dependencies=len(dependencies),
        integration_allowed=False, native_execution=False)))


if __name__ == '__main__':
    main()

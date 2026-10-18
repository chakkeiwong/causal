#!/usr/bin/env python3
"""Freeze a bounded DuckDB proposal decision; do not execute the engine."""
import hashlib
import json
from pathlib import Path
import re

import duckdb_semantic_reference_20261019 as exact
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run = extension.base
core = run.core
ROOT = core.ROOT
BASE = ROOT/'docs/program/execution/2026-10-19/duckdb-reuse-v1'
RAW = ROOT/'docs/literature/raw'
PIN = 'b8a06e4a22672e254cd0baa68a3dbed2eb51c56e'
OP = 'SW.DECISION.inherited_duckdb'
OUTPUT = ROOT/f'docs/program/comprehensive-v14/work/{OP}/decision.json'
REVIEWER = dict(name='Codex author/coordinator', kind='author')


def read(path):
    return json.loads(path.read_text())


def main():
    assert not OUTPUT.exists() and not (BASE/'source-audit.json').exists()
    assert read(BASE/'plan-review.json')['status'] == 'pass'
    identity = read(BASE/'identity-review.json')
    verify_bindings(identity)
    commit = read(RAW/'exec19_duckdb_commit_v140.json')
    release = read(RAW/'exec19_duckdb_release_v140.json')
    tree = read(RAW/'exec19_duckdb_tree_v140.json')
    assert commit['sha'] == PIN and commit['commit']['committer']['date'] == '2025-09-15T19:32:06Z'
    assert release['tag_name'] == 'v1.4.0' and release['published_at'] == '2025-09-16T10:17:31Z'
    assert tree['sha'] == commit['commit']['tree']['sha'] == '51f1a609fd0b272306708a73d4441bcb932ad2d3'
    assert tree['truncated'] is False and len(tree['tree']) == 15449
    blobs = {r['path']: r['sha'] for r in tree['tree'] if r['type'] == 'blob'}
    assert '.gitmodules' not in blobs
    files = [dict(id=f'exec19_duckdb_root_{i}', path=p) for i,p in enumerate([
        'README.md','LICENSE','CMakeLists.txt','extension/extension_config.cmake'])]
    for name in ['technical','contract']:
        files += read(BASE/f'{name}-acquisition-manifest.json')['files']
    assert len(files) == 23
    ranges = {
        'exec19_duckdb_root_0':[(1,110)], 'exec19_duckdb_root_1':[(1,100)],
        'exec19_duckdb_root_2':[(20,42),(150,170),(245,258)], 'exec19_duckdb_root_3':[(1,40)],
        'exec19_duckdb_technical_0':[(90,145),(200,215)],
        'exec19_duckdb_technical_1':[(610,645)], 'exec19_duckdb_technical_2':[(95,125),(339,360)],
        'exec19_duckdb_technical_3':[(1,175)], 'exec19_duckdb_technical_4':[(1,125)],
        'exec19_duckdb_technical_5':[(209,261)], 'exec19_duckdb_technical_6':[(1,40)],
        'exec19_duckdb_technical_7':[(1,180)], 'exec19_duckdb_technical_8':[(1,170)],
        'exec19_duckdb_technical_9':[(1,200)], 'exec19_duckdb_technical_10':[(1,160)],
        'exec19_duckdb_technical_11':[(1,180)], 'exec19_duckdb_contract_0':[(1,60)],
        'exec19_duckdb_contract_1':[(1,25),(260,410)], 'exec19_duckdb_contract_2':[(1,80)],
        'exec19_duckdb_contract_3':[(1,100)], 'exec19_duckdb_contract_4':[(1,160)],
        'exec19_duckdb_contract_5':[(1,100)], 'exec19_duckdb_contract_6':[(1,100)]}
    records, extracts = [], []
    for row in files:
        path = RAW/(row['id']+'.txt')
        receipt_path = RAW/(row['id']+'.receipt.json')
        data = path.read_bytes()
        receipt = read(receipt_path)
        blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        url = f'https://raw.githubusercontent.com/duckdb/duckdb/{PIN}/{row["path"]}'
        assert receipt['status'] == 'saved' and receipt['url'] == url
        assert receipt['sha256'] == core.sha(path) and blob == blobs[row['path']], row
        assert row.get('git_blob_sha1',blob) == blob
        lines = data.decode().splitlines()
        anchors = [f'lines {lo}-{min(hi,len(lines))}' for lo,hi in ranges[row['id']]]
        extracts.append(dict(source=row['path'],local_copy=ref(path, '; '.join(anchors)),
            ranges=[dict(start=lo,end=min(hi,len(lines)),text='\n'.join(
                f'{n+1}: {lines[n]}' for n in range(lo-1,min(hi,len(lines))))) for lo,hi in ranges[row['id']]]))
        records.append(dict(role='inspected_primary_technical_text',source_identity=url,
            version_date='v1.4.0; selected commit 2025-09-15; '+PIN,git_blob_sha1=blob,
            accessed_utc=receipt['accessed_utc'],local_copy=ref(path,'; '.join(anchors)),
            receipt=ref(receipt_path,'Authentic bounded public acquisition'),inspected_anchors=anchors,executed=False))
    write(BASE/'inspected-extracts.json',dict(records=extracts,upstream_execution=False))
    third = (RAW/'exec19_duckdb_technical_6.txt').read_text()
    direct = re.findall(r'add_subdirectory\(([^)]+)\)',third.split('if(NOT WIN32')[0])
    assert len(direct) == 12
    assert 'set(CMAKE_CXX_STANDARD "11"' in (RAW/'exec19_duckdb_root_2.txt').read_text()
    limits = [
        'Twenty-three selected source blobs at one historical revision are not a complete distribution or dependency/rights inventory.',
        'Upstream tests are inspected specifications, not tests executed here; no DuckDB binary, package, downloaded code or sibling repository was run.',
        'CMake declarations and source defaults do not establish the configuration of any binary or installed client.',
        'External-access disablement permits already attached database/WAL paths and configured temporary storage; it is not an OS sandbox or read-only guarantee.',
        'A selected transaction conflict test does not prove a full isolation regime or freeze external file bytes.',
        'The exact reference is authored descriptive arithmetic without causal assignment, calibrated uncertainty, measured speed or bank ROI.',
        'Selected tag identity is historical; latest-release, present maintenance and vendor support claims remain unverified.',
        'The bounded proposal selection enables no adapter or deployment; native conformance, actual distribution notices and operational qualification remain future work.'
    ]
    claims = [
        'The selected source uses C++11 and declares twelve direct non-amalgamation third-party subdirectories; test-only directories and extensions are separate.',
        'Base extension configuration includes core_functions and parquet, with conditional jemalloc; autoload/install defaults depend on build definitions.',
        'The selected C++ Query path materializes; result types expose errors/schema and separate streaming/pending paths.',
        'External access initially defaults true; disabling it retains attached database/WAL paths and temporary storage permissions.',
        'Upstream tests distinguish COUNT zero and NULL aggregate outputs on empty/all-missing inputs; null order is configurable and unordered LIMIT is not a stable cohort rule.',
        'Transaction wrappers check errors; the selected autoload helper catches exceptions and returns false. Neither failure is a scientific negative.',
        'Root MIT and four inspected third-party notices have distinct scopes; utf8proc also includes a Unicode data notice and MbedTLS declares Apache-2.0 OR GPL-2.0-or-later.'
    ]
    source = dict(integrated_citation_key='exec19_duckdb_source',kind='software_primary_sources',
        title='DuckDB v1.4.0: selected build, query, external-access, aggregate, transaction and notice sources',
        author='DuckDB contributors',year=2025,source_identity='https://github.com/duckdb/duckdb',
        version_date='v1.4.0 released 2025-09-16; commit '+PIN,selected_commit=PIN,
        local_copy=ref(RAW/'exec19_duckdb_root_0.txt','README; selected source identity'),
        records=records,identity_evidence=identity['evidence']+[
            ref(RAW/'exec19_duckdb_tree_v140.json','Complete selected recursive tree; 15449 entries')],
        inspected_anchors=[dict(anchor=c,inspection='Selected primary code/test/notice text') for c in claims],
        supported_claims=claims,limitations=limits,software_executed=False,rights_qualified=False)
    reference_source = dict(integrated_citation_key='exec19_duckdb_reference',kind='project_authored_exact_reference',
        title='Exact tabular preparation reference: missingness, multiplicity, ordering and information clocks',
        author='Causal banking proposal project',year=2026,
        source_identity='tools/duckdb_semantic_reference_20261019.py',version_date='2026-10-19',
        local_copy=ref(ROOT/'tools/duckdb_semantic_reference_20261019.py','calculate: exact finite enumeration and 24 row permutations'),
        inspected_anchors=[dict(anchor='calculate()',inspection='Exact rational replay and authored assumptions')],
        supported_claims=['Finite contrasts 0,1/3,2/3; assumed values -40,60,160USD; join duplication changes 50 to75USD; preaction clock excludes a later feature.'],
        limitations=['Authored counterexamples; no native SQL or causal qualification.'])
    audit = dict(sources=[source,reference_source],records=records,cutoff='2026-10-07',
        source_identity=source['source_identity'],selected_commit=PIN,supported_claims=claims,limitations=limits)
    write(BASE/'source-audit.json',audit)
    write(BASE/'exact-results.json',exact.calculate())
    failures = [ref(RAW/'head_duckdb.receipt.json','Inherited403 lookup failure'),
        ref(RAW/'exec19_duckdb_root_4.receipt.json','Requested .gitmodules returns404; complete selected tree confirms absence')]
    failures += [ref(p,'Preserved original sandbox acquisition failure') for p in sorted((BASE/'sandbox-failures').rglob('*.json'))]
    write(BASE/'acquisition-review.json',dict(status='pass_for_selected_sources',original_blobs=23,
        evidence=records,identity=identity,failures=failures,
        limits='Absent .gitmodules does not mean absent dependencies. Failed originals remain preserved.'))
    contract = dict(status='proposed_not_implemented',preferred_profile='Pinned original DuckDB engine behind a typed local analytical-preparation boundary',
        requirements=[
            'Freeze immutable input copies and hashes, schema/units, extraction and availability clocks, query revision and selected engine/client/build configuration.',
            'Declare entity keys and join cardinality; reject unexpected duplicates and preserve population weights. Row count is not effective independent sample size.',
            'Preserve NULL, NaN, empty relation, all-missing group and observed zero as distinct states, with denominators and nullable aggregates.',
            'Convert integers, decimals, timestamps/time zones and names reversibly; preserve precision and refuse lossy conversions.',
            'Specify total output keys and tie-breaks plus explicit null order. LIMIT and row position cannot define an unstated cohort or time ordering.',
            'Use approved typed query templates and a single completed bounded materialized result initially; verify schema, every error and terminal status before publication.',
            'Budget memory, disk and cancellation independently; materialization can exceed memory. Reject partial output as a complete analytical result.',
            'Disable automatic extension installation/loading for the proposed profile; allow only reviewed pinned artifacts in an explicitly permissioned worker.',
            'Treat transaction scope and frozen external bytes separately; external_access=false is neither a read-only switch nor OS isolation.',
            'Keep the causal query, graph, assignment/missingness assumptions, sampling law and uncertainty argument outside the database success signal.'
        ],failures=dict(empty='Completed empty relation, not zero effect',all_missing='Observed rows with no observed outcome, not zero',
            query_error='Execution failure with original diagnostic',extension_unavailable='Dependency/configuration failure, not causal nonidentification',
            cancelled='Incomplete execution; discard partial inference',invalid_keys='Population/weighting contract violation',
            clock_violation='Postdecision information cannot be relabeled as predecision'),native_conformance_passed=False)
    write(BASE/'conversion-contract.json',contract)
    evidence = [ref(BASE/n,'Scoped DuckDB proposal evidence') for n in ['plan-review.json','identity-review.json',
        'source-audit.json','inspected-extracts.json','acquisition-review.json','exact-results.json','conversion-contract.json']]
    evidence += [ref(Path(__file__),'Exact review and receipt construction')]
    decision = dict(operation_id=OP,status='pass',decision='defer',
        decision_scope='Complete the bounded proposal selection of DuckDB for local analytical preparation; defer executable admission.',
        preferred_proposal_route=contract['preferred_profile'],integration_allowed=False,capabilities=[],runtime_qualification=False,
        deployment_allowed=False,original_gap_qualification=False,
        identity=dict(canonical_repository='duckdb/duckdb',entry='inherited_duckdb',version='v1.4.0',selected_commit=PIN,
            cutoff='2026-10-07',aliases=['DuckDB engine','duckdb Python client'],
            alias_boundary='Client bindings are interfaces to an engine; no Python wrapper or binary qualification follows from selected C++ sources.'),
        license=dict(root='MIT',selected_notices=['RE2 BSD-style','utf8proc MIT and Unicode data notice',
            'MbedTLS Apache-2.0 OR GPL-2.0-or-later','Zstd BSD-style'],complete_distribution_or_transitive_rights=False,
            permissible_selected_embedding_verified=False),
        dependencies=dict(CXX_standard='11',direct_non_amalgamation=direct,base_extensions=['core_functions','parquet'],
            conditional_extension='jemalloc under selected platform/build conditions',resolved_environment=False),
        maintenance=dict(commit_date=identity['commit_date'],release_date=identity['release_date'],observation_date='2026-10-19',
            current_support_or_latest_release_verified=False),
        target_and_uncertainty='Analytical population construction and tabular preparation. A completed query provides no causal identification or calibrated sampling uncertainty.',
        reason=['Selected source and semantic boundaries justify a concrete preferred prototype candidate.',
            'Retain the original engine; no demonstrated target-platform need justifies reproducing its optimizer, storage and SQL semantics in a port.',
            'Native conformance and complete rights/dependencies remain executable-admission work without blocking proposal choice.'],
        alternatives=[dict(route='Explicit-file exact reference',disposition='retain_baseline',reason='Transparent small-case population and null semantics; no scale claim.'),
            dict(route='SQLite',disposition='separate_candidate',reason='A different SQL/storage boundary needs its own types, query and scale review; no parity inferred.'),
            dict(route='Dataframe or columnar processing',disposition='separate_candidate',reason='Potentially narrower preparation path; independently inspect joins, missingness, conversion and memory.'),
            dict(route='Port the SQL engine',disposition='defer',reason='Duplicates substantial correctness and maintenance obligations without measured need.'),
            dict(route='Unrestricted agent SQL and automatic extension installation',disposition='reject_for_initial_profile',reason='An unconstrained execution surface exceeds the declared local input and failure contract.')],
        costs_to_measure=['Input freezing/storage','Full distribution and notice review','Conversions and joins','Memory/disk including materialization',
            'Startup and failed-query cost','Upgrade regression and operational ownership'],measured_prices_or_bank_ROI=False,
        owner_obligations=dict(scientific_owner='Own population, estimand, information clocks and missingness/assignment assumptions.',
            adapter_maintainer='Own pinned build/client, typed conversions, failure handling, resource controls and native conformance.',
            product_rights_owner='Own the actual distribution, dependencies, licenses and applicable notices.'),
        revisit_trigger='Bind a complete pinned distribution/client, notices and build settings; run native conformance on empty/all-missing/zero groups, duplicate joins, clocks, total ordering, precision, query/transaction errors, extensions, cancellation and external file mutation. New engine/client versions or execution profiles reopen review.',
        evidence=evidence,limitations=limits,reviewer=REVIEWER,bank_inputs_required_for_next_step=False)
    write(OUTPUT,decision)
    write(BASE/'review.json',dict(status='pass_for_scoped_proposal_decision',reviewer=REVIEWER,
        reviewed_output=ref(OUTPUT,'Bounded completed proposal selection; executable admission deferred'),
        evidence=evidence,findings=claims,limitations=limits))
    state = core.read(ROOT,core.STATE)
    assert state['execution_runtime']['active']['operation'] == OP
    graph,_,_ = run.combined(ROOT,state)
    receipt = run.ledger.receipt_template(run.ledger.operation(graph,OP))
    findings = ['Selected source/version, alias boundary, root and selected third-party notices, twelve direct dependencies and historical maintenance observations are authenticated.',
        'Preparation and causal semantics, alternatives, unmeasured costs, owners and exact revisit triggers are explicit.',
        'No integration capability is granted. Proposed typed conversion/failure contracts and exact authored references support a bounded proposal decision; executable admission remains deferred.']
    receipt.update(outcome='pass',execution='performed',scope=decision['decision_scope'],reviewer=REVIEWER,
        capabilities=[],outputs=[ref(OUTPUT,'Contracted DuckDB proposal reuse decision')],limitations=limits,
        nonexecution_reason='',revisit_trigger=decision['revisit_trigger'],
        criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence+[ref(BASE/'review.json','Author review')]) for i,f in enumerate(findings)])
    write(BASE/'operation-receipt.json',receipt)
    verify_bindings([audit,decision,receipt])
    print(json.dumps(dict(operation=OP,outcome='pass',original_blobs=23,direct_dependencies=12,
        decision='defer_executable_admission',integration_allowed=False,upstream_execution=False)))


if __name__ == '__main__':
    main()

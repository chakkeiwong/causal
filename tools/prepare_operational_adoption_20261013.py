#!/usr/bin/env python3
"""Preserve operational source, inspect local fault receipts and review I4."""
from fractions import Fraction as F
from itertools import product
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import build_integrated_monograph_v12 as shared
import master_control as core

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/operational-adoption'
CHAPTER = ROOT / 'docs/program/comprehensive-v14/work/TEXT.DRAFT.I4/chapter.tex'
ref = shared.ref


def main():
    assert not (BASE / 'source-audit.json').exists(), 'Preserve reviewed source audit'
    snapshots = BASE / 'source-snapshot'; snapshots.mkdir(exist_ok=True)
    names = ['artifacts_v12.py', 'operation_contract_v12.py', 'operation_service_v12.py',
             'runtime_v12.py', 'worker_v12.py', 'cli_v12.py', 'mcp_server_v12.py',
             'responses.py', 'causal_workflow.py']
    captured = []
    fingerprint = {}
    for name in names:
        p = ROOT / 'src/causalbank' / name
        q = snapshots / name; q.write_bytes(p.read_bytes())
        captured.append({'original_path': str(p.relative_to(ROOT)),
                         'snapshot': ref(q, 'Preserved selected runtime identity input')})
        fingerprint[name] = hashlib.sha256(q.read_bytes()).hexdigest()
    for name in ['request-schema.json', 'response-schema.json']:
        p = ROOT / 'docs/program/repair-v12/work/IN02' / name
        q = snapshots / name; q.write_bytes(p.read_bytes())
        captured.append({'original_path': str(p.relative_to(ROOT)), 'snapshot': ref(q, 'Preserved schema identity input')})
        fingerprint[name] = hashlib.sha256(q.read_bytes()).hexdigest()
    source_digest = hashlib.sha256(json.dumps(fingerprint, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    faults_path = ROOT / 'docs/program/execution/2026-10-13/prototype-review/runtime-replay/faults.json'
    faults = json.loads(faults_path.read_text()); shared.verify_refs(faults)
    cases = [{'case': x['case'], 'status': x['status']} for x in faults['cases']]
    assert len(cases) == 9 and all(x['status'] == 'pass' for x in cases)
    restart = next(x for x in faults['cases'] if x['case'] == 'kill_restart_checkpoint')['terminal']
    assert restart['state'] == 'completed' and restart['spawn_attempts'] == 2
    assert len(restart['completed_work_ids']) == len(set(restart['completed_work_ids'])) == 100
    core.write(BASE / 'source-and-fault-review.json', {
        'status': 'pass', 'issues': [], 'source_snapshot': captured,
        'snapshot_source_digest': source_digest,
        'matches_fault_execution_source_digest': source_digest == faults['execution_identity']['source_sha256'],
        'faults': ref(faults_path, 'Actual preserved nine-case replay; not new execution'),
        'fault_execution_identity': faults['execution_identity'], 'fault_executed_at': faults['executed_at'],
        'fresh_mcp_run': faults['fresh_mcp_run'], 'cases': cases,
        'restart': {'distinct_committed_work_ids': 100, 'worker_starts': 2},
        'inspected_anchors': {'runtime_v12.py': ['execution_identity', '_replay_or_run', '_run_sync', 'resume', '_report_worker'],
            'artifacts_v12.py': ['atomic', 'bounded_read', 'ArtifactStore.put', 'ArtifactStore.get'],
            'worker_v12.py': ['main: RLIMIT_AS and wall timer'],
            'operation_service_v12.py': ['request_digest: excluded request_id and idempotency_key']},
        'source_findings': ['Selected fingerprint is not a complete transitive environment lock.',
            'Canonical output budget is checked after collection; worker memory bound does not include the parent/SDK.',
            'Content and metadata publications are individually atomic, not a general distributed transaction.',
            'Report checkpoints bind prefix, summaries and selected identities; retries keep the original local wall deadline.',
            'No external bank-action operation or distributed exactly-once result is established.'],
        'new_runtime_trials': 0, 'target_platform_qualification': False})
    code = ROOT / 'tools/operation_planning_examples_20261013.py'
    replay = subprocess.check_output([sys.executable, str(code)], timeout=15)
    assert replay == (BASE / 'exact-results.json').read_bytes()
    (BASE / 'exact-replay.json').write_bytes(replay)
    # Independently enumerate equally weighted latent types and discrete draws.
    successes = attempts = 0
    for latent, a, b, c in product(range(10), repeat=4):
        for draw in [a, b, c]:
            attempts += 1
            if latent != 0 and draw != 0:
                successes += 1
                break
    assert F(successes, 10000) == F(8991, 10000)
    assert F(attempts, 10000) == F(1299, 1000)
    s = a = 0
    for draws in product(range(5), repeat=3):
        for draw in draws:
            a += 1
            if draw:
                s += 1
                break
    assert F(s,125) == F(124,125) and F(a,125) == F(31,25)
    all_net = (70*10+15*(-30)-100*2-15*20)/F(100)
    complete_net = (70*10+15*(-30))/F(85)-2
    assert all_net == F(-5,2) and complete_net == F(16,17)
    assert 1-F(19,20)**3 == F(1141,8000)
    core.write(BASE / 'exact-review.json', {'status': 'pass', 'issues': [],
        'replay': ref(BASE / 'exact-replay.json', 'Byte-identical arithmetic replay'),
        'results': ref(BASE / 'exact-results.json', 'Four stipulated finite constructions'),
        'independent_checks': ['10,000 equally weighted persistent-type/three-draw worlds give success 8991/10000 and expected attempts 1299/1000.',
            '125 transient-only worlds give success 124/125 and expected attempts 31/25.',
            '100-request count account independently gives all-attempt net -5/2 and completed-only 16/17.',
            'Independent complement calculation gives selective-null rejection probability 1141/8000.'],
        'review_code': ref(Path(__file__), 'Independent enumeration and inspected-source review'),
        'new_runtime_trials': 0, 'empirical_prices_or_reliability': False})
    common = {'author': 'Causal banking proposal project', 'year': 2026,
              'version_date': '2026-10-13 project review; preserved trial timestamp stated separately'}
    sources = [
        {**common, 'integrated_citation_key': 'exec13_ops_source', 'kind': 'project_source',
         'title': 'Local runtime identity, checkpoint, publication and resource boundaries',
         'source_identity': 'Selected reviewed local Python sources and schema snapshot',
         'local_copy': ref(snapshots / 'runtime_v12.py', 'execution_identity, replay, resume, report worker'),
         'snapshot': captured, 'review': ref(BASE / 'source-and-fault-review.json', 'Inspected code and stated limits'),
         'inspected_anchors': ['execution_identity', '_replay_or_run', '_run_sync', 'resume', '_report_worker', 'atomic', 'ArtifactStore.put', 'worker main', 'request_digest'],
         'supported_claims': ['The selected request/code/dependency identity is checked for replay and resume.',
             'The worker has local resource limits; the parent collects output before canonical size validation.',
             'Local report checkpoints bind completed prefix and summaries; starts are capped at three under the original deadline.',
             'Artifact content, metadata and job state have separate atomic publication boundaries.'],
         'limits': 'Static source inspection and preserved fixtures; not complete environment, multi-host, arbitrary-adapter or bank-action qualification.'},
        {**common, 'integrated_citation_key': 'exec13_ops_faults', 'kind': 'project_evidence',
         'title': 'Preserved local runtime fault replay and restart identities',
         'source_identity': 'Nine actual recorded author fault fixtures with source and execution identities',
         'local_copy': ref(faults_path, 'cases, limits, execution_identity, fresh_mcp_run'),
         'review': ref(BASE / 'source-and-fault-review.json', 'Nine pass outcomes and 100 unique completed IDs'),
         'inspected_anchors': ['cases[*].case/status', 'kill_restart_checkpoint.terminal', 'execution_identity', 'fresh_mcp_run'],
         'supported_claims': ['The nine specified preserved fault cases passed.',
             'The preserved restart case completed 100 distinct report work IDs after two worker starts.',
             'The later local replay was not a fresh MCP transport trial.'],
         'limits': 'Deterministic selected local trials do not estimate a production failure probability or service-level objective.'},
        {**common, 'integrated_citation_key': 'exec13_ops_exact', 'kind': 'project_derivation',
         'title': 'Exact retry, recovery, selective-redraw and all-attempt cost constructions',
         'source_identity': 'Stipulated finite probability laws and pure keyed reduction',
         'local_copy': ref(BASE / 'exact-results.json', 'Exact finite outcomes'),
         'code': ref(code, 'Reproducible standard-library construction'),
         'review': ref(BASE / 'exact-review.json', 'Independent finite enumeration and count account'),
         'inspected_anchors': ['selection_cost', 'retry', 'keyed_recovery', 'selective_redraw'],
         'supported_claims': ['Naive duplicated contribution totals 90; keyed total is 130.',
             'Persistent failure mixture gives success .8991 instead of the incorrect .993141 marginal-IID result.',
             'Completed-only cost comparison is 16/17 while the all-attempt account is -5/2.',
             'Selecting any of three independent uniform-null p-values below .05 has probability .142625.'],
         'limits': 'Exact project counterexamples only; no measured prices, reliability, harmful runtime behavior or bank outcomes.'}]
    core.write(BASE / 'source-audit.json', {'sources': sources, 'cutoff': '2026-10-07',
        'project_work_date': '2026-10-13', 'new_external_sources': 0, 'new_runtime_trials': 0})
    shared.verify_refs(json.loads((BASE / 'source-audit.json').read_text()))
    inherited = (BASE / 'inherited-operations.tex').read_text()
    marker = r'\section{The next complete qualification}'
    expected = inherited.replace(marker, (BASE / 'development.tex').read_text()+'\n'+marker)+'\n'+r'\label{exec13:operations-end}'+'\n'
    assert CHAPTER.read_text() == expected
    review = {'status': 'pass', 'issues': [], 'reviewer': {'name': 'Codex author/coordinator', 'kind': 'author'},
        'scope': 'Developed proposal operating chapter, preserving earlier text and narrowing runtime claim boundaries',
        'chapter': ref(CHAPTER, 'Connected banking consequences, notation, invariants, alternatives and diagnostics'),
        'criteria': [
            {'index': 0, 'verdict': 'pass', 'finding': 'Develops analysis identity, recovery invariant, bounded/persistent retries, statistical selection, cancellation, semantic compatibility, ownership and all-attempt economic accounting with exact examples.'},
            {'index': 1, 'verdict': 'pass', 'finding': 'Implementation claims bind inspected source and actual preserved receipts; mathematical examples are declared assumptions and new code reproduces them. No platform, owner or cost receipt is invented.'}],
        'evidence': [ref(BASE / n, n) for n in ['plan-review.md', 'source-audit.json', 'source-and-fault-review.json', 'exact-review.json']],
        'limits': ['No new local fault/MCP run, target-platform trial or institution acceptance.',
                   'A selected source fingerprint is not a full reproducible environment manifest.',
                   'This chapter draft does not close all MR03 requirements or depth acceptance.'],
        'visual_acceptance': False, 'independent_review': False, 'runtime_qualification': False}
    core.write(BASE / 'author-review.json', review)
    print(json.dumps({'review': 'pass', 'sources': 3, 'recorded_fault_cases': 9,
        'matches_fault_source_digest': source_digest == faults['execution_identity']['source_sha256'],
        'new_runtime_trials': 0}))


if __name__ == '__main__':
    main()

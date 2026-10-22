#!/usr/bin/env python3
"""Freeze inspected manual evidence and exact authored replay arithmetic once."""
import json
from pathlib import Path

import acquire_computation_workflow_20261022 as acquisition
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write
import workflow_replay_reference_20261022 as replay

ROOT = acquisition.transport.ROOT
BASE = acquisition.BASE
read = lambda p: json.loads(p.read_text())

# All anchors refer to newline-delimited inert extractions, original HTML authoritative.
SOURCES = [
    dict(id='databricks_repair', title='Troubleshoot and repair job failures',
        author='Databricks', edition='Databricks on AWS; last updated 9 October 2026',
        temporal='Explicitly post-cutoff; excluded from cutoff-era capability acceptance.',
        anchors=[(4, 4), (23, 37), (40, 45)],
        claims=['Partial repair reruns unsuccessful/dependent tasks using current job/task settings.',
            'Each unsuccessful task restarts; the manual explicitly warns that Jobs does not make tasks idempotent and partial append writes may duplicate data.',
            'Shared job clusters are recreated using current settings; repair parameters can override earlier values.']),
    dict(id='databricks_monitor', title='Monitor job runs', author='Databricks',
        edition='Databricks on AWS; last updated 15 October 2026',
        temporal='Explicitly post-cutoff; excluded from cutoff-era capability acceptance.',
        anchors=[(4, 7), (38, 40), (47, 58), (78, 85), (105, 118)],
        claims=['The inspected page gives a 48-hour finished-run graph and 60-day job/pipeline run history.',
            'Succeeded with failures is a distinct outcome, with job result semantics explained in terms of leaf tasks.',
            'One-time runs/submit jobs have no saved job name; Run ID is needed for that search.']),
    dict(id='snowflake_graphs', title='Task graphs', author='Snowflake',
        edition='Mutable official task-graph manual retrieved 22 October 2026; historical/API revision unverified',
        temporal='No authenticated cutoff revision. Current observations only; historical capability acceptance withheld.',
        anchors=[(4, 8), (38, 56), (59, 69), (93, 109), (126, 165), (206, 214)],
        claims=['Task graphs describe an execution dependency DAG, not a causal-identification result.',
            'Suspended child tasks can be treated as succeeded; a finalizer does not start if the root is skipped.',
            'Task-graph versions include task properties but not called stored-procedure definitions; changed procedures may run within a current graph run.',
            'The inspected page describes retry, overlap and configuration mechanisms; pin their exact edition before historical claims.']),
    dict(id='azure_reuse', title='Debug pipeline reuse issues in Azure Machine Learning',
        author='Microsoft', edition='Azure ML API v2; displayed ms.date 30 March 2026; HTML updated_at 19 October 2026',
        temporal='Displayed date does not authenticate cutoff-era bytes; HTML metadata is post-cutoff. Historical acceptance withheld.',
        anchors=[(15, 16), (25, 43), (44, 60), (75, 82)],
        claims=['Reuse requires is_deterministic=true, ForceReRun=false and matching code/environment/inputs/parameters/output/run settings.',
            'Reused components display earlier status, output, logs and metrics; ForceReRun children cannot be reused by other jobs.',
            'Determinism is declared; false causes rerunning. Snapshot/environment comparisons help diagnose reuse.',
            'Authorization banners are present but the technical body was returned and inspected.']),
    dict(id='dataiku_scenarios', title='Automation scenarios', author='Dataiku',
        edition='Latest URL resolved to DSS 15; historical edition/date unverified',
        temporal='No authenticated cutoff edition; index-level current observations only.',
        anchors=[(1, 1), (70, 100), (103, 121), (150, 158)],
        claims=['The page identifies DSS 15 and indexes automation, build/check/metrics/code steps, triggers and failure/conditional-execution topics.',
            'This index does not establish detailed transaction, retry, concurrency or failure semantics; linked technical originals remain unread.']),
    dict(id='aws_errors', title='Handling errors in Step Functions workflows', author='Amazon Web Services',
        edition='Mutable latest Developer Guide retrieved 22 October 2026; cutoff/API revision unverified',
        temporal='No authenticated cutoff revision. Current observations only; historical capability acceptance withheld.',
        anchors=[(11, 17), (29, 39), (58, 69), (80, 112), (147, 179), (180, 228)],
        claims=['Task/Parallel/Map catchers do not catch top-level execution failures.',
            'Current States.ALL excludes DataLimitExceeded/Runtime; the current manual explicitly allows a named DataLimitExceeded retry/catch, whereas Runtime is non-retryable.',
            'Retriers and catchers are ordered; retry counts reset for eligible states on redrive; MaxAttempts counts retries.',
            'Retries are billed as state transitions; actual total cost needs a separately pinned pricing/deployment/workflow contract.']),
]


def main():
    assert not (BASE / 'review.json').exists(), 'Preserve frozen review; use a successor.'
    verify_bindings(read(BASE / 'plan-review.json'))
    sources, attempts = [], []
    for source in SOURCES:
        identifier = source['id']
        receipt_path = BASE / 'acquisition/network' / (identifier + '.receipt.json')
        receipt = read(receipt_path)
        prior = read(BASE / 'acquisition/sandbox' / (identifier + '.receipt.json'))
        assert prior['returncode'] == 6
        assert receipt['returncode'] == 0 and receipt['format_valid']
        original = ROOT / receipt['local_copy']
        binding = ref(original, 'Authentic official HTML, not an agent summary')
        assert binding['sha256'] == receipt['sha256']
        assert original.stat().st_size == receipt['bytes']
        text_path = BASE / 'extracted' / (identifier + '.txt')
        lines = text_path.read_text().splitlines()
        anchors = []
        for start, end in source['anchors']:
            assert 1 <= start <= end <= len(lines)
            anchors.append(dict(anchor=f'extracted lines {start}-{end}',
                inspected_text='\n'.join(lines[start-1:end])))
        if identifier == 'azure_reuse':
            html = original.read_text()
            assert '2026-03-30T00:00:00Z' in html and '2026-10-19T22:12:00Z' in html
            anchors.append(dict(anchor='original HTML meta ms.date, updated_at, gitcommit',
                inspected_text='ms.date=2026-03-30T00:00:00Z; updated_at=2026-10-19T22:12:00Z; '
                    'gitcommit=3e93bdb19c5ffcfbdd60f01ccb4dd44a195c53a5'))
        sources.append(dict(integrated_citation_key='exec22_workflow_' + identifier,
            kind='official_documentation', title=source['title'], author=source['author'],
            year=2026, source_identity=receipt['url'], version_date=source['edition'],
            accessed_utc=receipt['finished_at'], local_copy=binding,
            text_copy=ref(text_path, 'Inert extraction; original authoritative'),
            acquisition_receipt=ref(receipt_path, 'Bound transport receipt'),
            inspected_anchors=anchors, supported_claims=source['claims'],
            historical_limit=source['temporal'], cutoff_eligible=False,
            native_execution=False,
            unsupported=['Unchanged cutoff-era capabilities', 'Complete market coverage',
                'Causal correctness or calibrated uncertainty', 'Native adapter acceptance',
                'License/price/ROI or superiority claims']))
        attempts.append(dict(id=identifier,
            sandbox=ref(BASE / 'acquisition/sandbox' / (identifier + '.receipt.json'), 'Preserved DNS failure'),
            network=ref(receipt_path, 'Separate successful network attempt')))
    audit = dict(cutoff='2026-10-07T15:59:59Z', sources=sources,
        survey_acceptance=False, current_observations_only=True)
    verify_bindings(audit)
    write(BASE / 'source-audit.json', audit)
    write(BASE / 'acquisition-review.json', dict(status='six_current_official_manuals_acquired',
        attempts=attempts, failures_preserved=True, downloaded_code_executed=False,
        historical_acceptance=False))
    extra = [
        dict(family='SAS Viya', status='unread_candidate',
            next_action='Resolve orchestration product/release; acquire cutoff technical and licensed-runtime originals.'),
        dict(family='Domino', status='unread_candidate',
            next_action='Acquire pinned job/environment, retry, lineage and deployment/entitlement originals.'),
        dict(family='Posit Workbench/Connect', status='unread_candidate',
            next_action='Resolve product boundaries; inspect pinned scheduled-content/job, environment and failure-history manuals.'),
    ]
    candidates = [dict(family=s['author'] + ': ' + s['title'],
        status='current_primary_text_inspected_historical_coverage_open',
        evidence=ref(BASE / 'source-audit.json', s['id']),
        next_action=('Acquire detailed linked scenario pages and cutoff DSS edition; do not infer semantics from headings.'
            if s['id'] == 'dataiku_scenarios' else
            'Recover a publicly authenticated cutoff revision or retain a temporal omission; inspect pinned runtime/API, licensed terms and full cost separately.'))
        for s in SOURCES]
    write(BASE / 'omissions-register.json', dict(candidates=candidates + extra,
        crosscutting=['Complementary market discovery, deployment editions and canonical aliases.',
            'Exact cutoff revisions and broader source-based comparison before any absence finding.',
            'Native replay/adapter behavior, license/terms/prices and measured full workflow cost.',
            'Main-reader integration of this reviewed comparison and exact authored example.'],
        global_blocker=None, bank_input_required_for_next_public_work=False))
    write(BASE / 'exact-results.json', replay.calculate())
    assert read(BASE / 'exact-results.json') == replay.calculate()
    evidence = [ref(BASE / name, anchor) for name, anchor in [
        ('plan-review.json', 'Reviewed bounded plan'), ('source-audit.json', 'Six inspected authentic manuals'),
        ('acquisition-review.json', 'Six failures preserved alongside separate successes'),
        ('omissions-register.json', 'Candidate-specific next actions and coverage limits'),
        ('comparison.md', 'Connected comparison, contract and public known-law protocol'),
        ('exact-results.json', 'Exact finite-table results')]]
    evidence += [ref(Path(__file__), 'Exact audit/review generator'),
        ref(ROOT / 'tools/workflow_replay_reference_20261022.py', 'Executable authored reference')]
    write(BASE / 'review.json', dict(status='pass_for_inspected_current_source_preflight',
        reviewer=dict(name='Codex author/coordinator', kind='author'), evidence=evidence,
        checks=replay.calculate()['checks'], current_manuals=6, families_inspected=5,
        cutoff_accepted_manuals=0, candidate_frame_complete=False,
        native_execution=False, survey_acceptance=False, main_reader_integration=False,
        findings=['Post-cutoff/undated mutable bytes are not promoted into cutoff-era capability findings.',
            'A documented scheduler or cache does not by itself preserve scientific target/data/code identity.',
            'The exact authored example separates replay equivalence from causal and statistical validity.',
            'Public fixture work can proceed independently of costly bank studies and native commercial trials.'],
        unresolved=['Cutoff revisions for all six manuals', 'Three unread families and complementary discovery',
            'Detailed Dataiku technical pages', 'License/prices and native adapters',
            'Connected main-reader integration'], issues=[]))
    next_action=('Integrate the reviewed commercial workflow comparison and exact replay example into the existing '
        'computation chapter with explicit post-cutoff/current-observation limits. Recover cutoff revisions and '
        'Dataiku technical originals; inspect SAS Viya, Domino and Posit and complementary discovery; retain '
        'native/licensing/cost unknowns. Current manuals do not close historical coverage. Independent census, '
        'reuse and Python IV/RD work remains eligible.')
    write(BASE / 'inspection-progress.json', dict(
        finding='Six official manuals across five commercial workflow families inspected; all cutoff editions remain unverified. '
            'Exact authored replay demonstrates duplicate-weight bias, target/vintage drift and manifest checks. '
            'Six failed sandbox attempts preserved with separate successful acquisitions; no coverage/native acceptance.',
        next_action=next_action, evidence=[ref(BASE / 'review.json', 'Reviewed actual preflight evidence')],
        coverage_acceptance=False, global_blocker=None,
        yield_reason='Freeze completed source preflight and arithmetic for integrated synthesis and program/Git preservation. '
            'This yields the active lease, not the remaining work or user authorization.'))
    print(json.dumps(dict(status='reviewed_current_source_progress', manuals=6,
        historical_accepted=0, exact_checks=len(replay.calculate()['checks']),
        survey_acceptance=False, main_reader_integration=False)))


if __name__ == '__main__':
    main()

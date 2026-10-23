#!/usr/bin/env python3
"""Bind inspected commercial workflow delegates to authenticated primary bytes."""
import hashlib
import json
from pathlib import Path

import workflow_delegate_reference_20261023 as exact
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'docs/literature/raw'
BASE = ROOT / 'docs/program/execution/2026-10-23/workflow-delegates-v2'
PRIOR = ROOT / 'docs/program/execution/2026-10-23/commercial-workflow-recovery-v1'
read = lambda p: json.loads(p.read_text())
LIMITS = [
    'Static inspection of selected cutoff client/SDK files; no downloaded code, tests or commercial servers execute.',
    'Authenticated client commits do not establish a distributed release or complete server/API compatibility matrix.',
    'Mock tests, source comments and conformance scenarios describe intent and selected checks, not observed runtime conformance.',
    'An open client license grants no commercial server entitlement, dependency clearance or verified price.',
    'Dataiku historical originals, server schemas, REST manuals, native trials, wider coverage and visual/final acceptance remain open.'
]
# Every listed span was read directly. Other bytes receive no technical claim.
SPECS = {
 'sasctl_00': [
    (61, 105, 'core.request', 'Service.request prefixes the service root and delegates kwargs to core.request; Service.get maps HTTP 404 to None.'),
    (399, 436, 'max_retries=60', 'The generic Service._monitor_job accepts completed and failed as terminal, sleeps 0.5 seconds per poll and bounds refresh count, not request duration. The inspected Workflow method is not shown to call this helper.')],
 'sasctl_01': [
    (617, 702, 'timeout=None', 'Session.request forwards timeout, default None, and repeats a request once after a 401 with an access-token-expired challenge when refresh succeeds.'),
    (1469, 1588, 'ThreadPoolExecutor', 'PageIterator derives offset and limit from the next link, schedules offset requests and stops on an empty page; this code does not establish a snapshot-consistent sampling frame.'),
    (1590, 1655, 'approximate count', 'PagedItemIterator documents length as an approximate count, including possible permission-related differences.'),
    (2015, 2080, '400 <= response.status_code', 'The top-level request delegate raises HTTPError for status 400 through 599, then converts the requested response format.'),
    (2113, 2133, 'link["method"]', 'request_link uses the method and href stored in the resource link.')],
 'sasctl_02': [(25, 39, 'JobTimeoutError', 'JobTimeoutError inherits RuntimeError; ServiceUnavailableError explicitly allows missing license/components or temporary outage as alternatives.')],
 'sasctl_03': [(102, 165, 'mock.patch', 'Workflow submission unit tests mock definition lookup and POST; they check URL/prompt formatting and string datetime conversion without contacting a server.')],
 'dominopy_00': [(53, 63, '/runs/', 'Legacy run routes differ from the v4 job routes.'),
                 (207, 248, '/v4/jobs/', 'The selected client routes start, stop, status, restart and execution details through v4/jobs endpoints.')],
 'dominopy_01': [(33, 55, 'status_forcelist', 'The HTTPS adapter supplies Retry total default four, backoff factor one and status list 408/502/503/504, without an explicit allowed_methods override. POST retry behavior is not established without the dependency policy.'),
                 (56, 101, 'HTTPStatus.CONFLICT', 'Verb wrappers forward kwargs without setting an overall deadline; HTTP 409 is converted into ReloginRequiredException while other HTTP errors are re-raised.')],
 'dominopy_02': [(1, 5, 'DominoException(Exception)', 'The selected Domino exception base directly inherits Exception.'),
                 (95, 100, 'ReloginRequiredException(DominoException)', 'ReloginRequiredException inherits DominoException, rather than the RequestException ignored by the blocking helper default.')],
 'dominopy_03': [(1, 130, '9.9.9', 'Unit fixtures supply a mock version 9.9.9 and Queued/Succeeded job dictionaries; these do not identify a supported real server schema.'),
                 (350, 365, 'isCompleted', 'The happy-path blocking unit test supplies a completed Succeeded response.'),
                 (539, 581, 'skipif', 'Unit tests specify ignored RequestException versus immediate propagation when ignore_exceptions is empty; live tests are conditional on server reachability. No tests were run here.')],
 'positgo_00': [(1, 75, 'SchedulerClient', 'The scheduler example separates the product/Launcher protocol from a SchedulerClient backend interface.'),
                (140, 187, 'default:', 'The template proposes status polling and maps unrecognized scheduler status to Pending; that illustrative mapping is not a complete scheduler contract.'),
                (190, 232, 'RunWorkflows', 'The guide asks implementers to provide a scheduler backend and explicitly configured conformance profile.')],
 'positgo_01': [(138, 176, 'non-zero exit code', 'Failed means launch failure while Finished includes a launched process with nonzero exit; terminal status includes Canceled, Failed, Finished and Killed.'),
                (349, 405, 'ExitCode *int', 'Job status, status reason/code, optional PID and optional process exit code are distinct fields.')],
 'positgo_02': [(15, 181, 'NetworkAvailable bool', 'Profile requires job factories and stop/kill status/exit-code expectations. Optional output/network/suspend switches govern coverage. The NetworkAvailable comment says default true, but the inspected applyDefaults sets only durations; an omitted Go bool remains false.'),
                (409, 450, '200 * time.Millisecond', 'The terminal-regression invariant waits for a terminal state and compares it with one revisit after 200 milliseconds; this is a finite check, not proof of permanent stability.')],
 'positgo_03': [(14, 154, 'if profile.NetworkAvailable', 'RunWorkflows invokes launch/stop/kill/cancel/list and conditional suspend; launch network and output checks depend on profile booleans.'),
                (300, 401, 'ExpectExitCodes', 'Stop and Kill scenarios use separate wait contexts and verify configured terminal status and exit code.'),
                (408, 438, 't.Skipf', 'RunCancelJob skips on any returned cancellation API error, with a possible start race as its explanation; the skip branch does not first prove that race.'),
                (691, 708, 'job.ExitCode == nil', 'The exit-code assertion rejects a missing exit code when acceptable values are declared.')],
}


def main():
    assert not (BASE / 'source-audit.json').exists(), 'Preserve reviews; use a successor.'
    selection = read(BASE / 'source-selection.json')['selected']
    assert len(selection) == 12
    inventories, sources = [], []
    for group, author, title in [
        ('sasctl', 'SAS Institute', 'SAS sasctl service, request, pagination and workflow-test delegates'),
        ('dominopy', 'Domino Data Lab', 'Domino Python client routes, retry exceptions and job-test contracts'),
        ('positgo', 'Posit PBC', 'Posit Launcher job state, scheduler template and conformance profiles'),
    ]:
        cp, tp = [RAW / f'exec23_workflow_{group}_{n}.json' for n in ['cutoff', 'tree']]
        commit, tree = read(cp)[0], read(tp)
        assert not tree['truncated'] and tree['sha'] == commit['commit']['tree']['sha']
        for p in [cp, tp]:
            rec = read(p.with_suffix('.receipt.json'))
            assert rec['status'] == 'saved' and rec['sha256'] == hashlib.sha256(p.read_bytes()).hexdigest()
        entries = {r['path']: r for r in tree['tree']}
        records = []
        for row in [s for s in selection if s['candidate'] == group]:
            assert row['commit'] == commit['sha'] and row['tree'] == tree['sha']
            assert row['date'] == commit['commit']['committer']['date'] < '2026-10-07T16:00:00Z'
            p = RAW / (row['id'] + '.txt')
            rp, data = p.with_suffix('.receipt.json'), p.read_bytes()
            blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + bytes([0]) + data).hexdigest()
            rec = read(rp)
            url = f'https://raw.githubusercontent.com/{row["repository"]}/{row["commit"]}/{row["path"]}'
            assert row['blob'] == entries[row['path']]['sha'] == blob
            assert row['size'] == entries[row['path']]['size'] == len(data)
            assert rec['status'] == 'saved' and rec['url'] == url and rec['sha256'] == hashlib.sha256(data).hexdigest()
            lines, anchors = data.decode().splitlines(), []
            for first, last, token, claim in SPECS[row['id'].removeprefix('exec23_workflow_v2_')]:
                excerpt = '\n'.join(lines[first-1:last])
                assert token in excerpt, (row['id'], first, last, token)
                anchors.append(dict(anchor=f'{row["path"]} lines {first}-{last}', inspected_text=excerpt, supported_claim=claim))
            records.append(dict(source_identity=url, version_date=row['date']+'; '+row['commit'],
                local_copy=ref(p, 'Authenticated primary bytes; only listed spans inspected'),
                acquisition_receipt=ref(rp, 'Acquisition hash'), git_blob_sha1=blob,
                inspected_anchors=anchors, supported_claims=[a['supported_claim'] for a in anchors],
                technical_inspected=True, executed=False))
        inventories += records
        sources.append(dict(integrated_citation_key='exec23_workflow_delegates_'+group,
            kind='software_primary_sources', title=title, author=author, year=2026,
            source_identity='https://github.com/'+next(s['repository'] for s in selection if s['candidate']==group)+'/tree/'+commit['sha'],
            version_date=commit['commit']['committer']['date']+'; '+commit['sha'],
            local_copy=records[0]['local_copy'], identity_evidence=[ref(cp,'Cutoff commit'),ref(tp,'Complete tree')],
            records=records, inspected_anchors=[a['anchor'] for r in records for a in r['inspected_anchors']],
            supported_claims=[c for r in records for c in r['supported_claims']], limitations=LIMITS))
    sources.append(dict(integrated_citation_key='exec23_workflow_delegates_reference',
        kind='project_derivation_and_exact_reference', title='Exact authored workflow deadline, sampling-frame and completion witnesses',
        author='Causal banking proposal project', year=2026, source_identity='tools/workflow_delegate_reference_20261023.py',
        version_date='2026-10-23; supplied laws and prices', local_copy=ref(Path(exact.__file__),'calculate(): exact rational witnesses'),
        inspected_anchors=['calculate(): polling, changing_frame, terminal_accounting, finite_revisit'],
        supported_claims=['Three supplied polls use 3/2 seconds of sleep and 15/2 seconds including requests.',
            'A changing offset frame omits initial ID 3 and changes a binary mean from 1/2 to 1/3.',
            'Four supplied terminal records contain one accepted artifact; stipulated cost per terminal/accepted is USD 3/12.',
            'Agreement at two finite observation times does not establish permanent state stability.'], limitations=LIMITS))
    write(BASE/'source-audit.json',dict(cutoff='2026-10-07',sources=sources,native_execution=False))
    write(BASE/'inspected-source-inventory.json',dict(authenticated_blobs=12,inspected_blobs=12,records=inventories))
    write(BASE/'exact-results.json',exact.calculate())
    write(BASE/'omissions-register.json',dict(predecessor=ref(PRIOR/'omissions-register.json','Preserved vendor omissions'),
        items=[
            dict(gap='SAS public server REST/workflow contract',action='Acquire immutable cutoff REST/workflow manuals and declared supported server versions. The generic monitor is not shown to be the workflow execution path.'),
            dict(gap='Domino supported server terminal schema',action='Acquire a version-bound schema for v4/jobs and error semantics. Mock version 9.9.9 and selected tests are not the schema; authenticate HTTP dependency policies before asserting POST retries.'),
            dict(gap='Posit backend and server conformance',action='Select a concrete scheduler/plugin and product versions, state mapping, explicit profile switches and qualified exit codes; register native checks, error classification and skipped-test accounting.'),
            dict(gap='Dataiku historical original',action='Retain the 15.0.2 temporal omission until immutable cutoff technical bytes are acquired; current manuals retain only their stated scope.'),
            dict(gap='Rights, prices and native trials',action='Keep client licensing, server entitlement, transitive notices, quoted costs and actual native/scientific trials as separate obligations; no entitlement or native success is inferred.')],
        whole_cell_complete=False))
    write(BASE/'conversion-contract.json',dict(status='proposed_not_implemented',integration_allowed=False,native_execution=False,
        requirements=[
            'Use a monotonic overall observation deadline plus bounded transport requests; timeout leaves remote state unknown until reconciliation.',
            'Separate stable scientific request identity, each attempt, authentication refresh, error class and remote cancellation confirmation.',
            'Freeze or reconcile membership, permissions, sort order and dataset revision before treating paged workflow records as a sampling frame.',
            'Require declared success state, allowed exit code, bound artifact and scientific validation separately from terminal status.',
            'Preserve native unknown states; explicitly configure conformance switches and distinguish pass, fail, skip and unsupported.',
            'Qualify cancellation races using observed state and classify every remaining API error; a skipped test is not cancellation success.']))
    evidence=[ref(BASE/n,'Inspected delegates and exact authored argument') for n in ['plan.md','plan-review.json','acquisition-verification.json','source-audit.json','inspected-source-inventory.json','exact-results.json','conversion-contract.json','omissions-register.json']]
    evidence += [ref(Path(__file__),'Span verification and authentication'),ref(Path(exact.__file__),'Exact authored calculations')]
    review=dict(status='pass_for_scoped_delegate_comparison_with_limits',reviewer=dict(name='Codex author/coordinator',kind='author'),
        evidence=evidence,findings=[
            'Twelve blobs authenticate and listed primary spans support three complementary delegate profiles.',
            'SAS generic count-limited monitoring, transport deadlines and paged membership remain separate contracts.',
            'Domino retry method policy is unresolved; ReloginRequiredException is not the default ignored RequestException.',
            'Posit Finished may have a nonzero exit. Explicit profile booleans and broad cancellation skips constrain conformance evidence.',
            'Exact authored witnesses reproduce; no upstream behavior, paid entitlement or scientific capability is qualified.'],
        whole_cell_complete=False,integration_allowed=False,capabilities=[],native_execution=False,
        visual_acceptance=False,limitations=LIMITS)
    verify_bindings(review)
    write(BASE/'review.json',review)
    print(json.dumps(dict(authenticated_blobs=12,inspected_blobs=12,source_records=4,whole_cell_complete=False)))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Authenticate bounded vendor contracts and preserve explicit source omissions."""
import hashlib
import json
from pathlib import Path
import workflow_contract_reference_20261024 as exact
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'docs/literature/raw'
BASE = ROOT / 'docs/program/execution/2026-10-24/workflow-contracts-v3'
PRIOR = ROOT / 'docs/program/execution/2026-10-23/workflow-delegates-v2'
read = lambda p: json.loads(p.read_text())
LIMITS = [
    'Static inspection of pinned primary text only; no downloaded software, tests, licensed server or native integration executed.',
    'Repository identity and a historical client revision do not establish a complete product/server support matrix.',
    'The selected HTTP dependency profile fits inspected declared ranges, but no solved environment, distribution lock or runtime is established.',
    'Public client/SDK notices do not grant server entitlement or establish complete rights, prices, adoption or bank value.',
    'Whole-cell coverage, visual review and final proposal acceptance remain open.'
]

# These exact spans have been read. Acquired files without a span are not technical evidence.
SPECS = {
 'sassamples_file_0': [(1, 3, 'asynchronous', 'The preview Job Execution example separates an asynchronous execution job from its definition.'),
     (243, 262, 'failed', 'The sample polls the state link and distinguishes completed from failed, with a separate error member.'),
     (409, 427, 'provider specific', 'Result maps are provider-specific; logs and expiration/cleanup are separate. The submitter=workflow example supplies an event-origin tag.'),
     (1093, 1093, '2019', 'This example identifies document version 5 and an update date of 26 November 2019, not a supported server release.')],
 'sassamples_file_2': [(1, 27, 'case management', 'Visual Investigator workflow examples concern BPMN case management and must not be assumed to be the generic analytics workflow service.')],
 'sassamples_file_3': [(1, 3, 'preview', 'The repository explicitly calls itself preview examples, not a version-bound normative API schema.')],
 'dataiku_file_0': [(30, 46, 'wait_for_scenario_run(no_fail)', 'run_and_wait forwards no_fail to trigger waiting and then constructs a waiter without a None guard.'),
     (49, 95, 'trigger fire', 'A trigger fire is distinct from a scenario run and may be cancelled before any run is created.'),
     (710, 745, "'SUCCESS'", 'Completion tests presence of result; the strict path accepts SUCCESS and raises for WARNING, FAILED or ABORTED.'),
     (1018, 1042, 'self.scenario_run.run', 'The waiter dereferences scenario_run.run; a supplied None from cancelled-trigger no_fail handling is not guarded on this path.'),
     (1070, 1101, 'return None', 'Trigger cancellation returns None when no_fail=True; other cases raise or continue polling, with every tenth iteration refreshing cancellation state.')],
 'dataiku_file_2': [(1, 15, '14.7.3', 'The authenticated historical client identifies version 14.7.3.'),
     (29, 35, 'requests<3', 'Declared dependencies include requests<3 and python-dateutil, not a resolved lock.')],
 'dataiku_file_4': [(1, 14, 'Apache', 'The client notice refers to Apache 2.0; this is not a DSS server entitlement.')],
 'dataiku_extra_2': [(177, 204, '15000', 'Backoff starts at 200 ms, multiplies by 1.1 and caps each sleep at 15 seconds; no total observation deadline is defined by this helper.')],
 'dataiku_extra_3': [(1921, 1937, 'self._session.request', 'The inspected DSS HTTP call does not pass a timeout argument; no whole-operation time bound is established here.')],
 'domino_setup': [(40, 61, 'requests>=2.4.2', 'The pinned client setup allows requests>=2.4.2 and urllib3>=1.26.19,<3.' )],
 'domino_requirements': [(1, 13, 'requests~=2.31.0', 'The requirements file restricts requests to the 2.31 release line and permits urllib3>=1.26.19,<3; setup and requirements are distinct specifications.')],
 'requests231_file_0': [(135, 148, 'Retry.from_int', 'The adapter preserves a supplied Retry policy through Retry.from_int.'),
     (485, 498, 'retries=self.max_retries', 'The adapter passes its retry policy into connection-pool urlopen with redirects disabled at this layer.')],
 'requests231_file_1': [(5, 14, '2.31.0', 'The pinned Requests tag identifies version 2.31.0.')],
 'requests231_file_2': [(61, 68, 'urllib3>=1.21.1,<3', 'Requests 2.31.0 permits the selected urllib3 1.26.20 by its declared range; this is not environment resolution.')],
 'urllib126_file_0': [(228, 232, 'DEFAULT_ALLOWED_METHODS', 'The default allowed-method set excludes POST and PATCH.'),
     (342, 354, 'return retries', 'Retry.from_int returns an existing Retry object unchanged.'),
     (437, 489, 'not self._is_method_retryable', 'Status retries first test allowed methods. Read errors and connection errors are classified separately.'),
     (539, 560, 'self._is_connection_error', 'The connection-error branch lacks the method gate used by the read-error branch; a blanket no-POST-retry statement would be too broad.')],
 'urllib126_file_1': [(883, 896, 'retries.is_retry', 'Response retry follows the policy method/status predicate before incrementing and sleeping.')],
 'urllib126_file_2': [(1, 2, '1.26.20', 'The pinned urllib3 tag identifies version 1.26.20.')],
 'dominodocs_file_0': [(1, 2, 'redirects', 'The pinned api-docs repository describes a redirect site, not stored server schemas.')],
 'dominodocs_file_1': [(1, 13, 'en/latest/api_guide', 'The pinned index redirects to a mutable latest guide; it cannot authenticate historical v4/jobs response or error schemas.')],
 'positcpp_extra_0': [(202, 223, 'State::PENDING', 'The Local plugin launches an asynchronous child, stores its PID and publishes Pending before watching execution.'),
     (262, 298, 'State::FINISHED', 'The exit callback records ExitCode and sets non-killed jobs to Finished without requiring a zero exit code.')],
 'positcpp_extra_1': [(80, 85, 'does not support canceling', 'The sample Local backend explicitly does not support cancelJob.'),
     (119, 149, 'SIGTERM', 'Kill, resume, stop and suspend use different signals; kill and suspend/resume update state separately.')],
 'positcpp_extra_2': [(47, 67, 'node-connection-timeout-seconds', 'The default three-second setting concerns inter-node connections, not overall causal computation or job observation.')],
 'positcpp_extra_3': [(1, 30, 'v1.4', 'The historical guide cites Workbench 1.4 compatibility, later says 1.4 or greater, requires a launcher-enabled license and a test scheduler. It is not a current support matrix.')],
 'positcpp_extra_5': [(1, 34, 'not intended to replace integration testing', 'Smoke tests use explicit privilege and configuration choices, print responses for manual verification, and do not replace Launcher/product integration tests.'),
     (52, 56, 'Finished', 'The smoke guide describes Finished as without a failure; consumer interpretation must still preserve the executable exit-code behavior.')],
 'positcpp_extra_6': [(1, 20, 'commercial license agreement', 'The SDK notice provides permissive terms subject to its commercial-receipt exception; it does not license Workbench.')],
 'positcpp_extra_7': [(22, 58, '1.83.0', 'The build declares C++11, Boost default 1.83.0 and OpenSSL 1.1.1, distinct from the older prerequisites table.')],
}


def main():
    assert not (BASE/'source-audit.json').exists(), 'Preserve reviews; create a successor.'
    rows = []
    for name in ['dependency-source-selection.json','dependency-source-selection-2.json',
                 'vendor-source-selection-1.json','vendor-source-selection-2.json','vendor-source-selection-3.json']:
        rows += read(BASE/name)['selected']
    prior_tree=read(RAW/'exec23_workflow_dominopy_tree.json')
    for key,path in [('domino_setup','setup.py'),('domino_requirements','requirements.txt')]:
        item=next(x for x in prior_tree['tree'] if x['path']==path)
        rows.append(dict(id='exec24_workflow3_'+key, repository='dominodatalab/python-domino',
                         commit='c36d3cae32a7b97716dc75cbbfeac1899e113a41',**item))
    assert len(rows)==38 and len({x['id'] for x in rows})==38
    inventory=[]
    for row in rows:
        p=RAW/(row['id']+'.txt');b=p.read_bytes();r=read(p.with_suffix('.receipt.json'))
        blob=hashlib.sha1(b'blob '+str(len(b)).encode()+bytes([0])+b).hexdigest()
        assert blob==row['sha'] and len(b)==row['size']
        assert r['status']=='saved' and r['sha256']==hashlib.sha256(b).hexdigest()
        url=f'https://raw.githubusercontent.com/{row["repository"]}/{row["commit"]}/{row["path"]}'
        assert r['url']==url
        anchors=[];lines=b.decode().splitlines();key=row['id'].removeprefix('exec24_workflow3_')
        for first,last,token,claim in SPECS.get(key,[]):
            excerpt='\n'.join(lines[first-1:last]);assert token in excerpt,(key,first,last,token)
            anchors.append(dict(anchor=f'{row["path"]} lines {first}-{last}',inspected_text=excerpt,supported_claim=claim))
        inventory.append(dict(id=row['id'],repository=row['repository'],source_identity=url,
            version_date='Pinned cutoff revision '+row['commit'],local_copy=ref(p,'Authenticated original bytes'),
            acquisition_receipt=ref(p.with_suffix('.receipt.json'),'SHA-256 acquisition receipt'),git_blob_sha1=blob,
            inspected_anchors=anchors,supported_claims=[a['supported_claim'] for a in anchors],
            technical_inspected=bool(anchors),executed=False))
    sources=[]
    for key,author,title,repos in [
        ('sas','SAS Institute','SAS historical preview job execution and Visual Investigator workflow examples',['sassoftware/devsascom-rest-api-samples']),
        ('dataiku','Dataiku SAS','Dataiku 14.7.3 trigger, run, outcome and deadline source contracts',['dataiku/dataiku-api-client-python']),
        ('domino','Domino Data Lab and HTTP library contributors','Domino declared-range HTTP dependency profile and unresolved server schema',['dominodatalab/python-domino','psf/requests','urllib3/urllib3','dominodatalab/api-docs']),
        ('posit','Posit PBC','Posit C++ Local Launcher backend, exit codes and historical product profile',['rstudio/rstudio-launcher-plugin-sdk'])]:
        records=[x for x in inventory if x['repository'] in repos and x['technical_inspected']]
        sources.append(dict(integrated_citation_key='exec24_workflow_contracts_'+key,kind='software_primary_sources',
            title=title,author=author,year=2026,source_identity=records[0]['source_identity'],
            version_date='Immutable source revisions before 7 October 2026; versions and commit identities in records',
            local_copy=records[0]['local_copy'],records=records,
            inspected_anchors=[a['anchor'] for x in records for a in x['inspected_anchors']],
            supported_claims=[a for x in records for a in x['supported_claims']],limitations=LIMITS))
    sources.append(dict(integrated_citation_key='exec24_workflow_contracts_reference',kind='project_derivation_and_exact_reference',
        title='Authored trigger denominators, observation time and accepted-artifact costs',author='Causal banking proposal project',year=2026,
        source_identity='tools/workflow_contract_reference_20261024.py',version_date='24 October 2026; stipulated laws and costs',
        local_copy=ref(Path(exact.__file__),'Exact rational accounting'),inspected_anchors=['calculate(): four attempts and three sleeps'],
        supported_claims=['Four requested triggers create three runs and one accepted artifact; fractions are 1/4 and 1/3.',
            'Stipulated USD12 total costs yield USD4 per started run and USD12 per accepted artifact.',
            'Three stipulated backoff sleeps total331/500 seconds; three two-second requests give3331/500 seconds.'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(cutoff='2026-10-07',sources=sources,native_execution=False))
    write(BASE/'inspected-source-inventory.json',dict(authenticated_blobs=38,inspected_blobs=sum(x['technical_inspected'] for x in inventory),records=inventory))
    write(BASE/'exact-results.json',exact.calculate())
    searches=[]
    for p in sorted(RAW.glob('exec24_workflow3_search_*.json')):
        if p.name.endswith('.receipt.json'):continue
        j=read(p);searches.append(dict(source=ref(p,'Current repository discovery, not technical evidence'),total=j['total_count'],returned=len(j['items']),identities=[x['full_name'] for x in j['items']]))
    write(BASE/'search-screening.json',dict(cutoff='2026-10-07',searches=searches,
        rule='Current indexes identify leads; candidate technical sources are separately pinned before cutoff. No exhaustive market or absence claim.',
        domino_pages_reconciled=True,prior_omissions=ref(PRIOR/'omissions-register.json','Earlier coverage limits retained')))
    omissions=[
        dict(gap='Dataiku historical client versus server',progress='14.7.3 client and delegates authenticated; historical public client-byte gap narrowed.',action='Acquire immutable DSS 15.0.2/server workflow manuals, trigger precedence and support matrix; do not substitute older client evidence for newer server behavior.'),
        dict(gap='SAS normative and supported server schema',progress='Pinned preview REST examples establish job/state/result route and separate Visual Investigator workflow.',action='Acquire normative version-bound workflow/REST schemas, complete error states, server compatibility and timezone rules; preview document version 5 is not a server version.'),
        dict(gap='Domino terminal/error schema and locked dependencies',progress='Declared-range Requests2.31.0/urllib3 1.26.20 source policy reviewed. api-docs original is a redirect, not schema.',action='Acquire immutable supported v4/jobs schema and all error meanings; solve exact wheel/environment lock before native tests. Preserve initial502 and mutable-latest omission.'),
        dict(gap='Posit concrete product conformance',progress='Local C++ backend and historical license/profile inspected; no Cancel support and separate ExitCode are explicit.',action='Select supported Workbench/Launcher build and exact SDK/backend lock; preregister launch, nonzero exit, stop/kill, unsupported cancel, privilege/network/output profiles and skipped-case accounting.'),
        dict(gap='Whole market coverage, rights, economics and trials',progress='Bounded source review only; earlier omissions remain.',action='Continue complementary candidates and source tails; keep rights/entitlements, actual quoted costs and registered native qualification separate from proposal reasoning.')]
    write(BASE/'omissions-register.json',dict(predecessor=ref(PRIOR/'omissions-register.json','Preserved historical limits'),items=omissions,whole_cell_complete=False))
    write(BASE/'conversion-contract.json',dict(status='proposed_not_implemented',integration_allowed=False,capabilities=[],native_execution=False,
        requirements=['Keep trigger identity, actual run identity, terminal state, exit code, valid artifact and scientific acceptance as separate typed fields.',
            'Record cancelled-before-start attempts and all failures in the requested denominator and full workflow cost.',
            'Distinguish method/status retries, connection/read errors, server idempotency and a new scientific attempt; never infer exactly-once behavior.',
            'Use observation and transport deadlines; retain remote unknown state on timeout and reconcile before reissuing effects.',
            'Reject unsupported cancellation explicitly; qualify product and backend profiles without turning skips into passes.']))
    evidence=[ref(BASE/n,'Bounded source comparison') for n in ['plan.md','plan-review.json','source-audit.json','inspected-source-inventory.json','search-screening.json','exact-results.json','omissions-register.json','conversion-contract.json']]
    evidence += [ref(Path(__file__),'Authentication and claim-anchor review'),ref(Path(exact.__file__),'Project-owned exact arithmetic')]
    review=dict(status='pass_for_scoped_contract_review_with_limits',reviewer=dict(name='Codex author/coordinator',kind='author'),
        evidence=evidence,findings=['38 primary blobs authenticate; only explicitly read spans support technical claims.',
            'Dataiku cancelled trigger and strict success handling remain distinct; no_fail composition has an unguarded None path under the documented cancellation condition.',
            'SAS historical preview contracts improve the route comparison without qualifying supported server behavior.',
            'Declared-range retry profile excludes POST status/read retries by default but not every connection-error retry; all environments remain unqualified.',
            'Posit Local backend records nonzero exit separately from Finished and explicitly lacks Cancel support; smoke testing is not integration acceptance.'],
        whole_cell_complete=False,integration_allowed=False,capabilities=[],native_execution=False,visual_acceptance=False,limitations=LIMITS)
    verify_bindings(review);write(BASE/'review.json',review)
    print(json.dumps(dict(authenticated_blobs=38,inspected_blobs=sum(x['technical_inspected'] for x in inventory),source_records=5,whole_cell_complete=False)))


if __name__=='__main__':main()

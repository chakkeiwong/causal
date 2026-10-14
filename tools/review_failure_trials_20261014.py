#!/usr/bin/env python3
"""Bind actual fault observations and a proposed recovery contract."""
import json
from pathlib import Path

import run_program as control
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings

ROOT=control.core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-14/failure-trials'
OP='IN.REQ.failure_trials'
SYN=ROOT/'docs/program/comprehensive-v14/work'/OP/'requirement-review.json'
AUDIT=ROOT/'docs/program/execution/2026-10-14/r-temporal/v2/reader/source-audit.json'
REVIEWER={'name':'Codex author/coordinator','kind':'author'}
LIMITS=['Proposal requirement development; implementation unchanged and no bank/consumer qualification.',
    'Generated one-host fixtures and deterministic test-process publication hooks; no outage-frequency or all-orderings guarantee.',
    'Fifteen reviewed cases comprise12 runtime/instrumented cases and3 CLI cases; the preserved first CLI run repeats the latter3 and adds no distinct-case credit.',
    'No new live MCP, sibling-repository or external service execution.',
    'Truncated replay is misclassified by CLI; inherited coherent-descriptor and FIFO findings remain unrepaired.',
    'Rendered visual acceptance remains open under the inherited exhausted image allowance.']

def verify_observations():
    local=json.loads((BASE/'local-observations.json').read_text());cli=json.loads((BASE/'cli-observations-v2.json').read_text())
    verify_bindings(local);verify_bindings(cli)
    assert local['count']==len(local['cases'])==12 and cli['count']==len(cli['cases'])==3
    by={r['case']:r for r in local['cases']}
    assert by['truncated_cache']['exception']['type']=='JSONDecodeError'
    assert by['valid_empty_set']['response']['result']['coordinate_sets'][0]['topology']=='empty'
    assert by['changed_units_context']['response']['result']is None
    assert by['unsupported_discovery']['response']['disposition']=='unsupported'
    for name in ['killed_after_checkpoint','report_before_terminal']:
        r=by[name];assert r['fault']['returncode']==-9
        ids=r['request']['parameters']['artifact_ids']
        assert r['terminal']['state']=='completed'and r['terminal']['completed_work_ids']==ids
        assert [s['source']['artifact_id']for s in r['report']['summaries']]==ids
        assert all(s['verification']=='schema_only_not_causal_or_external_review'for s in r['report']['summaries'])
    r=by['report_before_terminal'];assert r['terminal']['result_ref']==r['fault']['marker']['result_ref']
    assert r['report']==r['published_before_terminal']
    r=by['changed_checkpoint'];assert r['terminal']['state']=='failed'and r['terminal']['result_ref']is None
    assert 'Checkpoint content identity changed'in r['terminal']['error']
    assert cli['cases'][1]['response']['error']['code']=='invalid_request'and cli['cases'][1]['exit_code']==2
    assert cli['cases'][1]['request']==cli['cases'][0]['request']
    assert cli['cases'][2]['response']['error']['code']=='invalid_request'and cli['cases'][2]['exit_code']==2
    return local,cli

def main():
    assert not(BASE/'primary-review.json').exists()
    local,cli=verify_observations()
    records=[]
    for name,anchor,claims in [
        ('artifacts_v12.py','atomic, ArtifactStore.put/reference/get',
            ['Atomic content and metadata writes are separate; same-value retry can complete missing metadata.','No cross-file transaction or bank identity authority is claimed.']),
        ('runtime_v12.py','_replay_or_run; resume; _job_query; _report_worker',
            ['Replay JSON decoding can raise before a canonical response; source/schema/environment identities bind normal replay.',
             'Resume validates execution identity, completed prefix, checkpoint digest/count and original deadline.',
             'Final report artifact is stored before completed state is atomically written.']),
        ('operation_service_v12.py','_artifact and scientific response envelope',
            ['Artifact scientific-context mismatch is distinct from a mathematically empty set.']),
        ('worker_v12.py','main exception envelope',
            ['Selected worker input exceptions map to invalid_or_unavailable_input with no result.']),
        ('cli_v12.py','main exception handlers',
            ['JSONDecodeError and schema errors both map to invalid_request/exit2 in the current CLI, including valid requests with corrupt replay.'])]:
        records.append({'local_copy':ref(ROOT/'src/causalbank'/name,anchor),'inspected_anchors':[anchor],'supported_claims':claims})
    inherited=[ref(ROOT/p,a)for p,a in [
        ('docs/program/repair-v12/work/IN02/receipt.json','Design semantics, not an executed interface'),
        ('docs/program/repair-v12/work/IN04/fault-trials.json','Nine historical local cases; not rerun or recounted as new'),
        ('docs/program/repair-v12/work/IN04/receipt.json','Pinned local transport scope and limitations'),
        ('docs/program/execution/2026-10-14/artifact-custody/primary-review.json','Prior custody cases and source identities'),
        ('docs/program/execution/2026-10-14/artifact-custody/design-review.json','Unrepaired descriptor and FIFO cases')]]
    primary={'status':'reviewed','reviewer':REVIEWER,'records':records,'inherited':inherited,
        'observations':[ref(BASE/'local-observations.json','12 actual/instrumented local cases'),ref(BASE/'cli-observations-v2.json','3 actual CLI cases')],
        'repair_note':ref(BASE/'cli-probe-repair.json','Original complete observations retained; post-save summary print fixed separately'),
        'limitations':LIMITS}
    write(BASE/'primary-review.json',primary)
    design={'status':'proposed_not_implemented','implementation_changed':False,'consumer_enabled':False,
        'repairs':[{'id':'error_classification','problem':'Valid request with corrupt replay produces library JSONDecodeError and CLI invalid_request.',
            'route':'Centralize typed failure mapping; distinguish request syntax/schema from corrupt/unavailable saved state, budgets and scientific refusals.',
            'acceptance':['Valid request with invalid/missing cache','Schema error','Cache shape and identity mismatch','Library/CLI/MCP parity on same normalized error'],
            'retention':'Preserve corrupt bytes and hash; do not silently delete/rerun as if the original execution had succeeded.'},
            {'id':'publication_reconciliation','problem':'Bytes, descriptor and terminal job acknowledgement have separate publication boundaries.',
             'route':'Validate each identity before retry; deterministic same-value artifact repair and final acknowledgement reconciliation.',
             'acceptance':['Content-only orphan','Metadata-only/missing bytes','Report stored before terminal state','Wrong preexisting descriptor','Failure during final acknowledgement']},
            {'id':'resume_integrity','problem':'Restart must preserve original scientific and operational conditions.',
             'route':'Bind original request/context/inputs/environment/deadline; preserve work prefix, output uniqueness and causal qualification.',
             'acceptance':['Changed units/horizon/population/clock/schema/code','Corrupt or reordered checkpoint','All partial-work boundary positions',
                 'Cancellation before/during/after publication','Original deadline exhausted','Retry cap','Unbounded result sets retained']}],
        'observed_failures':['Corrupt saved replay misclassified as invalid caller request','Library raises for malformed replay'],
        'inherited_unrepaired':['Coherent descriptor replacement under old handle','FIFO blocks preflight before worker timer'],
        'owner_inputs':['Named consumer and supported library/CLI/MCP versions','OS/filesystem atomicity and durability model','Trusted identity/manifest authority',
            'Retention, quarantine and recovery decision policy','Service limits, rollback and external-side-effect semantics'],
        'public_evidence_route':'Generated/public provenance and deterministic interruption examples before target-platform or bank trials.',
        'economics':'No new throughput, failure-rate, monetary-savings or bank-ROI estimate.',
        'limits':LIMITS}
    write(BASE/'design-review.json',design)
    sources=[]
    for key,title,kind,p,anchor,claims,extra in [
        ('implementation','Preserved local replay and report-publication implementation','project_implementation',BASE/'primary-review.json',
            'Five primary source files and inherited scope',[c for r in records for c in r['supported_claims']],records),
        ('observations','Generated interruption, recovery and CLI failure observations','project_execution',BASE/'local-observations.json',
            'Twelve runtime/instrumented cases with exact requests, markers and results',
            ['Two interrupted report jobs recover without duplicate summaries; stored report identity survives acknowledgement loss.',
             'Content-only orphan same-value retry completes metadata; altered checkpoint fails.',
             'Actual CLI maps corrupted replay and invalid caller schema to same invalid_request/exit2.'],
            [ref(BASE/'cli-observations-v2.json','Three reviewed CLI follow-up cases'),ref(BASE/'cli-probe-repair.json','First CLI run preserved'),
             ref(ROOT/'tools/probe_failure_trials_20261014.py','Exact local harness'),ref(ROOT/'tools/probe_failure_cli_v2_20261014.py','CLI harness')]),
        ('design','Proposed typed failures and scientific recovery contract','project_design',BASE/'design-review.json',
            'Repairs, acceptance cases and owner inputs',
            ['Proposed error normalization, publication reconciliation and identity/deadline checks remain unimplemented.'],
            [ref(BASE/'plan-review.md','Reviewed bounded plan')])]:
        sources.append({'integrated_citation_key':'exec14_failure_'+key,'kind':kind,'title':title,'author':'Causal banking proposal','year':2026,
            'source_identity':'Project-authored '+kind,'version_date':'2026-10-14; selected implementation bytes pinned by SHA-256',
            'local_copy':ref(p,anchor),'records':extra,'inspected_anchors':[anchor],'supported_claims':claims,'limitations':LIMITS})
    write(BASE/'source-audit.json',{'cutoff':'2026-10-07','note':'New project observations, no new external scholarly claim','sources':sources})
    evidence=[ref(p,'Reviewed failure/recovery evidence')for p in [BASE/'primary-review.json',BASE/'local-observations.json',
        BASE/'cli-observations-v2.json',BASE/'design-review.json',BASE/'source-audit.json',BASE/'development.template',BASE/'plan-review.md',
        BASE/'cli-probe-repair.json',Path(__file__).resolve()]]
    verify_bindings(evidence)
    findings=['Current implementation/design and inherited qualification scope are hash-bound. Concrete error-classification, publication and recovery cases are specified with remaining owner/platform inputs.',
        'Twelve generated local/instrumented cases plus three actual CLI cases retain requests and outcomes. Correct recovery and corrupt-checkpoint refusal coexist with a preserved corrupt-cache misclassification; no rate, bank acceptance or new product is claimed.']
    write(SYN,{'operation':OP,'status':'pass','scope':'Proposal requirement development with generated mechanism evidence','reviewer':REVIEWER,
        'findings':findings,'evidence':evidence,'capability_qualification':False,'implementation_changed':False,'limitations':LIMITS})
    write(BASE/'author-review.json',{'status':'pass','reviewer':REVIEWER,'evidence':evidence+[ref(SYN,'Required review output')],
        'findings':findings,'limitations':LIMITS,'substantive_page_credit':0,'test_basis':'Meaningful actual cases; no broad repeated test run needed for unchanged implementation.'})
    graph,_,_=control.combined(ROOT,control.core.read(ROOT,control.core.STATE));node=control.ledger.operation(graph,OP)
    receipt=control.ledger.receipt_template(node);receipt.update(outcome='pass',execution='performed',scope='Proposal recovery requirement review; product limitations retained',
        reviewer=REVIEWER,outputs=[ref(SYN,'Reviewed requirement')],limitations=LIMITS,
        criteria=[{'index':i,'verdict':'pass','finding':f,'evidence':evidence}for i,f in enumerate(findings)])
    write(BASE/'operation-receipt.json',receipt)
    print(json.dumps({'requirement_review':'pass','distinct_cases':15,'sources':3,'implementation_changed':False,'corrupt_cache_repair':'proposed'}))

if __name__=='__main__':main()

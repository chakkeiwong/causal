#!/usr/bin/env python3
"""Authenticate acquired cutoff sources and bind only inspected technical claims."""
import hashlib
import json
from pathlib import Path
import workflow_client_reference_20261023 as exact
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'docs/literature/raw'
BASE = ROOT / 'docs/program/execution/2026-10-23/commercial-workflow-recovery-v1'
read = lambda p: json.loads(p.read_text())
LIMITS = [
    'Static inspection of selected official open client/SDK sources, not execution of downloaded code or licensed servers.',
    'Cutoff commit dates and authenticated selected blobs establish these client revisions, not a complete product release or server compatibility matrix.',
    'Root license texts do not establish commercial server entitlement, prices, complete dependency rights or legal clearance.',
    'Uninspected acquired files are inventoried without technical claims. Search results are bounded and not an exhaustive market census.',
    'Prior Dataiku and six-manual cutoff omissions, native qualification, visual acceptance and whole commercial-cell completion remain open.'
]
# Each span has been read directly; text outside these spans receives no claim.
SPECS = {
 'positgo_file_1': [(1,17,'Permission is hereby','The root license offers an MIT-style grant with notices and warranty limits unless received under a commercial agreement.')],
 'positgo_more_0': [(18,79,'shared state','The official guide describes a JSON-over-stdio scheduler bridge, bootstrap reconciliation, shared state for multiple instances, heartbeats and product prerequisites.')],
 'positgo_more_1': [(37,127,'Three-tier architecture','Documented tests separate universal invariants, product request workflows and individual scenarios; profiles allow different terminal statuses and exit codes.')],
 'connectapi_file_1': [(1,4,'0.12.1.9000','The selected R package declares development version 0.12.1.9000; this is not a server release.')],
 'connectapi_file_2': [(1,21,'MIT License','The selected client declares MIT license text with notice and warranty conditions.')],
 'connectapi_file_3': [(41,59,'unversioned_url','Schedule updates are marked experimental and use unversioned schedule endpoints; start_time and next_run are converted.')],
 'connectapi_more_0': [(49,98,'task_id','Task normalizes id to task_id when necessary.'),(631,673,'if (code != 0)','poll_task waits for finished, then rejects nonzero code, records optional result and has no overall deadline argument in this function.')],
 'connectapi_more_1': [(735,807,'bundle_id','Jobs expose bundle and execution metadata; documented older-server omissions and type coercion need explicit handling.')],
 'dominopy_file_1': [(1,4,'Apache License','The selected Python client includes the Apache License version 2.0.')],
 'dominopy_file_2': [(277,331,'outputCommitId','The legacy run loop resets consecutive status-read retries, waits for an output commit and requires status Succeeded.'),(723,758,'commitId','Submission transmits code, environment and hardware identifiers; stop can request result commits.'),(795,867,'isCompleted','Job restart selects original input commit by default. The blocking helper raises on Failed, then uses isCompleted as its polling success predicate and forwards a timeout to polling2.')],
 'sasctl_more_0': [(53,63,'command line interface','sasctl exposes both Python module and CLI access to SAS Viya.')],
 'sasctl_more_1': [(1,4,'Apache License','The selected SAS Python client includes the Apache License version 2.0.')],
 'sasctl_more_2': [(12,26,'experimental','The Workflow class explicitly calls its partial implementation experimental; its historical 2022.09 warning is not a claim about current public API documentation.'),(102,171,'definitionId','Workflow submission looks up enabled definitions, maps declared prompt values, and converts naive datetime values using local timezone with a UTC fallback.')],
 'sasctl_more_3': [(111,146,'while time.time() - start_poll < timeout','The score polling function returns completed or failed; a timeout branch is inside the loop with no explicit return after loop exit, so a zero timeout falls through.')],
}


def main():
    assert not (BASE/'source-audit.json').exists(), 'Use a successor for any changed audit.'
    maps=[]
    for name in ['technical-manifest.json','delegate-manifest.json']:
        maps += [r for r in read(BASE/name)['requests'] if r.get('source_path')]
    assert len(maps)==23
    groups={}; inventory=[]
    for candidate in ['positgo','connectapi','dominopy','sasctl']:
        cp=RAW/f'exec23_workflow_{candidate}_cutoff.json'; tp=RAW/f'exec23_workflow_{candidate}_tree.json'
        commit=read(cp)[0]; tree=read(tp)
        assert commit['commit']['committer']['date']<'2026-10-07T16:00:00Z'
        assert tree['sha']==commit['commit']['tree']['sha'] and not tree['truncated']
        for p in [cp,tp]:
            receipt=read(p.with_suffix('.receipt.json'))
            assert receipt['status']=='saved' and receipt['sha256']==hashlib.sha256(p.read_bytes()).hexdigest()
        entries={r['path']:r for r in tree['tree']}; records=[]
        for row in [r for r in maps if r['candidate']==candidate]:
            p=RAW/(row['id']+'.txt'); data=p.read_bytes(); rp=p.with_suffix('.receipt.json'); receipt=read(rp)
            blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            # A real Git blob uses a NUL byte, not an escaped display sequence.
            blob=hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()
            assert entries[row['source_path']]['sha']==blob and entries[row['source_path']]['size']==len(data)
            assert receipt['status']=='saved' and receipt['url']==row['url'] and receipt['sha256']==hashlib.sha256(data).hexdigest()
            assert '/'+commit['sha']+'/' in row['url']
            short=row['id'].removeprefix('exec23_workflow_'); anchors=[]; lines=data.decode().splitlines()
            for first,last,token,claim in SPECS.get(short,[]):
                excerpt='\n'.join(lines[first-1:last]); assert token in excerpt,(short,token)
                anchors.append(dict(anchor=f'{row["source_path"]} lines {first}-{last}', inspected_text=excerpt, supported_claim=claim))
            item=dict(source_identity=row['url'],version_date=commit['commit']['committer']['date']+'; '+commit['sha'],
                      local_copy=ref(p,'Authenticated upstream blob; see explicit inspected spans'),
                      acquisition_receipt=ref(rp,'Saved response identity/hash'),git_blob_sha1=blob,
                      inspected_anchors=anchors,supported_claims=[x['supported_claim'] for x in anchors],
                      technical_inspected=bool(anchors),executed=False)
            records.append(item); inventory.append(item)
        claims=[c for r in records for c in r['supported_claims']]
        groups[candidate]=dict(integrated_citation_key='exec23_workflow_'+candidate,kind='software_primary_sources',
            title={'positgo':'Posit Launcher Go SDK: scheduler and conformance contracts','connectapi':'Posit connectapi: task, job and schedule contracts','dominopy':'Domino Python client: job restart and terminal-state contracts','sasctl':'SAS sasctl: workflow prompts and score polling contracts'}[candidate],
            author={'positgo':'Posit PBC','connectapi':'Posit PBC','dominopy':'Domino Data Lab','sasctl':'SAS Institute'}[candidate],year=2026,
            source_identity='https://github.com/'+next(r['repository'] for r in maps if r['candidate']==candidate)+'/tree/'+commit['sha'],
            version_date=commit['commit']['committer']['date']+'; '+commit['sha'],
            local_copy=next(r['local_copy'] for r in records if r['technical_inspected']),records=records,
            identity_evidence=[ref(cp,'Cutoff-filtered commit identity'),ref(tp,'Nontruncated authenticated tree')],
            inspected_anchors=[a['anchor'] for r in records for a in r['inspected_anchors']], supported_claims=claims,limitations=LIMITS)
    write(BASE/'authenticated-source-inventory.json',dict(authenticated_blobs=len(inventory),inspected_blobs=sum(x['technical_inspected'] for x in inventory),records=inventory))
    reference=dict(integrated_citation_key='exec23_workflow_client_reference',kind='project_derivation_and_exact_reference',
        title='Exact authored workflow revision, retry-cost and terminal-predicate witnesses',author='Causal banking proposal project',year=2026,
        source_identity='tools/workflow_client_reference_20261023.py',version_date='2026-10-23',
        local_copy=ref(Path(exact.__file__),'calculate(): rational arithmetic and supplied logical responses'),
        inspected_anchors=['calculate(): revision, duplicate, terminal_predicate and sas_zero_timeout'],
        supported_claims=['Stipulated revision-specific net values are 10 and 20 USD.', 'One useful gain with one or two charges gives 5 or -2 USD.',
                          'A hypothetical completed non-Failed response satisfies the inspected Domino predicate without an explicit Succeeded check.',
                          'A zero timeout fails the SAS while guard before entering its body; no native claim is made.'],limitations=LIMITS)
    write(BASE/'source-audit.json',dict(cutoff='2026-10-07',sources=list(groups.values())+[reference],native_execution=False))
    write(BASE/'exact-results.json',exact.calculate())
    omissions=[
        dict(gap='Dataiku exact cutoff technical bytes',action='Acquire an immutable DSS 15.0.2 technical original or leave historical claims explicitly unresolved; earlier detailed current-manual findings remain valid in their stated scope.'),
        dict(gap='SAS complete workflow and API contract',action='Inspect authenticated service delegates and public REST manuals, declared versions, enabled workflow schema, timezone policy and timeout/error behavior; this experimental client is only a partial route.'),
        dict(gap='Domino actual terminal state space',action='Inspect pinned routes, exception mapping and supported server API schema before interpreting completed as success; qualify original-code restart separately from data/environment custody.'),
        dict(gap='Posit runtime conformance',action='Bind server/client versions and execution environments; inspect plugin implementations and run registered fault and state-reconciliation tests. Documentation of tests is not a passing run.'),
        dict(gap='Product rights and economics',action='Obtain edition-specific public entitlements, current quoted costs and relevant dependency notices when accessible; do not infer free server use from an open client license.'),
        dict(gap='Census breadth and historical originals',action='Retain seven bounded GitHub searches, including truncated SAS results and empty-query limits; expand complementary discovery and preserve previous six-manual omissions.'),
        dict(gap='SAS programming examples',action='A separate cutoff tree is saved but technical examples remain uninspected; acquire selected workflow/job originals only as needed.'),
    ]
    prior=ROOT/'docs/program/execution/2026-10-23/dataiku-workflow-v1/omissions-register.json'
    write(BASE/'omissions-register.json',dict(predecessor=ref(prior,'Preserved earlier vendor/temporal omissions'),items=omissions,whole_cell_complete=False))
    requirements=['Separate immutable scientific request ID from run attempt ID, code revision, dataset snapshot, image digest and deployment ID.',
      'Represent terminal state, allowed success state, exit code, result existence and causal validation separately.',
      'Set a client-side observation deadline; a polling timeout is not proof that a remote job stopped.',
      'Reconcile remote state before resubmission and give externally visible side effects an idempotency key.',
      'Preserve timezone/clock semantics, unversioned API risks and missing fields on older servers.',
      'Use a read-only source audit first, then registered public/synthetic fault trials, then costed prototype comparison.']
    write(BASE/'conversion-contract.json',dict(status='proposed_not_implemented',requirements=requirements,integration_allowed=False,native_execution=False))
    write(BASE/'plan-review.json',dict(status='pass_for_scoped_source_review',evidence=[ref(BASE/'crash-continuation-plan.md','Recovered plan')],
      findings=['Only inspected spans support technical claims.', 'Acquired originals bind to cutoff commit trees, not a supposed licensed-server release.',
                'Concrete client alternatives and proposed adapter checks are documented; absent trials and historical omissions remain independent.']))
    evidence=[ref(BASE/n,'Source inspection and exact authored reference') for n in ['plan-review.json','authenticated-source-inventory.json','source-audit.json','exact-results.json','conversion-contract.json','omissions-register.json']]
    evidence += [ref(Path(__file__),'Authentication and claim-span verification')]
    review=dict(status='pass_for_scoped_comparison_with_limits',reviewer=dict(name='Codex author/coordinator',kind='author'),
      evidence=evidence,findings=['23 upstream blobs authenticate; selected spans in 14 files support four client/SDK profiles.',
      'Client completion predicates, retry/revision choices, clock conversion and scheduler conformance differ materially.',
      'Exact monetary witnesses distinguish retry cost and revision identity without claiming vendor observations.'],
      whole_cell_complete=False,integration_allowed=False,capabilities=[],native_execution=False,visual_acceptance=False,limitations=LIMITS)
    verify_bindings(review);write(BASE/'review.json',review)
    print(json.dumps(dict(authenticated_blobs=23,inspected_blobs=sum(x['technical_inspected'] for x in inventory),source_records=5,whole_cell_complete=False)))


if __name__=='__main__': main()

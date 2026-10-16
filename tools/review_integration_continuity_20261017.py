#!/usr/bin/env python3
"""Bind recovered originals and develop four integration proposal requirements."""
import argparse
import copy
from collections import Counter
import json
from pathlib import Path

import integration_continuity_reference_20261017 as exact
import review_integration_continuity_reference_20261017 as arithmetic
import master_control as core
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write
import run_program as run

ROOT = core.ROOT
BASE = ROOT/'docs/program/execution/2026-10-17/integration-continuity'
PRIOR = ROOT/'docs/program/execution/2026-10-17/other-temporal/publication/reader/source-audit.json'
PARITY = ROOT/'docs/program/execution/2026-10-16/semantic-parity'
FAULT = ROOT/'docs/program/execution/2026-10-14/failure-trials'
OPS = ['IN.REQ.long_jobs_resume_cancel', 'IN.REQ.one_shared_operation_layer',
       'IN.REQ.schema_version_negotiation', 'IN.REQ.signed_adoption_separate']
REVIEWER = {'name': 'Codex author/coordinator', 'kind': 'author'}
LIMITS = [
    'Proposal requirement development only; no runtime repair or capability grant.',
    'Saved generated local trials are rereviewed, not rerun or counted as fresh observations.',
    'Exact finite models are authored references, not host failures, wire negotiation or authentic signatures.',
    'General estimator recovery, complete dependency identity and distributed service guarantees remain unqualified.',
    'Modern MCP support, typed replay errors, descriptor/FIFO repairs and complete consumer conformance remain open.',
    'No bank truth, independent institutional review, consumer/platform adoption, actual prices or ROI is supplied.',
    'Q1 coverage/depth, Q5 sponsor coherence and rendered visual acceptance remain open.']


def read(path):
    return json.loads(path.read_text())


def evidence():
    before = read(ROOT/core.STATE)
    assert before['reader']['sha256'] == '88c8169c632060126c4a430df2df22922fea217069988965c89e9a0548cb0bd0'
    assert before['execution_runtime']['active']['operation'] == OPS[0]
    assert not before['input_receipts']
    old = read(PARITY/'source-review.json')
    verify_bindings(old)
    code = [copy.deepcopy(r) for r in old['records'] if r['kind'] == 'project_implementation_source']
    for row in code:
        original = ROOT/row['source_identity']
        assert core.sha(original) == row['local_copy']['sha256'], original
        row['continuation_check'] = 'Original still matches preserved source on 2026-10-17; no implementation edit.'
    anchors = {
        'runtime_v12.py': ['execution_identity lines 28-36: selected sources and four dependencies; MCP/AnyIO/tool map absent',
            'resume lines 197-235: terminal/cancel, prefix, digest/count, three starts and original wall-clock formula',
            '_job_query lines 237-275: terminal immutability, cooperative cancellation and process lease',
            '_report_worker lines 291-348: checkpoint commits, final artifact and acknowledgement within job lock; separate persistence writes'],
        'artifacts_v12.py': ['atomic lines 33-52: file flush, replacement and directory fsync',
            'bounded_read lines 55-69: descriptor regular-file check after opening; FIFO concern remains',
            'ArtifactStore.put/reference/get lines 78-116: bytes and metadata separate; identity and custody limits'],
        'operation_contract_v12.py': ['context_digest and validate_response: declared target, units, topology and uncertainty; no truth validation'],
        'operation_service_v12.py': ['SUPPORTED: six bounded operations', 'request_digest: display request ID and idempotency key omitted',
            '_artifact: expected schema and scientific context required'],
        'cli_v12.py': ['read_request and main: bounded input and Runtime invocation',
            'main error handlers: JSONDecodeError/ValueError classified as invalid_request including corrupt replay'],
        'mcp_server_v12.py': ['mapping/AVAILABLE: nine runtime operations; hard-coded legacy protocol',
            'call_tool: one canonical Runtime object, explicit response-schema validation, two response representations'],
        'worker_v12.py': ['main: fixed entrypoint, RLIMIT_AS and process timer; report job versus synchronous scientific operation']}
    for row in code:
        name = Path(row['source_identity']).name
        if name in anchors:
            row['reread_anchors'] = anchors[name]
    audit = read(ROOT/'docs/program/repair-v12/work/IN02/source-audit.json')
    verify_bindings(audit)
    keys = ['v12_mcp_legacy_lifecycle', 'v12_mcp_legacy_cancellation', 'v12_mcp_legacy_tools',
        'v12_mcp_legacy_stdio', 'v12_mcp_versioning', 'v12_mcp_stdio', 'v12_mcp_basic',
        'v12_mcp_sdk_types', 'v12_mcp_sdk_constants', 'v12_mcp_cutoff_commit']
    protocol = [copy.deepcopy(next(x for x in audit['entries'] if x['id'] == k)) for k in keys]
    for row in protocol:
        row['continuation_review'] = 'Preserved primary bytes verified; specification scope, not modern runtime support.'
    modern = next(x for x in protocol if x['id'] == 'v12_mcp_versioning')
    modern['reread_anchors'] = ['lines 42-77: per-request version, -32022 supported list; server MUST implement discovery, client MAY call it',
        'lines 80-125: extensions and core fallback or refusal', 'lines 128-182: era detection, cache lifetime, seven-pair matrix']
    next(x for x in protocol if x['id'] == 'v12_mcp_stdio')['reread_anchors'] = [
        'lines 122-151: discovery, recognized modern errors, other errors or timeout; fallback not keyed to one code']
    next(x for x in protocol if x['id'] == 'v12_mcp_basic')['reread_anchors'] = [
        'lines 181-213: stateless requests and explicit identifiers for persistent application state']
    sdk = read(ROOT/'docs/program/repair-v12/work/IN04/runtime-source-audit.json')
    verify_bindings(sdk)
    results = exact.calculate()
    reviewed = arithmetic.review()
    assert reviewed.pop('results') == results
    local, cli, parity = read(FAULT/'local-observations.json'), read(FAULT/'cli-observations-v2.json'), read(PARITY/'observation-review.json')
    assert len(local['cases']) == 12 and len(cli['cases']) == 3
    assert parity['scientific_comparisons'] == 13 and parity['lifecycle_comparisons'] == 3
    saved = [ref(p, 'Saved observations; no rerun') for p in [FAULT/'local-observations.json',
        FAULT/'cli-observations-v2.json', FAULT/'cli-probe-repair.json', PARITY/'observation-review.json',
        ROOT/'docs/program/repair-v12/work/IN04/fault-trials.json']]
    prior_sources = {s['integrated_citation_key']: s for s in read(PRIOR)['sources']}
    for key in ['exec14_failure_observations','exec14_failure_implementation','exec16_parity_observed','exec13_ops_faults']:
        verify_bindings(prior_sources[key])
    trial_rows = [{k:c[k] for k in ['case','mode','finding'] if k in c} for c in local['cases']]
    for c in local['cases']:
        if c['case'] in ['killed_after_checkpoint','report_before_terminal','changed_checkpoint']:
            target = next(x for x in trial_rows if x['case'] == c['case'])
            target['terminal'] = {k:c['terminal'][k] for k in ['state','error','spawn_attempts']}
            target['completed_count'] = len(c['terminal']['completed_work_ids'])
            if c['case'] == 'changed_checkpoint':
                assert c['terminal']['state'] == 'failed' and 'Checkpoint content identity changed' in c['terminal']['error']
            else:
                ids = c['terminal']['completed_work_ids']
                assert c['terminal']['state'] == 'completed'
                assert ids == c['request']['parameters']['artifact_ids'] and len(ids) == len(set(ids))
    source = {'status': 'pass_for_static_source_rereview', 'reviewer': REVIEWER,
        'date': '2026-10-17', 'current_originals_match': len(code), 'implementation_records': code,
        'protocol_records': protocol, 'sdk_source_audit': ref(ROOT/'docs/program/repair-v12/work/IN04/runtime-source-audit.json',
            'Six genuine SDK originals; prior execution evidence remains scoped'),
        'sdk_reread': ['mcp_types.py line27: latest legacy protocol',
            'mcp_server_lowlevel_server.py lines 540-570: explicit CallToolResult returns before later structured validation',
            'mcp_server_session.py lines 168-176: legacy version selection'],
        'findings': ['Six core operations plus three Runtime lifecycle/report operations; both adapters use Runtime.',
            'Resume is a report-summary path, not a general estimator checkpoint API.',
            'Publication and terminal acknowledgement ordinarily hold one lock; a crash separates writes and permits cancellation before acknowledgement.',
            'Wall-time formula has a backward-clock counterexample; not an observed host clock failure.',
            'Modern servers must implement discovery; clients are not universally required to call it.',
            'SDK1.27.0/legacy stdio observations cannot qualify modern or dual-era support.'],
        'limitations': LIMITS}
    write(BASE/'source-review.json', source)
    write(BASE/'exact-results.json', results)
    reviewed.update(evidence=[ref(ROOT/'tools/integration_continuity_reference_20261017.py','Five exact authored reference families'),
        ref(Path(__file__).with_name('review_integration_continuity_reference_20261017.py'),'Alternative author recomputation')],
        correction='Preserved draft used a broad recognized-modern-error retry category; final table separates unsupported-version retry from other recognized modern errors.')
    write(BASE/'arithmetic-review.json', reviewed)
    write(BASE/'saved-trial-review.json', {'status':'pass_for_saved_evidence_review','reviewer':REVIEWER,
        'runtime_and_instrumented_cases':12, 'distinct_cli_cases':3,
        'parity_scientific_cases':13, 'parity_lifecycle_cases':3,
        'counting_rule':'Different suites are not summed into a universal coverage/rate claim; first CLI run duplicates three cases.',
        'trials_rerun':False, 'cases':trial_rows, 'parity_adverse_findings':parity['adverse_cases'],
        'evidence':saved, 'limitations':LIMITS})
    write(BASE/'owner-input-status.json', {'observed_at':core.now(),
        'observed_state_sha256':core.sha(ROOT/core.STATE), 'observed_state_source':'docs/program/state.json',
        'input_receipts':before['input_receipts'], 'seven_adoption_groups':before['external_inputs'][:7],
        'other_live_study_groups':before['external_inputs'][7:],
        'boundary':'Author observation of empty intake ledger; no institutional attestation.'})
    with (BASE/'external-inputs-snapshot.md').open('xb') as stream:
        stream.write((ROOT/'docs/program/master/external-inputs.md').read_bytes())
    print(json.dumps({'source_originals_match':len(code),'protocol_originals':len(protocol),
        'reference_families':len(results),'saved_trials_rerun':False}))


def contract():
    # These are prospective cases, not an unregistered product experiment.
    gaps = [
        ('deadline','static formula concern','Use monotonic within-process time; choose trusted cross-restart deadline or conservative refusal. Freeze backward/forward adjustment and reboot cases.','Clock/lease contract and target operator; no portable reboot-safe clock is supplied.'),
        ('publication_cancel','source and finite reference','Reconcile bytes, descriptor, checkpoint and terminal state separately; never overwrite terminal cancellation or imply rollback.','Multi-host fencing and external-effect authority need actual platform design.'),
        ('replay_errors','saved actual negative finding','Separate input validation from stored-state decoding; return context-bound failed/unavailable for corrupt replay; preserve bad bytes.','No repair has yet been executed.'),
        ('complete_identity','static omission','Bind MCP/AnyIO, tool map, decoder/normalizer and launch profile alongside scientific runtime; review meaningful migrations.','Full transitive numerical environment must be chosen per backend.'),
        ('artifact_preflight','inherited negative findings','Validate descriptor self-identity and establish bounded regular-file access without blocking on FIFO; preserve tampered bytes.','Existing descriptor/FIFO findings remain unrepaired; full target storage threat/availability model absent.'),
        ('operation_registry','bounded parity and static source','One versioned operation registry and typed failure boundary; compare all canonical fields on the negotiated common domain.','Actual consumer decoders, languages and maintained versions require their owners.'),
        ('modern_mcp','primary specification only','Implement explicit legacy/modern selection and nine-row proposed decisions; run frozen real stdio client/server cases before advertising.','Unknown actual SDK/client behavior until executed; HTTP is a separate branch.'),
        ('arbitrary_estimator_resume','unsupported extension','Define algorithm-specific sufficient checkpoint state including random state, data partition and selection decisions; prove unchanged target then test.','No generic checkpoint solves all estimator states or restores unseen external effects.'),
        ('platform_scale','external evidence missing','Use generated whole workloads first, then frozen operator-run storage/clock/concurrency/failure matrix and complete cost measurements.','No supplied workload thresholds, operator, hardware or accepted service level.'),
        ('authentic_adoption','external evidence missing','Prepare exact-release package and receipt template; require authentic authorized owner evidence, independent scope review and impact-aware successors.','Local hashes and Boolean tables cannot authenticate institutional authority or supply a decision.'),
        ('scientific_truth','research and information limits','Preserve assumptions/refusals; obtain justified assignment, clocks and additional restrictions or experiments where observational laws are equivalent.','A transport repair cannot identify a contrast from insufficient information or promise general calibration.'),
        ('economics','outcome unknown','Demonstrate public/generated prototype merit; compare full matched workflow with all failures, review and maintenance costs, then collect actual prices and bank utility.','Actual usefulness, costs and sponsor willingness remain unknown.')]
    write(BASE/'open-gap-register.json', {'status':'open_scoped_remedies', 'global_blocker':False,
        'gaps':[{'id':'IC%02d'%(i+1),'area':g[0],'evidence_class':g[1],'known_route':g[2],
            'remaining_unknown_or_input':g[3],'implementation_closed':False} for i,g in enumerate(gaps)],
        'rule':'A missing platform, owner or modern peer blocks only that qualification branch; proposal and independent public work continue.'})
    cases = [
        ('long_jobs_resume_cancel','prefix and retry','Freeze three distinct artifact IDs; reject reordered, repeated, unknown or changed-prefix state; retain one summary per original ID.'),
        ('long_jobs_resume_cancel','publication boundary','Interrupt before/after content, descriptor and terminal write; observe retained bytes and correct job state; no duplicate effect.'),
        ('long_jobs_resume_cancel','cancel and completion','Cancel queued/running/completed jobs and after crash between publication and acknowledgement; terminal states immutable and artifact retention explicit.'),
        ('long_jobs_resume_cancel','clock and budget','Test expired budget, backward/forward clock movement, reboot epoch, start limit and overlapping leases under chosen policy; account parent and worker resources.'),
        ('one_shared_operation_layer','canonical meaning','Finite, empty, whole, disconnected and unknown sets; exact units/sign/horizon/sampling law; full response equality within common capability domain.'),
        ('one_shared_operation_layer','failure origin','Distinguish malformed caller JSON, schema mismatch, wrong tool, invalid artifact, corrupt replay, worker failure and protocol failure; do not fabricate context for unparseable input.'),
        ('one_shared_operation_layer','validation ownership','Inject wrong context/units, nonfinite output and text/structured divergence on each adapter return path; explicit canonical validation required.'),
        ('one_shared_operation_layer','identity change','Change SDK, tool map, normalizer or launch profile under one idempotency key; preserve old evidence and require reviewed compatibility.'),
        ('schema_version_negotiation','era detection','Real discovery result; unsupported-version error with common/no common version; other recognized modern error; two ordinary legacy error codes; timeout; modern-only refusal.'),
        ('schema_version_negotiation','wire parsing','Malformed discovery/error shape, missing supported list, contradictory metadata and unknown mandatory fields; bounded refusal without coercing scientific semantics.'),
        ('schema_version_negotiation','cache and restart','Bind era cache to server process/configuration; re-probe after changed assumptions; compare legacy and modern capability and response objects.'),
        ('schema_version_negotiation','extension and schema','Unsupported optional extension reverts only where specified or rejects; independently reject incompatible operation/artifact/request schema.'),
        ('signed_adoption_separate','missing evidence','Generated empty and partial receipts cannot establish adoption; retain missing owner and criterion identifiers.'),
        ('signed_adoption_separate','stale release','Change each of reader/core/adapter/consumer/scientific context/platform; require an impact-reviewed exact successor or explicit scoped carry-forward.'),
        ('signed_adoption_separate','authority and scope','An authentic verifier must check signer identity, authority, conflicts, evidence scope and unresolved conditions; local shape/hash success cannot do this.')]
    template = {'template_only':True, 'origin_required':'external',
        'required_fields':['input_id','owner.name','owner.role','owner.organization','scope','agreed_criteria',
            'baseline_manifest_sha256','assessed_release.path','assessed_release.sha256','assessed_release.anchor',
            'signed_evidence.path','signed_evidence.sha256','signed_evidence.anchor','input_sha256'],
        'owner_values_supplied':False,'signatures_supplied':False,
        'authentic_verification':['identity and authority of original signer','independence/conflicts where applicable',
            'release and claim scope','conditions, unresolved findings and revocation/current applicability'],
        'machine_intake_limit':'Shape and hash checks only; authenticity, legal access and scientific truth need the responsible original owner.'}
    write(BASE/'evaluation-package-template.json', {'status':'prepared_proposal_template_not_acceptance',
        'release_fields':['reader/audit','request and response schemas','operation registry','core/adapter/dependencies',
            'protocol/extension versions','consumer/decoder','scientific context','platform profile','criteria/protocol'],
        'receipt_template':template,'package_contents':['exact release manifest','claim-by-claim review and conflicts',
            'authorized custody manifest without bank raw data','consumer valid/refusal/stale fixtures',
            'whole-workload platform/fault schedule','matched full-cost workflow protocol','original owner decision and operating obligations'],
        'current_inputs':ref(BASE/'owner-input-status.json','Zero authentic input receipts recorded'),
        'original_contract':ref(BASE/'external-inputs-snapshot.md','Seven missing adoption groups and exact intake limits')})
    write(BASE/'proposed-contract.json', {'status':'proposed_not_implemented', 'scope':'Four independent proposal requirements',
        'operation_ids':OPS, 'public_entrypoint':'Runtime.invoke; OperationService has six operations, Runtime adds three',
        'common_domain':'Intersection of advertised library, CLI and negotiated MCP method/schema capabilities; preserve full canonical object.',
        'version_axes':['scientific context','request/response schema','operation','artifact','wire protocol','optional extension'],
        'future_cases':[{'requirement':'IN.REQ.'+r,'family':f,'expected_acceptance':v,'execution':'proposed_not_run'} for r,f,v in cases],
        'known_remedies':ref(BASE/'open-gap-register.json','Twelve explicit unresolved gaps and routes'),
        'owner_package':ref(BASE/'evaluation-package-template.json','Reviewable template without invented identities'),
        'comparison':'Generated cases and permitted public inputs before expensive bank experiment; freeze expected semantics and failure origins first.',
        'costs':['preparation and custody','all attempts and failures','runtime/storage/serialization','human review and reconciliation',
            'licensing and dependencies','consumer/platform qualification','maintenance and changed-release review'],
        'merit_trigger':'Demonstrated correct target/refusal preservation and bounded recovery with useful complete workflow costs; no promised pass or universal service threshold.',
        'limits':LIMITS})
    print(json.dumps({'proposed_case_families':len(cases),'open_gap_routes':len(gaps),'authentic_receipts':0}))


def prepare_reader():
    import build_java_temporal_engine_20261016 as engine
    old=ROOT/'docs/causal_proposal_other_temporal_2026-10-17.tex'
    driver=ROOT/'docs/causal_proposal_continuity_2026-10-17.tex'
    reader=BASE/'publication/reader'
    refs=BASE/'publication/refs.bib'
    assert not driver.exists() and not reader.exists() and not refs.exists()
    book=old.read_text()
    draft=(BASE/'development.tex').read_text()
    divider=r'\section{Make adoption evidence exact, external, and conditional}'
    assert draft.count(divider)==1
    continuity, adoption = draft.split(divider, 1)
    with (BASE/'continuity.tex').open('x') as stream:
        stream.write(continuity+'\n\\label{exec17:continuity-end}\n')
    with (BASE/'adoption.tex').open('x') as stream:
        stream.write(divider+adoption)
    marker=r'\input{program/execution/2026-10-16/semantic-parity/development.tex}'
    assert book.count(marker)==1
    book=book.replace(marker,marker+'\n'+r'\input{program/execution/2026-10-17/integration-continuity/continuity.tex}')
    marker=r'\input{program/execution/2026-10-13/operational-adoption/integration-preserving.tex}'
    assert book.count(marker)==1
    book=book.replace(marker,marker+'\n'+r'\input{program/execution/2026-10-17/integration-continuity/adoption.tex}')
    import re
    pattern=re.compile(r'\\bibliography\{([^}]+)\}')
    assert len(pattern.findall(book))==1
    book=pattern.sub(lambda m:r'\bibliography{'+m.group(1)+',program/execution/2026-10-17/integration-continuity/publication/refs}',book)
    driver.write_text(book)
    sources=[]
    for key,title,path,anchor,claims in [
        ('exec17_continuity_reference','Exact authored continuity, deadline, money, protocol and adoption references',
         BASE/'exact-results.json','Five exact families; cross-process deadline counterexample and scoped truth table',
         ['16 ordered no-repeat prefixes include four valid prefixes; authored cancellation and crash schedules.',
          'A wall-clock adjustment can make original-deadline formula return positive budget after true elapsed expiry; this is not an observed clock failure.',
          'Stipulated set arithmetic preserves USD units when costs are converted consistently.',
          'Modern negotiation decisions distinguish unsupported version from other recognized modern errors.',
          'Six assumed owner gates yield 64 combinations and one all-true conjunction; no authentic receipt or signature.']),
        ('exec17_continuity_contract','Proposed continuity, interface, protocol and owner-acceptance contract',
         BASE/'proposed-contract.json','Fifteen proposed case families and twelve explicit gap routes',
         ['Four requirements have explicit local/generated routes and remaining authentic input requirements.',
          'Public/generated prototype precedes expensive bank experiments; no capability or adoption is granted.'])]:
        sources.append({'integrated_citation_key':key,'title':title,'author':'Causal banking proposal',
            'kind':'project_evidence','year':2026,'source_identity':'Project-authored proposal evidence; no external data or execution',
            'version_date':'2026-10-17; exact local source and result hashes bound below',
            'local_copy':ref(path,anchor),'inspected_anchors':[anchor],'supported_claims':claims,
            'limitations':LIMITS})
    stdio=next(x for x in read(ROOT/'docs/program/repair-v12/work/IN02/source-audit.json')['entries']
               if x['id']=='v12_mcp_stdio')
    sdk_audit=read(ROOT/'docs/program/repair-v12/work/IN04/runtime-source-audit.json')
    sdk_types=next(x for x in sdk_audit['entries'] if x['local_copy']['path'].endswith('/mcp_types.py'))
    sdk_constants=next(x for x in sdk_audit['entries'] if x['local_copy']['path'].endswith('/mcp_shared_version.py'))
    sources.append({'id':'v12_mcp_stdio','integrated_citation_key':'v12_mcp_stdio',
        'title':'MCP modern stdio backward compatibility and legacy Python SDK version sources',
        'kind':'official_documentation','year':2026,
        'source_identity':stdio['source_identity'],
        'version_date':stdio['version_date']+'; SDK 1.27.0 source snapshots',
        'local_copy':stdio['local_copy'],
        'inspected_anchors':['MCP stdio lines 122-151: three discovery/error/timeout outcomes and no error-code-specific fallback',
            'MCP versioning lines 42-77: modern discovery is mandatory for servers and optional for clients',
            'SDK types.py line 27: LATEST_PROTOCOL_VERSION is 2025-11-25'],
        'supported_claims':['A dual-era stdio client probes discovery; unsupported-version modern errors do not downgrade; other errors or timeout select legacy initialization.',
            'Modern servers implement discovery; modern clients may use inline version negotiation.',
            'The preserved SDK 1.27.0 snapshot declares 2025-11-25 latest; this does not qualify its newer or all future versions.'],
        'records':[sdk_types['local_copy'],sdk_constants['local_copy']],
        'limitations':['Protocol text specifies behavior; no new modern or dual-era client/server trial.',
            'Installed SDK snapshot is static evidence, not all-SDK compatibility evidence.']})
    write(BASE/'publication/source-audit.json',{'cutoff':'2026-10-07','sources':sources,
        'evidence_bindings':[ref(BASE/'source-review.json','Static source reread'),
            ref(BASE/'saved-trial-review.json','Recovered local observations, not rerun'),
            ref(BASE/'arithmetic-review.json','Alternative exact author calculation'),
            ref(BASE/'open-gap-register.json','Twelve gaps and remedies'),
            ref(BASE/'evaluation-package-template.json','No fabricated owner receipts')],
        'visual_acceptance':False})
    bib=[]
    for s in sources:
        author=s.get('author','Model Context Protocol contributors')
        note=('Specification 2026-07-28 at pinned 2026-10-07 revision; saved Python SDK 1.27.0 sources'
              if s['kind']=='official_documentation' else 'Project-authored evidence; 2026-10-17')
        bib.append('@misc{'+s['integrated_citation_key']+',\n author={{'+author+'}},\n title={'+
            s['title']+'},\n year={2026},\n note={'+note+'}\n}')
    refs.write_text('\n\n'.join(bib)+'\n')
    write(BASE/'publication/prepared-inputs.json',{'inputs':[ref(p,'Reviewed preserving input') for p in
        [old,PRIOR,BASE/'source-review.json',BASE/'saved-trial-review.json',BASE/'arithmetic-review.json',
         BASE/'proposed-contract.json',BASE/'open-gap-register.json',BASE/'evaluation-package-template.json',
         BASE/'development.tex',Path(__file__),ROOT/'tools/integration_continuity_reference_20261017.py']],
        'generated':[ref(p,'New preserving reader input') for p in [driver,BASE/'publication/source-audit.json',refs,BASE/'continuity.tex',BASE/'adoption.tex']],
        'preservation':'All predecessor PDF, source records, literature originals, compiled source inputs and citation contexts retained.',
        'acceptance':'No automatic mandatory-repair depth, bank, independent, visual or adoption credit.'})
    print(json.dumps({'driver':str(driver.relative_to(ROOT)),'new_audited_records':len(sources),'predecessor_preserved':True}))


def build_reader():
    import build_java_temporal_engine_20261016 as engine
    for key,value in {'BASE':BASE/'publication','OUT':BASE/'publication/reader',
        'OLD':ROOT/'docs/causal_proposal_other_temporal_2026-10-17.tex',
        'NAME':'causal_proposal_continuity_2026-10-17','DRIVER':ROOT/'docs/causal_proposal_continuity_2026-10-17.tex',
        'PDF':ROOT/'docs/causal_proposal_continuity_2026-10-17.pdf',
        'PRIOR_AUDIT':PRIOR}.items(): setattr(engine,key,value)
    engine.build()
    from audit_reader_traceability_v2_20261013 import audit
    driver=engine.DRIVER
    index=audit(driver,engine.OUT/'source-audit.json')
    write(engine.BASE/'traceability-review.json',index)
    assert index['status']=='pass' and index['scholarly_pdfs']==187
    report=read(engine.OUT/'build-report.json')
    text=' '.join((engine.OUT/'reader.txt').read_text().split())
    phrases=['Continuity across jobs, interfaces, and ownership','A durable report is not an arbitrary resumable estimator',
        'Make adoption evidence exact, external, and conditional','seventy seconds','modern client may call another request',
        'only the all-true combination is eligible']
    missing=[p for p in phrases if p.lower() not in text.lower()]
    assert not missing,missing
    prev=read(PRIOR); cur=read(engine.OUT/'source-audit.json')
    old_sources={s['integrated_citation_key']:s for s in prev['sources']}
    new_sources={s['integrated_citation_key']:s for s in cur['sources']}
    assert len(old_sources)==696 and len(new_sources)==699
    assert all(new_sources[k]==v for k,v in old_sources.items())
    kept=[x for x in prev['tex_files'] if x['path']!=str(engine.OLD.relative_to(ROOT))]
    paths={x['path']:x['sha256'] for x in cur['tex_files']}
    assert all(paths[x['path']]==x['sha256'] for x in kept)
    oldidx=read(PRIOR.parent.parent/'traceability-review.json')
    old_contexts={r['citation_key']:Counter(json.dumps(c,sort_keys=True) for c in r['citation_contexts']) for r in oldidx['records']}
    for row in index['records']:
        current=Counter(json.dumps(c,sort_keys=True) for c in row['citation_contexts'])
        assert not (old_contexts.get(row['citation_key'],Counter())-current)
    assert not [w for w in report['warnings'] if 'Overfull' in w or 'undefined' in w.lower() or 'multiply defined' in w.lower()]
    import re
    aux=(engine.OUT/(engine.NAME+'.aux')).read_text()
    for label in ['exec17:integration-continuity','exec17:continuity-end','exec17:signed-adoption','exec17:integration-continuity-end']:
        m=re.search(r'\\newlabel\{'+re.escape(label)+r'\}\{\{[^}]*\}\{(\d+)\}',aux)
        assert m,label
        report['added_sections'][label]=int(m.group(1))
    report['builder']=ref(Path(__file__),'Preserving continuity and adoption reader builder')
    report['predecessor_pdf']=ref(engine.OLD.with_suffix('.pdf'),'Frozen 879-page temporal reader')
    core.write(engine.OUT/'build-report.json',report)
    write(BASE/'preservation-review.json',{'status':'pass','prior_records':696,'current_records':699,
        'prior_compiled_sources_preserved':len(kept),'all_prior_source_records_equal':True,
        'prior_citation_contexts_preserved':True,'prior_pdfs_immutable':True,
        'new_scholarly_pdfs':0,'scholarly_pdfs_total':index['scholarly_pdfs'],
        'new_citations':['exec17_continuity_reference','exec17_continuity_contract','v12_mcp_stdio'],
        'text_checks':phrases,'visual_acceptance':False,'warnings':report['warnings'],
        'reader':report['pdf'],'evidence':[ref(engine.OUT/'build-report.json','Compiled output'),
            ref(engine.OUT/'text-layout-review.json','All-page text bounds'),ref(engine.OUT/'source-audit.json','Complete source identity'),
            ref(engine.BASE/'traceability-review.json','Citations and current context index')]})
    print(json.dumps({'pages':report['pages'],'records':index['audit_records'],
        'scholarly_pdfs':index['scholarly_pdfs'],'retained_sources':len(kept),
        'layout':read(engine.OUT/'text-layout-review.json')['status'],'new_pages':report['added_sections']}))


def record_operations():
    import build_java_temporal_engine_20261016 as engine
    state=core.read(ROOT,core.STATE)
    expected=['IN.REQ.long_jobs_resume_cancel','IN.REQ.one_shared_operation_layer',
        'IN.REQ.schema_version_negotiation','IN.REQ.signed_adoption_separate']
    assert state['execution_runtime']['active']['operation']==expected[0]
    evidence_common=[ref(BASE/'source-review.json','Static source and primary protocol reread'),
        ref(BASE/'saved-trial-review.json','Recovered execution evidence reviewed without rerun'),
        ref(BASE/'proposed-contract.json','Four independent requirement contracts'),
        ref(BASE/'open-gap-register.json','Remedies and unknown inputs'),
        ref(BASE/'arithmetic-review.json','Recomputed authored examples'),
        ref(BASE/'preservation-review.json','Integrated reader and source preservation')]
    findings={
        expected[0]:['Static source and saved failure trials bind report-only prefix recovery, cancellation and publication boundaries; arbitrary estimators remain outside this worker.','Reproducible prefix/deadline/publication cases and a frozen local/target-platform test matrix specify known remedies; backward clock concern is a formula counterexample, not observed failure.'],
        expected[1]:['Saved actual trials exercise thirteen generated scientific and three lifecycle comparisons; all nine advertised operations, capability asymmetry and corrupt-replay attribution defect remain explicit.','Exact authored unit/set example and typed-layer cases specify common-domain equality; no extra adapter execution or consumer acceptance is claimed.'],
        expected[2]:['Pinned legacy and modern MCP originals, installed SDK snapshots, request/response schemas and local adapter were reread; only legacy 2025-11-25 was exercised.','A nine-row authored decision reference and wire test matrix separate protocol/schema axes; modern or dual-era support is not implemented or wire-tested.'],
        expected[3]:['The exact-release receipt contract and seven missing owner groups are hash-bound; current input_receipts is empty and intake checks do not authenticate authority or truth.','A six-gate table and six release-change cases reproduce proposal logic only; no identity, signature, independent review, bank acceptance or adoption is manufactured.']}
    for i,op in enumerate(expected):
        if i:
            state=core.read(ROOT,core.STATE); before=core.sha(ROOT/core.STATE)
            event=run.apply(ROOT,state,'start',op,reason='Continue the reviewed independent integration requirement sequence; prior operation is durably recorded.')
            run.commit(ROOT,before,state,event)
        state=core.read(ROOT,core.STATE)
        graph,_,_=run.combined(ROOT,state); node=run.ledger.operation(graph,op)
        out=ROOT/node['outputs'][0]; out.parent.mkdir(parents=True,exist_ok=True)
        ev=evidence_common+[ref(BASE/'exact-results.json','Five authored finite reference families')]
        write(out,{'status':'proposal_requirement_reviewed','operation':op,
            'criterion_findings':findings[op],'evidence':ev,
            'proposal_only':True,'capability_granted':False,'bank_acceptance':False,
            'implementation_repair_completed':False,'limits':LIMITS,
            'next_local_action':'Continue the next independent proposal requirement; then review and compile the integrated reader.'})
        receipt=run.ledger.receipt_template(node)
        receipt.update(outcome='pass',execution='performed',scope='Author-reviewed proposal requirement; no product qualification',
            reviewer=REVIEWER,limitations=LIMITS,outputs=[ref(out,'Reviewed requirement review')],
            nonexecution_reason='',revisit_trigger='',
            criteria=[{'index':j,'verdict':'pass','finding':findings[op][j],
                'evidence':ev} for j in range(2)])
        rec=BASE/'operation-receipts'/op/'operation-receipt.json'
        write(rec,receipt)
        state=core.read(ROOT,core.STATE); before=core.sha(ROOT/core.STATE)
        event=run.apply(ROOT,state,'record',op,str(rec.relative_to(ROOT)))
        run.commit(ROOT,before,state,event)
    print(json.dumps({'recorded_sequentially':expected,'proposal_operations':sum(1 for _ in expected),
        'capabilities':[],'next':run.status(ROOT,core.read(ROOT,core.STATE))['next']}))


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('command',choices=['evidence','contract','prepare-reader','build-reader','record-operations'])
    args=parser.parse_args()
    {'evidence':evidence,'contract':contract,'prepare-reader':prepare_reader,
     'build-reader':build_reader,'record-operations':record_operations}[args.command]()



#!/usr/bin/env python3
"""Review exact MCP source profiles and authored witnesses without native execution."""
import argparse,hashlib,json
from pathlib import Path
import mcp_reuse_reference_20261024 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-24/mcp-reuse-v1'
PRIOR=ROOT/'docs/program/execution/2026-10-24/frameworks-reuse-reader-v1/reader/source-audit.json'
read=lambda p:json.loads(p.read_text())
LIMITS=['Selected pinned originals and authored exact examples; no downloaded SDK code, service or native benchmark executed.',
 'Source declarations, protocol constants, snapshots and dynamic versions are not installed artifacts or a solved environment.',
 'Selected routines do not establish absence across every callback, transport, configuration or uninspected delegate.',
 'Original root notices are recorded; complete dependency/contribution rights, support, prices and native conformance remain open.',
 'Additional SDK/language candidates, hosted/local backends, frontier coverage, visual, independent and final acceptance remain open.']
PROFILES={
 'official':('MCP specification and selected official Python/TypeScript SDKs','SW.DECISION.seed_106',['python','typescript']),
 'fastmcp':('FastMCP implementations: SDK migration boundary and separate PrefectHQ project','SW.DECISION.seed_107',['python','fastmcp']),
 'r':('Posit mcptools R implementation','SW.DECISION.seed_108',['r']),
 'java':('Official Java MCP SDK','SW.DECISION.seed_109',['java']),
 'cpp':('Three concrete C++ MCP implementations','SW.DECISION.seed_110',['cpp_hkr','cpp_jesspig','cpp_vogler'])}
VERSIONS={'python':'MCP2.x source tree with dynamic version; separately inspected mcp-types registry',
 'typescript':'Core/server2.3.1;Node>=20;root licensing transition retained',
 'java':'2.1.0-SNAPSHOT;Java17;selected constants through2025-11-25',
 'fastmcp':'Dynamic-version PrefectHQ root/slim composition;selected mcp>=2,<3 extra',
 'r':'1.0.3.9000 development source;R>=4.1;registry through2025-11-25',
 'cpp_hkr':'CMake2025.03.26;protocol constant2025-03-26',
 'cpp_jesspig':'SDK0.3.5;registry through2026-07-28',
 'cpp_vogler':'CMake0.1.0;selected protocol declarations through2025-11-25'}
SPANS={
 'python_source_0':[(1,21)],'python_source_1':[(1,45),(116,130)],
 'python_source_2':[(1,13)],'python_source_3':[(1,16)],
 'python_source_4':[(1070,1155)],'python_delegate_0':[(1,74)],
 'python_delegate_1':[(132,198)],'python_contract_0':[(186,226)],
 'typescript_source_0':[(1,9)],'typescript_source_1':[(1,18)],'typescript_source_2':[(1,18)],
 'typescript_source_4':[(2365,2477)],
 'java_source_0':[(1,21)],'java_source_1':[(1,34),(53,60)],
 'java_source_2':[(685,745)],'java_source_3':[(570,598)],
 'java_contract_0':[(1,29)],'java_contract_1':[(28,55)],
 'fastmcp_source_0':[(1,18)],'fastmcp_source_1':[(1,20),(36,58)],
 'fastmcp_source_2':[(1,18),(50,106)],'fastmcp_source_3':[(1357,1439),(1465,1533)],
 'fastmcp_source_5':[(393,459)],'fastmcp_source_6':[(145,180),(230,305)],
 'r_source_0':[(1,21)],'r_source_1':[(1,51)],'r_source_2':[(1,32)],
 'r_source_4':[(76,113),(278,330)],'r_source_6':[(1075,1125),(1146,1200)],
 'cpp_hkr_source_0':[(1,21)],'cpp_hkr_source_1':[(1,10)],'cpp_hkr_source_4':[(22,42)],
 'cpp_hkr_source_5':[(560,615),(1294,1350)],'cpp_hkr_source_6':[(105,125)],'cpp_hkr_delegate_0':[(1,30)],
 'cpp_jesspig_source_0':[(1,21)],'cpp_jesspig_source_1':[(39,48)],'cpp_jesspig_source_2':[(1,24)],
 'cpp_jesspig_source_3':[(60,100)],'cpp_jesspig_source_4':[(961,1015),(1075,1130)],
 'cpp_jesspig_source_6':[(1,27)],'cpp_jesspig_delegate_0':[(1,9)],'cpp_jesspig_delegate_1':[(25,69)],
 'cpp_vogler_source_0':[(1,9)],'cpp_vogler_source_1':[(1,12)],
 'cpp_vogler_source_2':[(320,388)],'cpp_vogler_source_4':[(20,84)],
 'cpp_vogler_delegate_0':[(85,115)],'cpp_vogler_delegate_1':[(20,43)]}
CLAIMS={
 'python':['SDK2.x removes legacy FastMCP import in favor of MCPServer;dynamic package version is not inferred.',
  'Delegated registry enumerates handshake and modern eras;unknown versions compare conservatively.',
  'Successful client result validates when an output schema is available;refresh/warning and missing-content branches are explicit.',
  'High-level conversion with schema but no output model does not validate in that routine;separate paths/configurations remain qualified.'],
 'typescript':['Core/server source declares2.3.1 and Node>=20;root notice preserves mixed licensing transition.',
  'Selected client compiles output schema before request;cache-store error can report and continue without validation.',
  'Available validator enforces structured-content presence and shape on successful results.',
  'Specific modern header-mismatch recovery refreshes and retries once;not generic exactly-once economic execution.'],
 'java':['Source snapshot2.1.0-SNAPSHOT and Java17;selected constants list four legacy revisions.',
  'Input validator skips disabled,missing/empty-schema or absent-validator cases;validation failure returns tool error.',
  'Client skips disabled-cache/error-result validation;missing cached schema warns;available schema is checked.',
  'No-argument listTools follows cursors and aggregates;no scientific or transport-wide parity claim.'],
 'fastmcp':['Historical repository identity redirects to PrefectHQ;dynamic root/slim composition differs from SDK migration stub.',
  'Selected extras declare MCP2 range;Apache original notice retained;environment not solved.',
  'Server applies middleware by default and resolves unspecified tool version to highest available.',
  'Raw and convenience client calls differ on tool-error raising;failed work remains in denominators.',
  'Function timeout rejects late thread result after shielded execution;not guaranteed remote rollback.'],
 'r':['Development1.0.3.9000,R>=4.1,MIT and component dependencies are explicit.',
  'Registry ends2025-11-25;structured result conversion excludes earlier-than2025-06-18 protocol.',
  'Automatic structured-content predicate excludes dataframe,matrix,array and unnamed entries;not a claim that no content can be returned.',
  'Client distinguishes protocol/tool errors and structured results;interrupt attempts courtesy cancellation,then rethrows.'],
 'cpp_hkr':['Protocol constant2025-03-26 and MIT notice;tool serializer has input schema/annotations.',
  'Selected callback path shows no schema validation before invoking handler and wraps callback content;ordinary exceptions become tool errors.',
  'No separate structuredContent field in that selected handler;custom callbacks/extensions not excluded.'],
 'cpp_jesspig':['SDK0.3.5,MIT and protocol registry through2026-07-28 are distinct identities.',
  'Selected wrapper maps caught exceptions to tool-error result;server exposes cooperative cancellation flag.',
  'Output validator branch requires both schema and structured content;branch alone does not enforce missing-content rejection.',
  'Selected task-mode branch rejects modern-era calls;not generic native conformance evidence.'],
 'cpp_vogler':['CMake0.1.0;root notice retains licensing transition;selected protocol declarations through2025-11-25.',
  'Result model serializes structured content and error status;router dispatch has no schema check shown.',
  'Cancellation state propagates to children and exposes polling;no external rollback proof.']}

def prepare():
    assert not (BASE/'review.json').exists()
    pins={x['role']:x for x in read(BASE/'pins.json')};records={};uninspected=[];all_records=[]
    manifests={}
    for n in ['source','delegate','contract']:
        manifests.update({x['id']:x for x in read(BASE/(n+'-manifest.json'))['requests']})
    rows=sum([read(BASE/(n+'-inventory.json')) for n in ['source','delegate','contract']],[])
    assert len(rows)==68 and len({x['id'] for x in rows})==68
    for row in rows:
        p=ROOT/row['local_path'];data=p.read_bytes();receipt=read(p.with_name(p.stem+'.receipt.json'));req=manifests[row['id']];pin=pins[row['role']]
        assert receipt['status']=='saved' and receipt['url']==req['url']
        assert receipt['sha256']==hashlib.sha256(data).hexdigest()
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==row['blob_sha']
        assert pin['date']<='2026-10-07T23:59:59Z'
        spans=SPANS.get(row['id'].removeprefix('exec24_mcp_'),[]);lines=data.decode().splitlines();anchors=[]
        for lo,hi in spans:
            assert 1<=lo<=hi<=len(lines),(row['id'],lo,hi,len(lines))
            excerpt='\n'.join(lines[lo-1:hi]);anchors.append(dict(upstream_path=row['repository_path'],lines=[lo,hi],excerpt_sha256=hashlib.sha256(excerpt.encode()).hexdigest(),inspection='Author inspected selected substantive source;no execution'))
        r=dict(source_identity=req['url'],version_date=pin['date']+'; '+pin['commit'],local_copy=ref(p,'Authentic pinned original'),git_blob_sha1=row['blob_sha'],receipt=ref(p.with_name(p.stem+'.receipt.json'),'HTTPS acquisition'),inspected_anchors=anchors,technical_inspected=bool(anchors),executed=False)
        all_records.append(r)
        if anchors:records.setdefault(row['role'],[]).append(r)
        else:uninspected.append(dict(id=row['id'],repository_path=row['repository_path'],reason='Acquired inventory only;no new technical claim'))
    write(BASE/'acquisition-review.json',dict(status='pass',files=68,identity=ref(BASE/'pins.json','Eight cutoff repository pins'),records=all_records))
    old=read(PRIOR);keys=['v12_mcp_basic','v12_mcp_legacy_lifecycle','v12_mcp_versioning']
    inherited=[s for s in old['sources'] if s['integrated_citation_key'] in keys];assert len(inherited)==3
    for s in inherited:verify_bindings(s)
    write(BASE/'inherited-review-bindings.json',dict(prior_audit=ref(PRIOR,'Preserved complete predecessor audit'),sources=inherited,scope='Protocol-era findings preserved;new source profiles do not replace historical SDK evidence'))
    write(BASE/'primary-review.json',dict(status='pass_for_selected_static_contracts',profiles=VERSIONS,records=records,claims=CLAIMS,uninspected_acquired_files=uninspected,evidence=[ref(BASE/'acquisition-review.json','All68 original byte identities'),ref(BASE/'inherited-review-bindings.json','Retained protocol editions')],limitations=LIMITS))
    assert exact.calculate()==read(BASE/'exact-results.json')
    write(BASE/'mathematical-review.json',dict(status='pass_for_exact_authored_witnesses',evidence=[ref(Path(exact.__file__),'Independent standard-library code'),ref(BASE/'exact-results.json','Exact outputs'),ref(BASE/'development.tex','Explained definitions and assumptions')],findings=['Declared version intersection2025-03-26 is necessary only;no native interoperability inferred.','Shape-valid monetary objects normalize to1 and1000USD.','Endpoint-marked graphs collapse under adjacency projection;inverse impossible on both.','Under A=U,Y(a)=U,observed difference1 and causal effect0.','Cancellation after500USD commit leaves charge;naive retry yields1000USD.','Scientific missing and true zero collapse under invalid zero fallback.','100/90/80/60 statuses yield3/5,2/3,3/4 rates;18000USD yields180/200/300USD costs.'],native_execution=False))
    constraints={
     'official':'Pin protocol era,transport,SDK/types packages and scientific schema;validate required scientific fields independently of cache behavior;preserve original license transition.',
     'fastmcp':'Distinguish obsolete SDK FastMCP import from PrefectHQ composition;pin tool revision,middleware and extras;preserve raw error flags,timeouts and complete attempt costs.',
     'r':'Use explicit typed envelope for estimates,covariance and graphs;retain protocol version and conversion status;reconcile cancellation and ellmer error surfaces.',
     'java':'Pin snapshot and transport;require input validation and output-schema availability;retain paginated listings,tool errors and scientific status.',
     'cpp':'Choose among hkr04,jesspig and vogler75 per declared era and callback contract;add explicit schema/semantic guard,cooperative cancellation and durable external-job reconciliation.'}
    for key,(name,op,roles) in PROFILES.items():
        next_action='Retain reviewed reference; '+constraints[key]+' Resolve exact distributions,dependencies and contribution rights;run public library/CLI/MCP equivalence,refusal,configuration,pagination,cancellation,replay and cost fixtures before native integration.'
        choice=dict(operation=op,candidate=name,canonical_candidate=name,decision='reference',selected_profiles=[dict(role=k,version=VERSIONS[k],pin=pins[k]) for k in roles],reason='Exact selected source contracts support a concrete proposal comparison;no native or unrestricted scientific capability follows.',alternatives=[dict(route='adopt',decision='defer',reason='No resolved native environment or full scientific contract qualification'),dict(route='integrate',decision='conditional',reason=constraints[key]),dict(route='port',decision='selective_conditional',reason='Only justified stable adapter behavior after source rights and maintenance comparison;no unnecessary estimator or whole-protocol rewrite'),dict(route='reference',decision='retain',reason='Original pinned source supports explicit contracts and limits'),dict(route='reject',decision='restricted',reason='Reject silent schema downgrade,uncertainty loss,missing-to-zero and unsupported exactly-once or termination claims')],owners=[dict(role=k,responsibility=v) for k,v in [('Scientific','Intervention,target,graph and assumptions'),('Statistical','Identification status,dependence,uncertainty and refusal'),('Adapter','Round-trip semantics,units,error taxonomy and logical identities'),('Platform','Artifact,rights,configuration,budgets,recovery and costs')]],costs=dict(measured=False,illustration='18000USD over100 submitted,90 returned and60 qualified gives180,200,300USD',categories=['all submissions','failed and interrupted work','retries','remote effects','human review','maintenance']),maintenance='Exact source pin;complete distribution and platform support remain to qualify',conversion_contract=constraints[key],integration_allowed=False,capabilities=[],revisit_trigger=next_action,limitations=LIMITS)
        write(BASE/(key+'-choice.json'),choice)
    write(BASE/'omissions-register.json',dict(global_blocker=False,remaining=['Other official SDKs,additional R/C++ candidates and search tails','Complete runtime/transitive dependencies and configuration paths','Native protocol and scientific equivalence evidence','Hosted/local model-backend comparison','Frontier originals and broader coverage','Visual,independent and final acceptance'],uninspected_acquired_files=uninspected,known_routes=['Acquire authentic pinned remaining delegates','Run shared public/generated native equivalence and refusal fixtures after environment review','Preserve side-effect identity and complete-cost observations'],unknown_without_information=['Unobserved assignment truth or confounding','Lost graph marks,uncertainty or units','Universal dependent-data/adaptive-inference validity'],next_action='Integrate five bounded reference choices;continue independent remaining software,backend and frontier obligations without closing exhaustive coverage.'))
    sources=[]
    for key,rs in records.items():
        sources.append(dict(integrated_citation_key='exec24_mcp_'+key,kind='software_primary_sources',title=key+' MCP exact protocol,validation,result and recovery source contracts',author=key+' project contributors',year=2026,source_identity=rs[0]['source_identity'],version_date=VERSIONS[key]+'; '+pins[key]['date']+'; '+pins[key]['commit'],local_copy=rs[0]['local_copy'],records=rs,inspected_anchors=[a for r in rs for a in r['inspected_anchors']],supported_claims=CLAIMS[key],limitations=LIMITS))
    assert len(sources)==8
    sources.append(dict(integrated_citation_key='exec24_mcp_contracts',kind='project_evidence_not_scholarly_paper',title='Cross-language MCP scientific-equivalence,refusal,cancellation and complete-cost contracts',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='24October2026;cutoff7October2026;authored finite constructions;no native execution',local_copy=ref(BASE/'mathematical-review.json','Exact authored witness review'),inspected_anchors=[ref(BASE/n,'Bounded comparison') for n in ['primary-review.json','inherited-review-bindings.json','omissions-register.json']]+[ref(BASE/(k+'-choice.json'),'Candidate-specific reference choice') for k in PROFILES],supported_claims=['Eight specific implementation profiles and five reference dispositions','Scientific equivalence differs from protocol/tool success','Exact graph,units,identification,cancellation and denominator witnesses','Conditional public qualification before expensive bank experiments'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,new_records=9,new_scholarly_pdfs=0,preserved_inherited_records=3,native_execution=False))
    write(BASE/'plan-review.json',dict(status='pass_for_bounded_source_wave',evidence=[ref(BASE/n,'Reviewed inputs') for n in ['plan.md','primary-review.json','mathematical-review.json','omissions-register.json']],findings=['Five distinct decisions resolve concrete sources,not language-wide approval.','Version,protocol,transport and schema identities separate;dynamic/snapshot declarations retained.','Selected-path gaps are not whole-product absence claims.','Public oracles and native qualification gates precede expensive bank work.','Independent source work does not wait for unrelated canonical publications.']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_bounded_argument',evidence=[ref(BASE/'development.tex','Connected scholarly banking argument'),ref(BASE/'sponsor-addition.md','Investment implications')],findings=['Question,notation,assumptions,source alternatives,diagnostics and monetary implications connected.','Project witnesses distinct from source inspection and verified native performance.','Exact word choices preserve missing-validation,conversion and cancellation scope.'],visual_acceptance=False))
    evidence=[ref(BASE/n,'Reviewed evidence') for n in ['acquisition-review.json','primary-review.json','inherited-review-bindings.json','mathematical-review.json','exact-results.json','source-audit.json','omissions-register.json','plan-review.json','copyedit-review.json','development.tex','sponsor-addition.md']]+[ref(BASE/(k+'-choice.json'),'Candidate disposition') for k in PROFILES]+[ref(Path(__file__),'Review procedure')]
    result=dict(status='pass_for_bounded_mcp_reference_wave',reviewer=dict(name='Codex author/coordinator',kind='author'),evidence=evidence,findings=['68 acquired originals authenticated against HTTPS SHA256 and Git blob identity.','Eight technical profiles,nine new citation records,five proposal reference decisions.','Exact project examples reproduce;no native,exhaustive,visual or final acceptance.'],limitations=LIMITS)
    verify_bindings(result);write(BASE/'review.json',result);print(json.dumps(dict(originals=68,inspected=sum(len(v) for v in records.values()),new_records=9,reference_decisions=5,native_execution=False)))

def receipt(key):
    name,op,_=PROFILES[key];state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==op
    verify_bindings(read(BASE/'review.json'));graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,op)
    value=read(BASE/(key+'-choice.json'));value.update(status='pass',scope='Bounded '+name+' proposal reference choice;no native admission',evidence=[ref(BASE/'review.json','Author review')])
    out=ROOT/node['outputs'][0];write(out,value);evidence=[ref(BASE/n,'Reviewed choice') for n in ['review.json','primary-review.json',key+'-choice.json','mathematical-review.json','omissions-register.json']]
    findings=['Concrete component/revision,dependency and original notice identities reviewed.','Adopt/integrate/port/reference/reject alternatives,owners,costs and conversion explicit.','Bounded reference choice;native and scientific qualification remain separately gated.']
    r=run.ledger.receipt_template(node);r.update(outcome='pass',execution='performed',scope=value['scope'],reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(out,'Reference disposition')],criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=value['revisit_trigger']);run.validate_receipt(ROOT,merged,node,r,len(state['execution_program']['turns']));verify_bindings(r);write(BASE/(key+'-operation-receipt.json'),r);print(name+' receipt prepared.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare']+list(PROFILES));a=p.parse_args();prepare() if a.command=='prepare' else receipt(a.command)

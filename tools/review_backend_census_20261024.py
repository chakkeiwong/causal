#!/usr/bin/env python3
"""Review bounded pinned backend sources; no downloaded source is executed."""
from pathlib import Path
import hashlib,json
import backend_contract_reference_20261024 as exact
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'docs/program/execution/2026-10-24/backend-census-v1'
RAW=ROOT/'docs/literature/raw';read=lambda p:json.loads(p.read_text())
LIMITS=['Five pinned implementation profiles,not exhaustive providers,models or deployment variants.',
 'Client/source contracts are not commercial-server guarantees or native model measurements.',
 'No downloaded code,model call,installed SDK,weights or vendor server executed.',
 'Direct source notices do not clear dependencies,model weights,service entitlement,data or bank deployment.',
 'OpenAI guide originals remain HTTP403 after the bounded elevated retry;additional provider and service evidence remains open.',
 'Authored costs,timings and outcomes are stipulated mathematical examples,not observed vendor prices or bank value.',
 'Visual,independent,full coverage and final acceptance remain open.']
SPECS={
 'anthropic':{
  'file_0':[(1,19,'Official SDK role,documentation route and major-version migration distinction'),(47,57,'Python3.10and direct MIT notice')],
  'file_1':[(1,7,'MIT grant,notice condition and disclaimer')],
  'file_2':[(1,45,'Version1.11.0,Python3.10,declared httpx2 and optional platform dependencies')],
  'file_3':[(1,2,'Explicit1.11.0source version')],
  'file_4':[(686,708,'Strict object validation versus construction;validation errors retained'),(837,896,'Retry hints,backoff and status-specific retry policy')],
  'file_6':[(85,107,'Native stop/refusal and streaming-incomplete states'),(123,135,'Usage counts differ from visible content length')],
  'file_8':[(8,14,'Ten-minute timeout profile,two retries and local backoff constants')],
  'extra_0':[(158,183,'Configurable timeout,retry and strict-response-validation default false')],
  'extra_2':[(1,13,'Explicit JSON-schema output format type')],
  'extra_3':[(11,25,'Output effort and schema configuration,not scientific validation')]},
 'google':{
  'file_0':[(723,748,'Direct Python function automatic execution can be disabled'),(838,843,'ANY-mode remote-call description'),(873,895,'Two remote calls for one automatic tool turn example')],
  'file_1':[(1,6,'Apache2.0direct notice')],
  'file_2':[(4,38,'Version2.28.0,Python3.10,rights and dependency declarations')],
  'file_3':[(14,16,'Explicit2.28.0version')],
  'file_5':[(6207,6279,'Remote-call loop stops before executing final returned tool requests;history retained')],
  'file_6':[(510,543,'Native stop,limit,filter and invalid-tool states'),(2636,2664,'Retry attempts include original request;declared defaults'),(2694,2729,'API version,timeout milliseconds and separate retry configuration'),(5713,5738,'Automatic function calling default and history setting'),(8864,8946,'Pydantic validation versus plain JSON parsing;error handling leaves parsed unset')],
  'extra_0':[(355,387,'Multiple function parts per response and exception-to-error-response path')]},
 'ollama':{
  'file_1':[(1,21,'MIT notice and conditions')],
  'file_2':[(1,26,'Official client,Python3.8,dependencies and VCS-derived version')],
  'file_3':[(84,99,'Timeout defaults to none'),(141,203,'HTTP errors,stream chunk parsing and typed response construction'),(344,408,'Chat sends tool declarations and format then returns response;no automatic execution loop here')],
  'file_4':[(230,259,'Native done states,token counts and nanosecond durations')]},
 'vllm':{
  'file_0':[(1,6,'Apache2.0direct notice')],
  'file_1':[(1,36,'Build dependencies,Python range,dynamic version/dependencies and license')],
  'file_2':[(1,39,'Structured-output interface and automatic backend default')],
  'file_3':[(86,135,'Named/required broad prose qualified by structural-tag versus schema-derived constraints and strictness switches')],
  'file_4':[(16,30,'Compatible endpoints with parameter/model qualifications'),(67,80,'Extra parameters and model-repository generation defaults')],
  'file_5':[(12,34,'Automatic backend selection and backend-specific schema/whitespace settings'),(61,73,'Configuration validation limits')],
  'extra_0':[(4,12,'Generated version import or dev fallback;no release wheel inferred')]},
 'llamacpp':{
  'file_0':[(1,21,'MIT source notice')],
  'file_1':[(1,20,'Base0.6.0with default development mode')],
  'file_2':[(569,587,'Grammar/schema controls,prediction-time qualification and cache reproducibility limit')],
  'extra_0':[(2072,2083,'Time limit checked on a newline branch'),(2659,2668,'Cancel task releases matching slot only in selected branch')]}}
VERSIONS={'anthropic':'1.11.0;Python>=3.10;MIT','google':'2.28.0;Python>=3.10;Apache2.0',
 'ollama':'VCS-derived version not resolved to release;Python>=3.8;MIT',
 'vllm':'Pinned development source;dynamic version;Python>=3.10,<3.15;Apache2.0',
 'llamacpp':'Base0.6.0;development default ON;MIT'}
ROLES={'anthropic':'Official Anthropic Python client object,stop and retry contracts',
 'google':'Google GenAI Python parsing,automatic function and attempt contracts',
 'ollama':'Official Ollama Python request,stream and duration contracts',
 'vllm':'vLLM compatible serving,parser strictness and generation configuration',
 'llamacpp':'llama.cpp constrained generation,prediction-time and cancellation contracts'}


def main():
    assert not (BASE/'review.json').exists()
    pins={x['key']:x for x in read(BASE/'pinned-identities.json')}
    entries=read(BASE/'source-index.json')+read(BASE/'source-index-extra.json');auth=[];records={r:[] for r in pins}
    for item in entries:
        role=item['role'];pin=pins[role];assert pin['date']<='2026-10-07T15:59:59Z'
        tree=read(RAW/f'exec24_backend_{role}_tree.json');assert not tree['truncated']
        by={x['path']:x for x in tree['tree']};p=ROOT/item['raw_path'];data=p.read_bytes();receipt=p.with_suffix('.receipt.json');r=read(receipt)
        assert r['status']=='saved' and r['url']==item['url'] and hashlib.sha256(data).hexdigest()==r['sha256']
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==item['blob_sha']==by[item['upstream_path']]['sha']
        index=str(item['index']);key=index if index.startswith('extra_') else 'file_'+index
        inspected=key in SPECS[role];auth.append(dict(source=item,local_copy=ref(p,'Authenticated source bytes'),receipt=ref(receipt,'Public acquisition'),technically_inspected=inspected))
        if not inspected:continue
        lines=data.decode().splitlines();anchors=[]
        for lo,hi,finding in SPECS[role][key]:
            assert 1<=lo<=hi<=len(lines),(role,key,lo,hi,len(lines))
            anchors.append(dict(lines=[lo,hi],excerpt_sha256=hashlib.sha256('\n'.join(lines[lo-1:hi]).encode()).hexdigest(),finding=finding))
        records[role].append(dict(source_identity=item['url'],version_date=pin['date']+';'+pin['commit'],
            upstream_path=item['upstream_path'],local_copy=ref(p,'Inspected primary source'),acquisition_receipt=ref(receipt,'Acquired original'),git_blob_sha1=item['blob_sha'],inspected_anchors=anchors,supported_claims=[x['finding'] for x in anchors],executed=False))
    assert len(auth)==45
    write(BASE/'authenticated-source-index.json',dict(authenticated=45,inspected=sum(len(r) for r in records.values()),records=auth))
    attempts=[]
    for key in ['structured','function','background']:
        for suffix in ['', '_retry']:
            p=RAW/f'exec24_backend_openai_{key}{suffix}.receipt.json';r=read(p);assert r['status']=='failed' and '403' in r['error']
            attempts.append(ref(p,'Denied official original;no technical claim'))
    write(BASE/'acquisition-review.json',dict(status='five_pinned_profiles_acquired_with_local_openai_omission',
        evidence=[ref(BASE/'pinned-identities.json','Pre-cutoff commits'),ref(BASE/'authenticated-source-index.json','45full-byte and Git-blob checks')],
        denied_official_originals=attempts,openai_search=ref(BASE/'web-discovery.json','No visible usable source from server search/open'),
        global_blocker=False,cutoff='2026-10-07T15:59:59Z',downloaded_code_executed=False))
    assert exact.calculate()==read(BASE/'exact-results.json')
    sources=[]
    for role,pin in pins.items():
        sources.append(dict(integrated_citation_key='exec24_backend_'+role,kind='software_primary_sources',title=ROLES[role],author=pin['repository']+' contributors',year=2026,
            source_identity=f'https://github.com/{pin["repository"]}/tree/{pin["commit"]}',version_date=VERSIONS[role]+';'+pin['date']+';'+pin['commit'],
            local_copy=records[role][0]['local_copy'],records=records[role],identity_evidence=[ref(BASE/'pinned-identities.json','Exact source identity'),ref(BASE/'acquisition-review.json','Acquisition limits')],
            inspected_anchors=[r['local_copy'] for r in records[role]],supported_claims=[c for r in records[role] for c in r['supported_claims']],limitations=LIMITS))
    sources.append(dict(integrated_citation_key='exec24_backend_reference',kind='project_derivation_and_exact_reference',title='Authored backend schema,tool-budget,deadline and all-request ranking examples',author='Causal banking proposal project',year=2026,
        source_identity='tools/backend_contract_reference_20261024.py',version_date='24October2026;exact authored finite constructions',local_copy=ref(Path(exact.__file__),'Independent authored code'),
        inspected_anchors=[ref(BASE/'exact-results.json','Exact arithmetic'),ref(BASE/'development.tex','Explained assumptions'),ref(BASE/'acquisition-review.json','Explicit provider omissions')],
        supported_claims=['Typed three-edge cycle fails DAG requirement.','Two remote calls can surround three executed and two pending local tool requests;stipulated total10.50USD.',
            'Conditional newline check gives stipulated16second end-to-end despite2second prediction setting.','Two retries mean3attempts;specified requests and waits total36seconds.',
            'Conditional90versus80percent reverses at45versus72percent all-request;costs10/3versus5/2USD per correct response.','Four paired logical cases differ from repeated model attempts.'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,records=6,new_scholarly_pdfs=0,cutoff='2026-10-07',native_execution=False))
    write(BASE/'mathematical-review.json',dict(status='pass_for_exact_authored_witnesses',findings=sources[-1]['supported_claims'],evidence=[ref(Path(exact.__file__),'Exact procedure'),ref(BASE/'exact-results.json','Reproduced rational values'),ref(BASE/'development.tex','Definitions and assumptions')],limitations=LIMITS))
    choices=[dict(profile=role,revision=pins[role],decision='reference',conditional_integration='Original client or local worker after exact environment,model/service,rights,conversion and public scientific qualification.',
        port='Reject wholesale port without a measured need and semantic equivalence case.',integration_allowed=False,capabilities=[],
        owners=['Scientific:target,graph,refusal and loss','Adapter:native states,units,artifacts and conversion','Platform:model/dependency rights,environment and budgets','Evaluation:paired cases,all attempts,coverage and full costs'],
        costs='Unmeasured model/service,hardware,engineering,energy,review,storage and maintenance costs;examples are illustrative.',
        revisit_trigger='Resolve applicable service/model contracts and rights,then preregister public/generated causal-oracle and fault cases before native execution.') for role in pins]
    write(BASE/'choices.json',dict(choices=choices,whole_backend_coverage=False,native_execution=False,evidence=[ref(BASE/'source-audit.json','Component evidence')]))
    write(BASE/'omissions-register.json',dict(global_blocker=False,known_routes=['Acquire applicable official OpenAI originals through an authorized accessible route,without treating403as feature absence.','Extend named hosted/Azure/Bedrock/model families and local-serving delegates with cutoff-aware originals.','Pin model weights,tokenizer,chat template,parser,sampling,quantization,dependencies and rights.','Register public/generated paired causal cases,partial/refusal/error and whole-budget tests,then run only authorized native trials.'],
        no_universal_solution=['A schema cannot supply causal truth or unobserved assignment information.','A provider/client guarantee does not create universal causal uncertainty or bank value.'],
        inventory_only=[x['source']['upstream_path'] for x in auth if not x['technically_inspected']],limitations=LIMITS))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_bounded_comparison',findings=['Business-to-causal target remains primary.','Client,service,model,decoding backend and artifact rights are distinct.','Source-specific structural-tag prose qualifies broader documentation;no unconditional parser guarantee.','Exact hypothetical examples are labelled;no empirical provider ranking.','Original current capability limits and missing named profiles remain explicit.'],evidence=[ref(BASE/'development.tex','Connected chapter'),ref(BASE/'sponsor-addition.md','Sponsor explanation')],visual_acceptance=False))
    write(BASE/'plan-review.json',dict(status='pass_for_preserving_scoped_integration',findings=['45authentic files;selected technical ranges explicit;inventory-only files grant no claims.','Preserve1180source records and257papers;add6software/project records.','No fullL6closure while named provider and applicable-service evidence remains missing.','Keep canonical publication serialized;independent research continues.'],evidence=[ref(BASE/n,'Reviewed input') for n in ['plan.md','acquisition-review.json','source-audit.json','choices.json','mathematical-review.json','omissions-register.json']]))
    review=dict(status='pass_for_bounded_backend_comparison',evidence=[ref(BASE/n,'Reviewed source and argument') for n in ['source-audit.json','authenticated-source-index.json','acquisition-review.json','choices.json','mathematical-review.json','copyedit-review.json','plan-review.json','development.tex','sponsor-addition.md','omissions-register.json','exact-results.json']]+[ref(Path(__file__),'Review logic')],reviewer=dict(name='Codex author/coordinator',kind='author'),findings=['Five pinned source profiles and exact semantic/budget/cost examples inspected.','Reference-only choices;no native or complete backend acceptance.'],limitations=LIMITS,native_execution=False,visual_acceptance=False)
    verify_bindings(review);write(BASE/'review.json',review)
    print(json.dumps(dict(records=6,authenticated=45,inspected=sum(len(r) for r in records.values()),new_papers=0,whole_backend_coverage=False)))


if __name__=='__main__':main()

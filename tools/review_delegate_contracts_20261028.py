"""Record finite original-source inspections without changing inherited audits."""
import hashlib
import json
from pathlib import Path
import delegate_contract_reference_20261028 as exact

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-28/l6-delegate-review-v1'
OLD = ROOT / 'docs/program/execution/2026-10-24'
CUTOFF = '2026-10-07T15:59:59Z'


def read(p):
    return json.loads(p.read_text())


def ref(p, anchor):
    return dict(path=str(p.relative_to(ROOT)), sha256=hashlib.sha256(p.read_bytes()).hexdigest(), anchor=anchor)


def write(p, d):
    assert not p.exists(), p
    p.write_text(json.dumps(d, indent=2) + chr(10))


SPECS = {
 'exec24_framework_langchain_source_1': [(24,27,'Identity and product-scope lead only; no performance or Deep Agents qualification.')],
 'exec24_framework_langchain_source_2': [(92,150,'Narrow retry scope recommended; Exception default, three attempts and exponential jitter.'),(227,288,'Batch retry retains successful results and remaps retries to failed original indices.')],
 'exec24_framework_langchain_source_3': [(778,860,'Dictionary args_schema branch returns input; Pydantic branch validates and handles injected tool identity.'),(1105,1135,'Handled validation/tool errors retain error status; unhandled errors raise.')],
 'exec24_framework_langchain_source_5': [(922,971,'Force stop returns a limit response; generate stop invokes an extra model call.'),(1023,1049,'Iteration/time limits and parsing-error configuration.'),(1235,1238,'Continuation checks iteration and elapsed time.'),(1584,1622,'Synchronous elapsed time updated between steps; stop output is not evidence of causal success.')],
 'exec24_framework_semantic_kernel_source_1': [(1,6,'README names Microsoft Agent Framework migration; separate unreviewed successor lead.'),(15,24,'Project identity and advertised runtime scope only.')],
 'exec24_framework_semantic_kernel_source_3': [(414,446,'Streaming agent merges arguments/settings and delegates to selected chat service.'),(510,542,'Nonstreaming invocation delegates to selected chat service after configuration.')],
 'exec24_framework_semantic_kernel_source_5': [(262,297,'Function invocation passes filter stack, records errors and propagates exceptions.'),(336,378,'Streaming invocation yields partial results and propagates errors; no scientific validator established.')],
 'exec24_framework_dspy_source_1': [(7,18,'Project identity and optimization scope; README does not qualify learned programs.')],
 'exec24_framework_dspy_source_2': [(124,151,'Provided arguments conditionally schema-validated, then typed values parsed through Pydantic.'),(187,210,'Synchronous/asynchronous function paths and coroutine configuration.')],
 'exec24_framework_dspy_source_5': [(148,174,'Bootstrap traces selected from trainset; validation variable uses unbootstrapped training examples.'),(187,223,'Example excluded from teacher demos; metric-dependent success, truthy threshold branch, no-metric success and exception accounting.')],
 'exec24_framework_llama_index_source_1': [(10,17,'README reports parsing/extraction focus; named services and benchmarks are discovery leads, not verified comparisons.')],
 'exec24_framework_llama_index_source_4': [(484,547,'Generate early stopping requests another model result; otherwise iteration limit raises.'),(590,628,'Structured-response exceptions warn before StopEvent; terminal event does not prove structured success.')],
 'exec24_framework_haystack_source_1': [(12,14,'Project identity and advertised orchestration scope only.')],
 'exec24_framework_haystack_source_3': [(1126,1163,'Component/socket and mandatory-input validation.'),(1460,1477,'Visit limit is component-specific, not a workflow HTTP budget.'),(1755,1768,'Blocked pipeline queue raises rather than establishing a completed scientific result.')],
 'exec24_framework_haystack_source_4': [(153,198,'Component execution preserves/wraps errors, counts visits after return and checks mapping/output keys.'),(315,341,'Same breakpoint and snapshot rejected to avoid immediate repeated pause.')],
 'exec24_framework_workflows_source_5': [(336,355,'Cancellation delegated for external context; other contexts warn; store described as process-local.'),(357,408,'Context serialization retains state and queue metadata through delegates; remote exactly-once behavior not established.')],
 'exec24_backend_anthropic_file_5': [(995,1057,'Nonstream timeout may depend on max_tokens/model; request preserves stop,stream,tool and output configuration.')],
 'exec24_backend_anthropic_file_7': [(1,82,'Tool schema and strict/eager streaming declarations; declarations do not independently verify service execution.')],
 'exec24_backend_google_file_4': [(206,211,'Server timeout header uses ceiling of seconds.'),(248,258,'HTTP timeout converts milliseconds to seconds; falsey timeout selects None.'),(896,902,'Client retry configuration delegated to Tenacity.'),(1435,1461,'Request construction carries configured timeouts.'),(1526,1544,'Request-level retry settings override client retry when supplied.')],
 'exec24_backend_google_file_7': [(58,66,'Unsupported function signature raises.'),(330,449,'Signature conversion creates schema, required fields and definitions; Vertex branch handles missing type with anyOf.')],
 'exec24_backend_ollama_file_0': [(1,14,'Python client requires separately running Ollama and selected model; README is not server/model qualification.')],
 'exec24_backend_vllm_file_6': [(761,801,'Schema payload/structural-tag and stream-options validation.'),(918,978,'Tool-choice default and conditional tool presence/name validation; none skips tool validation.')],
 'exec24_backend_llamacpp_file_3': [(390,408,'Unsupported pattern warns and relaxes to any string; invalid pattern records an error.'),(975,1012,'Errors raise, warnings print; LLGuidance and forced/default GBNF paths differ.')],
 'exec24_backend_llamacpp_file_4': [(45,55,'Argument parse fallback can retain text instead of parsed JSON.'),(1422,1446,'Selected template path constructs prompt and selects schema-derived or supplied grammar.')],
 'exec24_backend_llamacpp_file_5': [(251,257,'Native stop classes retain eos,word,limit and none.'),(374,425,'Compatibility response maps native stop and tool presence into finish reason.')],
 'exec24_backend_anthropic_extra_1': [(1,7,'Native stop reason includes refusal,pause,tool use,length and context exhaustion.')],
 'exec24_backend_anthropic_extra_4': [(1,47,'Tool decorator derives schema from signature/docstring.'),(64,105,'Documented runner dispatches by stop reason; eager tool side effects can outlive an interrupted reply.'),(109,145,'Compaction excluded from ordinary iteration count; nested usage, pending-result and stopping rules matter.')],
 'exec24_backend_vllm_extra_1': [(119,170,'Parser configuration includes tool strictness, model, tokenizer and reasoning/tool parser choices.'),(749,777,'Stream maps selected native stops to tool_calls and retains stop_reason.'),(1082,1116,'Nonstream compatibility finish reason depends on tool mode and selected native output.')],
 'exec24_backend_llamacpp_extra_1': [(44,49,'Native stop enumeration.'),(137,153,'Cancellation target and parent-child task identities are represented.'),(249,270,'Child identities collected/copied; declarations alone do not prove cancellation observed.')],
}


def main():
    files = read(BASE/'input-register.json')['files']
    assert len(files)==29 and len(SPECS)==29
    custody = {}
    inputs = []
    for name in ['acquisition-review.json','supplementary-acquisition-review.json','workflow-acquisition-review.json']:
        p=OLD/'framework-census-v1'/name
        inputs.append(ref(p,'Preserved acquisition identity'))
        for row in read(p)['records']:
            custody[row['local_copy']['path']] = dict(row, custody=ref(p,'Selected exact original'))
    p=OLD/'backend-census-v1/authenticated-source-index.json'
    inputs.append(ref(p,'Preserved backend custody'))
    pins={x['key']:x for x in read(OLD/'backend-census-v1/pinned-identities.json')}
    for row in read(p)['records']:
        s=row['source']; pin=pins[s['role']]
        custody[row['local_copy']['path']]=dict(candidate=s['role'],repository=pin['repository'],revision=pin['commit'],commit_date=pin['date'],git_blob_sha1=s['blob_sha'],request=dict(url=s['url']),local_copy=row['local_copy'],acquisition_receipt=row['receipt'],custody=ref(p,'Selected exact original'))
    groups={}; records=[]
    for item in files:
        path=ROOT/item['source']['path']; original=path.read_bytes(); key=path.stem
        c=custody[item['source']['path']]
        assert hashlib.sha256(original).hexdigest()==item['source']['sha256']==c['local_copy']['sha256']
        blob=hashlib.sha1(b'blob '+str(len(original)).encode()+b'\0'+original).hexdigest()
        assert blob==c['git_blob_sha1'] and c['commit_date']<=CUTOFF
        lines=original.decode().splitlines(); anchors=[]
        for lo,hi,finding in SPECS[key]:
            assert 1<=lo<=hi<=len(lines),(key,lo,hi,len(lines))
            excerpt=chr(10).join(lines[lo-1:hi])
            anchors.append(dict(lines=[lo,hi],excerpt_sha256=hashlib.sha256(excerpt.encode()).hexdigest(),finding=finding))
        receipt=c.get('acquisition_receipt') or ref(path.with_suffix('.receipt.json'),'Collector receipt')
        assert hashlib.sha256((ROOT/receipt['path']).read_bytes()).hexdigest()==receipt['sha256']
        record=dict(source_identity=c['request']['url'],version_date=c['commit_date']+';'+c['revision'],upstream_path=item['upstream_path'],local_copy=ref(path,'Inspected original'),acquisition_receipt=receipt,git_blob_sha1=blob,custody=c['custody'],inspected_anchors=anchors,supported_claims=[a['finding'] for a in anchors],scope_only=item['upstream_path']=='README.md',executed=False)
        groups.setdefault(c['candidate'],[]).append(record);records.append(record)
    sources=[]
    for group,rs in groups.items():
        sources.append(dict(integrated_citation_key='exec28_dl_'+group,kind='software_primary_sources',title=group.replace('_',' ').title()+' selected delegate contracts and scope boundaries',author=group.replace('_',' ')+' project contributors',year=2026,source_identity=rs[0]['source_identity'],version_date=rs[0]['version_date'],local_copy=rs[0]['local_copy'],records=rs,inspected_anchors=[a for r in rs for a in r['inspected_anchors']],supported_claims=[c for r in rs for c in r['supported_claims']],limitations=['Only selected anchored branches inspected; not whole-repository assurance.','Pinned client/framework source, not independently verified hosted service or model behavior.','No downloaded code or native model execution.']))
    result=exact.calculate(); assert result['admitted']==1 and result['false_admissions']==['x'] and result['selective_total']==5
    write(BASE/'exact-results.json',result)
    sources.append(dict(integrated_citation_key='exec28_dl_reference',kind='project_derivation_and_exact_reference',title='Authored schema weakening, selective retry and terminal-state witnesses',author='Causal banking proposal project',year=2026,source_identity='tools/delegate_contract_reference_20261028.py',version_date='28 October 2026; authored finite constructions',local_copy=ref(Path(exact.__file__),'Exact independent construction'),inspected_anchors=[ref(BASE/'exact-results.json','Exact local calculation')],supported_claims=['A weakened string constraint admits an extra value in the stipulated domain.','Selective retries total five versus nine whole-batch attempts; stipulated costs USD1.25 versus USD2.25.','Only one of four terminal/validity/identification combinations admits an effect; two ordinary turns plus one separate compaction yield three calls.'],limitations=['Mathematical interface witnesses; not measured package, model, price or bank performance.']))
    write(BASE/'source-audit.json',dict(sources=sources,cutoff=CUTOFF,inspected_files=29,technical_files=23,scope_documents=6,evidence=inputs+[ref(BASE/'input-register.json','Finite scope')],native_execution=False))
    write(BASE/'inspection-review.json',dict(status='pass',scope='All29 finite acquired files dispositioned through relevant technical anchors or explicit identity-only limits',files=records,technical_files=23,scope_documents=6,not_reviewed=['Unlisted implementation branches and transitive delegates; claims restricted to inspected paths.','Microsoft Agent Framework successor source and migration conformance.','Hosted endpoints, exact model/tokenizer/template/parser artifacts and service terms.','Native execution, independent efficacy, bank deployment and fresh visual review.'],inventory_only_files_remaining_in_this_worklist=0,global_L6_coverage_complete=False,evidence=[ref(Path(__file__),'Exact reviewed spans and custody checks')]))
    write(BASE/'mathematical-review.json',dict(status='pass',findings=['Finite requested/relaxed set inclusion is strict.','Selective retry accounting gives five versus nine attempts and exact stipulated costs.','Terminal control flow is separately checked from representation and scientific admission.'],evidence=[ref(Path(exact.__file__),'Authored calculation'),ref(BASE/'exact-results.json','Observed local replay')],native_execution=False))
    print(json.dumps(dict(inspected=29,technical=23,scope=6,citation_records=len(sources),full_L6_coverage=False)))


if __name__=='__main__':
    main()

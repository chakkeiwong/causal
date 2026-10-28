"""Disposition named service/model profiles against acquired source evidence."""
import json
from pathlib import Path
from run_followup_program_20261028 import ROOT,BASE,append,load,bound
from prepare_followup_program_20261028 import ref,write


def main():
    key='L6.PROFILES';node=load()['nodes'][key];day=ROOT/'docs/program/execution/2026-10-28'
    paths=[day/'l6-openai-pinned-v1/source-audit.json',ROOT/'docs/program/execution/2026-10-24/backend-census-v1/source-audit.json',day/'l6-delegate-review-v1/source-audit.json',day/'l6-delegate-criterion-v1/contract-matrix.json']
    evidence=[ref(p,'Existing exact-source findings and limits') for p in paths]
    start=BASE/'l6-profiles-start.json';write(start,dict(task=key,awards_acceptance=False,next_action=node['action'],evidence=evidence));append('start',key,str(start.relative_to(ROOT)))
    audits=[json.loads(p.read_text()) for p in paths[:3]];sources={s['integrated_citation_key']:s for a in audits for s in a['sources']}
    specs=[
      ('OpenAI',['exec28_oa_sdk','exec28_oa_cookbook'],'Official Python client and cookbook','A named hosted API endpoint/model revision and eligible deployment','SDK/cookbook source notices concern those artifacts; selected service/data terms and model entitlement not established.','Retain parsing,phase,refusal and incomplete states; exact request-wide retries/costs need independent qualification.','Obtain dated official service/model terms and endpoint support original through a distinct permitted route; do not rerun failed guide Markdown URLs.'),
      ('Anthropic',['exec24_backend_anthropic','exec28_dl_anthropic'],'Pinned Python SDK and documented tool runner','A named hosted endpoint/model and runner mode','Client-source notice does not establish hosted entitlement,toolset rights or data handling terms.','Normal typed stop and beta runner compaction contracts are distinct; retain eager-tool effects and nested usage.','Identify dated hosted-service/model terms and endpoint contract; a nonallowlisted official host remains a local source route limitation.'),
      ('Google GenAI',['exec24_backend_google','exec28_dl_google'],'Pinned Python GenAI client','Select Developer API or Vertex profile explicitly,with endpoint/model and identity','Source notice does not resolve the selected cloud service,model,region,data or deployment terms.','Schema conversion and per-request retry rules depend on selected client path; do not merge Developer and Vertex semantics.','Acquire permitted dated official endpoint/model/terms originals or authentic local copies for one named profile at a time.'),
      ('Ollama',['exec24_backend_ollama','exec28_dl_ollama'],'Pinned Python client','Separate server build and selected local model manifest','Client source notice is separate from server source,deps,model weights and data rights.','README requires a running server/model; client coverage cannot silently satisfy either artifact contract.','Select official cutoff server commit and one declared model manifest; inspect server API/cancellation and weight-license originals before a runtime claim.'),
      ('vLLM',['exec24_backend_vllm','exec28_dl_vllm'],'Pinned serving/protocol source','Exact server build,model,tokenizer,template,tool/reasoning parser and grammar backend','Serving source license is separate from dependency,model,tokenizer and deployment rights.','Strictness and finish mapping depend on selected configuration; source representation is not observed model conformance.','Freeze a candidate deployment manifest and acquire only missing original config/rights/delegate artifacts; qualify public fixtures later.'),
      ('llama.cpp',['exec24_backend_llamacpp','exec28_dl_llamacpp'],'Pinned grammar,chat and task sources','Exact build flags,grammar backend,model conversion/weights,tokenizer and template','Source notice does not clear chosen weights,conversion or dependencies.','GBNF warning/relaxation and LLGuidance path remain distinct; preserve original schema validation and native stops.','Freeze one build/model manifest; inspect model and converter originals and rights,then test generated-schema and interruption fixtures under a declared budget.'),
    ]
    rows=[]
    for family,keys,inspected,profile,rights,semantics,action in specs:
        records=[]
        for k in keys:
            s=sources[k];bound(ROOT,s['local_copy']);records.append(dict(citation_key=k,source_identity=s['source_identity'],version_date=s['version_date'],local_copy=s['local_copy'],supported_claims=s['supported_claims'],limitations=s.get('limitations',[])))
        rows.append(dict(family=family,inspected_scope=inspected,required_named_profile=profile,rights_boundary=rights,material_contract=semantics,next_action=action,records=records,profile_qualified=False,service_terms_verified=False,current_price_verified=False,native_execution=False,source_disposition='Conditional source reuse only;full service/model profile inconclusive'))
    leads=[]
    for family,k,decision in [
      ('Microsoft Agent Framework','exec28_dl_semantic_kernel','README names migration; need a separate cutoff identity,source/rights and compatibility comparison. No inherited Semantic Kernel qualification.'),
      ('LlamaParse,LiteParse and named parsing benchmarks','exec28_dl_llama_index','README product-focus names are discovery leads; no claimed superiority or adoption. Determine causal observation-construction relevance before acquisition.'),
      ('Deep Agents','exec28_dl_langchain','README introductory link does not qualify its implementation; inspect separately only if selected for the proposed workflow.')]:
        s=sources[k];leads.append(dict(family=family,decision=decision,evidence=[r for r in s['records'] if r['upstream_path']=='README.md'],technical_claims_admitted=False))
    out=BASE/'l6-profiles.json'
    write(out,dict(status='performed_profile_boundary_review',provider_families=rows,migration_and_scope_leads=leads,evidence=evidence+[ref(Path(__file__),'Explicit six-family comparison')],full_L6_coverage='inconclusive',new_online_sources_acquired=False,unknowns=['No complete dated service/model/entitlement/pricing profile is established by this source review.','No universal output-equivalence,cancellation or effectiveness guarantee follows from client compatibility.'],known_route='Artifact-specific public original acquisition and bounded fixture design; independent profiles proceed separately.'))
    receipt=BASE/'l6-profiles-receipt.json';write(receipt,dict(task=key,awards_acceptance=False,execution='performed',outcome='pass',outputs=[ref(out,'Six provider profiles and three discovery leads')],evidence=evidence,criteria=[dict(index=0,verdict='pass',finding='Sixnamed families and three explicit leads have distinct acquired evidence,target profiles and missing original requirements.'),dict(index=1,verdict='pass',finding='No license transfer,service/model entitlement,price or uninspected capability is inferred.')],next_action='Select one local server/artifact profile for bounded permitted acquisition; hosted terms and migration leads remain independent omissions.'))
    append('record',key,str(receipt.relative_to(ROOT)));print(json.dumps(dict(profiles=6,leads=3,full_L6_coverage='inconclusive',next=load()['next'])))


if __name__=='__main__':main()

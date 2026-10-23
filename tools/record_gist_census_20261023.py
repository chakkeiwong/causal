#!/usr/bin/env python3
"""Record one authentic frontier original, pinned artifact review and reproducible CSV audit."""
from pathlib import Path
from collections import Counter
import csv,hashlib,json,xml.etree.ElementTree as ET
from html.parser import HTMLParser
from datetime import datetime
import gist_artifact_reference_20261023 as exact
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1];DAY=ROOT/'docs/program/execution/2026-10-23';BASE=DAY/'census-goal-state-v1';RAW=ROOT/'docs/literature/raw'
read=lambda p:json.loads(p.read_text())
def main():
    state=read(ROOT/'docs/program/state.json');assert state['execution_runtime']['active']['operation']=='LL.CENSUS'
    register=read(DAY/'proof-statspai-v1/census-register.json');old=read(DAY/'census-admission-conformal-v1/census-register-v2.json')
    source=read(RAW/'exec23_gist_abs.receipt.json');paper=RAW/'exec23_gist_v1.pdf';assert source['status']=='saved' and paper.read_bytes().startswith(b'%PDF-')
    paper_sha=hashlib.sha256(paper.read_bytes()).hexdigest();assert paper_sha==hashlib.sha256((ROOT/'docs/papers/GIST-CMTF Goal-State Inference for Causal Minimal Tool Filtering in LLM Agents Babu(2026).pdf').read_bytes()).hexdigest()
    html=(RAW/'exec23_gist_abs.html').read_text()
    class Meta(HTMLParser):
        def __init__(self):super().__init__();self.tags=[]
        def handle_starttag(self,tag,attrs):
            d=dict(attrs)
            if d.get('name','').startswith('citation_'):self.tags.append((d['name'],d.get('content')))
    m=Meta();m.feed(html);meta={};
    for k,v in m.tags:meta.setdefault(k,[]).append(v)
    assert meta['citation_title']==['GIST-CMTF: Goal-State Inference for Causal Minimal Tool Filtering in LLM Agents']
    assert meta['citation_author']==['Babu, Rahul Suresh','Shukla, Rohit'] and meta['citation_date']==['2026/06/15']
    commit=read(RAW/'exec23_gist_commit.json')[0];tree=read(RAW/'exec23_gist_tree.json')
    assert commit['sha']=='e5a83858c6afdf3f3378defbdb723075496f035b' and commit['commit']['tree']['sha']==tree['sha']=='99962404fecb7e4b5b862edc1047bd7be60e4a35' and not tree['truncated']
    assert commit['commit']['committer']['date']<'2026-10-07T15:59:59Z'
    entries={x['path']:x for x in tree['tree']};raw_records=[]
    paths=['README.md','LICENSE','CITATION.cff','requirements.txt','src/gist_cmtf_runner.py','src/expand_gist_tasks.py','data/gist_tasks_120.json','data/gist_tool_registry.json','results/gist_task_metrics.csv','paper_outputs/tables/table_2_main_results_by_method.csv','paper_outputs/tables/appendix_error_breakdown.csv']
    spans={
      'README.md':[(1,68),'The artifact separates deterministic aggregate-table reproduction from provider-backed model-call replay.'],
      'LICENSE':[(1,21),'MIT notice, attribution, warranty and liability terms.'],
      'CITATION.cff':[(1,25),'Names both authors, repository identity and arXiv citation; does not establish scientific evidence.'],
      'requirements.txt':[(1,5),'Five unpinned packages include provider SDK; environment is not locked.'],
      'src/gist_cmtf_runner.py':[(37,64),(211,240),(243,259),(262,323),(382,425),(428,473),(551,585),(618,640),(654,714),'Source-level goal and execution contract, deterministic symbolic path, type-forced clarification, oracle-goal substitution, mismatch between gold-path input and saved task schema, and runner output fields.'],
      'src/expand_gist_tasks.py':[(1,20),(390,403),'Task generator, asserted/sliced total120 and artifact output.'],
      'data/gist_tasks_120.json':[(1,1),(120,120),'120 constructed task objects: request type, candidate goals, annotated intent and gold_chains; no gold_path field.'],
      'data/gist_tool_registry.json':[(1,1),(32,32),'32 symbolic tools and their preconditions/effects.'],
      'results/gist_task_metrics.csv':[(1,1),(5041,5041),'Header and all5040 final per-run records; model, task, outcome, clarification, wrong-tool, token and error fields.'],
      'paper_outputs/tables/table_2_main_results_by_method.csv':[(1,7),'Six aggregate method rows reproduce from final per-run data.'],
      'paper_outputs/tables/appendix_error_breakdown.csv':[(1,7),'Seven error-denominator rows reproduce from final per-run data.']}
    for i,path in enumerate(paths,1):
        file_id=f'exec23_gist_file_{i}';p=RAW/(file_id+('.json' if i in [7,8] else '.txt'));data=p.read_bytes();receipt=read(RAW/(file_id+'.receipt.json'));url=f'https://raw.githubusercontent.com/R-Suresh/GIST-CMTF/{commit["sha"]}/{path}'
        gitblob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert receipt['status']=='saved' and receipt['url']==url and receipt['sha256']==hashlib.sha256(data).hexdigest()
        assert gitblob==entries[path]['sha'] and len(data)==entries[path]['size']
        raw_records.append(dict(source_identity=url,upstream_path=path,git_blob_sha1=gitblob,version_date=commit['commit']['committer']['date']+'; '+commit['sha'],local_copy=ref(p,str(spans[path][0])),receipt=ref(RAW/(file_id+'.receipt.json'),'Bound acquisition receipt'),inspected_anchors=[dict(span=x,claim=spans[path][1]) for x in spans[path][0]],supported_claims=[spans[path][1]],executed=False))
    result=exact.calculate();assert result==read(BASE/'exact-results.json')
    source_record=dict(integrated_citation_key='exec23_gist_sources',kind='software_primary_sources',title='GIST-CMTF cutoff source and benchmark artifact contracts',author='Rahul Suresh Babu and Rohit Shukla',year=2026,source_identity='https://github.com/R-Suresh/GIST-CMTF/tree/'+commit['sha'],version_date='Cutoff commit '+commit['sha']+'; '+commit['commit']['committer']['date']+'; canonical tree '+tree['sha'],records=raw_records,local_copy=raw_records[4]['local_copy'],inspected_anchors=[r['inspected_anchors'] for r in raw_records],supported_claims=[
    'Pinned runner forces clarification for annotated nonexplicit request types and substitutes intended_goal after the clarification action; this is not a real user-turn evaluation.',
    'Pinned runner reads gold_path while all120 saved task objects contain gold_chains and no gold_path; paper metric replay cannot be asserted from this runner plus inputs.',
    'Released final CSV has5040 unique positive-token rows; 53/560 nonexplicit GIST rows show zero clarifications. Paper aggregate tables reproduce from that CSV, not from fresh model calls.',
    'Run CSV has fields absent from the runner writer and lacks writer fields; a separate producer/transform or revision remains possible.',
    'Cutoff default model list names Nova 2 Pro preview while saved final data uses Nova Pro; an explicit override is possible but not retained in inspected artifacts.',
    'MIT source notice is explicit; the five package requirements are unpinned. Latency, costs, users, real APIs, multi-turn clarification and full provider-failure denominator are not established.'],limitations=['Primary paper reports results; source inconsistency leaves producer/cleaning provenance open, not a fabrication finding.','No upstream code or model call executed.','No arbitrary causal diagram discovery, statistical identification, bank benefit or live-client integration is established.'])
    paper_record=dict(integrated_citation_key='exec23_gist_paper',kind='paper',title=meta['citation_title'],filename_title='GIST-CMTF Goal-State Inference for Causal Minimal Tool Filtering in LLM Agents',author='Rahul Suresh Babu and Rohit Shukla',first_author='Babu',year=2026,source_identity='https://arxiv.org/abs/2606.16813v1',version_date='arXiv:2606.16813v1; submitted15 June2026; PDF/'+paper_sha,local_path='docs/papers/GIST-CMTF Goal-State Inference for Causal Minimal Tool Filtering in LLM Agents Babu(2026).pdf',sha256=paper_sha,bytes=paper.stat().st_size,local_copy=ref(ROOT/'docs/papers/GIST-CMTF Goal-State Inference for Causal Minimal Tool Filtering in LLM Agents Babu(2026).pdf','Authentic arXiv v1 PDF'),identity_metadata=ref(RAW/'exec23_gist_abs.html','HTML citation identity; abstract not used as method evidence'),pdf_receipt=ref(RAW/'exec23_gist_v1.receipt.json','Original PDF bytes and acquisition hash'),inspected_anchors=[dict(physical_page=i,anchor=a) for i,a in {1:'Task motivation and reported headline; abstract only',3:'Operational ambiguity as upstream goal assumption',4:'Ambiguity thresholds, clarification action and symbolic contract',5:'Candidate goals and decision rule',6:'120 tasks, six methods and5,040-run design; mocked deterministic environment',7:'Headline results plus explicit-task regression, unnecessary clarification and token costs',8:'Per-request-type outcomes and tradeoff',9:'Backend results and final-row error counts',10:'Limitations: synthetic requests, fixed state vocabulary, open-world gaps, no real-user cost, artifact statement'}.items()],supported_claims=[
    'Tool discovery/filtering assumes a symbolic target goal; goal inference and downstream path filtering are separate tasks.',
    'Clarification can be represented as a state transition; it is a design for controlled preconditions/effects, not an identified causal estimand.',
    'Author-reported 97.0% success versus80.1% top-goal CMTF and2.5% versus19.4% wrong-goal rates are conditional on120 controlled tasks and deterministic mocked tool execution.',
    'Reported explicit requests show lower GIST success than semantic-goal filtering and 16.8% unnecessary clarification; ambiguity handling trades friction for wrong-goal reduction.',
    'The original explicitly lists noisy users, evolving APIs, nondeterministic effects, open-world goals, real users, latency and monetary cost as unresolved.'],limitations=['A single arXiv v1 is reviewed, not peer accepted or independently reproduced.','The paper maps user text to symbolic goals and action/tool transitions; it does not construct or validate a banking causal DAG or effect.'])
    project=dict(integrated_citation_key='exec23_gist_reference',kind='project_authored_data_audit',title='Independent GIST-CMTF final-table reconstruction and source-to-output audit',author='Causal banking proposal project',year=2026,version_date='23 October 2026',source_identity='tools/gist_artifact_reference_20261023.py',local_copy=ref(ROOT/'tools/gist_artifact_reference_20261023.py','Rational aggregation checks and AST-only source/data comparison'),inspected_anchors=['calculate()'],supported_claims=['All six result summaries and error counts exactly reproduce from final CSV; 5,040 rows are unique and positive-token.','53 of560 nonexplicit GIST rows have zero clarification; all120 task records lack runner gold_path although they carry gold_chains.','Runner and CSV output schemas differ; missing producer/cleaning/version evidence is recorded as a reproducibility omission.','Stipulated success/token/clarification values can change illustrative net sign; not measured economics.'],limitations=['Read only downloaded source/artifacts as data and parsed source syntax; executed no upstream code.'])
    assert not (BASE/'source-audit.json').exists();write(BASE/'source-audit.json',dict(sources=[paper_record,source_record,project],cutoff='2026-10-07',native_execution=False))
    items=register['items'];old_items=old['items'];candidate=next(x for x in items if x['id']=='LA01-candidate-172');old_row=next(x for x in old_items if x['id']=='LA01-candidate-172');assert candidate['disposition']=='open_original_not_inspected'
    candidate.update(prior_disposition=candidate['disposition'],disposition='inspected_primary_retained_with_limits',technical_source_review_open=False,source_key='exec23_gist_paper',primary_source_record=paper_record,artifact_source_key='exec23_gist_sources',mapping_basis='Authentic v1 original and cutoff-pinned benchmark inspected; symbolic business-goal mediation maps to business translation and agent architecture. Does not address causal-diagram correctness.',availability='Genuine arXiv PDF authenticated by local hash; selected source files checked against pinned repository Git blobs.',effect_on_claims='Retains a scoped goal-validation design comparator; no general LLM superiority, bank workflow or causal diagram capability claim.',next_action='Keep this source in goal clarification and agent architecture comparisons. Resolve the source-to-data generating revision and label-free user response path before a registered prototype comparison.',publication_keys=['exec23_gist_paper','exec23_gist_sources','exec23_gist_reference'])
    # Move this candidate only within the relevant task-map families; retain every other mapping.
    tm=read(DAY/'census-admission-conformal-v1/task-map-v2.json')
    for family in tm['task_families']:
        un=family.get('uninspected_candidate_ids',[])
        if candidate['id'] in un:
            un.remove(candidate['id']);family.setdefault('inspected_candidate_ids',[]).append(candidate['id'])
            family.setdefault('inspected_source_keys',[]).append('exec23_gist_paper')
        family['coverage_acceptance']=False
    for family_name in ['business_translation','agent_architecture']:
        family=next(x for x in tm['task_families'] if x.get('family')==family_name or x.get('task')==family_name or x.get('id')==family_name)
        if candidate['id'] not in family.get('inspected_candidate_ids',[]):family.setdefault('inspected_candidate_ids',[]).append(candidate['id'])
        family.setdefault('inspected_source_keys',[]).extend(k for k in ['exec23_gist_paper','exec23_gist_sources','exec23_gist_reference'] if k not in family.get('inspected_source_keys',[]))
    old_candidates=sorted(x['id'] for x in old_items if x.get('disposition')=='open_original_not_inspected')
    now_candidates=sorted(x['id'] for x in items if x.get('disposition')=='open_original_not_inspected')
    assert len(old_candidates)==45 and len(now_candidates)==44 and set(old_candidates)-set(now_candidates)=={candidate['id']}
    census=Counter(x['disposition'] for x in items)
    register.update(counts=dict(census),supersedes=ref(DAY/'proof-statspai-v1/census-register.json','Preserved68/45 census'),changes=['Only candidate172 changed from original unread to inspected primary with source limits; all other candidate and crosscutting dispositions remain byte-for-byte deep-equal. Three genuine paper/source/reference audit records attach.'],closure=False,interpretation='69/113 candidate originals inspected;44 unread; four crosscutting searches remain.')
    assert all(old_row==next(x for x in items if x['id']==old_row['id']) for old_row in old_items if old_row['id']!='LA01-candidate-172')
    write(BASE/'census-register.json',register);write(BASE/'task-map.json',tm)
    omissions=dict(items=['The source-to-data producing commit, CLI overrides and full provider/cleaning logs are not bound; saved outputs aggregate, runner replay unproved.','No actual human clarification, open-world or changing-API study; no latency, monetary cost or user preference measure.','No LLM-generated causal diagram, identification or effect uncertainty is evaluated; symbolic tool graph is a different object.','44 unread originals and four crosscutting searches remain; full cutoff completeness is not claimed.'],limitations=source_record['limitations'])
    write(BASE/'omissions-register.json',omissions)
    evidence=[ref(BASE/n,'Reviewed primary/artifact census evidence') for n in ['source-audit.json','exact-results.json','paper-layout.txt','development.tex','plan.md','task-map.json','census-register.json','omissions-register.json']]+[ref(ROOT/'docs/papers/GIST-CMTF Goal-State Inference for Causal Minimal Tool Filtering in LLM Agents Babu(2026).pdf','Authentic inspected original'),ref(Path(__file__),'Exact record construction')]
    write(BASE/'review.json',dict(status='pass_for_bounded_census_retention_with_limits',reviewer=dict(name='Codex author/coordinator',kind='author'),evidence=evidence,findings=paper_record['supported_claims']+source_record['supported_claims']+project['supported_claims'],limitations=source_record['limitations'],coverage_acceptance=False,native_execution=False,visual_acceptance=False))
    verify_bindings(read(BASE/'review.json'));write(BASE/'operation-receipt.json',dict(operation_id='LL.CENSUS',outcome='pass',execution='performed',scope='One authentic original and one goal-state artifact; 69/113 inspected,44 unread, four searches open.',reviewer=dict(name='Codex author/coordinator',kind='author'),limitations=source_record['limitations'],criteria=[dict(index=0,verdict='pass',finding='Candidate172 authentic original is inspected and retained with bounded claims.',evidence=evidence),dict(index=1,verdict='pass',finding='Candidate172 mapped to affected tasks; other candidate dispositions preserved and bounded search limits remain explicit.',evidence=evidence)],outputs=[ref(BASE/'census-register.json','Successor census'),ref(BASE/'task-map.json','Task mapping')],capabilities=[],nonexecution_reason='',revisit_trigger='Obtain generating commit/log and evaluate actual label-free user clarification on a preregistered held-out task set.'))
    verify_bindings(read(BASE/'operation-receipt.json'))
    print(json.dumps(dict(candidate='LA01-candidate-172',inspected=69,unread=44,artifact_files=len(paths),cutoff_commit=commit['sha'],native_execution=False)))
if __name__=='__main__':main()

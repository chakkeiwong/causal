#!/usr/bin/env python3
"""Complete census mapping after preserving source and exact-data audit."""
from copy import deepcopy
import json
from pathlib import Path
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1];DAY=ROOT/'docs/program/execution/2026-10-23';BASE=DAY/'census-goal-state-v1'
read=lambda p:json.loads(p.read_text())
def main():
    state=read(ROOT/'docs/program/state.json');assert state['execution_runtime']['active']['operation']=='LL.CENSUS'
    register=read(DAY/'proof-statspai-v1/census-register.json')
    baseline=deepcopy(register);prior=BASE/'census-register-before.json';
    if prior.exists(): assert read(prior)==baseline
    else: write(prior,baseline)
    row=next(x for x in register['items'] if x['id']=='LA01-candidate-172')
    assert row['disposition']=='open_original_not_inspected'
    paper=next(x for x in read(BASE/'source-audit.json')['sources'] if x['integrated_citation_key']=='exec23_gist_paper')
    row.update(prior_disposition=row['disposition'],disposition='inspected_primary_retained_with_limits',technical_source_review_open=False,source_key='exec23_gist_paper',primary_source_record=paper,artifact_source_key='exec23_gist_sources',mapping_basis='Authentic v1 original and cutoff-pinned benchmark inspected; symbolic business-goal mediation maps to business translation and agent architecture. Does not address causal-diagram correctness.',availability='Genuine arXiv PDF authenticated by local hash; selected source files checked against pinned repository Git blobs.',effect_on_claims='Retains a scoped goal-validation design comparator; no general LLM superiority, bank workflow or causal diagram capability claim.',next_action='Keep this source in goal clarification and agent architecture comparisons. Resolve the source-to-data generating revision and label-free user response path before a registered prototype comparison.',publication_keys=['exec23_gist_paper','exec23_gist_sources','exec23_gist_reference'])
    tm=read(DAY/'proof-statspai-v1/task-map.json')
    for family in tm['task_families']:
        un=family.get('uninspected_candidate_ids',[])
        if row['id'] in un:un.remove(row['id']);family.setdefault('inspected_candidate_ids',[]).append(row['id'])
        if family['id']=='agent_architecture':family.setdefault('inspected_source_keys',[]).extend(k for k in ['exec23_gist_paper','exec23_gist_sources','exec23_gist_reference'] if k not in family.get('inspected_source_keys',[]))
        family['coverage_acceptance']=False
    family=next(x for x in tm['task_families'] if x['id']=='business_translation')
    family.setdefault('inspected_candidate_ids',[]).append(row['id'])
    family.setdefault('inspected_source_keys',[]).extend(k for k in ['exec23_gist_paper','exec23_gist_sources','exec23_gist_reference'] if k not in family.get('inspected_source_keys',[]))
    counts={k:sum(x['disposition']==k for x in register['items']) for k in set(x['disposition'] for x in register['items'])}
    assert counts['inspected_primary_retained_with_limits']==69 and counts['open_original_not_inspected']==44 and counts['open_search_specificity_and_saturation']==1
    assert all(x==y for x,y in zip(baseline['items'],register['items']) if x['id']!='LA01-candidate-172')
    register.update(counts=counts,supersedes=ref(prior,'Preserved68/45 state'),changes=['Only candidate172 changed; all other candidate and crosscutting dispositions are byte-for-byte equal to the preserved baseline. Three audited records attach.'],closure=False,interpretation='69/113 candidate originals inspected;44 unread; four crosscutting searches remain.')
    write(BASE/'census-register.json',register)
    tm['register']=ref(BASE/'census-register.json','69 inspected and44 unread originals')
    tm['supersedes']=ref(DAY/'proof-statspai-v1/task-map.json','Preserved68/45 task mapping')
    tm['current_evidence']=[ref(BASE/'source-audit.json','Three additional audited records'),ref(BASE/'exact-results.json','Final CSV source-to-output audit')]
    write(BASE/'census-register.json',register);write(BASE/'task-map.json',tm)
    omissions=dict(items=['The source-to-data producing commit, CLI overrides and full provider/cleaning logs are not bound; saved outputs aggregate, runner replay unproved.','No actual human clarification, open-world or changing-API study; no latency, monetary cost or user preference measure.','No LLM-generated causal diagram, identification or effect uncertainty is evaluated; symbolic tool graph is a different object.','44 unread originals and four crosscutting searches remain; full cutoff completeness is not claimed.'],limitations=['One authentic v1 original and selected cutoff artifacts; no downloaded code executed.','No native qualification, bank performance or general LLM causal-reasoning claim.'])
    write(BASE/'omissions-register.json',omissions)
    evidence=[ref(BASE/n,'Reviewed primary/artifact census evidence') for n in ['source-audit.json','exact-results.json','paper-layout.txt','development.tex','plan.md','task-map.json','census-register.json','omissions-register.json','census-register-before.json']]+[ref(ROOT/'docs/papers/GIST-CMTF Goal-State Inference for Causal Minimal Tool Filtering in LLM Agents Babu(2026).pdf','Authentic inspected original'),ref(Path(__file__),'Census successor construction')]
    review=dict(status='pass_for_bounded_census_retention_with_limits',reviewer=dict(name='Codex author/coordinator',kind='author'),evidence=evidence,findings=[x for src in read(BASE/'source-audit.json')['sources'] for x in src['supported_claims']],limitations=omissions['limitations'],coverage_acceptance=False,native_execution=False,visual_acceptance=False)
    verify_bindings(review);write(BASE/'review.json',review)
    receipt=dict(operation_id='LL.CENSUS',outcome='pass',execution='performed',scope='One authentic original and one goal-state artifact; 69/113 inspected,44 unread, four searches open.',reviewer=review['reviewer'],limitations=omissions['limitations'],criteria=[dict(index=0,verdict='pass',finding='Candidate172 authentic original is inspected and retained with bounded claims.',evidence=evidence),dict(index=1,verdict='pass',finding='Candidate172 mapped to affected task families; all other candidate dispositions preserved and bounded search limits remain explicit.',evidence=evidence)],outputs=[ref(BASE/'census-register.json','Successor census'),ref(BASE/'task-map.json','Task mapping')],capabilities=[],nonexecution_reason='',revisit_trigger='Obtain generating commit/log and evaluate actual label-free user clarification on a preregistered held-out task set.')
    verify_bindings(receipt);write(BASE/'operation-receipt.json',receipt)
    print(json.dumps(dict(inspected=69,unread=44,source_records=3,other_dispositions_preserved=True)))
if __name__=='__main__':main()

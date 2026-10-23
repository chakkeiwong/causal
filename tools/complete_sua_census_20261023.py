#!/usr/bin/env python3
import json,re
from copy import deepcopy
from collections import Counter
from pathlib import Path
import sua_counterexamples_20261023 as exact
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1];DAY=ROOT/'docs/program/execution/2026-10-23';BASE=DAY/'census-sensitivity-alignment-v1'
read=lambda p:json.loads(p.read_text())
def main():
 primary=read(BASE/'primary-review.json');verify_bindings(primary)
 source,project=deepcopy(read(BASE/'source-audit.json')['sources'])
 source.update(first_author='Hiremath',local_path=source['local_copy']['path'],sha256=source['local_copy']['sha256'])
 p=ROOT/source['local_path'];assert p.name==source['filename_title']+' Hiremath(2026).pdf' and p.read_bytes().startswith(b'%PDF-')
 write(BASE/'source-audit-v2.json',dict(sources=[source,project],cutoff='2026-10-07',supersedes=ref(BASE/'source-audit.json','Same supported claims; explicit PDF naming fields added'),native_execution=False))
 text=(BASE/'development.tex').read_text();assert not any(chr(i) in text for i in range(32) if i not in [10,13]);assert text.count(chr(92))>50
 assert exact.calculate()==read(BASE/'exact-results.json')
 write(BASE/'copyedit-review.json',dict(status='pass',evidence=[ref(BASE/'development.tex','Connected critical argument'),ref(BASE/'sponsor-addition.md','Sponsor discussion')],findings=['Distinguish reported claims, proof failures and authored counterexamples.','No fabrication allegation or native-performance claim.','Valid TV self-risk derivation remains narrower than causal truth and selective error.','Interpretation slack can make a bound vacuous; do not reject the triangle inequality itself.'],visual_acceptance=False))
 predecessor=DAY/'census-controlled-writes-v1/census-register.json';register=deepcopy(read(predecessor));baseline=deepcopy(register)
 row=next(x for x in register['items'] if x['id']=='LA01-candidate-261');assert row['disposition']=='open_original_not_inspected'
 row.update(prior_disposition=row['disposition'],disposition='inspected_primary_retained_with_limits',technical_source_review_open=False,source_key=source['integrated_citation_key'],primary_source_record=source,publication_keys=[source['integrated_citation_key'],project['integrated_citation_key']],task_families=['business_translation','diagram_construction','estimation_validation','agent_architecture','evaluation_cost'],mapping_basis='Diagnostic and adverse-theory relevance; no causal graph or effect certification.',availability='Genuine24-page v1 saved and text-inspected; visual review pending.',effect_on_claims='Retain diagnostic proposal; reject generic risk certification as stated. Empirical tables not reproduced.',next_action='Obtain empirical identity artifacts; derive restricted valid average/worst and conditional-risk statements; preregister semantic and matched-coverage trials.')
 assert all(x==next(y for y in register['items'] if y['id']==x['id']) for x in baseline['items'] if x['id']!=row['id'])
 counts=dict(Counter(x['disposition'] for x in register['items']));assert counts['inspected_primary_retained_with_limits']==71 and counts['open_original_not_inspected']==42
 register.update(counts=counts,supersedes=ref(predecessor,'Preserved70/43 baseline'),changes=['Only candidate261 changes; all113 candidate identities preserved.'],closure=False,interpretation='71 of113 originals inspected;42 unread; four crosscutting obligations remain.')
 write(BASE/'census-register.json',register)
 oldmap=DAY/'census-controlled-writes-v1/task-map.json';taskmap=deepcopy(read(oldmap))
 for family in taskmap['task_families']:
  if row['id'] in family.get('uninspected_candidate_ids',[]):family['uninspected_candidate_ids'].remove(row['id'])
  if family['id'] in row['task_families']:
   for field,values in [('inspected_candidate_ids',[row['id']]),('inspected_source_keys',row['publication_keys'])]:
    family.setdefault(field,[]);family[field].extend(x for x in values if x not in family[field])
  family['coverage_acceptance']=False
 taskmap.update(register=ref(BASE/'census-register.json','71/42 successor'),supersedes=ref(oldmap,'Preserved prior mapping'));write(BASE/'task-map.json',taskmap)
 evidence=[ref(BASE/n,'Reviewed original, counterexamples and connected proposal') for n in ['source-audit-v2.json','primary-review.json','mathematical-review.json','copyedit-review.json','exact-results.json','development.tex','sponsor-addition.md','census-register.json','task-map.json','omissions-register.json','plan-review.json']]+[ref(Path(__file__),'Preserving census update')]
 review=dict(status='pass_for_scoped_adverse_source_review',evidence=evidence,findings=primary['findings']+['Valid narrow zero-one self-risk TV bound is derived; no entropy subtraction or truth certificate.','All prior census rows preserved; only261 moves from unread to inspected.'],limitations=primary['limitations'],coverage_acceptance=False,native_execution=False,visual_acceptance=False)
 verify_bindings(review);write(BASE/'review.json',review)
 write(BASE/'progress.json',dict(finding='Candidate261 genuine24-page original inspected; explicit counterexamples reject generic risk guarantees. Census71/42; coverage not closed.',next_action='Integrate the critical SUA chapter and paired sponsor, renew exact-reader reviews, then continue42 unread originals and four crosscutting obligations. Candidate252 RECON and206 financing constraints remain independent next originals;165 acquisition omission remains local.',yield_reason='Release operation for preserving publication; no phase-boundary approval or global blocker.',evidence=[ref(BASE/'review.json','Scoped critical review'),ref(BASE/'census-register.json','71/42 census')]))
 print(json.dumps(dict(inspected=71,unread=42,candidates_preserved=113,coverage_closed=False)))
if __name__=='__main__':main()

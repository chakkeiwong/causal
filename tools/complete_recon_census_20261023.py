#!/usr/bin/env python3
import json,re
from copy import deepcopy
from collections import Counter
from pathlib import Path
import recon_reference_20261023 as exact
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1];DAY=ROOT/'docs/program/execution/2026-10-23';BASE=DAY/'census-recon-memory-v1'
read=lambda p:json.loads(p.read_text())
def main():
 primary=read(BASE/'primary-review.json');verify_bindings(primary)
 source,project=deepcopy(read(BASE/'source-audit.json')['sources'])
 source.update(first_author='Arya',local_path=source['local_copy']['path'],sha256=source['local_copy']['sha256'])
 p=ROOT/source['local_path'];assert p.name==source['filename_title']+' Arya(2026).pdf' and p.read_bytes().startswith(b'%PDF-')
 audit=dict(sources=[source,project],cutoff='2026-10-07',supersedes=ref(BASE/'source-audit.json','Same supported claims; explicit PDF naming fields added'),native_execution=False)
 if (BASE/'source-audit-v2.json').exists():assert read(BASE/'source-audit-v2.json')==audit
 else:write(BASE/'source-audit-v2.json',audit)
 text=(BASE/'development.tex').read_text();assert not any(chr(i) in text for i in range(32) if i not in [10,13]);assert all(chr(92)+token in text for token in ['section{','label{','citep{','frac'])
 assert exact.calculate()==read(BASE/'exact-results.json')
 write(BASE/'copyedit-review.json',dict(status='pass',evidence=[ref(BASE/'development.tex','Connected critical argument'),ref(BASE/'sponsor-addition.md','Sponsor discussion')],findings=['Distinguish source-reported results, denominator inconsistencies and authored checks.','No fabrication allegation or native-performance claim.','Provenance correctness remains narrower than bank truth and intervention identification.','Human aggregation may differ from stated majority denominators; do not allege fabrication.'],visual_acceptance=False))
 predecessor=DAY/'census-sensitivity-alignment-v1/census-register.json';register=deepcopy(read(predecessor));baseline=deepcopy(register)
 row=next(x for x in register['items'] if x['id']=='LA01-candidate-252');assert row['disposition']=='open_original_not_inspected'
 row.update(prior_disposition=row['disposition'],disposition='inspected_primary_retained_with_limits',technical_source_review_open=False,source_key=source['integrated_citation_key'],primary_source_record=source,publication_keys=[source['integrated_citation_key'],project['integrated_citation_key']],task_families=['business_translation','diagram_construction','estimation_validation','agent_architecture','evaluation_cost'],mapping_basis='Provenance/memory test design and denominator limits; no identified intervention effect.',availability='Genuine25-page v1 saved and text-inspected; visual review pending.',effect_on_claims='Retain benchmark design; human denominators, architecture attribution, case uncertainty and full costs remain unresolved.',next_action='Acquire versioned generator/data and per-item/annotator artifacts; reconcile denominators and preregister matched-evidence case-aware trials.')
 assert all(x==next(y for y in register['items'] if y['id']==x['id']) for x in baseline['items'] if x['id']!=row['id'])
 counts=dict(Counter(x['disposition'] for x in register['items']));assert counts['inspected_primary_retained_with_limits']==72 and counts['open_original_not_inspected']==41
 register.update(counts=counts,supersedes=ref(predecessor,'Preserved71/42 baseline'),changes=['Only candidate252 changes; all113 candidate identities preserved.'],closure=False,interpretation='72 of113 originals inspected;41 unread; four crosscutting obligations remain.')
 write(BASE/'census-register.json',register)
 oldmap=DAY/'census-sensitivity-alignment-v1/task-map.json';taskmap=deepcopy(read(oldmap))
 for family in taskmap['task_families']:
  if row['id'] in family.get('uninspected_candidate_ids',[]):family['uninspected_candidate_ids'].remove(row['id'])
  if family['id'] in row['task_families']:
   for field,values in [('inspected_candidate_ids',[row['id']]),('inspected_source_keys',row['publication_keys'])]:
    family.setdefault(field,[]);family[field].extend(x for x in values if x not in family[field])
  family['coverage_acceptance']=False
 taskmap.update(register=ref(BASE/'census-register.json','72/41 successor'),supersedes=ref(oldmap,'Preserved prior mapping'));write(BASE/'task-map.json',taskmap)
 evidence=[ref(BASE/n,'Reviewed original, checks and connected proposal') for n in ['source-audit-v2.json','primary-review.json','mathematical-review.json','copyedit-review.json','exact-results.json','development.tex','sponsor-addition.md','census-register.json','task-map.json','omissions-register.json','plan-review.json']]+[ref(Path(__file__),'Preserving census update')]
 review=dict(status='pass_for_scoped_adverse_source_review',evidence=evidence,findings=primary['findings']+['Score and accuracy differ; denominator feasibility, case correlation and causal-world examples reproduce.','All prior census rows preserved; only252 moves from unread to inspected.'],limitations=primary['limitations'],coverage_acceptance=False,native_execution=False,visual_acceptance=False)
 verify_bindings(review);write(BASE/'review.json',review)
 write(BASE/'progress.json',dict(finding='Candidate252 genuine25-page original inspected; denominator, evidence and dependence limits retained. Census72/41; coverage not closed.',next_action='Integrate RECON chapter and paired sponsor, renew exact-reader reviews, then continue41 unread originals and four crosscutting obligations. Candidate206 financing constraints and other eligible originals remain independent;165 acquisition omission remains local.',yield_reason='Release operation for preserving publication; no phase-boundary approval or global blocker.',evidence=[ref(BASE/'review.json','Scoped critical review'),ref(BASE/'census-register.json','72/41 census')]))
 print(json.dumps(dict(inspected=72,unread=41,candidates_preserved=113,coverage_closed=False)))
if __name__=='__main__':main()

#!/usr/bin/env python3
import copy,json
from pathlib import Path
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'docs/program/execution/2026-10-23/census-admission-conformal-v1'
read=lambda p:json.loads(p.read_text())
audit=read(BASE/'source-audit.json');new=copy.deepcopy(audit)
for s in new['sources']:
 if s['kind']=='paper':s['filename_title']=Path(s['local_path']).name.rsplit(' '+s['first_author']+'(',1)[0]
write(BASE/'source-audit-v2.json',new)
write(BASE/'schema-repair-review.json',dict(status='pass',failure='Successful1279-page compile/text bounds followed by traceability KeyError filename_title; no canonical publication occurred.',repair='Add filename_title to two genuine paper records. Preserve source bytes, claims, prior audits, census and failed reader.',scientific_claims_changed=False,evidence=[ref(BASE/'source-audit.json','Preserved source audit'),ref(BASE/'source-audit-v2.json','Schema-complete successor'),ref(ROOT/'tools/build_integrated_monograph_v12.py','verify_refs requires filename_title')]))
register=read(BASE/'census-register.json');patches={x['integrated_citation_key']:x for x in new['sources']}
for row in register['items']:
 if row.get('source_key') in patches:row['primary_source_record']=patches[row['source_key']]
register['supersedes']=ref(BASE/'census-register.json','Preserved67/46 register');register['changes']=['Two source records receive required filename metadata only; dispositions unchanged.'];write(BASE/'census-register-v2.json',register)
task=read(BASE/'task-map.json');task['register']=ref(BASE/'census-register-v2.json','Schema-complete67/46 register');task['supersedes']=ref(BASE/'task-map.json','Preserved task map');write(BASE/'task-map-v2.json',task)
review=read(BASE/'review.json');review['evidence'] += [ref(BASE/n,'Schema-only correction') for n in ['source-audit-v2.json','census-register-v2.json','task-map-v2.json','schema-repair-review.json']];review['findings']=['Two required filename_title fields added; no original/claim/disposition altered.'];write(BASE/'review-v2.json',review);verify_bindings(review)
print('Preserved failed audit and wrote schema-complete successors')

#!/usr/bin/env python3
"""Preserve the initial review and correct two inaccurate source-anchor labels."""
import json
from pathlib import Path
import review_causalpy_reuse_20261014 as work
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings

B=work.BASE
p=json.loads((B/'primary-review.json').read_text())
corrections={
 'causalpy/formula_utils.py':('67-132: nullable-string normalization and Patsy design-matrix construction',
   ['Normalizes selected nullable string columns for Patsy and uses saved design information for new matrices; this is not causal-design validation.']),
 'causalpy/skl_models.py':('24-31,87-102: coefficient mixin and estimator augmentation',
   ['Adds coefficient access through a mixin and augments an estimator class; the RD prediction uncertainty boundary is inspected separately in model_adapter.py.'])}
for r in p['sources']:
 for suffix,(anchor,claims) in corrections.items():
  if r['source_identity'].endswith('/'+suffix):
   r['local_copy']['anchor']=anchor;r['inspected_anchors']=[anchor];r['supported_claims']=claims
p['correction_of']=ref(B/'primary-review.json','Initial unregistered review retained')
p['correction_reason']='Two source-anchor descriptions named symbols not present in their files. Corrected against actual source; no RD calculation or decision changed.'
write(B/'primary-review-v2.json',p)
a=json.loads((B/'source-audit.json').read_text())
a['sources'][0]['local_copy']=ref(B/'primary-review-v2.json','Twelve pinned originals with corrected formula/mixin anchors')
a['sources'][0]['records']=p['sources']
a['sources'][0]['supported_claims']=[c for r in p['sources']for c in r['supported_claims']]
write(B/'source-audit-v2.json',a)
old=json.loads((B/'author-review.json').read_text())
e=[ref(B/'primary-review-v2.json','Corrected authoritative primary review'),ref(B/'primary-review.json','Preserved failed anchor labels'),ref(Path(__file__),'Explicit anchor repair')]
old['evidence']+=e;old['findings'].append(p['correction_reason']);verify_bindings(old)
write(B/'author-review-v2.json',old)
r=json.loads((B/'operation-receipt.json').read_text())
for c in r['criteria']:c['evidence']+=e
r['limitations'].append('The two anchor labels in the original primary review are superseded by primary-review-v2.json; original artifacts retained.')
write(B/'operation-receipt-v2.json',r)
print(json.dumps({'status':'corrected','preserved':True,'affected_source_anchors':list(corrections)}))

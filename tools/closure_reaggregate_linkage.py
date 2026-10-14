#!/usr/bin/env python3
"""Repair availability counts by replaying all retained result aggregation."""
import hashlib
import json
import zipfile
from closure_common import ROOT, save, digest
from closure_linkage_study import projection_summary

archive='docs/program/history/closure-linkage-before-availability-summary.zip'
with zipfile.ZipFile(ROOT/archive) as saved:
    result=json.loads(saved.read('docs/studies/closure-linkage-results.json'))
old_inputs=dict(result['input_sha256'])
assert all(digest(p)==h for p,h in old_inputs.items() if p!='tools/closure_linkage_study.py')
payload=lambda:hashlib.sha256(json.dumps([c['runs'] for family in ('persistent','fresh','retrospective') for c in result[family]],sort_keys=True).encode()).hexdigest()
before=payload()
for case in result['fresh']:
    case['summary']=projection_summary(case['runs'],1.2)
truth=json.loads((ROOT/'docs/studies/linkage-projection-results.json').read_text())['financial_truth']
for case in result['retrospective']:
    case['summary']=projection_summary(case['runs'],truth)
assert before==payload()
result['aggregation_repair']={'archive':archive,'retained_per_request_sha256':before,'action':'Recomputed coverage/availability summaries only; all requested draws unchanged.'}
save('docs/studies/closure-linkage-results.json',result,list(old_inputs)+[archive,'tools/closure_reaggregate_linkage.py'])
print(json.dumps({'status':'pass','retained_per_request_sha256':before,'regular_available':{c['case']:c['summary']['regular_retained']['available'] for c in result['retrospective']}}))

#!/usr/bin/env python3
"""Reconstruct retained coverage/topology summaries and bind executed evidence."""
import hashlib
import json
import math
from pathlib import Path
import sys
import zipfile

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from causalbank.linkage_sets import decode_set,binomial_interval,sum_difference_projection,pair_projection,weighted_sum
from causalbank.dynamic_funding import FundingTarget


def main():
    issues=[];inputs={}
    def bind(name):
        p=ROOT/name
        if not p.is_file():issues.append('Missing '+name);return
        inputs[name]=hashlib.sha256(p.read_bytes()).hexdigest()
    def receipt(name):
        r=json.loads((ROOT/name).read_text());bind(name)
        if r.get('status','pass')!='pass' or r.get('mode','final')!='final':issues.append('Failed/pilot '+name)
        for p,h in r.get('input_sha256',{}).items():
            bind(p)
            if inputs.get(p)!=h:issues.append('Stale '+name+' -> '+p)
        return r
    study=receipt('docs/studies/linkage-projection-results.json')
    checks=receipt('docs/reviews/linkage-scientific-checks.json')
    receipt('docs/literature/linkage-decision-ledger.json')
    if not all(checks['checks'].values()):issues.append('Scientific check failed')
    truth=study['financial_truth'];summaries=[]
    target=FundingTarget()
    for case in study['results']:
        rows=case['runs'];summary=case['summary'];sets=[];challengers=[];valid=[]
        if len(rows)!=study['spec']['repetitions']:issues.append('Incomplete registered draws')
        for r in rows:
            result=r['projection'];pieces=decode_set(result['financial_set']);sets.append(pieces)
            challengers.append(decode_set(result['candidate_box_challenger']))
            bands=result['transformed_bands'];audit=result['audit_intervals'];cb=result['candidate_bands']
            reconstructed=weighted_sum([sum_difference_projection(bands[2*s],bands[2*s+1],audit[s]) for s in (0,1)],[.5,.5],-target.direct_cost())
            candidate=weighted_sum([pair_projection(cb[2*s],cb[2*s+1],audit[s]) for s in (0,1)],[.5,.5],-target.direct_cost())
            if reconstructed!=pieces or candidate!=challengers[-1]:issues.append('Saved set reconstruction mismatch')
            if r['regular']['status']=='computed':valid.append(r['regular'])
        covered=sum(any(lo<=truth<=hi for lo,hi in x) for x in sets)
        rcovered=sum(x['financial_interval'][0]<=truth<=x['financial_interval'][1] for x in valid)
        bounded=[x for x in sets if x and all(math.isfinite(v) for p in x for v in p)]
        candidate_bounded=[x for x in challengers if x and all(math.isfinite(v) for p in x for v in p)]
        reconstructed={'projection_coverage':covered/len(rows),'bounded_fraction':len(bounded)/len(rows),
            'disconnected_fraction':sum(len(x)>1 for x in sets)/len(rows),
            'whole_line_fraction':sum(x==[(-math.inf,math.inf)] for x in sets)/len(rows),
            'regular_available':len(valid),'regular_coverage_all':rcovered/len(rows),
            'regular_coverage_given_available':rcovered/len(valid) if valid else None,
            'median_width_given_bounded':float(np.median([sum(hi-lo for lo,hi in x) for x in bounded])) if bounded else None,
            'candidate_box_coverage':sum(any(lo<=truth<=hi for lo,hi in x) for x in challengers)/len(rows),
            'candidate_box_bounded_fraction':len(candidate_bounded)/len(rows),
            'candidate_box_median_width_given_bounded':float(np.median([sum(hi-lo for lo,hi in x) for x in candidate_bounded])) if candidate_bounded else None}
        for k,v in reconstructed.items():
            if v!=summary[k]:issues.append('Summary mismatch '+case['case']['name']+'/'+k)
        reconstructed['regular_coverage_all_mc_interval']=binomial_interval(rcovered,len(rows),.05)
        reconstructed['case']=case['case'];summaries.append(reconstructed)
    # The guard repair must leave every registered scientific draw unchanged.
    before='docs/studies/linkage-before-output-guards.zip';bind(before)
    with zipfile.ZipFile(ROOT/before) as z:
        prior=json.loads(z.read('docs/studies/linkage-projection-results.json'))
    if prior['results']!=study['results']:issues.append('Guard-only repair changed scientific draws')
    for pattern in ['docs/literature/linkage-*','docs/reviews/linkage-source-excerpts/*',
                    'docs/program/linkage-inference-plan.md','docs/reviews/linkage-plan-review.md',
                    'docs/reviews/linkage-invalid-result-before.json','docs/studies/linkage-candidate-box-pilot.zip',
                    'contracts/dynamic-funding.md',
                    'docs/derivations/linkage_projection_results.tex']:
        for p in ROOT.glob(pattern):
            if p.is_file():bind(str(p.relative_to(ROOT)))
    bind('tools/verify_linkage.py')
    result={'status':'pass' if not issues else 'fail','issues':issues,'reconstructed':summaries,
            'input_sha256':inputs,'scope':'Executed input identities, every retained set and summary, source anchors and finite checks; author verification, not independent review or bank qualification'}
    (ROOT/'docs/reviews/linkage-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'inputs':len(inputs),'issues':issues,'summaries':summaries},indent=2))
    raise SystemExit(bool(issues))


if __name__=='__main__':main()

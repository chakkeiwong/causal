#!/usr/bin/env python3
"""Read-only reconstruction of the repaired fresh comparison and preserved run."""
import hashlib
import json
import math
from pathlib import Path
import sys
import zipfile

import numpy as np
from scipy.stats import norm

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from causalbank.dynamic_funding import FundingTarget
from causalbank.linkage_sets import decode_set,pair_projection,sum_difference_projection,weighted_sum
from causalbank.weak_audit_projection import audit_interval
from weak_audit_study import properties

SPEC='docs/studies/weak-audit-sharpening-spec.json'
JOURNAL='docs/studies/weak-audit-sharpening-final.jsonl'
RESULT='docs/studies/weak-audit-sharpening-results.json'


def read(name):return json.loads((ROOT/name).read_text())
def digest(name):
    with (ROOT/name).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
def require(test,message):
    if not test:raise ValueError(message)


def pieces_equal(left,right):
    return len(left)==len(right) and all(
        (a==c or math.isclose(a,c,rel_tol=1e-11,abs_tol=1e-6)) and
        (b==d or math.isclose(b,d,rel_tol=1e-11,abs_tol=1e-6))
        for (a,b),(c,d) in zip(left,right))


def main():
    spec,result=read(SPEC),read(RESULT)
    require(spec['version']==2 and result['status']=='pass' and result['requests']==3600,
            'Incomplete registered repair')
    for name,expected in result['input_sha256'].items():
        require(digest(name)==expected,'Changed final input: '+name)
    check=read('docs/reviews/weak-audit-sharpening-checks.json')
    require(check['status']=='pass' and check['zero_difference_fixture']=='unavailable_response_variance',
            'Degenerate-score guard unqualified')
    for name,expected in check['input_sha256'].items():
        require(digest(name)==expected,'Changed independent check input: '+name)
    preserved=read(spec['initial_preservation'])
    require(preserved['status']=='preserved_exploratory_not_qualified' and
            digest(preserved['archive'])==preserved['sha256'] and
            preserved['original_request_count']==3600,'Initial run not preserved')
    with zipfile.ZipFile(ROOT/preserved['archive']) as archive:
        for name,expected in preserved['input_sha256'].items():
            require(hashlib.sha256(archive.read(name)).hexdigest()==expected,
                    'Changed preserved exploratory artifact: '+name)
    base=read(spec['base'])
    target=FundingTarget(horizon=base['horizon'],branches=base['branches'])
    z=norm.ppf(1-spec['response_error']/8)
    transformation=np.kron(np.eye(2),np.array([[.5,.5],[.5,-.5]]))
    saved={r['design']['name']:r for r in result['results']}
    counts={name:dict(covered={m:0 for m in spec['methods']},finite={m:0 for m in spec['methods']},
                      whole={m:0 for m in spec['methods']},narrower=0,both_finite=0)
            for name in saved}
    seen=set()
    with (ROOT/JOURNAL).open() as stream:
        require(json.loads(next(stream))=={'input_sha256':{k:v for k,v in result['input_sha256'].items() if k!=JOURNAL}},
                'Wrong final journal header')
        for line in stream:
            row=json.loads(line);key=row['key']
            require(key not in seen,'Duplicate request: '+key);seen.add(key)
            design,index=key.split('/')
            require(design in saved and 0<=int(index)<spec['repetitions'],'Unregistered request')
            details=row['result'];a,b=(details['methods'][m] for m in spec['methods'])
            require(a['status']=='computed_set' and b['status']=='computed_set',
                    'Unreviewed request failure: '+key)
            means=np.asarray(a['candidate_financial_means'])
            require(np.allclose(transformation@means,b['transformed_means'],rtol=2e-12,atol=1e-6),
                    'Changed transformed candidate slopes: '+key)
            audit=[audit_interval(int(k),saved[design]['design']['audit'],spec['audit_error']/2)
                   for k in details['audit_successes']]
            for method,entry,coordinates,variances,projector in (
                    (spec['methods'][0],a,'candidate_financial_means','candidate_financial_variances',pair_projection),
                    (spec['methods'][1],b,'transformed_means','transformed_variances',sum_difference_projection)):
                values=np.asarray(entry[coordinates]).reshape(2,2)
                variance=np.asarray(entry[variances]).reshape(2,2)
                require(np.isfinite(variance).all() and np.all(variance>0),'Invalid response variance')
                bands=np.stack((values-z*np.sqrt(variance),values+z*np.sqrt(variance)),axis=-1)
                bound_key='candidate_bands' if method==spec['methods'][0] else 'transformed_bands'
                require(np.allclose(bands,entry[bound_key],rtol=1e-12,atol=1e-6),
                        'Changed response bands: '+key)
                require(np.allclose(audit,entry['audit_intervals'],rtol=0,atol=1e-14),
                        'Changed audit intervals: '+key)
                parts=[projector(bands[s,0],bands[s,1],audit[s]) for s in (0,1)]
                expected=weighted_sum(parts,[.5,.5],-target.direct_cost())
                require(pieces_equal(expected,decode_set(entry['financial_set'])),
                        'Changed projected set: '+key)
                flags=properties(entry,saved[design]['truth'])
                counts[design]['covered'][method]+=int(flags['covered'])
                counts[design]['finite'][method]+=int(flags['finite'])
                counts[design]['whole'][method]+=int(flags['whole'])
            fa,fb=(properties(x,saved[design]['truth']) for x in (a,b))
            if fa['finite'] and fb['finite']:
                counts[design]['both_finite']+=1
                counts[design]['narrower']+=int(fb['width']<fa['width'])
    require(len(seen)==3600,'Missing final request')
    for name,item in saved.items():
        totals=counts[name]
        for method in spec['methods']:
            summary=item['summary']['methods'][method]
            require(totals['covered'][method]==summary['covered'] and
                    totals['finite'][method]==summary['finite'] and
                    totals['whole'][method]==summary['whole_line'],
                    'Summary mismatch: '+name+'/'+method)
        paired=item['summary']['paired']
        require(totals['both_finite']==paired['both_finite'] and
                totals['narrower']==paired['transformed_narrower'],
                'Paired precision mismatch: '+name)
    receipt=dict(status='pass',date='2026-10-11',issues=[],requests=len(seen),
                 preserved_exploratory_requests=3600,
                 total_both_finite=sum(x['both_finite'] for x in counts.values()),
                 transformed_narrower_total=sum(x['narrower'] for x in counts.values()),
                 scope='Reconstructs both projected sets, audit/response bands, coverage and paired finite widths from saved fresh requests; external and bank validity remain untested.',
                 input_sha256={name:digest(name) for name in [SPEC,JOURNAL,RESULT,
                     'docs/reviews/weak-audit-sharpening-checks.json',spec['initial_preservation'],
                     preserved['archive'],'tools/weak_audit_sharpening_verify.py',
                     'src/causalbank/weak_audit_sharpening.py',
                     'src/causalbank/weak_audit_projection.py']})
    (ROOT/'docs/reviews/weak-audit-sharpening-verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(dict(status='pass',requests=len(seen),preserved_initial=3600,
                          both_finite=receipt['total_both_finite'],
                          transformed_narrower=receipt['transformed_narrower_total']),indent=2))


if __name__=='__main__':main()

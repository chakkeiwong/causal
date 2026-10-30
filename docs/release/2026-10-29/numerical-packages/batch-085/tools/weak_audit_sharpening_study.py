#!/usr/bin/env python3
"""Durable fresh comparison of candidate and average/difference audit sets."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys

import numpy as np
from threadpoolctl import threadpool_limits

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from causalbank.dynamic_funding import FundingTarget
from causalbank.funding_calibration import DECLARATIONS, simulate_rows
from causalbank.weak_audit_projection import fit_weak_audit_projection
from causalbank.weak_audit_sharpening import fit_transformed_projection
from weak_audit_study import properties, interval

SPEC = 'docs/studies/weak-audit-sharpening-spec.json'
JOURNAL = 'docs/studies/weak-audit-sharpening-final.jsonl'
RESULT = 'docs/studies/weak-audit-sharpening-results.json'
INPUTS = [SPEC, 'docs/program/weak-audit-sharpening-plan-2026-10-11.md',
          'docs/reviews/weak-audit-sharpening-checks.json',
          'docs/reviews/weak-audit-sharpening-initial-preservation.json',
          'tools/weak_audit_sharpening_study.py', 'tools/weak_audit_study.py',
          'src/causalbank/weak_audit_sharpening.py',
          'src/causalbank/weak_audit_projection.py',
          'src/causalbank/funding_calibration.py',
          'src/causalbank/streaming_pilot.py',
          'src/causalbank/linkage_sets.py',
          'src/causalbank/dynamic_funding.py',
          'docs/studies/dynamic-funding-spec.json',
          'docs/studies/dynamic-observation-spec.json']


def read(name):
    return json.loads((ROOT / name).read_text())


def digest(name):
    with (ROOT / name).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def summarize(rows, truth, spec):
    by_method = {}
    flags = {}
    for method in spec['methods']:
        current = [properties(row['methods'][method], truth) for row in rows]
        flags[method] = current
        count, n = sum(x['covered'] for x in current), len(current)
        finite = [x['width'] for x in current if x['finite']]
        statuses = {}
        for row in rows:
            key = row['methods'][method]['status']
            statuses[key] = statuses.get(key, 0) + 1
        by_method[method] = dict(
            requests=n, covered=count, coverage_all=count/n,
            mc95=interval(count,n), simultaneous_mc95=interval(count,n,.05/len(spec['designs'])),
            computed=sum(x['computed'] for x in current),
            finite=sum(x['finite'] for x in current),
            whole_line=sum(x['whole'] for x in current),
            unbounded=sum(x['unbounded'] for x in current),
            disconnected=sum(x['disconnected'] for x in current),
            empty=sum(x['empty'] for x in current),
            conditional_finite_median_width=float(np.median(finite)) if finite else None,
            statuses=statuses)
    left, right = (flags[key] for key in spec['methods'])
    paired_width = [(a['width'], b['width']) for a,b in zip(left,right) if a['finite'] and b['finite']]
    return dict(methods=by_method, paired=dict(
        coverage_gained=sum(b['covered'] and not a['covered'] for a,b in zip(left,right)),
        coverage_lost=sum(a['covered'] and not b['covered'] for a,b in zip(left,right)),
        finite_gained=sum(b['finite'] and not a['finite'] for a,b in zip(left,right)),
        finite_lost=sum(a['finite'] and not b['finite'] for a,b in zip(left,right)),
        both_finite=len(paired_width),
        transformed_narrower=sum(b<a for a,b in paired_width),
        transformed_wider=sum(b>a for a,b in paired_width),
        median_width_ratio=float(np.median([b/a for a,b in paired_width])) if paired_width else None,
        median_width_difference=float(np.median([b-a for a,b in paired_width])) if paired_width else None))


def main(verify):
    spec = read(SPEC)
    preservation = read(spec['initial_preservation'])
    if (preservation['status'] != 'preserved_exploratory_not_qualified' or
            digest(preservation['archive']) != preservation['sha256']):
        raise ValueError('Initial exploratory run was not preserved')
    checks = read('docs/reviews/weak-audit-sharpening-checks.json')
    if checks['status'] != 'pass' or any(digest(k) != v for k,v in checks['input_sha256'].items()):
        raise ValueError('Stale independent numerical checks')
    identity = {name:digest(name) for name in sorted(INPUTS)}
    base, observation = read(spec['base']), read(spec['observation'])
    target = FundingTarget(horizon=base['horizon'],branches=base['branches'])
    journal = ROOT/JOURNAL
    records = {}
    if journal.exists():
        with journal.open() as stream:
            if json.loads(next(stream)) != {'input_sha256':identity}:
                raise ValueError('Changed registered study inputs')
            for line in stream:
                row=json.loads(line)
                if row['key'] in records: raise ValueError('Duplicate request')
                records[row['key']]=row['result']
    elif not verify:
        journal.write_text(json.dumps(dict(input_sha256=identity))+'\n')
    results=[]
    for cell, design in enumerate(spec['designs']):
        law=dict(base,rho=design.get('rho',base['rho']))
        obs=dict(observation,correct_pair_probability=design['probability'])
        corr=design.get('innovation_correlation',0.)
        truth=float(target.weights()@(base['beta']*law['rho']**np.arange(target.horizon+1))-target.direct_cost())
        rows=[]
        for i in range(spec['repetitions']):
            key=f'{design["name"]}/{i}'
            if key not in records:
                if verify: raise ValueError('Missing request '+key)
                data=simulate_rows(law,obs,design['dates'],[spec['seed'],cell,i,1],corr)
                pilot=simulate_rows(law,obs,spec['pilot_multiple']*design['dates'],[spec['seed'],cell,i,2],corr)
                counts=np.random.default_rng([spec['seed'],cell,i,3]).binomial(design['audit'],design['probability']).tolist()
                methods={}
                for method,function in zip(spec['methods'],(fit_weak_audit_projection,fit_transformed_projection)):
                    try:
                        methods[method]=function(pilot,data,target,counts,[design['audit']]*2,base['penalties'],
                                                 chunk_size=spec['chunk_size'],declarations=DECLARATIONS,
                                                 response_error=spec['response_error'],audit_error=spec['audit_error'])
                    except (ValueError,np.linalg.LinAlgError) as error:
                        methods[method]=dict(status='failed_request',error=str(error))
                record=dict(methods=methods,audit_successes=counts)
                with journal.open('a') as stream:
                    stream.write(json.dumps(dict(key=key,result=record),allow_nan=False)+'\n')
                    stream.flush();os.fsync(stream.fileno())
                records[key]=record
                if len(records)%100==0: print(f'Saved {len(records)}/3600 requests',flush=True)
            rows.append(records[key])
        results.append(dict(design=design,truth=truth,summary=summarize(rows,truth,spec)))
        print(json.dumps(dict(design=design['name'],coverage={m:x['coverage_all'] for m,x in results[-1]['summary']['methods'].items()},
                              finite={m:x['finite'] for m,x in results[-1]['summary']['methods'].items()})),flush=True)
    if len(records)!=len(spec['designs'])*spec['repetitions']:
        raise ValueError('Unexpected extra requests')
    result=dict(status='pass',date='2026-10-11',requests=len(records),results=results,
                scope='Fresh fixed selected-law comparison motivated by the earlier candidate-rectangle study; no universal calibration or adoption claim.',
                input_sha256=dict(identity,**{JOURNAL:digest(JOURNAL)}))
    if verify:
        if read(RESULT)!=result: raise ValueError('Saved summaries differ from journal reconstruction')
        print('Fresh sharpening journal and identities: pass')
    else:
        (ROOT/RESULT).write_text(json.dumps(result,indent=2)+'\n')
        print('Completed 3600 fresh paired requests.')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--verify',action='store_true')
    with threadpool_limits(limits=1): main(parser.parse_args().verify)

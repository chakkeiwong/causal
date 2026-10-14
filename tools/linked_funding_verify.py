#!/usr/bin/env python3
"""Verify saved inference arithmetic and regenerate fixed requests, without draws selection."""
import hashlib
import json
from pathlib import Path
import sys
import zipfile

import numpy as np
from scipy.stats import norm
from threadpoolctl import threadpool_limits

import linked_funding_study as study

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from causalbank.linkage_sets import decode_set


def require(condition, message):
    if not condition:
        raise ValueError(message)


def compare(left, right):
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(compare(v, right[k]) for k,v in left.items())
    if isinstance(left, (list, tuple)):
        return len(left) == len(right) and all(compare(a,b) for a,b in zip(left,right))
    if isinstance(left, (float, int)) and not isinstance(left, bool):
        return bool(np.isclose(left, right, rtol=2e-11, atol=1e-6))
    return left == right


def main():
    spec, result = study.read(study.SPEC), study.read(study.RESULT)
    for p,h in result['input_sha256'].items():
        require(study.digest(p) == h, 'Changed final input: '+p)
    preservation_path = spec['initial_preservation']
    preserved = study.read(preservation_path)
    require(preserved['requests'] == 600 and
            study.digest(preserved['archive']) == preserved['sha256'], 'Missing failed partial run')
    with zipfile.ZipFile(ROOT/preserved['archive']) as z:
        require(set(z.namelist()) == set(preserved['input_sha256']), 'Wrong archive entries')
        for p,h in preserved['input_sha256'].items():
            require(hashlib.sha256(z.read(p)).hexdigest() == h, 'Changed archived input: '+p)
    registered = {d['name']:i for i,d in enumerate(spec['designs'])}
    saved, counts = {}, {name:{m:dict(covered=0, finite=0, whole=0) for m in spec['methods']}
                        for name in registered}
    truths = {r['design']['name']:r['truth'] for r in result['results']}
    with (ROOT/study.JOURNAL).open() as stream:
        require(json.loads(next(stream)) == {'input_sha256':{p:h for p,h in result['input_sha256'].items()
                                                             if p != study.JOURNAL}}, 'Wrong journal header')
        for line in stream:
            row = json.loads(line)
            key = row['key']
            require(key not in saved, 'Duplicate request')
            name, index = key.split('/')
            require(name in registered and 0 <= int(index) < spec['repetitions'], 'Unregistered request')
            detail = row['result']
            saved[key] = detail
            for method in spec['methods']:
                item = detail['methods'][method]
                if item['status'] not in ('computed_set', 'empty_projection'):
                    continue
                pieces = decode_set(item['financial_set'])
                require(all(a <= b for a,b in pieces), 'Reversed set')
                truth = truths[name]
                flags = counts[name][method]
                flags['covered'] += int(any(a <= truth <= b for a,b in pieces))
                flags['finite'] += int(bool(pieces) and all(np.isfinite([a,b]).all() for a,b in pieces))
                flags['whole'] += int(len(pieces) == 1 and pieces[0] == (-np.inf,np.inf))
                if method != 'transformed_counts' and item['status'] == 'computed_set':
                    z = norm.ppf(1-spec['alpha']/2)
                    expected = [item['estimate']-z*item['standard_error'], item['estimate']+z*item['standard_error']]
                    require(np.allclose(item['interval'], expected, rtol=0, atol=1e-7), 'Changed scalar interval')
                    require(np.isclose(item['standard_error']**2, item['calendar_variance'], rtol=1e-12), 'Changed variance')
                    require(np.allclose(pieces, [expected], rtol=0, atol=1e-7), 'Wrong set encoding')
                    require(item['evaluation_labels'] == detail['evaluation_labels'] and
                            item['pilot_labels'] == detail['pilot_labels'], 'Wrong label accounting')
    require(len(saved) == 4800, 'Missing requests')
    for cell in result['results']:
        name = cell['design']['name']
        for method,item in cell['summary']['methods'].items():
            require(counts[name][method] == dict(covered=item['covered'], finite=item['finite'], whole=item['whole_line']),
                    'Summary counts differ: '+name+'/'+method)
        reconstructed = study.summarize([saved[f'{name}/{i}'] for i in range(spec['repetitions'])], truths[name], spec)
        require(reconstructed == cell['summary'], 'Full summary differs: '+name)
    # One fixed, preread index per cell, chosen before reading outcomes.
    keys = []
    for name, cell in registered.items():
        key = f'{name}/0'
        require(compare(study.request(spec, cell, 0), saved[key]), 'Deterministic regeneration differs: '+key)
        keys.append(key)
    inputs = [study.SPEC, study.RESULT, study.JOURNAL, study.CHECKS, preservation_path,
              preserved['archive'], 'tools/linked_funding_verify.py', 'tools/linked_funding_study.py',
              'src/causalbank/linked_funding.py']
    receipt = dict(status='pass', date='2026-10-11', issues=[], requests=len(saved),
                   preserved_schema_failure_requests=600, regenerated_request_keys=keys,
                   scope='All saved intervals, counts and summaries reconstructed; eight fixed requests regenerated, not all simulator draws independently rerun. Independent dense fixtures are separate.',
                   input_sha256={p:study.digest(p) for p in inputs})
    (ROOT/'docs/reviews/linked-funding-verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(dict(status='pass', requests=len(saved), regenerated=len(keys), preserved=600),indent=2))


if __name__ == '__main__':
    with threadpool_limits(limits=1):
        main()

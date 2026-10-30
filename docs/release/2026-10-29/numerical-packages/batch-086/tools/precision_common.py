"""Durable fixed-design V10 records and explicitly scoped Monte Carlo summaries."""
import json
import os
from pathlib import Path
import numpy as np
from scipy.stats import norm
from closure_common import ROOT, default, digest, save
from reliability_common import summarize

SPEC = 'docs/studies/precision-streaming-spec.json'
SCIENCE_INPUTS = [SPEC, 'tools/precision_common.py', 'tools/closure_common.py',
    'tools/reliability_common.py', 'src/causalbank/streaming_pilot.py',
    'src/causalbank/funding_pilot_rates.py', 'src/causalbank/funding_calibration.py',
    'src/causalbank/dynamic_funding.py', 'src/causalbank/responses.py',
    'src/causalbank/linkage_sets.py', 'docs/studies/dynamic-funding-spec.json',
    'docs/studies/dynamic-observation-spec.json']


class Journal:
    def __init__(self, name, inputs):
        self.inputs = sorted(set(SCIENCE_INPUTS+inputs))
        self.path = ROOT/f'docs/studies/precision-{name}.jsonl'
        self.identity = {p:digest(p) for p in self.inputs}
        self.rows = {}
        if self.path.exists():
            with self.path.open() as stream:
                if json.loads(next(stream))['input_sha256'] != self.identity:
                    raise ValueError('Inputs changed: preserve old evidence before new evaluation')
                for line in stream:
                    row = json.loads(line)
                    if row['key'] in self.rows:
                        raise ValueError('Duplicate request')
                    self.rows[row['key']] = row['result']
        else:
            self.path.write_text(json.dumps(dict(input_sha256=self.identity))+'\n')

    def run(self, key, compute):
        if key not in self.rows:
            encoded = json.dumps(dict(key=key, result=compute()), default=default, allow_nan=False)
            with self.path.open('a') as stream:
                stream.write(encoded+'\n')
                stream.flush()
                os.fsync(stream.fileno())
            self.rows[key] = json.loads(encoded)['result']
            if len(self.rows) % 250 == 0:
                print(json.dumps(dict(journal=self.path.stem, requests=len(self.rows))), flush=True)
        return self.rows[key]

    def finish(self, result):
        save(str(self.path.relative_to(ROOT)).replace('.jsonl','-results.json'), result,
             self.inputs+[str(self.path.relative_to(ROOT))])


def wilson(count, n, alpha=.05):
    z = norm.ppf(1-alpha/2)
    p = count/n
    middle = (p+z*z/(2*n))/(1+z*z/n)
    half = z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/(1+z*z/n)
    return [float(middle-half), float(middle+half)]


def summary(rows, truth):
    out = summarize(rows, truth)
    covered = {}
    for method in rows[0]['methods']:
        records = [r['methods'][method] for r in rows]
        covered[method] = np.array([r['status']=='computed' and r['interval'][0]<=truth<=r['interval'][1] for r in records], dtype=int)
        count = int(covered[method].sum())
        out[method].update(covered=count,mc95=wilson(count,len(rows)),
                          simultaneous_mc95=wilson(count,len(rows),.05/24),
                          availability_fraction=out[method]['available']/len(rows))
        sd = out[method]['empirical_sd']
        out[method]['se_to_sd'] = out[method]['mean_se']/sd if sd else None
    paired = {}
    methods = list(covered)
    for i,left in enumerate(methods):
        for right in methods[i+1:]:
            differences = covered[right]-covered[left]
            center = float(differences.mean())
            se = float(differences.std(ddof=1)/np.sqrt(len(rows)))
            paired[right+' minus '+left] = dict(coverage_difference=center,
                descriptive_mc95=[center-1.95996398454*se,center+1.95996398454*se],
                gained=int((differences==1).sum()),lost=int((differences==-1).sum()))
    return dict(methods=out, paired=paired)

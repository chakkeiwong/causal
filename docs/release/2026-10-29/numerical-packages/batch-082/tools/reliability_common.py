"""Small durable study records; reusing a journal requires unchanged inputs."""
import json
import numpy as np
from closure_common import ROOT, save, digest, default, coverage
from causalbank.linkage_sets import decode_set


SPEC='docs/studies/reliability-spec.json'


class Journal:
    def __init__(self,name,inputs,pilot=False):
        self.inputs=sorted(set(inputs+[SPEC,'tools/reliability_common.py','tools/closure_common.py']))
        self.path=ROOT/('docs/studies/reliability-'+name+('-pilot' if pilot else '-final')+'.jsonl')
        self.identity={p:digest(p) for p in self.inputs};self.rows={}
        if self.path.exists():
            lines=self.path.read_text().splitlines();header=json.loads(lines[0])
            if header['input_sha256']!=self.identity:
                raise ValueError('Changed inputs: preserve old journal and register a fresh follow-up')
            for line in lines[1:]:
                row=json.loads(line)
                if row['key'] in self.rows:raise ValueError('duplicate journal contribution')
                self.rows[row['key']]=row['result']
        else:
            self.path.write_text(json.dumps({'input_sha256':self.identity})+'\n')

    def run(self,key,compute):
        if key not in self.rows:
            result=compute()
            encoded=json.dumps({'key':key,'result':result},default=default,allow_nan=False)
            with self.path.open('a') as stream:
                stream.write(encoded+'\n');stream.flush()
            self.rows[key]=json.loads(encoded)['result']
            if len(self.rows)%50==0:print(json.dumps({'journal':self.path.stem,'saved':len(self.rows)}),flush=True)
        return self.rows[key]

    def finish(self,result,pilot=False):
        output=str(self.path.relative_to(ROOT)).replace('-final.jsonl','-results.json').replace('.jsonl','.json')
        save(output,result,self.inputs+[str(self.path.relative_to(ROOT))])
        print(json.dumps({'saved':output,'requests':len(self.rows)}),flush=True)


def summarize(runs,truth):
    result={}
    for method in runs[0]['methods']:
        records=[r['methods'][method] for r in runs];sets=[]
        for row in records:
            if row.get('status') not in ('computed','computed_set'):sets.append([])
            elif 'effect_set' in row:sets.append(decode_set(row['effect_set']))
            else:sets.append([row['interval']])
        available=sum(r.get('status') in ('computed','computed_set') for r in records)
        count=sum(any(a<=truth<=b for a,b in s) for s in sets)
        widths=[sum(b-a for a,b in s) for s in sets if s and all(np.isfinite(x) for p in s for x in p)]
        estimates=[r['estimate'] for r in records if r.get('status')=='computed' and 'estimate' in r]
        ses=[r['standard_error'] for r in records if r.get('status')=='computed' and 'standard_error' in r]
        result[method]=dict(requested=len(runs),available=available,coverage_all=coverage(count,len(runs)),
            coverage_given_available=count/available if available else None,
            bounded=len(widths),whole_line=sum(s==[(-np.inf,np.inf)] for s in sets),
            disconnected=sum(len(s)>1 for s in sets),median_bounded_width=float(np.median(widths)) if widths else None,
            bias=float(np.mean(estimates)-truth) if estimates else None,
            empirical_sd=float(np.std(estimates,ddof=1)) if len(estimates)>1 else None,
            mean_se=float(np.mean(ses)) if ses else None)
    return result

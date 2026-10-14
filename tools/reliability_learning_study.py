#!/usr/bin/env python3
import argparse
import json
import time
import numpy as np
from threadpoolctl import threadpool_limits
from reliability_common import ROOT,Journal,SPEC,summarize
from causalbank.chunked_learning import fit_chunked
from causalbank.blocked_learning import BlockedIVRequest,fit_blocked
from study_response_extensions import learning_sample


def data(s,rng,adverse=False):
    c,y,d,z,oracle=learning_sample(dict(dates=s['n'],controls=s['controls']),rng)
    extra=1.3*c[:,0]*c[:,1]
    if adverse:extra+=1.8*c[:,0]**2
    return c,np.column_stack([y+extra,d,z+extra])


def request(s):
    return BlockedIVRequest('fixed_basis',s['gap'],s['mixing_rate_lower_bound'],
        approximation_and_rate_statement='fixed correctly specified (1,X,X0X1); positive population Gram; bounded mixing; root-n nuisance and IV slope; covariance-rate conditions')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--pilot',action='store_true');args=ap.parse_args();all_s=json.loads((ROOT/SPEC).read_text());s=all_s['learning'];seed=all_s['pilot_seed'] if args.pilot else all_s['final_seed'];reps=all_s['pilot_repetitions'] if args.pilot else s['repetitions'];start=time.perf_counter()
    journal=Journal('learning',['tools/reliability_learning_study.py','tools/study_response_extensions.py','src/causalbank/chunked_learning.py','src/causalbank/blocked_learning.py'],args.pilot);results=[];errors=[]
    with threadpool_limits(limits=1):
        for ci,adverse in enumerate((False,True)):
            name='represented_interaction' if not adverse else 'omitted_quadratic'
            def run(i):
                c,y=data(s,np.random.default_rng([seed,50,ci,i]),adverse);req=request(s)
                chunk=fit_chunked(req,c,y,chunk_rows=s['chunk_rows']);dense=fit_chunked(req,c,y,chunk_rows=s['chunk_rows'],algorithm='dense_svd')
                old=fit_blocked(req,c,y[:,0],y[:,1],y[:,2]);delta=max(abs(chunk['estimate']-dense['estimate']),abs(chunk['standard_error']-dense['standard_error']),float(np.max(abs(chunk['scores']-dense['scores']))))
                fields=('status','estimate','standard_error','interval','inference')
                return dict(methods={k:{f:v[f] for f in fields} for k,v in [('chunked',chunk),('dense',dense),('old_linear_dictionary',old)]},dense_difference=delta,input_identity_equal=chunk['identity']==dense['identity'])
            rows=[journal.run(f'{name}/{i}',lambda i=i:run(i)) for i in range(reps)];errors.extend(r['dense_difference'] for r in rows)
            results.append(dict(case=name,truth=1.2,summary=summarize(rows,1.2)));print(json.dumps({'case':name,'chunked':results[-1]['summary']['chunked']['coverage_all']}),flush=True)
    checks=dict(dense_equivalence=max(errors)<1e-9,input_identity=all(r['input_identity_equal'] for r in journal.rows.values()))
    assert all(checks.values()),checks
    journal.finish(dict(mode='pilot' if args.pilot else 'final',checks=checks,max_dense_difference=max(errors),results=results,seconds=time.perf_counter()-start,
                        qualification='One prespecified richer dictionary. Omitted quadratic is a different law; numerical equivalence alone does not validate inference.'))


if __name__=='__main__':main()

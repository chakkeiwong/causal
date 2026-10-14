#!/usr/bin/env python3
"""Generated local failure observations; library sources remain unchanged."""
import copy
import hashlib
import json
import os
from pathlib import Path
import select
import signal
import subprocess
import sys
import tempfile
import time
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-14/failure-trials'
sys.path.insert(0,str(ROOT/'src'));sys.path.insert(0,str(ROOT/'tests'))

def child(root,boundary,job):
    import causalbank.artifacts_v12 as artifacts
    import causalbank.runtime_v12 as runtime
    original=artifacts.atomic
    def signal_boundary(details):
        print(json.dumps({'boundary':boundary,**details}),flush=True)
        time.sleep(30)
        raise RuntimeError('Parent did not terminate injected child within bound')
    def intercepted(path,value):
        if boundary=='content_before_metadata':
            original(path,value)
            if path.suffix=='.json':signal_boundary({'path':path.name,'value':value})
            return
        if path.name==job+'.json':
            if boundary=='report_before_terminal'and value['state']=='completed':
                signal_boundary({'result_ref':value['result_ref'],'completed':len(value['completed_work_ids'])})
            original(path,value)
            if boundary=='after_first_checkpoint'and value['state']=='running'and len(value['completed_work_ids'])==1:
                signal_boundary({'checkpoint_sha256':value['checkpoint_sha256'],'completed':1})
            return
        original(path,value)
    if boundary=='content_before_metadata':
        artifacts.atomic=intercepted
        artifacts.ArtifactStore(Path(root)).put({'generated_balance':100,'unit':'USD'},'trial/1','generated')
    else:
        runtime.atomic=intercepted
        runtime.Runtime(Path(root)).run_report_job(job)

def observe():
    import causalbank.artifacts_v12 as artifacts
    from causalbank.runtime_v12 import Runtime,execution_identity
    from causalbank.operation_contract_v12 import context_digest
    from test_operation_service_v12 import context,request
    from publish_latent_r_review_v2_20261013 import ref,write
    observations=[]
    def q(op,params,ctx=None,refs=None,key=None):
        a=request(op,params,ctx=ctx,refs=refs);a['idempotency_key']=key
        a['budget']={'wall_seconds':25,'memory_bytes':1024**3,'max_output_bytes':200000,'model_calls':0}
        return a
    def call(name,rt,req):
        row={'case':name,'mode':'actual_runtime_generated_request','request':req}
        try:row['response']=rt.invoke(req)
        except Exception as exc:row['exception']={'type':type(exc).__name__,'message':str(exc)[:300]}
        observations.append(row);return row
    def wait(rt,job):
        polls=[];end=time.monotonic()+20
        while time.monotonic()<end:
            req=q('job.status',{'job_id':job});r=rt.invoke(req);polls.append({'request':req,'response':r})
            state=r['result']['payload']
            if state['state']in {'failed','completed','cancelled'}:return state,polls
            time.sleep(.05)
        raise TimeoutError('Recovery did not terminate within20 seconds')
    def inject(root,boundary,job='unused'):
        p=subprocess.Popen([sys.executable,'-u',str(Path(__file__).resolve()),'child',str(root),boundary,job],
            cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,
            env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'})
        try:
            ready,_,_=select.select([p.stdout],[],[],10)
            if not ready:raise TimeoutError('No injection marker within10 seconds')
            marker=p.stdout.readline().strip()
            if not marker:raise RuntimeError('Child ended before marker: '+p.stderr.read(1000))
            info=json.loads(marker);assert info['boundary']==boundary
            p.kill();out,err=p.communicate(timeout=5)
            return {'pid':p.pid,'returncode':p.returncode,'marker':info,'remaining_stdout':out,'stderr':err,
                'mode':'instrumented_actual_code; marker pauses only at declared boundary; parent kills its own child'}
        finally:
            if p.poll()is None:p.kill();p.communicate(timeout=5)
    (ROOT/'.runtime').mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='failure-review-',dir=ROOT/'.runtime')as temp:
        root=Path(temp);rt=Runtime(root/'semantic');ctx=context()
        payload={'context_sha256':context_digest(ctx),'quadratics':[[1,0,1]]}
        ar=rt.store.put(payload,'quadratic-bounds/1','quadratic_bounds')
        base=q('sensitivity.evaluate',{'family_id':'quadratic-sublevel'},ctx,[ar])
        r=call('valid_empty_set',rt,base);assert r['response']['result']['coordinate_sets'][0]['topology']=='empty'
        changed=copy.deepcopy(base);changed['scientific_context']['units']=['EUR'];changed['scientific_context']['variables'][1]['unit']='EUR'
        r=call('changed_units_context',rt,changed);assert r['response']['result']is None
        assert r['response']['error']['code']=='invalid_or_unavailable_input'
        bad=copy.deepcopy(base);bad['schema_version']='causalbank.request/99.0.0'
        r=call('unsupported_request_schema',rt,bad);assert 'exception'in r
        r=call('unsupported_discovery',rt,q('graph.discover',{'algorithm_id':'oracle','algorithm_version':'1'},ctx))
        assert r['response']['disposition']=='unsupported'and r['response']['result']is None
        small=copy.deepcopy(base);small['budget']['max_output_bytes']=1
        r=call('bounded_output',rt,small);assert r['response']['error']['code']=='output_budget'
        cached=q('capabilities.describe',{},key='failure-review-cache')
        first=call('fresh_cache',rt,cached);again=call('unchanged_replay',rt,cached)
        assert first['response']==again['response']
        path=rt.cache/(hashlib.sha256(cached['idempotency_key'].encode()).hexdigest()+'.json')
        path.write_text('{')
        r=call('truncated_cache',rt,cached);assert r['exception']['type']=='JSONDecodeError'
        r['finding']='Corrupt replay JSON raises from Runtime.invoke; no canonical failure envelope returned.'

        partial=Runtime(root/'partial-artifact');fault=inject(partial.root,'content_before_metadata')
        content=partial.store.folder/fault['marker']['path'];aid=content.stem
        assert content.exists()and not content.with_suffix('.meta').exists()
        before={'content_exists':True,'metadata_exists':False,'listed_refs':partial.store.list_refs()}
        try:partial.store.reference(aid)
        except OSError as exc:before['lookup_error']=type(exc).__name__
        else:raise AssertionError('Partial publication unexpectedly readable')
        repaired=partial.store.put({'generated_balance':100,'unit':'USD'},'trial/1','generated')
        assert repaired['artifact_id']==aid and partial.store.get(repaired)==fault['marker']['value']
        observations.append({'case':'content_before_metadata','mode':'instrumented_actual_publication','fault':fault,
            'before_recovery':before,'retry_reference':repaired,'retry_value':partial.store.get(repaired),
            'finding':'Content-only orphan is unlisted and unreadable through reference; same-value retry finishes matching metadata.'})

        for name,boundary,corrupt in [('killed_after_checkpoint','after_first_checkpoint',False),
                ('report_before_terminal','report_before_terminal',False),('changed_checkpoint','after_first_checkpoint',True)]:
            rr=Runtime(root/name);cap=rr.invoke(q('capabilities.describe',{}))
            refs=[rr.store.put({**cap,'request_id':'generated-'+str(i)},'causalbank.response/1.0.0','canonical_response')for i in range(3)]
            req=q('report.build',{'artifact_ids':[x['artifact_id']for x in refs]},refs=refs,key=name)
            # Only submission scheduling is deferred; the instrumented child runs the unchanged report worker.
            with patch.object(Runtime,'resume',return_value='deferred_for_fault_trial'):submitted=rr.invoke(req)
            job=submitted['result']['payload']['job_id'];fault=inject(rr.root,boundary,job)
            p=rr._job_path(job);pre=json.loads(artifacts.bounded_read(p))
            assert pre['state']=='running'and pre['result_ref']is None
            completed=list(pre['completed_work_ids'])
            orphan=None
            if boundary=='report_before_terminal':
                assert len(completed)==3
                orphan=rr.store.get(fault['marker']['result_ref'])
                assert len(orphan['summaries'])==3
            if corrupt:
                pre['summaries'][0]['declared_status']='generated_corruption'
                artifacts.atomic(p,pre)
            terminal,polls=wait(rr,job)
            row={'case':name,'mode':'instrumented_actual_worker_then_unmodified_runtime_recovery',
                'request':req,'submit_response':submitted,'fault':fault,'checkpoint_before_recovery':pre,
                'polls':polls,'terminal':terminal,'published_before_terminal':orphan}
            if corrupt:
                assert terminal['state']=='failed'and terminal['result_ref']is None and 'Checkpoint'in terminal['error']
            else:
                assert terminal['state']=='completed'
                assert terminal['completed_work_ids']==req['parameters']['artifact_ids']
                report=rr.store.get(terminal['result_ref']);row['report']=report
                assert [x['source']['artifact_id']for x in report['summaries']]==req['parameters']['artifact_ids']
                assert all(x['verification']=='schema_only_not_causal_or_external_review'for x in report['summaries'])
                if orphan is not None:assert terminal['result_ref']==fault['marker']['result_ref']and report==orphan
            observations.append(row)
    result={'status':'observed','count':len(observations),'cases':observations,'execution_identity':execution_identity(),
        'source_files':[ref(ROOT/'src/causalbank'/n,'Preserved implementation used by actual probes')for n in
            ['artifacts_v12.py','operation_contract_v12.py','operation_service_v12.py','runtime_v12.py','worker_v12.py']],
        'probe':ref(Path(__file__).resolve(),'Exact generated inputs and declared fault hooks'),
        'limits':['One host and generated artifacts; no failure-rate estimate or bank acceptance.',
            'Deterministic publication hooks are test instrumentation, not naturally observed outages.',
            'Invalid request schema and corrupt replay can raise library exceptions; CLI/MCP behavior was not rerun.',
            'Inherited FIFO and coherent-descriptor limitations remain unrepaired.']}
    write(BASE/'local-observations.json',result)
    print(json.dumps({'cases':len(observations),'exception_cases':[r['case']for r in observations if 'exception'in r],
        'recovery_states':{r['case']:r['terminal']['state']for r in observations if 'terminal'in r}}))

if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='child':child(*sys.argv[2:])
    else:observe()

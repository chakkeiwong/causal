"""Actual fitted public-study summaries through existing library, CLI and MCP."""
import asyncio
import copy
from datetime import timedelta
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/scientific-gap-closure/2026-10-29'
sys.path.insert(0,str(ROOT/'src'))
from causalbank.runtime_v12 import Runtime
from causalbank.operation_contract_v12 import context_digest
from run_banking_walkthrough_20261029 import context, request
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters


async def main():
    result=json.loads((OUT/'study-results.json').read_text())
    ctx=context()
    ctx['population']={'definition':'Retained 445 male NSW RE74 experimental records','unit':'participant'}
    ctx['variables']=[{'id':'offer','role':'action','unit':'binary assignment'},
                      {'id':'value','role':'outcome','unit':'archived earnings dollars'}]
    ctx['units']=['archived earnings dollars']
    ctx['horizon']={'value':1978,'unit':'outcome calendar year'}
    ctx['sign_convention']='assignment-minus-control, 1978 earnings'
    ctx['sampling']={'law':'complete_randomization_conditional_subset','unit':'participant','fold_unit':'participant'}
    ctx['assumptions']=[{'id':'design','statement':result['target']+'; original assignment records unavailable',
                         'status':'unverified','evidence':[]},
                        {'id':'normal','statement':'Fixed-covariate normal approximation; no exact finite-sample coverage',
                         'status':'declared','evidence':[]}]
    ctx['graph']=None
    rows=[]
    with tempfile.TemporaryDirectory(prefix='public-study-',dir=ROOT/'.runtime') as tmp:
        runtime=Runtime(Path(tmp))
        env={'PATH':os.environ.get('PATH',''),'PYTHONPATH':str(ROOT/'src'),
             'CAUSALBANK_STATE_ROOT':tmp,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1',
             'MKL_NUM_THREADS':'1','PYTHONUNBUFFERED':'1','PYTHONDONTWRITEBYTECODE':'1'}
        for m in result['methods']:
            moment={'context_sha256':context_digest(ctx),'mean':[m['estimate'],1.],
                    'lrv':[[result['n']*m['variance'],0.],[0.,0.]],
                    'n':result['n'],'alpha':.05,'simultaneous':False}
            ref=runtime.store.put(moment,'moment-summary/1','moment_summary')
            req=request('estimate.effect',{'engine_id':'reference-moment-sets',
                        'estimator_id':'gaussian-residual-inversion'},ctx,[ref])
            req['request_id']='nsw-'+m['method']
            lib=runtime.invoke(req)
            ci=lib['result']['coordinate_sets'][0]['intervals'][0]
            assert np.allclose(ci,m['interval'],rtol=1e-10,atol=1e-7)
            proc=subprocess.run([sys.executable,'-B','-m','causalbank.cli_v12','operation','estimate.effect'],
                  input=json.dumps(req),capture_output=True,text=True,cwd=ROOT,env=env,timeout=25)
            assert proc.returncode==0,(proc.stdout,proc.stderr)
            cli=json.loads(proc.stdout)
            assert cli==lib
            rows.append(dict(method=m['method'],request=req,artifact=moment,library=lib,cli=cli))
        # Preserve honest refusal when the declared causal premise is contradicted.
        bad=copy.deepcopy(rows[0]['request']);bad['request_id']='contradicted-assignment'
        bad['scientific_context']['assumptions'][0]['status']='contradicted'
        refused=runtime.invoke(bad)
        assert refused['disposition']=='refused'
        (OUT/'interfaces-library-cli.json').write_text(json.dumps(rows,indent=2)+chr(10))
        print('Three fitted estimators agree through library and CLI; checking MCP.',flush=True)
        params=StdioServerParameters(command=sys.executable,args=['-B','-m','causalbank.mcp_server_v12'],env=env,cwd=str(ROOT))
        with (OUT/'interfaces-mcp.log').open('w') as log:
            async with stdio_client(params,errlog=log) as (reader,writer):
                async with ClientSession(reader,writer,read_timeout_seconds=timedelta(seconds=30)) as session:
                    init=await session.initialize()
                    for row in rows:
                        reply=await session.call_tool('causal_estimate_effect',row['request'])
                        assert not reply.isError and reply.structuredContent==row['library']
                        row['mcp']=reply.structuredContent
                    reply=await session.call_tool('causal_estimate_effect',bad)
                    assert reply.structuredContent==refused
        out=dict(three_surface_equality=True,estimators=rows,contradicted_premise=refused,
                 protocol=init.protocolVersion,versions={p:importlib.metadata.version(p) for p in ['mcp','numpy','scipy']},
                 scope='Public rows fitted by the project runner; Gaussian summary inference on existing interfaces. No report.build implementation, raw-data estimator endpoint or external consumer qualification.')
        (OUT/'interface-results.json').write_text(json.dumps(out,indent=2)+chr(10))
        print(json.dumps(dict(estimators=len(rows),surfaces=3,parity=True,contradicted_premise='refused')))


if __name__=='__main__':
    asyncio.run(main())

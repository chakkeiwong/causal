"""Run the same illustrative study checks through library, CLI and local MCP."""
import asyncio
import copy
from datetime import timedelta
from hashlib import sha256
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/scientific-synthesis/2026-10-29'
sys.path.insert(0, str(ROOT/'src'))
from causalbank.runtime_v12 import Runtime
from causalbank.operation_contract_v12 import context_digest
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters


def context():
    return {
      'target': {'kind':'average_effect','outcome':'value','treatment':'offer','contrast':'1-versus-0'},
      'population':{'definition':'Illustrative eligible accounts at decision','unit':'account'},
      'variables':[{'id':'offer','role':'action','unit':'binary'},
                   {'id':'value','role':'outcome','unit':'USD'}],
      'intervention':{'kind':'set','value':'offer=1'},
      'horizon':{'value':12,'unit':'months'},'units':['USD'],
      'sign_convention':'offer-minus-no-offer',
      'observation_clock':{'event_time':'event_at','available_time':'available_at',
                           'decision_time':'decision_at','rule':'strict_before_decision',
                           'alternative_justification':None},
      'sampling':{'law':'independent_units','unit':'account','fold_unit':'account'},
      'assumptions':[{'id':'graph_truth','statement':'Supplied graph is valid',
                      'status':'unverified','evidence':[]}],
      'graph':{'kind':'DAG','edges':[{'left_node':'offer','right_node':'value',
               'left_mark':'tail','right_mark':'arrow','evidence_type':'assumption',
               'evidence_refs':[],'review_status':'unverified'}]},'source_evidence':[]}


def request(name,params,ctx,refs=None):
    return {'schema_version':'causalbank.request/1.0.0','request_id':name,
            'operation':name,'artifact_inputs':refs or [],
            'budget':{'wall_seconds':10,'memory_bytes':1024**3,
                      'max_output_bytes':100000,'model_calls':0},
            'parameters':params,'scientific_context':ctx,'idempotency_key':None}


async def main():
    with tempfile.TemporaryDirectory(prefix='scientific-walkthrough-',dir=ROOT/'.runtime') as tmp:
        runtime=Runtime(Path(tmp))
        ctx=context()
        observation={'context_sha256':context_digest(ctx),'rows':[
            {'event_at':'2026-01-01T00:00:00+00:00','available_at':'2026-01-02T00:00:00+00:00','decision_at':'2026-01-03T00:00:00+00:00'},
            {'event_at':'2026-01-01T00:00:00+00:00','available_at':'2026-01-04T00:00:00+00:00','decision_at':'2026-01-03T00:00:00+00:00'},
            {'event_at':'2026-01-01T00:00:00+00:00','decision_at':'2026-01-03T00:00:00+00:00'}]}
        ref=runtime.store.put(observation,'observation-rows/1','observation_rows')
        requests=[request('graph.review',{'review_kind':'syntax'},ctx),
                  request('identify.effect',{'method_id':'backdoor'},ctx),
                  request('audit.observation',{'checks':['clock']},ctx,[ref])]
        dependent=copy.deepcopy(requests[1]); dependent['request_id']='dependent-identification'
        dependent['scientific_context']['sampling']['law']='dependent_months'
        requests.append(dependent)
        env={'PATH':os.environ.get('PATH',''),'PYTHONPATH':str(ROOT/'src'),'CAUSALBANK_STATE_ROOT':tmp,
             'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1',
             'PYTHONUNBUFFERED':'1','PYTHONDONTWRITEBYTECODE':'1'}
        rows=[]
        for req in requests:
            library=runtime.invoke(req)
            command=[sys.executable,'-B','-m','causalbank.cli_v12','operation',req['operation']]
            proc=subprocess.run(command,input=json.dumps(req),capture_output=True,text=True,
                                cwd=ROOT,env=env,timeout=20)
            if proc.returncode not in (0,4):
                raise RuntimeError(proc.stderr or proc.stdout)
            cli=json.loads(proc.stdout)
            assert library==cli,(req['request_id'],'CLI mismatch')
            rows.append({'request':req,'library':library,'cli':cli,'cli_exit_code':proc.returncode})
        (OUT/'walkthrough-library-cli.json').write_text(json.dumps(rows,indent=2)+'\n')
        print('Four library and CLI cases agree; initializing local MCP.',flush=True)
        params=StdioServerParameters(command=sys.executable,
                args=['-B','-m','causalbank.mcp_server_v12'],env=env,cwd=str(ROOT))
        with (OUT/'walkthrough-mcp.log').open('w') as errors:
            async with stdio_client(params,errlog=errors) as (read,write):
                async with ClientSession(read,write,read_timeout_seconds=timedelta(seconds=20)) as session:
                    init=await session.initialize()
                    names={t.name for t in (await session.list_tools()).tools}
                    for row in rows:
                        name='causal_'+row['request']['operation'].replace('.','_')
                        assert name in names
                        result=await session.call_tool(name,row['request'])
                        value=result.structuredContent
                        assert value==row['library'],(name,'MCP mismatch')
                        row['mcp']=value
                        row['mcp_is_error']=bool(result.isError)
        assert rows[0]['library']['qualification']['level']=='execution_only'
        assert rows[1]['library']['qualification']['level']=='conditional_inference'
        assert rows[2]['library']['result']['payload']['clock_failures']==[1,2]
        assert rows[3]['library']['disposition']=='unsupported'
        source_files=['src/causalbank/runtime_v12.py','src/causalbank/operation_service_v12.py',
                      'src/causalbank/cli_v12.py','src/causalbank/mcp_server_v12.py',
                      'src/causalbank/operation_contract_v12.py','src/causalbank/artifacts_v12.py']
        output={'date':'2026-10-29','scope':'Local constructed example; no external package adapter, live LLM, bank data or sibling-repository execution',
                'protocol_version':init.protocolVersion,
                'versions':{p:importlib.metadata.version(p) for p in ['mcp','numpy','scipy','jsonschema']},
                'source_hashes':{p:sha256((ROOT/p).read_bytes()).hexdigest() for p in source_files},
                'runner_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
                'observations':observation,'results':rows,'three_surface_equality':True}
        (OUT/'walkthrough-results.json').write_text(json.dumps(output,indent=2)+'\n')
        (OUT/'walkthrough-requests.json').write_text(json.dumps(requests,indent=2)+'\n')
        print(json.dumps({'cases':len(rows),'surfaces':3,'same_responses':True,
                          'clock_failures':[1,2],'dependent_design':'unsupported',
                          'protocol':init.protocolVersion}))


if __name__=='__main__':
    (ROOT/'.runtime').mkdir(exist_ok=True)
    asyncio.run(main())

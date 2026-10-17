#!/usr/bin/env python3
"""Bounded local proposal examples, not deployed clients or fresh MCP trials."""
import argparse
from copy import deepcopy
import json,os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'));sys.path.insert(0,str(ROOT/'tools'))
import jsonschema
from causalbank.runtime_v12 import Runtime,execution_identity
from causalbank.operation_service_v12 import RESPONSE_SCHEMA,validate_request
from integration_review_reference_20261017 import parse,meaning

def decode(request,text):
    validate_request(request)
    response=parse(text);jsonschema.validate(response,RESPONSE_SCHEMA)
    return dict(interpretation=meaning(request,response),response=response)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    output=args.output.resolve();output.relative_to(ROOT)
    assert not output.exists(),'Use a fresh output directory; preserve earlier results'
    output.mkdir(parents=True);store=ROOT/'.runtime'/('standalone-'+output.name)
    assert not store.exists(),'Use a unique output directory name'
    runtime=Runtime(store)
    env=dict(os.environ,PYTHONPATH=str(ROOT/'src'),CAUSALBANK_STATE_ROOT=str(store),OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
    source=ROOT/'docs/program/execution/2026-10-13/interfaces/examples'
    expected={'backdoor':'conditional_expression','unsupported-sampling':'scientific_unsupported','contradicted-premise':'scientific_refused'};rows=[]
    for name,label in expected.items():
        request=json.loads((source/'requests'/f'{name}.json').read_text())
        library=decode(request,json.dumps(runtime.invoke(request)))
        result=subprocess.run([sys.executable,'-m','causalbank.cli_v12','operation',request['operation'],'--input','-'],input=json.dumps(request),text=True,capture_output=True,env=env,cwd=ROOT,timeout=30)
        cli=decode(request,result.stdout)
        row=dict(case=name,request=request,library=library,cli=cli,exit_code=result.returncode,stderr=result.stderr,expected=label)
        (output/(name+'.json')).write_text(json.dumps(row,indent=2)+'\n')
        assert library==cli and cli['interpretation']==label and result.returncode==0
        assert cli['response']['result'] is None or cli['response']['result']['estimate'] is None
        rows.append(dict(case=name,interpretation=label,equal=True,exit_code=result.returncode))
    stored=[]
    for name in ['finite','empty','whole','disconnected']:
        historical=json.loads((source/'results'/f'{name}.json').read_text())
        request=json.loads((ROOT/historical['request']['path']).read_text())
        admitted=decode(request,json.dumps(historical['library']))
        stored.append(dict(case=name,interpretation=admitted['interpretation'],mode='preserved response replay'))
    request=json.loads((source/'requests/backdoor.json').read_text());good=json.loads((output/'backdoor.json').read_text())['library']['response']
    invalid=deepcopy(good);del invalid['schema_version'];wrong=deepcopy(good);wrong['request_id']='different'
    cases={'duplicate':'{"status":"completed","status":"failed"}','missing_schema':json.dumps(invalid),'wrong_request':json.dumps(wrong),'nonfinite':'{"estimate":NaN}','trailing':json.dumps(good)+' trailing'};rejected=[]
    for name,text in cases.items():
        try:decode(request,text)
        except (ValueError,jsonschema.ValidationError):rejected.append(name)
        else:raise AssertionError(name)
    report=dict(status='pass',actual_local_invocations=6,actual_request_types=3,preserved_response_replays=stored,rejected_adverse_cases=rejected,results=rows,execution_identity=execution_identity(),schema_scope='Existing canonical schemas plus semantic relation',limits=['No MCP execution, notebook-kernel qualification, provider calls, plotting/export UI, deployment or bank acceptance.','Finite byte cap is not adversarial parser resource qualification.','No new causal estimate, empirical accuracy, speedup or economic claim.'])
    (output/'results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='pass',actual_local_invocations=6,stored_replays=4,adverse_rejections=len(rejected))))

if __name__=='__main__':main()

#!/usr/bin/env python3
"""Follow the observed replay exception through the actual local CLI."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tests'))
from test_operation_service_v12 import request
from publish_latent_r_review_v2_20261013 import ref,write
BASE=ROOT/'docs/program/execution/2026-10-14/failure-trials'

def main():
    rows=[]
    with tempfile.TemporaryDirectory(prefix='failure-cli-',dir=ROOT/'.runtime')as tmp:
        root=Path(tmp)
        env={**os.environ,'PYTHONPATH':str(ROOT/'src'),'CAUSALBANK_STATE_ROOT':str(root),
            'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'}
        q=request('capabilities.describe',{});q['budget']['memory_bytes']=1024**3;q['idempotency_key']='cli-truncation'
        def invoke(name,value):
            p=subprocess.run([sys.executable,'-m','causalbank.cli_v12','operation','capabilities.describe'],
                input=json.dumps(value),capture_output=True,text=True,cwd=ROOT,env=env,timeout=10)
            row={'case':name,'mode':'actual_CLI_subprocess','request':value,'exit_code':p.returncode,
                'response':json.loads(p.stdout),'stderr':p.stderr};rows.append(row);return row
        a=invoke('valid_cached_request',q);assert a['exit_code']==0 and a['response']['status']=='completed'
        cache=root/'replay'/(hashlib.sha256(q['idempotency_key'].encode()).hexdigest()+'.json')
        original_sha256=hashlib.sha256(cache.read_bytes()).hexdigest()
        cache.write_text('{')
        b=invoke('valid_request_with_corrupt_local_cache',q)
        b['injection']={'file':'replay/<hash-of-key>.json','prior_sha256':original_sha256,'new_bytes':'{'}
        assert b['exit_code']==2 and b['response']['error']['code']=='invalid_request'
        bad=copy.deepcopy(q);bad['schema_version']='causalbank.request/99.0.0'
        c=invoke('invalid_schema_request',bad)
        assert c['exit_code']==2 and c['response']['error']['code']=='invalid_request'
    write(BASE/'cli-observations.json',{'count':len(rows),'cases':rows,
        'finding':'A valid request encountering corrupted local replay JSON is mapped to the same invalid_request code/exit2 as an invalid request schema.',
        'limits':['Generated one-host CLI calls; no live MCP exchange or production failure rate.',
            'Fault is manual local truncation, not evidence that the atomic writer naturally emits truncated files.'],
        'evidence':[ref(ROOT/'src/causalbank/cli_v12.py','main exception mapping'),ref(ROOT/'src/causalbank/runtime_v12.py','Replay JSON load'),
            ref(Path(__file__).resolve(),'Three bounded exact CLI calls')]})
    print(json.dumps({'CLI_cases':len(rows),'codes':[r['response'].get('error',{}).get('code','completed')for r in rows]}))

if __name__=='__main__':main()

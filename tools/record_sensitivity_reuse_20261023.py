#!/usr/bin/env python3
"""Serialize independent reviewed reuse outcomes with preserved transition logs."""
from pathlib import Path
import json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-23/sensitivity-reuse-v1'
for key,op in [('sensemakr','SW.DECISION.seed_057'),('evalue','SW.DECISION.seed_058')]:
    for label,args in [('start',['tools/run_program_checkpoint_v3.py','start',op,'--reason','Execute reviewed source-bounded sensitivity reference decision']),('prepare',['tools/review_sensitivity_reuse_20261023.py',key]),('record',['tools/run_program_checkpoint_v3.py','record',op,'--receipt',str((BASE/key/'operation-receipt.json').relative_to(ROOT))])]:
        log=BASE/(key+'-'+label+'.txt')
        with log.open('x') as stream:
            result=subprocess.run([sys.executable]+args,cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT,timeout=600)
        assert result.returncode==0,log
        print(json.dumps(dict(operation=op,step=label,status='pass')),flush=True)

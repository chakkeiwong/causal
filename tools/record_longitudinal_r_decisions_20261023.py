#!/usr/bin/env python3
"""Serialize completed reference choices; consume every controller exit."""
import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'docs/program/execution/2026-10-23/longitudinal-r-decisions-v1'
state=json.loads((ROOT/'docs/program/state.json').read_text());assert state['execution_runtime']['active'] is None
for key in ['060','062']:
 op='SW.DECISION.seed_'+key
 steps=[('start',[sys.executable,'tools/run_program_checkpoint_v3.py','start',op,'--reason','Record reviewed pinned reference choice; no native integration; continue independent obligations']),('receipt',[sys.executable,'tools/decide_longitudinal_r_20261023.py','receipt',key]),('record',[sys.executable,'tools/run_program_checkpoint_v3.py','record',op,'--receipt',str((BASE/(key+'-receipt.json')).relative_to(ROOT))])]
 for phase,args in steps:
  with (BASE/(key+'-'+phase+'.log')).open('x') as log:r=subprocess.run(args,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,timeout=600)
  assert r.returncode==0,(op,phase)
  print(json.dumps(dict(operation=op,phase=phase,status='pass')),flush=True)

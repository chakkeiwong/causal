#!/usr/bin/env python3
"""Execute five independent reviewed dispositions; serialize every state mutation."""
import json
from pathlib import Path
import subprocess
import sys
from review_r_iv_rd_20261022 import BASE, ROOT, core, read


def main():
    state=core.read(ROOT,core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['execution_program']['results']['SW.CELL.iv_rd_design.R']['outcome']=='inconclusive'
    for number in range(50,55):
        group=f'{number:03d}';identifier='SW.DECISION.seed_'+group
        for name,args in [
            ('start',['tools/run_program_reviews_v2.py','start',identifier,'--reason','Execute reviewed R IV/RD reference-only reuse decision']),
            ('prepare',['tools/review_r_iv_rd_20261022.py','receipt',identifier]),
            ('record',['tools/run_program_reviews_v2.py','record',identifier,'--receipt',str((BASE/'decisions'/group/'operation-receipt.json').relative_to(ROOT))])]:
            log=BASE/'transition-logs'/(group+'-'+name+'.log');log.parent.mkdir(exist_ok=True)
            with log.open('x') as stream:
                result=subprocess.run([sys.executable]+args,cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT,timeout=600)
            assert result.returncode==0,log
            print(json.dumps(dict(operation=identifier,step=name,status='pass')),flush=True)


if __name__=='__main__':main()

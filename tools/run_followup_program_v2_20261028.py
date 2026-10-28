"""Select the current immutable followup batch without rewriting earlier queues."""
import argparse,json
from pathlib import Path
import run_followup_program_20261028 as engine
ROOT=engine.ROOT
POINTER=ROOT/'docs/program/execution/followup-current.json'


def selected():
    binding=json.loads(POINTER.read_text());engine.bound(ROOT,binding['contracts'])
    base=(ROOT/binding['contracts']['path']).parent
    if not base.is_relative_to(ROOT/'docs/program/execution'):raise ValueError('Invalid queue directory')
    return base


def main():
    p=argparse.ArgumentParser();p.add_argument('command',choices=['status','next','check','start','checkpoint','record','block']);p.add_argument('task',nargs='?');p.add_argument('--receipt');a=p.parse_args();base=selected()
    if a.command in ['start','checkpoint','record','block']:
        if not a.task or not a.receipt:p.error('task and --receipt required')
        print(json.dumps(engine.append(a.command,a.task,a.receipt,ROOT,base)))
    else:
        data=engine.load(ROOT,base);result=engine.view(data)
        result['controller']='python3 tools/run_followup_program_v2_20261028.py';result['contracts']=str((base/'contracts.json').relative_to(ROOT))
        print(json.dumps(dict(status='pass',events=len(data['events']),awards_acceptance=False) if a.command=='check' else result,indent=2))


if __name__=='__main__':main()

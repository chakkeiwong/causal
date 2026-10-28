"""Durable work-packet queue; never awards or rewrites proposal acceptance."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-28/followup-runtime-v1'


def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def bound(root,ref):
    p=(root/ref['path']).resolve()
    if not p.is_relative_to(root.resolve()) or not p.is_file():raise ValueError('Invalid local evidence path')
    if hashlib.sha256(p.read_bytes()).hexdigest()!=ref['sha256']:raise ValueError('Changed evidence: '+ref['path'])


def load(root=ROOT,base=BASE):
    contract=json.loads((base/'contracts.json').read_text());nodes={n['id']:n for n in contract['tasks']}
    if len(nodes)!=len(contract['tasks']):raise ValueError('Duplicate task')
    for r in contract['evidence']:bound(root,r)
    if contract['awards_acceptance'] is not False:raise ValueError('Queue cannot award acceptance')
    for n in nodes.values():
        if not n['action'] or not n['outputs'] or not n['acceptance'] or not n['scope']:raise ValueError('Incomplete task contract')
        if not set(n['depends'])<=nodes.keys():raise ValueError('Unknown task dependency')
        if n['id'] in n['depends']:raise ValueError('Self dependency')
    def visit(key,stack,done):
        if key in stack:raise ValueError('Dependency cycle')
        if key in done:return
        for parent in nodes[key]['depends']:visit(parent,stack|{key},done)
        done.add(key)
    done=set()
    for key in nodes:visit(key,set(),done)
    states={k:'ready' for k in nodes};active=None;previous=digest(contract);events=[];next_actions={}
    log=base/'events.jsonl'
    for line in log.read_text().splitlines() if log.exists() else []:
        event=json.loads(line);payload={k:v for k,v in event.items() if k!='sha256'}
        if event['sha256']!=digest(payload) or event['previous']!=previous or event['sequence']!=len(events):raise ValueError('Broken event chain')
        key=event['task'];node=nodes[key];verb=event['action']
        bound(root,event['evidence']);note=json.loads((root/event['evidence']['path']).read_text())
        for b in note.get('evidence',[]):bound(root,b)
        if note.get('task')!=key or note.get('awards_acceptance') is not False:raise ValueError('Receipt identity/acceptance mismatch')
        if verb=='start':
            if active or states[key]!='ready' or not all(states[d]=='completed' for d in node['depends']):raise ValueError('Task cannot start')
            if not note.get('next_action'):raise ValueError('Missing resume action')
            states[key]='active';active=key
        elif verb in ['checkpoint','record','block']:
            if active!=key:raise ValueError('Task is not active')
            if verb=='record':
                if note.get('execution')!='performed' or note.get('outcome') not in ['pass','inconclusive','negative']:raise ValueError('Invalid performed result')
                if [x.get('index') for x in note.get('criteria',[])]!=list(range(len(node['acceptance']))):raise ValueError('Incomplete criterion review')
                if any(x.get('verdict') not in ['pass','inconclusive','negative'] or not x.get('finding') for x in note['criteria']):raise ValueError('Invalid criterion finding')
                if note['outcome']=='pass' and any(x['verdict']!='pass' for x in note['criteria']):raise ValueError('Passing result has unresolved criteria')
                if {r['path'] for r in note.get('outputs',[])}!=set(node['outputs']):raise ValueError('Output contract mismatch')
                for b in note['outputs']:bound(root,b)
                if note['outcome']!='pass' and not note.get('next_action'):raise ValueError('Unresolved result needs next action')
                states[key]='completed';active=None
            elif verb=='block':
                if not note.get('reason') or not note.get('revisit_trigger') or not note.get('next_action'):raise ValueError('Incomplete local blocker')
                states[key]='blocked';active=None
            elif not note.get('next_action'):raise ValueError('Checkpoint needs next action')
        else:raise ValueError('Unknown transition')
        next_actions[key]=note.get('next_action');events.append(event);previous=event['sha256']
    ready=[k for k,n in nodes.items() if states[k]=='ready' and all(states[d]=='completed' for d in n['depends'])]
    selected=active or (ready[0] if ready else None)
    return dict(contract=contract,nodes=nodes,states=states,events=events,previous=previous,active=active,ready=ready,next=selected,next_action=next_actions.get(selected) or (nodes[selected]['action'] if selected else None))


def append(action,task,receipt,root=ROOT,base=BASE):
    state=load(root,base)
    p=(root/receipt).resolve();boundref=dict(path=str(p.relative_to(root.resolve())),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
    event=dict(sequence=len(state['events']),previous=state['previous'],task=task,action=action,evidence=boundref)
    event['sha256']=digest(event)
    # Validate a trial log before appending to the durable queue.
    import tempfile
    with tempfile.TemporaryDirectory(dir=base) as folder:
        trial=Path(folder);(trial/'contracts.json').write_bytes((base/'contracts.json').read_bytes())
        prior=(base/'events.jsonl').read_text() if (base/'events.jsonl').exists() else ''
        (trial/'events.jsonl').write_text(prior+json.dumps(event)+chr(10));load(root,trial)
    with (base/'events.jsonl').open('a') as out:out.write(json.dumps(event)+chr(10));out.flush()
    return event


def view(data):
    return dict(controller='python3 tools/run_followup_program_20261028.py',scope='Followup work packets; canonical376proposal acceptance obligations unchanged',tasks=len(data['nodes']),completed=sum(x=='completed' for x in data['states'].values()),blocked=[k for k,v in data['states'].items() if v=='blocked'],ready=data['ready'],active=data['active'],next=data['next'],next_action=data['next_action'],continue_work=data['next'] is not None,awards_acceptance=False,background_worker_running=False)


def main():
    p=argparse.ArgumentParser();p.add_argument('command',choices=['status','next','check','start','checkpoint','record','block']);p.add_argument('task',nargs='?');p.add_argument('--receipt');a=p.parse_args()
    if a.command in ['start','checkpoint','record','block']:
        if not a.task or not a.receipt:p.error('task and --receipt required')
        print(json.dumps(append(a.command,a.task,a.receipt)))
    else:
        data=load();print(json.dumps(dict(status='pass',events=len(data['events']),awards_acceptance=False) if a.command=='check' else view(data),indent=2))


if __name__=='__main__':main()

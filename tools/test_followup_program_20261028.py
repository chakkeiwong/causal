"""Meaningful scheduler regressions: independent work, custody and acceptance."""
import hashlib,json,tempfile
from pathlib import Path
import run_followup_program_20261028 as queue


def main():
    checks=[]
    with tempfile.TemporaryDirectory() as directory:
        root=Path(directory);base=root/'queue';base.mkdir()
        tasks=[dict(id=k,depends=deps,scope='fixture',action='inspect',outputs=[k+'.json'],acceptance=['actual work']) for k,deps in [('a',[]),('b',[]),('c',['b'])]]
        (base/'contracts.json').write_text(json.dumps(dict(tasks=tasks,evidence=[],awards_acceptance=False)))
        def note(name,d):
            p=root/name;p.write_text(json.dumps(d));return name
        def send(verb,key,**data):
            path=note(str(len(queue.load(root,base)['events']))+'-receipt.json',dict(task=key,awards_acceptance=False,**data))
            queue.append(verb,key,path,root,base)
        send('start','a',next_action='inspect a');send('block','a',reason='unavailable original',revisit_trigger='new legitimate original',next_action='wait only a')
        assert queue.load(root,base)['next']=='b';checks.append('Local block does not block independent task')
        send('start','b',next_action='inspect b')
        before=(base/'events.jsonl').read_bytes()
        try:send('record','b',execution='performed',outcome='pass',criteria=[],outputs=[])
        except ValueError:pass
        else:raise AssertionError('Accepted incomplete review')
        assert before==(base/'events.jsonl').read_bytes();checks.append('Invalid record leaves durable log unchanged')
        output=root/'b.json';output.write_text('{}');binding=dict(path='b.json',sha256=hashlib.sha256(output.read_bytes()).hexdigest())
        send('record','b',execution='performed',outcome='inconclusive',criteria=[dict(index=0,verdict='inconclusive',finding='Missing one source')],outputs=[binding],next_action='separate source followup')
        assert queue.load(root,base)['next']=='c';checks.append('Performed inconclusive work releases packet dependency without awarding acceptance')
        assert queue.view(queue.load(root,base))['awards_acceptance'] is False
        output.write_text('{"changed":true}')
        try:queue.load(root,base)
        except ValueError:checks.append('Changed bound output is rejected')
        else:raise AssertionError('Changed output admitted')
    print(json.dumps(dict(status='pass',checks=checks,canonical_controller_modified=False)))


if __name__=='__main__':main()

#!/usr/bin/env python3
"""Run/export synthetic local proposal handoffs; never call a model provider."""
from copy import deepcopy
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from causalbank.agent_workflow_v12 import AgentWorkflow, ReviewGrant
from causalbank.operation_contract_v12 import context_digest
from causalbank.problem_contract_v12 import declaration_digest

WORK=ROOT/'docs/program/repair-v12/work/LA05'
PROMPT='Offline authored proposal fixture. Preserve business targets, graph alternatives, clocks and unresolved assumptions. Propose only fixed operations.'


def save(name,value):
    (WORK/name).write_text(json.dumps(value,indent=2)+'\n')


def make_proposal(case,operations):
    return {'schema_version':'causalbank.agent-proposal/1','problem':deepcopy(case['problem']),
       'diagram':deepcopy(case['diagram']),'operations':operations,
       'model_record':{'mode':'offline_fixture','provider':'none','model':'authored-casebook','revision':'LA05-1',
        'prompt':PROMPT,'prompt_sha256':hashlib.sha256(PROMPT.encode()).hexdigest(),'parameters':{},'usage':None}}


def grant(p):
    unit=p['problem']['unit_of_analysis']
    return ReviewGrant(declaration_digest(p['problem'],p['diagram']),tuple(p['operations']),
       {'law':'independent_units','unit':unit,'fold_unit':unit},'Project synthetic fixture author')


def run():
    WORK.mkdir(parents=True,exist_ok=True)
    cases=json.loads((ROOT/'docs/program/repair-v12/work/LA02/casebook.json').read_text())['cases']
    (ROOT/'.runtime').mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(dir=ROOT/'.runtime') as folder:
        w=AgentWorkflow(Path(folder));outputs=[]
        for case in cases:
            p=make_proposal(case,['graph.review','identify.effect'])
            outputs.append({'case':case['id'],'proposal':p,'result':w.run(p,grant(p))})
        case=next(c for c in cases if c['id']=='discovery')
        p=make_proposal(case,['graph.review','identify.effect']);p['diagram']['models']=[p['diagram']['models'][1]]
        g=grant(p)
        try:
            w.run(p,g,interrupt_after=1)
        except InterruptedError as exc:
            interruption=str(exc)
        else:
            raise AssertionError('Fault fixture did not interrupt')
        resumed=w.run(p,g)
        assert w.run(p,g)==resumed
        outputs.append({'case':'directed_revision_recovery','proposal':p,'result':resumed,
                        'interruption':interruption,'exact_replay_equal':True})
        p=make_proposal(case,['estimate.effect']);p['diagram']['models']=[p['diagram']['models'][1]]
        g=grant(p);context=w.prepare(p,g)['requests'][0]['request']['scientific_context']
        ref=w.store.put({'context_sha256':context_digest(context),'mean':[1.,0.],
              'lrv':[[.01,0],[0,1]],'n':100,'alpha':.05,'simultaneous':True},'moment-summary/1','moment_summary')
        result=w.run(p,replace(g,numerical_inputs={'forward':[ref]}))
        assert result['results'][0]['response']['result']['coordinate_sets'][0]['topology']=='unbounded_union'
        outputs.append({'case':'weak_moment_set','proposal':p,'result':result})
        artifacts=[{'reference':r,'value':w.store.get(r)} for r in w.store.list_refs()]
        journals=[json.loads(p.read_text()) for p in sorted(w.journal.glob('*.json'))]
        save('artifact-bundle.json',{'scope':'Exported local synthetic execution artifacts, preserving every descriptor and value','artifacts':artifacts})
        save('journal-export.json',{'scope':'Exact local fixed-tool checkpoints; no multi-host recovery claim','journals':journals})
    save('prototype-evidence.json',{'status':'pass','evidence_kind':'executed_local_synthetic_semantics',
         'live_model_calls':0,'bank_data_used':False,'cases':outputs,
         'scope':'Author fixtures exercise validators, fixed local tools and recovery; no live-model quality result.'})
    save('contract.json',{'version':'causalbank.agent-proposal/1','backend':'offline fixture or recorded output only',
         'proposal_fields':['schema_version','problem','diagram','operations','model_record'],
         'model_record':'Mode/provider/model/revision/exact prompt+hash/parameters; unverified usage remains null; complete proposal hash binds output.',
         'permissions':'Trusted in-process ReviewGrant bound to exact declaration; no proposal grants or bank actions.',
         'supported_projection':'Unconditional static population ATE, one binary 1-versus-0 action, horizon starting at zero; all original declarations retained.',
         'operation_bounds':{'max_planned_operations':16,'per_worker_seconds':10,'per_worker_address_space_bytes':1024**3,'model_calls':0},
         'external_limits':['No authentication service','No live model adapter','No dynamic-policy/overlap/proxy target projection','No implemented discovery algorithm','No general identification or dependent-inference guarantee','No target-platform acceptance'],
         'replay':'Hash-binds complete proposal, grant, predecessor, requests, controller, schemas and runtime environment; verifies source and input bytes before journal reuse.'})
    print(json.dumps({'cases':len(outputs),'artifacts':len(artifacts),'journals':len(journals),
          'dispositions':{x['case']:x['result']['status'] for x in outputs},'live_model_calls':0}))


if __name__=='__main__':
    run()

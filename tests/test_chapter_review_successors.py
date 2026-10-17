"""Actual failed chapter outcomes can be repaired without changing old evidence."""
import copy
import pytest
import run_program_reviews_v2 as ext
from test_run_program import workspace, receipt, transition, run


def prepare(root,state):
    graph=run.core.read(root,'graph.json')
    old=graph['nodes'][0]
    graph['nodes'].append(dict(old,id='TEXT.REVIEW.I4',outputs=['out/i4.json']))
    run.core.write(root/'graph.json',graph)
    scope=run.core.read(root,'scope.json');scope['operation_stages']['TEXT.REVIEW.I4']='proposal_now';run.core.write(root/'scope.json',scope)
    run.core.write(root/'docs/program/repair-v12/chapter-plan.json',dict(chapters=[dict(id='I4',body_pages=dict(min=1,target=2,max=3))]))
    (root/'book.pdf').write_bytes(b'%PDF-1.4\ntest')
    state['reader']=run.bind(root,'book.pdf','Test reader')
    path=receipt(root,state,'TEXT.REVIEW.I4');data=run.core.read(root,path)
    data['outcome']='inconclusive';data['criteria'][0]['verdict']='inconclusive';run.core.write(root/path,data)
    transition(root,state,'record','TEXT.REVIEW.I4',path)
    old_result=copy.deepcopy(state['execution_program']['results']['TEXT.REVIEW.I4'])
    graph,_,_=run.combined(root,state);node=run.ledger.operation(graph,'TEXT.REVIEW.I4')
    target=run.review_output_paths(node,state['reader'],1)[0]
    run.core.write(root/target,dict(operation_id=node['id'],status='pass',reviewed_reader=state['reader'],allocation=dict(min=1,target=2,max=3),substantive_page_credit=1,per_page=[dict(printed_page=1,credit=1,rationale='New substantive proof')]))
    refs=[run.bind(root,target,'New reviewed chapter')]
    data=run.ledger.receipt_template(node)
    data.update(outcome='pass',execution='performed',scope='Author chapter review',reviewer=dict(name='test',kind='author'),outputs=refs,criteria=[dict(index=0,verdict='pass',finding='Repaired',evidence=refs)],review_attempt=1,reviewed_reader=state['reader'],prior_result=old_result)
    run.core.write(root/'successor.json',data)
    return old_result,path,target


def test_repairs_negative_review_preserving_old_receipt_and_contract(workspace):
    root,state=workspace;old,path,target=prepare(root,state)
    before=(root/path).read_bytes();contract=(root/'graph.json').read_bytes()
    ext.record_chapter(root,state,'TEXT.REVIEW.I4','successor.json');ext.validate_successors(root,state)
    assert state['execution_program']['results']['TEXT.REVIEW.I4']==old
    assert run.combined(root,state)[1]['execution_program']['results']['TEXT.REVIEW.I4']['outcome']=='pass'
    assert (root/path).read_bytes()==before and (root/'graph.json').read_bytes()==contract
    (root/path).write_text('corrupted historical result')
    with pytest.raises(ValueError):ext.validate_successors(root,state)


@pytest.mark.parametrize('failure',['stale_reader','wrong_prior','unperformed','insufficient_depth','old_output','changed_contract'])
def test_bad_successor_rejected_without_state_mutation(workspace,failure):
    root,state=workspace;old,path,target=prepare(root,state)
    data=run.core.read(root,'successor.json')
    if failure=='stale_reader':data['reviewed_reader']=dict(data['reviewed_reader'],sha256='0'*64)
    elif failure=='wrong_prior':data['prior_result']=dict(old,sha256='0'*64)
    elif failure=='unperformed':data['execution']='not_performed'
    elif failure=='old_output':data['outputs']=[run.bind(root,'out/i4.json','Old output')]
    elif failure=='changed_contract':data['operation_contract_sha256']='0'*64
    else:
        report=run.core.read(root,target);report['per_page'][0]['credit']=.5;report['substantive_page_credit']=.5;run.core.write(root/target,report)
        data['outputs']=[run.bind(root,target,'Insufficient review')];data['criteria'][0]['evidence']=data['outputs']
    run.core.write(root/'successor.json',data);before=copy.deepcopy(state)
    with pytest.raises(ValueError):ext.record_chapter(root,state,'TEXT.REVIEW.I4','successor.json')
    assert state==before


def test_current_pass_cannot_be_replaced(workspace):
    root,state=workspace;prepare(root,state)
    ext.record_chapter(root,state,'TEXT.REVIEW.I4','successor.json')
    with pytest.raises(ValueError,match='negative or inconclusive'):ext.record_chapter(root,state,'TEXT.REVIEW.I4','successor.json')

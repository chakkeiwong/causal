"""Trace unresolved software tails to exact receipts without resetting later work."""
import json,re
from collections import Counter
from pathlib import Path
from run_followup_program_20261028 import ROOT,BASE,append,load,bound
from prepare_followup_program_20261028 import ref,write


def bindings(value):
    if isinstance(value,dict):
        if isinstance(value.get('path'),str) and value.get('sha256'):yield value
        for x in value.values():yield from bindings(x)
    elif isinstance(value,list):
        for x in value:yield from bindings(x)


def main():
    key='SOFTWARE.TAILS';node=load()['nodes'][key]
    path=ROOT/'docs/program/execution/2026-10-28/program-refresh-delegate-contract-v1/remaining-operations.json'
    evidence=[ref(path,'Current unresolved-operation register')]
    start=BASE/'software-tails-start.json';write(start,dict(task=key,awards_acceptance=False,next_action=node['action'],evidence=evidence));append('start',key,str(start.relative_to(ROOT)))
    data=json.loads(path.read_text());selected=[r for r in data['operations'] if (r['id'].startswith('SW.CELL.') and r['status']=='inconclusive') or r['id'].startswith('SW.DECISION.')]
    assert sum(r['id'].startswith('SW.CELL.') for r in selected)==98 and sum(r['id'].startswith('SW.DECISION.') for r in selected)==6
    rows=[];sourcepaths=set()
    for row in selected:
        basis=row['action_basis'];bound(ROOT,basis);receipt=json.loads((ROOT/basis['path']).read_text())
        refs={}
        for b in bindings(receipt):
            if b['path'].endswith('.json') and re.search(r'omission|remaining|gap|search|decision|conversion|comparison|license',b['path']):refs[b['path']]=b
        documents=[]
        for path,b in sorted(refs.items()):
            bound(ROOT,b);content=json.loads((ROOT/path).read_text());documents.append(dict(binding=b,content=content));sourcepaths.add(path)
        findings=[dict(index=c['index'],verdict=c['verdict'],finding=c['finding'],evidence=c.get('evidence',[])) for c in receipt.get('criteria',[]) if c['verdict']!='pass']
        rows.append(dict(id=row['id'],status=row['status'],current_action=row['action'],action_basis=basis,unresolved_receipt_criteria=findings,exact_bound_tail_documents=documents,local_prerequisites=row['prerequisites'],inherited_outputs=receipt.get('outputs',[]),qualification_rule='Separate proposal comparison from native enablement; preserve source notices and matched target/rights restrictions.',later_work_reconciliation='Receipt-bound tails are preserved historical evidence. Before acquisition or a stronger unresolved claim,compare each named artifact with later source audits; this packet does not declare already inspected originals missing.',next_execution='Create a candidate-specific delta against current source audit,then acquire/inspect only genuinely missing originals or record a specific route limitation.'))
    out=BASE/'software-tails.json'
    write(out,dict(status='performed_trace_with_delta_reconciliation_remaining',software_cells=98,reuse_decisions=6,rows=rows,bound_tail_document_count=len(sourcepaths),evidence=evidence+[ref(Path(__file__),'Exact receipt/tail extraction')],limitations=['Full later-artifact reconciliation has not been completed for104rows; no blanket unresolved-source claim.','No candidate absence,coverage pass,license entitlement or runtime qualification inferred.'],next_action='Start the first explicit bounded source-tail delta; keep all other independent rows eligible.'))
    receipt=BASE/'software-tails-receipt.json';write(receipt,dict(task=key,awards_acceptance=False,execution='performed',outcome='inconclusive',outputs=[ref(out,'104rows with exact source-tail documents')],evidence=evidence,criteria=[dict(index=0,verdict='pass',finding='All98inconclusive cells and six unresolved reuse decisions trace to exact receipts and selected tail documents.'),dict(index=1,verdict='inconclusive',finding='No old tail is reset or presumed still missing;104row later-artifact deltas require candidate-specific review before acquisition.')],next_action='Perform candidate-specific current-audit delta,beginning with Python IID discovery; proceed independently of unavailable commercial originals.'))
    append('record',key,str(receipt.relative_to(ROOT)))
    print(json.dumps(dict(rows=len(rows),tail_documents=len(sourcepaths),outcome='inconclusive',next=load()['next'])))


if __name__=='__main__':main()

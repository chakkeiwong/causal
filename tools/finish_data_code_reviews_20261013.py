#!/usr/bin/env python3
"""Resume exact-reader reviews after the rejected data/code receipt was repaired."""
import json
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref,transition,write

ROOT=core.ROOT
REVIEW=ROOT/'docs/program/execution/2026-10-13/data-code'
BASE=REVIEW/'final'

def main():
    report=core.read(ROOT,str((BASE/'reader/build-report.json').relative_to(ROOT)))
    state=core.read(ROOT,core.STATE)
    assert state['reader']['sha256']==report['pdf']['sha256']
    assert 'LL.TASK.data_code' in state['execution_program']['results']
    assert not state['execution_runtime']['active']
    binding=ref(BASE/'working-release.json','Reviewed650-page data/code working reader')
    review=json.loads((BASE/'release-source-review.json').read_text())
    output=ROOT/'docs/program/comprehensive-v14/work/LL.TASK.data_code/task-synthesis.md'
    findings={
        'Q2':'All487 prior source records and citation contexts are unchanged. Ten new cited records include five authentic inspected scholarly PDFs, four pinned software sources and one local controller evidence source. The exact650-page reader has497 cited records and153 scholarly PDFs; source scope and unresolved package claims remain explicit.',
        'Q3':'Earlier portfolio results are preserved. The added5 versus250/41 target and availability-clock arithmetic replay, while LA05 eighty-case conformance remains local/offline with zero live model calls. No external package run or bank effect is claimed.',
        'Q4':'The prior investment argument is preserved. Data/code agent tasks identify reviewer effort, source custody, ontology pinning, bounded execution and benchmark construction as costs or risks; no incremental live-model price, bank ROI or measured benefit is inferred from source reports.'}
    for q,finding in findings.items():
        identifier='PROPOSAL.'+q
        current=core.read(ROOT,core.STATE);prior=current['execution_runtime']['results'][identifier]
        old_receipt=core.read(ROOT,prior['path']);folder=BASE/q;folder.mkdir(exist_ok=False)
        ev=[prior,binding,ref(BASE/'release-source-review.json','Reviewed exact-reader delta'),
            ref(REVIEW/'exact-results.json','Exact target/clock fixture'),ref(output,'Developed data/code synthesis')]
        write(folder/'reopen.json',{'reason':'New integrated data/code reader requires exact-release author review.',
            'prior_result':prior,'reviewed_reader':report['pdf'],'evidence':ev,
            'next_action':'Record the reviewed preserving delta with inherited and new scope limits.'})
        transition('reopen',identifier,folder/'reopen.json')
        current=core.read(ROOT,core.STATE);graph,_,_=run.combined(ROOT,current);node=run.ledger.operation(graph,identifier)
        attempt=len(current['execution_runtime']['review_history'][identifier])
        out=ROOT/run.review_output_paths(node,current['reader'],attempt)[0]
        limits=old_receipt['limitations']+['No live data/code agent performance, external package execution or bank truth.',
            'Q1 coverage/depth and Q5 rendered/sponsor acceptance remain open.']
        reviewed={'operation':identifier,'status':'pass','criterion':node['criteria'][0],'reviewer':review['reviewer'],
            'reviewed_reader':report['pdf'],'review_attempt':attempt,'acceptance_scope':'proposal_only',
            'scope':'Exact-reader author review of preserved material plus data/code synthesis',
            'findings':[finding],'evidence':ev,'limitations':limits,'visual_acceptance':False,'bank_ROI_established':False}
        write(out,reviewed)
        receipt=run.ledger.receipt_template(node)
        receipt.update(outcome='pass',execution='performed',scope=reviewed['scope'],reviewer=review['reviewer'],limitations=limits,
            reviewed_reader=report['pdf'],review_attempt=attempt,acceptance_scope='proposal_only',
            outputs=[ref(out,'Current-reader '+q+' review')],nonexecution_reason='',revisit_trigger='',
            criteria=[{'index':0,'verdict':'pass','finding':finding,'evidence':ev}])
        write(folder/'operation-receipt.json',receipt);transition('record',identifier,folder/'operation-receipt.json')
    status=run.status(ROOT,core.read(ROOT,core.STATE))
    print(json.dumps({k:status[k] for k in ['reader','next','recorded_proposal_operations','proposal_gaps']}),flush=True)

if __name__=='__main__':main()

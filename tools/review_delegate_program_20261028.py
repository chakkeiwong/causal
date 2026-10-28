"""Record the finite delegate review under the unchanged L6 chapter contract."""
import json
from pathlib import Path
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings

ROOT=Path(__file__).resolve().parents[1]
DAY=ROOT/'docs/program/execution/2026-10-28'
run=controller.base


def read(p):return json.loads(p.read_text())


def main():
    state=run.core.read(ROOT,run.core.STATE)
    assert state['execution_runtime']['active'] is None
    reader=DAY/'delegate-contract-reader-v1'
    release=read(reader/'working-release.json');verify_bindings(release)
    assert run.same_reader(state['reader'],release['pdf'])
    graph,merged,_=run.combined(ROOT,state)
    op='TEXT.REVIEW.L6';node=run.ledger.operation(graph,op)
    prior=merged['execution_program']['results'][op];assert prior['outcome']=='inconclusive'
    folder=DAY/'l6-delegate-criterion-v1';assert not folder.exists();folder.mkdir()
    source=DAY/'l6-delegate-review-v1';inspection=read(source/'inspection-review.json')
    assert inspection['inventory_only_files_remaining_in_this_worklist']==0
    evidence=[ref(p,a) for p,a in [
        (reader/'working-release.json','Exact current reader'),
        (reader/'release-source-review.json','All1403prior records,contexts and content inputs preserved'),
        (source/'source-audit.json','29selected originals with exact inspected anchors'),
        (source/'inspection-review.json','23technical and6scope-only file dispositions'),
        (source/'mathematical-review.json','Exact authored schema,retry and admission examples'),
        (DAY/'l6-criterion-review-v1/contract-matrix.json','Previous complete requirement matrix'),
        (ROOT/'docs/program/comprehensive-v14/work/TEXT.REVIEW.L6/chapter-review.json','Preserved ten exclusive page-equivalents'),
    ]]
    for p in [source/'source-audit.json',reader/'release-source-review.json']:verify_bindings(read(p))
    rows=[
      dict(requirement='Named hosted and local backend comparison',verdict='partial',completed='Six named provider/client families retain selected source contracts; the finite13backend files now have explicit technical/scope dispositions.',remaining='Exact hosted-service/model terms and deployment support remain candidate-specific; source-client contracts do not resolve them.'),
      dict(requirement='Broader framework and runtime comparison',verdict='pass_for_finite_selected_delegates',completed='All16listed framework files reviewed: terminal output,conditional validation,retries,metrics,errors and context/recovery boundaries integrate in the reader.',remaining='Unlisted transitive delegates and new products named by README migration/focus statements remain separate candidates; no whole-repository guarantee.'),
      dict(requirement='Scientific envelope and failure semantics',verdict='pass_for_proposal_design',completed='Original-schema validation,terminal versus scientific completion,selective retry accounting,pending actions,native stop reasons and explicit recovery identity are developed.',remaining='Native fixture and adapter conformance are later qualification,not grounds to erase the bounded literature disposition.'),
      dict(requirement='Reuse,licensing and model/service boundaries',verdict='partial',completed='Conditional thin-adapter adoption and reasons against wholesale ports are explicit; README scope leads do not inherit approval.',remaining='Exact model,tokenizer,template,parser,dependency and hosted-service rights need bounded artifact-specific profiles.'),
      dict(requirement='Substantive chapter depth',verdict='pass_preserved_minimum',completed='The original ten exclusive page-equivalents remain preserved; the new section is additional argument without duplicate page credit.',remaining='No new total-depth or fresh visual acceptance asserted.'),
    ]
    write(folder/'contract-matrix.json',dict(status='inconclusive',rows=rows,evidence=evidence,finite_worklist=dict(total=29,technical=23,scope_only=6,inventory_only_remaining=0),global_blocker=False,native_execution_required_for_literature_disposition=False))
    attempt=len(state['execution_runtime'].get('chapter_review_successors',{}).get(op,[]))+1
    output=ROOT/run.review_output_paths(node,state['reader'],attempt)[0]
    allocation=next(x['body_pages'] for x in run.core.read(ROOT,'docs/program/repair-v12/chapter-plan.json')['chapters'] if x['id']=='L6')
    revisit='Prepare bounded named hosted-service/model/artifact rights profiles and an explicit disposition of migration leads; preserve the completed29file review and do not repeat its build.'
    report=dict(operation_id=op,status='inconclusive',reviewer=dict(name='Codex author/coordinator',kind='author'),reviewed_reader=release['pdf'],allocation=allocation,substantive_page_credit=10,depth_basis='Preserved exclusive minimum,not newly reassigned page credit',findings=rows,evidence=evidence+[ref(folder/'contract-matrix.json','Current requirement matrix')],remaining_coverage=['Named service/model/artifact profiles','Explicit bounded disposition of migration leads and any newly essential delegate'],revisit_trigger=revisit,visual_acceptance=False,final_acceptance=False)
    write(output,report)
    receipt=run.ledger.receipt_template(node)
    receipt.update(execution='performed',outcome='inconclusive',scope='Exact-reader L6 finite-delegate review',reviewer=report['reviewer'],prior_result=prior,reviewed_reader=release['pdf'],review_attempt=attempt,outputs=[ref(output,'Preserved exact-reader successor')],limitations=['Selected anchored paths only; no whole-repository or live model verification.','Full hosted-service/artifact coverage and fresh visual acceptance remain open.'],revisit_trigger=revisit,criteria=[
      dict(index=0,verdict='inconclusive',finding='The finite29file delegate inventory is resolved and material findings integrated; full hosted-service/model/artifact coverage remains incomplete.',evidence=report['evidence']),
      dict(index=1,verdict='pass',finding='Ten exclusive substantive page-equivalents remain byte-preserved; no duplicate/new credit is claimed.',evidence=[evidence[1],evidence[6]])])
    write(folder/'operation-receipt.json',receipt)
    before=run.core.sha(ROOT/run.core.STATE)
    event=controller.previous.record_chapter(ROOT,state,op,str((folder/'operation-receipt.json').relative_to(ROOT)))
    run.commit(ROOT,before,state,event)
    print('L6 successor recorded:29finite dispositions complete; service/artifact coverage inconclusive.')


if __name__=='__main__':main()

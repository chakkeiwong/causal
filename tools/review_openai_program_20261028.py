"""Record finite census and exact-reader L6 criterion findings without acceptance inflation."""
import argparse
import json
from pathlib import Path
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings

ROOT = Path(__file__).resolve().parents[1]
DAY = ROOT / 'docs/program/execution/2026-10-28'
BASE = DAY / 'openai-contract-review-v1'
CENSUS = DAY / 'census-criterion-review-v1'
READER = DAY / 'openai-contract-reader-v1'
run = controller.base
core = run.core


def read(p):
    return json.loads(p.read_text())


def census():
    state = core.read(ROOT, core.STATE)
    assert state['execution_runtime']['active'] is None
    path = CENSUS / 'operation-receipt.json'
    verify_bindings(read(path))
    assert 'LL.CENSUS' not in state['execution_program']['results']
    before = core.sha(ROOT / core.STATE)
    event = run.apply(ROOT, state, 'record', 'LL.CENSUS', receipt=str(path.relative_to(ROOT)))
    run.commit(ROOT, before, state, event)
    write(CENSUS / 'recorded.json', dict(status='recorded_inconclusive', operation='LL.CENSUS',
        evidence=[state['execution_program']['results']['LL.CENSUS']],
        next_action='Do not repeat this completed finite review. Continue task-specific missing-source/edition and essentiality decisions under a reviewed successor; independent L6 evidence proceeds now.'))
    print('Recorded actual finite census review: coverage inconclusive, bounded route criterion pass.')


def chapter():
    state = core.read(ROOT, core.STATE)
    assert state['execution_runtime']['active'] is None
    release = read(READER / 'working-release.json')
    assert run.same_reader(state['reader'], release['pdf'])
    verify_bindings(release)
    graph, merged, _ = run.combined(ROOT, state)
    op = 'TEXT.REVIEW.L6'
    node = run.ledger.operation(graph, op)
    prior = merged['execution_program']['results'][op]
    assert prior['outcome'] == 'inconclusive'
    folder = DAY / 'l6-criterion-review-v1'
    assert not folder.exists()
    folder.mkdir()
    backend = ROOT / 'docs/program/execution/2026-10-24/backend-census-v1'
    framework = ROOT / 'docs/program/execution/2026-10-24/framework-census-v1'
    source = DAY / 'l6-openai-pinned-v1'
    evidence = [ref(p, a) for p, a in [
        (READER / 'working-release.json', 'Exact current reader'),
        (READER / 'release-source-review.json', 'All inherited inputs and contexts preserved'),
        (source / 'source-audit.json', 'Pinned official OpenAI cookbook and SDK originals'),
        (backend / 'source-audit.json', 'Five previous provider/client source profiles'),
        (backend / 'remaining-l6-gap.json', 'Unresolved provider/rights scope'),
        (framework / 'source-audit.json', 'Six framework source profiles'),
        (framework / 'omissions-register.json', 'Exact uninspected delegates and limits'),
        (ROOT / 'docs/program/comprehensive-v14/work/TEXT.REVIEW.L6/chapter-review.json', 'Preserved exclusive ten-page depth measurement'),
        (DAY / 'l6-official-markdown-v1/acquisition-review.json', 'Distinct official guide routes still unavailable'),
    ]]
    for p in [source / 'source-audit.json', backend / 'source-audit.json', framework / 'source-audit.json']:
        verify_bindings(read(p))
    rows = [
        dict(requirement='Named hosted and local backend comparison', verdict='partial',
             completed='Six named families now have pinned inspected source contracts: OpenAI, Anthropic, Google GenAI, Ollama, vLLM and llama.cpp.',
             remaining='Hosted deployment variants, selected model/service terms and eligible endpoint support still need an explicit bounded disposition; source-client behavior is not the service contract.'),
        dict(requirement='Broader framework and runtime comparison', verdict='partial',
             completed='Preserved LangChain, Semantic Kernel, DSPy, LlamaIndex, Haystack and delegated workflows source comparisons, alongside prior framework arguments.',
             remaining='Sixteen acquired framework files and thirteen backend files remain inventory-only in the saved registers. Review their relevance and material contract gaps before admitting new technical claims.'),
        dict(requirement='Scientific envelope and failure semantics', verdict='pass_for_proposal_design',
             completed='Connected argument and exact witnesses separate completion, representation, identification, refusal, nonidentification, phases and nested retry budgets.',
             remaining='Proposed adapter conformance needs later native qualification; this does not invalidate the bounded proposal argument.'),
        dict(requirement='Reuse, licensing and model/service boundaries', verdict='partial',
             completed='Source notices and conditional adoption/port/rejection reasoning are explicit; OpenAI adds a thin-adapter proposal.',
             remaining='Exact dependency, model, tokenizer, template, parser, deployment and service rights remain artifact-specific. Do not label all source acquisition globally blocked.'),
        dict(requirement='Substantive chapter depth', verdict='pass_preserved_minimum',
             completed='The original ten exclusive page-equivalents remain byte-preserved; the new section adds content without reassigning previous credits.',
             remaining='No fresh total-depth or visual acceptance is asserted. Full coverage remains a separate criterion.'),
    ]
    write(folder / 'contract-matrix.json', dict(status='inconclusive', rows=rows, evidence=evidence,
        native_execution_required_for_literature_disposition=False, global_blocker=False))
    attempt = len(state['execution_runtime'].get('chapter_review_successors', {}).get(op, [])) + 1
    output = ROOT / run.review_output_paths(node, state['reader'], attempt)[0]
    allocation = next(x['body_pages'] for x in core.read(ROOT, 'docs/program/repair-v12/chapter-plan.json')['chapters'] if x['id'] == 'L6')
    report = dict(operation_id=op, status='inconclusive', reviewer=dict(name='Codex author/coordinator', kind='author'),
        reviewed_reader=release['pdf'], allocation=allocation, substantive_page_credit=10,
        depth_basis='Previous exclusive minimum preserved, not a new all-page credit claim.',
        findings=rows, evidence=evidence + [ref(folder / 'contract-matrix.json', 'Full requirement/disposition matrix')],
        remaining_coverage=['Hosted service/model/rights profiles and bounded endpoint coverage', 'Material uninspected provider/framework delegates and their relevance decisions'],
        revisit_trigger='Review the exact listed acquired delegates and remaining service/model profile originals, integrate material differences, then record another preserved L6 successor.',
        visual_acceptance=False, final_acceptance=False)
    write(output, report)
    receipt = run.ledger.receipt_template(node)
    receipt.update(execution='performed', outcome='inconclusive', scope='Exact-reader L6 source, coverage and preserved-depth review',
        reviewer=report['reviewer'], prior_result=prior, reviewed_reader=release['pdf'], review_attempt=attempt,
        outputs=[ref(output, 'Preserved exact-reader L6 successor')],
        limitations=['Source and authored-design review only; no live backend, bank or final acceptance.', 'Ten-page minimum is preserved; provider/framework scope remains incomplete.', 'Visual allowance remains exhausted in the inherited session.'],
        revisit_trigger=report['revisit_trigger'], criteria=[
            dict(index=0, verdict='inconclusive', finding='Official OpenAI original-source omission is narrowed by two pinned repositories; full hosted/local service and framework-delegate coverage remains explicit and incomplete.', evidence=report['evidence']),
            dict(index=1, verdict='pass', finding='The ten exclusive substantive page-equivalents previously reviewed are preserved byte-for-byte by the successor build. No duplicate or new page credit is claimed.', evidence=[evidence[1], evidence[7]]),
        ])
    write(folder / 'operation-receipt.json', receipt)
    before = core.sha(ROOT / core.STATE)
    event = controller.previous.record_chapter(ROOT, state, op, str((folder / 'operation-receipt.json').relative_to(ROOT)))
    run.commit(ROOT, before, state, event)
    print('Recorded preserving L6 successor: source access improved; full coverage remains inconclusive.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['census', 'chapter'])
    globals()[parser.parse_args().command]()

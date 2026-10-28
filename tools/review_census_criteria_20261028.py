"""Review the finite saved census against its actual, unchanged contract."""
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-28/census-criterion-review-v1'
OLD = ROOT / 'docs/program/execution/2026-10-28/followup-causal-review-v1'


def read(p):
    return json.loads(p.read_text())


def ref(p, anchor):
    return dict(path=str(p.relative_to(ROOT)), sha256=hashlib.sha256(p.read_bytes()).hexdigest(), anchor=anchor)


def write(p, data):
    assert not p.exists(), p
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2) + chr(10))


def main():
    census = copy.deepcopy(read(OLD / 'census-register.json'))
    prior = next(x for x in census['items'] if x['id'] == 'LA01-candidate-214')
    assert prior['disposition'] == 'inspected_primary_retained_with_limits'
    assert prior['technical_source_review_open'] is True
    correction = dict(candidate=prior['id'], previous_fields={k: prior[k] for k in
        ['technical_source_review_open', 'availability', 'effect_on_claims']},
        finding='The selected author original was inspected. A stale Boolean and generic no-claims text disagreed with its disposition and bound primary source audit.',
        evidence=[prior['original'], prior['source_review']],
        unchanged='Final publisher bytes, supplementary version review and native replication remain separate omissions; no scientific acceptance is added.')
    prior.update(technical_source_review_open=False,
        availability='Selected genuine author original inspected; final publisher edition and supplementary-version comparison remain unresolved.',
        effect_on_claims='Only the inspected author-original claims and limitations in its bound source audit are admitted; no publisher-edition equivalence, native replication or bank truth is inferred.')
    write(BASE / 'candidate-214-correction.json', correction)
    candidates = [x for x in census['items'] if x['id'].startswith('LA01-candidate-')]
    unread = [x for x in candidates if x['disposition'] == 'open_original_not_inspected']
    inspected = [x for x in candidates if x['disposition'] == 'inspected_primary_retained_with_limits']
    assert (len(candidates), len(unread), len(inspected)) == (113, 31, 82)
    assert sum(x['technical_source_review_open'] for x in candidates) == 31
    census['supersedes'] = ref(OLD / 'census-register.json', 'Unchanged predecessor census')
    census['changes'] = ['Repair stale candidate214 technical-review flag and generic claim restriction; preserve 82/31 counts and all other records.']
    census['correction'] = ref(BASE / 'candidate-214-correction.json', 'Exact reviewed field correction')
    write(BASE / 'census-register.json', census)
    later = read(OLD / 'followup-lead-register.json')
    rows = later['rows']
    assert len(rows) == 95 and len({x['metadata_identity'] for x in rows}) == 79
    assert sum(x.get('duplicate_metadata_identity_of') is not None for x in rows) == 16
    contract = read(ROOT / 'docs/program/repair-v12/coverage-contract.json')
    tasks = [x['id'] for x in contract['llm_tasks']]
    assert len(tasks) == 14
    assert all(x.get('task_families') and x.get('effect_on_claims') and x.get('next_action') for x in candidates + rows)
    assert {t for x in candidates for t in x['task_families']} == set(tasks)
    task_rows = []
    for task in tasks:
        selected = [x for x in candidates if task in x['task_families']]
        leads = [x for x in rows if task in x['task_families']]
        task_rows.append(dict(task=task,
            inspected_inherited=[x['id'] for x in selected if not x['technical_source_review_open']],
            unread_inherited=[x['id'] for x in selected if x['technical_source_review_open']],
            followup_row_indices=[x['queue_index'] for x in leads],
            coverage='inconclusive',
            impact='Selected primary evidence supports only its audited claims. Unread sources and unsettled edition/essentiality questions prevent a comprehensive frontier-coverage claim.',
            next_action='Review direct missing originals and their essentiality for this task; keep related editions distinct. Do not require native execution or bank validation for literature disposition.'))
    write(BASE / 'task-impact-matrix.json', dict(tasks=task_rows, mapping_not_coverage=True))
    routes = read(ROOT / 'docs/program/execution/2026-10-13/llm-census/search-ledger.json')
    baseline = read(ROOT / 'docs/program/repair-v12/work/LA01/search-ledger.json')
    specialist = read(ROOT / 'docs/program/execution/2026-10-25/longitudinal-specificity-v1/search-review.json')
    assert {x['provider'] for x in routes['searches']} == {'OpenAlex', 'Crossref'}
    assert len(routes['searches']) == 6 and len(routes['citation_chains']) == 3
    assert sum(x['status'] == 'saved' for x in baseline['searches']) == 14
    search_review = dict(status='pass_for_bounded_search_route_criterion',
        original_task_queries=14, complementary_queries=6, specialist_queries=4,
        providers=['OpenAlex', 'Crossref'], inherited_citation_chains=baseline['citation_chains'],
        later_citation_chains=routes['citation_chains'],
        limits=['Ranked finite queries and a selected chain are not exhaustive literature proof.',
                'All 95 later rows are dispositioned, but 66 distinct acquisition/edition obligations remain.',
                'Index dates establish discovery precision only; individual original versions and the cutoff remain explicit.',
                'The earlier three arXiv query failures are retained; successful complementary routes do not erase them.'],
        evidence=[ref(ROOT / p, 'Saved routes, exact query/source identities and limitations') for p in
            ['docs/program/repair-v12/work/LA01/search-ledger.json',
             'docs/program/execution/2026-10-13/llm-census/search-ledger.json',
             'docs/program/execution/2026-10-25/longitudinal-specificity-v1/search-review.json',
             'docs/program/execution/2026-10-28/longitudinal-backward-chain-v1/metadata-review.json']])
    write(BASE / 'search-route-review.json', search_review)
    graph_path = ROOT / 'docs/program/execution/2026-10-13/work-graph.json'
    node = next(x for x in read(graph_path)['nodes'] if x['id'] == 'LL.CENSUS')
    criteria = [dict(index=0, verdict='inconclusive',
        finding='All 113 inherited candidates and 95 later rows have explicit evidence-backed dispositions, task mappings and claim limits. However, 31 inherited originals and 66 later acquisition/edition obligations remain; essentiality and full task coverage are not established. The author cannot close the essential-source condition by treating missing originals as inspected or as harmless omissions.',
        evidence=[ref(BASE / 'census-register.json', '113 inherited candidates and four crosscutting records'),
                  ref(OLD / 'followup-lead-register.json', '95 later rows with distinct identities and editions'),
                  ref(BASE / 'task-impact-matrix.json', 'All 14 task impacts and unresolved coverage')]),
        dict(index=1, verdict='pass',
        finding='Fourteen task queries, complementary OpenAlex/Crossref followups, four specialist queries and preserved citation chains cover the declared search scope. All saved later rows have explicit dispositions. This is a bounded-search finding, not an exhaustive frontier or saturation claim.',
        evidence=[ref(BASE / 'search-route-review.json', 'Actual successful routes, chains and preserved limits'),
                  ref(OLD / 'followup-lead-register.json', 'Every saved later row reconciled')])]
    output = ROOT / node['outputs'][0]
    report = dict(status='inconclusive', review_completed=True, coverage_closed=False,
        operation='LL.CENSUS', cutoff='2026-10-07T15:59:59Z', criteria=criteria,
        counts=dict(inherited_candidates=113, inspected=82, unread=31, later_rows=95,
            later_metadata_identities=79, duplicate_rows=16, later_acquisition_or_edition_obligations=66),
        separate_obligations=['Runtime component rights and native qualification', 'Public benchmark-oracle execution',
            'Authentic bank validation and adoption', 'L1/L6 manuscript coverage', 'Fresh visual/final acceptance'],
        continuation='Prioritize direct missing original/edition decisions and task-specific essentiality under a reviewed successor; do not rerun the completed finite audit. Continue independent L6 provider/framework evidence and other eligible proposal obligations.',
        no_global_access_blocker=True, final_acceptance=False,
        evidence=[ref(graph_path, 'Unchanged LL.CENSUS contract'), ref(BASE / 'plan-review.json', 'Reviewed finite audit plan'),
            ref(BASE / 'candidate-214-correction.json', 'Preserved correction'), ref(Path(__file__), 'Exact audit implementation')])
    write(output, report)
    import causal_program_v14 as ledger
    receipt = ledger.receipt_template(node)
    receipt.update(outcome='inconclusive', execution='performed', scope='Finite bounded literature census and criterion review; no full-coverage or capability acceptance.',
        reviewer=dict(name='Codex author/coordinator', kind='author'), criteria=criteria,
        outputs=[ref(output, 'Completed declared search-closure review with inconclusive coverage')],
        limitations=search_review['limits'] + ['Essential-source sufficiency remains inconclusive.', 'No new native model, public benchmark or bank trial performed.'],
        revisit_trigger='A reviewed successor resolves direct-source/edition omissions and task-specific essentiality; retain this completed inconclusive audit.')
    write(BASE / 'operation-receipt.json', receipt)
    print(json.dumps(dict(status='inconclusive', criteria=['inconclusive', 'pass'], counts=report['counts'], output=str(output.relative_to(ROOT)))))


if __name__ == '__main__':
    main()

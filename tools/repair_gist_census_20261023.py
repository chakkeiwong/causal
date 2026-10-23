#!/usr/bin/env python3
"""Create verified successors to the interrupted, unpublished GIST census audit."""
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path

import gist_artifact_reference_20261023 as exact
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings

ROOT = Path(__file__).resolve().parents[1]
DAY = ROOT / 'docs/program/execution/2026-10-23'
BASE = DAY / 'census-goal-state-v1'
RAW = ROOT / 'docs/literature/raw'
read = lambda p: json.loads(p.read_text())


def main():
    state = read(ROOT / 'docs/program/state.json')
    assert state['execution_runtime']['active']['operation'] == 'LL.CENSUS'
    prior_register = read(DAY / 'proof-statspai-v1/census-register.json')
    assert prior_register == read(BASE / 'census-register-before.json')
    audit = deepcopy(read(BASE / 'source-audit.json'))
    paper, software, project = audit['sources']
    assert paper['title'] == ['GIST-CMTF: Goal-State Inference for Causal Minimal Tool Filtering in LLM Agents']
    paper['title'] = paper['title'][0]
    page_claims = {
        3: ('confidence score', 'Symbolic states, preconditions/effects, inferred goals and ambiguity formulation.'),
        4: ('margin threshold', 'Candidate goals, confidence and margin thresholds, and clarification as a state transition.'),
        5: ('120', 'Algorithm and task construction: four request types and a controlled 120-task suite.'),
        6: ('mocked', 'Deterministic mocked execution, comparator definitions, metric definitions and aggregate results.'),
        7: ('TABLE II', 'Six-method aggregate results and distinction between wrong goals and tool selection.'),
        8: ('16.8%', 'Request-type regression, unnecessary clarification, token cost, Nova replacement and final-row error analysis.'),
        9: ('changing APIs', 'Controlled benchmark limitations, noisy users, changing APIs, open-world goals and clarification assumptions.'),
        10: ('monetary cost', 'Latency, monetary cost and user satisfaction remain unmeasured; artifact availability statement.')
    }
    paper['inspected_anchors'] = []
    for page, (token, finding) in page_claims.items():
        path = BASE / f'paper-page-{page:03d}.txt'
        assert token in path.read_text(), (page, token)
        paper['inspected_anchors'].append(dict(physical_page=page, anchor=finding, extracted_text=ref(path, token)))
    spans = {
        'README.md': [([41, 82], 'Controlled benchmark dimensions; released CSV table reproduction is distinct from provider-backed reruns.')],
        'LICENSE': [([1, 21], 'MIT source notice and attribution/warranty conditions; no transitive-rights conclusion.')],
        'CITATION.cff': [([1, 22], 'Two authors, repository and paper identity; metadata establishes identity only.')],
        'requirements.txt': [([1, 6], 'Six unpinned requirements: pandas, numpy, matplotlib, tqdm, boto3 and botocore.')],
        'src/gist_cmtf_runner.py': [
            ([37, 64], 'Default backend identifiers.'),
            ([211, 259], 'Breadth-first shortest-path filtering and lexical goal comparator.'),
            ([262, 323], 'Single selected-goal inference prompt and parse behavior.'),
            ([382, 425], 'Annotated request-type rule and intended-goal prompt context.'),
            ([428, 473], 'gold_path input and direct intended-goal substitution after clarification.'),
            ([480, 550], 'Tool-selection and wrong-tool counting branches.'),
            ([551, 585], 'Returned metrics and trace fields.'),
            ([618, 714], 'CLI overrides, model defaults, CSV schema and attempted-run exception output.')],
        'src/expand_gist_tasks.py': [([1, 20], 'Project task-generator identity.'), ([390, 406], 'Final task extension, total assertion and JSON output.')],
        'data/gist_tasks_120.json': [([1, 5902], 'Entire 120-object task file parsed; every task has gold_chains and lacks gold_path.')],
        'data/gist_tool_registry.json': [([1, 389], 'Entire registry parsed; 32 declared symbolic tools.')],
        'results/gist_task_metrics.csv': [([1, 5041], 'Header and all 5,040 saved final model-method-task rows parsed and reaggregated.')],
        'paper_outputs/tables/table_2_main_results_by_method.csv': [([1, 7], 'Header plus six aggregate method rows; this is the paper table, not results/summary_by_method.csv.')],
        'paper_outputs/tables/appendix_error_breakdown.csv': [([1, 7], 'Header plus six categories, including no-error rows and five error categories.')],
    }
    commit = read(RAW / 'exec23_gist_commit.json')[0]
    tree = read(RAW / 'exec23_gist_tree.json')
    assert commit['sha'] == 'e5a83858c6afdf3f3378defbdb723075496f035b'
    assert commit['commit']['tree']['sha'] == tree['sha'] == '99962404fecb7e4b5b862edc1047bd7be60e4a35'
    assert not tree['truncated']
    assert commit['commit']['committer']['date'] < '2026-10-07T15:59:59Z'
    entries = {entry['path']: entry for entry in tree['tree']}
    assert len(software['records']) == len(spans) == 11
    for record in software['records']:
        path = ROOT / record['local_copy']['path']
        data = path.read_bytes()
        receipt = read(ROOT / record['receipt']['path'])
        upstream = record['upstream_path']
        url = f'https://raw.githubusercontent.com/R-Suresh/GIST-CMTF/{commit["sha"]}/{upstream}'
        assert receipt['status'] == 'saved' and receipt['url'] == record['source_identity'] == url
        assert receipt['sha256'] == hashlib.sha256(data).hexdigest()
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert blob == entries[upstream]['sha'] == record['git_blob_sha1']
        assert len(data) == entries[upstream]['size']
        lines = data.decode().splitlines()
        record['inspected_anchors'] = []
        for (lo, hi), finding in spans[upstream]:
            assert 1 <= lo <= hi <= len(lines), (upstream, lo, hi, len(lines))
            record['inspected_anchors'].append(dict(lines=[lo, hi], finding=finding))
        record['supported_claims'] = [finding for _, finding in spans[upstream]]
        record['local_copy'] = ref(path, '; '.join(record['supported_claims']))
    software['inspected_anchors'] = [dict(upstream_path=r['upstream_path'], anchors=r['inspected_anchors']) for r in software['records']]
    software['supported_claims'] = [s.replace('the five package requirements', 'the six package requirements') for s in software['supported_claims']]
    software['commit_evidence'] = ref(RAW / 'exec23_gist_commit.json', 'Cutoff commit identity')
    software['tree_evidence'] = ref(RAW / 'exec23_gist_tree.json', 'Complete canonical Git tree')
    assert exact.calculate() == read(BASE / 'exact-results.json')
    verify_bindings(audit)
    audit['supersedes'] = ref(BASE / 'source-audit.json', 'Interrupted unpublished audit, retained with known schema errors')
    audit['corrections'] = ['Scalar paper title; validated physical-page anchors; structured valid line spans; six requirements; exact paper-table identity.']
    write(BASE / 'source-audit-v2.json', audit)

    register = deepcopy(prior_register)
    candidate = next(x for x in register['items'] if x['id'] == 'LA01-candidate-172')
    assert candidate['disposition'] == 'open_original_not_inspected'
    candidate.update(prior_disposition=candidate['disposition'], disposition='inspected_primary_retained_with_limits',
        technical_source_review_open=False, source_key='exec23_gist_paper', primary_source_record=paper,
        artifact_source_key='exec23_gist_sources', task_families=['business_translation', 'data_code', 'agent_architecture'],
        mapping_basis='Authentic original and pinned artifact establish a scoped goal-contract comparator; not causal-diagram correctness.',
        availability='Authentic arXiv v1 PDF and eleven Git-blob-authenticated artifacts inspected.',
        effect_on_claims='Reference only; no native, banking, identification or general causal-reasoning capability is granted.',
        next_action='Resolve generating revision, schema and cleaning provenance before testing label-free actual-user clarification.',
        publication_keys=['exec23_gist_paper', 'exec23_gist_sources', 'exec23_gist_reference'])
    assert all(row == next(x for x in register['items'] if x['id'] == row['id']) for row in prior_register['items'] if row['id'] != candidate['id'])
    counts = dict(Counter(x['disposition'] for x in register['items']))
    assert counts['inspected_primary_retained_with_limits'] == 69 and counts['open_original_not_inspected'] == 44
    register.update(counts=counts, supersedes=ref(DAY / 'proof-statspai-v1/census-register.json', 'Valid 68/45 predecessor'),
        changes=['Only candidate172 disposition changes; all other originals, StatsPAI and four crosscutting items preserved.'],
        closure=False, interpretation='69 of113 candidate originals inspected;44 unread; four crosscutting obligations remain.')
    write(BASE / 'census-register-v2.json', register)
    taskmap = deepcopy(read(DAY / 'proof-statspai-v1/task-map.json'))
    for family in taskmap['task_families']:
        if candidate['id'] in family.get('uninspected_candidate_ids', []):
            family['uninspected_candidate_ids'].remove(candidate['id'])
        if family['id'] in candidate['task_families']:
            for field, additions in [('inspected_candidate_ids', [candidate['id']]), ('inspected_source_keys', candidate['publication_keys'])]:
                family.setdefault(field, [])
                family[field].extend(x for x in additions if x not in family[field])
        family['coverage_acceptance'] = False
    taskmap['register'] = ref(BASE / 'census-register-v2.json', 'Corrected successor')
    taskmap['supersedes'] = ref(DAY / 'proof-statspai-v1/task-map.json', 'Preserve StatsPAI and all prior family mappings')
    write(BASE / 'task-map-v2.json', taskmap)
    omissions = dict(items=[
        'Generating revision, CLI overrides and full provider/cleaning logs remain unresolved; saved-table aggregation is not model-call reproduction.',
        'Actual human clarification, label-free request classification, changing APIs, latency and costs remain untested.',
        'No causal-diagram correctness, effect identification or bank performance is established.',
        '44 originals and four crosscutting obligations remain; LL.CENSUS is not complete.'
    ], visual_acceptance=False, native_execution=False, coverage_acceptance=False)
    write(BASE / 'omissions-register-v2.json', omissions)
    corrections = dict(status='repaired_through_successor', evidence=[ref(BASE / n, 'Preserved failed preparation') for n in
        ['source-audit.json', 'census-register.json', 'source-audit-initial-failure.txt']],
        findings=['Failed preparations mixed scalar/list title and tuple structures; source line ranges and six-package count corrected.',
        'The paper summary artifact is paper_outputs/tables/table_2_main_results_by_method.csv, not results/summary_by_method.csv.',
        'Recovered from proof-statspai-v1 68/45 baseline, preserving StatsPAI and all other candidates.',
        'No full-operation pass receipt created: this unit supplies scoped progress only.',
        'The initial shell-read transport syntax error performed no filesystem action.'],
        successor=ref(BASE / 'source-audit-v2.json', 'Validated successor'))
    write(BASE / 'recovery-corrections-v2.json', corrections)
    evidence = [ref(BASE / n, 'Reviewed source/census evidence') for n in ['source-audit-v2.json', 'exact-results.json',
        'development.tex', 'plan.md', 'census-register-v2.json', 'task-map-v2.json', 'omissions-register-v2.json', 'recovery-corrections-v2.json']]
    evidence += [ref(Path(__file__), 'Successor validation and preservation logic'), ref(Path(exact.__file__), 'Independent data/AST checks')]
    review = dict(status='pass_for_scoped_source_review', reviewer=dict(name='Codex author/coordinator', kind='author'),
        evidence=evidence, findings=paper['supported_claims'] + software['supported_claims'] + project['supported_claims'],
        limitations=omissions['items'], coverage_acceptance=False, native_execution=False, visual_acceptance=False)
    verify_bindings(review)
    write(BASE / 'review-v2.json', review)
    progress = dict(finding='Candidate172 authentic original and eleven artifacts reviewed; source/schema and output-provenance gaps preserved. Census now69/44.',
        next_action='Integrate reviewed GIST goal-contract evidence into preserving reader/sponsor successors; then continue44 unread originals and independent reuse decisions. Full census remains open.',
        yield_reason='Release canonical operation for publication and independent obligations; this checkpoint is not completion or a permission boundary.',
        evidence=[ref(BASE / 'review-v2.json', 'Scoped author review'), ref(BASE / 'census-register-v2.json', '69/44 census'),
                  ref(BASE / 'task-map-v2.json', 'Preserved mappings with business translation added')])
    write(BASE / 'progress-v2.json', progress)
    print(json.dumps(dict(inspected=69, unread=44, authenticated_artifacts=11, requirements=6, full_census_closed=False)))


if __name__ == '__main__':
    main()

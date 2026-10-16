#!/usr/bin/env python3
"""Preserve primary sources and concrete omissions for reporting synthesis."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
from datetime import datetime, timezone
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write
import reporting_reference_20261016 as examples

ROOT, BASE = examples.ROOT, examples.BASE
PRIOR = ROOT / 'docs/program/execution/2026-10-16/datahub-reuse/publication/reader/source-audit.json'
OP = 'LL.TASK.reporting_monitoring'
OUTPUT = ROOT / 'docs/program/comprehensive-v14/work' / OP / 'task-synthesis.md'
REVIEWER = {'name': 'Codex author/coordinator', 'kind': 'author'}
LIMITS = [
    'Bounded task synthesis, not exhaustive census or completed chapter-depth acceptance.',
    'Paper findings are author-reported; no live-model or upstream package trial is claimed.',
    'Three task-specific candidate originals remain incomplete or unavailable on the tested routes.',
    'Static package paths and exact authored examples do not establish runtime integration.',
    'Identification assumptions, change truth and bank utility are not established by faithful reporting.',
    'Selective and sequential uncertainty require their own valid joint-law arguments.',
    'New package/dependency rights, complete distributions and actual adapters remain unqualified.',
    'Rendered visual acceptance remains open under the inherited exhausted six-preview allowance.'
]


def read(p):
    return json.loads(p.read_text())


def main():
    prior = read(PRIOR); verify_bindings(prior)
    by_key = {s['integrated_citation_key']: s for s in prior['sources']}
    inherited = read(BASE / 'inherited-primary-selection.json'); verify_bindings(inherited)
    assert len(prior['sources']) == 670
    assert examples.calculate() == read(BASE / 'exact-results.json')
    now = datetime.now(timezone.utc).isoformat()
    selections = [
        ('exec16_report_flowfixer', 'Diagnosis-Driven Automatic Repair for Agentic Workflow via Symbolic Inference',
         'Ma', 'Xuyan Ma and Yawen Wang and Junjie Wang and Xiaofei Xie and Boyu Wu and Mingyang Li and Dandan Wang and Qing Wang',
         ROOT / 'docs/literature/raw/exec16_report_repair.pdf', 'https://arxiv.org/pdf/2607.02882v1',
         'arXiv:2607.02882v1; 2026-07-03', 'repair',
         [(4, 'Symbolic node assertions include existence, ordering and input constraints; these are workflow specifications, not a bank identification theorem.'),
          (6, '307 AgentFail logs plus 136 n8n cases; dynamic verification uses original test inputs and bounded repair retries.'),
          (7, 'Table II: repair 71.3%, failure attribution84.4%; RCA87.9% is conditional on correct attribution; three repeated repairs per case; differences are percentage points.'),
          (9, 'Pre-execution filtering precision99.7% and recall84.6%; some model/tool failures only emerge during dynamic execution.')]),
        ('exec16_report_psebench', 'PSEBench A Controllable and Verifiable Benchmark for Evaluating LLMs in Patient Safety Event Triage',
         'Han', 'Keqi Han and Ryan Young and Annabel Strauss and Lindsey Hughes and Katharine M. Nesbitt and Nicole Schueler and Che Ngufor and Carl Yang and Yuan Xue and Zhijun Yin',
         ROOT / 'docs/literature/raw/exec16_report_psebench_v2.pdf', 'https://arxiv.org/pdf/2606.05463v2',
         'arXiv:2606.05463v2; 2026-06-09; v1 retained separately', 'psebench-v2',
         [(3, 'Clause cards factor policy predicates, facts, groundings and constraints; humans finalize reusable specifications.'),
          (6, 'Fifteen-model comparison: high verdict accuracy can coexist with low uncertainty detection; paper-reported GPT-5 scores90.2% verdict accuracy and12.8% uncertainty-detection F1.'),
          (7, '3455 complete,1362 missing and257 uncertain cases; conditioned verdict accuracy varies strongly by case type.'),
          (9, 'Synthetic narratives, idealized Ask interface and MN29-specific rules limit transfer to live or other-domain environments.')]),
        ('exec16_report_kimeconomy', 'Application of LLM Causal Inference about Prediction of Korean Economic Growth and The Characteristics Analysis of Causal Inference',
         'Kim', 'Dong Hwa Kim', BASE / 'candidate-35-elevated.response',
         'https://doi.org/10.17148/iarjset.2026.13222', 'IARJSET13(2); February2026; DOI10.17148/IARJSET.2026.13222', 'candidate-35',
         [(6, 'SectionIII introduces ChatGPT prediction/model illustrations.'),
          (7, 'The author explicitly says the SCM/backdoor response needs confirmation.'),
          (8, 'The author says Figures4-9 were made by ChatGPT and does not believe all are true or correct.'),
          (9, 'Discussion/conclusion calls for further model/application study; these passages are not validated causal or monitoring performance.')]),
        ('exec16_report_netops', 'Large Language Models for Agentic NetOps and AIOps Architectures Evaluation and Safety',
         'Bilal', 'Muhammad Bilal and Jon Crowcroft and Ruizhi Wang and Xiaolong Xu and Schahram Dustdar',
         BASE / 'candidate-196-elevated.response',
         'https://repositum.tuwien.at/bitstream/20.500.12708/229494/1/Bilal-2026-Large%20Language%20Models%20for%20Agentic%20NetOps%20and%20AIOps%20Architectu...-smur.pdf',
         'Retrieved preprint arXiv:2605.12729v2; 2026-06-15; not asserted identical to the journal edition', 'candidate-196',
         [(12, 'Provenance and freshness vary across logs, metrics, traces and change records; sampled traces have coverage gaps.'),
          (26, 'Service invariants and causal framing are proposed operational contracts, not evidence that calibrated probabilities are supplied.'),
          (32, 'Separate abstention quality, tool cost, latency, drift and trace-grounded scoring; LLM judge is auxiliary.'),
          (33, 'Trace replay, sandbox, live testbed and canary evidence occupy distinct evaluation levels.')])
    ]
    sources = []
    for key, title, surname, authors, raw, url, version, stem, findings in selections:
        data = raw.read_bytes(); assert data.startswith(b'%PDF-')
        subprocess.run(['pdfinfo', str(raw)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        target = ROOT / 'docs/papers' / f'{title} {surname}(2026).pdf'
        assert not target.exists(); shutil.copyfile(raw, target)
        assert target.read_bytes() == data
        anchors = []
        for page, finding in findings:
            extract = BASE / f'{stem}-page-{page}.txt'
            assert extract.is_file() and len(extract.read_text()) > 100
            anchors.append({'anchor': f'Physical PDF page {page}', 'finding': finding,
                            'extracted_text': ref(extract, 'Inspected primary text')})
        related = [ref(raw, 'Original retrieved bytes')]
        if key in ['exec16_report_flowfixer', 'exec16_report_psebench']:
            related += [ref(raw.with_suffix('.receipt.json'), 'Fixed-collector retrieval receipt'),
                        ref(ROOT / 'docs/literature/raw/exec16_report_versions.xml', 'Version discovery metadata')]
        else:
            related += [ref(raw.with_suffix('.headers'), 'Actual public response headers')]
        sources.append({'integrated_citation_key': key, 'kind': 'paper', 'title': title,
            'filename_title': title, 'first_author': surname, 'author': authors, 'year': 2026,
            'source_identity': url, 'version_date': version, 'cutoff': '2026-10-07', 'accessed_utc': now,
            'local_copy': ref(target, 'Genuine primary PDF inspected at stated pages'),
            'local_path': str(target.relative_to(ROOT)), 'sha256': hashlib.sha256(data).hexdigest(),
            'inspected_anchors': anchors, 'supported_claims': [f for _,f in findings],
            'related_primary_bytes': related, 'limitations': LIMITS})
    write(BASE / 'new-paper-audit.json', {'sources': sources})
    papers = []
    for row in inherited['papers']:
        source = by_key[row['key']]
        pages = row['pages']
        papers.append({'key': row['key'], 'inherited_source': source,
                       'reread_pages': [ref(BASE / f"{row['key']}-page-{p}.txt", f'Physical PDF page{p}') for p in pages]})
    papers.append({'key': 'exec13_pulse', 'inherited_source': by_key['exec13_pulse'],
                   'reread_pages': [ref(BASE / 'exec13_pulse-pages-6-8.txt', 'Physical pages6-8; separate orchestration and root-cause metrics')]})
    code_paths = [
        ('docs/literature/raw/v12_la_oci_agent_source_3.txt', [(15,49),(52,120),(120,175)],
         'OCI notebook runner checks interpreter, accepts selected notebook, disables notebook timeout and serializes per-estimand results; adapt artifact idea, bound execution separately.'),
        ('docs/literature/raw/v12_la_causalagent_source_2.txt', [(1,30)],
         'excute_output extracts outer braces and returns an empty dict on JSONDecodeError; require typed failure in proposed adapter.'),
        ('src/causalbank/runtime_v12.py', [(161,221),(311,349)],
         'Distinct authorized response artifacts, execution identity and checkpoint consistency; declaration summaries remain schema-only and do not render numerical results or scientific monitoring.'),
        ('src/causalbank/agent_workflow_v12.py', [(225,260)],
         'Agent report preserves decisions/obligations and explicitly denies bank-action authorization.')]
    records = []
    for path, spans, claim in code_paths:
        lines = (ROOT / path).read_text().splitlines()
        records.append({'role': 'inspected_primary_technical_text', 'local_copy': ref(ROOT/path, claim),
                        'inspected_anchors': [{'anchor': f'lines{a}-{min(b,len(lines))}',
                            'excerpt': '\n'.join(lines[a-1:min(b,len(lines))])} for a,b in spans], 'supported_claims': [claim]})
    review = {'status': 'pass_for_bounded_synthesis', 'reviewer': REVIEWER, 'papers': papers,
              'new_papers': sources, 'packages': inherited['packages'], 'records': records,
              'limits': LIMITS, 'runtime_execution': 'none newly performed'}
    verify_bindings(review); write(BASE/'source-review.json', review)
    census = read(ROOT/'docs/program/execution/2026-10-13/llm-census/census-register.json')
    decisions = {
        35: ('inspected_cautionary_example', 'Original explicitly qualifies its generated figures; do not use as validated forecasting or causal monitoring.'),
        138: ('inspected_adjacent_repair', 'Workflow specification and dynamic repair are useful mechanisms, with separate conditional metrics; no causal-effect calibration claim.'),
        196: ('inspected_adjacent_contract', 'Repository supplied genuine June15 preprint, distinct from October journal metadata; operational evidence ladder is relevant, underlying cited systems not independently reviewed here.'),
        246: ('inspected_adjacent_benchmark', 'Use cutoff-compatible v2. Separate missing information from irreducible uncertainty; medical policy benchmark is not banking causal ground truth.'),
        259: ('open_incomplete_original', 'Landing page200; direct publisher PDF timed out after25s with4955884 of9261063 bytes. Partial bytes retained and never treated as a paper.'),
        273: ('open_original_access_denied', 'DOI redirect to SSRN returned403. Obtain permitted author/repository original and inspect bitemporal semantic claims.'),
        282: ('open_nonpdf_download_page', 'PMC URL returned200 HTML download-preparation page,1817 bytes; no genuine original. Resolve permitted stable original and inspect before technical use.')}
    rows=[]
    for number,(status,reason) in decisions.items():
        candidate=next(r for r in census['items'] if r['id']==f'LA01-candidate-{number}')
        evidence=[ref(p,'Actual saved public response or headers') for p in sorted(BASE.glob(f'candidate-{number}*')) if p.suffix in ['.headers','.response'] and p.stat().st_size]
        rows.append({'id':candidate['id'],'candidate':candidate,'disposition':status,'reason':reason,
                     'availability': 'Actual route outcomes only; no global unavailability claim', 'evidence':evidence,
                     'revisit': 'Resolve authentic accessible version and inspect task-relevant methods, adverse findings, code and rights before broader claims.' if status.startswith('open') else 'Reassess when stronger version or matching causal monitoring evidence appears.'})
    write(BASE/'candidate-reassessment.json', {'cutoff':'2026-10-07','coverage_acceptance':False,'items':rows,
          'scope':'All seven task-specific pending IDs reassessed; four primary originals inspected; three remain open.',
          'failures':['Initial five sandbox curl attempts all failed DNS; authorized elevated retries produced recorded outcomes.',
                      'PSEBench v1 retained; v2 replaces it for technical claims after metadata revealed a pre-cutoff update.',
                      'Initial bounded inspection incorrectly assumed inherited schema fields; KeyError occurred before any mutation, then schema was inspected.'],
          'evidence':[ref(BASE/'new-paper-audit.json','Four new genuine papers'),ref(BASE/'acquisition-manifest.json','First bounded acquisition'),ref(BASE/'acquisition-manifest-v2.json','Version correction')]})
    write(BASE/'omissions-register.json', {'items':[r for r in rows if r['disposition'].startswith('open')],
          'other_gaps':['No comprehensive additional source search; inherited task census remains bounded.',
                        'New FlowFixer, PSEBench and CausalPulse package implementations, dependencies and rights not reviewed here.',
                        'No live-model comparison or calibrated monitoring mechanism implemented.',
                        'Conditional and sequential validity, data/assignment truth, future owner decisions and bank utility remain separate.'],
          'evidence':[ref(BASE/'candidate-reassessment.json','All seven concrete dispositions')], 'limitations':LIMITS})
    print(json.dumps({'new_genuine_papers':4,'inherited_papers_reread':5,'source_records':4,'pending_candidates':3}))


if __name__ == '__main__': main()

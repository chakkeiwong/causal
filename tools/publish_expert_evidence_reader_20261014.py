#!/usr/bin/env python3
"""Preserve and review the exact expert-evidence working reader."""
import argparse
import json
from pathlib import Path
import re

import build_expert_evidence_reader_20261014 as build
import master_control as core
import review_expert_evidence_20261014 as work
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

ROOT, BASE, OUT = work.ROOT, build.BASE, build.OUT
LIMITS = [
    'Author review only; no independent scientific or bank acceptance.',
    'Eight primary papers and selected PyWhyLLM source paths; no model calls or installed upstream engine.',
    'Exact imposed mechanisms do not establish empirical accuracy, general sharp bounds or bank ROI.',
    'No automatic substantive-page credit or mandatory-repair closure; Q1 remains open.',
    'The inherited six-preview allowance is exhausted under /home/ubuntu/AGENTS.md; rendered acceptance and Q5 remain open.',
]
NEW_KEYS = {'exec14_expert_auditor', 'exec14_expert_argumentation',
            'exec14_expert_pywhy', 'exec14_expert_oracle'}
CHANGED_CONTEXTS = {'exec13_hallucination', 'v12_la_2402_07770',
                    'v12_la_2402_15301', 'v12_la_2405_13551',
                    'v12_la_2410_14146', 'v12_la_2609_30867'}


def review():
    report = json.loads((OUT/'build-report.json').read_text())
    audit = json.loads((OUT/'source-audit.json').read_text())
    prior = json.loads(build.PRIOR.read_text())
    index = json.loads((BASE/'traceability-review.json').read_text())
    for obj in [report, audit, prior, index,
                json.loads((BASE/'prepared-inputs.json').read_text())]:
        verify_bindings(obj)
    assert index['status'] == 'pass' and not index['issues']
    assert index['scholarly_pdfs'] == 155
    assert json.loads((OUT/'text-layout-review.json').read_text())['status'] == 'pass'
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    old = {s['integrated_citation_key']: s for s in prior['sources']}
    new = {s['integrated_citation_key']: s for s in audit['sources']}
    assert len(old) == 518 and len(new) == 522
    assert all(new[k] == v for k, v in old.items())
    assert new.keys()-old.keys() == NEW_KEYS
    compiled = {r['path']: r for r in audit['tex_files']}
    inherited = [r for r in prior['tex_files'] if r['path'] != str(build.OLD.relative_to(ROOT))]
    assert all(compiled[r['path']]['sha256'] == r['sha256'] for r in inherited)
    previous = json.loads((ROOT/'docs/program/execution/2026-10-14/causalnex-reuse/publication/traceability-review.json').read_text())
    contexts = {r['citation_key']: r['citation_contexts'] for r in index['records']}
    changed = {r['citation_key'] for r in previous['records']
               if contexts[r['citation_key']] != r['citation_contexts']}
    assert changed == CHANGED_CONTEXTS
    assert work.calculate() == json.loads((work.BASE/'exact-oracle.json').read_text())
    extracted = re.sub(r'\s+', ' ', (OUT/'reader.txt').read_text())
    for phrase in ['Expert evidence, disagreement and causal refusal',
                   'hard constraints', 'USD 30 and minus USD 20', '1024/1025',
                   '1/1025', 'current review enables no adapter']:
        assert phrase.lower() in extracted.lower(), phrase
    findings = [
        'Eight primary readings distinguish retrieval, soft priors, auditing, formal consistency and evidential adequacy from causal truth; adverse findings and design restrictions remain explicit.',
        'The new Zhang and Li/Russo papers resolve two inherited omissions with authentic PDFs. Their BIC, design, constraint, semantic-leakage and runtime limitations accompany the reported findings.',
        'Six inherited citation contexts were substantively reread; their source records and all prior chapter inputs are preserved.',
        'The pinned PyWhyLLM inspection supports a conditional adaptation route with source identity, unknown states, finite budgets and separate graph validation; no adapter is enabled.',
        'Exact observational equivalence, intervention values, duplicate evidence and correlated-consensus calculations replay without changing saved evidence.',
        'Extracted physical pages 355-360 were inspected, including displayed distributions and transitions. Text/bounds checks pass for710 pages; this does not replace rendered review.',
    ]
    evidence = [ref(p, anchor) for p, anchor in [
        (OUT/'build-report.json', 'Exact successor PDF identity and pages'),
        (OUT/'source-audit.json', '522 complete citation records'),
        (OUT/'reader.txt', 'Expert discussion on physical pages355-360'),
        (OUT/'text-layout-review.json', 'All-page extracted text and bounds'),
        (BASE/'traceability-review.json', '155 genuine scholarly PDFs and citation contexts'),
        (BASE/'prepared-inputs.json', 'Preserved manuscript inputs'),
        (work.BASE/'primary-review.json', 'Eight papers and selected pinned code paths'),
        (work.BASE/'candidate-reassessment.json', 'Resolved and remaining omissions'),
        (work.BASE/'exact-oracle.json', 'Independently replayed rational calculations'),
        (work.SYN, 'Connected expert-evidence argument'),
        (Path(__file__), 'Exact-reader source and mathematics review'),
    ]]
    write(BASE/'release-source-review.json', {
        'status': 'pass', 'issues': [], 'reviewer': work.REVIEWER,
        'scope': 'Exact-reader expert-evidence argument, sources and mathematics',
        'reviewed_reader': report['pdf'], 'findings': findings, 'evidence': evidence,
        'unchanged_source_records': 518, 'new_source_records': sorted(NEW_KEYS),
        'changed_inherited_citation_contexts': sorted(changed),
        'unchanged_inherited_compiled_sources': len(inherited),
        'limitations': LIMITS, 'visual_acceptance': False, 'bank_ROI_established': False,
    })
    print(json.dumps({'review': 'pass', 'pages': report['pages'], 'cited_records': 522}))


def publish():
    state = core.read(ROOT, core.STATE)
    before = core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path'] == str(build.OLD.with_suffix('.pdf').relative_to(ROOT))
    assert 'LL.TASK.expert_evidence' in state['execution_program']['results']
    report = json.loads((OUT/'build-report.json').read_text())
    audit = json.loads((OUT/'source-audit.json').read_text())
    review = json.loads((BASE/'release-source-review.json').read_text())
    verify_bindings(review)
    manifest = {
        'kind': 'working_monograph', 'final_acceptance': False,
        'pdf': report['pdf'], 'pages': report['pages'],
        'supersedes': {k: state['reader'][k] for k in ['path', 'sha256']},
        'build_report': ref(OUT/'build-report.json', 'Compiled preserving expert-evidence addition'),
        'source_review': ref(BASE/'release-source-review.json', 'Reviewed source and mathematics delta'),
        'text_layout': ref(OUT/'text-layout-review.json', 'Every-page text and bounds check'),
        'source_artifacts': audit['tex_files']+review['evidence'],
        'visual_acceptance': False, 'mandatory_repairs_closed': [],
        'changes': [
            'Integrate expert evidence, conflicting sources, causal refusal and conditional PyWhyLLM adaptation.',
            'Develop exact banking ambiguity, shared-source and consensus-dependence mechanisms.',
        ],
        'sponsor_binding': 'Preserved sponsor baseline; Q5 reconciliation remains open.',
    }
    write(BASE/'working-release.json', manifest)
    binding = ref(BASE/'working-release.json', 'Reviewed expert-evidence working reader')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, {'action': 'publish_expert_evidence_reader',
                                    'manifest': binding, 'final_acceptance': False})
    print(json.dumps({'published': state['reader'], 'proposal_accepted': False}))


def renew():
    report = json.loads((OUT/'build-report.json').read_text())
    findings = {
        'Q2': 'All518 inherited records and chapter inputs are preserved. Six inherited citation contexts were reread, and four new records add two authentic papers, pinned PyWhyLLM code and exact derivations:522 records and155 genuine scholarly PDFs. Source support and explicit omissions pass for the current scope.',
        'Q3': 'The existing demonstration portfolio is preserved. Rational calculations reproduce identical observational laws with distinct causal values, duplicated evidence and consensus under independent versus shared errors. No empirical model accuracy, upstream runtime or general sharp bounds are claimed.',
        'Q4': 'Existing scenarios remain intact. The illustrative USD30 versus minus USD20 decision demonstrates why unresolved assignment matters; proposed public/generated evidence-handling comparisons include manual and deterministic baselines, all-request accounting and total costs before expensive bank trials. Prices and bank ROI are not invented.',
    }
    verify_bindings(json.loads((BASE/'release-source-review.json').read_text()))
    for q, finding in findings.items():
        identifier = 'PROPOSAL.'+q
        state = core.read(ROOT, core.STATE)
        assert state['reader']['sha256'] == report['pdf']['sha256']
        previous = state['execution_runtime']['results'][identifier]
        old = json.loads((ROOT/previous['path']).read_text())
        folder = BASE/q
        folder.mkdir(exist_ok=False)
        evidence = [previous, ref(BASE/'working-release.json', 'Exact successor working reader'),
                    ref(BASE/'release-source-review.json', 'Reviewed expert-evidence delta'),
                    ref(Path(__file__), 'Exact-reader renewal findings')]
        write(folder/'reopen.json', {
            'reason': 'Reader changed; preserve and renew the prior exact-reader review.',
            'prior_result': previous, 'reviewed_reader': report['pdf'], 'evidence': evidence,
            'next_action': 'Record the reviewed expert-evidence addition against the current reader.',
        })
        transition('reopen', identifier, folder/'reopen.json')
        state = core.read(ROOT, core.STATE)
        graph, _, _ = run.combined(ROOT, state)
        node = run.ledger.operation(graph, identifier)
        attempt = len(state['execution_runtime']['review_history'][identifier])
        output = ROOT/run.review_output_paths(node, state['reader'], attempt)[0]
        limits = list(dict.fromkeys(old['limitations']+LIMITS))
        scope = 'Author exact-reader delta review; proposal evidence only'
        write(output, {
            'operation': identifier, 'status': 'pass', 'criterion': node['criteria'][0],
            'reviewer': work.REVIEWER, 'reviewed_reader': report['pdf'],
            'review_attempt': attempt, 'acceptance_scope': 'proposal_only',
            'scope': scope, 'findings': [finding], 'evidence': evidence,
            'limitations': limits, 'visual_acceptance': False,
        })
        receipt = run.ledger.receipt_template(node)
        receipt.update(
            outcome='pass', execution='performed', scope=scope, reviewer=work.REVIEWER,
            limitations=limits, reviewed_reader=report['pdf'], review_attempt=attempt,
            acceptance_scope='proposal_only', outputs=[ref(output, 'Current-reader '+q+' author review')],
            nonexecution_reason='', revisit_trigger='',
            criteria=[{'index': 0, 'verdict': 'pass', 'finding': finding, 'evidence': evidence}],
        )
        write(folder/'operation-receipt.json', receipt)
        transition('record', identifier, folder/'operation-receipt.json')
    print(json.dumps({'exact_reader_reviews': 'Q2-Q4 pass', 'proposal_accepted': False}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['review', 'publish', 'renew'])
    args = parser.parse_args()
    {'review': review, 'publish': publish, 'renew': renew}[args.command]()

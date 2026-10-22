#!/usr/bin/env python3
"""Record a bounded two-source census review and conserve the prior register."""
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path

import context_conflict_reference_20261023 as exact
from publish_latent_r_review_v2_20261013 import ROOT, ref, verify_bindings, write

BASE = ROOT / 'docs/program/execution/2026-10-23/census-context-conflict-v1'
PRIOR = ROOT / 'docs/program/execution/2026-10-22/census-factuality-weighted-v1'
RAW = ROOT / 'docs/literature/raw'
PAPERS = ROOT / 'docs/papers'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def receipt(name):
    return json.loads((RAW / (name + '.receipt.json')).read_text())


def source_record(spec):
    raw_pdf = RAW / (spec['raw'] + '.pdf')
    rec = receipt(spec['raw'])
    assert rec['status'] == 'saved' and rec['http_status'] == 200
    assert digest(raw_pdf) == rec['sha256']
    paper = PAPERS / spec['filename']
    assert not paper.exists()
    paper.write_bytes(raw_pdf.read_bytes())
    assert digest(paper) == rec['sha256']
    identity_receipt = receipt(spec['identity'])
    page_refs = []
    for page, finding in spec['anchors'].items():
        text_path = BASE / f"{spec['short']}-page-{page:03}.txt"
        assert text_path.is_file()
        page_refs.append(dict(anchor=f"PDF physical page {page}", finding=finding,
                              extracted_text=ref(text_path, 'Extracted primary text; page pixels not visually reviewed')))
    return dict(
        integrated_citation_key=spec['key'], kind='paper', title=spec['title'],
        authors=spec['authors'], first_author=spec['surname'], year=spec['year'],
        source_identity=rec['url'], version_date=spec['version_date'],
        cutoff='2026-10-07', local_path=str(paper.relative_to(ROOT)),
        sha256=rec['sha256'], bytes=paper.stat().st_size,
        local_copy=ref(paper, 'Genuine selected pre-cutoff PDF under required scholarly filename'),
        inspected_anchors=page_refs, supported_claims=spec['claims'],
        limitations=spec['limitations'], identity_qualifications=spec['identity_qualifications'],
        identity_evidence=[
            ref(RAW / (spec['raw'] + '.receipt.json'), 'Successful selected-edition acquisition receipt'),
            ref(RAW / (spec['identity'] + '.xml'), 'Archive identity metadata; not a substitute for selected PDF bytes'),
            ref(BASE / f"{spec['short']}-pdfinfo.txt", 'Observed PDF metadata')],
        acquisition_note='Acquired 23 October 2026; edition date is retained separately from acquisition date.',
        archive_latest_note=spec['archive_latest_note'])


def main():
    specs = [
        dict(short='context', raw='exec23_context_v1', identity='exec23_context_identity',
             key='exec23_contextual_causality_survey', surname='Zhao', year=2026,
             title='Contextual Causality with Large Language Models: A Survey',
             filename='Contextual Causality with Large Language Models A Survey Zhao(2026).pdf',
             authors='Yiheng Zhao, Jun Yan and Chengming Hu',
             version_date='arXiv 2609.22409v1, printed 18 September 2026; acquired 23 October 2026',
             archive_latest_note='Atom identity is v1 and pre-cutoff; selected PDF is v1.',
             anchors={1: 'Abstract states the survey scope and distinguishes contextual from non-contextual causality.',
                      2: 'Introduction distinguishes semantic, intervention and counterfactual contextual causality and reports scope against other surveys.',
                      3: 'Taxonomy defines semantic tasks and says textual intervention differs from manipulating a data-generating process.',
                      4: 'Surveyed evaluations report hallucination, short-context and complex-structure limitations; cited studies are not independently qualified here.',
                      5: 'Benchmark construction and agent-trace discussion; cost and coverage limits remain.',
                      6: 'Training-free and training-based methods depend on model/task and knowledge-source coverage; limitations are survey claims.',
                      7: 'Table 3 lists representative benchmarks, predominantly intrinsic and based on news, Wikipedia, stories, human or agent traces.',
                      8: 'Survey calls for real-world and extrinsic evaluation, finer process evaluation, and long-horizon agent evidence.',
                      9: 'Survey limits itself to text-only contextual causality and says it does not extend causal theory.'},
             claims=[
                 'The taxonomy separates semantic, textual intervention and counterfactual contextual tasks; it is a survey framework, not a new identification theory.',
                 'The paper explicitly says textual intervention differs from manipulating the underlying data-generating process.',
                 'Its benchmark review reports a gap between intrinsic answer evaluation and extrinsic decision quality, with many sources drawn from news, Wikipedia, stories, human questions and agent traces.',
                 'The authors identify short/simple contexts, final-answer scoring, limited intervention/counterfactual coverage, misleading evidence and long-horizon gaps as limitations or future needs.',
                 'The paper states its scope is text-only and that the taxonomy primarily organizes classical causal concepts rather than extending causal theory.'],
             limitations='Survey synthesis only. Referenced methods, packages, benchmarks and empirical results remain unqualified unless separately acquired. No bank data, live model, causal graph or intervention was executed.'),
        dict(short='conflict', raw='exec23_conflict_v1', identity='exec23_conflict_identity',
             key='exec23_cross_modality_conflict', surname='Zhu', year=2024,
             title='Unraveling Cross-Modality Knowledge Conflicts in Large Vision-Language Models',
             filename='Unraveling Cross-Modality Knowledge Conflicts in Large Vision-Language Models Zhu(2024).pdf',
             authors='Tinghui Zhu, Qin Liu, Fei Wang, Zhengzhong Tu and Muhao Chen',
             version_date='arXiv 2410.03659v1, printed 4 October 2024; acquired 23 October 2026',
             archive_latest_note='Atom identity reports v2 updated 11 October 2024; selected PDF is explicitly v1. Claims and hashes bind v1, not the later revision.',
             anchors={1: 'Abstract and introduction define cross-modality parametric knowledge conflict as inconsistent visual and language representations.',
                      4: 'Defines recognized-set accuracy, flip rate and the proposed CR >= FR - DeltaAcc statistic.',
                      6: 'Reports Table 2 results and attributes a persistent conflict rate; attribution remains the authors’ interpretation.',
                      7: 'Confidence strategies do not reliably select correctness; contrastive metric and its interpretation are described.',
                      9: 'Table 4 reports DCD cells and the paper claims universal improvement; one displayed cell is a tie.',
                      10: 'Table 5 contains displayed baseline/value/delta combinations; four ViQuAE deltas do not match subtraction.',
                      11: 'Conclusion and reproducibility pointers; code/data/runtime were not acquired or executed.',
                      17: 'Appendix records prompt and disturbance details, including ten samples for prompt/dropout confidence analysis.'},
             claims=[
                 'The paper operationalizes multimodal conflict through differing text/image answers and recognized-set accuracy and flip rate.',
                 'CR >= FR - DeltaAcc is a paper-proposed lower bound under its attribution assumptions; observed prediction disagreement alone does not identify latent stored-knowledge conflict.',
                 'The paper reports that token confidence, confidence shifts and minimum-variance strategies did not reliably select the correct answer in its tested setup.',
                 'Table 4 reports DCD gains for selected cells, but the displayed InstructBlip-7b InfoSeek accuracy is a tie and the universal-improvement wording is therefore too broad as printed.',
                 'Four selected Table 5 ViQuAE deltas are arithmetically inconsistent with the displayed baseline and value; the discrepancy is preserved rather than corrected.',
                 'The selected v1 PDF is pre-cutoff; archive metadata latest is v2, and no code, data, license, runtime or reproduction was qualified.'],
             limitations='Selected v1 primary text only. The later archive revision, repository, code/data and supplementary licensing/runtime were not authenticated or executed. Reported gains are author-reported and not bank causal evidence.')]
    assert not (BASE / 'source-audit.json').exists()
    sources = [source_record(s) for s in specs]
    results = exact.calculate()
    write(BASE / 'exact-results.json', results)
    audit = dict(cutoff='2026-10-07', visual_acceptance=False,
                 sources=sources,
                 audit_scope='Two selected pre-cutoff originals; primary text and extracted tables reviewed, figures not visually reviewed.',
                 nonclaims=['No capability, causal truth, bank benefit, adoption, live-model superiority or package integration follows from this review.'])
    write(BASE / 'source-audit.json', audit)
    write(BASE / 'primary-review.json', dict(status='pass_for_bounded_primary_text_review', coverage_acceptance=False,
        visual_acceptance=False, native_execution=False,
        evidence=[ref(BASE / 'source-audit.json', 'Two-source traceable audit'),
                  ref(BASE / 'exact-results.json', 'Authored exact diagnostics and preserved arithmetic checks')],
        findings=[c for s in sources for c in s['supported_claims']],
        limitations=[s['limitations'] for s in sources]))
    write(BASE / 'omissions-register.json', dict(items=[
        dict(id='contextual-causality-cited-originals', next_action='Acquire and inspect cited benchmark and method originals before using their reported results as independent evidence.'),
        dict(id='cross-modality-reproduction', next_action='Acquire the repository at the selected v1-compatible revision, inspect license/data/runtime and reproduce Table 4/5 with frozen inputs; preserve discrepancies.'),
        dict(id='causal-truth-qualification', next_action='Use public known-law or independently adjudicated evidence to separate text support, answer correctness, causal identification and decision value.'),
        dict(id='census', next_action='Inspect the remaining 50 unread originals and four crosscutting searches; this two-source unit does not close census coverage.'),
        dict(id='visual', next_action='Use a fresh image allowance to inspect source figures and later rendered manuscript additions; text review does not grant visual acceptance.')],
        global_blocker=None, no_source_waivers=True))
    old = json.loads((PRIOR / 'census-register.json').read_text())
    new = copy.deepcopy(old)
    changed = {'LA01-candidate-126': sources[0], 'LA01-candidate-285': sources[1]}
    for candidate_id, source in changed.items():
        row = next(x for x in new['items'] if x['id'] == candidate_id)
        assert row['disposition'] == 'open_original_not_inspected'
        row.update(prior_disposition='open_original_not_inspected',
                   disposition='inspected_primary_retained_with_limits',
                   technical_source_review_open=False, source_key=source['integrated_citation_key'],
                   primary_source_record=source,
                   later_primary_review=ref(BASE / 'primary-review.json', 'Selected original primary-text review'),
                   task_families=['expert_evidence', 'evaluation_cost'],
                   mapping_basis='Inspected definitions, methods/evaluations and limits; not a title-only causal-method classification.',
                   availability='Authentic selected pre-cutoff PDF acquired; later editions and cited originals remain separate qualifications.',
                   effect_on_claims='Adds bounded evidence and explicit limitations; does not close LLM coverage or establish causal validity, native method or bank qualification.',
                   next_action=('Acquire cited originals and independent reproduction inputs; preserve survey and author-reported claims as qualified.' if candidate_id.endswith('126')
                                else 'Acquire the repository and v1-compatible code/data/license/runtime, reproduce selected tables, and preserve arithmetic discrepancies.'))
    assert len(new['items']) == len(old['items']) == 117
    for before, after in zip(old['items'], new['items']):
        if before['id'] not in changed:
            assert before == after
    counts = Counter(x['disposition'] for x in new['items'])
    assert counts['inspected_primary_retained_with_limits'] == 63
    assert counts['open_original_not_inspected'] == 50
    new.update(status='successor_bounded_review', counts=dict(counts),
               supersedes=ref(PRIOR / 'census-register.json', 'Preserved 61 inspected / 52 unread register'),
               changes=['Only LA01-candidate-126 and LA01-candidate-285 changed; all other 115 rows are byte/deep-equal.'],
               evidence=[ref(BASE / 'primary-review.json', 'Two actual selected-original reviews')], closure=False,
               interpretation='63/113 originals inspected; 50 unread; four crosscutting searches remain.')
    write(BASE / 'census-register.json', new)
    task_map = copy.deepcopy(json.loads((PRIOR / 'task-map.json').read_text()))
    assert len(task_map['task_families']) == 14
    for family in task_map['task_families']:
        family['coverage_acceptance'] = False
        for candidate_id, source in changed.items():
            if candidate_id in family.get('uninspected_candidate_ids', []):
                family['uninspected_candidate_ids'].remove(candidate_id)
            if family['id'] in ['expert_evidence', 'evaluation_cost']:
                if candidate_id not in family.setdefault('inspected_candidate_ids', []):
                    family['inspected_candidate_ids'].append(candidate_id)
                if source['integrated_citation_key'] not in family.setdefault('inspected_source_keys', []):
                    family['inspected_source_keys'].append(source['integrated_citation_key'])
    task_map.update(register=ref(BASE / 'census-register.json', '63 inspected / 50 unread census'),
                    supersedes=ref(PRIOR / 'task-map.json', 'Preserved fourteen-family map'))
    write(BASE / 'task-map.json', task_map)
    write(BASE / 'reconciliation-review.json', dict(status='pass', changed_ids=sorted(changed), unchanged_other_records=115,
        original_candidates=113, inspected=63, unread=50, task_families=14,
        evidence=[ref(BASE / 'census-register.json', 'Conserved 117 rows'), ref(BASE / 'task-map.json', 'Conserved fourteen task families')]))
    write(BASE / 'inspection-progress.json', dict(
        finding='Two authentic pre-cutoff originals were inspected. The contextual-causality survey establishes a textual-versus-data-generating-process boundary and benchmark limitations. The multimodal conflict paper supplies a qualified conflict statistic and preserved Table 4/5 contradictions. Exact authored twins show that identical observations can support 90 versus -10 USD incremental contact net under two compatible causal laws.',
        next_action='Integrate these qualified findings into the next paired release; inspect the remaining 50 originals and four crosscutting searches. Continue independent commercial computation/workflow, reuse and Python IV/RD work; Python fit/covariance kernels are acquired and inspected, while RD/CausalPy IV and numerical guards remain open.',
        evidence=[ref(BASE / n, 'Bounded census continuation') for n in ['source-audit.json', 'primary-review.json', 'exact-results.json', 'census-register.json', 'task-map.json', 'omissions-register.json']],
        coverage_acceptance=False, global_blocker=None, yield_reason='Two-source review is complete and preserved; yield for editorial integration without closing census coverage or pausing independent lanes.'))
    verify_bindings(audit)
    verify_bindings(json.loads((BASE / 'inspection-progress.json').read_text()))
    print(json.dumps(dict(status='pass_for_bounded_review', inspected=63, unread=50, rows=117,
                          added_papers=[str((PAPERS / s['filename']).relative_to(ROOT)) for s in specs],
                          exact_reference=str((BASE / 'exact-results.json').relative_to(ROOT)))))


if __name__ == '__main__':
    main()

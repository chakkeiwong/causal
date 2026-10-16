#!/usr/bin/env python3
"""Prepare discovery synthesis using preserved primary evidence and exact examples."""
import json
from pathlib import Path
import re
import s2_examples_20261016 as examples
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT, BASE = examples.ROOT, examples.BASE
PRIOR = ROOT / 'docs/program/execution/2026-10-16/semantic-parity/publication/reader/source-audit.json'
CHAPTER = ROOT / 'docs/program/comprehensive-v14/work/TEXT.DRAFT.S2/chapter.tex'
OP = 'TEXT.DRAFT.S2'
REVIEWER = {'name': 'Codex author/coordinator', 'kind': 'author'}
LIMITS = ['Bounded topic synthesis, not a complete software census or qualification of every candidate.',
          'Exact examples use authored structural laws and stipulated prices/model weights; no bank data, upstream benchmark or ROI claim.',
          'General graph/effect-set calibration, dependent latent regimes and actual platform/consumer acceptance remain separate work.',
          'Source-specific rights, environment and unresolved original-source conditions remain in the preserved comparisons.',
          'Rendered visual acceptance remains open; inherited six-image allowance exhausted.']


def main():
    assert not CHAPTER.exists()
    text = (BASE / 'chapter.template').read_text().replace('§', chr(92))
    assert ',+' not in text and not re.search(r'\S\\citep\{', text)
    assert examples.calculate() == json.loads((BASE / 'exact-results.json').read_text())
    prior = json.loads(PRIOR.read_text()); verify_bindings(prior)
    index = {s['integrated_citation_key']: s for s in prior['sources']}
    cited = {k.strip() for g in re.findall(r'\\citep\{([^}]+)\}', text) for k in g.split(',')}
    inherited = cited - {'exec16_s2_exact', 'exec16_s2_design'}
    assert inherited <= index.keys()
    papers = []
    for key, pages, claims in [
        ('exec13_latentr_colombo2012', [9, 15], ['RFCI adjacency is weaker than FCI adjacency; can represent multiple equivalence classes.', 'Theorem 3.2 requires faithful underlying DAG and oracle conditional-independence information.']),
        ('exec13_latentr_colombo2014', [18, 19], ['Stable skeleton, collider decisions and orientation invariance are distinct modifications; RFCI has later-stage differences.']),
        ('exec14_pt_paper_gies', [5, 6], ['Known targets, independent but nonidentical regime observations, conservative family and unchanged nonintervened mechanisms.']),
        ('zhang2008', [4, 5], ['Ancestral graph definitions, endpoint marks and absence of directed/almost-directed cycles; inherited PAG/effect distinctions retained.']),
    ]:
        s = index[key]
        assert examples.ROOT.joinpath(s['local_path']).is_file()
        papers.append({'citation_key': key, 'original': {'path': s['local_path'], 'sha256': s['sha256'], 'anchor': 'Genuine primary PDF'},
                       'inspected_pages': [ref(BASE / 'inspected' / (key + '-' + str(p) + '.txt'), 'Physical PDF page ' + str(p)) for p in pages],
                       'supported_claims': claims, 'version_date': s.get('version_date', s.get('version_status'))})
    rereads = []
    for name, first, last, claim in [
        ('exec14_pt_file_tigramite_1.txt', 15, 40, 'Method and CI-test assumption table distinguishes temporal object and test.'),
        ('v12_exec13_java_tetrad_sembic.txt', 50, 66, 'Gaussian BIC sums IID record likelihoods; not a general panel score guarantee.'),
        ('v12_gap3_lingam_technical.txt', 12, 55, 'DirectLiNGAM linear non-Gaussian scope, prior-knowledge path conventions and pruning option.'),
        ('v12_sw2_source_causallearn_pc.txt', 78, 116, 'Stable skeleton, collider priorities and PC bidirected conflict representation.'),
    ]:
        p = ROOT / 'docs/literature/raw' / name; lines = p.read_text().splitlines()
        rereads.append({'local_copy': ref(p, f'Lines {first}-{last}'), 'inspected_anchors': [claim], 'supported_claims': [claim],
                        'excerpt': '\n'.join(lines[first-1:last])})
    primary = {'status': 'pass_for_synthesis', 'reviewer': REVIEWER, 'cutoff': '2026-10-07',
        'new_primary_rereads': papers, 'new_software_rereads': rereads,
        'inherited_source_records': [index[k] for k in sorted(inherited)],
        'scope': 'Four genuine papers reread at eight saved pages and four pinned source excerpts. Remaining claims synthesize retained, inspected original-source audits; no claim all software was freshly rerun or reinspected.',
        'evidence': [ref(PRIOR, 'Preserved original identities and technical anchors'), ref(Path(__file__), 'Synthesis preparation'), ref(ROOT / 'tools/s2_examples_20261016.py', 'Separate exact reference')],
        'limitations': LIMITS}
    write(BASE / 'primary-review.json', primary)
    design = {'status': 'proposed_not_executed', 'scope': 'Public/generated discovery and decision comparison before costly bank experiments',
        'profiles': [
            {'topic': 'IID sufficient', 'candidates': ['pcalg PC/GES paths', 'Tetrad PC/FGES', 'causal-learn PC'],
             'admission': 'Declared independent units, graph assumptions and appropriate CI test or score', 'outputs': 'CPDAG or declared candidate plus test/score/search settings'},
            {'topic': 'Functional', 'candidates': ['LiNGAM', 'NOTEARS', 'DAGMA', 'Causica'],
             'admission': 'Distinct functional/noise/density assumptions and numerical acceptance', 'outputs': 'Candidate or model with raw/thresholded weights, constraints and diagnostics'},
            {'topic': 'Latent and selected', 'candidates': ['pcalg FCI/RFCI', 'Tetrad/causal-learn latent paths', 'inspected native methods'],
             'admission': 'Selection and hidden-variable graph class, method-specific oracle/sample premises', 'outputs': 'Exact endpoint object with weaker RFCI interpretation where applicable'},
            {'topic': 'Temporal', 'candidates': ['Tigramite method/test combinations', 'CausalAI', 'VARLiNGAM', 'DYNOTEARS', 'supplied dynamic-network reference'],
             'admission': 'Physical lag, subjects, masks, availability clock, horizon and sampling law', 'outputs': 'Declared temporal graph or supplied-model result; no automatic effect calibration'},
            {'topic': 'Interventional', 'candidates': ['R/native and Python GIES', 'UTIGSP-related method as a distinct profile'],
             'admission': 'Known/unknown targets and mechanism semantics admitted separately; unchanged mechanisms and sampling premises', 'outputs': 'Interventional graph class/target conclusions under exact method assumptions'},
        ],
        'fixed_examples': ref(BASE / 'exact-results.json', 'Cancellation, equivalent chains, selection and horizon/decision references'),
        'matched_comparison': 'Same admitted observation experiment and target for comparable methods; explicit extra assumptions for alternatives.',
        'diagnostics': ['Permutation/label and endpoint preservation', 'CI failure/rank/conditioning bounds', 'Raw graph versus postprocessing',
                        'Regime masks and unknown target refusal', 'Subject boundaries and physical time', 'Target effect and conditional decision loss'],
        'rights_and_costs': 'Retain package-specific adoption/bridge/port/reference/rejection choices; include preparation, runtime, diagnosis, review and maintenance.',
        'public_data_role': 'Permitted public covariates/calendars can inform generated examples; they do not supply unobserved intervention truth.',
        'known_next_routes': ['Implement one admitted generated comparison per profile after environment/rights closure.',
                              'Acquire and inspect remaining original-source candidates without blocking ready profiles.',
                              'Compare finite-sample graph retention and effect/decision consequences under a frozen fresh protocol.'],
        'unknown_or_external': ['No general guarantee for arbitrary nonlinear/latent/dependent families.',
                                'Bank assignment truth, feasible interventions, precision/loss and actual costs require later owners.'],
        'inherited_omissions': [ref(ROOT / p, 'Source-specific coverage and unresolved candidates') for p in [
            'docs/program/execution/2026-10-16/cxx-temporal/omissions-register.json',
            'docs/program/execution/2026-10-16/cxx-temporal/author-review.json',
            'docs/program/execution/2026-10-14/python-temporal/v3/release-source-review.json'] if (ROOT / p).is_file()],
        'whole_census_closed': False, 'bank_qualified': False}
    write(BASE / 'discovery-design.json', design)
    CHAPTER.parent.mkdir(parents=True, exist_ok=False); CHAPTER.write_text(text)
    source_rows = []
    for suffix, title, kind, path, claims, records in [
        ('exact', 'Exact discovery equivalence, intervention information and banking decision references', 'project_derivation', BASE / 'exact-results.json',
         ['Three Gaussian chains/fork share covariance but imply effect set {0,1}; exact intervention response table.',
          'Stipulated payoffs 22/-8, expected values 2,22/3,14/3 and information gains16/3,8/3; maximin versus regret.',
          'Cancellation, selected-population contrast and horizon sign reversal are exact generated examples.'],
         [ref(ROOT / 'tools/s2_examples_20261016.py', 'Rational matrix algebra, path enumeration and decision grouping')]),
        ('design', 'A proposed discovery portfolio by observation experiment and decision target', 'project_design', BASE / 'discovery-design.json',
         ['Scoped IID, functional, latent, temporal and interventional comparisons retain distinct assumptions and failures.',
          'Public/generated comparison, source-specific remaining candidates, rights and later bank inputs.'],
         [ref(BASE / 'primary-review.json', 'Inspected primary evidence and inherited source-specific limits'), ref(BASE / 'plan.md', 'Reviewed synthesis plan')]),
    ]:
        source_rows.append({'integrated_citation_key': 'exec16_s2_' + suffix, 'title': title, 'author': 'Causal banking proposal',
            'kind': kind, 'year': 2026, 'source_identity': 'Project-authored derivations and proposed comparison', 'version_date': '2026-10-16',
            'local_copy': ref(path, title), 'inspected_anchors': claims, 'supported_claims': claims, 'records': records, 'limitations': LIMITS})
    write(BASE / 'source-audit.json', {'sources': source_rows, 'prior': ref(PRIOR, '658 retained source records'), 'cutoff': '2026-10-07'})
    write(BASE / 'draft-author-review.json', {'status': 'pass_for_draft_integration', 'reviewer': REVIEWER,
        'criteria_verdicts': ['pass', 'pass'], 'findings': ['Connected observation-to-discovery-to-decision argument develops notation, hypotheses, alternatives, diagnostics and exact banking consequences.',
            'Twenty-nine inherited citation keys, four primary-paper rereads, four software excerpts and two project additions support the claims. Examples are reproducible authored laws; no new package or bank execution is invented.'],
        'evidence': [ref(p, p.name) for p in [CHAPTER, BASE / 'primary-review.json', BASE / 'exact-results.json', BASE / 'discovery-design.json', BASE / 'source-audit.json', BASE / 'plan.md']],
        'preparation_repair': ref(BASE / 'preparation-repair.json', 'Preserved legacy metadata and dependent-preparation failure'),
        'prior_draft_corrections': ['Removed four accidental comma-plus text joins before integration.', 'Separated noise variance vectors from model display to avoid excessive line width.'],
        'depth_status': 'To be measured in compiled reader across explicitly distributed S2 development; no automatic credit from physical span.',
        'limitations': LIMITS, 'visual_acceptance': False, 'whole_census_closed': False})
    print(json.dumps({'draft_prepared': str(CHAPTER.relative_to(ROOT)), 'inherited_citation_keys': len(inherited), 'new_citations': 2, 'exact_examples': 'pass'}))


if __name__ == '__main__': main()

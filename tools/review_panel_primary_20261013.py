#!/usr/bin/env python3
"""Record a bounded author review of panel and sensitivity primary papers."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-13/traceability'
INDEX = ROOT / 'docs/program/execution/2026-10-13/identification-review/traceability-review.json'

# Page numbers are PDF-page positions in text extracted from the genuine saved
# PDFs; printed page numbers are retained in findings where they matter.
REVIEWS = {
    'panelreview2024': ([8, 9, 13], 'The source distinguishes classical panel exogeneity/dynamics, fixed/random effects and nonlinear incidental parameters from modern heterogeneous-effect designs. Reader uses it for those organizing distinctions and flags that calendar time is generally not an exchangeable panel coordinate.'),
    'arellano1991': ([3, 4, 5, 6], 'The 1991 published source explicitly assumes independent short individual time series, no serial correlation in level innovations, and distinguishes predetermined from strictly exogenous instruments. Reader derives lag restrictions and does not treat a nonrejected AR(2) or overidentification test as proof of bank assignment validity.'),
    'blundellbond2023': ([4, 5, 6, 7], 'The 2023 account derives the extra level moments from an initial deviation uncorrelated with the unit effect; mean stationarity does not impose variance stationarity. It also describes weak differenced instruments and the Windmeijer finite-sample correction. Reader labels its own first-order sandwich and 2023-versus-1998 provenance correctly.'),
    'callaway2021': ([8, 9, 11, 12], 'Theorem 1 distinguishes never-treated and not-yet-treated comparisons under different trend assumptions and restricts eligible horizons when anticipation is allowed. The reader preserves cohort, baseline, support and aggregation meaning; its normalized influence is identified as a project derivation.'),
    'dechaisemartin2024': ([12, 13, 14], 'Assumptions 1 and 2 concern no anticipation and status-quo parallel trends among groups sharing the initial treatment; the source defines actual-versus-status-quo effects only while controls remain. Reader limits its switching-action alternative accordingly.'),
    'abadie2010': ([3, 4, 5], 'Published Section 2.2 uses convex donor weights, a latent factor law and preperiod-rank/approximation restrictions; close fit alone is not unconditional identification. Reader states a noiseless project balance identity and warns about donor contamination and support.'),
    'abadie2021': ([15, 17, 18, 19], 'The review discusses donor support, overfit and placebo comparisons; it says exact randomization inference needs actual random assignment, unusual for aggregate observational cases. Reader reserves its exact rank test for a stipulated uniform randomized regional pilot.'),
    'benmichael2021': ([1, 6, 7], 'The archived manuscript explicitly augments simplex synthetic-control weights with an outcome-model correction when prefit is poor. Reader calls this a model-dependent alternative, not a cure that preserves original interpolation assumptions.'),
    'synthdid2021': ([3], 'The primary paper combines unit and time weights and states that its main analysis uses a treatment block; staggered adaptation appears separately. Reader does not infer direct staggered support from the block package interface.'),
    'conformal2022': ([18, 19, 21, 22, 47], 'Theorem 1 requires null-imposed prediction accuracy with fixed postperiod length and stationary mixing shocks; Theorem 2 uses estimator stability and exponentially mixing data. Appendix D.1 gives exact permutation validity only under exchangeability and permutation-invariant fitting. Reader keeps these regimes distinct from arbitrary bank residual permutations.'),
    'paneldml2024': ([1, 6, 7, 14, 15], 'The 2024 paper compares early/late demeaning, unit dummies and correlated random effects primarily by point-estimator simulation; early demeaning requires additive separability that fails for generic nonlinear nuisances. Reader supplies its own quadratic counterexample and does not claim a general dependent-data confidence theorem.'),
    'rambachan2023': ([8, 9, 10, 11], 'Published Lemma 2.1 obtains an identified set by optimizing trend violations under declared restrictions; relative-magnitude and second-difference bounds differ. Section 2.5 separates a finite normal experiment from asymptotic approximation. Reader projection and its confidence-set caveat match these distinctions.'),
    'cluster2021': ([10, 11, 13], 'Assumptions 1–3 require separate exchangeability, dissociation, score regularity and nuisance rates; Theorems 1–2 address their array sampling law. Reader explicitly refuses to apply that theorem to ordered serial banking calendars merely because two cluster labels exist.'),
    'kleibergen2021': ([1, 10, 11], 'The preserved preprint defines the population continuous-updating criterion and its pseudo-true minimizer under misspecification, with joint moment/Jacobian CLT and covariance convergence. Reader treats it as an inferential challenger, not proof that the pseudo-true value remains a causal bank response.'),
}


def ref(path, anchor):
    return {'path': str(path.relative_to(ROOT)),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'anchor': anchor}


def main():
    prior_path = BASE / 'semantic-review-08.json'
    prior = json.loads(prior_path.read_text())
    index = json.loads(INDEX.read_text())
    reader = prior['reader']
    assert hashlib.sha256((ROOT / reader['path']).read_bytes()).hexdigest() == reader['sha256']
    indexed = {r['citation_key']: r for r in index['records']}
    records = []
    for key, (pages, finding) in REVIEWS.items():
        assert key in prior['remaining_source_keys']
        entry = indexed[key]
        assert entry['kind'] == 'paper'
        assert len(entry['local_copies']) == 1
        pdf = ROOT / entry['local_copies'][0]['path']
        assert hashlib.sha256(pdf.read_bytes()).hexdigest() == entry['local_copies'][0]['sha256']
        extracted = BASE / 'primary-09' / (key + '.txt')
        text = extracted.read_text()
        assert max(pages) <= len(text.split('\f')) - 1
        records.append({'citation_key': key, 'verdict': 'pass_in_stated_scope',
                        'finding': finding,
                        'primary_source': dict(ref(pdf, 'Genuine saved scholarly PDF'), inspected_pdf_pages=pages),
                        'extracted_text': ref(extracted, 'Text extracted locally from the hash-bound PDF for this author review'),
                        'version_date': entry['version_date'],
                        'contexts_reviewed': entry['citation_contexts'],
                        'limits': 'Author source/claim review; source theorem premises are not thereby verified for bank data or every implemented path.'})
    reviewed = sorted(set(prior['reviewed_source_key_list']) | set(REVIEWS))
    remaining = sorted(set(indexed) - set(reviewed))
    next_action = ('Continue exact-reader Q2 with remaining HMM, state-space, controlled identification and OPE papers; then theorem, LLM, commercial, public-data and software sources. Preserve source-specific negative findings. Resume from semantic-review-09.json.')
    result = {'status': 'partial_semantic_review_not_Q2_acceptance',
              'reviewer': {'name': 'Codex author/coordinator', 'kind': 'author'},
              'reader': reader, 'structural_review': ref(INDEX, 'Exact current reader source/context index'),
              'prior_review': ref(prior_path, 'Prior 117 reviewed source records'),
              'prior_review_continuity': 'Same exact reader hash; prior source/context findings retained by hash.',
              'review_procedure': ref(Path(__file__).resolve(), 'Explicit author findings and PDF-page anchors'),
              'records': records, 'cumulative_reviewed_source_keys': len(reviewed),
              'reviewed_source_key_list': reviewed, 'remaining_source_keys': remaining,
              'next_action': next_action, 'proposal_q2_acceptance': False}
    output = BASE / 'semantic-review-09.json'
    with output.open('x') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
        f.write('\n')
    checkpoint = {'finding': f'Reviewed {len(records)} panel, DiD, synthetic-control, sensitivity and dependence scholarly PDFs on the exact 626-page reader. {len(reviewed)}/{len(indexed)} source keys reviewed; {len(remaining)} remain. No bank-theorem premise or whole Q2 acceptance awarded.',
                  'next_action': next_action,
                  'evidence': [ref(output, 'Fourteen primary scholarly PDF/context dispositions and cumulative coverage')]}
    with (BASE / 'checkpoint-08.json').open('x') as f:
        json.dump(checkpoint, f, indent=2)
        f.write('\n')
    print(json.dumps({'reviewed_now': len(records), 'cumulative': len(reviewed),
                      'remaining': len(remaining), 'whole_q2_accepted': False}))


if __name__ == '__main__':
    main()

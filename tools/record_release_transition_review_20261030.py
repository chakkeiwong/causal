"""Record the actual bounded final-transition reading without widening prior reviews."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/release/2026-10-29'
OUT = BASE / 'transition-review-091'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def bind(path):
    return dict(path=str(path.relative_to(ROOT)), sha256=sha(path))


def main():
    build = read(BASE / 'latest-build.json')
    audit = read(BASE / 'deletion-audit.json')
    assert build['batch'] == 85 and audit['status'] == 'pass'
    assert len(read(BASE / 'edits.json')) == 290
    assert audit['ledger_sha256'] == build['ledger_sha256'] == sha(BASE / 'edits.json')
    for row in audit['publication'].values():
        assert sha(ROOT / row['path']) == row['sha256']
    assert not OUT.exists()
    OUT.mkdir()
    chapters = {1, 2, 3, 4, 5, 13, 14, 15, 16, 19, 22, 23, 24, 25,
                28, 29, 31, 32, 33, 41}
    contexts = []
    for row in read(BASE / 'context-review-290/manifest.json')['chapters']:
        if row['chapter'] not in chapters:
            continue
        assert sha(ROOT / row['extract']) == row['sha256']
        for name, digest in row['source_bindings'].items():
            assert sha(ROOT / name) == digest
        contexts.append({k: row[k] for k in ['chapter', 'title', 'extract',
                                            'sha256', 'lines', 'source_bindings']})
    assert len(contexts) == 20
    observations = [
        'Chapters1–5,19,23 and24 were read completely immediately before the context handoff. Chapter25 lines1–240 were read there; lines241–508 were read after it, completing that context. Chapters13–16,22,28–29,31–33 and41 were read completely after the handoff. These20 source contexts are additional to the15 in standard-review090. No new full rendered-page reading or whole-book reread is claimed.',
        'The opening offer example distinguishes assignment, delivery and acceptance. Automatic repricing is an explicit assumption for its expense equation. Four-cell normal intervals condition on observed counts, retain fixed accounting inputs and do not claim a new raw-data MCP endpoint. Servicing rewards already contain the action cost, preventing its second subtraction.',
        'Policy selection uses a finite policy class, independent training and evaluation, and an explicit nuisance-product requirement. Stopping and filtration conditions remain attached to confidence sequences. Transport distinguishes selection diagrams from sample membership and keeps source/target uncertainty, support and measurement shift explicit. Sensitivity calculations retain signed projection identities and confidence-region unions.',
        'Chapter13 retains the initial-customer denominator, reward-specific prefix weights and the distinction between future-dependent dropout and an omitted transition predictor. Chapter14 holds the separately selected policy fixed during evaluation resampling; it does not substitute the performance of a future retraining procedure. Failed coverage and extra pilot cost remain visible.',
        'Recovery in chapter14 requires actual random completion and faithful historical information. The full-score variance identity follows by conditional total variance. The outcome-assisted score telescopes with known action probabilities. Its cross-fitting argument uses a fixed number of folds and L2 convergence to a deterministic score; it is not asserted for arbitrary dependent or learned-probability designs. Equal collection resources are not equal operating costs.',
        'The later binary recovery construction explicitly differs from the unbounded longitudinal reward model. It distinguishes more invitations from a better recovery procedure, derives sharp arm bounds and a conservative whole-set confidence guarantee, retains crossed endpoints and empty sets in denominators, and separates effect positivity from net benefit after the stipulated cost. Outcome drift and nonresponse-mixture sensitivity are different restrictions.',
        'Chapter15 compares within, random, correlated, difference and system routes by restrictions. Initial-condition validity is not supplied by a covariance correction. The misspecified GMM example distinguishes one-step, centered and uncentered pseudo-true targets; the inverse-weight derivative counterexample is bounded to its proof step. Cohort shares and reused controls enter influence uncertainty. The randomized donor proof is separate from observational temporal conformal assumptions.',
        'Chapters16 and22 keep the economic unit and linkage uncertainty distinct from a wider standard error. The linkage budget must bound excluded true candidates and is not learned from fuzzy-match confidence. The support-based population envelope conditions on arm counts and retains assignment relaxation as conservative. No real bank error frequency is inferred.',
        'Chapter25 preserves the bridge-existence and completeness distinction, the prior-almost-sure oracle scope, label-simulation noise, rare target trajectories despite action positivity, and joint-model restrictions behind dynamic bounds. Width/cardinality and local rectangular sets do not automatically establish the required global identification.',
        'Chapters28–29 distinguish projection from population effect, valid sparse-support remedies from unsupported pooling, prediction from intervention and public-data assignment evidence from bank transport. The earnings contrast retains finite-population design qualifications, influential observations, the spending hurdle and the distinction between supplied fitted summaries and a complete raw-data service.',
        'Chapters31–33 and41 follow scientific outputs across interfaces. The declared initial proposal is a matched small offer-study comparison. Native success has the scope of selected operations; unsupported requests and nonidentification are distinct. The source comparisons preserve weights, clocks, truncation, effect type and actual covariance behavior. No fresh software execution is claimed by this reading.',
        'No new consequential mathematical defect or justified deletion was established. The bounded reread supports the stated transitions but cannot certify every theorem, source assertion, prose passage or visual layout. Dense specialist comparisons, repetition and proportionality remain appropriate questions for independent editorial reading; preservation takes priority over unreviewed shortening.'
    ]
    record = dict(recorded_utc=datetime.now(timezone.utc).isoformat(),
        status='complete_in_author_scope', batch=85, ledger=bind(BASE / 'edits.json'),
        publication=audit['publication'], complete_source_contexts=contexts,
        observations=observations, manuscript_edits=[], newly_read_rendered_pages=[],
        prior_standard_review=bind(BASE / 'standard-review-090/contextual-review.json'),
        limitations=['No new primary-source acquisition or native experiment.',
                     'No fresh visual inspection; session allowance is exhausted.',
                     'No independent editorial/scientific acceptance.',
                     'Supplemental20-context review; do not inflate the124-record global index.'])
    save(OUT / 'contextual-review.json', record)
    prose = ['# Final transition challenge: batch085', '',
        'Attributed author reading, 30 October2026. Twenty complete expanded source contexts; no manuscript edits.', '',
        'Chapters: ' + ', '.join(str(n) for n in sorted(chapters)) + '.', '']
    prose.extend(observations)
    prose += ['', 'This supplement leaves the immutable090 assessment and the124-record currency chain unchanged. It adds actual source reading, not independent or rendered/visual acceptance.', '']
    (OUT / 'review.md').write_text('\n\n'.join(prose))
    scope = read(BASE / 'review-scope-current.json')
    for path in [OUT / 'contextual-review.json', OUT / 'review.md'] + [ROOT / r['extract'] for r in contexts]:
        scope['basis'][str(path.relative_to(ROOT))] = sha(path)
    scope['latest_contextual_review'] = str((OUT / 'contextual-review.json').relative_to(ROOT))
    scope['supplemental_transition_review'] = bind(OUT / 'contextual-review.json')
    save(BASE / 'review-scope-current.json', scope)
    with (BASE / 'execution-log.md').open('a') as stream:
        stream.write('\n## Final transition review091\n\n')
        stream.write('Read20 complete expanded source contexts across opening examples, policy evaluation/recovery, panels, linkage, sensitivity, recent methods, public evidence and scientific interface composition. Retained actual reading boundaries across the context handoff. No consequential defect or deletion was established; no manuscript edit was made. The exact source/PDF-bound supplement is transition-review-091/contextual-review.json. Fresh visual and independent acceptance remain open.\n')
    print(json.dumps(dict(status='recorded', contexts=len(contexts), batch=85,
                          manuscript_edits=0, ledger_sha256=sha(BASE / 'edits.json'))))


if __name__ == '__main__':
    main()

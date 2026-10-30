"""Consolidate observed semantic assessments and verify their exact ledger scope."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

R = Path(__file__).resolve().parents[1]
B = R / 'docs/release/2026-10-29'
O = B / 'preservation-review-085'


def read(p):
    return json.loads(p.read_text())


def save(p, value):
    p.write_text(json.dumps(value, indent=2) + '\n')


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def bind(p):
    return dict(path=str(p.relative_to(R)), sha256=sha(p))


def main():
    edits = read(B / 'edits.json')
    audit, build = read(B / 'deletion-audit.json'), read(B / 'latest-build.json')
    assert len(edits) == 237 and audit['status'] == 'pass' and build['batch'] == 82
    assert audit['checks_after_final_edit'] and audit['exact_replay']
    assert not any(audit[k] for k in ['math_removed', 'missing_citation_keys', 'missing_labels', 'distinct_numeric_loss'])
    O.mkdir(exist_ok=False)
    prior_path = B / 'preservation-review-076/semantic-deletion-review.json'
    prior = read(prior_path)
    prefix = (json.dumps(edits[:213], indent=2) + '\n').encode()
    assert hashlib.sha256(prefix).hexdigest() == prior['basis'][0]['sha256']
    (O / 'verified-ledger-prefix-213.json').write_bytes(prefix)
    receipts = [B / folder / 'contextual-review.json' for folder in [
        'prose-review-078', 'funding-review-079', 'projection-review-080',
        'linked-history-review-081', 'master-study-review-082',
        'investment-review-083', 'bibliography-review-084']]
    reviewed = {}
    for p in receipts:
        review = read(p)
        for i in review['edits']:
            assert i not in reviewed
            reviewed[i] = bind(p)
    assert set(reviewed) == set(range(214, 238))
    assessments = {
        214: 'Replaces author-program completion language with institutional evidence, interface and cost requirements. The distinction between research completion and acceptance survives.',
        215: 'Replaces an underspecified scale statement with equal-stratum population weights, the additional averaging half and zero-based primitive indexing. Existing factors, units and variance equations survive.',
        216: 'Corrects a false exact-binomial exclusion statement: the Wilson interval excludes .95, while the exact interval narrowly includes it. The1880/2000 count and adjusted inference remain; a numerical error is corrected, not an adverse finding suppressed.',
        217: 'Restates institutional testing requirements without author-success narration. The required owners and operating observations remain in the same context.',
        218: 'Additive projection derivation retains the complete original coverage-event anchor and all original equations, assumptions and adverse cases.',
        219: 'Additive covariance explanation retains the complete original conditional-rate anchor and gives both width improvement and reversal examples.',
        220: 'Revises newly added rank terminology: determinant zero is matrix rank one. Corner extrema, connected branch images, disconnected union, pairwise sums, convex-hull warning, compatible whole line and incompatible empty image all survive.',
        221: 'Additive augmentation variance identity retains the complete original non-dominance statement; both favourable and adverse conditional examples are stated.',
        222: 'Replaces V10 drafting shorthand with its exact execution section; Wilson guard and interval procedure unchanged.',
        223: 'Replaces V10 shorthand with the pilot section; six-column dictionary, chronological half-split selection and full-pilot refit unchanged.',
        224: 'Replaces V9 shorthand with its innovation-filtration/covariance section; correct action-mean and exogeneity assumptions retained.',
        225: 'Replaces preserved V9 chapter wording with its exact pilot section; no scientific claim removed.',
        226: 'Replaces V10 shorthand with the precision-comparison chapter; disjoint seed statement retained.',
        227: 'Names the pilot and covariance sections for the existing conditional growing-pilot rate and score assumptions; no inference assumption dropped.',
        228: 'Adds common-level retrospective funding comparisons before the intact original failure warning; original mean argument and adverse cases remain.',
        229: 'Adds the critical-level confounding explanation before the intact successor condition; persistent-calendar calibration failure remains.',
        230: 'Adds the same-estimator width/coverage interpretation before the intact direct-weighting anchor; logger and institutional information costs remain.',
        231: 'Adds the expected-volume interpretation between both intact original sentences; conditional chain rule and failed-study costs unchanged.',
        232: 'Replaces first-tranche timing with a broader construction tranche conditional on the initial offer-study comparison. All three workspaces and matched comparator requirements remain.',
        233: 'Removes an unsupported automatic funding inference. The measurement question and useful-answer full-cost account remain; funding requires expected decision improvement to justify cost.',
        234: 'Whitespace-only bibliography changes; every nonspace character retained in order. No source detail removed.',
        235: 'Further whitespace-only bibliography changes; every nonspace character retained. The accidentally separated literal selected17 is restored in236.',
        236: 'Final selected whitespace repairs and selected17 restoration. Every nonspace bibliography character retained in order.',
        237: 'Changes title display to preserve supplied case and adds an attribution comment. Source title text, sorting and all1512 citation labels remain. Removed style code is not scholarly content.'
    }
    dispositions = []
    for i in range(214, 238):
        e = edits[i - 1]
        dispositions.append(dict(edit=i, file=e['file'],
            before_sha256=hashlib.sha256(e['before'].encode()).hexdigest(),
            after_sha256=hashlib.sha256(e['after'].encode()).hexdigest(),
            assessment=assessments[i], observed_context_review=reviewed[i]))
    restored = []
    for i in [212, 213]:
        e = edits[i - 1]
        assert e['after'] in (R / e['file']).read_text()
        restored.append(dict(edit=i, file=e['file'], exact_current_anchor=True,
            scope='Explicit correlation-test obligation' if i == 212 else 'Assignment-evidence and structural-restriction alternatives'))
    record = dict(recorded_utc=datetime.now(timezone.utc).isoformat(), status='complete_in_author_scope',
        batch=82, edits=237, ledger=bind(B / 'edits.json'), publication=audit['publication'],
        predecessor_review=bind(prior_path), predecessor_prefix_verified=213,
        predecessor_screened_edits=211, predecessor_substantive_candidates=80,
        later_reviewed_edits=24, dispositions=dispositions,
        preserved_repair_anchors=restored,
        mechanical_audit=bind(B / 'deletion-audit.json'),
        scope='Consolidates the observed earlier213-edit assessment and current contextual readings of214–237. This is not a new full-book reread or independent semantic certification.',
        conclusion='No unaccounted removal of important scientific material is identified in the assessed edits. Prior omissions of an explicit correlation-test requirement and two information alternatives were repaired in212/213 and remain present. Equations, assumptions, adverse observations, substantive alternatives and source qualifications remain.',
        limits='Exact replay, numeric/citation retention and whitespace tests alone do not prove semantic completeness. The verdict depends on the attributed contextual author assessments; fresh visual and independent editorial/scientific findings remain outstanding.',
        acceptance=dict(author_semantic_review=True, fresh_visual=False, independent=False, release_accepted=False))
    save(O / 'semantic-deletion-review.json', record)
    save(B / 'semantic-deletion-review-current.json', record)
    lines = ['# Current semantic deletion review', '',
        'Batch082;237 exact edits. The first213 edits match the immutable ledger prefix reviewed in the earlier preservation pass. '
        'Its80 substantive removal candidates and two repairs remain documented. All24 later edits have specific contextual dispositions below.', '',
        record['conclusion'], '', record['limits'], '', '| Edit | Assessment |', '|---|---|']
    for d in dispositions:
        lines.append(f'| {d["edit"]} | {d["assessment"]} |')
    (B / 'semantic-deletion-review-current.md').write_text('\n'.join(lines) + '\n')
    scope = read(B / 'review-scope-current.json')
    for p in [prior_path, O / 'verified-ledger-prefix-213.json', O / 'semantic-deletion-review.json',
              B / 'semantic-deletion-review-current.json']:
        scope['basis'][str(p.relative_to(R))] = sha(p)
    scope['semantic_deletion_review'] = bind(B / 'semantic-deletion-review-current.json')
    save(B / 'review-scope-current.json', scope)
    print(json.dumps(dict(status=record['status'], batch=82, edits=237,
        prior_prefix=213, later_dispositions=24, repaired_obligations_retained=True)))


if __name__ == '__main__':
    main()

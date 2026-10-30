"""Bind master-study and finite-calendar contextual review to batch078."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess

R = Path(__file__).resolve().parents[1]
B = R / 'docs/release/2026-10-29'
O = B / 'master-study-review-082'


def read(p):
    return json.loads(p.read_text())


def save(p, x):
    p.write_text(json.dumps(x, indent=2) + '\n')


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def bind(p):
    return dict(path=str(p.relative_to(R)), sha256=sha(p))


def main():
    audit, build, nums = [read(B / f) for f in
                          ['deletion-audit.json', 'latest-build.json', 'numerical-verification.json']]
    assert audit['status'] == 'pass' and audit['edits'] == 230 and build['batch'] == 78
    assert read(B / 'source-verification.json')['build_batch'] == 78
    assert nums['status'] == 'pass' and len(nums['checks']) == 68
    assert nums['checks']['master_study_evidence']['retained_requests'] == 22528
    for name in ['deletion-audit.json', 'source-verification.json', 'numerical-verification.json']:
        shutil.copy2(B / name, O / ('verified-' + name))
    manifest = read(B / 'context-review-230/manifest.json')
    reviews = read(B / 'changed-context-review.json')
    assert len(reviews['reviews']) == 117
    shutil.copy2(B / 'changed-context-review.json', O / 'changed-context-review-before.json')
    findings = [
        'Complete source contexts95/96 were read across the continuation, followed by complete batch078 rendered chapter95 physical1783–1792 and chapter96 physical1793–1798. The next chapter opening is included in the retained extract but is not counted as complete review.',
        'Independent reconstruction verifies22528 retained requests,99 method/cell summaries,40689 interval calculations and4096 graph-union calculations. Every displayed five-study table row agrees. All-request denominators, refusal and whole-line availability, exact binomial-tail inversion, paired gains/losses and conditional widths remain distinct.',
        'Edits228–230 explain the critical-value contribution to coverage comparisons. Retrospective saved-estimate calculations isolate the two servicing critical levels and expose the mixed level/design comparisons in funding and joint dependence. They do not change frozen thresholds, redraw studies or qualify any revised method.',
        'The persistent-calendar442/512 result, wrong-logger1/512 finding, graph whole-line outcomes, false-exclusion zero true-class retention and sparse-learner high-dimension/support failures remain explicit. Equal marginal cover counts are not claimed to imply identical intervals.',
        'Chapter96 states a finite confidence construction under explicit variance and persistence envelopes. Its audit-mixture variance, gold-rank inversion, union bound, leading-coefficient obstruction and AR(1) information counterexample were checked in context and against the existing qualification_design_laws numerical group. The counterexample concerns uniform persistence, not impossibility at the fixed value.95.',
        'Local streaming, reference-target and historical representative-replay claims retain their historical evidence scope. This reconstruction does not rerun original nuisance fitting, covariance-region estimation or all generators; institution-specific information, prices and acceptance remain absent.'
    ]
    contexts = []
    rendered = bind(O / 'chapters095-096-rendered-078.txt')
    for chapter in [95, 96]:
        c = next(x for x in manifest['chapters'] if x['chapter'] == chapter)
        contexts.append(dict(chapter=chapter, extract=c['extract'], sha256=c['sha256']))
        reviews['reviews'].append(dict(chapter=chapter, title=c['title'], status='complete_in_author_scope',
            source_bindings=c['source_bindings'], extract=c['extract'], extract_sha256=c['sha256'],
            review_scope='Complete source and complete batch078 rendered chapter text; author scope only.',
            findings=findings, publication_batch=78, publication=audit['publication']['full'],
            rendered_text=rendered, fresh_visual_acceptance=False, independent_acceptance=False))
    reviews['current_snapshot'] = str((B / 'context-review-230/manifest.json').relative_to(R))
    save(B / 'changed-context-review.json', reviews)
    assert reviews['sponsor_review']['publication']['sha256'] == audit['publication']['sponsor']['sha256']
    review = dict(recorded_utc=datetime.now(timezone.utc).isoformat(), batch=78, edits=[228, 229, 230],
        complete_source_contexts=contexts, rendered=[rendered], publication=audit['publication'],
        numerical_evidence=bind(O / 'verified-numerical-verification.json'), findings=findings,
        deletion_assessment='All three edits insert interpretation before an intact original anchor. No original word, mathematical expression, result, assumption, adverse observation, alternative or qualification is deleted. The retrospective comparisons add a limitation on attributing coverage gains; they do not weaken or remove the conditional-mean derivation or the adverse finite findings.',
        portability_change='The numerical runner resolves project-authored verifier helpers from the relocated package tools directory after checking manifest hashes. Actual relocation remains required before calling a package current.',
        scope='Two complete author-context renewals and independent retained-data reconstruction. No fresh whole-book, visual or independent acceptance.',
        acceptance=dict(author_context=True, fresh_visual=False, independent=False, release_accepted=False))
    save(O / 'contextual-review.json', review)
    x = read(O / 'integration.json')
    x.update(status='verified_in_author_scope', batch=78, review=bind(O / 'contextual-review.json'))
    save(O / 'integration.json', x)
    subprocess.run(['python3', 'tools/reconcile_release_review_currency_20261029.py'], cwd=R, check=True)
    assert read(B / 'review-currency-current.json')['status'] == 'pass'
    scope = read(B / 'review-scope-current.json')
    scope.update(batch=78, ledger_sha256=audit['ledger_sha256'], publication=audit['publication'],
        release_edits=230, edits=230, full_context_records=len(reviews['reviews']), numerical_groups=68,
        latest_contextual_review=str((O / 'contextual-review.json').relative_to(R)),
        latest_rendered_review=str((O / 'contextual-review.json').relative_to(R)),
        portable_package_current=False, numerical_package_current=False,
        scope='119 author records cover101 numbered chapters through95 exact complete-context matches (including two introductions), seven exact-component chains, one chapter47 chain and one preamble. No fresh whole-book, visual or independent acceptance.')
    for p in [B / 'changed-context-review.json', B / 'deletion-audit.json', B / 'source-verification.json',
              B / 'numerical-verification.json', B / 'review-currency-current.json', O / 'contextual-review.json',
              O / 'chapters095-096-rendered-078.txt', O / 'numerical-evidence.json', O / 'plan.md']:
        scope['basis'][str(p.relative_to(R))] = sha(p)
    save(B / 'review-scope-current.json', scope)
    (B / 'review-scope-current.md').write_text(
        '# Current author-review scope\n\nBatch078:230 exact edits;1,941 reader pages and four sponsor pages. '
        'Chapters95/96 have complete source and rendered-text renewal. All22528 master-study requests,99 summary cells '
        'and displayed table rows reconstruct. Added explanation distinguishes changes in critical value from the '
        'information and variance arguments.68 numerical groups pass.119 author records cover101 numbered chapters '
        'through exact contexts and explicit chains. Fresh visual and independent acceptance remain open.\n')
    p = R / 'docs/program/release-programme-2026-10-29.md'
    s = p.read_text()
    start, end = s.index('## Current continuation'), s.index('## Preserved continuation')
    shutil.copy2(p, O / 'programme-before.md')
    replacement = '''## Current continuation — verified batch078 and fair master-study comparisons

Batch078 contains230 exact edits and a1,941-page reader. Independent retained-
data reconstruction verifies22528 master-study requests,99 method/cell summaries,
40689 interval calculations and4096 saved graph unions. Three additive prose
changes explain the contribution of critical values to the reported coverage
differences. They preserve the complete original derivations and adverse
findings. Chapters95/96 have complete source and rendered-text renewal.
68 numerical groups, source verification, preservation and review currency pass.

Continue the late-chapter decision and investment synthesis. Inspect whether
the monetary examples distinguish policy value, information value, useful
precision and workflow savings, and whether the final recommendation follows
from the actual evidence. Avoid generating more studies or changing historical
qualification. Preserve each important alternative and substantive qualification.
At01:58:35 UTC stop new investigations, freeze the candidate, renew both
packages and actually relocate them. Complete final checks and explicit
residual dispositions for02:58:35 UTC delivery.

Plan review: the new reconstruction preserves failed candidates and identifies
comparison confounding without redefining success. The finite-calendar
counterexample remains a restriction on uniform precision, not a universal
rejection of causal funding. Packaging must resolve the new helper from its
own relocated files and include all22528 retained requests. Fresh visual,
independent editorial and institutional acceptance remain open;22 unread
frontier originals retain their claim-specific dispositions.

'''
    p.write_text(s[:start] + replacement + s[end:])
    subprocess.run(['python3', 'tools/refresh_release_controls_20261029.py'], cwd=R, check=True)


if __name__ == '__main__':
    main()

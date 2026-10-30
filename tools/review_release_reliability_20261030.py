"""Record completed contextual reading and retained-result reconstruction."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,shutil,subprocess

R=Path(__file__).resolve().parents[1]
B=R/'docs/release/2026-10-29'
O=B/'prose-review-078'
def read(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(p):return dict(path=str(p.relative_to(R)),sha256=sha(p))


def main():
    audit=read(B/'deletion-audit.json');build=read(B/'latest-build.json');numerics=read(B/'numerical-verification.json')
    assert audit['status']=='pass'and audit['edits']==215 and build['batch']==72
    assert read(B/'source-verification.json')['build_batch']==72
    assert numerics['status']=='pass'and len(numerics['checks'])==63
    assert numerics['checks']['reliability_evidence']['summary_cells']==104
    for name in ['deletion-audit.json','source-verification.json','numerical-verification.json']:
        shutil.copy2(B/name,O/('verified-'+name))
    manifest=read(B/'context-review-215/manifest.json');context=next(x for x in manifest['chapters']if x['chapter']==89)
    reviews=read(B/'changed-context-review.json')
    findings=[
        'Complete assembled chapter89 source read, with final edits214/215 reread. All batch071 rendered chapter text on physical1748–1756 and the next-chapter opening1757 were read; final batch072 changed pages1751/1756 were reread.',
        'The audit-label expectation, pair/calendar/gold sampling separation, finite projection and bandwidth assumptions remain explicit. Calendar precision cannot be bought solely by auditing more pairs.',
        'All104 method/design summaries from six retained study journals reconstruct independently, including unavailable nonlinear fits, whole-line/disconnected graph sets, all-request denominators and exact binomial Monte Carlo intervals. The1500 independent-reference covariance calculations and four complete-workload comparisons also reconstruct.',
        'The half-sum/half-difference coefficient is consistent with equal stratum weights. Edit215 makes those weights and zero-based primitive indices explicit without changing any equation or result.',
        'Edit214 removes author-program language while preserving the actual assignment, audit-truth, interface, platform and matched-cost requirements. Institutional acceptance remains absent.',
        'Final post-build audit retains every original expression, citation, numerical fact and protected input. No adverse result is removed or relabelled as a success.'
    ]
    reviews['reviews'].append(dict(chapter=89,title=context['title'],status='complete_in_author_scope',
        source_bindings=context['source_bindings'],extract=context['extract'],extract_sha256=context['sha256'],
        review_scope='Complete source reading with complete batch071 rendered text and final batch072 changed-page renewal; author scope only.',
        findings=findings,publication_batch=72,publication=audit['publication']['full'],
        rendered_text=bind(O/'chapter89-rendered-072.txt'),fresh_visual_acceptance=False,independent_acceptance=False))
    reviews['current_snapshot']=str((B/'context-review-215/manifest.json').relative_to(R));save(B/'changed-context-review.json',reviews)
    assert reviews['sponsor_review']['publication']['sha256']==audit['publication']['sponsor']['sha256']
    review=dict(recorded_utc=datetime.now(timezone.utc).isoformat(),batch=72,edits=[214,215],
        complete_source_context=dict(extract=context['extract'],sha256=context['sha256']),
        rendered=[bind(O/'chapter89-rendered.txt'),bind(O/'chapter89-rendered-072.txt')],
        numerical_evidence=bind(O/'verified-numerical-verification.json'),
        publication=audit['publication'],findings=findings,
        deletion_assessment='The two replacements remove only internal author-program phrasing and an underspecified scale sentence. Every substantive institutional requirement survives, while equal population weights and the existing indexing convention become explicit. No equation, assumption, adverse result or alternative is deleted.',
        diagnostic_dispositions=[
            'Treatment receipt is a substantive causal variable and remains.',
            'Author reviewers in a clinical source describe its actual evaluation method and remain.',
            'Author-reviewed evidence and excluded author-review costs describe real evaluation scope and remain.',
            'Completion state in implementation prose describes actual software behavior and remains.',
            'The chapter89 author-program adoption phrase is confirmed as unnecessary process narration and repaired.'],
        scope='One renewed complete chapter and targeted final-rendered reading; no fresh whole-book or independent acceptance.',
        acceptance=dict(author_context=True,fresh_visual=False,independent=False,release_accepted=False))
    save(O/'contextual-review.json',review)
    x=read(O/'integration.json');x.update(status='verified_in_author_scope',batch=72,review=bind(O/'contextual-review.json'));save(O/'integration.json',x)
    subprocess.run(['python3','tools/reconcile_release_review_currency_20261029.py'],cwd=R,check=True)
    scope=read(B/'review-scope-current.json');scope.update(batch=72,ledger_sha256=audit['ledger_sha256'],publication=audit['publication'],release_edits=215,edits=215,full_context_records=len(reviews['reviews']),numerical_groups=63,
        latest_contextual_review=str((O/'contextual-review.json').relative_to(R)),latest_rendered_review=str((O/'contextual-review.json').relative_to(R)),portable_package_current=False,numerical_package_current=False,
        scope='110 author records cover101 numbered chapters through95 exact complete-context matches (including two introductions), seven exact-component chains, one chapter47 chain and one preamble. No fresh whole-book, visual or independent acceptance.')
    for p in [B/'changed-context-review.json',B/'deletion-audit.json',B/'source-verification.json',B/'numerical-verification.json',B/'review-currency-current.json',O/'contextual-review.json']:
        scope['basis'][str(p.relative_to(R))]=sha(p)
    save(B/'review-scope-current.json',scope)
    (B/'review-scope-current.md').write_text('# Current author-review scope\n\nBatch072:215 exact edits;1,940 reader pages and four sponsor pages. Chapter89 has complete source and scoped final rendered-text renewal. Its104 retained method/design summaries reconstruct, taking independent numerical groups to63. The semantic deletion review records two repaired qualifications and preserves all scientific material.110 author records cover101 numbered chapters through exact contexts and explicit chains. Fresh visual and independent acceptance remain open.\n')
    p=R/'docs/program/release-programme-2026-10-29.md';s=p.read_text();start=s.index('## Current continuation');end=s.index('## Preserved continuation',start);shutil.copy2(p,O/'programme-before.md')
    replacement='''## Current continuation — verified batch072 and reliability evidence

Batch072 contains215 exact edits and a1,940-page reader. The institutional
conclusion now states the actual evidence requirements directly. Equal stratum
weights and primitive indexing are explicit beside the unchanged funding
inverse. Chapter89 has complete source review and scoped final rendered-text
renewal. All104 retained method/design summaries,1500 reference-covariance
calculations and four workload comparisons reconstruct;63 numerical groups
pass. Source traceability, exact preservation and current review coverage pass.

Continue consequential funding, precision and investment reasoning checks,
especially denominators, sample laws, costs and stale acceptance language.
Retain the post-build semantic deletion review and its two restored
qualifications. Renew affected reviews after every edit. At01:58:35 UTC stop
new investigations, freeze the final candidate and complete package relocation,
all final checks and explicit residual dispositions for02:58:35 UTC delivery.

Plan review: more reconstructed rows strengthen numerical traceability but
do not establish the scientific assumptions, natural voice or bank usefulness.
No fresh visual, independent editorial or institutional acceptance is claimed.
The22 unread frontier originals retain bounded claim-level dispositions.

'''
    p.write_text(s[:start]+replacement+s[end:])
    subprocess.run(['python3','tools/refresh_release_controls_20261029.py'],cwd=R,check=True)


if __name__=='__main__':main()

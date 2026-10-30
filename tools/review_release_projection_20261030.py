"""Record completed projection reading, reconstruction and semantic preservation."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,shutil,subprocess
R=Path(__file__).resolve().parents[1];B=R/'docs/release/2026-10-29';O=B/'projection-review-080'
def read(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(p):return dict(path=str(p.relative_to(R)),sha256=sha(p))

def main():
    audit=read(B/'deletion-audit.json');build=read(B/'latest-build.json');nums=read(B/'numerical-verification.json')
    assert audit['status']=='pass' and audit['edits']==220 and build['batch']==75
    assert read(B/'source-verification.json')['build_batch']==75
    assert nums['status']=='pass' and len(nums['checks'])==66
    assert nums['checks']['projected_funding_evidence']['independent_projected_sets']==10200
    for name in ['deletion-audit.json','source-verification.json','numerical-verification.json']:
        shutil.copy2(B/name,O/('verified-'+name))
    manifest=read(B/'context-review-220/manifest.json');reviews=read(B/'changed-context-review.json')
    assert len(reviews['reviews'])==112
    shutil.copy2(B/'changed-context-review.json',O/'changed-context-review-before.json')
    findings=[
        'Complete chapters92/93 source contexts were read, with additions218/219 and final terminology refinement220 reviewed. Complete batch074 rendered chapter text on physical1768–1776 and the following chapter opening were read; batch075 changed geometry and continuing discussion on physical1769–1771 were reread.',
        'Independent branchwise corner extrema and one-sided singular limits reconstruct10200 projected sets across6600 retained requests. Binomial-tail inversion, all-request coverage, whole-line/finite availability, conditional widths, paired gains/losses and2937 paired finite narrowing cases agree with retained records.',
        'The preserved exploratory3600-request failure remains distinct from the repaired study. False exogeneity still loses36 covers in the transformed comparison; higher-audit near-rank outputs still include105whole-line sets.',
        'Added covariance formulas explain why positive candidate correlation can help the transformed region, while a stipulated negative-correlation example reverses width ordering. The illustration is dimensionless and not attributed to the experiment or bank data.',
        'Rendered review caught determinant-versus-rank terminology in the newly added exposition. Edit220 states that zero determinant means matrix rank one and preserves all geometric cases.',
        'Exact audit inversion remains separate from approximate dependent response inference. Set width, availability, causal validity and information cost remain distinct requirements.'
    ]
    contexts=[]
    for chapter in [92,93]:
        c=next(x for x in manifest['chapters']if x['chapter']==chapter)
        contexts.append(dict(chapter=chapter,extract=c['extract'],sha256=c['sha256']))
        reviews['reviews'].append(dict(chapter=chapter,title=c['title'],status='complete_in_author_scope',
            source_bindings=c['source_bindings'],extract=c['extract'],extract_sha256=c['sha256'],
            review_scope='Complete source and batch074 rendered text with final batch075 changed-page renewal; author scope only.',
            findings=findings,publication_batch=75,publication=audit['publication']['full'],
            rendered_text=bind(O/'projection-rendered-075.txt'),fresh_visual_acceptance=False,independent_acceptance=False))
    reviews['current_snapshot']=str((B/'context-review-220/manifest.json').relative_to(R));save(B/'changed-context-review.json',reviews)
    assert reviews['sponsor_review']['publication']['sha256']==audit['publication']['sponsor']['sha256']
    review=dict(recorded_utc=datetime.now(timezone.utc).isoformat(),batch=75,edits=[218,219,220],
        complete_source_contexts=contexts,rendered=[bind(O/'projection-rendered.txt'),bind(O/'projection-rendered-075.txt')],
        numerical_evidence=bind(O/'verified-numerical-verification.json'),publication=audit['publication'],findings=findings,
        deletion_assessment='Edits218/219 are additive: each retains its entire original anchor and all inherited equations, tables, assumptions and adverse findings. Edit220 replaces only the newly added geometric explanation. Its exact semantic comparison retains corner extrema, derivative sign, branch continuity, disconnected intervals, all pairwise sums, convex-hull warning, compatible whole-line rank-one cases and incompatible empty images. No original scientific material is removed.',
        failures_and_repairs=['Initial checker assertions passed but NumPy counts were not JSON serializable; explicit integer conversion repaired the report.',
            'First post-build audit correctly rejected a missing project-derivation source-scope binding. The explicit binding was added; the subsequent audit passed with unchanged manuscript bytes.',
            'PyMuPDF was unavailable in both Python environments; existing pdftotext produced rendered text without an installation.',
            'A premature batch075-labelled extraction actually read still-current batch074. It is retained as premature-extract-batch074.txt and excluded from acceptance; the final extraction was made only after verifying batch075.'],
        scope='Two complete author-context renewals, independent retained-result reconstruction and post-build semantic assessment. No fresh whole-book, visual or independent acceptance.',
        acceptance=dict(author_context=True,fresh_visual=False,independent=False,release_accepted=False))
    save(O/'contextual-review.json',review)
    x=read(O/'integration.json');x.update(status='verified_in_author_scope',batch=75,review=bind(O/'contextual-review.json'));save(O/'integration.json',x)
    subprocess.run(['python3','tools/reconcile_release_review_currency_20261029.py'],cwd=R,check=True)
    currency=read(B/'review-currency-current.json');assert currency['status']=='pass'and currency['batch']==75
    scope=read(B/'review-scope-current.json');scope.update(batch=75,ledger_sha256=audit['ledger_sha256'],publication=audit['publication'],
        release_edits=220,edits=220,full_context_records=len(reviews['reviews']),numerical_groups=66,
        latest_contextual_review=str((O/'contextual-review.json').relative_to(R)),latest_rendered_review=str((O/'contextual-review.json').relative_to(R)),
        portable_package_current=False,numerical_package_current=False,
        scope='114 author records cover101 numbered chapters through95 exact complete-context matches (including two introductions), seven exact-component chains, one chapter47 chain and one preamble. No fresh whole-book, visual or independent acceptance.')
    for p in [B/'changed-context-review.json',B/'deletion-audit.json',B/'source-verification.json',B/'numerical-verification.json',
              B/'review-currency-current.json',B/'mathematical-addition-reviews.json',O/'contextual-review.json',
              O/'projection-rendered.txt',O/'projection-rendered-075.txt',O/'numerical-evidence.json',O/'source-scope.json']:
        scope['basis'][str(p.relative_to(R))]=sha(p)
    save(B/'review-scope-current.json',scope)
    (B/'review-scope-current.md').write_text('# Current author-review scope\n\nBatch075:220 exact edits;1,941 reader pages and four sponsor pages. Chapters92/93 have complete source and scoped final rendered-text renewal. Independent reconstruction verifies10200 projected sets and their6600 request denominators. Added geometric and covariance explanations preserve all inherited material.66 numerical groups pass.114 author records cover101 numbered chapters through exact contexts and explicit chains. Fresh visual and independent acceptance remain open.\n')
    p=R/'docs/program/release-programme-2026-10-29.md';s=p.read_text();start=s.index('## Current continuation');end=s.index('## Preserved continuation');shutil.copy2(p,O/'programme-before.md')
    replacement='''## Current continuation — verified batch075 and projected financial precision

Batch075 contains220 exact edits and a1,941-page reader. Chapters92/93 explain
the exact projection geometry and a covariance example that reverses width
ordering. Independent reconstruction verifies10200 projected sets from6600
retained requests, including whole-line outputs, conditional widths and the
preserved exploratory failure. No inherited scientific material is deleted.
The final rendered correction distinguishes zero determinant from matrix rank
one.66 numerical groups, source verification, post-build preservation and
current review coverage pass.

Continue linked-history and later investment reasoning checks. The study
counts, supplied information, financial precision and true workflow costs must
remain separate. At01:58:35 UTC stop new investigations, freeze the candidate,
renew both packages and actually relocate them. Complete final checks and
explicit residual dispositions for02:58:35 UTC delivery.

Plan review: high coverage can come from an uninformative whole-line set.
Conditional finite width cannot replace availability; observed paired narrowing
does not establish a universal width theorem. Final packages must include the
new exact derivation, rendered-review and numerical witnesses. Fresh visual,
independent editorial and institutional acceptance remain open;22 unread
frontier originals retain their claim-specific dispositions.

'''
    p.write_text(s[:start]+replacement+s[end:]);subprocess.run(['python3','tools/refresh_release_controls_20261029.py'],cwd=R,check=True)

if __name__=='__main__':main()

"""Renew chapter14 component coverage against final source and rendered text."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil,subprocess
R=Path(__file__).resolve().parents[1];B=R/'docs/release/2026-10-29';O=B/'partial-recovery-073'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(p):return dict(path=str(p.relative_to(R)),sha256=sha(p))
def read(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,indent=2)+chr(10))
def main():
    a=read(B/'deletion-audit.json');build=read(B/'latest-build.json');assert a['status']=='pass'and a['edits']==197 and build['batch']==65
    assert read(B/'source-verification.json')['build_batch']==65
    for n in ['deletion-audit.json','source-verification.json','numerical-verification.json']:shutil.copy2(B/n,O/('verified-'+n))
    c=read(B/'changed-context-review.json');prior=next(r for r in c['reviews']if r['chapter']==14 and 'context-review-188' in r['extract'])
    context=next(r for r in read(B/'context-review-197/manifest.json')['chapters']if r['chapter']==14)
    x=dict(recorded_utc=datetime.now(timezone.utc).isoformat(),batch=65,chapter=14,
      complete_predecessor=dict(extract=prior['extract'],sha256=prior['extract_sha256']),
      source_context=dict(extract=context['extract'],sha256=context['sha256']),edit_numbers=[196],
      reviewed_source_bindings=context['source_bindings'],rendered_text=bind(O/'rendered.txt'),
      numerics=bind(O/'verified-numerical-verification.json'),publication=a['publication']['full'],
      findings=['All350lines of the added section read in source, including assumptions, attainment argument, finite-sample proof, both tables, unstable outcomes, sensitivity and financial alternatives. Chapter opening and preceding conclusion read for transitions; the complete534-line predecessor retains its earlier author reading.',
      'Final physical pages109–114 read as rendered text, including all new material. No unresolved symbols or citation labels and no compiler or text-bound issues; no fresh visual acceptance inferred.',
      'Independent reconstruction passes8000retained rows,48raw endpoint/variance cases and512exact invitation cells. Positive decisions exclude empty sets; set widths usezero for empty while preserving the original signed summaries.',
      'Known independent invitations, stable historical outcomes and IIDarm observations are explicit. Identification width depends on completion law, not positive invitation frequency. The finite-sample bound covers both population endpoints; published true-ATE asymptotics and project normal bands are kept distinct.',
      'Outcome drift gamma differs from package nonresponse delta. The unstable historical-target failure remains. No binary support is imposed on the earlier Gaussian reward, no package code is executed and no bank prices or general qualification are inferred.',
      'Post-build deletion review finds no inherited removal. All earlier treatment, equations, figures, citations, negative findings and alternatives survive exact replay. New bibliography adds one genuine2017paper and one pinned software record.'],
      scope='Previously reviewed complete chapter plus a fully read additive component and exact reconstruction. This is not a fresh whole-chapter or independent review.',
      acceptance=dict(author_component=True,fresh_visual=False,independent=False,release_accepted=False))
    save(O/'component-renewal-014.json',x)
    review=dict(recorded_utc=x['recorded_utc'],batch=65,edits=[196,197],component=bind(O/'component-renewal-014.json'),source_audit=bind(O/'source-audit.json'),witness=bind(O/'exact-witnesses.json'),publication=a['publication'],rendered_text=bind(O/'rendered.txt'),findings=x['findings'],scope=x['scope'],acceptance=x['acceptance']);save(O/'contextual-review.json',review)
    c['current_snapshot']=str((B/'context-review-197/manifest.json').relative_to(R));assert not any(read(R/r['path'])['chapter']==14 for r in c['exact_component_renewals']);c['exact_component_renewals'].append(bind(O/'component-renewal-014.json'));save(B/'changed-context-review.json',c)
    integ=read(O/'integration.json');integ.update(status='verified_in_author_scope',batch=65,review=bind(O/'contextual-review.json'));save(O/'integration.json',integ)
    subprocess.run(['python3','tools/reconcile_release_review_currency_20261029.py'],cwd=R,check=True)
    currency=read(B/'review-currency-current.json');scope=read(B/'review-scope-current.json')
    exact=currency['coverage_modes']['exact_complete_context']-2;chains=101-exact
    scope.update(batch=65,ledger_sha256=a['ledger_sha256'],publication=a['publication'],release_edits=197,edits=197,numerical_groups=62,latest_contextual_review=str((O/'contextual-review.json').relative_to(R)),latest_rendered_review=str((O/'contextual-review.json').relative_to(R)),scope=f'101 numbered chapters:{exact} exact complete-context matches and{chains} complete-predecessor/component-renewal chains. Two introductory contexts and preamble separately current.107 author records are not107 unique chapters. No fresh whole-book, visual or independent acceptance.')
    for p in [B/'changed-context-review.json',B/'deletion-audit.json',B/'source-verification.json',B/'numerical-verification.json',B/'review-currency-current.json',B/'mathematical-addition-reviews.json',O/'contextual-review.json',O/'source-audit.json',O/'exact-witnesses.json']:scope['basis'][str(p.relative_to(R))]=sha(p)
    save(B/'review-scope-current.json',scope)
    (B/'review-scope-current.md').write_text('# Current author-review scope'+chr(10)*2+f'Batch065:197exact edits;{a["publication"]["full"]["pages"]}reader pages and four sponsor pages. Selective-recovery component is reviewed in source and final rendered text;62numerical groups pass. '+scope['scope']+chr(10))
    p=R/'docs/program/release-programme-2026-10-29.md';s=p.read_text();start=s.index('## Current continuation');end=s.index('## Preserved continuation',start);shutil.copy2(p,O/'programme-before.md')
    replacement='''## Current continuation — verified batch065 and release coherence

The release now includes the bounded-outcome selective-recovery argument.
All 8,000 retained procedure/rate cells reconstruct, with 2,000 independent
datasets, 48 raw endpoint/variance checks and exact population enumeration.
The argument separates invitation probability, successful completion and
historical-outcome stability; adverse and empty-set results remain visible.
The finite-sample confidence claim covers the full identified set under its
declared independent design. The normal-band and published package claims
remain distinct. One genuine primary article and one pinned software record
are added, without executing downloaded code or changing frontier counts.

Batch065 has 197 exact edits and 62 numerical groups, with source verification,
source/PDF-bound component review and post-build preservation passing. Renew
the portable manuscript and numerical packages now. Then prioritize release
coherence: align sponsor and conclusions with the completed scientific work,
inspect consequential unresolved-source dispositions, and repair confirmed
writing or cross-chapter inconsistencies. Do not repeat completed studies.

Plan review: additive completeness must not become an accumulation of process
reports. Conclusions should explain the decision and its alternatives, and
evidence details belong where the reader needs them. Preserve every important
mathematical condition, adverse result and source limit. Exact replay supports
preservation but does not substitute for reading. Final integration begins
01:58:35 UTC; delivery remains due 02:58:35 UTC. Fresh visual and independent
editorial acceptance are open, as are actual bank and native qualification.

''';p.write_text(s[:start]+replacement+s[end:])
    subprocess.run(['python3','tools/refresh_release_controls_20261029.py'],cwd=R,check=True)
if __name__=='__main__':main()

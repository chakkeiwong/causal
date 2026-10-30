"""Record the observed decision-synthesis review without promoting acceptance."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, shutil, subprocess
R=Path(__file__).resolve().parents[1]
B=R/'docs/release/2026-10-29'
O=B/'decision-synthesis-074'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text())
def save(p,x): p.write_text(json.dumps(x,indent=2)+'\n')
def bind(p): return dict(path=str(p.relative_to(R)),sha256=sha(p))
def main():
    a=read(B/'deletion-audit.json');build=read(B/'latest-build.json')
    assert a['status']=='pass' and a['edits']==203 and build['batch']==67
    assert read(B/'source-verification.json')['build_batch']==67
    assert len(read(B/'numerical-verification.json')['checks'])==62
    for n in ['deletion-audit.json','source-verification.json','numerical-verification.json']:
        shutil.copy2(B/n,O/('verified-'+n))
    c=read(B/'changed-context-review.json')
    manifest=read(B/'context-review-203/manifest.json')
    records=[]
    for ch,old_path,edits,rendered,findings in [
      (14,B/'partial-recovery-073/component-renewal-014.json',[196,198,203],O/'recovery-final-rendered.txt',[
        'Read the new decision-frequency paragraph and surrounding recovery conclusion as source and final rendered physical pages113–115. The fully read additive section and complete predecessor retain their earlier scopes.',
        'The same500 datasets produce intensive-recovery5 bounded and22 normal net-positive nonempty sets at q=1; complete stable recovery produces335 and432. These differ from401 and469 positive-effect decisions before offer cost.',
        'Corrected full invitation to mean every missing customer is invited. Selective noncompletion remains; no result, assumption, adverse finding or calculation is removed.']),
      (101,B/'energy-integration-071/component-renewal-101.json',[189,202],O/'investment-final-rendered.txt',[
        'Read the decision-synthesis addition and final investment recommendation in source and rendered physical pages1848–1850. Existing complete predecessor and energy-component review remain explicitly inherited.',
        'Recovery, graph ambiguity, finite-sample failure and useful-output expense lead to the same bounded analyst comparison. All four cross-references resolve to their intended arguments.',
        'No investment price, benefit estimate or bank-performance claim is added. Existing multi-year account, energy study, alternatives and reversal conditions survive.'])]:
        x=read(old_path);context=next(r for r in manifest['chapters']if r['chapter']==ch)
        x.update(recorded_utc=datetime.now(timezone.utc).isoformat(),batch=67,edit_numbers=edits,
          source_context=dict(extract=context['extract'],sha256=context['sha256']),
          reviewed_source_bindings=context['source_bindings'],rendered_text=bind(rendered),
          numerics=bind(O/'verified-numerical-verification.json'),publication=a['publication']['full'],
          prior_component_review=bind(old_path),findings=findings)
        path=O/f'component-renewal-{ch:03d}.json';save(path,x);records.append(bind(path))
        indexes=[i for i,r in enumerate(c['exact_component_renewals'])if read(R/r['path'])['chapter']==ch]
        assert len(indexes)==1;c['exact_component_renewals'][indexes[0]]=bind(path)
    review=dict(recorded_utc=datetime.now(timezone.utc).isoformat(),batch=67,edits=list(range(198,204)),
      components=records,publication=a['publication'],decision_witness=bind(O/'decision-witness.json'),
      sponsor_rendered=bind(O/'sponsor-final-rendered.txt'),
      findings=['Complete current sponsor source and all four rendered pages read. Recovery stability, finite-sample graph failures and whole-attempt economics now accompany earlier positive results.',
        'Net-benefit frequencies are post-processing of retained datasets, checked by the62-group numerical verifier. No added simulation or new mathematical expression.',
        'Post-build exact deletion review: edits198–202 add connections and consequences;203 replaces an overstatement about completion with the invitation mechanism. All inherited important material remains.',
        'Opening reading guide remains coherent; targeted navigation to new recovery, sampling and cost arguments is the next editorial priority.'],
      execution_observations=['The initial resumption status command overprinted the large historical state; bounded reads and saved status/check outputs were used thereafter. Historical programme check passes.',
        'No new images were viewed. Text extraction and geometry are distinct from visual acceptance.'],
      scope='Current sponsor complete author reading and exact component renewals for chapters14 and101; not independent or fresh whole-book acceptance.',
      acceptance=dict(author_component=True,fresh_visual=False,independent=False,release_accepted=False))
    save(O/'contextual-review.json',review)
    sponsor=c['sponsor_review'];sponsor.update(status='complete_in_author_scope',
       scope='Complete current sponsor source and four-page final rendered text read.',
       source_bindings={n:sha(R/n)for n in sponsor['source_bindings']},
       publication=a['publication']['sponsor'],rendered_text=bind(O/'sponsor-final-rendered.txt'),
       review_record=bind(O/'contextual-review.json'),
       findings=review['findings'][:3],renewal='Recovery, sampling and useful-answer conclusions added; all prior quantitative claims and qualification limits retained.')
    c['current_snapshot']=str((B/'context-review-203/manifest.json').relative_to(R));save(B/'changed-context-review.json',c)
    integ=read(O/'integration.json');integ.update(status='verified_in_author_scope',batch=67,review=bind(O/'contextual-review.json'))
    integ['targets']=[bind(R/r['path'])for r in integ['targets']];save(O/'integration.json',integ)
    subprocess.run(['python3','tools/reconcile_release_review_currency_20261029.py'],cwd=R,check=True)
    scope=read(B/'review-scope-current.json');scope.update(batch=67,ledger_sha256=a['ledger_sha256'],publication=a['publication'],
      release_edits=203,edits=203,numerical_groups=62,latest_contextual_review=str((O/'contextual-review.json').relative_to(R)),
      latest_rendered_review=str((O/'contextual-review.json').relative_to(R)),portable_package_current=False,numerical_package_current=False)
    for p in [B/'changed-context-review.json',B/'deletion-audit.json',B/'source-verification.json',B/'numerical-verification.json',B/'review-currency-current.json',B/'mathematical-addition-reviews.json',O/'contextual-review.json',O/'decision-witness.json']:
        scope['basis'][str(p.relative_to(R))]=sha(p)
    save(B/'review-scope-current.json',scope)
    (B/'review-scope-current.md').write_text('# Current author-review scope\n\nBatch067:203 exact edits,1,939 reader pages and four sponsor pages. Sponsor complete source/rendered review and chapters14/101 component renewals are current. All101 numbered chapters retain exact complete-context or documented cumulative component coverage;62 numerical groups pass. Batch065 remains the relocated portable fallback. Fresh visual, independent editorial and bank acceptance remain open.\n')
    p=R/'docs/program/release-programme-2026-10-29.md';s=p.read_text();start=s.index('## Current continuation');end=s.index('## Preserved continuation',start);shutil.copy2(p,O/'programme-before.md')
    replacement='''## Current continuation — verified batch067 and final argument review

The sponsor and final investment recommendation now incorporate selective
recovery, finite-sample graph failure and expense per useful completed study.
The repayment example also distinguishes a positive effect from a result that
covers the stipulated offer cost. Full invitation is explicitly separated
from completed recovery. Batch067 contains203 exact edits and62 numerical
groups; current author review, source checks and post-build preservation pass.
The1,939-page reader and four-page sponsor preserve all important inherited
material. Batch065 remains the verified relocated package fallback.

Next, review the opening navigation and consequential cross-chapter wording
against these completed arguments. Resolve confirmed inconsistencies in the
manuscript, record exact deletions and re-read their final contexts. Review
the22 unread frontier dispositions for any release-critical unsupported
assertion; do not repeat failed acquisitions without a new permitted route.
Prioritize scientific meaning and connected exposition over further census
or repeated experimental activity.

Plan review: a source count or correct build cannot certify readable scholarly
argument. The reader must follow the decision, assumptions, identification,
uncertainty, financial consequence and alternatives. Preservation requires
semantic destinations as well as unchanged mathematics. Reserve01:58:35 UTC
on30 October for final audit, package renewal and actual relocation; delivery
remains02:58:35 UTC. Fresh visual and independent editorial acceptance remain
open, separately from bank and native qualification.

''';p.write_text(s[:start]+replacement+s[end:])
    subprocess.run(['python3','tools/refresh_release_controls_20261029.py'],cwd=R,check=True)
if __name__=='__main__': main()

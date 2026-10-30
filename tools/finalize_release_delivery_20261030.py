"""Reconcile qualified batch086 delivery without changing frozen evidence."""
from pathlib import Path
import datetime
import hashlib
import json
import sys

R = Path(__file__).resolve().parents[1]
B = R / 'docs/release/2026-10-29'
D = B / 'delivery-094'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def load(p):
    return json.loads(p.read_text())

def save(p, data):
    p.write_text(json.dumps(data, indent=2) + '\n')

def ref(p):
    return {'path': str(p.relative_to(R)), 'sha256': sha(p)}

def reconcile_pages():
    p=R/'docs/program/release-programme-2026-10-29.md';s=p.read_text()
    start=s.index('## Current continuation — batch 086 final review and delivery')
    end=s.index('## Preserved continuation — verified batch082',start)
    block='''## Current continuation — final integration of batch 086 revision 1

The 1,941-page reader and four-page sponsor are verified and frozen. All 292
exact release edits preserve the 505-edit baseline. Both revision 1 packages
now pass actual relocation: byte-identical PDFs, exact edit replay, 611
author-review evidence files and 68 retained arithmetic groups. Five historical
semantic-review dependencies missing from revision 0 were recovered in revision
1; the diagnostic and original package remain preserved. No manuscript change
was required.

The final rendered-text pass reads chapters 14, 21, 100, 101 and the entire
sponsor. Together with the attributed complete contexts and component chains,
current author review covers 101 numbered chapters and 523 source segments.
This is not a fresh whole-book, visual or independent review. The semantic
deletion assessment identifies no unaccounted substantive loss in its scope.

| Work | Current disposition |
|---|---|
| REL01–REL02 | Baseline, programme review and scientific integration complete in declared scope. |
| REL03 | Selected consequential comparisons complete; 91 inspected/22 unread frontier entries and separate TCDF/Windmeijer omissions remain explicit. |
| REL04–REL06 | Author-context, retained arithmetic, portable package and preservation work complete for this exact candidate. |
| REL07 | Fresh visual inspection and independent editorial/scientific acceptance remain open. |
| REL08 | Final delivery manifest and control reconciliation in progress until 02:58:35 UTC. |

The remaining authorized work binds the exact candidate, package proofs,
standard assessment, residual inventory and reviewer handoff in a versioned
manifest; verifies current controls and final local links; and delivers the
qualified candidate by 30 October 2026, 02:58:35 UTC (10:58:35 Asia/Shanghai).
No new source investigation starts after 01:58:35 UTC. Further changes require
a demonstrated defect and renewed review/build/deletion/package evidence.

Plan review: the new state removes obsolete package and contextual-review
blockers without granting acceptance. Frozen creation-time records remain
unchanged; a post-package manifest records observed relocation. The historical
master-program.md, state.json and root README remain hash-protected. Only the
current release section of master-live.md and mission control changes; other
scientific continuations retain their own state and evidence. The next
publication gate requires actual observations from a fresh visual session and
actual independent critical reading. Deadlines, page counts and machine checks
cannot supply those judgments.

'''
    p.write_text(s[:start]+block+s[end:])
    for file,prefix in [('CURRENT.md','docs/'),('docs/mission-control.md',''),('docs/program/master-live.md','../')]:
        p=R/file;s=p.read_text();start=s.index('## Active release candidate:');end=s.index('<!-- release-candidate:end -->',start)
        old=s[start:end]
        new=old.replace('The current frozen batch086 package','The current frozen batch086 revision1 package')
        new=new.replace('Final source/PDF-bound author review, consequential source comparisons and final packaging continue.','Final author-context review and both package relocation checks are complete in their declared scope. Delivery-manifest integration and control verification continue; no new source investigation is open.')
        new+=f'[Final integration records]({prefix}release/2026-10-29/delivery-094/README.md) · [Current standard]({prefix}release/2026-10-29/final-readiness-093/writing-standard-current.md) · [Reviewer handoff]({prefix}release/2026-10-29/final-readiness-093/reviewer-handoff.md)\n\n'
        p.write_text(s[:start]+new+s[end:])
    p=R/'docs/mission-control.html';s=p.read_text();start=s.index('<section><h2>Active release candidate:');end=s.index('</section>',start)
    new=s[start:end].replace('Current batch086 reproduces','Current batch086 revision1 reproduces').replace('Source-bound author reviews and consequential comparisons continue.','Author-context review and both package relocation checks pass in declared scope. Final delivery records and controls are being reconciled; new source investigations are closed.')
    new+='<p><a href="release/2026-10-29/delivery-094/README.md">Final integration records</a> · <a href="release/2026-10-29/final-readiness-093/reviewer-handoff.md">Reviewer handoff</a></p>'
    p.write_text(s[:start]+new+s[end:])
    print(json.dumps({'status':'current_release_pages_reconciled','pages':5}))

def reconcile():
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    a = load(B / 'deletion-audit.json')
    proof = load(B / 'package-verification-batch-086-r01.json')
    nr = load(B / 'numerical-portability-batch-086-r01/result.json')
    assert a['status'] == proof['status'] == nr['status'] == 'pass'
    assert a['edits'] == 292 and a['ledger_sha256'] == sha(B / 'edits.json')
    for p in a['publication'].values():
        assert sha(R / p['path']) == p['sha256']
    assert proof['reader_sha256'] == a['publication']['full']['sha256']
    assert proof['sponsor_sha256'] == a['publication']['sponsor']['sha256']
    assert sha(R / proof['package'] / 'manifest.json') == proof['manifest_sha256']
    assert sha(R / nr['package'] / 'manifest.json') == nr['manifest_sha256']
    assert len(load(B / 'numerical-verification.json')['checks']) == 68
    blockers = ['Fresh visual inspection of the exact candidate PDFs',
                'Independent editorial/scientific findings and acceptance']
    evidence = {
        'manuscript_relocation': ref(B / 'package-verification-batch-086-r01.json'),
        'numerical_relocation': ref(B / 'numerical-portability-batch-086-r01/result.json'),
        'navigation': ref(B / 'final-readiness-093/pdf-navigation/navigation-verification.json'),
        'review_dependency_closure': ref(B / 'final-readiness-093/review-binding-closure.json')}
    inv = load(B / 'remaining-inventory.json')
    inv.update(as_of=now, status='candidate_bound_residuals_packages_verified', release_blockers=blockers)
    inv['completed_candidate_checks'].update(evidence)
    inv['completed_candidate_checks']['scope'] = 'Batch086 revision1 manuscript and numerical packages pass actual relocation. Both PDFs are byte-identical;292 edits replay and68 arithmetic groups reconstruct. Final delivery records bind later control reconciliation without modifying frozen packages.'
    save(B / 'remaining-inventory.json', inv)
    p = B / 'remaining-inventory.md'; s = p.read_text()
    s = s.replace('Batch 086; final package relocation pending.', 'Batch 086 revision 1; both packages have passed actual relocation.')
    s = s.replace('Both batch 086 packages must now pass relocation.', 'Both batch 086 revision 1 packages pass relocation; the reader and sponsor reproduce byte-identically.')
    s = s.replace('The post-package delivery manifest records the relocation outcome.', 'The delivery manifest records the relocation outcome and reconciled controls; frozen creation-time records remain unchanged.')
    p.write_text(s)
    review = load(B / 'review-scope-current.json')
    review.update(portable_package=proof['package'], numerical_package=nr['package'], portable_package_current=True, numerical_package_current=True,
                  portable_verification=evidence['manuscript_relocation'], numerical_portability=evidence['numerical_relocation'],
                  package_status='Batch086 revision1 passes actual manuscript and numerical relocation. Both PDF hashes reproduce;all292 edits replay,611 author-review evidence files verify,and all68 retained arithmetic groups reconstruct. Missing/altered evidence and external inputs are rejected.',
                  remaining=blockers + ['Bounded original-source omissions and explicitly scoped theoretical extensions;no exhaustive survey or universal implementation claim.'])
    for p in [B / 'remaining-inventory.json', B / 'remaining-inventory.md']:
        review['basis'][str(p.relative_to(R))] = sha(p)
    review['control_reconciliation_utc'] = now
    review['creation_time_package_scope'] = 'Frozen review-scope-current.json records the state before its own relocation. This live successor records observed results;no recursive re-freeze is needed or claimed.'
    save(B / 'review-scope-current.json', review)
    state = load(B / 'state.json')
    state.update(phase='REL08_final_integration', status='active', release_accepted=False, fresh_visual_acceptance=False, independent_acceptance=False,
                 observed_gaps=blockers + ['22 unread frontier originals;separate TCDF/Windmeijer omissions;broader theoretical and implementation qualifications remain bounded.'],
                 next_action='Finish versioned delivery manifest and validate exact links and identities before02:58:35UTC. No new source investigation. In a fresh session inspect these exact PDFs visually and incorporate actual independent findings. Any manuscript repair requires renewed context/deletion review,build and package proofs.')
    scopes = {
        'REL01': ('complete', 'Protected baseline and programme review retained.'),
        'REL02': ('complete', 'Completed scientific treatments integrated with adverse findings and source limits;no rerun claimed.'),
        'REL03': ('bounded_complete_with_omissions', 'Selected consequential comparisons integrated;91 inspected/22 unread fixed-frontier entries,one inspected quarantine and separate original omissions remain.'),
        'REL04': ('complete_in_author_scope', 'Contextual prose,citations,navigation and rendered-text repairs verified;visual/independent judgments remain separate.'),
        'REL05': ('complete_in_declared_scope', 'Revision1 same-system portable manuscript build and68-group reconstruction pass;not all studies regenerated.'),
        'REL06': ('complete_in_author_scope', 'Current context chains cover101 chapters;cumulative292-edit semantic and post-build preservation reviews pass.'),
        'REL07': ('blocked', 'Fresh visual allowance and actual independent editorial/scientific findings unavailable.'),
        'REL08': ('in_progress', 'Final manifest,control reconciliation and handoff in progress within authorized window.')}
    for t in state['tasks']:
        t['status'], t['scope'] = scopes[t['id']]
    state['final_integration'] = {'as_of': now, 'delivery_directory': str(D.relative_to(R)), 'evidence': evidence,
                                 'review_scope': ref(B / 'review-scope-current.json'), 'residual_inventory': ref(B / 'remaining-inventory.json')}
    save(B / 'state.json', state)
    save(B/'delivery-current.json', {'batch':86,'package_revision':1,'stage':'final_integration','directory':str(D.relative_to(R)),'updated_utc':now,'release_accepted':False})
    save(D/'control-reconciliation.json', {'status':'pass','recorded_utc':now,'batch':86,'package_revision':1,'manuscript_changes':0,'evidence':evidence,'before':str((D/'before').relative_to(R)),'review_scope':ref(B/'review-scope-current.json'),'residual_inventory':ref(B/'remaining-inventory.json'),'scope':'Correct stale pending statements and exact pointers;preserve frozen artifacts and external gates.'})
    print(json.dumps({'status':'reconciled','batch':86,'revision':1,'phase':state['phase'],'release_accepted':False}))

if __name__ == '__main__':
    if sys.argv[1:] == ['reconcile']:
        reconcile()
    elif sys.argv[1:] == ['pages']:
        reconcile_pages()
    else:
        raise SystemExit('Usage: finalize_release_delivery_20261030.py reconcile|pages')

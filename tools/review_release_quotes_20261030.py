"""Renew four existing context chains after seven literal quote-spacing edits."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess

R = Path(__file__).resolve().parents[1]
B = R / 'docs/release/2026-10-29'
O = B / 'quotation-review-088'


def read(p): return json.loads(p.read_text())
def save(p,x): p.write_text(json.dumps(x,indent=2)+'\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(p): return dict(path=str(p.relative_to(R)),sha256=sha(p))


def main():
    audit,build,edits=[read(B/f) for f in ['deletion-audit.json','latest-build.json','edits.json']]
    assert audit['status']=='pass' and build['batch']==85 and len(edits)==290
    assert read(B/'source-verification.json')['build_batch']==85
    assert all(e['before'].replace(r'\,','')==e['after'] for e in edits[283:])
    old=(B/'batches/084/full/rendered.txt').read_text().split('\f')
    new=(B/'batches/085/full/rendered.txt').read_text().split('\f')
    changed=[i+1 for i,(x,y) in enumerate(zip(old,new)) if x!=y]
    assert len(old)==len(new) and changed==[300,1037,1270,1271,1367]
    assert len(read(O/'rendered-quotes.json'))==7
    for name in ['deletion-audit.json','source-verification.json','numerical-verification.json']:
        shutil.copy2(B/name,O/('verified-'+name))
    reviews=read(O/'before-changed-context-review.json')
    manifest=read(B/'context-review-290/manifest.json')
    prior=read(B/'context-review-283/manifest.json')
    integration=read(O/'integration.json');chapters=[35,60,69,71]
    previous={};active=[]
    for item in reviews['exact_component_renewals']:
        rec=read(R/item['path'])
        if rec['chapter'] in chapters:
            previous[rec['chapter']]=(item,rec)
            reviews.setdefault('superseded_component_renewals',[]).append(dict(**item,superseded_by='Cumulative exact quote-spacing renewal at batch085.'))
        else:active.append(item)
    receipts=[]
    for n in chapters:
        c=next(x for x in manifest['chapters'] if x['chapter']==n)
        oldc=next(x for x in prior['chapters'] if x['chapter']==n)
        added=[v['edit'] for v in integration['changes'] if v['chapter']==n]
        if n in previous:
            item,rec=previous[n];complete=rec['complete_predecessor'];indices=rec['edit_numbers']+added
            assert rec['source_context']['sha256']==oldc['sha256']
            markers=rec.get('source_marker_updates',[])
        else:
            match=[r for r in reviews['reviews'] if r['chapter']==n and r['extract_sha256']==oldc['sha256']]
            assert len(match)==1
            complete=dict(extract=match[0]['extract'],sha256=match[0]['extract_sha256']);indices=added;markers=[];item=None
        text=(R/complete['extract']).read_text()
        for i in indices:
            e=edits[i-1];assert text.count(e['before'])==1,(n,i)
            text=text.replace(e['before'],e['after'],1)
        for m in markers:text=text.replace(m['before']+'\n',m['after']+'\n',1)
        assert text==(R/c['extract']).read_text(),n
        record=dict(chapter=n,recorded_utc=datetime.now(timezone.utc).isoformat(),batch=85,
            complete_predecessor=complete,source_context=dict(extract=c['extract'],sha256=c['sha256']),
            edit_numbers=indices,source_marker_updates=markers,predecessor_component_receipt=item,
            reviewed_source_bindings=c['source_bindings'],rendered_text=bind(O/'rendered-quotes.txt'),
            numerics=bind(O/'verified-numerical-verification.json'),publication=audit['publication']['full'],
            findings=['Exact source and rendered text surrounding every changed closing quotation was read. Only the thin-space command separating apostrophes is removed; all quoted words and sentence punctuation survive.',
                      'All other context content reconstructs exactly from its attributed complete predecessor and cumulative edits. This is a typographic component renewal, not a new whole-chapter reading.'],
            acceptance=dict(author_component=True,fresh_visual=False,independent=False,release_accepted=False))
        path=O/f'component-renewal-{n:03d}.json';save(path,record);receipts.append(bind(path));active.append(bind(path))
    reviews['exact_component_renewals']=active
    reviews['current_snapshot']=str((B/'context-review-290/manifest.json').relative_to(R))
    save(B/'changed-context-review.json',reviews)
    report=dict(recorded_utc=datetime.now(timezone.utc).isoformat(),batch=85,edits=list(range(284,291)),
        publication=audit['publication'],changed_physical_pages=changed,contextual_chains=receipts,
        rendered_text=bind(O/'rendered-quotes.txt'),numerics=bind(O/'verified-numerical-verification.json'),
        findings=['Seven inherited split closing quotation marks repaired in four chapters. Every changed source and rendered passage inspected. No substantive prose, mathematics, numerical input or source claim changes.',
                  'Five rendered pages changed; page count, sponsor and bibliography remain unchanged. No fresh full-chapter, primary-source, visual or independent review claimed.'],
        deletion_assessment=[dict(edit=i,disposition='Removes only a thin-space command inside a closing double quote; all quoted words and substantive material retained.') for i in range(284,291)],
        acceptance=dict(author_component=True,fresh_visual=False,independent=False,release_accepted=False))
    save(O/'contextual-review.json',report)
    integration.update(status='verified_in_author_scope',batch=85,review=bind(O/'contextual-review.json'));save(O/'integration.json',integration)
    subprocess.run(['python3','tools/reconcile_release_review_currency_20261029.py'],cwd=R,check=True)
    scope=read(B/'review-scope-current.json');scope.update(batch=85,ledger_sha256=audit['ledger_sha256'],publication=audit['publication'],release_edits=290,edits=290,
        latest_contextual_review=str((O/'contextual-review.json').relative_to(R)),latest_rendered_review=str((O/'contextual-review.json').relative_to(R)),portable_package_current=False,numerical_package_current=False)
    for p in [B/'changed-context-review.json',B/'deletion-audit.json',B/'source-verification.json',B/'review-currency-current.json',
              O/'contextual-review.json',O/'rendered-quotes.txt',O/'rendered-quotes.json',O/'source-occurrences.json',O/'plan.md']:
        scope['basis'][str(p.relative_to(R))]=sha(p)
    for r in receipts:scope['basis'][r['path']]=r['sha256']
    save(B/'review-scope-current.json',scope)
    (B/'review-scope-current.md').write_text('# Current author-review scope\n\nBatch085:290 exact edits;1,941 reader pages and four sponsor pages.124 complete author records and explicit component chains cover101 numbered chapters. The latest component renewal repairs seven closing quote marks; the prior415 supporting-citation repairs remain. All substantive material is retained. Fresh visual and independent acceptance remain open.\n')
    print(json.dumps(dict(status='complete_in_author_scope',batch=85,changed_pages=changed)))


if __name__=='__main__':main()

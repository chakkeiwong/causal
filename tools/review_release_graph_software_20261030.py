"""Bind the observed graph-component reading and exact deletion review."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil,subprocess
R=Path(__file__).resolve().parents[1];B=R/'docs/release/2026-10-29';O=B/'graph-software-072'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(p):return dict(path=str(p.relative_to(R)),sha256=sha(p))
def read(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,indent=2)+chr(10))
def main():
    a=read(B/'deletion-audit.json');build=read(B/'latest-build.json');assert a['status']=='pass'and a['edits']==195 and build['batch']==64
    assert read(B/'source-verification.json')['build_batch']==64
    for n in ['deletion-audit.json','source-verification.json','numerical-verification.json']:
        shutil.copy2(B/n,O/('verified-'+n))
    prior=B/'graph-integration-069/component-renewal-069.json';x=read(prior)
    context=B/'context-review-195/chapter-069.tex';target=B/'source/docs/writing-repair/2026-10-29/src/5e1bb6d4d921349d.tex'
    x.update(recorded_utc=datetime.now(timezone.utc).isoformat(),batch=64,
       source_context=dict(extract=str(context.relative_to(R)),sha256=sha(context)),
       edit_numbers=x['edit_numbers']+[193,195],reviewed_source_bindings={str(target.relative_to(R)):sha(target)},
       rendered_text=bind(O/'rendered-addition.txt'),numerics=bind(O/'verified-numerical-verification.json'),
       publication=a['publication']['full'],prior_component_review=bind(prior),
       findings=['Complete 527-line component read before the explanatory conclusion refinement; exact replacement then read with its surviving surrounding argument. All earlier mathematical examples, assumption qualifications and adverse results remain.',
       'Final rendered physical pages1295–1299 read, including the whole new subsection on1297–1298, transitions, citations and monetary conclusion. This is text inspection, not visual acceptance.',
       'Pinned front-end code and later Berry service are distinguished from the thesis pipeline and earlier dependency. No native execution, graph calibration or benchmark reproduction is claimed.',
       'Edit195 replaces only the newly imported imperative list. Every scientific requirement has a named surviving clause; no inherited substantive content is deleted. No new mathematical expressions or numerical study are added.'])
    save(O/'component-renewal-069.json',x)
    review=dict(recorded_utc=x['recorded_utc'],batch=64,edits=[193,194,195],
       component=bind(O/'component-renewal-069.json'),source_audit=bind(O/'source-audit.json'),
       publication=a['publication'],rendered_text=bind(O/'rendered-addition.txt'),
       deletion_findings=x['findings'][-1:],
       execution_observations=['Initial fitz-based extraction was unavailable in both installed Python environments; pdftotext successfully supplied final PDF text. No dependency installation or visual claim followed.'],
       scope='Full changed-component author reading plus exact cumulative reconstruction from the previously reviewed full chapter; not a new whole-chapter or independent reading.',
       acceptance=dict(author_component=True,fresh_visual=False,independent=False,release_accepted=False))
    save(O/'contextual-review.json',review)
    c=read(B/'changed-context-review.json');c['current_snapshot']=str((B/'context-review-195/manifest.json').relative_to(R))
    for i,row in enumerate(c['exact_component_renewals']):
        if read(R/row['path'])['chapter']==69:c['exact_component_renewals'][i]=bind(O/'component-renewal-069.json')
    save(B/'changed-context-review.json',c)
    integ=read(O/'integration.json');integ.update(status='verified_in_author_scope',edits=[193,194,195],batch=64,target=bind(target),review=bind(O/'contextual-review.json'));save(O/'integration.json',integ)
    subprocess.run(['python3','tools/reconcile_release_review_currency_20261029.py'],cwd=R,check=True)
    scope=read(B/'review-scope-current.json');scope.update(batch=64,ledger_sha256=a['ledger_sha256'],publication=a['publication'],release_edits=195,edits=195,latest_contextual_review=str((O/'contextual-review.json').relative_to(R)),latest_rendered_review=str((O/'contextual-review.json').relative_to(R)),portable_package=str((B/'packages/batch-062').relative_to(R)),numerical_package=str((B/'numerical-packages/batch-062').relative_to(R)),portable_package_current=False,numerical_package_current=False)
    for p in [B/'changed-context-review.json',B/'deletion-audit.json',B/'source-verification.json',B/'numerical-verification.json',B/'review-currency-current.json',O/'contextual-review.json',O/'source-audit.json',O/'conclusion-refinement.json']:
        scope['basis'][str(p.relative_to(R))]=sha(p)
    save(B/'review-scope-current.json',scope)
    (B/'review-scope-current.md').write_text('# Current author-review scope'+chr(10)*2+'Batch064: 195 exact edits, 1,934 reader pages and four sponsor pages. The graph software comparison and explanatory conclusion are current in author scope. All 101 numbered chapters retain exact full-context coverage or explicit component-renewal chains. The batch062 portable packages remain a verified earlier fallback. Fresh visual and independent acceptance remain open.'+chr(10))
    p=R/'docs/program/release-programme-2026-10-29.md';s=p.read_text();start=s.index('## Current continuation');end=s.index('## Preserved continuation',start);shutil.copy2(p,O/'programme-before.md')
    replacement='''## Current continuation — verified batch064 and selective recovery

The 1,934-page reader and four-page sponsor contain 195 exact edits. The
available graph-software comparison now distinguishes the thesis's front end,
its unexposed full pipeline and the later Berry evidence-support service.
Source/PDF-bound component review, exact edit replay, preservation, source
verification and 61 numerical groups pass. Batch062 remains the latest
relocated portable fallback; further manuscript changes require renewal.

Next, assess the completed selective-recovery study for a missing scientific
condition: a random invitation does not make completed recovery representative.
Read the genuine Coppock2017 primary text and pinned attrition implementation,
derive the bounded-outcome population set and finite-sample confidence claim,
then reconstruct the retained experiment. Keep invitation frequency distinct
from successful recovery and keep outcome drift distinct from nonresponse
mixture sensitivity. Integrate only after that review; do not rerun the study
or infer finite bounds for the earlier Gaussian servicing rewards.

Plan review: this addition must close the existing full-recovery assumption
without replacing the previous study. Preserve all failures, crossing bounds,
unstable-outcome results and differing inferential targets. No native software
or bank validation follows from static inspection or generated experiments.
Final integration still begins 01:58:35 UTC; delivery is due 02:58:35 UTC.
Fresh visual and independent editorial acceptance remain explicitly open.

'''
    p.write_text(s[:start]+replacement+s[end:])
    subprocess.run(['python3','tools/refresh_release_controls_20261029.py'],cwd=R,check=True)
if __name__=='__main__':main()

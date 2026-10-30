"""Bind actual opening/synthesis readings and renew changed components."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil,subprocess
R=Path(__file__).resolve().parents[1];B=R/'docs/release/2026-10-29';O=B/'argument-coherence-075'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def bind(p):return dict(path=str(p.relative_to(R)),sha256=sha(p))
def main():
 a=read(B/'deletion-audit.json');build=read(B/'latest-build.json');assert a['status']=='pass'and a['edits']==211 and build['batch']==69
 assert read(B/'source-verification.json')['build_batch']==69
 for n in ['deletion-audit.json','source-verification.json','numerical-verification.json']:shutil.copy2(B/n,O/('verified-'+n))
 c=read(B/'changed-context-review.json');manifest=read(B/'context-review-211/manifest.json')
 for ch,title,rendered,findings in [(0,'How to read the argument','opening-rendered.txt',[
  'Complete opening reading-guide source read after cross-reference repair, including the following part introduction; rendered physical page3 read in full.',
  'The guide connects exact-oracle repair to finite-sample failure, random invitation to historical recovery, and investment to full expense per useful answer. All referenced section numbers resolve correctly.']),
  (32,'What the evidence changes about the proposed service','evidence-rendered.txt',[
  'Complete assembled chapter source read and all rendered physical pages272–274 read, including the continuation across the last page break.',
  'Every earlier target-error, variance, timing, public-data and interface result remains. The new paragraph makes recovery, graph uncertainty and whole-attempt expense consequential for the same proposed comparison.'])]:
  context=next(r for r in manifest['chapters']if r['chapter']==ch and r['title']==title)
  c['reviews'].append(dict(chapter=ch,title=title,status='complete_in_author_scope',source_bindings=context['source_bindings'],
    extract=context['extract'],extract_sha256=context['sha256'],review_scope='Complete assembled source and stated final rendered text read; author review only.',
    findings=findings,publication_batch=69,publication=a['publication']['full'],rendered_text=bind(O/rendered),fresh_visual_acceptance=False,independent_acceptance=False))
 components=[]
 for ch,edits,rendered,findings in [
  (14,[196,198,203,206],'recovery-rendered.txt',['Final recovery conclusion read in source and rendered physical114. The bounded single-treatment result, unresolved bank recovery, unbounded-longitudinal limitation and absent operating acceptance remain. Authoring-status language is replaced by the actual information comparison.']),
  (101,[189,202,208],'investment-rendered.txt',['The revised historical-outcome phrase and whole final recommendation read as source and rendered physical1850–1851. The investment argument retains all cost, useful-answer, recovery, graph and adoption qualifications.'])]:
  prior=B/'decision-synthesis-074'/f'component-renewal-{ch:03d}.json';x=read(prior);context=next(r for r in manifest['chapters']if r['chapter']==ch)
  x.update(recorded_utc=datetime.now(timezone.utc).isoformat(),batch=69,edit_numbers=edits,source_context=dict(extract=context['extract'],sha256=context['sha256']),reviewed_source_bindings=context['source_bindings'],rendered_text=bind(O/rendered),numerics=bind(O/'verified-numerical-verification.json'),publication=a['publication']['full'],prior_component_review=bind(prior),findings=findings)
  p=O/f'component-renewal-{ch:03d}.json';save(p,x);components.append(bind(p))
  positions=[i for i,r in enumerate(c['exact_component_renewals'])if read(R/r['path'])['chapter']==ch];assert len(positions)==1;c['exact_component_renewals'][positions[0]]=bind(p)
 review=dict(recorded_utc=datetime.now(timezone.utc).isoformat(),batch=69,edits=list(range(204,212)),components=components,publication=a['publication'],
  source_text_check=bind(O/'source-text-check.json'),rendered=[bind(O/n)for n in ['opening-rendered.txt','evidence-rendered.txt','recovery-rendered.txt','investment-rendered.txt']],
  findings=['The reading guide and evidence synthesis now point to completed scientific arguments and their economic consequences without removing earlier navigation or studies.',
    'The semantic replacement preserves all four substantive limits: bounded single treatment, no demonstrated bank recovery, no general longitudinal solution and no operating acceptance.',
    'Exact post-build audit retains inherited input order, mathematics, numeric facts, labels and citations. No new mathematical expression or empirical result enters this batch.',
    'Sponsor source and PDF are byte-identical to the completely read batch067 sponsor.'],
  execution_repairs=read(O/'integration.json')['execution_repairs']+['A rendered-title locator also matched the contents page; the specific first prose sentence selected the actual reading-guide page. No incorrect review record was created.',
    'A focused regression guard now rejects control bytes and the observed normalized broken-reference pattern before build and during audit. Its positive and negative fixtures pass.'],
  scope='Complete opening-guide and chapter32 author readings; exact cumulative component renewals for chapters14/101. No fresh whole-book, visual or independent acceptance.',acceptance=dict(author_component=True,fresh_visual=False,independent=False,release_accepted=False))
 save(O/'contextual-review.json',review);c['current_snapshot']=str((B/'context-review-211/manifest.json').relative_to(R));save(B/'changed-context-review.json',c)
 assert c['sponsor_review']['publication']['sha256']==a['publication']['sponsor']['sha256']
 x=read(O/'integration.json');x.update(status='verified_in_author_scope',batch=69,review=bind(O/'contextual-review.json'));save(O/'integration.json',x)
 subprocess.run(['python3','tools/reconcile_release_review_currency_20261029.py'],cwd=R,check=True)
 currency=read(B/'review-currency-current.json');scope=read(B/'review-scope-current.json');scope.update(batch=69,ledger_sha256=a['ledger_sha256'],publication=a['publication'],release_edits=211,edits=211,full_context_records=len(c['reviews']),numerical_groups=62,latest_contextual_review=str((O/'contextual-review.json').relative_to(R)),latest_rendered_review=str((O/'contextual-review.json').relative_to(R)),portable_package_current=False,numerical_package_current=False,
  scope='101 numbered chapters retain96 exact complete-context matches including two introductions,6 exact-component chains,one chapter47 chain and one preamble.109 author records are not109 unique chapters. No fresh whole-book, visual or independent acceptance.')
 for p in [B/'changed-context-review.json',B/'deletion-audit.json',B/'source-verification.json',B/'numerical-verification.json',B/'review-currency-current.json',B/'mathematical-addition-reviews.json',O/'contextual-review.json',O/'source-text-check.json']:scope['basis'][str(p.relative_to(R))]=sha(p)
 save(B/'review-scope-current.json',scope)
 (B/'review-scope-current.md').write_text('# Current author-review scope\n\nBatch069:211 exact edits;'+str(a['publication']['full']['pages'])+' reader pages and four sponsor pages. Opening navigation and chapter32 are completely reread; chapters14/101 have exact component renewals.109 author records cover101 numbered chapters through current exact contexts or explicit chains;62 numerical groups pass. Fresh visual and independent acceptance remain open.\n')
 p=R/'docs/program/release-programme-2026-10-29.md';s=p.read_text();start=s.index('## Current continuation');end=s.index('## Preserved continuation',start);shutil.copy2(p,O/'programme-before.md')
 replacement='''## Current continuation — verified batch069 and preservation review

The opening now directs readers to the completed sampling, recovery and
whole-study cost arguments. Chapter32 carries their implications into the
initial service comparison; the recovery conclusion states its scientific
result without an authoring-status recap. Batch069 contains211 exact edits,
with current contextual author coverage, source checks and post-build
preservation passing. The sponsor remains the fully read four-page version.
An observed reference-escaping defect was repaired and is now checked before
build; the intermediate batch068 is not accepted as reviewed.

Next, critically review the semantic deletion surface, especially replacements
of earlier recommendations and duplicate conclusions. Confirm that no important
assumption, adverse result or alternative has been lost. Review the remaining
source omissions at claim level and pursue a new primary route only where it
can change the recommendation. Continue targeted prose and reasoning review;
do not add repetitive summaries merely to enlarge the book.

Plan review: current109 author records cover101 numbered chapters through
exact context matches or explicit preserved-component chains. That evidence
does not establish an independent reader's assessment of the whole book.
Compilation, source counts and arithmetic cannot certify its voice. Reserve
01:58:35 UTC for final integration and actual package relocation; delivery
remains02:58:35 UTC. Fresh visual and independent editorial acceptance remain
open, as do bank, native and operating qualification.

''';p.write_text(s[:start]+replacement+s[end:])
 subprocess.run(['python3','tools/refresh_release_controls_20261029.py'],cwd=R,check=True)
if __name__=='__main__':main()

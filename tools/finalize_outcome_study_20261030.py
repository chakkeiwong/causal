"""Record completed source-bound author review and update scientific pointers."""
from pathlib import Path
import json,datetime,hashlib
O=Path('docs/twelve-hour-closure/2026-10-29')
def read(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,indent=2)+chr(10))
def art(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
v=read(O/'outcome-publication/revision-3/publication-1/verification.json');assert v['status']=='pass'
review=dict(created_utc=now,status='pass_with_limits',scope='Author mathematical,source,numerical and rendered review;not independent acceptance',
 publications=v['publications'],source_support=art(O/'outcome-source-support.json'),
 studies=[art(p)for p in sorted((O/'outcome-audit-attempt-2').glob('*/result.json'))]+[art(p)for p in sorted((O/'outcome-audit-precision-attempt-1').glob('*/result.json'))]+[art(p)for p in sorted((O/'outcome-audit-budget-attempt-1').glob('*/result.json'))],
 independent_checks=[art(O/'outcome-audit-summary-check.json'),art(O/'outcome-audit-budget-attempt-1/independent-check.json')],
 mathematical_review=['Conditional expectation and variance for known random completed recovery.','Sequential score telescoping conditional on independent pilot.','Known-design cross-fit asymptotic expansion and pooled variance under score L2 convergence.','Cost derivative and conditional square-root allocation;untested allocation clearly separated.'],
 visual=dict(short_pages=list(range(1,11)),method='v2 pages1–8 viewed;v3 first6 pages pixel-identical;changed pages7–10 viewed',integrated_pages=list(range(100,110)),section='14.4',section_pdf_pages=list(range(101,109)),findings='Readable equations,tables,figures,citations,headings and entry/exit;no detected clipping or overlap.'),
 preservation=dict(inherited_files=499,inherited_inputs=463,changed_inherited_files=[]),
 limits=['3500 new generated replications are conditional evidence,not bank data.','Full recovery needs truthful complete missing histories and nonselective completion.','Known action/recovery probabilities,fixed policies,IID customers;estimated designs and dependent sampling unresolved.','No exact finite-sample95%coverage or global optimal allocation claim.','No price/ROI claim;equal realized collection resources do not price computing or administration.','Prototype and independent acceptance remain later.'])
p=O/'outcome-author-review.json';assert not p.exists();save(p,review)
pp=Path('docs/program/scientific-priorities.json');d=read(pp);a=d['active_twelve_hour_campaign']
a.update(last_completed='Random-history recovery,independent-pilot precision and equal-resource cross-fitting study:3500 replications integrated',last_evidence=str(p),reader=v['publications']['full'],short_study=v['publications']['short'],next='Continue consequential source/software comparisons and public-data proposal evidence;preserve scoped uncertainty and collection limits.')
for item in d['items']:
 if item['id']in ['S01','S03']:
  item['latest_recovery_study']=dict(review=str(p),section='14.4',result='Known random recovery repairs outcome-dependent dropout;equal-resource cross-fit width1.512 vs3.272,coverage94.4%in500 adverse replications;asymptotic conditions explicit.')
  if str(p)not in item['evidence']:item['evidence'].append(str(p))
save(pp,d)
cp=O/'checkpoint.json';c=read(cp);c.update(updated_utc=now,publications=v['publications'],last_completed=a['last_completed'],next=a['next'])
c.pop('active_work',None);c['do_not_repeat'].append('Completed random-recovery3500replications,three designs,source comparison andcross-fit derivation;no need to rerun.')
save(cp,c)
mp=Path('docs/program/master-live.md');s=mp.read_text();start=s.index('<!-- financing-continuation:start -->');end=s.index('<!-- financing-continuation:end -->')+len('<!-- financing-continuation:end -->')
block='''<!-- financing-continuation:start -->
## Scientific continuation: information, uncertainty and decision value

[Integrated scientific reader](../causal_banking_closure_integrated_v13_2026-10-30.pdf) · [Ten-page recovery study](../causal_banking_outcome_recovery_v3_2026-10-30.pdf) · [Graph study](../causal_banking_graph_uncertainty_v3_2026-10-30.pdf) · [Evidence](../twelve-hour-closure/2026-10-29/README.md).

The 1,911-page scientific successor preserves the batch015 lineage and the financing, discovery, text-signal and graph-confidence additions. Section14.4 (PDF101–108) now develops random recovery of missing customer histories, its exact information-variance tradeoff, independent-pilot assistance and equal-resource cross-fitting. Three new designs contain3,500 generated replications. Under outcome-dependent dropout, equal-resource cross-fitting reduces interval width from3.272 to1.512 with the same7,000 initial records and about1,086 recovered histories;coverage94.4%remains reported,not declared a finite-sample guarantee. A known-design asymptotic argument accompanies the experiment.

The ten-page study and integrated pages100–109 have source-bound author review and visual inspection. All499 inherited files and463 input occurrences remain unchanged;layout,references and all-page text bounds pass. The original frontier census remains90 inspected dispositions:89 retained with limits,one quarantined,and23 unread. New follow-up sampling sources are separate support,not inflation of that census. Truthful complete recovery,estimated assignment laws,dependence,independent acceptance and bank validation remain open. The concurrent release programme retains its own lineage. This campaign remains active through30October2026,11:00:01Asia/Shanghai.
<!-- financing-continuation:end -->'''
mp.write_text(s[:start]+block+s[end:])
p=O/'README.md';s=p.read_text();p.write_text('''## Latest scientific delivery: recovering missing customer histories

Current scientific reader: docs/causal_banking_closure_integrated_v13_2026-10-30.pdf (1,911pages). Focused reading: docs/causal_banking_outcome_recovery_v3_2026-10-30.pdf (tenpages). Section14.4,PDF101–108,contains the recovery derivation,3,500 generated replications,the equal-resource comparison,and a known-design cross-fit asymptotic argument. See outcome-author-review.json,outcome-source-support.json,outcome-crossfit-derivation.md and the three outcome-audit study folders. Earlier sources,PDFs and results remain preserved. No bank qualification or universal95%coverage claimed.

'''+s)
print(json.dumps(dict(status='active',publications=v['publications'],review=str(O/'outcome-author-review.json'),concurrent_release_block_preserved=True)))

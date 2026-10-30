"""Publication-bound author review and scoped scientific programme refresh."""
from pathlib import Path
import json,datetime,hashlib,shutil

O=Path('docs/twelve-hour-closure/2026-10-29')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def read(p):return json.loads(p.read_text())
def save(p,d):p.write_text(json.dumps(d,indent=2)+chr(10))
def art(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
v=read(O/'graph-publication/revision-3/publication-1/verification.json')
assert v['status']=='pass'
review={
 'created_utc':now,'scope':'Author source, algebra, numerical, preservation and rendered review; not independent acceptance',
 'status':'pass_with_limits','publications':v['publications'],
 'source_support':art(O/'graph-source-support.json'),
 'study':art(O/'graph-confidence-attempt-1/result.json'),
 'economic_amendment':art(O/'graph-confidence-attempt-1/economic-check-v2.json'),
 'review_amendment':art(O/'graph-review-amendment.json'),
 'findings':[
  'Original bound direction checked visually against thesis PDF67; equations17–19 checked PDF69.',
  'Four-point KL and binary branch counterexamples separate mathematical necessity from sufficiency.',
  'Eight rational cycle configurations enumerated; no allegation thesis actual draws were cyclic.',
  '2000 Gaussian replications retained; QR checks first, middle, last; confidence-set union proof reviewed.',
  'Inherited identification example explicitly referenced; new contribution is coverage/IoU interpretation; illustrative economics aligned.',
  'Source limitations retained; public-code reproduction limits and source-version differences explicit.',
  'Alcala original quarantined on specific identity/sample/repository discrepancies; no allegation of intent.'],
 'visual':{'short_pages':list(range(1,10)),
   'method':'v2 all9 pages visually inspected; v3 pages1–6,8–9 pixel-identical; changed page7 visually inspected',
   'integrated_pages':list(range(1268,1277)),'section':'69.30','section_pdf_pages':list(range(1268,1275)),
   'findings':'Readable equations, table, figure, headings, citations and transitions; no clipped content or detected overlap.'},
 'preservation':{'inherited_files':493,'inherited_inputs':462,'changed_inherited_files':[]},
 'remaining':['General calibrated graph/effect uncertainty','Complete external workflow reproduction',
              'Live LLM and bank validation','Independent scientific/editorial acceptance']}
p=O/'graph-author-review.json';assert not p.exists();save(p,review)

invp=Path('docs/scientific-gap-closure/2026-10-29/remaining-inventory.json')
inv=read(invp);shutil.copyfile(invp,O/'inventory-before-graph-uncertainty.json')
ids={'LA01-candidate-136','LA01-candidate-202'}
found=[x for x in inv['frontier_unread'] if x['id'] in ids];assert len(found)==2
inv['frontier_unread']=[x for x in inv['frontier_unread'] if x['id'] not in ids]
counts={'inspected':90,'retained_with_limits':89,'quarantined_after_inspection':1,'unread':23,
 'basis':str(O/'graph-source-support.json'),
 'meaning':'Inspected counts source dispositions, not90 accepted technical supports. One newly inspected original is quarantined.',
 'historical_counts_preserved':True}
inv['current_frontier_counts']=counts
inv['graph_uncertainty_followup']={
 'sources':[{'id':'LA01-candidate-136','disposition':'retained_with_methodological_limits'},
            {'id':'LA01-candidate-202','disposition':'quarantined_for_quantitative_and_survey_support'}],
 'source_support':str(O/'graph-source-support.json'),'publication':v['publications']['full'],
 'section':'69.30','review':str(p)}
save(invp,inv)

pp=Path('docs/program/scientific-priorities.json');d=read(pp)
d['frontier_current']={**counts,'audit':str(O/'graph-source-support.json')}
d['remaining_inventory']=str(invp)
a=d['active_twelve_hour_campaign']
a.update(last_completed='Graph-confidence source comparison, exact bound/cycle examples and2000-replication effect-set study integrated',
 last_evidence=str(p),reader=v['publications']['full'],short_study=v['publications']['short'],frontier_current=counts,
 next='Pursue remaining original routes and develop a constructive information-design comparison; continue independent proposal work.')
for t in d['tasks']:
 if t['id']=='FRONTIER-ORIGINALS':
  t['action']='90 sources inspected:89 retained with limits,1 quarantined;23 unread. Graph-confidence thesis and Alcala exclusion integrated. Continue distinct legitimate original routes.'
  if str(p) not in t['evidence']:t['evidence'].append(str(p))
for item in d['items']:
 if item['id']=='S02':
  item['latest_progress']='Financing, discovery-sampling, text-signal and graph-confidence studies integrated; census90 inspected(89 retained,1 quarantined),23 unread. No live-model benefit claimed.'
  if str(p) not in item['evidence']:item['evidence'].append(str(p))
save(pp,d)
cp=O/'checkpoint.json';c=read(cp)
c.update(updated_utc=now,publications=v['publications'],counts=counts,last_completed=a['last_completed'],next=a['next'])
c['do_not_repeat'].append('Completed graph-confidence counterexamples and2000 Gaussian replications; source/version audit reviewed')
save(cp,c)

p=Path('docs/program/master-live.md');s=p.read_text()
start=s.index('<!-- financing-continuation:start -->')
end=s.index('<!-- financing-continuation:end -->')+len('<!-- financing-continuation:end -->')
block='''<!-- financing-continuation:start -->
## Scientific continuation: from signals to defensible decisions

[Integrated scientific reader](../causal_banking_closure_integrated_v10_2026-10-30.pdf) · [Nine-page graph study](../causal_banking_graph_uncertainty_v3_2026-10-30.pdf) · [Seven-page text study](../causal_banking_text_signals_v3_2026-10-30.pdf) · [Evidence](../twelve-hour-closure/2026-10-29/README.md).

The 1,904-page scientific successor preserves the batch015 lineage and adds financing identification, finite-sample discovery, text signals versus policy effects, and graph confidence (section69.30, PDF1268–1274). The new source comparison distinguishes a ceiling on success from a calibrated arrow probability. Exact examples show the cost of conditioning away cycles, while2,000 generated datasets show95.7% versus0% coverage under observationally identical causal worlds. Retaining both graphs preserves the relevant effect possibilities; general validity still requires declared graph-retention and estimation guarantees.

The nine-page study and affected integrated pages have source-bound author review and visual inspection. All493 inherited files and462 input occurrences remain unchanged; layout, references and all-page text bounds pass. Source dispositions now total90 inspected:89 retained with limits,one quarantined for quantitative support,and23 unread. These are not90 accepted scientific results. Complete external implementation,general calibration,independent acceptance and bank validation remain separate. The concurrent release programme retains its own lineage. This campaign remains active through30October2026,11:00:01Asia/Shanghai.
<!-- financing-continuation:end -->'''
p.write_text(s[:start]+block+s[end:])
p=O/'README.md';s=p.read_text()
p.write_text('''## Latest scientific delivery: graph uncertainty

The current scientific reader is docs/causal_banking_closure_integrated_v10_2026-10-30.pdf (1,904pages). Focused reading: docs/causal_banking_graph_uncertainty_v3_2026-10-30.pdf (ninepages). Section69.30,PDF1268–1274,contains the source comparison, exact information/cycle examples,2,000-replication coverage study and constructive graph-to-effect guarantee. See graph-author-review.json,graph-source-support.json and graph-review-amendment.json.

Source census:90 inspected dispositions,89 retained with limits andone quarantined;23 originals remain unread. This count does not confer acceptance. The campaign continues; preserve earlier PDFs and experiments.

'''+s)
print(json.dumps({'reader':v['publications']['full'],'counts':counts,'status':'active','concurrent_release_block_preserved':True},indent=2))

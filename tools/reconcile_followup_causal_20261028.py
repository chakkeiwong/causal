"""Reconcile finite followup identities, distinct editions and integrated originals."""
from collections import Counter
from copy import deepcopy
import hashlib,json
from pathlib import Path
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings,transition
ROOT=Path(__file__).resolve().parents[1];DAY=ROOT/'docs/program/execution/2026-10-28'
BASE=DAY/'followup-causal-review-v1';QUEUE=DAY/'followup-identity-reconciliation-v1';PRIOR=DAY/'causal-modeling-lead-v1';READER=DAY/'followup-causal-reader-v1';RAW=ROOT/'docs/literature/raw'
read=lambda p:json.loads(p.read_text())
def main():
 for p in [BASE/'review.json',QUEUE/'review.json',READER/'working-release.json',PRIOR/'census-register.json']:verify_bindings(read(p))
 rows=deepcopy(read(QUEUE/'followup-lead-register.json'));metadata=[]
 for i in [0,1,2,4,14,16,23,27,46,88,89]:
  receipt=read(RAW/('exec28_followup_identity_'+str(i)+'.receipt.json'));p=ROOT/receipt['path'];assert receipt['status']=='saved' and hashlib.sha256(p.read_bytes()).hexdigest()==receipt['sha256'];d=read(p);row=rows['rows'][i];wanted=row['discovery_doi']
  returned=(d.get('doi') or '').lower().removeprefix('https://doi.org/');linked=any(wanted in str(loc).lower() for loc in d.get('locations',[]))
  assert wanted==returned or linked,(i,wanted,returned)
  finding=dict(index=i,requested_doi=wanted,returned_doi=returned,identity_relation='same_primary_doi' if wanted==returned else 'metadata_cluster_links_distinct_doi_not_version_equality',metadata_date=d.get('publication_date'),metadata=ref(p,'Identity/date/routes only;no technical claim'),receipt=ref(RAW/('exec28_followup_identity_'+str(i)+'.receipt.json'),'Successful bounded lookup'),original_routes=[dict(pdf=x.get('pdf_url'),landing=x.get('landing_page_url')) for x in d.get('locations',[])],limits='Indexed January1may reflect year-only precision;exact original/version and cutoff still require primary evidence.')
  metadata.append(finding);row['new_metadata_review']=finding
  if i==4:row['next_action']='SSRN lookup maps to a metadata cluster with journal DOI10.1016/j.ijar.2026.109809;inspect each genuine edition and exact publication date before equality or claims.'
 for i in [1,21]:
  rows['rows'][i].update(disposition='related_selected_source_distinct_edition_unresolved',related_source_key='exec28_fr_ma',related_source_record=ref(BASE/'source-audit.json','Ma selectedarXiv2409.09822v1'),next_action='Use selected2024v1survey only;2025NAACLconference original and equality remain uninspected. Exact metadata links the candidate but does not prove edition equality.',effect_on_claims='Survey taxonomy and stated limits supported by selectedv1;conference-specific additions are not inferred.')
 rows['rows'][44].update(disposition='retained_selected_primary_version',source_key='exec28_fr_hu',source_record=ref(BASE/'source-audit.json','Hu selectedarXiv2505.19474v1'),selected_original=next(s['local_copy'] for s in read(BASE/'source-audit.json')['sources'] if s['integrated_citation_key']=='exec28_fr_hu'),selected_version='2505.19474v1;26May2025',next_action='Retain source-specific architecture/results/limits and qualified approximation discussion;native rights,artifacts and matched public tests remain separate.',effect_on_claims='Integrated selected-v1claims only;no bank-effect identification or native replication.')
 rows.update(predecessor=ref(QUEUE/'followup-lead-register.json','Complete95rowdispositions'),counts=dict(Counter(r['disposition'] for r in rows['rows'])),selected_primary_rows=13,unique_retained_primary_sources=10,new_originals=2,all_identities_reconciled=True,identity_reconciliation_scope='Explicit disposition and identity boundary for every row;unresolved identities and editions remain labelled,not equated.',coverage_closed=False)
 unresolved=[r for r in rows['rows'] if r['duplicate_metadata_identity_of'] is None and r['disposition'] not in {'retained_selected_primary_version','peripheral_metadata_screen_only'}];assert len(unresolved)==66
 rows['remaining_unique_acquisition_or_edition_obligations']=len(unresolved)
 write(BASE/'followup-lead-register.json',rows)
 write(BASE/'metadata-review.json',dict(status='pass_for_identity_routes_only',records=metadata,collector_exit_code=0,collector_session=91504,survey_followup_exit_code=0,original_reviews=ref(BASE/'review.json','Two genuine selected originals'),limitations=['No original supplied by most listed routes;no global unavailability assertion.','One DOI lookup coalesces distinct SSRN/journal identities;original equality unproved.','Publicationdate defaults do not upgrade year-only evidence.'],coverage_closed=False))
 reg=deepcopy(read(PRIOR/'census-register.json'));counts=Counter(x['disposition'] for x in reg['items'])
 action='All95followup rows now have explicit identity/disposition/task records:79distinct metadata identities,16duplicates,13rows bound to10retained selected originals,and66unique acquisition/edition obligations. Continue direct-source and longitudinal gaps using their recorded permitted-route/edition limits;do not repeat reviewed originals or unchanged failures. Prepare a bounded LL.CENSUS criterion review using explicit omission impacts,two-provider searches and citation chains;never require native or bank acceptance for literature disposition. Retain31unread inherited originals and independent L6/visual followups.'
 row=next(x for x in reg['items'] if x['id']=='LA01-longitudinal-search');row.update(later_leads=ref(BASE/'followup-lead-register.json','Complete finite queue with two integrated selected originals'),effect_on_claims='All95later records dispositioned with explicit versions/duplicates;66unique acquisition/edition questions remain. Ma survey and Hu representation source do not establish longitudinal bank identification or comprehensive frontier coverage.',next_action=action)
 assert Counter(x['disposition'] for x in reg['items'])==counts
 reg.update(supersedes=ref(PRIOR/'census-register.json','Unchanged113inherited candidate dispositions'),changes=['Complete finite later-search reconciliation;two selected originals integrated without replacing inherited denominator.'],closure=False);write(BASE/'census-register.json',reg)
 run=controller.base;core=run.core;state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active'] is None
 note=dict(finding='Finite95rowqueue reconciled;Ma/Huoriginals and exact approximation witnesses integrated;explicit source editions,metadata precision and access limits preserved.',next_action=action,yield_reason='Independent substantive delta integrated;remaining source/coverage criteria stay explicit.',evidence=[state['execution_program']['progress']['LL.CENSUS'][-1],ref(BASE/'review.json','Two primary originals and exact examples'),ref(BASE/'followup-lead-register.json','Complete later-source queue'),ref(BASE/'metadata-review.json','Observed routes and dates'),ref(BASE/'census-register.json','Original113preserved'),ref(READER/'working-release.json','Integrated argument'),ref(Path(__file__),'Serial reconciliation')])
 write(BASE/'integrated-progress.json',note);digest=core.sha(ROOT/core.STATE);event=run.apply(ROOT,state,'start','LL.CENSUS',reason='Record finite identity queue and two source-specific integrations.');run.commit(ROOT,digest,state,event);transition('yield','LL.CENSUS',BASE/'integrated-progress.json')
 state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active'] is None
 write(BASE/'census-reconciliation.json',dict(status='pass',counts=dict(counts),census_dispositions_changed=0,new_scholarly_originals=2,followup_rows=95,unique_metadata_identities=79,remaining_unique_acquisition_or_edition_obligations=66,next_action=action,evidence=[ref(BASE/'integrated-progress.json','Saved durable continuation')]))
 print(json.dumps(dict(census=82,unread=31,followup_rows=95,remaining_unique=66)))
if __name__=='__main__':main()

"""Reconcile saved leads without promoting metadata to technical evidence."""
import ast, hashlib, json, re
from collections import Counter
from copy import deepcopy
from pathlib import Path
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[1]
DAY=ROOT/'docs/program/execution/2026-10-28'
BASE=DAY/'followup-identity-reconciliation-v1'
PRIOR=DAY/'causal-modeling-lead-v1/followup-lead-register.json'
AUDIT=DAY/'causal-modeling-reader-v1/reader/source-audit.json'
CENSUS=DAY/'causal-modeling-lead-v1/census-register.json'
EARLY=ROOT/'docs/program/execution/2026-10-13/llm-census/new-search-leads.json'
LATE=ROOT/'docs/program/execution/2026-10-25/longitudinal-specificity-v1/search-review.json'
read=lambda p:json.loads(p.read_text())
def ref(p,anchor):return dict(path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),anchor=anchor)
def write(name,data):
 p=BASE/name;assert not p.exists();p.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def doi(v):return (v or '').lower().removeprefix('https://doi.org/').removeprefix('http://dx.doi.org/')
def arxiv(v):
 m=re.search(r'(?:arxiv[.:/]|(?:abs|pdf)/)(\d{4}\.\d{4,5})(v\d+)?',v,re.I)
 return m.group(1) if m else None
MATCH={11:'exec17_benchmark_cherif',32:'pearl2009',43:'v12_la_2402_01454',49:'v12_la_2410_06392',51:'pearl2009',52:'exec28_cm_razouk',55:'v12_la_2407_19118',62:'pearl2009',67:'exec13_census_collaboration',78:'exec28_cm_razouk',84:'v12_la_2305_00050',91:'exec15_latent_yu'}
RELATED={37:'exec21_cxx_hahn',47:'exec19_surveys_evaluation',66:'peters2017',68:'exec13_census_collaboration',90:'exec21_cxx_hahn'}
GROUPS=[([0,1,4,20,21,25,26,27,28,29,30,31,32,34,48,50,51,53,54,59,61,62,63,64,65,70,73,74,75,77,79,80,82,87,92,93],['identification','business_translation']),([2,10,13,22,23,43,46,84,91],['iid_discovery','diagram_construction','expert_evidence']),([3,6,14,33,35,36,38,60,71,85,86,88,89],['longitudinal_policy','estimation_validation']),([5,7,52,66,72,76,78,81,83],['variable_ontology','identification']),([11,12,15,16,17,18,19,24,39,40,41,42,44,45,47,49,55,57,58],['evaluation_cost','agent_architecture']),([37,56,90],['estimation_validation']),([67,68],['longitudinal_policy','business_translation','agent_architecture']),([8,9,94],['data_code']),([69],['latent_temporal_discovery','identification'])]
DIRECT={0,1,2,4,10,11,13,14,16,20,21,22,23,27,30,43,44,46,48,49,50,52,55,60,64,67,68,78,84,88,89,91}
EVALUATION={12,15,17,18,19,24,39,40,41,42,45,47,57,58}
def main():
 plan=read(BASE/'plan-review.json');assert plan['status']=='pass'
 for b in plan['evidence']:assert hashlib.sha256((ROOT/b['path']).read_bytes()).hexdigest()==b['sha256']
 rows=deepcopy(read(PRIOR)['rows']);early=read(EARLY)['leads'];late=read(LATE);metadata=early+late['candidates'];assert len(rows)==len(metadata)==95
 sources={s['integrated_citation_key']:s for s in read(AUDIT)['sources']};census=read(CENSUS)['items']
 mapping={i:t for ids,t in GROUPS for i in ids};assert set(mapping)==set(range(95))
 tree=ast.parse((ROOT/'tools/public_sources.py').read_text());hosts=ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='HOSTS' for t in n.targets)))
 cache={};seen={};genuine=set()
 def raw(p):
  if str(p) not in cache:cache[str(p)]=read(p)
  return cache[str(p)]
 for i,(row,meta) in enumerate(zip(rows,metadata)):
  assert row['title']==meta['title']
  if i<60:
   binding=meta['source'];p=ROOT/binding['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==binding['sha256'];n=int(re.search(r'\[(\d+)\]',binding['anchor']).group(1));data=raw(p);item=(data.get('results') or data['message']['items'])[n]
  else:
   matches=[]
   for q in late['queries']:
    p=ROOT/q['source']['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==q['source']['sha256'];matches.extend((p,n,s) for n,s in enumerate(raw(p)['results']) if s['id']==meta['id'])
   assert matches; p,n,item=matches[0];binding=ref(p,'results['+str(n)+'];id='+meta['id'])
  d=doi(meta.get('doi'));provider=meta.get('provider_identity',meta.get('id'));identity=d or provider;assert identity
  duplicate=seen.get(identity);seen.setdefault(identity,i);date=meta.get('date',meta.get('date_metadata'))
  row.update(queue_index=i,discovery_doi=d or None,metadata_identity=provider,metadata_date=date,metadata_evidence=binding,task_families=mapping[i],mapping_basis='Manual metadata screening; no technical text inference.',duplicate_metadata_identity_of=duplicate,identity_and_version_equality=False,cutoff_status='date_precision_insufficient' if isinstance(date,dict) and date.get('date-parts')==[[2026]] else 'metadata_pre_cutoff_original_version_requires_verification',scope='direct_causal_language_agent' if i in DIRECT else 'adjacent_evaluation' if i in EVALUATION else 'peripheral_metadata_screen' if i in {8,9,94} else 'background_or_specialist_causal_methods',technical_claims_admitted=[],original_inspected_in_this_audit=False)
  urls=[s.get(k) for s in item.get('locations',[]) for k in ['pdf_url','landing_page_url'] if s.get(k)]+[s['URL'] for s in item.get('link',[]) if s.get('URL')]+[s.get(k) for s in meta.get('original_locations',[]) for k in ['pdf','landing'] if s.get(k)]
  row['recorded_routes']=[dict(url=u,within_fixed_collector=urlsplit(u).scheme=='https' and urlsplit(u).hostname in hosts) for u in dict.fromkeys(urls)]
  row['effect_on_claims']='No technical,score,superiority or completeness claim from metadata.'
  if i in MATCH:
   s=sources[MATCH[i]];sid=str(s.get('source_identity',s.get('url','')));same_doi=d and d==doi(s.get('doi',sid if 'doi.org/' in sid else None));same_arxiv=arxiv(d) and arxiv(d)==arxiv(sid);assert same_doi or same_arxiv,(i,d,sid)
   p=ROOT/s['local_path'];assert p.read_bytes().startswith(b'%PDF-');assert hashlib.sha256(p.read_bytes()).hexdigest()==s['sha256'];genuine.add(MATCH[i])
   row.update(disposition='retained_selected_primary_version',source_key=MATCH[i],source_record=ref(AUDIT,'sources[key='+MATCH[i]+']'),selected_original=ref(p,'Previously inspected genuine original; exact bytes reverified'),selected_version=s.get('arxiv_version',s.get('version_date',s.get('version_status'))),identity_basis='Exact normalized DOI' if same_doi else 'Exact arXiv base identifier; selected version retained',next_action='Use only audited selected version and inspected claims; index record does not establish byte equality or edition completeness.',effect_on_claims='Existing selected-version claims retained without extension.')
  elif i in RELATED:
   row.update(disposition='related_selected_source_distinct_edition_unresolved',related_source_key=RELATED[i],related_source_record=ref(AUDIT,'sources[key='+RELATED[i]+']'),next_action='Acquire exact indexed edition or establish identity from primary version text; existing preprint/book evidence does not establish equivalence.')
  elif i in {10,30,48,50,64}:
   cid='LA01-candidate-27' if i==10 else 'LA01-candidate-202';s=next(s for s in census if s['id']==cid);assert (d and d==doi(s.get('discovery_doi'))) or provider==s['candidate_identity']
   row.update(disposition='inherited_original_access_limit',inherited_candidate=cid,original_limit=ref(CENSUS,'items[id='+cid+'];source-access limits'),next_action=s['next_action'],effect_on_claims=s['effect_on_claims'])
  elif i in {8,9,94}:
   reasons={8:'Poetic composition analogy; saved metadata identifies no causal-agent intervention task.',9:'Hyperparameter optimization; sequential does not itself identify longitudinal causal inference.',94:'Generic few-shot review; saved metadata identifies no causal-inference task.'}
   row.update(disposition='peripheral_metadata_screen_only',rationale=reasons[i],next_action='Revisit if primary abstract or cited connection identifies a causal-agent task; no full-text exclusion claimed.')
  else:
   permitted=any(u['within_fixed_collector'] for u in row['recorded_routes']);row.update(disposition='uninspected_source_with_permitted_route' if permitted else 'uninspected_source_requires_distinct_permitted_route',next_action='Inspect genuine versioned original before citation; verify cutoff,using distinct permitted routes without repeating failed requests.' if permitted else 'Seek distinct permitted author/archive original and exact date. Outside-policy hosts are local limits,not proof of global unavailability.')
 counts=dict(Counter(r['disposition'] for r in rows));unique=len(seen)
 write('followup-lead-register.json',dict(status='all_saved_rows_dispositioned_not_all_originals_inspected',rows=rows,counts=counts,total_rows=95,unique_metadata_identities=unique,duplicate_rows=95-unique,selected_primary_rows=len(MATCH),unique_retained_primary_sources=len(genuine),new_originals=0,predecessor=ref(PRIOR,'All95rows preserved'),current_audit=ref(AUDIT,'Selected source identities'),coverage_closed=False,canonical_changes=False))
 queue=[dict(index=r['queue_index'],identity=r['discovery_doi'] or r['metadata_identity'],scope=r['scope'],disposition=r['disposition'],next_action=r['next_action']) for r in rows if r['duplicate_metadata_identity_of'] is None and r['disposition'] not in {'retained_selected_primary_version','peripheral_metadata_screen_only'}]
 write('acquisition-queue.json',dict(rows=queue,priority='Direct causal-agent and specialist longitudinal gaps before general background; suppress metadata duplicates and unchanged failed routes.',coverage_closed=False))
 write('review.json',dict(status='pass_for_finite_queue_reconciliation_not_literature_closure',evidence=[ref(p,'Reviewed exact input/output') for p in [PRIOR,AUDIT,CENSUS,EARLY,LATE,Path(__file__),BASE/'plan-review.json',BASE/'followup-lead-register.json',BASE/'acquisition-queue.json']],counts=counts,total_rows=95,unique_metadata_identities=unique,checks=['All95rows preserved with explicit tasks,dispositions,cutoff limits and next actions.','DOI/arXiv matching and exact PDF hashes required; title similarity does not admit a source.','Journal/conference and preprint identities remain distinct.','No new technical claims,native results or coverage acceptance inferred.'],canonical_changes=False,visual_acceptance=False,final_acceptance=False))
 print(json.dumps(dict(rows=95,unique_metadata_identities=unique,counts=counts,new_originals=0)))
if __name__=='__main__':main()

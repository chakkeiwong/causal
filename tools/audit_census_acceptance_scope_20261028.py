"""Separate bounded literature disposition from later runtime qualification."""
import json,re
from collections import Counter
from pathlib import Path
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-28/census-acceptance-scope-v1'
read=lambda p:json.loads(p.read_text())

def main():
    assert not BASE.exists();BASE.mkdir()
    census=ROOT/'docs/program/execution/2026-10-28/linguistic-measurement-v1/census-register.json'
    audit=ROOT/'docs/program/execution/2026-10-28/linguistic-measurement-reader-v1/reader/source-audit.json'
    graph=ROOT/'docs/program/execution/2026-10-13/work-graph.json'
    old=ROOT/'docs/program/execution/2026-10-13/llm-census/new-search-leads.json'
    new=ROOT/'docs/program/execution/2026-10-25/longitudinal-specificity-v1/search-review.json'
    corpus=read(audit)['sources'];register=read(census);contract=next(n for n in read(graph)['nodes'] if n['id']=='LL.CENSUS')
    norm=lambda s:re.sub('[^a-z0-9]','',s.lower())
    index={}
    for s in corpus:index.setdefault(norm(s.get('title','')),[]).append(s['integrated_citation_key'])
    rows=[]
    for x in read(old)['leads']:
        rows.append(dict(origin='six_query_followup',id=x['id'],title=x['title'],identity=x.get('provider_identity',x.get('doi')),prior_disposition=x['disposition'],matching_title_keys=index.get(norm(x['title']),[]),identity_and_version_equality=False,source=ref(old,'leads[id='+x['id']+']')))
    for x in read(new)['candidates']:
        rows.append(dict(origin='specialist_four_query_followup',id=x['id'],title=x['title'],identity=x['id'],prior_disposition='metadata_candidate',matching_title_keys=index.get(norm(x['title']),[]),identity_and_version_equality=False,source=ref(new,'candidates[id='+x['id']+']')))
    write(BASE/'followup-lead-register.json',dict(status='identity_reconciliation_queue_not_technical_admission',rows=rows,counts=dict(Counter(x['origin'] for x in rows)),limits=['Exact normalized title only suggests a source match; versions and original bytes require explicit review.','This followup queue is separate from113inherited census candidates.','Existing chapter discussions and source dispositions remain unchanged.']))
    candidates=[x for x in register['items'] if x['id'].startswith('LA01-candidate-')]
    assert len(candidates)==113 and all(x.get('task_families') for x in candidates)
    families=sorted({f for x in candidates for f in x['task_families']});assert len(families)==14
    for path in [census,audit,old,new]:verify_bindings(read(path))
    findings=dict(status='pass_for_contract_diagnosis_not_census_acceptance',contract=contract,counts=dict(Counter(x['disposition'] for x in register['items'])),mapped_candidates=113,mapped_task_families=families,
      criteria_review=[dict(index=0,observation='All113inherited candidates have explicit dispositions and task mappings.31originals remain unread with affected claims restricted; genuine local primary records and acquisition limits must remain individually verified.',not_required='Successful installation or native performance qualification is not this literature-disposition criterion.'),dict(index=1,observation='Saved OpenAlex and Crossref routes and citation chains exist; specialist relevance and later discovered leads still require explicit reconciliation.',not_required='The contract prohibits treating bounded search as exhaustive proof; global saturation is not a permitted completion claim.')],
      actionable_gaps=['Reconcile60saved followup rows and35specialist candidates against current source identities; title matches are not version equality.','Review direct causal-modeling lead arXiv2411.15888v1 through its unattempted permitted route.','Preserve unresolved originals,selection limits and temporal metadata discrepancies; state exact claim impacts.','Give source-disposition,manuscript coverage,native qualification and later bank acceptance distinct outcomes.'],
      protections=['No recorded operation changed from inconclusive to pass.','No unread source marked inspected or excluded from full text.','No unobserved benchmark,cost or bank result supplied.','No external communication,host expansion or sibling edits.'],
      evidence=[ref(p,'Reviewed existing evidence') for p in [graph,census,audit,old,new,ROOT/'docs/program/repair-v12/work/LA01/search-ledger.json',ROOT/'docs/program/execution/2026-10-13/llm-census/search-ledger.json',ROOT/'docs/program/execution/2026-10-28/longitudinal-backward-chain-v1/metadata-review.json',BASE/'followup-lead-register.json',Path(__file__)]],canonical_changes=False,global_blocker=False,final_acceptance=False)
    verify_bindings(findings);write(BASE/'review.json',findings)
    print(json.dumps(dict(mapped_candidates=113,task_families=14,followup_rows=len(rows),acceptance_unchanged=True)))

if __name__=='__main__':main()

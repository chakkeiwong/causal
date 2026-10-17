#!/usr/bin/env python3
"""Recover later primary reviews without declaring unread originals closed."""
import copy
from collections import Counter
import json
from pathlib import Path
import master_control as core
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write

ROOT=core.ROOT;BASE=ROOT/'docs/program/execution/2026-10-17/census-recovery'
OLD=ROOT/'docs/program/execution/2026-10-13/llm-census'
AUDIT=ROOT/'docs/program/execution/2026-10-17/s9/publication-v4/reader/source-audit.json'
UPDATES={
 33:('exec14_expert_auditor','2026-10-14/expert-evidence'),
 35:('exec16_report_kimeconomy','2026-10-16/reporting-monitoring'),
 58:('exec14_iid_materials','2026-10-14/iid-discovery'),
 104:('exec14_l7_causalbench','2026-10-14/l7-benchmarking/frontier'),
 108:('exec14_l7_causalgraphbench','2026-10-14/l7-benchmarking/frontier'),
 128:('exec14_ident_counterbench','2026-10-14/llm-identification'),
 138:('exec16_report_flowfixer','2026-10-16/reporting-monitoring'),
 148:('exec15_latent_shi','2026-10-15/latent-temporal'),
 166:('exec17_ontology_thesis','2026-10-17/variable-ontology'),
 180:('exec15_latent_yu','2026-10-15/latent-temporal'),
 189:('exec17_ontology_kg_challenges','2026-10-17/variable-ontology'),
 196:('exec16_report_netops','2026-10-16/reporting-monitoring'),
 204:('exec17_ontology_annotation','2026-10-17/variable-ontology'),
 213:('exec14_expert_argumentation','2026-10-14/expert-evidence'),
 221:('exec14_ident_meter','2026-10-14/llm-identification'),
 239:('exec17_ontology_ontourl','2026-10-17/variable-ontology'),
 246:('exec16_report_psebench','2026-10-16/reporting-monitoring'),
 263:('exec15_latent_sthcm','2026-10-15/latent-temporal'),
 270:('exec17_ontology_sociology','2026-10-17/variable-ontology'),
 283:('exec17_ontology_kg_roadmap','2026-10-17/variable-ontology')}


def read(p):return json.loads(p.read_text())


def main():
    assert not BASE.exists();BASE.mkdir(parents=True)
    old=read(OLD/'census-register.json');verify_bindings(old)
    sources={s['integrated_citation_key']:s for s in read(AUDIT)['sources']}
    rows=copy.deepcopy(old['items']);by_id={r['id']:r for r in rows};changes=[]
    for number,(key,folder) in UPDATES.items():
        identifier=f'LA01-candidate-{number}';row=by_id[identifier];source=sources[key]
        assert source['kind']=='paper'
        paper=ROOT/(source.get('local_copy',{}).get('path') or source['local_path'])
        assert paper.parent==ROOT/'docs/papers' and paper.read_bytes().startswith(b'%PDF-')
        verify_bindings(source)
        later=ROOT/'docs/program/execution'/folder/'candidate-reassessment.json';review=read(later);verify_bindings(review)
        assert identifier in json.dumps(review)
        record=ref(later,'Explicit candidate disposition '+identifier)
        changes.append(dict(id=identifier,prior_disposition=row['disposition'],source_key=key,primary_pdf=ref(paper,'Authentic previously inspected original'),review=record))
        row['prior_disposition']=row['disposition'];row['disposition']='inspected_primary_retained_with_limits'
        row['technical_source_review_open']=False
        row['source_key']=key;row['primary_source_record']=source
        row['later_primary_review']=record
        row['availability']='Genuine original already acquired and inspected in the later review; no new acquisition in this reconciliation.'
        row['effect_on_claims']='Only the original inspected anchors and limits carry forward; no completeness, empirical superiority or integration approval is inferred.'
        row['next_action']='Retain bounded original claims and explicit version/rights/qualification limits. Do not reacquire merely because the old census was stale.'
    # Preserve later failures as route history, not a reversal of a verified original.
    for p in sorted((ROOT/'docs/program/execution').glob('*/**/candidate-reassessment.json')):
        if BASE in p.parents:continue
        data=read(p)
        for r in data.get('items',[]):
            identifier=r.get('id')
            if identifier not in by_id:continue
            disposition=r.get('disposition',r.get('current_disposition',''))
            if any(w in disposition.lower() for w in ['failed','unresolved','denied','not_acquired','incomplete','nonpdf','not_inspected','returned html']):
                row=by_id[identifier]
                row.setdefault('later_route_observations',[]).append(dict(disposition=disposition,reason=r.get('reason',r.get('limitation','')),evidence=ref(p,'Candidate '+identifier)))
    conflict=by_id['LA01-candidate-180']
    assert conflict['technical_source_review_open'] is False and conflict.get('later_route_observations')
    conflict['reconciliation_note']='October17 route failure is retained, but the genuine Yu2025 PDF and October15 inspection already exist. A failed duplicate route does not make the original unread or unavailable.'
    counts=dict(Counter(r['disposition'] for r in rows))
    assert len(rows)==117 and len(by_id)==117 and counts['inspected_primary_retained_with_limits']==32
    assert counts['open_original_not_inspected']==81
    write(BASE/'census-register.json',dict(status='incomplete_reconciled_primary_dispositions',cutoff='2026-10-07',counts=counts,items=rows,
        supersedes=ref(OLD/'census-register.json','Preserved12-inspected101-unread baseline'),changes=changes,
        evidence=[ref(AUDIT,'Canonical audited source records'),ref(Path(__file__),'Explicit identity-matched reconciliation')],
        closure=False,interpretation='32/113 candidate originals inspected;81 remain open. Four cross-cutting records remain separately classified. No new papers or search saturation claimed.'))
    tasks=[]
    for task in read(OLD/'task-map.json')['task_families']:
        row=copy.deepcopy(task);ids=set(row['inherited_ids'])
        row['uninspected_candidate_ids']=[r['id'] for r in rows if r['id'] in ids and r['disposition']=='open_original_not_inspected']
        row['inspected_candidate_ids']=[r['id'] for r in rows if r['id'] in ids and r['disposition']=='inspected_primary_retained_with_limits']
        row['inspected_source_keys']=sorted(set(row.get('inspected_source_keys',[]))|{r['source_key'] for r in rows if r['id'] in ids and 'source_key' in r})
        row['coverage_acceptance']=False;tasks.append(row)
    assert len(tasks)==14
    write(BASE/'task-map.json',dict(task_families=tasks,register=ref(BASE/'census-register.json','Reconciled117-item corpus'),
        mapping_does_not_establish_depth_or_completeness=True))
    write(BASE/'review.json',dict(status='pass_for_reconciliation_only',findings=[
        'All117 inherited records survive with unique IDs and14 task families.',
        'Twenty later original inspections update the stale tally from12 to32 inspected; unread candidates fall101 to81.',
        'Candidate180 duplicate-route failure is retained without undoing an existing authentic original.',
        'No research claim, new acquisition, exhaustive search or completed LL.CENSUS operation is inferred.'],
        evidence=[ref(BASE/'census-register.json','Exact reconciliation'),ref(BASE/'task-map.json','All14 task mappings')],closure=False))
    write(BASE/'progress.json',dict(finding='Reconciled20 later authentic primary reviews:32/113 candidate originals inspected,81 still open; all117 inherited records and14 task mappings preserved. Candidate180 duplicate-route failure corrected without erasing history.',
        next_action='Acquire and inspect priority candidates137,242,31 and27 from verified public primary routes; preserve failures. Tighten longitudinal/off-policy and negative-result searches using complementary routes and citation chaining. Do not record census closure until remaining candidates have evidence-backed dispositions.',
        evidence=[ref(BASE/'review.json','Reconciliation review'),ref(BASE/'census-register.json','Current remaining candidates'),ref(BASE/'task-map.json','Task-specific gaps')]))
    print(json.dumps(dict(items=117,inspected_candidates=32,unread_candidates=81,task_families=14,conflict_repaired='LA01-candidate-180',closure=False)))


if __name__=='__main__':main()

"""Reconcile L1 task claims and retain unknown essentiality of unread originals."""
import json
from pathlib import Path
from run_followup_program_20261028 import ROOT,BASE,append,load,bound
from prepare_followup_program_20261028 import ref,write

SPECS={
 'business_translation':(31,'Retrieval,heuristic extraction and interactive diagrams motivate a proposed translation workflow; usability is not causal validity.'),
 'variable_ontology':(166,'Context,recoding,missingness and uncertain links belong in variable definitions; ontology traces depend on supplied relations.'),
 'expert_evidence':(10,'Contradiction-based hallucination reduction is distinct from true-edge accuracy; supplied mocked graph information changes the experiment.'),
 'diagram_construction':(26,'Typed bowtie construction and thresholded semantic alignment support an extraction comparison,not a universal causal-DAG guarantee.'),
 'iid_discovery':(10,'The nine-variable edge-audit case and opposing debaters have a declared evidence scope; true-graph validation remains separate.'),
 'latent_temporal_discovery':(40,'Future-trend prediction,graph agreement and summary agreement do not identify intervention effects or hidden confounders; causal-sufficiency limits remain.'),
 'active_experiments':(139,'DISCERN levels are separately instantiated with level-specific rubrics; aggregate scores are not end-to-end discovery-success probabilities.'),
 'identification':(56,'Tool-assisted synthetic graph/effect tasks support bounded architecture evidence; variable/test/parameter errors and adapted baselines remain explicit.'),
 'data_code':(32,'Sequential external-test feedback and pass@n differ from independent pass@k; unit-test success does not establish target or leakage validity.'),
 'longitudinal_policy':(74,'Sequential text interventions and ISE rely on declared exchangeability/positivity and version mixtures; constructed counterfactual evidence is not bank policy validation.'),
 'estimation_validation':(25,'Validation scope follows the claim and unit of analysis; methodological guidance is not empirical causal-assistant qualification.'),
 'reporting_monitoring':(35,'Generated macroeconomic diagrams are explicitly questioned by the author; they cannot certify a monitoring or intervention pipeline.'),
 'agent_architecture':(19,'Profile,memory,planning and action organize a survey; its taxonomy is not primary implementation evidence for each constituent framework.'),
 'evaluation_cost':(0,'Admission,lineage,exposure and assertion adoption are distinct; policy-dependent streams and scoring truth require separate denominators.'),
}


def main():
    key='L1.ESSENTIALITY';node=load()['nodes'][key];day=ROOT/'docs/program/execution/2026-10-28';cbase=day/'census-criterion-review-v1'
    cp=cbase/'census-register.json';tp=cbase/'task-impact-matrix.json';ap=day/'delegate-contract-reader-v1/reader/source-audit.json'
    evidence=[ref(cp,'82inspected/31unread source register'),ref(tp,'14task mapping'),ref(ap,'Current integrated citation records')]
    start=BASE/'l1-essentiality-start.json';write(start,dict(task=key,awards_acceptance=False,next_action=node['action'],evidence=evidence));append('start',key,str(start.relative_to(ROOT)))
    census=json.loads(cp.read_text());byid={r['id']:r for r in census['items']};audit={s['integrated_citation_key']:s for s in json.loads(ap.read_text())['sources']}
    tasks=json.loads(tp.read_text())['tasks'];assert len(tasks)==len(SPECS)==14;rows=[]
    for task in tasks:
        number,claim=SPECS[task['task']];candidate=byid['LA01-candidate-'+str(number)]
        source=candidate.get('primary_source_record') or audit[candidate['source_key']]
        assert source['integrated_citation_key'] in audit and audit[source['integrated_citation_key']]==source
        bound(ROOT,source['local_copy'])
        rows.append(dict(task=task['task'],inspected_count=len(task['inspected_inherited']),unread_ids=task['unread_inherited'],followup_row_indices=task['followup_row_indices'],specific_supported_comparison=claim,support=dict(candidate=candidate['id'],citation_key=source['integrated_citation_key'],source_identity=source['source_identity'],version_date=source['version_date'],local_copy=source['local_copy'],inspected_anchors=source['inspected_anchors'],supported_claims=source['supported_claims']),coverage='inconclusive',essentiality_decision='Uninspected candidates cannot be declared dispensable by title. Current bounded comparison is supported; exhaustive/frontier coverage remains unproved.',next_action='Inspect missing primary originals or justify a bounded subject-scope decision using actual primary contents; keep edition gaps distinct.'))
    unread=[]
    for candidate in census['items']:
        if candidate['disposition']!='open_original_not_inspected':continue
        related=candidate.get('related_primary_source_record')
        edition=related is not None
        if related:bound(ROOT,related['local_copy'])
        unread.append(dict(id=candidate['id'],title=candidate['title'],tasks=candidate['task_families'],identity_evidence=candidate['metadata'],status='selected_original_unread',availability=candidate.get('availability'),exact_next_action=candidate['next_action'],essentiality='unresolved_requires_original_or_substantive_scope_review',gap_type='separate_journal_edition_with_inspected_related_preprint' if edition else 'missing_selected_primary_original',related_primary=related,current_claim_effect='No claim is transferred from the unread original. Related inspected version supports only its own audited claims.' if edition else candidate['effect_on_claims'],dropped_from_census=False))
    assert len(unread)==31 and len({r['id'] for r in unread})==31
    assert set().union(*(set(r['unread_ids']) for r in rows))=={r['id'] for r in unread}
    out=BASE/'l1-essentiality.json'
    write(out,dict(status='performed_task_claim_and_essentiality_review',tasks=rows,unread_candidates=unread,inspected_related_preprint_edition_gaps=sum(r['gap_type'].startswith('separate') for r in unread),all_task_coverage='inconclusive',evidence=evidence+[ref(Path(__file__),'Explicit14task comparison')],limitations=['Task mappings can overlap and are not additive.','Title/metadata establishes identity and search priority,not technical essentiality or harmless omission.','31unread originals remain; no new source acquired or coverage pass awarded.']))
    receipt=BASE/'l1-essentiality-receipt.json';write(receipt,dict(task=key,awards_acceptance=False,execution='performed',outcome='pass',outputs=[ref(out,'14task claims and31unread identities')],evidence=evidence,criteria=[dict(index=0,verdict='pass',finding='All14tasks and31unread identities accounted for; no metadata-only dispensability finding.'),dict(index=1,verdict='pass',finding='Bounded integrated claims bind inspected originals; related preprints and missing selected editions remain distinct.')],next_action='Use preserving L1 successor for the explicit current claims and omissions; new source acquisition must use a distinct permitted original route.'))
    append('record',key,str(receipt.relative_to(ROOT)));print(json.dumps(dict(tasks=14,unread=31,coverage='inconclusive',next=load()['next'])))


if __name__=='__main__':main()

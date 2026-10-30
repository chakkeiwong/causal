from pathlib import Path
from hashlib import sha256
import json
from collections import Counter

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/scientific-gap-closure/2026-10-29'
STATE=ROOT/'docs/program/scientific-priorities.json'

def relative(name):return 'docs/scientific-gap-closure/2026-10-29/'+name
def task(id,stream,question,action,result,status='ready',evidence=None,blockers=None,priority=1):
    return dict(id=id,stream=stream,question=question,action=action,required_result=result,status=status,
                evidence=evidence or [],blockers=blockers or [],depends_on=[],priority=priority)

def main():
    s=json.loads(STATE.read_text())
    if s.get('gap_closure_finalized'):
        from finalize_gap_program_20261029 import main as refresh_verified_results
        refresh_verified_results()
        return
    old=json.loads((ROOT/'docs/program/execution/2026-10-28/recovered-followups-v1/remaining-operations.json').read_text())
    census=json.loads((ROOT/old['census']['path']).read_text())
    cells=[]
    for row in old['operations']:
        if row['id'].startswith('SW.CELL.'):
            copy={k:row.get(k) for k in ['id','title','status','action','prerequisites','action_basis']}
            checkpoint=row.get('corrected_action_checkpoint')
            if checkpoint and (ROOT/checkpoint['path']).is_file():
                correction=json.loads((ROOT/checkpoint['path']).read_text())
                copy['corrected_action']=correction.get('next_action')
            copy['decision_consequence']='Compare capabilities only in the inspected regime; no full coverage inferred.'
            cells.append(copy)
    reuse=[{k:r.get(k) for k in ['id','title','status','action','prerequisites','action_basis','source_followup']}
           for r in old['operations'] if r.get('lane')=='reuse' and r.get('status')!='pass']
    unread=[]
    for row in census['items']:
        if row.get('disposition')!='open_original_not_inspected':continue
        title=row.get('title','');lower=title.lower()
        primary=any(w in lower for w in ['causal discovery','causal inference','causal reasoning','causality game','causal benchmark','bayesian network','financing'])
        unread.append(dict(id=row['id'],title=title,decision_priority='direct_causal' if primary else 'adjacent_or_version_reconciliation',
          action=row.get('next_action'),availability=row.get('availability'),
          acquisition_leads=row.get('inherited_record',{}).get('acquisition_leads',[]),
          consequence='No technical assertion from this unread original; retain bounded conclusions from inspected sources.'))
    inventory=dict(as_of='2026-10-29',basis='Preserved corrected inventory; no automatic acceptance or reclassification',
      historical_coverage=old['coverage'],software_cells=cells,unresolved_reuse_decisions=reuse,
      frontier_unread=unread,frontier_counts=census['counts'],
      priority_decisions=[
       dict(comparison='Linear-model estimation across R and Python',result='Executed matched rows and HC2 covariance; agreement within 1e-6',consequence='Reuse existing fitting, preserve explicit covariance; do not port merely for a language preference'),
       dict(comparison='DoubleML',result='Full pinned executable distribution not present in checked environments',consequence='A native comparison needs a scoped environment; independent project calculations do not substitute'),
       dict(comparison='did',result='Complete installed package/environment not available',consequence='Continue methodological panel study independently; do not certify a native adapter'),
       dict(comparison='causaleffect',result='Source outcome remains inconclusive',consequence='Graph/query failures need exact distribution tests before adapter claims'),
       dict(comparison='MATLAB, HUGIN and commercial causaLens profile',result='Primary/version/rights limits remain',consequence='Obtain named official artifacts or keep capability unknown; no absence claim'),
       dict(comparison='LLM repeated measurement',result='Shared error floor derived and checked',consequence='Evaluate independent information and consequential bias, not prompt agreement')])
    (OUT/'remaining-inventory.json').write_text(json.dumps(inventory,indent=2)+chr(10))
    tasks=[
      task('PUBLIC-EXPERIMENT','S03','Does a public experiment support an economically material effect?',
        'Preserve the completed NSW calculation and its conditional interpretation.','Public target, baselines, uncertainty, sensitivity and economic interpretation','complete',
        [relative('study-results.json'),relative('source-audit.json'),relative('public-study.tex')]),
      task('R-PYTHON-COMPARISON','S01','Does simple native fitting preserve this estimation specification across languages?',
        'Retain matched R/Python output; extend only for a consequential target.','Same-row coefficients and HC2 variances independently checked','complete',
        [relative('r-verification.json'),relative('r-comparison.csv')]),
      task('PUBLIC-INTERFACES','S04','Do interfaces preserve real fitted estimates and uncertainty?',
        'Retain the actual public-data summary path and contradicted-premise refusal.','Library, CLI and MCP equality, actual estimation scope and service limits','complete',
        [relative('interface-results.json'),relative('public-study.tex')]),
      task('MEASUREMENT-FLOOR','S02','When do repeated measurements remove a sign error?',
        'Use the checked common-error derivation to specify independent-measurement comparisons.','Exact formula, covariance check and consequential remedy','complete',
        [relative('measurement-results.json'),relative('measurement.tex')]),
      task('SEQUENTIAL-SERVICING','S03','Can repeated decisions be evaluated despite dropout?',
        'Retain four executed scenarios; next address valid uncertainty for fitted value models.','Independent selection, baseline, weighted and fitted estimates, uncertainty and adverse cases','complete',
        [relative('servicing-results.json'),relative('servicing-verification.json'),relative('servicing.tex')]),
      task('SOFTWARE-CONSEQUENTIAL','S01','Which unresolved comparisons could reverse a recommendation?',
        'Use remaining-inventory.json and exact corrected sources. Obtain essential commercial originals and disposition them; do not re-run delivered publication steps.',
        'Seventeen-area/six-dimension recommendations with transparent consequential limitations and source-vs-runtime distinction',
        evidence=[relative('remaining-inventory.json')],priority=2),
      task('FRONTIER-ORIGINALS','S02','Do remaining originals change the formulation, diagram or discovery conclusions?',
        'Inspect legitimate distinct originals in the direct-causal priority group; existing repeated failed routes remain recorded. Adjacent version reconciliation does not block synthesis.',
        'Individual source dispositions and primary-text comparison, with 82/31 historical count unchanged until new inspection',
        evidence=[relative('remaining-inventory.json')],priority=2),
      task('FUNDING-CONTINUITY','S03','How do changing economic units affect a panel estimate?',
        'Retain verified panel results; seek externally checked institution histories before an authentic application.',
        'Known-target panel study, simple within/pooled alternatives, uncertainty and break-aware interpretation','complete',
        evidence=[relative('funding-results.json'),relative('funding-verification.json'),relative('funding.tex')],priority=1),
      task('OBSERVATION-STUDY','S04','How does uncertain linkage alter an intervention conclusion?',
        'Complete the P5 observation example with truth physically separated from analyst inputs and honest interval/ambiguity propagation.',
        'End-to-end observation-to-effect example and explicit information requirements',
        evidence=['docs/program/public-data-v15/studies/P5/design.json'],priority=1),
      task('FITTED-POLICY-UNCERTAINTY','S03','Can fitted servicing estimates carry honest and useful uncertainty?',
        'Specify a trajectory-level resampling or valid analytic construction; include selection and censoring model uncertainty and compare with weighted intervals.',
        'Predeclared calibration and decision-width evidence, without promoting point-error results',priority=2),
      task('LIVE-MODEL-BENEFIT','S02','Does model assistance improve consequential errors and analyst time?',
        'Use fixed model/version, independent task adjudication, permitted held-out tasks and matched non-LLM baselines.',
        'Measured live benefit with cost and critical-error uncertainty','blocked',blockers=['Specified backend and permitted calls','Budget/prices','Independent adjudication and held-out custody']),
      task('EDITORIAL-ACCEPTANCE','E01','Does the full document satisfy the requested narrative and voice standard?',
        'Incorporate findings from the reviewer arranged by the user; continue science meanwhile.',
        'Independent editorial acceptance or concrete repairs','blocked',blockers=['External reviewer findings not yet supplied'])]
    # Preserve tasks completed by later runs of this programme.
    previous={x['id']:x for x in s.get('tasks',[])}
    for i,t in enumerate(tasks):
        if t['id'] in previous and previous[t['id']]['status']=='complete' and t['status']=='ready':tasks[i]=previous[t['id']]
    s['tasks']=tasks;s['active_gap_plan']='docs/program/scientific-gap-closure-2026-10-29.md'
    s['remaining_inventory']=relative('remaining-inventory.json')
    updates={
      'S01':('Matched R stats::lm and NumPy calculations on public experimental data agree within 1e-6; all historical cell outcomes retained.',
             ['r-verification.json','remaining-inventory.json'], 'Resolve consequential original/version/rights gaps across the 17 areas; no native causal-package qualification inferred.'),
      'S02':('Derived and checked the repeated-measurement shared-error floor; 20 exact cases. No live model benefit or new frontier original counted.',
             ['measurement-results.json','measurement.tex'],'Inspect distinct legitimate direct-causal originals and develop the independent-measurement experiment; 82 inspected/31 unread remains.'),
      'S03':('Executed the 445-person NSW public study, 800 generated sequential-servicing replications and 900 generated funding panels. Conditional positive public contrast is not sufficient at a 1000-unit hurdle; unobserved-future dropout breaks weighted coverage; fixed effects do not repair corrupted institution identities.',
             ['study-results.json','servicing-results.json','servicing-verification.json','funding-results.json','funding-verification.json'],'Complete observation and fitted-policy uncertainty studies; preserve conditional interpretations.'),
      'S04':('Three actual fitted public-data summaries give identical inference through library, CLI and MCP; contradicted assignment is refused. Raw-data fitting and report remain local scripts.',
             ['interface-results.json','public-study.tex'],'Complete remaining banking journey reports and consumer-specific calls; source reviews and local transport do not certify target platforms.')}
    for item in s['items']:
        if item['id'] in updates:
            progress,paths,nxt=updates[item['id']];item['latest_progress']=progress;item['next_action']=nxt
            item['evidence']=list(dict.fromkeys(item.get('evidence',[])+[relative(p) for p in paths]));item['status']='in_progress'
            item['closure_criteria']=['A scientific question answered with assumptions, alternatives, diagnostics and economic consequences.',
               'All consequential residual gaps explicitly dispositioned; neither source administration nor interface parity substitutes for science.']
    s['proposal_complete']=False;s['final_editorial_acceptance']=False
    s['approval_scope']=dict(installed='security/scientific-installation-20261029.json',
        collector='tools/scientific_sources_20261029.py fetch',actual_execution='Approved source batch succeeded',
        global_settings_changed=False,paid_calls=0,packages_installed=0)
    s['last_completed_batch']=dict(date='2026-10-29',result='Public causal study, native R/Python arithmetic comparison, actual three-interface inference, measurement-error derivation and generated sequential servicing',
        public_records=445,generated_replications=800,new_frontier_originals=0,external_causal_package_benchmark=False)
    s['unresolved_scientific_limits']=[
        dict(gap='Identity and assignment truth',remedy='Validated records, independent measurement or explicit error bounds'),
        dict(gap='Latent temporal graph ambiguity',remedy='Restrictions or interventions; retain effect sets'),
        dict(gap='General hidden-state and dependent-learning guarantees',remedy='Derive results for declared models; no universal remedy'),
        dict(gap='Intervals too imprecise for action',remedy='More informative design and observed outcomes; no assumption chosen merely for significance')]
    STATE.write_text(json.dumps(s,indent=2)+chr(10))
    print(json.dumps(dict(tasks=len(tasks),states=dict(Counter(t['status'] for t in tasks)),inventory_cells=len(cells),unread=len(unread))))

if __name__=='__main__':main()

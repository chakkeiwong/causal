"""Publish observed scientific progress without closing unresolved survey claims."""
from pathlib import Path
from hashlib import sha256
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/scientific-gap-closure/2026-10-29'
def rel(p):return str((OUT/p).relative_to(ROOT))
def main():
    statepath=ROOT/'docs/program/scientific-priorities.json';s=json.loads(statepath.read_text())
    if s.get('active_writing_plan'):
        from refresh_survey_continuation_20261029 import apply_state
        apply_state(s)
        statepath.write_text(json.dumps(s,indent=2)+'\n')
        print(json.dumps(dict(status='survey_delta_refreshed',writing_plan_preserved=True,reader=s.get('reader'))))
        return
    pub=json.loads((OUT/'publication-verification.json').read_text());source=json.loads((OUT/'frontier-source-audit.json').read_text())
    counts=source['inspection_delta']['current'];delta=source['inspection_delta']['newly_inspected']
    completed={
      'OBSERVATION-STUDY':dict(action='Retain the 1800-run observed-linkage study and derived exclusion-budget envelope; obtain defensible identity/support information before an actual bank interpretation.',evidence=['observation-plan.json','observation-results.json','additional-numerical-verification.json','observation.tex']),
      'FITTED-POLICY-UNCERTAINTY':dict(action='Retain the 300-run trajectory-bootstrap study: conditional baseline evidence and severe observation/model misspecification failures. Bank inference needs its own initial/reward law and observation argument.',evidence=['policy-uncertainty-plan.json','policy-uncertainty-results.json','new-results-verification.json','policy-uncertainty.tex'])}
    for t in s['tasks']:
        if t['id'] in completed:
            t.update(completed[t['id']]);t['evidence']=[rel(x) for x in t['evidence']];t['status']='complete'
        if t['id']=='FRONTIER-ORIGINALS':
            t['status']='in_progress';t['evidence']=[rel('remaining-inventory.json'),rel('frontier-source-audit.json'),rel('frontier.tex')]
            t['action']=f'{len(delta)} original inspections completed: '+', '.join(delta)+f'. Current count {counts["inspected"]} inspected/{counts["unread"]} unread. Resolve candidate136 complete-file transfer before inspection; continue distinct legitimate routes for remaining originals, not repeated rejected requests. Review adjacent candidates for materiality without erasing them.'
        if t['id']=='SOFTWARE-CONSEQUENTIAL':
            t['status']='in_progress';t['evidence']=[rel('remaining-inventory.json'),rel('frontier-source-audit.json'),rel('software-followup.tex')]
            t['action']='MATLAB panel and HUGIN decision/rights originals inspected as current dated documentation. Resolve pre-cutoff version dates and named commercial causaLens scope; reconcile remaining area-language proposal recommendations. Native adapter execution is later prototype evidence, not a blanket proposal blocker.'
    s['reader']={k:pub['documents']['integrated'][k] for k in ['sha256','pages']};s['reader']['pdf']=pub['documents']['integrated']['path']
    s['scientific_supplement']={k:pub['documents']['short'][k] for k in ['path','sha256','pages']}
    s['latest_verification']=rel('publication-verification.json')
    s['frontier_current']=dict(historical=dict(inspected=82,unread=31),current=counts,evidence=rel('frontier-source-audit.json'))
    s['last_completed_batch']=dict(date='2026-10-29',result='Public experimental study, R/Python fitting comparison, fitted-summary interfaces, measurement derivation, servicing/funding/linkage/uncertainty studies, three frontier originals and official vendor comparisons',
        public_records=445,generated_replications=3800,new_frontier_originals=len(delta),chapters_added=8,external_causal_package_benchmark=False)
    s['approval_scope'].update(frontier_installed='security/frontier-installation-20261029.json',frontier_collector='tools/gap_sources_frontier_20261029.py fetch',
        actual_execution='Both dedicated source commands executed successfully with approved escalation; sandbox-only DNS attempt failed and is preserved.',live_reload_verified=False)
    updates={
      'S01':('Native R/Python arithmetic checked; current MATLAB panel and HUGIN decision-information/rights documentation now inspected. Native integration and historical coverage not inferred.', 'Resolve consequential version/rights and named-profile gaps; retain 102-cell historical outcomes and declared prototype trials.', ['software-followup.tex','frontier-source-audit.json']),
      'S02':(f'Repeated-measurement common-error floor derived; {len(delta)} original papers newly inspected. Current census {counts["inspected"]}/{counts["unread"]}. No live benefit measured.', 'Inspect remaining distinct originals where accessible; use task-validity and independent-answer-key tests before a live assistant comparison.', ['frontier.tex','frontier-source-audit.json']),
      'S03':('NSW445 public observations and3800 new generated replications completed. Validity/precision, record identity and model misspecification each have checked decision consequences.', 'Use completed public/generated evidence to refine the bounded prototype; further bank inference requires justified observation, reward and economic-unit information.', ['funding-results.json','observation-results.json','policy-uncertainty-results.json','new-results-verification.json']),
      'S04':('Actual fitted summaries agree through library, CLI and MCP; generated observation-to-effect case carries linkage uncertainty into the decision. No native target-platform acceptance claimed.', 'Complete consumer-specific proposal comparisons where consequential; native package/consumer runtime qualification belongs to the funded prototype.', ['interface-results.json','observation.tex'])}
    for item in s['items']:
        if item['id'] in updates:
            progress,nxt,files=updates[item['id']];item['latest_progress']=progress;item['next_action']=nxt
            item['latest_delivery']=s['reader']['pdf'];item['evidence']=list(dict.fromkeys(item.get('evidence',[])+[rel(x) for x in files]))
    s['proposal_complete']=False;s['final_editorial_acceptance']=False;s['gap_closure_finalized']=True
    s['phase_distinction']=dict(proposal=['Source-grounded comprehensive comparisons','Banking narrative and reproducible public/generated evidence','Declared evaluation and conditional investment'],
       prototype=['Complete native distributions and target-system testing','Matched live assistant/analyst studies with budget and adjudication'],
       bank_validation=['Bank-specific assignment/identity/observation evidence','Actual costs, benefits, platform acceptance and adoption'])
    s['continuation_note']='No unattended worker. Ready material work remains in two independent survey streams; specific access/identity limits are recorded. Completed experiment stages must not be repeated as new progress.'
    from refresh_survey_continuation_20261029 import apply_state, apply_inventory
    apply_state(s)
    statepath.write_text(json.dumps(s,indent=2)+'\n')
    invpath=OUT/'remaining-inventory.json';inv=json.loads(invpath.read_text());done=set(source['inspection_delta']['newly_inspected'])
    allrows={x['id']:x for x in inv.get('new_frontier_inspections',[])+inv['frontier_unread']}
    inv['new_frontier_inspections']=[x for x in allrows.values() if x['id'] in done];inv['frontier_unread']=[x for x in allrows.values() if x['id'] not in done]
    inv['current_frontier_counts']=counts;inv['source_followup']=rel('frontier-source-audit.json')
    inv['prototype_obligations_not_proposal_blockers']=['Native DoubleML/did/causaleffect distributions and target-runtime tests','Vendor order-specific entitlement and numerical trials','Paid live-model comparison and bank data qualification']
    apply_inventory(inv)
    invpath.write_text(json.dumps(inv,indent=2)+'\n')
    manifest=dict(date='2026-10-29',git_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),dirty_workspace=True,
       environment=dict(python=sys.version,analysis_python='/home/ubuntu/miniforge3/bin/python',interface_python='/home/ubuntu/miniforge3/envs/tf-gpu/bin/python',R='4.1.2',hardware='CPU; no GPU or paid calls'),runs=[])
    for stem,runner in [('study','run_public_experiment'),('servicing','run_servicing_study'),('funding','run_funding_study'),('observation','run_observation_study'),('policy-uncertainty','run_policy_uncertainty')]:
        plan=OUT/(stem+'-plan.json');result=OUT/(stem+'-results.json');code=ROOT/('tools/'+runner+'_20261029.py');r=json.loads(result.read_text())
        manifest['runs'].append(dict(name=stem,command='/home/ubuntu/miniforge3/bin/python '+str(code.relative_to(ROOT)),plan=rel(plan.name),result=rel(result.name),
          plan_sha256=sha256(plan.read_bytes()).hexdigest(),code_sha256=sha256(code.read_bytes()).hexdigest(),result_sha256=sha256(result.read_bytes()).hexdigest(),
          seeds=json.loads(plan.read_text()).get('seeds',json.loads(plan.read_text()).get('budget',{}).get('seed','See frozen plan')),seconds=r.get('seconds','Not retained by original runner')))
    manifest['runs'][-1]['command']='OPENBLAS_NUM_THREADS=1 '+manifest['runs'][-1]['command']
    (OUT/'run-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(dict(tasks=[dict(id=t['id'],status=t['status']) for t in s['tasks']],reader=s['reader'],supplement=s['scientific_supplement'])))
if __name__=='__main__':main()

"""Method-specific gfoRmula proposal reuse disposition; no runtime admission."""
from pathlib import Path
import hashlib,json
import gformula_reference_20261020 as exact
import run_program_reviews_v2 as ext
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-20/gformula-reuse-v1'
RAW=ROOT/'docs/literature/raw'
read=lambda p:json.loads(p.read_text())
LIMITS=['17 authenticated selected source blobs are not a full distribution or transitive dependency/rights audit.',
 'Source declares1.1.2 while NEWS marks its date TBD; no release/current-support claim.',
 'No downloaded R code, upstream tests, model or sibling repository executed.',
 'Exact authored examples do not establish native failures, interval calibration or bank value.',
 'Bootstrap scope is person resampling; arbitrary bank/calendar/shared-audit dependence remains unqualified.',
 'Rendered review, mandatory repairs, Q1/Q5 and final proposal acceptance remain open.']

def main():
    assert not (BASE/'source-audit.json').exists()
    assert exact.calculate()==read(BASE/'exact-results.json')
    identity=read(BASE/'authenticated-source-identities.json')
    selection=read(BASE/'source-selection.json');assert len(identity['sources'])==17
    root=read(RAW/'exec20_gformula_root_tree.json')
    assert root['sha']==selection['root_tree'] and not root['truncated']
    by={x['path']:x for x in root['tree']}
    for x in identity['sources']:
        path=ROOT/x['local_path'];b=path.read_bytes()
        assert hashlib.sha256(b).hexdigest()==x['sha256']
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==by[x['path']]['sha']==x['git_blob_sha1']
    write(BASE/'plan-review.json',dict(status='pass',evidence=[ref(BASE/'plan.md','Reviewed scoped plan')],
        checks=['Resolve alias, source commit/root tree, version declaration and release-date limit.',
          'Trace intervention/history order, risk targets, clipping and bootstrap failure handling.',
          'Reproduce exact laws independently without running downloaded code.',
          'Complete a reference disposition without integration_allowed; preserve native rights and qualification obligations.']))
    specs=[
      (0,1,100,'Version1.1.2,R>=3.5.0,GPL3 declaration, Imports/Suggests; declaration is not full rights approval.'),
      (1,1,40,'Exported functions and S3 output interfaces.'),
      (2,1,50,'Installation/reference leads; mutable badges do not establish current success.'),
      (3,1,46,'NEWS1.1.2TBD; prior custom-model fix, intervention syntax, truncation and seed changes; failed-bootstrap policy documented.'),
      (4,1,176,'Target types, model/intervention inputs, diagnostics, nsimul/nsamples, history/visit and sim_trunc contracts.'),
      (4,375,430,'General entrypoint dispatch to target-specific routines.'),
      (4,880,905,'Competing-event-as-censoring branch disables competing hazard in intervention simulation and preserves separate diagnostic handling.'),
      (4,1180,1290,'Bootstrap invocation and sd/quantile aggregation use na.rm=TRUE; normal/percentile interval options.'),
      (5,130,178,'Resample person identifiers and all associated histories, refit models, then adjust simulated population size.'),
      (5,341,376,'Failure wrapper warns and returns NA result arrays; not a successful replicate.'),
      (7,162,226,'Warn on small simulation; validate numeric consecutive ID-time rows and selected covariate encodings.'),
      (8,71,120,'Pre-baseline lag convention: baseline versus zero/reference level; cumulative histories have explicit time support.'),
      (9,70,82,'Static intervention indexes absolute time t+1.'),
      (9,142,196,'Threshold clamps current values; intfunc applies supplied functions in list order at selected times.'),
      (12,195,320,'Observed baseline, intervention, history update, outcome/competing hazards; competing event removes concurrent main event.'),
      (12,325,357,'Later covariates simulated in covnames order with conditional draws.'),
      (12,482,505,'Selected continuous simulation draws are clamped to observed ranges; zero-inflated branch preserves exact zeros.'),
      (12,525,565,'Intervention after conditional draws, then relevant history refresh and outcome prediction.'),
      (12,620,645,'Cumulative main-event risk uses same-period competing survival and prior main/competing survival.'),
      (13,1,190,'Selected upstream tests primarily assert no error for example regimes; not numerical or causal oracle; unexecuted.'),
      (14,16,119,'New intervention naming, absolute-time static vector, selected intervention times and dynamic custom function.'),
      (15,16,43,'Default models and custom fit/predict interface; correct probability/mean target must be preserved.'),
      (16,1,70,'Declared OS/R CI matrix, dependencies and unpinned action tags; no observed successful native run.')]
    extracts=[]
    for i,lo,hi,finding in specs:
        path=RAW/f'exec20_gformula_source_{i:02d}.txt';lines=path.read_text().splitlines(keepends=True)
        hi=min(hi,len(lines));part=''.join(lines[lo-1:hi])
        extracts.append(dict(source=ref(path,'Authenticated primary source'),lines=[lo,hi],finding=finding,
            excerpt=part,excerpt_sha256=hashlib.sha256(part.encode()).hexdigest()))
    write(BASE/'inspected-extracts.json',dict(anchors=extracts,native_execution=False))
    deps=['data.table','ggplot2','ggpubr','grDevices','nnet','parallel','progress','stats','stringr','survival','truncnorm','truncreg','utils']
    write(BASE/'identity-review.json',dict(repository='CausalInference/gfoRmula',commit=selection['commit'],
        commit_date=selection['commit_date'],root_tree=selection['root_tree'],aliases=['inherited:gformula','seed:061 gfoRmula'],
        distinct_implementation_count=1,source_version='1.1.2',release_date='NEWS TBD; unknown',license_declaration='GPL-3',
        standalone_license_in_selected_tree=False,imports=deps,dependency_lock=False,
        maintenance='Historical changelog and declared CI matrix inspected; latest release or maintained service not established.',
        evidence=[ref(BASE/'authenticated-source-identities.json','17 original identities'),ref(BASE/'inspected-extracts.json','Primary anchors')]))
    claims=['Pinned R code implements simulation-based longitudinal risk or terminal means/probabilities with configurable intervention functions and histories.',
      'Baseline covariates are taken from observed rows; later covariates are generated in covnames order, followed by interventions/history refresh.',
      'Main-event cumulative risk with competing events includes same-period competing survival; censoring/elimination branch changes the simulation target.',
      'Selected continuous draws are clamped to empirical ranges when sim_trunc is enabled.',
      'Bootstrap resamples whole people; replicate errors warn and return NA, while interval aggregation drops missing values.',
      'Version declaration, GPL3 and imports are inspected; native behavior, complete rights and general dependent inference remain open.']
    software=dict(integrated_citation_key='exec20_gformula_reuse',kind='software_primary_source',
        title='gfoRmula longitudinal simulation and bootstrap semantics at the November2025 source revision',
        author='CausalInference gfoRmula contributors',year=2025,
        source_identity='https://github.com/CausalInference/gfoRmula/tree/'+selection['commit'],
        version_date='3November2025,16:01:40UTC; declares1.1.2,release date TBD',cutoff='2026-10-07',
        local_copy=ref(BASE/'authenticated-source-identities.json','Original source identities'),
        primary_sources=[ref(ROOT/x['local_path'],'Authenticated selected source') for x in identity['sources']],
        inspected_anchors=[dict(anchor=f'{Path(x["source"]["path"]).name} lines{x["lines"][0]}-{x["lines"][1]}',
            finding=x['finding'],evidence=ref(BASE/'inspected-extracts.json','Verbatim inspected anchors')) for x in extracts],
        supported_claims=claims,limitations=LIMITS)
    authored=dict(integrated_citation_key='exec20_gformula_reference',kind='project_derivation',
        title='Exact longitudinal policy, competing-event, clipping and failed-bootstrap references',
        author='Causal banking proposal project',year=2026,source_identity='tools/gformula_reference_20261020.py',
        version_date='20October2026',local_copy=ref(ROOT/'tools/gformula_reference_20261020.py','Authored rational arithmetic'),
        inspected_anchors=[ref(BASE/'exact-results.json','All exact finite-law calculations')],
        supported_claims=['Two-period never/always/dynamic risks13/100,3/5,17/40; mean-path dynamic73/200.',
          'At assumed value100/cost20 dynamic-versus-never margin19/2 differs from mean-path7/2.',
          'Competing-event risk387/1250 differs from elimination9/25; assumed loss1000 difference252/5.',
          'Clipping changes second moment2 to1/2; at penalty100, difference150.',
          'Dropping two large example replicates changes mean3/2 to1/2 and sample variance5/3 to1/2.'],
        limitations=exact.calculate()['limits'])
    write(BASE/'source-audit.json',dict(sources=[software,authored],cutoff='2026-10-07'))
    contract=dict(status='proposed_not_implemented',selected_use='Original R reference worker candidate',
        inputs=['person/time schema,consecutive clock and pre-baseline convention','ordered covariate models and target-specific outcome',
          'typed intervention schedule and immutable approved custom callback','competing/censoring targets and restrictions',
          'separate observed n,simulation M,bootstrap B,seeds and parallel settings','sim_trunc and observed bounds,visit-process mapping'],
        outputs=['typed risk curve or terminal probability/mean,reference policy and contrasts','sampling versus MonteCarlo uncertainty and unsupported status',
          'requested/completed/failed replicates and warnings','event/history/selection metadata and full model identities'],
        refusals=['invalid or future-leaking clock','unsupported event coding/probabilities','unapproved arbitrary callback or dependency',
          'unqualified shared-bank/calendar dependence','unacceptable failed-replicate loss','unknown source/version/license'],
        oracle=ref(BASE/'exact-results.json','Independent finite-law values'),
        native_checks=['Joint/static/dynamic policies and absolute-time vectors','competing-event order/elimination difference',
          'range-clipping and baseline-lag toggles','ID resampling and replicate-failure reporting',
          'seed/parallel reproducibility; M varied independently of observed n and bootstrap B'],
        integration_allowed=False)
    write(BASE/'conversion-contract.json',contract)
    omissions=[('Full distribution rights','Inspect complete GPL terms and transitive dependencies/environment before distributing a worker or port.'),
      ('Native reference qualification','Run a separately authorized prototype against finite-law oracles, preserving all failures; no engine was run here.'),
      ('Dependent samples','Declare actual bank clustering/calendar dependence and justify a resampling design before interval claims.'),
      ('Current package paper','Acquire and inspect the genuine package paper and relevant corrections before importing their theorem/empirical claims.'),
      ('Worker costs','Measure simulation,refitting,serialization,review and deployment costs on matched accepted outputs.'),
      ('Coverage and acceptance','Keep mandatory repair completeness and fresh rendered review open.')]
    write(BASE/'omissions-register.json',dict(global_blocker=None,items=[dict(item=k,status='open',next_action=v) for k,v in omissions]))
    decision=dict(operation='SW.DECISION.inherited_gformula',status='pass',decision='reference',
        scope='Retain pinned original R simulation as a proposal comparator; no executable admission.',
        alternatives=[dict(choice='integrate_original_worker',disposition='candidate_after_qualification',
          reason='Preserves existing target/history/intervention logic; requires rights,environment and native oracles.'),
          dict(choice='port',disposition='defer',reason='Reimplementing ordered simulation,histories,visits and bootstrap duplicates scientific semantics; no demonstrated gain.'),
          dict(choice='direct_in_process_adoption',disposition='defer',reason='Runtime and callback/dependency qualifications are unperformed.'),
          dict(choice='reject_entire_project',disposition='not_selected',reason='The inspected finite-regime method is relevant; limits support bounded comparison rather than wholesale rejection.')],
        canonical_aliases=['inherited:gformula','seed:061'],capabilities=[],integration_allowed=False,
        owner_obligations=['Proposal author specifies estimand and clock','Future numerical reviewer qualifies oracles/uncertainty',
          'Future distribution owner resolves rights/environment','Bank owner later supplies assignment/observation truth'],
        revisit_trigger='Change of revision,target,custom learner,dependence law,rights or decision to implement a worker.',
        limitations=LIMITS,evidence=[ref(BASE/n,'Reviewed reuse basis') for n in ['identity-review.json','source-audit.json','inspected-extracts.json','conversion-contract.json','exact-results.json','omissions-register.json']])
    output=ROOT/'docs/program/comprehensive-v14/work/SW.DECISION.inherited_gformula/decision.json'
    output.parent.mkdir(parents=True,exist_ok=True);write(output,decision)
    write(BASE/'review.json',dict(status='pass',scope=decision['scope'],reviewer=dict(name='Codex author/coordinator',kind='author'),
        findings=claims,evidence=decision['evidence']+[ref(output,'Complete reference disposition')],limitations=LIMITS,
        native_execution=False,visual_acceptance=False))
    run=ext.base;state=run.core.read(ROOT,run.core.STATE);graph,_,_=run.combined(ROOT,state)
    node=run.ledger.operation(graph,decision['operation']);receipt=run.ledger.receipt_template(node)
    ev=decision['evidence']+[ref(BASE/'plan-review.json','Reviewed plan'),ref(BASE/'review.json','Author review'),ref(Path(__file__),'Review construction')]
    findings=['17 original blobs authenticate against explicit root tree; alias/version/license/dependency/maintenance limits are bound.',
      'Targets,event order,history,clipping,bootstrap failures,alternatives,costs and owner duties have concrete contracts and exact examples.',
      'Reference disposition grants no runtime capability; full rights,behavioral qualification and dependent inference remain later obligations.']
    receipt.update(outcome='pass',execution='performed',scope=decision['scope'],reviewer=dict(name='Codex author/coordinator',kind='author'),
        limitations=LIMITS,original_gap_qualification=False,capabilities=[],outputs=[ref(output,'Contracted gfoRmula decision')],
        nonexecution_reason='',revisit_trigger=decision['revisit_trigger'],
        criteria=[dict(index=i,verdict='pass',finding=finding,evidence=ev) for i,finding in enumerate(findings)])
    write(BASE/'operation-receipt.json',receipt)
    verify_bindings(read(BASE/'source-audit.json'));verify_bindings(read(BASE/'review.json'))
    print(json.dumps(dict(decision='reference',proposal_review='pass',integration_allowed=False,blobs=17)))

if __name__=='__main__':main()

#!/usr/bin/env python3
"""Review preserved commercial survival evidence against the current contract."""
import json
from pathlib import Path
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'src'),str(ROOT/'tests')]
from causalbank.operation_service_v12 import OperationService,REQUEST_SCHEMA,SUPPORTED
from causalbank.operation_contract_v12 import context_digest
from test_operation_service_v12 import context,request
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write

BASE=ROOT/'docs/program/execution/2026-10-16/commercial-survival'
OUTPUT=ROOT/'docs/program/comprehensive-v14/work/SW.COMM.longitudinal_survival/vendor-comparison.json'
AUDIT=ROOT/'docs/program/execution/2026-10-14/commercial-survival/v3/source-audit.json'
REGISTER=ROOT/'docs/program/execution/2026-10-14/commercial-survival/v2/candidate-register.json'
OMISSIONS=ROOT/'docs/program/execution/2026-10-14/commercial-survival/v2/omissions-register.json'
REVIEWER={'name':'Codex author/coordinator','kind':'author'}
LIMITS=[
 'Bounded author comparison, not a market census, installed vendor trial, purchase recommendation or independent acceptance.',
 'Commercial findings are limited to the inspected official source records and their declared edition/date/rights limits.',
 'Current capability is an actual local reference-service observation; no vendor runtime or upstream package execution occurred.',
 'Prices, entitlements, embedding/redistribution rights and deployment performance remain unavailable unless explicitly recorded.',
 'Dynamic-regime identification, survival fitting and competing-risk estimation remain outside the current operation enum.',
 'Public/generated acceptance cases are proposed next work; authentic bank truth and owner inputs remain later requirements.',
]


def source_map():
    audit=json.loads(AUDIT.read_text());verify_bindings(audit)
    return {s['integrated_citation_key']:s for s in audit['sources']},audit


def local_probe():
    with tempfile.TemporaryDirectory(prefix='causal-commercial-',dir=ROOT/'.runtime') as tmp:
        service=OperationService(Path(tmp))
        cap=service.invoke(request('capabilities.describe',{},ctx=None))
        c=context()
        discover=service.invoke(request('graph.discover',{'algorithm_id':'survival-profile','algorithm_version':'proposal'},ctx=c))
        dependent=json.loads(json.dumps(c));dependent['sampling']['law']='dependent_months'
        dependent_r=service.invoke(request('identify.effect',{'method_id':'backdoor'},ctx=dependent))
        # The schema itself is the authoritative transport surface: there is
        # no estimate.survival operation to submit to this runtime.
        enum=REQUEST_SCHEMA['properties']['operation']['enum']
        return {
          'mode':'actual local reference-service execution;no vendor/upstream runtime',
          'runtime':'local_reference_v12',
          'capabilities_response':cap,
          'graph_discover_response':discover,
          'dependent_backdoor_response':dependent_r,
          'operation_enum':enum,
          'survival_operation_present':any('survival' in x or 'longitudinal' in x for x in enum),
          'implemented':SUPPORTED,
          'scope':'Local transport and bounded refusal behavior only;not causal qualification.'}


def main():
    BASE.mkdir(parents=True,exist_ok=True)
    sources,audit=source_map();register=json.loads(REGISTER.read_text());omissions=json.loads(OMISSIONS.read_text())
    verify_bindings(register);verify_bindings(omissions)
    local=local_probe();assert local['survival_operation_present'] is False
    assert local['graph_discover_response']['disposition']=='unsupported'
    assert local['dependent_backdoor_response']['disposition']=='unsupported'
    source_keys=[
      'exec14_survival_stata','exec14_survival_stata_competing','exec14_survival_sas','exec14_survival_ibm',
      'exec14_survival_jmp','exec14_survival_minitab','exec14_survival_ncss','exec14_survival_statistica','exec14_survival_mplus']
    assert all(k in sources for k in source_keys)
    vendors=[
      {'vendor':'Stata','evidence':['exec14_survival_stata','exec14_survival_stata_competing'],
       'documented_strengths':['ATE/ATET and potential mean survival paths;RA/IPW/IPWRA/WRA;overlap and censoring diagnostics','Separate competing-risk subhazard path and multiple-record support'],
       'documented_limits':['stteffects excludes delayed entry,time-varying covariates and multiple-record data','stcrreg is not a dynamic-regime estimator'],
       'proposed_comparison':'Licensed fixed-treatment survival and separate competing-event comparator;bind treatment,censoring,event codes,sample,uncertainty and refusal.',
       'current_gap':'No survival operation or fitted survival estimator in current local service.',
       'recommendation':'candidate comparator;runtime/edition/rights trial required','price':'unavailable in inspected evidence','rights':'licensed terms and embedding/redistribution not verified'},
      {'vendor':'SAS/STAT','evidence':['exec14_survival_sas'],
       'documented_strengths':['PHREG counting-process intervals,delayed entry and recurrent-event examples','EVENTCODE subdistribution hazard,cluster covariance,CIF outputs and effective-option restrictions'],
       'documented_limits':['Inspected edition is14.1;15.1 full PDF exceeded acquisition bound','Ignored options and pointwise settings must not be silently exposed as effective'],
       'proposed_comparison':'Version14.1 interval and EVENTCODE conversion with subject identity,effective options,CIF and covariance diagnostics.',
       'current_gap':'No counting-process or competing-risk operation;no native SAS execution.',
       'recommendation':'candidate reference;edition and licensed runtime trial required','price':'unavailable','rights':'unverified'},
      {'vendor':'IBM SPSS','evidence':['exec14_survival_ibm'],
       'documented_strengths':['T_ time interactions and piecewise measured covariates for Cox models'],
       'documented_limits':['Time-expression support does not identify a dynamic policy effect;documentation route/date is not a runtime qualification'],
       'proposed_comparison':'Clock/interval conversion reference;test availability time against action time and preserve segmented covariates.',
       'current_gap':'No time-dependent survival or policy operation.',
       'recommendation':'representation comparator only pending licensed trial','price':'unavailable','rights':'unverified'},
      {'vendor':'JMP','evidence':['exec14_survival_jmp'],
       'documented_strengths':['Competing Causes display with cause-wise survival and saved cause coordinates','Omit Causes documents an explicit removal illustration'],
       'documented_limits':['Independence premise and censoring of other causes are substantive;Omit Causes is not a causal intervention'],
       'proposed_comparison':'Cause-specific/cause-removal display with explicit event-removal premise;compare incidence and value separately.',
       'current_gap':'No competing-event representation or survival display.',
       'recommendation':'documentation comparator;do not port as causal removal','price':'unavailable','rights':'unverified'},
      {'vendor':'Minitab','evidence':['exec14_survival_minitab'],
       'documented_strengths':['Counting-process/time-dependent repeated data;ties,covariance,strata and PH diagnostics;row exclusions/errors'],
       'documented_limits':['Exact edition/update unresolved;input representation does not identify a policy effect'],
       'proposed_comparison':'Record reconciliation and diagnostic export comparator;test entry/exit,events,excluded rows,ties and covariance.',
       'current_gap':'No interval survival input or diagnostics operation.',
       'recommendation':'reference-only until dated edition and runtime evidence','price':'unavailable','rights':'unverified'},
      {'vendor':'NCSS','evidence':['exec14_survival_ncss'],
       'documented_strengths':['Processed/used rows,iterations,achieved convergence and completion status'],
       'documented_limits':['Undated Chapter565;convergence reporting is not causal identification or calibrated inference'],
       'proposed_comparison':'Convergence and row-accounting export;retain nonconvergence as unavailable.',
       'current_gap':'No convergence or survival fitting operation.',
       'recommendation':'diagnostic reference only pending exact edition','price':'unavailable','rights':'unverified'},
      {'vendor':'Statistica','evidence':['exec14_survival_statistica'],
       'documented_strengths':['Survival-time,time-function and start/stop counting-process input forms'],
       'documented_limits':['Risk-set representation does not establish sequential regime semantics;conversion must preserve event/censor codes'],
       'proposed_comparison':'Clock and start/stop conversion fixtures;compare interval inclusion and event ordering.',
       'current_gap':'No start/stop or time-function operation.',
       'recommendation':'representation comparator pending licensed trial','price':'unavailable','rights':'unverified'},
      {'vendor':'Mplus','evidence':['exec14_survival_mplus'],
       'documented_strengths':['Discrete-time,Cox,parametric baseline and latent-factor survival examples'],
       'documented_limits':['Exact edition/date unresolved;post-event/dropout code and latent measurement require scientific separation'],
       'proposed_comparison':'Separate model-family and missingness conversion reference;no hidden-confounding claim.',
       'current_gap':'No survival,latent-factor or missingness model operation.',
       'recommendation':'reference-only pending exact edition/runtime','price':'unavailable','rights':'unverified'},
      {'vendor':'MATLAB / fitcox / coxphfit','evidence':[],
       'documented_strengths':[],'documented_limits':['Both official method routes returned HTTP403;capability unknown,not absent'],
       'proposed_comparison':'Acquire accessible version-specific originals through authorized route,then inspect method,license and runtime.',
       'current_gap':'Unknown commercial capability;not represented as a negative feature finding.',
       'recommendation':'omission register;no comparison conclusion','price':'unavailable','rights':'unverified'},
    ]
    for row in vendors:
        for key in row['evidence']:assert key in sources
    proposed=[
      {'profile':'fixed_treatment_survival','truth':'public/generated exact competing-event law plus documented public data','acceptance':['target/time origin/event coding','entry/exit and availability clocks','censoring and uncertainty','unsupported/refusal denominator'],'later_input':'licensed selected edition and bank event/assignment truth'},
      {'profile':'competing_event_incidence','truth':'exact two-period recursion and public event data with documented limits','acceptance':['cause-specific versus cumulative incidence','retained competing risk sets','pointwise versus simultaneous uncertainty','value map separate from event risk'],'later_input':'owner-approved event definitions and economic losses'},
      {'profile':'time_varying_records','truth':'generated start/stop records with known ordering','acceptance':['subject/interval reconciliation','no future covariates','entry/exit errors','covariance and ties'],'later_input':'bank observation clock and record lineage'},
      {'profile':'sequential_policy','truth':'generated randomized two-stage law','acceptance':['history-indexed assignment','policy target and support','censoring/dropout','joint uncertainty'],'later_input':'authentic intervention/retention evidence;current service refusal until implemented'},
    ]
    matrix={'operation':'SW.COMM.longitudinal_survival','status':'inconclusive','reviewer':REVIEWER,'reviewed_on':'2026-10-16 Asia/Shanghai',
      'cutoff':'2026-10-07 Asia/Shanghai','scope':'Nine-family edition-specific commercial comparison against current bounded local service and proposed public/generated profiles.',
      'current_capability':{'observed':local,'implemented_operations':SUPPORTED,'survival_operation':'absent from request schema and runtime;this is an implementation observation,not a claim that survival software does not exist.'},
      'vendor_matrix':vendors,'proposed_acceptance_profiles':proposed,
      'known_gaps':[x['gap'] for x in omissions['items']],
      'routes_not_awarded':['No vendor is selected for purchase or production integration.','No price,license entitlement,unattended execution or benchmark right is inferred.','No dynamic policy,causal survival or competing-risk capability is awarded to the local service.'],
      'evidence':[ref(AUDIT,'614-record commercial source audit;14 original documents and bounded claims'),ref(REGISTER,'Nine-family candidate register'),ref(OMISSIONS,'Coverage and missing-originals register'),ref(BASE/'plan.md','Reviewed comparison plan'),ref(Path(__file__),'Actual local probe and matrix construction')],
      'limitations':LIMITS}
    write(OUTPUT,matrix)
    write(BASE/'primary-review.json',{'status':'pass','reviewer':REVIEWER,'scope':matrix['scope'],'source_audit':ref(AUDIT,'Original source identities/hashes/anchors'),
      'candidate_register':ref(REGISTER,'Nine candidates and dispositions'),'omissions':ref(OMISSIONS,'Unresolved originals/editions/rights'),
      'local_probe':ref(BASE/'local-probe.json','Actual local operation results'),'observations':['Current runtime exposes six bounded operations and no survival/longitudinal operation.','All nine vendor rows retain an explicit route,limit and missing-evidence disposition.'], 'limitations':LIMITS})
    write(BASE/'local-probe.json',local)
    write(BASE/'author-review.json',{'status':'pass','reviewer':REVIEWER,'scope':'Author source and current/proposed capability comparison;no purchase/runtime qualification',
      'findings':['Fourteen original official documents support eight vendor-family rows;MATLAB remains unknown after403 responses.','Current local service actually returns unsupported for graph discovery and dependent back-door requests and has no survival operation enum.','Proposed profiles separate fixed survival,competing event,clock conversion and sequential policy;each retains later owner inputs.'],
      'evidence':[ref(OUTPUT,'Nine-row current/proposed/vendor matrix'),ref(BASE/'primary-review.json','Source and local review'),ref(BASE/'local-probe.json','Actual local runtime'),ref(AUDIT,'Original source audit')], 'limitations':LIMITS})
    print(json.dumps({'status':'inconclusive','vendors':len(vendors),'source_families':9,'local_probe':'pass','survival_runtime':'absent','output':str(OUTPUT.relative_to(ROOT))}))

if __name__=='__main__':main()

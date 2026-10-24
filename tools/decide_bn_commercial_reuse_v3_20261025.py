#!/usr/bin/env python3
"""Two commercial reference choices, with no native or contractual admission."""
import argparse
import hashlib
import json
from pathlib import Path
from html.parser import HTMLParser
import bn_commercial_reuse_reference_20261025 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-25/bn-commercial-reuse-v1'
AUDIT=ROOT/'docs/program/execution/2026-10-25/copilot-reuse-reader-v1/reader/source-audit.json'
KEYS=['exec13_bayesia_api','exec13_bayesia_professional','exec13_ci_bayesia_criteria',
      'exec13_ci_bayesia_surgery','exec13_ci_bayesia_matching','exec13_ci_bayesia_counterfactual',
      'exec13_ci_bayesserver_causality','exec14_ci_eula','exec14_ci_purchase','exec14_ci_release_history']
OPS={'bayesia':'SW.DECISION.seed_090','bayesserver':'SW.DECISION.seed_091'}
read=lambda p:json.loads(p.read_text())
LIMITS=['Retained mutable official pages acquired after cutoff are not immutable cutoff bytes or current commercial offers.',
 'No vendor binary, service, GUI, CLI or MCP runtime executed; no vendor contacted or agreement accepted.',
 'Applicable order/addenda, supported artifacts, deployment and benchmark reporting rights, prices and maintenance remain unresolved.',
 'Exact authored witnesses are not vendor failures, public benchmark results, universal identification or observed bank value.',
 'No full software-family coverage, independent, visual, bank or final acceptance.']

class Text(HTMLParser):
    def __init__(self):super().__init__();self.out=[];self.skip=0
    def handle_starttag(self,t,a):
        if t in ['script','style']:self.skip+=1
    def handle_endtag(self,t):
        if t in ['script','style']:self.skip-=1
    def handle_data(self,s):
        if not self.skip and s.strip():self.out.append(s.strip())

def prepare():
    assert not (BASE/'review.json').exists()
    selected=[s for s in read(AUDIT)['sources'] if s['integrated_citation_key'] in KEYS]
    assert len(selected)==10
    for s in selected:
        verify_bindings(s);p=ROOT/s['local_copy']['path'];raw=p.read_bytes()
        assert hashlib.sha256(raw).hexdigest()==s['local_copy']['sha256']
        if p.suffix=='.html':parser=Text();parser.feed(raw.decode('utf-8-sig'));text=chr(10).join(parser.out)+chr(10)
        else:text=raw.decode('utf-8-sig')
        assert (BASE/(s['integrated_citation_key']+'.txt')).read_bytes()==text.encode('utf-8')
    anchors={
        'exec13_bayesia_api':['stateless Web Service','inference with a given Bayesian network','one instance means that a network model is loaded'],
        'exec13_bayesia_professional':['desktop application','Floating Token License'],
        'exec13_ci_bayesia_criteria':['Adjustment Criterion','unobserved'],
        'exec13_ci_bayesia_surgery':['inbound','intervention'],
        'exec13_ci_bayesia_matching':['Fix Probabilities','confounder'],
        'exec13_ci_bayesia_counterfactual':['Likelihood Matching'],
        'exec13_ci_bayesserver_causality':['characteristic variables','remove the original evidence','9.4 or later','not always possible to find a valid criterion'],
        'exec14_ci_eula':['BENCHMARK TESTING','prior written consent'],
        'exec14_ci_purchase':['perpetual for version 11','per developer'],
        'exec14_ci_release_history':['Version 11.4.0.0','April 17, 2026','Version 10.2.0.0 Beta'],
    }
    for key,tokens in anchors.items():
        text=(BASE/(key+'.txt')).read_text().lower()
        assert all(t.lower() in text for t in tokens),(key,tokens)
    write(BASE/'inherited-review-bindings.json',dict(sources=selected,
        extracted=[ref(BASE/(k+'.txt'),'Fresh inert extraction of authentic retained original') for k in KEYS],
        inspected_tokens=anchors,cutoff='2026-10-07',source_count=10,native_execution=False))
    write(BASE/'exact-results.json',exact.calculate())
    write(BASE/'identity-review.json',dict(status='pass_for_separate_official_profiles',
        profiles=[dict(candidate='BayesiaLab',scope='Desktop plus separately documented Engine Java/REST configurations',version='Mutable acquired pages; numbered artifact not selected'),
                  dict(candidate='Bayes Server',scope='Documented intervention/abduction workflow; desktop/API purchase options',version='Acquired history lists11.4.0.0 dated17April2026;installed build unverified')],
        independent_vendors=True,configuration_parity=False,
        evidence=[ref(BASE/'inherited-review-bindings.json','Exact official source identities and dates')]))
    matrix=[
        ('model_and_diagram','BayesiaLab supplied DAG, path explanation and desktop workflow','Bayes Server supplied causal network and evidence/intervention distinction','Preserve assumptions, graph identity, variable states and parameter provenance'),
        ('population_intervention','Graph surgery and likelihood matching in documented examples','Interventions with criteria discussion and acknowledged identification failure','Bind target and applicable identification conditions; missing evidence cannot become a scalar effect'),
        ('individual_counterfactual','Selected contribution page has factual/intervention contrasts under expert assumptions','Explicit evidence, characteristic-variable abduction, removal and intervention sequence','Retain structural coupling and factual context; distinguish effect, attribution and cross-world query'),
        ('panel_longitudinal','Selected pages do not establish a complete matched panel/policy contract','Selected pages do not establish a complete matched panel/policy contract','Separate timing, assignment, censoring, support and dependent uncertainty review; no feature-absence claim'),
        ('runtime_profile','REST inference differs from separately listed Java learning/modeling','Version-specific helpers and separately purchased desktop/API profiles','Select exact entitled profile; test graph/state/evidence/failure round trips'),
        ('commercial_units','Concurrent loaded model instances, desktop seat/floating options','Developer/API and desktop offers with separate linked terms','Reconcile actual order/addenda, hosting, reporting rights, quotes and maintenance')
    ]
    write(BASE/'capability-comparison.json',dict(rows=[dict(area=a,bayesia=b,bayesserver=c,proposal_obligation=d) for a,b,c,d in matrix],
        scope='Selected authentic documentation, not exhaustive feature inventory',
        evidence=[ref(BASE/'inherited-review-bindings.json','Primary text'),ref(BASE/'exact-results.json','Independent semantic witness')]))
    write(BASE/'mathematical-review.json',dict(status='pass_for_exact_authored_models',
        evidence=[ref(Path(exact.__file__),'Independent enumeration and Fraction accounting'),ref(BASE/'exact-results.json','Exact outcomes'),ref(BASE/'development.tex','Assumptions and derivation')],
        findings=['Both stipulated worlds have four observed probabilities1/4 and intervention means1/2, but individual Y1 given X0,Y0 is0 versus1.',
                  'No faithfulness or monotonicity assumption; counterexample concerns class containing both models, not a vendor defect or sharp bound.',
                  'Three half-open model intervals have peak occupancy2, not3; host count is separate.',
                  '8000/200=40;8000/160=50;8000/100=80USD; no empirical costs.'],native_execution=False))
    rights=dict(status='documented_terms_require_profile_reconciliation',
        bayesia=['Development versus production API configurations','Concurrent loaded-instance accounting distinct from hosts','Desktop seat/floating and purchase/rental distinctions'],
        bayesserver=['Selected purchase description distinguishes developer/API and desktop','Undated linked text restricts transfer and benchmark disclosure','Applicable purchased order/addendum not established by these pages'],
        unresolved=['Exact cutoff edition and supported present artifact','Actual entitlement for chosen internal/server/API use','Native benchmark publication rights under applicable terms','Actual quote, taxes, support and maintenance','Full component/data/model rights where applicable'],
        agreement_accepted=False,vendor_contacted=False,integration_allowed=False,
        evidence=[ref(BASE/'inherited-review-bindings.json','Retained official terms and scope')])
    write(BASE/'dependency-license-review.json',rights)
    common=['Artifact/version and profile','Graph/variable/state identity','Parameter provenance','Evidence versus intervention','Target and assumptions','Model and request digests','Failure/recovery and all-request accounting']
    contracts={
        'bayesia':dict(inputs=common+['Selected REST inference or Java modeling/learning configuration','Load/unload intervals'],
            outputs=['Declared target/model result','Graph and state mappings','Loaded-model occupancy','Typed failure/refusal'],
            refusals=['Undocumented API parity','Unjustified graph directions','Parameter defaults treated as estimates','Missing entitled profile']),
        'bayesserver':dict(inputs=common+['Factual evidence','Characteristic-variable/structural coupling','Abduction/evidence-removal/intervention sequence'],
            outputs=['Population versus individual target type','Retained exogenous/factual context','Identified, conditional or unresolved result','Typed failure/refusal'],
            refusals=['Individual counterfactual without specified coupling','Stale factual evidence after intervention','Unsupported criterion','Missing applicable rights/profile'])
    }
    write(BASE/'conversion-contract.json',dict(status='proposed_reference_only',profiles=contracts,integration_allowed=False,native_execution=False))
    fixtures=['Hand-enumerated supplied DAG intervention','Observed/intervention-equivalent worlds with different individual counterfactuals','Unobserved confounding or unavailable criterion/refusal','Node/state permutation and export/import','Default versus fitted/elicited parameter status','Evidence clearing and stale model','Timeout/cancellation and duplicate request','Service/license-server unavailable','Loaded-model occupancy and all attempts/costs']
    write(BASE/'qualification-plan.json',dict(status='proposed_not_run',
        arms=['Exact independent small-model oracle','Selected permitted native vendor profile','Proposed adapter using the same model/query/information'],
        fixtures=[dict(name=x,status='not_run') for x in fixtures],
        prerequisites=['Exact artifact and all rights applicable to planned use/reporting','Fixed task/version/split, query, graph and state semantics','Target-specific numerical tolerances and scientific criteria','Recorded full costs and owner responsibility'],
        data='Generated SCMs for causal truth; permitted public observational data only for supported data/workflow stress',
        output_denominator='All requests, completions, refusals, failures and admissible results',native_execution=False))
    choices={}
    for role,op in OPS.items():
        candidate='BayesiaLab' if role=='bayesia' else 'Bayes Server'
        route=('Select desktop/Engine REST or Java profile and entitlement; qualify graph/state/parameter/evidence mapping, target identification and loaded-instance/failure accounting.' if role=='bayesia' else 'Select supported edition/API and applicable order/addenda; qualify intervention/abduction coupling and sequence, graph/state conversions and native reporting rights.')
        revisit=route+' Preregister public/generated scientific and operational oracles and matched full costs before adoption; retain unknown bank truth and unrestricted identification as separate limits.'
        choice=dict(operation=op,candidate=candidate,canonical_candidate=candidate+' named offering with explicitly distinct interface profiles',
            selected_revision='Exact retained official byte hashes; no executable revision selected',selected_version=read(BASE/'identity-review.json')['profiles'][0 if role=='bayesia' else 1]['version'],
            decision='reference',reason='Authentic official workflow provides a concrete comparator; selected artifact, applicable rights and native scientific/runtime qualification remain absent.',
            alternatives=[dict(route=a,disposition=b,reason=c) for a,b,c in [
                ('adopt','defer','No complete supported and entitled native profile'),
                ('integrate','conditional',route),
                ('port','not_selected','No proprietary source-port right inferred; independent public-method implementation is separate'),
                ('reference','retain','Use selected official workflows and bounded comparisons'),
                ('reject','component_specific','Reject unsupported target equivalence, guessed API parity and unqualified causal outputs')]],
            owners=[dict(role=a,responsibility=b) for a,b in [('Scientific','Supplied model, target, assumptions and uncertainty'),('Adapter','Graph/state/evidence/abduction conversions and failures'),('Platform/procurement','Supported artifact, network profile, order/addenda and price'),('Evaluation','Independent oracles, permitted reporting and complete denominators'),('Maintenance','Version/profile drift and semantic regression')]],
            owner_status='Proposed roles, no institutional acceptance',
            costs=dict(measured=False,actual_price='Unestablished for selected banking use',categories=['entitlement','preparation','model loading','all calls','review','maintenance'],illustration=ref(BASE/'exact-results.json','Authored costs only')),
            maintenance='Current supported artifact and terms require confirmation',revisit_trigger=revisit,integration_allowed=False,capabilities=[],limitations=LIMITS)
        write(BASE/(role+'-choice.json'),choice);choices[role]=choice
    write(BASE/'choice.json',dict(decision='two_separate_commercial_reference_choices',choices=choices,integration_allowed=False,limitations=LIMITS))
    write(BASE/'omissions-register.json',dict(global_blocker=False,next_action='Complete selected native profiles, rights, public qualification contracts and actual costs independently for each offering.',
        known_routes=['Profile-specific official artifact/terms review','Finite public scientific and failure fixtures','Matched complete-cost comparison'],
        unresolved=['Exact cutoff documents','Installed/API behavior','Applicable commercial order/addenda','Current support and price','Dependent/panel/policy coverage outside inspected scope'],
        unknown_without_information=['Bank assignment truth and hidden causes','Cross-world coupling not implied by population laws','Universal causal identification and dependent-data calibration']))
    authored=dict(integrated_citation_key='exec25_bn_commercial_choice',kind='project_evidence_not_scholarly_paper',
        title='BayesiaLab and Bayes Server reference choices, counterfactual coupling and deployment contracts',author='Causal banking proposal project',year=2026,
        source_identity=str(BASE.relative_to(ROOT)),version_date='25 October 2026; retained acquired official text; cutoff7October2026 limits explicit',
        local_copy=ref(BASE/'choice.json','Separate proposal reference choices'),
        inspected_anchors=[ref(BASE/n,'Bounded authored review') for n in ['identity-review.json','capability-comparison.json','mathematical-review.json','conversion-contract.json','qualification-plan.json','dependency-license-review.json','omissions-register.json']],
        supported_claims=['Separate named commercial reference choices without native admission','Counterfactual coupling witness and instance-count illustration','Conditional profile/rights/public scientific/runtime qualification routes','Exact hypothetical cost denominators'],limitations=LIMITS)
    write(BASE/'source-audit.json',dict(sources=[authored],new_records=1,new_scholarly_pdfs=0,preserved_original_records=10,native_execution=False))
    write(BASE/'plan-review.json',dict(status='pass_for_two_reference_choices',
        evidence=[ref(BASE/n,'Reviewed proposal plan') for n in ['plan.md','identity-review.json','choice.json','mathematical-review.json','conversion-contract.json','qualification-plan.json','dependency-license-review.json']],
        findings=['All three criteria covered separately for each named vendor','No profile parity, current quote or applicable entitlement inferred','Scientific counterfactual distinction and full-cost accounting exact','Preserve immutable predecessor and source records; serialize canonical publication']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_bounded_argument',
        evidence=[ref(BASE/'development.tex','Connected product argument'),ref(BASE/'sponsor-addition.md','Sponsor implications')],
        findings=['Queries, interfaces and rights distinguished','No product absence inferred from source silence','Hypothetical accounting and proposed tests clearly labeled'],visual_acceptance=False))
    review=dict(status='pass_for_two_reference_only_decisions',reviewer=dict(name='Codex author/coordinator',kind='author'),
        evidence=[ref(BASE/n,'Reviewed evidence') for n in ['inherited-review-bindings.json','identity-review.json','choice.json','bayesia-choice.json','bayesserver-choice.json','capability-comparison.json','mathematical-review.json','exact-results.json','source-audit.json','conversion-contract.json','qualification-plan.json','dependency-license-review.json','omissions-register.json','plan-review.json','copyedit-review.json','development.tex','sponsor-addition.md']]+[ref(Path(__file__),'Review and receipt logic')],
        findings=['Ten retained authentic originals re-inspected and rebound','Two named decisions complete without native admission','Exact counterfactual, occupancy and cost examples reproduce'],limitations=LIMITS,integration_allowed=False)
    verify_bindings(review);write(BASE/'review.json',review);print(json.dumps(dict(review='pass',decisions=2,original_records=10,new_records=1,native_execution=False)))

def receipt(role):
    op=OPS[role];state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==op
    verify_bindings(read(BASE/'review.json'));graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,op)
    value=read(BASE/(role+'-choice.json'));value.update(status='pass',scope='Completed '+role+' proposal reference choice; no native admission',evidence=[ref(BASE/'review.json','Author source and semantic review')])
    output=ROOT/node['outputs'][0];write(output,value)
    evidence=[ref(BASE/n,'Separate reviewed reference decision') for n in ['review.json',role+'-choice.json','conversion-contract.json','dependency-license-review.json','qualification-plan.json']]
    findings=['Separate vendor/profile, source/version/rights/dependency and maintenance limits bound','Target, uncertainty, alternatives, costs, proposed owners and revisit trigger explicit','Reference only with proposed scientific/failure oracles; integration disallowed']
    result=run.ledger.receipt_template(node);result.update(outcome='pass',execution='performed',scope=value['scope'],reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(output,'Named reference disposition')],criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=value['revisit_trigger'])
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/(role+'-operation-receipt.json'),result);print(role+' receipt prepared.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','bayesia','bayesserver']);a=p.parse_args();prepare() if a.command=='prepare' else receipt(a.command)

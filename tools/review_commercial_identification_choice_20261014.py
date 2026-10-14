#!/usr/bin/env python3
"""Review preserved vendor sources, scoped contracts and exact project examples."""
from copy import deepcopy
from fractions import Fraction as F
from html.parser import HTMLParser
import json
from pathlib import Path

import run_program as run
import master_control as core
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-14/commercial-identification-comparison'
PRIOR=ROOT/'docs/program/execution/2026-10-13/commercial-identification'
AUDIT=ROOT/'docs/program/execution/2026-10-14/l6-architecture/v2/reader/source-audit.json'
OP='SW.COMM.identification_counterfactual'
OUTPUT=ROOT/('docs/program/comprehensive-v14/work/'+OP+'/vendor-comparison.json')
REVIEWER={'name':'Codex author/coordinator','kind':'author'}
LIMITS=[
 'Finite sixteen-family comparison; twelve unresolved or adjacent-only families remain.',
 'Mutable sources acquired after 2026-10-07 do not authenticate exact historical bytes.',
 'No commercial binary, API or licensed runtime was executed; no contact, purchase or terms acceptance.',
 'General ID/IDC completeness, uncertain-abduction distribution semantics and cross-wrapper parity remain unresolved.',
 'Published prices are version-11 individual GBP prices before applicable VAT, not bank total costs or a quotation.',
 'Author review only; full MR01 coverage, Q1 and rendered/Q5 acceptance remain open.'
]

def calculate():
 states=[F(0),F(1),F(3)]
 factual=[u for u in states if u>=1]
 posterior=F(sum(u>=2 for u in factual),len(factual))
 prior=F(sum(u>=2 for u in states),len(states))
 mean=sum(factual)/len(factual)
 plugin=F(mean>=2)
 assert (prior,posterior,mean,plugin)==(F(1,3),F(1,2),F(2),F(1))
 assert F(1000)*posterior-20==480 and F(1000)*plugin-20==980
 return {'kind':'exact_project_construction','latent_support':[str(u)for u in states],
  'prior_weights':['1/3']*3,'equation':'Y(a)=1{U>=a}; U independent of assigned A',
  'factual_evidence':{'A':1,'Y':1},'posterior_support':[str(u)for u in factual],
  'posterior_weights':['1/2']*2,'alternative_A':2,
  'population_alternative_success':str(prior),'posterior_alternative_success':str(posterior),
  'posterior_mean_U':str(mean),'mean_plugin_success':str(plugin),
  'illustrative_value_USD':1000,'illustrative_cost_USD':20,
  'posterior_net_payoff_USD':480,'plugin_net_payoff_USD':980,'overstatement_USD':500,
  'interpretation':'Expected alternative payoff conditional on factual evidence; not incremental policy profit or bank ROI.',
  'vendor_execution':False,'random_draws':0}

class Selections(HTMLParser):
 def __init__(self):super().__init__();self.selected=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='option'and 'selected'in a:self.selected.append(a['value'])

def source(key,title,url,version,phrases,claims,extension='html'):
 raw=ROOT/('docs/literature/raw/exec14_ci_'+key+'.'+extension)
 txt=raw if extension=='txt' else BASE/(key+'.txt')
 lines=txt.read_text().splitlines();anchors=[]
 for phrase in phrases:
  hits=[i+1 for i,line in enumerate(lines)if phrase in line]
  assert hits,(key,phrase)
  anchors.append({'anchor':'Extracted text line(s) '+','.join(map(str,hits)),
                  'inspected_phrase':phrase})
 return {'integrated_citation_key':'exec14_ci_'+key,'kind':'official_technical_documentation',
  'title':title,'author':'Bayes Server','year':2026,'source_identity':url,
  'version_date':version+'; acquired 2026-10-14',
  'cutoff':'2026-10-07','cutoff_limit':'Post-cutoff mutable bytes; no historical-byte authentication.',
  'local_copy':ref(raw,'Authentic original public bytes'),
  'text_copy':ref(txt,'Inert text extraction; raw bytes authoritative'),
  'inspected_anchors':anchors,'supported_claims':claims,
  'limits':'Static official text only; no runtime, independent verification or general algorithm completeness inferred.'}

def prepare():
 assert not OUTPUT.exists() and not (BASE/'source-audit.json').exists()
 sources=[]
 specs=[
 ('causal_query','Advanced Causal Query','docs/causality/causal-query/',
  'Since version 10; copyright 2025',
  ['Since version 10','FrontDoor nodes, and subsequent adjustment sets','Direct Effects only includes'],
  ['Documents back-door/front-door identification and inference with algorithm-dependent hidden-confounder and direct-effect support.',
   'The total-effects examples include a back-door path; that prose does not redefine a causal path or prove general ID/IDC.']),
 ('abduction','Abduction Dialog','docs/causality/abduction/',
  'Since version 10; copyright 2025',['Since version 10','The abduction step simply queries'],
  ['Documents querying characteristic variables, removing factual evidence and setting characteristic evidence.',
   'Selected guide does not specify all uncertain multivariate posterior or point-summary behavior.']),
 ('effects','Effects Analysis','docs/causality/effects-analysis/',
  'Since version 10; copyright 2025',['Values on the X-axis are normalized','the treatment X is discretized','the mean and the variance of Y'],
  ['Documents intervention sweeps, normalized chart axes and evidence-dependent continuous-treatment discretization.',
   'Predictive outcome variance is documented; statistical uncertainty of an estimated mean is not established by this statement.']),
 ('interventions','Interventions','docs/queries/interventions/',
  'Unnumbered mutable guide; copyright 2025',['Intervention evidence can be set','stops the normal flow of information'],
  ['Describes interventions on discrete, continuous and DBN variables and their distinction from ordinary evidence.']),
 ('api_abduction','Abduction .NET API','api/dotnet/api/BayesServer.Causal.Counterfactuals.Abduction.html',
  'Unnumbered API documentation; BayesServer.Causal.dll',
  ['Assembly: BayesServer.Causal.dll','public static void Update','current query values'],
  ['Update explicitly separates current evidence, abduction-evidence variables, characteristic variables and options.',
   'No claim that uncertain exogenous posteriors are fully propagated follows from the selected signature.']),
 ('api_frontdoor','FrontDoorCriterion .NET API','api/dotnet/api/BayesServer.Causal.Identification.FrontDoorCriterion.html',
  'Unnumbered API documentation; BayesServer.Causal.dll',
  ['public sealed class FrontDoorCriterion','for use outside Bayes Server','perform the actual estimation','Tests whether adjustment inputs are valid, without raising an exception.'],
  ['FrontDoorCriterion identifies criterion-specific node sets separately from estimation; external use is explicitly described.',
   'IdentifyXZ and IdentifyZY expose associated back-door subqueries; IsValid and Validate have distinct false/exception reporting.',
   'A criterion failure does not certify general nonidentification.']),
 ('release_history','Bayes Server release history','ReleaseList.aspx',
  'Dated vendor history through 11.4.0.0 (2026-04-17)',
  ['Version 11.4.0.0 - Friday, April 17, 2026','Version 10.2.0.0 Beta','FrontDoor criterion/causal inference algorithm.'],
  ['History associates advanced causal queries/front-door/back-door/abduction with 10.2 beta (2022-06-19).',
   'Highest release listed in this acquired history is 11.4.0.0, dated 2026-04-17; installed build and feature parity untested.']),
 ('purchase','Bayes Server purchase information','Purchase.aspx',
  'Version 11 Professional; selected Commercial/GBP page',
  ['All new licenses are perpetual for version 11','£550.00','£1,100.00','The Bayes Server API is sold per developer.'],
  ['Selected Commercial GBP page shows UI550, API550 and combined1100 before applicable VAT.',
   'Page states perpetual version-11 licenses with minor upgrades and per-developer API use within own products.']),
 ]
 for key,title,path,version,phrases,claims in specs:
  sources.append(source(key,title,'https://www.bayesserver.com/'+path,version,phrases,claims))
 sources.append(source('eula','Bayes Server linked software license agreement',
  'https://www.bayesserver.com/Documents/EULA.txt','Undated linked EULA; amendment/addendum may accompany software',
  ['An amendment or addendum','single copy','shall not rent','4.  PERFORMANCE OR BENCHMARK TESTING.'],
  ['Linked text describes restricted executable use and transfer, and requires prior written consent for third-party benchmark-result disclosure.',
   'The source is not a determination of applicable purchased terms; reconcile selected order/addendum before promising deployment or public benchmark rights.'],'txt'))
 parser=Selections();parser.feed((ROOT/'docs/literature/raw/exec14_ci_purchase.html').read_text())
 assert parser.selected==['GBP','Commercial']
 write(BASE/'price-observation.json',{'selected_form_values':parser.selected,'currency':'GBP','before_applicable_VAT':True,
  'version':'11 Professional','license_basis':'individual, perpetual major version with minor upgrades',
  'public_prices':{'UI':550,'API_developer':550,'UI_and_API':1100},'quoted':False,
  'basis':ref(ROOT/'docs/literature/raw/exec14_ci_purchase.html','Selected option attributes and visible product rows'),
  'exclusions':['tax','future major upgrades','bank deployment/addenda','support and operation labor','actual quotation'],
  'access_date':'2026-10-14','cutoff_bytes_authenticated':False})
 write(BASE/'exact-results.json',calculate())
 selected_keys={'exec13_ci_bayesia_criteria','exec13_ci_bayesia_surgery','exec13_ci_bayesia_matching',
  'exec13_ci_bayesia_counterfactual','exec13_ci_stata_causal_intro','exec13_ci_stata_mediate',
  'exec13_ci_bayesserver_causality','exec13_ci_mplus_mediation','exec13_bayesia_api',
  'exec13_bayesia_professional','exec13_ivrd_license','exec13_smile_license','exec13_smile_intro','exec13_ch_jmp_causal'}
 inherited=json.loads(AUDIT.read_text());verify_bindings(inherited)
 selected=[deepcopy(s)for s in inherited['sources']if s['integrated_citation_key']in selected_keys]
 assert len(selected)==len(selected_keys)
 write(BASE/'primary-review.json',{'reviewer':REVIEWER,'selected_inherited_records':selected,'new_records':sources,
  'inspected_new_contexts':'New manual/API/release/price/rights comparison; independent structural example, with limitations.',
  'acquisitions':[ref(BASE/('acquisition-%02d.json'%i),'Bounded public request result')for i in range(1,7)],
  'requests':12,'downloaded_code_executed':False,
  'cross_lane_repair':'JMP causal manuals already present in heterogeneity lane repair the earlier identification-source omission; originals retained.',
  'limits':LIMITS})
 extra=[{'integrated_citation_key':'exec14_ci_exact','kind':'project_derivation',
  'title':'Exact conditional-abduction and mean-substitution counterexample','author':'Causal banking proposal','year':2026,
  'source_identity':'Project-authored finite structural law','version_date':'2026-10-14',
  'local_copy':ref(BASE/'exact-results.json','Enumerated prior/posterior structural calculation'),
  'inspected_anchors':['calculate(): all three latent states and two posterior states'],
  'supported_claims':['Prior1/3, posterior1/2, mean substitution1; stipulated alternative net payoff480 versus980 USD.'],
  'records':[ref(Path(__file__).resolve(),'Fraction enumeration; no draws or vendor execution')]}]
 write(BASE/'source-audit.json',{'sources':sources+extra,'cutoff':'2026-10-07',
  'inherited_review':ref(BASE/'primary-review.json','Fourteen original records reinspected without altering their identities'),
  'limits':LIMITS})
 print(json.dumps({'new_official_sources':len(sources),'inherited_reinspected':len(selected),'public_gets':12,
                   'exact_example':calculate(),'price_selection':parser.selected}))

def compare():
 assert not OUTPUT.exists()
 primary=json.loads((BASE/'primary-review.json').read_text());verify_bindings(primary)
 source_map={s['integrated_citation_key']:s for s in primary['new_records']+primary['selected_inherited_records']}
 current=ref(ROOT/'src/causalbank/operation_service_v12.py','SUPPORTED: supplied DAG backdoor; supplied moments; no general counterfactual engine')
 specs=[
 ('Bayesia','Supplied-DAG adjustment and likelihood-matching workflow; contribution analysis is not established as general individual abduction.',
  'Unnumbered help; Engine Java/REST configuration table; no matched installed binary.',
  ['exec13_ci_bayesia_criteria','exec13_ci_bayesia_surgery','exec13_ci_bayesia_matching','exec13_ci_bayesia_counterfactual','exec13_bayesia_api','exec13_bayesia_professional'],
  'Customer-hosted Java model files versus France-hosted REST model files; development and production configurations differ.',
  'Production concurrency licensing and validation connectivity documented. Selected causal-function exposure remains unknown.',
  'Compare a supplied offer DAG and data-node mapping; use a licensed adapter only after exact intervention/export semantics are pinned.'),
 ('StataCorp','Treatment-effect estimators and specified mediation with explicit target and confounding assumptions.',
  'Manuals carry copyright2025 and release19 data references; purchased edition/automation entitlement unknown.',
  ['exec13_ci_stata_causal_intro','exec13_ci_stata_mediate','exec13_ivrd_license'],
  'Command-based local workflow; named-user and concurrent-network categories differ.',
  'License-options page is not a server-embedding or redistribution grant; numerical selected deployment price unavailable.',
  'Benchmark a fixed one-time offer ATE/ATT and separately specified mediated effect; no unrestricted individual counterfactual or ID/IDC inference.'),
 ('Bayes Server','Criterion-specific back-door/front-door, intervention sweeps and characteristic-variable abduction.',
  'Guide says10+; release history ties features to10.2 beta2022-06-19; highest listed11.4.0.0 dated2026-04-17; purchase version11 Professional.',
  ['exec14_ci_causal_query','exec14_ci_abduction','exec14_ci_effects','exec14_ci_interventions','exec14_ci_api_frontdoor','exec14_ci_api_abduction','exec14_ci_release_history','exec14_ci_purchase','exec14_ci_eula'],
  'Documented .NET causal assembly and API/developer purchase option. Native/wrapper parity, build pinning and uncertainty propagation remain untested.',
  'Purchase page permits own-product API functionality per developer; linked undated EULA has transfer and benchmark-disclosure restrictions. Applicable order/addendum must be reconciled.',
  'Candidate narrow front-door identification export before broader embedding. Separately test uncertain abduction and retention of node/clock/units/status semantics.'),
 ('JMP','JMP Pro Causal Treatment ATE/ATET and potential-outcome means under declared assumptions.',
  'Help19.2 dated2026-01-13; explicitly JMP Pro personality; installed version untested.',
  ['exec13_ch_jmp_causal'],
  'Interactive documented platform; unattended CLI/MCP export and exact license terms unresolved.',
  'No selected deployment price or redistribution/automation entitlement in inspected sources.',
  'Reuse as a specified-model treatment comparator; do not map predicted potential-outcome means to identified individual missing outcomes.')
 ]
 vendors=[]
 for name,strength,edition,keys,deployment,rights,decision in specs:
  vendors.append({'vendor':name,'comparison_status':'documented_scoped_methods','documented_strength':strength,
   'edition_evidence':edition,'source_keys':keys,'source_records':[source_map[k]for k in keys],
   'deployment':deployment,'license_evidence':rights,'decision':decision,
   'our_observed':'Local supplied-DAG back-door checks and supplied-moment inversion; no comparable fitted mediation, front-door or abduction service.',
   'our_proposed':'Auditable target/clock/graph/set contract with optional scoped licensed adapters and justified refusal.',
   'gap':'Documented vendor modeling/estimation tools exceed the canonical local service in these matched tasks; proposed semantics are not proven superiority.',
   'runtime_executed':False,'price':{'status':'public_numeric'if name=='Bayes Server'else 'unavailable_for_selected_deployment',
      'evidence':ref(BASE/'price-observation.json','Commercial GBP selection')if name=='Bayes Server'else None,'quoted':False}})
 inherited=json.loads((PRIOR/'candidate-register.json').read_text())['families']
 compared={x['vendor']for x in vendors}
 remaining=[]
 for item in inherited:
  if item['vendor']in compared:continue
  row={k:item[k]for k in ['vendor','status','finding','next_action']}
  row.update(comparison_status='unresolved_or_adjacent_only',our_observed='No selected commercial engine installed or qualified',
   our_proposed='Only a semantically and legally scoped optional adapter after missing evidence is reviewed',
   gap='Unknown, not absent',runtime_executed=False,price={'status':'unavailable_for_selected_deployment','amount':None,'quoted':False})
  remaining.append(row)
 assert len(vendors)+len(remaining)==16
 write(BASE/'omissions-register.json',{'remaining_families':remaining,'cross_cutting':LIMITS,
  'new_source_gaps':['Exact installed API assembly version and complete option behavior','Uncertain joint abduction distribution handling',
     'General ID/IDC and arbitrary counterfactual completeness','Matched purchased/addendum terms and bank total cost'],
  'resolved_prior_source_gaps':['Bayes Server Advanced Causal Query, Abduction, Effects, intervention guides and two API references',
     'JMP Pro treatment/assumption manual through existing cross-lane originals'],
  'no_market_absence_claim':True,'next_action':'Acquire named missing originals; test scoped generated/public contracts only after justified prototype and rights review.'})
 comparison={'operation_id':OP,'outcome':'inconclusive','vendors':vendors,'unresolved':remaining,
  'scope':'Four scoped vendor comparisons; all sixteen original families retained. Edition/runtime/coverage incomplete.',
  'cutoff':'2026-10-07','narrative':ref(BASE/'development.tex','Integrated scholarly comparison, example and implementation choices'),
  'primary_review':ref(BASE/'primary-review.json','Verified originals/versions/anchors'),
  'exact_results':ref(BASE/'exact-results.json','Independent project example'),
  'implementation':current,'omissions':ref(BASE/'omissions-register.json','Exact successor triggers'),
  'contacts':0,'purchases':0,'vendor_runs':0,'bank_validation':False,'original_gap_qualification':False}
 write(OUTPUT,comparison)
 findings=['Four families have developed comparisons; twelve unresolved or adjacent-only families remain.',
  'Recovered API explicitly separates front-door identification from estimation; API failure remains distinct from general nonidentification.',
  'Stale JMP source omission is repaired using already acquired primary text, without rewriting the old search.',
  'Source wording about a back-door path as total effect is not adopted as a causal definition.',
  'Posterior point substitution can change counterfactual probability from1/2 to1 in the exact authored mechanism.',
  'Commercial GBP form selection verified in raw HTML; source-bound prices and licensing tensions are explicit.',
  'No licensed execution, acquired rights, scientific truth or proposal completion is fabricated.']
 write(BASE/'author-review.json',{'status':'pass','issues':[],'reviewer':REVIEWER,
  'scope':'Claim-limited substantive comparison; full operation coverage inconclusive','findings':findings,
  'evidence':[ref(OUTPUT,'Sixteen-family comparison'),ref(BASE/'source-audit.json','Nine new originals and exact project result'),
    ref(BASE/'primary-review.json','Preserved inherited sources and all new anchors'),
    ref(BASE/'exact-results.json','Exact replay matches calculate()'),current],
  'limitations':LIMITS,'visual_acceptance':False})
 assert calculate()==json.loads((BASE/'exact-results.json').read_text())
 graph,_,_=run.combined(ROOT,core.read(ROOT,core.STATE));node=run.ledger.operation(graph,OP)
 receipt=run.ledger.receipt_template(node)
 evidence=[ref(OUTPUT,'Complete comparison'),ref(BASE/'author-review.json','Author review'),ref(BASE/'primary-review.json','Authentic sources')]
 receipt.update(outcome='inconclusive',execution='performed',scope=comparison['scope'],reviewer=REVIEWER,limitations=LIMITS,
   outputs=[ref(OUTPUT,'Declared vendor comparison')],nonexecution_reason='',
   revisit_trigger='Missing technical/edition sources acquired and matched contracts reviewed.',
   criteria=[{'index':0,'verdict':'inconclusive','finding':'Four scoped comparisons; twelve families remain unresolved/adjacent-only; full edition-specific coverage withheld.','evidence':evidence},
             {'index':1,'verdict':'pass','finding':'Unknown, not evaluated, documented and source prices are distinct; no fabricated contacts, purchases or tests.','evidence':evidence}])
 write(BASE/'operation-receipt.json',receipt)
 print(json.dumps({'scope_compared':len(vendors),'remaining':len(remaining),'outcome':'inconclusive'}))

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','compare']);a=p.parse_args()
 {'prepare':prepare,'compare':compare}[a.command]()

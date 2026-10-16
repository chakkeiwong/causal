#!/usr/bin/env python3
"""Bind a proposal qualification chapter to exact references and prior sources."""
import json
from pathlib import Path
import re
import s10_examples_20261016 as examples
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write,transition

ROOT=Path(__file__).resolve().parents[1]
BASE=examples.BASE
CHAPTER=ROOT/'docs/program/comprehensive-v14/work/TEXT.DRAFT.S10/chapter.tex'
AUDIT=ROOT/'docs/program/execution/2026-10-16/topology/publication/reader/source-audit.json'
REVIEWER={'name':'Codex author/coordinator','kind':'author'}
LIMITS=[
 'Author proposal chapter;no matched native-package,commercial or port experiment executed.',
 'All new counts,costs,losses and numerical bounds are stipulated exact examples,not measured bank or vendor performance.',
 'Failure-probability bounds require the stated fixed independent Bernoulli experiment;no universal guarantee.',
 'Existing primary-source findings retain their pinned revision and original runtime/coverage limitations.',
 'Public/generated prototypes can proceed;authentic bank inputs,real costs,consumer acceptance and independent review remain later inputs.',
 'Whole-manuscript coverage and rendered visual acceptance remain open;no automatic page credit.',
]


def main():
    assert examples.calculate()==json.loads((BASE/'exact-results.json').read_text())
    prior=json.loads(AUDIT.read_text());sources={s['integrated_citation_key']:s for s in prior['sources']}
    keys=set(k.strip() for group in re.findall(r'\\cite[a-zA-Z*]*{([^}]+)}',CHAPTER.read_text()) for k in group.split(','))
    inherited=sorted(keys-{'exec16_s10_exact','exec16_s10_design'})
    assert set(inherited)<=sources.keys()
    for key in inherited:verify_bindings(sources[key])
    inspections=[
      ref(ROOT/'docs/literature/raw/v12_sw2_source_pgmpy_adjustment.txt','Reread _identify lines153-156:minimal_variance raises NotImplementedError'),
      ref(ROOT/'docs/literature/raw/v12_exec13_pydisc_causalnex_source_1.txt','Reread README lines1-9:dated end-of-life and support notice'),
      ref(ROOT/'docs/program/execution/2026-10-14/causalpy-reuse/conversion-contract.json','Reference-only sharp-RD target,draw,support and failure contract'),
      ref(ROOT/'docs/program/execution/2026-10-15/d3rlpy-reuse/conversion-contract.json','Episode,policy,initial-state,clock,reward and repair obligations'),
      ref(ROOT/'docs/program/comprehensive-v14/work/SW.DECISION.inherited_tetrad/decision.json','Selected Java PC prototype;integration admission deferred'),
    ]
    write(BASE/'primary-review.json',{'status':'pass','reviewer':REVIEWER,'cutoff':'2026-10-07','review_date':'2026-10-16',
      'new_acquisition':False,'inherited_source_records':[sources[k] for k in inherited],
      'reread_anchors':inspections,'claim_policy':'Existing package findings remain scoped to their inspected revisions;proposed contracts are not native results.',
      'adjacent_chapters_inspected':[ref(ROOT/p,'Overlap reviewed;no duplicate substantive credit') for p in [
        'docs/program/comprehensive-v14/work/TEXT.DRAFT.S1/chapter.tex',
        'docs/program/execution/2026-10-13/causalimpact-reuse/software-preserving.tex',
        'docs/program/execution/2026-10-14/l8-economics/v3/development.tex',
        'docs/program/execution/2026-10-14/l7-benchmarking/v3/frontier.tex']],
      'limits':LIMITS})
    design={'status':'proposed','version_date':'2026-10-16','profile':{
       'identity':['Scientific request and sampling regime','Exact package revision,environment and route','Target,graph class,uncertainty,numeric representation','Rights and operational requirements'],
       'admission':'Each necessary scientific,representation,operating and rights condition must be established;unknown remains unresolved.',
       'comparisons':['Method comparison for a common target/information law','Compatibility or mathematical port with explicit equivalence objective','Whole-workflow build/buy/bridge/port/reference-only alternatives']},
      'trial_contract':{'truth':['Exact finite/analytic constructions','Registered generated sampling laws','Documented public examples with limited causal-truth claims'],
       'accounting':['Requested denominator and per-profile counts','Paired request identities and shared outcomes','Correct,wrong,unavailable and invalid cases','Semantic,numerical,statistical and recovery events remain distinct'],
       'before_sampling':['Profile definitions','Failure and coverage events','Fixed sample sizes','Simultaneous error allocation','Stopping rule','Costs and fallback policy'],
       'numeric_acceptance':['Coordinate identities and graph/set topology','Independent references','Deterministic error transported to decision units','Statistical uncertainty separately justified'],
       'measurement':['Cold/warm lifecycle','Serialization and data movement','Fitting,tuning and uncertainty','Human repair and review','Failures,replay and publication']},
      'route_decision':{'alternatives':['direct_adoption','process_bridge','port','internal_implementation','commercial_purchase','reference_only','reject_for_declared_profile'],
       'costs':['Initial engineering/qualification','License/subscription','Maintenance and version migration','Per-request full workflow','Incident and recovery','Discounting and workload'],
       'commercial_evidence':['Exact edition and method','Official technical sources','Automation and export semantics','Intended terms','Dated actual quote when available'],
       'update_trigger':'Acceptance failure,changed source/runtime,target or workload,verified price/maintenance evidence,or new scientific information'},
      'later_inputs':['Authentic bank assignment,identity,clock and feasibility evidence','Precision thresholds and losses','Actual vendor/maintenance/workflow prices','Platform/consumer and independent acceptance'],
      'nonclaims':LIMITS}
    write(BASE/'qualification-design.json',design)
    new=[]
    for key,title,kind,name,anchor,claims in [
      ('exec16_s10_exact','Exact matched-qualification and acquisition planning references','project_derivation','exact-results.json',
       'paired_trial,zero_failure,numerical_acceptance,bridge_port_planning',
       ['Exact paired-law counts,covariance and cost-sensitive comparison','Fixed independent zero-failure inversion and simultaneous profile sample sizes','Deterministic numerical decision enclosure','Hypothetical bridge/port maintenance break-even']),
      ('exec16_s10_design','Proposed matched qualification and software acquisition contract','project_design','qualification-design.json',
       'profile,trial_contract,route_decision,later_inputs and nonclaims',
       ['A proposed route-specific acceptance experiment and admission rule','Separate public/generated evidence,measured native trials and later bank acceptance','No executed commercial comparison or product qualification'])]:
        new.append({'integrated_citation_key':key,'title':title,'kind':kind,'author':'Causal banking research project','year':2026,
          'source_identity':str((BASE/name).relative_to(ROOT)),'version_date':'2026-10-16;project-authored proposal evidence',
          'local_copy':ref(BASE/name,anchor),'inspected_anchors':[anchor],'supported_claims':claims,
          'primary_artifacts':[ref(ROOT/'tools/s10_examples_20261016.py','Exact Fraction calculations and assertions'),
            ref(CHAPTER,'Connected mathematical derivations and qualification discussion'),ref(BASE/'primary-review.json','Preserved source identities and inspected anchors')],
          'limits':LIMITS})
    write(BASE/'source-audit.json',{'cutoff':'2026-10-07','sources':new,'new_scholarly_papers':0,'prior':ref(AUDIT,'639 preserved records'),'visual_acceptance':False})
    findings=['Admission gates precede rankings;method comparison and port equivalence have separate objectives.',
      'Paired requested-denominator law and covariance explain different conditional/available and decision outcomes.',
      'Fixed Bernoulli inversion yields299 and505 requests for stated one-percent limits;not an executed qualification.',
      'Triangle-inequality numerical enclosure and full maintenance arithmetic connect procedural accuracy and acquisition choices.',
      'Package details retain inspected source scope;new counts and costs are explicitly authored;logs stay outside narrative.']
    write(BASE/'draft-author-review.json',{'status':'pass','reviewer':REVIEWER,'scope':'Source and mathematical draft review;compiled depth assessed separately',
      'findings':findings,'evidence':[ref(p,'Reviewed draft input') for p in [CHAPTER,BASE/'exact-results.json',BASE/'primary-review.json',BASE/'qualification-design.json',BASE/'source-audit.json']],
      'limitations':LIMITS})
    write(BASE/'progress-01.json',{'finding':'Connected chapter drafted and mathematically reviewed;four exact reference families reproduce;inherited primary claims bound.',
      'next_action':'Compile preserving reader,inspect extracted chapter,review nonduplicate substantive pages,record draft and review outcomes,and renew supported author acceptance.',
      'evidence':[ref(p,'Draft checkpoint evidence') for p in [CHAPTER,BASE/'draft-author-review.json',BASE/'plan.md']]})
    transition('progress','TEXT.DRAFT.S10',BASE/'progress-01.json')
    print(json.dumps({'draft_review':'pass','inherited_keys':len(inherited),'new_keys':2}))

if __name__=='__main__':main()

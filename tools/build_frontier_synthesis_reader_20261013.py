#!/usr/bin/env python3
"""Integrate the frontier evidence chapter, preserving all earlier source bytes."""
import argparse
import contextlib
import json
from pathlib import Path
import re
import build_integrated_monograph_v12 as shared
import build_java_reader_20261013 as inherited
import master_control as core

ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-13/frontier-synthesis'
OUT=BASE/'reader'
NAME='causal_proposal_frontier_evidence_2026-10-13'
OLD=ROOT/'docs/causal_proposal_agent_architecture_2026-10-13.tex'
DRIVER=ROOT/'docs'/(NAME+'.tex')
PDF=DRIVER.with_suffix('.pdf')
PRIOR_AUDIT=ROOT/'docs/program/execution/2026-10-13/agent-architecture/reader/source-audit.json'
CHAPTER=ROOT/'docs/program/comprehensive-v14/work/TEXT.DRAFT.L1/chapter.tex'
ref=shared.ref

def configure():
    for key in ['BASE','OUT','NAME','OLD','DRIVER','PDF','PRIOR_AUDIT']:setattr(inherited,key,globals()[key])

def expected_driver():
    text=OLD.read_text()
    marker=r'\input{program/repair-v12/work/LA07/frontier-chapter.tex}'
    assert text.count(marker)==1
    text=text.replace(marker,r'\input{program/comprehensive-v14/work/TEXT.DRAFT.L1/chapter.tex}',1)
    marker='program/execution/2026-10-13/agent-architecture/refs}'
    assert text.count(marker)==1
    text=text.replace(marker,'program/execution/2026-10-13/agent-architecture/refs,program/execution/2026-10-13/frontier-synthesis/refs}',1)
    return text.replace('Proposal working edition with developed software contract','Proposal working edition with developed frontier evidence',1)

def prepare():
    configure();inherited.guard()
    prior=json.loads(PRIOR_AUDIT.read_text());shared.verify_refs(prior)
    text=(BASE/'development.tex').read_text()
    cited={k.strip() for g in re.findall(shared.CITE,text) for k in g.split(',')}
    bykey={s['integrated_citation_key']:s for s in prior['sources']}
    assert cited-bykey.keys()=={'exec13_frontier_exact'}
    inspections=[
      ('v12_la_2305_00050','Physical pages18,30,32: memorization probes and proposed graph/workflow roles'),
      ('v12_la_2312_04350','Physical pages3,8,10: generated formal tasks and remaining language-to-tool problem'),
      ('v12_la_2402_15301','Physical page8: ASIA retrieval decline, CORONARY improvement and SACHS limitations'),
      ('v12_la_2609_30867','Physical pages2,6,9: support auditing, flaw injection, five-paper pilot and in-sample calibration'),
      ('exec13_census_causaleval','Physical pages6,7,18,19: task-specific scores, samples, repeated questions and human comparator'),
      ('exec13_census_graph_validation','Physical pages4-6: labeled training, DDI F1 and pairwise scope'),
      ('exec13_census_collaboration','Physical pages4-7: sequential assumptions, text-version functional and generated evaluation components')
    ]
    primary={'status':'pass','cutoff':'2026-10-07','inspection_date':'2026-10-13',
      'sources':[{'source_record':bykey[key],'inspected_anchor':anchor} for key,anchor in inspections],
      'findings':['Benchmark task, information, assumptions, oracle, budget and loss are compared separately.','Published point scores are used in an explicitly illustrative reweighting, with no invented standard errors or bank workload weights.','Both retrieval gains and adverse cases remain; document support does not adjudicate assumption truth.','Supervised extraction and deterministic/formal tools remain substantive alternatives to general agents.','Sequential text interventions retain the source theorem premises and version-mixture boundary.'],
      'inherited_search_limits':ref(ROOT/'docs/program/execution/2026-10-13/llm-census/search-ledger.json','Bounded search and failure record'),
      'inherited_omissions':ref(ROOT/'docs/program/execution/2026-10-13/llm-census/census-register.json','Unread originals and unsaturated specialist routes remain open'),
      'scope':'Primary-corpus reinspection and frontier chapter synthesis, not new search saturation, live performance or code qualification'}
    core.write(BASE/'primary-review.json',primary)
    results=json.loads((BASE/'exact-results.json').read_text())
    assert results['workflow_composition']['conditional_chain_success']=='2438289/3125000'
    core.write(BASE/'mathematical-review.json',{'status':'pass','evidence':[ref(BASE/'exact-results.json','Exact rational values and independent constructed cases'),ref(ROOT/'tools/frontier_evidence_examples_20261013.py','Exact calculations'),ref(BASE/'development.tex','Derivations and limitations')],
      'findings':['Mixture ranking switches at17/24 for the supplied published point scores.','The conditional chain rule requires no independence; marginal scores permit a .76-.90 joint-success range, attained by disjoint/nested failures.','The indicator disagreement inequality bounds truth accuracy by label agreement plus/minus the specified label-error rate; two100-case examples attain the bounds.','Equal-law action probability yields minimax expected regret125 USD in the two-world authored scenario.'],
      'scope':'Author-reviewed finite calculations and elementary derivations; not a sampled empirical study, new general inference theorem or independent review'})
    source={'integrated_citation_key':'exec13_frontier_exact','kind':'project_derivation',
      'title':'Exact task-mixture, workflow-composition, answer-key and decision-regret examples',
      'author':'Causal banking proposal project','year':2026,'version_date':'2026-10-13',
      'source_identity':'Authored exact evidence-composition examples with a labeled reweighting of published point scores',
      'local_copy':ref(BASE/'exact-results.json','benchmark_mixture, workflow_composition, oracle_error and decision_ambiguity'),
      'code':ref(ROOT/'tools/frontier_evidence_examples_20261013.py','Fractions, independent enumeration and explicit finite populations'),
      'review':ref(BASE/'mathematical-review.json','Author review'),
      'inspected_anchors':['benchmark_mixture','workflow_composition','oracle_error','decision_ambiguity'],
      'supported_claims':['Illustrative method ranking changes at formal-task weight17/24.','Stipulated conditional success is.78025248; the same marginal probabilities admit joint success.76-.90.','Agreement.9 and stipulated key error.1 admit truth accuracy.8 or1.','Restricted two-world minimax expected regret is125 USD.'],
      'limits':'No new live/model/backend execution, estimated oracle error, bank mixture, prices or external acceptance.'}
    core.write(BASE/'source-audit.json',{'sources':[source],'cutoff':'2026-10-07','primary_reinspection':ref(BASE/'primary-review.json','Primary source comparisons'),'scholarship_status':'Draft chapter evidence; whole MR02 coverage review still open'})
    (BASE/'refs.bib').write_text('@misc{exec13_frontier_exact,\n author={{Causal banking proposal project}},\n title={'+source['title']+'},\n year={2026},\n note={13 October 2026; exact authored examples}\n}\n')
    DRIVER.write_text(expected_driver())
    core.write(BASE/'prepared-inputs.json',{'inputs':[ref(p,'Reviewed preserving input') for p in [OLD,PRIOR_AUDIT,CHAPTER,BASE/'development.tex',BASE/'source-audit.json',BASE/'primary-review.json',BASE/'mathematical-review.json',Path(__file__)]],'generated':[ref(DRIVER,'Preserving driver'),ref(BASE/'refs.bib','Project evidence citation')]})
    print(json.dumps({'prepared':str(DRIVER.relative_to(ROOT)),'primary_records_reinspected':len(inspections),'new_project_records':1}))

def build():
    configure();OUT.mkdir(exist_ok=True)
    for suffix in ['.aux','.bbl','.toc','.out']:
        p=OUT/(NAME+suffix)
        if not p.exists():p.write_text('')
    with (OUT/'compile-summary.txt').open('w') as output,contextlib.redirect_stdout(output):inherited.build()
    report=json.loads((OUT/'build-report.json').read_text());report.pop('java_comparison',None)
    aux=(OUT/(NAME+'.aux')).read_text()
    def page(label):return int(re.search(r'\\newlabel\{'+re.escape(label)+r'\}\{\{[^}]*\}\{(\d+)\}',aux).group(1))
    report.update(builder=ref(Path(__file__),'Preserving frontier chapter builder'),compile_routine=ref(ROOT/'tools/build_java_reader_20261013.py','Bounded compiler'),pdf=ref(PDF,'Working frontier evidence successor'),predecessor_pdf=ref(OLD.with_suffix('.pdf'),'Preserved620-page reader'),frontier_chapter={'chapter_first_printed_page':page('la:frontier'),'addition_first_printed_page':page('exec13:frontier-synthesis'),'addition_last_printed_page':page('exec13:frontier-synthesis-end')},visual_review='Whole-reader visual acceptance remains open under inherited image allowance.')
    audit=json.loads((OUT/'source-audit.json').read_text());audit['added_bibliography']=ref(BASE/'refs.bib','Frontier project citation');core.write(OUT/'source-audit.json',audit)
    report['source_audit']=ref(OUT/'source-audit.json','Whole-reader source traceability');core.write(OUT/'build-report.json',report)
    print(json.dumps({k:report[k] for k in ['pages','cited_records','frontier_chapter']}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','build']);a=p.parse_args();prepare() if a.command=='prepare' else build()

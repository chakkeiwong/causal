#!/usr/bin/env python3
"""Review L6 development and preserve remaining backend coverage explicitly."""
import argparse
import json
from pathlib import Path
import re

import build_l6_architecture_v2_20261014 as build
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref,transition,verify_bindings,write

ROOT,BASE,OUT=build.ROOT,build.BASE,build.OUT
REVIEWER=build.REVIEWER
LIMITS=[
 'Author source/content review; no independent scientific or bank acceptance.',
 'Local/hosted model contracts are prospective; no new named-provider capability/price or empirical ranking.',
 'Three pinned frameworks and selected causal packages do not close the broader backend/framework census.',
 'Exact state, budget, set and factorial examples are stipulated project constructions, not model performance or bank ROI.',
 'Original local prototype evidence is preserved; no downloaded framework or live model execution.',
 'L6 meets minimum depth but full coverage review remains inconclusive; MR01/MR02/MR03 and Q1 remain open.',
 'Rendered visual acceptance and Q5 remain open under the exhausted inherited image allowance.',
]
REVIEW=ROOT/'docs/program/comprehensive-v14/work/TEXT.REVIEW.L6/chapter-review.json'


def review():
 report=json.loads((OUT/'build-report.json').read_text())
 audit=json.loads((OUT/'source-audit.json').read_text())
 prior=json.loads(build.PRIOR.read_text())
 index=json.loads((BASE/'traceability-review.json').read_text())
 for value in [report,audit,prior,index,json.loads((BASE/'prepared-inputs.json').read_text())]:verify_bindings(value)
 assert index['status']=='pass' and not index['issues'] and index['scholarly_pdfs']==156
 assert json.loads((OUT/'text-layout-review.json').read_text())['status']=='pass'
 assert not [w for w in report['warnings']if 'Underfull'not in w]
 old={r['integrated_citation_key']:r for r in prior['sources']}
 new={r['integrated_citation_key']:r for r in audit['sources']}
 assert len(old)==534 and len(new)==538
 assert new.keys()-old.keys()=={'exec14_l6_design','exec14_l6_exact','exec14_l6_local','exec14_l6_adapter_exact'}
 assert all(new[k]==v for k,v in old.items())
 files={r['path']:r for r in audit['tex_files']}
 inherited=[r for r in prior['tex_files']if r['path']not in [str(build.OLD.relative_to(ROOT)),str(build.prior.PROTOTYPE.relative_to(ROOT))]]
 assert all(files[r['path']]['sha256']==r['sha256']for r in inherited)
 original=build.prior.PROTOTYPE.read_text()
 assert (build.prior.BASE/'prototype-body.tex').read_text()==original[original.index(r'\section{The implemented boundary}'):]
 original_development=(build.prior.BASE/'development.tex').read_text()
 assert (BASE/'development.tex').read_text()==original_development.replace(r'\cite{',r'\citep{').replace(r'.\citep{',r'. \citep{')
 assert build.prior.calculate()==json.loads((build.prior.BASE/'exact-results.json').read_text())
 assert build.calculate()==json.loads((BASE/'exact-results.json').read_text())
 prev=json.loads((build.PRIOR.parent.parent/'traceability-review.json').read_text())
 contexts={r['citation_key']:r['citation_contexts']for r in index['records']}
 assert all(all(c in contexts[r['citation_key']]for c in r['citation_contexts'])for r in prev['records'])
 changed=[r['citation_key']for r in prev['records']if r['citation_contexts']!=contexts[r['citation_key']]]
 selected=json.loads((build.prior.BASE/'primary-review.json').read_text())['selected_inherited_records']
 assert set(changed)=={r['integrated_citation_key']for r in selected}
 text=re.sub(r's+',' ',(OUT/'reader.txt').read_text())
 for phrase in ['Shared budgets require reservations','An adapter must preserve the scientific object',
                'Attribute improvements to the component that changed','120 total loss units and B 150',
                'a thousandfold error','not a complete census of all']:
  assert phrase.lower()in text.lower(),phrase
 evidence=[ref(p,anchor)for p,anchor in [
  (OUT/'build-report.json','Exact730-page successor'),(OUT/'source-audit.json','538 cited records'),
  (OUT/'reader.txt','Inspected printed439-452, physical457-470'),
  (OUT/'text-layout-review.json','Every-page extraction and bounds'),
  (BASE/'traceability-review.json','Whole-reader citation contexts;156 scholarly PDFs'),
  (BASE/'prepared-inputs.json','Preserving successor inputs'),
  (BASE/'repair-review.json','Depth/format repair and prior attempt'),
  (BASE/'exact-results.json','Exact adapter, factorial and denominator examples'),
  (build.prior.BASE/'exact-results.json','Exact dependency, unknown-outcome, reservation and route examples'),
  (build.prior.BASE/'primary-review.json','Pinned source reinspection and inherited package contexts'),
  (build.prior.BASE/'local-evidence-review.json','Preserved local implementation/trials'),
  (build.prior.BASE/'omissions-register.json','Current official source-access and broader census limitations'),
  (Path(__file__).resolve(),'Exact author review procedure')]]
 findings=[
  'Scientific responsibilities, backend alternatives and three pinned framework choices are explained with explicit reuse conditions; no causal engine ability inferred from orchestration.',
  'Four original exact examples and set/factorial/availability successors reproduce; mathematical invariants retain their atomicity, complete-dependency, fixed-map and evaluation-law premises.',
  'Lossy endpoint/set encodings cannot be inverted uniquely; fixed known bijective set images preserve existing coverage, without validating the original inference.',
  'Matched four-cell contrasts distinguish backend and framework changes; missed/returned answer losses change ranking under explicitly stipulated costs.',
  'New citation typography repaired; original prototype body and every other inherited chapter preserved; all original citation contexts retained,13 keys gain inspected contexts.',
  'Ten nonduplicate substantive pages meet minimum10, but full commercial/local provider and broader framework comparative coverage remains unclosed.',
 ]
 write(BASE/'release-source-review.json',{'status':'pass','issues':[],'reviewer':REVIEWER,
   'scope':'Scoped draft source/mathematics and text review; coverage completion not awarded',
   'reviewed_reader':report['pdf'],'findings':findings,'evidence':evidence,
   'unchanged_source_records':534,'new_source_records':sorted(new.keys()-old.keys()),
   'changed_existing_context_keys':changed,'all_old_contexts_retained':True,
   'unchanged_inherited_compiled_sources':len(inherited),'prototype_body_exact':True,
   'limitations':LIMITS,'visual_acceptance':False})
 credits=[(.5,'State/contract setup; repeated causal framing discounted'),(.75,'Backend contracts; overlap discounted'),
  (.5,'Framework-specific choices; earlier architecture mechanics discounted'),(.25,'Framework/package recap mostly excluded'),
  (.75,'Dependency invariant and selective invalidation; package overlap excluded'),(1,'Unknown outcome and reservation proofs'),
  (.75,'Routing threshold; repeated evaluation framing excluded'),(.75,'New adapter relation and encoding impossibility; repeated status framing excluded'),
  (1,'Set transforms, coverage premises and exact banking consequences'),(1,'Factorial attribution and denominator-loss comparison'),
  (.75,'New rubric distinction .25 plus prototype-specific boundary .5'),(1,'Detailed projection and context/graph qualification'),
  (.75,'Actual local paths and journal/recovery, summary overlap discounted'),(.25,'Historical failed configuration and review evidence; generic future-work text excluded')]
 assert sum(c for c,r in credits)==10
 write(REVIEW,{'operation_id':'TEXT.REVIEW.L6','status':'inconclusive','reviewer':REVIEWER,
   'scope':'Developed L6 and measured minimum depth; broader backend/framework comparison incomplete',
   'allocated_title':'Packages, model backends and auditable agent architecture',
   'allocation':{'min':10,'target':11,'max':12},'substantive_page_credit':10,
   'physical_span':{'first_printed_page':439,'last_printed_page':452,'first_pdf_page':457,'last_pdf_page':470,'pages':14},
   'per_page':[{'printed_page':439+i,'credit':c,'rationale':r}for i,(c,r)in enumerate(credits)],
   'measurement':'Conservative standard-typography page equivalents after excluding process/catalog repetition and adjacent coverage.',
   'double_counting':'Credit assigned to L6 only; previous L5 review excluded architecture/prototype continuation.',
   'allocation_exception':None,'reviewed_reader':report['pdf'],'findings':findings,
   'remaining_coverage':['Named hosted/local backend comparison using authentic applicable official evidence.',
                         'Broader framework census with pinned source/rights/runtime dispositions.'],
   'revisit_trigger':'Acquire and inspect missing provider/framework evidence, develop comparisons, then review a preserved successor.',
   'evidence':evidence+[ref(BASE/'release-source-review.json','Scoped draft/source review')],
   'limitations':LIMITS,'visual_acceptance':False,'original_gap_qualification':False})
 graph,_,_=run.combined(ROOT,core.read(ROOT,core.STATE))
 for identifier,outcome,outputs,facts,verdicts in [
  ('TEXT.DRAFT.L6','pass',[ref(build.prior.CHAPTER,'Preserved first developed chapter'),ref(build.CHAPTER,'Corrected substantive successor')],
   ['Connected scholarly chapter develops scoped architecture, backend contracts, formal adapter/operating invariants and banking consequences.',
    'All537 inherited/new sources from first attempt plus exact successor record are audited; project examples reproduce and local/source/proposed claims remain distinct.'],['pass','pass']),
  ('TEXT.REVIEW.L6','inconclusive',[ref(REVIEW,'Actual depth and coverage review')],
   ['Scoped source/math/notation defects resolved, but full provider and broader framework comparative coverage remains open.',
    'Measured10 nonduplicate substantive pages against10/11/12 allocation; earlier seven-page shortfall preserved.'],['inconclusive','pass'])]:
  node=run.ledger.operation(graph,identifier);receipt=run.ledger.receipt_template(node)
  receipt.update(outcome=outcome,execution='performed',scope='Proposal chapter development and honest source/depth review',
     reviewer=REVIEWER,limitations=LIMITS,outputs=outputs,nonexecution_reason='',
     revisit_trigger=''if outcome=='pass'else 'Missing official provider and broader framework evidence acquired; review successor coverage.',
     criteria=[{'index':i,'verdict':v,'finding':f,'evidence':evidence+[ref(REVIEW,'Measured remaining coverage')]}for i,(v,f)in enumerate(zip(verdicts,facts))])
  write(BASE/('draft-operation-receipt.json'if identifier.startswith('TEXT.DRAFT')else 'review-operation-receipt.json'),receipt)
 print(json.dumps({'draft':'pass','coverage_review':'inconclusive','substantive_pages':10,'pages':report['pages']}))


if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('command',choices=['review']);args=parser.parse_args();review()

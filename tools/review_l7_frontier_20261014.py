#!/usr/bin/env python3
"""Audit two acquired publisher originals and their bounded reuse implications."""
import json
from fractions import Fraction as F
from pathlib import Path
import subprocess
import develop_l7_benchmarking_20261014 as work
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT=work.ROOT
BASE=work.BASE/'frontier'


def exact():
    p=[F(786,1000),F(883,1000),F(917,1000),F(960,1000)]
    lower=max(F(0),sum(p,F(0))-3)
    upper=min(p)
    assert lower==F(273,500) and upper==F(393,500)
    assert lower<=F(614,1000)<=upper
    deviation=F(9-7,7)
    assert deviation>F(15,100)
    return work.serial({
        'status':'Exact project arithmetic; no reconstruction of unpublished records',
        'four_question_probabilities_from_Wang_Table2_GPT4Turbo':p,
        'mean':sum(p,F(0))/4,
        'all_correct_bounds':(lower,upper),
        'reported_all_correct':F(614,1000),
        'independent_fair_binary_guess_all_correct':F(1,16),
        'independence_limit':'Correlated questions/answers need not have chance probability1/16.',
        'Babakov_Llama33_asiam':{'true_nodes':7,'generated_nodes':9,'relative_deviation':deviation,
                               'stated_max_deviation':F(15,100),'meets_stated_count_rule':False},
    })


def main():
    receipts=json.loads((BASE/'acquisition-receipts.json').read_text())
    definitions=[
        ('causalbench','Wang',2024,
         'CausalBench: A Comprehensive Benchmark for Evaluating Causal Reasoning Capabilities of Large Language Models',
         ['Zeyu Wang'],'2024-08-16',9,
         {
             1:'Identity, proceedings and date; dataset link is a lead only.',
             2:'Four perspectives per scenario,100 CLadder seed cases; text/code/math expansion.',
             3:'Manual seeds and GPT-4 Turbo generation; no original dataset bytes inspected.',
             4:'Claimed extraction/inference engine and disagreement-triggered manual review.',
             5:'Estimator outline and IV/front-door mentions; these require their own identification assumptions.',
             6:'Agreement accepted as ground truth; four-question joint versus marginal score definitions.',
             7:'Tables1-3; GPT-4 Turbo math61.4% joint and88.7% overall; cross-domain rankings differ.',
             8:'Hallucination comparison is a separate leaderboard association; stated limitations.',
             9:'CLADDER bibliography attribution differs from the inspected Jin et al. original; requires version/identity reconciliation.',
         },
         [
             'The paper reports a four-perspective group metric across text, math and code; it uses GPT-4 Turbo generation and targeted human review of disagreements.',
             'Joint correctness is a stricter descriptive outcome but neither eliminates guessing nor proves causal understanding.',
             'Reported math GPT-4 Turbo61.4% joint versus88.7% overall is source evidence, not locally replicated performance.',
             'Claimed engine availability, exact dataset/version/count, rights and every causal label remain unverified.',
         ]),
        ('causalgraphbench','Babakov',2025,
         'CausalGraphBench: a Benchmark for Evaluating Language Models capabilities of Causal Graph discovery',
         ['Nikolay Babakov','Ehud Reiter','Alberto Bugarín'],'2025-07-28',19,
         {
             1:'Identity, proceedings/date and repository lead.',
             2:'Named-variable graph reconstruction;163 candidate BNs and source/size selection.',
             3:'35 graphs,14 repository/21 paper; GPT-4o metadata extraction; provenance/size selection.',
             4:'Pair/triplet limited to10 nodes,efficient50; others broader; leave-one-graph fine-tuning.',
             5:'SHD convention reversal costs2; edge normalization; Table2 scoped comparisons; source-recall contamination probe.',
             6:'Table3 false positives and Table4 node recall; graph-size-specific evidence.',
             7:'Less-than15% count deviation and recall>0.85 rule; named asiam contamination flag includes Llama3.3 output9 versus7.',
             8:'Manual JSON intervention; token limits; no underlying-data/classical discovery comparison; paraphrase caveat.',
             18:'Source-conditioned node/edge prompts and model-based semantic matching.',
             19:'Table9 Llama3.3 asiam9 generated/7 true,recall1; matching prompt; low recall not evidence of no training exposure.',
         },
         [
             '35 chosen BN graphs support a named-variable graph reconstruction comparison, not tabular causal identification.',
             'Method size limits and graph provenance differ; exact source metric counts a reversed edge twice.',
             'GPT-4o Table2 small-graph normalized SHD baseline0.65,pair1.67,triplet2.02; these are scoped source-reported outcomes.',
             'The recall/count probe is a diagnostic, without established sensitivity or specificity for training exposure.',
             'Reported Llama3.3 asiam contamination designation conflicts with the stated15% count threshold on the printed9/7 counts.',
         ]),
    ]
    records=[]
    (BASE/'inspected').mkdir(exist_ok=False)
    for (key,surname,year,title,authors,date,pages,anchors,claims),receipt in zip(definitions,receipts):
        pdf=ROOT/receipt['convention_named_pdf']
        assert ref(pdf,'original')['sha256']==receipt['sha256']
        inspected=[]
        for n,finding in anchors.items():
            dest=BASE/'inspected'/(key+'-page-'+str(n)+'.txt')
            subprocess.run(['pdftotext','-f',str(n),'-l',str(n),str(pdf),str(dest)],check=True,timeout=15)
            inspected.append({'pdf_page':n,'finding':finding,'extract':ref(dest,'Inspected publisher primary text')})
        filename_title=pdf.name.rsplit(' '+surname+'(',1)[0]
        records.append({
            'integrated_citation_key':'exec14_l7_'+key,'id':'acl:'+receipt['url'].rsplit('/',1)[-1].removesuffix('.pdf'),
            'kind':'paper','title':title,'filename_title':filename_title,'authors':authors,'first_author':surname,'year':year,
            'url':receipt['url'],'version_date':date+'; publisher proceedings PDF acquired2026-10-14',
            'local_path':str(pdf.relative_to(ROOT)),'sha256':receipt['sha256'],'pages':pages,
            'inspected_anchors':inspected,'supported_claims':claims,
            'acquisition':ref(BASE/'acquisition-receipts.json','Successful bounded publisher reads after preserved sandbox timeouts'),
            'cutoff_status':'Proceedings date before2026-10-07; exact acquired version fixed bySHA256.',
            'limits':[
                'Selected primary-paper inspection; no benchmark, model or package execution.',
                'Original dataset/code, runtime model revisions and complete rights audit remain to be inspected.',
                'Historical results do not establish bank performance, causal graph truth or exposure absence.',
            ],
        })
    write(BASE/'exact-results.json',exact())
    write(BASE/'primary-review.json',{
        'reviewer':work.REVIEWER,'sources':records,
        'exact':ref(BASE/'exact-results.json','Union-bound and threshold arithmetic'),
        'procedure':ref(Path(__file__).resolve(),'Source identity, anchors and independent arithmetic'),
        'scope':'Two relevant formerly uninspected benchmark originals; no exhaustive frontier claim.',
        'reuse_decisions':{
            'causalbench':'Adapt the four-perspective rubric after independent target/oracle checks; defer importing labels or engine until authentic dataset/code/rights inspection.',
            'causalgraphbench':'Use the standardized descriptions and small-graph baseline comparison as a design reference; defer dataset/prompt adoption until rights, graph semantics and discrepancies are resolved.',
        },
    })
    sources=records+[{
        'integrated_citation_key':'exec14_l7_frontier_exact','kind':'project_derivation',
        'title':'Four-question joint-score and graph-recall threshold arithmetic',
        'author':'Causal banking proposal','year':2026,'version_date':'2026-10-14',
        'source_identity':'Exact project arithmetic using explicitly identified source-reported inputs',
        'local_copy':ref(BASE/'exact-results.json','Joint-success bounds and9/7 node-count discrepancy'),
        'inspected_anchors':['All fields'],
        'supported_claims':['Bounds54.6%-78.6% for four-question joint score; independent fair guess1/16;9/7 implies28.57% deviation.'],
        'records':[ref(Path(__file__).resolve(),'Exact Fraction calculations')],
        'limitations':['No raw-data reconstruction or model trial.'],
    }]
    write(BASE/'source-audit.json',{'cutoff':'2026-10-07','sources':sources})
    write(BASE/'candidate-reassessment.json',{
        'resolved_primary_inspection':['LA01-candidate-104','LA01-candidate-108'],
        'evidence':ref(BASE/'primary-review.json','Originals inspected; labels and code not adopted'),
        'remaining':[
            {'candidate':'LA01-candidate-53','scope':'Applied ASCVD discovery case','action':'Inspect genuine original under the discovery census; no claim imported here.'},
            {'candidate':'LA01-candidate-18','scope':'Generic LLM evaluation survey','action':'Retain as adjacent background; not necessary for the derived scoped claims.'},
            {'candidate':'LA01-candidate-0','scope':'Generic agent-memory epistemic admission','action':'Retain as adjacent background; not a causal benchmark claim.'},
        ],
        'remaining_L7_coverage':'Broader search saturation and candidate reconciliation, authentic benchmark bytes/code/rights and exact model settings remain open.',
    })
    for p in ['primary-review.json','source-audit.json','candidate-reassessment.json']:
        verify_bindings(json.loads((BASE/p).read_text()))
    print(json.dumps({'primary_pdfs':2,'new_records':3,'exact_arithmetic':'pass',
                      'reuse':'conditional rubric/reference; dataset and code adoption deferred'}))


if __name__=='__main__':
    main()

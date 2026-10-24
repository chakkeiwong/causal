#!/usr/bin/env python3
"""Primary preprint review with explicit conference-byte and native limits."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
import hashlib,html,json,re
import judge_bias_reference_20261024 as exact
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1];DAY=ROOT/'docs/program/execution/2026-10-24'
BASE=DAY/'census-judge-bias-v1';PRIOR=DAY/'census-affordance-fuzzing-v1';RAW=ROOT/'docs/literature/raw'
read=lambda p:json.loads(p.read_text())
TITLE='MM-JudgeBias: A Benchmark for Evaluating Compositional Biases in MLLM-as-a-Judge'
FILENAME='MM-JudgeBias A Benchmark for Evaluating Compositional Biases in MLLM-as-a-Judge'
LIMITS=['Selected authentic arXiv2604.18164v3 preprint;final ACL2026 PDF not acquired or claimed byte-identical.',
 'Original experiments concern curated pointwise vision-language judging;no bank causal,diagram or estimator qualification.',
 'No model execution,independent replication,figure inspection or dataset/code adoption;source text and metric extraction only.',
 'Authored exact examples use stipulated task truth,costs and losses;not empirical benchmark or bank findings.',
 'Coverage,exact code/data rights,public native validation,visual,independent and final acceptance remain open.']

def main():
    assert not (BASE/'review.json').exists()
    p=ROOT/'docs/papers/versions/arxiv-2604.18164v3'/(FILENAME+' Lee(2026).pdf')
    raw=RAW/'exec24_judgebias_v3.pdf';r=read(RAW/'exec24_judgebias_v3.receipt.json')
    assert p.read_bytes()==raw.read_bytes() and hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
    assert r['url']=='https://arxiv.org/pdf/2604.18164v3' and r['status']=='saved'
    landing=(RAW/'exec24_judgebias_arxiv_identity.html').read_text()
    title=html.unescape(re.search(r'name="citation_title" content="([^"]+)"',landing)[1])
    authors=[html.unescape(x) for x in re.findall(r'name="citation_author" content="([^"]+)"',landing)]
    assert title==TITLE and authors==['Lee, Sua','Park, Sanghee','Im, Jinbae']
    assert '23 Apr 2026 13:57:12 UTC' in landing
    cross=read(RAW/'exec24_judgebias_crossref.json')['message'];assert cross['title'][0]==TITLE
    assert [x['family']+', '+x['given'] for x in cross['author']]==authors
    pages=(BASE/'paper-v3.txt').read_text().split(chr(12));assert len(pages)-1==38 and not pages[-1].strip()
    assert '2604.18164v3' in pages[0] and '23 Apr 2026' in pages[0]
    specs=[(1,1,'Original title,author order,version and restricted multimodal scope.'),
      (4,5,'Query/image/response score;BD conditional on baseline>1;BC normalization;distinct perturbation targets;1804pairs.'),
      (6,7,'29source benchmarks,curation,three runs,26judge-model description,reasoning modes and16384token settings;variance is supporting evidence.'),
      (8,9,'Reported bias-specific tradeoffs,prompt and abstention comparisons;not universal model rankings.'),
      (10,10,'Vision-language,pointwise scoring and multimodal-bias limitations;other domains/modalities are future work.'),
      (19,19,'Twelve human annotators and four query-selection criteria.'),
      (23,23,'N/A judgments excluded from numerical metrics and separately reported as abstention ratio.')]
    identity=[ref(RAW/n,'Authentic source identity/acquisition') for n in ['exec24_judgebias_arxiv_identity.html','exec24_judgebias_arxiv_identity.receipt.json','exec24_judgebias_v3.receipt.json','exec24_judgebias_crossref.json','exec24_judgebias_crossref.receipt.json']]
    source=dict(integrated_citation_key='exec24_judgebias_original',kind='paper',title=TITLE,filename_title=FILENAME,author=' and '.join(authors),first_author='Lee',year=2026,source_identity='https://arxiv.org/abs/2604.18164v3',version_date='arXiv2604.18164v3;23April2026 13:57:12UTC;selected pre-cutoff author original;conference identity corroborated,not bytes',local_path=str(p.relative_to(ROOT)),sha256=r['sha256'],local_copy=ref(p,'Genuine38page selected original'),identity_evidence=identity,inspected_anchors=[dict(anchor=f'Physical PDF pages {a}-{z}',pages=[a,z],finding=f,text_extract=ref(BASE/'paper-v3.txt','Form-feed original extraction')) for a,z,f in specs]+[dict(anchor='Physical page5,left column metric definitions',text_extract=ref(BASE/'metric-left-v3.txt','Bounded column extraction;no figure claim'),finding='Normalized BD and BC equations inspected with explanatory prose')],supported_claims=[f for _,_,f in specs],limitations=LIMITS)
    write(BASE/'paper-identity-review.json',dict(status='pass_for_selected_preprint',title=TITLE,authors=authors,version='2604.18164v3',pages=38,local_copy=source['local_copy'],identity_evidence=identity,earlier_original=ref(ROOT/'docs/papers'/(FILENAME+' Lee(2026).pdf'),'Preserved v1,not cited as v3'),version_difference='v3 is separately retained;query-generation and perturbation descriptions changed fromv1. Metric left-column extraction is identical. No blanket byte/text equivalence.',final_original_gap='ACL2026 final PDF remains unacquired.'))
    assert exact.calculate()==read(BASE/'exact-results.json')
    project=dict(integrated_citation_key='exec24_judgebias_reference',kind='project_derivation_and_exact_reference',title='Authored causal-evaluator correctness,conditional-denominator and decision-loss witnesses',author='Causal banking proposal project',year=2026,source_identity='tools/judge_bias_reference_20261024.py',version_date='24October2026;exact authored finite examples;no native model experiment',local_copy=ref(Path(exact.__file__),'Exact authored metric functions and examples'),inspected_anchors=[ref(BASE/'exact-results.json','Rational arithmetic'),ref(BASE/'development.tex','Explained notation and banking assumptions')],supported_claims=['Constant score7 has BC1 and BD0 yet accepts two invalid claims in four-case oracle.','BD1 in one eligible of two cases;two-point drops normalize to2/9and1.','45correct of50scored versus100submitted gives90percent conditional and45percent all-request.','Stipulated false-accept loss500000USD versus4000USD expert review;15000USD gives150/300/1000over3USD costs.','300attempts on100cases are not300independent cases.'],limitations=LIMITS)
    write(BASE/'source-audit.json',dict(sources=[source,project],new_records=2,new_scholarly_pdfs=1,native_execution=False))
    write(BASE/'mathematical-review.json',dict(status='pass_for_exact_authored_witnesses',findings=project['supported_claims'],evidence=[ref(Path(exact.__file__),'Independent code'),ref(BASE/'exact-results.json','Exact output'),ref(BASE/'development.tex','Connected derivations'),ref(BASE/'metric-left-v3.txt','Inherited definitions')],limitations=LIMITS))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_bounded_argument',findings=['Bias sensitivity,stability,absolute correctness and refusal are distinct.','Conditioned metric populations and baseline normalization explicit.','Original benchmark claims do not become bank causal or native qualification.','Public prototype proposal precedes expensive bank experiments.'],evidence=[ref(BASE/'development.tex','Connected scholarly argument'),ref(BASE/'sponsor-addition.md','Sponsor implications')],visual_acceptance=False))
    omissions=dict(global_blocker=False,items=[dict(gap='candidate225_final_conference_bytes',action='Acquire final ACL2026 PDF by an authorized public route;compare it to the explicitly citedv3 original.'),dict(gap='native_reuse',action='Inspect exact dataset/code licenses and artifacts,model access,task splits,perturbation validity,oracle and full-cost protocol before native experiment.'),dict(gap='frontier_coverage',action='Continue32unread originals and4crosscutting tasks;all prior local access/date limits preserved.'),dict(gap='scientific_transfer',action='Use public/generated causal questions and independent identification/refusal oracles;do not infer bank validity from multimodal scores.')],unknown_without_information=['True bank assignment law,omitted confounding and universal uncertainty cannot be supplied by a judge score.'],limitations=LIMITS)
    write(BASE/'omissions-register.json',omissions)
    reg=deepcopy(read(PRIOR/'census-register.json'));before=deepcopy(reg);byid={x['id']:x for x in reg['items']};row=byid['LA01-candidate-225'];assert row['disposition']=='open_original_not_inspected' and row['title']==TITLE
    row.update(prior_disposition=row['disposition'],disposition='inspected_primary_retained_with_limits',technical_source_review_open=False,source_key=source['integrated_citation_key'],primary_source_record=source,availability='Authentic same-title/author arXivv3original inspected;conference identity corroborated;final conference bytes remain open.',mapping_basis='Primary metrics,curation,operational settings,abstention and limitations inspected.',effect_on_claims='Bounded inherited judge-evaluation findings and separate authored causal acceptance witnesses;no native or bank transfer claim.',next_action='Acquire exact final conference bytes;qualify data/code rights and public causal-oracle fixtures before native adoption.')
    assert len(reg['items'])==117 and all(x==byid[x['id']] for x in before['items'] if x['id']!='LA01-candidate-225')
    counts=dict(Counter(x['disposition'] for x in reg['items']));assert counts['inspected_primary_retained_with_limits']==81 and counts['open_original_not_inspected']==32
    reg.update(counts=counts,supersedes=ref(PRIOR/'census-register.json','Preserved80/33census'),changes=['Candidate225selected authentic preprint inspected;final conference original remains separately open.'],closure=False,interpretation='81of113candidate works have selected originals inspected;32unread and4crosscutting;selected-original inspection is not complete version or coverage acceptance.');write(BASE/'census-register.json',reg)
    mapping=deepcopy(read(PRIOR/'task-map.json'))
    for fam in mapping['task_families']:
        if fam['id'] in ['diagram_construction','evaluation_cost','reporting_monitoring']:
            fam['inspected_source_keys']=list(dict.fromkeys(fam.get('inspected_source_keys',[])+[source['integrated_citation_key'],project['integrated_citation_key']]))
        if 'LA01-candidate-225' in fam.get('uninspected_candidate_ids',[]):fam['uninspected_candidate_ids'].remove('LA01-candidate-225')
        if 'LA01-candidate-225' in fam.get('inherited_ids',[]):fam['inspected_candidate_ids']=list(dict.fromkeys(fam.get('inspected_candidate_ids',[])+['LA01-candidate-225']))
        fam['coverage_acceptance']=False
    mapping.update(register=ref(BASE/'census-register.json','81/32scoped census'),supersedes=ref(PRIOR/'task-map.json','Preserved task map'));write(BASE/'task-map.json',mapping)
    write(BASE/'plan-review.json',dict(status='pass_for_scoped_preserving_integration',findings=['Exactv3original and earlier-v1 distinction;unacquired final edition remains omitted.','Metrics,denominators,validity of perturbations and banking consequences connected.','All other census entries unchanged;no market-wide or native closure.','Preserve1178records/256papers;add2records/1paper.'],evidence=[ref(BASE/n,'Reviewed foundation') for n in ['plan.md','paper-identity-review.json','source-audit.json','mathematical-review.json','omissions-register.json','census-register.json']]))
    evidence=[ref(BASE/n,'Reviewed evidence') for n in ['paper-identity-review.json','source-audit.json','exact-results.json','mathematical-review.json','copyedit-review.json','plan-review.json','development.tex','sponsor-addition.md','omissions-register.json','census-register.json','task-map.json']]+[ref(Path(__file__),'Audit procedure')]
    result=dict(status='pass_for_scoped_primary_review',reviewer=dict(name='Codex author/coordinator',kind='author'),candidates=['LA01-candidate-225'],evidence=evidence,findings=['81inspected/32unread plus4crosscutting;final conference bytes retained as separate omission.','Selected original metrics and methods inspected;exact project counterexamples reproduce.','Evaluator reliability does not establish causal identification or bank value.'],limitations=LIMITS,coverage_acceptance=False,native_execution=False,visual_acceptance=False)
    verify_bindings(result);write(BASE/'review.json',result)
    write(BASE/'progress.json',dict(finding='Candidate225selected authentic preprint inspected;81inspected/32unread plus4crosscutting;bounded evaluator-bias and causal-acceptance distinction.',next_action='Integrate preserving judge-bias reader and paired sponsor after MCP publication;continue32unread originals and independent backend/software obligations;final conference bytes remain an omission.',yield_reason='Reviewed source unit proceeds to integration;independent work continues.',evidence=[ref(BASE/'review.json','Primary review'),ref(BASE/'census-register.json','81/32census')]))
    print(json.dumps(dict(records=2,new_genuine_papers=1,census_inspected=81,census_unread=32,native_execution=False)))

if __name__=='__main__':main()

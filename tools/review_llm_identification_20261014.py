#!/usr/bin/env python3
"""Bind identification literature, static package paths and exact IV references."""
from collections import defaultdict
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import run_program as control
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings

ROOT=control.core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-14/llm-identification'
SYN=ROOT/'docs/program/comprehensive-v14/work/LL.TASK.identification/task-synthesis.md'
OP='LL.TASK.identification'
AUDIT=ROOT/'docs/program/execution/2026-10-14/causalpy-reuse/publication/reader/source-audit.json'
PIN='66f2d59b0cf74dfabf0a83704bd1de708f8520ac'
REVIEWER={'name':'Codex author/coordinator','kind':'author'}
LIMITS=['Literature findings are author-reported; no live LLM calls, upstream package execution or bank validation.',
    'Selected primary texts and static paths do not establish exhaustive frontier coverage or complete dependency/data rights.',
    'Formal proofs and exact examples are conditional on supplied statements and mechanisms, not business-assumption truth.',
    'Rendered visual acceptance remains open under the inherited image allowance.']


def exact():
    weights={'always':F(1,4),'never':F(1,4),'complier':F(1,2)}
    treatment={'always':(1,1),'never':(0,0),'complier':(0,1)}
    laws=[{'always':(0,1),'never':(0,1),'complier':(0,1)},
          {'always':(1,1),'never':(0,0),'complier':(0,1)}]
    worlds=[]
    for law in laws:
        observed=defaultdict(F)
        for s,p in weights.items():
            for z in (0,1):
                t=treatment[s][z];y=law[s][t];observed[z,t,y]+=p/2
        means_t=[sum(p*t for (zz,t,y),p in observed.items()if zz==z)*2 for z in (0,1)]
        means_y=[sum(p*y for (zz,t,y),p in observed.items()if zz==z)*2 for z in (0,1)]
        ate=sum(weights[s]*(law[s][1]-law[s][0])for s in weights)
        wald=(means_y[1]-means_y[0])/(means_t[1]-means_t[0])
        assert means_t==means_y==[F(1,4),F(3,4)]and wald==1
        worlds.append({'potential_outcomes':{s:list(v)for s,v in law.items()},
            'observed_joint':{str(k):str(p)for k,p in sorted(observed.items())},
            'treatment_means':list(map(str,means_t)),'outcome_means':list(map(str,means_y)),
            'wald':str(wald),'population_ate':str(ate),'net_treat_all_vs_none_USD':str(100*ate-75)})
    assert worlds[0]['observed_joint']==worlds[1]['observed_joint']
    assert [w['population_ate']for w in worlds]==['1','1/2']
    return {'kind':'exact_project_reference','random_draws':0,'model_calls':0,'upstream_execution':False,
        'banking_question':'Encouragement Z at time0, actual servicing A before day7, repayment Y by day30; eligible population at time0.',
        'assumptions':['Z independent of principal stratum and both potential outcomes','Exclusion: Z acts only through A',
            'Consistency, binary outcomes, no interference, monotone take-up with no defiers','Complier fraction1/2 gives nonzero first stage'],
        'stratum_probabilities':{k:str(v)for k,v in weights.items()},'take_up_by_Z':treatment,'worlds':worlds,
        'identified_complier_effect':'1','population_ate_compatible_range':['1/2','1'],
        'range_scope':'Under this stipulated binary monotone model and observed law; missing never-taker Y1 and always-taker Y0 vary in[0,1]. Convex mixtures attain interior values.',
        'economics':{'benefit_USD':'100','cost_USD':'75','population_policy_net_range':['-25','25'],
            'complier_net':'25','scope':'Treat-all versus treat-none thought experiment; not the encouragement-policy value or bank ROI.'},
        'semantic_cases':[
            {'case':'valid instrument plus local target','result':'identified conditional complier effect'},
            {'case':'same instrument plus population target','result':'not point identified under stipulated class; retain compatible range'},
            {'case':'missing target node','result':'unknown with invalid_request'},
            {'case':'criterion unsupported or engine timeout','result':'unknown with reason; not a nonidentification certificate'}]}


def main():
    assert SYN.exists()and not(BASE/'operation-receipt.json').exists()
    root=ET.fromstring((BASE/'versions.xml').read_text());ns={'a':'http://www.w3.org/2005/Atom'}
    entries={e.findtext('a:id',namespaces=ns).rsplit('/',1)[1]:e for e in root.findall('a:entry',ns)}
    specs=[('counterbench','2502.11008v1','Chen',2025,'CounterBench A Benchmark for Counterfactuals Reasoning in Large Language Models',
        [1,3,4,6,7,8],
        ['Version1 uses deterministic SCM questions with binary answers;1000 questions and balanced response classes.',
         'Table3 reports GPT4o52.5 standard,78.8 CausalCoT and92.0 CoIn; Davinci decreases51.8 to49.8. These are author-reported historical outcomes.',
         'CoIn uses elicited graph/state extraction and search/backtracking demonstrations; this is not automatically a checked formal proof.',
         'The authors retain probabilistic dimensions and hidden confounders as future work.']),
        ('meter','2604.11502v1','Li',2026,'METER Evaluating Multi-Level Contextual Causal Reasoning in Large Language Models',
        [1,3,4,5,6],
        ['4145 shared contexts each support questions at three named linguistic levels; answers are five-option choices.',
         'Relation extraction is called discovery; this linguistic taxonomy does not establish observational graph identification.',
         'Intervention/counterfactual options are model-generated then human edited/filtered; these are curated semantic labels, not SCM oracle truth.',
         'Table4 reports GPT4o zero-shot87.92,77.96,67.42 across the three tasks and lower CoT86.46,75.14,66.18.',
         'Reported error analysis distinguishes irrelevant factual distractors, causal reversal, unfounded and contradictory statements.'])]
    new_sources=[]
    for stem,version,surname,year,title,pages,claims in specs:
        e=entries[version];date=e.findtext('a:updated',namespaces=ns);assert date<'2026-10-07T16:00:00Z'
        data=(BASE/(stem+'.pdf')).read_bytes();assert data.startswith(b'%PDF-')
        pdf=ROOT/'docs/papers'/f'{title} {surname}({year}).pdf'
        if pdf.exists():assert pdf.read_bytes()==data
        else:pdf.write_bytes(data)
        texts=(BASE/(stem+'.txt')).read_text().split(chr(12));assert version in texts[0]
        inspected=[]
        for page in pages:
            p=BASE/'inspected'/f'{stem}-page-{page}.txt';p.parent.mkdir(exist_ok=True)
            if p.exists():assert p.read_text()==texts[page-1]
            else:
                with p.open('x')as stream:stream.write(texts[page-1])
            inspected.append({'pdf_page':page,'extract':ref(p,'Selected original PDF text')})
        authors=[a.findtext('a:name',namespaces=ns)for a in e.findall('a:author',ns)]
        discrepancy=None
        if stem=='counterbench':
            discrepancy='PDF title differs from inherited later-title lead; v1 title retained. PDF spells last author Ruixiang Tang; API says Ruxiang Tang.'
            authors[-1]='Ruixiang Tang'
        new_sources.append({'integrated_citation_key':'exec14_ident_'+stem,'kind':'paper','title':e.findtext('a:title',namespaces=ns).strip(),
            'filename_title':title,'first_author':surname,'author':' and '.join(authors),'year':year,'source_identity':'https://arxiv.org/pdf/'+version,
            'version_date':version+'; '+date,'cutoff':'2026-10-07','local_path':str(pdf.relative_to(ROOT)),'sha256':hashlib.sha256(data).hexdigest(),
            'local_copy':ref(pdf,'Genuine original; matched PDF version stamp and metadata'),
            'metadata':ref(BASE/'versions.xml','Identity/version only'),'acquisition_receipt':ref(BASE/'acquisition-01.json','Observed bounded public GETs'),
            'inspected_anchors':inspected,'supported_claims':claims,'identity_discrepancy':discrepancy,
            'extracted_text':ref(BASE/(stem+'.txt'),'Searchable primary text'),'limitations':['Literature outcome only; not local replication or bank evidence.']})
    audit=json.loads(AUDIT.read_text());mapping={s['integrated_citation_key']:s for s in audit['sources']}
    inherited_path=ROOT/'docs/program/repair-v12/work/LA01/source-audit.json'
    inherited={s['id']:s for s in json.loads(inherited_path.read_text())['sources']}
    missing_key='v12_la_2410_06392'
    if missing_key not in mapping:
        restored=dict(inherited[missing_key]);restored['integrated_citation_key']=missing_key
        new_sources.append(restored);mapping[missing_key]=restored
    rereads=[]
    selections=[('v12_la_2312_04350','docs/program/repair-v12/work/LA01/extracted/2312.04350.txt',[3,4],
        ['Formal engine/questions are distinguished from language formulation; reported prompting gains are scoped to dataset and model.']),
        ('v12_la_2607_08093','docs/program/repair-v12/work/LA01/extracted/2607.08093.txt',[3,10],
        ['PopulationATE and counterfactual identification are separate gates; conceptual law differs from noisy observed proxies.',
         'Public scene files and private truth/scoring are separated; reported model results are not local replication.']),
        ('v12_la_2410_06392','docs/program/repair-v12/work/LA01/extracted/2410.06392.txt',[6,10],
        ['Correct graph does not remove mechanism-evaluation errors; real-world counterfactual truth was proxied with LLM outputs.']),
        ('exec13_census_causalsmith','docs/program/execution/2026-10-13/llm-census/causalsmith.txt',[12,14,17],
        ['Type checking and faithful statement matching are separate; self-rated research quality lacks independent human validation.',
         '144 recorded runs include14 accepted,59 downgraded,71 failed;94 identification/SCM runs yield one acceptance.'])]
    for key,path,pages,claims in selections:
        source=mapping[key];texts=(ROOT/path).read_text().split(chr(12));extracts=[]
        for page in pages:
            p=BASE/'inspected'/f'{key}-page-{page}.txt'
            if p.exists():assert p.read_text()==texts[page-1]
            else:
                with p.open('x')as stream:stream.write(texts[page-1])
            extracts.append(ref(p,f'Physical PDF page{page}'))
        rereads.append({'citation_key':key,'preserved_source':source,'primary_text':ref(ROOT/path,'Primary PDF extraction'),
            'inspected_anchors':extracts,'supported_claims':claims})
    tree=json.loads((ROOT/'docs/literature/raw/v12_la_pywhy_llm_tree.json').read_text());assert tree['sha']==PIN and not tree['truncated']
    indexed={r['path']:r['sha']for r in tree['tree']};records=[]
    paths=[('pywhyllm/__init__.py',BASE/'pywhyllm____init__.py','1-15: public imports'),
        ('pywhyllm/protocols/validator.py',BASE/'pywhyllm__protocols__validator.py','complete protocol: methods with pass'),
        ('pywhyllm/suggesters/validation_suggester.py',BASE/'pywhyllm__suggesters__validation_suggester.py','1-24,26-133,231-440: prompted critique, parsing and unbounded retry paths'),
        ('tests/model_suggester/test_simple_identification_suggester.py',BASE/'tests__model_suggester__test_simple_identification_suggester.py','complete three mocked parser tests'),
        ('pywhyllm/suggesters/identification_suggester.py',ROOT/'docs/literature/raw/v12_la_pywhy_llm_source_2.txt','commented estimand, backdoor delegation, frontdoor pass, IV prompts and retry'),
        ('pywhyllm/suggesters/simple_identification_suggester.py',ROOT/'docs/literature/raw/v12_la_pywhy_llm_source_3.txt','complete IV/backdoor/frontdoor prompt and regex methods'),
        ('pywhyllm/protocols/identifier.py',ROOT/'docs/literature/raw/exec14_expert_pywhy_identifier.txt','complete protocol methods')]
    for upstream,path,anchor in paths:
        data=path.read_bytes();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest();assert blob==indexed[upstream]
        records.append({'source_identity':'https://raw.githubusercontent.com/py-why/pywhy-llm/'+PIN+'/'+upstream,
            'revision':PIN,'source_date':'2026-01-06T05:14:41Z','local_copy':ref(path,anchor),'git_blob_sha1':blob,'inspected_anchors':[anchor]})
    packages=json.loads((ROOT/'docs/program/execution/2026-10-14/evaluation-cost/primary-review.json').read_text())['packages']
    package_findings=['PyWhyLLM identification suggestions are prompted variable-name candidates; selected full path contains no formal certificate.',
        'Frontdoor method in IdentificationSuggester is pass; separate SimpleIdentificationSuggester supplies prompted names, not a criterion check.',
        'ValidationSuggester invokes more prompt critique; its name is not evidence of a formal checker. Selected tests mock model output and test parsing.',
        'CLadder selected template associates an IV ratio with an ATE query; unrestricted populationATE needs extra assumptions.',
        'CausalDS preserves None for exceptions and missing backends, but invalid nodes/unobserved targets are False with error codes.',
        'CausalDS DoWhy path returns False when no accepted non-IV method exists; if y0 is absent or errors, a False can remain without a general nonidentification certificate.']
    primary={'cutoff':'2026-10-07 Asia/Shanghai','new_papers':new_sources,'reread_papers':rereads,
        'pywhy':{'revision':PIN,'records':records,'license_evidence':ref(ROOT/'docs/program/execution/2026-10-14/expert-evidence/primary-review.json','Decoded rootMIT license matched to tree'),
            'acquisition_receipt':ref(BASE/'acquisition-02.json','Four successful HTTP200 reads; no source executed')},
        'formal_packages':packages,'additional_inspected_anchors':[
            ref(ROOT/'docs/literature/raw/v12_la_causalds_source_1.txt','120-238,243-331: validation, fallback and false/None boundaries'),
            ref(ROOT/'docs/literature/raw/v12_la_cladder_source_1.txt','57-90: known estimand templates including IV ratio')],
        'package_findings':package_findings,'limitations':LIMITS}
    write(BASE/'primary-review.json',primary);write(BASE/'exact-results.json',exact())
    contract={'status':'proposal_contract','integration_allowed':False,
        'request':['Business decision, eligible population, horizon, information clock, treatment/evidence/query distinctions.',
            'Immutable graph/latent edges, target expression, observation law, assumptions and variable/domain mapping.'],
        'result_states':{'identified':'Expression or value with checked certificate in declared model/query domain.',
            'not_identified':'Witness or applicable complete-method certificate for that exact query/class.',
            'unknown':'Unsupported class, insufficient assumptions, invalid input, timeout, missing backend or unverified negative result.'},
        'separate_fields':['execution_status','scientific_status','reason','engine/version','certificate','assumption IDs','graph/query hashes','target population'],
        'remedies':['Keep model suggestions provisional until evidence/assumption review.',
            'Allowlist variables and validate graph/query before formal calls; do not accept parser output as proof.',
            'Inspect false reasons and fallback traces; preserve criteria failure separately from general nonidentification.',
            'Quarantine IV-as-populationATE answer keys; derive local target or provide additional assumptions.',
            'Check prose-to-formal statement equivalence separately from proof/type checking.',
            'Separate causal identification, numerical estimation, uncertainty and monetary interpretation.'],
        'public_prototype':['Finite SCM oracle with same-observed-law alternatives','Independent formal expression checks',
            'Paraphrase and nonsense-name invariance','Unsupported/invalid/timeout cases','Hidden mechanisms and private scoring',
            'Report false identifications, target substitutions, invalid certificates, unknown reasons and full cost'],
        'open':['Full dataset/generator and runtime/license reviews','Representative translation error and calibrated uncertainty',
            'Independent statement-matching assessment','Bank-specific design truth after justified prototype']}
    write(BASE/'identification-contract.json',contract)
    new_sources += [
        {'integrated_citation_key':'exec14_ident_packages','kind':'software_primary_sources','title':'Prompted identification and formal-backend result semantics',
         'author':'PyWhy Community and CLadder and CausalDS contributors','year':2026,'source_identity':'Pinned original package paths',
         'version_date':'PyWhyLLM66f2d59b; CLadder3d2d1169; CausalDSc74671d0; inspected2026-10-14',
         'local_copy':ref(BASE/'primary-review.json','Selected pinned package originals'),'records':records+packages,
         'inspected_anchors':['PyWhy selected imports/suggesters/protocols/mocked tests; CLadder known estimands; CausalDS120-331'],
         'supported_claims':package_findings},
        {'integrated_citation_key':'exec14_ident_exact','kind':'project_derivation','title':'Exact encouragement, complier and population-effect ambiguity',
         'author':'Causal banking proposal','year':2026,'source_identity':'Project-authored principal-strata law','version_date':'2026-10-14',
         'local_copy':ref(BASE/'exact-results.json','Full exact laws and common observation table'),
         'records':[ref(Path(__file__),'Fraction enumeration')],'inspected_anchors':['exact()'],
         'supported_claims':['Wald/complier effect1, population effects1 and1/2 with same observed law; net treat-all values25 and-25 USD.']},
        {'integrated_citation_key':'exec14_ident_contract','kind':'project_analysis','title':'Three-state identification and faithful translation proposal',
         'author':'Causal banking proposal','year':2026,'source_identity':'Project-authored proposed contract','version_date':'2026-10-14',
         'local_copy':ref(BASE/'identification-contract.json','Result states, failure reasons, prototype and open work'),
         'inspected_anchors':['request/result_states/remedies/public_prototype'],'supported_claims':['Proposed interface preserves uncertainty about identification without enabling an unqualified engine.']}
    ]
    write(BASE/'source-audit.json',{'cutoff':'2026-10-07','sources':new_sources})
    write(BASE/'candidate-reassessment.json',{'resolved':[
        {'id':'LA01-candidate-128','source_key':'exec14_ident_counterbench','disposition':'Authenticv1 inspected; title/version and metadata author spelling differences retained.'},
        {'id':'LA01-candidate-221','source_key':'exec14_ident_meter','disposition':'Authenticv1 inspected; contextual semantic benchmark, not formal identification oracle.'}],
        'reassessed':[{'id':'LA01-candidate-114','source_key':'exec13_census_causalsmith','disposition':'Retain formal checking and statement matching as separate obligations; one acceptance among94 identification/SCM runs.'}],
        'remaining':['CounterBench dataset/generator rights and exact nested/conditional query semantics require item-level review.',
            'METER code/data rights and released-item review remain; curated labels cannot replace a formal engine.',
            'Full CausalSmith source/toolchain and independent statement-faithfulness validation remain.',
            'CausalBench, CausalityCheck and other inherited candidates remain uninspected; no exhaustive closure.'],
        'new_public_reads':7,'prior_failures_preserved':True,'prior_register':ref(ROOT/'docs/program/execution/2026-10-13/llm-census/census-register.json','Inherited dispositions unchanged')})
    evidence=[ref(p,'Reviewed task evidence')for p in[SYN,BASE/'primary-review.json',BASE/'exact-results.json',BASE/'identification-contract.json',BASE/'candidate-reassessment.json',BASE/'plan-review.md',Path(__file__)]]
    verify_bindings(evidence)
    facts=['Six primary papers and scoped pinned package paths compare formal, contextual and counterfactual tasks, favorable/adverse findings and unresolved candidates.',
        'Banking encouragement/take-up/day30 target and exact same-observed-law example distinguish complier effect from population decision value.',
        'All numerical references are exact project algebra; literature results, proposed contracts, model calls and bank truth are explicitly separated.']
    write(BASE/'author-review.json',{'outcome':'pass','reviewer':REVIEWER,'findings':facts,'evidence':evidence,'limitations':LIMITS})
    graph,_,_=control.combined(ROOT,control.core.read(ROOT,control.core.STATE));node=control.ledger.operation(graph,OP)
    receipt=control.ledger.receipt_template(node)
    receipt.update(outcome='pass',execution='performed',scope='Bounded proposal synthesis of LLM-assisted identification and formal result semantics',reviewer=REVIEWER,outputs=[evidence[0]],limitations=LIMITS)
    for c,fact in zip(receipt['criteria'],facts):c.update(verdict='pass',finding=fact,evidence=evidence)
    write(BASE/'operation-receipt.json',receipt)
    print(json.dumps({'status':'reviewed','new_papers':2,'reread_papers':4,'new_source_records':len(new_sources),'exact':exact()}))


if __name__=='__main__':main()

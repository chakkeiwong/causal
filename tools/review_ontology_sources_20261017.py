#!/usr/bin/env python3
"""Bind genuine ontology originals, pinned code and concrete omissions."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import ontology_reference_20261017 as examples
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT, BASE = examples.ROOT, examples.BASE
RAW = ROOT/'docs/literature/raw'
PRIOR = ROOT/'docs/program/execution/2026-10-16/reporting-monitoring/publication-v2/reader/source-audit.json'
OP = 'LL.TASK.variable_ontology'
OUTPUT = ROOT/'docs/program/comprehensive-v14/work'/OP/'task-synthesis.md'
REVIEWER = {'name':'Codex author/coordinator','kind':'author'}
LIMITS = [
    'Bounded proposal synthesis, not an exhaustive census or completed mandatory repair.',
    'Literature findings are author-reported; no upstream package or live-model execution.',
    'Two task candidate originals remain unresolved on the tested public routes.',
    'OntoURL v3 has inconsistent reported definition-generation scores; no aggregate ranking is inferred.',
    'The sociology article is published before cutoff, but its exact modified-edition date remains unresolved.',
    'Typed mappings and declared assumptions do not establish measurement truth or causal sufficiency.',
    'Package dependency/data/model rights and runtime qualification remain incomplete.',
    'Rendered visual acceptance remains open under the inherited exhausted six-preview allowance.'
]


def read(path):
    return json.loads(path.read_text())


def extract(raw, target, page):
    if not target.exists():
        subprocess.run(['pdftotext','-f',str(page),'-l',str(page),'-layout',str(raw),str(target)],check=True,timeout=20)
    assert len(target.read_text().strip()) > 60
    return ref(target, f'Physical PDF page {page}')


def main():
    prior = read(PRIOR); verify_bindings(prior)
    assert len(prior['sources']) == 677
    by_key = {s['integrated_citation_key']:s for s in prior['sources']}
    inherited = read(BASE/'inherited-primary-selection.json'); verify_bindings(inherited)
    now = datetime.now(timezone.utc).isoformat()
    selections = [
        (166,'thesis','Modèle ontologique formel, un appui à la sélection des variables pour la construction des modèles multivariés',
         'Pressat-Laffouilhere','Thibaut Pressat-Laffouilhere',2023,BASE/'candidate-166-complete.response',
         'https://theses.hal.science/tel-04500818v1/file/pressat-laffouilhere.pdf',
         'Doctoral thesis; defended 2023-12-19; HAL tel-04500818v1', 'thesis',
         [(141,'Hypothetical and under-validation causal relations retain uncertain status; sensitivity analysis varies uncertain links.'),
          (142,'Recoding creates a different variable; context, domains, missingness and transformations belong to variable definitions.'),
          (183,'A worked case removes uncertain links and reruns the reasoner; explanation traces depend on supplied relations.'),
          (187,'Conclusion describes explicit context, missingness and implicit variables; this is not independent validation of causal truth.')]),
        (189,'kg_challenges','Large Language Models and Knowledge Graphs: Opportunities and Challenges',
         'Pan','Jeff Z. Pan and Simon Razniewski and Jan-Christoph Kalo and Sneha Singhania and Jiaoyan Chen and Stefan Dietze and Hajira Jabeen and Janna Omeliyanenko and Wen Zhang and Matteo Lissandrini and Russa Biswas and Gerard de Melo and Angela Bonifati and Edlira Vakaj and Mauro Dragoni and Damien Graux',
         2023,RAW/'exec17_ontology_kg_challenges.pdf','https://arxiv.org/pdf/2308.06374v1',
         'arXiv:2308.06374v1; 2023-08-11','kg_challenges',
         [(5,'Explicit-knowledge-first and parametric-knowledge-first approaches organize extraction and canonicalization.'),
          (17,'Knowledge-graph context can guide prompting; this position discussion supplies no causal identification guarantee.')]),
        (204,'annotation','Large Language Models for Data Annotation and Synthesis: A Survey','Tan',
         'Zhen Tan and Dawei Li and Song Wang and Alimohammad Beigi and Bohan Jiang and Amrita Bhattacharjee and Mansooreh Karami and Jundong Li and Lu Cheng and Huan Liu',
         2024,BASE/'candidate-204-elevated.response','https://aclanthology.org/2024.emnlp-main.54.pdf',
         'EMNLP 2024, pages 930-957; November 12-16, 2024','candidate-204',
         [(1,'Survey distinguishes annotation generation, assessment and utilization.'),
          (9,'Discusses hallucination, synthetic-feedback model collapse, manual and automatic validation, and efficiency. Underlying cited methods are not newly independently verified.')]),
        (239,'ontourl','OntoURL: A Benchmark for Evaluating Large Language Models on Symbolic Ontological Understanding, Reasoning and Learning',
         'Zhang','Xiao Zhang and Huiyuan Lai and Qianru Meng and Johan Bos',2025,RAW/'exec17_ontology_ontourl_v3.pdf',
         'https://arxiv.org/pdf/2505.11031v3','arXiv:2505.11031v3; 2025-10-02; distinct from inaccessible journal edition','ontourl-v3',
         [(5,'Question construction combines rule extraction, HermiT reasoning, distractors, filtering and expert evaluation.'),
          (8,'Table 2 separates task metrics; Qwen2.5-72B U1=89.1,U2=92.6,R4=75.6,R5=68.4,L2=0.1,L3=0.0,L4=1.0,L5=21.6. L1 table values near79-83 conflict with prose saying typically below10.'),
          (10,'Table 3 also reports L1 on a different apparent scale. Three PhD-level human participants answer30 sampled questions per task while model results cover the full dataset. Prompt effects vary; English, domain and task coverage are limited.')]),
        (270,'sociology','Text as Data and Causal Inference in Sociology','Schwitter',
         'Nicole Schwitter and Ruben L. Bach and Christopher Klamm',2026,BASE/'candidate-270-elevated.response',
         'https://link.springer.com/content/pdf/10.1007/s11577-026-01071-y.pdf',
         'DOI10.1007/s11577-026-01071-y; published2026-04-23; modified publication2026, exact modification date unknown','candidate-270',
         [(1,'Text as outcome, treatment and control have distinct measurement and identification obligations.'),
          (23,'Example reports kappa0.63±0.01 zero-shot and0.78±0.01 three-shot, across three reruns; annotations of real people differ from generated respondent simulations.'),
          (24,'Measurement uncertainty and text-stimulus construction remain substantive modeling choices.'),
          (26,'More typeII than typeI error is discussed for their illustrated noise setting, not a universal theorem about annotation error.'),
          (29,'GIP text is onsite-only; public treatment-data DOI and code URL are leads whose behavior and rights remain unreviewed.')]),
        (283,'kg_roadmap','Unifying Large Language Models and Knowledge Graphs: A Roadmap','Pan',
         'Shirui Pan and Linhao Luo and Yufei Wang and Chen Chen and Jiapu Wang and Xindong Wu',
         2024,RAW/'exec17_ontology_kg_roadmap_v3.pdf','https://arxiv.org/pdf/2306.08302v3',
         'arXiv:2306.08302v3; 2024-01-25; initial version2023-06-14','kg_roadmap_v3',
         [(5,'Distinguishes KG-enhanced LLMs, LLM-augmented KGs and synergized systems.'),
          (18,'Graph retrieval and path-scoring mechanisms target question answering, not identified intervention effects.'),
          (19,'Fusion and attention mechanisms exchange text/graph representations; relevance and redundancy remain issues.')])
    ]
    sources=[]
    for number,key,title,surname,authors,year,raw,url,version,stem,findings in selections:
        data=raw.read_bytes(); assert data.startswith(b'%PDF-')
        subprocess.run(['pdfinfo',str(raw)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,timeout=20)
        filename_title=title.replace(':','')
        target=ROOT/'docs/papers'/f'{filename_title} {surname}({year}).pdf'
        assert not target.exists(); shutil.copyfile(raw,target); assert target.read_bytes()==data
        anchors=[{'anchor':f'Physical PDF page {page}','finding':finding,
                  'extracted_text':extract(raw,BASE/f'{stem}-page-{page}.txt',page)} for page,finding in findings]
        anchors.append({'anchor':'Physical PDF page 1','finding':'Original title, authors and version identity',
                        'extracted_text':extract(raw,BASE/f'{stem}-page-1.txt',1)})
        related=[ref(raw,'Original retrieved bytes')]
        receipt=raw.with_suffix('.receipt.json')
        related.append(ref(receipt if receipt.exists() else raw.with_suffix('.headers'),'Actual retrieval receipt or headers'))
        sources.append({'integrated_citation_key':'exec17_ontology_'+key,'kind':'paper','title':title,
            'filename_title':filename_title,'first_author':surname,'author':authors,'year':year,
            'source_identity':url,'version_date':version,'cutoff':'2026-10-07','accessed_utc':now,
            'local_copy':ref(target,'Genuine primary PDF at inspected anchors'),
            'local_path':str(target.relative_to(ROOT)),'sha256':hashlib.sha256(data).hexdigest(),
            'inspected_anchors':anchors,'supported_claims':[f for _,f in findings],
            'related_primary_bytes':related,'candidate_id':f'LA01-candidate-{number}','limitations':LIMITS})
    write(BASE/'new-paper-audit.json',{'sources':sources})
    code_claims=[
        (0,[(67,85),(104,124),(169,231)],'Dispatch supports term typing, taxonomy, non-taxonomic relations and text2onto. The base data former deduplicates terms/types with sets and has no text2onto branch; subclass behavior must be checked separately. Ground-truth formation retains document-to-term/type links.'),
        (1,[(33,81),(102,124)],'Loader preserves doc_id and extraction_method in document references; missing train/test/validation splits produce warnings and continuation. A generic document link is not an event/availability or causal-variable contract.'),
        (2,[(16,29)],'Evaluator dispatches to four metrics and raises ValueError for unknown task; it does not add causal or clock validation.'),
        (3,[(16,86),(89,125),(129,156),(159,194)],'Text2onto greedily matches token Jaccard after concatenating doc_id and value. Term typing uses normalized sets; taxonomy uses set intersections but list-length denominators. Only equivalentclass, sameas and disjointwith reverse automatically; directed cause reversal is not accepted by this symmetry rule.'),
        (4,[(1,21)],'MIT permits copying and modification subject to notice; this file does not grant rights to every ontology, dataset, model or dependency.')]
    originals=[]
    manifest=read(BASE/'code-manifest.json')
    for number,spans,claim in code_claims:
        req=manifest['requests'][number];path=RAW/(req['id']+'.txt');data=path.read_bytes()
        receipt=read(RAW/(req['id']+'.receipt.json'))
        assert len(data)==req['expected_bytes'] and hashlib.sha256(data).hexdigest()==receipt['sha256']
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert blob==req['blob_sha1'] and receipt['url']==req['url']
        lines=data.decode().splitlines()
        originals.append({'source_identity':req['url'],'version_date':'074a41ba23a85f5b72d4e28da042eab3d50bd90a; 2026-09-03',
            'local_copy':ref(path,req['source_path']),'retrieval':ref(RAW/(req['id']+'.receipt.json'),'Collector receipt'),
            'git_blob_sha1':blob,'inspected_anchors':[{'anchor':f'lines {a}-{min(b,len(lines))}',
                'excerpt':'\n'.join(lines[a-1:min(b,len(lines))])} for a,b in spans],'supported_claims':[claim]})
    for path,spans,claim in [
        ('docs/literature/raw/v12_la_ontolearner_source_1.txt',[(86,114),(172,203),(322,330)],'Ontology loader omits dataset revision in inspected downloads; enabled import-loading failures are logged and processing continues.'),
        ('src/causalbank/problem_contract_v12.py',[(114,140)],'Checks declared measurement/lineage, latent availability, event order, parent availability and decision information. No row-level audit or scientific truth follows.'),
        ('src/causalbank/agent_workflow_v12.py',[(94,141)],'Restricted static ATE projection retains full declarations as evidence and variable identity/role/unit; rejects outcome/loss unit mismatch without utility conversion.')]:
        lines=(ROOT/path).read_text().splitlines()
        originals.append({'local_copy':ref(ROOT/path,claim),'inspected_anchors':[{'anchor':f'lines {a}-{b}',
            'excerpt':'\n'.join(lines[a-1:b])} for a,b in spans],'supported_claims':[claim]})
    papers=[]
    for key,pages in {'exec13_census_texts':[9,11,14,16], 'exec13_census_text_review_arxiv':[4,5,6],
                      'v12_la_2402_07770':[7,8], 'v12_la_2607_01977':[5,24]}.items():
        papers.append({'key':key,'inherited_source':by_key[key],
                       'reread_pages':[ref(BASE/f'{key}-page-{p}.txt',f'Physical PDF page {p}') for p in pages]})
    review={'status':'pass_for_bounded_synthesis','reviewer':REVIEWER,'papers':papers,'new_papers':sources,
            'packages':[inherited['v12_la_package_ontolearner'],inherited['exec13_ontolearner_inspection']],
            'records':originals,'limitations':LIMITS,'runtime_execution':'No downloaded code or model executed'}
    verify_bindings(review);write(BASE/'source-review.json',review)
    candidates=read(BASE/'candidate-selection.json')['items'];rows=[]
    for candidate in candidates:
        number=int(candidate['id'].rsplit('-',1)[1]);paper=next((s for s in sources if s['candidate_id']==candidate['id']),None)
        evidence=[ref(p,'Actual response or headers') for p in sorted(BASE.glob(f'candidate-{number}*'))
                  if p.suffix in ['.response','.headers'] and p.stat().st_size]
        if number==180:
            evidence += [ref(RAW/'exec17_ontology_dementia.receipt.json','Rejected non-PDF response'),
                         ref(RAW/'exec17_ontology_dementia_landing.html','Client Challenge landing page')]
        if paper:
            disposition='inspected_original_bounded_use'
            reason=paper['version_date']+'; only stated technical anchors support claims.'
            evidence.append(paper['local_copy'])
        else:
            disposition='open_original_route_failed'
            reason=('ACM returned403; no technical text used.' if number==41 else
                    'Registered PDF route returned non-PDF; inspected landing page is Client Challenge; no technical claims.')
        rows.append({'id':candidate['id'],'candidate':candidate,'disposition':disposition,'reason':reason,
            'evidence':evidence,'revisit':'Acquire permitted original/edition, inspect method and adverse findings, then review package/data rights.'})
    write(BASE/'candidate-reassessment.json',{'cutoff':'2026-10-07','coverage_acceptance':False,
        'items':rows,'scope':'All eight mapped candidates reassessed; six original works inspected; two unresolved.',
        'version_limits':['OntoURL and Roadmap use cutoff-compatible v3; earlier originals retained.',
            'Sociology publication date is pre-cutoff; exact modified-edition date unknown.',
            'Thesis 25-second partial download retained; only the complete55-second retry is a paper.'],
        'evidence':[ref(BASE/'new-paper-audit.json','Six genuine PDFs'),ref(BASE/'code-manifest.json','Five pinned source originals'),
                    ref(RAW/'exec17_ontology_versions.xml','Version discovery'),ref(RAW/'exec17_ontology_ontourl_versions.xml','OntoURL versions')]})
    search=read(RAW/'exec17_ontology_ontourl_search.json')
    leads=[{'id':r.get('id'),'title':r.get('display_name'),'doi':r.get('doi'),'date':r.get('publication_date'),
            'status':'discovery_metadata_only_uninspected'} for r in search.get('results',[])]
    write(BASE/'omissions-register.json',{'items':[r for r in rows if r['disposition'].startswith('open')],
        'additional_search_leads':leads,'search_scope':'Bounded inherited census plus one OntoURL identity search; no exhaustive frontier assertion.',
        'other_gaps':[
            {'gap':'Exact cutoff-era modified sociology edition','route':'Obtain publisher revision history or dated author original before edition-specific frontier claims.'},
            {'gap':'OntoURL inconsistent L1 scales and unequal human/model evaluation sets','route':'Inspect released raw scores and evaluator at a pinned revision; do not compute an aggregate ranking now.'},
            {'gap':'OntoLearner complete runtime/data/dependency rights and subclass paths','route':'Freeze dataset/model revisions and imports, audit permitted complete distribution, then run bounded generated contract cases.'},
            {'gap':'OntoBioStat, OntoURL and text_treat executable integrations','route':'Review code/license/data originals and target-preserving adapters before any execution claim.'},
            {'gap':'True variable meaning, latent measurement law and causal sufficiency','route':'Public/generated prototype first; expensive representative validation and owner evidence only after demonstrated merit.'}],
        'evidence':[ref(BASE/'candidate-reassessment.json','Source-specific dispositions'),
                    ref(RAW/'exec17_ontology_ontourl_search.json','Saved search metadata')],'limitations':LIMITS})
    print(json.dumps({'new_papers':6,'inherited_papers':4,'pinned_blobs_verified':5,'unresolved_originals':2}))


if __name__=='__main__':main()

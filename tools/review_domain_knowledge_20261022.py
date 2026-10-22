#!/usr/bin/env python3
"""Preserving two-original review and one failed-route follow-up in LL.CENSUS."""
from collections import Counter
import copy
import hashlib
import json
import subprocess
from pathlib import Path
import domain_knowledge_reference_20261022 as exact
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-22/census-domain-knowledge-v1'
PRIOR=ROOT/'docs/program/execution/2026-10-21/census-prophets-v2'
REVIEWER=dict(name='Codex author/coordinator',kind='author')
read=lambda p:json.loads(p.read_text())
LIMITS=[
    'Two authentic originals inspected as extracted technical text; figure pixels and rendered visual acceptance remain unreviewed.',
    'Acquired22 October2026; printed pre-cutoff dates and metadata establish selected editions, not exact historical archive bytes.',
    'Single clinical scenario per paper; no bank effects, graph truth or general model superiority established.',
    'ASCVD supplementary appendix/raw outputs, chronic-pain raw data/code/model outputs and pinned dependencies not acquired or executed.',
    'Ontology publisher returned HTTP403; OpenAlex supplies no alternate repository location. Candidate176 remains unread, not excluded.',
    'Reported rounded graph scores are descriptive; source-author repeats, independent targets and joint outputs are needed for uncertainty.',
    'Source summaries of dependency software and cited literature do not constitute independent package or scholarly-original reviews.',
    'No live model, downloaded code, native package or sibling repository execution; no independent or final acceptance.',
    '59/113 original candidates inspected;54 unread and four crosscutting search obligations remain.']

ASCVD={
 1:'Printed title, authors, publication30October2025, CC-BY-NC notice; abstract more-than-half wording.',
 2:'Statin versus no-treatment scenario; four prompts on GPT-4o and zero-shot on GPT-o1; no fine-tuning claim.',
 3:'Three runs per configuration, two reviewers, risk-score inclusion proxy; reported missing/nonexistent references and one cycle.',
 4:'Figure1-2 captions; pixels not reviewed and no edges transcribed from these images.',
 5:'Instruction cycle and absent time indices; chain prompt no sources; o1 one generated-code repair; citation denominators.',
 6:'Figure4-5 captions only; no image edge-truth verification.',
 7:'Table1 counts; o1 run3 says nine sources then uses denominators six; seven-of-fifteen text begins.',
 8:'Table1 continued;7/15 contain six criteria; source provision and prompt compliance differ from graph truth.',
 9:'Single-scenario and two-reviewer limitations, no fairness evaluation; source hallucinations and proposed human oversight.',
 10:'Disclosures and bibliography; bibliography entries are leads, not inspected originals.',
 11:'Publisher closing page; no additional technical evidence.'}
PAIN={
 1:'Title and18February2026 preprint banner; not peer reviewed; all-rights-reserved notice.',
 2:'Printed title/authors and abstract F1 .745/.714/.636/.396.',
 3:'Abstract continuation and causal-model motivation.',
 4:'Discovery-equivalence limitations and expert reference design.',
 5:'Related-work descriptions; not independent reviews of those originals.',
 6:'1,868 baseline participants; observational cohort; expert ESC-DAG-derived reference.',
 7:'Authors explicitly state reference is cyclic, not a DAG;14 variables and defined knowledge corpus.',
 8:'Figure1 caption and three knowledge-system definitions; no figure-edge transcription.',
 9:'Same corpus as expert reference;600-token chunks with100 overlap; constrained entity/relation extraction.',
 10:'Neo4j, entity resolution, Leiden summaries, local retrieval;8,000-token cap and matched ordinary-RAG context.',
 11:'Mistral7B-Instruct v0.3; author model-date argument does not audit training data.',
 12:'Plausibility/association/temporality prompts allow direct or indirect relationships.',
 13:'Direct query and two-phase existence/orientation procedure.',
 14:'Age/Sex roots, PEG sink; binary direction tie-break; hill-climb GLM/BIC source description.',
 15:'500 bootstraps; moralization adds co-parent edges; union of learned and suggested edges then direction query.',
 16:'TP/FP/FN and FDR/TPR/F1;HD/SHD definitions;100 random graph comparator.',
 17:'Threshold.538 and directed/moralized comparison; no intervention-validation claim.',
 18:'Proto-model table F1.396; random comparator mean.170(sd.054); figure caption only.',
 19:'Figure7 caption; metric-by-threshold text and pre-resolution plausibility scores.',
 20:'Table2 before direction resolution; KG-RAG plausibility.602 below LLM.627.',
 21:'Table3 after direction resolution; KG-RAG.737 versus RAG.706 and LLM.636; different query ranking.',
 22:'Table4 disagreement with proto-model; general improvement interpretation is benchmark-specific.',
 23:'Table5 final scores, FDR.360 and TPR.891; incremental.008 over KG-RAG, .031 over augmented RAG.',
 24:'Authors acknowledge same-document alignment with reference; support-role interpretation.',
 25:'RAG outperforms KG-RAG on association/temporality; local entity retrieval may miss relationships.',
 26:'Combining sources raises floor only in shown results; not a universal guarantee.',
 27:'High false-positive proportions; opposite directions and conflicting source evidence.',
 28:'Single-dataset future work and limitations on determining causality.',
 29:'Conclusion and acknowledgments; no measured bank economics.',
 30:'References begin; no independent support borrowed from bibliography.',
 31:'Expert reference and LLM-discovery citation leads only.',
 32:'GraphRAG/ESC-DAG/tool citation leads only.',
 33:'Embedding, clustering and native package citation leads only.',
 34:'Conflicting-evidence citation leads only.',
 35:'AppendixA.6/A.7 repeated correct/incorrect edges across configurations; correlated votes, not independent experts.',
 36:'FigureA.8 caption; pixels unreviewed.',
 37:'Parent/child aggregate edge counts and definitions; no raw per-run reconstruction.',
 38:'FigureA.9 caption; pixels unreviewed.',
 39:'KG-RAG prompt: insufficient retrieval invites general-knowledge completion; no abstain class.',
 40:'Boolean JSON schema, community/relationship report descriptions and variable definitions.',
 41:'RAG system prompt begins; text-only inspection.',
 42:'RAG Boolean conclusion and general-knowledge fallback; no calibrated uncertainty.',
 43:'RAG example and LLM-only system prompt.',
 44:'LLM-only Boolean schema and example; syntactic constraints do not authenticate claims.',
 45:'Variable definitions, including ambiguous obesity/BMI and financial-strain mappings.'}

def main():
    assert not (BASE/'source-audit.json').exists()
    specs=[dict(name='ascvd',id='LA01-candidate-53',key='exec22_domain_aziz',surname='Aziz',year=2025,
      title='Can Contemporary Large Language Models Provide the Domain Knowledge Needed for Causal Inference? Evaluating Automated Causal Graph Discovery Through an ASCVD Case Study',
      author='Aziz, Maryam and Brookhart, M. Alan',doi='10.2147/CLEP.S550565',date='30 October 2025 publisher edition',pages=ASCVD,
      claims=['Five prompt/model configurations with three runs each; two author reviewers assess one hypothetical statin scenario.',
       'Completeness uses ASCVD predictor inclusion, not a known causal edge graph or valid adjustment-set oracle.',
       'Table1/text report14/15 acyclic graphs and7/15 with six of seven criteria; race omitted in all15.',
       'Sources may be missing, wrong or nonexistent; o1 run3 has nine-versus-six denominator inconsistency; raw appendix is still needed.',
       'Instruction prompt produces a cycle; time indexing is needed if feedback is intended; one o1 graph-code output required manual repair.']),
      dict(name='pain',id='LA01-candidate-182',key='exec22_domain_lin',surname='Lin',year=2026,
      title='Knowledge augmented causal discovery through large language models and knowledge graphs: application in chronic low back pain',
      author='Lin, Damon and Rizi, Marzieh Mussavi and O\'Neill, Conor and Lotz, Jeffrey C. and Anderson, Paul and Torres-Espin, Abel',
      doi='10.64898/2026.02.13.26346255',date='18 February 2026 medRxiv preprint; not peer reviewed',pages=PAIN,
      claims=['Uses baseline records of1868 participants,14 variables and a reference the authors explicitly say contains cycles.',
       'Mistral7B-Instruct v0.3 is used for LLM/RAG/KG-RAG; retrieved articles are the same ones used by experts to build the reference.',
       'KG extraction uses600-token chunks,100 overlap, entity resolution and community summaries; retrieval context is8000 tokens.',
       'Mixed-type GLM/BIC hill climbing with500 bootstrap samples supplies a proto-model; union with suggested edges is followed by reciprocal-direction resolution.',
       'Final plausibility F1 values are.396 proto,.636 augmented LLM,.714 augmented RAG,.745 augmented KG-RAG; KG-RAG without proto is.737.',
       'Before direction resolution KG-RAG plausibility.602 is below LLM.627; ordinary RAG is stronger for association/temporality in the displayed comparisons.',
       'Plausibility/temporality prompts include indirect effects, while evaluation counts directed edges; candidate semantics need explicit reconciliation.',
       'The Boolean schema lacks an abstain class and prompt permits general-knowledge completion; no calibrated edge confidence follows.',
       'Reported high false-positive fractions and conflicting direction evidence motivate support roles and additional datasets.'])]
    sources=[]
    for s in specs:
        acq=BASE/'acquisition/network';original=acq/(s['name']+'-original.pdf')
        receipt=read(acq/(s['name']+'-original.receipt.json'))
        assert receipt['returncode']==0 and receipt['format_valid']
        assert hashlib.sha256(original.read_bytes()).hexdigest()==receipt['sha256']
        metadata=read(acq/(s['name']+'-identity.json'))['message']
        assert metadata['title'][0].casefold()==s['title'].casefold()
        title=s['title'].replace('?','')
        paper=ROOT/'docs/papers'/f'{title} {s["surname"]}({s["year"]}).pdf'
        assert not paper.exists();paper.write_bytes(original.read_bytes())
        info=subprocess.check_output(['pdfinfo',str(paper)],text=True)
        (BASE/(s['name']+'-pdfinfo.txt')).write_text(info)
        assert len([p for p in (BASE/(s['name']+'-original.txt')).read_text().split('\f') if p.strip()])==len(s['pages'])
        anchors=[dict(anchor=f'PDF physical page {n}',finding=finding,
            extracted_text=ref(BASE/f'{s["name"]}-page-{n:02}.txt','Inspected extracted text; figure pixels unreviewed')) for n,finding in s['pages'].items()]
        sources.append(dict(integrated_citation_key=s['key'],kind='paper',title=s['title'],filename_title=title,
            author=s['author'],first_author=s['surname'],year=s['year'],source_identity='https://doi.org/'+s['doi'],
            version_date=s['date']+'; acquired22October2026',cutoff='2026-10-07',local_path=str(paper.relative_to(ROOT)),
            sha256=receipt['sha256'],local_copy=ref(paper,'Genuine original under required scholarly filename'),
            inspected_anchors=anchors,supported_claims=s['claims'],limitations=LIMITS,
            identity_evidence=[ref(acq/(s['name']+'-identity.json'),'Crossref identity only'),
                ref(acq/(s['name']+'-original.receipt.json'),'Original public bytes and acquisition'),
                ref(BASE/(s['name']+'-pdfinfo.txt'),'Observed PDF metadata')]))
    (BASE/'exact-results.json').write_text(json.dumps(exact.calculate(),indent=2)+'\n')
    sources.append(dict(integrated_citation_key='exec22_domain_reference',kind='project_derivation',
        title='Exact graph semantics, observational equivalence and domain-knowledge score comparisons',
        author='Causal banking proposal project',year=2026,version_date='22 October2026',
        source_identity='tools/domain_knowledge_reference_20261022.py',
        local_copy=ref(ROOT/'tools/domain_knowledge_reference_20261022.py','Exact authored arithmetic'),
        inspected_anchors=[ref(BASE/'exact-results.json','Rational covariance, margins and graph witnesses')],
        supported_claims=['Displayed F1 differences.349,.031,.008; no inferred paired significance.',
          'Union can reduce perfect F1 to4/5 and create a three-cycle with no reciprocal pair.',
          'A directed chain has an ancestral pair absent from its direct adjacency.',
          'Two specified centered Gaussian models share covariance[[1,-1/2],[-1/2,1]], with intervention effects-1/2 and0.',
          'At assumed USD100 per loss unit and USD20 incremental cost, margins are30 and-20; subjective mixture threshold2/5.'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,cutoff='2026-10-07',visual_acceptance=False))
    omissions=[dict(id='LA01-candidate-176',status='route_unavailable_original_unread',
        evidence=[ref(BASE/'acquisition/network/ontology-original.receipt.json','Publisher403'),
          ref(ROOT/'docs/literature/raw/domain22_ontology_openalex.json','Only the same publisher location; no alternate repository'),
          ref(BASE/'acquisition/network/ontology-identity.json','Corrected identity:13October2023 online,31October print')],
        next_action='Seek an authorized institutional/author copy or a newly listed public repository; inspect full text before any technical claim; do not bypass access controls.'),
      dict(id='ascvd-reproducibility',next_action='Acquire supplementary appendix and raw15 outputs; reconcile7/15 versus abstract more-than-half, and o1 run3 nine/six references; pin API model/date/configuration.'),
      dict(id='pain-reproducibility',next_action='Recover code, corpus manifest, licenses, model/settings and edge outputs; reconcile direct-edge versus ancestral prompts and cyclic reference; obtain independent reference/corpus splits.'),
      dict(id='public-prototype',next_action='Use public known-law cases with causal and confounded observational twins; compare retrieval methods and uncertain-edge/abstain output at matched budgets before costly bank work.'),
      dict(id='census',next_action='Inspect54 remaining originals and four crosscutting search obligations; ontology failure does not block other candidates.'),
      dict(id='visual',next_action='Inspect original figures and integrated rendered pages in a fresh image allowance; extracted text is not visual acceptance.')]
    write(BASE/'omissions-register.json',dict(global_blocker=None,items=omissions,no_source_waivers=True))
    findings=[claim for s in sources for claim in s['supported_claims']]
    qualifications=[
      'Risk predictor inclusion is a variable-recall proxy; it cannot establish a sufficient adjustment set or require a particular protected-attribute causal role.',
      'A clinical expert graph is a declared reference with its own uncertainty. Same-corpus retrieval measures aligned reconstruction, not independent causal validation.',
      'Moralization adds co-parent links; a moralized comparison is not a direction-free skeleton comparison.',
      'Resolving reciprocal edges does not ensure global acyclicity; graph cycles require explicit temporal or cyclic semantics.',
      'Indirect-effect evidence must not be silently converted to a direct edge among measured variables.',
      'The best displayed KG-RAG score is query-specific; residual FDR.360 is disagreement against that reference, not a certified false-causal-claim probability.',
      'Literal .636-.396=.240 versus printed delta.241 is compatible with rounded underlying scores; do not declare a software defect or corrected result.',
      'Model release timing alone cannot audit contamination, and same-document retrieval is an intentional study condition requiring separate held-out validation.',
      'No general floor-improvement guarantee follows from a table of nonnegative changes; the exact union witness refutes such a generalization.']
    write(BASE/'plan-review.json',dict(status='pass_for_bounded_execution',reviewer=REVIEWER,
        evidence=[ref(BASE/'plan.md','Reviewed execution plan')],
        checks=['Three related leads examined independently; two originals acquired and inspected, one failure scoped.',
          'Review negative findings, metrics, evidence provenance and graph semantics before banking transfer.',
          'Preserve all117 census rows and fourteen task families; publication is not coverage closure.']))
    write(BASE/'primary-review.json',dict(status='pass_for_bounded_primary_text_review',reviewer=REVIEWER,
        findings=findings,qualifications=qualifications,limitations=LIMITS,
        evidence=[ref(BASE/n,'Inspected original evidence') for n in ['source-audit.json','exact-results.json','omissions-register.json']],
        visual_acceptance=False,native_execution=False,coverage_acceptance=False))
    old=read(PRIOR/'census-register.json');new=copy.deepcopy(old)
    mapped=['expert_evidence','diagram_construction','iid_discovery','evaluation_cost']
    for s in specs:
        row=next(r for r in new['items'] if r['id']==s['id']);assert row['disposition']=='open_original_not_inspected'
        row.update(prior_disposition=row['disposition'],disposition='inspected_primary_retained_with_limits',
            technical_source_review_open=False,source_key=s['key'],primary_source_record=next(x for x in sources if x['integrated_citation_key']==s['key']),
            later_primary_review=ref(BASE/'primary-review.json','Bounded technical text review'),task_families=mapped,
            mapping_basis='Inspected source methods, graph target, domain-evidence workflow and empirical limits.',
            availability='Authentic public original acquired; saved initial sandbox failures.',
            effect_on_claims='Supports qualified diagram/evidence workflow design; no calibrated graph truth, bank effect or native qualification.',
            next_action='Recover the listed supplemental/raw/pinned evidence and qualify public known-law cases; continue unrelated originals.')
    row=next(r for r in new['items'] if r['id']=='LA01-candidate-176')
    row.update(availability='Publisher403 preserved; OpenAlex lists only the same route and no repository original.',
        latest_acquisition_review=ref(BASE/'omissions-register.json','Candidate176 remains unread'),
        identity_correction='Crossref13October2023 online/31October print, versus discovery17June2023; no technical text acquired.',
        next_action=omissions[0]['next_action'])
    changed={'LA01-candidate-53','LA01-candidate-176','LA01-candidate-182'}
    assert all(a==b for a,b in zip(old['items'],new['items']) if a['id'] not in changed)
    counts=Counter(r['disposition'] for r in new['items']);assert len(new['items'])==117
    assert counts['inspected_primary_retained_with_limits']==59 and counts['open_original_not_inspected']==54
    new.update(counts=dict(counts),supersedes=ref(PRIOR/'census-register.json','Preserved57/56 register'),
        changes=['Candidates53/182 inspected;176 actual unavailable route recorded;114 other rows unchanged.'],
        evidence=[ref(BASE/'primary-review.json','Two source-critical reviews')],closure=False,
        interpretation='59/113 originals inspected;54 unread including176;four crosscutting search obligations remain.')
    write(BASE/'census-register.json',new)
    tasks=copy.deepcopy(read(PRIOR/'task-map.json'));assert len(tasks['task_families'])==14
    for task in tasks['task_families']:
        for s in specs:
            if s['id'] in task.get('uninspected_candidate_ids',[]):task['uninspected_candidate_ids'].remove(s['id'])
            if task['id'] in mapped:
                for name,value in [('inspected_candidate_ids',s['id']),('inspected_source_keys',s['key'])]:
                    if value not in task.setdefault(name,[]):task[name].append(value)
        task['coverage_acceptance']=False
    tasks.update(register=ref(BASE/'census-register.json','59 inspected/54 unread'),supersedes=ref(PRIOR/'task-map.json','Preserved14-family map'))
    write(BASE/'task-map.json',tasks)
    write(BASE/'reconciliation-review.json',dict(status='pass',changed_ids=sorted(changed),unchanged_other_records=114,
        original_candidates=113,inspected=59,unread=54,task_families=14,
        evidence=[ref(BASE/'census-register.json','All117 rows conserved'),ref(BASE/'task-map.json','Fourteen families conserved')]))
    write(BASE/'conversion-contract.json',dict(status='proposed_not_implemented',integration_allowed=False,
        inputs=['Decision/action/population/horizon/loss units, time-indexed variable definitions and admissible graph semantics.',
          'Retrieved original spans with identity/edition/hash, separate direct/ancestral/associational relations and conflicting evidence.',
          'Optional observed data with sampling/selection constraints; declared latent variables and expert-added constraints.'],
        outputs=['Candidate edges with source support, role/time scope and unresolved status; uncertainty/abstention, not forced direction.',
          'Separate syntactic validation, provenance checks, graph constraints, identification/refusal and effect/value sets.',
          'Typed CLI/MCP request for reviewed tools; no free-form retrieved instruction may invoke a tool or authorize an action.'],
        qualification=['Freeze known-law cases and independent corpora; include hidden confounding, indirect-only relations, cycles and temporal-feedback cases.',
          'Compare data-only, expert-only, ontology-only, LLM, RAG, KG-RAG and mixed systems at matched evidence and token budgets.',
          'Measure direct-edge/ancestral/equivalence metrics, citation entailment, disagreement/abstention, identification validity and cost separately.',
          'Hold out domains/documents and adjudicators; repeat seeds/prompts; count building, retrieval, maintenance and human review costs.',
          'Require public prototype merit before private bank experiments; actual data access/rights and live execution require separately scoped work.'],
        oracle=ref(BASE/'exact-results.json','Exact authored witnesses only')))
    write(BASE/'review.json',dict(status='pass_for_bounded_candidate_inspection',coverage_acceptance=False,limitations=LIMITS,
        evidence=[ref(BASE/n,'Reviewed domain-knowledge continuation') for n in ['primary-review.json','reconciliation-review.json','conversion-contract.json']]))
    write(BASE/'inspection-progress.json',dict(finding='Two original domain-knowledge studies inspected;59/54 census;ontology403 remains scoped. Graph semantics, comparator limits and exact banking witnesses developed.',
        next_action='Integrate source-critical synthesis into paired monograph/sponsor, then continue54 unread originals and complementary searches.',
        evidence=[ref(BASE/n,'Scoped census progress') for n in ['source-audit.json','review.json','census-register.json','task-map.json','omissions-register.json']]))
    verify_bindings(read(BASE/'review.json'));verify_bindings(read(BASE/'source-audit.json'))
    print(json.dumps(dict(inspected=59,unread=54,records=3,scholarly_pdfs_added=2,global_blocker=None)))

if __name__=='__main__':main()

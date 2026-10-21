"""Inspect a genuine ACE original and conservatively update one census entry."""
from collections import Counter
import copy
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import shutil
import ace_reference_20261021 as exact
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-21/census-ace-v1'
PRIOR=ROOT/'docs/program/execution/2026-10-21/census-causalitycheck-v1'
read=lambda p:json.loads(p.read_text())
LIMITS=[
    'Bounded author inspection of a 10-page publisher original; no complete frontier census or independent reproduction.',
    'Publisher date 3 July 2026 and PDF creation 27 June 2026 precede cutoff; later acquisition does not authenticate exact historical bytes.',
    'Results are reported for selected quantized models and three tabular components; narrative evaluation uses dynamic seals.',
    'Full prompts, raw outputs, semantic matches, Sobol design, model revisions and code/dependency rights remain unqualified.',
    'Bowtie extraction fidelity is not causal identification, calibrated intervention uncertainty or banking transfer.',
    'No live model, downloaded code or upstream experiment executed; rendered visual and final acceptance remain open.']


class Metadata(HTMLParser):
    def __init__(self):
        super().__init__();self.items=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag=='meta' and d.get('name','').startswith(('citation_','DC.')):
            self.items.append(d)


def main():
    assert not (BASE/'source-audit.json').exists()
    acq=BASE/'acquisition/network'
    for name,suffix in [('original','pdf'),('identity','html')]:
        receipt=read(acq/(name+'.receipt.json'))
        assert receipt['returncode']==0
        assert receipt['sha256']==hashlib.sha256((acq/(name+'.'+suffix)).read_bytes()).hexdigest()
    pages=(BASE/'original.txt').read_text().split(chr(12))
    assert len([p for p in pages if p.strip()])==10
    assert 'Priyank Venkatesh' in pages[0] and 'Bowtie Diagram Generation' in pages[0]
    metadata=Metadata();metadata.feed((acq/'identity.html').read_text())
    assert any(m.get('name')=='citation_doi' and m['content']=='10.36001/phme.2026.v9i1.4953' for m in metadata.items)
    assert any(m.get('name')=='citation_date' and m['content']=='2026/07/03' for m in metadata.items)
    title='ACE – Automating Causal Extraction: Leveraging Large Language Models for Bowtie Diagram Generation in Failure Analysis'
    filename='ACE Automating Causal Extraction Leveraging Large Language Models for Bowtie Diagram Generation in Failure Analysis'
    paper=ROOT/'docs/papers'/f'{filename} Venkatesh(2026).pdf'
    assert not paper.exists();shutil.copyfile(acq/'original.pdf',paper)
    write(BASE/'exact-results.json',exact.calculate())
    anchors={
        1:'Title, three authors, CC-BY-3.0-US article notice; structured-table versus narrative claims.',
        2:'Bowtie roles, preventive/mitigating barriers and distinction from feedback-loop diagrams; related-work references are leads only.',
        3:'Eight model candidates, four CLD texts, ten hallucination prompts; Python/llama.cpp/GGUF stack; three expert tabular references.',
        4:'Three pipelines and all-MiniLM/FAISS/PaddleOCR/Img2Table/Mistral-Small roles; SBERT .75 semantic alignment; GED count proxy; Sobol and five-expert design.',
        5:'Table 2 model metrics; 80-response categories 21/10/49 versus 9/11/60; 12/32 schema failures; first-order context index interpreted as interchangeability.',
        6:'Selected prompt configurations, ten-seed identity, malformed outputs; Table 4 node/edge gaps and critical-role omissions.',
        7:'Dynamic-seal narratives, absent consequence information, five-expert Table 5 and incorrect critical-event/barrier roles.',
        8:'Quantization explanation without controlled precision ablation; schema fallback hazards; tailored documents, one-pass and single-component limitations; agentic and Neo4j future work.',
        9:'Conclusion retains human review and generalization limits; bibliography for further acquisition.',
        10:'Bibliographic continuation; referenced methods not separately reviewed by citing this paper.'}
    inspected=[]
    for n,finding in anchors.items():
        p=BASE/f'page-{n}.txt';assert not p.exists();p.write_text(pages[n-1])
        inspected.append(dict(anchor=f'Physical/printed PDF page {n}',finding=finding,
            extracted_text=ref(p,'Inspected original text; figures not visually accepted')))
    write(BASE/'version-selection.json',dict(candidate='LA01-candidate-26',title=title,filename_title=filename,
        authors=['Priyank Venkatesh','Jules Oudmans','Florian Zurfluh'],
        doi='10.36001/phme.2026.v9i1.4953',publication='PHM Society European Conference 9(1), 1-10; 3 July 2026',
        pdf_metadata='Created 27 June 2026; metadata Author Jose Ramon Celaya differs from printed authors and is not used as authorship evidence.',
        cutoff='2026-10-07',pages=10,metadata=metadata.items,
        evidence=[ref(acq/'identity.html','Publisher identity'),ref(acq/'original.pdf','Genuine original'),ref(BASE/'pdfinfo.txt','Observed PDF metadata')]))
    claims=[
        'Three pipelines transform structured or narrative FMEA inputs into typed bowtie JSON using retrieval, OCR or vision plus a second model.',
        'Evaluation uses three tabular component references and dynamic-seal narratives, with semantic label matching at cosine threshold .75.',
        'The graph edit distance reported is a false-positive/false-negative count proxy after alignment, not minimum graph edit distance.',
        'Selected tabular configurations have node F1 .81-.94 and edge F1 .58-.93 in Table 4; narrative accuracy ratings range 1.2-3.0 in Table 5.',
        'Ten repeated outputs were reported identical for selected fixed settings; this does not establish the causal mechanism of that stability.',
        'The paper acknowledges tailored prompts, single-component scope, narrative failure and no automatic correction stage.']
    source=dict(integrated_citation_key='exec21_ace',kind='paper',title=title,filename_title=filename,
        first_author='Venkatesh',author='Venkatesh, Priyank and Oudmans, Jules and Zurfluh, Florian',year=2026,
        source_identity='https://papers.phmsociety.org/index.php/phme/article/view/4953; DOI 10.36001/phme.2026.v9i1.4953',
        version_date='3 July 2026 publisher edition; acquired 21 October 2026',cutoff='2026-10-07',
        local_path=str(paper.relative_to(ROOT)),sha256=hashlib.sha256(paper.read_bytes()).hexdigest(),
        local_copy=ref(paper,'Genuine publisher PDF'),inspected_anchors=inspected,supported_claims=claims,limitations=LIMITS,
        identity_evidence=[ref(BASE/'version-selection.json','Publisher and PDF reconciliation'),ref(acq/'original.receipt.json','Original acquisition')])
    authored=dict(integrated_citation_key='exec21_ace_reference',kind='project_derivation',
        title='Bowtie extraction denominator, interaction, critical-path and intervention witnesses',
        author='Causal banking proposal project',year=2026,version_date='21 October 2026',
        source_identity='tools/ace_reference_20261021.py',local_copy=ref(ROOT/'tools/ace_reference_20261021.py','Independent exact references'),
        inspected_anchors=[ref(BASE/'exact-results.json','Exact finite-law calculations')],
        supported_claims=['Reported category counts each sum 80; hallucinations decrease 15 percentage points while unclear responses rise from 10 to 11.',
            'Uniform binary prompt/context equality gives zero first-order indices but total-order indices one.',
            'A missing bridge in a 100-edge chain leaves edge F1 198/199 and all nodes intact but breaks the end-to-end path.',
            'Topology A -> Y permits Y=A or Y=1-A; assumed loss 10 and cost 2 yield margins -12 and 8.'],
        limitations=exact.calculate()['limits'])
    write(BASE/'source-audit.json',dict(sources=[source,authored],cutoff='2026-10-07',limitations=LIMITS))
    critical=[
        'Graph-role extraction measures agreement with a reference representation, not intervention identification or mechanism truth.',
        'One expert constructs references with some implicit variables absent from text; distinguish text support from expert-added hypotheses.',
        'Semantic alignment at an empirically chosen .75 threshold needs frozen mappings and threshold sensitivity; role/direction errors cannot be erased by label similarity.',
        'Near-zero first-order context index is not an equivalence test. Independent-factor design distribution, total interactions and held-out domain differences matter.',
        'Selected configurations and repeated tests on three components do not establish generalization to new institutions or formats.',
        'Ten identical outputs do not identify quantization as the cause; seed propagation, caching, decoding, prompt constraints and precision need controlled checks.',
        'The prose says unclear responses reduced from 10 to 11; the printed counts instead increase by one. Preserve the table/counts.',
        'Narrative Table 5 averages require raw rating units, missingness and aggregation details; no bank-wide precision or agreement claim is inferred.',
        'The paragraph specifying Sobol Run 2 leaves whether temperature/top-p remain in the expanded design insufficiently explicit; recover actual design/code before reproducing counts.',
        'Article license does not qualify code, model weights, handbook data or dependency rights; named components are leads, not audited integrations.']
    omissions=[
        dict(item='Executable reproduction bundle',next_action='Obtain exact model/quantization hashes, prompts, generation flags, seed plumbing, preprocessing and dependency/code revisions.'),
        dict(item='Evaluation bundle',next_action='Recover reference diagrams, implicit-variable annotations, raw outputs, matching matrices, invalid JSON and expert-level ratings.'),
        dict(item='Sensitivity and selection',next_action='Recover categorical factor encoding, input distributions, full Sobol sample matrix and selected configurations; evaluate held-out documents.'),
        dict(item='Rights',next_action='Audit handbook, code, models and dependencies separately from article CC-BY notice before prototype reuse.'),
        dict(item='Causal and bank validation',next_action='Design public known-mechanism tasks with clocked roles, unsupported-edge labels and intervention tests; later obtain bank-owner evidence.'),
        dict(item='Citation chaining and visual review',next_action='Acquire primary originals for relevant cited methods; conduct fresh bounded visual review without importing their results from ACE.')]
    write(BASE/'omissions-register.json',dict(global_blocker=False,items=omissions,no_source_waivers=True))
    write(BASE/'plan-review.json',dict(status='pass',evidence=[ref(BASE/'plan.md','Reviewed original-recovery scope')],
        checks=['Authenticate original, reconcile publication date and preserve network failures.',
            'Inspect methods, denominators, adverse examples and limitations.',
            'Test the logic of interchangeability, graph fidelity and intervention meaning with exact examples.',
            'Update one census candidate, preserve all other records and integrate the substantive review.']))
    write(BASE/'primary-review.json',dict(status='pass_for_bounded_primary_review',reviewer=dict(name='Codex author/coordinator',kind='author'),
        findings=claims,source_critical_qualifications=critical,limitations=LIMITS,
        evidence=[ref(BASE/n,'Reviewed primary evidence') for n in ['source-audit.json','version-selection.json','exact-results.json','omissions-register.json']],
        native_execution=False,visual_acceptance=False,coverage_acceptance=False))
    old=read(PRIOR/'census-register.json');new=copy.deepcopy(old)
    item=next(x for x in new['items'] if x['id']=='LA01-candidate-26')
    assert item['disposition']=='open_original_not_inspected'
    item.update(prior_disposition=item['disposition'],disposition='inspected_primary_retained_with_limits',
        technical_source_review_open=False,source_key='exec21_ace',primary_source_record=source,
        later_primary_review=ref(BASE/'primary-review.json','Bounded source-critical review'),
        availability='Genuine 10-page publisher PDF recovered; sandbox DNS failures preserved.',
        effect_on_claims='Supports assisted bowtie extraction and evaluation design with narrow dataset limits; no SCM identification or executable adoption.',
        next_action='Integrate reviewed argument; recover executable/raw evaluation bundle and rights before prototype reuse.')
    assert len(new['items'])==117
    assert all(a==b for a,b in zip(old['items'],new['items']) if a['id']!='LA01-candidate-26')
    counts=Counter(x['disposition'] for x in new['items'])
    assert counts['inspected_primary_retained_with_limits']==56 and counts['open_original_not_inspected']==57
    new.update(counts=dict(counts),supersedes=ref(PRIOR/'census-register.json','Preserved 55/58 census'),
        changes=['Candidate26 reviewed; 116 other records unchanged.'],evidence=[ref(BASE/'primary-review.json','Primary inspection')],
        closure=False,interpretation='56/113 originals inspected; 57 unread; four separate crosscutting obligations remain.')
    write(BASE/'census-register.json',new)
    tasks=copy.deepcopy(read(PRIOR/'task-map.json'));assert len(tasks['task_families'])==14
    for task in tasks['task_families']:
        if 'LA01-candidate-26' in task['inherited_ids']:
            task['uninspected_candidate_ids'].remove('LA01-candidate-26')
            task['inspected_candidate_ids'].append('LA01-candidate-26');task['inspected_source_keys'].append('exec21_ace')
        task['coverage_acceptance']=False
    tasks.update(register=ref(BASE/'census-register.json','56/57 census'),supersedes=ref(PRIOR/'task-map.json','Preserved task map'))
    tasks.setdefault('primary_application_notes',{})['ace_bowtie']='Separate text-supported roles and expert-added hypotheses; preserve missing roles and known-mechanism evaluation.'
    write(BASE/'task-map.json',tasks)
    write(BASE/'reconciliation-review.json',dict(status='pass',changed_ids=['LA01-candidate-26'],
        unchanged_other_records=116,original_candidates=113,inspected=56,unread=57,task_families=14,coverage_acceptance=False,
        evidence=[ref(BASE/'census-register.json','Census conservation'),ref(BASE/'task-map.json','Task conservation')]))
    write(BASE/'conversion-contract.json',dict(status='proposed_not_implemented',integration_allowed=False,
        inputs=['Immutable source/page/span/table-cell identity and permissible document rights.',
            'Schema version, component/event time and typed cause/mechanism/barrier/consequence roles.',
            'Pinned pipeline/model/prompt/decoding parameters and full request cost budget.'],
        outputs=['Proposed roles/edges with source spans, inferred versus explicit status and conflicting evidence.',
            'Separate parse failure, unsupported role, unknown role, expert dispute and accepted extraction.',
            'No intervention query without separately specified action, outcome, SCM assumptions and identification.'],
        oracle=ref(BASE/'exact-results.json','Metric and intervention witnesses'),
        qualification=['Held-out public documents with explicit/implicit/adversarial roles and blinded adjudication.',
            'Frozen semantic matching, critical-path metrics and invalid-output denominator.',
            'Paired pipeline comparisons with equivalence margins and cost accounting.',
            'Known-mechanism public fixtures, correction-loop budgets and unresolved-result preservation.']))
    write(BASE/'review.json',dict(status='pass_for_bounded_primary_review',limitations=LIMITS,coverage_acceptance=False,
        evidence=[ref(BASE/'primary-review.json','Critical technical inspection'),ref(BASE/'reconciliation-review.json','Conservation'),
            ref(BASE/'conversion-contract.json','Proposed interface, not implementation')]))
    write(BASE/'inspection-progress.json',dict(finding='Candidate26 technically inspected; census56/57; extraction, sensitivity and intervention limits retained.',
        next_action='Integrate ACE argument and exact counterexamples into paired reader/sponsor; continue57 originals and independent software coverage.',
        evidence=[ref(BASE/n,'Bounded census evidence') for n in ['source-audit.json','review.json','census-register.json','task-map.json']]))
    verify_bindings(read(BASE/'source-audit.json'));verify_bindings(read(BASE/'review.json'))
    print(json.dumps(dict(inspected=56,unread=57,sources=2,coverage_acceptance=False)))


if __name__=='__main__':main()

"""Inspect authentic hypothesis-generation paper and reconcile one census entry."""
from collections import Counter
import copy, hashlib, json
from pathlib import Path
import hypothesis_reference_20261020 as exact
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-20/census-hypothesis-v1'
PRIOR=ROOT/'docs/program/execution/2026-10-20/census-expert-averaging-v1'
RAW=ROOT/'docs/literature/raw'
read=lambda p:json.loads(p.read_text())
LIMITS=['Bounded author primary-text review; no independent reproduction or complete literature coverage.',
 'Selected July2024 arXiv v3 contains the14-page journal article; current publisher supplement, raw ratings and code were not acquired or qualified.',
 'Earlier58-page v1 is preserved separately; its appendix is not silently substituted for the revised supplement.',
 'Model snapshots, code dependencies, graph conventions and full corpus rights remain unqualified.',
 'Reported novelty/utility ratings do not establish causal truth, calibrated effects or bank transfer.',
 'No live model, downloaded code or upstream experiments executed; no rendered acceptance.']

def main():
    assert not (BASE/'source-audit.json').exists()
    assert exact.calculate()==read(BASE/'exact-results.json')
    write(BASE/'plan-review.json',dict(status='pass',evidence=[ref(BASE/'plan.md','Reviewed scope')],
        checks=['Inspect genuine pre-cutoff revision and preserve failed publisher routes.',
          'Separate extracted claims, graph-link scores, novelty ratings and causal identification.',
          'Read adverse findings, comparator selection and numerical inconsistencies.',
          'Preserve116 other census records, all14 tasks and all prior manuscript sources.']))
    for key,suffix in [('arxiv_abs','html'),('arxiv_v1','pdf'),('arxiv_v3','pdf')]:
        path=RAW/f'exec20_census_hypothesis_{key}.{suffix}'
        receipt=read(RAW/f'exec20_census_hypothesis_{key}.receipt.json')
        assert receipt['status']=='saved' and receipt['sha256']==hashlib.sha256(path.read_bytes()).hexdigest()
    identity=RAW/'exec20_census_hypothesis_arxiv_abs.html'
    assert '16 Jul 2024 03:12:45 UTC' in identity.read_text()
    text=Path('/tmp/causal-hypothesis-v3.txt').read_text();pages=text.split(chr(12))
    assert len([p for p in pages if p.strip()])==14 and 'Song Tong' in pages[0]
    assert '10.1057/s41599-024-03407-5' in pages[0]
    title='Automating psychological hypothesis generation with AI: when large language models meet causal graph'
    filename_title=title.replace(':','')
    pdf=ROOT/'docs/papers'/f'{filename_title} Tong(2024).pdf'
    data=(RAW/'exec20_census_hypothesis_arxiv_v3.pdf').read_bytes()
    with pdf.open('xb') as stream:stream.write(data)
    (BASE/'original-v3.txt').write_text(text)
    anchors={1:'Title/authors/DOI and abstract; journal article11:896.',
      2:'Three-stage literature retrieval, causal-pair extraction and hypothesis generation.',
      3:'PMC open-access selection, journal-title filter,43,312 articles,35,797 from Frontiers in Psychology; PyPDF2 cleaning.',
      4:'Prompt explicitly extracts both causality and correlation;4000-token chunks, model filtering and expert feedback;197k concepts/235k links;156/238 causal agreement,31/238 nonexistent.',
      5:'node2vec similarity shortlist and neighbor Jaccard ranking; graph predictions generate testable hypotheses rather than tested mechanisms.',
      6:'130 hypotheses; random30 and expert-selected30;13 responding doctoral students produced41, sampled30; different selection processes.',
      7:'Claude2 generates50 and GPT4 selects30; three expert raters, randomized order; reviewer agreement varies; BERT/tSNE are semantic diagnostics.',
      8:'Rater-standardized averaged novelty scores; reported novelty advantage; no equivalence design.',
      9:'Table5 expert-selected mean comparison p=.085, median p=.550; usefulness F(3,116)=5.25 paired with p=.553; GPT4 ablation60 versus60.',
      10:'Ablation novelty advantage and usefulness p=.1937; semantic F(3,1652)=84.1611 with claimed R2=.8696; pair-distance dependence needs raw design.',
      12:'Sparse graph, synonymous concepts, extraction errors and restricted130-hypothesis evaluation acknowledged.',
      13:'Authors identify shift of expert work from generation to evaluation; data partly supplementary, additional data on request.',
      14:'Supplement pointer, author roles and CC-BY4 article license; it does not license every corpus/code dependency.'}
    inspected=[]
    for n,finding in anchors.items():
        p=BASE/f'hypothesis-page-{n}.txt';p.write_text(pages[n-1])
        inspected.append(dict(anchor=f'Physical PDF page {n}',finding=finding,extracted_text=ref(p,'Inspected primary text')))
    write(BASE/'version-selection.json',dict(candidate='LA01-candidate-42',selected='arXiv:2402.14424v3',
        selected_date='2024-07-16T03:12:45Z',publication_date='2024-07-09',cutoff='2026-10-07',
        title_page_title=title,filename_title=filename_title,selected_pages=14,
        earlier_version='v1,22February2024,58pages; title variation and older appendices retained separately',
        publisher_routes='PDF rejected non-PDF; HTML contains only browser challenge; not inspected article evidence',
        evidence=[ref(identity,'Version history only'),ref(RAW/'exec20_census_hypothesis_arxiv_v1.pdf','Preserved earlier original'),
          ref(RAW/'exec20_census_hypothesis_crossref.json','Publication identity only'),ref(pdf,'Selected authentic article')]))
    claims=['The paper combines GPT4 literature relation extraction, Neo4j graph storage, node2vec/Jaccard link ranking and generated psychological hypotheses.',
      'It reports43,312 articles,197k concepts and235k links; corpus selection and source concentration constrain coverage.',
      'The prompt distinguishes causal/correlational labels;156 of238 predicted causal pairs agree with human causal labels,31 are not recognized as relationships.',
      'The main comparison uses30 hypotheses per arm with different random, expert and model-selection pipelines; three experts rate novelty and utility.',
      'Reported novelty gains and nonsignificant utility contrasts concern these selected ideas and raters; the study does not experimentally validate proposed interventions.',
      'The revised article explicitly retains extraction error, sparse/synonymous concepts, limited evaluated hypotheses and expert-evaluation bottlenecks.']
    source=dict(integrated_citation_key='exec20_hypothesis_generation',kind='paper',title=title,filename_title=filename_title,
        first_author='Tong',author='Tong, Song and Mao, Kai and Huang, Zhen and Zhao, Yukun and Peng, Kaiping',year=2024,
        source_identity='arXiv:2402.14424v3; DOI10.1057/s41599-024-03407-5',version_date='16July2024 v3; journal publication9July2024',
        cutoff='2026-10-07',local_copy=ref(pdf,'Genuine selected original'),local_path=str(pdf.relative_to(ROOT)),
        sha256=hashlib.sha256(data).hexdigest(),inspected_anchors=inspected,supported_claims=claims,limitations=LIMITS,
        identity_evidence=[ref(BASE/'version-selection.json','Version reconciliation'),ref(RAW/'exec20_census_hypothesis_arxiv_v3.receipt.json','Acquisition receipt')])
    authored=dict(integrated_citation_key='exec20_hypothesis_reference',kind='project_derivation',
        title='Relation-label denominators, printed ANOVA identities and graph-similarity intervention witness',
        author='Causal banking proposal project',year=2026,source_identity='tools/hypothesis_reference_20261020.py',
        version_date='20October2026',local_copy=ref(ROOT/'tools/hypothesis_reference_20261020.py','Reproducible authored reference'),
        inspected_anchors=[ref(BASE/'exact-results.json','Exact fractions and independent tail calculation')],
        supported_claims=['156/238 causal-label agreement differs from207/238 relation-existence agreement.',
          'Under ordinary printed ANOVA, F5.25 at3,116 has upper tail about.001967, not.553.',
          'F84.1611 at3,1652 implies ordinary R2 about.132573, not.8696.',
          'Identical undirected neighborhoods give Jaccard1 while a structural intervention effect is0; assumed margin80 is invalid versus true-20.'],
        limitations=exact.calculate()['limitations'])
    write(BASE/'source-audit.json',dict(sources=[source,authored],cutoff='2026-10-07',scope='Primary article and authored checks'))
    critical=['Do not conflate relation-existence recognition with correct causal-label classification or interventional truth.',
      'The model also filters its extraction; expert feedback and familiar-paper evaluations do not establish blinded out-of-corpus calibration.',
      'Jaccard and embedding scores are not causal probabilities or identification proofs; direction, cycles, clocks and latent variables need separate treatment.',
      'Main comparator selection differs; failure to reject a human-versus-model contrast does not establish equivalence.',
      'Paper p=.553 beside F5.25 and R2=.8696 beside F84.1611 are incompatible under the ordinary printed ANOVA; preserve both and request raw analysis before reuse.',
      'Table5 human mean t4.36 differs from prose4.32; the prose significance claim for median expert/Claude conflicts with tablep=.550.',
      'Raw reviewer and shared-hypothesis dependence, exact model revisions, prompt budgets and graph threshold/neighbor conventions remain unresolved.',
      'Data availability is partial; public article license does not independently establish software/corpus reuse rights.']
    omissions=[('Revised supplement and raw ratings','Acquire the current publisher supplement and deidentified ratings/code; do not substitute older v1 appendices.'),
      ('Statistics reconciliation','Reconcile printed F/p/R2/t values and repeated-rater/shared-hypothesis dependence before inheriting inferential claims.'),
      ('Executable components','Inspect immutable graph/extraction code, exact models, thresholds, dependency licenses and corpus permissions.'),
      ('Public experiment','Separate held-out extraction, graph assumptions, blinded novelty/utility and known-mechanism intervention tests with full costs.'),
      ('Coverage','Continue59 unread originals, complementary searches and citation chaining; four crosscutting obligations stay open.'),
      ('Visual/final acceptance','Fresh rendered review and mandatory repair depth/coverage remain open.')]
    write(BASE/'omissions-register.json',dict(global_blocker=None,items=[dict(item=k,status='open',next_action=v) for k,v in omissions]))
    write(BASE/'primary-review.json',dict(status='pass_for_bounded_primary_review',reviewer=dict(name='Codex author/coordinator',kind='author'),
        findings=claims,source_critical_qualifications=critical,limitations=LIMITS,
        evidence=[ref(BASE/n,'Inspected evidence') for n in ['source-audit.json','version-selection.json','exact-results.json','omissions-register.json']],
        native_execution=False,visual_acceptance=False,coverage_acceptance=False))
    old=read(PRIOR/'census-register.json');new=copy.deepcopy(old)
    item=next(x for x in new['items'] if x['id']=='LA01-candidate-42');assert item['disposition']=='open_original_not_inspected'
    item.update(prior_disposition=item['disposition'],disposition='inspected_primary_retained_with_limits',technical_source_review_open=False,
        source_key='exec20_hypothesis_generation',primary_source_record=source,later_primary_review=ref(BASE/'primary-review.json','Primary review'),
        availability='Authentic14-page July2024 v3 acquired;58-page v1 and failed publisher routes preserved.',
        effect_on_claims='Supports a hypothesis-generation proposal with explicit limits; no causal truth or bank qualification.',
        next_action='Integrate critical argument; acquire current supplement/raw analysis and inspect code before executable reuse.')
    assert len(new['items'])==117 and all(a==b for a,b in zip(old['items'],new['items']) if a['id']!='LA01-candidate-42')
    counts=Counter(x['disposition'] for x in new['items']);assert counts['inspected_primary_retained_with_limits']==54 and counts['open_original_not_inspected']==59
    new.update(counts=dict(counts),supersedes=ref(PRIOR/'census-register.json','Preserved53/60 census'),
        changes=['Candidate42 reviewed;116 other records unchanged.'],evidence=[ref(BASE/'primary-review.json','Primary review')],
        closure=False,interpretation='54/113 originals inspected;59 unread. Four crosscutting obligations remain separate.')
    write(BASE/'census-register.json',new)
    tasks=copy.deepcopy(read(PRIOR/'task-map.json'));assert len(tasks['task_families'])==14
    for task in tasks['task_families']:
        if 'LA01-candidate-42' in task['inherited_ids']:
            task['uninspected_candidate_ids'].remove('LA01-candidate-42');task['inspected_candidate_ids'].append('LA01-candidate-42')
            task['inspected_source_keys'].append('exec20_hypothesis_generation')
        task['coverage_acceptance']=False
    tasks.update(register=ref(BASE/'census-register.json','Current54/59 census'),supersedes=ref(PRIOR/'task-map.json','Preserved task map'))
    tasks.setdefault('primary_application_notes',{}).update(business_translation='Use claim-level provenance and operational targets; proposed graph links stay hypotheses.',active_experiments='Validate generated hypotheses with held-out mechanisms before expensive bank intervention evidence.')
    write(BASE/'task-map.json',tasks)
    write(BASE/'reconciliation-review.json',dict(status='pass',changed_ids=['LA01-candidate-42'],unchanged_other_records=116,
        original_candidates=113,inspected=54,unread=59,task_families=14,coverage_acceptance=False,
        evidence=[ref(BASE/'census-register.json','Census conservation'),ref(BASE/'task-map.json','Preserved task coverage')]))
    write(BASE/'review.json',dict(status='pass_for_bounded_primary_review',limitations=LIMITS,coverage_acceptance=False,
        evidence=[ref(BASE/'primary-review.json','Critical inspection'),ref(BASE/'reconciliation-review.json','Census conservation')]))
    write(BASE/'inspection-progress.json',dict(finding='Candidate42 authentic July2024 article inspected; novelty, causal-label and printed-statistic limits retained; census54/59.',
        next_action='Integrate the hypothesis-generation argument and public evaluation design, publish paired reader/sponsor, then continue candidate45 or another accessible original.',
        evidence=[ref(BASE/n,'Completed bounded review') for n in ['source-audit.json','review.json','census-register.json','task-map.json']]))
    verify_bindings(read(BASE/'source-audit.json'));verify_bindings(read(BASE/'review.json'))
    print(json.dumps(dict(inspected=54,unread=59,sources=2,coverage_acceptance=False)))

if __name__=='__main__':main()


#!/usr/bin/env python3
"""Preserve two primary inspections, exact reference and a census successor."""
import copy
from collections import Counter
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import agent_reasoning_reference_20261018 as exact
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'docs/program/execution/2026-10-18/census-biomedical-reasoning-v1'
PRIOR = ROOT/'docs/program/execution/2026-10-18/census-frameworks-v1'
RAW = ROOT/'docs/literature/raw'


def read(p):
    return json.loads(p.read_text())


def main():
    verify_bindings(read(BASE/'plan-review.json'))
    metadata = RAW/'exec18_biomedical_reasoning_identity.xml'
    ns={'a':'http://www.w3.org/2005/Atom'}
    entries={e.findtext('a:id',namespaces=ns).rsplit('/',1)[-1]:e
        for e in ET.parse(metadata).getroot().findall('a:entry',ns)}
    definitions=[dict(name='biomedical', id='2505.16982v1', candidate='LA01-candidate-46',
        key='exec18_reasoning_biomedical',
        title='Beyond Correlation: Towards Causal Large Language Model Agents in Biomedicine',
        first='Bazgir', author='Bazgir, Adib and Lafmajani, Amir Habibdoust and Zhang, Yuwen',
        date='22 May 2025', pages=6, anchors={
            1:'Actual title, three authors,22May2025v1 stamp; explicitly a position paper and research agenda.',
            2:'Sections2.1-2.2: controlled external actions, human oversight, causal-task and whole-workflow evaluation, stochasticity and model-update concerns.',
            3:'Section2.3: proposed formal-tool and heterogeneous-data integration; constituent-system claims are secondary reports, not locally verified components.',
            4:'Sections3.2-4: personalized and longitudinal applications are motivations; integration, data and standardized evaluation remain research directions.',
            5:'Conclusion explicitly calls for integration, evaluation and validation; references1-12 establish citation-chain leads only.',
            6:'References13-22; compare MATMCD mention on physical3 against cited reference7 (Trialscope) and reference17 (multimodal agents).'},
        claims=['The authors propose a causal-agent architecture combining language models, structured knowledge, formal tools and multimodal data.',
            'The agenda treats controlled actions, verification, causal-task evaluation, reproducibility and data integration as open design obligations.',
            'This selected paper reports no new matched causal-agent experiment or quantified personalized-treatment qualification.'],
        limits=['Primary evidence for the authors own agenda; constituent package and performance claims require the original technical sources.',
            'Physical3 attaches reference7 to a MATMCD discussion although reference7 on physical5 is Trialscope and reference17 on physical6 is the multimodal-agent paper. Do not silently propagate this citation chain.',
            'No package, benchmark, clinical use or bank integration was executed or validated in this review.']),
        dict(name='neuron', id='2506.14239v1', candidate='LA01-candidate-115',
        key='exec18_reasoning_neuron',
        title='Causes in neuron diagrams, and testing causal reasoning in Large Language Models. A glimpse of the future of philosophy?',
        first='Vervoort', author='Vervoort, Louis and Nikolaev, Vitaly', date='17 June 2025', pages=35, anchors={
            1:'Title and two authors; manuscript dateline30April2025 differs from17June2025 arXiv submission, both preserved.',
            4:'Purpose is illustrative feasibility, explicitly not large-scale statistical experiments; tests dated2023/2024 and February2025.',
            6:'Separate event-occurrence and Q-CAUSE questions; diagrams supplied rather than learned from observational data.',
            7:'Stimulation, inhibition, time order and early preemption; special double-border activation rule.',
            8:'Selected25-diagram ensemble helped develop DEF-1; tables from a single no-feedback run; no completeness claim.',
            9:'Labels combine prior intuitions, author judgment and DEF-1; some causes omitted. In diagram1 recorded answer attributes backup blocking to A although prompt specifies C.',
            10:'Continuation labels diagram1 CORRECT despite preceding explanatory mismatch; explicit incorrect diagram5 response is retained.',
            11:'Diagram17 transcription asks whether G occurs but then asks for causes of E; target inconsistency needs adjudication before a strict reusable benchmark.',
            12:'Prose reports13/25 fully correct versus6/9 in selected subset; two partially correct separately. These are source-reported counts, not a local rerun.',
            13:'Newer-model comparison changes prompts to short answers and initial causes; author admits no compelling explanation for one reversal.',
            14:'DEF-1 proposed with counterfactual, temporal/path and maximal off-path blocking conditions; footnote11 acknowledges possible ad-hoc character and future work.',
            15:'Forward propagation and non-bifurcating/off-node rules; not a generic population effect estimand.',
            16:'Shortest-path simplification and retention of factual off-path blocking explicitly do not fully implement ordinary node removal.',
            18:'Definition excludes non-classic diagrams; even a classic ambiguous case may require extension; relation to other causal theories remains open.',
            19:'Complexity failures and black-box limits; no large-scale human comparison.',
            20:'Authors explicitly decline to treat small-scale counts as general causal competence; proposed counterfactual and paraphrase extensions.',
            21:'Limited nine-diagram paraphrase checks and text changes do not certify contamination control.',
            22:'Systematic programmable benchmark is a future proposal; broader generality still to establish.'},
        claims=['The authors propose a textual neuron-diagram test separating event occurrence from causal attribution and a scoped DEF-1 labeling rule.',
            'DEF-1 retains factual off-path blocking in selected bifurcating cases, and the authors state limits and an ambiguous extension case.',
            'Illustrative source-reported small experiments and selected diagrams do not establish general or current model performance.',
            'Inspected transcription, explanatory-label and target inconsistencies need explicit adjudication before adopting a strict causal-contract benchmark.'],
        limits=['The definition and examples are the authors proposed philosophical criterion, not an accepted universal identification theorem.',
            'No diagrams, underlining or complete table scores were visually reinspected under the exhausted image allowance. Numeric claims are limited to explicit prose.',
            'The reference set contributed to definition development; a fresh held-out graph-family evaluation is needed for generalization claims.',
            'No model was queried; no current ranking, calibration, uncertainty interval or bank benefit is inferred.'])]
    sources=[]
    for d in definitions:
        raw=RAW/('exec18_census_'+d['name']+'_v1.pdf')
        receipt=read(raw.with_suffix('.receipt.json'))
        assert receipt['status']=='saved' and receipt['sha256']==ref(raw,'Authentic original')['sha256']
        entry=entries[d['id']]
        assert ' '.join(entry.findtext('a:title',namespaces=ns).split())==d['title']
        assert entry.findtext('a:published',namespaces=ns)[:10] < '2026-10-08'
        target=ROOT/'docs/papers'/(d['title']+' '+d['first']+'(2025).pdf')
        assert not target.exists();target.write_bytes(raw.read_bytes())
        pages=(BASE/(d['name']+'-selected.txt')).read_text().split('\f')
        assert sum(bool(p.strip()) for p in pages)==d['pages']
        anchors=[]
        for page,finding in d['anchors'].items():
            path=BASE/(d['name']+'-page-'+str(page)+'.txt')
            assert not path.exists();path.write_text(pages[page-1])
            anchors.append(dict(anchor='Physical PDF page'+str(page),finding=finding,
                extracted_text=ref(path,'Inspected technical text; no new visual acceptance')))
        sources.append(dict(integrated_citation_key=d['key'],kind='paper',title=d['title'],
            filename_title=d['title'],first_author=d['first'],author=d['author'],year=2025,
            source_identity='arXiv:'+d['id'],version_date='Selected v1 submitted'+d['date']+'; retrieved18October2026',
            cutoff='2026-10-07',local_copy=ref(target,'Authentic selected original'),
            local_path=str(target.relative_to(ROOT)),sha256=ref(target,'Original')['sha256'],
            inspected_anchors=anchors,supported_claims=d['claims'],limitations=d['limits'],
            identity_evidence=[ref(raw.with_suffix('.receipt.json'),'Actual acquisition'),
                ref(metadata,'Submission/version identity only'),
                ref(RAW/('exec18_census_'+d['name']+'_history.html'),'Preserved archive history; selected historical version')]))
    write(BASE/'exact-results.json',exact.calculate())
    sources.append(dict(integrated_citation_key='exec18_reasoning_reference',kind='project_derivation',
        title='Exact servicing routes separating attribution, intervention and value',author='Causal banking proposal project',year=2026,
        source_identity='Authored deterministic structural equations and rational enumeration',version_date='18October2026',
        local_copy=ref(ROOT/'tools/agent_reasoning_reference_20261018.py','Exact calculate function'),
        inspected_anchors=[ref(BASE/'exact-results.json','All four natural route states, compound removal and exact threshold')],
        supported_claims=['At available backup, removing priority preserves success while removing both routes eliminates it.',
            'Assumed success and route costs yield160 versus190USD net, and priority advantage160-190p with threshold16/19.'],
        limitations=['Stipulated mechanics and costs; not DEF-1 implementation, empirical identification, a statistical interval, live model performance or bank ROI.']))
    write(BASE/'source-audit.json',dict(sources=sources,cutoff='2026-10-07',
        scope='Two selected primary originals and one authored exact reference; no constituent-source or census completeness claim'))
    write(BASE/'primary-review.json',dict(status='pass',reviewer=dict(name='Codex author/coordinator',kind='author'),
        evidence=[ref(BASE/'source-audit.json','Source identities, inspected anchors and supported scope'),
            ref(BASE/'exact-results.json','Exact authored reference'),ref(Path(__file__),'Preserving review and census checks')],
        findings=[dict(candidate=d['candidate'],claims=d['claims'],limitations=d['limits']) for d in definitions],
        repairs_required_before_reuse=['Resolve biomedical citation-chain mismatch against the constituent original.',
            'Adjudicate neuron transcript/target errors and specify definition-specific labels before adopting a benchmark.',
            'Use fresh generated families and a frozen rubric for future model evaluation; paraphrases alone do not prove novelty.'],
        visual_acceptance=False,independent_acceptance=False,coverage_acceptance=False))
    old=read(PRIOR/'census-register.json');new=copy.deepcopy(old)
    changed={d['candidate']:d for d in definitions}; by_key={s['integrated_citation_key']:s for s in sources}
    for item in new['items']:
        if item['id'] not in changed:continue
        d=changed[item['id']]; assert item['disposition']=='open_original_not_inspected'
        item.update(prior_disposition=item['disposition'],disposition='inspected_primary_retained_with_limits',
            technical_source_review_open=False,source_key=d['key'],primary_source_record=by_key[d['key']],
            later_primary_review=ref(BASE/'primary-review.json','Inspected selected original and explicit adverse findings'),
            availability='Authentic v1 acquired and technically inspected; sandbox DNS failures preserved.',
            effect_on_claims='Supports only bounded agenda/test design and source-critical findings; no causal identification, model or clinical qualification.',
            next_action='Integrate bounded discussion; inspect constituent originals and adjudicate benchmark defects before executable adoption.')
    assert all(a==b for a,b in zip(old['items'],new['items']) if a['id'] not in changed)
    counts=Counter(i['disposition'] for i in new['items']);assert counts['open_original_not_inspected']==69 and counts['inspected_primary_retained_with_limits']==44
    new.update(counts=dict(counts),supersedes=ref(PRIOR/'census-register.json','Preserved42/71 original census'),
        changes=['Only candidate46 and115 receive selected-original primary inspections.'],
        evidence=[ref(BASE/'primary-review.json','Source-critical review'),ref(BASE/'source-audit.json','Authentic sources')],
        closure=False,interpretation='44/113 original candidates inspected;69 unread. Four crosscutting records and three separate citation-chain leads keep separate denominators.')
    write(BASE/'census-register.json',new)
    taskmap=copy.deepcopy(read(PRIOR/'task-map.json'))
    assert len(taskmap['task_families'])==14
    for task in taskmap['task_families']:
        for identifier,d in changed.items():
            if identifier not in task['inherited_ids']:continue
            assert identifier in task['uninspected_candidate_ids']
            task['uninspected_candidate_ids'].remove(identifier);task['inspected_candidate_ids'].append(identifier);task['inspected_source_keys'].append(d['key'])
        task['coverage_acceptance']=False
    taskmap.update(register=ref(BASE/'census-register.json','Current44/69 census'),supersedes=ref(PRIOR/'task-map.json','Preserved14-task mapping'))
    write(BASE/'task-map.json',taskmap)
    write(BASE/'reconciliation-review.json',dict(status='pass',changed_ids=sorted(changed),unchanged_other_records=True,
        original_candidates=113,inspected=44,unread=69,task_families=14,coverage_acceptance=False,
        evidence=[ref(BASE/'census-register.json','Preserving successor'),ref(BASE/'task-map.json','Reconciled mapping')]))
    write(BASE/'inspection-progress.json',dict(finding='Two selected originals inspected;44/113 inspected and69unread. Source-critical limitations and exact authored servicing reference recorded.',
        next_action='Integrate the bounded agenda/test critique and exact servicing distinction into a preserving monograph and sponsor successor; retain L1/L6 and final coverage obligations.',
        evidence=[ref(BASE/n,'Inspected evidence') for n in ['primary-review.json','source-audit.json','census-register.json','task-map.json','reconciliation-review.json']]))
    verify_bindings(read(BASE/'source-audit.json'));verify_bindings(read(BASE/'primary-review.json'))
    print(json.dumps(dict(inspected=44,unread=69,source_records=3,coverage_acceptance=False)))


if __name__=='__main__':
    main()

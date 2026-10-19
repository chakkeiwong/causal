#!/usr/bin/env python3
"""Preserve two original-paper reviews and reconcile the existing census."""
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path

import population_attribution_reference_20261020 as exact
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'docs/program/execution/2026-10-20/census-population-attribution-v1'
PRIOR = ROOT/'docs/program/execution/2026-10-19/census-hidden-reasoning-v1'
RAW = ROOT/'docs/literature/raw'
read = lambda p: json.loads(p.read_text())
LIMITS = ['Bounded primary-text inspection, not independent replication or complete citation chaining.',
          'No model weights, code release, native runtime, or statistical calibration verified.',
          'No rendered visual acceptance; inherited image allowance exhausted.',
          'The proposal remains incomplete; authentic bank validation is a later conditional gate.']


def main():
    assert not (BASE/'source-audit.json').exists()
    specifications = [
        dict(candidate='LA01-candidate-193', tag='population193', version='v1', arxiv='2310.17888',
             title='Large Language Models as Subpopulation Representative Models: A Review',
             first='Simmons', author='Simmons, Gabriel and Hare, Christopher', year=2023,
             date='27 October 2023', pages=53, key='exec20_population', anchors={
                 1: 'Title/authors and scope as a survey of subpopulation representative models.',
                 8: 'Figure 1 describes prompting/fine-tuning, data grounding and deployment; opinion alignment compares response distributions.',
                 16: 'Distinguishes apparent and actual model sensitivity and model-dependent representation distances.',
                 17: 'Missing-data prediction, retrodiction and zero-shot settings differ in access to target-relevant observations.',
                 20: 'Evaluation distinguishes direct ground-truth comparison, human annotation and macroscopic checks.',
                 21: 'Five guiding criteria: fidelity, necessity, robustness, sensitivity and fairness.',
                 22: 'Indistinguishability is one fidelity criterion; out-of-sample predictive performance is a different check.',
                 23: 'Consistency, pattern correspondence and within-subpopulation diversity are distinct; reports of earlier studies remain secondary here.',
                 28: 'Warns against replacing a difficult substantive evaluation with a convenient predictive proxy.'},
             claims=['The review organizes SRM design by population, behavior elicitation, grounding data and deployment.',
                     'It distinguishes ground-truth, human and macroscopic evaluation and five guiding evaluation criteria.',
                     'It distinguishes response consistency, pattern correspondence and diversity; apparent and actual model sensitivity may differ.',
                     'Its survey is a design framework, not a bank-response replication or an intervention-identification guarantee.']),
        dict(candidate='LA01-candidate-154', tag='attribution154', version='v3', arxiv='2401.00139',
             title='Enhancing Causal Reasoning in Large Language Models: A Causal Attribution Model for Precision Fine-Tuning',
             first='Cai', author='Cai, Hengrui and Liu, Shengjie and Song, Rui', year=2026,
             date='21 May 2026', pages=51, key='exec20_attribution', anchors={
                 1: 'Title/authors and v3 21 May 2026 identifier; v1 had a different title and did not support the current fine-tuning claim.',
                 7: 'Assumed model distinguishes context, name-associated knowledge, numerical data and controlled model/training conditions.',
                 8: 'Definitions 2.1/2.2 compare prompt-input conditions for correctness probabilities.',
                 9: 'Definitions 2.3/2.4 and the attribution-difference equality; equality is algebraic and does not verify intervention purity.',
                 11: 'Nine benchmark datasets, each with fifteen column-order permutations, give 135 task instances.',
                 12: 'Suggestive prompt wording, column-order randomization and arbitrary replacement names operationalize input manipulations.',
                 13: 'Omitting numerical data retains variable names; removing names does not erase learned model parameters.',
                 14: 'No-input guessing baseline; selected linear non-Gaussian regime motivates pairwise tasks. A guessing score is not a universal lower bound.',
                 16: 'Reverse-task text says numerical data stay intact while adjacency/order is reversed; this is not by itself a sampled intervention law.',
                 17: 'Algorithm 2 uses 135 instances; TDR denominator is the number of true causal pairs.',
                 18: 'TDR, SHD, false discovery rate and F1 are separate measures; reverse and reverse-raw labels use different target graphs.',
                 24: 'Fine-tuning instruction contains variable definitions and algorithm outputs; prose uses residual correlation. Numerical-independence semantics require native inspection.',
                 25: '300 pairs/1200 training samples, 106 pairs/424 testing samples; Mistral-7B-v0.2 LoRA; Table 4 overall 0.90, undefined case 0.58 versus GPT-4 turbo 0.66.',
                 27: 'Table 5 has equal selected scores, with Mixtral wording while main training text says Mistral; general no-forgetting cannot be inferred from three tasks.',
                 28: 'Authors acknowledge benchmark generalization, finite-sample and missing-data limits; uncertainty-based knowledge weighting is future work.'},
             claims=['The four attribution quantities describe differences between controlled prompt-input conditions on chosen benchmarks.',
                     'Nine datasets and repeated column permutations distinguish prompt variation from independent domain replication.',
                     'Fine-tuning uses numerical discovery outputs and names; reported overall accuracy is 0.90, with weaker performance on the undefined scenario.',
                     'Residual correlation wording, reverse-task semantics, native artifact identity and benchmark transfer require separate qualification.',
                     'The proposed uncertainty-weighted combination is a future direction, not calibrated evidence delivered by the reported model.'])]
    sources=[]; identities=[]
    for s in specifications:
        raw=RAW/f"exec20_{s['tag']}_{s['version']}.pdf"; receipt=RAW/f"exec20_{s['tag']}_{s['version']}.receipt.json"
        r=read(receipt); data=raw.read_bytes()
        assert data.startswith(b'%PDF-') and r['status']=='saved' and r['sha256']==hashlib.sha256(data).hexdigest()
        text=BASE/f"{s['tag']}-{s['version']}.txt"; pages=text.read_text().split(chr(12))
        assert sum(bool(p.strip()) for p in pages)==s['pages'] and s['first'] in pages[0]
        pdf=ROOT/'docs/papers'/f"{s['title']} {s['first']}({s['year']}).pdf"
        with pdf.open('xb') as stream: stream.write(data)
        anchors=[]
        for page,finding in s['anchors'].items():
            path=BASE/f"{s['tag']}-page-{page}.txt"
            with path.open('x') as stream: stream.write(pages[page-1])
            anchors.append(dict(anchor=f'Physical PDF page {page}',finding=finding,
                                extracted_text=ref(path,'Inspected technical text; no visual acceptance')))
        source=dict(integrated_citation_key=s['key'],kind='paper',title=s['title'],filename_title=s['title'],
                    first_author=s['first'],author=s['author'],year=s['year'],source_identity=f"arXiv:{s['arxiv']}{s['version']}",
                    version_date=s['date']+'; '+s['version'],cutoff='2026-10-07',local_copy=ref(pdf,'Genuine selected original'),
                    local_path=str(pdf.relative_to(ROOT)),sha256=r['sha256'],inspected_anchors=anchors,
                    supported_claims=s['claims'],limitations=LIMITS,
                    identity_evidence=[ref(receipt,'Genuine versioned PDF acquisition'),ref(RAW/f"exec20_{s['tag']}_identity.html",'Identity and submission history only')])
        sources.append(source); identities.append(dict(candidate=s['candidate'],source=source['local_copy'],identity=source['source_identity'],date=s['date'],pages=s['pages']))
    write(BASE/'paper-identities.json',dict(originals=identities,version_selection=ref(BASE/'version-selection.json','Preserved v1-to-v3 distinction')))
    write(BASE/'exact-results.json',exact.calculate())
    sources.append(dict(integrated_citation_key='exec20_population_attribution_reference',kind='project_derivation',
        title='Exact population-simulation, factorial-attribution and residual-independence witnesses',
        author='Causal banking proposal project',year=2026,source_identity='tools/population_attribution_reference_20261020.py',
        version_date='20 October 2026',local_copy=ref(ROOT/'tools/population_attribution_reference_20261020.py','Exact rational calculations'),
        inspected_anchors=[ref(BASE/'exact-results.json','All rational witness values')],
        supported_claims=['Simulation MSE retains squared population bias as decoder draws increase; assumed margins are USD 5 and USD -5.',
                          'Factorial interaction is 1/5; conditional attribution sum 4/5 exceeds total gain 3/5.',
                          'Forward/reverse linear residual covariances both vanish, but reverse squared covariance is -16/25.',
                          'Nine perfectly correlated sets of fifteen repeats contain nine independent units, under the explicitly hypothetical law.'],
        limitations=exact.calculate()['limitations']))
    write(BASE/'source-audit.json',dict(sources=sources,cutoff='2026-10-07',scope='Two primary originals plus exact authored witnesses'))
    omissions=[
        ('Native artifact', 'Resolve code, weight, prompt, license and environment identity; inspect residual independence tests and reverse-task transformations before adoption.'),
        ('Population validity', 'Use frozen public response data for descriptive fidelity; preserve population, time, subgroup variance and selection limits. Simulated answers are not real customer outcomes.'),
        ('Independent evaluation', 'Hold out generating mechanisms, domains and causal pairs; group prompt variants and report refusals, uncertainty and full prediction denominators.'),
        ('Future uncertainty weighting', 'Declare a probabilistic calibration target and test a frozen weighting rule; the paper proposes this direction without establishing it.'),
        ('Census search', 'Continue 62 unread original candidates, complementary longitudinal/off-policy and negative-result searches, and citation chaining.'),
        ('Rendered and bank acceptance', 'Fresh visual review and later independent/bank acceptance remain distinct from author text/source checks.')]
    write(BASE/'omissions-register.json',dict(global_blocker=None,items=[dict(item=k,status='open',next_action=v) for k,v in omissions]))
    write(BASE/'primary-review.json',dict(status='pass_for_bounded_primary_review',reviewer=dict(name='Codex author/coordinator',kind='author'),
        findings=[c for s in specifications for c in s['claims']],
        evidence=[ref(BASE/n,'Reviewed source and authored evidence') for n in ['source-audit.json','paper-identities.json','exact-results.json','omissions-register.json']],
        limitations=LIMITS,visual_acceptance=False,coverage_acceptance=False,native_execution=False))
    old=read(PRIOR/'census-register.json'); new=copy.deepcopy(old)
    by_id={s['candidate']:s for s in specifications}
    for item in new['items']:
        if item['id'] not in by_id: continue
        spec=by_id[item['id']]; source=next(s for s in sources if s['integrated_citation_key']==spec['key'])
        assert item['disposition']=='open_original_not_inspected'
        item.update(prior_disposition=item['disposition'],disposition='inspected_primary_retained_with_limits',technical_source_review_open=False,
            source_key=spec['key'],primary_source_record=source,later_primary_review=ref(BASE/'primary-review.json','Bounded selected-original review'),
            availability='Genuine versioned original acquired; selected technical anchors inspected.',
            effect_on_claims='Scoped proposal design evidence, with native artifacts, calibration and banking transfer still open.',
            next_action='Integrate the connected proposal argument; execute public prototype qualification only under its separate frozen design.')
    assert len(new['items'])==117
    assert all(a==b for a,b in zip(old['items'],new['items']) if a['id'] not in by_id)
    counts=Counter(i['disposition'] for i in new['items'])
    assert counts['inspected_primary_retained_with_limits']==51 and counts['open_original_not_inspected']==62
    new.update(counts=dict(counts),supersedes=ref(PRIOR/'census-register.json','Preserved 49/64 census'),
        changes=['Candidates 193 and 154 receive bounded primary-original reviews.'],
        evidence=[ref(BASE/'primary-review.json','Two original reviews')],closure=False,
        interpretation='51/113 originals inspected; 62 unread. Four crosscutting obligations retain separate denominators.')
    write(BASE/'census-register.json',new)
    taskmap=copy.deepcopy(read(PRIOR/'task-map.json')); assert len(taskmap['task_families'])==14
    for task in taskmap['task_families']:
        for identifier,spec in by_id.items():
            if identifier in task['inherited_ids']:
                task['uninspected_candidate_ids'].remove(identifier)
                task['inspected_candidate_ids'].append(identifier); task['inspected_source_keys'].append(spec['key'])
        task['coverage_acceptance']=False
    taskmap.update(register=ref(BASE/'census-register.json','Current 51/62 census'),supersedes=ref(PRIOR/'task-map.json','Preserved fourteen-task mapping'),
        primary_application_notes={'business_translation':'Population, response construct and proposed intervention must be distinct.',
                                   'iid_discovery':'Preserve assumptions of numerical discovery; names are prompts, not identified effects.',
                                   'agent_architecture':'Use explicit input-ablation and abstention contracts.',
                                   'evaluation_cost':'Group prompt repetitions; benchmark accuracy and native qualification differ.'})
    write(BASE/'task-map.json',taskmap)
    write(BASE/'reconciliation-review.json',dict(status='pass',changed_ids=sorted(by_id),unchanged_other_records=True,
        original_candidates=113,inspected=51,unread=62,task_families=14,coverage_acceptance=False,
        evidence=[ref(BASE/'census-register.json','Preserving census successor'),ref(BASE/'task-map.json','Task mapping successor')]))
    write(BASE/'review.json',dict(status='pass_for_bounded_primary_review',limitations=LIMITS,coverage_acceptance=False,
        evidence=[ref(BASE/'primary-review.json','Source-critical review'),ref(BASE/'reconciliation-review.json','Candidate conservation')]))
    write(BASE/'inspection-progress.json',dict(finding='Two genuine originals inspected; selected Cai v3 identity preserved. Census 51/113 inspected and 62 unread.',
        next_action='Integrate population-simulation and attribution limits, compile preserving reader and sponsor, then continue eligible work.',
        evidence=[ref(BASE/n,'Inspected evidence') for n in ['source-audit.json','review.json','census-register.json','task-map.json']]))
    verify_bindings(read(BASE/'source-audit.json')); verify_bindings(read(BASE/'review.json'))
    print(json.dumps(dict(inspected=51,unread=62,sources=3,coverage_acceptance=False)))


if __name__ == '__main__':
    main()

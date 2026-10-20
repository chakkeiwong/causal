#!/usr/bin/env python3
"""Inspect a genuine pre-cutoff LLM validity original and preserve its census successor."""
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path

import validity_measurement_reference_20261020 as exact
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-20/census-validity-v1'
PRIOR=ROOT/'docs/program/execution/2026-10-20/census-population-attribution-v1'
RAW=ROOT/'docs/literature/raw'
read=lambda p:json.loads(p.read_text())
LIMITS=['Bounded methodological primary-text review, not independent replication or a complete census.',
        'No original empirical study is reported in this paper; no model, package or supplementary code executed here.',
        'Secondary numerical results and broad statistical equivalence claims are not inherited without their originals and assumptions.',
        'Rendered visual acceptance remains pending; inherited image allowance exhausted.',
        'Bank transfer, independently adjudicated measurement and future prototype qualification remain separate obligations.']


def main():
    assert not (BASE/'source-audit.json').exists()
    write(BASE/'plan-review.json',dict(status='pass',scope='Candidate25: methodological source, measurement model and public evaluation design',
        evidence=[ref(BASE/'plan.md','Saved continuation plan')],
        checks=['Select the authentic August2026 v2, preserving v1 and version history; both predate client cutoff.',
                'Read the primary tutorial; do not borrow cited empirical estimates as inspected results.',
                'Separate measurement invariance, causal assignment and actual sampling independence.',
                'Qualify source shorthand about aggregation, cluster labels and safe cluster counts.',
                'Verify exact arithmetic and conservation of all116 other census records.',
                'Integrate in the existing evaluation chapter, preserving previous citations and content; no duplicate depth credit.']))
    identity=RAW/'exec20_validity_abs.html'
    html=identity.read_text()
    assert '15 Aug 2026 22:44:29 UTC' in html and '6 Jul 2025 18:06:12 UTC' in html
    for tag in ['abs','v1','v2']:
        suffix='html' if tag=='abs' else 'pdf'
        path=RAW/f'exec20_validity_{tag}.{suffix}';receipt=read(RAW/f'exec20_validity_{tag}.receipt.json')
        assert receipt['status']=='saved' and receipt['sha256']==hashlib.sha256(path.read_bytes()).hexdigest()
    raw=RAW/'exec20_validity_v2.pdf';data=raw.read_bytes()
    assert data.startswith(b'%PDF-')
    pages=(BASE/'original-v2.txt').read_text().split(chr(12))
    assert sum(bool(p.strip()) for p in pages)==37 and 'Zhicheng Lin' in pages[0]
    assert '58, Article 216' in pages[0] and '10.3758/s13428-026-03073-2' in pages[0]
    title='A validity-guided workflow for robust large language model research in psychology'
    pdf=ROOT/'docs/papers'/f'{title} Lin(2026).pdf'
    with pdf.open('xb') as stream:stream.write(data)
    anchors={
        1:'Title, sole author, published2026 identity and tutorial objective.',
        5:'Workflow table distinguishes design, execution and analysis requirements.',
        6:'Table2 differentiates tools, evaluation targets, human simulators and cognitive models; invariance depends on claim.',
        7:'Stages1-2: define the operational claim, develop on one subset and assess a finalized instrument on held-out material.',
        16:'Stage3: distinguish manipulation/outcome semantics, wording/format/context confounds and version/session controls.',
        18:'Staged preregistration, multiplicity, stopping rules and environment documentation.',
        19:'Exact prompts, raw outputs, metadata and code; observation, experimental and analysis units are distinguished.',
        20:'Figure2 proposes grouped or paired analysis and whole-cluster sensitivity analysis, conditional on actual design.',
        21:'Aggregation and multilevel alternatives; shorthand about eliminating correlation and numeric cluster rules requires qualification.',
        22:'Few-cluster caution and paired item differences; cited empirical magnitudes are secondary, not re-established here.',
        23:'Stage6: operational reporting, version/model/population limits and distinct behavioral versus competence claims.',
        27:'Methodological half-life and declarations: no original empirical analysis code; supplementary code is illustrative.'}
    inspected=[]
    for page,finding in anchors.items():
        path=BASE/f'validity-page-{page}.txt'
        with path.open('x') as stream:stream.write(pages[page-1])
        inspected.append(dict(anchor=f'Physical PDF page {page}',finding=finding,
            extracted_text=ref(path,'Inspected primary technical text; no rendered visual acceptance')))
    write(BASE/'version-selection.json',dict(candidate='LA01-candidate-25',selected='arXiv:2507.04491v2',
        selected_date='2026-08-15T22:44:29Z',earlier_date='2025-07-06T18:06:12Z',cutoff='2026-10-07',
        title_page_publication='Behavior Research Methods58, Article216 (2026)',
        doi='10.3758/s13428-026-03073-2',
        rationale='Select the acquired revised primary text available before cutoff; no claim to have separately acquired the publisher PDF.',
        evidence=[ref(identity,'Title, author and submission-history identity only'),
                  ref(RAW/'exec20_validity_v1.pdf','Preserved genuine earlier version'),
                  ref(pdf,'Genuine selected v2 original')]))
    claims=['The tutorial scales validation requirements to the role of an LLM and the claim being made.',
            'It proposes development followed by held-out assessment, controlled experiments and exact execution records.',
            'It distinguishes observation, experimental and analysis units and recommends dependence-aware, often paired analysis.',
            'It provides methodological guidance and illustrative code, not original empirical validation of a causal assistant or bank use.']
    source=dict(integrated_citation_key='exec20_validity',kind='paper',title=title,filename_title=title,
        first_author='Lin',author='Lin, Zhicheng',year=2026,source_identity='arXiv:2507.04491v2; DOI10.3758/s13428-026-03073-2',
        version_date='15 August2026,22:44:29UTC; v2',cutoff='2026-10-07',
        local_copy=ref(pdf,'Genuine selected original'),local_path=str(pdf.relative_to(ROOT)),
        sha256=hashlib.sha256(data).hexdigest(),inspected_anchors=inspected,supported_claims=claims,limitations=LIMITS,
        identity_evidence=[ref(BASE/'version-selection.json','Selected version'),
                           ref(RAW/'exec20_validity_v2.receipt.json','Versioned PDF acquisition receipt')])
    result=exact.calculate();write(BASE/'exact-results.json',result)
    authored=dict(integrated_citation_key='exec20_validity_reference',kind='project_derivation',
        title='Exact noisy-grading and shared-shock references for causal-assistant evaluation',
        author='Causal banking proposal project',year=2026,source_identity='tools/validity_measurement_reference_20261020.py',
        version_date='20 October2026',local_copy=ref(ROOT/'tools/validity_measurement_reference_20261020.py','Exact rational reference'),
        inspected_anchors=[ref(BASE/'exact-results.json','All exact outputs')],
        supported_claims=['Under the imposed arm-specific grading law, true correctness stays3/5 while observed rates rise13/25 to13/20.',
                          'Known sensitivity and specificity invert the measurement law when their sum differs from1.',
                          'A true improvement1/5 becomes7/50 under the specified invariant imperfect grader.',
                          'At assumed value100 and extra cost8, the true incremental value is-8 while the grade-based value is5.',
                          'A shared-shock model leaves covariance1/4 and correlation5/16 between20-repeat cluster averages.'],
        limitations=result['limitations'])
    write(BASE/'source-audit.json',dict(sources=[source,authored],cutoff='2026-10-07',scope='One primary tutorial and exact authored witnesses'))
    critical=['Averaging removes row multiplicity, but independence of group averages must come from the sampling law; shared shocks survive.',
              'Randomization units, sampling units and analysis units are distinct. Model/condition/session labels alone do not identify them.',
              'No universal20-cluster threshold, general balanced-design equivalence theorem or automatic mixed-model calibration is asserted.',
              'Randomizing a prompt can identify an effect on a specified observed grade without identifying an effect on semantic correctness.',
              'Real sensitivity/specificity must be estimated under held-out adjudication and transport assumptions; uncertainty and weak separation matter.',
              'Fluent output and self-report do not establish psychological properties or bank-customer response behavior.']
    omissions=[('Measurement calibration','Design a held-out, blinded adjudication sample spanning both arms, errors, refusals and subgroup support; estimate calibration uncertainty.'),
               ('Public experiment','Freeze mechanisms, public scenarios, rubric, prompt and grader after development; run only after a separately qualified prototype exists.'),
               ('Dependence and transfer','Define the scenario-sampling law and any shared version/time/session shocks before choosing paired or cluster inference.'),
               ('Secondary literature','Inspect the tutorial\'s original measurement-invariance and dependence references before making their empirical or general theorem claims.'),
               ('Census','Continue61 unread originals, complementary longitudinal/off-policy and negative-result searches, and citation chaining.'),
               ('Rendered and final acceptance','Obtain a fresh visual-review allowance; Q1/Q5 and mandatory repair completeness remain open.')]
    write(BASE/'omissions-register.json',dict(global_blocker=None,items=[dict(item=k,status='open',next_action=v) for k,v in omissions]))
    write(BASE/'primary-review.json',dict(status='pass_for_bounded_primary_review',reviewer=dict(name='Codex author/coordinator',kind='author'),
        findings=claims,source_critical_qualifications=critical,evidence=[ref(BASE/n,'Inspected source and exact argument') for n in
            ['source-audit.json','version-selection.json','exact-results.json','omissions-register.json']],
        limitations=LIMITS,visual_acceptance=False,native_execution=False,coverage_acceptance=False))
    old=read(PRIOR/'census-register.json');new=copy.deepcopy(old)
    item=next(i for i in new['items'] if i['id']=='LA01-candidate-25')
    assert item['disposition']=='open_original_not_inspected'
    item.update(prior_disposition=item['disposition'],disposition='inspected_primary_retained_with_limits',technical_source_review_open=False,
        source_key='exec20_validity',primary_source_record=source,later_primary_review=ref(BASE/'primary-review.json','Bounded methodological review'),
        availability='Genuine v2 selected before cutoff; technical and limitation anchors inspected.',
        effect_on_claims='Supports proposal evaluation design with source-critical qualifications; no empirical bank or runtime claim.',
        next_action='Integrate measurement-validity argument and preserve the separate calibration, dependence and public-prototype obligations.')
    assert len(new['items'])==117 and all(a==b for a,b in zip(old['items'],new['items']) if a['id']!='LA01-candidate-25')
    counts=Counter(i['disposition'] for i in new['items'])
    assert counts['inspected_primary_retained_with_limits']==52 and counts['open_original_not_inspected']==61
    new.update(counts=dict(counts),supersedes=ref(PRIOR/'census-register.json','Preserved51/62 census'),
        changes=['Candidate25 receives bounded primary-original review;116 other records unchanged.'],
        evidence=[ref(BASE/'primary-review.json','Original review')],closure=False,
        interpretation='52/113 originals inspected;61 unread. Four crosscutting obligations retain separate denominators.')
    write(BASE/'census-register.json',new)
    tasks=copy.deepcopy(read(PRIOR/'task-map.json'));assert len(tasks['task_families'])==14
    for task in tasks['task_families']:
        if 'LA01-candidate-25' in task['inherited_ids']:
            task['uninspected_candidate_ids'].remove('LA01-candidate-25')
            task['inspected_candidate_ids'].append('LA01-candidate-25');task['inspected_source_keys'].append('exec20_validity')
        task['coverage_acceptance']=False
    tasks.update(register=ref(BASE/'census-register.json','Current52/61 census'),
        supersedes=ref(PRIOR/'task-map.json','Preserved fourteen-task mapping'))
    tasks.setdefault('primary_application_notes',{}).update(estimation_validation='A prompt experiment must distinguish observed grades from calibrated semantic correctness.',
        evaluation_cost='Pair genuinely shared scenarios, preserve the sampling law and all requests, and report grading and adjudication costs.')
    write(BASE/'task-map.json',tasks)
    write(BASE/'reconciliation-review.json',dict(status='pass',changed_ids=['LA01-candidate-25'],unchanged_other_records=116,
        original_candidates=113,inspected=52,unread=61,task_families=14,coverage_acceptance=False,
        evidence=[ref(BASE/'census-register.json','Preserving successor'),ref(BASE/'task-map.json','Fourteen-task successor')]))
    write(BASE/'review.json',dict(status='pass_for_bounded_primary_review',limitations=LIMITS,coverage_acceptance=False,
        evidence=[ref(BASE/'primary-review.json','Source-critical findings'),ref(BASE/'reconciliation-review.json','Census conservation')]))
    write(BASE/'inspection-progress.json',dict(finding='Candidate25 v2 inspected with source-critical measurement and dependence review; census52 inspected/61 unread.',
        next_action='Integrate measurement validity, compile preserving reader and sponsor, and continue independent eligible work.',
        evidence=[ref(BASE/n,'Inspected evidence') for n in ['source-audit.json','review.json','census-register.json','task-map.json']]))
    verify_bindings(read(BASE/'source-audit.json'));verify_bindings(read(BASE/'review.json'))
    print(json.dumps(dict(inspected=52,unread=61,sources=2,coverage_acceptance=False)))


if __name__=='__main__':main()

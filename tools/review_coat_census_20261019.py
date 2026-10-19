#!/usr/bin/env python3
"""Preserve a bounded primary COAT review and an independently blocked candidate."""
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path

import coat_reference_20261019 as exact
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT/'docs/literature/raw'
BASE = ROOT/'docs/program/execution/2026-10-19/census-hidden-reasoning-v1'
PRIOR = ROOT/'docs/program/execution/2026-10-19/census-retrieval-selfcorrection-v1'
read = lambda p: json.loads(p.read_text())


def main():
    assert not (BASE/'source-audit.json').exists()
    identity = read(BASE/'paper-identity.json')
    pdf = ROOT/identity['pdf']
    assert hashlib.sha256(pdf.read_bytes()).hexdigest() == identity['sha256']
    receipt = read(RAW/'exec19_hidden140_v3.receipt.json')
    assert receipt['status'] == 'saved' and receipt['sha256'] == identity['sha256']
    assert pdf.read_bytes() == (RAW/'exec19_hidden140_v3.pdf').read_bytes()
    assert exact.calculate() == read(BASE/'exact-results.json')
    pages = (BASE/'coat-v3.txt').read_text().split(chr(12))
    assert sum(bool(p.strip()) for p in pages) == 78
    findings = {
        1: 'Title, authors,13October2025v3 and CC-BY4.0 paper notice; project website is a lead, not an audited executable artifact.',
        3: 'COAT-MB, COAT-PAG and treatment-effect extension are distinct tasks; Markov blanket alone need not orient the full graph.',
        8: 'Independent sampled pairs (X,U); deterministic prompt-induced factor mapping W=h(X). Hidden-world wording does not create information absent from X.',
        12: 'Algorithm1 uses highest conditional-entropy cluster and stops at maximum rounds or unchanged blanket; this is an adaptive proposal procedure.',
        17: 'Assumption2 requires Markov/faithful graph-law correspondence and preservation of all conditional independences after factor parsing; measurement noise can violate it.',
        18: 'Definition4 posits positive useful-factor probability and positive multiplicative information reduction; Propositions5/6 assert probability/rate statements.',
        19: 'Proposition8 preserves adjacency and arrowheads within a subset only under its blanket-inclusion condition and maximally informative PAG premise.',
        20: 'Adjustment extension depends on amenability, forbidden-set and blocking conditions; no arbitrary identification claim.',
        21: 'Proposition15 adjustment preservation is conditional on blanket inclusion in the enlarged measured set.',
        30: 'Hillstrom and RetailHero study uses synthesized social-media text under an inherited confounded evaluation design, not a bank deployment.',
        31: 'Largest valid adjustment sets and averaging over tied sets; experiments repeated3times; finite uncertainty/calibration not established by this choice.',
        32: 'Extracted Table7: DeepSeek-V3 COAT RMSE0.47/0.50; GPT-4.1-mini1.90/0.78; Human N-IPW1.32/1.39. No blanket superiority across every model/baseline.',
        37: 'MSFT news/price case uses first200trading days for elicitation and next400for evaluation; next-week target. Printed rolling-window index inequalities need clarification against code.',
        38: 'A200day rolling regression is fitted before the daily decision; source describes an observational trading comparison.',
        39: 'Long/short sign rule and Table9 are reported trading outcomes; transaction-cost, executable timing and causal intervention validation are not established by these paragraphs.',
        41: 'Intervention and experiment-design extensions are future directions, not completed experimental validation.',
        45: 'Proof of Proposition5 treats useful-round count as Binomial(t,p) and explicitly uses Gaussian approximation; exact finite probability guarantee is not derived by that approximation alone.'}
    anchors = []
    for number, finding in findings.items():
        path = BASE/f'coat-page-{number}.txt'
        with path.open('x') as stream:
            stream.write(pages[number-1])
        anchors.append(dict(anchor=f'Physical PDF page {number}',finding=finding,
            extracted_text=ref(path,'Inspected primary text; no rendered visual acceptance')))
    claims = ['COAT proposes and parses factors from unstructured observations, then uses conventional discovery feedback; it separates blanket, PAG and adjustment tasks.',
        'The selected theory explicitly assumes conditional-independence preservation after parsing, appropriate graph/distribution premises and useful-factor proposal ability.',
        'The convergence proof uses a binomial count and a Gaussian approximation; finite adaptive-run guarantees require an additional justified probability model and error control.',
        'PAG and adjustment preservation are conditional on the specified blanket-inclusion and graph premises, not arbitrary hidden-confounder identification.',
        'The marketing experiment uses synthesized text and three repeated experiments; reported RMSE differs by model and comparator.',
        'The financial case is an author-reported historical trading comparison; causal intervention truth, complete costs, timing and native code correspondence remain separate.']
    limits = ['Selected78page v3 dated13October2025, before7October2026 cutoff; original discovery2024 and selected2025version are distinguished.',
        'Bounded inspected technical anchors; no independent proof verification of every graph proposition, replication, live LLM run or code audit.',
        'No images forwarded; extracted tables and text are not rendered visual acceptance.',
        'Reference chains and linked project artifact require separate inspected originals before independent attribution or executable integration.',
        'No universal variable recovery, finite calibration, bank acceptance or observed project ROI.']
    source = dict(integrated_citation_key='exec19_coat',kind='paper',title=identity['title'],filename_title=identity['title'],
        first_author='Liu',author='Liu, Chenxi and Chen, Yongqiang and Liu, Tongliang and Gong, Mingming and Cheng, James and Han, Bo and Zhang, Kun',
        year=2025,source_identity='arXiv:2402.03941v3',version_date='13 October 2025; arXiv:2402.03941v3',cutoff='2026-10-07',
        local_copy=ref(pdf,'Genuine selected original'),local_path=str(pdf.relative_to(ROOT)),sha256=identity['sha256'],
        inspected_anchors=anchors,supported_claims=claims,limitations=limits,
        identity_evidence=[ref(RAW/'exec19_hidden140_abs.html','Title/authors/submission history only'),
            ref(RAW/'exec19_hidden140_v3.receipt.json','Versioned original acquisition'),ref(BASE/'paper-identity.json','Version selection and genuine bytes')])
    reference = dict(integrated_citation_key='exec19_coat_reference',kind='project_derivation',
        title='Exact noisy-factor adjustment and dependent proposal-attempt examples',author='Causal banking proposal project',year=2026,
        source_identity='tools/coat_reference_20261019.py',version_date='19 October2026',
        local_copy=ref(ROOT/'tools/coat_reference_20261019.py','calculate: rational finite-law enumeration'),
        inspected_anchors=[ref(BASE/'exact-results.json','Exact risks, conditional covariance and attempt probabilities')],
        supported_claims=['A75percent-accurate noisy confounder leaves conditional covariance3/64 and standardized contrast1/5 despite true effect0.',
            'Assumed payoff100 and action cost10 give proxy net10 versus true net-10.',
            'Four independent half-success rounds have no-success probability1/16; one shared half-success variable gives1/2 with the same marginals.'],
        limitations=exact.calculate()['limitations'])
    write(BASE/'source-audit.json',dict(sources=[source,reference],cutoff='2026-10-07',
        scope='Bounded COAT primary review and exact authored assumption witnesses'))
    acquisition_failures=[ref(RAW/(name+'.receipt.json'),'Observed fixed-collector allowlist rejection, not source unavailability')
        for name in ['exec19_prophets167_abs','exec19_prophets167_pdf']]
    write(BASE/'omissions-register.json',dict(global_blocker=None,items=[
        dict(candidate='LA01-candidate-167',status='acquisition_route_blocked_original_unread',evidence=acquisition_failures,
            next_action='Use a user-supplied genuine original or an independently authorized public route; do not bypass the fixed collector restriction or infer source absence.'),
        dict(item='COAT executable artifact',status='paper_link_only',next_action='Resolve actual source repository, selected commit, license and environment; inspect parser, time-window and experiment implementation before native admission.'),
        dict(item='Finite adaptive convergence',status='not_established',next_action='Specify history-conditional success assumptions and contraction, then use an exact or justified nonasymptotic probability bound; do not relabel a Gaussian approximation.'),
        dict(item='Bank annotation and temporal truth',status='later_conditional',next_action='Use public/generated gold factors first; later validate bank extraction error, clock and target premises with owners.')]))
    write(BASE/'primary-review.json',dict(status='pass_for_bounded_primary_review',reviewer=dict(name='Codex author/coordinator',kind='author'),
        findings=claims,evidence=[ref(BASE/'source-audit.json','Source identity and inspected anchors'),ref(BASE/'exact-results.json','Authored assumptions witness'),
            ref(BASE/'omissions-register.json','Unresolved originals and proposed repairs'),ref(Path(__file__),'Exact review construction')],
        mathematical_review='Exact authored examples pass. General source propositions retained with premises; approximation and attempt dependence prevent adopting an unconditional finite guarantee.',
        limitations=limits,visual_acceptance=False,independent_acceptance=False,coverage_acceptance=False))
    old=read(PRIOR/'census-register.json');new=copy.deepcopy(old)
    for item in new['items']:
        if item['id']=='LA01-candidate-140':
            assert item['disposition']=='open_original_not_inspected'
            item.update(prior_disposition=item['disposition'],disposition='inspected_primary_retained_with_limits',technical_source_review_open=False,
                source_key='exec19_coat',primary_source_record=source,later_primary_review=ref(BASE/'primary-review.json','Selected COAT original'),
                availability='Genuine v3 acquired and selected technical anchors inspected; native artifact remains a lead.',
                effect_on_claims='Conditional representation, PAG and adjustment proposal evidence; no general hidden-variable or finite-calibration award.',
                next_action='Integrate conditional argument and exact measurement-error/attempt examples; inspect native artifact and sampling/error assumptions before prototype qualification.')
        if item['id']=='LA01-candidate-167':
            item.update(availability='Fixed collector rejected the ACL host; original remains unread. This is a route restriction, not source unavailability.',
                acquisition_evidence=acquisition_failures,next_action='Obtain a supplied original or an independently authorized acquisition route before any technical claim.')
    changed={'LA01-candidate-140','LA01-candidate-167'}
    assert all(a==b for a,b in zip(old['items'],new['items']) if a['id'] not in changed)
    counts=Counter(i['disposition'] for i in new['items'])
    assert counts['open_original_not_inspected']==64 and counts['inspected_primary_retained_with_limits']==49
    new.update(counts=dict(counts),supersedes=ref(PRIOR/'census-register.json','Preserved48/65census'),
        changes=['Candidate140 receives bounded primary inspection; candidate167 receives acquisition-failure evidence only.'],
        evidence=[ref(BASE/'primary-review.json','One original inspected'),ref(BASE/'source-audit.json','Genuine original and authored reference')],
        closure=False,interpretation='49/113originals inspected;64unread. Four crosscutting records retain separate denominators.')
    write(BASE/'census-register.json',new)
    taskmap=copy.deepcopy(read(PRIOR/'task-map.json'));assert len(taskmap['task_families'])==14
    for task in taskmap['task_families']:
        if 'LA01-candidate-140' in task['inherited_ids']:
            task['uninspected_candidate_ids'].remove('LA01-candidate-140')
            task['inspected_candidate_ids'].append('LA01-candidate-140');task['inspected_source_keys'].append('exec19_coat')
        task['coverage_acceptance']=False
    taskmap.update(register=ref(BASE/'census-register.json','Current49/64census'),supersedes=ref(PRIOR/'task-map.json','Preserved14-task mapping'))
    write(BASE/'task-map.json',taskmap)
    write(BASE/'reconciliation-review.json',dict(status='pass',changed_ids=sorted(changed),
        newly_inspected=['LA01-candidate-140'],failure_only=['LA01-candidate-167'],unchanged_other_records=True,
        original_candidates=113,inspected=49,unread=64,task_families=14,coverage_acceptance=False,
        evidence=[ref(BASE/'census-register.json','Preserving successor'),ref(BASE/'task-map.json','Preserved task mapping')]))
    write(BASE/'review.json',dict(status='pass_for_bounded_primary_review',evidence=[ref(BASE/'primary-review.json','Source and assumption review'),
        ref(BASE/'reconciliation-review.json','Census conservation')],limitations=limits,coverage_acceptance=False))
    write(BASE/'inspection-progress.json',dict(finding='COATv3 primary anchors inspected;49of113originals inspected,64unread. Independent ACL candidate is route-blocked and remains unread.',
        next_action='Integrate COAT conditional representation and exact noisy-factor examples into preserving reader and sponsor, then continue other eligible census/software work.',
        evidence=[ref(BASE/n,'Bounded inspected evidence') for n in ['source-audit.json','primary-review.json','review.json','census-register.json','task-map.json','reconciliation-review.json']]))
    verify_bindings(read(BASE/'source-audit.json'));verify_bindings(read(BASE/'primary-review.json'))
    print(json.dumps(dict(inspected=49,unread=64,sources=2,coverage_acceptance=False)))


if __name__=='__main__':
    main()

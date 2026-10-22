#!/usr/bin/env python3
"""Record two inspected pre-cutoff originals without closing the frontier census."""
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import weighted_target_reference_20261022 as exact
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-22/census-factuality-weighted-v1'
PRIOR=ROOT/'docs/program/execution/2026-10-22/census-domain-knowledge-v1'
RAW=ROOT/'docs/literature/raw'
read=lambda p:json.loads(p.read_text())
LIMITS=[
    'Selected extracted primary technical text inspected; figures and rendered visual acceptance remain unreviewed.',
    'Selected editions have printed pre-cutoff dates; acquisition22October2026 does not reconstruct historical archive bytes.',
    'The factuality paper is a survey: its descriptions of cited experiments are not independently reviewed originals.',
    'The weighted-estimands paper is econometrics, not a new LLM or causal-discovery algorithm.',
    'Weighted-target robustness presupposes valid group effects; it does not repair confounding or identify unknown population weights.',
    'No downloaded code, paper implementation, live model, public dataset or sibling repository was executed.',
    'Authored financial examples and known-normal coverage are mathematical illustrations, not bank observations or native qualification.',
    '61/113 original candidates inspected;52 unread plus four crosscutting search obligations remain.',
    'No source license, release equivalence, uniform live-agent calibration, independent acceptance or product deployment is established.']

FACTUALITY={
 1:'Printed18-author identity and16December2023 arXivv3 banner; ACM2018 footer and placeholder DOI are template artifacts, not publication evidence.',
 4:'Section2.2 scopes factuality to clear, determinable, undisputed facts; footnote excludes minor errors in reliable sources.',
 5:'Knowledge/model configurations; survey scope does not resolve causal identification.',
 8:'Survey taxonomy separates rule-based, neural, human and LLM-based factuality evaluation.',
 10:'Lexical and semantic metrics are discussed as factuality proxies; overlap is not causal entailment.',
 11:'Attribution and atomic support assess evidence support; survey reports human-evaluation limitations.',
 12:'LLM-based judges require validation and face bias/domain limitations.',
 28:'Retrieval failure routes include insufficient, conflicting or misleading information, distraction and misinterpretation.',
 32:'Multi-agent debate described as surveyed work, not an independently inspected experiment.',
 36:'Interactive/agent retrieval is a surveyed strategy; no calibrated causal validity claim follows.',
 37:'Task/domain adaptation discussion; dependent retrieval and reasoning errors remain possible.',
 40:'Structured knowledge, entity and query mapping; KG relations have no automatic causal-edge semantics.',
 45:'Financial NLP applications do not validate interventions or causal graphs.',
 46:'Causal language model denotes autoregressive architecture in the discussed finance context, not intervention identification.'}
WEIGHTED={
 1:'Vilfort sole-author identity;28August2026v2 banner and1September2026 title date, both pre-cutoff.',
 7:'Group effects, normalized possibly negative weights and weighted targets; causal interpretation depends on group-effect assumptions.',
 8:'Exact multivariate normal experiment with known positive-definite covariance and fixed finite group count.',
 9:'Known baseline weights and standard baseline confidence intervals; distributional and target conditions.',
 10:'Ambiguity and disagreement about weights are distinct from sampling error.',
 11:'Alternative weight class nonempty, compact and convex; meaning of alternative targets.',
 13:'Class specifications and distance geometry; not identification of an unknown population.',
 14:'Heterogeneity norm and sharp Cauchy-Schwarz bound on weighted-target differences.',
 15:'Whitened mean-residual projection and heterogeneity construction.',
 16:'Noncentral chi-square distribution notation parameterizes by heterogeneity; conventional noncentrality is its square.',
 17:'Heterogeneity UCB from monotone CDF inversion, including zero-bound branch.',
 18:'Bounds and confidence set interpretation; distinguish source theorem from authored example.',
 19:'Worst-case bias bound as heterogeneity UCB times maximum covariance-metric distance.',
 20:'Minimax-bias center minimizes maximum distance, not necessarily total confidence-interval length.',
 22:'Folded-normal two-sided critical value;Proposition6 guarantees1-(alpha+beta) for each fixed target uniformly.',
 23:'Uniform target guarantee and confidence-budget tradeoffs.',
 24:'Fixed-K asymptotic body; growing-K AppendixG is not technically reviewed.',
 25:'Uniform CLT and covariance/eigenvalue conditions for asymptotic extension.',
 26:'Weight consistency, random weight classes and continuity conditions.',
 27:'Class consistency and sufficient optimization regularity, including uniform Slater-type conditions.',
 35:'Estimated-class convergence does not by itself contain a fixed boundary target.',
 36:'Random versus fixed targets and target-class interpretation.',
 37:'Enlarged-class and containment conditions; no unqualified feasible coverage from consistency alone.',
 38:'PropositionU8 targets a subclass contained in estimated classes with adequate probability.',
 39:'Remark8 guarantees fixed positive delta; empirical delta0 and unchanged rounding at.0001 do not prove the theorem at zero slack.',
 40:'Feasible construction with group estimates, covariance, weights and class specifications.',
 41:'Specification choices and numerical optimization are part of implementation needs.',
 44:'Event-study target construction requires group-time effects and joint covariance.',
 45:'Per-event-time results do not automatically cover all event times simultaneously.',
 46:'Multisite experiment mapping; target weights are substantive assumptions.',
 50:'Author ProjectSTAR application, not a project replication.',
 51:'Reported weight sensitivity in author application; no raw data/code executed here.',
 52:'Reported class/interval comparisons depend on target specifications.',
 53:'Author application discussion; no measured bank transport or economics.',
 69:'AppendixC.1 distinguishes uniform point from simultaneous set coverage.',
 70:'Proposition7 gives two-sided1-(2alpha+beta), one-sided1-(alpha+beta); target-use interpretation.',
 71:'AppendixD.1 inspected Cauchy-Schwarz proof of sharp target-difference bound.',
 74:'Proposition6 proof uses heterogeneity-bound event and nominal sampling event.',
 75:'Proposition7 proof controls both endpoints; union bound changes two-sided simultaneous confidence.'}


def main():
    assert not (BASE/'source-audit.json').exists()
    specs=[dict(name='factuality',id='LA01-candidate-268',key='exec22_factuality_wang',surname='Wang',year=2023,
      title='Survey on Factuality in Large Language Models: Knowledge, Retrieval and Domain-Specificity',
      author='Wang, Cunxiang and Liu, Xiaoze and Yue, Yuanhao and Guo, Qipeng and Hu, Xiangkun and Tang, Xiangru and Zhang, Tianhang and Jiayang, Cheng and Yao, Yunzhi and Hu, Xuming and Qi, Zehan and Gao, Wenyang and Wang, Yidong and Yang, Linyi and Wang, Jindong and Xie, Xing and Zhang, Zheng and Zhang, Yue',
      raw='exec22_census_factuality_v3',identity='exec22_census_factuality_identity',pages=62,anchors=FACTUALITY,
      version='arXiv2310.07521v3,16December2023; not an authenticated ACM2018 publication',
      mapping=['expert_evidence','diagram_construction','agent_architecture','reporting_monitoring','evaluation_cost'],
      identity_qualifications=['Atom metadata lists16 authors while selected printed v3 lists18; bibliography follows the printed edition, including Qipeng Guo and Xiangkun Hu.',
        'ACM2018 footer, copyright boilerplate and placeholder DOI do not establish publication or unrestricted software/republication rights.'],
      claims=['Survey taxonomy separates lexical/rule-based, neural, human and LLM-based evaluation; attribution support differs from external truth.',
        'Its factuality scope favors determinable undisputed facts; disputed causal hypotheses need separate scientific assumptions and evidence.',
        'Retrieval can fail through missing/conflicting evidence, distraction and reasoning mistakes; agent agreement and repeated retrieval are not independent causal evidence.',
        'Finance NLP applications and autoregressive causal language models do not establish intervention validity.']),
      dict(name='weighted',id='LA01-candidate-256',key='exec22_weighted_vilfort',surname='Vilfort',year=2026,
      title='Robust Inference for Weighted Estimands',author='Vilfort, Vod',raw='exec22_census_weighted_v2',
      identity='exec22_census_weighted_identity',pages=104,anchors=WEIGHTED,
      version='arXiv2607.07524v2,28August2026; printed title date1September2026',
      mapping=['business_translation','estimation_validation','reporting_monitoring','evaluation_cost'],
      identity_qualifications=['Archive revision and printed title dates are both pre-cutoff; no journal publication is asserted.'],
      claims=['Fixed weighted targets and a nonempty compact convex alternative weight class are studied under exact multivariate normal estimates with known positive-definite covariance.',
        'The covariance-metric Cauchy-Schwarz bound factors target differences into heterogeneity and weight distance; minimax-bias weights minimize maximum distance.',
        'Proposition6 gives1-(alpha+beta) uniform coverage of each fixed alternative target;Proposition7 gives1-(2alpha+beta) simultaneous two-sided set coverage.',
        'Conventional noncentral chi-square noncentrality is H squared, and feasible inference needs covariance/weight/class regularity.',
        'PropositionU8 needs target containment;Remark8 fixed positive slack guarantee is distinct from displayed delta0 empirical results.',
        'Full joint group-time covariance is needed; public application results are author-reported, not project replications.'])]
    sources=[]
    for s in specs:
        original=RAW/(s['raw']+'.pdf');receipt=read(RAW/(s['raw']+'.receipt.json'))
        assert receipt['status']=='saved' and receipt['http_status']==200
        assert hashlib.sha256(original.read_bytes()).hexdigest()==receipt['sha256']
        paper=ROOT/'docs/papers'/f'{s["title"]} {s["surname"]}({s["year"]}).pdf'
        assert not paper.exists();paper.write_bytes(original.read_bytes())
        pages=(BASE/(s['name']+'-original.txt')).read_text().split('\f')
        assert len([p for p in pages if p.strip()])==s['pages']
        for n in s['anchors']:
            p=BASE/f'{s["name"]}-page-{n:03}.txt'
            if not p.exists():
                assert n==1
                p.write_text(pages[0])
        source=dict(integrated_citation_key=s['key'],kind='paper',title=s['title'],author=s['author'],
          first_author=s['surname'],year=s['year'],source_identity=receipt['url'],version_date=s['version']+'; acquired22October2026',
          cutoff='2026-10-07',local_path=str(paper.relative_to(ROOT)),sha256=receipt['sha256'],
          local_copy=ref(paper,'Genuine selected pre-cutoff edition under required scholarly filename'),
          inspected_anchors=[dict(anchor=f'PDF physical page{n}',finding=finding,
            extracted_text=ref(BASE/f'{s["name"]}-page-{n:03}.txt','Inspected primary text; figure pixels unreviewed')) for n,finding in s['anchors'].items()],
          supported_claims=s['claims'],identity_qualifications=s['identity_qualifications'],limitations=LIMITS,
          identity_evidence=[ref(RAW/(s['raw']+'.receipt.json'),'Successful selected-edition acquisition'),
            ref(RAW/(s['identity']+'.xml'),'Archive identity only; printed-edition author qualification applies'),
            ref(BASE/(s['name']+'-pdfinfo.txt'),'Observed PDF information')])
        sources.append(source)
    write(BASE/'exact-results.json',exact.calculate())
    sources.append(dict(integrated_citation_key='exec22_weighted_reference',kind='project_derivation',
      title='Exact banking target-weight geometry and analytic wrong-target normal coverage',author='Causal banking proposal project',year=2026,
      source_identity='tools/weighted_target_reference_20261022.py',version_date='22October2026',
      local_copy=ref(ROOT/'tools/weighted_target_reference_20261022.py','Authored exact rational geometry and analytic normal probability'),
      inspected_anchors=[ref(BASE/'exact-results.json','Reproduced target, net, ambiguity, sharpness and confidence-budget values')],
      supported_claims=['Stipulated effects6/-2 give baseline4, alternative0 and net3/-1 at cost1.',
        'Truncated-simplex net bounds3-6epsilon/3+2epsilon; strictly positive worst case needs epsilon<1/2.',
        'Known covarianceI gives H squared32 and distance squared1/2, attaining squared difference16.',
        'At epsilon2/3, minimax first weight7/12 gives effect8/3 with oracle radius8/3.',
        'Analytic baseline-normal95% interval covers the stipulated different target with the saved probability; this is not robust-method execution.',
        'Alpha/beta.05/.05 imply point90% and simultaneous two-sided85%;.0125/.025 yield simultaneous95% under source assumptions.'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,cutoff='2026-10-07',visual_acceptance=False))
    write(BASE/'plan-review.json',dict(status='pass_for_bounded_execution',reviewer=dict(name='Codex author/coordinator',kind='author'),
      evidence=[ref(BASE/'plan.md','Reviewed bounded plan')],checks=[
        'Acquire and inspect selected pre-cutoff editions, preserve v1 and failed receipts, qualify date/author/template differences.',
        'Separate survey synthesis, actual econometric guarantees and authored reference calculations.',
        'Preserve117 rows and14 task families; do not turn two inspections into census closure.']))
    omissions=[
      dict(id='factuality-originals',next_action='Acquire and independently inspect the original attribution/judge/agent studies before citing their technical or comparative results; survey-only descriptions stay attributed.'),
      dict(id='weighted-implementation',next_action='Acquire pinned public code/data and terms; inspect noncentral-CDF parameterization, folded-normal critical values, optimization and class containment before native comparison.'),
      dict(id='weighted-growing-K',next_action='Inspect AppendixG separately before any growing-group or general panel guarantee.'),
      dict(id='feasible-target-class',next_action='Specify fixed versus result-selected target, covariance estimation and class slack/containment; do not transfer exact known-covariance guarantees to estimated classes automatically.'),
      dict(id='public-evaluation',next_action='Use public known-law effects and independent evidence corpora; evaluate citation support, causal validity and fixed/simultaneous target coverage separately before costly bank work.'),
      dict(id='census',next_action='Inspect52 remaining originals and four crosscutting searches; no candidate acquisition failure blocks unrelated work.'),
      dict(id='visual',next_action='Use a fresh image allowance to inspect figures and rendered additions; text extraction and text bounds do not grant visual acceptance.')]
    write(BASE/'omissions-register.json',dict(items=omissions,global_blocker=None,no_source_waivers=True))
    write(BASE/'primary-review.json',dict(status='pass_for_scoped_primary_text_review',coverage_acceptance=False,
      evidence=[ref(BASE/n,'Bounded primary-source evidence') for n in ['source-audit.json','exact-results.json','plan-review.json','omissions-register.json']],
      findings=[c for s in sources for c in s['supported_claims']],limitations=LIMITS,
      visual_acceptance=False,native_execution=False))
    old=read(PRIOR/'census-register.json');new=copy.deepcopy(old)
    for s in specs:
        row=next(r for r in new['items'] if r['id']==s['id'])
        assert row['disposition']=='open_original_not_inspected'
        row.update(prior_disposition=row['disposition'],disposition='inspected_primary_retained_with_limits',
          technical_source_review_open=False,source_key=s['key'],primary_source_record=next(x for x in sources if x['integrated_citation_key']==s['key']),
          later_primary_review=ref(BASE/'primary-review.json','Actual selected-edition primary-text inspection'),
          task_families=s['mapping'],mapping_basis='Inspected definitions, target, evaluation and limitations; not a title-level causal-method classification.',
          availability='Authentic explicit pre-cutoff edition acquired; earlier edition and failed-route evidence preserved.',
          effect_on_claims='Qualified factuality/target specification support; no causal validity, native method, coverage closure or bank qualification.',
          next_action=omissions[0 if s['name']=='factuality' else 1]['next_action'])
    changed={s['id'] for s in specs}
    assert all(a==b for a,b in zip(old['items'],new['items']) if a['id'] not in changed)
    counts=Counter(r['disposition'] for r in new['items'])
    assert len(new['items'])==117 and counts['inspected_primary_retained_with_limits']==61 and counts['open_original_not_inspected']==52
    new.update(counts=dict(counts),supersedes=ref(PRIOR/'census-register.json','Preserved59/54 census'),
      changes=['Only candidates256/268 technically reviewed;115 other rows unchanged.'],
      evidence=[ref(BASE/'primary-review.json','Two authentic-original reviews')],closure=False,
      interpretation='61/113 originals inspected;52 unread;four crosscutting searches remain. Weighted-estimands paper is econometric support, not an LLM algorithm.')
    write(BASE/'census-register.json',new)
    tasks=copy.deepcopy(read(PRIOR/'task-map.json'));assert len(tasks['task_families'])==14
    for task in tasks['task_families']:
        for s in specs:
            if s['id'] in task['uninspected_candidate_ids']:task['uninspected_candidate_ids'].remove(s['id'])
            if task['id'] in s['mapping']:
                for field,value in [('inspected_candidate_ids',s['id']),('inspected_source_keys',s['key'])]:
                    if value not in task.setdefault(field,[]):task[field].append(value)
        task['coverage_acceptance']=False
    tasks.update(register=ref(BASE/'census-register.json','61 inspected/52 unread'),supersedes=ref(PRIOR/'task-map.json','Preserved14-family map'))
    write(BASE/'task-map.json',tasks)
    write(BASE/'reconciliation-review.json',dict(status='pass',changed_ids=sorted(changed),unchanged_other_records=115,
      original_candidates=113,inspected=61,unread=52,task_families=14,
      evidence=[ref(BASE/'census-register.json','Conserved117 rows'),ref(BASE/'task-map.json','Conserved14 task families')]))
    write(BASE/'conversion-contract.json',dict(status='proposed_not_implemented',integration_allowed=False,
      inputs=['Business action, clock, units, group effects and identification/sampling assumptions.',
        'Fixed baseline and alternative weights or declared admissible class; signed/simplex semantics, covariance, target-selection rule and confidence budget.',
        'Evidence spans, edition/hash and separate source-support, external-truth, causal and numerical checks.'],
      outputs=['Explicit fixed-target versus simultaneous-set coverage, actual alpha/beta, class/containment and solver status.',
        'Target effect/value set, sensitivity breakpoints and refusal for unsupported inference.',
        'Typed library/CLI/MCP fields; model summaries cannot invent missing covariance, weights, evidence or authorization.'],
      qualification=['Separate known-normal oracle checks from estimated-covariance/asymptotic studies.',
        'Match evidence and budgets for retrieval/agent baselines; hold out documents and domains.',
        'Include confounded twins, unsupported citations, weight-shift and boundary-class failures; measure uncertainty and cost separately.'],
      reference=ref(BASE/'exact-results.json','Authored mathematical oracle only')))
    write(BASE/'review.json',dict(status='pass_for_bounded_candidate_inspection',coverage_acceptance=False,limitations=LIMITS,
      evidence=[ref(BASE/n,'Scoped reviewed progress') for n in ['primary-review.json','reconciliation-review.json','conversion-contract.json']]))
    write(BASE/'inspection-progress.json',dict(
      finding='Candidates256/268 inspected in explicit pre-cutoff editions;61/52 census;survey/econometric scope and coverage distinctions reviewed.',
      next_action='Integrate factuality and target-weight arguments into preserving paired documents, then inspect52 remaining originals and four crosscutting searches. Continue independent Python IV/RD, commercial and reuse work; Python fit/covariance kernels are acquired and inspected, while RD/CausalPy IV and numerical guards remain open.',
      evidence=[ref(BASE/n,'Reviewed census continuation') for n in ['source-audit.json','review.json','census-register.json','task-map.json','omissions-register.json']],
      coverage_acceptance=False,global_blocker=None,
      yield_reason='Two-source review is complete and preserved; release the active operation for integration without closing census coverage or pausing independent work.'))
    verify_bindings(read(BASE/'source-audit.json'));verify_bindings(read(BASE/'review.json'))
    print(json.dumps(dict(inspected=61,unread=52,records=3,scholarly_pdfs_added=2,wrong_target_coverage=exact.calculate()['wrong_target_interval']['wrong_target_coverage'],global_blocker=None)))


if __name__=='__main__':main()

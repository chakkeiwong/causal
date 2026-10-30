"""Single-use primary flexBCF paper integration and exact additions review."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re
from release_candidate_20261029 import MATH

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/release/2026-10-29'
EVIDENCE=BASE/'source-flexpaper-017'
SOURCE=BASE/'source/docs/writing-repair/2026-10-29'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ledger=json.loads((BASE/'edits.json').read_text())
    assert len(ledger)==81, 'Single-use integration'
    changes={}
    def edit(p,before,after,reason,destination):
        original,current=changes.get(p,(p.read_text(),p.read_text()))
        assert current.count(before)==1
        changes[p]=(original,current.replace(before,after,1))
        ledger.append(dict(file=str(p.relative_to(ROOT)),before=before,after=after,
                           reason=reason,substantive_destination=destination))
    p=SOURCE/'src/d587fa2f22fbb93b.tex'
    before=r'''\subsection{Integration choices and the remaining census}'''
    extra=r'''\subsection{A scalable longitudinal forest still needs an identification model}
\label{rel17:flex-paper}
The original flexBCF study by \citet{rel17flexpaper} supplies a consequential comparison between computational feasibility and scientific adequacy. The inspected original is arXiv version 2, posted on 11 May 2023 and carrying a 15 May 2023 title-page date. It is distinct from both a fresh replication and an audit of the selected 2025 package. The authors analyze the 2022 ACIC challenge: 3,400 synthetic datasets, comprising 200 replications of each of seventeen mechanisms, with treatment assigned to medical practices after two pre-treatment years. For banking, the analogous question is the effect of a branch-level intervention on customers served by treated branches. It requires a branch assignment clock, a specified customer population and a defense of the comparison across branches.~\citep{rel17flexpaper}

Their identification argument uses consistency and no anticipation, overlap, and conditional independence of untreated outcome changes and assignment given baseline covariates. Define $Z$ as branch assignment, $X$ as permitted baseline information, $s$ as a pre-intervention date and $t$ as a post-intervention date. Let $m_{zt}(x)=E(Y_t\mid Z=z,X=x)$. The corresponding conditional effect among treated units is
\begin{equation}
 \tau_{\rm T}(x,t)
 =m_{1t}(x)-m_{0t}(x)-\{m_{1s}(x)-m_{0s}(x)\}.
 \label{rel17:flex-did}
\end{equation}
The paper proves this difference-in-differences identity in its Appendix S1. Its stated conditional independence is stronger than the equality of conditional untreated mean changes needed for this mean identity. A portfolio ATT must further average over the declared treated population; an unqualified all-customer average is a different target. Neither a fitted propensity feature nor a large number of customer rows verifies the identifying assumptions.~\citep{rel17flexpaper}

The estimation model adds a separate restriction. It represents the outcome mean by a common prognostic function of covariates and time, plus a treatment function activated only after intervention. Before intervention, that specification forces treated and untreated groups with the same included covariates to have the same expected outcome level. Parallel untreated trends alone do not impose equal baseline levels. To see the distinction, consider equally likely branch groups with no varying observed covariates. Their pre-intervention monetary means are USD 10 and USD 14. Untreated outcomes rise by USD 3 in both groups; the second group receives an intervention adding USD 2. Observed post-intervention means are therefore USD 13 and USD 19. The post-period gap is USD 6, but subtracting the USD 4 pre-period gap identifies the USD 2 effect. At an assumed USD 3 per-customer intervention cost, the identified margin is USD $-1$, whereas treating the post-period gap as the effect yields USD 3. This exact law satisfies overlap and parallel untreated increments while violating equal baseline levels. It does not assert that a particular fitted forest necessarily returns the post-period gap.~\citep{rel17flexpaper,rel17flexwitness}

The challenge analysis also conditions the treatment component on some post-treatment practice-composition summaries. The authors explicitly assume that intervention does not change attrition and hence practice composition. A bank must examine that assumption when assistance changes account closure, migration or the customers remaining at a branch. If composition responds to intervention, conditioning on its later value can change the causal question or introduce selection. A serious alternative is to model changes under a defended trend restriction, with a fixed population and dependence-aware evaluation; it is not enough to feed later composition into a flexible learner and retain the original target label.~\citep{rel17flexpaper}

Computational improvement did not remove the inferential limitation in the reported challenge. For nominal 90\% overall-ATT credible intervals, the original beneficiary-level submission had mean coverage 52.15\% across the seventeen mechanisms; the practice-level analysis had mean coverage 83.68\%. Its mean RMSE rose from 20.54 to 23.04 when aggregated to practices. The paper reports that flexible propensity estimation often increased interval width and coverage, while point-estimation differences were modest. These historical summaries are attributed results, not independent reconstructions, and they do not establish a universal preference for aggregation, a propensity learner or a sparsity prior. The authors discuss outcome-model misspecification, omitted pre-treatment outcomes or trends, and limited sensitivity analysis as explanations and limits.~\citep{rel17flexpaper}

The study motivates examining tree persistence, categorical partitioning and memory allocation, but its runtime narrative supplies no matched bank total-cost estimate. Nor does its empirical performance diagnose the later pinned caller defect above: these concern different versioned evidence. For a bank prototype, the useful comparison separates the identifying trend restriction, additional response-model restrictions, customer and branch sampling units, composition assumptions, and the reporting path. Faster computation merits adoption only when the resulting estimand and uncertainty remain appropriate to the decision. A failed calibration or an unsupported composition assumption should reverse an otherwise attractive computational recommendation.~\citep{rel17flexpaper,rel16flexcallers}

'''
    edit(p,before,extra+before,
         'Close the missing dedicated flexBCF original with its identification, estimation restrictions and adverse empirical evidence.',
         'Additive subsection; every prior mathematical, implementation, alternative and historical-coverage passage remains. Distinguishes trend identification from equal-level modeling and versioned source defects.')
    p=SOURCE/'references-0.bib';before=p.read_text()[-500:]
    extra=r'''

@article{rel17flexpaper,
 author={Kokandakar, Ajinkya H. and Kang, Hyunseung and Deshpande, Sameer K.},
 title={Bayesian Causal Forests \& the 2022 ACIC Data Challenge: Scalability and Sensitivity},
 year={2023},
 journal={arXiv preprint},
 note={2211.02020v2, posted 11 May 2023; title-page date 15 May 2023; genuine 18-page original inspected, including Appendix S1. Journal identity: Observational Studies 9(3), 29--41; preprint bytes are the inspected version},
 url={https://arxiv.org/abs/2211.02020v2}
}

@misc{rel17flexwitness,
 author={{Causal banking proposal project}},
 title={Exact parallel-trend and unequal-baseline branch witness},
 year={2026},
 note={29 October 2026; constructed two-group potential-outcome law and monetary comparison; no fitted forest or bank observations}
}
'''
    edit(p,before,before+extra,'Add authentic original and exact project-law bibliography identities.',
         'All existing references survive; distinguishes inspected arXiv version from later journal identity and separates original evidence from project illustration.')
    paper='docs/papers/Bayesian Causal Forests & the 2022 ACIC Data Challenge Scalability and Sensitivity Kokandakar(2023).pdf'
    def bindings(names):return [dict(path=n,sha256=sha(ROOT/n)) for n in names]
    names=[paper,'docs/literature/raw/rel16_flexpaper_v2.pdf','docs/literature/raw/rel16_flexpaper_v2.receipt.json',
           'docs/literature/raw/rel16_flexpaper_arxiv.xml','docs/literature/raw/rel16_flexpaper_arxiv.receipt.json',
           'docs/literature/raw/rel16_flexpaper_crossref.json','docs/literature/raw/rel16_flexpaper_crossref.receipt.json',
           'docs/release/2026-10-29/source-flexbcf-016/paper.txt','docs/release/2026-10-29/source-flexbcf-016/paper-pdfinfo.txt']
    audit={'cutoff':'2026-10-07','scope':'Authentic original fully read as text including proof and supplement; figure captions read, figures not visually inspected in this session. No benchmark replication or native execution.','sources':[
        dict(citation_key='rel17flexpaper',kind='paper',source_identity='https://arxiv.org/abs/2211.02020v2; journal DOI 10.1353/obs.2023.0024',
             version_date='arXiv v2 posted 2023-05-11; PDF title-page date 2023-05-15. Retrieved 2026-10-29. Pre-cutoff availability supported by versioned arXiv metadata; not asserted byte-identical to journal.',
             local_bindings=bindings(names),
             inspected_anchors=['All18 pages extracted and read, including main text, references, S1 identification proof and S2/S3 text/captions.',
                 'Pages3-4: four-period practice assignment, CATT, A1-A3, Eq2 conditional difference-in-differences and Eq4 outcome-level restriction.',
                 'Pages5-6: implementation memory motivation, tree serialization, categorical partitioning, composition/attrition assumption,90% credible intervals and reported mean coverage/RMSE.',
                 'Pages7-11: propensity/prior sensitivity, limited generalization and omitted pre-treatment-outcome/model-misspecification explanation.',
                 'Page13: complete identification derivation. Pages14-18: practice-level sensitivity and figure captions; no digitized graph values used.'],
             supported_claims=['Conditional untreated-change independence identifies the displayed conditional effect via baseline-gap subtraction; response-level model separately forces equal included-covariate baseline means.',
                 'Challenge had3400 datasets from17 mechanisms with200 replications. Nominal90% overall-ATT intervals had reported mean coverage52.15% beneficiary-level and83.68% practice-level, with mean RMSE20.54 and23.04.',
                 'The analysis assumes intervention does not change attrition/composition when conditioning on later composition summaries.',
                 'Authors report computational feasibility improvements and sensitivity limits; these do not establish current native correctness or bank costs.'],
             limitations=['No independent empirical reproduction or figure-level visual reading.','Paper version and selected2025 package are distinct; the caller defect is not offered as an explanation of historical paper results.','References inside this paper are not automatically admitted as inspected originals.']),
        dict(citation_key='rel17flexwitness',kind='project_derivation',source_identity='tools/release_flexbcf_paper_witness_20261029.py',version_date='2026-10-29; exact two-group law',
             local_bindings=bindings(['tools/release_flexbcf_paper_witness_20261029.py','docs/release/2026-10-29/source-flexpaper-017/exact-witnesses.json']),
             inspected_anchors=['main(): equally likely branch types, no varying X, fixed untreated increment3, treatment increment2, pre means10/14 and observed post means13/19; exact gap and cost arithmetic.'],
             supported_claims=['Parallel untreated increments with marginal overlap need not imply equal baseline means.','Post gap6 minus pre gap4 equals effect2; cost3 yields correct margin-1, while misusing post gap yields3.'],
             limitations=['Constructed law only; no fitted implementation or causal assertion about bank records.'])]}
    audit_path=EVIDENCE/'source-audit.json';assert not audit_path.exists()
    math_path=BASE/'mathematical-addition-reviews.json';math_reviews=json.loads(math_path.read_text())
    e=ledger[-2]
    count=lambda s:Counter(re.sub(r'\s+',' ',m[0]) for m in MATH.finditer(s))
    assert not count(e['before'])-count(e['after'])
    math_reviews['reviews'].append(dict(scope='Author review of additive conditional-DID notation and exact two-group law; no removals.',
        edits=[dict(edit=82,file=e['file'],before_sha256=hashlib.sha256(e['before'].encode()).hexdigest(),after_sha256=hashlib.sha256(e['after'].encode()).hexdigest())],
        allowed_added=dict(count(e['after'])-count(e['before'])),allowed_removed={},status='reviewed_additions_only',
        derivation='Consistency/no anticipation converts observed baseline to untreated potential outcomes. Conditional untreated-change means agree across groups, so subtracting the baseline group gap from the post group gap identifies the treated conditional effect. Conditional change independence in the paper is sufficient and stronger than this mean condition. Portfolio ATT integrates over treated X. Equal baseline levels are an additional response-model restriction.',
        reviewed_assumptions=['Well-defined branch intervention, no cross-branch interference, no anticipation, overlap and integrable outcomes.','The synthetic branch group fixes untreated level, not untreated change; the latter is constant, so trend independence holds at constant X despite unequal levels.','No universal fitted-forest value or benchmark replication is inferred.'],
        witness=dict(path='docs/release/2026-10-29/source-flexpaper-017/exact-witnesses.json',sha256=sha(EVIDENCE/'exact-witnesses.json')),
        source_audit=dict(path=str(audit_path.relative_to(ROOT)),sha256=hashlib.sha256((json.dumps(audit,indent=2)+'\n').encode()).hexdigest()),
        fresh_visual_acceptance=False,independent_acceptance=False))
    backup=EVIDENCE/'before';backup.mkdir(exist_ok=False)
    for p,(old,new) in changes.items():
        assert p.read_text()==old
        (backup/p.name).write_text(old)
    (backup/'edits.json').write_bytes((BASE/'edits.json').read_bytes())
    (backup/'mathematical-addition-reviews.json').write_bytes(math_path.read_bytes())
    audit_path.write_text(json.dumps(audit,indent=2)+'\n')
    for p,(old,new) in changes.items():p.write_text(new)
    (BASE/'edits.json').write_text(json.dumps(ledger,indent=2)+'\n')
    math_path.write_text(json.dumps(math_reviews,indent=2)+'\n')
    print(json.dumps(dict(edits=len(ledger),audit_sha256=sha(audit_path),new_paper=paper)))


if __name__=='__main__':main()

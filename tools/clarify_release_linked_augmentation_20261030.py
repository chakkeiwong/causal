"""Explain the retained augmentation comparison without assuming dominance."""
from pathlib import Path
from collections import Counter
import hashlib,json,re,shutil
from release_candidate_20261029 import MATH
R=Path(__file__).resolve().parents[1];B=R/'docs/release/2026-10-29';O=B/'linked-history-review-081'
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def bind(p):return dict(path=str(p.relative_to(R)),sha256=hashlib.sha256(p.read_bytes()).hexdigest())

def main():
    ledger=json.loads((B/'edits.json').read_text());assert len(ledger)==220
    evidence=json.loads((O/'numerical-evidence.json').read_text());assert evidence['result']['status']=='pass'
    assert len(evidence['result']['augmentation_examples'])==2
    p=B/'source/docs/writing-repair/2026-10-29/src/ef0385a590696022.tex';old=p.read_text()
    anchor=r'''There is no unconditional theorem that either has lower variance for every
possible outcome law.'''
    after=anchor+r'''

The variance comparison follows from the audit randomization. Write
$f_t=w'F_t$ and $b_t=w'B_t$ for the focal and candidate-average monetary
outcomes before taking the action score. Conditional on the complete history,
the two scalar pseudo-outcomes have the same mean and audit variances
\begin{equation}\label{rel81:audit-augmentation}
 \operatorname{Var}(w'Z_t\mid\mathcal H)
   =(q_t^{-1}-1)(f_t-b_t)^2,\qquad
 \operatorname{Var}(w'Z_t^I\mid\mathcal H)
   =(q_t^{-1}-1)f_t^2.
\end{equation}
For an incomplete audit, augmentation reduces this conditional contribution
exactly when the candidate average is closer to the focal outcome than zero
is. Multiplying by the squared oracle action-score coefficient and averaging
gives the corresponding comparison of added audit variance. Both constructions
retain the same latent focal score; estimated nuisance functions introduce
further finite-sample differences, so this calculation does not order every
fitted interval.

For a dimensionless illustration, stipulate a focal monetary outcome of two
and audit probability one quarter. A candidate average of 1.25 gives audit
variance 1.6875, compared with 12 under pure inverse weighting. If the candidate
average is instead five, the augmented variance is 27 and exceeds 12. These
values illustrate the conditional identity, not a new empirical funding case.
With complete auditing both additional variances vanish. The candidate average
can therefore be useful information without being a uniformly beneficial
augmentation under every outcome law.
'''
    assert old.count(anchor)==1;shutil.copy2(p,O/'before-chapter094.tex')
    save(O/'source-scope.json',dict(support_class='PROJECT_DERIVATION',new_citations=False,
        inspected_context='Existing chapter94 pseudo-outcome, conditional audit law and oracle influence decomposition.',
        supported_claims=['Conditional Bernoulli variance gives the two displayed audit contributions.','A common conditional mean permits a total-variance comparison; the outcome baseline must approximate the focal outcome better than zero.','Stipulated finite examples reverse the variance ordering without altering the retained study.'],
        inherited_scope='Existing DML and Newey–West source roles are unchanged; no source is credited with a new dependent theorem.',witness=bind(O/'numerical-evidence.json')))
    ledger.append(dict(file=str(p.relative_to(R)),before=anchor,after=after,
        reason='Explain why candidate-average augmentation often helps and why the saved narrowing is not a universal theorem.',
        substantive_destination='Every original sentence and mathematical expression remains. The new conditional-variance derivation and explicit reversal example explain the existing qualification; all4800 requests and adverse findings are unchanged.'))
    count=lambda text:Counter(re.sub(r'\s+',' ',m[0])for m in MATH.finditer(text))
    reviews=json.loads((B/'mathematical-addition-reviews.json').read_text());reviews['reviews'].append(dict(
        scope='Additive conditional audit-variance comparison and stipulated reversal example.',
        edits=[dict(edit=221,file=str(p.relative_to(R)),before_sha256=hashlib.sha256(anchor.encode()).hexdigest(),after_sha256=hashlib.sha256(after.encode()).hexdigest())],
        allowed_added=dict(count(after)-count(anchor)),allowed_removed={},status='reviewed_additions_only',
        derivation='Conditional on complete history, R/q has variance(1-q)/q. Both pseudo-outcomes have focal conditional mean. Their added audit variances differ by(1/q-1)(b^2-2fb), or the same expression times the squared oracle score coefficient. At f=2,q=.25, b=1.25 gives1.6875 versus12; b=5 gives27 versus12.',
        reviewed_assumptions=['Truthful known positive inclusion and complete-history conditioning; audit outcomes fixed conditionally.','Comparison concerns added audit variance, not finite fitted nuisance errors or every reported interval.','Examples are dimensionless stipulated algebra; no new observations or price assumptions.'],
        witness=bind(O/'numerical-evidence.json'),source_audit=bind(O/'source-scope.json'),fresh_visual_acceptance=False,independent_acceptance=False))
    p.write_text(old.replace(anchor,after,1));save(B/'edits.json',ledger);save(B/'mathematical-addition-reviews.json',reviews)
    save(O/'integration.json',dict(status='written_pending_build_review',edits=[221],inherited_material_removed='none',retained_requests=4800,new_empirical_results=False))
    print('Applied additive edit221; conditional augmentation variance explained.')

if __name__=='__main__':main()

"""Expose the projection calculation and a covariance counterexample."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import re
import shutil

from release_candidate_20261029 import MATH

R = Path(__file__).resolve().parents[1]
B = R / 'docs/release/2026-10-29'
O = B / 'projection-review-080'


def save(p, x):
    p.write_text(json.dumps(x, indent=2) + '\n')


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ledger = json.loads((B / 'edits.json').read_text())
    assert len(ledger) == 217
    evidence = json.loads((O / 'numerical-evidence.json').read_text())
    assert evidence['result']['status'] == 'pass'
    assert evidence['result']['independent_projected_sets'] == 10200
    patches = []
    target = B / 'source/docs/writing-repair/2026-10-29/src/92c294197eb52e9f.tex'
    anchor = r'''On the event that all six primitive intervals cover their truths, $V\in
\mathcal V$ regardless of the rank of the audit matrix.'''
    addition = r'''The projection can be computed without a grid over audit probabilities.
For one stratum, write $u=\mu_{s1}$, $v=\mu_{s2}$ and $r=2p_s-1$.
The inverse becomes
\begin{equation}\label{rel80:projection-corners}
 \theta_s=\frac{u+v}{2}+\frac{u-v}{2r},\qquad
 \frac{\partial\theta_s}{\partial r}=-\frac{u-v}{2r^2}.
\end{equation}
For a fixed nonzero rank, the inverse is linear in the two candidate
responses, so its minimum and maximum over their rectangle occur at corners.
For each corner, the derivative has a fixed sign on either side of zero.
Thus the extrema on a rank-sign branch occur at its endpoints or at its
one-sided limit at zero. Each branch is connected and the inverse is
continuous there; its image is an interval. The union of the two branch
images can remain disconnected. Combining stratum intervals requires all
pairwise sums, followed by merging overlaps; replacing disconnected pieces
by their convex hull would report a different set.

If the audit interval contains rank zero and the two candidate bands overlap,
their common value is compatible with equal observed responses. The focal
response can then be any real number, with the unrestricted companion
response adjusting to preserve their sum. This makes the stratum projection
the whole line. If the bands do not overlap, rank zero itself is incompatible;
the images on either side can instead be two unbounded components. An audit
region consisting only of rank zero with incompatible response bands has an
empty image. These cases explain why a nearly singular inverse cannot be
replaced by a large but finite interval: the topology and the financial
meaning of the result can change.

'''
    patches.append((target, anchor, addition + anchor,
        'Develop the exact projection calculation and its singular cases for the reader.',
        'The original inverse, set definition, coverage argument and all study results remain verbatim. Added algebra explains corners, rank-sign branches, disconnected sums, whole-line compatibility and empty images.'))
    target = B / 'source/docs/writing-repair/2026-10-29/src/0cff1da10e2094f3.tex'
    anchor = '''The normal/dependent-calendar bands inherit the conditional growing-pilot
rate and score assumptions from the preserved monograph.'''
    addition = r'''The covariance gain and its limit can be seen directly. If the candidate
slope covariance in one stratum has diagonal entries $v_1,v_2$ and
off-diagonal entry $c$, the transformed variances are
\begin{equation}\label{rel80:transformed-covariance}
 \operatorname{Var}(\widehat A_s)=\frac{v_1+v_2+2c}{4},\qquad
 \operatorname{Var}(\widehat D_s)=\frac{v_1+v_2-2c}{4}.
\end{equation}
Positive shared noise therefore increases uncertainty about the average but
reduces uncertainty about the difference. Near rank zero the inverse magnifies
the difference, so that reduction can matter greatly. Negative covariance
reverses this allocation. Separate marginal bands do not retain all the
information in a joint confidence region even after transformation.

A dimensionless covariance illustration makes the lack of width dominance
explicit. Suppose the two candidate variances are one, their correlation is
$c=0.9$, and the audit probability is known to be $p_s=3/4$. These are
stipulated values for an algebraic comparison, not estimates from the funding
experiment. With the same normal critical value $z$, candidate-coordinate
bands give a projected half-width $2z$. Transformed bands give
$z(\sqrt{0.95}+2\sqrt{0.05})\simeq1.422z$, since the focal response is the
average plus twice the difference. If the correlation is instead $c=-0.9$,
the transformed half-width is
$z(\sqrt{0.05}+2\sqrt{0.95})\simeq2.173z$, wider than the candidate result.
Both covariance matrices are positive definite. The observed narrowing in
the registered study is consequently a property of those paired requests,
not a consequence of the coordinate change alone. Audit uncertainty adds
another projection step and cannot restore a universal width ordering.

'''
    patches.append((target, anchor, addition + anchor,
        'Explain the covariance mechanism and provide a concrete width-order reversal.',
        'All original assumptions, failed-run evidence, registered results and observational-equivalence proof remain. The added explicitly stipulated covariance example shows why the observed narrowing cannot support a universal theorem.'))
    reviews = json.loads((B / 'mathematical-addition-reviews.json').read_text())
    occurrence = lambda text: Counter(re.sub(r'\s+', ' ', m[0]) for m in MATH.finditer(text))
    additions = Counter(); records = []
    for target, before, after, reason, destination in patches:
        old = target.read_text(); assert old.count(before) == 1
        shutil.copy2(target, O / ('before-' + target.name))
        assert not occurrence(before) - occurrence(after)
        additions.update(occurrence(after)-occurrence(before))
        ledger.append(dict(file=str(target.relative_to(R)), before=before, after=after,
                           reason=reason, substantive_destination=destination))
        records.append(dict(edit=len(ledger), file=str(target.relative_to(R)),
                            before_sha256=hashlib.sha256(before.encode()).hexdigest(),
                            after_sha256=hashlib.sha256(after.encode()).hexdigest()))
        target.write_text(old.replace(before, after, 1))
    save(O / 'source-scope.json', dict(
        support_class='PROJECT_DERIVATION', new_citations=False,
        inspected_contexts=['Chapter92 existing mixture and inverse equations; four response bands and two audit bands.',
                            'Chapter93 existing half-sum/half-difference transform and non-nesting qualification.'],
        supported_claims=['Corner extrema and rank-sign limits follow algebraically from the displayed inverse.',
                          'Covariance formulas follow by bilinear expansion; the two examples are stipulated counterexamples to universal width dominance.'],
        inherited_source_scope='The unchanged DML and Newey–West citations retain their existing attributed score/rate and Bartlett-covariance scope; neither is credited with proving these project projection constructions.',
        witness=dict(path=str((O/'numerical-evidence.json').relative_to(R)), sha256=sha(O/'numerical-evidence.json'))))
    reviews['reviews'].append(dict(
        scope='Additive projection geometry and covariance explanation in chapters92/93.',
        edits=records, allowed_added=dict(additions), allowed_removed={}, status='reviewed_additions_only',
        derivation='The inverse is affine in candidate means at fixed nonzero rank, and each corner has derivative -(u-v)/(2r^2). Branchwise continuity gives interval images and endpoint/singular limits. Compatible zero rank permits any focal value through the unrestricted companion. Covariance transformation gives (v1+v2±2c)/4. Known p=3/4 gives candidate half-width2z, versus approximately1.421893z at c=.9 and2.172966z at c=-.9; covariance eigenvalues are.1 and1.9.',
        reviewed_assumptions=['Closed candidate response and audit intervals; companion unrestricted; both rank signs retained.',
                              'Stipulated positive-definite covariance examples with known audit probability and common critical value, not empirical funding results.',
                              'Existing normal dependent-score approximation and pointwise assumptions remain; no finite-sample or uniform claim added.'],
        witness=dict(path=str((O/'numerical-evidence.json').relative_to(R)), sha256=sha(O/'numerical-evidence.json')),
        source_audit=dict(path=str((O/'source-scope.json').relative_to(R)), sha256=sha(O/'source-scope.json')),
        fresh_visual_acceptance=False, independent_acceptance=False))
    save(B / 'edits.json', ledger)
    save(B / 'mathematical-addition-reviews.json', reviews)
    save(O / 'integration.json', dict(status='written_pending_build_review', edits=[218, 219],
        inherited_material_removed='none', mathematical_additions=len(additions), new_empirical_results=False,
        checker_repair='Initial reconstruction passed all assertions but report serialization found NumPy integer counts. Explicit int conversion repaired serialization; first failure log retained.'))
    print('Applied additive edits218/219; projection geometry and width reversal explained.')


if __name__ == '__main__':
    main()

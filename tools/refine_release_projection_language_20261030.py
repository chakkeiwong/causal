"""Distinguish determinant zero from matrix rank while preserving the cases."""
from pathlib import Path
import json
import shutil

R=Path(__file__).resolve().parents[1]
B=R/'docs/release/2026-10-29'
O=B/'projection-review-080'


def main():
    ledger=json.loads((B/'edits.json').read_text()); assert len(ledger)==219
    p=B/'source/docs/writing-repair/2026-10-29/src/92c294197eb52e9f.tex'
    old=p.read_text()
    before=r'''For a fixed nonzero rank, the inverse is linear in the two candidate
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
meaning of the result can change.'''
    after=r'''Here the denominator parameter is the mixing matrix's determinant; zero
determinant means matrix rank one. At any nonzero determinant, the inverse
is linear in the candidate responses, so its extrema occur at rectangle
corners. Each corner's derivative has a fixed sign on either side of zero;
its extrema therefore occur at branch endpoints or one-sided zero limits.
Continuity on each connected branch gives an interval image, although the
union can be disconnected. Combine stratum images by all pairwise interval
sums and merge overlaps; taking a convex hull would fill unsupported gaps.

If the audit interval contains one half and the candidate bands overlap,
equal observed responses are compatible with a rank-one matrix. Any focal
response is then possible: the unrestricted companion adjusts to preserve
their sum. The projection is the whole line. Nonoverlapping bands exclude
that singular case and can produce two unbounded components, one from each
side of the singularity. If the audit region consists only of one half,
nonoverlapping bands give an empty image. Substituting a large finite
interval would change both the set and its financial meaning.'''
    assert old.count(before)==1;shutil.copy2(p,O/'before-edit220.tex')
    p.write_text(old.replace(before,after,1))
    ledger.append(dict(file=str(p.relative_to(R)),before=before,after=after,
        reason='Correct determinant-versus-matrix-rank terminology and tighten the added geometric explanation.',
        substantive_destination='All mathematical expressions remain untouched. Corner extrema, derivative sign, branch continuity, disconnected images, interval sums, unsupported convex-hull gaps, compatible rank-one whole-line sets and incompatible empty cases all remain explicit.'))
    (B/'edits.json').write_text(json.dumps(ledger,indent=2)+'\n')
    x=json.loads((O/'integration.json').read_text());x['edits'].append(220)
    x['rendered_finding']='Batch074 rendered review found imprecise rank-zero terminology in the added prose. Edit220 names zero determinant and rank-one matrix correctly; every case and equation survives.'
    (O/'integration.json').write_text(json.dumps(x,indent=2)+'\n')
    print('Applied edit220; determinant and matrix rank distinguished.')


if __name__=='__main__':main()

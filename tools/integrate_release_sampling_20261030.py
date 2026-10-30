"""Preserve and integrate completed sampling evidence into the release argument."""
from pathlib import Path
from collections import Counter
import hashlib,json,re,shutil

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/release/2026-10-29'
OUT=BASE/'sampling-integration-068'
STUDY=ROOT/'docs/twelve-hour-closure/2026-10-29'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(p):return dict(path=str(p.relative_to(ROOT)),sha256=sha(p))
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def main():
    ledger=json.loads((BASE/'edits.json').read_text());assert len(ledger)==183
    witness=json.loads((OUT/'exact-witnesses.json').read_text());assert witness['status']=='pass'
    source=STUDY/'discovery-sampling.tex';text=source.read_text()
    text=text.replace(r'\section{',r'\subsection{').replace(r'\chapter{',r'\section{')
    text=text.replace('The complete short-study table retains both thresholds;',
                      'The complete comparison below retains both thresholds;')
    table=(STUDY/'sampling-complete-table.tex').read_text()
    follow=json.loads((STUDY/'discovery-timing-attempt-1/results.json').read_text())
    rows=[r'\begin{longtable}{llrrrrrr}',r'\toprule',
          r'Mechanism & Search & $n$ & $\alpha$ & Wrong & Unfinished & Coverage & Change\\',
          r'\midrule\endhead']
    for row in follow['summaries']:
        rows.append(f"{row['mechanism']} & {row['method']} & {row['n']} & {row['alpha']:.2f} & {row['wrong_skeleton']} & {row['incomplete']} & {100*row['coverage']:.1f}"+r'\% & '+f"{100*row['coverage_paired_difference']:+.1f}"+r'\\')
    rows.append(r'\bottomrule\end{longtable}')
    text+=r'''
\subsection{Complete method and threshold comparisons}

The following tables retain every declared comparison. Strong and weak denote
the larger- and smaller-coefficient mechanisms above; cancellation denotes
the explicitly unfaithful mechanism. Full, screen and depth2 mean full stable
subsets, the all-neighbour screen and the depth-two cap. Each row contains
200 samples. Wrong and unfinished are counts, whereas coverage is the
percentage of ordinary selected-regression intervals containing the stipulated
effect. Equal coverage can coexist with different graph errors when the
errors leave the selected baseline controls unchanged.

\begingroup\small
'''+table+r'''
\endgroup

The timing follow-up omits the later descendant from discovery. Its final
column is the paired change in coverage, in percentage points, relative to
the corresponding first-study row. The graph-error columns concern the reduced
five-variable task and therefore have a different graph target from the first
table. This follow-up was specified after the first study; the comparison
does not acquire a prospective status retrospectively.

\begingroup\small
'''+ '\n'.join(rows)+r'''
\endgroup

The next chapter asks a prior question for any such search: whether recorded
variables and customer identities faithfully represent the economic observations
whose relationships are being learned.
'''
    target=BASE/'source/docs/discovery-repair/2026-10-29/chapter.tex'
    before=' The next chapter asks a prior question for any such search: whether the recorded variables and customer identities faithfully represent the economic observations whose relationships are being learned.'
    original=target.read_text();assert original.count(before)==1
    after=' The following sampling comparison addresses one of these separate questions.\n\n'+text
    shutil.copy2(target,OUT/'before-discovery.tex')
    audit=json.loads((STUDY/'sampling-source-support.json').read_text())
    audit['release_reinspection']={
        'scope':'Kalisch equation3/A1-A4/Theorem1 and Colombo Algorithm4.1/Theorems2-3 read in primary extracted texts; exact rational population and retained sample accounting independently reconstructed.',
        'inspected_primary_extracts':[bind(OUT/'kalisch.txt'),bind(OUT/'colombo.txt')],
        'original_scientific_treatment':bind(source),'witness':bind(OUT/'exact-witnesses.json'),
        'cutoff':'2026-10-07','new_experiment':False,'independent_acceptance':False}
    save(OUT/'source-audit.json',audit)
    figure=STUDY/'sampling-figures/coverage.pdf'
    dest=BASE/'source/docs/twelve-hour-closure/2026-10-29/sampling-figures/coverage.pdf'
    dest.parent.mkdir(parents=True,exist_ok=True);assert not dest.exists()
    shutil.copy2(figure,dest)
    additions=json.loads((BASE/'additions.json').read_text())
    additions.append(dict(path=str(dest.relative_to(ROOT)),original=str(figure.relative_to(ROOT)),sha256=sha(figure),reason='Preserve the original sampling-coverage figure accompanying the integrated study.',source_audit=str((OUT/'source-audit.json').relative_to(ROOT))))
    ledger.append(dict(file=str(target.relative_to(ROOT)),before=before,after=after,
        reason='Integrate completed finite-sample discovery and information-clock follow-up, with all90 result cells and exact original figure.',
        substantive_destination='Existing exact-oracle treatment remains complete. Its final observation bridge moves after the new sampling treatment; all prior scientific content and negative findings survive.'))
    from release_candidate_20261029 import MATH
    counts=lambda s:Counter(re.sub(r'\s+',' ',m[0]) for m in MATH.finditer(s))
    assert not counts(before)-counts(after)
    review=json.loads((BASE/'mathematical-addition-reviews.json').read_text())
    review['reviews'].append(dict(scope='Exact additive sampling study, rational population laws and retained90-cell comparison.',
        edits=[dict(edit=184,file=str(target.relative_to(ROOT)),before_sha256=hashlib.sha256(before.encode()).hexdigest(),after_sha256=hashlib.sha256(after.encode()).hexdigest())],
        allowed_added=dict(counts(after)-counts(before)),allowed_removed={},status='reviewed_additions_only',
        derivation='Linear independent-normal SEM gives Cov(X,Y)=(133/50)s^2 and Var(X)=1+(77/25)s^2. Partialling all baseline causes gives zero; also conditioning on their collider gives-33/68. Exact cancellation gives effect1 and observational slope1/2. Fisher transformation follows the inspected primary equation. Independent rational conditioning and ancestral moralization verify480 faithfulness queries;18000 retained search records reconstruct90 cells and paired differences.',
        reviewed_assumptions=['IID Gaussian stipulated mechanisms; known unit noise and fixed structural coefficients.','Common estimated baseline neighbors are a naive diagnostic rule, not general adjustment or IDA.','Fixed significance thresholds give no graph confidence. The timing follow-up was specified after initial results.','Wilson intervals describe independent Monte Carlo draws, not population-of-banks uncertainty. Native packages, orientations, hidden confounding and actual banking effects are untested.'],
        witness=bind(OUT/'exact-witnesses.json'),source_audit=bind(OUT/'source-audit.json'),fresh_visual_acceptance=False,independent_acceptance=False))
    target.write_text(original.replace(before,after,1));save(BASE/'edits.json',ledger)
    save(BASE/'additions.json',additions);save(BASE/'mathematical-addition-reviews.json',review)
    verifier=ROOT/'tools/release_source_verification_20261029.py';v=verifier.read_text()
    anchor=" 'docs/release/2026-10-29/text-signals-066/source-audit.json']"
    assert v.count(anchor)==1
    verifier.write_text(v.replace(anchor," 'docs/release/2026-10-29/text-signals-066/source-audit.json',\n 'docs/release/2026-10-29/sampling-integration-068/source-audit.json']"))
    save(OUT/'integration.json',dict(status='written_pending_build_and_review',edit=184,source=bind(source),target=bind(target),figure=bind(dest),source_audit=bind(OUT/'source-audit.json'),witness=bind(OUT/'exact-witnesses.json'),semantic_deletion='Only the prior chapter-transition sentence moves; its complete meaning is retained at the end of the added treatment.'))
    print(json.dumps(dict(edit=184,initial_cells=54,timing_cells=36,status='written')))
if __name__=='__main__':main()

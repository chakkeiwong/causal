"""Add the preserved missing-history study, with checked rounding and sources."""
from pathlib import Path
from collections import Counter
import hashlib,json,re,shutil
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/release/2026-10-29'
OUT=BASE/'outcome-integration-070'
STUDY=ROOT/'docs/twelve-hour-closure/2026-10-29'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(p):return dict(path=str(p.relative_to(ROOT)),sha256=sha(p))
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def main():
    ledger=json.loads((BASE/'edits.json').read_text());assert len(ledger)==186
    witness=json.loads((OUT/'exact-witnesses.json').read_text());assert witness['status']=='pass'
    source=STUDY/'outcome-audit.tex';text=source.read_text()
    text=re.sub(r'\\ifdefined\\OutcomeAuditIntegrated\n(.*?)\\else\n.*?\\fi\n',r'\1',text,flags=re.S)
    text=text.replace(r'\section{',r'\subsection{').replace(r'\chapter{',r'\section{')
    corrections=[
        ('Random recovery, 25\\% & -0.051 &','Random recovery, 25\\% & -0.052 &','Exact retained bias=-0.051514 rounds to-0.052.'),
        ('Assumed $g_t$, assisted & 0.926 & 0.590 & 2.195 &','Assumed $g_t$, assisted & 0.925 & 0.590 & 2.194 &','Retained bias=.925479 and width2.194495 round to.925 and2.194.'),
        ('5\\% recovery, assisted & 0.082 & 0.958 & 4.770 &','5\\% recovery, assisted & 0.082 & 0.958 & 4.769 &','Retained width4.769494 rounds to4.769.'),
        ('standard error 0.063. Coverage','standard error 0.0625. Coverage','Retained selective-recovery bias MCSE=.062450; show four decimals.'),
        ('dangerous result: bias 0.926 and coverage','dangerous result: bias 0.925 and coverage','Use the same correctly rounded assisted-routine bias as its table.')]
    for before,after,reason in corrections:
        assert text.count(before)==1,(before,text.count(before));text=text.replace(before,after,1)
    tail='sampling argument and measurement evidence.\n'
    target=BASE/'source/docs/writing-repair/2026-10-29/src/1de93e537048440f.tex'
    original=target.read_text();assert original.count(tail)==1
    after=tail+'\n'+text
    shutil.copy2(target,OUT/'before-policy.tex')
    raw_audit=json.loads((STUDY/'outcome-source-support.json').read_text())
    sources=[];reinspected=[]
    urls={'levis2023double':'https://arxiv.org/abs/2204.02432v2','sun2025double':'https://arxiv.org/abs/2310.09239v3','jiang2016':'https://proceedings.mlr.press/v48/jiang16.html'}
    for row in raw_audit['sources']:
        record=dict(citation_key=row['id'],kind='paper',title=row['title'],authors=row['authors'],source_identity=urls[row['id']],version_date=row['version'],local_copy=row['artifact'],inspected_anchors=row['inspected'],supported_claims=row['allowed'],scope=row['forbidden'],version_warning=row.get('version_warning'),primary_extract=bind(OUT/(row['id']+'.txt')))
        (reinspected if row['id']=='jiang2016' else sources).append(record)
    source_audit=dict(cutoff='2026-10-07',sources=sources,reinspected_inherited_sources=reinspected,original_audit=bind(STUDY/'outcome-source-support.json'),original_treatment=bind(source),witness=bind(OUT/'exact-witnesses.json'),proof=bind(STUDY/'outcome-crossfit-derivation.md'),scope='Primary method support and author-derived known-design composition; no efficiency claim, bank recovery validation or general cross-fit qualification.')
    save(OUT/'source-audit.json',source_audit)
    ledger.append(dict(file=str(target.relative_to(ROOT)),before=tail,after=after,reason='Integrate completed missing-history recovery, independent-pilot and equal-resource studies, preserving all adverse findings and mathematical conditions.',substantive_destination='All prior chapter14 source survives verbatim. New section develops the previously proposed outcome-audit response and retains its full theory, experiments, costs and limits. Five imported decimal transcriptions are corrected against retained records and documented separately.'))
    refs=BASE/'source/docs/writing-repair/2026-10-29/references-0.bib'
    reftext=refs.read_text();anchor=reftext[-250:];assert reftext.count(anchor)==1
    newrefs=(STUDY/'outcome-refs.bib').read_text();assert 'levis2023double' not in reftext and 'sun2025double' not in reftext
    ledger.append(dict(file=str(refs.relative_to(ROOT)),before=anchor,after=anchor+'\n'+newrefs,reason='Add authentic version-specific Levis and Sun primary bibliography records.',substantive_destination='All existing bibliography entries retained; only two explicitly inspected originals added.'))
    additions=json.loads((BASE/'additions.json').read_text())
    for name in ['precision.pdf','bias-coverage.pdf']:
        figure=STUDY/'outcome-figures'/name;dest=BASE/'source/docs/twelve-hour-closure/2026-10-29/outcome-figures'/name
        dest.parent.mkdir(parents=True,exist_ok=True);assert not dest.exists();shutil.copy2(figure,dest)
        additions.append(dict(path=str(dest.relative_to(ROOT)),original=str(figure.relative_to(ROOT)),sha256=sha(figure),reason='Preserve exact original outcome-recovery study figure.',source_audit=str((OUT/'source-audit.json').relative_to(ROOT))))
    from release_candidate_20261029 import MATH
    counts=lambda s:Counter(re.sub(r'\s+',' ',m[0]) for m in MATH.finditer(s))
    review=json.loads((BASE/'mathematical-addition-reviews.json').read_text())
    review['reviews'].append(dict(scope='Additive random-recovery and known-design sequential-score derivation with complete study accounting.',edits=[dict(edit=187,file=str(target.relative_to(ROOT)),before_sha256=hashlib.sha256(tail.encode()).hexdigest(),after_sha256=hashlib.sha256(after.encode()).hexdigest())],allowed_added=dict(counts(after)-counts(tail)),allowed_removed={},status='reviewed_additions_only',derivation='Condition on complete history: E(B/q)=1 gives E(K+BM/q)=E(F); conditional error variance is(q^-1-1)M^2. Known action weights telescope for any independent fixed outcome regressions. With fixed cross-fit folds and score L2 consistency to a deterministic limit, conditional Chebyshev makes each centered fold remainder negligible; pooled squared differences vanish by conditional Markov and Cauchy-Schwarz. Cost derivative is A*r*cA-BM*c0/q^2, giving the stated interior square-root allocation only when A>0; nonpositiveA favors full recovery. Conditional residual allocation follows Lagrange differentiation.',reviewed_assumptions=['IID customers, fixed policies, fixed horizon, known positive treatment/recovery probabilities and truthful complete histories.','Successful completion rather than invitation must be noninformative conditional on design information. Selective-completion counterexample remains.','Independent pilot or held-out cross-fit evaluation, square-integrable regressions and common deterministic L2 score limit. Gaussian finite-dimensional basis has finite moments and nonsingular population Gram matrices.','Normal interval coverage is empirical/asymptotic; numerical-reference uncertainty is separate. Equal collection resources do not price compute/administration. Allocation derivation is not a tested optimal bank design.'],witness=bind(OUT/'exact-witnesses.json'),source_audit=bind(OUT/'source-audit.json'),fresh_visual_acceptance=False,independent_acceptance=False))
    target.write_text(original.replace(tail,after,1));refs.write_text(reftext.replace(anchor,anchor+'\n'+newrefs,1))
    save(BASE/'edits.json',ledger);save(BASE/'additions.json',additions);save(BASE/'mathematical-addition-reviews.json',review)
    verifier=ROOT/'tools/release_source_verification_20261029.py';v=verifier.read_text();anchor=" 'docs/release/2026-10-29/sampling-integration-068/source-audit.json']";assert v.count(anchor)==1
    verifier.write_text(v.replace(anchor," 'docs/release/2026-10-29/sampling-integration-068/source-audit.json',\n 'docs/release/2026-10-29/outcome-integration-070/source-audit.json']"))
    save(OUT/'integration.json',dict(status='written_pending_build_review',edits=[187,188],target=bind(target),imported_original=bind(source),source_audit=bind(OUT/'source-audit.json'),witness=bind(OUT/'exact-witnesses.json'),corrections=[dict(before=a,after=z,reason=r) for a,z,r in corrections],deleted_inherited_material='none',new_study=False))
    print(json.dumps(dict(edits=[187,188],replication_rows=67500,rounding_corrections=len(corrections))))
if __name__=='__main__':main()

"""One-shot, preserving integration of inspected text-method originals."""
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/release/2026-10-29'
OUT = BASE / 'text-signals-066'
SOURCE = BASE / 'source/docs/writing-repair/2026-10-29'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def binding(p):
    return dict(path=str(p.relative_to(ROOT)), sha256=sha(p))


def save(p, value):
    p.write_text(json.dumps(value, indent=2)+chr(10))


def main():
    ledger = json.loads((BASE/'edits.json').read_text())
    assert len(ledger) == 168
    acquired = ROOT/'docs/twelve-hour-closure/2026-10-29/text-source-support.json'
    shutil.copy2(acquired, OUT/'inherited-acquisition.json')
    inherited = json.loads(acquired.read_text())
    anchors = {
        'inferbert': ['PDF1,3–10: identity; commercial cohort construction and label definitions;64:16:20 split;equations2–6 and Algorithm1;reported adjusted tests, term overlap and limitations.', 'Selected pinned causal_inference.py,lines1–250: saved predictions, membership partitions, support threshold, sample variance and unadjusted one-sided filtering.'],
        'deepcausality': ['PDF1–11, especially4–9: classifier/NER and group-membership algorithm; drug-level labels copied to sentences;90:10sentence split; test-based checkpoint selection;18/20clinical relevance and175case stratification.', 'PDF11 explicitly cannot distinguish confounders/colliders. Complete pinned scoring notebook source cell0 inspected; filter lines commented out.'],
        'pharma': ['PDF1–10, printed1908–1917: cohort definitions, task metrics and model comparisons;PPR formula on1911;expert term relevance and textual PPV .95/.20/.25 on1916;method references9/10 versus actual InferBERT/DeepCausality entries17/18 on1917.'],
        'veitch': ['PDF1–7, printed919–925: text-sufficiency assumption,ATT definition and equations2.1–2.3;equation3.1;Theorems3.1–3.2 and overlap/consistency qualifications;semi-synthetic construction and omitted-confounding experiment.', 'Theorem3.1 final expectation and equation3.1 omit treated conditioning/weights present in2.1–2.3. No separate appendix proof is included in this ten-page proceedings original.']}
    claims = {
        'inferbert': ['Observed term-group comparisons of saved classifier probabilities do not by themselves identify an intervention contrast.', 'Reported study uses commercial curation and structured-to-sentence transformation; no independent reconstruction of those experiments.'],
        'deepcausality': ['Named-entity ranking, drug-level sentence labels and reported clinical relevance are distinct from effect identification.', 'Reported sentence split and test-based checkpoint selection do not establish untouched drug-level evaluation.', 'Paper states confounder/collider limitation; no quantitative leakage penalty is asserted.'],
        'pharma': ['Model comparison concerns classifier outcomes and domain-expert relevance of enriched terms, not intervention-effect error or coverage.', 'Published method-reference mismatch and explicit narrative PPV identities are preserved.'],
        'veitch': ['Compression can preserve adjustment information under original sufficiency and stated representation/estimation assumptions.', 'ATT requires a treated-population averaging law; displayed formula inconsistency is retained, not silently repaired as a source theorem.', 'Semi-synthetic evidence and strong original-text sufficiency are separate from bank validity.']}
    receipts = {'inferbert':'closure30_inferbert_pdf.receipt.json', 'deepcausality':'closure30_deepcausality_pdf.receipt.json', 'pharma':'closure30_pharma_new_pdf.receipt.json', 'veitch':'closure30_veitch_pdf.receipt.json'}
    records = []
    for name in anchors:
        old = next(r for r in inherited['sources'] if r['name']==name)
        p = ROOT/old['local_copy']['path']
        assert sha(p)==old['local_copy']['sha256'] and p.read_bytes().startswith(b'%PDF-')
        receipt = ROOT/'docs/literature/raw'/receipts[name]
        identity = ('https://doi.org/'+old['doi']) if old.get('doi') else json.loads(receipt.read_text())['url']
        records.append(dict(citation_key='rel66'+name,kind='paper',source_identity=identity,
            version_date=old['version_date']+'; inspected29October2026UTC; client cutoff7October2026.',
            local_bindings=[binding(p),binding(OUT/(name+'.txt')),binding(receipt)],
            inspected_anchors=anchors[name],supported_claims=claims[name],
            limitations=['Independent release-specific primary-text reading; acquisition from another campaign only.', 'No fresh visual inspection, source experiment replication, live-model performance or bank acceptance.', 'Bounded version-specific comparison; no exhaustive correction/retraction clearance.']))
    for name, indices in [('inferbert',[0,2]),('deepcausality',[1])]:
        old=next(r for r in inherited['software'] if r['citation_key']=='closure30'+name+'code')
        files=[]
        for i in indices:
            p=ROOT/f'docs/literature/raw/closure30_{name}_code_{i}.txt'
            wanted=next(r for r in old['files'] if r['path']==str(p.relative_to(ROOT)))
            assert sha(p)==wanted['sha256']
            files += [binding(p),binding(p.with_suffix('.receipt.json'))]
        if name=='deepcausality': files.append(binding(OUT/'deepcausality-notebook-source.txt'))
        records.append(dict(citation_key='rel66'+name+'code',kind='software',source_identity=old['repository'],
            version_date=old['commit']+'; '+old['commit_date']+'; retrieved29October2026UTC; before client cutoff.',
            local_bindings=files,inspected_anchors=anchors[name][-1:] if name=='inferbert' else ['Complete243-line extracted notebook source; cell0 partition, mean/variance score, commented significance filter and caller.'],
            supported_claims=['Static saved-prediction membership comparison; exact visible significance handling only.'],
            limitations=['No downloaded code executed; complete upstream results and dependency/rights profile not qualified.']))
    save(OUT/'source-audit.json',dict(recorded_utc=datetime.now(timezone.utc).isoformat(),cutoff='2026-10-07',sources=records,
        inherited_acquisition=binding(OUT/'inherited-acquisition.json'),exact_derivation=binding(OUT/'exact-witnesses.json'),
        generator=binding(ROOT/'tools/release_text_signal_witnesses_20261029.py'),
        scope='Independent primary-method comparison and authored exact probability examples; no inherited acceptance or simulations.',
        search_limit='Built-in primary-source search returned no usable result this continuation; no search citation or coverage claim inferred.'))
    amendments=[]
    def edit(p,before,after,reason,destination):
        old=p.read_text();assert old.count(before)==1 and before!=after
        amendments.append((p,old,old.replace(before,after,1)))
        ledger.append(dict(file=str(p.relative_to(ROOT)),before=before,after=after,reason=reason,substantive_destination=destination))
    component=SOURCE/'src/ef6e4a66d3e6badf.tex'
    anchor=r'\subsection{Public complaints as a prototype resource}'
    edit(component,anchor,(OUT/'addition.tex').read_text()+chr(10)+anchor,
        'Develop the newly inspected text-signal methods and constructive embedding alternative, with explicit identification, score and target-weight distinctions.',
        'All prior linguistic measurement, perception-error derivations, public complaint study, longitudinal policy and component alternatives remain verbatim. Added exact examples make the monetary consequences reconstructible.')
    bib=SOURCE/'references-2.bib';before=bib.read_text()[bib.read_text().rindex('@'):]
    addition=(ROOT/'docs/twelve-hour-closure/2026-10-29/text-refs.bib').read_text().replace('closure30','rel66')
    assert len(re.findall(r'^@',addition,re.M))==6
    edit(bib,before,before+chr(10)+addition,'Add four genuine scholarly originals and two pinned software identities.', 'All existing bibliography identities preserved; additional citations bind actual primary readings.')
    assistance=SOURCE/'assistance.tex';before=assistance.read_text()[assistance.read_text().index('The end-to-end workflow in Section'):].rstrip()
    after=before.replace('The current inventory therefore contains','That comparison brought the inventory to')+r'''

The pharmacovigilance comparison in Section~\ref{rel66:text-signals}
adds one further inspected frontier original, bringing the inventory to
90 inspected entries, including the same explicit quarantine, and 23 unread.
Its enriched text terms are useful diagnostic candidates; their classifier
score differences do not identify a banking intervention. The primary
InferBERT and DeepCausality methods and the conditional text-embedding
alternative make the missing adjustment and population-weighting requirements
explicit. These additional supporting sources are not additional entries in
the fixed frontier denominator. \citep{rel66pharma,rel66inferbert,rel66deepcausality,rel66veitch}
'''
    edit(assistance,before,after,'Reconcile the primary text-method comparison and frontier disposition with the assistance recommendation.', 'Preserve prior recommendation, graph-confidence review, quarantine and historical counts; add exact new comparison and fixed-denominator distinction.')
    sponsor=SOURCE/'sponsor-body.tex'
    before='''exclusion bring the inventory to 89 inspected, including one explicit
quarantine, and 24 unread. The graph-confidence comparison does not establish
calibrated intervention intervals.'''
    after='''exclusion brought the inventory to 89 inspected, including one explicit
quarantine, and 24 unread. The graph-confidence comparison does not establish
calibrated intervention intervals. A further pharmacovigilance original brings
coverage to 90 inspected, including the same quarantine, and 23 unread.
Its term-relevance comparisons do not identify banking intervention effects;
text-based adjustment also requires sufficient information and the correct
target-population weights.'''
    edit(sponsor,before,after,'Align sponsor census and the text-method conclusion.', 'Preserve historical evidence and caveats; no new live-model or bank-performance assertion.')
    assert len(ledger)==172
    from release_candidate_20261029 import MATH
    occurrences=lambda s:Counter(re.sub(r'\s+',' ',m[0]) for m in MATH.finditer(s))
    e=ledger[168];before_math=occurrences(e['before']);after_math=occurrences(e['after'])
    assert not before_math-after_math
    reviews=json.loads((BASE/'mathematical-addition-reviews.json').read_text())
    reviews['reviews'].append(dict(scope='Exact additions for observational score contrasts, conditional adjustment and ATT/ATE weighting.',
        edits=[dict(edit=169,file=e['file'],before_sha256=hashlib.sha256(e['before'].encode()).hexdigest(),after_sha256=hashlib.sha256(e['after'].encode()).hexdigest())],
        allowed_added=dict(after_math-before_math),allowed_removed={},status='reviewed_additions_only',
        derivation='Finite eight-cell joint law gives observational0.36 but causal0; Bayes weighting gives ATT0.24 versus ATE0.15. Stipulated dollars use declared outcome value and action costs. Adjustment formulas require consistency, exchangeability, positivity and sufficient representation.',
        reviewed_assumptions=['Fixed score and nonempty term groups; no causal interpretation of membership partition without identification.', 'Independent structural uniforms and latent readiness generate first law; intervention leaves outcome equation unchanged.', 'Two observed strata with declared propensities and potential-outcome means define second law; target populations differ.', 'Published notation mismatch is explicitly distinguished from project derivation; no appendix proof claimed inspected.'],
        witness=binding(OUT/'exact-witnesses.json'),source_audit=binding(OUT/'source-audit.json'),fresh_visual_acceptance=False,independent_acceptance=False))
    for p,old,new in amendments:
        assert p.read_text()==old
        (OUT/('before-'+p.name)).write_text(old)
        p.write_text(new)
    save(BASE/'edits.json',ledger);save(BASE/'mathematical-addition-reviews.json',reviews)
    pending=dict(status='awaiting_build_and_context_review',edits=list(range(169,173)),previous_batch=54,source_audit=binding(OUT/'source-audit.json'))
    save(OUT/'integration.json',pending);print(json.dumps(pending))


if __name__=='__main__':
    main()

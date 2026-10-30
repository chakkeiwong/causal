"""Record demonstrated prose/formula-description repairs after rendered reading."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/release/2026-10-29'
OUT=BASE/'text-signals-066'


def main():
    ledger=json.loads((BASE/'edits.json').read_text());assert len(ledger)==172
    p=BASE/'source/docs/writing-repair/2026-10-29/src/ef6e4a66d3e6badf.tex'
    before=p.read_text();text=before
    changes=[
        (r'\citet{rel66inferbert} trains a classifier',r'The InferBERT study by \citet{rel66inferbert} trains a classifier','Resolve plural-author subject and singular study verb in rendered prose.'),
        (r'\citet{rel66deepcausality} extends this design',r'The DeepCausality study by \citet{rel66deepcausality} extends this design','Resolve plural-author subject and singular study verb in rendered prose.'),
        ('nonmissing fields and groups exceeding its support threshold. Its normal-score\ndenominator uses the sum of the two within-group sample variances divided by\ntheir respective counts.', 'nonmissing fields and groups meeting its minimum support threshold. Its\nnormal-score denominator is the square root of the sum of the two within-group\nsample variances divided by their respective counts.', 'State the inclusive support threshold and square-root denominator exactly as the inspected routine computes them.'),
        ('The source supplies two distinct kinds of evaluation. Its Amazon setting', r'Returning to the text-rewriting question, the study by \citet{exec28_lm_pryzant} supplies two distinct kinds of evaluation. Its Amazon setting', 'Restore an explicit source antecedent after inserting a different primary-method comparison.')]
    for old,new,reason in changes:
        assert text.count(old)==1
        ledger.append(dict(file=str(p.relative_to(ROOT)),before=old,after=new,reason=reason,substantive_destination='All mathematical expressions, reported findings, assumptions and alternatives remain; prose clarifies the existing operation or source identity.'))
        text=text.replace(old,new,1)
    (OUT/'before-prose-refinement.tex').write_text(before)
    p.write_text(text);(BASE/'edits.json').write_text(json.dumps(ledger,indent=2)+chr(10))
    print(json.dumps(dict(edits=list(range(173,177)),status='written_pending_rebuild')))


if __name__=='__main__':main()

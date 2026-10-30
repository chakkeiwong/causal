"""Ledger a connected conclusion while preserving every scientific condition."""
from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parents[1];B=R/'docs/release/2026-10-29';O=B/'graph-software-072'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2)+chr(10))
def main():
    p=B/'source/docs/writing-repair/2026-10-29/src/5e1bb6d4d921349d.tex'
    s=p.read_text();ledger=json.loads((B/'edits.json').read_text());assert len(ledger)==194
    shutil.copy2(p,O/'before-conclusion-refinement.tex')
    old='''The decision is consequently specific. Adopt the separation between
evidence retrieval, graph construction and intervention calculation.
Evaluate quotation and evidence-support checks for their own stated
predicates. Decline the direct conversion of an information ceiling into
calibrated edge probabilities, and decline unqualified confidence-interval
language for the spread of fitted-model effects. Before a prototype makes
stronger claims, it needs an authentic complete implementation, a declared
joint graph law or retention procedure, the relevant calibration evidence,
and public or synthetic experiments with known interventions and matched
information across comparators. Bank validation can follow when those
experiments justify its cost.'''
    new='''The software comparison reinforces the separation between evidence retrieval,
graph construction and intervention calculation. A quotation check can test
whether a cited passage supports a claim under a declared predicate without
establishing that claim's causal truth. Similarly, an information ceiling does
not supply calibrated edge probabilities, and the spread of fitted-model
effects does not acquire confidence-interval coverage from repetition alone.
A prototype could support stronger claims only with an authentic complete
implementation, a declared joint graph law or retention procedure, relevant
calibration evidence, and public or synthetic experiments with known
interventions and matched information across comparators. Those experiments
would determine whether the prospective gain warrants bank validation.'''
    assert s.count(old)==1
    ledger.append(dict(file=str(p.relative_to(R)),before=old,after=new,reason='Replace imperative adoption list with connected reasoning linking software scope to scientific requirements.',substantive_destination='All conditions survive in this paragraph: separated operations, declared checking predicate, error-bound direction, coverage qualification, complete implementation, graph law/retention, calibration, known interventions, matched information and justified bank-validation cost. The original monetary conclusion immediately follows.'))
    p.write_text(s.replace(old,new,1));save(B/'edits.json',ledger)
    q=B/'energy-integration-071/integration.json';x=json.loads(q.read_text());rp=R/x['review']['path'];before=x['review']['sha256'];x['review']['sha256']=sha(rp);save(q,x)
    save(O/'conclusion-refinement.json',dict(edit=195,important_material_removed=False,removed_form='Imperative adoption list; replaced by explanatory argument with all substantive conditions.',energy_review_pointer_repaired=before!=sha(rp),energy_review_sha256=sha(rp)))
    print(json.dumps(dict(edit=195,energy_pointer_repaired=before!=sha(rp))))
if __name__=='__main__':main()

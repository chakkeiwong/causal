"""Single-use primary GMM comparison; all inherited scientific text retained."""
from pathlib import Path
from collections import Counter
import hashlib,json,re,shutil
from release_candidate_20261029 import MATH
R=Path(__file__).resolve().parents[1];B=R/'docs/release/2026-10-29';O=B/'source-windmeijer-032'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(p):return dict(path=str(p.relative_to(R)),sha256=sha(p))
def main():
 ledger=json.loads((B/'edits.json').read_text());assert len(ledger)==117,'Single-use integration: do not repeat.'
 witness=O/'exact-witnesses.json';assert json.loads(witness.read_text())['status']=='pass'
 source=B/'source/docs/writing-repair/2026-10-29/src/cef8e4a7fc22ef80.tex';bib=B/'source/docs/writing-repair/2026-10-29/references-0.bib'
 anchor=r'\subsection{A paired comparison and a banking decision rule}';addition=(O/'addition.tex').read_text()+'\n';assert source.read_text().count(anchor)==1
 edit=dict(file=str(source.relative_to(R)),before=anchor,after=addition+anchor,reason='Develop the difference between two-stage weight estimation, nonzero moment residuals, corrected uncertainty and a causal target using the accessible primary follow-up.',substantive_destination='All original panel derivations, first-order reference, correction omission, paired study, adverse outcomes and weak-identification alternative survive in place; three additive subsections supply a primary derivation and exact counterexample before the retained paired study.')
 ledger.append(edit);tail=bib.read_text()[-180:]
 entry=r'''
@misc{rel32hkl,
 author={Hwang, Jungbin and Kang, Byunghoon and Lee, Seojeong},
 title={A Doubly Corrected Robust Variance Estimator for Linear {GMM}},
 year={2020},
 note={Inspected preprint arXiv:1908.07821v2, 29 May; title page dated 1 June. Later journal DOI 10.1016/j.jeconom.2020.09.010 is an identity link, not the inspected text},
 url={https://arxiv.org/abs/1908.07821v2}
}
'''
 ledger.append(dict(file=str(bib.relative_to(R)),before=tail,after=tail+entry,reason='Record exact primary preprint identity rather than attributing its claims to the uninspected journal version or Windmeijer original.',substantive_destination='Every inherited bibliography entry survives; one preprint entry added.'))
 papers=[R/'docs/papers/A Doubly Corrected Robust Variance Estimator for Linear GMM Hwang(2020).pdf',O/'hkl-primary.txt']
 receipt=R/'docs/literature/raw/rel32_hkl_original_v2.receipt.json'
 row=dict(citation_key='rel32hkl',kind='paper',source_identity='https://arxiv.org/abs/1908.07821v2',version_date='arXiv v2 uploaded29May2020; title page1June2020. Crossref identifies August2022 journal version, which is not the inspected text. Accessed29October2026; before7October2026 literature cutoff.',local_bindings=[bind(p) for p in papers+[receipt,R/'docs/literature/raw/rel32_hkl_arxiv_identity.xml',R/'docs/literature/raw/rel32_hkl_crossref.json']],inspected_anchors=[
 'Sections2–3,printed pp4–9,eqs(3)–(33): linear overidentified iid moment model; fixed first-stage weight, plug-in second moment, Windmeijer expansion and nonzero-moment/Jacobian/weight correction.',
 'Section4,pp9–13,eqs(34)–(41),Assumption1,Theorem1,Remarks1–2: distinct pseudo-true one/two-step targets; fixed dimension/full rank and finite moments; centered-weight target and derivative.',
 'Section5,pp14–15,eqs(42)–(48): iterated versus continuously updated GMM and nonlinear effective Jacobian.',
 'Section6,pp15–18,eqs(49)–(58): cross-sectional IV and entity-level difference-GMM formulas; different first-stage weight from the identity illustration.',
 'AppendixA,pp27–30,eqs(85)–(105): moment/Jacobian/weight influence expansion and covariance; aftereq(94), the claimed zero fifth derivative of inverse-weight functional is rejected by the authored finite-law counterexample.',
 'Tables2–3,pp42–43 inspected for their distinct panel simulation scope; no paper simulation numbers reused as project evidence.'
 ],supported_claims=[
 'Under the stated fixed-dimensional iid linear/full-rank regularity, residual-dependent Jacobian and weight variation is negligible at the leading correct-specification limit but can contribute at first order under misspecification.',
 'One-step and two-step pseudo-true values and centered/uncentered weights need not share a target.',
 'The source derives corrected covariance forms for linear one-step,two-step and iterated GMM; this does not imply many/weak-instrument robustness or a causal interpretation.',
 'The selected preprint contains an incorrect polynomial-degree inference aftereq(94); the manuscript states a local smooth-inversion Taylor argument and exact counterexample rather than adopting that step.'
 ],limitations=[
 'Selected technical sections and proof inspected; no claim of every theorem, appendix or version certified.',
 'The Windmeijer2005 original and Hwang etal2022 journal version remain uninspected; metadata supplies identity only.',
 'The preprint upload/title-page dates differ; both are explicitly retained.',
 'The exact four-cell law, numerical influence values, centered-weight target and illustrative dollar map are project derivations, not source-reported bank effects.',
 'No native panel adapter, new coverage study, bank evidence or independent acceptance.'],manuscript_edits=[118,119])
 audit=dict(sources=[row],project_derivation=dict(witness=bind(witness),generator=bind(R/'tools/release_gmm_witnesses_20261029.py'),assumptions=['Independent fair finite signs;identity initial weight;fixed2moments/1parameter.','Smooth nonsingular neighborhood and root-N preliminary estimator for the local Taylor argument.','Dollar map is stipulated and has no causal validity claim.']),omission=bind(O/'omission-record.json'),scope='Consequential primary comparison and exact reconstruction; no exhaustive survey or qualification.')
 ap=O/'source-audit.json';assert not ap.exists();at=json.dumps(audit,indent=2)+'\n'
 reviews_path=B/'mathematical-addition-reviews.json';reviews=json.loads(reviews_path.read_text());occ=lambda t:Counter(re.sub(r'\s+',' ',m[0]) for m in MATH.finditer(t))
 assert not occ(edit['before'])-occ(edit['after'])
 reviews['reviews'].append(dict(scope='Additive GMM influence derivation, exact misspecified target/variance construction and qualified proof-step counterexample.',edits=[dict(edit=118,file=edit['file'],before_sha256=hashlib.sha256(edit['before'].encode()).hexdigest(),after_sha256=hashlib.sha256(edit['after'].encode()).hexdigest())],allowed_added=dict(occ(edit['after'])-occ(edit['before'])),allowed_removed={},status='reviewed_additions_only',derivation='Differentiate the one/two-step FOCs with respect to moment,Jacobian,weight and first-stage components; exact symbolic four-cell enumeration verified by independent complex-step perturbation of all probabilities. Differentiate rational inverse-weight functional five times; nonzero result rejects degree argument while smooth local Taylor expansion retains asymptotic remainder order.',reviewed_assumptions=['Fixed dimensions;independent entities;unique interior pseudo-true minima;full-rankG;nonsingular weight;stated finite moments.','Identity first-stage weight;uncentered second moment;estimated first-stage weight requires extra derivative.','Correct-specification limit distinguished from fitted residual terms and misspecified pseudo-true target.','Explicit source error is limited to selected preprint step; no theorem-refutation or journal-version claim.','No historical study replaced or corrected native coverage claimed.'],witness=bind(witness),source_audit=dict(path=str(ap.relative_to(R)),sha256=hashlib.sha256(at.encode()).hexdigest()),fresh_visual_acceptance=False,independent_acceptance=False))
 before=O/'before-integration';before.mkdir(exist_ok=False)
 for p in [source,bib,B/'edits.json',reviews_path,R/'tools/release_source_verification_20261029.py']:shutil.copy2(p,before/p.name)
 ap.write_text(at);source.write_text(source.read_text().replace(anchor,edit['after'],1));bib.write_text(bib.read_text().replace(tail,tail+entry,1));(B/'edits.json').write_text(json.dumps(ledger,indent=2)+'\n');reviews_path.write_text(json.dumps(reviews,indent=2)+'\n')
 verifier=R/'tools/release_source_verification_20261029.py';s=verifier.read_text();old=" 'docs/release/2026-10-29/source-pygformula-025/source-audit.json']";assert s.count(old)==1;verifier.write_text(s.replace(old," 'docs/release/2026-10-29/source-pygformula-025/source-audit.json',\n 'docs/release/2026-10-29/source-windmeijer-032/source-audit.json']",1))
 print(json.dumps(dict(edits=len(ledger),new_paper=bind(papers[0]),audit=bind(ap),scope='All inherited science retained; build and final contextual review follow.')))
if __name__=='__main__':main()

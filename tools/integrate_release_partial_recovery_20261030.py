"""Add the selective-recovery argument with primary support and preservation."""
from pathlib import Path
from collections import Counter
import hashlib,json,re,shutil
R=Path(__file__).resolve().parents[1];B=R/'docs/release/2026-10-29';O=B/'partial-recovery-073';RAW=R/'docs/literature/raw'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(p):return dict(path=str(p.relative_to(R)),sha256=sha(p))
def save(p,x):p.write_text(json.dumps(x,indent=2)+chr(10))
def main():
    ledger=json.loads((B/'edits.json').read_text());assert len(ledger)==195
    witness=json.loads((O/'exact-witnesses.json').read_text());assert witness['status']=='pass'and witness['retained_rows']==8000
    title='Combining Double Sampling and Bounds to Address Nonignorable Missing Outcomes in Randomized Experiments'
    paper=R/'docs/papers'/f'{title} Coppock(2017).pdf';original=RAW/'closure30_coppock_original.pdf';assert original.read_bytes().startswith(b'%PDF')
    if paper.exists():assert sha(paper)==sha(original)
    else:shutil.copy2(original,paper)
    software=['DESCRIPTION','R_user_facing_functions_R','R_helper_functions_R','R_estimators_R','NEWS_md']
    files=[RAW/('closure30_attrition_'+x+'.txt')for x in software]
    files += [RAW/'closure30_attrition_commits.json',RAW/'closure30_attrition_tree.json']
    sources=[dict(citation_key='rel73coppock2017',kind='paper',title=title,
      authors='Alexander Coppock; Alan S. Gerber; Donald P. Green; Holger L. Kern',
      source_identity='doi:10.1017/pan.2016.6',version_date='Political Analysis25(2),188–206; published online23February2017',
      local_copy=bind(paper),acquisition=bind(RAW/'closure30_coppock_original.receipt.json'),primary_extract=bind(O/'coppock2017.txt'),
      inspected_anchors=['Sections2.1–2.4,pages190–195: randomized treatment, outcome stability, selective follow-up response and equations1–16.','Section2.5,pages195–197: sample-ratio endpoints, analytic variance and asymptotic true-ATE coverage, equations17–24.','Section2.6: poststratification; Section2.7,pages198–199:delta mixture restriction on nonresponders, equations28–29.','Sections3–5: response-rate versus sample-size distinction, original application and limits.'],
      supported_claims=['Random follow-up combined with bounded outcomes supplies partial identification under outcome stability despite selective completion.','Published sensitivity delta restricts nonresponse mixture, not change in the recovered historical outcome.','The published confidence target is asymptotic true-ATE coverage, distinct from the authored finite-sample whole-set claim.'],
      scope=['Primary theory read; no reproduction of the original application or generalization to bank data.','An acquired2016appendix has a different listed author set; its identity is preserved separately and it is not cited as the2017article.']),
      dict(citation_key='rel73attrition',kind='software',title='attrition: Addressing Nonignorable Attrition with Double Sampling and Bounds',
      source_identity='https://github.com/acoppock/attrition',version_date='Version1.0.0; commit162f979c44e5d28465d34ffe2d68b413b99ca3d5,21September2026',
      local_bindings=[bind(p)for p in files],inspected_anchors=['DESCRIPTION version, GPL-3 declaration and outcome-stability wording.','Full243-line helper source:ds_moments,gen_mean,gen_var,ds_var,poststratify,pool_strata,im_interval and im_critical_value.','Full277-line estimators source: double-sampling combination, bootstrap accounting and trimming branches.','User-facing lines1–145,300–345,548–645: input mapping, selection target and delta definition.','NEWS1.0.0 estimator descriptions;81-path pinned tree.'],
      supported_claims=['The inspected implementation uses follow-up response ratios and analytic variance before a normal critical-value inversion.','Actual delta code and function documentation implement the paper nonresponse mixture and cannot repair changed outcomes when completion is full.','The trimming interface targets always-reporters, a different estimand, and separately declares selection assumptions.','GPL-3 is a package declaration, not evidence of qualified integration or resolved dependency permissions.'],scope=['Static inspection only; no downloaded code executed.','No native performance, interface qualification, package coverage or correctness beyond inspected algebra claimed.'])]
    audit=dict(cutoff='2026-10-07',sources=sources,witness=bind(O/'exact-witnesses.json'),
        study_registration=[bind(R/f'docs/twelve-hour-closure/2026-10-29/partial-recovery-attempt-1/{name}/registration.json')for name in ['standard','intensive','complete','unstable']],
        study_runner=bind(R/'tools/run_partial_recovery_20261030.py'),study_independent_check=bind(R/'docs/twelve-hour-closure/2026-10-29/partial-recovery-attempt-1/independent-check.json'),
        appendix_identity=dict(path=str((RAW/'closure30_coppock_appendix.pdf').relative_to(R)),sha256=sha(RAW/'closure30_coppock_appendix.pdf'),title='Online Appendix',date='14March2016',authors='Peter M. Aronow; Alexander Coppock; Alan S. Gerber; Donald P. Green; Holger L. Kern',scope='Pages1–4read; not used as the final2017article or counted as a new cited paper.'),
        scope='Primary bounded-outcome theory and version-specific static comparison; project derivations and retained generated study are separately identified. No fixed-frontier count change.')
    save(O/'source-audit.json',audit)
    target=B/'source/docs/writing-repair/2026-10-29/src/1de93e537048440f.tex';old=target.read_text();anchor='alternatives at an acceptable total cost.';assert old.count(anchor)==1
    text=(O/'treatment.tex').read_text();after=anchor+chr(10)*2+text;shutil.copy2(target,O/'before-chapter014.tex')
    ledger.append(dict(file=str(target.relative_to(R)),before=anchor,after=after,reason='Close the selective-completion and historical-outcome stability gap with a bounded-outcome derivation, retained study and substantive alternatives.',substantive_destination='All inherited chapter14 mathematics, Gaussian servicing study, negative results and full-history recovery argument remain verbatim. New section makes the distinct binary target, confidence-set scope, empty intervals, stability violation and cost assumptions explicit.'))
    refs=B/'source/docs/writing-repair/2026-10-29/references-0.bib';s=refs.read_text();ra=s[-250:];assert s.count(ra)==1
    bib=r'''@article{rel73coppock2017,
  author = {Coppock, Alexander and Gerber, Alan S. and Green, Donald P. and Kern, Holger L.},
  title = {Combining Double Sampling and Bounds to Address Nonignorable Missing Outcomes in Randomized Experiments},
  journal = {Political Analysis},
  year = {2017}, volume = {25}, number = {2}, pages = {188--206},
  doi = {10.1017/pan.2016.6}
}
@misc{rel73attrition,
  author = {Coppock, Alexander and Gerber, Alan S. and Green, Donald P. and Kern, Holger L.},
  title = {attrition: Addressing Nonignorable Attrition with Double Sampling and Bounds},
  year = {2026},
  note = {Version 1.0.0; source revision 162f979c44e5d28465d34ffe2d68b413b99ca3d5, 21 September 2026},
  url = {https://github.com/acoppock/attrition}
}
'''
    assert 'rel73coppock2017'not in s and 'rel73attrition'not in s
    ledger.append(dict(file=str(refs.relative_to(R)),before=ra,after=ra+chr(10)+bib,reason='Add the genuine2017primary article and cutoff-pinned attrition software identity.',substantive_destination='Every earlier bibliography record retained; local genuine paper and claim-level software records accompany both additions.'))
    from release_candidate_20261029 import MATH
    count=lambda s:Counter(re.sub(r'\s+',' ',m[0])for m in MATH.finditer(s))
    reviews=json.loads((B/'mathematical-addition-reviews.json').read_text());reviews['reviews'].append(dict(scope='Additive bounded-outcome partial identification, inverse-invitation endpoints and simultaneous finite-sample confidence.',edits=[dict(edit=196,file=str(target.relative_to(R)),before_sha256=hashlib.sha256(anchor.encode()).hexdigest(),after_sha256=hashlib.sha256(after.encode()).hexdigest())],allowed_added=dict(count(after)-count(anchor)),allowed_removed={},status='reviewed_additions_only',
      derivation='Random invitation identifies completed-response masses; unresolved binary outcomes attain0and1 independently across otherwise unrestricted arms. Width equals both unresolved masses. Scores have range1/q_a; independent scaled scores have summed squared rangesD. Tilted-variance bound yields logmgf<=s^2D/8; Chernoff and two adverse tails give t=sqrt(D log(2/alpha)/2). Both population endpoints are covered simultaneously, with support clipping. Drift sensitivity restricts the recovered conditional mean separately from nonresponse delta.',
      reviewed_assumptions=['Random treatment, consistency, no interference, independent customer observations across and within arms, known independently drawn Bernoulli invitations.','Outcome stability and binary historical support; no finite bounds imposed on prior unbounded Gaussian reward.','Follow-up procedure and completion law fixed across positive invitation probabilities; zero invitation not covered.','Sharpness is relative to unrestricted unresolved outcomes and potential-outcome coupling, not to the fully specified simulation truth.','Normal bands empirical; empty sets and raw crossings retained. Gamma sensitivity is population-level and not automatically endowed with the original confidence guarantee.'],witness=bind(O/'exact-witnesses.json'),source_audit=bind(O/'source-audit.json'),fresh_visual_acceptance=False,independent_acceptance=False))
    target.write_text(old.replace(anchor,after,1));refs.write_text(s.replace(ra,ra+chr(10)+bib,1));save(B/'edits.json',ledger);save(B/'mathematical-addition-reviews.json',reviews)
    p=R/'tools/release_source_verification_20261029.py';s=p.read_text();a=" 'docs/release/2026-10-29/graph-software-072/source-audit.json']";assert s.count(a)==1;p.write_text(s.replace(a," 'docs/release/2026-10-29/graph-software-072/source-audit.json',"+chr(10)+" 'docs/release/2026-10-29/partial-recovery-073/source-audit.json']"))
    p=R/'tools/release_numerical_verification_20261029.py';s=p.read_text();helper=(R/'tools/reconstruct_release_partial_recovery_20261030.py').read_text();fn=helper[helper.index('def reconstruct():'):helper.index('def main():')]
    fn=fn.replace('def reconstruct():','def selective_recovery():'+chr(10)+'    import csv,io').replace(',bindings=bindings)',')')
    assert 'def selective_recovery'not in s;s=s.replace('def main():',fn+chr(10)+'def main():',1);a="    checks['useful_answer_economics']=useful_answer_economics()";assert s.count(a)==1;s=s.replace(a,a+chr(10)+"    checks['selective_recovery']=selective_recovery()",1);p.write_text(s)
    save(O/'integration.json',dict(status='written_pending_build_review',edits=[196,197],target=bind(target),treatment=bind(O/'treatment.tex'),source_audit=bind(O/'source-audit.json'),witness=bind(O/'exact-witnesses.json'),deleted_inherited_material='none',new_simulation=False,original_study_unchanged=True,execution_observation='One initial JavaScript template-literal patch failed before filesystem application because of a literal backtick; corrected patch succeeded.'))
    print(json.dumps(dict(edits=[196,197],new_cited_papers=1,retained_rows=8000)))
if __name__=='__main__':main()

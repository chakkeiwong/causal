"""Preserve the completed useful-answer economics study in the release."""
from pathlib import Path
from collections import Counter
import hashlib,json,re,shutil
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/release/2026-10-29'
OUT=BASE/'energy-integration-071'
STUDY=ROOT/'docs/twelve-hour-closure/2026-10-29'
NL=chr(10)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(p):return dict(path=str(p.relative_to(ROOT)),sha256=sha(p))
def save(p,d):p.write_text(json.dumps(d,indent=2)+NL)
def main():
    ledger=json.loads((BASE/'edits.json').read_text());assert len(ledger)==188
    witness=json.loads((OUT/'exact-witnesses.json').read_text());assert witness['status']=='pass'
    static=json.loads((OUT/'scoring-reinspection.json').read_text());assert static['stored_tests']==164
    source=STUDY/'energy-study.tex';text=source.read_text()
    text=text.replace(r'\section{',r'\subsection{').replace(r'\chapter{',r'\section{')
    before='The inexpensive public-data exercise establishes the relevant'+NL+'tradeoff before undertaking that more costly prototype measurement.'
    after='The inexpensive generated-arrival exercise establishes the relevant'+NL+'tradeoff before undertaking that more costly prototype measurement.'
    assert text.count(before)==1;text=text.replace(before,after,1)
    target=BASE/'source/docs/writing-repair/2026-10-29/investment.tex'
    original=target.read_text();anchor=r'\section{A spending sequence with real alternatives}'
    assert original.count(anchor)==1
    added=text+NL+anchor
    shutil.copy2(target,OUT/'before-investment.tex')
    raw_audit=json.loads((STUDY/'energy-source-support.json').read_text())
    keymap={'argerich2024':'closureArgerich2024','husom2025':'closureHusom2025','energymeter2026':'closureEnergyMeter2026','edgecode2026':'closureEdgeCode2026','hfeval2022':'closureCodeEval2022'}
    sources=[]
    for row in raw_audit['sources']:
        record=dict(citation_key=keymap[row['id']],kind='paper' if 'artifact' in row else 'software',title=row['title'],source_identity=row['original_url'],version_date=row['version'],local_bindings=[row['artifact']] if 'artifact' in row else row['artifacts'],inspected_anchors=row['inspected'],supported_claims=row['allowed'],scope=row['forbidden'],disposition=row['status'])
        for field in ['authors','license','qualification','version_limit','risk_record']:
            if field in row:record[field]=row[field]
        if row['id']=='argerich2024':record['primary_extract']=bind(OUT/'argerich2024.txt')
        if row['id']=='husom2025':
            record['primary_extract']=bind(OUT/'husom2025.txt')
            record['scope'].append('Project exclusion of quality and joint rankings is not a formal retraction or a finding about author intent.')
        if row['id'] in ['edgecode2026','hfeval2022']:record['release_static_reinspection']=bind(OUT/'scoring-reinspection.json')
        sources.append(record)
    names=['closure30_edge_paperera_evaluation.txt','closure30_edge_paperera_data.txt','closure30_sustainable_energy_tree.json','closure30_energy_tree.json','closure30_energy_commits.json','closure30_edge_humaneval_history.json']
    source_audit=dict(cutoff='2026-10-07',sources=sources,original_audit=bind(STUDY/'energy-source-support.json'),original_treatment=bind(source),supporting_bindings=[bind(ROOT/'docs/literature/raw'/x) for x in names],witness=bind(OUT/'exact-witnesses.json'),static_reinspection=bind(OUT/'scoring-reinspection.json'),scope='Claim-specific primary-text and static-source inspection; no native sensor qualification, published-experiment reproduction or bank value claim. Later retrieval does not change the cutoff.')
    save(OUT/'source-audit.json',source_audit)
    ledger.append(dict(file=str(target.relative_to(ROOT)),before=anchor,after=added,reason='Integrate completed useful-answer quality, energy-boundary and batch-delay argument before the investment recommendation.',substantive_destination='Every prior chapter101 paragraph and nested input remains. Complete scientific treatment added, with generated-arrival wording corrected; source-specific exclusions and operating limits preserved.'))
    refs=BASE/'source/docs/writing-repair/2026-10-29/references-0.bib';rt=refs.read_text();ra=rt[-250:];assert rt.count(ra)==1
    newrefs=(STUDY/'energy-refs.bib').read_text();assert all(k not in rt for k in keymap.values())
    ledger.append(dict(file=str(refs.relative_to(ROOT)),before=ra,after=ra+NL+newrefs,reason='Add five inspected primary paper/software identities with exact versions.',substantive_destination='All previous bibliography identities retained; two genuine paper PDFs and three pinned software sources added.'))
    patches=[]
    for name,before,after in [
        ('assistance.tex','contains 90 inspected entries, including the one source-quality quarantine,'+NL+'and 23 unread entries.','contains 91 inspected entries, including the one source-quality quarantine,'+NL+'and 22 unread entries.'),
        ('sponsor-body.tex','The fixed frontier inventory contains 90 inspected'+NL+'entries, including one explicit source-quality quarantine, and 23 unread.','The fixed frontier inventory contains 91 inspected'+NL+'entries, including one explicit source-quality quarantine, and 22 unread.')]:
        p=BASE/'source/docs/writing-repair/2026-10-29'/name;s=p.read_text();assert s.count(before)==1
        shutil.copy2(p,OUT/('before-'+name));patches.append((p,s,before,after))
        ledger.append(dict(file=str(p.relative_to(ROOT)),before=before,after=after,reason='Admit the primary-read and integrated fixed-frontier energy paper, candidate218.',substantive_destination='Previous candidate dispositions remain; one unread source becomes inspected. Husom is a separately excluded comparator outside this113-entry inventory.'))
    figure=STUDY/'energy-figures/energy-waiting.pdf';dest=BASE/'source/docs/twelve-hour-closure/2026-10-29/energy-figures/energy-waiting.pdf';assert not dest.exists();dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(figure,dest)
    additions=json.loads((BASE/'additions.json').read_text());additions.append(dict(path=str(dest.relative_to(ROOT)),original=str(figure.relative_to(ROOT)),sha256=sha(figure),reason='Preserve original synthetic trace and exact batching figure.',source_audit=str((OUT/'source-audit.json').relative_to(ROOT))))
    from release_candidate_20261029 import MATH
    counts=lambda s:Counter(re.sub(r'\s+',' ',m[0]) for m in MATH.finditer(s))
    reviews=json.loads((BASE/'mathematical-addition-reviews.json').read_text());reviews['reviews'].append(dict(scope='Additive exact energy integration, Poisson collection-delay moments and whole-attempt ratio economics.',edits=[dict(edit=189,file=str(target.relative_to(ROOT)),before_sha256=hashlib.sha256(anchor.encode()).hexdigest(),after_sha256=hashlib.sha256(added.encode()).hexdigest())],allowed_added=dict(counts(added)-counts(anchor)),allowed_removed={},status='reviewed_additions_only',derivation='Trapezoidal rule integrates linear interpolation with timestamp intervals. Rational trace yields330,300,600,270J under four declared conventions. Within each count batch, gapj delays j earlier requests; independent exponential gaps give sumj/b and sumj^2/b^2 moments. Batch-level MCSE preserves dependence. Ratio LLN requires positive acceptance probability and finite means, not independence of energy and success within attempts; cross-multiplication gives the relative-quality break-even condition. Whole-attempt expense counts failures and avoids duplicate cost categories.',reviewed_assumptions=['No sensor observations or empirical bank energy claims; artificial trace and generated Poisson arrivals.','Collection waiting excludes service, backlog, cancellations and timeouts; percentile is descriptive customer waiting, not an uncertainty bound on the mean.','Comparable fixed acceptance rule, repeatable whole attempts, appropriate LLN and positive useful-output probability.','Paper2024 GPU method differs from pinned2026 code. Static164-test defect does not reconstruct exact published executions or invalidate every power measurement.'],witness=bind(OUT/'exact-witnesses.json'),source_audit=bind(OUT/'source-audit.json'),fresh_visual_acceptance=False,independent_acceptance=False))
    target.write_text(original.replace(anchor,added,1));refs.write_text(rt.replace(ra,ra+NL+newrefs,1))
    for p,s,before,after in patches:p.write_text(s.replace(before,after,1))
    save(BASE/'edits.json',ledger);save(BASE/'additions.json',additions);save(BASE/'mathematical-addition-reviews.json',reviews)
    verifier=ROOT/'tools/release_source_verification_20261029.py';s=verifier.read_text();a=" 'docs/release/2026-10-29/outcome-integration-070/source-audit.json']";assert s.count(a)==1;verifier.write_text(s.replace(a," 'docs/release/2026-10-29/outcome-integration-070/source-audit.json',"+NL+" 'docs/release/2026-10-29/energy-integration-071/source-audit.json']"))
    save(OUT/'integration.json',dict(status='written_pending_build_review',edits=[189,190,191,192],target=bind(target),imported_original=bind(source),source_audit=bind(OUT/'source-audit.json'),witness=bind(OUT/'exact-witnesses.json'),correction='Public-data exercise replaced by generated-arrival exercise: the study simulates arrivals and fits no bank traffic.',deleted_inherited_material='No scientific removal; frontier count replaces stale metadata with one newly inspected original. The full inherited investment chapter remains.',new_study=False,execution_observation='Initial patch formatting was rejected before file creation; corrected patch uses explicit newline construction. No partial manuscript mutation occurred.'))
    print(json.dumps(dict(edits=[189,190,191,192],retained_batches=900000,source_records=5)))
if __name__=='__main__':main()

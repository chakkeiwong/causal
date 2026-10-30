"""Add the consequential pinned-software comparison without repeating theory."""
from pathlib import Path
import hashlib,json,re,shutil
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/release/2026-10-29'
OUT=BASE/'graph-software-072'
STUDY=ROOT/'docs/twelve-hour-closure/2026-10-29'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(p):return dict(path=str(p.relative_to(ROOT)),sha256=sha(p))
def save(p,d):p.write_text(json.dumps(d,indent=2)+chr(10))
def main():
    ledger=json.loads((BASE/'edits.json').read_text());assert len(ledger)==192
    source=STUDY/'graph-confidence.tex';s=source.read_text();start=s.index(r'\section{What to adopt, what to test and what to decline}');end=s.index(r'\section{A survey source',start)
    addition=s[start:end].replace(r'\section{What to adopt, what to test and what to decline}',r'\subsection{What the available software can contribute}')
    old="The inspected complete tree and selected\nnotebooks do not contain the thesis's HallBayes integration, Monte Carlo\ngraph construction or causal-flow training pipeline."
    new="The complete file inventory and two inspected notebooks do not expose the\nthesis's HallBayes integration, Monte Carlo graph construction or causal-flow\ntraining pipeline. This is a limit of the available reproduction evidence,\nnot proof that no private or differently named implementation exists."
    assert addition.count(old)==1;addition=addition.replace(old,new,1)
    addition=addition.replace('The HallBayes repository at the latest inspected pre-cutoff revision presents','The HallBayes repository at the inspected June 2026 revision presents')
    addition=addition.replace('Its README and source distinguish cited-evidence support from world truth.','Its README distinguishes cited-evidence support from world truth, and the\ninspected core accepts claims and cited spans as the scoring inputs.')
    addition=addition.replace('The proposal should\nintegrate the front-end ideas through a small,\nversioned interface and prefer maintained upstream components where their\nscope matches; porting the incomplete repository wholesale offers no\ndemonstrated advantage. Preserve applicable notices and review dependencies\nand data permissions separately.','The front-end ideas therefore belong behind a small, versioned interface.\nAn upstream component that supplies the required operation with maintained\ninterfaces is a serious alternative to maintaining this adaptation. The\ninspected repository establishes no performance advantage for a wholesale\nport. Its MIT notice is distinct from the permissions needed for dependencies,\nretrieval data and models.')
    target=BASE/'source/docs/writing-repair/2026-10-29/src/5e1bb6d4d921349d.tex';text=target.read_text();anchor='For the bank, the investment conclusion follows from the retained example in'
    assert text.count(anchor)==1;shutil.copy2(target,OUT/'before-component.tex')
    raw=json.loads((STUDY/'graph-source-support.json').read_text());records=[]
    anchors={'closure30molerocode':['README adaptation identity; complete95-path tree at120652bd;34-cell baseline and38-cell pairwise notebook sources.','AugmentedModelSuggester.suggest_pairwise_relationship retrieval/no-match branches and query_llm constructing its own client.','pyproject version placeholder/dependencies and MIT notice.'],'closure30berry':['README definition of evidence support versus world truth and CLI/MCP descriptions.','core.run_detect_hallucination inputs, citation normalization, scoring dispatch, truncation handling and result flag.','June17commit and full tree; December17date-bounded history response is empty; version-one tag points to February3commit.','MIT notice and explicit version boundary; no native execution or verification of benchmark claims.']}
    claims={'closure30molerocode':['The available adaptation supports suggestion/retrieval comparison but does not supply demonstrated reproduction of the complete printed flow/graph pipeline.','Inspected retrieval helper creates its own model client and falls back to a non-retrieved answer when no pair matches.'],'closure30berry':['The inspected Berry revision is a candidate evidence-support comparator with advertised CLI/MCP interfaces.','It is distinct from the thesis-era dependency; a bounded default-branch query does not prove older software never existed.']}
    selected={'closure30molerocode':['readme.md','tree.json','commits.json','augmented.txt','augmented_utils.txt','baseline_notebook.txt','tuebingen_notebook.txt','pyproject.txt','license.txt'],'closure30berry':['readme.md','core.txt','tree.json','commits.json','thesis_commit.json','thesis_commit.receipt.json','v1_commit.json','tags.json','license.txt']}
    for row in raw['software']:
        prefix='closure30_upm_' if row['key']=='closure30molerocode' else 'closure30_hallbayes_'
        copies=[bind(ROOT/'docs/literature/raw'/(prefix+n)) for n in selected[row['key']]]
        records.append(dict(citation_key=row['key'],kind='software',title='Causality LLMs medical-domain adaptation' if row['key']=='closure30molerocode' else 'HallBayes repository: Berry evidence-support service',source_identity=row['repository'],version_date=row['commit']+'; '+row['commit_date'],local_bindings=copies,inspected_anchors=anchors[row['key']],supported_claims=claims[row['key']],scope=['Static source inspection only; no downloaded code or model calls executed.','No causal correctness, graph-calibration, interval-coverage or native interface guarantee inferred.','Rights observation is version-specific and does not transfer dependency/data/model permissions.'],original_record=row))
    save(OUT/'source-audit.json',dict(cutoff='2026-10-07',sources=records,original_source_audit=bind(STUDY/'graph-source-support.json'),static_inventory=bind(OUT/'static-inventory.json'),scope='Consequential software comparison added to existing primary-theory critique; no new frontier admission.'))
    ledger.append(dict(file=str(target.relative_to(ROOT)),before=anchor,after=addition+anchor,reason='Complete the source-specific integration choice by distinguishing available retrieval/front-end code from the thesis pipeline and later Berry service.',substantive_destination='All existing theory, adverse examples, coverage experiment and financial conclusion remain. New subsection adds pinned implementation, dependency/date and reuse limits without duplicating them.'))
    refs=BASE/'source/docs/writing-repair/2026-10-29/references-0.bib';rt=refs.read_text();ra=rt[-250:];bib=(STUDY/'graph-refs.bib').read_text();newrefs=[]
    for key in ['closure30molerocode','closure30berry']:
        assert key not in rt;match=re.search(r'@misc\{'+key+r',.*?\n\}',bib,re.S);assert match;newrefs.append(match[0])
    # Use separate author names so the rendered scholarly label is readable.
    newrefs[0]=newrefs[0].replace("author = {{Molero P{\\'e}rez, Alba Mar{\\'i}a and PyWhy contributors}},","author = {Molero P{\\'e}rez, Alba Mar{\\'i}a and {PyWhy contributors}},")
    newrefs[1]=newrefs[1].replace('author = {{Hassana Labs and contributors}},','author = {{Hassana Labs} and others},')
    added=chr(10).join(newrefs)+chr(10);assert rt.count(ra)==1
    ledger.append(dict(file=str(refs.relative_to(ROOT)),before=ra,after=ra+chr(10)+added,reason='Add two exact software identities with legible author labels.',substantive_destination='All inherited bibliography records retained; existing primary-thesis and Chlon paper citations remain authoritative.'))
    target.write_text(text.replace(anchor,addition+anchor,1));refs.write_text(rt.replace(ra,ra+chr(10)+added,1));save(BASE/'edits.json',ledger)
    verifier=ROOT/'tools/release_source_verification_20261029.py';v=verifier.read_text();a=" 'docs/release/2026-10-29/energy-integration-071/source-audit.json']";assert v.count(a)==1;verifier.write_text(v.replace(a," 'docs/release/2026-10-29/energy-integration-071/source-audit.json',"+chr(10)+" 'docs/release/2026-10-29/graph-software-072/source-audit.json']"))
    save(OUT/'integration.json',dict(status='written_pending_build_review',edits=[193,194],target=bind(target),source_audit=bind(OUT/'source-audit.json'),imported_original=bind(source),scope='Only previously absent software comparison imported; already integrated mathematical critique, coverage experiment and source-quality exclusion retain their existing locations.',deleted_inherited_material='none',new_experiment=False))
    print(json.dumps(dict(edits=[193,194],new_software_records=2)))
if __name__=='__main__':main()

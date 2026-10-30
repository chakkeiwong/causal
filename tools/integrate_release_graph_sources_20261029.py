"""One-shot, ledgered integration of four independently inspected originals."""
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/release/2026-10-29'
OUT = BASE / 'graph-source-064'
SOURCE = BASE / 'source/docs/writing-repair/2026-10-29'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def binding(p):
    return dict(path=str(p.relative_to(ROOT)), sha256=sha(p))

def save(p, value):
    p.write_text(json.dumps(value, indent=2) + chr(10))

def main():
    ledger = json.loads((BASE/'edits.json').read_text())
    assert len(ledger) == 162, 'One-shot integration expects verified162-edit predecessor'
    inherited = json.loads((OUT/'inherited-source-support.json').read_text())
    names = ['molero','chlonone','chlonthree','aitlhouss']
    inspected = {
        'molero': ['PDF1,52,55–82,85–91,97–100,108–109,121–125: identity; pairwise/RAG proposal; equations14–19; PC comparator; four flow groups; percentile and IoU definitions; reported comparisons; explicit limitations; implementation appendix.', 'PDF67 equations14–16: selected-answer clipped positive lift and incorrect upper-error-bound interpretation; PDF69–70,124: independent Bernoulli edge sampling and topological sort; PDF81 and98: percentile definition and IoU results.'],
        'chlonone': ['PDF1,4–11; especially PDF5 Theorem5 and planners, PDF11 AppendixA.4–A.5: KL convexity/coarse-graining proof and clipped-information distinction. Title-page author/version identity checked.'],
        'chlonthree': ['PDF1,3,5–9,11–13: reference/predicate definition, Theorem5, Algorithm1, deployment instantiations, Proposition3, reported evaluation scope and limitations, AppendixA.4–A.6 proof and clipping, worked table.', 'The entire-chain equality needs both Jensen and event-coarsening equality; necessary information is not sufficient reliability. No universal model or graph/effect calibration inferred.'],
        'aitlhouss': ['PDF1–4: identity and abstract; PDF42–43 section4.1 versus Tables5–6:10 versus80 studies; PDF48–51 Table9 andPDF72 AppendixA: ten entries; PDF59–60: source-reported generalization and generic independent-trial labels.', 'AppendixA entries3/5 checked against retained authentic arXiv identity pages: identifiers refer to different titles. Retained repository receipt is HTTP404 on29October2026; not proof the repository never existed.']
    }
    claims = {
        'molero': ['The printed workflow maps prompt-based risk scores to independently sampled graph edges and flow-model effect percentiles.', 'The complement of its largest feasible success probability is a lower error bound under the printed inequality; using it as an upper error bound or graph probability needs additional justification.', 'Reported means .723/.712/.301 compare intervals with fitted expert-graph reference intervals, not observed intervention truth.', 'Source acknowledges calibration/false-negative problems and excludes hidden confounders; source-specific PC comparator and information mismatch require follow-up.'],
        'chlonone': ['The KL mixture and event-coarsening inequality supplies a necessary information requirement.', 'Selected-answer scoring and prompt masking do not automatically identify the reference correctness distribution.'],
        'chlonthree': ['This exact later version explicitly limits deployment to a specified predicate and available verification reference.', 'The displayed budget selector and necessary inequality do not prove attained reliability; binary inversion has two branches absent a direction restriction.', 'One reported held-out audit is not a universal calibration or intervention-coverage theorem.'],
        'aitlhouss': ['Identity and specific exclusion rationale only: internally inconsistent study counts and mismatched reference identities.']
    }
    receipts = {'molero':['closure30_upm_original.receipt.json','closure30_upm_landing.html'],
        'chlonone':['closure30_chlon_v1.receipt.json','closure30_chlon_landing.html'],
        'chlonthree':['closure30_chlon_v3.receipt.json','closure30_chlon_landing.html'],
        'aitlhouss':['closure30_uah_original.receipt.json','closure30_uah_reference_3.html','closure30_uah_reference_3.receipt.json','closure30_uah_reference_5.html','closure30_uah_reference_5.receipt.json','closure30_uah_repo.receipt.json']}
    records = []
    for name in names:
        old = next(r for r in inherited['sources'] if r['key']=='closure30'+name)
        p = ROOT/old['local_copy']['path']
        assert sha(p) == old['local_copy']['sha256'] and p.read_bytes().startswith(b'%PDF-')
        files = [p,OUT/('closure30'+name+'.txt')] + [ROOT/'docs/literature/raw'/f for f in receipts[name]]
        records.append(dict(citation_key='rel64'+name,kind='paper',source_identity=old['url'],
            version_date=old['version_date']+'; inspected29October2026UTC. Client literature cutoff7October2026.',
            local_bindings=[binding(f) for f in files],inspected_anchors=inspected[name],supported_claims=claims[name],
            limitations=['Selected primary passages inspected as extracted text; no fresh visual inspection, independent acceptance or upstream numerical replication.', 'Acquisition inherited from a separate campaign; current reading and exact witnesses belong to this release.', 'Version-specific findings; no current software claim or exhaustive correction/retraction clearance.'] + (['Quarantined for quantitative and survey support; no allegation of intent or formal retraction.'] if name=='aitlhouss' else ['No bank validation, graph/effect calibration or native package admission.'])))
    audit = dict(recorded_utc=datetime.now(timezone.utc).isoformat(),cutoff='2026-10-07',sources=records,
        inherited_acquisition=binding(OUT/'inherited-source-support.json'),
        exact_derivation=binding(OUT/'exact-witnesses.json'),generator=binding(ROOT/'tools/release_graph_confidence_witnesses_20261029.py'),
        scope='Release-specific primary comparison, exact algebra and source-quality exclusion. Prior campaign simulations and acceptance not imported.')
    save(OUT/'source-audit.json',audit)
    amendments=[]
    def edit(p,before,after,reason,destination):
        old=p.read_text();assert old.count(before)==1 and before!=after
        amendments.append((p,old,old.replace(before,after,1)))
        ledger.append(dict(file=str(p.relative_to(ROOT)),before=before,after=after,reason=reason,substantive_destination=destination))
    graph=SOURCE/'src/5e1bb6d4d921349d.tex'
    before=graph.read_text().split('The proposal should therefore retain expert-guided averaging as a candidate')[1]
    before='The proposal should therefore retain expert-guided averaging as a candidate'+before
    edit(graph,before,before+chr(10)+(OUT/'addition.tex').read_text(),
        'Develop the newly available primary workflow and its version-specific confidence foundations, with exact bound, graph-law and interval-reference counterexamples.',
        'Every existing graph-ensemble derivation, adverse result, dollar example and alternative remains verbatim. New sections use its existing identification and monetary example instead of duplicating a study.')
    bib=SOURCE/'references-2.bib';before=bib.read_text().splitlines()[-1]
    source_bib=(ROOT/'docs/twelve-hour-closure/2026-10-29/graph-refs.bib').read_text()
    blocks=re.split(r'(?=^@)',source_bib,flags=re.M)
    selected=[b for b in blocks if any(re.match(r'@\w+\{closure30'+name+r',',b) for name in names)]
    assert len(selected)==4
    addition=chr(10).join(selected)
    for name in names:addition=addition.replace('closure30'+name,'rel64'+name)
    edit(bib,before,before+chr(10)+addition,'Add four version-specific bibliography identities for inspected primary originals.', 'All existing bibliography entries retained; new entries distinguish both Chlon versions and source-quality exclusion.')
    assistance=SOURCE/'assistance.tex';old=assistance.read_text();before=old[old.index('The preferred first assisted task is therefore'):].rstrip()
    after=before.replace('bring this edition to','brought the preceding edition to')+r'''

The end-to-end workflow in Section~\ref{rel64:graph-confidence} adds a
further primary comparison. It turns a prompt-based risk score into sampled
graphs and fitted effect intervals, but its uncertainty interpretation needs
the additional conditions developed there. A separate thesis by Ait Lhouss
has been inspected only for a source-quality disposition. Section~4.1 gives
ten included studies, whereas its abstract and Tables~5--6 give eighty; its
selected-study table lists ten. Those unresolved denominators prevent using
its reported review coverage or productivity results here. This is an
exclusion of those claims, not an allegation of intent or formal retraction.
The current inventory therefore contains 89 inspected entries, including
this one explicit quarantine, and 24 unread entries. Inspection does not
mean that every inspected work supplies positive evidence. \citep{rel64molero,rel64aitlhouss}
'''
    edit(assistance,before,after,'Reconcile new primary reading and explicit quarantine with the recommendation and candidate census.',
        'Preserve the questionnaire comparator, earlier readings, cutoff limitations and live-evaluation requirements; add precise disposition and distinguish inspection from evidential admission.')
    sponsor=SOURCE/'sponsor-body.tex';before='''85 inspected and 28 unread entries; two further primary readings bring this
edition to 87 inspected and 26 unread. They refine extraction and explanation
claims without establishing a lending effect or this product's live-model benefit.'''
    after='''85 inspected and 28 unread entries; two further primary readings brought the
preceding edition to 87 inspected and 26 unread. They refine extraction and
explanation claims without establishing a lending effect or this product's
live-model benefit. A further workflow comparison and a source-quality
exclusion bring the inventory to 89 inspected, including one explicit
quarantine, and 24 unread. The graph-confidence comparison does not establish
calibrated intervention intervals.'''
    edit(sponsor,before,after,'Align sponsor coverage with the bounded primary comparison and excluded survey claims.',
        'Historical counts, interpretation and absence of live-model benefit remain explicit. The new census includes an inspected quarantine, not a positive source admission.')
    assert len(ledger)==166
    from release_candidate_20261029 import MATH
    occurrences=lambda s:Counter(re.sub(r'\s+',' ',m[0]) for m in MATH.finditer(s))
    e=ledger[162];before_math=occurrences(e['before']);after_math=occurrences(e['after'])
    assert not before_math-after_math
    reviews=json.loads((BASE/'mathematical-addition-reviews.json').read_text())
    reviews['reviews'].append(dict(scope='Exact additions for information bounds, coherent graph sampling and interval-reference distinction.',
        edits=[dict(edit=163,file=e['file'],before_sha256=hashlib.sha256(e['before'].encode()).hexdigest(),after_sha256=hashlib.sha256(e['after'].encode()).hexdigest())],
        allowed_added=dict(after_math-before_math),allowed_removed={},status='reviewed_additions_only',
        derivation='Invert the necessary Bernoulli inequality on its upper branch; complement reverses the bound. Four-state construction isolates within-event divergence. Enumerate all eight edge subsets exactly and condition on the seven DAGs. Equal-interval overlap is independent of truth inclusion.',
        reviewed_assumptions=['Reference versus predictive law explicitly distinguished; absolute continuity and finite KL for the inequality.', 'Three stipulated directed edges with independent Bernoulli4/5 draws; no claim about cycles in the source study.', 'Graph-class uncertainty and training variability are not repeated-sampling coverage; actual source result retained as fitted-reference overlap.', 'Financial values refer to the existing authored100USD/unit and40USD cost example; no new empirical evidence.'],
        witness=binding(OUT/'exact-witnesses.json'),source_audit=binding(OUT/'source-audit.json'),fresh_visual_acceptance=False,independent_acceptance=False))
    for p,old,new in amendments:
        assert p.read_text()==old
        (OUT/('before-'+p.name)).write_text(old)
        p.write_text(new)
    save(BASE/'edits.json',ledger);save(BASE/'mathematical-addition-reviews.json',reviews)
    pending=dict(status='awaiting_build_and_context_review',edits=list(range(163,167)),source_audit=binding(OUT/'source-audit.json'),
        previous_batch=51,scope='Primary reading and exact derivations complete; successor not certified until build, preservation, numerics and affected-context review.')
    save(OUT/'integration.json',pending)
    print(json.dumps(pending))

if __name__ == '__main__':
    main()

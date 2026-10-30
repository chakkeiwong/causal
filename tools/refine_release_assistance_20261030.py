"""Rewrite confirmed instruction-heavy prose and preserve exact dispositions."""
from pathlib import Path
import hashlib
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/release/2026-10-29'
SOURCE = BASE / 'source/docs/writing-repair/2026-10-29'
OUT = BASE / 'assistance-prose-067'

def main():
    ledger = json.loads((BASE / 'edits.json').read_text())
    assert len(ledger) == 176
    assert json.loads((BASE / 'deletion-audit.json').read_text())['status'] == 'pass'
    OUT.mkdir(exist_ok=True)
    assert not (OUT / 'semantic-dispositions.json').exists()
    changes = []
    texts = {}
    def replace(path, start, end, after, retained, moved=None):
        text = texts.setdefault(path, path.read_text())
        a = text.index(start)
        z = text.index(end, a)
        before = text[a:z]
        assert text.count(before) == 1 and before != after
        texts[path] = text[:a] + after + text[z:]
        number = len(ledger) + 1
        ledger.append(dict(file=str(path.relative_to(ROOT)), before=before, after=after,
                           reason='Replace instruction sequences or acquisition chronology with connected scientific and economic explanation.',
                           substantive_destination=retained + (' Historical editorial details retained in assistance-prose-067/semantic-dispositions.json and the exact ledger.' if moved else '')))
        changes.append(dict(edit=number, file=str(path.relative_to(ROOT)),
                            retained_claims=retained, moved_editorial_details=moved or [],
                            before_sha256=hashlib.sha256(before.encode()).hexdigest(),
                            after_sha256=hashlib.sha256(after.encode()).hexdigest()))
    a = SOURCE / 'assistance.tex'
    replace(a, 'For formulation, the useful output', '\input{writing-repair/2026-10-29/src/0dc21980bfecb7cc.tex}', r'''A useful formulation states the intervention and its alternative, the
population, outcome, horizon and information date, and the choices that remain
unresolved. The retained Kıcıman and causal-learn+ discussions motivate a
prototype for question clarification and graph critique; they cannot establish
the truth of a bank's assumptions. A structured questionnaire completed by an
economist is therefore a serious comparator. The relevant outcomes are material
omissions in the final question and the time needed to correct them. In the
deposit example, assignment, receipt, acceptance and price define different
questions. A fluent response that silently substitutes one for another fails
this comparison. \citep{v12_la_2305_00050,v12_la_2606_23608}

Variable construction introduces a further question: does an extracted field
measure the scientific variable? The retained review of text-based adjustment
explains relevant uses of text, but supplies no general guarantee that an
embedding removes confounding. A documented coding rule and independently
labelled examples provide a comparison for the proposed extraction, including
missing and ambiguous cases. The observation journey explains why predictive
accuracy and apparent completeness alone cannot establish measurement validity.
Auditable field definitions and retrieval assistance are justified starting
points; autonomous scientific measurement requires independent validation of
the relation between the field and the variable. \citep{exec13_census_text_review_arxiv}

''', 'Formulation fields, unresolved choices, Kıcıman and causal-learn+ scope, questionnaire comparator, correction effort, deposit counterexample, text-adjustment limits, coding-rule and labelled-example baselines, missing/ambiguous cases and independent validation remain explicit.')
    replace(a, 'For diagram work, require evidence', '\input{writing-repair/2026-10-29/src/02a318fabcd8ae09.tex}', r'''A proposed diagram is useful when each relationship has an interpretation,
an information date and supporting evidence, and competing explanations remain
visible. LACR's retrieval results show why the choice of evidence matters: the
retained study reports both improvement and deterioration, including the ASIA
skeleton comparison and the SACHS comparison after adding PC output. More
context is therefore a candidate design choice whose consequences need
measurement. \citep{v12_la_2402_15301}

Ordinary search by an economist and an applicable numerical discovery method
are substantive alternatives. A comparison with matched inputs should follow
false orientations and missed common causes through to the estimated effect
or chosen action. Edge counts alone conceal that consequence. The first
assisted workflow can propose a diagram and its alternatives for review, then
invoke a named discovery or identification method under explicit assumptions.
Numerical discovery contributes evidence within those assumptions; textual
plausibility cannot resolve directions that the observations leave equivalent.
In the three-model pricing example, one unjustified orientation is enough to
reverse the financial sign.

''', 'Edge interpretation, timing, evidence, competing diagrams, adverse and positive ASIA/SACHS retrieval findings, matched-information economist/numerical comparators, false orientations, missed confounders, financial consequence and equivalence-class restrictions remain.')
    replace(a, 'CLadder evaluates formal causal questions', 'The preferred first assisted task', r'''CLadder evaluates formal causal questions under constructed mechanisms. Its
historical model results concern a supplied task rather than the elicitation
of a new bank mechanism. A defined formal procedure provides the identification
comparator: an assisted answer must preserve both the conclusion and the
conditions under which it follows. When identification fails, an explanation
of the missing restriction is useful; an unexplained empty response is not.
The benchmark literature and retained mechanism-clustering critiques also
justify retaining failed cases and the full uncertainty denominator.
\citep{v12_la_2312_04350}

For execution, the local interface study establishes equality for four
constructed requests. Assessing assistance requires a further comparison with
a scripted workflow, because choosing the request and correcting mistakes are
part of the analytical work. Request construction, faithful tool use, detected
errors and correction effort are the relevant outcomes. The formal tool's
calculation cannot by itself establish the assistant's contribution.

A deterministic reporting template is another strong comparator. It already
states the estimand, assumptions, interval and scope. The proposed additional
value is an explanation of why the result changes a decision, or why it
cannot yet support one, that remains faithful to the result and its sources.
An explanation that promotes a set crossing zero into a positive recommendation
is substantively wrong. No local live-model evaluation yet establishes an
incremental benefit for this reporting task.

''', 'CLadder supplied-mechanism scope, formal identification comparator, justified refusal, failures and uncertainty denominator, four-case interface scope, scripted baseline, request/correction costs, deterministic reporting baseline, zero-crossing adverse case and absence of measured live-model benefit remain.')
    replace(a, 'The preferred first assisted task', '\citep{rel66pharma,rel66inferbert,rel66deepcausality,rel66veitch}', r'''Question clarification with evidence retrieval and explicit alternatives is
the preferred first assisted task, evaluated against the questionnaire.
Identification and numerical results remain with defined procedures. Expansion
to autonomous discovery, variable construction or recommendations needs
evidence specific to those tasks. The three frontier studies in
Section~\ref{gap29:frontier} sharpen this distinction. The financing-and-exports
study in Section~\ref{closure30:formulation} supports a bounded extraction and
explanation comparison; its scores do not identify a lending effect. The
related epistemology discussion supplies no separate intervention estimate.
These findings refine the proposed experiment without establishing a live
banking benefit. \citep{rel18li,rel18mugleston}

The end-to-end workflow in Section~\ref{rel64:graph-confidence} turns a
prompt-based risk score into sampled graphs and fitted effect intervals. Its
uncertainty interpretation depends on the additional conditions developed
there. The thesis by Ait Lhouss is used only to explain a source-quality
exclusion: Section~4.1 and the selected-study table report ten studies, whereas
the abstract and Tables~5--6 report eighty. These unresolved denominators
prevent using its reported review coverage or productivity results. That
limited exclusion implies neither intent nor a formal retraction.
\citep{rel64molero,rel64aitlhouss}

The pharmacovigilance comparison in Section~\ref{rel66:text-signals} shows
that useful enriched terms and classifier-score differences still need an
intervention argument. The InferBERT and DeepCausality methods expose the
missing adjustment requirements; the conditional text-embedding alternative
also makes target-population weighting explicit. The fixed frontier inventory
contains 90 inspected entries, including the one source-quality quarantine,
and 23 unread entries. Supporting method originals are audited separately
and do not enlarge that denominator. Inspection is therefore distinct from
positive scientific support, and the remaining omissions limit broader claims.
A live comparison needs a fixed model version, held-out questions, matched
information, independent adjudication and a budget. ''', 'Preferred formulation/retrieval task, defined numerical delegation, all three frontier studies, financing and epistemology limits, graph-confidence conditions, Ait Lhouss ten/eighty discrepancy and restricted quarantine, pharmacovigilance/embedding comparison, current90/23 census, separate supporting-source denominator and live-comparison design remain.', ['Earlier candidate census85/28, subsequent87/26 and89/24, and acquisition sequence moved to the exact editorial record; these describe edition history, not additional scientific findings.'])
    s = SOURCE / 'sponsor-body.tex'
    replace(s, 'Language assistance should initially', 'The matched analyst comparison', r'''Language assistance should initially clarify the question, retrieve relevant
evidence and expose alternatives, with a structured questionnaire and ordinary
search as comparators. Formal identification and numerical calculations remain
with defined procedures. Historical paper results and local scripted cases
do not establish this product's incremental live-model benefit. The literature
cutoff is 7 October 2026. The fixed frontier inventory contains 90 inspected
entries, including one explicit source-quality quarantine, and 23 unread.
The financing and epistemology comparisons refine extraction and explanation
claims without identifying a lending effect. The graph workflow does not
establish calibrated intervention intervals. The pharmacovigilance comparison
shows why relevant text terms cannot substitute for an intervention argument;
text-based adjustment requires sufficient information and the correct
target-population weights.

''', 'Initial assistance task, questionnaire/search baselines, formal delegation, no measured product benefit, cutoff, current90/23 census and quarantine, financing/epistemology limits, graph-interval limitation, pharmacovigilance and population-weight requirements remain.', ['Historical85/28,87/26,89/24 updates and their ordering moved to editorial record.'])
    replace(s, 'The matched analyst comparison', '\section*{An economic decision', r'''The proposed analyst comparison includes both answerable questions and
deliberately insufficient designs. Independent assessment covers the final
target, assumptions, uncertainty and financial interpretation. Its effort
measure includes preparation, correction, interpretation and unsuccessful
attempts as well as runtime; a correct refusal remains distinguishable from
an avoidable tool failure. The comparison has not yet measured hours saved
or improvements in bank decisions.

''', 'Proposed trial status, answerable/insufficient designs, independent target/assumption/uncertainty/value assessment, full effort and failed attempts, correct refusal versus tool failure, and absence of measured savings remain.')
    replace(s, 'This sponsor text is aligned', 'Editorial delivery, fresh visual acceptance', r'''The accompanying monograph contains the public experimental study, generated
comparisons, retained derivations and comparative source arguments behind this
proposal. Its source audit records original papers, versions, inspected
anchors and supported claim scopes. The sponsor introduces no separate source,
bank measurement, vendor price or deployment claim.
''', 'Reader/sponsor alignment, public/generated/derivational evidence, source traceability and absence of separate sponsor data, prices or deployment claims remain.', ['Alignment through an edition date is replaced by direct alignment to the accompanying monograph; the date remains on the title page and in publication records.'])
    from release_candidate_20261029 import MATH, CITE
    from collections import Counter
    for path, after in texts.items():
        before = path.read_text()
        assert Counter(m[0] for m in MATH.finditer(before)) == Counter(m[0] for m in MATH.finditer(after))
        before_keys = {k.strip() for group in CITE.findall(before) for k in group.split(',')}
        after_keys = {k.strip() for group in CITE.findall(after) for k in group.split(',')}
        assert before_keys == after_keys, dict(missing=sorted(before_keys-after_keys), added=sorted(after_keys-before_keys))
        shutil.copy2(path, OUT / ('before-' + path.name))
    save = lambda p, d: p.write_text(json.dumps(d, indent=2) + chr(10))
    save(OUT / 'semantic-dispositions.json', dict(
        status='prebuild_editorial_review', edits=changes,
        standard='Connected argument and current recommendations; retain all scientific substance and audit removed editorial history.',
        no_removed_mathematics=True, citation_commands_preserved=True,
        history_destination='Before-text snapshots and exact ledger preserve all historical counts and chronology. Scientific outcomes and source-specific adverse findings remain in both delivered arguments.',
        postbuild_semantic_deletion_review='pending'))
    for path, after in texts.items():
        path.write_text(after)
    save(BASE / 'edits.json', ledger)
    print(json.dumps(dict(edits=list(range(177, len(ledger)+1)), status='written_pending_build_and_postdeletion_review')))

if __name__ == '__main__':
    main()

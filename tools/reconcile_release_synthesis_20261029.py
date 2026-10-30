"""Single-use synthesis/sponsor reconciliation; preserve exact prior passages."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'docs/release/2026-10-29'
SOURCE = BASE/'source/docs/writing-repair/2026-10-29'
OUT = BASE/'synthesis-reconciliation-026'


def main():
    ledger=json.loads((BASE/'edits.json').read_text())
    assert len(ledger)==107, 'Single-use reconciliation; do not rerun.'
    assert not OUT.exists()
    changes={}
    def edit(p,before,after,reason,destination):
        old,current=changes.get(p,(p.read_text(),p.read_text()))
        assert current.count(before)==1,(str(p),before[:80])
        changes[p]=(old,current.replace(before,after,1))
        ledger.append(dict(file=str(p.relative_to(ROOT)),before=before,after=after,
                           reason=reason,substantive_destination=destination))
    p=SOURCE/'src/301406daaa5228ef.tex'
    before='The remaining uncertainty is specific to a candidate: its supported target,\n'
    new=r'''The longitudinal comparisons identify a more specific reason to withhold
some profiles. In the selected pygformula restriction path, deterministic
histories enter the fitting population even though simulation subsequently
enforces their known values. In the selected lmtp uncertainty composition,
the order of centering, weighting and aggregation matters when weights or
cluster sizes differ. The Julia survival comparison similarly separates
identified parameter combinations, observation entry and extrapolated tails.
These findings concern which distribution or uncertainty is computed, not
merely programming style. They narrow the proposed reuse contracts without
establishing how often failures occur in bank data.
Sections~\ref{sec:exec24-longitudinal-python}, \ref{rel23:ife-centering} and
\ref{rel22:survival-delegates} develop their source traces, exact constructions
and alternatives.~\citep{rel25pygfit,rel23ife,rel23ifecaller,rel22survbase,rel22survdist,rel22survcaller}

A source-level discrepancy can justify withholding an affected profile before
an empirical trial. It does not justify rejecting every method in the same
library, nor does a corrected formula alone establish native qualification.
The next comparison must reproduce the intended fitting population, output
scale and sampling unit, including adverse cases that expose those differences.
That requirement makes conditional reuse more precise: retain a useful original
method where its contract holds, repair and verify a specific mismatch, or
choose a substantively matched alternative.

'''
    edit(p,before,new+before,'Bring developed longitudinal source findings into the authoritative implementation synthesis.',
         'Original projection/panel examples and caveats remain; new prose points to the complete source-specific derivations and distinguishes profile refusal from whole-library rejection.')
    p=SOURCE/'src/626099247fe4b6ef.tex'
    before='of a released 1.1.2 binary. The complete history, event order, interventions\nand resampling procedure must be matched before drawing a reuse conclusion.'
    after='of a released 1.1.2 binary. The complete history, event order, interventions\nand resampling procedure must be matched before drawing a reuse conclusion.\nFor the selected pygformula revision, withhold the documented deterministic\ncovariate-restriction profile until its fitting-population mismatch is corrected\nand verified. This restricts that profile rather than treating every simulator\noutput as invalid (Section~\\ref{sec:exec24-longitudinal-python}).'
    edit(p,before,after,'Qualify the named longitudinal candidate by the now-developed fitting mismatch.',
         'Both R and Python candidates and the full matching requirement survive; a profile-specific refusal is made explicit.')
    before='7. Longitudinal effects & gfoRmula; pygformula comparator & Begin with a short fixed policy and observed histories. Compare entire simulation and uncertainty routes. Missing action determinants or sparse histories require a new design. \\citep{exec20_gformula_reuse,exec24_longpy_pygformula_source}\\\\[5pt]'
    after='7. Longitudinal effects & gfoRmula; pygformula comparator & Begin with a short fixed policy and observed histories. Compare entire simulation and uncertainty routes; withhold the selected pygformula covariate-restriction profile pending correction and verification. Missing action determinants or sparse histories require a new design. \\citep{exec20_gformula_reuse,exec24_longpy_pygformula_source,rel25pygfit}\\\\[5pt]'
    edit(p,before,after,'Carry the profile restriction into the selection matrix.',
         'Original short-policy scope, uncertainty comparison and missing-information cautions remain in the same row.')
    p=SOURCE/'assistance.tex'
    before='frontier evidence includes the three additional inspected originals discussed\nin Section~\\ref{gap29:frontier}. The current census is 85 inspected and\n28 unread; these omissions still limit broad claims. A live comparison still\nrequires a fixed model version, held-out questions, matched information,\nindependent adjudication and a budget.'
    after='frontier evidence includes the three additional inspected originals discussed\nin Section~\\ref{gap29:frontier}. The preceding inventory recorded 85 inspected\nand 28 unread entries. The financing-and-exports and epistemology originals\nnow developed in Section~\\ref{closure30:formulation} bring this edition to\n87 inspected and 26 unread. The financing study supports a bounded extraction\nand explanation comparison; its scores do not identify a lending effect.\nThe epistemology discussion supplies no separate intervention estimate. These\nreadings sharpen the limits of assistance without establishing live banking\nbenefit. The remaining omissions still limit broad claims. A live comparison\nrequires a fixed model version, held-out questions, matched information,\nindependent adjudication and a budget.~\\citep{rel18li,rel18mugleston}'
    edit(p,before,after,'Reconcile the central assistance conclusion with two already integrated originals and exact coverage.',
         'Retains the historical85/28 inventory and all evaluation requirements; current87/26 scope and the substantive limits of both sources are explicit.')
    p=SOURCE/'sponsor-body.tex'
    before='source comparisons. The first integration should reuse a transparent\nstatistical procedure with an independently understandable alternative.'
    after='source comparisons. Selected fitting and uncertainty paths have specific\nrestrictions that require correction and verification before reuse; source\ninspection does not establish native qualification. The first integration\nshould reuse a transparent statistical procedure with an independently\nunderstandable alternative.'
    edit(p,before,after,'Align sponsor conditional reuse with the developed static implementation findings.',
         'The original seventeen-area synthesis and understandable alternative remain; source findings do not become empirical or bank qualification claims.')
    before='literature cutoff is 7 October 2026; the retained frontier census still has\n85 inspected and 28 unread entries.'
    after='literature cutoff is 7 October 2026. The earlier frontier inventory had\n85 inspected and 28 unread entries; two further primary readings bring this\nedition to 87 inspected and 26 unread. They refine extraction and explanation\nclaims without establishing a lending effect or this product\'s live-model benefit.'
    edit(p,before,after,'Update the sponsor coverage and source-role statement while preserving prior count identity.',
         'Historical85/28 count retained explicitly; current87/26 agrees with the candidate inventory and two integrated originals.')
    OUT.mkdir()
    for p,(old,new) in changes.items():
        assert p.read_text()==old
        (OUT/p.name).write_text(old)
    (OUT/'edits-before.json').write_bytes((BASE/'edits.json').read_bytes())
    for p,(_,new) in changes.items():p.write_text(new)
    (BASE/'edits.json').write_text(json.dumps(ledger,indent=2)+'\n')
    (OUT/'review-plan.json').write_text(json.dumps(dict(
        basis='Complete chapters26,27,32,101, front matter and sponsor read at snapshot107. New edits affect chapters26/27 and sponsor; other reviewed contexts remain byte-identical.',
        findings=['Central27 and sponsor mistakenly presented85/28 as current despite two integrated originals.',
                  'Longitudinal selection matrix did not carry the newly established profile-specific fitting restriction.',
                  'General source synthesis needed to distinguish a static discrepancy, an exact consequence and native qualification.'],
        preservation='All scientific examples, equations, alternative routes, adverse results and prior inventory identity remain.',
        required_next=['Build exact successor','Post-build deletion/source checks','Read changed paragraphs and both sponsor and reader rendered text','Renew affected full-context records and sponsor identity'],
        release_accepted=False),indent=2)+'\n')
    print(json.dumps(dict(edits=len(ledger),changed_files=len(changes),ledger_sha256=hashlib.sha256((BASE/'edits.json').read_bytes()).hexdigest())))


if __name__=='__main__':
    main()

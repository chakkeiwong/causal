"""Join the opening and evidence synthesis to the completed argument."""
from pathlib import Path
import json,shutil
R=Path(__file__).resolve().parents[1];B=R/'docs/release/2026-10-29';O=B/'argument-coherence-075'
def main():
    ledger=json.loads((B/'edits.json').read_text());assert len(ledger)==203
    O.mkdir(exist_ok=True);patches=[]
    p=B/'source/docs/writing-repair/2026-10-29/src/45358a4637eac946.tex'
    before='''established relationship.

The evidence and method-choice part''';after=r'''established relationship. The finite-sample comparison in
Section~\ref{closure30:sampling} then asks whether completing that search
produces reliable graphs and effect intervals. In the servicing study,
Sections~\ref{closure30:outcome-audit} and~\ref{rel73:partial-recovery}
distinguish buying more observations from recovering the intended historical
outcome. These distinctions connect computational and information choices
to the financial decision.

The evidence and method-choice part'''
    patches.append((p,before,after,'Make completed graph-sampling and recovery arguments discoverable from the opening.','All original navigation and substantive distinctions remain; added references lead directly to the completed arguments.'))
    before='''Its recommendation is tested against expert composition and existing
commercial capability.''';after=r'''Its comparison also prices the full effort per useful answer and the
waiting cost of batching in Section~\ref{closure:energy-study}. The
recommendation is tested against expert composition and existing
commercial capability.'''
    patches.append((p,before,after,'Connect the opening investment guide to whole-study expense and waiting.','The same recommendation and alternatives remain, with specific navigation to the developed economics.'))
    p=B/'source/docs/writing-repair/2026-10-29/src/1de93e537048440f.tex'
    before='''withhold the historical-effect recommendation. These generated results close
the missing selective-completion argument for a bounded single-treatment
example. They do not establish feasible bank recovery, a general solution
for unbounded longitudinal rewards, or independent operating acceptance.'''
    after='''withhold the historical-effect recommendation. The generated single-treatment
example shows why more invitations, more completed responses and more stable
historical information can have different decision values. Extending that
conclusion to a bank requires evidence about its actual recovery process.
Unbounded longitudinal rewards require their own identification and sampling
arguments, and operating acceptance remains unestablished.'''
    patches.append((p,before,after,'Replace an authoring-status conclusion with the substantive information comparison.','Preserve the bounded single-treatment scope, no established bank recovery, no general result for unbounded longitudinal rewards and no operating acceptance. No equation, result or source removed.'))
    p=B/'source/docs/writing-repair/2026-10-29/src/324f17c385ce10b1.tex'
    before='''Together they favour a comparison on completed scientific work: whether an'''
    after=r'''The follow-up studies make that recommendation more specific. Random
invitations can leave selective completion, and a later report can describe
a different outcome from the historical one the bank needs
(Section~\ref{rel73:partial-recovery}). A more complete graph search can
still select the wrong relationships from a finite sample
(Section~\ref{closure30:sampling}). Where compatible graphs imply different
actions, more computation does not replace identifying information
(Section~\ref{rel64:graph-confidence}). A useful study may therefore
recommend better records, a different experiment or no decision yet.
Its cost must include the effort of reaching that conclusion, including
unsuccessful attempts; Section~\ref{closure:energy-study} develops this
comparison per useful completed answer.

Together they favour a comparison on completed scientific work: whether an'''
    patches.append((p,before,after,'Connect completed follow-up evidence to the service comparison before detailed method chapters.','Every earlier study and the existing comparison remain. New paragraph explains selection, outcome stability, graph sampling, information and whole-attempt expense without adding unsupported empirical claims.'))
    p=B/'source/docs/writing-repair/2026-10-29/investment.tex'
    before=r'''a useful result. Section~\ref{closure30:outcome-audit} shows how truthful
random recovery can repair an observation problem; its precision improvement'''
    after=r'''a useful result. Section~\ref{closure30:outcome-audit} shows how random
recovery of the fixed historical outcome can repair an observation problem;
its precision improvement'''
    patches.append((p,before,after,'Name the historical-outcome requirement directly in the investment synthesis.','The same recovery condition and precision qualification survive with an explicit outcome target.'))
    originals={p:p.read_text()for p,*_ in patches};updates=dict(originals)
    for p,before,after,reason,destination in patches:
        assert updates[p].count(before)==1,(p,before)
        updates[p]=updates[p].replace(before,after,1)
        ledger.append(dict(file=str(p.relative_to(R)),before=before,after=after,reason=reason,substantive_destination=destination))
    for p in originals:shutil.copy2(p,O/('before-'+p.name))
    for p,s in updates.items():p.write_text(s)
    (B/'edits.json').write_text(json.dumps(ledger,indent=2)+'\n')
    (O/'integration.json').write_text(json.dumps(dict(status='written_pending_build_review',edits=list(range(204,209)),targets=[str(p.relative_to(R))for p in updates],important_material_removed=False,new_results=False),indent=2)+'\n')
    print('Applied exact ledger edits204–208 to four source files.')
if __name__=='__main__':main()

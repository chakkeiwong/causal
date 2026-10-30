"""Replace drafting-version shorthand with exact reader navigation."""
from pathlib import Path
import json,shutil
R=Path(__file__).resolve().parents[1];B=R/'docs/release/2026-10-29';O=B/'linked-history-review-081'

def main():
    ledger=json.loads((B/'edits.json').read_text());assert len(ledger)==221
    targets={
        '92c294197eb52e9f':[
            ('''The
preserved V10 procedure instead uses a Wilson rank guard and returns''',r'''The regular procedure in Section~\ref{v10:execution}
uses a Wilson rank guard and returns'''),
            ('''retains the fixed six-column dictionary, chronological half-split ridge
selection and full-pilot refit of V10.''',r'''retains the fixed six-column dictionary, chronological half-split ridge
selection and full-pilot refit described in Section~\ref{v10:pilot}.'''),
            ('''uses the V9 innovation-filtration argument under correct action-mean and
exogeneity premises.''',r'''uses the innovation-filtration argument in Section~\ref{v9:covariance}
under correct action-mean and exogeneity premises.'''),
            ('''in the preserved V9 chapter.''',r'''in Section~\ref{v9:pilot}.'''),
            ('''seeds are disjoint from V10.''',r'''seeds are disjoint from the precision comparison in Chapter~\ref{ch:precision-streaming}.''')],
        '0cff1da10e2094f3':[
            ('''The normal/dependent-calendar bands inherit the conditional growing-pilot
rate and score assumptions from the preserved monograph.''',r'''The normal/dependent-calendar bands use the conditional growing-pilot rate
and score assumptions developed in Sections~\ref{v9:pilot} and~\ref{v9:covariance}.''')]
    }
    changed=[]
    for stem,patches in targets.items():
        p=B/'source/docs/writing-repair/2026-10-29/src'/(stem+'.tex');text=p.read_text();shutil.copy2(p,O/('before-navigation-'+p.name))
        for before,after in patches:
            assert text.count(before)==1,(stem,before)
            text=text.replace(before,after,1)
            ledger.append(dict(file=str(p.relative_to(R)),before=before,after=after,
                reason='Replace internal drafting-version shorthand with the exact argument or procedure in the delivered reader.',
                substantive_destination='The identified procedure, assumptions, nuisance-rate result and independence of study seeds retain their original meaning. Exact chapter/section references make the dependency reconstructible without draft history. No mathematics, result, qualification or source citation is removed.'))
            changed.append(len(ledger))
        p.write_text(text)
    (B/'edits.json').write_text(json.dumps(ledger,indent=2)+'\n')
    p=O/'integration.json';x=json.loads(p.read_text());x['edits']+=changed;x['navigation']='Six replacements map V9/V10 drafting shorthand to the existing pilot, covariance, execution and precision sections; all referents remain substantively unchanged.';p.write_text(json.dumps(x,indent=2)+'\n')
    print('Applied navigation edits',changed)

if __name__=='__main__':main()

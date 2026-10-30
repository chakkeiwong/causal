"""Connect completed evidence to investment decisions without deleting detail."""
from pathlib import Path
import csv,hashlib,json,shutil
R=Path(__file__).resolve().parents[1];B=R/'docs/release/2026-10-29';O=B/'decision-synthesis-074'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(p):return dict(path=str(p.relative_to(R)),sha256=sha(p))
def save(p,x):p.write_text(json.dumps(x,indent=2)+chr(10))
def main():
    ledger=json.loads((B/'edits.json').read_text());assert len(ledger)==197;O.mkdir(exist_ok=True)
    witness={}
    for name in ['standard','intensive','complete','unstable']:
        p=R/f'docs/twelve-hour-closure/2026-10-29/partial-recovery-attempt-1/{name}/replications.csv';rows=list(csv.DictReader(p.open()));counts={}
        for q in [.1,.25,.5,1.]:
            cells=[r for r in rows if float(r['q'])==q]
            counts[str(q)]={m:sum(float(r[m+'_lower'])>.05 and float(r[m+'_lower'])<=float(r[m+'_upper'])for r in cells)for m in ['normal','hoeffding']}
        witness[name]=dict(source=bind(p),nonempty_net_positive=counts)
    assert witness['intensive']['nonempty_net_positive']['1.0']==dict(normal=22,hoeffding=5)
    assert witness['complete']['nonempty_net_positive']['1.0']==dict(normal=432,hoeffding=335)
    save(O/'decision-witness.json',dict(status='pass',benefit_per_additional_repayment_usd=100,cost_per_offer_usd=5,effect_threshold=.05,regimes=witness,scope='Post-processing the retained registered study, not an added simulation or bank-price observation.'))
    patches=[]
    chapter=B/'source/docs/writing-repair/2026-10-29/src/1de93e537048440f.tex'
    anchor='USD~5 threshold.'
    after=anchor+chr(10)*2+'''At full invitation under intensive recovery, only 5 of 500 bounded sets
and 22 normal bands have a nonempty net-benefit range wholly above zero.
The earlier counts of 401 and 469 concerned a positive effect, before
deducting the offer cost. Under complete stable recovery, the corresponding
net-positive counts are 335 and 432. These are decision frequencies in the
same retained datasets. They show how a small population margin can remain
hard to distinguish from zero even after follow-up reaches every missing
customer. The normal-band frequencies retain their empirical qualification;
more affirmative decisions alone do not establish a better procedure.'''
    patches.append((chapter,anchor,after,'Connect the financial threshold to actual retained interval decisions.','No earlier result removed. New frequencies distinguish effect positivity from covering the stated offer cost; assumptions and normal-band limitations remain.'))
    sponsor=B/'source/docs/writing-repair/2026-10-29/sponsor-body.tex'
    anchor='A separate exact-oracle discovery comparison tests a computational repair on'
    addition='''A follow-up design can buy missing information when it recovers the intended
historical outcome. Random invitations alone are insufficient when completion
is selective. The bounded repayment example derives an honest effect range
under that selection and a conservative confidence set; changing the outcome
during follow-up can instead make the wrong contrast more precise. The cost
of obtaining trustworthy records must accompany any proposed precision gain.

'''
    patches.append((sponsor,anchor,addition+anchor,'Bring the completed recovery-design conclusion into the sponsor.','Every earlier empirical result and qualification remains. Added synthesis distinguishes selective completion and outcome drift without new bank claims.'))
    anchor='benchmark, a field failure rate or a calibrated bank discovery service.'
    after=anchor+''' The
finite-sample follow-up shows that completed search can still produce wrong
graphs and unreliable effect intervals. Timing information helps in selected
cases; it does not supply general calibration.'''
    patches.append((sponsor,anchor,after,'Prevent exact-oracle success from standing alone after finite-sample follow-up.','Oracle counts remain unchanged; added qualification reports the already retained sampling study, with conditional timing benefit and unresolved general coverage.'))
    anchor='Equivalent quality and cost favour the existing workflow.'
    addition='''The comparison must also price useful completed answers. Cheaper model
requests can cost more per accepted study when failures and correction
increase. The monograph therefore separates whole-attempt expense, independently
assessed usefulness and waiting time. Public energy measurements do not supply
bank quality, traffic, tariffs or operating savings.

'''
    patches.append((sponsor,anchor,addition+anchor,'Align sponsor economics with the completed useful-answer argument.','Existing benefit formula, no-double-counting condition and reversal criteria remain verbatim. No additional quantitative assumption enters sponsor.'))
    investment=B/'source/docs/writing-repair/2026-10-29/investment.tex'
    anchor=r'\section{A spending sequence with real alternatives}'
    addition=r'''The information studies clarify what the first comparison must recognize as
a useful result. Section~\ref{closure30:outcome-audit} shows how truthful
random recovery can repair an observation problem; its precision improvement
depends on the information and effort purchased. Section~\ref{rel73:partial-recovery}
then separates random invitation, successful completion and a stable historical
outcome. The bank can buy more replies without resolving the effect, or obtain
a precise answer about the wrong date. In the bounded example, even a positive
effect set may not cover the offer cost.

The graph studies make the parallel distinction between more computation and
more identifying information. Completing the oracle search does not qualify
the finite-sample selection procedure in Section~\ref{closure30:sampling}.
The two compatible mechanisms in Section~\ref{rel64:graph-confidence} still
imply different financial actions until new information excludes one. A shared
service earns its place if it helps the analyst recognize these distinctions,
choose an informative next study or avoid an unsupported recommendation at
lower full cost. Producing more estimates is not by itself that benefit.

'''
    patches.append((investment,anchor,addition+anchor,'Synthesize the scientific information studies before the final spending recommendation.','All prior investment arguments and energy-study detail remain. Cross-references connect recovery, graph ambiguity and offer-cost thresholds to the same completed-study criterion.'))
    originals={p:p.read_text()for p,*_ in patches};updated=dict(originals)
    for p,before,after,reason,destination in patches:
        assert updated[p].count(before)==1,(p,before)
        ledger.append(dict(file=str(p.relative_to(R)),before=before,after=after,reason=reason,substantive_destination=destination));updated[p]=updated[p].replace(before,after,1)
    for p,s in originals.items():shutil.copy2(p,O/('before-'+p.name))
    for p,s in updated.items():p.write_text(s)
    save(B/'edits.json',ledger)
    verifier=R/'tools/release_numerical_verification_20261029.py';s=verifier.read_text()
    before="            cells.append(dict(q=q,n=500,counts={k:sum(r[k]for r in group)for k in flags},set_mean_width=widths,empty_sets=empty,positive_nonempty=positive_nonempty,mean_invitations=expected['mean_invitations'],mean_recoveries=expected['mean_recoveries'],mean_naive=expected['mean_naive'],naive_mcse=expected['naive_mcse']))"
    after="            net_positive_nonempty={m:sum(r[m+'_lower']>.05 and r[m+'_lower']<=r[m+'_upper']for r in group)for m in ['normal','hoeffding']}"+chr(10)+before.replace('positive_nonempty=positive_nonempty,','positive_nonempty=positive_nonempty,net_positive_nonempty=net_positive_nonempty,')
    assert s.count(before)==1;s=s.replace(before,after,1)
    before="    gamma=F(27,76);assert F(47,200)-F(19,50)*gamma==F(1,10)"
    extra="    assert results['intensive']['cells'][-1]['net_positive_nonempty']==dict(normal=22,hoeffding=5)"+chr(10)+"    assert results['complete']['cells'][-1]['net_positive_nonempty']==dict(normal=432,hoeffding=335)"+chr(10)
    assert s.count(before)==1;s=s.replace(before,extra+before,1);verifier.write_text(s)
    save(O/'integration.json',dict(status='written_pending_build_review',edits=list(range(198,203)),targets=[bind(p)for p in updated],witness=bind(O/'decision-witness.json'),deleted_inherited_material='none',new_simulation=False))
    print(json.dumps(dict(edits=list(range(198,203)),targets=3)))
if __name__=='__main__':main()

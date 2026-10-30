"""Stipulated parallel-trends law with unequal baseline levels, exact arithmetic."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/release/2026-10-29/source-flexpaper-017/exact-witnesses.json'


def main():
    assert not OUT.exists(), 'Frozen witness: use a successor'
    # U indexes an equally likely branch group; action Z=U follows at date 3.
    # X is constant; P(Z=1|X)=1/2. Untreated changes are constant across groups.
    rows=[]
    for u in [0,1]:
        pre=F(10)+4*u
        untreated_post=pre+3
        treated_post=untreated_post+2
        observed_post=treated_post if u else untreated_post
        rows.append(dict(group=u,probability='1/2',pre=str(pre),
                         untreated_post=str(untreated_post),treated_post=str(treated_post),
                         observed_post=str(observed_post),untreated_increment=str(untreated_post-pre)))
    pre_gap=F(rows[1]['pre'])-F(rows[0]['pre'])
    post_gap=F(rows[1]['observed_post'])-F(rows[0]['observed_post'])
    effect=post_gap-pre_gap
    assert (pre_gap,post_gap,effect)==(4,6,2)
    assert all(F(x['untreated_increment'])==3 for x in rows)
    assert all(F(x['treated_post'])-F(x['untreated_post'])==effect for x in rows)
    cost=F(3)
    report=dict(status='pass',rows=rows,pre_gap=str(pre_gap),post_gap=str(post_gap),
                identified_effect=str(effect),action_cost=str(cost),
                correct_margin=str(effect-cost),post_gap_margin=str(post_gap-cost),
                scope='Exact project law: no interference, no anticipation, common untreated increments and marginal overlap for constant X. The common-baseline-level outcome model is false. No paper rerun, fitted forest, bank evidence or general calibration result.',
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    OUT.parent.mkdir(exist_ok=False)
    OUT.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))


if __name__=='__main__':main()

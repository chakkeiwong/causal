"""Correct a Wilson-versus-exact reading without changing the underlying study."""
from pathlib import Path
import json,shutil

R=Path(__file__).resolve().parents[1]
B=R/'docs/release/2026-10-29'
O=B/'funding-review-079'


def main():
    ledger=json.loads((B/'edits.json').read_text());assert len(ledger)==215
    patches=[]
    p=B/'source/docs/writing-repair/2026-10-29/src/52581f9fe00a8116.tex'
    before='''cover .9400 and .9405. The ordinary exact binomial interval for .9400 only
slightly excludes .95; the adjusted interval includes it. With 200 audit'''
    after='''cover .9400 and .9405. For the fourfold pilot, the ordinary Wilson interval
ends below .95, whereas the exact binomial interval is approximately
[.928681, .950007] and narrowly includes .95. The adjusted exact interval
also includes it. With 200 audit'''
    patches.append((p,before,after,'Correct the interpretation of the ordinary interval for1880covers in2000requests.',
        'The1880/2000 count and all tables are unchanged. The Wilson upper endpoint is.9495888029; the exact binomial upper endpoint is.9500067612. The text now separates them. Small-audit and persistent-case adjusted shortfalls, paired gains and all adverse findings survive.'))
    p=B/'source/docs/writing-repair/2026-10-29/src/65a610a93e0ddf97.tex'
    before='''output quality. These are additional observations, not consequences of an
author having obtained a passing calculation or a useful local memory ratio.'''
    after='''output quality. Correct calculations and useful local memory ratios leave
these institutional requirements to be tested with the relevant owners and
operating conditions.'''
    patches.append((p,before,after,'Express the institutional inference directly without narrating author success.',
        'All independent-review, authentic assignment, source-clock, audit, invariant-pilot, precision, interface, platform, acquisition and labor requirements remain immediately before this sentence. The distinction between local numerical results and institutional observations remains explicit.'))
    for p,before,after,reason,destination in patches:
        text=p.read_text();assert text.count(before)==1
        shutil.copy2(p,O/('before-'+p.name));p.write_text(text.replace(before,after,1))
        ledger.append(dict(file=str(p.relative_to(R)),before=before,after=after,reason=reason,substantive_destination=destination))
    (B/'edits.json').write_text(json.dumps(ledger,indent=2)+'\n')
    (O/'integration.json').write_text(json.dumps(dict(status='written_pending_build_review',edits=[216,217],
        finding='The prose had called a Wilson exclusion an exact-binomial exclusion. Independent binomial-tail inversion agrees with the retained exact review and contradicts that sentence.',
        original_wilson=[.9287241955068138,.9495888028856835],original_exact=[.9286806804041159,.9500067611955054],
        methods_and_draws_unchanged=True,new_empirical_results=False),indent=2)+'\n')
    print('Applied exact edits216/217; statistical interpretation corrected, studies preserved.')


if __name__=='__main__':main()

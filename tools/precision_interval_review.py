#!/usr/bin/env python3
"""Conservative reporting repair; retains frozen studies and original summaries."""
import json
import numpy as np
from scipy.stats import beta, binom, binomtest
from precision_common import ROOT, save


def exact(count,n,alpha):
    return [float(beta.ppf(alpha/2,count,n-count+1)) if count else 0.,
            float(beta.ppf(1-alpha/2,count+1,n-count)) if count<n else 1.]


def main():
    minimum_margin=1.
    for n in range(1,26):
        for alpha in (.05,.05/24,.05/48):
            intervals=np.asarray([exact(k,n,alpha) for k in range(n+1)])
            for probability in np.linspace(0,1,201):
                keep=(intervals[:,0]<=probability)&(probability<=intervals[:,1])
                coverage=float(binom.pmf(np.arange(n+1),n,probability)[keep].sum())
                minimum_margin=min(minimum_margin,coverage-(1-alpha))
                assert coverage>=1-alpha-1e-12
    report=json.loads((ROOT/'docs/studies/precision-final-results.json').read_text())
    rows=[]
    for case in report['results']:
        methods={}
        for name,method in case['summary']['methods'].items():
            methods[name]=dict(exact_mc95=exact(method['covered'],method['requested'],.05),
                exact_simultaneous_mc95=exact(method['covered'],method['requested'],.05/24))
        pairs={}
        for name,pair in case['summary']['paired'].items():
            g,l=pair['gained'],pair['lost'];n=report['repetitions']
            # Each cell count is marginally binomial. Union bounds do not
            # require independence between gain and loss counts or methods.
            gain,loss=exact(g,n,.025),exact(l,n,.025)
            sg,sl=exact(g,n,.05/48),exact(l,n,.05/48)
            p=binomtest(g,g+l,.5).pvalue if g+l else 1.
            pairs[name]=dict(coverage_difference=pair['coverage_difference'],
                conservative_mc95=[gain[0]-loss[1],gain[1]-loss[0]],
                conservative_simultaneous_mc95=[sg[0]-sl[1],sg[1]-sl[0]],
                exact_equal_coverage_p=float(p),bonferroni_equal_coverage_p=min(1.,24*float(p)),
                gained=g,lost=l)
        rows.append(dict(design=case['design']['name'],methods=methods,paired=pairs))
    zero=next(r for r in rows if r['design']=='near_rank_1200')['paired']['pilot8_horizon minus pilot4_horizon']
    assert zero['gained']==zero['lost']==0 and zero['conservative_mc95'][0]<0<zero['conservative_mc95'][1]
    save('docs/reviews/precision-interval-review.json',dict(status='pass',results=rows,
        checks=dict(exhaustive_small_binomial_coverage=True,zero_discordance_has_positive_uncertainty=True),
        minimum_checked_coverage_margin=minimum_margin,
        issues=[],scope='Post-execution reporting repair: original Wilson/Wald summaries retained. Binomial inversion and union bounds add conservative marginal/family intervals, including nonzero uncertainty for zero observed discordance. Each simultaneous family separately has 24 estimates/comparisons. No combined guarantee across both families. Estimators, seeds and draws are unchanged.'),
        ['tools/precision_interval_review.py','docs/studies/precision-final-results.json'])
    print(json.dumps(dict(status='pass',designs=len(rows),marginal_cells=24,paired_comparisons=24)))


if __name__=='__main__': main()

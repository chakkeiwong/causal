"""Independent result accounting and exact moment checks for the repair study."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
from collections import Counter
import json

R=Path(__file__).resolve().parents[1];O=R/'docs/discovery-repair/2026-10-29';A=O/'attempt-1'
def main():
    results=json.loads((A/'results.json').read_text());cases=json.loads((A/'cases.json').read_text());manifest=json.loads((A/'manifest.json').read_text())
    assert sha256((A/'results.json').read_bytes()).hexdigest()==manifest['results_sha256']
    assert sha256((A/'cases.json').read_bytes()).hexdigest()==manifest['cases_sha256']
    assert len(cases)==1098+256+24
    assert Counter(x['n'] for x in cases if x['name'].startswith('ordered'))=={2:2,3:8,4:64,5:1024}
    groups=[cases[:1098],cases[1098:1354],results['witnesses'],cases[1354:]]
    for row,group in zip(results['summary'],groups):
        assert row['cases']==len(group)
        for mode,key in [('full','full_failures'),('screen','screened_failures'),('depth2','depth2_wrong_skeletons')]:
            assert row[key]==sum(x[mode]['false_positive']+x[mode]['false_negative']>0 for x in group)
        assert row['full_requests']==sum(x['full']['calls'] for x in group)
        assert row['screen_requests']==sum(x['screen']['calls'] for x in group)
    assert all(x['full']['false_positive']==x['full']['false_negative']==0 for x in cases)
    assert all(x['depth2']['completion']=='incomplete_search' for x in cases if x['depth2']['false_positive'])
    # Independent derivation after residualising the k baseline factors:
    # X*=eX, Y*=eY, C*=eX+eY+eC, all three errors independent variance one.
    # Projection on C* gives covariance 0-1*1/3, and variance 1-1/3.
    covariance=F(0)-F(1,3);variance=F(1)-F(1,3);slope=covariance/variance
    for x in results['gaussian']:
        k=x['k'];assert F(x['collider_conditional_covariance'])==covariance
        assert F(x['collider_conditional_variance'])==variance
        assert F(x['collider_adjusted_slope'])==slope==F(-1,2)
        assert F(x['unadjusted_slope'])==F(k,k+1)
        assert x['true_intervention_effect']=='0'
    receipt=json.loads((R/'docs/literature/raw/v12_exec13_java_aitiotita_pc.receipt.json').read_text())
    raw=R/receipt['path'];assert sha256(raw.read_bytes()).hexdigest()==receipt['sha256']
    source=dict(citation_key='repair29pc',source_identity=receipt['url'],version_date='8a8e566a87186de4935e644cec0fa80e6d456fd7; 2023-09-09',
      accessed_utc=receipt['accessed_utc'],local_copy=receipt['path'],sha256=receipt['sha256'],
      inspected_anchors=['PcAlgorithm.java lines 59-115: depth and all-neighbour freezing','lines 118-214: subset tests and stable removal'],
      supported_claims=['The inspected generic skeleton path can freeze a link on all-neighbour dependence at depth greater than two.'],
      limitations=['Bundled linguistic oracle is different. Project tests do not execute or qualify Java code, orientation, sample-based tests or banking effects.'],
      classification='IMPLEMENTATION_OR_SOFTWARE',cutoff='2026-10-07')
    (O/'source-audit.json').write_text(json.dumps(dict(sources=[source],project_derivation=['Residualisation formula and exact structural intervention','Project oracle/repair comparison'],new_scholarly_sources=0,scholarly_census_unchanged=True),indent=2)+'\n')
    report=dict(status='pass',cases_checked=sum(len(x) for x in groups),independent_oracle_agreements=results['oracle_crosschecks'],
        counts_recomputed=True,exact_covariance_derivation=True,source_hash_verified=True,
        screened_failures=sum(x['screened_failures'] for x in results['summary']),
        depth_capped_wrong=sum(x['depth2_wrong_skeletons'] for x in results['summary']),
        full_search_failures=0,native_package_execution=False,scope='Declared finite project suite; not universal correctness or field failure prevalence')
    (O/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()

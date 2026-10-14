#!/usr/bin/env python3
"""Replay current saved evidence without relabelling adverse outcomes as passes."""
import json
import zipfile
from importlib.metadata import version
from reliability_common import ROOT,SPEC,summarize
from closure_common import save,digest

def read(p):return json.loads((ROOT/p).read_text())

def main():
    issues=[];inputs=['tools/reliability_verify.py','tools/reliability_common.py','tools/closure_common.py',SPEC];s=read(SPEC)
    def bind(path):
        r=read(path);inputs.append(path)
        for p,h in r.get('input_sha256',{}).items():
            inputs.append(p)
            if digest(p)!=h:issues.append('Stale input: '+path+' / '+p)
        return r
    def journal(name,expected):
        path='docs/studies/reliability-'+name+'-final.jsonl';inputs.append(path);lines=(ROOT/path).read_text().splitlines();header=json.loads(lines[0]);rows={}
        for p,h in header['input_sha256'].items():
            inputs.append(p)
            if digest(p)!=h:issues.append('Journal input changed: '+name+' / '+p)
        for line in lines[1:]:
            row=json.loads(line)
            if row['key'] in rows:issues.append('Duplicate journal key: '+name)
            rows[row['key']]=row['result']
        if len(rows)!=expected:issues.append('Incomplete journal: '+name)
        return rows,bind('docs/studies/reliability-'+name+'-results.json')
    def replay(rows,prefix,reps,truth,expected):
        runs=[rows[f'{prefix}/{i}'] for i in range(reps)]
        if summarize(runs,truth)!=expected:issues.append('Summary mismatch: '+prefix)
    cal,r=journal('calibration',4500)
    if not all(r['checks'].values()):issues.append('Calibration reconstruction failed')
    for case in r['results']:replay(cal,case['design']['name']+'/evaluation',s['calibration']['repetitions'],r['financial_truth'],case['summary'])
    joint,r=journal('joint',3001)
    if not all(r['checks'].values()):issues.append('Joint algebra failed')
    for case in r['results']:replay(joint,case['case'],s['joint']['repetitions'],s['joint']['beta']*s['joint']['monetary_scale'],case['summary'])
    graph,r=journal('graphs',12000)
    if not all(r['checks'].values()):issues.append('Graph inversion checks failed')
    for case in r['results']:replay(graph,case['case'],s['graphs']['repetitions'],case['truth'],case['summary'])
    nonlinear,r=journal('nonlinear',242)
    if not all(r['numerical']['checks'].values()):issues.append('Nonlinear numerical gate failed')
    for case in r['results']:replay(nonlinear,case['case'],s['nonlinear']['repetitions'],case['truth_currency'],case['summary'])
    learning,r=journal('learning',600)
    if not all(r['checks'].values()):issues.append('Dense equivalence failed')
    for case in r['results']:replay(learning,case['case'],s['learning']['repetitions'],case['truth'],case['summary'])
    follow,r=journal('followup',900);fs=read('docs/studies/reliability-followup-spec.json')
    replay(follow,'joint',fs['joint']['repetitions'],s['joint']['beta']*s['joint']['monetary_scale'],r['results'][0]['summary'])
    replay(follow,'learning',fs['learning']['repetitions'],1.2,r['results'][1]['summary'])
    workload,r=journal('workloads',8)
    if not all(all(c['checks'].values()) for c in r['comparisons']):issues.append('Matched workload obligations failed')
    for p,h in r['artifact_sha256'].items():
        inputs.append(p)
        if digest(p)!=h:issues.append('Changed workload artifact: '+p)
    for p in ['docs/reviews/reliability-independent-algebra.json','docs/reviews/reliability-local-rehearsal.json','docs/reviews/reliability-table-generation.json','docs/literature/reliability-source-review.json','docs/reviews/reliability-exact-replay.json']:
        check=bind(p)
        if check['status']!='pass' or not all(check.get('checks',{}).values()):issues.append('Failed local check: '+p)
    # Verify exact inherited scientific bytes against the preserved assessed V7.
    receipt=read('docs/program/history/v7-preservation-receipt.json');archive=receipt['archive'];inputs+=['docs/program/history/v7-preservation-receipt.json',archive]
    if digest(archive)!=receipt['sha256']:issues.append('V7 archive changed')
    with zipfile.ZipFile(ROOT/archive) as z:
        manifest=json.loads(z.read('docs/program/reconstruction-delivery-manifest.json'));bound={r['path']:r for r in manifest['artifacts']}
    claims=read('docs/literature/reconstruction-claims.json');inherited=[]
    for claim in claims:
        for p in claim.get('artifacts',[]):
            inputs.append(p)
            if not claim['id'].startswith('E-R'):
                unchanged=p in bound and digest(p)==bound[p]['sha256'];inherited.append(dict(claim=claim['id'],path=p,unchanged_v7=unchanged))
                if not unchanged:issues.append('Changed inherited scientific evidence: '+p)
    old=read('docs/reviews/closure-verification.json');inputs.append('docs/reviews/closure-verification.json')
    editorial={'docs/causal_foundations.tex','docs/sponsor_reconstruction.tex','docs/literature/reconstruction-claims.json'}
    for p,h in old['input_sha256'].items():
        inputs.append(p)
        if p not in editorial and digest(p)!=h:issues.append('Changed inherited verification input: '+p)
    inputs+=['docs/literature/reconstruction-claims.json','docs/literature/sources.json','docs/reconstruction/22_reliability.tex','contracts/reliability.md','docs/program/external-validation-v8.md']
    runtime={name:version(name) for name in ('numpy','scipy','jax','jaxlib','scikit-learn','threadpoolctl')}
    result=dict(status='pass' if not issues else 'fail',issues=issues,verified_journal_requests=21251,inherited_artifacts=inherited,runtime_versions_observed=runtime,
        scope='Current input/journal/count/summary and inherited-byte verification, not independent review or general coverage. Negative scientific findings are retained; passing identity/algebra does not make them qualified.')
    save('docs/reviews/reliability-verification.json',result,inputs);print(json.dumps(dict(status=result['status'],issues=issues,verified_journal_requests=result['verified_journal_requests'])));raise SystemExit(bool(issues))

if __name__=='__main__':main()

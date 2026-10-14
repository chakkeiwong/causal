#!/usr/bin/env python3
"""Reconstruct new study summaries and require current execution bindings."""
import hashlib,json,math,statistics
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]


def read(name):return json.loads((ROOT/name).read_text())
def digest(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()


def main():
    issues=[];inputs={};summaries={}
    def require(ok,message):
        if not ok:issues.append(message)
    def bind(name):
        require((ROOT/name).is_file(),'Missing '+name)
        if (ROOT/name).is_file():inputs[name]=digest(name)
    def close(a,b,label,tol=1e-9):require(np.allclose(a,b,rtol=tol,atol=tol),label)
    def receipt(name):
        r=read(name);bind(name);require(r.get('mode','final')=='final','Pilot substituted: '+name)
        require(r.get('status','pass')=='pass','Failed receipt: '+name)
        for p,h in r.get('input_sha256',{}).items():bind(p);require(inputs.get(p)==h,'Stale executed input: '+name+' -> '+p)
        return r
    names=['dynamic-funding-results','dynamic-servicing-diagnose-results','dynamic-servicing-latent-results','dynamic-servicing-audit-results','dynamic-servicing-diagnostics-results','dynamic-discovery-results','dynamic-observation-results','dynamic-public-results','dynamic-product-results']
    studies={name:receipt('docs/studies/'+name+'.json') for name in names}
    exact=receipt('docs/reviews/dynamic-scientific-checks.json');require(all(exact['checks'].values()),'Failed finite scientific check')
    for key,error in exact['errors'].items():require(error<exact['tolerances'][key],'Failed numerical check '+key)
    oracle=receipt('docs/reviews/dynamic-graph-oracle.json');require(oracle['independent_dseparation_comparisons']==240 and not oracle['mismatches'],'Oracle separator comparison')
    # Funding: reconstruct from saved estimates, not stored coverage flags.
    funding=studies['dynamic-funding-results'];truth=np.array(funding['truth']);ftruth=funding['financial_truth'];coverage=[]
    from scipy.stats import norm
    for case in funding['results']:
        rows=case['runs'];s=case['summary'];require(len(rows)==funding['spec']['repetitions'],'Funding replication count')
        covered=[abs(np.array(r['estimate'])-truth)<=1.95996398454*np.array(r['se']) for r in rows]
        close(np.mean(covered,axis=0),s['marginal_coverage'],'Funding marginal coverage')
        joint=[np.all(abs(np.array(r['estimate'])-truth)<=norm.ppf(1-.05/(2*len(truth)))*np.array(r['se'])) for r in rows]
        close(np.mean(joint),s['joint_coverage'],'Funding joint coverage')
        count=sum(abs(r['financial_value']-ftruth)<=1.95996398454*r['financial_se'] for r in rows)
        close(count/len(rows),s['financial_coverage'],'Funding financial coverage');coverage.append(s)
        require(rows[0]['direct_statsmodels']['maximum_estimate_error']<1e-10 and rows[0]['direct_statsmodels']['maximum_variance_error']<1e-10,'Matched statsmodels funding')
    summaries['funding']=coverage
    def check_value(rows,s,truth,key):
        valid=[r for r in rows if r['available']];require(len(rows)==s['requested'] and len(valid)==s['available'],'Servicing denominator')
        count=sum(r[key]['interval'][0]<=truth<=r[key]['interval'][1] for r in valid)
        close(count/len(rows),s['coverage_all'],'Servicing all-request coverage');close(count/len(valid),s['coverage_given_available'],'Servicing conditional coverage')
        close(statistics.mean(r[key]['estimate'] for r in valid)-truth,s['bias_available'],'Servicing bias')
    audit=studies['dynamic-servicing-audit-results']
    for case in audit['results']:
        require(len(case['runs'])==audit['spec']['repetitions'],'Audit replication count')
        check_value(case['runs'],case['fixed_summary'],audit['fixed_truth'],'fixed');check_value(case['runs'],case['dynamic_summary'],audit['dynamic_truth'],'dynamic')
    latent=studies['dynamic-servicing-latent-results'];check_value(latent['runs'],latent['summary'],latent['fixed_truth'],'fixed')
    require(len(latent['runs'])==latent['spec']['latent_followup_repetitions'],'Latent follow-up replication count')
    diagnosis=studies['dynamic-servicing-diagnose-results'];require(all(abs(r['value_reconstruction_error'])<1e-10 for r in diagnosis['boundary_reconstructions']),'Exact V5 boundary reconstruction')
    retained=diagnosis['retained'];bind(retained['source']);require(inputs[retained['source']]==retained['source_sha256'],'Retained V5 identity')
    sensitivity=studies['dynamic-servicing-diagnostics-results'];require(sensitivity['common_problem']['history_dependent_action_cases'],'Policy is genuinely history-dependent')
    close(np.mean([r['covered'] for r in sensitivity['audit_error']['runs']]),sensitivity['audit_error']['coverage'],'Audit-error coverage')
    summaries['servicing']={'audit':[{k:v for k,v in case.items() if k!='runs'} for case in audit['results']],'latent':latent['summary'],'common_information_comparison':sensitivity['common_problem']}
    discovery=studies['dynamic-discovery-results'];require(len(discovery['runs'])==discovery['spec']['repetitions'],'Graph replication count')
    # Recompute graph metrics with the independent explicit ancestry truth.
    for row in discovery['runs']:
        graph=row['graph'];truthg=discovery['truth']['graph'];ancestry=discovery['truth']['ancestry'];tp=fp=fn=claims=wrong=0
        for i in range(len(graph)):
            for j in range(i+1,len(graph)):
                predicted=bool(graph[i][j]);actual=bool(truthg[i][j]);tp+=predicted and actual;fp+=predicted and not actual;fn+=actual and not predicted
                if predicted:
                    for mark,a,b in [(graph[i][j][0],i,j),(graph[i][j][2],j,i)]:
                        if mark in ('-','<','>'):claims+=1;wrong+=not actual or bool(ancestry[a][b])!=(mark=='-')
        require([tp,fp,fn,claims,wrong]==[row['score'][k] for k in ['true_positive','false_positive','false_negative','definite_endpoint_claims','wrong_definite_endpoints']],'Graph target/endpoint arithmetic')
    summaries['discovery']=discovery['summary']
    obs=studies['dynamic-observation-results']
    for case in obs['results']:
        rows=case['runs'];s=case['summary'];require(len(rows)==obs['spec']['repetitions'],'Observation replication count')
        valid=[r for r in rows if r['status']=='computed'];require(len(valid)==s['available'],'Mapping availability')
        for name,point,se in [('coverage_joint','financial','se'),('coverage_fixed','financial','fixed_calibration_se'),('coverage_naive','naive_financial','naive_se')]:
            close(sum(abs(r[point]-obs['financial_truth'])<=1.95996398454*r[se] for r in valid)/len(rows),s[name],'Mapping '+name)
    require(any(r['wrong_acceptance'] for r in obs['fixtures']),'False semantic assertion case retained');require(obs['rank_failure']=='unavailable_mapping_rank','Singular map refusal')
    product=studies['dynamic-product-results'];groups={}
    for run in product['runs']:
        bind(run['path']);require(inputs[run['path']]==run['sha256'],'Changed workload result');row=read(run['path']);require(all(row['checks'].values()),'Failed product semantic checks')
        require(row['maximum_reference_error']<1e-6 and row['result']['maximum_worker_numeric_threads']==1,'Partition/source reference or thread limit')
        groups.setdefault(row['dates'],[]).append(row)
        close(np.array(row['application_consumer']['interval_per_account'])*480000,row['treasury_consumer']['interval_currency'],'Consumer interval unit conversion')
    for size,rows in groups.items():
        for row in rows:
            close(row['result']['response'],rows[0]['result']['response'],'Same-data partition response');close(row['result']['covariance'],rows[0]['result']['covariance'],'Same-data partition covariance')
            require(row['result']['identity']==rows[0]['result']['identity'],'Physical worker count changed scientific identity')
    require(len(product['runs'])==len(product['spec']['workloads'])*len(product['spec']['workers'])*product['spec']['repetitions'],'Complete workload grid')
    public=studies['dynamic-public-results'];require(public['source_rows']==203 and len(public['results'])==4,'Public design/snapshot')
    require(max(r['maximum_direct_error'] for r in public['results'])<1e-10,'Public matched software covariance')
    for pattern in ['docs/literature/dynamic-*','docs/reviews/dynamic-source-excerpts/*','docs/literature/runtime-dynamic/*','docs/studies/dynamic-*-spec.json','docs/studies/observation-fixtures-v6.json']:
        for p in ROOT.glob(pattern):
            if p.is_file():bind(str(p.relative_to(ROOT)))
    ledger=read('docs/literature/dynamic-decision-ledger.json')
    for p,h in ledger['input_sha256'].items():bind(p);require(inputs[p]==h,'Stale literature inspection binding '+p)
    sources={r['id']:r for r in read('docs/literature/sources.json')}
    for d in ledger['decisions']:
        for key in d['primary']+d['challengers']:require(key in sources,'Unregistered method-decision source '+key)
    for key in ['guha2022','conformal2022','runtime_statsmodels_dynamic','public_macrodata_dynamic','fed_h8_dynamic','runtime_networkx_dynamic']:
        s=sources[key];bind(s['local_path']);require(inputs[s['local_path']]==s['sha256'],'Dynamic source hash '+key)
        for a in s.get('artifacts',[]):bind(a['path']);require(inputs[a['path']]==a['sha256'],'Dynamic source child hash '+key)
    bind('tools/verify_dynamic.py')
    result={'status':'pass' if not issues else 'fail','issues':issues,'reconstructed':summaries,'input_sha256':inputs,
        'scope':'Current executed inputs, all retained replication summaries, finite identities, source/operation evidence and composition arithmetic; not independent proof review or bank validation'}
    (ROOT/'docs/reviews/dynamic-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'inputs':len(inputs),'issues':issues},indent=2));raise SystemExit(bool(issues))


if __name__=='__main__':main()

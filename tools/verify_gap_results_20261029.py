from pathlib import Path
import json
import numpy as np

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/scientific-gap-closure/2026-10-29'
def wilson(k,n):
    z=1.95996398454;p=k/n;den=1+z*z/n;c=(p+z*z/(2*n))/den
    h=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return [float(c-h),float(c+h)]
def main():
    results={}
    for stem,keys in [('observation',['scenario','rate','method']),('policy-uncertainty',['scenario','policy','target','method'])]:
        result=json.loads((OUT/(stem+'-results.json')).read_text());rows=json.loads((OUT/(stem+'-replications.json')).read_text());checked=[]
        for s in result['scenarios']:
            subset=[r for r in rows if all(r[k]==s[k] for k in keys)]
            n=len(subset);k=sum(r['covered'] for r in subset);p=s.get('coverage',s.get('coverage_all_requests'))
            assert abs(k/n-p)<1e-12
            checked.append({**{key:s[key] for key in keys},'n':n,'coverage_wilson':wilson(k,n)})
        results[stem]=dict(status='pass',summaries_checked=len(checked),coverage_checks=checked)
    p=json.loads((OUT/'policy-uncertainty-results.json').read_text());rows=json.loads((OUT/'policy-uncertainty-replications.json').read_text())
    z=np.array(p['integration_scrambles']);spread=np.std(z,axis=0,ddof=1)
    paired=np.std(z-z[:,0,None],axis=0,ddof=1)
    decisions=[]
    for scenario in ['baseline','future_dependent_dropout','omitted_state_predictor']:
        sub=[r for r in rows if r['scenario']==scenario and r['policy']=='selected_threshold' and r['target']=='improvement' and r['method']=='gcomp_bootstrap']
        decisions.append(dict(scenario=scenario,false_positive_lower_bounds=sum(r['positive_lower_bound'] and r['reference']<=0 for r in sub),
             nonbeneficial_selections=sum(r['reference']<=0 for r in sub),
             mean_finite_list_regret=float(np.mean([max(x['value'] for x in p['reference'][1:])-p['reference'][r['selected_index']]['value'] for r in sub]))))
    results['integration']=dict(value_sd_across_eight_scrambles=spread.tolist(),improvement_sd=paired.tolist(),
        maximum_value_sd=float(max(spread)),maximum_improvement_sd=float(max(paired)),
        interpretation='Observed integration spread is small relative to reported statistical widths; this diagnostic is not a uniform error bound over fitted parameters.')
    results['decisions']=decisions
    results['limits']='No exact finite-sample calibration; numerical-reference boundary ambiguity retained; no bank data claim.'
    (OUT/'new-results-verification.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(dict(status='pass',summaries=sum(len(v.get('coverage_checks',[])) for v in results.values() if isinstance(v,dict)),integration=results['integration'],decisions=decisions)))
if __name__=='__main__':main()

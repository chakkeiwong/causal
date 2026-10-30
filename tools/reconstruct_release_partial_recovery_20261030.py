"""Reconstruct retained Bernoulli-invitation results without regenerating data."""
from pathlib import Path
from fractions import Fraction as F
import csv,hashlib,io,json,math,statistics
import numpy as np
from scipy.stats import norm
R=Path(__file__).resolve().parents[1]
B=R/'docs/release/2026-10-29';O=B/'partial-recovery-073'
bindings={}
def raw(name):
    p=R/name;v=p.read_bytes();bindings[name]=hashlib.sha256(v).hexdigest();return v
def read(name):return json.loads(raw(name))
def close(a,b):assert np.allclose(a,b,atol=1e-10,rtol=1e-10),(a,b)
def reconstruct():
    base='docs/twelve-hour-closure/2026-10-29/partial-recovery-attempt-1/'
    mu=[F(9,20),F(11,20)];routine=[[F(4,5),F(2,5)],[F(2,5),F(4,5)]]
    laws={'standard':[[F(1,10),F(9,10)],[F(9,10),F(1,5)]],
          'intensive':[[F(4,5),F(49,50)],[F(49,50),F(4,5)]],
          'complete':[[F(1),F(1)],[F(1),F(1)]],
          'unstable':[[F(1),F(1)],[F(1),F(1)]]}
    results={};count=0;diagnostics=0;enumerated=0
    for regime,law in laws.items():
        old=read(base+regime+'/population.json');arms=[]
        for a in [0,1]:
            # Enumerate every outcome/response/completion type with exact masses.
            types=[]
            for y in [0,1]:
                for r in [0,1]:
                    for s in [0,1]:
                        mass=(mu[a] if y else 1-mu[a])*(routine[a][y] if r else 1-routine[a][y])*(law[a][y] if s else 1-law[a][y])
                        reported=F(1,2) if regime=='unstable'and a==1 and y==0 else F(y)
                        types.append((mass,y,r,s,reported))
            assert sum(v[0]for v in types)==1
            observed=sum(p*r for p,y,r,s,z in types);oy=sum(p*r*y for p,y,r,s,z in types)
            recovered=sum(p*(1-r)*s for p,y,r,s,z in types);ry=sum(p*(1-r)*s*z for p,y,r,s,z in types)
            unresolved=1-observed-recovered;lower=oy+ry;upper=lower+unresolved
            values=dict(mu=mu[a],observed=observed,observed_y=oy,recovered=recovered,recovered_y=ry,unresolved=unresolved,lower=lower,upper=upper,completecase=oy/observed,naive=oy+(1-observed)*ry/recovered)
            for key,v in values.items():close(float(v),old['arms'][a][key])
            for q in [F(1,10),F(1,4),F(1,2),F(1)]:
                el=eu=F(0)
                for p,y,r,s,z in types:
                    for b in [0,1]:
                        pb=q if b else 1-q
                        lo=r*y+(1-r)*b*s*z/q
                        hi=r*y+(1-r)*(1-b*s*(1-z)/q)
                        el+=p*pb*lo;eu+=p*pb*hi
                        assert 0<=lo<=1/q and 1-1/q<=hi<=1
                        enumerated+=1
                assert el==lower and eu==upper
            arms.append(values)
        low=arms[1]['lower']-arms[0]['upper'];up=arms[1]['upper']-arms[0]['lower']
        assert up-low==sum(x['unresolved']for x in arms)
        for side in ['lower','upper']:
            fills=[int((side=='lower'and a==0)or(side=='upper'and a==1))for a in [0,1]]
            means=[ar['observed_y']+ar['recovered_y']+fill*ar['unresolved']for ar,fill in zip(arms,fills)]
            assert means[1]-means[0]==(low if side=='lower'else up)
        close([float(low),float(up)],[old['lower'],old['upper']])
        rr=list(csv.DictReader(io.StringIO(raw(base+regime+'/replications.csv').decode())));assert len(rr)==2000
        for row in rr:
            for k in row:
                row[k]=row[k]=='True' if row[k]in['True','False']else float(row[k])
            q=row['q'];t=math.sqrt(math.log(40)/(2000*q*q));close(t,row['hoeffding_radius'])
            hl=max(-1,row['lower']-t);hu=min(1,row['upper']+t)
            nl=max(-1,row['lower']-norm.ppf(.975)*row['se_lower']);nu=min(1,row['upper']+norm.ppf(.975)*row['se_upper'])
            for k,v in dict(hoeffding_lower=hl,hoeffding_upper=hu,normal_lower=nl,normal_upper=nu).items():close(v,row[k])
            for m,l,u in [('hoeffding',hl,hu),('normal',nl,nu)]:
                assert row[m+'_covers_truth']==(l<=.1<=u)
                assert row[m+'_covers_region']==(l<=float(low)and u>=float(up))
            assert row['crossing_raw']==(row['lower']>row['upper'])
        prior=read(base+regime+'/result.json');cells=[]
        for q in [.1,.25,.5,1.]:
            group=[r for r in rr if r['q']==q];assert len(group)==500
            expected=next(s for s in prior['summaries']if s['q']==q)
            for key in ['lower','upper','se_lower','se_upper','invitations','recoveries','naive','complete_case']:
                vals=[r[key]for r in group];close(statistics.mean(vals),expected['mean_'+key]);close(statistics.stdev(vals)/math.sqrt(500),expected[key+'_mcse'])
            flags=['hoeffding_covers_truth','normal_covers_truth','hoeffding_covers_region','normal_covers_region','positive_hoeffding','positive_normal','negative_normal','crossing_raw']
            for key in flags:
                p=sum(r[key]for r in group)/500;close(p,expected[key]);close(math.sqrt(p*(1-p)/500),expected[key+'_mcse'])
            widths={};empty={}
            for m in ['normal','hoeffding']:
                signed=[r[m+'_upper']-r[m+'_lower']for r in group]
                close(statistics.mean(signed),expected[m+'_mean_width'])
                widths[m]=statistics.mean(max(0,w)for w in signed);empty[m]=sum(w<0 for w in signed)
            positive_nonempty={m:sum(r[m+'_lower']>0 and r[m+'_lower']<=r[m+'_upper']for r in group)for m in ['normal','hoeffding']}
            cells.append(dict(q=q,n=500,counts={k:sum(r[k]for r in group)for k in flags},set_mean_width=widths,empty_sets=empty,positive_nonempty=positive_nonempty,mean_invitations=expected['mean_invitations'],mean_recoveries=expected['mean_recoveries'],mean_naive=expected['mean_naive'],naive_mcse=expected['naive_mcse']))
        for rep in [0,249,499]:
            with np.load(io.BytesIO(raw(base+regime+f'/data-{rep}.npz')))as d:
                for q in [.1,.25,.5,1.]:
                    estimates=[];vars=[]
                    for a in [0,1]:
                        y=d[f'a{a}_y'];r=d[f'a{a}_r'];s=d[f'a{a}_s'];u=d[f'a{a}_u'];z=d[f'a{a}_reported'];rec=(~r)&s&(u<q)
                        # Direct observed-cell sums and squares, independent of runner masks.
                        n=len(y);sy=float(y[r].sum());sz=float(z[rec].sum());n0=int((~r).sum());nr=int(rec.sum())
                        ls=sy+sz/q;us=sy+n0-(nr-sz)/q
                        l2=sy+sz/q**2;u2=sy+n0+(nr-sz)*((1-1/q)**2-1)
                        estimates.append((ls/n,us/n));vars.append(((l2-ls*ls/n)/(n-1),(u2-us*us/n)/(n-1)))
                    row=next(r for r in rr if r['q']==q and r['rep']==rep)
                    close([estimates[1][0]-estimates[0][1],estimates[1][1]-estimates[0][0]],[row['lower'],row['upper']])
                    close([math.sqrt((vars[1][0]+vars[0][1])/2000),math.sqrt((vars[1][1]+vars[0][0])/2000)],[row['se_lower'],row['se_upper']]);diagnostics+=1
        results[regime]=dict(population={k:str(v)for k,v in dict(lower=low,upper=up,width=up-low,naive=arms[1]['naive']-arms[0]['naive'],completecase=arms[1]['completecase']-arms[0]['completecase']).items()},cells=cells)
        count+=len(rr)
    gamma=F(27,76);assert F(47,200)-F(19,50)*gamma==F(1,10)
    decision={name:[str(100*F(x['population']['lower'])-5),str(100*F(x['population']['upper'])-5)]for name,x in results.items()}
    return dict(status='pass',retained_rows=count,independent_datasets=2000,raw_endpoint_and_variance_checks=diagnostics,exact_invitation_cells=enumerated,regimes=results,required_stability_gamma=str(gamma),illustrative_net_intervals_usd=decision,finite_sample_proof='With independent scores of range1/q_a, centered endpoint log mgf <=s^2 D/8, D=sum_a1/(n_a q_a^2). Chernoff gives exp(-2t^2/D) per adverse tail. Union two tails at t=sqrt(D log(2/alpha)/2) covers both population endpoints. Clipping to[-1,1] preserves coverage. This statement requires historical-outcome stability; unstable regime targets a different recorded mean.',scope='Retained-data and exact-law reconstruction, not native attrition execution or new simulation. Width of an empty confidence set is0; original signed-width summaries remain preserved and separately matched.',bindings=bindings)
def main():
    x=reconstruct();O.mkdir(exist_ok=True);(O/'exact-witnesses.json').write_text(json.dumps(x,indent=2)+chr(10));print(json.dumps({k:x[k]for k in ['status','retained_rows','independent_datasets','raw_endpoint_and_variance_checks','exact_invitation_cells']}))
if __name__=='__main__':main()

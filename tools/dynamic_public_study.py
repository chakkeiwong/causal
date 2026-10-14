#!/usr/bin/env python3
"""Preserved public financial time series and explicit design sensitivity."""
import hashlib,json,sys,inspect,shutil,importlib.metadata
from pathlib import Path
import numpy as np
import statsmodels.api as sm
import statsmodels.datasets.macrodata as macro
from statsmodels.stats.sandwich_covariance import cov_hac
from threadpoolctl import threadpool_limits
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from causalbank.responses import bartlett_lrv


def main():
    path=ROOT/'docs/studies/dynamic-public-spec.json';spec=json.loads(path.read_text());folder=ROOT/'docs/literature/runtime-dynamic';folder.mkdir(exist_ok=True)
    origin=Path(inspect.getfile(macro)).parent/'macrodata.csv';copy=folder/'macrodata.csv';shutil.copyfile(origin,copy)
    sourcefile=Path(inspect.getfile(macro)).parent/'data.py';shutil.copyfile(sourcefile,folder/'macrodata-source.py')
    (folder/'statsmodels-cov-hac.txt').write_text(inspect.getsource(cov_hac))
    (folder/'macrodata-notes.txt').write_text(macro.TITLE+'\n'+macro.SOURCE+'\n'+macro.NOTE)
    dist=importlib.metadata.distribution('statsmodels');(folder/'statsmodels-metadata.txt').write_text(dist.read_text('METADATA') or '')
    data=macro.load_pandas().data;money=100*np.log(data['m1'].to_numpy());growth=np.diff(money,prepend=np.nan);rate=np.diff(data['tbilrate'].to_numpy(),prepend=np.nan);gdp=100*np.diff(np.log(data['realgdp'].to_numpy()),prepend=np.nan);infl=data['infl'].to_numpy();features=np.column_stack((rate,growth,gdp,infl));origins=np.arange(3,len(data)-max(spec['horizons']));results=[]
    with threadpool_limits(limits=1):
        for variant in spec['variants']:
            t=origins.copy()
            if variant=='pre_1984':t=t[data['year'].to_numpy()[t]<1984]
            if variant=='post_1984':t=t[data['year'].to_numpy()[t]>=1984]
            x=np.column_stack([np.ones(len(t)),rate[t]]+[features[t-l] for l in range(1,spec['lags']+1)]+([np.column_stack((gdp[t],infl[t]))] if variant=='current_output_inflation_controls' else []))
            coefficients=[];ses=[];errors=[]
            for horizon in spec['horizons']:
                y=money[t+horizon]-money[t-1];coef=np.linalg.lstsq(x,y,rcond=None)[0];u=y-x@coef;bread=np.linalg.inv(x.T@x/len(t));influence=(x*u[:,None])@bread;cov=bartlett_lrv(influence,spec['bandwidth'])/len(t)
                direct=sm.OLS(y,x).fit();dcov=cov_hac(direct,nlags=spec['bandwidth'],use_correction=False)
                coefficients.append(float(coef[1]));ses.append(float(np.sqrt(cov[1,1])));errors.append(max(float(abs(direct.params-coef).max()),float(abs(dcov-cov).max())))
            results.append({'variant':variant,'origins':len(t),'first':[int(data.iloc[t[0]].year),int(data.iloc[t[0]].quarter)],'last_origin':[int(data.iloc[t[-1]].year),int(data.iloc[t[-1]].quarter)],'estimate':coefficients,'se':ses,'maximum_direct_error':max(errors)})
    files=[path,Path(__file__),ROOT/'src/causalbank/responses.py',*sorted(folder.iterdir())];receipt={'spec':spec,'results':results,'source_rows':len(data),'source_sha256':hashlib.sha256(copy.read_bytes()).hexdigest(),'causal_status':'unresolved_policy_information_and_observation_clock','input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
    (ROOT/'docs/studies/dynamic-public-results.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(results,indent=2))


if __name__=='__main__':main()

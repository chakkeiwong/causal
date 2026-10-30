"""Public archived-contact prediction; deliberately distinguish unavailable data."""
from hashlib import sha256
import importlib.metadata
import json
from pathlib import Path
import time
import warnings

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, log_loss, brier_score_loss
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from threadpoolctl import threadpool_limits

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/scientific-synthesis/2026-10-29'


def main():
    start=time.monotonic();raw=(OUT/'public-timing-plan.json').read_bytes();plan=json.loads(raw)
    source=ROOT/plan['data'];assert sha256(source.read_bytes()).hexdigest()==plan['sha256']
    df=pd.read_csv(source,sep=';');y=(df['y']=='yes').astype(int).to_numpy()
    df['no_previous_contact']=(df.pdays==999).astype(int)
    df['pdays']=df.pdays.where(df.pdays!=999,0)
    n=len(df);cut=int(.7*n);indices=np.arange(n)
    random_train,random_test=train_test_split(indices,test_size=.3,stratify=y,random_state=20261029)
    splits=[('ordered_archive',indices[:cut],indices[cut:]),('random_development',random_train,random_test)]
    features=plan['candidate_pre_call_features']+['no_previous_contact']
    results=[]
    with threadpool_limits(limits=1):
        for split,train,test in splits:
            for method,columns in [('constant',[]),('candidate_pre_call',features),('plus_unavailable_duration',features+['duration'])]:
                warn=[];unseen={};iterations=None
                if method=='constant':p=np.repeat(y[train].mean(),len(test))
                else:
                    numeric=[c for c in columns if pd.api.types.is_numeric_dtype(df[c])]
                    categorical=[c for c in columns if c not in numeric]
                    unseen={c:int((~df.iloc[test][c].isin(df.iloc[train][c].unique())).sum()) for c in categorical}
                    preprocessing=ColumnTransformer([('numbers',StandardScaler(),numeric),
                        ('categories',OneHotEncoder(handle_unknown='ignore'),categorical)])
                    model=make_pipeline(preprocessing,LogisticRegression(C=1,solver='lbfgs',max_iter=2000))
                    with warnings.catch_warnings(record=True) as notices:
                        warnings.simplefilter('always');model.fit(df.iloc[train][columns],y[train]);p=model.predict_proba(df.iloc[test][columns])[:,1]
                    warn=[str(w.message) for w in notices];iterations=model[-1].n_iter_.tolist()
                top_count=int(np.ceil(.1*len(test)))
                top=np.argsort(-p,kind='stable')[:top_count]
                results.append({'split':split,'model':method,'train_rows':len(train),'test_rows':len(test),
                    'train_subscription_rate':float(y[train].mean()),'test_subscription_rate':float(y[test].mean()),
                    'auc':float(roc_auc_score(y[test],p)),'log_loss':float(log_loss(y[test],p)),
                    'brier':float(brier_score_loss(y[test],p)),
                    'top_decile_records':top_count,'top_decile_subscriptions':int(y[test][top].sum()),
                    'top_decile_rate':float(y[test][top].mean()),
                    'tie_rule':'stable test-order; constant ranking has no targeting interpretation',
                    'train_indices_sha256':sha256(np.asarray(train,dtype='<i8').tobytes()).hexdigest(),
                    'test_indices_sha256':sha256(np.asarray(test,dtype='<i8').tobytes()).hexdigest(),
                    'unseen_category_counts':unseen,'warnings':warn,'iterations':iterations})
    output={'date':'2026-10-29','plan_sha256':sha256(raw).hexdigest(),'code_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
        'data':{'path':plan['data'],'sha256':plan['sha256'],'rows':n},
        'versions':{x:importlib.metadata.version(x) for x in ['numpy','pandas','scikit-learn','scipy']},
        'results':results,'seconds':round(time.monotonic()-start,3),
        'claim':'Actual public-data prediction; no causal effect or deployable pre-call model is established'}
    (OUT/'public-timing-results.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))


if __name__=='__main__':main()

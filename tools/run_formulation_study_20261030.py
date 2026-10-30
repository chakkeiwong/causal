"""Exact observational-equivalence example; no model or source code executed."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib,json,time

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/twelve-hour-closure/2026-10-29/formulation-attempt-1'

def prob(x,p):return p if x else 1-p

def confounded(intervene=None):
    table={(f,y):F(0) for f,y in product(range(2),repeat=2)}
    for u,ef,ey in product(range(2),repeat=3):
        w=F(1,2)*prob(ef,F(1,5))*prob(ey,F(1,5))
        f=(u^ef) if intervene is None else intervene
        y=(1-u)^ey
        table[f,y]+=w
    return table

def causal(intervene=None):
    table={(f,y):F(0) for f,y in product(range(2),repeat=2)}
    for z,e in product(range(2),repeat=2):
        w=F(1,2)*prob(e,F(8,25))
        f=z if intervene is None else intervene
        y=(1-f)^e
        table[f,y]+=w
    return table

def outcome(table):return sum(p for (f,y),p in table.items() if y)
def risk(table,f):return table[f,1]/sum(p for (ff,y),p in table.items() if ff==f)
def string_table(table):return [{'F':f,'Y':y,'probability':str(p)} for (f,y),p in sorted(table.items())]

def main():
    start=time.monotonic();OUT.mkdir(parents=True,exist_ok=False)
    try:
        a=confounded();b=causal()
        expected={(0,0):F(4,25),(0,1):F(17,50),(1,0):F(17,50),(1,1):F(4,25)}
        assert a==b==expected and sum(a.values())==1
        text=lambda f,y:f'Constraint indicator {f}; export participation {y}.'
        at={text(f,y):p for (f,y),p in a.items()};bt={text(f,y):p for (f,y),p in b.items()}
        assert at==bt
        effects={}
        for name,law in [('confounded',confounded),('causal',causal)]:
            r0=outcome(law(0));r1=outcome(law(1))
            assert sum(law(0).values())==sum(law(1).values())==1
            effects[name]={'do_0':str(r0),'do_1':str(r1),'tightening_effect':str(r1-r0),
                           'relief_effect':str(r0-r1)}
        assert effects['confounded']['tightening_effect']=='0'
        assert effects['causal']['tightening_effect']=='-9/25'
        assert risk(a,0)==F(17,25) and risk(a,1)==F(8,25)
        # Independent algebra: disagreement in two Bernoulli errors occurs
        # with 2*p*(1-p); risk(Y=1|F=1) equals that probability.
        p=F(1,5);disagreement=2*p*(1-p)
        assert disagreement==F(8,25)==risk(a,1)
        result={'status':'pass','kind':'project_exact_counterexample','observed_joint':string_table(a),
          'observational_risks':{'F0':str(risk(a,0)),'F1':str(risk(a,1)),
            'difference':str(risk(a,1)-risk(a,0))},'interventions':effects,
          'text_channel_identical':True,'independent_algebra_agrees':True,
          'unit':'probability of export participation in stipulated model',
          'bounds':'Only the two displayed worlds; not sharp bounds over all compatible models',
          'native_model_evaluation':False,'source_empirical_reproduction':False,
          'seconds':round(time.monotonic()-start,5)}
        (OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
        files=[Path(__file__),ROOT/'docs/twelve-hour-closure/2026-10-29/formulation-study-plan.md',OUT/'results.json']
        (OUT/'manifest.json').write_text(json.dumps({'files':[{'path':str(x.relative_to(ROOT)),
         'sha256':hashlib.sha256(x.read_bytes()).hexdigest()} for x in files]},indent=2)+'\n')
        print(json.dumps(result))
    except Exception as e:
        (OUT/'failure.json').write_text(json.dumps({'error':repr(e),'seconds':time.monotonic()-start})+'\n')
        raise

if __name__=='__main__':main()

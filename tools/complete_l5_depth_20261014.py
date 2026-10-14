#!/usr/bin/env python3
"""Preserve L5 depth findings and develop exact estimation/composition references."""
import argparse
from contextlib import redirect_stdout
from fractions import Fraction as F
import json
from pathlib import Path
import re

import build_native_evaluation_reader_v3_20261014 as engine
import build_integrated_monograph_v12 as shared
import master_control as core
from publish_latent_r_review_v2_20261013 import write, transition, verify_bindings

ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-14/l5-depth'
OUT=BASE/'reader'
OLD=ROOT/'docs/causal_proposal_longitudinal_workflow_2026-10-14.tex'
NAME='causal_proposal_longitudinal_review_2026-10-14'
DRIVER=ROOT/'docs'/(NAME+'.tex')
PDF=DRIVER.with_suffix('.pdf')
PRIOR=ROOT/'docs/program/execution/2026-10-14/l5-workflow/publication/reader/source-audit.json'
ADDITION=BASE/'estimation-composition.tex'
REVIEWER={'name':'Codex author/coordinator','kind':'author'}
ref=shared.ref

def num(x):
    return {'exact':str(x),'decimal':float(x)}

def calculate():
    value=F(474,5)
    def augmented(p0,p1,q,errors):
        pieces=[F(0),F(0),q]
        for a0 in (0,1):
            risk=F(2,5) if a0 else F(4,5)
            for l in (0,1):
                lp=risk if l else 1-risk
                e=F(3,4) if l else F(1,2)
                for a1 in (0,1):
                    p=F(1,2)*lp*(e if a1 else 1-e)
                    y=F(100-40*l+2*a0+(30*l-8)*a1)
                    w0=1/p0 if a0==1 else F(0)
                    w1=1/p1[l] if a1==l else F(0)
                    m=F(100-40*l+2*a0+(30*l-8)*l)+errors[l]
                    pieces[0]+=p*w0*w1*(y-m)
                    pieces[1]+=p*w0*(m-q)
        return pieces
    errors=[F(0),F(5)]
    pieces=augmented(F(2,5),[F(1,2),F(1,2)],value+3,errors)
    rho0=F(5,4)
    formula=(1-rho0)*3+rho0*(F(2,5)*(1-F(3,2))*5)
    assert sum(pieces)-value==formula==F(-2)
    correct_assignment=sum(augmented(F(1,2),[F(1,2),F(3,4)],value+3,errors))
    correct_outcomes=sum(augmented(F(2,5),[F(1,2),F(1,2)],value,[F(0),F(0)]))
    assert correct_assignment==correct_outcomes==value
    treated=[F(1,4),F(3,4)]
    control=[F(3,4),F(1,4)]
    drift=[F(2),F(10)]
    effect=[F(4),F(8)]
    treated_change=sum(p*(d+t) for p,d,t in zip(treated,drift,effect))
    control_change=sum(p*d for p,d in zip(control,drift))
    att=sum(p*t for p,t in zip(treated,effect))
    standardized=sum(p*d for p,d in zip(treated,drift))
    propensity=[treated[i]/(treated[i]+control[i]) for i in range(2)]
    weights=[e/(1-e) for e in propensity]
    weight_mean=sum(p*w for p,w in zip(control,weights))
    weighted=sum(p*w*d for p,w,d in zip(control,weights,drift))/weight_mean
    assert treated_change==15 and control_change==4 and att==7
    assert weighted==standardized==8 and weight_mean==1
    raw=F(196,100)**2*F(16688,25)/F(4,5)**2
    n=(raw.numerator+raw.denominator-1)//raw.denominator
    assert n==4007
    return {'scope':'Exact fixed-nuisance population calculation and stipulated panel; no fitted coverage or bank qualification',
        'sequential':{'true_value':num(value),'augmented_components':list(map(num,pieces)),
            'misspecified_value':num(sum(pieces)),'bias':num(formula),
            'correct_assignment_value':num(correct_assignment),'correct_outcomes_value':num(correct_outcomes)},
        'panel':{'treated_change':num(treated_change),'pooled_control_change':num(control_change),
            'pooled_difference':num(treated_change-control_change),'target_att':num(att),
            'standardized_control':num(standardized),'weighted_control':num(weighted),
            'propensities':list(map(num,propensity)),'control_weights':list(map(num,weights)),
            'cost':num(F(6)),'net_att':num(att-6),'naive_net':num(treated_change-control_change-6)},
        'planning':{'variance':num(F(16688,25)),'normal_multiplier':num(F(49,25)),
            'tolerance':num(F(4,5)),'continuous_size':num(raw),'rounded_size':n,
            'achieved_interval_or_trial_size':False}}

def checkpoint():
    old=json.loads((ROOT/'docs/program/execution/2026-10-14/l5-workflow/publication/reader/build-report.json').read_text())
    credits=[(.25,'Decision translation overlaps L2; keep only the cross-path contract.'),
      (.5,'Observation applicability and clock distinctions; retrieval/discovery overlap discounted.'),
      (.5,'Identification and estimator handoff; repeated package and OCI examples discounted.'),
      (.75,'Longitudinal functional and regime clock; shared assumptions discounted.'),
      (0,'Package/framework comparison allocated to software and architecture chapters.'),
      (0,'Permission, recovery and reporting allocated to architecture/integration/evaluation.'),
      (.5,'New servicing law on a partial page; repeated economic recap excluded.'),
      (1,'Policy values, biased matching and transition averaging.'),
      (1,'Retention correction, centered score and exact moments.'),
      (.75,'Stage robustness/support and panel target; generic caution discounted.'),
      (1,'Cohort contrasts, aggregation, exact TWFE and counterfactual ambiguity.'),
      (1,'Observation selection, framed estimator and label inversion.'),
      (.75,'Label uncertainty and dependence; shared assistant framing discounted.'),
      (.5,'Restricted longitudinal interface and matched alternatives; adjacent CausalEval excluded.')]
    assert sum(c for c,r in credits)==8.5
    review={'status':'needs_development','reviewer':REVIEWER,'operation_id':'TEXT.REVIEW.L5',
      'reviewed_reader':old['pdf'],'allocation':{'min':10,'target':11,'max':12},
      'substantive_page_credit':8.5,'first_printed_page':396,'last_reviewed_page':409,
      'per_page':[{'printed_page':396+i,'credit':c,'rationale':r} for i,(c,r) in enumerate(credits)],
      'excluded':'Printed410–423: later data/code/architecture inserts; no L5 credit.',
      'findings':['Longitudinal/panel/observation coverage is present, but overlaps prevent claiming the minimum10 pages.',
          'The population score must be developed into an explicit nuisance-error calculation.',
          'Conditional panel targets need a worked composition-adjusted comparison.'],
      'evidence':[ref(PRIOR,'515 unchanged source identities'),ref(OLD.with_suffix('.pdf'),'Exact reviewed700-page reader')],
      'next_action':'Develop independent misspecification and composition oracles; integrate a preserving successor, inspect text and measure depth again.',
      'visual_acceptance':False}
    if (BASE/'depth-review-predecessor.json').exists():
        assert json.loads((BASE/'depth-review-predecessor.json').read_text())==review
    else:
        write(BASE/'depth-review-predecessor.json',review)
    note={'scope':'Actual preliminary content/depth review; repair remains active',
      'reviewer':REVIEWER,'findings':review['findings'],
      'finding':'The conservative review awards8.5 pages, below the minimum10; two substantive derivations are required.',
      'evidence':[ref(BASE/'depth-review-predecessor.json','Conservative8.5-page negative depth finding')],
      'next_action':review['next_action']}
    write(BASE/'progress-schema-repair.json',{'status':'repaired','action':'TEXT.REVIEW.L5 progress',
      'failure':'Controller rejected the first note: progress requires finding, next_action, evidence.',
      'preserved_attempt':ref(BASE/'progress.json','Failed note omitted singular finding; no state mutation'),
      'repair':'A successor adds the required finding; the scientific review is unchanged.'})
    write(BASE/'progress-v2.json',note)
    transition('progress','TEXT.REVIEW.L5',BASE/'progress-v2.json')

def prepare():
    assert not DRIVER.exists()
    write(BASE/'plan-review.json',{'status':'pass','reviewer':REVIEWER,
      'plan':['Preserve the negative depth finding and all delivered bytes.',
        'Derive and independently enumerate a fixed-component sequential-score remainder.',
        'Develop conditional panel standardization/weighting and its monetary consequence.',
        'Compile, source-audit and measure the exact successor; no automatic depth or visual acceptance.'],
      'review_findings':['The two additions address missing derivations rather than repeat workflow framing.',
          'Known-law planning is distinguished from achieved coverage; no nuisance-rate or panel-premise guarantee is invented.',
          'Author review can proceed while LFS publication and rendered-image review remain separate.']})
    result=calculate()
    write(BASE/'exact-oracle.json',result)
    record=engine.source('exec14_workflow_remainder','Exact sequential nuisance-error and conditional panel composition references',
        'Causal banking proposal','project_derivation','Project-authored finite servicing and branch laws','2026-10-14',
        BASE/'exact-oracle.json','Sequential components/bias; corrected assignment/outcome values; panel target/composition; planning scale',
        ['Fixed-nuisance bias−2 and mean92.8; both correct assignment or outcome components restore94.8.',
         'Conditional ATT7 versus pooled11; weighted/standardized control8 and net margin1 versus5.',
         'Known-law normal planning4007 units; not achieved confidence coverage.'],
        [{'local_copy':ref(Path(__file__),'calculate(): independent observational enumeration and exact algebra')}])
    write(BASE/'source-audit.json',{'cutoff':'2026-10-07','sources':[record],
      'prior':ref(PRIOR,'Preserved515-source reader audit'),
      'primary_support':ref(ROOT/'docs/program/execution/2026-10-14/l5-workflow/primary-review.json','Inspected longitudinal/panel primary support'),
      'limits':['Population algebra is a project derivation; generic nuisance-rate and bank sampling validity remain conditional.']})
    (BASE/'refs.bib').write_text('@misc{exec14_workflow_remainder,\n author={{Causal banking proposal}},\n title={Exact sequential nuisance-error and conditional panel composition references},\n year={2026},\n note={Project finite laws and exact enumeration; 14 October 2026}\n}\n')
    chapter=BASE/'chapter.tex'
    chapter.write_text('\\input{program/comprehensive-v14/work/TEXT.DRAFT.L5/chapter.tex}\n\\input{program/execution/2026-10-14/l5-depth/estimation-composition.tex}\n')
    text=OLD.read_text()
    marker=r'\input{program/comprehensive-v14/work/TEXT.DRAFT.L5/chapter.tex}'
    assert text.count(marker)==1
    text=text.replace(marker,r'\input{program/execution/2026-10-14/l5-depth/chapter.tex}')
    text=re.sub(r'\\bibliography\{([^}]+)\}',lambda m:r'\bibliography{'+m.group(1)+',program/execution/2026-10-14/l5-depth/refs}',text)
    DRIVER.write_text(text)
    write(BASE/'prepared-inputs.json',{'inputs':[ref(p,'Reviewed preserving input') for p in
      [OLD,PRIOR,ADDITION,chapter,BASE/'refs.bib',BASE/'source-audit.json',BASE/'exact-oracle.json',
       BASE/'depth-review-predecessor.json',BASE/'plan-review.json',Path(__file__)]],
      'generated':[ref(DRIVER,'Preserving driver')],'visual_acceptance':False})
    print(json.dumps({'prepared':str(DRIVER.relative_to(ROOT)),'exact_oracle':'pass','prior_depth_credit':8.5}))

def build():
    for k,v in {'BASE':BASE,'OUT':OUT,'OLD':OLD,'NAME':NAME,'DRIVER':DRIVER,'PDF':PDF,'PRIOR_AUDIT':PRIOR}.items():
        setattr(engine,k,v)
    with (BASE/'bounded-build-summary.txt').open('w') as log, redirect_stdout(log):
        engine.build()
    print(json.dumps({k:json.loads((OUT/'build-report.json').read_text())[k] for k in ['pages','pdf','cited_records']}))

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('command',choices=['checkpoint','prepare','build'])
    a=p.parse_args(); {'checkpoint':checkpoint,'prepare':prepare,'build':build}[a.command]()

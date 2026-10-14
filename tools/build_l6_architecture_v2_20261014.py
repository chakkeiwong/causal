#!/usr/bin/env python3
"""Preserve the seven-page depth finding and develop a substantive successor."""
import argparse
from contextlib import redirect_stdout
from fractions import Fraction as F
import json
from pathlib import Path
import re

import audit_reader_traceability_v2_20261013 as trace
import build_l6_architecture_20261014 as prior
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = prior.ROOT
BASE = prior.BASE / 'v2'
OUT = BASE / 'reader'
OLD = prior.OLD
PRIOR = prior.PRIOR
NAME = 'causal_proposal_agent_backends_v2_2026-10-14'
DRIVER = ROOT / 'docs' / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
CHAPTER = prior.CHAPTER.with_name('chapter-v2.tex')
REVIEWER = prior.REVIEWER


def calculate():
    # None denotes an infinite endpoint, interpreted according to its position.
    def affine(intervals, a, b):
        a,b=F(a),F(b)
        assert a != 0
        mapped=[]
        for lo,hi in intervals:
            left=None if lo is None else a*F(lo)+b
            right=None if hi is None else a*F(hi)+b
            mapped.append((left,right) if a>0 else (right,left))
        mapped.sort(key=lambda pair: float('-inf') if pair[0] is None else pair[0])
        return mapped
    def serial(intervals):
        return [[None if x is None else str(x) for x in pair]for pair in intervals]
    union=[(None,F(-2)),(F(3),None)]
    line=[(None,None)]
    def hull(intervals):
        return [(intervals[0][0],intervals[-1][1])]
    assert hull(union)==hull(line) and union!=line
    assert affine(union,1,-1)==[(None,F(-3)),(F(2),None)]
    assert affine(union,-1,0)==[(None,F(-3)),(F(2),None)]
    assert affine([(2,5)],1,-1)==[(F(1),F(4))]
    assert affine([(2,5)],-1,0)==[(F(-5),F(-2))]
    assert affine([(2,5)],F(1,1000),0)==[(F(1,500),F(1,200))]
    assert affine([],1,-1)==[] and affine(line,-1,2)==line
    a0,a1,b0,b1=map(F,[10,8,7,6])
    df=((a1-a0)+(b1-b0))/2
    db=((b0-a0)+(b1-a1))/2
    inter=(b1-b0)-(a1-a0)
    assert df==F(-3,2) and db==F(-5,2) and inter==1 and df+db==b1-a0==-4
    routes={'A':{'assigned':100,'returned':90,'correct':81},
            'B':{'assigned':100,'returned':60,'correct':57}}
    for r in routes.values():
        r['wrong']=r['returned']-r['correct'];r['unanswered']=r['assigned']-r['returned']
        r['conditional_correct']=str(F(r['correct'],r['returned']))
        r['assigned_correct']=str(F(r['correct'],r['assigned']))
        r['loss_unanswered3']=10*r['wrong']+3*r['unanswered']
        r['loss_unanswered1']=10*r['wrong']+r['unanswered']
    assert [routes[x]['loss_unanswered3']for x in ['A','B']]==[120,150]
    assert [routes[x]['loss_unanswered1']for x in ['A','B']]==[100,70]
    return {'kind':'exact_project_representation_and_factorial_examples',
            'set_images':{'original_union':serial(union),'whole_line':serial(line),'common_hull':serial(hull(union)),
                          'net_union':serial(affine(union,1,-1)),'reversed_union':serial(affine(union,-1,0)),
                          'bounded_net':serial(affine([(2,5)],1,-1)),
                          'bounded_reverse':serial(affine([(2,5)],-1,0)),
                          'thousands':serial(affine([(2,5)],F(1,1000),0)),
                          'empty':serial(affine([],1,-1))},
            'factorial':{'means':dict(zip(['A0','A1','B0','B1'],map(str,[a0,a1,b0,b1]))),
                         'framework_contrast':str(df),'backend_contrast':str(db),
                         'interaction':str(inter),'diagonal_contrast':str(b1-a0)},
            'availability':routes,
            'limitations':['All effect sets, costs, losses and counts are stipulated, not estimated from bank/model data.',
                           'Fixed-map coverage argument requires valid input coverage and a known bijective map; no original calibration claim.',
                           'Factorial identification/uncertainty requires its own assignment, missingness and task-sampling law.',
                           'No new backend/framework code executed.']}


def prepare():
    assert not BASE.exists() and not DRIVER.exists() and not CHAPTER.exists()
    verify_bindings(json.loads((prior.BASE/'prepared-inputs.json').read_text()))
    assert prior.calculate()==json.loads((prior.BASE/'exact-results.json').read_text())
    BASE.mkdir()
    original=(prior.BASE/'development.tex').read_text()
    corrected=original.replace(r'\cite{',r'\citep{')
    corrected=corrected.replace(r'.\citep{',r'. \citep{')
    (BASE/'development.tex').write_text(corrected)
    write(BASE/'exact-results.json',calculate())
    write(BASE/'repair-review.json',{'status':'prepared','reviewer':REVIEWER,
          'prior_attempt':ref(prior.PDF,'726-page attempt retained, not released'),
          'depth_finding':ref(prior.BASE/'depth-review-predecessor.json','Seven credited pages versus minimum ten'),
          'repairs':['Separate new citations from preceding sentences; use parenthetical citations.',
                     'Develop information-loss and affine-set preservation arguments with exact cases.',
                     'Develop matched backend/framework contrasts and availability-loss comparisons.'],
          'new_source':ref(prior.BASE/'adapter-comparison.tex','Developed successor argument'),
          'original_development':ref(prior.BASE/'development.tex','Preserved original new exposition'),
          'corrected_development':ref(BASE/'development.tex','Citation-format successor'),
          'implemented_product_change':False,'visual_acceptance':False})
    record=prior.engine.source('exec14_l6_adapter_exact',
        'Exact adapter set images, information loss and matched architecture contrasts',
        'Causal banking proposal','project_derivation',
        'Project-authored set transformations and factorial/count examples','2026-10-14',
        BASE/'exact-results.json','Set images, hull collision, four-cell mean contrasts and availability losses',
        ['Exact images preserve set meaning under fixed known transforms; lossy hull cannot be inverted uniquely.',
         'Factorial means10/8/7/6 give framework contrast−1.5, backend−2.5 and interaction1.',
         'Stipulated unanswered losses change the preferred route:120/150 versus100/70.'],
        [{'local_copy':ref(Path(__file__).resolve(),'calculate(): exact Fraction and tagged-set comparisons')},
         {'local_copy':ref(prior.BASE/'adapter-comparison.tex','Proof premises and connected banking exposition')}])
    audit=json.loads((prior.BASE/'source-audit.json').read_text())
    audit['sources'].append(record)
    audit['repair']=ref(BASE/'repair-review.json','Preserved depth/format finding and reviewed successor')
    write(BASE/'source-audit.json',audit)
    (BASE/'refs.bib').write_text((prior.BASE/'refs.bib').read_text()+
        '@misc{exec14_l6_adapter_exact,\n author={{Causal banking proposal}},\n title={Exact adapter set images, information loss and matched architecture contrasts},\n year={2026},\n note={Exact project examples; 14 October 2026}\n}\n')
    CHAPTER.write_text('\\input{program/execution/2026-10-14/l6-architecture/v2/development.tex}\n'+
        '\\input{program/execution/2026-10-14/l6-architecture/adapter-comparison.tex}\n'+
        '\\input{program/execution/2026-10-14/l6-architecture/prototype-body.tex}\n'+
        '\\par The local implementation and historical conformance counts in this chapter are bound to the preserved source, original trials and subsequent six-case replay. They do not constitute new provider execution. \\citep{exec14_l6_local}\n'+
        '\\label{exec14:l6-end}\n')
    text=OLD.read_text()
    marker=r'\input{program/repair-v12/work/LA05/chapter-draft.tex}'
    assert text.count(marker)==1
    text=text.replace(marker,r'\input{program/comprehensive-v14/work/TEXT.DRAFT.L6/chapter-v2.tex}')
    text=re.sub(r'\\bibliography\{([^}]+)\}',lambda m:r'\bibliography{'+m.group(1)+
                ',program/execution/2026-10-14/l6-architecture/v2/refs}',text)
    DRIVER.write_text(text)
    write(BASE/'prepared-inputs.json',{'inputs':[ref(p,'Preserved or reviewed source')for p in [
         OLD,PRIOR,prior.PROTOTYPE,prior.BASE/'prepared-inputs.json',prior.BASE/'depth-review-predecessor.json',
         prior.BASE/'adapter-comparison.tex',BASE/'repair-review.json',BASE/'exact-results.json',Path(__file__).resolve()]],
         'generated':[ref(p,'Successor input')for p in [DRIVER,CHAPTER,BASE/'development.tex',BASE/'source-audit.json',BASE/'refs.bib']],
         'preservation':'All inherited chapter bytes retained except an exact prototype-body relocation; prior attempt preserved.',
         'credit_policy':'Substantive depth requires explicit review; physical span is not credit.',
         'visual_acceptance':False})
    print(json.dumps({'prepared':str(DRIVER.relative_to(ROOT)),'new_examples':'pass','prior_depth':7}))


def build():
    for name,value in {'BASE':BASE,'OUT':OUT,'OLD':OLD,'NAME':NAME,
                       'DRIVER':DRIVER,'PDF':PDF,'PRIOR_AUDIT':PRIOR}.items():
        setattr(prior.engine,name,value)
    with (BASE/'compile-summary.log').open('x')as stream:
        with redirect_stdout(stream):prior.engine.build()
    report=json.loads((OUT/'build-report.json').read_text())
    aux=(OUT/(NAME+'.aux')).read_text()
    report.update(builder=ref(Path(__file__).resolve(),'Preserving depth/format successor'),
       predecessor_pdf=ref(OLD.with_suffix('.pdf'),'Frozen719-page working reader'),
       chapter_sections={name:int(re.search(r'\\newlabel\{exec14:'+name+
            r'\}\{\{[^}]*\}\{(\d+)\}',aux).group(1))for name in ['l6','l6-extension-end','l6-adapter','l6-factorial','l6-adapter-end','l6-end']})
    prior.engine.core.write(OUT/'build-report.json',report)
    result=trace.audit(DRIVER,OUT/'source-audit.json')
    write(BASE/'traceability-review.json',result)
    assert result['status']=='pass' and not result['issues']
    print(json.dumps({'pages':report['pages'],'cited_records':report['cited_records'],
                      'chapter_sections':report['chapter_sections'],'scholarly_pdfs':result['scholarly_pdfs'],
                      'material_warnings':[w for w in report['warnings']if 'Underfull'not in w]}))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['prepare','build']);args=parser.parse_args()
    prepare()if args.command=='prepare'else build()

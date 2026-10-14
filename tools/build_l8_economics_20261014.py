#!/usr/bin/env python3
"""Build the integrated banking economics chapter with preserved source records."""
import argparse
from contextlib import redirect_stdout
import json
from pathlib import Path
import re

import audit_reader_traceability_v2_20261013 as trace
import build_native_evaluation_reader_v3_20261014 as engine
import l8_economics_examples_20261014 as examples
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = engine.ROOT
BASE = ROOT/'docs/program/execution/2026-10-14/l8-economics'
OUT = BASE/'reader'
OLD = ROOT/'docs/causal_proposal_python_temporal_v3_2026-10-14.tex'
PRIOR = ROOT/'docs/program/execution/2026-10-14/python-temporal/v3/reader/source-audit.json'
NAME = 'causal_proposal_banking_economics_2026-10-14'
DRIVER = ROOT/'docs'/(NAME+'.tex')
PDF = DRIVER.with_suffix('.pdf')
CHAPTER = ROOT/'docs/program/comprehensive-v14/work/TEXT.DRAFT.L8/chapter.tex'
REVIEWER = {'name':'Codex author/coordinator','kind':'author'}
BS, NL = chr(92), chr(10)
LIMITS = [
    'Author proposal development and exact project planning constructions; no measured bank ROI.',
    'All new costs, losses, populations, state probabilities and pilot quality are stipulated.',
    'Conditional probabilities are not inferred from language-model confidence or repeated agreement.',
    'Published usability and benchmark evidence retains its original task, population and protocol limits.',
    'No new model calls, external package execution, bank sample or implemented decision policy.',
    'Authentic deployment weights, prices, assignments and owner acceptance are conditional later inputs.',
    'Current manuscript depth is reviewed separately; rendered visual acceptance remains open.',
]


def prepare():
    assert not DRIVER.exists() and not CHAPTER.exists() and not (BASE/'source-audit.json').exists()
    result = examples.calculate()
    write(BASE/'exact-results.json',result)
    old_review = json.loads((ROOT/'docs/program/execution/2026-10-14/evaluation-cost/primary-review.json').read_text())
    rereads=[]
    for key,pages,claims in [
        ('v12_la_2410_14146',[10,11,12],[
            'Three expert sessions and concerns about citations are qualitative evidence, not causal adoption effects.',
            'Six students used fixed stages and selected edges; edge-editing means3.3 and0.9 minutes do not establish a bank productivity effect.']),
        ('v12_la_2607_08093',[10,11],[
            'The100-scene exam reports distinct content/abstention/numerical outcomes and tool/token trajectories.',
            'Reported nominal95% ATE coverage uses7 eligible cases per model or5 for one; token totals do not determine bank cost.']),
    ]:
        paper=next(p for p in old_review['papers'] if p['id']==key)
        verify_bindings(paper)
        extracts=[ref(BASE/'inspected'/(key+'-page-'+str(p)+'.txt'),'Inspected physical PDF page'+str(p)) for p in pages]
        rereads.append({'citation_key':key,'inherited_identity':paper,'inspected_pages':extracts,'supported_claims_here':claims})
    feng=next(p for p in old_review['papers'] if p['id']=='v12_la_2407_19638')
    verify_bindings(feng)
    rereads.append({'citation_key':feng['id'],'inherited_identity':feng,
        'inspected_pages':[ref(ROOT/'docs/program/execution/2026-10-14/l7-benchmarking/inspected/feng-page-9.txt','Conclusion and explicit accessible-corpus/commonsense limits')],
        'supported_claims_here':['The study does not identify an error law for all closed models or complex dynamic banking tasks.']})
    write(BASE/'primary-review.json',{'reviewer':REVIEWER,'status':'reviewed','cutoff':'2026-10-07',
        'inspected_at':'2026-10-14','new_acquisitions':0,'papers':rereads,'limitations':LIMITS})
    write(BASE/'derivation-review.json',{'status':'pass','reviewer':REVIEWER,
        'evidence':[ref(BASE/'exact-results.json','Exact calculations'),ref(ROOT/'tools/l8_economics_examples_20261014.py','Rational arithmetic and independent full-path enumeration')],
        'findings':[
            'Request-level loss includes errors, all requests, fallback and delay; conditional accuracy alone does not rank value.',
            'Tail-sum and full latent/transient path enumeration agree for capped retries; correctness remains separate from a passed format check.',
            'Funding ambiguity, deterministic regret and randomized regret have distinct decision rules; confidence sets are not posterior laws.',
            'Joint policy values preserve a ranking destroyed by a Cartesian coordinate enlargement.',
            'Pilot value includes the existing build option, signal-contingent stopping, current cost and delayed value; branch and threshold calculations verified.',
            'Deployment mixture can reverse a public advantage even with unchanged within-stratum savings.'],
        'financial_claim':'All prices, probabilities and losses are exposed assumptions; no empirical or vendor-value claim.',
        'limitations':LIMITS})
    design=ROOT/'docs/program/execution/2026-10-14/four-journeys/acceptance-cases.json'
    verify_bindings(json.loads(design.read_text()))
    sources=[]
    for key,title,kind,path,anchor,claims,records in [
        ('exec14_l8_economics','Exact banking workflow loss, retry, ambiguity and prototype option examples',
         'project_derivation',BASE/'exact-results.json','All seven exposed scenario groups',
         ['Full request-level loss and review thresholds','Capped retry under persistent failure','Set-valued policy choice and joint-value information',
          'Delayed pilot option and information thresholds','Deployment-mixture value reversal'],
         [ref(BASE/'derivation-review.json','Author mathematical review'),ref(ROOT/'tools/l8_economics_examples_20261014.py','Reproducible exact construction')]),
        ('exec14_l8_design','Banking journey prototype decisions and conditional evidence requirements',
         'project_design',design,'Four independent public/generated routes and later owner inputs',
         ['Distinct prototype acceptance cases for funding, servicing, discovery and observation construction',
          'Bank truth, actual prices and institutional acceptance follow justified prototype work',
          'Known engineering routes do not establish universal hidden-state or temporal-graph inference'],
         [ref(ROOT/'docs/program/execution/2026-10-14/four-journeys/reconciliation.json','Existing local evidence and scientific boundaries'),
          ref(BASE/'plan-review.md','Reviewed chapter scope'),ref(BASE/'primary-review.json','Reread primary evidence and limits')]),
    ]:
        sources.append({'integrated_citation_key':key,'title':title,'author':'Causal banking proposal','kind':kind,'year':2026,
            'source_identity':'Project-authored '+kind+'; '+str(path.relative_to(ROOT)), 'version_date':'2026-10-14; exact bytes bound by SHA-256',
            'local_copy':ref(path,anchor),'inspected_anchors':[anchor],'supported_claims':claims,
            'records':[{'local_copy':r} for r in records],'limitations':LIMITS})
    write(BASE/'source-audit.json',{'cutoff':'2026-10-07','sources':sources,
        'primary_rereads':ref(BASE/'primary-review.json','Three genuine primary works; inherited identities retained'),
        'prior':ref(PRIOR,'601 preserved citation records'),'post_cutoff_project_work':True})
    bib=[]
    for s in sources:
        bib.append('@misc{'+s['integrated_citation_key']+','+NL+' author={{Causal banking proposal}},'+NL+
                   ' title={'+engine.shared.escape(s['title'])+'},'+NL+' year={2026},'+NL+
                   ' note={'+engine.shared.escape(s['version_date'])+'}'+NL+'}'+NL)
    (BASE/'refs.bib').write_text(NL.join(bib))
    preserved=['program/repair-v12/work/LA07/economics-chapter.tex',
               'program/execution/2026-10-14/native-evaluation-reader/v3/cost-development.tex']
    CHAPTER.parent.mkdir(parents=True)
    CHAPTER.write_text(NL.join(BS+'input{'+p+'}' for p in preserved+[str((BASE/'development.tex').relative_to(ROOT/'docs'))])+NL)
    book=OLD.read_text()
    marker=NL.join(BS+'input{'+p+'}' for p in preserved)
    assert book.count(marker)==1
    book=book.replace(marker,BS+'input{'+str(CHAPTER.relative_to(ROOT/'docs'))+'}')
    pattern=re.compile(re.escape(BS+'bibliography{')+'([^}]+)'+re.escape('}'))
    assert len(pattern.findall(book))==1
    book=pattern.sub(lambda m:BS+'bibliography{'+m.group(1)+',program/execution/2026-10-14/l8-economics/refs}',book)
    DRIVER.write_text(book)
    write(BASE/'prepared-inputs.json',{'inputs':[ref(p,'Reviewed preserving input') for p in [OLD,PRIOR,BASE/'primary-review.json',BASE/'derivation-review.json',Path(__file__)]],
        'generated':[ref(p,'Integrated successor source') for p in [DRIVER,CHAPTER,BASE/'development.tex',BASE/'refs.bib',BASE/'source-audit.json']],
        'credit_policy':'No duplicate credit for existing mathematical examples, general evaluation plans or adjacent chapters.', 'visual_acceptance':False})
    print(json.dumps({'prepared':str(DRIVER.relative_to(ROOT)),'new_records':2,'primary_rereads':3}))


def build():
    for name,value in {'BASE':BASE,'OUT':OUT,'OLD':OLD,'NAME':NAME,'DRIVER':DRIVER,'PDF':PDF,'PRIOR_AUDIT':PRIOR}.items():
        setattr(engine,name,value)
    with (BASE/'compile-summary.log').open('x') as stream:
        with redirect_stdout(stream):engine.build()
    report=json.loads((OUT/'build-report.json').read_text())
    aux=(OUT/(NAME+'.aux')).read_text()
    def page(label):
        return int(re.search(re.escape(BS+'newlabel{'+label+'}{{')+'[^}]*'+re.escape('}{')+'([0-9]+)',aux).group(1))
    report.update(builder=ref(Path(__file__),'Preserving banking economics builder'),predecessor_pdf=ref(OLD.with_suffix('.pdf'),'Frozen773-page reader'),
        chapter_sections={label:page(label) for label in ['la:economics','exec14:l8-development','exec14:l8-retry','exec14:l8-ambiguity',
                                                        'exec14:l8-option','exec14:l8-transfer','exec14:l8-research','exec14:l8-development-end']})
    engine.core.write(OUT/'build-report.json',report)
    audited=trace.audit(DRIVER,OUT/'source-audit.json');write(BASE/'traceability-review.json',audited)
    assert audited['status']=='pass' and not audited['issues'] and audited['scholarly_pdfs']==172
    assert report['cited_records']==603
    print(json.dumps({'pages':report['pages'],'cited_records':report['cited_records'],'sections':report['chapter_sections'],
                      'scholarly_pdfs':audited['scholarly_pdfs'],'material_warnings':[w for w in report['warnings'] if 'Underfull' not in w]}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','build']);a=p.parse_args()
    {'prepare':prepare,'build':build}[a.command]()

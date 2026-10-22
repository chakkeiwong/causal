#!/usr/bin/env python3
"""Preserve the reader while integrating primary factuality and weighted-target reviews."""
import argparse
import json
from pathlib import Path
import re
import build_network_commercial_reader_20261020 as engine
import weighted_target_reference_20261022 as exact
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write

ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'docs'
BASE=DOCS/'program/execution/2026-10-22/factuality-weighted-reader-v1/publication-v2';OUT=BASE/'reader'
CENSUS=DOCS/'program/execution/2026-10-22/census-factuality-weighted-v1'
PREDECESSOR=DOCS/'program/execution/2026-10-22/sensitivity-iv-reader-v1'
OLD=DOCS/'causal_proposal_sensitivity_iv_reviewed_2026-10-22.tex'
PRIOR=PREDECESSOR/'reader/source-audit.json'
NAME='causal_proposal_factuality_targets_reviewed_v2_2026-10-22'
DRIVER=DOCS/(NAME+'.tex');PDF=DRIVER.with_suffix('.pdf')
DEVELOPMENT=BASE/'targets-development.tex';FACTUALITY_DEVELOPMENT=BASE/'factuality-development.tex'
LABELS=['exec22:targets-'+s for s in ['scope','definition','experiment','class','value','wrong','geometry','bound','ci','point','set']]
LABELS+=['exec22:fact-scope']
read=lambda p:json.loads(p.read_text())


def expected_driver():
    text=OLD.read_text()
    for marker,source in [
      (r'\input{program/execution/2026-10-13/formulation.tex}',DEVELOPMENT),
      (r'\input{program/execution/2026-10-22/census-domain-knowledge-v1/development.tex}',FACTUALITY_DEVELOPMENT)]:
        assert text.count(marker)==1
        text=text.replace(marker,marker+'\n'+r'\input{'+str(source.relative_to(DOCS))+'}')
    return re.sub(r'\\bibliography\{([^}]+)\}',lambda m:r'\bibliography{'+m.group(1)+','+str((BASE/'refs').relative_to(DOCS))+'}',text)


def configure():
    for name in ['ROOT','DOCS','BASE','OUT','PREDECESSOR','OLD','PRIOR','NAME','DRIVER','PDF','DEVELOPMENT','LABELS']:
        setattr(engine,name,globals()[name])
    engine.exact=exact;engine.expected_driver=expected_driver


def prepare():
    configure();assert not DRIVER.exists() and not PDF.exists() and not OUT.exists()
    evidence=[]
    for name in ['source-audit.json','review.json','conversion-contract.json','exact-results.json','census-register.json','task-map.json']:
        verify_bindings(read(CENSUS/name));evidence.append(ref(CENSUS/name,'Reviewed primary-source continuation'))
    assert exact.calculate()==read(CENSUS/'exact-results.json')
    records=read(CENSUS/'source-audit.json')['sources'];assert len(records)==3
    for record in records:
        if record['kind']=='paper':record['filename_title']=record['title']
    evidence.append(ref(BASE.parent/'schema-failure.json','Preserved failed audit and exact schema correction'))
    write(BASE/'source-audit.json',dict(sources=records,cutoff='2026-10-07',source_reviews=evidence))
    write(BASE/'exact-results.json',exact.calculate())
    write(BASE/'plan-review.json',dict(status='pass',evidence=[ref(BASE/'integration-plan.md','Reviewed preserving integration plan')],
      checks=['Preserve every earlier citation, context and manuscript input.',
        'Use only inspected pre-cutoff originals and separately labeled authored arithmetic.',
        'Explain fixed versus simultaneous targets, known covariance, feasible-class conditions and causal limits.',
        'Compile/text-check both additions and retain visual/final acceptance obligations.']))
    write(BASE/'review.json',dict(status='pass_for_connected_source_synthesis',evidence=evidence,
      findings=['Survey synthesis supports an evidence-workflow design, without inheriting unreviewed experimental results.',
        'Weighted-estimands theory helps specify business targets; it supplies no causal discovery or confounding repair.',
        'Exact and feasible guarantees, point versus set coverage and post-selection uses are distinguished.',
        'Public known-law/corpus studies are proposed before expensive bank experiments.'],
      visual_acceptance=False,native_execution=False))
    write(BASE/'mathematical-review.json',dict(status='pass_for_scoped_authored_derivations',issues=[],
      evidence=[ref(DEVELOPMENT,'Connected definitions, assumptions and derivations'),
        ref(ROOT/'tools/weighted_target_reference_20261022.py','Exact rational geometry and analytic normal coverage'),
        ref(BASE/'exact-results.json','Reproduced financial values and confidence budgets'),
        ref(CENSUS/'source-audit.json','Inspected theorem and proof anchors')],
      findings=['Normalized signed weights differ from simplex populations; group-effect identification is a separate condition.',
        'Convex mixing gives effect4-6epsilon/4+2epsilon and net3-6epsilon/3+2epsilon; threshold1/2 and alternative entry2/3 reproduce.',
        'Normal baseline variance5/8 and target shift4 produce analytic wrong-target coverage0.0009686482242958205.',
        'Centering eliminates the normalized-weight constant; Cauchy-Schwarz gives H times covariance-metric distance, attained at the stated example.',
        'H squared32, distance squared1/2 and minimax first weight7/12 reproduce.',
        'Proposition6 fixed-target andProposition7 simultaneous-set budgets yield90%/85% at.05/.05; one possible simultaneous95% allocation is.0125/.025.',
        'No noncentral-CDF inversion, folded-normal solver, empirical coverage or native equivalence is implemented here.'],
      native_execution=False,empirical_coverage=False))
    write(BASE/'copyedit-review.json',dict(status='pass',evidence=[ref(DEVELOPMENT,'Target narrative'),ref(FACTUALITY_DEVELOPMENT,'Factuality narrative')],
      findings=['Motivate each contribution with a banking decision, compatible units and explicit claim roles.',
        'Distinguish survey descriptions from independently reviewed experiments, autoregressive models from intervention claims, and source support from causal validity.',
        'Explain assumptions, alternatives, negative cases and public qualification routes without process records in the narrative.',
        'Keep ambiguous template publication details in source audit; cite authentic arXiv editions.'],rendered_review=False))
    write(BASE/'manuscript-plan-review.json',dict(status='pass',evidence=[ref(BASE/'plan-review.json','Reviewed integration')],
      checks=['Insert weighted-target analysis in formulation and factuality after domain-knowledge discussion.',
        'Retain every prior source object and compiled content hash.',
        'New content adds substantive target/class/coverage distinctions without assigning duplicate coverage credit.']))
    bib=[]
    for s in records:
        author=s['author'] if s['kind']=='paper' else '{'+engine.shared.escape(s['author'])+'}'
        note=(r'\url{'+s['source_identity']+'}; '+engine.shared.escape(s['version_date']) if s['source_identity'].startswith('https://') else engine.shared.escape(s['source_identity']+'; '+s['version_date']))
        bib.append('@misc{'+s['integrated_citation_key']+',\n author={'+author+'},\n title={'+engine.shared.escape(s['title'])+'},\n year={'+str(s['year'])+'},\n note={'+note+'}\n}\n')
    (BASE/'refs.bib').write_text('\n'.join(bib));DRIVER.write_text(expected_driver())
    entries=engine.sources()
    paths=[OLD,PRIOR,DEVELOPMENT,FACTUALITY_DEVELOPMENT,Path(__file__),
      ROOT/'tools/build_network_commercial_reader_20261020.py',ROOT/'tools/weighted_target_reference_20261022.py']
    paths += [BASE/n for n in ['integration-plan.md','source-audit.json','review.json','plan-review.json','mathematical-review.json','copyedit-review.json','manuscript-plan-review.json','exact-results.json']]
    write(BASE/'prepared-inputs.json',dict(inputs=[ref(p,'Reviewed preserving input') for p in paths],
      generated=[ref(DRIVER,'Preserving driver'),ref(BASE/'refs.bib','Audited additions')],
      prior_cited_records=len(read(PRIOR)['sources']),expected_cited_records=len(entries),
      expected_scholarly_pdfs=read(PREDECESSOR/'traceability-review.json')['scholarly_pdfs']+2,visual_acceptance=False))
    print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)),records=len(entries),scholarly_pdfs=221)))


def build():configure();engine.build()


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['prepare','build'])
    {'prepare':prepare,'build':build}[parser.parse_args().command]()

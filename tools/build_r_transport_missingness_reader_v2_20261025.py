#!/usr/bin/env python3
"""Preserve all prior sources and integrate the R transport and missingness component comparison."""
import argparse,json,re
from pathlib import Path
import build_preserving_reader_v2_20261024 as engine
import r_transport_missingness_reference_20261025 as exact
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'docs';BS=chr(92);NL=chr(10)
BASE=DOCS/'program/execution/2026-10-25/r-transport-missingness-reader-v2';OUT=BASE/'reader'
SOURCE=DOCS/'program/execution/2026-10-25/r-transport-missingness-v1'
PREDECESSOR=DOCS/'program/execution/2026-10-25/other-mediation-coverage-reader-v1'
OLD=DOCS/'causal_proposal_other_mediation_coverage_reviewed_v1_2026-10-25.tex';PRIOR=PREDECESSOR/'reader/source-audit.json'
NAME='causal_proposal_r_transport_missingness_reviewed_v2_2026-10-25';DRIVER=DOCS/(NAME+'.tex');PDF=DRIVER.with_suffix('.pdf');DEVELOPMENT=BASE/'development.tex'
LABELS=['sec:exec25-rtm'];read=lambda p:json.loads(p.read_text())

def expected_driver():
    text=OLD.read_text();marker=BS+'input{program/execution/2026-10-25/other-mediation-coverage-reader-v1/development.tex}';assert text.count(marker)==1
    text=text.replace(marker,marker+NL+BS+'input{'+str(DEVELOPMENT.relative_to(DOCS))+'}')
    start=text.index(BS+'bibliography{')+len(BS+'bibliography{');end=text.index('}',start)
    return text[:end]+','+str((BASE/'refs').relative_to(DOCS))+text[end:]

def expected_development():
    text=(SOURCE/'development.tex').read_text()
    return text.replace('{1'+BS+'over P(S=0)}',BS+'frac{1}{P(S=0)}').replace('{1-'+BS+'rho(X)'+BS+'over'+BS+'rho(X)}',BS+'frac{1-'+BS+'rho(X)}{'+BS+'rho(X)}').replace('{A'+BS+'over e(X)}',BS+'frac{A}{e(X)}').replace('{1-A'+BS+'over1-e(X)}',BS+'frac{1-A}{1-e(X)}')

def configure():
    for k in ['ROOT','DOCS','BASE','OUT','PREDECESSOR','OLD','PRIOR','NAME','DRIVER','PDF','DEVELOPMENT','LABELS','expected_driver']:setattr(engine,k,globals()[k])
    engine.exact=exact

def display_version(value):
    value=engine.shared.escape(value).replace('^',BS+'textasciicircum{}').replace(';','; ')
    return re.sub(r'[0-9a-f]{40}',lambda m:m.group(0)[:20]+BS+'allowbreak{}'+m.group(0)[20:],value)

def prepare():
    configure();assert not BASE.exists() and not DRIVER.exists()
    for p in [PRIOR,PREDECESSOR/'release-source-review-v2.json',SOURCE/'review.json',SOURCE/'source-audit.json']:verify_bindings(read(p))
    prior_records={s['integrated_citation_key']:s for s in read(PRIOR)['sources']};prior_count=len(prior_records);incoming=read(SOURCE/'source-audit.json')['sources'];added=sum(s['integrated_citation_key'] not in prior_records for s in incoming);assert all(prior_records[s['integrated_citation_key']]==s for s in incoming if s['integrated_citation_key'] in prior_records)
    assert prior_count==1346 and added==7 and exact.calculate()==read(SOURCE/'exact-results.json');BASE.mkdir()
    for name in ['development.tex','sponsor-addition.md','source-audit.json','exact-results.json','mathematical-review.json','copyedit-review.json','plan-review.json']:
        (BASE/name).write_bytes((SOURCE/('plan-review-v2.json' if name=='plan-review.json' else name)).read_bytes())
    original=(SOURCE/'development.tex').read_text();assert original.startswith(BS+'section[R transport and missingness contracts]{')
    DEVELOPMENT.write_text(expected_development())
    (BASE/'integration-plan.md').write_text('Preserve all1346 prior source records,citation contexts and content inputs. Add R population targets, selection odds, missingness, compatible imputation and pooling contracts; preserve all inherited comparisons. Keep coverage, native, visual and final acceptance open. Pair sponsor and reconcile all obligations.'+NL)
    bib=[]
    for s in read(BASE/'source-audit.json')['sources']:
        if s['integrated_citation_key'] in prior_records:continue
        bib.append(NL.join(['@misc{'+s['integrated_citation_key']+',',' author={'+(s['author'] if s['kind']=='paper' else '{'+engine.shared.escape(s['author'])+'}')+'},',' title={'+engine.shared.escape(s['title'])+'},',' year={'+str(s['year'])+'},',' note={'+display_version(s['version_date'])+'}','}']))
    (BASE/'refs.bib').write_text(NL.join(bib));DRIVER.write_text(expected_driver())
    paths=[OLD,PRIOR,Path(__file__),Path(exact.__file__),SOURCE/'review.json',PREDECESSOR/'release-source-review-v2.json']+[BASE/n for n in ['development.tex','source-audit.json','exact-results.json','mathematical-review.json','copyedit-review.json','plan-review.json','integration-plan.md']]
    write(BASE/'prepared-inputs.json',dict(inputs=[ref(p,'Reviewed input') for p in paths],generated=[ref(DRIVER,'Preserving driver'),ref(BASE/'refs.bib','Original R transport and missingness software source and authored comparison records')],prior_cited_records=prior_count,expected_cited_records=prior_count+added,expected_scholarly_pdfs=265,visual_acceptance=False))
    print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)),prior_records=prior_count,records=prior_count+added)))

def build():configure();engine.build()
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','build']);globals()[p.parse_args().command]()

#!/usr/bin/env python3
"""Build a preserving sponsor paired to the reviewed interference comparison reader."""
import argparse,json,re,subprocess
from pathlib import Path
import build_prophets_repository_sponsor_20261021 as engine
import build_interference_reuse_reader_20261024 as reader
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write
run,core,ROOT=engine.run,engine.core,reader.ROOT;DOCS=ROOT/'docs'
BASE=DOCS/'program/execution/2026-10-24/sponsor-interference-reuse-v1';OUT=BASE/'reader'
PRIOR=DOCS/'program/execution/2026-10-24/sponsor-backend-census-v1'
READER_BASE=reader.BASE;READER_PDF=reader.PDF;NAME='sponsor-proposal'
MIRROR=DOCS/'sponsor_proposal_interference_reuse_reviewed_2026-10-24.pdf'
read=lambda p:json.loads(p.read_text())

def manuscript(pages):
    text=(PRIOR/'proposal.md').read_text()
    prior_pages=read(DOCS/'program/execution/2026-10-24/backend-census-reader-v1/reader/build-report.json')['pages']
    assert text.count('1186 audited citation records')==1
    text=text.replace(f'{prior_pages:,} pages',f'{pages:,} pages').replace('1186 audited citation records','1189 audited citation records')
    marker='sp24backends_reader,sp24backends_progress';assert text.count(marker)==1
    text=text.replace(marker,marker+',sp24interference_reader,sp24interference_progress')
    assert 'The program has 294 recorded outcomes of 376' in text
    text=text.replace('The program has 294 recorded outcomes of 376','The program has 296 recorded outcomes of 376')
    old='reuse is 99 passing, three inconclusive and 13 open.';assert text.count(old)==1
    text=text.replace(old,'reuse is 101 passing, three inconclusive and 11 open.')
    marker='# Public evidence before expensive bank experiments';assert text.count(marker)==1
    addition=(READER_BASE/'sponsor-addition.md').read_text()
    addition=re.sub(r'\[@([^\]]+)\]',lambda m:chr(92)+'citep{'+m.group(1).replace('; @',',')+'}',addition)
    return text.replace(marker,addition+chr(10)*2+marker)

def prepare():
    assert not BASE.exists() and not MIRROR.exists();state=core.read(ROOT,core.STATE)
    assert state['execution_runtime']['active'] is None and run.same_reader(state['reader'],ref(READER_PDF,'Current reader'))
    verify_bindings(read(READER_BASE/'working-release.json'));BASE.mkdir();OUT.mkdir()
    progress=engine.snapshot(state);progress['census']=ref(DOCS/'program/execution/2026-10-24/census-judge-bias-v1/census-register.json','81 inspected and 32 unread originals of 113')
    write(BASE/'progress-evidence.json',progress);write(BASE/'economics-results.json',engine.economics.calculate())
    pages=state['reader']['pages'];(BASE/'proposal.md').write_text(manuscript(pages));prior=read(PRIOR/'source-audit.json');verify_bindings(prior)
    write(BASE/'plan-review.json',dict(status='pass',scope='Preserve sponsor arguments and pair exact interference comparison reader',evidence=[ref(PRIOR/'proposal.md','Predecessor manuscript'),ref(PRIOR/'source-audit.json','Preserved source identities'),ref(READER_BASE/'working-release.json','Exact paired reader'),ref(BASE/'proposal.md','Connected sponsor'),ref(BASE/'progress-evidence.json','Canonical counts'),ref(Path(__file__),'Preserving builder')],checks=['All 730 prior citations and historical snapshots retained.','Update only current reader/count statements and add connected interference comparison arguments.','No native, rights, secure-protocol, visual or final acceptance inferred.']))
    entries={s['integrated_citation_key']:s for s in prior['sources']};inherited=read(READER_BASE/'reader/source-audit.json');verify_bindings(inherited)
    for s in inherited['sources']:entries.setdefault(s['integrated_citation_key'],s)
    for key,title,path,claim in [('sp24interference_reader','Exact interference comparison working monograph',READER_BASE/'working-release.json',f'Exact {pages}-page reader with 1189 audited citations; no final acceptance'),('sp24interference_progress','interference comparison proposal coverage snapshot',BASE/'progress-evidence.json','Current software3/53/46, reuse101/3/11 and census81/32; no native admission')]:
        assert key not in entries;entries[key]=dict(integrated_citation_key=key,kind='project_evidence_not_scholarly_paper',title=title,author='Causal banking proposal project',year=2026,source_identity=str(path.relative_to(ROOT)),version_date='24 October 2026; exact bytes',local_copy=ref(path,claim),inspected_anchors=[dict(anchor=claim,inspection='Author inspection')],supported_claims=[claim],limitations=['Proposal evidence; no visual, independent, bank or final acceptance.'])
    cited={k.strip() for group in re.findall(engine.shared.CITE,(BASE/'proposal.md').read_text()) for k in group.split(',')}
    assert cited<=entries.keys() and {s['integrated_citation_key'] for s in prior['sources']}<=cited
    sources=[entries[k] for k in sorted(cited)];assert len(sources)==735
    audit=dict(sources=sources,cutoff='2026-10-07',predecessor_audit=ref(PRIOR/'source-audit.json','730 preserved identities'),reader_audit=ref(READER_BASE/'reader/source-audit.json','Combined interference comparison source/target comparisons'),manuscript=ref(BASE/'proposal.md','Connected sponsor'),plan_review=ref(BASE/'plan-review.json','Reviewed plan'),economics_code=ref(ROOT/'tools/sponsor_economics_20261013.py','Unchanged exact economics'),economics_results=ref(BASE/'economics-results.json','Exact replay'));verify_bindings(audit);write(BASE/'source-audit.json',audit)
    bib=[]
    for s in sources:
        author=s.get('author',s.get('authors',s.get('name','Software')+' contributors'))
        if isinstance(author,list):author=' and '.join(author)
        author=(author if s['integrated_citation_key'] in {'exec24_opengm_paper','exec24_libdai_paper','exec24_pytetrad_paper','exec24_policyjava_lspi','exec24_policycxx_aitoolbox_paper','exec24_policycxx_cs2021','exec24_policycxx_anytime2024','exec24_bnlearn_original','exec24_dose_original','exec24_mediation_original','exec24_policyother_original','exec24_judgebias_original'} else author.replace(', ',' and ')) if s['kind']=='paper' else '{'+engine.shared.escape(author)+'}'
        version=s.get('version_date',s.get('version_status','Bound original'))
        if isinstance(version,dict):version=json.dumps(version,sort_keys=True)
        bib.append('@misc{'+s['integrated_citation_key']+',\n author={'+author+'},\n title={'+engine.shared.escape(s.get('title',s.get('name','Software')+' primary review'))+'},\n year={'+str(s.get('year',2026))+'},\n note={'+reader.display_version(version)+'}\n}\n')
    (BASE/'refs.bib').write_text('\n'.join(x.rstrip() for x in '\n'.join(bib).splitlines())+'\n')
    subprocess.run(['pandoc','--from=markdown+raw_tex+tex_math_single_backslash','--to=latex','--top-level-division=section','--wrap=auto',str(BASE/'proposal.md'),'-o',str(BASE/'proposal.tex')],check=True,timeout=20)
    driver=(PRIOR/'reader/sponsor-proposal.tex').read_text().replace(str(PRIOR.relative_to(DOCS))+'/',str(BASE.relative_to(DOCS))+'/');(OUT/(NAME+'.tex')).write_text(driver)
    print(json.dumps(dict(prepared=str(BASE.relative_to(ROOT)),citations=735,paired_pages=pages)))

def build():
    for n in ['ROOT','DOCS','BASE','OUT','PRIOR','NAME','MIRROR','reader']:setattr(engine,n,globals()[n])
    engine.build()
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','build']);globals()[p.parse_args().command]()

#!/usr/bin/env python3
"""Build a preserving sponsor paired to the reviewed R bnlearn reader."""
import argparse,json,re,subprocess
from pathlib import Path
import build_prophets_repository_sponsor_20261021 as engine
import build_bnlearn_reader_20261024 as reader
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write
run,core,ROOT=engine.run,engine.core,reader.ROOT;DOCS=ROOT/'docs'
BASE=DOCS/'program/execution/2026-10-24/sponsor-bnlearn-v1';OUT=BASE/'reader'
PRIOR=DOCS/'program/execution/2026-10-24/sponsor-policies-cxx-v1'
READER_BASE=reader.BASE;READER_PDF=reader.PDF;NAME='sponsor-proposal'
MIRROR=DOCS/'sponsor_proposal_bnlearn_reviewed_2026-10-24.pdf'
read=lambda p:json.loads(p.read_text())

def manuscript(pages):
    text=(PRIOR/'proposal.md').read_text()
    old='1,430 pages and 1097 audited citation records, including 249 genuine scholarly PDFs';assert text.count(old)==1
    text=text.replace(old,f'{pages:,} pages and 1101 audited citation records, including 250 genuine scholarly PDFs')
    old='Current software coverage is three passing, 50 inconclusive and 49 open cells; reuse is 62 passing, three inconclusive and 50 open. Census has 80 inspected and 33 unread originals, plus four crosscutting obligations. The program has 254 recorded outcomes of 376, including inconclusive results.';assert text.count(old)==1
    text=text.replace(old,'At the cited C++ policy review, software coverage was three passing, 50 inconclusive and 49 open cells; reuse was 62 passing, three inconclusive and 50 open. Census had 80 inspected and 33 unread originals, plus four crosscutting obligations. That snapshot recorded 254 outcomes of 376, including inconclusive results.')
    marker='# Public evidence before expensive bank experiments';assert text.count(marker)==1
    addition=(READER_BASE/'sponsor-addition.md').read_text()
    addition+=chr(10)*2+'Current software coverage is three passing, 50 inconclusive and 49 open cells; reuse is 63 passing, three inconclusive and 49 open. Census has 80 inspected and 33 unread originals, plus four crosscutting obligations. The program has 255 recorded outcomes of 376, including inconclusive results. '+chr(92)+'citep{sp24bnlearn_reader,sp24bnlearn_progress}'+chr(10)*2
    return text.replace(marker,addition+marker)

def prepare():
    assert not BASE.exists() and not MIRROR.exists();state=core.read(ROOT,core.STATE)
    assert state['execution_runtime']['active'] is None and run.same_reader(state['reader'],ref(READER_PDF,'Current reader'))
    verify_bindings(read(READER_BASE/'working-release.json'));BASE.mkdir();OUT.mkdir()
    progress=engine.snapshot(state);progress['census']=ref(DOCS/'program/execution/2026-10-24/census-affordance-fuzzing-v1/census-register.json','80 inspected and 33 unread originals of 113')
    write(BASE/'progress-evidence.json',progress);write(BASE/'economics-results.json',engine.economics.calculate())
    pages=state['reader']['pages'];(BASE/'proposal.md').write_text(manuscript(pages));prior=read(PRIOR/'source-audit.json');verify_bindings(prior)
    write(BASE/'plan-review.json',dict(status='pass',scope='Preserve sponsor arguments and pair exact R bnlearn reader',evidence=[ref(PRIOR/'proposal.md','Predecessor manuscript'),ref(PRIOR/'source-audit.json','Preserved source identities'),ref(READER_BASE/'working-release.json','Exact paired reader'),ref(BASE/'proposal.md','Connected sponsor'),ref(BASE/'progress-evidence.json','Canonical counts'),ref(Path(__file__),'Preserving builder')],checks=['All 585 prior citations and historical snapshots retained.','Update only current reader/count statements and add connected R bnlearn argument.','No native, rights, secure-protocol, visual or final acceptance inferred.']))
    entries={s['integrated_citation_key']:s for s in prior['sources']};inherited=read(READER_BASE/'reader/source-audit.json');verify_bindings(inherited)
    for s in inherited['sources']:entries.setdefault(s['integrated_citation_key'],s)
    for key,title,path,claim in [('sp24bnlearn_reader','Exact R bnlearn working monograph',READER_BASE/'working-release.json',f'Exact {pages}-page reader with 1101 audited citations; no final acceptance'),('sp24bnlearn_progress','R bnlearn proposal coverage snapshot',BASE/'progress-evidence.json','Current software3/50/49, reuse63/3/49 and census80/33; no native admission')]:
        assert key not in entries;entries[key]=dict(integrated_citation_key=key,kind='project_evidence_not_scholarly_paper',title=title,author='Causal banking proposal project',year=2026,source_identity=str(path.relative_to(ROOT)),version_date='24 October 2026; exact bytes',local_copy=ref(path,claim),inspected_anchors=[dict(anchor=claim,inspection='Author inspection')],supported_claims=[claim],limitations=['Proposal evidence; no visual, independent, bank or final acceptance.'])
    cited={k.strip() for group in re.findall(engine.shared.CITE,(BASE/'proposal.md').read_text()) for k in group.split(',')}
    assert cited<=entries.keys() and {s['integrated_citation_key'] for s in prior['sources']}<=cited
    sources=[entries[k] for k in sorted(cited)];assert len(sources)==591
    audit=dict(sources=sources,cutoff='2026-10-07',predecessor_audit=ref(PRIOR/'source-audit.json','585 preserved identities'),reader_audit=ref(READER_BASE/'reader/source-audit.json','One genuine original,pinned R source,separate namesake identity and exact authored derivations'),manuscript=ref(BASE/'proposal.md','Connected sponsor'),plan_review=ref(BASE/'plan-review.json','Reviewed plan'),economics_code=ref(ROOT/'tools/sponsor_economics_20261013.py','Unchanged exact economics'),economics_results=ref(BASE/'economics-results.json','Exact replay'));verify_bindings(audit);write(BASE/'source-audit.json',audit)
    bib=[]
    for s in sources:
        author=s.get('author',s.get('authors',s.get('name','Software')+' contributors'))
        if isinstance(author,list):author=' and '.join(author)
        author=(author if s['integrated_citation_key'] in {'exec24_policyjava_lspi','exec24_policycxx_aitoolbox_paper','exec24_policycxx_cs2021','exec24_policycxx_anytime2024','exec24_bnlearn_original'} else author.replace(', ',' and ')) if s['kind']=='paper' else '{'+engine.shared.escape(author)+'}'
        version=s.get('version_date',s.get('version_status','Bound original'))
        if isinstance(version,dict):version=json.dumps(version,sort_keys=True)
        bib.append('@misc{'+s['integrated_citation_key']+',\n author={'+author+'},\n title={'+engine.shared.escape(s.get('title',s.get('name','Software')+' primary review'))+'},\n year={'+str(s.get('year',2026))+'},\n note={'+reader.display_version(version)+'}\n}\n')
    (BASE/'refs.bib').write_text('\n'.join(x.rstrip() for x in '\n'.join(bib).splitlines())+'\n')
    subprocess.run(['pandoc','--from=markdown+raw_tex+tex_math_single_backslash','--to=latex','--top-level-division=section','--wrap=auto',str(BASE/'proposal.md'),'-o',str(BASE/'proposal.tex')],check=True,timeout=20)
    driver=(PRIOR/'reader/sponsor-proposal.tex').read_text().replace(str(PRIOR.relative_to(DOCS))+'/',str(BASE.relative_to(DOCS))+'/');(OUT/(NAME+'.tex')).write_text(driver)
    print(json.dumps(dict(prepared=str(BASE.relative_to(ROOT)),citations=591,paired_pages=pages)))

def build():
    for n in ['ROOT','DOCS','BASE','OUT','PRIOR','NAME','MIRROR','reader']:setattr(engine,n,globals()[n])
    engine.build()
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','build']);globals()[p.parse_args().command]()

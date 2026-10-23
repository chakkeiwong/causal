#!/usr/bin/env python3
"""Build a preserving sponsor paired to the reviewed unlearning reader."""
import argparse,json,re,subprocess
from pathlib import Path
import build_prophets_repository_sponsor_20261021 as engine
import build_unlearning_reader_v2_20261024 as reader
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write
run,core,ROOT=engine.run,engine.core,reader.ROOT;DOCS=ROOT/'docs'
BASE=DOCS/'program/execution/2026-10-24/sponsor-unlearning-v1';OUT=BASE/'reader'
PRIOR=DOCS/'program/execution/2026-10-24/sponsor-workflow-contracts-v1'
READER_BASE=reader.BASE;READER_PDF=reader.PDF;NAME='sponsor-proposal'
MIRROR=DOCS/'sponsor_proposal_unlearning_reviewed_2026-10-24.pdf'
read=lambda p:json.loads(p.read_text())

def manuscript(pages):
    text=(PRIOR/'proposal.md').read_text()
    old='1,352 pages and 1031 audited citation records, including 235 genuine scholarly PDFs';assert text.count(old)==1
    text=text.replace(old,f'{pages:,} pages and 1034 audited citation records, including 236 genuine scholarly PDFs')
    old='The census remains 73 inspected and 40 unread originals, plus four crosscutting obligations.';assert text.count(old)==1
    text=text.replace(old,'At the workflow-contract review the census remained 73 inspected and 40 unread originals, plus four crosscutting obligations.')
    old='The current census has 73 inspected and 40 unread originals out of 113';assert text.count(old)==1
    text=text.replace(old,'At the collaboration review the census had 73 inspected and 40 unread originals out of 113')
    old='The census remains 73 inspected and 40 unread originals, with four crosscutting obligations open.';assert text.count(old)==3
    text=text.replace(old,'At that cited review the census remained 73 inspected and 40 unread originals, with four crosscutting obligations open.')
    old='The original-candidate census now contains 73 inspected and 40 unread originals out of 113';assert text.count(old)==1
    text=text.replace(old,'The original-candidate census now contains 74 inspected and 39 unread originals out of 113')
    old='Current census totals are bound to this release. '+chr(92)+'citep{sp24collaboration_progress}';assert text.count(old)==1
    text=text.replace(old,'The historical collaboration census is bound to its release. '+chr(92)+'citep{sp24collaboration_progress} Current census totals are bound to the unlearning release. '+chr(92)+'citep{sp24unlearning_progress}')
    old='Current totals are bound to the workflow-contract snapshot.';assert text.count(old)==1
    text=text.replace(old,'The workflow-contract totals are bound to their snapshot.')
    marker='# Public evidence before expensive bank experiments';assert text.count(marker)==1
    addition=(READER_BASE/'sponsor-addition.md').read_text()
    addition+='\n\nCurrent software coverage is three passing, 43 inconclusive and 56 open cells; reuse remains 56 passing, three inconclusive and 56 open. The census is now 74 inspected and 39 unread originals, plus four crosscutting obligations. '+chr(92)+'citep{sp24unlearning_reader,sp24unlearning_progress}'+chr(10)*2
    return text.replace(marker,addition+marker)

def prepare():
    assert not BASE.exists() and not MIRROR.exists();state=core.read(ROOT,core.STATE)
    assert state['execution_runtime']['active'] is None and run.same_reader(state['reader'],ref(READER_PDF,'Current reader'))
    verify_bindings(read(READER_BASE/'working-release.json'));BASE.mkdir();OUT.mkdir()
    progress=engine.snapshot(state);progress['census']=ref(DOCS/'program/execution/2026-10-24/census-agent-unlearning-v1/census-register.json','74 inspected and 39 unread originals of 113')
    write(BASE/'progress-evidence.json',progress);write(BASE/'economics-results.json',engine.economics.calculate())
    pages=state['reader']['pages'];(BASE/'proposal.md').write_text(manuscript(pages));prior=read(PRIOR/'source-audit.json');verify_bindings(prior)
    write(BASE/'plan-review.json',dict(status='pass',scope='Preserve sponsor arguments and pair exact unlearning reader',evidence=[ref(PRIOR/'proposal.md','Predecessor manuscript'),ref(PRIOR/'source-audit.json','Preserved source identities'),ref(READER_BASE/'working-release.json','Exact paired reader'),ref(BASE/'proposal.md','Connected sponsor'),ref(BASE/'progress-evidence.json','Canonical counts'),ref(Path(__file__),'Preserving builder')],checks=['All 472 prior citations and historical snapshots retained.','Update only current reader/count statements and add connected unlearning argument.','No supported-server, native, rights, visual or final acceptance inferred.']))
    entries={s['integrated_citation_key']:s for s in prior['sources']};inherited=read(READER_BASE/'source-audit.json');verify_bindings(inherited)
    for s in inherited['sources']:entries.setdefault(s['integrated_citation_key'],s)
    for key,title,path,claim in [('sp24unlearning_reader','Exact unlearning working monograph',READER_BASE/'working-release.json',f'Exact {pages}-page reader with 1034 audited citations; no final acceptance'),('sp24unlearning_progress','Unlearning proposal coverage snapshot',BASE/'progress-evidence.json','Current software3/43/56, reuse56/3/56 and census74/39; no native admission')]:
        assert key not in entries;entries[key]=dict(integrated_citation_key=key,kind='project_evidence_not_scholarly_paper',title=title,author='Causal banking proposal project',year=2026,source_identity=str(path.relative_to(ROOT)),version_date='24 October 2026; exact bytes',local_copy=ref(path,claim),inspected_anchors=[dict(anchor=claim,inspection='Author inspection')],supported_claims=[claim],limitations=['Proposal evidence; no visual, independent, bank or final acceptance.'])
    cited={k.strip() for group in re.findall(engine.shared.CITE,(BASE/'proposal.md').read_text()) for k in group.split(',')}
    assert cited<=entries.keys() and {s['integrated_citation_key'] for s in prior['sources']}<=cited
    sources=[entries[k] for k in sorted(cited)];assert len(sources)==477
    audit=dict(sources=sources,cutoff='2026-10-07',predecessor_audit=ref(PRIOR/'source-audit.json','472 preserved identities'),reader_audit=ref(READER_BASE/'source-audit.json','Three added records'),manuscript=ref(BASE/'proposal.md','Connected sponsor'),plan_review=ref(BASE/'plan-review.json','Reviewed plan'),economics_code=ref(ROOT/'tools/sponsor_economics_20261013.py','Unchanged exact economics'),economics_results=ref(BASE/'economics-results.json','Exact replay'));verify_bindings(audit);write(BASE/'source-audit.json',audit)
    bib=[]
    for s in sources:
        author=s.get('author',s.get('authors',s.get('name','Software')+' contributors'))
        if isinstance(author,list):author=' and '.join(author)
        author=author.replace(', ',' and ') if s['kind']=='paper' else '{'+engine.shared.escape(author)+'}'
        version=s.get('version_date',s.get('version_status','Bound original'))
        if isinstance(version,dict):version=json.dumps(version,sort_keys=True)
        bib.append('@misc{'+s['integrated_citation_key']+',\n author={'+author+'},\n title={'+engine.shared.escape(s.get('title',s.get('name','Software')+' primary review'))+'},\n year={'+str(s.get('year',2026))+'},\n note={'+engine.shared.escape(version)+'}\n}\n')
    (BASE/'refs.bib').write_text('\n'.join(x.rstrip() for x in '\n'.join(bib).splitlines())+'\n')
    subprocess.run(['pandoc','--from=markdown+raw_tex+tex_math_single_backslash','--to=latex','--top-level-division=section','--wrap=auto',str(BASE/'proposal.md'),'-o',str(BASE/'proposal.tex')],check=True,timeout=20)
    driver=(PRIOR/'reader/sponsor-proposal.tex').read_text().replace(str(PRIOR.relative_to(DOCS))+'/',str(BASE.relative_to(DOCS))+'/');(OUT/(NAME+'.tex')).write_text(driver)
    print(json.dumps(dict(prepared=str(BASE.relative_to(ROOT)),citations=477,paired_pages=pages)))

def build():
    for n in ['ROOT','DOCS','BASE','OUT','PRIOR','NAME','MIRROR','reader']:setattr(engine,n,globals()[n])
    engine.build()
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','build']);globals()[p.parse_args().command]()

#!/usr/bin/env python3
"""Preserve sponsor content and pair the R IV/RD successor to exact reader bytes."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import subprocess
import build_prophets_repository_sponsor_20261021 as engine
import build_r_iv_rd_reader_20261022 as reader
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run,core=engine.run,engine.core
ROOT=reader.ROOT
DOCS=ROOT/'docs'
BASE=DOCS/'program/execution/2026-10-22/sponsor-r-iv-rd-v1'
OUT=BASE/'reader'
PRIOR=DOCS/'program/execution/2026-10-22/sponsor-bayesian-commercial-v1'
NAME='sponsor-proposal'
MIRROR=DOCS/'sponsor_proposal_r_iv_rd_reviewed_2026-10-22.pdf'
read=lambda p:json.loads(p.read_text())


def manuscript(pages):
    text=(PRIOR/'proposal.md').read_text()
    count=len(read(reader.OUT/'source-audit.json')['sources'])
    papers=read(reader.BASE/'traceability-review.json')['scholarly_pdfs']
    progress=read(BASE/'progress-evidence.json');c=progress['software_cells']
    replacements={
        '1,209 pages and 896 audited citation records, including 217 genuine scholarly PDFs':
            f'{pages:,} pages and {count} audited citation records, including {papers} genuine scholarly PDFs',
        '63 open and 37 inconclusive cells':f'{c["open"]} open and {c["inconclusive"]} inconclusive cells',
        '87 open and three inconclusive decisions':f'{progress["reuse_decisions"]["open"]} open and three inconclusive decisions',
        'sp22bs_reader':'sp22iv_reader','sp22bs_progress':'sp22iv_progress'}
    for old,new in replacements.items():
        assert old in text,old
        text=text.replace(old,new)
    text=text.replace('sp22iv_reader,','sp22iv_reader,sp22bs_reader,',1)
    text=text.replace('sp22iv_progress,','sp22iv_progress,sp22bs_progress,',1)
    marker='# Public evidence before expensive bank experiments'
    assert text.count(marker)==1
    return text.replace(marker,(reader.BASE/'sponsor-addition.md').read_text()+'\n'+marker)


def prepare():
    assert not BASE.exists() and not MIRROR.exists()
    state=core.read(ROOT,core.STATE)
    assert state['execution_runtime']['active'] is None
    assert run.same_reader(state['reader'],ref(reader.PDF,'Current reader'))
    assert {q['id']:q['status'] for q in run.status(ROOT,state)['proposal_gaps']}==dict(Q1='open',Q2='pass',Q3='pass',Q4='pass',Q5='open')
    verify_bindings(read(reader.BASE/'working-release.json'))
    BASE.mkdir(parents=True);OUT.mkdir()
    write(BASE/'progress-evidence.json',engine.snapshot(state))
    write(BASE/'economics-results.json',engine.economics.calculate())
    pages=state['reader']['pages'];(BASE/'proposal.md').write_text(manuscript(pages))
    prior=read(PRIOR/'source-audit.json');verify_bindings(prior)
    write(BASE/'plan-review.json',dict(status='pass',
        scope='Preserving R IV/RD sponsor comparison with actual coverage counts',
        evidence=[ref(PRIOR/'proposal.md','Prior source'),ref(PRIOR/'source-audit.json','Preserved citations'),
            ref(reader.BASE/'working-release.json','Exact reader'),ref(BASE/'proposal.md','Updated sponsor'),
            ref(BASE/'progress-evidence.json','Effective receipts'),ref(Path(__file__),'Exact preserving builder')],
        checks=['All earlier substantive sections and citation identities survive.',
            'Counts derive from receipts and actual audited reader; Q2-Q4 renewal precedes sponsor preparation.',
            'Describe IV/RD targets, confidence sets and reference-only decisions without claiming native runtime, rights clearance or measured bank value.',
            'Visual and final acceptance remain open.']))
    entries={s['integrated_citation_key']:s for s in prior['sources']}
    inherited=read(reader.OUT/'source-audit.json');verify_bindings(inherited)
    for s in inherited['sources']:entries.setdefault(s['integrated_citation_key'],s)
    for key,title,path,claim in [
        ('sp22iv_reader','Current R IV/RD working reader',reader.BASE/'working-release.json',
         f'Exact {pages}-page reader with {len(inherited["sources"])} audited source records; no final acceptance'),
        ('sp22iv_progress','Current effective proposal coverage',BASE/'progress-evidence.json',
         'Actual effective software, reuse and chapter receipts; unchanged census57/56; no native capability')]:
        assert key not in entries
        entries[key]=dict(integrated_citation_key=key,kind='project_evidence_not_scholarly_paper',
            title=title,author='Causal banking proposal project',year=2026,source_identity=str(path.relative_to(ROOT)),
            version_date='22October2026; exact artifact bytes',local_copy=ref(path,claim),
            inspected_anchors=[dict(anchor=claim,inspection='Author inspection')],supported_claims=[claim],
            limitations=['Proposal evidence, not independent or bank acceptance.'])
    cited={k.strip() for group in re.findall(engine.shared.CITE,(BASE/'proposal.md').read_text()) for k in group.split(',')}
    assert cited<=entries.keys() and {s['integrated_citation_key'] for s in prior['sources']}<=cited
    sources=[entries[k] for k in sorted(cited)]
    audit=dict(sources=sources,cutoff='2026-10-07',
        predecessor_audit=ref(PRIOR/'source-audit.json','Unchanged earlier source identities'),
        reader_audit=ref(reader.OUT/'source-audit.json','Current integrated reader citations'),
        manuscript=ref(BASE/'proposal.md','Reconciled sponsor narrative'),plan_review=ref(BASE/'plan-review.json','Preserving plan'),
        economics_code=ref(ROOT/'tools/sponsor_economics_20261013.py','Unchanged exact economics'),
        economics_results=ref(BASE/'economics-results.json','Exact replay'))
    verify_bindings(audit);write(BASE/'source-audit.json',audit)
    bib=[]
    for s in sources:
        author=s.get('author',s.get('authors',s.get('name','Software')+' contributors'))
        if isinstance(author,list):author=' and '.join(author)
        author=author if s['kind']=='paper' else '{'+engine.shared.escape(author)+'}'
        title=s.get('title',s.get('name','Software')+' primary source review')
        version=s.get('version_date',s.get('version_status','Bound local original'))
        if isinstance(version,dict):version=json.dumps(version,sort_keys=True)
        bib.append('@misc{'+s['integrated_citation_key']+',\n author={'+author+'},\n title={'+
            engine.shared.escape(title)+'},\n year={'+str(s.get('year',2026))+'},\n note={'+engine.shared.escape(version)+'}\n}\n')
    (BASE/'refs.bib').write_text('\n'.join(bib))
    subprocess.run(['pandoc','--from=markdown+raw_tex+tex_math_single_backslash','--to=latex',
        '--top-level-division=section','--wrap=auto',str(BASE/'proposal.md'),'-o',str(BASE/'proposal.tex')],check=True,timeout=20)
    driver=(PRIOR/'reader/sponsor-proposal.tex').read_text().replace(
        str(PRIOR.relative_to(DOCS))+'/',str(BASE.relative_to(DOCS))+'/').replace('21 October 2026','22 October 2026')
    (OUT/(NAME+'.tex')).write_text(driver)
    print(json.dumps(dict(prepared=str(BASE.relative_to(ROOT)),citations=len(cited),paired_pages=pages)))


def build():
    for name in ['ROOT','DOCS','BASE','OUT','PRIOR','NAME','MIRROR','reader']:
        setattr(engine,name,globals()[name])
    engine.build()


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','build'])
    {'prepare':prepare,'build':build}[p.parse_args().command]()

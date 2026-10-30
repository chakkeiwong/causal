"""Assemble protected successor sources with exact edit dispositions."""
from pathlib import Path
import argparse,difflib,json,re,subprocess,time
from rewrite_preservation_20261029 import ROOT,DOCS,OUT,BASE,INPUT,digest,save,tree
PREFIX='developmental-rewrite/2026-10-29/'
FULL='causal_banking_developmental_rewrite_2026-10-29'
SPONSOR='causal_banking_sponsor_rewrite_2026-10-29'

def normalize_name(v):
    p=DOCS/v
    if not p.suffix:p=p.with_suffix('.tex')
    return str(p.relative_to(ROOT))

def prepare():
    baseline=json.loads((OUT/'baseline.json').read_text())
    originals={n:(OUT/'baseline'/n).read_text() for n in baseline['source_files']}
    rootname=str(BASE.relative_to(ROOT))
    mapping={n:PREFIX+'retained/'+n[len('docs/'):] for n in originals if n!=rootname}
    edits=[]
    def record(source,dest,before,after,kind,reason,claims):
        if before!=after:edits.append(dict(source=source,destination=dest,before=before,after=after,category=kind,reason=reason,surviving_claims_and_limits=claims))
    def replace(t,old,new,source,dest,kind,reason,claims):
        if old not in t:raise RuntimeError('Missing anchor '+source+': '+old[:70])
        record(source,dest,old,new,kind,reason,claims)
        return t.replace(old,new,1)
    for name,original in originals.items():
        if name==rootname:continue
        dest='docs/'+mapping[name];t=original
        if name=='docs/reading-edition/opening.tex':
            new=(OUT/'opening.tex').read_text()
            record(name,dest,t,new,'developmental_replacement','Reconstruct the argument and reading route.',
                'Selection, intervention alternatives, four journeys, expert comparator, mathematical depth, evidence distinctions and cutoff retained; all details remain reachable.')
            t=new
        if name=='docs/reading-edition/banking-decision.tex':
            t=replace(t,r'''$Y_i(1)$ be the contribution over the next quarter if the offer is sent and
$Y_i(0)$ the contribution under the alternative. Contribution includes the
agreed funding value, interest expense and servicing costs over the same
quarter. The average effect for the eligible population is
\[
 \tau=\mathbb E\{Y_i(1)-Y_i(0)\}.
\]''',r'''$C_i(1)$ be contribution over the following year if the offer is assigned and
$C_i(0)$ contribution over that same year under the alternative. Contribution
includes the agreed funding value, interest expense and servicing costs.
Assignment, delivery, acceptance and the resulting price are distinguished
in Chapter~\ref{rewrite:deposit}. The average assignment effect is
\[
 \tau_C=\mathbb E\{C_i(1)-C_i(0)\}.
\]''',name,dest,'target_correction','Unify annual horizon and distinguish contribution from balances.',
                'Household weighting and selection argument retained; the quarterly illustration is explicitly superseded by the annual target. No observed quarterly result existed.')
            t=replace(t,r'''Suppose
a rate increase attracts an additional balance $\Delta B$ for one year.''',r'''For the price rule used here, assignment delivers the offer and reprices
the eligible balance automatically. Suppose the resulting rate increase
attracts an additional average balance $\Delta B$ for one year.''',name,dest,'assumption_clarification','Specify the price rule behind the unchanged expense equation.',
                'Annual accounting, all amounts, omissions and break-even figure retained; voluntary activation requires another cost map.')
            t=replace(t,"""Comparing customers who accepted an offer with those who did not generally
mixes the offer's effect with the reasons for acceptance.""",r'''Comparing customers who received an offer with those who did not can
mix its effect with the reasons for targeted delivery. Comparing acceptors
with nonacceptors introduces a separate selection problem. The constructed
comparison below concerns receipt, denoted $A$, and balances, denoted $B$.''',name,dest,'target_correction','Separate acceptance from receipt in the selection example.',
                'Selected group composition, 80-versus-20 contrast and selection qualification retained.')
            for a in ['1','0']:
                t=replace(t,r'\mathbb E[Y\mid A='+a+']',r'\mathbb E[B\mid A='+a+']',name,dest,'notation_correction','Use a balance symbol.','Means and difference unchanged.')
            t=replace(t,r'Chapters~\ref{r3:graphs} and~\ref{r3:investment} and the intervening analysis.',
                r'Chapters~\ref{r3:graphs} and~\ref{r3:instruments}; Chapter~\ref{rewrite:deposit} carries the assigned-offer target into estimation and contribution.',
                name,dest,'reference_correction','Point to the relevant identification argument.','All technical identification and investment content retained.')
        if name.endswith('s_49cadb031985ea.tex'):
            t=replace(t,r'\chapter{Conducting a study with the proposed service}',r'\chapter{Operating a study without changing its scientific meaning}',name,dest,'role_clarification','Put operations after the complete economist study.','All operating content retained.')
        if name.endswith('s_7d439ea161defb.tex'):
            t=replace(t,r'\section{Make adoption evidence exact, external, and conditional}',r'\section{Evidence required for institutional adoption}',name,dest,'role_clarification','Move dated institutional evidence to operating detail.','All 64 cases, missing receipts, authority limits and impact-review conditions retained.')
        def space(m):
            new=m[1]+'~'+m[2]
            record(name,dest,m[0],new,'citation_spacing','Separate parenthetical citation from preceding text.','Citation key and attachment unchanged.')
            return new
        t=re.sub(r'([A-Za-z0-9.,;:!?])(\\citep(?=[\[{]))',space,t)
        def f(m):
            key=normalize_name(m[1]);new=r'\input{'+mapping[key]+'}'
            record(name,dest,m[0],new,'link_relocation','Bind child input to successor copy.','Child content retained except separately recorded edits.')
            return new
        t=INPUT.sub(f,t)
        p=ROOT/dest;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t)
    root=originals[rootname];sections=re.split(r'(?=\\part\{)',root);front=sections[0];parts=sections[1:]
    bibpos=parts[-1].index(r'\bibliographystyle');tail=parts[-1][bibpos:];parts[-1]=parts[-1][:bibpos]
    def remove_input(name):
        nonlocal parts
        pat=re.compile(r'\\input\{'+re.escape(name)+r'(?:\.tex)?\}\s*');hits=0
        for i,p in enumerate(parts):parts[i],n=pat.subn('',p);hits+=n
        if hits!=1:raise RuntimeError((name,hits))
    move=['scientific-synthesis/2026-10-29/software-decisions','scientific-synthesis/2026-10-29/assistance-decisions',
          'scientific-synthesis/2026-10-29/decision-evidence','reading-edition/sources/s_ecd3b672756f80',
          'scientific-synthesis/2026-10-29/practical-investment','reading-edition/sources/s_617eeb5ab919f5']
    for name in move:remove_input(name)
    runtime='reading-edition/sources/s_cbb1f54fbcfcf8';adoption='reading-edition/sources/s_7d439ea161defb'
    remove_input(runtime);remove_input(adoption)
    parts[0]=parts[0].replace(r'\input{reading-edition/banking-decision}',r'\input{reading-edition/banking-decision}'+'\n'+r'\input{'+PREFIX+'journeys}')
    parts[6]=parts[6].replace(r'\part{Putting a banking study into practice}',r'\part{Operating the analytical service}')
    parts[6]+=r'''\chapter{Runtime uncertainty and institutional evidence}
The following treatments support the completed studies in the main argument.
They retain version-dependent uncertainty behavior, recovery restrictions
and the scope of institutional evidence. These facts qualify an operating
claim; they do not replace the economist's identification or value calculation.
'''+ '\n'+r'\input{'+runtime+'}\n'+r'\input{'+adoption+'}\n'
    main=r'''\part{From evidence to a bounded investment}
\label{rewrite:part-synthesis}
The banking journeys and their foundations determine what a useful service
must preserve. The next chapters connect software choices, assistance,
observed studies, practical capabilities and the full cost account. Their
conclusion selects the first experiment. Detailed comparative and operating
treatments remain in the following parts.
'''+ '\n'+'\n'.join(r'\input{'+n+'}' for n in move)+'\n'+r'\input{'+PREFIX+'software-selection}'+'\n'+r'\input{'+PREFIX+'decision-synthesis}'+'\n'
    front=front.replace(r'\large Scientific continuation',r'\large Developmental rewrite')
    # Three-digit chapter numbers need a wider contents number box.
    front=front.replace(r'\makeatother',r'\renewcommand*\l@chapter{\@dottedtocline{0}{0pt}{2.5em}}'+'\n'+r'\makeatother',1)
    assembled=front+''.join(parts[:3])+main+''.join(parts[3:])+tail
    def root_input(m):
        key=normalize_name(m[1]);return r'\input{'+mapping[key]+'}' if key in mapping else m[0]
    assembled=INPUT.sub(root_input,assembled)
    assembled=re.sub(r'\\bibliography\{[^}]+\}',lambda m:r'\bibliography{'+PREFIX+'references}',assembled)
    dest=DOCS/(FULL+'.tex');dest.write_text(assembled)
    a=root.splitlines(keepends=True);b=assembled.splitlines(keepends=True)
    for tag,i,j,k,l in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
        if tag!='equal':record(rootname,str(dest.relative_to(ROOT)),''.join(a[i:j]),''.join(b[k:l]),'driver_reassembly',
            'Reorder complete argument, retaining detailed supporting treatments.',
            'Every inherited input reachable once; moved chapters retain full content; part descriptions retain scope; bibliography keeps stable keys.')
        if tag!='equal':edits[-1].update(before_line_start=i,before_line_end=j,after_line_start=k,after_line_end=l)
    bibliography(baseline,edits)
    save('edit-ledger.json',edits)
    save('source-map.json',[{'original':n,'original_sha256':digest(OUT/'baseline'/n),'destination':str(dest.relative_to(ROOT)) if n==rootname else 'docs/'+mapping[n],
        'disposition':'root_reassembled' if n==rootname else 'retained_in_complete_monograph'} for n in originals])
    header=INPUT.sub(root_input,front[:front.index(r'\begin{document}')]).replace(r'\large Developmental rewrite',r'\large Sponsor proposal')
    (DOCS/(SPONSOR+'.tex')).write_text(header+'\\begin{document}\n\\maketitle\n'+(OUT/'sponsor-body.tex').read_text()+'\n\\end{document}\n')
    save('assembly.json',{'source_files_mapped':len(originals),'main_moves':move,'operating_moves':[runtime,adoption],'edit_entries':len(edits)})
    print(json.dumps({'mapped':len(originals),'edits':len(edits),'root':FULL}))

def bibliography(baseline,edits):
    a=json.loads((DOCS/'scientific-synthesis/2026-10-29/source-audit.json').read_text())
    records=json.loads((ROOT/a['inherited_audit']).read_text())['sources'];d={r.get('integrated_citation_key',r.get('id')):r for r in records}
    overrides={
     'exec13_census_orca':'Joanie Hayoun Chung and Sumin Lee and Sungbin Lim',
     'exec13_census_augur_arxiv':'Zhiqing Cui and Binwu Wang and Qingxiang Liu and Yeqiang Wang and Zhengyang Zhou and Yuxuan Liang and Yang Wang',
     'exec13_census_causal_agent':'Kairong Han and Kun Kuang and Ziyu Zhao and Junjian Ye and Fei Wu',
     'exec13_data_causalagent':'Jiawei Zhu and Wei Chen and Ruichu Cai',
     'exec13_data_oci':'Winston Chou and Adrien Alexandre and Lars Olds and Yi Zhang and Nathan Kallus',
     'exec13_data_causalds':'Andrej Leban and Yuekai Sun',
     'exec13_data_ontolearner':r'Babaei Giglou, Hamed and D{\textquotesingle}Souza, Jennifer and Aioanei, Andrei and Mihindukulasooriya, Nandana and Auer, S{\"o}ren',
     'exec13_data_causaldiscovery':'Yujia Zheng and Vishal Verma and Mantej Gill and Haoyue Dai and Peter Spirtes and Kun Zhang'}
    entries={};rows=[];norm=[]
    for name in baseline['bibliography_files']:
        text=(OUT/'baseline'/name).read_text()
        for s in re.finditer(r'(?m)^\s*@([A-Za-z]+)\s*\{',text):
            i=s.end();depth=1
            while i<len(text) and depth:
                if text[i]=='{' and text[i-1]!='\\':depth+=1
                elif text[i]=='}' and text[i-1]!='\\':depth-=1
                i+=1
            entry=text[s.start():i].strip();key=entry[entry.index('{')+1:].split(',',1)[0].strip()
            if s[1].lower() in ['comment','preamble','string']:raise RuntimeError('Unsupported directive '+s[1])
            if key in entries:
                if entries[key]['original']!=entry:raise RuntimeError('Conflicting bibliography key '+key)
                continue
            new=entry;r=d.get(key,{});m=re.search(r'author\s*=\s*\{\{([^{}]+)\}\}',entry,re.I)
            if m and r.get('kind')=='paper':
                old=m[0];replacement='author={'+overrides.get(key,m[1])+'}';new=new.replace(old,replacement,1)
                row=dict(source=name,destination='docs/'+PREFIX+'references.bib',category='scholarly_author_parsing',citation_key=key,
                    reason='Restore individual author parsing using retained original and identity audit.',surviving_claims_and_limits='Stable key, title, version and supported claims; no works merged.',
                    before=old,after=replacement,primary_pdf=r.get('local_path'),primary_sha256=r.get('sha256'))
                edits.append(row);norm.append(row)
            spaced=re.sub(r'\b(pages?|published|retrieved|posted|accessed)(\d)',r'\1 \2',new)
            if spaced!=new:
                edits.append(dict(source=name,destination='docs/'+PREFIX+'references.bib',category='bibliography_spacing',citation_key=key,
                    reason='Separate words from date or page digits.',surviving_claims_and_limits='All fields, identity and numbers retained.',before=new,after=spaced))
            entries[key]=dict(original=entry,after=spaced,source=name)
            rows.append(dict(key=key,source=name,destination='docs/'+PREFIX+'references.bib',kind=r.get('kind','inherited')))
    (OUT/'references.bib').write_text('\n\n'.join(v['after'] for v in entries.values())+'\n')
    save('bibliography-map.json',rows);save('bibliography-normalization.json',norm)

def build(kind):
    stem=FULL if kind=='full' else SPONSOR;directory=OUT/('build-'+kind);directory.mkdir(exist_ok=True)
    command=['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error','-recorder','-output-directory='+str(directory),stem+'.tex']
    commands=[command]
    if kind=='full':commands.append(['bibtex',str((directory/stem).relative_to(DOCS))])
    commands += [command,command];results=[]
    for i,cmd in enumerate(commands,1):
        path=directory/f'pass-{i}.txt';started=time.monotonic()
        with path.open('w') as out:proc=subprocess.run(cmd,cwd=DOCS,stdout=out,stderr=subprocess.STDOUT,timeout=240)
        row=dict(pass_number=i,returncode=proc.returncode,seconds=round(time.monotonic()-started,2),log=str(path.relative_to(ROOT)))
        results.append(row);save('build-'+kind+'.json',results);print(json.dumps(row),flush=True)
        if proc.returncode:print('\n'.join(path.read_text(errors='replace').splitlines()[-30:]));raise SystemExit(proc.returncode)
    target=DOCS/(stem+'.pdf');target.write_bytes((directory/(stem+'.pdf')).read_bytes())
    print(json.dumps({'pdf':str(target.relative_to(ROOT)),'sha256':digest(target)}),flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','full','sponsor']);a=p.parse_args()
    prepare() if a.command=='prepare' else build(a.command)

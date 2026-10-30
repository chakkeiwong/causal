"""Finish the reading extract; leave the concurrent release unchanged."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,re,shutil,sys,os
os.environ.setdefault('MPLCONFIGDIR','/tmp/causal-partial-matplotlib')
os.environ.setdefault('XDG_CACHE_HOME','/tmp/causal-partial-cache')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import build_closure_publication_20261030 as base
R=Path(__file__).resolve().parents[1]
O=R/'docs/twelve-hour-closure/2026-10-29'
B=R/'docs/release/2026-10-29'
S=B/'packages/batch-086-r01/source/docs'
P=O/'partial-publication'
STEM='causal_banking_selective_recovery_2026-10-30'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(p):return dict(path=str(p.relative_to(R)),sha256=sha(p))
def read(p):return json.loads(p.read_text())
def save(p,x):
    p.parent.mkdir(parents=True,exist_ok=True);assert not p.exists(),str(p)
    p.write_text(json.dumps(x,indent=2)+chr(10))
def sources():
    prior=read(B/'partial-recovery-073/source-audit.json');records=prior['sources'];raw=R/'docs/literature/raw'
    paper=R/'docs/papers/Probability Inequalities for Sums of Bounded Random Variables Hoeffding(1963).pdf'
    original=raw/'closure30_hoeffding_original.pdf'
    if paper.exists():assert sha(paper)==sha(original)
    else:shutil.copyfile(original,paper)
    records.append(dict(citation_key='closure30hoeffding',kind='paper',title='Probability Inequalities for Sums of Bounded Random Variables',authors='Wassily Hoeffding',year=1963,
      source_identity='doi:10.1080/01621459.1963.10500830',publication_status='JASA58(301),13–30',local_copy=bind(paper),
      inspected_anchors=['PDF5 / printed16: Theorem2, equation2.6, two-sample corollary2.7, visually inspected.'],
      supported_claims=['Independent bounded summands have exponential tails. The project applies this to inverse-invitation scores and supplies the full proof.'],
      forbidden_claims=['No dependent-customer, normal-band or changed-outcome guarantee.'],full_text_status='Genuine scanned original; rendered inspection.',acquisition=bind(raw/'closure30_hoeffding_original.receipt.json')))
    save(O/'partial-source-support.json',dict(cutoff='2026-10-07',recorded_utc=datetime.now(timezone.utc).isoformat(),sources=records,inherited_audit=bind(B/'partial-recovery-073/source-audit.json'),appendix_identity=prior['appendix_identity'],scope='Primary theory and static software inspection. No native qualification, bank validation or change to original113-candidate census.'))
    metadata=[]
    for name,oa_name in [('coppock','closure30_coppock_openalex.json'),('hoeffding','closure30_hoeffding_metadata.json')]:
        oa=read(raw/oa_name)
        if 'results'in oa:
            matches=[x for x in oa['results']if '10.1017/pan.2016.6'in str(x.get('doi','')).lower()];oa=matches[0]if matches else{}
        cr=read(raw/f'closure30_{name}_crossref.json')['message']
        metadata.append(dict(source=name,openalex=bind(raw/oa_name),crossref=bind(raw/f'closure30_{name}_crossref.json'),citation_count=oa.get('cited_by_count','not available'),is_retracted=oa.get('is_retracted','not available'),venue=cr.get('container-title'),published=cr.get('published'),update_to=cr.get('update-to'),updated_by=cr.get('updated-by'),relation=cr.get('relation'),access_date='2026-10-30 Asia/Shanghai',venue_metric='not available',caveat='Metadata is discovery evidence. No update/retraction flag is not exhaustive absence. Citation counts postdate cutoff.'))
    save(O/'partial-citation-metadata.json',metadata)
    groups=[
      ('FOUNDATIONAL','Neyman1938; Hansen and Hurwitz1946; Birnbaum and Sirken1950a,b; Cochran,Mosteller,Tukey1954; Cochran1977; Rao1973; Glynn,Laird,Rubin1993','Double-sampling and variance antecedents. No uninspected historical optimality claims.'),
      ('FOUNDATIONAL','Manski1990,1995,2007; Horowitz and Manski1998,2000; Tamer2010','Partial-identification foundations; not independently imported as theorem support.'),
      ('DIRECT_METHOD','Imbens and Manski2004; Stoye2009','ATE confidence differs from whole-set containment. Inspect originals for comparative optimality; project finite-sample proof is explicit.'),
      ('COMPETITOR','Lee,Training,wages,and sample selection; Imai2008,2009; Zhang and Rubin2004; McConnell,Stuart,Devaney2008','Different always-observed/truncation targets. Coppock bibliography lists Lee2010 while package identifies2009 DOI; retain date conflict.'),
      ('COMPETITOR','Heckman1979; Das,Newey,Vella2003; Freedman and Sekhon2010; Little and Rubin2002; Little2008; Robins,Rotnitzky,Scharfstein1999; Aronow and Lee2013; Rosenbaum and Rubin1983; Rosenbaum2002','Selection,sensitivity and imputation alternatives; no uninspected technical ranking.'),
      ('DIRECT_METHOD','Miratrix,Sekhon,Yu2013; Kang and Schafer2007','Poststratification and incomplete-data comparison; no arbitrary recovery adjustment guarantee.'),
      ('EMPIRICAL_EXAMPLE','Levendusky and Malhotra2016; Jenkins etal2004; An etal2009; Manski and Nagin1998; Manski and Pepper2011; Mebane and Poast2013','Applications and different targets; no bank validity inferred.'),
      ('BACKGROUND','Peress2010; Frankel and Hillygus2014; Si,Reiter,Hillygus2014; Grogger2012; Baird,Hamory,Miguel2008; Kern etal2016; Keele and Minozzi2013','Missing-data/transport context, not support for the binary design.')]
    back=[dict(seed='Coppock2017',anchors='Introduction,Sections2–5,references203–206',classification=c,candidates=n,disposition=a)for c,n,a in groups]
    back.append(dict(seed='Hoeffding1963',anchors='Printed16',classification='FOUNDATIONAL',candidates='Chernoff and Bennett exponential-tail antecedents',disposition='Theorem2 inspected; broader inequality survey not undertaken.'))
    save(O/'partial-backward-snowball.json',back)
    forward=[]
    for order in ['cited','recent']:
        p=raw/f'closure30_coppock_{order}.json';d=read(p)
        forward.append(dict(seed='Coppock2017',order=order,query=bind(p),cutoff='2026-10-07',indexed_count=d['meta']['count'],returned=len(d['results']),results=[dict(title=x.get('title'),date=x.get('publication_date'),doi=x.get('doi'),citations=x.get('cited_by_count'),disposition='Metadata only unless separately in source-support ledger')for x in d['results']],limit='Top5 and recent5 for this indexed identity; duplicates/incomplete indexing possible. Not exhaustive.'))
    forward.append(dict(seed='Hoeffding1963',status='not expanded',reason='Foundation for completed proof; no new open-ended research after deadline. General survey closure not claimed.'))
    save(O/'partial-forward-snowball.json',forward)
    save(O/'partial-claim-support.json',[
      dict(claim='Partial identification despite random invitations',support='PRIMARY_TECHNICAL_SUPPORT',anchor='Coppock2.1–2.4,equations1–16;binary specialization'),
      dict(claim='Invitations change precision;completion changes identification',support='PROJECT_DERIVATION',anchor='Fixed completion law,endpoint expectations,exact populations'),
      dict(claim='Finite-sample whole-set containment',support='PROJECT_DERIVATION and PRIMARY_TECHNICAL_SUPPORT',anchor='Explicit tilted-variance proof;Hoeffding Theorem2;independent customers and known Bernoulli probabilities'),
      dict(claim='Empirical intervals and decisions',support='GENERATED_EVIDENCE',anchor='2000datasets,8000ratecells;partial-recovery-corrected-summary.json;release exact-witnesses.json'),
      dict(claim='Outcome drift differs from nonresponse delta',support='PROJECT_DERIVATION and IMPLEMENTATION_EVIDENCE',anchor='Coppock2.7,pinned gen_mean,gamma27/76'),
      dict(claim='Conditional reuse recommendation',support='PROJECT_RECOMMENDATION',anchor='Static source only;no native execution/dependency acceptance')])
    save(O/'partial-omissions-risk.json',dict(omissions=[
      dict(source='Imbens–Manski,Stoye,Lee originals',reason='No new full-text comparative audit',risk='No shortest-interval or exhaustive-survey claim',next='Inspect genuine originals when interval/target choice changes'),
      dict(source='2025 weighted-quantile and randomized-response-instrument candidates',reason='Metadata only',risk='Extensions may affect comparators',next='Obtain originals before extension claims'),
      dict(source='2016 appendix',reason='Different author set from2017article',risk='Version conflation',next='Preserve separately;not final-paper proof'),
      dict(source='Native attrition1.0.0',reason='Static inspection only',risk='Inputs,small cells and runtime semantics unqualified',next='Match estimand/design;check R2 implies Attempt and R1=0,Attempt only R1=0,observed Y present,variance sample sizes'),
      dict(source='Dependent customers/unbounded rewards',reason='Outside binary IIDexample',risk='Theorem does not transfer',next='Specify dependence/tails before deriving guarantees')],external_obligations=['Historical-outcome truth','Recovery feasibility/prices','Independent acceptance'],survey_complete=False))
    print(json.dumps(dict(status='sources recorded',sources=len(records),ledgers=6)))
def prepare():
    snapshot=P/'publication-1/snapshot/docs';assert not snapshot.exists();snapshot.mkdir(parents=True)
    treatment=S/'writing-repair/2026-10-29/src/1de93e537048440f.tex'
    chapter=treatment.read_text();anchor=r'\section{When a random invitation still leaves selective recovery}'
    assert chapter.count(anchor)==1;raw=chapter[chapter.index(anchor):]
    text=re.sub(r'\\(section|subsection)\{',lambda m:'\\'+{'section':'chapter','subsection':'section'}[m[1]]+'{',raw)
    text=text.replace('The full-history design answers the preceding question only when a selected\nhistory can actually be recovered.',"A bank's plan to recover missing customer histories can fail at the follow-up stage.")
    text=text.replace('the earlier Gaussian servicing rewards','unbounded Gaussian servicing rewards')
    text=text.replace('A conservative finite-sample guarantee follows directly from the score\nranges.',r'A conservative finite-sample guarantee follows from the bounded-sum inequality of \citet[Theorem 2]{closure30hoeffding}, applied to these score ranges.')
    marker=r'\section{A recovered record can concern the wrong outcome}'
    figure=r'''
\begin{figure}[htbp]
\centering\includegraphics[width=\textwidth]{partial-recovery-figure.pdf}
\caption{Different purchases of information. Left: exact population effect
sets under the generated completion laws; the dashed line marks the historical
effect of ten percentage points. Right: intensive recovery with different
invitation rates, showing mean confidence-set width over 500 datasets per rate.
The dotted line is the unchanged population-set width. These are generated
comparisons, not bank measurements.}
\end{figure}
'''
    assert text.count(marker)==1;text=text.replace(marker,figure+chr(10)+marker)
    (snapshot/'partial-recovery.tex').write_text(text)
    for n in ['writing-repair/2026-10-29/src/1ceaa4065c38959e.tex','writing-repair/2026-10-29/src/c1f96ce05de9176e.tex','writing-repair/2026-10-29/causalplainnat-reading.bst']:
        p=snapshot/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(S/n,p)
    bib=(S/'writing-repair/2026-10-29/references-0.bib').read_text();entries=[]
    for key in ['rel73coppock2017','rel73attrition']:
        at=bib.index(key);a=bib.rfind('@',0,at);z=bib.find(chr(10)+'@',at);entries.append(bib[a:z if z>=0 else len(bib)])
    entries.append(r'''@article{closure30hoeffding,
author={Hoeffding, Wassily},title={Probability Inequalities for Sums of Bounded Random Variables},
journal={Journal of the American Statistical Association},year={1963},volume={58},number={301},pages={13--30},doi={10.1080/01621459.1963.10500830}}
''')
    (snapshot/'partial-refs.bib').write_text(chr(10).join(entries))
    root=(S/'causal_banking_release_candidate_2026-10-29.tex').read_text().split(r'\begin{document}',1)[0]
    root=re.sub(r'\\title\{.*?\\author',lambda _:r'\title{\sffamily\bfseries\color{ink}What a follow-up can establish}\author',root,flags=re.S)
    root=root.replace(r'\date{29 October 2026',r'\date{30 October 2026').replace('Causal Inference for Banking: Decisions, Evidence and Investment','What a follow-up can establish')
    root+=r'''
\begin{document}
\frontmatter\maketitle\mainmatter
\input{partial-recovery.tex}
\backmatter\bibliographystyle{writing-repair/2026-10-29/causalplainnat-reading}
\bibliography{partial-refs}
\end{document}
'''
    (snapshot/(STEM+'.tex')).write_text(root)
    fig,axs=plt.subplots(1,2,figsize=(7.4,2.9),layout='constrained')
    names=['Routine only','Standard','Intensive','Complete'];bounds=[(-.12,.64),(-.087,.154),(.056,.1108),(.1,.1)]
    for i,(lo,hi)in enumerate(bounds):axs[0].plot([100*lo,100*hi],[3-i,3-i],color='#23778A',lw=4,marker='o',markersize=4)
    axs[0].set_yticks(range(4),list(reversed(names)));axs[0].axvline(10,color='#555555',ls='--',lw=1)
    axs[0].set_xlabel('Effect (percentage points)');axs[0].set_title('Identification',fontsize=10)
    cells=read(O/'partial-recovery-corrected-summary.json')['regimes']['intensive']
    for m,label in [('hoeffding','Finite-sample bound'),('normal','Normal approximation')]:axs[1].plot([c['q']for c in cells],[100*c[m]['mean_set_width']for c in cells],marker='o',label=label)
    axs[1].axhline(5.48,color='#777777',ls=':',lw=1);axs[1].set_xlabel('Invitation probability');axs[1].set_ylabel('Width (percentage points)')
    axs[1].set_title('Precision under intensive recovery',fontsize=10);axs[1].legend(fontsize=7,frameon=False);axs[1].set_xticks([.1,.25,.5,1])
    for ax in axs:ax.spines[['right','top']].set_visible(False);ax.tick_params(labelsize=8)
    fig.savefig(snapshot/'partial-recovery-figure.pdf');plt.close(fig)
    save(P/'publication-1/extract-provenance.json',dict(source_treatment=bind(treatment),source_section=anchor,source_release=bind(R/'docs/causal_banking_release_candidate_2026-10-29.pdf'),changes=['Standalone hierarchy/opening','Original Hoeffding citation','Figure from retained quantities','Current batch086 financial decision paragraph retained'],inherited_release_changed=False,sources={str(p.relative_to(snapshot)):sha(p)for p in snapshot.rglob('*')if p.is_file()}))
    print(json.dumps(dict(status='prepared',snapshot=str(snapshot.relative_to(R)))))
if __name__=='__main__':
    actions=sys.argv[1:]
    if actions and actions[0]=='revision2':
        actions.pop(0);P=P/'revision-2';STEM='causal_banking_selective_recovery_v2_2026-10-30'
    for action in actions:
        if action=='sources':sources()
        elif action=='prepare':prepare()
        elif action=='build':base.O=P;base.S=P/'publication-1/snapshot/docs';base.NAMES={'short':STEM};base.build('short')
        else:raise SystemExit(action)

"""Integrate primary RL discovery arguments, source contracts and exact witnesses."""
import json
from pathlib import Path
import rl_discovery_boundary_reference_20261028 as exact
from prepare_followup_program_20261028 import ROOT,ref,write
DAY=ROOT/'docs/program/execution/2026-10-28';BASE=DAY/'rl-discovery-review-v1';FOLLOW=DAY/'followup-runtime-v3'

def main():
    assert not BASE.exists();BASE.mkdir();report=json.loads((FOLLOW/'python-rl-tail.json').read_text());deps=json.loads((FOLLOW/'cdt-dependencies.json').read_text())
    sources=[]
    authors=['Shengyu Zhu and Ignavier Ng and Zhitang Chen','Xiaoqiang Wang and Yali Du and Shengyu Zhu and Liangjun Ke and Zhitang Chen and Jianye Hao and Jun Wang']
    for key,p,author in zip(['zhu','wang'],report['papers'],authors,strict=True):
        text=(ROOT/p['text']['path']).read_text().split('\f');anchors=[]
        for a in p['inspected_anchors']:
            target=BASE/(key+'-page-'+str(a['physical_page'])+'.txt');target.write_text(text[a['physical_page']-1]);anchors.append(ref(target,a['finding']))
        title=p['title'];local=p['local_copy'];sources.append(dict(integrated_citation_key='exec28_rl_'+key,kind='paper',title=title,filename_title=title,author=author,authors=author.split(' and '),first_author=p['author'],year=p['year'],source_identity=p['source_identity'],url=p['source_identity'],local_path=local['path'],sha256=local['sha256'],version_date=p['version_date'],version_status=p['version_date'],local_copy=local,inspected_anchors=anchors,supported_claims=p['supported_claims'],claims=p['supported_claims'],inspected=['Physical pages '+','.join(str(a['physical_page']) for a in p['inspected_anchors'])],limitations='Selected original model,theorem and method anchors; no native replication,complete search or general uncertainty qualification.',identity_evidence=[p['acquisition_receipt'],ref(ROOT/'docs/literature/raw'/('exec28_rl_paper_'+('rl' if key=='zhu' else 'corl')+'_identity.html'),'Author,title and version identity')] ))
    for key,title,records,path in [('gcastle','gCastle selected reinforcement and ordering discovery source contracts',report['source_records'],FOLLOW/'python-rl-tail.json'),('cdt','CDT selected dependency,distribution and interpreter declarations',deps['source_records'],FOLLOW/'cdt-dependencies.json')]:
        sources.append(dict(integrated_citation_key='exec28_rl_'+key,kind='software_primary_sources',title=title,author='gCastle contributors' if key=='gcastle' else 'CausalDiscoveryToolbox contributors',year=2026,source_identity=records[0]['source_identity'],version_date=records[0]['version_date'],local_copy=records[0]['local_copy'],records=records,inspected_anchors=[a for r in records for a in r['inspected_anchors']],supported_claims=[c for r in records for c in r['supported_claims']],evidence=[ref(path,'Reviewed finite source work')],limitations=['Only exact selected branches inspected; no native execution.','Declared dependencies and source notices are not a resolved build or transitive rights clearance.']))
    write(BASE/'exact-results.json',exact.calculate())
    sources.append(dict(integrated_citation_key='exec28_rl_reference',kind='project_derivation_and_exact_reference',title='Authored penalty equality and keyword mask lookup witnesses',author='Causal banking proposal project',year=2026,source_identity='tools/rl_discovery_boundary_reference_20261028.py',version_date='28 October2026; finite exact constructions',local_copy=ref(Path(exact.__file__),'Independent exact construction'),inspected_anchors=[ref(BASE/'exact-results.json','Four-graph equality and keyword lookup results')],supported_claims=['At the non-strict penalty boundary,an arbitrary bounded score can tie cyclic and acyclic minimizers; strict domination excludes the cyclic tie in the witness.','Python keyword dictionaries require key lookup to retrieve a supplied dag_mask; attribute lookup returns the default.'],limitations=['Project qualification of a general stated condition; not a replicated BIC or native implementation result.']))
    write(BASE/'source-audit.json',dict(sources=sources,cutoff='2026-10-07T15:59:59Z',evidence=[ref(FOLLOW/n,'Performed bounded review') for n in ['python-rl-tail.json','cdt-dependencies.json']],native_execution=False))
    (BASE/'development.tex').write_text(DEVELOPMENT);(BASE/'sponsor-addition.md').write_text(SPONSOR)
    write(BASE/'mathematical-review.json',dict(status='pass',evidence=[ref(Path(exact.__file__),'Independent exhaustive finite enumeration'),ref(BASE/'exact-results.json','Exact equality and strict-boundary results'),ref(BASE/'zhu-page-5.txt','Original statement'),ref(BASE/'zhu-page-15.txt','Original reverse proof')],findings=['All four loopless two-node graphs enumerated:three DAGs and one cyclic graph.','SL=0,SU=1,lambda1=1,lambda2=0 satisfy the stated non-strict bound,but allfour penalized scores equal1.','A DAG remains an optimizer and optimal values agree; the stronger claim that every optimizer is acyclic needs strict domination or a declared acyclic tie rule.','No claim of BIC empirical failure or universal learning/calibration repair.'],native_execution=False))
    write(BASE/'copyedit-review.json',dict(status='pass',evidence=[ref(BASE/n,'Reviewed argument') for n in ['development.tex','sponsor-addition.md','exact-results.json']],findings=['Connects collections question to observational assumptions,search mechanics,source conversion and public fixtures.','Inherited theorem and project equality qualification are distinguished.','Source issues are conditional static findings; no false native outcome.']))
    write(BASE/'plan-review.json',dict(status='pass',scope='Preserve1418reader and1073sponsor records;add five source/project records including two genuine scholarly PDFs;pair exact reader.',evidence=[ref(FOLLOW/n,'Completed finite evidence') for n in ['python-rl-tail.json','cdt-dependencies.json']],checks=['All previous content and citation contexts retained.','Both scholarly sources have genuine named PDFs,edition identities and inspected technical anchors.','Equality case reviewed against both original proof directions.','Source mask,score,orientation,dropout and dependency limits do not infer native performance.','Run unchanged full controllers; preserve visual/full-coverage limitations.']))
    write(BASE/'review.json',dict(status='pass',issues=[],evidence=[ref(BASE/n,'Reviewed source package') for n in ['source-audit.json','mathematical-review.json','copyedit-review.json','plan-review.json','development.tex','sponsor-addition.md']],visual_acceptance=False,final_acceptance=False,native_execution=False))
    print(json.dumps(dict(records=len(sources),new_scholarly_pdfs=2,source_package=str(BASE.relative_to(ROOT)))))

DEVELOPMENT=r"""\section[Reinforcement search and discovery contracts]{Reinforcement search and discovery contracts}
\label{sec:exec28-rl}
Reinforcement learning can search for a causal graph without establishing that the graph is identified.
For a bank considering early reminders, the graph-search problem is to compare possible relations
among eligibility,reminder assignment,repayment and recorded customer characteristics. This is
different from learning a servicing policy that will act on customers. In the discovery methods
reviewed here, the reinforcement learner is an optimizer: its actions generate graphs or variable
orders, and a statistical score supplies a reward. A better search can improve a score while
leaving the information needed for a causal effect unchanged. Public or generated data can test
the search and interface contracts before costly bank experiments, provided the score's assumptions
and the target graph are declared separately.\citep{exec28_rl_zhu,exec28_rl_wang}

\subsection{Graph search versus ordering search}
Zhu,Ng and Chen formulate discovery as a search over directed graphs with a score and acyclicity
penalties. Their model discussion assumes scalar structural equations with jointly independent
additive noises,causal minimality and independently sampled observations. The paper explicitly
recognizes that further restrictions are needed for unique graph identification; its selected
experiments use identifiable families. Its encoder-decoder proposes adjacency matrices,and the
best-scoring sampled graph is the output of the search. Those statements do not establish validity
under a latent common cause,a persistent panel or unmeasured selection into reminders. In a
banking application, such features must be represented or restricted before the graph score can
be interpreted scientifically.\citep{exec28_rl_zhu}

Wang and coauthors instead search variable orderings. Each complete ordering defines a fully
connected acyclic candidate; variable selection subsequently removes edges. Their sequential
decoder masks previously selected nodes,and the paper distinguishes episodic and dense rewards.
The consistency discussion assumes an identifiable structural equation model and a suitable
distribution family. Its proposition explains why an ordering-compatible model reproducing the
same distribution must cover the true graph under those assumptions. It does not guarantee
global optimization by policy gradients; the paper explicitly discusses local convergence and
approximation. Ordering removes a combinatorial acyclicity burden from the candidate construction,
but does not remove misspecification,finite-sample selection error or causal nonidentification.
Attention in an encoder is a representation mechanism,not an edge-confidence or identification
certificate.\citep{exec28_rl_wang}

\subsection{A precise qualification at the penalty boundary}
For a graph $G$ with binary adjacency matrix $A$,write $S(G)$ for the score to minimize and
$h(A)=\operatorname{tr}(e^A)-d$ for the nonnegative cycle measure on $d$ nodes. The graph-search
formulation adds $\lambda_1\mathbf{1}\{G\notin\mathcal D\}+\lambda_2h(A)$,where $\mathcal D$
is the set of DAGs. Proposition1 in the inspected Zhu preprint gives the non-strict condition
\[
 \lambda_1+\lambda_2h_{\min}\geq S_U-S_L,
\]
with $S_L$ a lower bound on all graph scores,$S_U$ an upper bound on the optimum DAG score,and
$h_{\min}>0$ the smallest cycle measure over cyclic candidates. Its proof establishes that an
optimal DAG cannot be beaten by a cyclic candidate under this bound. At equality,however,that
argument need not exclude a cyclic candidate tied with the optimal DAG. The reverse proof uses
a strict improvement that does not follow from being a distinct tied minimizer. The distinction
matters if an implementation returns any maximizer of reward.\citep{exec28_rl_zhu}

An exact project construction isolates the boundary without making a claim about the paper's
empirical BIC results. Enumerate the four loopless directed graphs on two nodes. Assign score1
to each of the three DAGs and score0 to the two-cycle. Set $S_L=0$, $S_U=1$,
$\lambda_1=1$ and $\lambda_2=0$. The displayed condition holds with equality,and every penalized
score is1. The cyclic graph is therefore also a minimizer. The optimal value still equals the
DAG-constrained optimum,and an optimal DAG remains available; what fails is the stronger
conclusion that every unconstrained minimizer is acyclic.\citep{exec28_rl_reference}

A sufficient repair for that stronger conclusion is strict domination,
$\lambda_1+\lambda_2h_{\min}>S_U-S_L$. Then every cyclic penalized score is strictly greater
than $S_U$,whereas some optimal DAG has score at most $S_U$. Alternatively,an exact optimizer
can explicitly prefer a DAG among tied optimal candidates,if such a candidate is available.
In the finite witness,$\lambda_1=3/2$ makes the cyclic score $3/2$ and leaves the DAG scores1.
Neither repair proves that a practical policy-gradient search finds the global optimum or samples
a DAG. A returned candidate must still pass an independent acyclicity check,and approximate
cycle thresholds need a declared tolerance policy. The construction qualifies the stated general
score condition; it does not assert a failure rate for the original experiments.
\citep{exec28_rl_reference}

\subsection{What the selected implementation supports}
The selected gCastle source gives concrete contracts beyond the algorithm names. The RL reward
has BIC and unequal-variance variants,regression choices,and a cycle threshold of $10^{-5}$.
Its positive-$\ell_1$ branch refers to \texttt{l1\_grapha\_reg},whereas initialization stores
\texttt{l1\_graph\_reg}. Under the ordinary constructor path without an injected extra attribute,
that branch requires correction or a demonstrated supported alternative before enablement.
The selected normal-equation regression and median-scaled Gaussian-process paths also motivate
rank and scale fixtures. These are static source findings,not observed runtime error counts.
\citep{exec28_rl_gcastle}

The selected CORL entrypoint documents a \texttt{dag\_mask} keyword but retrieves it using
attribute lookup on the keyword dictionary. A plain Python dictionary does not expose a key
through that attribute lookup. The authored witness supplies an all-zero mask by key and obtains
the default through attribute lookup,while key lookup retrieves the mask. The next integration
must demonstrate that forbidden-edge constraints actually reach the graph constructor.
The inspected constructor builds order-consistent entries and multiplies by a mask; its pruning
routine treats row-selected columns as predictors of each variable,and the search returns a
transpose. This complete conversion needs a declared endpoint convention and a labelled
round-trip fixture. A high score cannot compensate for a reversed named edge.
\citep{exec28_rl_gcastle,exec28_rl_reference}

The reward comparison requires similar care. CORL's selected score branches omit the displayed
edge-count penalties,whereas the RL score includes them. That observation alone does not prove
incorrect ordering rankings: fully connected candidates of the same dimension have the same
number of edges before pruning. The correct comparison must trace which candidate is scored,
which regression family is fitted,and when pruning occurs. Its Transformer source normalizes
the attention scores along dimension1 and calls functional dropout without an explicit training
argument. A pinned tensor-library profile and repeated evaluation fixture should establish the
intended normalization and evaluation behavior before this path is adopted. These source details
do not turn an attention matrix into a causal graph.\citep{exec28_rl_gcastle}

\subsection{Dependency profiles and a finite public qualification}
The complementary CDT inspection shows why listing dependencies is insufficient. The selected
Python and R requirement files list package names without versions. Python setup and requirements
also differ: torch is listed in one route,while skrebate is included in setup. Container recipes use
mutable base-image tags and unpinned package installation. The default interpreter is
\texttt{Rscript},resolved from the environment unless overridden; the availability template calls
\texttt{library} rather than querying versions. A repository MIT notice and Apache2 setup metadata
remain different declarations,so neither should be silently promoted to a complete distribution
rights decision. A proposed reproducible environment must be selected and recorded explicitly;
these manifests cannot reconstruct an exact historical installation by themselves.
\citep{exec28_rl_cdt}

A finite public prototype can address these known interfaces without requiring bank truth.
First,bind one package/build/dependency route and its component terms. Second,use labelled
generated variables to test permutation,mask and endpoint preservation,including forbidden edges
and ambiguous graph output. Third,separate equality and strict-penalty examples from finite search
tests,retaining every failed or nonacyclic candidate in the denominator. Fourth,exercise constant,
collinear and nonfinite data and repeated evaluation under the selected regression and tensor
profile. Finally,inject failed children,large diagnostics,partial files and interruption into the
R boundary. Each fixture needs an independently declared expected result; a numerical output is
not automatically success. These are proposed conformance tests,not trials performed by this review.

Conditional reuse remains the defensible product decision. A narrow discovery adapter can retain
upstream search mechanics while imposing explicit variable,score,constraint and failure contracts.
A direct R route or a separately implemented ordering search may be preferable when those
contracts are easier to verify than a broad wrapper. Porting requires an additional equivalence
argument and maintenance budget. The two primary papers and selected code paths strengthen the
proposal's mechanism-level comparison,but do not exhaust reinforcement or attention-based
discovery,establish graph confidence,or qualify dependent banking data.
A discovery optimizer is useful only when its search result preserves the declared causal target and assumptions.
"""

SPONSOR=r"""# Qualify reinforcement discovery before reuse

Reinforcement learning in the reviewed discovery methods searches graphs or variable orderings; it does not itself learn an accepted banking servicing policy. Zhu and coauthors use a score with cycle penalties under an IID additive-noise model,while Wang and coauthors search orderings and then prune. The latter consistency discussion requires an identifiable model and suitable likelihood; policy-gradient optimization remains local. Better search or an attention representation therefore does not resolve latent confounding,panel dependence or uncertainty by itself. [@exec28_rl_zhu; @exec28_rl_wang]

An independent exact construction qualifies the non-strict penalty boundary in the first paper. On four two-node graphs,three DAGs have score1 and a cycle has score0. With lower bound0,upper bound1,penalty1 and no smooth penalty,all four penalized scores tie at1. The optimum value and an optimal DAG survive,but a cyclic minimizer survives too. Strict domination,or an explicitly justified acyclic tie rule,repairs that narrower conclusion; it does not prove that finite policy-gradient search succeeds. This is a project argument about the general stated condition,not a replicated failure of the paper's BIC experiments. [@exec28_rl_reference]

The selected gCastle source adds specific adapter requirements. CORL's documented mask is read by attribute lookup on a keyword dictionary; RL's positive regularization branch uses a differently spelled attribute from initialization. Order-to-matrix,pruning and output transpose need a labelled endpoint fixture. Selected attention normalization and dropout calls need a pinned tensor-profile check. These static findings require verification before native enablement and are not observed benchmark rates. [@exec28_rl_gcastle]

CDT's selected distribution recipes list unpinned Python/R dependencies,use mutable image tags,and resolve Rscript from the environment. Availability is not version identity,and the source/setup license declarations remain inconsistent. The next public/generated prototype should test exact build identity,variable permutations,forbidden-edge masks,score family,degenerate inputs and failed/interrupted children. Conditional thin-adapter reuse or direct R usage remains preferable to claiming an already qualified wholesale integration. [@exec28_rl_cdt]
"""

if __name__=='__main__':main()

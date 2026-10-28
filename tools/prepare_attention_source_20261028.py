"""Build a preserving attention-discovery proposal argument from reviewed originals."""
import json
from pathlib import Path
import attention_boundary_reference_20261028 as exact
from prepare_followup_program_20261028 import ROOT,ref,write
DAY=ROOT/'docs/program/execution/2026-10-28'
BASE=DAY/'attention-discovery-review-v1';FOLLOW=DAY/'followup-runtime-v4'


def main():
    assert not BASE.exists();BASE.mkdir()
    report=json.loads((FOLLOW/'attention-search.json').read_text())
    installer=json.loads((FOLLOW/'cdt-installer.json').read_text())
    paper=report['primary_papers'][0];pages=(ROOT/paper['extracted_text']['path']).read_text().split('\f')
    anchors=[]
    for a in paper['inspected_anchors']:
        p=BASE/('liu-page-'+str(a['physical_page'])+'.txt');p.write_text(pages[a['physical_page']-1]);anchors.append(ref(p,a['finding']))
    authors='Yusen Liu and Yong Wang and Yifan Yin and Tianqing Zhu and Xiufeng Liu and Huan Huo'
    sources=[dict(integrated_citation_key='exec28_at_liu',kind='paper',title=paper['title'],filename_title=paper['title'],
        author=authors,authors=authors.split(' and '),first_author='Liu',year=2026,
        source_identity=paper['acquisition']['source_identity'],url=paper['acquisition']['source_identity'],
        local_path=paper['local_copy']['path'],sha256=paper['local_copy']['sha256'],local_copy=paper['local_copy'],
        version_date=paper['edition'],version_status=paper['edition'],inspected_anchors=anchors,
        supported_claims=[a['finding'] for a in paper['inspected_anchors']],claims=[a['finding'] for a in paper['inspected_anchors']],
        inspected=['Physical pages 1,4,7,8'],identity_evidence=[paper['acquisition']['acquisition_receipt'],paper['identity']['local_copy']],
        limitations='Selected versioned preprint; 2025 proceedings identity not equated; no native replication or full search.')]
    specs=[('ct','CausalTransformer figure-reproduction source profile','sgao-academics/CausalTransformer','2026-09-01'),
           ('camcns','CAMCNs selected architecture and namespace source profile','nicoirribarra/CAMCNs-Causal-Discovery','2024-06-17'),
           ('tacd','TACD event discovery and model-selection source profile','Aquariuaa/TACD','2026-09-18'),
           ('tcdf','TCDF selected attention,permutation and delay source profile','M-Nauta/TCDF','2019-10-03')]
    for key,title,repo,date in specs:
        records=[r for r in report['selected_sources'] if '/'+repo+'/' in r['source_identity']]
        assert records
        sources.append(dict(integrated_citation_key='exec28_at_'+key,kind='software_primary_sources',title=title,
            author=repo+' contributors',year=2026,source_identity=records[0]['source_identity'],
            version_date=date+';'+records[0]['version'],local_copy=records[0]['local_copy'],records=records,
            inspected_anchors=[a for r in records for a in r['inspected_anchors']],supported_claims=[c for r in records for c in r['supported_claims']],
            evidence=[ref(FOLLOW/'attention-search.json','Finite source,tree,pin and query review'),ref(FOLLOW/'attention-static-inspection.json','Source-only namespace/tree inspection')],
            limitations=['Selected exact source branches only; no native execution or transitive dependency/rights qualification.','Software citation does not substitute for an unavailable scholarly original.']))
    records=installer['source_records']
    sources.append(dict(integrated_citation_key='exec28_at_cdt',kind='software_primary_sources',
        title='CDT pinned historical installer and unresolved remote dependency inputs',author='CausalDiscoveryToolbox contributors',year=2026,
        source_identity=records[0]['source_identity'],version_date='commit '+records[0]['version'],
        local_copy=records[0]['local_copy'],records=records,inspected_anchors=records[0]['inspected_anchors'],
        supported_claims=records[0]['supported_claims'],evidence=[ref(FOLLOW/'cdt-installer.json','Full15-line source review and unresolved immediate delegates')],
        limitations=['Installer and remote code not executed; remote script/package bodies not inspected; historical environment unresolved.']))
    write(BASE/'exact-results.json',exact.calculate())
    sources.append(dict(integrated_citation_key='exec28_at_reference',kind='project_derivation_and_exact_reference',
        title='Authored permutation,dependence and intervention distinction',author='Causal banking proposal project',year=2026,
        source_identity='tools/attention_boundary_reference_20261028.py',version_date='28 October 2026;exact finite construction',
        local_copy=ref(Path(exact.__file__),'Independent authored reference'),inspected_anchors=[ref(BASE/'exact-results.json','Exact covariance,loss and temporal calculations')],
        supported_claims=['A single-variable permutation can preserve the empirical marginal while changing joint and temporal statistics.','A fixed predictor can lose accuracy after permutation even when the stipulated structural effect is zero.'],
        limitations=['Project mathematical witness; not a native reproduction,empirical rejection rate or criticism of all permutation procedures.']))
    assert len(sources)==7
    write(BASE/'source-audit.json',dict(sources=sources,cutoff='2026-10-07T15:59:59Z',evidence=[ref(FOLLOW/n,'Performed finite review') for n in ['attention-search.json','cdt-installer.json','attention-omissions.json']],native_execution=False))
    (BASE/'development.tex').write_text(DEVELOPMENT);(BASE/'sponsor-addition.md').write_text(SPONSOR)
    write(BASE/'mathematical-review.json',dict(status='pass',evidence=[ref(Path(exact.__file__),'Independent exact calculation'),ref(BASE/'exact-results.json','Verified fractions'),ref(BASE/'liu-page-7.txt','Original permutation statement')],
        findings=['Marginal multiset preserved; covariance changes1/4 to-1/4 and fixed-predictor MSE0to1.','Alternative permutation changes adjacent agreement2/3to0.','Stipulated common-cause SCM X=U,Z=U has intervention contrast0; the finite sample witness is not a rate claim.','Conditional/blocked resampling is a proposed design requiring its own null/exchangeability argument.']))
    write(BASE/'copyedit-review.json',dict(status='pass',evidence=[ref(BASE/n,'Reviewed connected narrative') for n in ['development.tex','sponsor-addition.md']],findings=['Banking decision,variable clock,statistical target,alternatives and adoption conditions are connected.','Query counts and process logs stay outside product narrative.','Static source findings,author derivations,inherited assumptions and proposed native fixtures stay distinct.']))
    write(BASE/'plan-review.json',dict(status='pass',evidence=[ref(FOLLOW/n,'Completed recovered source packets') for n in ['attention-search.json','cdt-installer.json']],
        scope='Preserve1423reader and1080sponsor citations; add seven records,one scholarly PDF; reader1430/sponsor1089.',
        checks=['Retain all predecessor content and citation contexts.','Cite genuine Liu2026preprint; unavailable Nauta/Yang originals remain omissions.','Retain source license and runtime limits without adoption claims.','Pair exact reader/sponsor; run both unchanged full controllers; fresh visual/final acceptance remains open.']))
    write(BASE/'review.json',dict(status='pass',issues=[],evidence=[ref(BASE/n,'Reviewed publication input') for n in ['source-audit.json','mathematical-review.json','copyedit-review.json','plan-review.json','development.tex','sponsor-addition.md']],visual_acceptance=False,final_acceptance=False,native_execution=False))
    print(json.dumps(dict(records=7,new_scholarly_pdfs=1,source_package=str(BASE.relative_to(ROOT)))))


DEVELOPMENT=r"""\section[Attention discovery and evaluation contracts]{Attention discovery and evaluation contracts}
\label{sec:exec28-at}
Attention can rank predictive relationships without identifying the effect of a banking intervention.
Consider a bank asking whether an earlier reminder changes repayment, using histories of reminders,
balances, delinquency and recorded contacts. A prediction graph relates information available at
specified times to future repayments. An intervention question instead changes an assignment rule
and asks what would happen under that change. Shared financial stress, servicing selection and
measurement delays can make these different questions even when prediction is accurate. The
proposal therefore treats attention as a candidate-construction mechanism whose sampling law,
variable clock, graph meaning and evaluation procedure must be stated explicitly.

\subsection{Distinct meanings of attention and of a causal graph}
The inspected Liu preprint defines a DAG of Granger relationships, with Markov, faithfulness,
strict-order and minimum-signal assumptions. Its strict ordering is written as $i<j$ for a
relationship from variable $i$ to variable $j$, and the text excludes contemporaneous causation.
That is a substantive restriction on the admitted graph, rather than a consequence of computing
self-attention. A bank with feedback between arrears and subsequent reminders must decide whether
its nodes are time-indexed events, entire series, or a restricted ordering of series. A series-level
DAG cannot be silently substituted for an unfolded temporal graph with feedback across dates.
The inspected method aggregates attention contributions across tokens, selects potential edges
using an order-statistic threshold, and compares predictions after permuting a candidate series.
These operations support a particular predictive discovery procedure under the stated model;
they do not supply a general intervention-effect confidence region.\citep{exec28_at_liu}

Attention also describes different computational objects. In the selected TCDF implementation,
a trainable vector supplies a softmax gate on input variables before depthwise convolution and a
pointwise convolution. Candidate selection uses attention scores, and a later permutation step
compares a fitted model's loss on the original training target. The delay extraction reads maxima
of convolutional kernel weights. These are concrete mechanisms, but neither a gate weight nor a
kernel maximum is automatically an intervention coefficient. The inspected source's
\texttt{significance} parameter enters a loss-improvement fraction; that expression alone does
not establish a calibrated $p$-value or a familywise graph error guarantee. The software is cited
for these selected source mechanics; its scholarly article remains a separate primary-source
obligation.\citep{exec28_at_tcdf}

The selected CAMCNs model likewise contains a softmax feature gate followed by depthwise and
pointwise convolutions, while its discovery path adds correlation and lag selection. A README's
multihead description does not establish that every selected module implements query-key-value
multihead attention. The proposal should compare the actual selected computation, not collapse
all architectures into one label. Its entrypoint imports \texttt{train} and \texttt{VAL} from the
model module, whereas the inspected definitions are methods of \texttt{TCFMODEL} rather than
top-level functions. The namespace mismatch is a static integration finding at the pinned
source revision. It calls for a supported entrypoint or a documented repair and conformance
fixture before native evaluation; no runtime failure rate was measured here.
\citep{exec28_at_camcns}

\subsection{What permutation changes}
The inspected Liu text states that shuffling a candidate series while holding the other variables
fixed preserves the original data distribution. This requires qualification. A permutation
preserves that series' empirical marginal multiset, but generally changes its joint alignment
with other series and its temporal arrangement. The change can be the intended perturbation;
it cannot simultaneously be assumed to preserve every relevant observational law.
\citep{exec28_at_liu}

An exact author construction makes the distinction explicit. Let the four observations be
$x=z=(0,0,1,1)$, and keep $z$ fixed. Replacing $x$ with
$x^\pi=(1,1,0,0)$ leaves the marginal counts unchanged. With empirical covariance defined using
denominator four, however,
\[
 \widehat{\operatorname{Cov}}(x,z)=\tfrac14,
 \qquad \widehat{\operatorname{Cov}}(x^\pi,z)=-\tfrac14.
\]
The fitted predictor $f(x)=x$ has mean squared error zero before the permutation and one
after it. A different permutation, $(0,1,0,1)$, changes the proportion of adjacent equal values
from $2/3$ to zero. Thus even this small example separates preservation of the marginal,
the joint distribution and temporal structure.\citep{exec28_at_reference}

The predictive-loss increase does not by itself identify an effect. Suppose the structural model
is $X=U$, $Z=U$, where $U$ is a fair binary common cause. The displayed observations are compatible
with that model. Intervening on $X$ leaves the equation for $Z$ unchanged, so
$E[Z\mid\operatorname{do}(X=1)]-E[Z\mid\operatorname{do}(X=0)]=0$, despite the loss increase of
the fixed predictor under the displayed permutation. This is a project witness against a
universal interpretation of permutation importance as intervention effect. It is not an
empirical reproduction of the paper, an estimate of its error rate, or a claim that a properly
specified permutation test can never be valid.\citep{exec28_at_reference}

For repayment histories, the resampling design must answer a precise null question. An unrestricted
shuffle, a within-calendar shuffle, a block permutation and a conditional resampling scheme alter
different information. Restricting permutations can preserve some nuisance structure, but then
requires an exchangeability or conditional-law argument for the chosen null. Refitting after a
perturbation asks a different question from measuring reliance of a fixed predictor. Training,
candidate screening, threshold choice and held-out scoring also need separate information sets.
These are proposed design requirements; the exact witness establishes neither their calibration
under arbitrary banking dependence nor a universal repair for hidden common causes.

\subsection{Evaluation truth, empty denominators and temporal splits}
TACD addresses topological event sequences in telecommunications. Its selected source combines
attention with excitation, learned ordering and a regularized likelihood. This is a specialist
candidate for questions about event propagation, not an interchangeable estimator for IID tabular
reminder data. Any banking adaptation would first define devices or counterparties, event types,
network exposure and observation time. The resulting point-process or event target must remain
explicit through the adapter.\citep{exec28_at_tacd}

Two selected evaluation branches are especially consequential. When \texttt{dag\_matrix} is supplied,
the training routine passes it to threshold optimization and computes graph F1 for checkpoint
selection. Such an experiment uses graph truth in model selection. It can be legitimate as a
declared oracle-assisted or training-graph study, but its score cannot be presented as blind
held-out discovery on that same truth. A public qualification should freeze thresholds and
selection rules on training graphs, then evaluate once on separate unseen graphs and independent
realizations under the intended deployment information. A prediction-loss selection branch is
also available in the selected source; it addresses a different objective and still requires
an explicit connection between prediction and graph quality.\citep{exec28_at_tacd}

The evaluation routine omits NaN losses and divides the accumulated loss by
$\max(n_{\rm valid},1)$. If no batch has a valid loss, this returns zero. Zero is then a
sentinel produced by an empty effective denominator, not observed perfect prediction. The adapter
must preserve requested, valid and failed counts and return an unavailable score when the
predeclared valid-data rule fails. Likewise, the entrypoint randomly shuffles event pairs and
uses a default \texttt{split\_ratio} of one when that key is absent; at values at least one,
the training and validation pair lists are the same. This is a conditional source branch,
not a claim about every supplied dataset configuration. Event pairs may also share history,
so a row split alone need not isolate information. The exact configuration and event-construction
delegates must be inspected before a native trial's split is described as temporal or independent.
\citep{exec28_at_tacd}

The appropriate public experiment therefore separates four denominators: candidate graphs
requested, graphs returned, graphs selected using available training information, and graphs
scored on untouched evaluation truth. Failed batches and unsupported graphs remain visible.
Evaluation on a known synthetic graph can verify mechanisms cheaply, while observational public
financial data can test data contracts and sensitivity without supplying nonexistent graph truth.
Neither exercise should be promoted to bank validation solely because the dataset is public.

\subsection{Reproduction scope and dependency identity}
The selected CausalTransformer repository illustrates a further boundary. Its README describes
figure regeneration from recorded benchmark results and explicitly says that model-training
benchmarks are not rerun. A reproduction command for those figures therefore does not by itself
reproduce learning, data generation, selection or reported performance. In the inspected revision,
the runner also conditionally requests two LaTeX source files that are absent from the complete
selected tree. That is a static packaging mismatch, not an observed execution result. The stated
journal target and current repository description cannot establish publication acceptance, and
an academic-review notice alone does not establish a broad reuse grant. The defensible proposal
disposition is to retain the artifact as a limited reproduction lead until the training source,
primary article and reuse terms are resolved.\citep{exec28_at_ct}

Dependency identity is equally important for a method that delegates to R. The inspected CDT
installer is itself pinned, but installs unversioned operating-system and R packages, uses
several unauthenticated-package options, references HTTP CRAN endpoints, sources a mutable
Bioconductor script, and requests GitHub packages without commit pins. Freezing the wrapper's
bytes does not freeze those remote inputs. The installer was inspected as text and was not run;
the immediate remote script and package-installation bodies remain unresolved dependencies.
A proposed replacement should bind the operating system, interpreter, compiler, package archives,
digests and component terms, then qualify a selected isolated environment on public fixtures.
Verified HTTPS acquisition and an archive identity are necessary provenance steps, but do not
by themselves establish scientific correctness or transitive rights.\citep{exec28_at_cdt}

\subsection{A conditional product decision}
The present evidence supports a differentiated reuse strategy. TCDF and CAMCNs can inform a
time-series candidate-generation comparison after their selected source and dependency contracts
are resolved. Their inspected GPL notices require component-level intake for the intended use;
this proposal does not declare a legal clearance. TACD is a specialist event-network candidate
whose truth-assisted selection and split routes need an explicit public protocol. CausalTransformer
currently contributes a figure-reproduction artifact rather than an established native learner
route. Porting any method would add an equivalence and maintenance obligation; an isolated adapter
may be preferable when it can retain upstream computation and expose the required semantics.
\citep{exec28_at_tcdf,exec28_at_camcns,exec28_at_tacd,exec28_at_ct}

Before enablement, a finite fixture set should check variable and timestamp identity, permitted
lags, target shifting and padding, missing and nonfinite values, candidate threshold ties,
empty score denominators, training/evaluation separation and failure propagation. A second layer
should compare generated confounded and unconfounded systems with independently specified truth,
including a fixed-predictor permutation witness. These are proposed public qualification steps,
not results of executing the acquired packages. The final report should retain predictive and
interventional targets separately, state which identification assumptions are substantive, and
refuse an effect claim when the required information is absent.
Attention discovery becomes a useful proposal component only when its predictive target, evaluation information and reuse conditions remain explicit.
"""

SPONSOR=r"""# Separate attention discovery from intervention evidence

Attention discovery offers several distinct mechanisms. The inspected Liu preprint uses a restricted Granger graph, aggregates attention into potential edges, and evaluates a fixed predictor after permutation. TCDF and the selected CAMCNs model instead expose a trainable feature gate with temporal convolutions. These mechanisms can propose predictive relationships, but the proposal must separately state the banking intervention, graph meaning, observation clock and identifying assumptions. [@exec28_at_liu; @exec28_at_tcdf; @exec28_at_camcns]

An exact authored example qualifies the claim that single-variable permutation preserves the original distribution. With X=Z=(0,0,1,1), reversing X preserves its marginal counts but changes covariance from1/4to-1/4 and fixed-predictor MSE from0to1. Under the stipulated common-cause model X=U,Z=U, intervention on X still has zero effect on Z. The example distinguishes model reliance from causal effect; it is not an empirical replication or a universal rejection of permutation tests. [@exec28_at_reference]

TACD is a specialist event/topology candidate. Its selected source can use a supplied true graph for threshold and checkpoint selection, and an evaluation branch returns zero if no valid batches remain. An absent split-ratio setting defaults to shared training/validation pairs. Public qualification should therefore separate oracle-assisted selection from untouched graph evaluation, preserve failed denominators, and specify temporal information boundaries before reporting performance. These are conditional static findings, not measured runtime rates. [@exec28_at_tacd]

The selected CausalTransformer artifact regenerates figures from stored results; it does not rerun model training. Its conditional LaTeX route requests absent source files, and the inspected academic-review statement does not resolve broad reuse rights. CDT's pinned historical installer still resolves mutable, unversioned remote inputs. Conditional adapters, exact dependency identities and component-level rights intake remain the proposed route; porting requires additional equivalence and maintenance evidence. The acquired software was not executed. [@exec28_at_ct; @exec28_at_cdt]
"""


if __name__=='__main__':main()

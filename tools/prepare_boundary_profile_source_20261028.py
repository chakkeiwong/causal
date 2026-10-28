"""Prepare connected manuscript additions from two completed source packets."""
import json
from pathlib import Path
import boundary_profile_reference_20261028 as exact
from prepare_followup_program_20261028 import ROOT,ref,write

BASE=ROOT/'docs/program/execution/2026-10-28/boundary-profile-review-v1'
FOLLOW=ROOT/'docs/program/execution/2026-10-28/followup-runtime-v2'

def main():
    assert not BASE.exists();BASE.mkdir()
    cdt=json.loads((FOLLOW/'cdt-delegates.json').read_text());server=json.loads((FOLLOW/'local-profile.json').read_text())
    sources=[]
    for key,title,author,records,report in [
      ('cdt','CDT R templates and launcher with a separate pcalg score comparator','CausalDiscoveryToolbox and pcalg contributors',cdt['sources']+[cdt['pcalg_comparator']],FOLLOW/'cdt-delegates.json'),
      ('ollama','Ollama selected server routing, streaming and model-residency contracts','Ollama project contributors',server['sources'],FOLLOW/'local-profile.json')]:
        sources.append(dict(integrated_citation_key='exec28_bp_'+key,kind='software_primary_sources',title=title,author=author,year=2026,source_identity=records[0]['source_identity'],version_date=('CDT ff46dbca3d91f2dba30e6ae54986eea30c9b331f; separate pcalg comparator version in records' if key=='cdt' else '2026-10-07T04:39:34Z;d3c846f8b0279e79b0e3a960a7575fde6920e9df'),local_copy=records[0]['local_copy'],records=records,inspected_anchors=[a for r in records for a in r['inspected_anchors']],supported_claims=[c for r in records for c in r['supported_claims']],evidence=[ref(report,'Bounded technical review')],limitations=['Selected source branches only; no downloaded code or model executed.','Separately selected comparator is not a resolved dependency.','Build, weights, transitive rights, native behavior and full coverage remain unqualified.']))
    write(BASE/'exact-results.json',exact.calculate())
    sources.append(dict(integrated_citation_key='exec28_bp_reference',kind='project_derivation_and_exact_reference',title='Authored positional conversion and streaming admission witnesses',author='Causal banking proposal project',year=2026,source_identity='tools/boundary_profile_reference_20261028.py',version_date='28 October 2026; exact authored constructions',local_copy=ref(Path(exact.__file__),'Independent finite witness'),inspected_anchors=[ref(BASE/'exact-results.json','Exact permutation and six-state calculation')],supported_claims=['Sorting only labels reverses the named edge in the stipulated two-node matrix.','Exactly one of six stipulated HTTP200 traces satisfies the proposed terminal,validity and identification gate.'],limitations=['No native outcome, vendor price or banking performance measurement.']))
    write(BASE/'source-audit.json',dict(sources=sources,cutoff='2026-10-07T15:59:59Z',evidence=[ref(FOLLOW/n,'Completed selected-source packet') for n in ['cdt-delegates.json','local-profile.json']],native_execution=False))
    (BASE/'development.tex').write_text(DEVELOPMENT)
    (BASE/'sponsor-addition.md').write_text(SPONSOR)
    write(BASE/'mathematical-review.json',dict(status='pass',evidence=[ref(Path(exact.__file__),'Independent authored calculation'),ref(BASE/'exact-results.json','Exact outputs')],findings=['The same positional matrix names opposite directed edges under incompatible label orders.','A conjunction requiring recognized inference termination,no error,valid representation and identification admits exactly one stipulated trace.'],native_execution=False))
    write(BASE/'plan-review.json',dict(status='pass',scope='Preserve all1415reader and1068sponsor records; add three bounded source/project records plus exact sponsor pairing.',evidence=[ref(FOLLOW/n,'Reviewed source packets') for n in ['cdt-delegates.json','local-profile.json']],checks=['Existing content inputs and citation contexts remain unchanged.','CDT and separate pcalg identities are not conflated.','Ollama client,server,build,runner and model identities remain distinct.','Public authored fixtures explain failure modes without pretending to execute third-party code.','Use unchanged original full controllers and consume process exits.','No fresh visual acceptance; original coverage outcomes remain inconclusive.']))
    write(BASE/'copyedit-review.json',dict(status='pass',evidence=[ref(BASE/n,'Connected source-grounded argument') for n in ['development.tex','sponsor-addition.md','exact-results.json']],findings=['Banking question,variable order,score semantics and admission state are connected.','Inferences and proposed adapter requirements are explicitly separated from observed source branches.','No native,rights or scientific qualification is inferred from documentation.']))
    write(BASE/'review.json',dict(status='pass',issues=[],evidence=[ref(BASE/n,'Reviewed addition') for n in ['plan-review.json','source-audit.json','mathematical-review.json','copyedit-review.json','development.tex','sponsor-addition.md']],visual_acceptance=False,final_acceptance=False,native_execution=False))
    print(json.dumps(dict(prepared=str(BASE.relative_to(ROOT)),added_records=len(sources))))

DEVELOPMENT=r"""\section[Discovery delegates and local model boundaries]{Discovery delegates and local model boundaries}
\label{sec:exec28-bp}
A banking proposal must preserve variable identity across discovery and execution boundaries.
Consider a collections team asking whether an early reminder changes later repayment.
Its proposed workflow first represents an information clock and candidate graph, then asks whether
the reminder effect is identified under that graph and the available observations. A Python
discovery wrapper and a local language-model endpoint can help implement this workflow, but each
introduces a separate conversion contract. The first can change the names attached to a matrix;
the second can change the place or completion state of a computation. Neither conversion may
silently redefine the causal question. The following comparison concerns selected original
source paths and exact authored examples, not an executed integration.

\subsection{What an R delegate actually contributes}
The selected CausalDiscoveryToolbox (CDT) commit delegates PC and GES through R templates.
The PC template loads pcalg, kpcalg, methods and RCIT, selects its conditional-test route, and
sets algorithm options including the stable.fast method and majority/conflict behavior.
Although the template's options list contains a core-count field, the inspected call does not
pass that field to PC. A proposal therefore cannot infer parallel scaling from the existence
of the field. The data and constraint matrices cross the boundary as headerless CSV, and a
matrix returns through another CSV. The representation has lost the protection that named
variables could otherwise provide.\citep{exec28_bp_cdt}

The GES path provides a second semantic warning. Its wrapper describes an \texttt{int} option
with a categorical label while mapping that option to \texttt{GaussL0penIntScore}. The selected
template constructs the chosen score using the data alone, runs GES, extracts the essential
graph and writes a matrix. In the separately inspected pcalg source, that class is Gaussian;
its default target list is empty and its default row assignment places every row in the first
environment. This comparator explains why an adapter must inspect the actual likelihood and
intervention metadata. It does not prove which pcalg version a particular CDT installation
resolves. An intervention-labelled class name does not create an intervention design, and a
Gaussian score is not made appropriate for categorical banking outcomes by a wrapper's label.
The exact R and package versions, endpoint conventions and categorical alternative remain
explicit selection requirements.\citep{exec28_bp_cdt}

Variable order is independently consequential. In the inspected direct-orientation paths,
skeleton or output labels are sorted while the input data retain their original column order.
This source observation motivates a conversion fixture; it is not a measured defect rate.
Let the declared data order be $v=(z,a)$ and suppose the interface convention interprets
$A_{ij}=1$ as a directed edge from row variable $i$ to column variable $j$. For the authored matrix
\[
 A=\begin{pmatrix}0&1\\0&0\end{pmatrix},
\]
the edge is $z\to a$. If the matrix stays fixed but labels become $(a,z)$, the named edge becomes
$a\to z$. A correct reordering uses the same permutation for the data, constraint matrices,
result matrix and label vector. Under a permutation matrix $P$, the corresponding matrix is
$PAP^{\mathsf T}$; changing labels alone does not perform that operation. The two-node example
reproduces exactly in the project reference. Its directed convention is stipulated for the
witness; PC/GES endpoint encodings must still be established on their selected native paths.
For reminder and repayment variables, exchanging names would change the scientific question
before an identification routine even starts.\citep{exec28_bp_reference,exec28_bp_cdt}

The launcher introduces a different boundary. It creates a UUID-based template copy and
performs literal placeholder replacement. The inspected callback branch waits for the child
process and then retrieves output without conditioning that retrieval on a checked return code.
Package-availability probes do not record a resolved version or establish redistribution rights.
The source consequently motivates explicit trials for failed children, large stderr, partial
CSV, interrupted execution and stale output; it supplies no observed results for those trials.
A typed adapter should bind an ordered-variable manifest, data/constraint identities, score
family, interventions, selected package versions, exit state and output provenance before
returning an identified query to a banking user. A direct pcalg route is a substantive alternative
when explicit R dependency control is preferable. A wholesale port would add a numerical and
semantic equivalence obligation without resolving identification by itself. We therefore propose
conditional reuse of the selected delegate through a thin adapter, while deferring native
enablement until these finite conversion and failure contracts have been demonstrated.
\citep{exec28_bp_cdt}

\subsection{A local endpoint is only one part of a model profile}
The previously inspected Ollama Python client requires a separately selected server and model.
The current server review pins eleven originals to commit
\texttt{d3c846f8b0279e79b0e3a960a7575fde6920e9df}, dated 7 October 2026.
The source variable \texttt{Version} contains the placeholder \texttt{0.0.0}; this is not a
verified release identifier. The module file declares a Go toolchain requirement and dependency
versions, but does not by itself establish a reproducible binary or complete transitive rights.
The selected server's MIT notice and a Modelfile's license declaration also do not independently
establish the rights of separately obtained weights. A useful profile must bind the client,
server commit and build, runner, model manifest and weight hashes, tokenizer/template,
quantization, request configuration and execution destination. Unknown fields should remain
unknown until inspected, rather than inheriting a reassuring product-level label.
\citep{exec28_bp_ollama}

This distinction matters to a banking workflow that may contain customer information.
The inspected API documentation distinguishes local and cloud endpoints, while also describing
cloud inference through a local server. The selected Chat handler has an explicit remote-model
branch: it checks the remote configuration, forwards the request and records remote host and
model fields in responses. Thus a localhost address alone is insufficient evidence that inference
stays on the machine. The documentation describes local requests without authentication and
separate cloud credentials. These are source-supported boundary conditions, not a security
assessment of a deployed system. The proposal should require an explicit routing decision and
deployment controls for its chosen profile; a private local prototype can be designed using
public or generated data before bank data are involved.\citep{exec28_bp_ollama}

\subsection{Completion, residency and scientific admission}
Selected endpoints stream newline-delimited JSON. The documented protocol includes nonterminal
chunks, a terminal \texttt{done} field and a stop reason. In the inspected stream handler an error
before output can set an HTTP error status; after output begins, an error is encoded in the
stream. The documentation correspondingly warns that an error arriving midstream cannot change
the status already sent. Receiving HTTP 200 and a plausible text prefix therefore does not
establish successful completion. Moreover, the inspected Chat handler can return
\texttt{done=true} with reason \texttt{unload}; successful unloading is not successful inference.
The full response state must survive the adapter boundary.\citep{exec28_bp_ollama}

Define $T$ to mean a recognized inference terminal state, $E$ an error anywhere in the trace,
$V$ successful validation against the original response contract, and $I$ an identified causal
target under explicitly recorded assumptions. A proposed admission rule is
\[
 \mathrm{admit}=T\land\neg E\land V\land I.
\]
The precise terminal reasons allowed by $T$ belong to the chosen endpoint and profile.
In an authored six-trace example we stipulate an HTTP 200 status for every trace and allow
\texttt{stop} as the successful inference reason. Only the complete, valid, identified trace
passes. A midstream error, truncated trace, unload response, invalid representation and
nonidentified query each fail a different conjunct. Exactly one trace is admitted and five are
rejected. This is a transparent specification example, not evidence of a six-request model test
or an estimate of error frequency. A rejected inference may still yield a useful explanation,
identified set or request for more information; rejection must not be hidden as a numeric zero.
\citep{exec28_bp_reference}

Model residency must also be separated from workflow recovery. The request type describes
\texttt{keep\_alive} as how long a model stays loaded, and the inspected scheduler decrements
reference counts and schedules unloading after the residency duration. This does not persist
the banking decision, original assumptions, tool effects or a recoverable conversation.
Similarly, the generation path propagates a request context and cancels it on a selected parser
error, but source-level context propagation is not an observed guarantee that all downstream
work has stopped. The request's format is passed to a runner; this forwarding alone does not
establish conformance to every original schema constraint. Native cancellation and format
fixtures remain necessary for the chosen runner and model.\citep{exec28_bp_ollama}

\subsection{Public prototype route and adoption decision}
These observations define a finite next prototype without requiring costly bank experiments.
The discovery fixture should use public or generated labelled columns, permutations and
constraint matrices, plus intentionally failing children, to test whether the selected CDT/R
path preserves the declared graph representation and refuses incomplete output. The model
fixture should bind one permitted build and weight profile, exercise complete and interrupted
streams, validate against the original schema, and retain routing and stop-state evidence.
The two exact authored witnesses provide independent expected behavior for narrow interface
contracts; they do not provide a truth oracle for an arbitrary discovered graph or language-model
answer. Native implementation, rights review and actual trial results remain separate work.

The proposed investment choice is therefore conditional reuse, with explicit alternatives.
CDT can supply selected discovery orchestration if its conversions and dependencies are controlled;
direct R usage can reduce wrapper ambiguity; a port is justified only when the maintenance and
equivalence burden is preferable. Ollama can supply a selected inference service boundary after
build, model, routing and termination contracts are pinned. A managed service is a different
choice with its own entitlement, cost and data-handling evidence. Neither choice earns causal
identification from a successful call. The resulting proposal keeps source-supported capabilities,
project specifications and future empirical qualifications distinct.
Variable identity and execution identity must survive every boundary before a causal result is admitted.
"""

SPONSOR=r"""# Bind discovery and model execution boundaries

The reminder-to-repayment workflow can fail before causal identification if a discovery wrapper changes variable order. Inspection of selected CDT R templates, Python wrappers and launcher shows why the proposal needs explicit score, intervention, dependency, matrix and failure contracts. The option labelled categorical selects a Gaussian interventional-score class name; a separately inspected pcalg comparator explains the Gaussian/default-target semantics but is not proof of the dependency resolved by CDT. Sorted skeleton/output labels and original-order data motivate a permutation fixture. The callback launcher retrieves output after waiting without checking the child return code on that branch. These are bounded static findings, not measured native failure rates. Conditional reuse through a typed adapter, or direct declared pcalg usage, is preferable to an unqualified wholesale port. [@exec28_bp_cdt]

An exact authored two-variable example makes the conversion risk concrete: a fixed matrix representing z to a is relabelled as a to z if only the labels are sorted. A separate six-trace specification assigns HTTP 200 to every trace, but admits only the complete, valid, identified inference. Midstream error, truncation, unload, invalid representation and nonidentification remain explicit failure states. These examples are independent interface witnesses, not package or model experiments. [@exec28_bp_reference]

The Ollama comparison now includes eleven pinned server originals as well as the prior client evidence. The selected documentation and code distinguish local and cloud execution, show that a local endpoint can forward to a remote model, and retain remote identity in responses. Streaming errors after output begins cannot replace the original HTTP status. A done flag can describe unloading; keep_alive concerns model residency rather than durable workflow state. The selected version variable is a placeholder, so the server commit and actual build must be bound separately. The source license does not settle the rights of model weights. The required profile therefore includes client, server build, runner, model manifest and hashes, tokenizer/template, quantization, configuration and execution destination. [@exec28_bp_ollama]

The next economic step is a finite public/generated prototype: permutation and failed-child fixtures for the selected discovery delegate, and terminal/error/schema/routing fixtures for one permitted model profile. Exact source versions, separate weight rights, actual native behavior and full request costs remain unresolved qualification items. No bank data or live model execution was used in this review. The proposal gains a concrete integration route without treating documentation or HTTP success as demonstrated causal merit.
"""

if __name__=='__main__':main()

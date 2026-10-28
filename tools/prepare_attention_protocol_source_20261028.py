"""Audit exact delegate-level temporal and evaluation protocols for a preserving edition."""
import json
from pathlib import Path
from record_attention_installer_recovery_20261028 import original,anchors
from prepare_followup_program_20261028 import ROOT,ref,write

DAY=ROOT/'docs/program/execution/2026-10-28'
BASE=DAY/'attention-protocol-review-v4'
FOLLOW=DAY/'followup-runtime-v5'
FOLLOW6=DAY/'followup-runtime-v6'


def main():
    assert not BASE.exists();BASE.mkdir()
    plans={}
    for name in ['attention-primary-plan.json','tcdf-source-plan.json']:
        plans.update({r['id']:r for r in json.loads((DAY/'followup-runtime-v4'/name).read_text())['requests']})
    plans.update({r['id']:r for r in json.loads((FOLLOW/'delegate-acquisition-plan.json').read_text())['requests']})
    ids=['exec28_tcdf_source_2','exec28_tcdf_delegate_0','exec28_tacd_delegate_0','exec28_tacd_delegate_1','exec28_tacd_delegate_2','exec28_tacd_delegate_3']
    records={i:original(plans[i]) for i in ids}
    anchor_map={
      'exec28_tcdf_source_2':[(14,28,'Target-only one-step lag; first shifted target value set to zero'),(31,79,'Target-specific model trained using shifted input and unshifted target')],
      'exec28_tcdf_delegate_0':[(6,12,'Right-edge chomp slice; zero size yields empty slice'),(14,23,'Grouped convolution,declared padding and right-edge chop'),(35,53,'Dilated residual block uses same chomp mechanism'),(55,72,'Final block includes a learned across-channel linear map'),(74,96,'Exponential dilation schedule and receptive-field padding')],
      'exec28_tacd_delegate_0':[(3,13,'Simulation profile explicitly sets split_ratio=1.0'),(15,24,'18V profile explicitly sets split_ratio=1.0'),(27,36,'24V profile explicitly sets split_ratio=1.0'),(39,49,'25V profile explicitly sets split_ratio=1.0')],
      'exec28_tacd_delegate_1':[(8,25,'Manual confusion counts iterate the full matrix,including diagonal'),(28,49,'Threshold curve removes diagonal,selects F1 maximizer and uses strict greater-than')],
      'exec28_tacd_delegate_2':[(7,23,'24V/25V data branches load true graph and reorder supplied fields'),(24,38,'18V branch loads true graph'),(39,42,'Simulation falls through with no selected data branch before returning locals')],
      'exec28_tacd_delegate_3':[(9,14,'CLI names dataset choices and seed limitation'),(38,48,'CLI threshold,seed and configuration surface'),(51,60,'Loaded graph supplied into discovery and reused for output threshold/metrics')],
    }
    for key,spans in anchor_map.items():records[key]=anchors(records[key],spans)
    config=json.loads((FOLLOW/'delegate-exact-results.json').read_text())
    fixture=json.loads((FOLLOW6/'public-fixture.json').read_text())
    assert config['temporal']['non_target_lags']==list(range(8))
    assert config['temporal']['shifted_target_lags']==list(range(1,9))
    write(BASE/'protocol-exact-results.json',dict(status='pass',temporal=config,fixtures=fixture))
    tcdf=[records['exec28_tcdf_source_2'],records['exec28_tcdf_delegate_0']]
    tacd=[records[k] for k in ['exec28_tacd_delegate_0','exec28_tacd_delegate_1','exec28_tacd_delegate_2','exec28_tacd_delegate_3']]
    sources=[
      dict(integrated_citation_key='exec28_at_tcdf_temporal',kind='software_primary_sources',
           title='TCDF exact target-shift and dilated temporal support delegates',author='M-Nauta/TCDF contributors',
           year=2019,source_identity=tcdf[0]['source_identity'],version_date='2019-10-03;commit 82422321492effdf5666c7f7f1ca14196c41ed3d',
           local_copy=tcdf[0]['local_copy'],records=tcdf,inspected_anchors=[a for r in tcdf for a in r['inspected_anchors']],
           supported_claims=[a['finding'] for r in tcdf for a in r['inspected_anchors']],
           evidence=[ref(FOLLOW/'tcdf-delegate.json','Prior exact delegate support review')],
           limitations=['Static source/index derivation only; no tensor runtime or learned-delay validation.','Scholarly article original remains a separate omission.']),
      dict(integrated_citation_key='exec28_at_tacd_protocol',kind='software_primary_sources',
           title='TACD exact profile,threshold,data and CLI delegates',author='Aquariuaa/TACD contributors',
           year=2026,source_identity=tacd[0]['source_identity'],version_date='2026-09-18;b2f45faaaa8048691955776e12ad1bf33713e8cc',
           local_copy=tacd[0]['local_copy'],records=tacd,inspected_anchors=[a for r in tacd for a in r['inspected_anchors']],
           supported_claims=[a['finding'] for r in tacd for a in r['inspected_anchors']],
           evidence=[ref(FOLLOW/'tacd-protocol.json','Prior exact entrypoint/config review')],
           limitations=['Selected pinned files only; missing data_mapto_es.py and transitive scorer semantics remain unresolved.','No native package execution or empirical result.']),
      dict(integrated_citation_key='exec28_at_protocol_reference',kind='project_derivation_and_exact_reference',
           title='Authored temporal support,strict threshold and public split fixtures',author='Causal banking proposal project',
           year=2026,source_identity='tools/attention_delegate_reference_20261028.py',
           version_date='28 October 2026;exact independent constructions',
           local_copy=ref(ROOT/'tools/attention_delegate_reference_20261028.py','Independent exact derivations'),
           inspected_anchors=[ref(FOLLOW/'delegate-exact-results.json','Finite support,threshold and empty-score results'),
                              ref(FOLLOW6/'public-fixture.json','Proposal-owned public contract fixtures')],
           supported_claims=['Declared convolution support is causal in index order but includes contemporaneous non-target variables; target shift changes raw target lags.','Strict and inclusive threshold comparisons can differ on tied scores.','Validation truth and evaluation truth belong to different information sets; zero valid outcomes must not become a numeric zero score.'],
           limitations=['Authored contract expectations,not native PyTorch/scikit-learn result,calibration rate or bank experiment.'])
    ]
    write(BASE/'source-audit.json',dict(sources=sources,cutoff='2026-10-07T15:59:59Z',
        input_evidence=[ref(FOLLOW/n,'Performed finite source/fixture result') for n in ['tcdf-delegate.json','tacd-protocol.json']]+[ref(FOLLOW6/n,'Performed finite source/fixture result') for n in ['public-fixture.json','python-discovery-delta.json']],
        exact_source_records=records,native_execution=False))
    development=DEVELOPMENT.replace('A zero-layer profile also has no convolutional support to report.',
        'A zero-layer Sequential stack is an identity on the input, so its support is lag zero; this is not the same as an empty output.')
    development=development.replace('If $K=1$, then $p=0$ and the\nselected source still applies the slice',
        'If $K=1$, then $p=0$ and the\nselected source still applies the slice')
    (BASE/'development.tex').write_text(development);(BASE/'sponsor-addition.md').write_text(SPONSOR)
    write(BASE/'mathematical-review.json',dict(status='pass',evidence=[ref(BASE/'protocol-exact-results.json','Exact support and threshold fixtures'),ref(BASE/'source-audit.json','Exact source anchors')],
        findings=['For the stated stride-one padded/cropped convolution, output t only uses inputs at t-p+qd; the maximum lag adds (K-1)d per layer.','With the selected one-step target shift, target raw observations enter at lags1-8 in the k2,dilation2,L3 witness; non-target inputs can include lag0.','All four selected TACD profiles explicitly set split_ratio to1.0; training and validation use the same event-pair list in that branch.','True graph labels are passed into checkpoint/threshold selection and final threshold scoring on selected real-data paths.','Zero-valid denominator and strict-threshold outcomes are exact proposed contract results,not upstream runtime measurements.']))
    write(BASE/'copyedit-review.json',dict(status='pass',evidence=[ref(BASE/'development.tex','Connected source-grounded argument'),ref(BASE/'sponsor-addition.md','Paired sponsor text')],
        findings=['Distinguishes source facts from project derivations and proposed public tests.','Names the exact four configuration profiles; no generic absent-key inference replaces them.','Maintains event/network,series and intervention targets separately.']))
    write(BASE/'plan-review.json',dict(status='pass',scope='Add three audited source/project citations and exact delegate protocol to preserving reader; retain all existing content.',
        evidence=[ref(FOLLOW/n,'Current completed packet') for n in ['tcdf-delegate.json','tacd-protocol.json']]+[ref(FOLLOW6/n,'Current completed packet') for n in ['public-fixture.json','python-discovery-delta.json']],
        checks=['Three additions have exact local bytes,URL,version/hash,inspected anchors and supported claims.','Prior 1430 reader and1089 sponsor records remain bound.','The prior split wording is explicitly narrowed to the inspected actual four profiles.','Run unchanged full controllers after paired exact-byte successor; native/full coverage and visual acceptance stay open.']))
    write(BASE/'review.json',dict(status='pass',issues=[],evidence=[ref(BASE/n,'Reviewed source publication package') for n in ['source-audit.json','protocol-exact-results.json','mathematical-review.json','copyedit-review.json','plan-review.json','development.tex','sponsor-addition.md']],native_execution=False,visual_acceptance=False,final_acceptance=False))
    print(json.dumps(dict(source_records=3,delegate_files=len(records),reader_records=1433,sponsor_records=1092)))


DEVELOPMENT=r"""\section[Delegate-level temporal and evaluation protocol]{Delegate-level temporal and evaluation protocol}
\label{sec:exec28-at2}
The primary method description and the code path are different evidence. This supplement traces
the selected temporal and event-discovery delegates far enough to state what their current
proposal can compare, and what a public qualification would have to measure. Four inspected TACD
configuration profiles explicitly request a training/validation pair split ratio of one. They
therefore enter the shared-pair branch described below; this conclusion is tied to those exact
profiles and commit.

\subsection{Temporal support is not a learned causal delay}
For a one-dimensional convolution with stride one and left padding $p=(K-1)d$, the source uses
cross-correlation, so output index $t$ can depend on input indices
$t-p+qd$, $q=0,\ldots,K-1$. The final point is $t$ and the first is $t-(K-1)d$.
The selected \texttt{Chomp1d} removes the rightmost $p$ padded outputs, preserving sequence
length and excluding future indices under this index convention. With layer dilations
$d_c^\ell$, the largest support lag across $L$ layers is
\[
  (K-1)\sum_{\ell=0}^{L-1}d_c^\ell.
\]
For $K=2$, $d_c=2$ and $L=3$, non-target channel support may include lags zero through seven.
The TCDF data path separately shifts only the target channel by one row, zero-fills the initial
shift, and predicts the unshifted target. Thus the target's raw-history support in this finite
index calculation is lags one through eight, while non-target variables may still contribute
at the contemporaneous index zero. A method called temporal or causal does not thereby exclude
same-row predictors; the variable clock and allowable information time must be explicit.
\citep{exec28_at_tcdf_temporal,exec28_at_protocol_reference}

The final temporal block also applies a learned linear map across channels at each time point.
The source extracts maxima from depthwise kernel weights and turns them into candidate delays.
That statistic does not describe every path through channel mixing and residual connections.
The support calculation bounds which indexed inputs could matter; it does not say which
parameters the trained model uses, establish a stable delay estimate, or identify an intervention.
The application should preserve an explicit representation for candidate lag support, learned
predictive attribution, and causal-effect timing rather than serializing each as one integer lag.
\citep{exec28_at_tcdf_temporal}

There are concrete boundary conditions for a native fixture. If $K=1$, then $p=0$ and the
selected source still applies the slice \texttt{:-0}; ordinary Python indexing yields an empty
sequence. A zero-layer profile also has no convolutional support to report. The proposal does not
silently assign behavior to these parameter values. A version-pinned adapter must either reject
them with an informative contract error or establish valid supported semantics using a native
trial. The source-free reference records the empty-slice fact and proposed expectations without
importing the acquired model.\citep{exec28_at_protocol_reference}

\subsection{Four TACD profiles use the same event-pair sets}
The selected configuration file contains four named profiles: simulated events and the 18V,
24V and 25V network datasets. Each explicitly assigns \texttt{split\_ratio=1.0}. The selected
entrypoint shuffles event pairs and, for ratios at least one, assigns the complete pair list to
both training and validation. For these four profiles the overlap is therefore source-confirmed;
it is not merely an inference from a missing configuration key. Shared event histories can make
the effective dependence even broader than pair identity. No value of a generic row-level
validation metric from this branch should be described as held-out graph discovery.
\citep{exec28_at_tacd_protocol}

On selected real-data paths, the data processor loads a supplied graph matrix; the wrapper
passes that matrix to the discovery method; the training method uses it for threshold selection
and F1 checkpoint selection; and the top-level driver again selects an output threshold and prints
metrics against the same graph. This is an oracle-assisted result. It can support an explicitly
labeled method-debugging comparison, but not a blind discovery-performance estimate on untouched
graph truth. The selected command-line interface offers a simulation label, while the inspected
data processor has no matching branch that assigns its returned locals for that choice. Its
selected source tree also omits an imported data-mapping module. These packaging and control-flow
facts require repair or a supported external component before any execution claim; no runtime
failure was measured in this source-only review.\citep{exec28_at_tacd_protocol}

The evaluation code compares graph scores using a strict greater-than threshold after choosing an
F1 maximizing value. A labelled tied-score fixture demonstrates why inclusive and strict
comparisons can create different graphs at the same numeric threshold. The source's manual
confusion-count loop includes diagonal cells, whereas the threshold helper removes them before
selection; any report that exposes both must define its denominator and graph universe. The
selected device path chooses \texttt{cuda:4} whenever CUDA is available and the method sets its own
seed. A reproducible run must record visible devices, the effective configuration and all sources
of randomness, not just the top-level CLI seed. These are scoped static observations; the reference
fixture does not assert that any installed external metric implementation disagrees.
\citep{exec28_at_tacd_protocol,exec28_at_protocol_reference}

\subsection{A public protocol that preserves information boundaries}
A low-cost public experiment should have graph instances, rather than just rows, as part of its
identity. Before running a candidate, freeze an independently generated training graph set,
a validation set used for thresholds and model selection, and a held-out evaluation set. If the
target is an event process, also freeze the calendar horizon, history-window rule, event-pair
construction and any purge gap between training and later evaluation. Where multiple rows share
an initiating event, device or graph, do not treat them as independent assignments without a
declared sampling argument. Record graph truth access as hidden until final scoring, available for
training/debugging only, or deliberately oracle-assisted.

The selector must receive only its declared validation labels. After its threshold and checkpoint
are frozen, the evaluator binds held-out graph identity and truth, then computes a predeclared
off-diagonal metric. All requested graphs remain in the denominator. Invalid or missing scores
retain separate requested and valid counts; zero valid batches produce an unavailable outcome,
not a numerical loss of zero. Tied scores require an explicit comparison convention and deterministic
tie resolution. Missing topology, an unavailable simulation delegate, CUDA index selection and
source package identity are logged as input conditions, not repaired by undocumented defaults.
\citep{exec28_at_protocol_reference,exec28_at_contract_fixture}

The source-free fixture implemented here verifies only these proposal-owned contracts on a tiny
stipulated example. It selects a threshold on a validation instance, checks that a distinct
evaluation instance is scored afterward, rejects overlapping identities, returns unavailable
for an empty valid denominator and checks exact lag/tie expectations. It does not call TACD,
TCDF, PyTorch, gCastle or scikit-learn. It provides a reviewable test shape before a native
environment and rights packet are ready, not evidence that either external algorithm meets the
contract.

This supplemental trace sharpens reuse decisions without broadening their scope. TCDF may remain
a conditional temporal candidate after native window, padding and delay-conversion fixtures.
TACD remains a specialist event/topology candidate whose supplied-graph results must be segregated
from truth-free evaluation and whose four selected profiles share their training/validation pairs.
Both must pass exact source closure, rights intake and a registered public known-truth comparison
before those candidates can enter a product adapter.
"""

SPONSOR=r"""# Keep graph truth outside TACD evaluation

The selected TACD repository has four named configurations, and every one sets split_ratio=1.0. Its entrypoint shuffles event pairs and uses the same pair list for both training and validation in this branch. On selected real-data paths, the supplied graph is also passed into model/checkpoint threshold selection and used again by the top-level driver. These results are oracle-assisted and not held-out graph discovery; split each graph family into training, validation, and untouched evaluation instances before making a performance claim. [@exec28_at_tacd_protocol]

The selected TCDF padding/chop path has a bounded indexed receptive field, not a direct causal-delay certificate. With the exact kernel-2, dilation-2, three-layer witness, non-target inputs can include lags zero through seven; a separate one-step target shift moves target raw-history support to lags one through eight. A final channel-mixing layer also means a maximum kernel weight is not every learned path. [@exec28_at_tcdf_temporal; @exec28_at_protocol_reference]

A proposal-owned public fixture now checks validation-only threshold choice, disjoint graph identities, held-out truth binding, exact threshold ties and unavailable zero-valid denominators. It passes as an authored contract test without importing the acquired packages. It establishes test behavior only; native software, calibration, rights and bank performance remain open. [@exec28_at_contract_fixture]
"""


if __name__=='__main__':main()

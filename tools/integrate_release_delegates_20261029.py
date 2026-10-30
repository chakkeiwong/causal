"""Single-use, exact-ledger integration of inspected delegate contracts."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/release/2026-10-29'
EVIDENCE = BASE / 'source-delegates-015'
SOURCE = BASE / 'source/docs/writing-repair/2026-10-29'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ledger = json.loads((BASE / 'edits.json').read_text())
    assert len(ledger) == 73, 'This integration is single-use'
    changes = []

    def edit(path, before, after, reason, destination):
        text = path.read_text()
        assert text.count(before) == 1, str(path)
        changes.append((path, text, text.replace(before, after, 1)))
        ledger.append(dict(file=str(path.relative_to(ROOT)), before=before, after=after,
                           reason=reason, substantive_destination=destination))

    path = SOURCE / 'src/e6fc8271214ca907.tex'
    before = r'''Nested nuisance-fitting folds and outer policy-evaluation folds are different
controls. An adapter must preserve both, record any supplied prefit models and
avoid translating a method name into a blanket calibration claim. Source comments
about the orientation of one weighted-learning solver require inspection of that
delegate before they are inherited as established behaviour. For the present
proposal, polle is a conditional original-R-worker candidate with named method,
history, support and evaluation contracts.~\citep{exec24_policiesr_polle}'''
    after = r'''Nested nuisance-fitting folds and outer policy-evaluation folds are different
controls. An adapter must preserve both, record any supplied prefit models and
avoid translating a method name into a blanket calibration claim. The
outcome-weighted delegate supplies a concrete reason to preserve the resolved
solver and dependency versions as well.~\citep{exec24_policiesr_polle}

The pinned polle wrapper selects \texttt{ipop} by default and passes that
choice to DTRlearn2. Inspection of DTRlearn2 2.1 and WeightSVM 1.7-16
traces the alternative \texttt{svm} route beyond the warning in polle's
comments. WeightSVM converts the signed binary responses to factor codes.
Its native classifier orders classes by first appearance and gives the
first class the positive decision-function sign. The special native rule
for literal signed labels does not apply after this factor conversion.
DTRlearn2 copies the returned support-vector coefficients into its own
decision function without translating the returned class order back to the
signed response. Positive output can consequently refer to the opposite
action from the one its downstream threshold assumes.
\citep{rel15policydelegates}

An exact project witness isolates the convention. Take two one-dimensional
points at -1 and +1 with matching signed labels, positive unit weights and
unit penalty. The stipulated hard-margin solution has dual weights 1/2.
When the negative observation appears first, the native convention gives
the negative class a positive score; importing its coefficients without
the class translation gives slope -1 and, under the inspected bias
reconstruction, intercept zero. The returned action labels are reversed.
Reversing the row order gives slope +1. This is an algebraic witness using
an exact solution, not execution of either solver. The small diagonal
regularizer and finite numerical tolerances require separate native tests.
The source comparison and polle's retained relabelling test motivate those
tests; an unrun test file is not a passing result.
\citep{rel15policydelegates,rel15delegatewitnesses}

The default safeguard also has a boundary. DTRlearn2's augmented branch
calls \texttt{owl\_aug} without forwarding the selected solver; that
delegate defaults to \texttt{svm}. Thus setting \texttt{ipop} at the outer
interface does not select it for this branch. The initial worker should
exclude the augmented hinge-loss route until the call is repaired and
qualified, and test row permutations, action relabelling and both
augmentation settings at the exact dependency versions. A different
qualified learner is a substantive alternative. For the present proposal,
polle remains a conditional original-R-worker candidate with named method,
history, support and evaluation contracts; source inspection establishes
neither calibrated policy value nor native acceptance.
\citep{exec24_policiesr_polle,rel15policydelegates}'''
    edit(path, before, after,
         'Resolve the explicitly uninspected policy solver delegate using pinned primary wrapper/native sources and an exact, non-executed algebraic witness.',
         'Original fold, prefit-model, history, support and calibration limits remain. The vague delegate obligation becomes an explained class-orientation path, augmented-call limitation, scoped witness and concrete qualification/refusal alternatives. No original mathematics or adverse result is removed.')

    path = SOURCE / 'src/291dfdd96a75e082.tex'
    before = r'''learnDBM is a related implementation. At the selected revisions, 15 of the
17 shared paths in the repositories' dynamic-network source directory have
identical Git blobs. Their observation classes and CLI entry points differ:
learnDBM accepts a cluster count and invokes \texttt{MultiNet.clust} with the
requested stationarity flag. The inner clustering path is not inspected here.
The learnDBN CLI finding cannot automatically be attributed to this different
caller. Nor do learned clusters necessarily represent externally assigned
intervention regimes; that interpretation needs another identification
argument.~\citep{exec15_javatemporal_learndbn,exec15_javatemporal_learndbm}'''
    after = r'''learnDBM is a related implementation. At the selected revisions, 15 of the
17 shared paths in the repositories' dynamic-network source directory have
identical Git blobs. Their observation classes and CLI entry points differ:
learnDBM accepts a cluster count, supplies the requested stationarity flag
to \texttt{MultiNet}, and invokes its clustering method. The learnDBN CLI
finding cannot automatically be attributed to this different caller.
Inspection of the inner class at the same learnDBM revision nevertheless
reveals a separate option mismatch: training and the inner reassignment
pass the declared flag, but the final stored reassignment calls
\texttt{computeClusters(networkPrev, true, false)}. Its stationary branch
uses transition network zero at every date.
\citep{exec15_javatemporal_learndbn,exec15_javatemporal_learndbm,rel15multinet}

This matters even when every required conditional probability is available.
In an authored two-transition example with equal component weights, let
the observed-path probabilities be 0.9 then 0.1 for one component and 0.6
then 0.6 for the other. Their likelihoods are 0.09 and 0.36, giving
normalized weights 1/5 and 4/5. Reusing the first transition gives 0.81
and 0.36, hence weights 9/13 and 4/13. The final routine samples a hard
assignment, so this discrepancy changes its sampling probabilities; it
does not imply a deterministic native outcome in every run.
\citep{rel15multinet,rel15delegatewitnesses}

Two other distinctions prevent a generic EM claim. The reassignment helper
gets mixture weights from the object's stored clustering while the loop
updates a local count array; these are not synchronized within that loop.
Its classification branch chooses the greatest trajectory likelihood
before mixture weights are applied. For weights 0.9 and 0.1 and
likelihoods 0.4 and 0.8, the likelihood-only choice favors the second
component, whereas the weighted products 0.36 and 0.08 favor the first.
The loop can switch from stochastic to classification assignment after
one hundred iterations; that switch is not a hard iteration limit.
An adapter must specify the intended mixture objective, propagate the
stationarity option and qualify the stopping and assignment behavior.
These are selected-source findings and exact illustrations, not an
executed Java failure or a proof that all clustering paths fail. Learned
clusters also need not represent externally assigned intervention regimes;
that interpretation still needs an identification argument.
\citep{rel15multinet,rel15delegatewitnesses,exec15_javatemporal_learndbm}'''
    edit(path, before, after,
         'Replace the unresolved learnDBM inner-path statement with inspected same-revision stationarity, assignment-weight and stopping contracts.',
         'All lineage counts, distinct-caller caution and intervention-regime limits survive. Added exact likelihood witnesses explain consequential mismatches; no Java execution or convergence claim is introduced.')
    # This second change must see the first change in this file.
    before = r'''version clarification. learnDBM needs an inspected clustering path before
becoming an enabled backend. Porting is a later option where rights, numerical'''
    after = r'''version clarification. learnDBM remains disabled pending repair and native
qualification of the inspected clustering contracts. Porting is a later option
where rights, numerical'''
    text = changes[-1][2]
    assert text.count(before) == 1
    changes[-1] = (path, changes[-1][1], text.replace(before, after, 1))
    ledger.append(dict(file=str(path.relative_to(ROOT)), before=before, after=after,
        reason='Align the integration recommendation with the completed inner-source inspection.',
        substantive_destination='The disabled-backend recommendation remains; its next condition becomes repair and native qualification, rather than a source inspection now completed. Rights, numerical equivalence and maintenance requirements remain.'))

    path = SOURCE / 'references-0.bib'
    before = path.read_text()[-500:]
    extra = r'''

@misc{rel15policydelegates,
 author={{polle, DTRlearn2 and WeightSVM contributors}},
 title={Pinned outcome-weighted policy delegates: class orientation and solver forwarding},
 year={2026},
 note={polle 1.6.5, DTRlearn2 2.1 and WeightSVM 1.7-16; primary R and native sources inspected at pre-cutoff revisions; exact identities and anchors in the release source audit}
}

@misc{rel15multinet,
 author={{learnDBM contributors}},
 title={MultiNet clustering: transition selection, mixture assignment and stopping contracts},
 year={2020},
 note={Revision e8ba2c4e9e64c0010615\allowbreak{}a54fa254dcacf377e05d, 26 March 2020; primary source inspection, not native execution}
}

@misc{rel15delegatewitnesses,
 author={{Causal banking proposal project}},
 title={Exact class-orientation and transition-mixture witnesses},
 year={2026},
 note={29 October 2026; rational arithmetic on stipulated cases; no vendor solver or Java execution}
}
'''
    edit(path, before, before + extra,
         'Add traceable software-original and authored-witness references for the new bounded comparisons.',
         'All inherited bibliography entries and their identities remain byte-preserved except previously ledgered changes; three distinct evidence records are added.')

    def bindings(names):
        return [dict(path=n, sha256=sha(ROOT / n)) for n in names]

    raw = 'docs/literature/raw/'
    policy_stems = ['rel15_polle_owl', 'rel15_polle_owl_tests'] + [f'rel15_dtrlearn2_src_{i}' for i in [0, 1, 2, 3]] + [f'rel15_weightsvm_src_{i}' for i in range(4)]
    policy_files = [raw + n + ext for n in policy_stems for ext in ['.txt', '.receipt.json']]
    policy_files += [raw + n + ext for n in ['rel15_dtrlearn2_cutoff', 'rel15_weightsvm_cutoff'] for ext in ['.json', '.receipt.json']]
    policy_sources = [json.loads((ROOT / (raw + n + '.receipt.json')).read_text())['url'] for n in policy_stems]
    audit = dict(cutoff='2026-10-07', scope='Primary implementation inspection and exact project witnesses; no new scholarly paper, native execution or bank validation.', sources=[
        dict(citation_key='rel15policydelegates', kind='implementation', source_identity=policy_sources,
             version_date='polle 1.6.5 revision 16469f06e30bb26869ec02f06ab2d37365306ae2 (2026-09-30); DTRlearn2 2.1 revision 9467b8c378b4488d22417b35ed9134ef99d1b11c (2026-09-10); WeightSVM 1.7-16 revision f5887a8d5f255bdfd1c25409cb7517601b873b29 (2024-10-12). Retrieved 2026-10-29.',
             local_bindings=bindings(policy_files), inspected_anchors=[
                 'polle owl.R: complete 324 lines; defaults 42-54, restrictions 71-100, design/action coding 171-208, delegate call 224-237, prediction/remapping 259-324.',
                 'polle test-policy_learn-owl.R: complete 230 lines; direct one/two-stage parity and action-relabelling assertions; tests not executed.',
                 'DTRlearn2 DESCRIPTION: identity/dependencies/version. owl.R: complete 240-line file, solver defaults 8/114, augmented call 162-165, ordinary solver forwarding 174-193, backward selection 207.',
                 'DTRlearn2 owl_aug.R: complete file; default svm line 8 and forwarding to owl_single. wsvm_solve.R: complete file; signed response 19, returned coefficients 40-46, bias 56-69, action threshold 74/77.',
                 'WeightSVM DESCRIPTION: version. R/wsvm.R lines 247-265 factor conversion and 305-398 native returns. Rsvm.c lines 290-318 coefficient/label transfer.',
                 'WeightSVM src/svm.cpp lines 2074-2145 class ordering; 2290-2335 signed subproblem and retained labels; 2640-2683 prediction sign/label convention.'
             ], supported_claims=[
                 'Class factor conversion and first-occurrence native orientation must be translated when signed coefficients are reused. DTRlearn2 selected source omits that translation.',
                 'polle defaults to ipop and forwards the choice; the augmented DTRlearn2 call omits it and the delegate defaults to svm.',
                 'The selected tests encode parity and relabelling checks but no execution result is claimed.'
             ], limitations=['Exact pinned source paths only; complete package/runtime qualification and finite-sample value inference remain open. Numerical solver realization is not asserted by the rational witness.']),
        dict(citation_key='rel15multinet', kind='implementation',
             source_identity='https://raw.githubusercontent.com/SSamDav/learnDBM/e8ba2c4e9e64c0010615a54fa254dcacf377e05d/src/dbn/MultiNet.java',
             version_date='e8ba2c4e9e64c0010615a54fa254dcacf377e05d; 2020-03-26. Retrieved 2026-10-29.',
             local_bindings=bindings([raw+'rel15_learndbm_multinet.txt',raw+'rel15_learndbm_multinet.receipt.json',raw+'exec15_javatemporal_commit_learndbm.json']),
             inspected_anchors=['Complete MultiNet.java, 471 lines: constructor 41-78; transition selection and classification/stochastic reassignment 81-177; stored-weight accessor 179-203; network training 221-249; clust loop and final literal flags 251-281; score and export 283-408.'],
             supported_claims=['Final stored assignment hard-codes stationary=true and stochastic assignment, while inner training/reassignment use the field flag.', 'Mixture weights in computeClusters come from stored field clustering; loop counts change locally. Classification maximizes unweighted trajectory likelihood. The hundred-iteration switch is not a hard iteration cap.'],
             limitations=['Selected source inspection only; no Java execution, convergence guarantee, general library absence or intervention-regime interpretation.']),
        dict(citation_key='rel15delegatewitnesses', kind='project_derivation', source_identity='Project-authored exact arithmetic: tools/release_delegate_witnesses_20261029.py',
             version_date='2026-10-29; frozen source-delegates-015 witness',
             local_bindings=bindings(['tools/release_delegate_witnesses_20261029.py','docs/release/2026-10-29/source-delegates-015/exact-witnesses.json']),
             inspected_anchors=['orientation(): exact two-point dual/margin equations and copied coefficient/bias algebra for two row orders.', 'clustering(): two-transition normalized likelihood weights and unequal-prior classification choice.'],
             supported_claims=['The stipulated class-orientation witness reverses action labels under one row order.', 'The stipulated transition weights change from 1/5,4/5 to 9/13,4/13; unequal priors can reverse likelihood-only component selection.'],
             limitations=['Rational project examples, not executed upstream solvers, Java paths, empirical studies or bank outcomes.'])
    ])
    audit_path = EVIDENCE / 'source-audit.json'
    assert not audit_path.exists()
    for p, before_text, after_text in changes:
        assert p.read_text() == before_text
    # Preserve exact current bytes before any manuscript mutation.
    backup = EVIDENCE / 'before'
    backup.mkdir(exist_ok=False)
    for p, before_text, after_text in changes:
        (backup / p.name).write_text(before_text)
    (backup / 'edits.json').write_bytes((BASE / 'edits.json').read_bytes())
    audit_path.write_text(json.dumps(audit, indent=2) + '\n')
    for p, before_text, after_text in changes:
        p.write_text(after_text)
    (BASE / 'edits.json').write_text(json.dumps(ledger, indent=2) + '\n')
    print(json.dumps(dict(edits=len(ledger), touched=[str(p.relative_to(ROOT)) for p,_,_ in changes], source_audit=str(audit_path.relative_to(ROOT)), source_audit_sha256=sha(audit_path))))


if __name__ == '__main__':
    main()

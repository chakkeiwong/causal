"""Single-use, ledgered temporal-source comparison with additive mathematics."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import re
from release_candidate_20261029 import MATH

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/release/2026-10-29'
OUT = BASE / 'source-dbn-019'
SOURCE = BASE / 'source/docs/writing-repair/2026-10-29'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ledger = json.loads((BASE / 'edits.json').read_text())
    assert len(ledger) == 85, 'Single-use integration; do not replay.'
    assert not (OUT / 'source-audit.json').exists()
    changes = {}

    def edit(p, before, after, reason, destination):
        original, current = changes.get(p, (p.read_text(), p.read_text()))
        assert current.count(before) == 1, before[:100]
        changes[p] = original, current.replace(before, after, 1)
        ledger.append(dict(file=str(p.relative_to(ROOT)), before=before, after=after,
                           reason=reason, substantive_destination=destination))

    p = SOURCE / 'src/f26f479adef0a0f2.tex'
    edit(p, 'Five families illuminate different parts of this choice.',
         'Five initial families illuminate different parts of this choice.',
         'Distinguish the initial five-family comparison from the three later source closures.',
         'The five original roles, their complete argument and every numerical example remain; the added families follow in the same section.')
    before = r'\subsection{Reuse choices and the next affordable experiment}'
    extra = r'''\subsection{DBN++: filtering depends on model identity and the evidence clock}
\label{rel19:dbnpp}

DBN++ makes the supplied-model distinction especially clear. Its February
2016 revision describes filtering in discrete-time finite-state dynamic
Bayesian networks. The three advertised routes are variable elimination in
an unrolled network, the interface forward algorithm, and a forward algorithm
using algebraic decision diagrams. The model file supplies factors and the
mapping between slices; the evidence file supplies a sequence of observed
states. These paths do not estimate a causal structure or identify the effect
of a servicing action. They can nevertheless be useful reference calculations
when a bank has justified a particular latent-state model. The experimental
file format must then carry the ordered state dictionary and the physical
meaning of a transition. \citep{rel19dbnpp}

The first evidence time matters. Both interface implementations construct the
initial forward distribution, project it through the transition factors, and
then update it with the first observation. Let $D_t$ denote a binary borrower
distress state, let $K(d'\mid d)$ be its supplied transition law, and let
$\ell_{t+1}(d')$ be the likelihood of the next observed flag. If $p_t$ is the
current state distribution, the intended update is
\begin{equation}
 p_{t+1}(d')=
 \frac{\ell_{t+1}(d')\sum_d K(d'\mid d)p_t(d)}
 {\sum_z\ell_{t+1}(z)\sum_d K(z\mid d)p_t(d)}.
 \label{rel19:filter}
\end{equation}
Thus a wrapper must say whether its initial distribution precedes the first
evidence interval. Feeding evidence already used to construct that distribution
would be a different experiment. The denominator must be positive: an
impossible observation has no conditional distribution under the supplied
model. The inspected dense and diagram normalization methods divide without
an explicit positive-mass guard. The parser and caller also do not establish
a nonempty evidence horizon before the unrolled route accesses its first
record. Validate these conditions and return their scientific or input failure
meaning instead of a seemingly valid probability. \citep{rel19dbnpp}

Model identity is a separate concern for a persistent service. In each
\texttt{project} overload, function-static vectors retain the variable pointers
and transition factors from the first initialization. Later calls append and
remove the current forward factor but do not rebuild those retained vectors
for a different model. The shipped CLI loads one model, a narrower use than
a service evaluating several portfolios or actions in one process. Replacing
its factor objects while reusing the function can therefore retain the earlier
kernel; changing variable objects also raises lifetime and identity questions.
This is a static source finding, not an executed failure of every CLI request.
A prospective adapter needs model-scoped state and a concurrency contract.
\citep{rel19dbnpp}

An exact constructed example shows the monetary significance of substituting
the kernel. Take $P(D_t=1)=1/4$, with flag likelihoods $1/5$ in state zero and
$4/5$ in state one. Kernel A gives distress probabilities $1/10$ and $4/5$
from current states zero and one; kernel B gives $2/5$ and $9/10$. The next
distress probabilities before the flag are $11/40$ and $21/40$. Equation
\eqref{rel19:filter} then gives posterior probabilities $44/73$ and $84/103$.
Suppose, as an additional stipulated causal payoff law, a subsequent action
prevents USD~14 of loss only in the distressed state and costs USD~10 for
every customer. Its expected net value is USD~$14p-10$: approximately
USD~$-1.56$ under A and USD~1.42 under B. Reusing A when B was requested reverses
the action recommendation. The arithmetic assumes the same variable identities
and well-defined kernels; it does not predict the result of dangling pointers,
nor does a filtered probability establish the stipulated causal payoff law.
\citep{rel19dbnwitness}

The finite-state label also needs an algorithm-specific qualification. The
diagram constructor uses one Boolean variable for each domain variable and
selects its positive literal whenever a state index is nonzero. A three-state
dictionary such as current, delinquent and default is therefore not represented
injectively by that construction: indices one and two select the same literal.
For masses $(1/5,3/10,1/2)$, this Boolean mapping preserves only the combined
positive-state mass $4/5$. This demonstrates loss of state identity, not the
exact output of CUDD when supplied an invalid nonbinary evaluation input. A
future diagram route must reject this domain or implement and verify a proper
multivalued encoding; agreement on binary examples cannot qualify ternary
borrower states. \citep{rel19dbnpp,rel19dbnwitness}

The reuse decision is consequently limited to a supplied-model filtering
reference pending those contracts and numerical tests. The build points to
CUDD 3.0.0 through a host-specific directory. README and inspected source
headers declare LGPL version 3 or later, whereas the root LICENSE contains
GPL version 3 text. That discrepancy requires clarification before a
distribution decision; this comparison does not resolve it legally. Neither
a faster forward pass nor a license label supplies causal identification.
\citep{rel19dbnpp}

\subsection{EISALab/DBN: anomaly processing changes the observation experiment}
\label{rel19:eisadbn}

The July 2013 EISALab/DBN revision contains a flat-file anomaly-detection
application. Its Bayesian driver selects ordinary, robust, mixture and online
Kalman variants, Rao--Blackwellized particle filters and scale-recursive
methods from supplied model specifications. The inspected path is therefore
relevant to observation construction and state estimation. It does not
establish a causal structure learner merely because the repository is named
DBN. The wrapper calls an external batch-EM routine for ordinary Kalman
learning; the robust Kalman class's two \texttt{Learn} overloads explicitly
perform no learning. The common command-line learning option cannot be treated
as evidence that every selected filter fits new parameters. The external
numerical implementations remain outside this inspection. \citep{rel19eisadbn}

Its clock and output policies are consequential. The driver advances an
expected timestamp by a configured number of seconds and creates all-missing
records while awaiting the next observation. An optional sufficiently long
gap resets the filter and starts another training sequence; the shown reset
branch supports only the ordinary Kalman and first particle-filter choices.
The chronology check rejects any record earlier than the expected timestamp
before applying the nominal symmetric timing tolerance. A banking adapter must
therefore define positive time resolution, arrival ordering, gaps and restart
meaning explicitly. A missing interval, a delayed report and a new customer
history must not acquire the same interpretation by accident. \citep{rel19eisadbn}

The ordinary filter wrapper returns an observation, lower and upper predictive
limits, a predictive mean and an anomaly indicator. In the optional cleaned
file, a nonmissing observation flagged as anomalous is written as NA. That
policy may help isolate sensor failures, but a large genuine response to a
bank action is not a sensor failure. Consider an exact randomized example:
customer type $U$ and action $A$ are independent Bernoulli variables with
probability one half, and monetary outcomes obey
\begin{equation}
 Y(0)=100,\qquad Y(1)=100+100U,\qquad
 R=\mathbf 1\{Y\leq150\}.
 \label{rel19:cleaning}
\end{equation}
Here $R$ records retention after a stipulated anomaly rule, and all outcomes
are accurate measurements. The population treatment effect is USD~50.
Among retained treated customers only type zero remains; both retained group
means are USD~100, so their contrast is zero. At a stipulated action cost of
USD~20, the population net benefit is USD~30 while the retained-row comparison
suggests USD~$-20$. Randomization before cleaning does not justify the latter
comparison after outcome-dependent selection. This is a constructed law,
not an assertion that the external filter necessarily implements this threshold
or produced these results. \citep{rel19dbnwitness}

The defensible alternative retains the original outcome, flag, missingness
reason and transformation history as separate fields. A causal analysis must
justify any exclusion, model the measurement or selection mechanism when
appropriate, and examine sensitivity when that mechanism cannot be learned.
Prediction intervals concern the stipulated observation model; they are not
automatically intervals for an action effect. The inspected Makefile refers
to external libraries and absolute directories on the original developer's
machine, while the complete tree supplies no file named as a license or
copyright notice. These limits favor a scientific and interface reference
until dependency, rights and numerical behavior are resolved. They do not
negate the potential usefulness of anomaly detection for its own task.
\citep{rel19eisadbn}

\subsection{pdbntk: a parallel skeleton is not a fitted dynamic model}
\label{rel19:pdbntk}

The July 2013 pdbntk revision describes a parallel dynamic-network toolkit,
but the actual demonstration path is unfinished. Its executable declares
hidden-state models and allocates 40,000 sequences of length 100, then passes
a \texttt{DummyInfEngine} to the parallel driver. That engine performs an
arithmetic workload and returns one for each sequence, with an empty vector
of sufficient-statistic objects. The iteration loop repeatedly calls its
expectation routine; the maximization routine is empty and is never called,
and the convergence flag is never updated. If those loops complete as written,
the last accumulated value is 40,000, irrespective of the observations. Its
printed label \texttt{loglik} does not make it a fitted likelihood. No timing,
successful build or native execution is inferred here. \citep{rel19pdbntk,rel19dbnwitness}

The alternative junction-tree interface does not close the gap: its sequence
evidence entry returns zero and its sufficient-statistic method returns an
empty vector. A separate tabular parser checks header identities and numeric
characters but appends an empty observation map without inserting the parsed
values. These are concrete reasons to reject the inspected path as an admitted
learning backend. They do not show that the borrowed Mocapy++ and libDAI
libraries lack their own inference capabilities. The driver also shares one
inference-engine pointer across its OpenMP region; replacing the dummy with
a mutable engine would require an explicit state-ownership design before
parallel correctness could be claimed. \citep{rel19pdbntk}

For banking, an acceptable future EM implementation would need an observation
contract, actual posterior sufficient statistics, a defined parameter update,
an evaluated objective and convergence diagnostics. Those requirements concern
parameter estimation in a supplied model; successful EM would still not turn
an observational hidden-state model into an identified intervention model.
The selected build depends on Boost, OpenMP, GMP, LAPACK and borrowed native
libraries. Inspected libDAI and Mocapy headers carry distinct notices, while
the tree has no project-root license. Resolve their respective scope before
reuse. The appropriate current role is an unfinished design reference, with
no claimed bank benefit from parallelism. \citep{rel19pdbntk}

'''
    edit(p, before, extra + before,
         'Close three named temporal software omissions using authenticated primary source and exact authored banking consequences.',
         'Additive three-family comparison; all existing equations, negative results, alternatives and implementation contracts remain in the manuscript.')
    before = 'BayesNetty & Reference constrained search & Preserve constraint predicates and\nfailure meaning; establish a suitable target before temporal/effect claims.\\\\\n'
    after = before + r'''DBN++ & Reference supplied-model filtering & Bind model, state dictionary and first evidence time; validate mass, horizon, encoding and reuse terms.\\
EISALab/DBN & Reference anomaly and observation processing & Preserve originals and selection meaning; resolve external numerical dependencies and rights.\\
pdbntk & Unfinished design reference & Do not admit the dummy learning path; establish inference, parameter updates, state ownership and rights first.\\
'''
    edit(p, before, after, 'Extend the reuse table with the three inspected source decisions.',
         'The five prior role decisions remain; three bounded reference decisions are added.')
    before = '''The search remains bounded. The inherited scholarly query includes duplicate
and publication aliases, and the native repository queries leave relevant
families such as DBN++, EISALab/DBN and pdbntk uninspected. Name and language
metadata cannot decide their causal capability.'''
    after = '''The search remains bounded. The inherited scholarly query includes duplicate
and publication aliases. The earlier native repository census left DBN++,
EISALab/DBN and pdbntk uninspected; the pinned primary comparisons above now
close that specific omission, without establishing an exhaustive census or
qualifying a native backend. Name and language metadata cannot decide causal
capability.'''
    edit(p, before, after, 'Correct stale omission status without erasing the historical census limit.',
         'Historical noninspection is explicitly retained; current bounded source closure replaces only the obsolete present-tense assertion. Broader scientific and rights gaps remain in the following original sentences.')
    p = SOURCE / 'references-0.bib'
    before = p.read_text()[-500:]
    after = before + r'''

@misc{rel19dbnpp,
 author={Bueno, Thiago Pereira},
 title={DBN++: supplied dynamic-network filtering source},
 year={2016},
 note={thiagopbueno/dbn-pp, revision e5c4f7a265fd2616f165940ba7f752dee25a79f7, 5 February 2016. Authenticated README, build, license, parser, factors and inference source inspected; no native execution},
 url={https://github.com/thiagopbueno/dbn-pp}
}
@misc{rel19eisadbn,
 author={{EISALab}},
 title={DBN repository: anomaly-detection driver and filter wrappers},
 year={2013},
 note={Revision 035dcf4b0007ba1e1a72a4850799a603fc355de9, 15 July 2013. Authenticated Bayesian driver, learning wrappers, clock and build inspected; external numerical libraries not qualified},
 url={https://github.com/EISALab/DBN}
}
@misc{rel19pdbntk,
 author={{ushadow}},
 title={pdbntk: parallel dynamic-network prototype source},
 year={2013},
 note={Revision 640b9cb1e86220f3e3d422e473a637fa3d861ac3, 9 July 2013. Authenticated executable, parallel driver, dummy and junction-tree interfaces, evidence parser and build inspected; no native execution},
 url={https://github.com/ushadow/pdbntk}
}
@misc{rel19dbnwitness,
 author={{Causal banking proposal project}},
 title={Exact temporal model-identity and outcome-cleaning witnesses},
 year={2026},
 note={29 October 2026. Exact rational transition, posterior and monetary calculations; randomized potential-outcome selection example; no upstream execution or bank observations}
}
'''
    edit(p, before, after, 'Add primary software and distinct authored-law bibliography identities.',
         'All prior bibliography entries survive; no scholarly paper is invented or inferred from repository metadata.')

    authenticated = json.loads((OUT / 'authenticated-files.json').read_text())
    sources = []
    specs = [
        ('dbnpp', 'rel19dbnpp', '2016-02-05',
         ['README lines1-17,46-113,189-205: supplied finite-state filtering, experimental input and LGPL notice.',
          'inference.cpp lines100-184,257-350: retained static factors/pointers, projection before evidence, normalized update.',
          'inference.cpp lines354-445; main.cpp lines76-163; io.cpp lines193-229: no nonempty-horizon validation before first unrolled evidence access.',
          'factor.cpp lines159-168 and addfactor.cpp lines193-202: normalization without explicit positive-partition check.',
          'addfactor.cpp lines48-69,205-247: one Boolean literal per variable, nonzero-state conflation; invalid nonbinary evaluation behavior not established.',
          'Makefile and root LICENSE title/terms: host-specific CUDD3.0.0 route; GPLv3 text distinct from LGPLv3-or-later source declarations.'],
         ['Supplied-model discrete filtering, not established causal structure discovery.',
          'Multi-model service must address retained factor identity and lifetime, first-evidence clock, zero probability, empty horizon and Boolean-domain contract.',
          'Per-file rights discrepancy is observed and unresolved; no legal or native qualification.']),
        ('eisadbn', 'rel19eisadbn', '2013-07-15',
         ['adet/README and adet.cpp task dispatch: flat-file anomaly application with Bayesian route.',
          'bayesian_adet.cc lines433-655: model choice, learning, cleaning, gap and resolution options.',
          'bayesian_adet.cc lines668-785: expected timestamp, missing slots, restricted reset, earlier-than-expected rejection preceding tolerance.',
          'bayesian_adet.cc lines795-897: cleaned NA output and Learn dispatch.',
          'bayesian_adet.cc lines955-1041,1178-1192: predictive wrapper, external TrainBatchEM and no-op robust Learn.',
          'adet_filters.cc lines1-134: external numerical includes and online wrapper; not a full inspection of precipitation variants.',
          'Makefile lines1-34, full immutable tree: external host paths and no license/copyright-named paths.'],
         ['Inspected path supports anomaly processing and supplied-filter interfaces; not evidence of causal discovery.',
          'Observed output cleaning introduces missingness; clock, restart, model-specific learning and selection meanings need preservation.',
          'External numerical implementation, dependency closure and reuse rights remain unresolved.']),
        ('pdbntk', 'rel19pdbntk', '2013-07-09',
         ['app/parallel_em_hmm.cpp lines20-84: declared models,40000 sequences of length100, DummyInfEngine and ten iterations.',
          'parallel_em_engine.cpp complete: E-step-only iteration, unchanged convergence, empty M-step and shared engine in OpenMP.',
          'dummy_inf_engine.cpp complete: constant one after arithmetic workload, empty ESS.',
          'jtree_2tbn_inf_engine.cpp complete and interface headers: constant-zero evidence entry and empty ESS; partial forward routines.',
          'evidence.cpp lines25-67 and evidence.h: parser validates fields but never populates observation map.',
          'Root/src/app CMake files; evidence.h lines1-6 and bundled framework/dbn.h notice: build dependencies and distinct borrowed notices.',
          'Complete immutable tree: notices only under third-party glog/gtest paths, no project-root license.'],
         ['Shown demonstration is an unfinished parallel scaffold, not a fitted likelihood or admitted EM backend.',
          'Constant-return arithmetic is a source-path consequence conditional on loop completion, not measured runtime or upstream execution.',
          'Replacing dummy inference requires real evidence, sufficient statistics, parameter updates and thread-state ownership; causal identification remains separate.']),
    ]
    for family, key, date, anchors, claims in specs:
        rows = [r for r in authenticated if r['family'] == family]
        bindings = []
        for row in rows:
            path = ROOT / row['local_copy']
            assert sha(path) == row['sha256'] and row['blob_match']
            data = path.read_bytes()
            assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == row['git_blob']
            bindings.append(dict(path=row['local_copy'], sha256=sha(path), repository_path=row['path'], git_blob=row['git_blob']))
            receipt = ROOT / 'docs/literature/raw' / (row['id'] + '.receipt.json')
            bindings.append(dict(path=str(receipt.relative_to(ROOT)), sha256=sha(receipt)))
        for suffix in ['repo.json', 'commit.json', 'tree.json']:
            path = ROOT / 'docs/literature/raw' / f'rel19_{family}_{suffix}'
            bindings.append(dict(path=str(path.relative_to(ROOT)), sha256=sha(path)))
        sources.append(dict(citation_key=key, kind='software_source',
                            source_identity='https://github.com/' + rows[0]['repository'],
                            version_date=f"Commit {rows[0]['revision']}; {date}; cutoff-selected before 2026-10-07, retrieved 2026-10-29.",
                            local_bindings=bindings, inspected_anchors=anchors,
                            supported_claims=claims,
                            limitations=['Bounded static source reading, not whole-repository correctness or native execution.',
                                         'Commit timestamp and pinned bytes do not establish independent scientific, rights or bank acceptance.']))
    witness = OUT / 'exact-witnesses.json'
    sources.append(dict(citation_key='rel19dbnwitness', kind='project_derivation',
                        source_identity='tools/release_dbn_witnesses_20261029.py', version_date='2026-10-29 exact authored laws',
                        local_bindings=[dict(path=str(q.relative_to(ROOT)), sha256=sha(q)) for q in [witness, ROOT / 'tools/release_dbn_witnesses_20261029.py']],
                        inspected_anchors=['compute(): exhaustive latent-transition contributions; four randomized type/action states and selection; Boolean mapping; conditional dummy-sum arithmetic.'],
                        supported_claims=['Kernel substitution changes posterior44/73 to84/103 and stipulated14p-10 net sign.',
                                          'Correct treatment-responsive outcomes selected at150 produce zero retained contrast despite population effect50; cost20 reverses monetary sign.',
                                          'Boolean mapping conflates positive states; no actual invalid CUDD return predicted.'],
                        limitations=['Constructed laws only, not bank data, empirical calibration, upstream bug execution or source performance replication.']))
    audit = dict(cutoff='2026-10-07', sources=sources,
                 scope='Three named omissions closed by versioned primary reading; no exhaustive census, additional scholarly-paper count or native qualification.')
    audit_path = OUT / 'source-audit.json'
    audit_text = json.dumps(audit, indent=2) + '\n'
    math_path = BASE / 'mathematical-addition-reviews.json'
    reviews = json.loads(math_path.read_text())
    e = ledger[86]
    occurrences = lambda s: Counter(re.sub(r'\s+', ' ', m[0]) for m in MATH.finditer(s))
    assert not occurrences(e['before']) - occurrences(e['after'])
    reviews['reviews'].append(dict(
        scope='Author review of additive filtering and outcome-dependent selection laws.',
        edits=[dict(edit=87, file=e['file'], before_sha256=hashlib.sha256(e['before'].encode()).hexdigest(),
                    after_sha256=hashlib.sha256(e['after'].encode()).hexdigest())],
        allowed_added=dict(occurrences(e['after']) - occurrences(e['before'])), allowed_removed={}, status='reviewed_additions_only',
        derivation='Sum prior times transition times likelihood over current state and normalize; separately average the two randomized potential-outcome types before and after deterministic outcome-dependent retention. Exact fractions enumerate all states.',
        reviewed_assumptions=['Specified binary state labels and positive evidence probability; first observation follows transition.',
                              'Kernel substitution example keeps variable identities; no universal pointer or concurrency behavior inferred.',
                              'USD14 distress-contingent avoided loss and USD10 cost are additional stipulated causal payoff assumptions.',
                              'Cleaning example has randomized independent action, accurate outcomes, fixed half-probability types, threshold150 and cost20.',
                              'Boolean-map loss is not an execution prediction for invalid CUDD input.'],
        witness=dict(path=str(witness.relative_to(ROOT)), sha256=sha(witness)),
        source_audit=dict(path=str(audit_path.relative_to(ROOT)), sha256=hashlib.sha256(audit_text.encode()).hexdigest()),
        fresh_visual_acceptance=False, independent_acceptance=False))
    backup = OUT / 'before'
    backup.mkdir(exist_ok=False)
    for q, (old, new) in changes.items():
        assert q.read_text() == old
        (backup / q.name).write_text(old)
    for name in ['edits.json', 'mathematical-addition-reviews.json']:
        (backup / name).write_bytes((BASE / name).read_bytes())
    audit_path.write_text(audit_text)
    for q, (old, new) in changes.items():
        q.write_text(new)
    (BASE / 'edits.json').write_text(json.dumps(ledger, indent=2) + '\n')
    math_path.write_text(json.dumps(reviews, indent=2) + '\n')
    print(json.dumps(dict(edits=len(ledger), source_audit_sha256=sha(audit_path), witness_sha256=sha(witness))))


if __name__ == '__main__':
    main()

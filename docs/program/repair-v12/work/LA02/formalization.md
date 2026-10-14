# Business meaning, graph alternatives and the information clock

A causal question is a collection of commitments. Write it as

\[
Q=(\mathcal U,P,\mathcal A,\pi,\pi_0,Y,H,\nu,\ell,\mathcal I).
\]

Here \(\mathcal U\) defines the observational unit; \(P\) is the target
population; \(\mathcal A\) is the set of feasible interventions; \(\pi\) and
\(\pi_0\) are the policy and comparator; \(Y\) and \(H\) define the outcome
and horizon; \(\nu\) specifies the target population measure; \(\ell\)
defines decision loss and its units; and \(\mathcal I\) supplies the available
information at each action. These symbols describe this project's contract,
not a new identification theorem. A business request can determine a set of
such questions rather than one question.

For an average treatment contrast, specifying \(\nu\) is essential. If
\(\tau(x)=E[Y(1)-Y(0)\mid X=x]\), a weighted target is

\[
\theta_w=\frac{E[w(X)\tau(X)]}{E[w(X)]},\qquad E[w(X)]>0.
\]

Uniform, treated-population, overlap and trimmed-population targets use
different weighting rules. Under the additional conditions that make a
treatment propensity meaningful for the intended population, the familiar
weights are respectively \(1\), \(e(X)\), \(e(X)(1-e(X))\), and
\(1\{a\le e(X)\le b\}\). This formula states which population is being
averaged; it does not establish identification, positivity, estimation rates
or valid uncertainty. The exact two-stratum example in `case-design.md`
distinguishes a trimmed mean of 5 from an overlap mean of \(250/41\).

The schema makes the measure a typed object, so changing the displayed target
name without changing the population rule is invalid. It also preserves the
intervention and comparator as explicit actions. A dynamic action contains a
bounded predicate and its two possible values, not a string of executable code.
The accompanying description remains prose; the validator never evaluates it.
Future LA05 execution must map this declaration to a supported fixed operation
or refuse it.

Two clocks govern an observed variable \(V\): the event time \(e_V\) and
the time \(a_V\) at which its value is available for a decision. The current
finite fixtures require \(e_V\le a_V\), and a history at time \(t\) may use
that value only when \(a_V\le t\). Derived variables must wait for every
input and their lineage must be acyclic. Latent variables have no observed
availability time. These checks deliberately implement a narrow recorded-value
contract. Advance announcements, nowcasts and revised historical values require
separate variables with their own meanings and timestamps; they cannot be
smuggled in by assigning a measurement an impossible availability time.

In servicing, \(A_0\) affects an intermediate state \(L_1\), which influences
both the next action \(A_1\) and repayment \(Y\). The same \(L_1\) can be
a mediator for the first action and a common cause of the second action and
outcome. A static total-effect adjustment that simply includes every available
column is therefore not justified. The validator flags descendants proposed as
ordinary total-effect controls. It does not declare all post-treatment
conditioning universally invalid: controlled direct effects, dynamic regimes
and longitudinal g-methods require their own explicit questions and formal
procedures. The policy-history purpose is kept separate for precisely this
reason. No flag substitutes for a graphical adjustment criterion.

The graph representation separates a collection of candidate models from a
single arbitrarily selected DAG. Within a candidate, edges record endpoint
marks, sources, counterevidence status and review disposition. A “possible”
edge is part of that proposed model; the qualifier expresses the evidential
status of the proposal. It is not a claim that the listed models enumerate all
combinations of independently optional edges. A CPDAG or PAG can be preserved
directly, including circle marks, rather than expanded incompletely and then
misrepresented as an exhaustive class.

For a proposed graph class \(\mathcal G\), the downstream object is generally
\(\bigcup_{G\in\mathcal G}\Theta_G(P,Q)\), where
\(\Theta_G(P,Q)\) contains every effect compatible with the distribution,
target and assumptions under graph \(G\). A nonidentified member can make
that union broad. An unverified LLM suggestion does not authorize deleting
the member. In the binary discovery construction the two opposite DAGs yield
the identical observational table and effects \(0\) and \(0.8\). A
single-model answer would discard an observationally compatible alternative.
The exact enumeration proves this property of the finite construction only.
It does not certify a learned class's coverage or completeness.

The reference validator checks endpoint types, directed cycles, declared time
order and explicit forbidden directions. It also reports directed-path
mediators, common ancestors and collider candidates. It does not recognize
every valid MAG/PAG/CPDAG, enforce every ancestral-graph property, perform ID,
or discover latent variables. Those jobs remain with a formal causal engine.
This boundary is essential when interpreting a `ready_for_formal_analysis`
result: the declaration is prepared for the next conditional analysis, not
scientifically qualified.

Selection and observations introduce another form of ambiguity. Conditioning
on successful linkage \(S=1\) can change the target population and open a
path when both action and outcome affect linkage. Calling a link score
“identity” does not turn the proxy into audited ownership. The observation
case retains a latent ownership node, an observed proxy and an explicit
selection node. Choosing the selected-population target triggers review of
its treatment-dependent membership. This is not an assertion that no such
target can ever be identified; the ordinary original-population ATE cannot
silently serve as its replacement.

Evidence references record identities and hashes, but the declaration validator
does not open arbitrary paths or authenticate a claimed reviewer. It checks
that references exist within the declaration and that the scientific roles are
not conflated. File custody and authorization must be checked by the artifact
service and by the responsible institution. An `accepted_assumption` remains
an accepted premise, not a fact certified by software. An unresolved question,
infeasible action, contradicted bound assumption or unsupported promotion of
model proposals remains a review obligation. Synthetic review cannot be relabeled
as bank evidence.

The design takes its interaction and evidence lessons from the inspected
LA01 sources: CausalChat's proposal/editing workflow, CausalDS's distinction
between symbolic questions and noisy observation models, the OCI target-label
finding, and causal-learn+'s separation of suggestions from formal output.
Those sources are bound in LA01's frozen audit. The schemas, clock rules,
four banking examples and exact counterexamples here are project constructions.
They are not represented as inherited theorems or as demonstrations of an
external package's runtime behavior.

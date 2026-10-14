## Why an accurate clock need not identify the answer

It is useful to follow one restriction through an entire finite model comparison. Return to an offer \(A\) and a later repayment outcome \(Y\), both binary. Consider three explicitly listed models, using mutually independent primitive variables in each model. In model \(F\), \(A\) is fair Bernoulli and \(Y=A\mathbin{\oplus}E\), where \(E\) is Bernoulli with probability \(1/10\) and \(\oplus\) denotes exclusive OR. In model \(R\), \(Y\) is fair Bernoulli and \(A=Y\mathbin{\oplus}E\). In model \(C\), a pre-offer latent variable \(U\) is fair Bernoulli, \(A=U\mathbin{\oplus}E\) and \(Y=U\). Each error variable has the same probability \(1/10\). These are alternative constructions, not simultaneous equations for one population.

Every model produces the observed table

\[
 P(A=0,Y=0)=P(A=1,Y=1)=\frac9{20},\qquad
 P(A=0,Y=1)=P(A=1,Y=0)=\frac1{20}.
\]

All four observed cells are positive. In model \(C\), even conditioning on the latent variable leaves both offer assignments possible: \(P(A=1\mid U=0)=1/10\) and \(P(A=1\mid U=1)=9/10\). Thus the comparison does not rely on an empty observed treatment stratum or deterministic assignment given the confounder. Deterministic repayment given \(U\) is part of this constructed example, and is not a banking empirical claim.

Replacing the action equation gives mean outcomes \(1/10\) and \(9/10\) in model \(F\), hence effect \(4/5\). In \(R\), replacing the action equation leaves the fair outcome unchanged; in \(C\), it leaves the fair latent variable and \(Y=U\) unchanged. Both have effect zero. A separate exact enumeration verifies the common observed table, positive assignment probabilities and intervention contrasts. \citep{exec13_diagram_restrictions}

Now introduce a verified restriction: this particular offer was chosen before this particular repayment outcome was generated, with no backward-time causal mechanism in the admitted class. Model \(R\)'s direct arrow from this outcome to the earlier offer is incompatible with that restriction. Models \(F\) and \(C\) both respect it. The candidate graph list shrinks from three models to two, but the candidate effect set stays

\[
 \{0,4/5\}.
\]

Correctly resolving an orientation has not reduced the decision-relevant ambiguity in this example. An edge score that rewards removal of \(R\) can therefore improve while an effect-set or decision measure remains unchanged. Both statements are useful; they measure different progress. The set above belongs only to the three-model comparison. It is not asserted to exhaust every effect compatible with the observed law under an unrestricted hidden-variable model.

There are several possible next restrictions, with different evidential costs. If the offer equation is known to use independent random assignment, the stipulated mechanism of \(C\) is excluded too; among these candidates only \(F\) remains. If \(U\) becomes correctly observed, adjustment can identify the zero effect within \(C\)'s declared mechanism. If a noisy measurement of \(U\) becomes available, the earlier proxy example shows why adjustment needs further justification. These routes should not be compressed into one label such as "expert-validated diagram." They add distinct information and impose distinct assumptions.

An offer timestamp alone supplies none of the exogeneity information. A policy document describing randomization might support it, but the analyst must establish that the document applies to the relevant assignment, population and period. A random seed recorded after an officer overrode assignment does not establish the same mechanism. A public controlled experiment can test whether software applies the restriction correctly; it cannot verify an unobserved institution's compliance with its policy. That is the later, targeted evidence question.

The assistant should show a consequence table after each accepted premise: which models were removed, which target values were removed, and which claims now depend on that premise. A useful diagnostic temporarily withdraws the premise and recomputes those consequences. Here withdrawing the time order restores \(R\) without changing the two effect values, while withdrawing the additional exogeneity restriction restores a zero-effect alternative. This sensitivity report makes the pivotal premise explicit and can guide the next experiment without assigning invented probabilities to the models.

## Minimal conflicts locate a question; they do not settle it

The earlier offer–engagement–score example can also be made exact. Let three restrictions require the direct arrows \(A\to M\), \(M\to S\) and \(S\to A\) between the same three variable instances in a DAG. All three together create a directed cycle. Removing any one leaves an acyclic directed path. The triple is therefore an inclusion-minimal inconsistent set of these restrictions within the DAG class. A small exhaustive closure calculation verifies this combinatorial statement. \citep{exec13_diagram_restrictions}

Here “inclusion-minimal” means that deleting any member removes this conflict. In a larger restriction system it need not mean the smallest possible cardinality; different minimal conflicting subsets can coexist. Nor does minimality select a scientifically preferred repair. Deleting the arrow with the lowest language-model confidence can yield a syntactically valid graph while deleting the only premise supported by a reliable process record.

One legitimate repair might refine the score into \(S_t\) and \(S_{t+1}\). The earlier score affects \(A_t\), which changes engagement and a later score; that time-unrolled construction can respect all the underlying mechanism descriptions. Another repair might find that the phrase “engagement changes score” described a deterministic calculation rather than the primitive intervention contemplated by the analyst. A third might withdraw an unsupported causal assertion. These are alternatives to investigate, not guaranteed equivalent versions of one graph.

The scientific review should therefore report the conflicting predicates together with their variable identities, clocks and evidence. It should distinguish a change to the model class, a refinement of a variable, and a rejection of a premise. Keeping that distinction makes both favorable and adverse prototype results interpretable: a detector can correctly find the contradiction even if it cannot resolve its scientific cause. Its useful contribution is a precise next question whose answer would change the admissible analysis.
\label{exec13:restriction-development-end}

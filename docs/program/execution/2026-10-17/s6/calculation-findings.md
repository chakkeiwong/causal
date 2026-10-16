# S6 calculation findings before evidence freeze

The first exact-reference invocation failed its separate structural recursion
check before writing any outputs. The independent recursion initialized its
state as a Python integer, and division by two introduced a float. The primary
closed-form calculation used rational arithmetic throughout. Initializing the
recursion with a SymPy integer restores exact arithmetic; the assertion is
retained. This is an author calculation repair, not a statistical failure or an
upstream estimator result.

The recovered exploratory witness placed a treatment effect at the last
early-cohort period. Its lead weights are zero and it cannot demonstrate a
false lead. The executed construction places the effect at the first treated
period instead. Both exact leads are checked against a separately demeaned
regression. The chapter will state the complete design and population premise.

The robust extension passed its mathematical assertions and saved its results,
then failed while constructing its review receipt because the reference helper
requires a Path rather than a string. The corrected rerun verifies the saved
results exactly and creates the review without overwriting the calculation.

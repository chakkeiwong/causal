## Preserve the target when adopting panel software

The selected gsynth 1.4.0 is a compatibility wrapper around fect; the reviewed
engine candidate is fect 2.4.5. The complete wrapper declares a documented
weight argument but never forwards it. A stored request can therefore say
weights were requested without establishing that the engine used them. The
wrapper also remaps estimator and inference choices and supplies defaults
that differ from direct fect use. This is a pinned source finding; no native
execution or general package failure claim is made.
\cite{exec21_gsynth_wrapper,exec21_gsynth_engine}

Exact public examples show the stakes. Effects of USD -6 and USD 10 average
USD 2, but weights 9:1 give USD -4.4. At assumed cost USD 1, the corresponding
margins are USD 1 and USD -5.4. A separate example gives a treated-period
average of USD 6 and an equal-unit average of USD 2, with margins USD 2 and
USD -2 at cost USD 4. A deterministic factor example preserves the complete
observed panel while allowing effects USD 6 or USD 2 because a factor
direction is absent before treatment. Adding pre-period rows need not add
that information. These examples are outside full-rank identification and
are not native estimator failures or observed bank returns.
\cite{exec21_gsynth_reference}

The proposal keeps the wrapper as a reference and identifies a direct fect
worker as a future candidate. Admission requires explicit target and weight
roles, method and dependency pins, retained-sample and donor records, rank
and convergence diagnostics, and an uncertainty contract that counts failed
fits and bootstrap draws. Source inspection also finds restrictions on
treatment reversals, distinct fitting/aggregation weight columns and
clustered jackknife. Complete license-template and dependency review,
native parity and declared-law calibration remain prototype obligations.
Public panels and known-law examples can establish the value of that work
before expensive bank experiments.


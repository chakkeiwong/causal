## Use expert-guided ensembles to propose graphs with explicit limits

Tench and Demeester combine discovery algorithms by counting connections,
separating orientation, checking cycles and querying an expert on selected
disagreements. Their method is a candidate for the proposed diagram-review
workflow. Its main evidence uses synthetic categorical networks. A narrower
five-network model study reports mean orientation accuracy of 93.3% and
existence accuracy of 66.4%, while existence accuracy is 43.9% on Property.
Responses are cached across repeated seeds and sample sizes. These reported
results support further comparison, with domain dependence, shared errors and
memorization concerns retained. \citep{exec20_expert_averaging}

The proposed interface must distinguish a plausible causal path from a direct
edge and preserve unresolved graph types. Two printed algorithm details require
source inspection before reuse: rejected existence calls appear not to increment
the budget, and the exhausted orientation branch omits the majority fallback
described in the prose. These are specification discrepancies, not demonstrated
runtime defects. Physical calls, both argument orders, retries and cache reuse
must be accounted for before estimating operating cost.
\citep{exec20_expert_averaging_reference}

A graph vote is also not a calibrated probability of an intervention effect.
An exact example gives the same observational Gaussian distribution under two
models whose effects are 0.6 and zero. With assumed value USD 100 per outcome
unit and intervention cost USD 40, their margins are USD 20 and USD -40.
Giving the first model an unjustified 90% probability based on its vote yields
an apparent USD 14 margin. Valid temporal or experimental information could
resolve the direction; algorithm agreement alone cannot. Public prototype
evaluation should therefore compare intervention answers, useful refusal,
ambiguity and total review cost alongside graph accuracy. This retains the
method as a proposal candidate while source identity, rights and executable
conformance remain to be qualified. \citep{exec20_expert_averaging_reference}


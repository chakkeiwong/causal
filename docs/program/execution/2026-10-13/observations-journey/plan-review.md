# Trustworthy-observations workflow: reviewed design

This proposal task connects source records to a defined causal request. It does
not require bank records, live models, sibling execution or every language
adapter. The immediate executable scope is the existing local library and CLI,
with generated fixtures, independent references and explicit unsupported cases.
No final service invocation precedes registration.

The business question is whether an eligible borrower should receive a contact
before a twelve-month adverse event. The eventual effect is the difference in
that event under contact versus no contact in a declared eligible population.
The measurement task is earlier: establish whose records, which event definition,
which observation/selection process, and which available information the effect
procedure will use. A prevalence, a recovered identity or an audit pass is not
itself a causal effect.

Feature event time must be no later than first usable availability, and availability
must strictly precede the decision. Revisions retain their actual later availability.
Follow-up outcomes have a separate horizon, censoring and ascertainment rule;
they must not be rejected merely because they occur after the decision. The local
strict-clock checker covers feature rows only. Source timestamps are declarations,
not proof of custody or historical availability.

The proposed observation manifest retains origin/household identifiers, duplicate
and linkage alternatives, source and license identities, byte hashes, extraction
and revision versions, inclusion probabilities and their provenance, joint sampling
units, label definitions, adjudication evidence, rejected/missing records and target
population coverage. A shared map or calendar may induce shared uncertainty.
The manifest is a proposed contract; the current service does not enforce all of it.

The mathematical reference has three independent components. A two-origin
finite population with values 20 and 80 and inclusion probabilities one half
has expansion-estimator mean 50. Independent inclusions give variance 1700;
shared inclusion gives 2500, despite identical marginal probabilities. If an
origin is never included, its value is not determined by the observed law.
Two possible bijective record maps preserve the total 100 but reverse an
origin contrast from 60 to -60. Duplicating a record is not a new independent
origin and marginal match scores are not a joint distribution over bijections.

For a binary true event Z and reported label B, write prevalence p, sensitivity
s and false-positive probability f. Under this explicit homogeneous observation
law, q=P(B=1)=f+(s-f)p. The same q=17/50 arises from (s,f,p)=(9/10,1/10,3/10)
and (1/2,1/10,3/5). An unvalidated noisy label cannot distinguish these worlds.
For s different from f the first-order score is
(psi_q-p psi_s-(1-p)psi_f)/(s-f). Its variance needs the full joint covariance,
including shared-audit terms; the expansion needs its own regularity and sampling
argument. At s=f, division cannot identify p. A region for (q,s,f) can instead
be projected through q=f+(s-f)p with 0<=p<=1. Its coverage can only inherit
an actually justified joint-region guarantee.

With stipulated s=9/10, f=1/10 and q in [3/10,19/50], compatible p lies in
[1/4,7/20]. The polynomial (4p-1)(20p-7)<=0 supplies an independent exact
runtime sensitivity reference. It has no attached sampling probability.
An illustrative prevention effect equal to one half of event risk, event loss
USD 1000 and action cost USD 200 gives value 500p-200. The two equal-reporting
worlds give -50 and 100; the finite sensitivity interval gives [-75,-25];
an unrestricted p in [0,1] gives [-200,300]. The intervention efficacy is a
separate assumed causal effect model, not identified by a prevalence calculation.

The fixed service screen uses 26 cases, library and CLI, initial and restart
calls, plus two changed-horizon calls under a previously used key: 106 slots.
It includes valid and invalid timezone-aware clocks, empty data, duplicate
origins and false labels, a contradicted identity declaration, unsupported
joint/identity/inclusion/noisy-label checks, explicit alternate clocks,
missing/malformed/wrong-schema artifacts, context and population drift,
byte corruption and custody mismatch, follow-up outcomes incorrectly presented
as features, unavailable measurement fitting, conditional supplied-moment
results, explicit contradicted-premise refusal, and finite/empty/whole-line
and disconnected sensitivity results.

Schema preflight validates requests without calling the service. Expected clock
failures follow explicit ordered timestamps; set endpoints follow factored
polynomials. Supplied normal-summary intervals are deterministic arithmetic
references with critical value two, not a Bernoulli label model or a coverage
experiment. The declared alpha is erfc(sqrt(2)). Absolute endpoint tolerance
is 1e-9 and relative tolerance 1e-10. Full response parity excludes only the
request correlation ID; units, context hashes, qualifications and diagnostic
boundaries remain included.

The review found a critical interpretation trap: an audit operation returning
`computed` means diagnostics were computed. Empty rows can satisfy all declared
clocks vacuously; duplicate origins or false labels with valid timestamps can
also pass. A later estimate can still compute conditional on unverified
measurement premises. An explicitly contradicted premise forces refusal for
estimation, but not for the separate clock check. These are prospectively
declared capability limits, not hidden failures or automatic product acceptance.
The future consumer must require a nonempty, relevant audit, bind it to the
same population/clock/input version, and separately resolve or propagate the
remaining uncertainty. That consumer is a design, not an implemented gate here.

Before registration, author review also caught an inherited recovery-amount
variable in the draft risk-prevalence fixtures. The draft is preserved and the
final context uses a binary adverse event, contact and probability units
consistently. Measurement-only requests explicitly disclaim an intervention
contrast. The generic whole-line and disconnected serializer cases do not apply
the physical parameter bounds; a proposed consumer must do that separately.

Review of the reusable runner preserves its repaired hashing import and uses
an actual clock case for the idempotency test. Artifact references are journaled
before corruption and reused on restart. All slots, process failures and
refusals remain in the denominator. Resume prefixes are hashed. A possible
crash between a call and journal commit can cause an identical repeated
invocation; there is no exactly-once or multi-host claim. No outcomes are used
to change cases, references or the fixed stopping rule.

Cost reporting includes failed and replayed invocation time, worker/CLI startup,
fixture import, journaling, and separate parent/child process high-water RSS.
It excludes idle gaps, initial runner startup, author labor and unexecuted work.
The full proposed workflow additionally budgets data acquisition/rights,
identity resolution, audit sampling/adjudication, nuisance estimation,
integration, scientific review, storage, monitoring/recovery and failed work.
Those prices remain unknown; the USD example is a declared decision scenario.

Local execution, exact mathematical references, a future consumer contract
double and an authentic owner-run validation are separate evidence classes.
A later bank claim needs the owner's population, actual record histories,
inclusion/randomization evidence and independent label truth. None is fabricated
by generated examples. Public or generated cases justify testing prototype
semantics now; costly bank experiments follow only when they answer a
decision-relevant uncertainty with plausible value of information.

Author disposition: proceed with the bounded design, then record and register
before the fixed local screen. Integrate its actual findings into the monograph.
Whole observation reconstruction, sampling calibration and bank acceptance
remain unqualified. This review is not independent acceptance.

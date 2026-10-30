"""Single-use additive clarification of the existing finite proxy construction."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import re
import shutil

from release_candidate_20261029 import MATH

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/release/2026-10-29'
OUT = BASE / 'foundations-029'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def binding(path):
    return {'path': str(path.relative_to(ROOT)), 'sha256': sha(path)}


def main():
    ledger = json.loads((BASE / 'edits.json').read_text())
    assert len(ledger) == 116, 'Single-use integration; do not rerun.'
    source = BASE / 'source/docs/writing-repair/2026-10-29/src/7ccd8624e4c82556.tex'
    anchor = r'\section{Learning the bridge is a conditional-moment problem}'
    addition = r'''\subsection{A treatment bridge need not be a positive weight}
\label{rel29:signed-proxy-bridge}
Equation~\eqref{r3:treatment-bridge} constrains a conditional average of
the bridge, not its pointwise sign. It is an inverse equation, rather
than the definition of an inverse propensity. This distinction follows
from the source's treatment-bridge condition
\citep[Section 4, Assumption 7 and equation (9)]{ghassami2022}.
The finite banking construction above makes the consequence explicit.
Solving its two conditional equations for each action gives
\[
 q(z,0)=-\frac{25}{16}+\frac{75}{8}z,\qquad
 q(z,1)=\frac{125}{16}-\frac{75}{8}z.
\]
For example, among untreated units the probabilities of $Z=1$ given
$W=0$ and $W=1$ are $23/74$ and $15/26$, respectively. Substituting
them gives conditional bridge means $50/37$ and $50/13$. These are
exactly the reciprocals of the untreated probabilities $37/50$ and
$13/50$ given those proxy values. Thus a bridge can take the negative
value $-25/16$ while satisfying both positive conditional targets.
The treated equations give the symmetric construction. These are
project calculations under the already stated finite law, not an
additional empirical finding or a theorem that all bridges are signed.

With these bridges, direct enumeration gives
\[
 \E[\ind\{A=0\}q(Z,0)Y]=\frac32,\qquad
 \E[\ind\{A=1\}q(Z,1)Y]=\frac72.
\]
Their difference is the causal effect $2$. If a generic weighting
routine replaces every negative bridge value by zero, the corresponding
means become $105/64$ and $185/32$, producing the incorrect contrast
$265/64$. The total clipped weight is $95/64$ in each arm, so
normalizing the clipped weights does not repair the result: it gives
arm means $21/19$ and $74/19$, and contrast $53/19$. Positivity of the
action mechanism has not failed; clipping has broken the bridge
equations. If the outcome bridge were also correct, augmentation
would still have its separate outcome-bridge robustness, but the
clipped treatment bridge could no longer justify the other branch.

This example changes the implementation choice. A proxy-bridge solver
must preserve the signed solution and evaluate its conditional moments,
second moments and regularization sensitivity. Large signed values can
signal an unstable inverse problem. Restricting or clipping them is a
new approximation whose bias must be analyzed; calling the operation
ordinary weight stabilization would conceal the changed estimating
equation and potentially change a cost-based decision.

'''
    text = source.read_text()
    assert text.count(anchor) == 1
    edit = dict(file=str(source.relative_to(ROOT)), before=anchor,
                after=addition + anchor,
                reason='Explain the signed nature of an inverse treatment bridge and the consequence of generic positive-weight clipping.',
                substantive_destination='All existing identification, outcome-bridge, remainder, rate and minimax material remains; the new subsection extends the same finite example with its treatment bridge and exact clipping counterexample.')
    ledger.append(edit)
    receipt = json.loads((BASE / 'numerical-verification.json').read_text())
    assert receipt['status'] == 'pass'
    snapshot = OUT / 'numerical-verifier-snapshot.py'
    assert not snapshot.exists()
    shutil.copy2(ROOT / 'tools/release_numerical_verification_20261029.py', snapshot)
    witness = OUT / 'exact-witnesses.json'
    witness.write_text(json.dumps(dict(status='pass', checks=receipt['checks']['foundational_laws'],
        verifier=binding(snapshot), original_bound_inputs=receipt['bindings'],
        scope='Exact enumeration of retained finite laws and explicit perturbations; no new sample or upstream execution.'), indent=2) + '\n')
    primary = ROOT / 'docs/papers/Minimax Kernel Machine Learning for a Class of Doubly Robust Functionals with Application to Proximal Causal Inference Ghassami(2022).pdf'
    original_audit = ROOT / 'docs/program/execution/2026-10-29/panel-runtime-reader-v2/reader/source-audit.json'
    row = dict(citation_key='ghassami2022',
        source_identity='https://proceedings.mlr.press/v151/ghassami22a.html',
        version_date='AISTATS2022 proceedings copy; client literature cutoff2026-10-07; retained original reread2026-10-29',
        primary_audit=str(original_audit.relative_to(ROOT)), primary_audit_sha256=sha(original_audit),
        local_bindings=[binding(primary),binding(OUT/'ghassami-primary.txt')],
        inspected_anchors=['Section4, Assumptions4–7 and equations(8)–(10), Theorems3–4: distinct proxy exclusions, inverse bridge equations and intersection-model influence function; extracted text lines385–490.'],
        supported_claims=['The treatment bridge satisfies a conditional expectation equation; it is not defined as a pointwise reciprocal propensity.',
                          'The source states bridge existence/completeness and influence-function qualifications; the numerical signed-bridge and clipping values are the project derivation.'],
        scope_limits=['Selected primary passage reinspected, not a fresh full-paper review.',
                      'No positivity restriction is imposed on each bridge value by the displayed equation; general existence, uniqueness and stable estimation still require separate assumptions.',
                      'No claim of empirical coverage, bank validation or native implementation.'],
        manuscript_edits=[117])
    audit = OUT / 'source-audit.json'
    audit.write_text(json.dumps(dict(sources=[row], project_derivation=dict(witness=binding(witness),
        source='Existing finite latent law in chapter9; independently enumerated rather than simulated.',
        inspected_anchors=['All16(U,A,Z,W) combinations; two conditional systems per action; clipping, normalization and augmented remainder.'],
        supported_claims=['Signed treatment bridge, preserved mean effect2, clipping contrast265/64 and normalized contrast53/19.'])),indent=2)+'\n')
    reviews_path = BASE / 'mathematical-addition-reviews.json'
    reviews = json.loads(reviews_path.read_text())
    occurrences = lambda s: Counter(re.sub(r'\s+',' ',m[0]) for m in MATH.finditer(s))
    assert not occurrences(edit['before']) - occurrences(edit['after'])
    reviews['reviews'].append(dict(scope='Additive signed treatment-bridge derivation and clipping counterexample within the retained finite law.',
        edits=[dict(edit=117,file=edit['file'],before_sha256=hashlib.sha256(edit['before'].encode()).hexdigest(),after_sha256=hashlib.sha256(edit['after'].encode()).hexdigest())],
        allowed_added=dict(occurrences(edit['after'])-occurrences(edit['before'])), allowed_removed={},
        status='reviewed_additions_only',
        derivation='Solve observable2x2 treatment-bridge equations exactly; enumerate weighted outcomes before and after zero-clipping and arm normalization. The correct outcome bridge retains its independent robustness branch.',
        reviewed_assumptions=['Same stipulated binary latent law, positive action support, independent proxy/assignment innovations conditional onU.',
                              'Exact finite rational calculation, not finite-sample uncertainty or an empirical banking effect.',
                              'Clipping acts only on treatment-bridge values; separate outcome-bridge robustness is not invalidated.'],
        witness=binding(witness), source_audit=binding(audit), fresh_visual_acceptance=False, independent_acceptance=False))
    before = OUT / 'before-integration'
    before.mkdir(exist_ok=False)
    for p in [source,BASE/'edits.json',reviews_path,BASE/'supplemental-source-support.json']:
        shutil.copy2(p,before/p.name)
    supplement = json.loads((BASE/'supplemental-source-support.json').read_text())
    supplement['sources'].append(row)
    source.write_text(text.replace(anchor, edit['after'], 1))
    (BASE/'edits.json').write_text(json.dumps(ledger,indent=2)+'\n')
    reviews_path.write_text(json.dumps(reviews,indent=2)+'\n')
    (BASE/'supplemental-source-support.json').write_text(json.dumps(supplement,indent=2)+'\n')
    print(json.dumps({'edits':len(ledger),'file':edit['file'],'witness':binding(witness),'source_audit':binding(audit)}))


if __name__ == '__main__':
    main()

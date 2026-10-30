"""Single-use integration of pinned flexBCF caller findings, with exact ledger."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/release/2026-10-29'
EVIDENCE = BASE / 'source-flexbcf-016'
SOURCE = BASE / 'source/docs/writing-repair/2026-10-29'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ledger = json.loads((BASE / 'edits.json').read_text())
    assert len(ledger) == 77, 'Single-use integration'
    changes = {}

    def edit(path, before, after, reason, destination):
        original, current = changes.get(path, (path.read_text(), path.read_text()))
        assert current.count(before) == 1, (path, before[:90])
        changes[path] = (original, current.replace(before, after, 1))
        ledger.append(dict(file=str(path.relative_to(ROOT)), before=before, after=after,
                           reason=reason, substantive_destination=destination))

    path = SOURCE / 'src/d587fa2f22fbb93b.tex'
    before = r'''The inspected flexBCF native SATT routine evaluates each stored ensemble on supplied rows, averages within the draw and then calculates quantiles. Its weighted companion divides by the supplied weight sum. The routine name does not select treated rows: cohort selection must already be reflected in its inputs. These selected functions do not settle how all public callers validate empty cohorts, nonfinite weights, zero sums or category levels. The proposed adapter must require explicit cohort and weight contracts; complete caller tracing remains open.~\citep{exec21_cxx_flexbcf}'''
    after = r'''The inspected flexBCF native SATT routine evaluates each stored ensemble on supplied rows, averages within the draw and then calculates quantiles. Its weighted companion divides by the supplied weight sum. The routine name does not select treated rows: cohort selection must already be reflected in its inputs. Following the exported caller at the same revision reveals a more specific problem. In \texttt{average\_tree\_fits}, the treatment branch selects the treatment trees but passes \texttt{treat = FALSE}. The native routine consequently applies prognostic restoration, multiplying by the outcome standard deviation and adding the outcome mean. By contrast, \texttt{get\_tree\_fits} passes \texttt{TRUE} for treatment trees and its native predictor restores only the scale. The supplied predictors reach the corresponding evaluation fields in either branch; the consequential difference here is the additive outcome mean.~\citep{exec21_cxx_flexbcf,rel16flexcallers}

Let $g_i^{(s)}$ denote a standardized treatment-tree evaluation, let $q_i$ be nonnegative target weights with positive sum, and let $\bar Y$ and $s_Y$ be the training outcome mean and standard deviation. The intended and incorrectly restored portfolio draws are
\begin{equation}
 T^{(s)}=s_Y\frac{\sum_i q_i g_i^{(s)}}{\sum_i q_i},
 \qquad \widetilde T^{(s)}=T^{(s)}+\bar Y.
 \label{rel16:flex-scale}
\end{equation}
This difference shifts the posterior mean and every translation-equivariant posterior quantile by the same amount. Consider an authored draw for twenty equally weighted customers: ten standardized evaluations are $1/5$ and ten are $2/5$. With an outcome mean of USD 100 and standard deviation of USD 10, the intended average gain is USD 3; prognostic restoration produces USD 103. At an assumed USD 5 action cost, the corresponding margins are USD $-2$ and USD 98. The two routes imply opposite decisions despite using the same tree evaluations. These are stipulated exact calculations, not output from an executed package or evidence about an actual bank.~\citep{rel16flexcallers,rel16flexwitnesses}

A useful qualification test follows from the meaning of an effect. Adding a common constant to every observed outcome leaves the centered, standardized training outcomes unchanged and should leave the action contrast unchanged, for the same fitted draws and settings. An unwanted additive outcome mean instead transfers that constant into the reported effect. The adapter should test this invariance and compare draw-wise weighted averages from the individual-evaluation path with the summary path after repairing the branch. Simply subtracting the outcome mean downstream would leave the original caller defect and other boundary contracts unresolved.~\citep{rel16flexcallers,rel16flexwitnesses}

The caller rejects a single-row prediction and negative weights, but the inspected caller and weighted routine do not establish a complete contract for finite aligned weights with positive sum or nonempty retained draws. The native routine accesses the first stored draw and divides by the supplied weight sum. A further small-cohort hazard comes from the default progress interval: for two through nine rows, its floor-of-one-tenth rule gives zero, which reaches an integer remainder operation even when verbose output is disabled. The individual-evaluation caller similarly derives its default from the number of draws. These source paths require explicit positive progress intervals, valid draw counts and input checks before native testing. They are findings about the pinned implementation, not a claim that every entrypoint fails or that a particular exception has been observed.~\citep{rel16flexcallers,rel16flexwitnesses}'''
    edit(path, before, after,
         'Resolve the explicitly open public summary caller and expose its scale-restoration and validation contracts.',
         'Preserves draw-first aggregation, target-cohort responsibility and all outstanding weight/draw safeguards; adds the inspected caller distinction, exact monetary witness and reversal test.')

    before = r'''The selected flexBCF trainer derives the control count from prognostic and treatment design sizes and offsets treatment updates accordingly. Its wrapper transposes inputs and passes the treatment indicator. Training order and treatment-specific rows therefore require tracing through public callers and documentation. Assuming the same row layout across all four libraries would hide a consequential boundary error.~\citep{exec21_cxx_flexbcf}'''
    after = r'''The selected flexBCF trainer derives the control count from prognostic and treatment design sizes and offsets treatment updates accordingly. Its public wrapper transposes the supplied matrices and passes the treatment indicator without rearranging rows. The same-revision manual explicitly requires controls before treated subjects; its worked construction supplies prognostic predictors for all subjects but treatment predictors only for treated subjects. The native traversal and residual offsets follow that arrangement. An adapter must apply one common permutation to outcomes, treatment, identifiers and prognostic predictors, then form the treated-only design in the corresponding order. Sorting just the treatment vector would corrupt the correspondence. For subjects $(a,b,c,d)$ with labels $(1,0,1,0)$, a stable valid order is $(b,d,a,c)$ and the treatment design contains $(a,c)$. This identity check is an authored fixture, not a fitted forest.~\citep{exec21_cxx_flexbcf,rel16flexcallers,rel16flexwitnesses}

The manual also requires continuous predictors scaled to $[-1,1]$ and zero-indexed categorical levels. The inspected parsers check selected matrix and level-list dimensions; they do not establish validation of every observed category, outcome scale or treatment-row correspondence. The training wrapper standardizes outcomes before the native call, so a constant outcome needs an explicit supported disposition. These checks should be retained alongside the documented input order and scale conventions. Assuming the same row layout across all four libraries would hide a consequential boundary error.~\citep{exec21_cxx_flexbcf,rel16flexcallers}'''
    edit(path, before, after,
         'Complete the public training-order and treated-only design trace at the already selected revision.',
         'Preserves the native count/offset finding and cross-library warning; replaces the open tracing task with documented conventions, aligned identifiers and remaining validation conditions.')

    before = 'flexBCF is a distinct alternative needing prior, coding, training-order and cohort contracts.'
    after = 'flexBCF is a distinct alternative needing prior, coding, training-order and cohort contracts; its inspected public treatment-summary path must be repaired and qualified before it is enabled.'
    edit(path, before, after,
         'Align the proposal recommendation with the newly established public summary-path defect.',
         'All alternative-library and porting responsibilities remain; the flexBCF candidate is explicitly gated on repair and native qualification.')

    path = SOURCE / 'references-0.bib'
    before = path.read_text()[-500:]
    after = before + r'''

@misc{rel16flexcallers,
 author={{flexBCF contributors}},
 title={Pinned public callers, native restoration and training input contracts},
 year={2025},
 note={flexBCF 1.0.3, revision cf6e51f8c1e0c7a3c1f7\allowbreak{}bfa837196f27bbee751e, 1 December 2025; primary R, C++ and manual inspection; exact identities in the release source audit}
}

@misc{rel16flexwitnesses,
 author={{Causal banking proposal project}},
 title={Exact treatment-scale and training-row correspondence witnesses},
 year={2026},
 note={29 October 2026; stipulated rational arithmetic and identifier alignment; no upstream execution or empirical bank result}
}
'''
    edit(path, before, after,
         'Add primary caller and project-witness citations for the bounded new comparison.',
         'Every existing reference and full identity remains; two evidence records are added.')

    selection = json.loads((EVIDENCE / 'source-selection.json').read_text())
    binding_names = []
    for row in selection:
        raw = ROOT / 'docs/literature/raw' / (row['id'] + '.txt')
        data = raw.read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert blob == row['git_blob_sha1'], row['id']
        receipt = raw.with_name(row['id'] + '.receipt.json')
        rec = json.loads(receipt.read_text())
        assert rec['url'] == row['url'] and rec['sha256'] == sha(raw)
        binding_names.extend([str(raw.relative_to(ROOT)), str(receipt.relative_to(ROOT))])
    for i in range(6):
        binding_names.append(f'docs/literature/raw/exec20_cxx_effects_flexbcf_{i:02d}.txt')
    binding_names.extend(['docs/program/execution/2026-10-20/cxx-effects-v1/alternative-identities.json',
                          'docs/literature/raw/exec20_cxx_effects_tree_flexbcf.json',
                          'docs/release/2026-10-29/source-flexbcf-016/source-selection.json'])
    def bindings(names):
        return [dict(path=n, sha256=sha(ROOT/n)) for n in names]
    audit = dict(cutoff='2026-10-07', scope='Selected primary-source caller trace and exact project witnesses; no upstream execution, new paper admission or bank qualification.', sources=[
        dict(citation_key='rel16flexcallers', kind='implementation', source_identity=[r['url'] for r in selection],
             version_date='flexBCF 1.0.3; cf6e51f8c1e0c7a3c1f7bfa837196f27bbee751e, 2025-12-01. Retrieved 2026-10-29.',
             local_bindings=bindings(binding_names),
             inspected_anchors=[
                 'R/average_tree_fits.R, all 48 lines: singleton/weight guards 9-19; treatment trees with treat=FALSE 31-41; default progress 7.',
                 'R/get_tree_fits.R, all 43 lines: singletons 9-14, draw-derived progress 18/28, treatment TRUE 27-36.',
                 'R/RcppExports.R all 19 lines; src/RcppExports.cpp all 128 lines: argument conversion and direct forwarding; NAMESPACE all 5 lines.',
                 'man/average_tree_fits.Rd all 38 lines; man/get_tree_fits.Rd all 33 lines; man/flexBCF.Rd all 208 lines: controls-first 32-36, scaling/category conventions, treated-only construction 111-156, output shape and method-source leads.',
                 'R/flexBCF.R all 66 lines; src/flexBCF.cpp all 347 lines: standardization and unchanged input order, count derivation 45-49, residual offsets 223-228 and 282-307.',
                 'src/compute_SATT.cpp all 133 lines; src/compute_weighted_SATT.cpp all 141 lines: first draw, weight normalization, progress remainder, scale/mean branches 116-123.',
                 'src/predict_flexBART.cpp all 112 lines: first draw, unconditional progress remainder, true/false restoration 102-109.',
                 'src/funs.cpp lines 1-106: treated traversal and structurally equivalent mean/effect predictor evaluation. src/helpers.h lines 264-380: level-list parsing and design shape checks.',
                 'DESCRIPTION/README/CITATION and retained commit/tree identities establish version and prior differences; no dedicated method-paper result is inherited.'
             ],
             supported_claims=[
                 'The public treatment-average caller sends treatment trees with treat=FALSE; native restoration adds the training outcome mean. Individual treatment evaluations send TRUE and restore scale only.',
                 'Same-revision training documentation and native offsets require controls first and treatment design rows for treated subjects; public wrapper does not sort.',
                 'Selected caller rejects a singleton and negative weights; finite aligned positive-total weights and nonempty draws remain explicit adapter requirements.',
                 'Two to nine prediction rows yield zero default progress for the averaging caller and reach native integer remainder; individual prediction uses a corresponding draw-count default.'
             ], limitations=['Static pinned-source trace, not observed runtime errors or universal package failure.', 'Dedicated method original, transitive rights, complete input validation, repaired native parity and statistical calibration remain open.']),
        dict(citation_key='rel16flexwitnesses', kind='project_derivation',
             source_identity='tools/release_flexbcf_witnesses_20261029.py', version_date='2026-10-29; frozen source-flexbcf-016 witness',
             local_bindings=bindings(['tools/release_flexbcf_witnesses_20261029.py','docs/release/2026-10-29/source-flexbcf-016/exact-witnesses.json']),
             inspected_anchors=['reconstruct(): twenty-row rational scale restoration, outcome-translation invariance, exact margins, stable controls-first identifier correspondence, floor progress for two through nine rows.'],
             supported_claims=['Stipulated USD3 versus USD103 effects produce USD-2 versus USD98 margins at USD5 cost.', 'Common outcome translation should preserve the contrast; wrong restoration shifts it.', 'Joint permutation b,d,a,c aligns treated-only design a,c.'],
             limitations=['No vendor execution, posterior simulation, coverage result or actual bank economics.'])
    ])
    audit_path = EVIDENCE / 'source-audit.json'
    assert not audit_path.exists()
    for p, (old, new) in changes.items():
        assert p.read_text() == old
    backup = EVIDENCE / 'before'
    backup.mkdir(exist_ok=False)
    for p, (old, new) in changes.items():
        (backup / p.name).write_text(old)
    (backup / 'edits.json').write_bytes((BASE / 'edits.json').read_bytes())
    audit_path.write_text(json.dumps(audit, indent=2) + '\n')
    for p, (old, new) in changes.items():
        p.write_text(new)
    (BASE / 'edits.json').write_text(json.dumps(ledger, indent=2) + '\n')
    print(json.dumps({'edits': len(ledger), 'changed_files': len(changes), 'audit_sha256': sha(audit_path)}))


if __name__ == '__main__':
    main()

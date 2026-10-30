"""Explain the equal-stratum weighting already used in the retained calculation."""
from pathlib import Path
import json
import shutil

R = Path(__file__).resolve().parents[1]
B = R / 'docs/release/2026-10-29'
O = B / 'prose-review-078'


def main():
    ledger = json.loads((B / 'edits.json').read_text())
    assert len(ledger) == 214
    p = B / 'source/docs/writing-repair/2026-10-29/src/7849b4fafc2c69f2.tex'
    before = '''The primitives are half-sums and half-differences of the horizon-weighted
candidate responses. This factor matters for both currency units and variance.
Independent binomial audits contribute the delta variance through'''
    after = '''The primitives are half-sums and half-differences of the horizon-weighted
candidate responses. The two strata have equal population weights in this
construction. The additional factor one half in each coefficient averages
their reconstructed focal responses; it is not a second halving of the same
portfolio. Number the four primitives from zero, with each half-sum followed
by its half-difference. This convention explains the difference-component
index in the audit derivative. Independent binomial audits contribute the
delta variance through'''
    text = p.read_text()
    assert text.count(before) == 1
    shutil.copy2(p, O / 'before-weight-clarification.tex')
    p.write_text(text.replace(before, after, 1))
    ledger.append(dict(file=str(p.relative_to(R)), before=before, after=after,
        reason='Explain the equal-stratum weights and zero-based primitive indices used by the existing funding inverse.',
        substantive_destination='The exact original coefficients, audit derivative, covariance, study counts and all adverse findings remain. Added prose exposes the equal-population averaging assumption verified against the retained primitive reconstruction.'))
    (B / 'edits.json').write_text(json.dumps(ledger, indent=2) + '\n')
    receipt=json.loads((O / 'integration.json').read_text())
    receipt.update(edits=[214,215],weight_clarification='Equal population weights and zero-based primitive ordering made explicit; no changed formula or new empirical result.')
    (O / 'integration.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('Applied exact edit215; original equations and retained results unchanged.')


if __name__ == '__main__':
    main()

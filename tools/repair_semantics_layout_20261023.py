#!/usr/bin/env python3
"""Preserve a failed line-break attempt and prepare a separate corrected source."""
from pathlib import Path
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings
import json

ROOT = Path(__file__).resolve().parents[1]
PRIOR = ROOT / 'docs/program/execution/2026-10-23/semantics-reader-v1'
BASE = PRIOR.with_name('semantics-reader-v2')


def main():
    assert not BASE.exists()
    log = PRIOR / 'reader/causal_proposal_semantics_reviewed_2026-10-23.log'
    assert 'Overfull \\hbox (22.40672pt too wide)' in log.read_text()
    verify_bindings(json.loads((PRIOR / 'prepared-inputs.json').read_text()))
    write(PRIOR / 'build-failure.json', dict(status='failed_layout_check',
        evidence=[ref(PRIOR / 'prepared-inputs.json', 'Immutable first prepared inputs'),
            ref(log, 'Observed 22.40672pt overflow at new IV source lines35-45'),
            ref(PRIOR / 'reader/causal_proposal_semantics_reviewed_2026-10-23.pdf', 'Unpublished failed-attempt PDF'),
            ref(Path(__file__), 'Separate successor repair')],
        reason='Unbreakable 40-character Tetrad revision identifier overflows its paragraph.',
        repair='Allow a TeX line break between the first and last20 characters, without changing the identifier.',
        canonical_reader_changed=False, final_acceptance=False))
    BASE.mkdir()
    names = ['integration-plan.md', 'iv-development.tex', 'longitudinal-development.tex',
             'context-development.tex', 'conflict-development.tex']
    for name in names:
        text = (PRIOR / name).read_text()
        if name == 'iv-development.tex':
            old = r'\texttt{b89afaf952a4fd647df0d85b08102250106c6764}'
            new = r'\texttt{b89afaf952a4fd647df0}\allowbreak\texttt{d85b08102250106c6764}'
            assert text.count(old) == 1
            text = text.replace(old, new)
        if name == 'integration-plan.md':
            text += '\nThe first compile overflowed at the Tetrad revision identifier. Its inputs and\nfailed PDF remain preserved in semantics-reader-v1. The v2 successor allows a\nline break inside the same identifier; no source claim or numerical value changes.\n'
        (BASE / name).write_text(text)
    tool = ROOT / 'tools/build_semantics_reader_20261023.py'
    successor = ROOT / 'tools/build_semantics_reader_v2_20261023.py'
    assert not successor.exists()
    code = tool.read_text().replace('semantics-reader-v1', 'semantics-reader-v2').replace(
        'causal_proposal_semantics_reviewed_2026-10-23', 'causal_proposal_semantics_reviewed_v2_2026-10-23')
    code = code.replace("paths = [OLD, PRIOR, Path(__file__),", "paths = [BASE / 'layout-correction.json', OLD, PRIOR, Path(__file__),")
    successor.write_text(code)
    write(BASE / 'layout-correction.json', dict(status='reviewed_source_correction',
        evidence=[ref(PRIOR / 'build-failure.json', 'Preserved failed attempt'),
            ref(tool, 'Original immutable builder'), ref(successor, 'Successor builder'),
            ref(Path(__file__), 'Exact conserving correction')],
        changed_file='iv-development.tex', semantic_change=False, visual_acceptance=False))
    print(json.dumps(dict(successor=str(successor.relative_to(ROOT)), correction='line break only')))


if __name__ == '__main__':
    main()

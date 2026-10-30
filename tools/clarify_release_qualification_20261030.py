"""Repair eleven non-grammatical temporal evidence citations, retaining content."""
from pathlib import Path
import json
import shutil

R = Path(__file__).resolve().parents[1]
B = R / 'docs/release/2026-10-29'
O = B / 'qualification-review-086'


def main():
    ledger = json.loads((B / 'edits.json').read_text())
    assert len(ledger) == 237
    changed = []
    for filename, count in [('72275a22fb653cf2.tex', 2), ('db9ea6894074d6d4.tex', 9)]:
        p = B / 'source/docs/writing-repair/2026-10-29/src' / filename
        before = p.read_text()
        assert before.count(r'\cite{') == count
        after = before.replace(r'\cite{', r'\citep{')
        assert after.replace(r'\citep{', r'\cite{') == before.replace(r'\citep{', r'\cite{')
        shutil.copy2(p, O / ('before-' + filename))
        p.write_text(after)
        ledger.append(dict(file=str(p.relative_to(R)), before=before, after=after,
            reason='Render supporting temporal evidence as parenthetical citations; bare textual author references interrupt otherwise complete sentences.',
            substantive_destination='Every word, equation, number, citation key, label, assumption, negative result and qualification remains in the same source position. Only the citation command changes; no substantive content is deleted.'))
        changed.append(dict(file=str(p.relative_to(R)), commands=count, edit=len(ledger)))
    (B / 'edits.json').write_text(json.dumps(ledger, indent=2) + '\n')
    record = dict(status='written_pending_build_review', edits=[238, 239], changes=changed,
        mathematical_change=False, financial_input_change=False, new_citations=False,
        new_source_reading=False, new_experiment=False,
        review_scope='Complete source chapters97–99 and complete batch082 rendered text read. Eleven confirmed citation-command defects in chapter98; no mathematical defect established by this pass. Fresh visual and independent acceptance remain open.')
    (O / 'integration.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record))


if __name__ == '__main__':
    main()

"""Keep the institutional conclusion about evidence rather than authoring status."""
from pathlib import Path
import json
import shutil

R = Path(__file__).resolve().parents[1]
B = R / 'docs/release/2026-10-29'
O = B / 'prose-review-078'


def main():
    ledger = json.loads((B / 'edits.json').read_text())
    assert len(ledger) == 213
    p = B / 'source/docs/writing-repair/2026-10-29/src/7849b4fafc2c69f2.tex'
    before = '''external observations. The investment argument therefore continues with
bounded scientific capabilities and explicit dependencies, rather than an
assumption that completing the author program has completed adoption.'''
    after = '''external observations. Investment therefore depends on whether the bounded
scientific capabilities meet the institution's evidence, interface and cost
requirements. Completing a research study does not supply institutional
acceptance.'''
    text = p.read_text()
    assert text.count(before) == 1
    O.mkdir(exist_ok=True)
    shutil.copy2(p, O / ('before-' + p.name))
    p.write_text(text.replace(before, after, 1))
    ledger.append(dict(file=str(p.relative_to(R)), before=before, after=after,
        reason='Replace an author-program conclusion with the actual institutional evidence requirement.',
        substantive_destination='The complete independent-review, bank-assignment, truth, selection, interface, economics and platform requirements remain in the preceding paragraphs; the transition retains the distinction between completed research and institutional acceptance. All mathematics and adverse comparisons remain.'))
    (B / 'edits.json').write_text(json.dumps(ledger, indent=2) + '\n')
    (O / 'integration.json').write_text(json.dumps(dict(status='written_pending_build_review',
        edits=[214], target=str(p.relative_to(R)), new_results=False,
        disposition='Confirmed internal author-program wording repaired; other diagnostic uses of receipt, author review and completion state retained where they describe actual treatment, study or software semantics.'), indent=2) + '\n')
    print('Applied exact edit214; institutional requirements and scientific content preserved.')


if __name__ == '__main__':
    main()

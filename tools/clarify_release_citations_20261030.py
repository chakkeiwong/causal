"""Repair reviewed support-citation grammar with exact content preservation."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import shutil

R = Path(__file__).resolve().parents[1]
B = R / 'docs/release/2026-10-29'
O = B / 'citation-review-087'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ledger = json.loads((B / 'edits.json').read_text())
    assert len(ledger) == 239
    rows = json.loads((O / 'occurrences-before.json').read_text())
    assert len(rows) == 43 and sum(len(x['occurrences']) for x in rows) == 415
    manifest = json.loads((B / 'context-review-239/manifest.json').read_text())
    shutil.copy2(B / 'changed-context-review.json', O / 'changed-context-review-before.json')
    shutil.copy2(B / 'review-currency-current.json', O / 'review-currency-before.json')
    (O / 'plan.md').write_text('''# Citation grammar repair

The complete actual input-tree scan finds415 remaining bare cite commands in43
files across22 chapters. Every occurrence and adjacent prose was reviewed.
They supply supporting attribution after a complete clause or sentence; none
uses the citation itself as a grammatical subject. Render them parenthetically.
Retain every prose character, formula, key, number, label and input order.

Plan review: this is a typographic renewal of existing author-reviewed contexts,
not a fresh reading of22 complete chapters or of the primary sources. Exact
component replay must chain to the preserved complete-context reviews, including
the existing35/66/69 component chains. Read the changed rendered citations;
verify unchanged citation labels and mathematical content; rebuild, inspect
text geometry and warnings, renew source checks and package evidence. Review
the deleted command text explicitly after execution. Existing visual and
independent acceptance remain open. No global cite-command redefinition and no
change to intentionally textual citet or existing citep commands.
''')
    changes, prepared = [], []
    for row in rows:
        p = R / row['file']
        text = p.read_text()
        chapter, = {x['chapter'] for x in row['occurrences']}
        c = next(c for c in manifest['chapters'] if c['chapter'] == chapter)
        context = (R / c['extract']).read_text()
        parts = [text]
        # Chapter35 has an expanded nested input; its first complete component
        # contains all reviewed citations and can replay without flattening it.
        if context.count(text) != 1:
            assert p.name == 'f4a7a966d885f66a.tex'
            segments = [s for s in c['segments'] if s['file'] == row['file']]
            parts = [text[s['start']:s['start']+s['characters']] for s in segments
                     if any(s['start'] <= x['start'] < s['start']+s['characters'] for x in row['occurrences'])]
        assert sum(part.count(r'\cite{') for part in parts) == len(row['occurrences'])
        rewritten = text
        for before in parts:
            assert text.count(before) == context.count(before) == 1
            after = before.replace(r'\cite{', r'\citep{')
            assert after.replace(r'\citep{', r'\cite{') == before.replace(r'\citep{', r'\cite{')
            rewritten = rewritten.replace(before, after, 1)
            ledger.append(dict(file=row['file'], before=before, after=after,
                reason='Use parenthetical supporting citations at the individually inspected non-subject occurrences; bare cite renders author names as stray prose.',
                substantive_destination='All substantive text remains at the same position. The only replacement is the citation command name cite→citep. Every equation, numeric input, citation key, label, assumption, negative result and alternative survives in order.'))
            changes.append(dict(file=row['file'], chapter=chapter, edit=len(ledger),
                count=before.count(r'\cite{'), before_sha256=hashlib.sha256(before.encode()).hexdigest(), after_sha256=hashlib.sha256(after.encode()).hexdigest()))
        assert rewritten == text.replace(r'\cite{', r'\citep{')
        prepared.append((p, text, rewritten))
    assert len(ledger) == 283 and sum(c['count'] for c in changes) == 415
    # All exact-context checks complete before mutating any manuscript file.
    for p, text, rewritten in prepared:
        prior = O / ('before-' + p.name)
        if prior.exists():
            assert prior.read_text() == text
        else:
            shutil.copy2(p, prior)
        p.write_text(rewritten)
    (B / 'edits.json').write_text(json.dumps(ledger, indent=2) + '\n')
    result = dict(recorded_utc=datetime.now(timezone.utc).isoformat(), status='written_pending_build_review',
        edits=list(range(240,284)), changes=changes, commands=415,
        chapters=sorted({x['chapter'] for x in changes}),
        scope='Every changed citation and neighboring prose inspected; no new full-chapter, primary-source or visual review.',
        mathematical_change=False, new_sources=False, new_financial_inputs=False, new_experiment=False)
    (O / 'integration.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k:result[k] for k in ['status','edits','commands','chapters']}))


if __name__ == '__main__':
    main()

"""Preserve source title case and complete selected bibliography spacing repairs."""
from pathlib import Path
import hashlib
import json
import re
import shutil

R = Path(__file__).resolve().parents[1]
B = R / 'docs/release/2026-10-29'
O = B / 'bibliography-review-084'


def main():
    ledger = json.loads((B / 'edits.json').read_text())
    assert len(ledger) == 235
    audit = json.loads((B / 'deletion-audit.json').read_text())
    assert audit['status'] == 'pass' and audit['edits'] == 235
    with (O / 'plan.md').open('a') as out:
        out.write('''
## Rendered follow-up

Selected rendered pages reveal that the inherited style lowercases software
names and scientific acronyms even when the bibliographic source supplies the
correct case. Preserve the supplied title case in the renamed local style.
Do not edit sorting, citation labels, names, year suffixes, source identities or
dates. Verify the entire citation-label mapping and body rendering against
batch079. Also repair the explicitly observed remaining joined prose and retain
the literal historical identifier selected17. A case-preserving style cannot
certify that every inherited title is itself correct; such source fidelity
remains bounded by the existing audits.
''')
    p = B / 'source/docs/writing-repair/2026-10-29/references-0.bib'
    before = p.read_text()
    shutil.copy2(p, O / 'before-final-references-0.bib')
    lines = before.splitlines(keepends=True)
    rows = []
    key = ''
    for i, line in enumerate(lines):
        if line.startswith('@'):
            key = line.split('{', 1)[1].split(',', 1)[0]
        if not re.match(r'\s*(title|note)\s*=', line):
            continue
        parts = re.split(r'(https?://[^\s{}]+|[a-f0-9]{40,64})', line)
        for j in range(0, len(parts), 2):
            s = parts[j]
            s = re.sub(r'\b(creation|identity|mirror|package|schema|Julia|POM|CRAN|PMLR|declares)(?=\d)', r'\1 ', s)
            s = s.replace('clientcutoff7', 'client cutoff 7').replace('printedpp759', 'printed pp 759')
            s = re.sub(r'\b(\d+)page\b', r'\1 page', s)
            s = re.sub(r'(\d)UTC\b', r'\1 UTC', s)
            s = re.sub(r',(?=[A-Za-z])', ', ', s)
            s = re.sub(r'(20\d{2}),(?=\d{2}:)', r'\1, ', s)
            s = re.sub(r',(?=20\d{2}\b)', ', ', s)
            if j + 1 < len(parts) and re.fullmatch(r'[a-f0-9]{40,64}', parts[j + 1]):
                if s.endswith(';'):
                    s += ' '
            parts[j] = s
        after_line = ''.join(parts)
        if key == 'exec13_servicing_predecessor':
            after_line = after_line.replace('selected 17', 'selected17')
        assert ''.join(line.split()) == ''.join(after_line.split())
        if line != after_line:
            rows.append(dict(line=i + 1, citation_key=key, before=line.rstrip('\n'), after=after_line.rstrip('\n')))
            lines[i] = after_line
    after = ''.join(lines)
    assert rows and ''.join(before.split()) == ''.join(after.split())
    ledger.append(dict(file=str(p.relative_to(R)), before=before, after=after,
        reason='Complete selected rendered bibliography spacing and preserve literal selected17 identifier.',
        substantive_destination='Whitespace-only copyediting; every non-whitespace character, identifier, date, version and qualification remains.'))
    p.write_text(after)
    p = B / 'source/docs/writing-repair/2026-10-29/causalplainnat-reading.bst'
    before = p.read_text()
    shutil.copy2(p, O / 'before-causalplainnat-reading.bst')
    anchor = '    { title "t" change.case$ }'
    assert before.count(anchor) == 1
    after = before.replace(anchor, '    { title }', 1)
    after = ('% Release copyedit, 2026-10-30: preserve supplied title case.\n'
             '% Renamed project style; no change to sorting or citation labels.\n' + after)
    ledger.append(dict(file=str(p.relative_to(R)), before=before, after=after,
        reason='Render bibliographic titles in their supplied case so software names and scientific acronyms remain readable.',
        substantive_destination='Only title case conversion is removed from the renamed project bibliography style. All source title text, names, keys, sorting, date fields and citation-label logic remain unchanged. This is a presentation change, not a source-identity correction.'))
    p.write_text(after)
    (B / 'edits.json').write_text(json.dumps(ledger, indent=2) + '\n')
    (O / 'style-integration.json').write_text(json.dumps(dict(status='written_pending_review',
        edits=[236, 237], changed_lines=len(rows), rows=rows,
        source_nonspace_identity=True, style_change='Preserve supplied title case; no sorting or citation-label change.',
        scientific_deletions=0), indent=2) + '\n')
    print(json.dumps(dict(edits=[236, 237], changed_lines=len(rows))))


if __name__ == '__main__':
    main()

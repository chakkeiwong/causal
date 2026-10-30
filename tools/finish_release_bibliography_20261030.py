"""Separate remaining observed bibliography compounds without changing content."""
from pathlib import Path
import json
import re
import shutil
from clarify_release_bibliography_20261030 import repair_plain, MONTHS

R = Path(__file__).resolve().parents[1]
B = R / 'docs/release/2026-10-29'
O = B / 'bibliography-review-084'
WORDS = 'family|build|predecessor|reviewed|acquisition|margin|date|Project|publication|and|Findings|metadata|PDF|Pinned|to|edition|CMake|constant|before|selected|command|help|distribution|platform|ingestion|README|Rust|Python|bsts|Boom|BoomSpikeSlab|CausalImpact|Help|EMNLP|ACM|AOAS|AAAI'


def main():
    ledger = json.loads((B / 'edits.json').read_text())
    assert len(ledger) == 234
    audit = json.loads((B / 'deletion-audit.json').read_text())
    assert audit['status'] == 'pass' and audit['edits'] == 234
    p = B / 'source/docs/writing-repair/2026-10-29/references-0.bib'
    before = p.read_text()
    shutil.copy2(p, O / 'before-followup-references-0.bib')
    lines = before.splitlines(keepends=True)
    rows = []
    key = ''
    for i, line in enumerate(lines):
        if line.startswith('@'):
            key = line.split('{', 1)[1].split(',', 1)[0]
        match = re.match(r'\s*(title|note)\s*=', line)
        if not match:
            continue
        parts = re.split(r'(https?://[^\s{}]+|[a-f0-9]{40,64})', line)
        for j in range(0, len(parts), 2):
            s = parts[j]
            s = re.sub(r'\b(' + WORDS + r')(?=\d)', r'\1 ', s)
            s = re.sub(r'(' + MONTHS + r')(20\d{2})', r'\1 \2', s)
            s = re.sub(r'(20\d{2})(?=archive|cover|cutoff|source|version|commit|mirror|arXiv|Ccore)', r'\1 ', s)
            s = re.sub(r'(' + MONTHS + r')(?=\d)', r'\1 ', s)
            s = re.sub(r'\b(\d+)(?=pages\b)', r'\1 ', s)
            for a, z in [('andvariance', 'and variance'), ('C++panel', 'C++ panel'),
                         ('C++:identity', 'C++: identity'), ('onlyv1', 'only v1'),
                         ('of6listed', 'of 6 listed'), ('arXivv4', 'arXiv v4'),
                         ('directMIT', 'direct MIT'), ('Ccore', 'C core')]:
                s = s.replace(a, z)
            s = repair_plain(s, match[1] == 'title')
            # Protected hash tokens retain their exact bytes; separate a prose
            # prefix that touches the start of such a token.
            if j + 1 < len(parts) and re.fullmatch(r'[a-f0-9]{40,64}', parts[j + 1]):
                s = re.sub(r'\b(commit|revision)$', r'\1 ', s)
            parts[j] = s
        after_line = ''.join(parts)
        assert ''.join(line.split()) == ''.join(after_line.split())
        if line != after_line:
            rows.append(dict(line=i + 1, citation_key=key, field=match[1],
                before=line.rstrip('\n'), after=after_line.rstrip('\n')))
            lines[i] = after_line
    after = ''.join(lines)
    assert rows and ''.join(before.split()) == ''.join(after.split())
    ledger.append(dict(file=str(p.relative_to(R)), before=before, after=after,
        reason='Finish observed joined date, descriptive-word and software-version spacing in bibliography fields; whitespace only.',
        substantive_destination='Every non-whitespace character remains in exact order. Full before/after lines identify the copyedits. Source identity, authors, titles, versions, dates, URLs, hashes and technical qualifications are unchanged.'))
    p.write_text(after)
    (B / 'edits.json').write_text(json.dumps(ledger, indent=2) + '\n')
    (O / 'followup-integration.json').write_text(json.dumps(dict(status='written_pending_review',
        edits=[235], changed_lines=len(rows), rows=rows,
        nonspace_identity=True, scientific_deletions=0), indent=2) + '\n')
    print(json.dumps(dict(edit=235, changed_lines=len(rows), nonspace_identity=True)))


if __name__ == '__main__':
    main()

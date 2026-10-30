"""Repair spacing in bibliography prose while preserving every nonspace byte."""
from pathlib import Path
import hashlib
import json
import re
import shutil

R = Path(__file__).resolve().parents[1]
B = R / 'docs/release/2026-10-29'
O = B / 'bibliography-review-084'
MONTHS = 'January|February|March|April|May|June|July|August|September|October|November|December'
WORDS = 'Commit|commit|committed|cutoff|acquired|inspected|accessed|dated|uploaded|released|revision|version|copyright|predates|review|retrieved|submitted|revised|published|preprint|header|through|chapter|DOI'
NAMES = ['pcalg', 'Statistica', 'Stata', 'aGrUM', 'medflex', 'SCOPE-RL',
         'Pipeline', 'POMDP-Py', 'bnlearn', 'mediation', 'POMDPTools', 'tmle',
         'Synth', 'scpi', 'Ananke', 'LiNGAM', 'Delicatessen', 'Dara', 'DiDInt']


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def repair_plain(text, title):
    text = re.sub(r'\b(' + WORDS + r')(?=\d)', r'\1 ', text)
    text = re.sub(r'(?<!\d)(\d{1,2})(' + MONTHS + r')(?=\d|\b)', r'\1 \2', text)
    text = re.sub(r'(' + MONTHS + r')(20\d{2})\b', r'\1 \2', text)
    if title:
        for name in NAMES:
            text = re.sub(r'\b(' + re.escape(name) + r')(?=\d+\.\d)', r'\1 ', text)
        text = text.replace('3.2.0tensor', '3.2.0 tensor')
        text = re.sub(r',(?=[A-Za-z])', ', ', text)
    text = re.sub(r';(?=\S)', '; ', text)
    return text


def main():
    ledger = json.loads((B / 'edits.json').read_text())
    assert len(ledger) == 233
    O.mkdir(exist_ok=False)
    (O / 'plan.md').write_text('''# Bibliography spacing repair

Rendered bibliography inspection found joined dates and package/version names.
Repair only whitespace in title/note prose. Protect URLs and long hexadecimal
identifiers; retain every non-whitespace character and all citation keys,
authors, source titles, version numbers, dates and qualifications. Record each
changed line and use one exact whole-file ledger entry per affected bibliography.

Review the changed rendered entries and their neighbours, compile and repeat
source/preservation checks. This is copyediting of retained bibliographic text,
not new source verification, a complete bibliography reread or visual acceptance.
The author-context records remain meaningful only if all body sources are
unchanged. The final semantic deletion review must confirm no nonspace removal.
''')
    changed = []
    for p in sorted((B / 'source/docs/writing-repair/2026-10-29').glob('references-*.bib')):
        before = p.read_text()
        lines = before.splitlines(keepends=True)
        key = None
        rows = []
        for i, line in enumerate(lines):
            if line.startswith('@'):
                key = line.split('{', 1)[1].split(',', 1)[0]
            match = re.match(r'\s*(title|note)\s*=', line)
            if not match:
                continue
            parts = re.split(r'(https?://[^\s{}]+|[a-f0-9]{40,64})', line)
            for j in range(0, len(parts), 2):
                parts[j] = repair_plain(parts[j], match[1] == 'title')
            after_line = ''.join(parts)
            assert ''.join(line.split()) == ''.join(after_line.split())
            if line != after_line:
                rows.append(dict(line=i + 1, citation_key=key, field=match[1],
                                 before=line.rstrip('\n'), after=after_line.rstrip('\n')))
                lines[i] = after_line
        after = ''.join(lines)
        if before == after:
            continue
        assert ''.join(before.split()) == ''.join(after.split())
        shutil.copy2(p, O / ('before-' + p.name))
        ledger.append(dict(file=str(p.relative_to(R)), before=before, after=after,
            reason='Separate joined dates, descriptive punctuation and software/version names in bibliography prose; whitespace only.',
            substantive_destination='Every non-whitespace character is preserved in exact order. All citation keys, author names, titles, source identities, dates, versions, URLs, hashes and scope qualifications remain. Per-entry line comparison is in bibliography-review-084/integration.json.'))
        p.write_text(after)
        changed.append(dict(file=str(p.relative_to(R)), edit=len(ledger),
                            before_sha256=sha(O / ('before-' + p.name)), after_sha256=sha(p),
                            nonspace_identity=True, rows=rows))
    assert changed
    (B / 'edits.json').write_text(json.dumps(ledger, indent=2) + '\n')
    (O / 'integration.json').write_text(json.dumps(dict(
        status='written_pending_build_review', edits=[x['edit'] for x in changed],
        changed_files=changed, changed_lines=sum(len(x['rows']) for x in changed),
        new_citations=False, nonspace_identity=True, scientific_deletions=0), indent=2) + '\n')
    print(json.dumps(dict(edits=[x['edit'] for x in changed],
        changed_lines=sum(len(x['rows']) for x in changed), nonspace_identity=True)))


if __name__ == '__main__':
    main()

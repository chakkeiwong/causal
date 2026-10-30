"""Correct two observed chapter-reference nouns and preserve the exact predecessor."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil

R = Path(__file__).resolve().parents[1]
B = R / 'docs/release/2026-10-29'
O = B / 'closing-review-092'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    edits = json.loads((B / 'edits.json').read_text())
    assert len(edits) == 290
    before = O / 'before'
    before.mkdir(exist_ok=False)
    snapshots = {}
    for name in ['latest-build.json', 'edits.json', 'deletion-audit.json',
                 'source-verification.json', 'numerical-verification.json',
                 'review-currency-current.json', 'changed-context-review.json',
                 'review-scope-current.json', 'semantic-deletion-review-current.json',
                 'remaining-inventory.json']:
        shutil.copy2(B / name, before / name)
        snapshots[str((B / name).relative_to(R))] = dict(
            path=str((before / name).relative_to(R)), sha256=sha(before / name))
    rows = json.loads((O / 'reference-type-scan-before.json').read_text())
    assert len(rows) == 2
    changes = []
    for row in rows:
        p = R / row['file']
        old = row['before']
        assert old.startswith('Section~') and row['destination']['kind'] == 'chapter'
        new = old.replace('Section~', 'Chapter~', 1)
        text = p.read_text()
        assert text.count(old) == 1
        shutil.copy2(p, before / p.name)
        edits.append(dict(file=row['file'], before=old, after=new,
            reason='Rendered-text review found a chapter described as a section; the compiled label explicitly targets a chapter.',
            substantive_destination='The same label, destination, surrounding scientific argument and all mathematics remain. Only the reference noun Section changes to Chapter.'))
        p.write_text(text.replace(old, new, 1))
        changes.append(dict(edit=len(edits), file=row['file'], before=old, after=new,
                            compiled_destination=row['destination']))
    (B / 'edits.json').write_text(json.dumps(edits, indent=2) + '\n')
    record = dict(recorded_utc=datetime.now(timezone.utc).isoformat(),
        status='written_pending_build_and_context_renewal', predecessor_batch=85,
        changes=changes, preserved_predecessor_pointers=snapshots,
        scope='Two reference-noun corrections only. No mathematical, numerical, source or scientific claim changes.',
        plan_review='Renew both affected context chains, read actual changed rendered passages, rerun final deletion/source/numerical checks and bind final packages to the successor. Frozen085 evidence remains unchanged.')
    (O / 'integration.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(dict(status=record['status'], edits=len(edits), changes=changes)))


if __name__ == '__main__':
    main()

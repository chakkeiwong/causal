"""Extend the attributed deletion assessment to the verified 290-edit candidate."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

R = Path(__file__).resolve().parents[1]
B = R / 'docs/release/2026-10-29'
O = B / 'preservation-review-089'


def read(p):
    return json.loads(p.read_text())


def save(p, value):
    p.write_text(json.dumps(value, indent=2) + '\n')


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def bind(p):
    return dict(path=str(p.relative_to(R)), sha256=sha(p))


def main():
    edits = read(B / 'edits.json')
    audit, build = read(B / 'deletion-audit.json'), read(B / 'latest-build.json')
    assert len(edits) == 290 and build['batch'] == 85 and audit['status'] == 'pass'
    assert audit['ledger_sha256'] == sha(B / 'edits.json')
    assert audit['checks_after_final_edit'] and audit['exact_replay']
    assert not any(audit[k] for k in ['math_removed', 'missing_citation_keys', 'missing_labels', 'distinct_numeric_loss'])
    prior_path = B / 'preservation-review-085/semantic-deletion-review.json'
    prior = read(prior_path)
    prefix = (json.dumps(edits[:237], indent=2) + '\n').encode()
    assert hashlib.sha256(prefix).hexdigest() == prior['ledger']['sha256']
    receipts = [B / folder / 'contextual-review.json' for folder in [
        'qualification-review-086', 'citation-review-087', 'quotation-review-088']]
    reviewed = {}
    for p in receipts:
        review = read(p)
        for item in review['deletion_assessment']:
            i = item['edit']
            assert i not in reviewed
            reviewed[i] = dict(assessment=item['disposition'], observed_context_review=bind(p))
    assert set(reviewed) == set(range(238, 291))
    dispositions = []
    for i in range(238, 291):
        e = edits[i - 1]
        if i <= 283:
            assert e['before'].replace(r'\cite{', r'\citep{') == e['after']
            operation = 'Supporting citation command only; every non-command character retained.'
        else:
            assert e['before'].replace(r"'\,'", "''") == e['after']
            operation = 'Thin-space command inside closing quote only; quoted text retained.'
        dispositions.append(dict(edit=i, file=e['file'],
            before_sha256=hashlib.sha256(e['before'].encode()).hexdigest(),
            after_sha256=hashlib.sha256(e['after'].encode()).hexdigest(),
            exact_transformation=operation, **reviewed[i]))
    restored = []
    for i in [212, 213]:
        e = edits[i - 1]
        assert e['after'] in (R / e['file']).read_text()
        restored.append(dict(edit=i, file=e['file'], exact_current_anchor=True,
            scope='Explicit correlation-test obligation' if i == 212 else
            'Assignment-evidence and structural-restriction alternatives'))
    numerics = read(B / 'numerical-verification.json')
    assert numerics['status'] == 'pass' and len(numerics['checks']) == 68
    O.mkdir(exist_ok=False)
    (O / 'verified-ledger-prefix-237.json').write_bytes(prefix)
    record = dict(recorded_utc=datetime.now(timezone.utc).isoformat(),
        status='complete_in_author_scope', batch=85, edits=290,
        ledger=bind(B / 'edits.json'), publication=audit['publication'],
        predecessor_review=bind(prior_path), predecessor_prefix_verified=237,
        earlier_substantive_candidates=80, later_reviewed_edits=53,
        citation_only_edits=46, quotation_spacing_only_edits=7,
        dispositions=dispositions, preserved_repair_anchors=restored,
        mechanical_audit=bind(B / 'deletion-audit.json'),
        scope='Extends the exact 237-edit predecessor assessment using the attributed source/rendered reviews of edits238–290 and exact constrained transformations. No fresh full-book reading or independent semantic certification is claimed.',
        conclusion='No unaccounted removal of important scientific material is identified in the assessed290 edits. Both earlier repaired obligations remain verbatim. The53 later edits retain every substantive character:46 repair supporting citation commands and7 remove erroneous quote spacing. Equations, assumptions, adverse findings, serious alternatives and source qualifications remain.',
        limits='Mechanical retention is not a general proof of semantic completeness. Earlier substantive dispositions rely on the recorded contextual author assessments. Fresh visual and independent editorial/scientific acceptance remain outstanding.',
        acceptance=dict(author_semantic_review=True, fresh_visual=False,
                        independent=False, release_accepted=False))
    save(O / 'semantic-deletion-review.json', record)
    save(B / 'semantic-deletion-review-current.json', record)
    lines = ['# Current semantic deletion review', '',
        'Batch085;290 exact edits. The first237 match the immutable predecessor ledger. '
        'Its80 substantive removal candidates, later individual dispositions and two repairs '
        'remain attributable through the preserved review chain. The53 latest edits '
        'have exact constrained transformations and contextual dispositions.', '',
        record['conclusion'], '', record['limits'], '', '| Edit | Assessment |', '|---|---|']
    for d in dispositions:
        lines.append(f'| {d["edit"]} | {d["assessment"]} |')
    (B / 'semantic-deletion-review-current.md').write_text('\n'.join(lines) + '\n')
    scope = read(B / 'review-scope-current.json')
    for p in [prior_path, O / 'verified-ledger-prefix-237.json',
              O / 'semantic-deletion-review.json', B / 'semantic-deletion-review-current.json',
              B / 'numerical-verification.json']:
        scope['basis'][str(p.relative_to(R))] = sha(p)
    scope['semantic_deletion_review'] = bind(B / 'semantic-deletion-review-current.json')
    save(B / 'review-scope-current.json', scope)
    print(json.dumps(dict(status=record['status'], batch=85, edits=290,
        prior_prefix=237, later_dispositions=53, repaired_obligations_retained=True)))


if __name__ == '__main__':
    main()

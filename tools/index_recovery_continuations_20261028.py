"""Index all unresolved obligations; structural recovery does not close research."""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

from publish_latent_r_review_v2_20261013 import ref, write

ROOT = Path(__file__).resolve().parents[1]
DAY = ROOT / 'docs/program/execution/2026-10-28'
BASE = DAY / 'continuation-inventory-v1'
TAIL_NAMES = re.compile(r'omission|conversion|search|candidate|dependency|license|comparison-design|primary-review')


def refs(value):
    if isinstance(value, dict):
        if isinstance(value.get('path'), str) and isinstance(value.get('sha256'), str):
            yield value
        for child in value.values():
            yield from refs(child)
    elif isinstance(value, list):
        for child in value:
            yield from refs(child)


def main():
    assert not BASE.exists()
    remaining_path = DAY / 'program-refresh-nested-v1/remaining-operations.json'
    old_path = DAY / 'followup-runtime-v1/software-tails.json'
    remaining = json.loads(remaining_path.read_text())
    trace = json.loads(old_path.read_text())
    old = {r['id']: r for r in trace['rows']}
    operations = remaining['operations']
    assert len(operations) == 150 and len(old) == 104
    desired = {r['id'] for r in operations if r['id'].startswith(('SW.CELL.', 'SW.DECISION.'))}
    assert len(desired) == 105 and desired - old.keys() == {'SW.CELL.discovery_iid.commercial'}
    BASE.mkdir()
    plan = dict(status='reviewed_for_structural_recovery', evidence=[
        ref(remaining_path, 'All 150 original unresolved obligations'),
        ref(old_path, 'Prior 104-row software trace'),
        ref(DAY / 'continuation-control-recovery-v1/plan-review.json', 'Recovery execution plan'),
        ref(Path(__file__), 'Exact bounded index and custody checks')],
        checks=[
            'Account for all 150 obligations and all 105 software/reuse rows, including the omitted open commercial cell.',
            'Verify each exact action-basis binding; recover tail paths from bound receipts and outputs without filename-only omission assumptions.',
            'Preserve every original status, local prerequisite and missing external input.',
            'Match current citation evidence only as a navigation lead, never as semantic reconciliation or acceptance.',
            'Retain all mismatches and scope limits; do not overwrite historical receipts.',
        ], awards_acceptance=False)
    write(BASE / 'plan-review.json', plan)
    audit_path = DAY / 'nested-reader-v2/reader/source-audit.json'
    audit = json.loads(audit_path.read_text())
    current_sources = []
    for s in audit['sources']:
        key = s.get('integrated_citation_key', s.get('id'))
        current_sources.append((key, {r['path'] for r in refs(s)}))
    checked = {}
    issues = []

    def check(binding):
        identity = (binding['path'], binding['sha256'])
        if identity in checked:
            return checked[identity]
        p = ROOT / binding['path']
        actual = hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
        ok = actual == binding['sha256']
        checked[identity] = ok
        if not ok:
            issues.append(dict(path=binding['path'], expected_sha256=binding['sha256'], observed_sha256=actual))
        return ok

    corrected = {
        'SW.CELL.discovery_iid.Python': [DAY / 'python-continuation-recovery-v1/reconciliation.json'],
        'SW.CELL.discovery_iid.Java': [DAY / 'software-tail-java-panel-delta-v1/source-tail-delta.json', DAY / 'reliableai-nested-v1/author-review.json'],
        'SW.CELL.panels_did.R': [DAY / 'software-tail-java-panel-delta-v1/source-tail-delta.json'],
    }
    rows = []
    for operation in operations:
        key = operation['id']
        historical = old.get(key)
        basis = operation.get('action_basis') or operation.get('evidence')
        if basis:
            check(basis)
        candidates = {}
        documents = []
        if basis and check(basis):
            documents.append(ROOT / basis['path'])
        for name in operation.get('outputs', []):
            p = ROOT / name
            if p.is_file():
                documents.append(p)
        if historical:
            for item in historical['exact_bound_tail_documents']:
                binding = item['binding']
                candidates[binding['path']] = binding
                check(binding)
        # Inspect direct bound records, then one layer of scientific source/tail
        # packets. Avoid recursively opening large historical publication audits.
        visited = set()
        related = set()
        for depth in range(2):
            next_docs = []
            for p in documents:
                relative = str(p.relative_to(ROOT))
                if relative in visited:
                    continue
                visited.add(relative)
                try:
                    value = json.loads(p.read_text())
                except (ValueError, UnicodeError):
                    continue
                for binding in refs(value):
                    related.add(binding['path'])
                    if TAIL_NAMES.search(Path(binding['path']).name):
                        if check(binding):
                            candidates[binding['path']] = binding
                            if binding['path'].endswith('.json'):
                                next_docs.append(ROOT / binding['path'])
            documents = next_docs
        leads = sorted({k for k, paths in current_sources if k and paths & (related | set(candidates))})
        row = dict(id=key, lane=operation['lane'], original_status=operation['status'],
                   original_action=operation['action'], action_basis=basis,
                   acceptance_prerequisites=operation.get('prerequisites', []),
                   required_external_inputs=operation.get('requires_inputs', []),
                   exact_tail_documents=list(candidates.values()),
                   citation_evidence_overlap_leads=leads,
                   overlap_status='Navigation only; source meaning and later completeness require review.',
                   historical_status_unchanged=True)
        if historical:
            row['unresolved_receipt_criteria'] = historical['unresolved_receipt_criteria']
        if key in corrected:
            row['later_continuation_reviews'] = [ref(p, 'Verified bounded later continuation; original qualification unchanged') for p in corrected[key]]
            row['reconciliation_status'] = 'bounded_later_delta_recorded'
        else:
            row['reconciliation_status'] = 'later_semantic_reconciliation_still_required'
        if key.startswith('SW.REVIEW.') or key in ('RELEASE.RECONCILE', 'PROPOSAL.Q1', 'PROPOSAL.Q5'):
            row['eligible_next_action'] = 'Prepare and review component evidence independently; retain listed prerequisites only for final acceptance. ' + operation['action']
        elif key == 'RELEASE.VISUAL':
            row['eligible_next_action'] = 'Local blocker: fresh image allowance is required; retain current text/bounds evidence and continue independent nonvisual work.'
        else:
            row['eligible_next_action'] = operation.get('corrected_continuation', operation['action'])
        if key == 'SW.CELL.discovery_iid.Python':
            row['eligible_next_action'] = 'Use corrected Python reconciliation: retain completed RL/attention/CDT/causal-learn work; screen remaining aliases/original editions and declare one reproducible source/rights profile before native qualification.'
        rows.append(row)
    register = dict(status='performed_structural_inventory', rows=rows,
        counts=dict(original_unresolved=150, software_reuse_rows=105, historical_trace_rows=104,
                    newly_recovered_trace_rows=1, bounded_later_delta_rows=3,
                    software_reuse_rows_needing_semantic_reconciliation=102,
                    rows_with_tail_bindings=sum(bool(r['exact_tail_documents']) for r in rows),
                    verified_binding_identities=sum(checked.values()), binding_mismatches=len(issues)),
        evidence=[ref(remaining_path, 'Original statuses and actions'), ref(old_path, 'Preserved historical trace'),
                  ref(audit_path, 'Current integrated evidence used only for navigation'), ref(BASE / 'plan-review.json', 'Reviewed scope')],
        issues=issues, original_status_counts=dict(Counter(r['original_status'] for r in rows)),
        limitations=['This is a complete structural inventory, not full 105-row semantic reconciliation.',
                     'Citation overlap is not evidence of coverage, rights, native behavior or completion.',
                     'Inspection is bounded to receipt/output and one scientific packet layer; not recursive global custody validation.'],
        original_outcomes_unchanged=True, awards_acceptance=False, final_acceptance=False)
    write(BASE / 'continuation-register.json', register)
    missing_before = [r['id'] for r in trace['rows'] if not r['exact_bound_tail_documents']]
    recovered = {r['id']: len(r['exact_tail_documents']) for r in rows if r['id'] in missing_before}
    write(BASE / 'author-review.json', dict(status='pass_for_inventory' if not issues else 'inconclusive_due_to_bindings',
        evidence=[ref(BASE / 'continuation-register.json', 'Every original unresolved operation indexed')],
        checks=dict(unique_ids=len({r['id'] for r in rows}) == 150,
                    software_reuse_union={r['id'] for r in rows if r['id'].startswith(('SW.CELL.', 'SW.DECISION.'))} == desired,
                    original_statuses_preserved=all(r['original_status'] == o['status'] for r, o in zip(rows, operations)),
                    prior_empty_tail_rows=recovered),
        issues=issues, awards_acceptance=False))
    lines = ['# Complete continuation inventory after recovery', '',
        'All 150 original unresolved obligations remain: 121 inconclusive, 25 open and four negative.',
        'The software/reuse continuation subset has 105 rows. The prior 104-row trace omitted the open commercial IID-discovery cell.',
        'Three rows have bounded later-evidence deltas (Python IID, Java IID and R panel); 102 still need semantic reconciliation.',
        'This inventory repairs routing and exact evidence navigation. It does not qualify software or close mandatory proposal coverage.', '',
        '## Independent execution rule', '',
        'Candidate source reconciliation and public proposal design remain eligible regardless of later bank validation or rendered-image limits.',
        'Acceptance dependencies apply to final acceptance, not to preparing independent comparisons.',
        'Keep source identity, inspected meaning, reproducible prototype behavior and institutional acceptance distinct.', '',
        '## Evidence recovered from formerly empty tail lists', '']
    lines += [f'- {k}: {v} exact tail/source bindings recovered.' for k, v in recovered.items()]
    lines += ['', f'Binding mismatches in this bounded pass: {len(issues)}. Every mismatch remains in the JSON register.',
              'The separate Python recovery preserves two earlier authored-reference hash mismatches and verifies a successor replay; it does not erase them.', '']
    (BASE / 'continuation-guide.md').write_text(chr(10).join(lines))
    print(json.dumps(dict(status=register['status'], counts=register['counts'], empty_tail_recovery=recovered)))


if __name__ == '__main__':
    main()

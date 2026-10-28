"""Preserve prior findings while repairing a demonstrably stale source omission."""
import hashlib
import json
from pathlib import Path

from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = Path(__file__).resolve().parents[1]
DAY = ROOT / 'docs/program/execution/2026-10-28'
BASE = DAY / 'python-continuation-recovery-v1'


def main():
    assert not BASE.exists(), 'Preserve performed reconciliation.'
    prior = DAY / 'followup-runtime-v6/python-discovery-delta.json'
    old = json.loads(prior.read_text())
    verify_bindings(old)
    primary = ROOT / 'docs/program/execution/2026-10-14/causallearn-reuse/primary-review.json'
    review = ROOT / 'docs/program/execution/2026-10-14/causallearn-reuse/author-review.json'
    primary_data = json.loads(primary.read_text())
    verify_bindings(primary_data)
    verify_bindings(json.loads(review.read_text()))
    pin = '0dacacf36390e3084704636bc3c36e82e35ee0cc'
    assert primary_data['pinned_revision'] == pin
    license_record = next(s for s in primary_data['sources'] if s['source_identity'].endswith('/LICENSE'))
    assert '/' + pin + '/LICENSE' in license_record['source_identity']
    content = (ROOT / license_record['local_copy']['path']).read_bytes()
    assert hashlib.sha256(content).hexdigest() == license_record['local_copy']['sha256']
    blob = hashlib.sha1(b'blob ' + str(len(content)).encode() + bytes([0]) + content).hexdigest()
    assert blob == license_record['git_blob_sha1'] and license_record['tree_match']
    assert b'MIT License' in content and b'Copyright (c) 2022 cmu-phil' in content
    retained = [
        'followup-runtime-v2/cdt-delegates.json',
        'followup-runtime-v3/cdt-dependencies.json',
        'followup-runtime-v3/python-rl-tail.json',
        'followup-runtime-v4/cdt-installer.json',
        'followup-runtime-v4/attention-search.json',
        'followup-runtime-v5/tcdf-delegate.json',
        'followup-runtime-v5/tacd-protocol.json',
        'followup-runtime-v5/attention-originals.json',
        'followup-runtime-v6/paper-identity.json',
        'public-attention-contract-v2/author-review.json',
    ]
    for name in retained:
        verify_bindings(json.loads((DAY / name).read_text()))
    BASE.mkdir()
    evidence = [ref(prior, 'Preserved earlier delta containing stale license omission'),
                ref(primary, 'Pinned 14 October primary-source and Git-blob review'),
                ref(review, 'Existing author review; conditional reuse only'),
                ref(Path(__file__), 'Exact recovery and verification logic')]
    write(BASE / 'plan-review.json', dict(
        status='pass_for_continuation_repair', evidence=evidence,
        checks=[
            'Match exact technical commit, SHA-256, Git blob and inspected license bytes.',
            'Correct only source-access omission; transitive rights and native qualification remain open.',
            'Retain later CDT, RL, attention, TCDF, TACD and 48-case public fixture records.',
            'Do not edit historical receipts or infer complete family coverage.',
        ], awards_acceptance=False))
    rows = old['rows']
    for row in rows:
        if row['id'] == 'CAUSALLEARN-LICENSE-PIN':
            row.update(status='named_source_identity_addressed',
                finding='The authentic LICENSE at the exact technical commit was already inspected on 14 October. Its SHA-256 and Git blob reverify. The 28 October delta incorrectly carried the acquisition omission forward; preserve that historical error and use this successor.',
                evidence=[ref(primary, 'Exact pinned original and Git-blob agreement'), ref(review, 'Existing author-reviewed conditional reuse decision')],
                next_action='Do not reacquire this LICENSE. Preserve its notice and resolve the selected dependency/distribution terms before redistribution or native admission.')
        elif row['id'] == 'CDT-DELEGATES':
            row['next_action'] = 'Retain inspected templates, launcher, dependency declarations and installer. Declare a new resolved distribution profile and component terms, then preregister native permutation, failure and cancellation trials; do not invent a historical environment.'
        elif row['id'] == 'PY-CENSUS':
            row['next_action'] = 'Retain ENCO, RL/CORL and selected attention reviews, including later TCDF/TACD delegates and the separate 48-case authored contract. Screen remaining candidate aliases and genuine original editions; family census and native/calibration claims remain open.'
        else:
            row['next_action'] = row['original_action']
    write(BASE / 'reconciliation.json', dict(
        status='performed_bounded_continuation_repair', operation_id='SW.CELL.discovery_iid.Python',
        rows=rows, retained_later_evidence=[ref(DAY / p, 'Retain completed selected work; do not reset acquisition') for p in retained],
        verified_license=dict(source_identity=license_record['source_identity'], local_copy=license_record['local_copy'],
                              git_blob_sha1=blob, bytes=len(content), inspected_lines=[1, 21]),
        evidence=evidence + [ref(BASE / 'plan-review.json', 'Reviewed bounded repair')],
        historical_outcome='inconclusive', original_outcome_unchanged=True,
        source_access_omissions_corrected=1, new_acquisitions=0,
        native_execution=False, awards_acceptance=False, final_acceptance=False))
    text = '''# Python discovery continuation after recovery

The exact causal-learn license acquisition gap is already addressed. The
14 October primary review binds the MIT text to the same technical commit,
0dacacf36390e3084704636bc3c36e82e35ee0cc. Rechecking the original 1,065 bytes
confirms both SHA-256 and Git blob identity. The later 28 October delta carried
this omission forward incorrectly. Both earlier records are preserved; this
successor corrects the action without awarding broader rights or acceptance.

Keep the inspected CDT templates, launcher, dependency declarations and installer;
the RL/CORL papers and source findings; and the attention, TCDF and TACD reviews.
The later 48-case project fixture remains separate from any native engine trial.
No repeated acquisition or test run is needed for those completed scoped tasks.

The remaining work is candidate/alias coverage and genuine missing original
editions, one declared reproducible dependency profile, component and transitive
terms, and matched native conversion/failure/calibration trials after proposal
merit. Do not reconstruct an unpinned historical environment by assertion.
No bank evidence is required to continue independent public proposal research.
The original Python coverage outcome remains inconclusive.
'''
    (BASE / 'reconciliation.md').write_text(text)
    result = json.loads((BASE / 'reconciliation.json').read_text())
    verify_bindings(result)
    write(BASE / 'author-review.json', dict(status='pass_for_stale_source_omission_only',
        evidence=[ref(BASE / 'reconciliation.json', 'Exact source and preserved later work'), ref(BASE / 'reconciliation.md', 'Readable continuation')],
        outcome='inconclusive_for_original_coverage', awards_acceptance=False,
        next_action='Use corrected source tails and continue independent candidate-specific proposal work.'))
    print(json.dumps(dict(status='pass', corrected_source_omissions=1, retained_later_packets=len(retained), original_outcome='inconclusive')))


if __name__ == '__main__':
    main()

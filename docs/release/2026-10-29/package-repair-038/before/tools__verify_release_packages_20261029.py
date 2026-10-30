"""Relocate frozen packages, reconstruct them and reject altered evidence."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/release/2026-10-29'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch', type=int, required=True)
    args = parser.parse_args()
    suffix = f'batch-{args.batch:03d}'
    package = BASE / 'packages' / suffix
    numerical = BASE / 'numerical-packages' / suffix
    manifest = json.loads((package / 'manifest.json').read_text())
    nm = json.loads((numerical / 'manifest.json').read_text())
    assert manifest['batch'] == nm['reference_batch'] == args.batch
    assert manifest['publications']['full']['sha256'] == nm['reader_sha256']
    output = BASE / ('portability-' + suffix)
    noutput = BASE / ('numerical-portability-' + suffix)
    output.mkdir(exist_ok=False)
    noutput.mkdir(exist_ok=False)
    temporary = Path(tempfile.mkdtemp(prefix=f'causal-release-{args.batch:03d}-'))
    relocated = temporary / 'manuscript'
    relocated_num = temporary / 'numerical'
    external = temporary / 'external'
    shutil.copytree(package, relocated)
    shutil.copytree(numerical, relocated_num)
    for name, row in nm['inputs'].items():
        if row['external']:
            target = external / name
            target.parent.mkdir(parents=True, exist_ok=True)
            assert sha(ROOT / name) == row['sha256']
            shutil.copy2(ROOT / name, target)

    def run(command, log):
        with log.open('w') as stream:
            result = subprocess.run(command, cwd=temporary, stdout=stream,
                                    stderr=subprocess.STDOUT, timeout=1800)
        print(json.dumps({'command': command, 'returncode': result.returncode,
                          'log': str(log.relative_to(ROOT))}), flush=True)
        return result.returncode

    # Build and preservation operate only on the relocated frozen package.
    build = temporary / 'compiled'
    assert run(['python3', str(relocated / 'build.py'), '--output', str(build)],
               output / 'build.log') == 0
    build_result = json.loads((build / 'result.json').read_text())
    assert build_result['status'] == 'pass'
    shutil.copy2(build / 'result.json', output / 'result.json')
    preserve = temporary / 'preservation'
    assert run(['python3', str(relocated / 'check_preservation.py'), '--output', str(preserve)],
               output / 'preservation.log') == 0
    preservation = json.loads((preserve / 'preservation-replay.json').read_text())
    assert preservation['status'] == 'pass'
    shutil.copy2(preserve / 'preservation-replay.json', output / 'preservation-replay.json')

    adversarial = []
    for case in ['missing_witness', 'changed_protected_original', 'changed_math_review']:
        altered = temporary / case
        shutil.copytree(relocated, altered)
        if case == 'missing_witness':
            review = json.loads((altered / 'evidence/mathematical-addition-reviews.json').read_text())['reviews'][-1]
            name = review['witness']['path'].removeprefix('docs/release/2026-10-29/')
            victim = altered / 'evidence' / name
            victim.rename(victim.with_suffix('.withheld'))
        elif case == 'changed_protected_original':
            row = json.loads((altered / 'evidence/protected-relocations.json').read_text())['relocations'][0]
            name = row['preserved'].removeprefix('docs/release/2026-10-29/')
            victim = altered / 'evidence' / name
            victim.write_bytes(victim.read_bytes() + b'\nintentional test corruption\n')
        else:
            victim = altered / 'evidence/mathematical-addition-reviews.json'
            value = json.loads(victim.read_text())
            value['reviews'][-1]['after_sha256'] = '0' * 64
            victim.write_text(json.dumps(value, indent=2) + '\n')
        test_output = temporary / (case + '-result')
        code = run(['python3', str(altered / 'check_preservation.py'), '--output', str(test_output)],
                   output / (case + '.log'))
        report = json.loads((test_output / 'preservation-replay.json').read_text())
        assert code != 0 and report['status'] == 'fail' and report['issues']
        adversarial.append({'case': case, 'returncode': code, 'issues': report['issues']})
    (output / 'adversarial-preservation.json').write_text(json.dumps(adversarial, indent=2) + '\n')

    tests = []
    for case in ['complete', 'missing_external', 'corrupt_external']:
        supplied = external
        if case != 'complete':
            supplied = temporary / case
            shutil.copytree(external, supplied)
            name = next(k for k, v in nm['inputs'].items() if v['external'])
            victim = supplied / name
            if case == 'missing_external':
                victim.rename(victim.with_suffix('.withheld'))
            else:
                victim.write_bytes(victim.read_bytes() + b'\nintentional test corruption\n')
        test_output = temporary / ('numerical-' + case)
        code = run(['/home/ubuntu/miniforge3/bin/python', str(relocated_num / 'reconstruct.py'),
                    '--external-root', str(supplied), '--output', str(test_output)],
                   noutput / (case + '.log'))
        report = json.loads((test_output / 'result.json').read_text())
        if case == 'complete':
            assert code == 0 and report['status'] == 'pass'
            assert len(report['reconstructed_checks']) == len(nm['check_groups'])
            shutil.copy2(test_output / 'numerical-verification.json', noutput / 'reconstructed.json')
        else:
            assert code != 0 and report['status'] == 'fail' and report['issues']
        tests.append({'case': case, 'returncode': code, 'report': report})
    nreceipt = {'status': 'pass',
                'scope': f'Relocated {len(nm["check_groups"])}-group reconstruction plus missing/corrupt external-input rejection; no original-checkout numerical input used by runner.',
                'reader_sha256': nm['reader_sha256'],
                'manifest_sha256': sha(numerical / 'manifest.json'), 'tests': tests}
    (noutput / 'result.json').write_text(json.dumps(nreceipt, indent=2) + '\n')

    # Prove test mutations were confined to their deliberately altered copies.
    for line in (package / 'SHA256SUMS').read_text().splitlines():
        digest, name = line.split('  ', 1)
        assert sha(package / name) == sha(relocated / name) == digest
    for name, digest in nm['files'].items():
        assert sha(numerical / name) == sha(relocated_num / name) == digest
    proof = {'status': 'pass', 'batch': args.batch,
             'package': str(package.relative_to(ROOT)),
             'manifest_sha256': sha(package / 'manifest.json'),
             'build_result': str((output / 'result.json').relative_to(ROOT)),
             'build_result_sha256': sha(output / 'result.json'),
             'preservation_replay': str((output / 'preservation-replay.json').relative_to(ROOT)),
             'preservation_replay_sha256': sha(output / 'preservation-replay.json'),
             'adversarial_checks': {'path': str((output / 'adversarial-preservation.json').relative_to(ROOT)),
                                    'sha256': sha(output / 'adversarial-preservation.json')},
             'reader_sha256': manifest['publications']['full']['sha256'],
             'sponsor_sha256': manifest['publications']['sponsor']['sha256'],
             'scope': f'Same installed TeX system, relocated package; no original-checkout compiler input; {preservation["edits"]} edits replayed from {preservation["replayed_sources"]} originals; {preservation["reviewed_added_expressions"]} distinct additive mathematical expressions and declared protected relocation verified. Missing witness, corrupted relocated original and altered review rejected. No visual or independent acceptance.'}
    (BASE / ('package-verification-' + suffix + '.json')).write_text(json.dumps(proof, indent=2) + '\n')
    print(json.dumps({'status': 'pass', 'batch': args.batch, 'numerical_groups': len(nm['check_groups']),
                      'temporary': str(temporary), 'proof': proof}, indent=2), flush=True)


if __name__ == '__main__':
    main()

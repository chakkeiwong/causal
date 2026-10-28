"""One bounded recoverable publication step with durable logs and actual exits."""
import argparse
import json
import subprocess
import sys
from pathlib import Path

from publish_latent_r_review_v2_20261013 import ref, write

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-28/fixture-java-publication-v1'
STEPS = {
    'reader-build': ('build_fixture_java_reader_20261028', 'build'),
    'reader-review': ('publish_fixture_java_reader_20261028', 'review'),
    'reader-publish': ('publish_fixture_java_reader_20261028', 'publish'),
    'reader-renew': ('publish_fixture_java_reader_20261028', 'renew'),
    'sponsor-prepare': ('build_fixture_java_sponsor_20261028', 'prepare'),
    'sponsor-build': ('build_fixture_java_sponsor_20261028', 'build'),
    'sponsor-review': ('publish_fixture_java_sponsor_20261028', 'review'),
    'sponsor-publish': ('publish_fixture_java_sponsor_20261028', 'publish'),
    'chapters': ('review_fixture_java_chapters_20261028', None),
    'refresh': ('refresh_fixture_java_program_20261028', None),
    'legacy-check': ('causal_program', 'check'),
    'program-check': ('run_program_checkpoint_v3', 'check'),
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('step', choices=STEPS)
    args = parser.parse_args()
    BASE.mkdir(exist_ok=True)
    script, verb = STEPS[args.step]
    log = BASE / (args.step + '.log')
    receipt = BASE / (args.step + '-exit.json')
    assert not log.exists() and not receipt.exists(), 'Consume existing exit; never repeat a recorded step.'
    unwrapped = args.step.endswith('-check')
    command = [sys.executable]
    if not unwrapped:
        command.append('tools/run_with_review_context_cache_20261025.py')
    command.append('tools/' + script + '.py')
    if verb:
        command.append(verb)
    with log.open('x') as stream:
        result = subprocess.run(command, cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT)
    write(receipt, dict(step=args.step, command=command, actual_exit_code=result.returncode,
          execution='performed', unwrapped=unwrapped,
          evidence=[ref(log, 'Complete performed step output'), ref(ROOT / ('tools/' + script + '.py'), 'Executed tool')]))
    print(json.dumps(dict(step=args.step, actual_exit_code=result.returncode,
                          receipt=str(receipt.relative_to(ROOT)))), flush=True)
    raise SystemExit(result.returncode)


if __name__ == '__main__':
    main()

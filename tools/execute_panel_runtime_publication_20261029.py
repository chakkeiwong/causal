"""One bounded preserving publication step with durable logs and real exits."""
import argparse
import json
import subprocess
import sys
from pathlib import Path

from publish_latent_r_review_v2_20261013 import ref, write

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-29/panel-runtime-publication-v1'
STEPS = {
    'reader-prepare': ('build_panel_runtime_reader_20261029', 'prepare'),
    'reader-build': ('build_panel_runtime_reader_20261029', 'build'),
    'reader-review': ('publish_panel_runtime_reader_20261029', 'review'),
    'reader-publish': ('publish_panel_runtime_reader_20261029', 'publish'),
    'reader-renew': ('publish_panel_runtime_reader_20261029', 'renew'),
    'sponsor-prepare': ('build_panel_runtime_sponsor_20261029', 'prepare'),
    'sponsor-build': ('build_panel_runtime_sponsor_20261029', 'build'),
    'sponsor-review': ('publish_panel_runtime_sponsor_20261029', 'review'),
    'sponsor-publish': ('publish_panel_runtime_sponsor_20261029', 'publish'),
    'chapters': ('review_panel_runtime_chapters_20261029', None),
    'refresh': ('refresh_panel_runtime_program_20261029', None),
    'legacy-check': ('causal_program', 'check'),
    'program-check': ('run_program_checkpoint_v3', 'check'),
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('step', choices=STEPS)
    args = parser.parse_args()
    BASE.mkdir(exist_ok=True)
    module, verb = STEPS[args.step]
    log = BASE / (args.step + '.log')
    receipt = BASE / (args.step + '-exit.json')
    assert not log.exists() and not receipt.exists(), 'Consume recorded step; never repeat it.'
    unwrapped = args.step.endswith('-check')
    command = [sys.executable]
    if not unwrapped:
        command.append('tools/run_with_review_context_cache_20261025.py')
    command.append('tools/' + module + '.py')
    if verb:
        command.append(verb)
    with log.open('x') as stream:
        result = subprocess.run(command, cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT)
    write(receipt, dict(step=args.step, command=command, actual_exit_code=result.returncode, execution='performed', unwrapped=unwrapped,
        evidence=[ref(log, 'Complete performed step output'), ref(ROOT / ('tools/' + module + '.py'), 'Executed tool')]))
    print(json.dumps(dict(step=args.step, actual_exit_code=result.returncode, receipt=str(receipt.relative_to(ROOT)))), flush=True)
    raise SystemExit(result.returncode)


if __name__ == '__main__':
    main()

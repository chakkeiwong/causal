"""Run only unperformed eligible publication steps; stop only on a real failure."""
import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-29/panel-runtime-publication-v1'
STEPS=['reader-publish','reader-renew','sponsor-prepare','sponsor-build','sponsor-review',
       'sponsor-publish','chapters','refresh','legacy-check','program-check']


def main():
    assert json.loads((BASE/'reader-review-exit.json').read_text())['actual_exit_code']==0
    for step in STEPS:
        receipt=BASE/(step+'-exit.json')
        if receipt.exists():
            assert json.loads(receipt.read_text())['actual_exit_code']==0, 'Preserved failed step: '+step
            continue
        result=subprocess.run([sys.executable,'tools/execute_panel_runtime_publication_20261029.py',step],cwd=ROOT)
        if result.returncode:raise SystemExit(result.returncode)
    print('All remaining publication steps completed with consumed actual zero exits.',flush=True)


if __name__=='__main__':main()

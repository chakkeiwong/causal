"""Run the fixed public collector once with bounded durable outcome reporting."""
import json
import subprocess
from pathlib import Path

from prepare_reliableai_nested_review_20261028 import BASE, RAW, ROOT
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write


def main():
    log = BASE / 'fetch.log'
    output = BASE / 'fetch-exit.json'
    assert not log.exists() and not output.exists(), 'Recover existing acquisition; do not overwrite attempts.'
    plan = json.loads((BASE / 'plan-review.json').read_text())
    verify_bindings(plan)
    assert (ROOT / 'docs/literature/fetch-manifest.json').read_bytes() == (BASE / 'proposed-fetch-manifest.json').read_bytes()
    command = [str(ROOT / 'tools/public_sources.py'), 'fetch']
    with log.open('x') as stream:
        result = subprocess.run(command, cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT)
    records = []
    for item in plan['worklist']:
        path = RAW / (item['id'] + '.receipt.json')
        receipt = json.loads(path.read_text()) if path.exists() else {}
        records.append(dict(id=item['id'], status=receipt.get('status', 'missing_receipt'),
                            evidence=ref(path, 'Performed collector request') if path.exists() else None))
    write(output, dict(actual_exit_code=result.returncode, command=command, requests=records,
                       evidence=[ref(log, 'Complete bounded collector output'), ref(BASE / 'plan-review.json', 'Declared sources'), ref(Path(__file__), 'Acquisition wrapper')]))
    print(json.dumps(dict(actual_exit_code=result.returncode, saved=sum(r['status'] == 'saved' for r in records), requests=len(records))), flush=True)
    raise SystemExit(result.returncode)


if __name__ == '__main__':
    main()

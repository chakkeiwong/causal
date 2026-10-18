#!/usr/bin/env python3
"""Fetch one bounded public Ananke wheel as inert primary source, never install it."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-18/python-identification-v1'
META = ROOT / 'docs/literature/raw/v12_sw2_pypi_ananke.json'


def main():
    metadata = json.loads(META.read_text())
    assert metadata['info']['name'] == 'ananke-causal'
    selected = next(f for f in metadata['releases']['0.5.0']
                    if f['filename'] == 'ananke_causal-0.5.0-py3-none-any.whl')
    assert selected['upload_time_iso_8601'] < '2026-10-08'
    url = selected['url']
    assert url.startswith('https://files.pythonhosted.org/packages/')
    assert selected['digests']['sha256'] == '93953b521738117691ddf52e05d72f77b0c5b8f5636486a4481aa1f0db617618'
    BASE.mkdir(parents=True, exist_ok=True)
    target = BASE / selected['filename']
    assert not target.exists() and not (BASE/'acquisition.json').exists()
    args = ['curl', '-fL', '--proto', '=https', '--proto-redir', '=https',
            '--max-time', '25', '--max-filesize', '8388608', '--silent', '--show-error',
            '-D', str(BASE/'ananke.headers'), '-o', str(target), '-w',
            '%{http_code} %{url_effective} %{size_download}\n', url]
    result = subprocess.run(args, text=True, capture_output=True, timeout=30)
    (BASE/'ananke-fetch.log').write_text(result.stdout + result.stderr)
    record = dict(source_identity=url, selected_version='0.5.0',
        declared_upload=selected['upload_time_iso_8601'], cutoff='2026-10-07',
        accessed_utc=datetime.now(timezone.utc).isoformat(), command=args,
        returncode=result.returncode, executed_downloaded_code=False,
        metadata_path=str(META.relative_to(ROOT)),
        metadata_sha256=hashlib.sha256(META.read_bytes()).hexdigest())
    if result.returncode == 0:
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        assert digest == selected['digests']['sha256']
        with zipfile.ZipFile(target) as archive:
            members = archive.infolist()
            assert len(members) < 500 and sum(m.file_size for m in members) < 16*1024*1024
            record.update(status='saved_hash_matches_selected_release',
                path=str(target.relative_to(ROOT)), sha256=digest,
                bytes=target.stat().st_size,
                members=[dict(name=m.filename, bytes=m.file_size) for m in members])
    else:
        record.update(status='failed', error=(result.stdout+result.stderr)[-2000:])
    receipt = BASE/'acquisition.json'
    if result.returncode:
        attempt = len(list(BASE.glob('acquisition-failure-*.json'))) + 1
        receipt = BASE/f'acquisition-failure-{attempt}.json'
        if target.exists():
            target.rename(BASE/f'ananke-incomplete-attempt-{attempt}.whl')
        (BASE/f'ananke-fetch-failure-{attempt}.log').write_text(result.stdout+result.stderr)
    assert not receipt.exists()
    receipt.write_text(json.dumps(record, indent=2)+'\n')
    print(json.dumps({k:record[k] for k in ['status', 'selected_version', 'returncode']}))
    if result.returncode:
        raise SystemExit(result.returncode)


if __name__ == '__main__':
    main()

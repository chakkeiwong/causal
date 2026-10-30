"""Standalone, network-free build of a frozen causal monograph source package.

The packaging tool places this script beside source/ and manifest.json. It has
no checkout dependency and checks every actual compiler input after building.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import subprocess
import time


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--output', type=Path, help='New build directory; never overwrites a previous run')
    args = parser.parse_args()
    package = args.package.resolve()
    manifest = json.loads((package / 'manifest.json').read_text())
    output = args.output.resolve() if args.output else package / 'build'
    output.mkdir(parents=True, exist_ok=False)
    source = package / 'source' / 'docs'
    actual = {str(p.relative_to(package)): sha(p) for p in (package / 'source').rglob('*') if p.is_file()}
    if actual != manifest['source_hashes']:
        raise RuntimeError('Source package differs from frozen manifest')
    environment_mismatch = [name for name, digest in manifest['system_input_hashes'].items()
                            if not Path(name).is_file() or sha(Path(name)) != digest]
    env = {k: v for k, v in os.environ.items()
           if k not in {'TEXINPUTS', 'BIBINPUTS', 'BSTINPUTS', 'TEXMFOUTPUT'}}
    env.update(SOURCE_DATE_EPOCH=manifest['source_date_epoch'], FORCE_SOURCE_DATE='1',
               TZ='UTC', BIBINPUTS=str(source) + '//:', BSTINPUTS=str(source) + '//:')
    report = dict(package_batch=manifest['batch'], environment_mismatch=environment_mismatch,
                  publications={}, scope='Local source and recorded environment reproducibility; no visual or independent acceptance.')

    def run(command, cwd, log):
        start = time.monotonic()
        with log.open('w') as stream:
            p = subprocess.run(command, cwd=cwd, env=env, stdout=stream,
                               stderr=subprocess.STDOUT, timeout=300)
        result = dict(command=command, returncode=p.returncode,
                      seconds=round(time.monotonic() - start, 3), log=str(log))
        print(json.dumps(result), flush=True)
        if p.returncode:
            raise RuntimeError('Compilation failed; inspect ' + str(log))
        return result

    for kind, expected in manifest['publications'].items():
        stem = expected['stem']
        folder = output / kind
        folder.mkdir()
        cmd = ['pdflatex', '-no-shell-escape', '-interaction=nonstopmode', '-halt-on-error',
               '-file-line-error', '-recorder', '-output-directory=' + str(folder), stem + '.tex']
        passes = [run(cmd, source, folder / 'pass-1.txt')]
        if kind == 'full':
            passes.append(run(['bibtex', stem], folder, folder / 'pass-bibtex.txt'))
        for turn in range(2, 6):
            passes.append(run(cmd, source, folder / f'pass-{turn}.txt'))
            log = (folder / (stem + '.log')).read_text(errors='replace')
            if turn >= 3 and not re.search(r'undefined|multiply defined|Label.*changed', log, re.I):
                break
        inputs = set()
        for line in (folder / (stem + '.fls')).read_text().splitlines():
            if line.startswith('INPUT '):
                p = Path(line[6:])
                inputs.add((p if p.is_absolute() else source / p).resolve())
        unexpected = [str(p) for p in inputs if not p.is_relative_to(source)
                      and not p.is_relative_to(output) and str(p) not in manifest['system_input_hashes']]
        system_changed = [str(p) for p in inputs if str(p) in manifest['system_input_hashes']
                          and sha(p) != manifest['system_input_hashes'][str(p)]]
        warnings = {w: len(re.findall(w, log, re.I)) for w in
                    ['undefined', 'multiply defined', 'Overfull', 'Underfull', 'Label.*changed']}
        pdf = folder / (stem + '.pdf')
        report['publications'][kind] = dict(path=str(pdf), sha256=sha(pdf),
                                           expected_sha256=expected['sha256'],
                                           byte_identical=sha(pdf) == expected['sha256'],
                                           unexpected_inputs=unexpected, changed_system_inputs=system_changed,
                                           warnings=warnings, passes=passes)
    after = {str(p.relative_to(package)): sha(p) for p in (package / 'source').rglob('*') if p.is_file()}
    report['source_unchanged'] = after == actual
    report['status'] = 'pass' if (report['source_unchanged'] and not environment_mismatch and
        all(x['byte_identical'] and not x['unexpected_inputs'] and not x['changed_system_inputs']
            and not any(v for k, v in x['warnings'].items() if k != 'Underfull')
            for x in report['publications'].values())) else 'fail'
    (output / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2), flush=True)
    if report['status'] != 'pass':
        raise SystemExit(1)


if __name__ == '__main__':
    main()

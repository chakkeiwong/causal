"""Package the latest audited candidate without modifying source or prior packages."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import platform
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/release/2026-10-29'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--revision', type=int, default=0)
    args = parser.parse_args()
    assert args.revision >= 0
    build = json.loads((BASE / 'latest-build.json').read_text())
    audit = json.loads((BASE / 'deletion-audit.json').read_text())
    trace = json.loads((BASE / 'source-verification.json').read_text())
    assert audit['status'] == 'pass' and audit['checks_after_final_edit']
    assert audit['ledger_sha256'] == build['ledger_sha256'] == sha(BASE / 'edits.json')
    assert trace['status'] == 'pass' and trace['build_batch'] == build['batch']
    assert trace['ledger_sha256'] == build['ledger_sha256']
    assert all(sha(ROOT / p) == digest for p, digest in audit['final_source_hashes'].items())
    suffix = f"batch-{build['batch']:03d}" + (f'-r{args.revision:02d}' if args.revision else '')
    package = BASE / 'packages' / suffix
    package.mkdir(parents=True, exist_ok=False)
    shutil.copytree(BASE / 'source', package / 'source')
    shutil.copy2(ROOT / 'tools/release_portable_build_20261029.py', package / 'build.py')
    shutil.copy2(ROOT / 'tools/release_portable_preservation_20261029.py', package / 'check_preservation.py')
    shutil.copy2(ROOT / 'tools/release_mathematical_review_20261029.py', package / 'math_review.py')
    mapping = json.loads((BASE / 'source-map.json').read_text())
    additions = json.loads((BASE / 'additions.json').read_text())
    for row in list(mapping.values()) + additions:
        original = ROOT / row['original']
        assert sha(original) == row['sha256'], row['original']
        target = package / 'preserved' / row['original']
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            shutil.copy2(original, target)
    evidence = package / 'evidence'
    evidence.mkdir()
    names = ['edits.json', 'source-map.json', 'additions.json', 'full-deletion-ledger.md',
             'deletion-audit.json', 'source-verification.json', 'numerical-verification.json',
             'commercial-context-reinspection.json', 'discovery-integration-verification.json']
    for name in names:
        shutil.copy2(BASE / name, evidence / name)
    for name in ['supplemental-source-support.json', 'changed-context-review.json',
                 'changed-context-review.md', 'release-final-review.json', 'release-final-review.md',
                 'remaining-inventory.json', 'review-scope-current.json', 'review-scope-current.md',
                 'mathematical-addition-reviews.json', 'protected-relocations.json']:
        if (BASE / name).is_file():
            shutil.copy2(BASE / name, evidence / name)
    for pattern in ['local-context-review-*.json', 'rendered-context-batch*.json']:
        for path in BASE.glob(pattern):
            shutil.copy2(path, evidence / path.name)
    for path in sorted(BASE.glob('source-*/source-audit.json')):
        destination = evidence / path.parent.name
        destination.mkdir(exist_ok=True)
        shutil.copy2(path, destination / path.name)
        witness = path.parent / 'exact-witnesses.json'
        if witness.exists():
            shutil.copy2(witness, destination / witness.name)
    # Review bindings, rather than directory naming, define required evidence.
    reviews = json.loads((BASE / 'mathematical-addition-reviews.json').read_text())['reviews']
    for review in reviews:
        for field in ['witness', 'source_audit']:
            row = review[field]
            source = ROOT / row['path']
            assert source.resolve().is_relative_to(BASE.resolve())
            assert sha(source) == row['sha256'], row['path']
            destination = evidence / source.relative_to(BASE)
            destination.parent.mkdir(parents=True, exist_ok=True)
            if destination.exists():
                assert sha(destination) == row['sha256'], row['path']
            else:
                shutil.copy2(source, destination)
    # Retain actual bytes behind the exceptional protected-path reconciliation,
    # together with its review; copying the registry alone is insufficient.
    relocation = BASE / 'protected-relocations.json'
    if relocation.exists():
        for row in json.loads(relocation.read_text())['relocations']:
            for name, digest in [(row['preserved'], row['expected_sha256']),
                                 (row['review_record']['path'], row['review_record']['sha256'])]:
                source = ROOT / name
                assert source.resolve().is_relative_to(BASE.resolve())
                assert sha(source) == digest
                destination = evidence / source.relative_to(BASE)
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)
    for pattern in ['source-*/integration-map.json', 'source-*/formulation-original.tex']:
        for source in BASE.glob(pattern):
            destination = evidence / source.relative_to(BASE)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
    # Bundle exact author-review records and extracts, not just their paths.
    # Do not follow primary-source references into third-party collections.
    review_index = {}
    def retain_review(name, digest):
        source = ROOT / name
        assert source.is_file() and sha(source) == digest, name
        if source.resolve().is_relative_to(BASE.resolve()):
            relative = source.relative_to(BASE)
            assert relative.parts[0] != 'source', name
        else:
            assert source.resolve().is_relative_to((ROOT / 'docs/writing-repair/2026-10-29').resolve()), name
            relative = Path('baseline-review') / source.relative_to(ROOT)
        destination = evidence / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            assert sha(destination) == digest, name
        else:
            shutil.copy2(source, destination)
        review_index[name] = {'path': str(destination.relative_to(package)), 'sha256': digest}
    review_scope = json.loads((BASE / 'review-scope-current.json').read_text())
    assert review_scope['batch'] == build['batch']
    for name, digest in review_scope['basis'].items():
        retain_review(name, digest)
    baseline_review = json.loads((BASE / 'baseline-whole-book-review.json').read_text())
    for name, digest in baseline_review['review_files'].items():
        retain_review(name, digest)
    contexts = json.loads((BASE / 'changed-context-review.json').read_text())
    for row in contexts['reviews']:
        retain_review(row['extract'], row['extract_sha256'])
    currency = json.loads((BASE / 'review-currency-current.json').read_text())
    assert currency['status'] == 'pass' and currency['batch'] == build['batch']
    assert currency['ledger_sha256'] == build['ledger_sha256']
    assert currency['expanded_manuscript_matches'] and not currency['issues']
    retain_review(str((BASE / 'review-currency-current.json').relative_to(ROOT)),
                  sha(BASE / 'review-currency-current.json'))
    for name, digest in currency['basis'].items():
        retain_review(name, digest)
    for name in review_scope['basis']:
        if Path(name).name != 'contextual-review.json':
            continue
        record = json.loads((ROOT / name).read_text())
        for field in ['final_context_snapshot', 'rendered_text', 'numerics']:
            row = record.get(field)
            if isinstance(row, dict) and 'path' in row and 'sha256' in row:
                retain_review(row['path'], row['sha256'])
    (evidence / 'author-review-index.json').write_text(json.dumps({
        'scope': 'Exact author-review records, reviewed context extracts and explicitly bound rendered/numerical receipts; not independent or fresh visual acceptance.',
        'full_context_records': len(contexts['reviews']),
        'current_numbered_chapters': currency['numbered_chapters'],
        'current_source_segments': currency['source_segments_checked'],
        'review_currency': 'evidence/review-currency-current.json',
        'files': review_index,
    }, indent=2) + '\n')
    pdfdir = package / 'pdf'
    pdfdir.mkdir()
    system = {}
    publications = {}
    d = BASE / 'source/docs'
    for kind, row in build['publications'].items():
        pdf = ROOT / row['path']
        assert sha(pdf) == row['sha256'] == audit['publication'][kind]['sha256']
        shutil.copy2(pdf, pdfdir / pdf.name)
        publications[kind] = dict(stem=row['stem'], path='pdf/' + pdf.name, sha256=row['sha256'],
                                   pages=audit['publication'][kind]['pages'])
        folder = ROOT / row['folder']
        for line in (folder / (row['stem'] + '.fls')).read_text().splitlines():
            if line.startswith('INPUT '):
                p = Path(line[6:])
                p = (p if p.is_absolute() else d / p).resolve()
                if not p.is_relative_to(d) and not p.is_relative_to(folder):
                    assert str(p).startswith(('/usr/share/texlive/', '/usr/share/texmf/',
                                              '/var/lib/texmf/', '/etc/texmf/')), str(p)
                    system[str(p)] = sha(p)
        logs = evidence / ('build-' + kind)
        logs.mkdir()
        for name in [row['stem'] + '.log', row['stem'] + '.fls', 'passes.json']:
            shutil.copy2(folder / name, logs / name)
    manifest = dict(schema_version=1, batch=build['batch'], package_revision=args.revision, source_date_epoch='1793285915',
        publications=publications, ledger_sha256=build['ledger_sha256'],
        source_hashes={str(p.relative_to(package)): sha(p) for p in (package / 'source').rglob('*') if p.is_file()},
        preserved_source_hashes={str(p.relative_to(package)): sha(p) for p in (package / 'preserved').rglob('*') if p.is_file()},
        evidence_hashes={str(p.relative_to(package)): sha(p) for p in evidence.rglob('*') if p.is_file()},
        verifier_hashes={name: sha(package / name) for name in ['build.py', 'check_preservation.py', 'math_review.py']},
        system_input_hashes=system, environment={'python': platform.python_version(),
            'platform': platform.platform(), 'pdflatex': subprocess.check_output(['pdflatex', '--version'], text=True).splitlines()[0],
            'bibtex': subprocess.check_output(['bibtex', '--version'], text=True).splitlines()[0]},
        release_accepted=False, fresh_visual_acceptance=False, independent_acceptance=False,
        evidence_scope='Source and numerical audit navigation; external papers, vendor code, bank data and native engines are not bundled.')
    (package / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    frozen_date = datetime.now(timezone.utc).strftime('%d %B %Y')
    figure_count = sum(name.endswith('.pdf') for name in manifest['source_hashes'])
    (package / 'README.md').write_text(f'''# Causal banking monograph: reproducible candidate package

Frozen from verified batch {build['batch']:03d} on {frozen_date} UTC. This is a release
candidate, not a record of independent acceptance or bank qualification. The
reader has {publications['full']['pages']:,} pages; the aligned sponsor has
{publications['sponsor']['pages']} pages. The literature cutoff is 7 October 2026;
individual later retrievals retain their recorded coverage limits.

## Build

Prerequisites: Python 3, pdfLaTeX, BibTeX and the TeX packages/fonts recorded in
manifest.json. No network requests or downloaded executable dependencies occur.
Run from any directory with this extracted folder intact:

    python3 /absolute/path/to/package/build.py --output /absolute/path/to/new-build

The output directory must not exist. The script verifies all {len(manifest['source_hashes'])} source files,
compiles both documents with shell escape disabled, records actual compiler
inputs, checks warnings and compares both PDF hashes with this candidate.
It records changed or missing system inputs instead of silently claiming
cross-platform reproducibility. The exact system packages and fonts may be
needed for byte identity. The audit does not certify visual readability.

## Read and audit

pdf/ contains the candidate and sponsor. source/ contains all manuscript text,
bibliography, {figure_count} figure PDFs and two inherited bibliography-style files.
Their existing copyright and licence notices remain intact. This local review
package makes no new grant of rights over third-party material.

evidence/full-deletion-ledger.md records each exact replacement and substantive
destination. evidence/deletion-audit.json binds the unchanged baseline, compiled
input order, mathematics, labels, citation keys and final candidate sources.
The preserved/ tree contains the exact release-stage baseline and declared
additions, so the reader can replay every replacement outside the checkout:

    python3 /absolute/path/to/package/check_preservation.py --output /path/to/new-audit

This checks exact before/after anchors and final bytes for every source. It
also verifies the packaged mathematical-addition reviews and their bound
witness/audit identities, disallows mathematical removal, and checks the
archived original behind the declared protected-inventory relocation. It
retains each reason and substantive destination for editorial assessment. The
earlier 505-edit baseline remains a separately scoped historical review; this
runner does not pretend to redo that earlier rewrite or judge scientific prose.

evidence/source-verification.json maps every citation to inspected original
anchors, supported claims, version/date and local hashes. Its repository-relative
original-source paths refer to the retained research workspace; genuine papers
and vendor documents are not redistributed in this build-only package. Numerical
receipts identify retained input data and independently reconstructed results;
the underlying research data/code remain in that same workspace. The separate
numerical reconstruction package declares its retained arithmetic groups and
requires five hash-checked external inputs through separate intake: two public
experimental subsets and three saved benchmark tables. A manuscript
build alone does not rerun or independently validate those studies.

Visual inspection of these exact candidate bytes and actual independent
editorial findings remain outstanding. No native vendor run, live language-model
benefit, bank-data validation or adoption is asserted by this package.
''')
    files = {str(p.relative_to(package)): sha(p) for p in package.rglob('*') if p.is_file()}
    (package / 'SHA256SUMS').write_text(''.join(digest + '  ' + name + '\n' for name, digest in sorted(files.items())))
    receipt = dict(batch=build['batch'], package=str(package.relative_to(ROOT)), files=len(files),
                   source_files=len(manifest['source_hashes']), source_bytes=sum(p.stat().st_size for p in (package / 'source').rglob('*') if p.is_file()),
                   manifest_sha256=sha(package / 'manifest.json'), checksum_file_sha256=sha(package / 'SHA256SUMS'),
                   relocation_test='pending', release_accepted=False)
    (BASE / f"package-{suffix}.json").write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()

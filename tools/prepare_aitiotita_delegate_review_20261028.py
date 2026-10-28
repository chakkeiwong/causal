"""Register exact, previously omitted Java delegates for bounded source inspection."""
import json
from pathlib import Path

from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-28/aitiotita-delegates-v1'
RAW = ROOT / 'docs/literature/raw'
PIN = '8a8e566a87186de4935e644cec0fa80e6d456fd7'
PATHS = [
    'src/main/java/de/tuebingen/sfs/causal/heuristics/separation/PartialCorrelation.java',
    'src/main/java/de/tuebingen/sfs/causal/heuristics/separation/PartialCorrelationDiscreteUnitFlow.java',
    'src/main/java/de/tuebingen/sfs/causal/heuristics/arrows/CausalArrowFinderPcDefault.java',
    'src/main/java/de/tuebingen/sfs/causal/heuristics/arrows/OrientationRules.java',
    'src/main/java/de/tuebingen/sfs/causal/data/CausalGraph.java',
    'src/test/java/de/tuebingen/sfs/AitiotitaTest.java',
    'src/main/java/de/tuebingen/sfs/Aitiotita.java',
]


def main():
    assert not BASE.exists()
    tree = json.loads((RAW / 'v12_exec13_java_aitiotita_tree.json').read_text())
    commits = json.loads((RAW / 'v12_exec13_java_aitiotita_commit.json').read_text())
    commit = commits[0] if isinstance(commits, list) else commits
    assert commit['sha'] == PIN and commit['commit']['committer']['date'] <= '2026-10-07T15:59:59Z'
    assert tree['truncated'] is False
    blobs = {item['path']: item for item in tree['tree'] if item['type'] == 'blob'}
    assert all(path in blobs for path in PATHS)
    BASE.mkdir()
    manifest = ROOT / 'docs/literature/fetch-manifest.json'
    (BASE / 'prior-fetch-manifest.json').write_bytes(manifest.read_bytes())
    items = [dict(id=f'exec28_aitiotita_delegate_{index}', extension='txt',
                  url=f'https://raw.githubusercontent.com/jdellert/aitiotita/{PIN}/{path}')
             for index, path in enumerate(PATHS)]
    proposal = dict(status='reviewed_bounded_acquisition', requests=items, cutoff='2026-10-07',
                    scope='Seven exact omitted Aitiotita delegates; public GETs only, no code execution')
    write(BASE / 'proposed-fetch-manifest.json', proposal)
    worklist = [dict(id=item['id'], upstream_path=path, expected_git_blob=blobs[path]['sha'],
                     expected_bytes=blobs[path].get('size'), url=item['url'])
                for item, path in zip(items, PATHS, strict=True)]
    evidence = [ref(RAW / n, 'Existing cutoff identity or source boundary') for n in
                ('v12_exec13_java_aitiotita_commit.json', 'v12_exec13_java_aitiotita_tree.json',
                 'v12_exec13_java_aitiotita_pc.txt', 'v12_exec13_java_aitiotita_license.txt')]
    evidence += [ref(ROOT / 'docs/program/execution/2026-10-13/java-discovery/omissions-register.json', 'JAVA03 delegate gap'),
                 ref(BASE / 'proposed-fetch-manifest.json', 'Bounded source acquisition'),
                 ref(Path(__file__), 'Exact manifest preparation')]
    write(BASE / 'plan-review.json', dict(
        status='pass_for_static_review', cutoff='2026-10-07', commit=PIN,
        worklist=worklist, evidence=evidence,
        steps=['Acquire the seven registered files through the fixed public collector.',
               'Verify exact Git blobs and inspect line-numbered primary text.',
               'Trace separation, orientation, graph mutation and actual test scope.',
               'Compare the old conditioning witness with the actual declared oracle interface.',
               'Record conditional adoption/porting choices and uninspected dependencies.'],
        boundaries=['No Java build or downloaded code execution.',
                    'The Gaussian witness tests the generic algorithm shortcut; it need not match the bundled discrete oracle.',
                    'Reading test bodies does not prove broad correctness or run the tests.',
                    'This finite review cannot establish full Java census, complete rights or bank validity.'],
        acceptance=['All acquired bytes match the pinned tree or have a precise local failure disposition.',
                    'Technical statements use inspected anchors and separate generic and bundled-oracle domains.'],
        awards_acceptance=False))
    verify_bindings(json.loads((BASE / 'plan-review.json').read_text()))
    manifest.write_bytes((BASE / 'proposed-fetch-manifest.json').read_bytes())
    print(json.dumps(dict(prepared=str(BASE.relative_to(ROOT)), requests=len(items),
                          next_action='Run fixed collector; inspect verified delegates without executing them.')))


if __name__ == '__main__':
    main()

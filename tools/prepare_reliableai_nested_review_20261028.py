"""Register a bounded nested-engine review against the saved cutoff tree."""
import json
from pathlib import Path

from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-28/reliableai-nested-v1'
RAW = ROOT / 'docs/literature/raw'
PIN = '42dea82a5d13a989d08983a08527ed982776bccf'
PATHS = [
    'LICENSE',
    'causal-kit/Spot/LICENSE',
    'causal-kit/Spot/README.md',
    'causal-kit/Spot/requirements.txt',
    'causal-kit/Spot/utils/convertMag2Pag.java',
    'causal-kit/Spot/utils/convertPag2Mag.java',
    'causal-kit/Spot/utils/setup_tetrad.sh',
    'causal-kit/Spot/utils/graph.py',
    'causal-kit/Spot/baselines/fci.py',
    'causal-kit/Spot/learn/bootstrap.py',
    'causal-kit/TICL/baselines/blip/LICENSE',
    'causal-kit/TICL/baselines/blip/README.md',
    'causal-kit/TICL/baselines/blip/api/pom.xml',
    'causal-kit/TICL/baselines/blip/core/pom.xml',
    'causal-kit/TICL/baselines/blip/api/src/main/java/ch/idsia/blip/api/Blip.java',
    'causal-kit/TICL/baselines/blip/core/src/main/java/ch/idsia/blip/core/utils/score/BDeu.java',
    'causal-kit/TICL/baselines/blip/core/src/main/java/ch/idsia/blip/core/learn/solver/BaseSolver.java',
    'causal-kit/TICL/baselines/blip/core/src/main/java/ch/idsia/blip/core/learn/solver/brtl/BrutalSolver.java',
    'causal-kit/TICL/baselines/blip/api/src/test/java/ch/idsia/blip/api/learn/solver/SolverTest.java',
    'causal-kit/TICL/baselines/blip/core/src/test/java/ch/idsia/blip/core/utils/score/BDeuTest.java',
]


def main():
    assert not BASE.exists()
    tree = json.loads((RAW / 'v12_exec13_java_reliableai_tree.json').read_text())
    commits = json.loads((RAW / 'v12_exec13_java_reliableai_commit.json').read_text())
    commit = commits[0] if isinstance(commits, list) else commits
    assert tree['sha'] == commit['sha'] == PIN and tree['truncated'] is False
    assert commit['commit']['committer']['date'] <= '2026-10-07T15:59:59Z'
    blobs = {x['path']: x for x in tree['tree'] if x['type'] == 'blob'}
    assert all(p in blobs for p in PATHS)
    assert sum(blobs[p]['size'] for p in PATHS) == 77700
    BASE.mkdir()
    manifest = ROOT / 'docs/literature/fetch-manifest.json'
    (BASE / 'prior-fetch-manifest.json').write_bytes(manifest.read_bytes())
    requests = [dict(id=f'exec28_nested_{i:02}', extension='txt', url=f'https://raw.githubusercontent.com/microsoft/reliableAI/{PIN}/{p}') for i, p in enumerate(PATHS)]
    write(BASE / 'proposed-fetch-manifest.json', dict(status='reviewed_bounded_acquisition', requests=requests, cutoff='2026-10-07', scope='20 selected pinned nested-engine text originals; public HTTPS GET only'))
    worklist = [dict(id=item['id'], upstream_path=p, expected_git_blob=blobs[p]['sha'], expected_bytes=blobs[p]['size'], url=item['url']) for item, p in zip(requests, PATHS, strict=True)]
    evidence = [ref(RAW / n, 'Saved cutoff navigation identity') for n in ('v12_exec13_java_reliableai_commit.json', 'v12_exec13_java_reliableai_tree.json', 'v12_exec13_java_reliableai_readme.txt')]
    evidence += [ref(ROOT / 'docs/program/execution/2026-10-28/software-tail-java-panel-delta-v1/source-tail-delta.json', 'Reconciled JAVA04 route'), ref(BASE / 'proposed-fetch-manifest.json', 'Bounded requests'), ref(Path(__file__), 'Reviewed preparation')]
    write(BASE / 'plan-review.json', dict(status='pass_for_bounded_static_review', commit=PIN, version_date=commit['commit']['committer']['date'], cutoff='2026-10-07', worklist=worklist, evidence=evidence,
        steps=['Acquire only registered text originals and verify bytes, SHA-256 and exact Git blobs.',
               'Inspect root and nested license declarations separately; record origin and artifact limits.',
               'Trace selected Spot Java graph conversion, shell boundary and FCI/bootstrap paths.',
               'Trace selected BLIP score/search entrypoints and actual test bodies; distinguish score optimization from causal identification.',
               'Write banking reuse/port/refusal decisions with anchored claims and uninspected delegates.',
               'Integrate reviewed source findings in paired proposal documents, retain predecessor citations and verify the result.'],
        acceptance=['Every selected original has verified identity and inspected primary anchors or a precise local omission.',
                    'Claims distinguish upstream technical behavior, authored deductions and unexecuted native behavior; root license does not grant blanket dependency rights.',
                    'Bounded decisions and residual tails are explicit without claiming complete Java census or acceptance.'],
        boundaries=['No downloaded source, setup shell, Java, JAR or imported engine execution.',
                    'No scholarly paper is cited from README metadata without its genuine local PDF.',
                    'Selected files do not establish origin/derivative equivalence or compiled artifact equality.',
                    'This branch does not block other source tails, manuscript or public fixture work.'], awards_acceptance=False))
    verify_bindings(json.loads((BASE / 'plan-review.json').read_text()))
    manifest.write_bytes((BASE / 'proposed-fetch-manifest.json').read_bytes())
    print(json.dumps(dict(prepared=str(BASE.relative_to(ROOT)), requests=len(requests), selected_bytes=77700, native_execution=False)))


if __name__ == '__main__':
    main()

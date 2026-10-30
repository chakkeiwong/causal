"""Keep a separately verified scientific delivery visible after editorial refresh."""
from pathlib import Path
import hashlib
import json
import os
import re

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- scientific-delivery:start -->'
END = '<!-- scientific-delivery:end -->'

def refresh():
    state = json.loads((ROOT/'docs/program/scientific-priorities.json').read_text())
    delivery = state.get('discovery_scientific_delivery')
    if not delivery:
        return []
    full = delivery['integrated_successor']; short = delivery['short_reading']
    for pub in [full, short]:
        actual = hashlib.sha256((ROOT/pub['path']).read_bytes()).hexdigest()
        assert actual == pub['sha256'], 'Scientific PDF changed; review before linking.'
    updated = []
    for name in ['CURRENT.md','docs/mission-control.md','docs/program/master-live.md',
                 'docs/program/master-current.md','docs/program/execution/current-program.md']:
        path = ROOT/name
        if not path.is_file():
            continue
        before = path.read_text()
        content = re.sub(re.escape(START)+r'.*?'+re.escape(END)+r'\n*','',before,flags=re.S)
        old_heading = '# Scientific continuation delivered: 29 October 2026\n\n'
        if content.startswith(old_heading):
            next_heading = content.find('\n# ',len(old_heading))
            assert next_heading != -1
            content = content[next_heading+1:]
        def relative(target):return Path(os.path.relpath(ROOT/target,path.parent)).as_posix()
        block = (START+'\n## Scientific continuation: 29 October 2026\n\n'
          f"[Integrated scientific successor]({relative(full['path'])}) · "
          f"[Six-page study]({relative(short['path'])}) · "
          f"[Evidence and remaining work]({relative(delivery['record'])}).\n\n"
          'The search repair recovered all 1,381 reference skeletons in the declared exact-oracle suite; '
          'the screened candidate failed on 49. The result is Chapter 21 of a preserved 1,858-page '
          'scientific successor. The live editorial reader above is separately maintained. '
          'Native package qualification, finite-sample calibration and bank validation remain open.\n'+END+'\n')
        after = content.rstrip()+'\n\n'+block
        if after != before:
            assert path.read_text() == before, 'Concurrent dashboard change; retry from current state.'
            path.write_text(after)
            updated.append(name)
    return updated

if __name__ == '__main__':
    print(json.dumps({'scientific_delivery_links_updated':refresh()}))

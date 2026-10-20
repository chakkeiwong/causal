"""Preserve the failed Java sponsor and prepare a corrected successor."""
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]
p = root/'docs/program/execution/2026-10-20/sponsor-java-effects-v1'
a = json.loads((p/'source-audit.json').read_text())
keys = {s['integrated_citation_key'] for s in a['sources']}
delta = root/'docs/program/execution/2026-10-20/java-effects-v1/source-audit.json'
required = {s['integrated_citation_key'] for s in json.loads(delta.read_text())['sources']}
assert required.isdisjoint(keys)
(p/'failed-review.json').write_text(json.dumps(dict(status='fail',
    reason='Bare citep groups lack LaTeX backslashes; three required citations missing',
    missing=sorted(required), published=False,
    next_action='Build v2 with corrected syntax and exact citation delta'), indent=2)+'\n')
s = (root/'tools/build_java_effects_sponsor_20261020.py').read_text()
s = s.replace('sponsor-java-effects-v1', 'sponsor-java-effects-v2')
s = s.replace('sponsor_proposal_java_effects_reviewed_2026', 'sponsor_proposal_java_effects_reviewed_v2_2026')
old = "return text.replace(marker,(reader.BASE/'sponsor-addition.md').read_text()+chr(10)+marker)"
new = "addition=(reader.BASE/'sponsor-addition.md').read_text().replace(' citep{',' '+chr(92)+'citep{')\n    assert ' citep{' not in addition\n    return text.replace(marker,addition+chr(10)+marker)"
assert old in s
s = s.replace(old, new)
s = s.replace('assert len(sources) > prior_count', "assert len(sources) == prior_count + len(read(reader.BASE/'source-audit.json')['sources']) + 2")
(root/'tools/build_java_effects_sponsor_v2_20261020.py').write_text(s)
s = (root/'tools/review_publish_java_effects_sponsor_20261020.py').read_text()
s = s.replace('import build_java_effects_sponsor_20261020', 'import build_java_effects_sponsor_v2_20261020')
(root/'tools/review_publish_java_effects_sponsor_v2_20261020.py').write_text(s)
print('Preserved failed v1; created strict v2 builder and publisher.')

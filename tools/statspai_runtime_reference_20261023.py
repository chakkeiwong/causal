#!/usr/bin/env python3
"""Static AST/data witnesses, never importing or running downloaded code."""
import ast,json,hashlib
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];RAW=ROOT/'docs/literature/raw'
def calculate():
 p=RAW/'exec23_statspai_runtime_7.txt';tree=ast.parse(p.read_text())
 node=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='_SCRIPT' for x in n.targets))
 template=ast.literal_eval(node.value)
 assert 'checked = 0' in template and 'reproduced:' in template
 assert '"std_error" in EXPECTED' not in template and '"n_obs" in EXPECTED' not in template
 assert '"estimate" in EXPECTED and hasattr(result, "estimate")' in template
 assert 'EXPECTED.get("coefficients"' in template and 'checked > 0' not in template
 source=ast.parse((RAW/'exec23_statspai_runtime_6.txt').read_text());cls=next(n for n in source.body if isinstance(n,ast.ClassDef) and n.name=='ResultCache');put=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='put')
 guard=[ast.unparse(n.test) for n in ast.walk(put) if isinstance(n,ast.While) and '_total_bytes' in ast.unparse(n.test)]
 assert len(guard)==1 and 'len(self._store) > 1' in guard[0]
 # Independent mathematical example of the inspected eviction guard, not a native cache trial.
 sizes=[12];budget=10
 while sum(sizes)>budget and len(sizes)>1:sizes.pop(0)
 assert sum(sizes)==12
 a,b=b'x,y\n1,2\n',b'x,y\n3,4\n';assert len(a)==len(b) and hashlib.sha256(a).digest()!=hashlib.sha256(b).digest()
 return dict(kind='project_static_reference_not_native_trial',
  replay_template_sha256=hashlib.sha256(template.encode()).hexdigest(),
  replay_template_checks=['estimate when expected and result attribute exists','coefficient point estimates'],
  replay_template_does_not_compare=['std_error','n_obs','confidence interval','covariance','diagnostics'],
  permits_zero_checked_success_text=True,cache_eviction_guard=guard[0],
  independent_single_entry_example=dict(budget_units=10,retained_units=12,hard_bound_satisfied=False),
  independent_same_metadata_example=dict(equal_length=len(a),different_hashes=True,metadata_can_be_equal=True,claim='A path/mtime/size key alone is not a content identity; no filesystem manipulation or upstream runtime occurred.'),
  stipulated_retry_economics=dict(benefit_usd=10,attempt_cost_usd=7,one_attempt_net_usd=3,two_attempt_net_usd=-4,assumption='Same one benefit; duplicate attempts both charged; invented illustration only.'),
  downloaded_code_executed=False,native_qualification=False)
if __name__=='__main__':print(json.dumps(calculate(),indent=2))

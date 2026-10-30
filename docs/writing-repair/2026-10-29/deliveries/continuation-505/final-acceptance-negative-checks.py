from pathlib import Path
import copy, hashlib, json, sys
R=Path('/home/ubuntu/workspace/causal');B=R/'docs/writing-repair/2026-10-29';prefix='docs/writing-repair/2026-10-29/'
sys.path.insert(0,str(R/'tools'))
from scientific_program import whole_book_issues, writing_issues
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
a=json.loads((B/'deletion-audit.json').read_text());chapters=json.loads((B/'chapter-review.json').read_text())['chapters'];receipt_name=prefix+'whole-book-review.json';receipt=json.loads((R/receipt_name).read_text())
assert not whole_book_issues(a,chapters)
base_digests={name:sha(R/name) for name in set(receipt['final_source_hashes'])|set(receipt['review_files'])|{prefix+'edits.json'}|{p['path'] for p in receipt['publication'].values()}}
json_values={receipt_name:receipt,prefix+f"rendered-continuation-{a['edits']}.json":json.loads((B/f"rendered-continuation-{a['edits']}.json").read_text())}
results=[]
def check(name,expected,mutate=None,missing=None,drift=None,pending=False,audit_change=None):
 values=copy.deepcopy(json_values);digests=dict(base_digests);rows=copy.deepcopy(chapters);audit=copy.deepcopy(a)
 if mutate:mutate(values[receipt_name],values)
 if drift:digests[drift]='0'*64
 if pending:rows[-1]['full_chapter_acceptance']=False
 if audit_change:audit_change(audit)
 def read(path):
  if path==missing:raise FileNotFoundError(path)
  return values[path]
 issues=whole_book_issues(audit,rows,read_json=read,digest_file=lambda path:digests[path])
 passed=any(expected in issue for issue in issues)
 results.append({'case':name,'expected_rejection':expected,'issues':issues,'pass':passed})
check('missing final review receipt','cannot be verified',missing=receipt_name)
check('receipt from an earlier edit ledger','predates the current edit ledger',mutate=lambda r,v:r.update(ledger_sha256='0'*64))
check('changed manuscript after author review','reviewed source changed',drift='docs/causal_banking_integrated_argument_2026-10-29.tex')
check('changed successor bibliography style','reviewed source changed',drift=prefix+'causalplainnat-reading.bst')
check('changed sponsor body','reviewed source changed',drift=prefix+'sponsor-body.tex')
check('changed bibliography source','reviewed source changed',drift=prefix+'references-0.bib')
check('changed independent supporting review file','supporting review changed',drift=prefix+'whole-book-review.md')
check('changed delivered PDF','reviewed PDF changed',drift=a['publication']['full']['path'])
check('receipt omits supporting review','omits required final review evidence',mutate=lambda r,v:r['review_files'].pop(prefix+'contextual-review-records.json'))
check('receipt omits citation style','omits the successor citation-style identity',mutate=lambda r,v:r['final_source_hashes'].pop(prefix+'causalplainnat-reading.bst'))
check('rendered inspection belongs to earlier edition','rendered-text inspection refers to another edition',mutate=lambda r,v:v[prefix+f"rendered-continuation-{a['edits']}.json"].update(edits=474))
check('unread chapter under completed W08','lacks complete contextual chapter coverage',pending=True)
check('publication disagrees with final audit','publication receipt differs',mutate=lambda r,v:r['publication']['sponsor'].update(sha256='0'*64))
state=json.loads((R/'docs/program/scientific-priorities.json').read_text());assert not writing_issues(state)
for key in ['proposal_complete','gap_closure_finalized','final_editorial_acceptance']:
 candidate=copy.deepcopy(state);candidate[key]=True;issues=writing_issues(candidate)
 results.append({'case':'unearned '+key,'issues':issues,'pass':any('Programme completion contradicts' in i for i in issues)})
report={'scope':'In-memory changed/missing evidence; live programme and manuscripts remain untouched. Valid current records pass; stale or overclaimed records must fail.','valid_current_receipt':True,'checks':results,'pass':all(x['pass'] for x in results),'current_ledger_sha256':a['ledger_sha256'],'checker_sha256':sha(R/'tools/scientific_program.py')}
(B/'final-acceptance-negative-checks.json').write_text(json.dumps(report,indent=2)+chr(10))
print(json.dumps({'pass':report['pass'],'cases':len(results),'failed':[x for x in results if not x['pass']]}))
assert report['pass']

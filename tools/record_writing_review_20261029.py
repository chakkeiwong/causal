"""Record honest contextual coverage, preserving unreviewed chapters as executable work."""
from pathlib import Path
import json,re,hashlib
R=Path(__file__).resolve().parents[1];D=R/'docs';O=D/'writing-repair/2026-10-29';M=json.loads((O/'source-map.json').read_text());reverse={v:k for k,v in M.items()}
rows=[];number=0
full_suffix=['/banking-decision.tex','/public-study.tex','/journeys.tex','/s_c46c4d6cc7751a.tex','/s_55f02779b54808.tex','/servicing.tex','/policy-uncertainty.tex','/funding.tex','/observation.tex','/software-decisions.tex','/decision-synthesis.tex','/practical-investment.tex']
partial_suffix=['/public-study.tex','/s_97e18b4378e863.tex','/s_7a1bc5db6dafe0.tex','/s_577cf7bfe01094.tex','/s_075429285ad5c6.tex','/s_84f3849de7d66f.tex','/s_866a36af07dddf.tex','/s_1aff5098b69c18.tex','/s_b282fa4619d36e.tex','/s_4fdddc32eaa4a4.tex']
notes={
'rewrite:deposit':'Assignment/receipt/acceptance/price and affine expense map retained; normal cellwise interval conditions explicit; interface boundary and funding/public evidence links repaired.',
'rewrite:servicing':'Two-contact pounds example distinguished from three-decision reward units; linked selection, whole-customer bootstrap and dropout failures.',
'rewrite:discovery':'Three observationally equivalent models retain opposite net values; restricted temporal region gives an inferential continuation without a fictitious general pipeline.',
'rewrite:observation':'Known receipt matrix separated from fitted record linkage; external corruption budget and sampling support made explicit.',
'r3:graphs':'Full primary chapter read. Clarified ninety-day voluntary activation versus opening annual automatic repricing. Identification, front-door, ID/IDC, counterexamples and mediation distinctions retained.',
'r3:instruments':'Full primary chapter read. Linear IV, LATE, weak/invalid instruments, AR inversion, control rank and NPIV remain developed and distinct. No edit needed.',
'scisyn:software':'Developed seventeen-area comparison read and command-heavy paragraphs revised. Selection, commercial update, target example and omissions consolidated. Source-specific deeper chapters remain separate review obligations.',
'rewrite:assistance-tasks':'Task comparison, ORCA qualifications, Gaussian measurement example, shared-error limit and frontier critique integrated in evidential order; current census corrected.',
'rewrite:investment-decision':'Annual benefit, multi-year cost account, EVSI and reversal conditions integrated. Numerical assumptions and distinctions from actual bank value retained.',
'gap29:servicing':'Initial denominator, support, observation law, supplied reward and reference uncertainty inspected; moved beside longitudinal foundations.',
'gap29:policy-uncertainty':'Selected-policy conditioning, training/evaluation split, bootstrap unit, 6% failure and model omissions inspected; no numerical changes.',
'gap29:funding':'Within effects do not repair identity; all denominator/variance failures retained; moved beside panel foundation.',
'gap29:observation':'Candidate inclusion and K-budget bound, support enlargement, MC uncertainty and 119.1 width inspected; no mathematical change.',
'scisyn:investment':'Four interface cases, timeout, retry and reproduction commands retained; duplicate economic recommendation replaced by current investment reference.',
'scisyn:evidence':'Generated target-error, sparse-support and UCI evidence retained; detailed retained experiment exposition not fully reread in this pass.',
'rewrite:evidence-consequences':'Existing and new evidence connected to design choices; no additional experiment claimed.'}
# Traverse actual TeX in occurrence order, including in-driver chapter declarations.
token=re.compile(r'\\input\{([^}]+)\}|\\chapter(?P<star>\*)?\{(?P<title>[^}]+)\}')
def visit(p):
 global number
 s=p.read_text();origin=reverse.get(str(p.relative_to(R)),str(p.relative_to(R)))
 for m in token.finditer(s):
  if m[1]:
   q=D/m[1];visit(q if q.suffix else q.with_suffix('.tex'));continue
  if m['star']:continue
  number+=1;tail=s[m.end():];n=re.search(r'\\label\{([^}]+)\}',tail);label=n[1] if n and n.start()<180 else None
  full=any(origin.endswith(x) for x in full_suffix) or p.name in ['assistance.tex','investment.tex']
  partial=any(origin.endswith(x) for x in partial_suffix)
  # Chapter-level nested content must not be accepted from a primary-file reading alone.
  end=re.search(r'\\chapter\{',tail);body=tail[:end.start()] if end else tail
  nested=re.findall(r'\\input\{([^}]+)\}',body)
  status='primary_text_contextually_reviewed' if full else ('focused_passages_reviewed' if partial else 'structural_inventory_only')
  if p.name in ['assistance.tex','investment.tex'] or origin.endswith('/software-decisions.tex'):status='integrated_treatment_contextually_reviewed'
  nested_reviewed=origin.endswith('/journeys.tex') or origin.endswith('/public-study.tex')
  rows.append({'chapter':number,'title':' '.join(m['title'].split()),'label':label,'source':str(p.relative_to(R)),'inherited_source':origin,'status':status,'nested_inputs':nested,'full_chapter_acceptance':bool(full and (not nested or nested_reviewed or status=='integrated_treatment_contextually_reviewed')),'finding':notes.get(label,'No whole-chapter writing-quality claim from the structural inventory. Read all sections and nested treatments in final order, record notation/assumptions/derivation/comparison/transition findings, then edit only confirmed defects.'),'next_action':'Read complete chapter and any nested sources in final position; reconcile scientific claims and adverse results after any change.' if not full else 'Retain author-reviewed treatment; fresh visual and independent review remain separate.'})
visit(D/'causal_banking_integrated_argument_2026-10-29.tex')
# Continuations record actual readings against the final source hashes.
# A changed source invalidates this acceptance until it is reread.
record_path=O/'contextual-review-records.json'
if record_path.exists():
 for record in json.loads(record_path.read_text())['reviews']:
  row=next(x for x in rows if x['chapter']==record['chapter'])
  assert row['label']==record['label'], 'Chapter identity changed'
  checked={x['path'] for x in record['sources']}
  assert row['source'] in checked, 'Primary chapter reading missing'
  for source in record['sources']:
   p=R/source['path']
   if source.get('read_sha256'):
    first,last=source['read_lines'];body='\n'.join(p.read_text().splitlines()[first-1:last])+'\n'
    assert hashlib.sha256(body.encode()).hexdigest()==source['read_sha256'], 'Reviewed passage changed: '+source['path']
   else:
    assert hashlib.sha256(p.read_bytes()).hexdigest()==source['sha256'], 'Reviewed source changed: '+source['path']
  def nested_sources(path):
   found=set()
   for name in re.findall(r'\\input\{([^}]+)\}',path.read_text()):
    child=D/name
    if not child.suffix:child=child.with_suffix('.tex')
    found.add(str(child.relative_to(R)));found.update(nested_sources(child))
   return found
  if row['source']!='docs/causal_banking_integrated_argument_2026-10-29.tex':
   assert nested_sources(R/row['source'])<=checked, 'Nested chapter reading missing'
  if row['source']=='docs/causal_banking_integrated_argument_2026-10-29.tex':
   assert any(x['path']==row['source'] and x.get('read_sha256') for x in record['sources']), 'Driver chapter needs passage-bound reading evidence'
  row.update(status='full_final_context_reviewed',full_chapter_acceptance=True,
             finding=record['finding'],next_action=record['next_action'],
             reviewed_sources=record['sources'])
# Bind review coverage to the expanded assembly, including sibling inputs.
# A file after a chapter's primary source still belongs to that chapter until
# the next chapter command, even if the input occurs in the book driver.
assembly={};active=None
assembly_token=re.compile(r'\\input\{([^}]+)\}|\\chapter(?P<star>\*)?\{(?P<title>[^}]+)\}')
number_assembled=0
def assemble(path,stack=()):
 global active,number_assembled
 assert path not in stack,'Cyclic manuscript input'
 text=path.read_text();cursor=0
 def segment(start,end):
  if active is None:return
  body=text[start:end]
  if not re.sub(r'%[^\n]*','',body).strip():return
  assembly.setdefault(active,[]).append({'path':str(path.relative_to(R)),
   'lines':[text.count('\n',0,start)+1,text.count('\n',0,max(start,end-1))+1],
   'sha256':hashlib.sha256(body.encode()).hexdigest()})
 for match in assembly_token.finditer(text):
  segment(cursor,match.start())
  if match[1]:
   child=D/match[1];assemble(child if child.suffix else child.with_suffix('.tex'),stack+(path,))
  elif not match['star']:
   number_assembled+=1;active=number_assembled
   assert rows[active-1]['title']==' '.join(match['title'].split())
   segment(match.start(),match.end())
  cursor=match.end()
 segment(cursor,len(text))
assemble(D/'causal_banking_integrated_argument_2026-10-29.tex')
assert number_assembled==len(rows)
for row in rows:
 prior_accepted=row['full_chapter_acceptance']
 reviewed={x['path'] for x in row.get('reviewed_sources',[])}
 # Initial recorded reviews include their primary file and its explicitly
 # reviewed nested content, but never unmentioned following sibling inputs.
 if prior_accepted and not reviewed:
  reviewed.add(row['source'])
  def add_nested(path):
   for name in re.findall(r'\\input\{([^}]+)\}',path.read_text()):
    child=D/name
    if not child.suffix:child=child.with_suffix('.tex')
    reviewed.add(str(child.relative_to(R)));add_nested(child)
  if row['source']!='docs/causal_banking_integrated_argument_2026-10-29.tex':add_nested(R/row['source'])
 row['assembled_segments']=assembly.get(row['chapter'],[])
 # Driver text surrounding inputs is a separate cross-chapter editorial task;
 # a driver-declared chapter requires its own opening reading record.
 required={x['path'] for x in row['assembled_segments'] if x['path']!='docs/causal_banking_integrated_argument_2026-10-29.tex'}
 missing=sorted(required-reviewed)
 row['unreviewed_assembled_sources']=missing
 row['primary_review_recorded']=prior_accepted
 if prior_accepted and missing:
  row['full_chapter_acceptance']=False
  row['status']='primary_reviewed_additional_assembled_text_pending'
  row['finding']+=' Assembly audit found additional chapter text outside the reviewed source tree; complete chapter acceptance is withdrawn until that text is read.'
  row['next_action']='Read unreviewed_assembled_sources in final order, record hashes and findings, then review the complete chapter transition.'
 row['nested_inputs']=[n.removeprefix('docs/') for n in dict.fromkeys(x['path'] for x in row['assembled_segments']) if n not in (row['source'],'docs/causal_banking_integrated_argument_2026-10-29.tex')]
(O/'chapter-review.json').write_text(json.dumps({'scope':'Actual contextual coverage this execution, not inherited certification. Full acceptance does not follow from labels, hashes or search hits.','chapters':rows},indent=2)+'\n')
lines=['# Chapter-level writing review','','The table separates actual reading from a structural inventory. “Primary text” does not certify nested additions that were not read. Independent science and fresh visual review remain separate.','', '| Chapter | Question | Review depth | Finding / next action |','|---|---|---|---|']
for x in rows:lines.append(f"| {x['chapter']} | {x['title']} | {x['status']} | {x['finding']} |")
(O/'chapter-review.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({'chapters':len(rows),'author_reviewed_treatments':sum(x['full_chapter_acceptance'] for x in rows),'remaining_complete_contextual_reviews':[x['chapter'] for x in rows if not x['full_chapter_acceptance']]}))

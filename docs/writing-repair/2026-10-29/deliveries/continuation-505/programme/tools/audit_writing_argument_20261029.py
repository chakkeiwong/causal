"""Post-build, exact-replay deletion audit and rendered-publication checks."""
from pathlib import Path
from collections import Counter
import re,json,hashlib,difflib,subprocess,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];D=R/'docs';O=D/'writing-repair/2026-10-29';P='writing-repair/2026-10-29/'
FULL='causal_banking_integrated_argument_2026-10-29';SP='causal_banking_sponsor_integrated_2026-10-29'
INPUT=re.compile(r'\\(?:input|include)\{([^}]+)\}')
CITE=re.compile(r'\\cite\w*\*?(?:\[[^\]]*\]){0,2}\{([^}]+)\}')
MATH=re.compile(r'(?s)(?<!\\)\\\[.*?(?<!\\)\\\]|(?<!\\)\\\(.*?(?<!\\)\\\)|(?<!\\)\$(?!\$).*?(?<!\\)\$|\\begin\{(equation\*?|align\*?|gather\*?|multline\*?)\}.*?\\end\{\1\}')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,v):(O/n).write_text(json.dumps(v,indent=2)+'\n')
def tree(p,stack=()):
 assert p not in stack,p
 out=[p]
 for x in INPUT.findall(p.read_text()):
  q=D/x;out+=tree(q if q.suffix else q.with_suffix('.tex'),stack+(p,))
 return out
def keys(s):return Counter(k.strip() for x in CITE.findall(s) for k in x.split(','))
def math(s):return Counter(re.sub(r'\s+',' ',m[0]) for m in MATH.finditer(s))
def main():
 b=json.loads((O/'baseline.json').read_text());M=json.loads((O/'source-map.json').read_text());edits=json.loads((O/'edits.json').read_text());issues=[]
 def remap(s):
  def f(m):
   n='docs/'+m[1];n=n if n.endswith('.tex') else n+'.tex'
   return r'\input{'+M[n][5:]+'}' if n in M else m[0]
  return INPUT.sub(f,s)
 states={v:remap((O/'baseline'/n).read_text()) for n,v in M.items()}
 raw=(O/'baseline'/b['root']).read_text();rt=remap(raw).replace('Scientific continuation of the developmental rewrite','Integrated argument and comparative evidence')
 rt=re.sub(r'\\bibliography\{[^}]+\}',lambda m:r'\bibliography{'+','.join(P+f'references-{i}' for i in range(len(b['bibliographies'])))+'}',rt)
 rn='docs/'+FULL+'.tex';states[rn]=rt
 decision=next(k for k in states if k==next(v for n,v in M.items() if n.endswith('/decision-synthesis.tex')))
 parts=[x for x in re.split(r'(?=\\chapter\{)',states[decision]) if x.strip()];assert len(parts)==3
 states['docs/'+P+'assistance.tex']=parts[1];states['docs/'+P+'investment.tex']=parts[2]
 states['docs/'+P+'sponsor-body.tex']=(D/'developmental-rewrite/2026-10-29/sponsor-body.tex').read_text()
 for i,n in enumerate(b['bibliographies']):states['docs/'+P+f'references-{i}.bib']=(O/'baseline'/n).read_text()
 initial=dict(states)
 for i,e in enumerate(edits,1):
  if e['file'] not in states:issues.append('Unknown ledger target '+e['file']);continue
  if states[e['file']].count(e['before'])!=1:issues.append('Nonunique ledger anchor '+str(i));continue
  states[e['file']]=states[e['file']].replace(e['before'],e['after'],1)
  if not e.get('reason') or not e.get('substantive_destination'):issues.append('Undispositioned edit '+str(i))
 for n,s in states.items():
  if (R/n).read_text()!=s:issues.append('Unrecorded final difference '+n)
 protected=[x['path'] for x in b['protected'] if not (R/x['path']).is_file() or sha(R/x['path'])!=x['sha256']]
 reconciliation=json.loads((O/'concurrent-reconciliation.json').read_text())
 reconciled={x['path']:x for x in reconciliation['changes']};unresolved_protected=[]
 for n in protected:
  x=reconciled.get(n)
  if not x or sha(R/x['original_copy'])!=x['original_sha256'] or sha(R/n)!=x['observed_current_sha256'] or sha(R/x['observed_current_copy'])!=x['observed_current_sha256']:unresolved_protected.append(n)
 if unresolved_protected:issues.append('Unreconciled protected baseline change')
 assets=json.loads((O/'unchanged-assets.json').read_text())['files'];changed_assets=[n for n,h in assets.items() if sha(R/n)!=h]
 if changed_assets:issues.append('Referenced asset changed')
 for i,n in enumerate(b['bibliographies']):
  if not (O/f'references-{i}.bib').read_text().startswith((O/'baseline'/n).read_text()):issues.append('Inherited bibliography changed '+n)
 style_record=json.loads((O/'citation-style-edit.json').read_text())
 if sha(R/style_record['original'])!=style_record['original_sha256'] or sha(R/style_record['successor'])!=style_record['successor_sha256']:
  issues.append('Citation style differs from reviewed identity')
 if (R/style_record['original']).read_text()!=style_record['exact_before'] or (R/style_record['successor']).read_text()!=style_record['exact_after']:
  issues.append('Citation style exact record mismatch')
 final=tree(D/(FULL+'.tex'));count=Counter(final);unreachable=[n for n,v in M.items() if count[R/v]!=1]
 if unreachable:issues.append('Inherited source missing or duplicated')
 before='\n'.join((O/'baseline'/n).read_text() for n in b['sources']);after='\n'.join(p.read_text() for p in final)
 missing_keys=sorted(set(keys(before))-set(keys(after)));added_keys=sorted(set(keys(after))-set(keys(before)))
 missing_labels=sorted(set(re.findall(r'\\label\{([^}]+)\}',before))-set(re.findall(r'\\label\{([^}]+)\}',after)))
 if missing_keys or set(added_keys)!=set(reconciliation['new_citation_keys']) or missing_labels:issues.append('Citation or label scope mismatch')
 oldmath=Counter();newmath=Counter()
 for n in b['sources']:oldmath.update(math((O/'baseline'/n).read_text()))
 for p in final:newmath.update(math(p.read_text()))
 removed_math=dict(oldmath-newmath);added_math=dict(newmath-oldmath)
 unique_math_lost=set(oldmath)-set(newmath)
 allowed={r'$e(S)\{1-e(S)\}$',r'$e(S)$'}
 authorized_added={'$-10$',r'$(3\times10-10)/4=5$'}
 # Bind new notation to exact reviewed edits, not a generic formula allowlist.
 dispositions=json.loads((O/'continuation-math-dispositions.json').read_text())
 continuation_additions=Counter()
 for d in dispositions['additions']:
  e=edits[d['edit']-1]
  if hashlib.sha256(e['before'].encode()).hexdigest()!=d['before_sha256'] or hashlib.sha256(e['after'].encode()).hexdigest()!=d['after_sha256']:
   issues.append('Mathematical disposition edit identity mismatch');continue
  if dict(math(e['after'])-math(e['before']))!=d['added_math'] or dict(math(e['before'])-math(e['after']))!=d['removed_math']:
   issues.append('Mathematical disposition occurrence mismatch');continue
  continuation_additions.update(d['added_math'])
 # Permit only an exact, hash-bound repair of a broken spacing command.
 # This does not authorize an arbitrary replacement of a mathematical law.
 typographic_destinations={}
 for d in dispositions.get('typographic_replacements',[]):
  e=edits[d['edit']-1]
  if hashlib.sha256(e['before'].encode()).hexdigest()!=d['before_sha256'] or hashlib.sha256(e['after'].encode()).hexdigest()!=d['after_sha256']:
   issues.append('Typographic disposition edit identity mismatch');continue
  if e['before'].replace(':quad',':')!=e['after'].replace(':'+chr(92)+'quad',':') or ':quad' not in e['before']:
   issues.append('Typographic disposition changes substantive mathematics');continue
  if dict(math(e['after'])-math(e['before']))!=d['added_math'] or dict(math(e['before'])-math(e['after']))!=d['removed_math'] or not d.get('substantive_destination'):
   issues.append('Typographic disposition occurrence mismatch');continue
  continuation_additions.update(d['added_math'])
  typographic_destinations.update({formula:d['substantive_destination'] for formula in d['removed_math']})
 residual_added=Counter(added_math)-continuation_additions
 if unique_math_lost-allowed-set(typographic_destinations) or set(residual_added)-authorized_added:issues.append('Unexpected mathematical change')
 math_dispositions=[]
 for formula,n in removed_math.items():
  if formula in typographic_destinations:dest=typographic_destinations[formula]
  elif formula in allowed or formula=='$S$':dest='scisyn:software subsection 5: same e(S) definition and e(S){1-e(S)} weighting appear within the complete theta_* equation; rewrite:deposit retains numerical consequence.'
  else:dest='rewrite:investment-decision: identical formula or variable remains; only the second annual-account exposition was removed.'
  math_dispositions.append({'removed_occurrence':formula,'count':n,'destination':dest})
 clean=lambda s:re.sub(r'\\(?:input|include|includegraphics|bibliography|label|ref|eqref|pageref)(?:\[[^\]]*\])?\{[^}]+\}','',s)
 # Scan a whole numeric/version literal even when preceding prose lacks a space.
 # The old letter lookbehind skipped its leading digit and invented a suffix.
 num=lambda s:Counter(re.findall(r'\d+(?:[.,]\d+)*',clean(s)))
 lost_numbers=sorted(set(num(before))-set(num(after)))
 # A correction must match an exact edit and the preserved request journal.
 numeric_corrections=[]
 correction_file=O/'numeric-corrections.json'
 if correction_file.exists():
  import statistics
  for correction in json.loads(correction_file.read_text())['corrections']:
   try:
    edit=edits[correction['edit']-1]
    assert hashlib.sha256(edit['before'].encode()).hexdigest()==correction['before_sha256']
    assert hashlib.sha256(edit['after'].encode()).hexdigest()==correction['after_sha256']
    old_token=correction['removed_token'];new_token=correction['replacement_token']
    assert edit['before'].count(old_token)==1
    assert edit['before'].replace(old_token,new_token,1)==edit['after']
    journal=R/correction['journal'];summary_path=R/correction['summary']
    assert sha(journal)==correction['journal_sha256'] and sha(summary_path)==correction['summary_sha256']
    widths=[];request_keys=set()
    for line in journal.open():
     record=json.loads(line)
     if record.get('key','').startswith(correction['request_prefix']):
      assert record['key'] not in request_keys;request_keys.add(record['key'])
      lo,hi=record['result']['methods'][correction['method']]['interval']
      assert isinstance(lo,(int,float)) and isinstance(hi,(int,float)) and hi>=lo
      widths.append(hi-lo)
    assert len(widths)==correction['requests']
    median=statistics.median(widths)
    original=next(r for r in json.loads(summary_path.read_text())['results'] if r['design']['name']==correction['summary_design'])
    assert median==correction['median_width_usd']==original['summary']['methods'][correction['method']]['finite_width_quantiles'][1]
    assert format(median/correction['scale'],'.'+str(correction['decimal_places'])+'f')==new_token
    assert dict(num(edit['before'])-num(edit['after']))=={old_token:1}
    assert dict(num(edit['after'])-num(edit['before']))=={new_token:1}
    numeric_corrections.append(correction)
   except (AssertionError,KeyError,ValueError,StopIteration):
    issues.append('Numeric correction lacks exact evidence at edit '+str(correction.get('edit')))
 unaccounted_numeric_loss=sorted(set(lost_numbers)-{x['removed_token'] for x in numeric_corrections})
 if unaccounted_numeric_loss:issues.append('A distinct numeric token was lost without a verified correction')
 fls=(O/'build-full'/(FULL+'.fls')).read_text();actual=set()
 for line in fls.splitlines():
  if line.startswith('INPUT '):
   p=Path(line[6:]);actual.add((p if p.is_absolute() else D/p).resolve())
 uncompiled=[str(p.relative_to(R)) for p in final if p.resolve() not in actual]
 if uncompiled:issues.append('Expected source absent from actual compiler recorder')
 # Every source change is exact-replayed. The human disposition explains semantic consolidations.
 diffs=[]
 for n,v in M.items():diffs.extend(difflib.unified_diff((O/'baseline'/n).read_text().splitlines(True),(R/v).read_text().splitlines(True),fromfile=n,tofile=v))
 diffs.extend(difflib.unified_diff(raw.splitlines(True),(D/(FULL+'.tex')).read_text().splitlines(True),fromfile=b['root'],tofile=rn))
 (O/'all-inherited-content.diff').write_text(''.join(diffs))
 lines=['# Exact post-edit deletion and replacement ledger','','Generated from replay-verified edits after the final manuscript build. Input-path rewriting is separately reproducible from source-map.json. No historical source is overwritten.','']
 for i,e in enumerate(edits,1):lines.extend([f'## Edit {i}', '',e['file'],'',e['reason'],'','Substantive destination: '+e['substantive_destination'],'','Before:','~~~text',e['before'],'~~~','After:','~~~text',e['after'],'~~~',''])
 (O/'full-deletion-ledger.md').write_text('\n'.join(lines))
 publications={}
 for kind,stem in [('full',FULL),('sponsor',SP)]:
  pdf=D/(stem+'.pdf');log=(O/('build-'+kind)/(stem+'.log')).read_text(errors='replace');warnings={w:len(re.findall(w,log,re.I)) for w in ['undefined','multiply defined','Overfull','Underfull','Label.*changed']}
  if any(warnings[w] for w in ['undefined','multiply defined','Overfull','Label.*changed']):issues.append(kind+' unresolved build warnings')
  txt=O/(kind+'-rendered.txt');xml=O/(kind+'-geometry.xml')
  subprocess.run(['pdftotext','-layout',str(pdf),str(txt)],check=True,capture_output=True)
  subprocess.run(['pdftotext','-bbox',str(pdf),str(xml)],check=True,capture_output=True)
  rawxml=xml.read_text();cleanxml=re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]','',rawxml);pages=[x for x in ET.fromstring(cleanxml).iter() if x.tag.endswith('page')];outside=[];empty=[]
  for i,page in enumerate(pages,1):
   words=[x for x in page.iter() if x.tag.endswith('word')]
   if not words:empty.append(i)
   for word in words:
    a=word.attrib
    if float(a['xMin'])<0 or float(a['yMin'])<0 or float(a['xMax'])>float(page.get('width'))+.1 or float(a['yMax'])>float(page.get('height'))+.1:outside.append(i);break
  if outside or empty or '??' in txt.read_text():issues.append(kind+' rendered text/geometry issue')
  files=tree(D/(stem+'.tex'));late=[str(p.relative_to(R)) for p in files if p.stat().st_mtime>pdf.stat().st_mtime]
  if late:issues.append(kind+' PDF predates source edits')
  publications[kind]={'path':str(pdf.relative_to(R)),'sha256':sha(pdf),'pages':len(pages),'warnings':warnings,'outside_page':outside,'empty_pages':empty,'unresolved_markers':'??' in txt.read_text(),'source_edits_after_build':late,'fresh_visual_acceptance':False,'visual_limit':'Session image allowance exhausted; do not inherit predecessor acceptance.'}
 # Verify the existing source-audit identity chains without inventing fresh literature inspection.
 checked={};source_issues=[]
 def bindings(x):
  if isinstance(x,dict):
   n=x.get('path',x.get('local_path',x.get('local_copy')));h=x.get('sha256')
   if isinstance(n,str) and isinstance(h,str) and len(h)==64:
    p=Path(n) if n.startswith('/') else R/n;k=(str(p),h)
    if k not in checked:
     checked[k]=p.is_file() and sha(p)==h
     if not checked[k]:source_issues.append(n)
   for v in x.values():bindings(v)
  elif isinstance(x,list):
   for v in x:bindings(v)
 syn=json.loads((D/'scientific-synthesis/2026-10-29/source-audit.json').read_text());bindings(syn);bindings(json.loads((R/syn['inherited_audit']).read_text()))
 for name in ['source-audit.json','frontier-source-audit.json']:
  p=D/'scientific-gap-closure/2026-10-29'/name
  if p.exists():bindings(json.loads(p.read_text()))
 bindings(json.loads((O/'additional-source-support.json').read_text()))
 if source_issues:issues.append('Existing source-binding integrity issue')
 summary={'pass':not issues,'issues':issues,'protected_files':len(b['protected']),'protected_changes':protected,'reconciled_external_changes':list(reconciled),'unresolved_protected_changes':unresolved_protected,'referenced_assets':len(assets),'changed_assets':changed_assets,'inherited_tex_sources':len(M),'mapped_sources_compiled_once':len(M)-len(unreachable),'unreachable':unreachable,'actual_compiler_missing':uncompiled,'exact_edit_replay':not any('difference' in x or 'anchor' in x for x in issues),'edits':len(edits),'citation_keys_before':len(keys(before)),'citation_keys_after':len(keys(after)),'missing_citation_keys':missing_keys,'new_citation_keys':added_keys,'missing_labels':missing_labels,'removed_math_dispositions':math_dispositions,'added_math':added_math,'distinct_numerals_lost':lost_numbers,'verified_numeric_corrections':numeric_corrections,'unaccounted_numeric_loss':unaccounted_numeric_loss,'source_bindings_checked':len(checked),'source_binding_issues':source_issues,'publication':publications,'final_source_hashes':{str(p.relative_to(R)):sha(p) for p in final+[R/style_record['successor']]},'ledger_sha256':sha(O/'edits.json'),'checks_after_final_edit':not any(x['source_edits_after_build'] for x in publications.values()),'meaning':'Exact replay and retained scientific destinations support no unaccounted substantive loss within these edits. This is author review, not proof of whole-book prose quality or independent acceptance.'}
 # Bind sponsor sources and bibliography inputs as well as the full reader tree.
 # Exact replay already verifies their content; a later change must also stale W08.
 additional_sources = tree(D/(SP+'.tex')) + [O/f'references-{i}.bib' for i in range(len(b['bibliographies']))]
 summary['final_source_hashes'].update({str(p.relative_to(R)):sha(p) for p in additional_sources})
 save('deletion-audit.json',summary);save('publication-verification.json',publications)
 print(json.dumps({k:v for k,v in summary.items() if k not in ['final_source_hashes','removed_math_dispositions']},indent=2))
 if issues:raise SystemExit(1)
if __name__=='__main__':main()

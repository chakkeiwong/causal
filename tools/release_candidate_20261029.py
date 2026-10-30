"""Build and preserve-audit the separately maintained 2026-10-29 release candidate."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json,os,re,shutil,subprocess,time
import xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];B=R/'docs/release/2026-10-29';S=B/'source';D=S/'docs'
NAMES={'full':'causal_banking_release_candidate_2026-10-29','sponsor':'causal_banking_sponsor_release_candidate_2026-10-29'}
INPUT=re.compile(r'\\(?:input|include)\{([^}]+)\}')
CITE=re.compile(r'\\cite\w*\*?(?:\[[^\]]*\]){0,2}\{([^}]+)\}')
MATH=re.compile(r'(?s)(?<!\\)\\\[.*?(?<!\\)\\\]|(?<!\\)\\\(.*?(?<!\\)\\\)|(?<!\\)\$(?!\$).*?(?<!\\)\$|\\begin\{(equation\*?|align\*?|gather\*?|multline\*?)\}.*?\\end\{\1\}')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def save(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+'\n')
def source_text_issues(root):
 findings=[]
 for path in root.rglob('*.tex'):
  raw=path.read_bytes()
  bad=sorted({c for c in raw if c<32 and c not in (9,10)})
  if bad:findings.append({'file':str(path.relative_to(root)),'control_bytes':bad})
  for number,line in enumerate(raw.decode('utf-8').splitlines(),1):
   if re.match(r'^\s*ef\{[^}]+\}',line):
    findings.append({'file':str(path.relative_to(root)),'line':number,'issue':'Broken reference command, likely normalized carriage-return escape'})
 return findings
def tree(root,path,stack=()):
 assert path not in stack,'Input cycle'
 result=[path]
 for name in INPUT.findall(path.read_text()):
  child=root/name;child=child if child.suffix else child.with_suffix('.tex');result+=tree(root,child,stack+(path,))
 return result
def checked_run(command,cwd,env,log):
 start=time.monotonic()
 with log.open('w') as out:p=subprocess.run(command,cwd=cwd,env=env,stdout=out,stderr=subprocess.STDOUT,timeout=300)
 result={'command':command,'cwd':str(cwd.relative_to(R)),'returncode':p.returncode,'seconds':round(time.monotonic()-start,3),'log':str(log.relative_to(R))}
 print(json.dumps(result),flush=True)
 if p.returncode:raise RuntimeError(log.read_text(errors='replace')[-5000:])
 return result

def build():
 malformed=source_text_issues(D)
 assert not malformed,('Malformed source text before build',malformed)
 batch=B/'batches';batch.mkdir(exist_ok=True)
 number=1+max([int(p.name) for p in batch.iterdir() if p.is_dir() and p.name.isdigit()]+[0]);folder=batch/f'{number:03d}';folder.mkdir()
 sources={str(p.relative_to(R)):sha(p) for p in S.rglob('*') if p.is_file()};ledger=sha(B/'edits.json')
 save(folder/'source-before.json',{'files':sources,'ledger_sha256':ledger})
 env=dict(os.environ,SOURCE_DATE_EPOCH='1793285915',FORCE_SOURCE_DATE='1',TZ='UTC',BIBINPUTS=str(D)+'//:',BSTINPUTS=str(D)+'//:')
 results={}
 for kind,stem in NAMES.items():
  out=folder/kind;out.mkdir();cmd=['pdflatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error','-file-line-error','-recorder','-output-directory='+str(out),stem+'.tex'];passes=[]
  passes.append(checked_run(cmd,D,env,out/'pass-1.txt'))
  if kind=='full':passes.append(checked_run(['bibtex',stem],out,env,out/'pass-bibtex.txt'))
  for turn in range(2,6):
   passes.append(checked_run(cmd,D,env,out/f'pass-{turn}.txt'))
   log=(out/(stem+'.log')).read_text(errors='replace')
   if turn>=3 and not re.search(r'undefined|multiply defined|Label.*changed',log,re.I):break
  save(out/'passes.json',passes);results[kind]={'folder':str(out.relative_to(R)),'stem':stem,'passes':passes}
 assert sha(B/'edits.json')==ledger,'Ledger changed during build'
 assert all(sha(R/name)==h for name,h in sources.items()),'Source changed during build'
 for kind,row in results.items():
  p=R/row['folder']/(row['stem']+'.pdf');target=R/'docs'/(row['stem']+'.pdf');shutil.copy2(p,target);row.update(path=str(target.relative_to(R)),sha256=sha(target))
 receipt={'batch':number,'folder':str(folder.relative_to(R)),'source_before':str((folder/'source-before.json').relative_to(R)),'ledger_sha256':ledger,'publications':results,'reproducible_environment':{'SOURCE_DATE_EPOCH':'1793285915','FORCE_SOURCE_DATE':'1','TZ':'UTC'},'sources_unchanged_during_build':True}
 save(folder/'build.json',receipt);save(B/'latest-build.json',receipt)
 print(json.dumps({'built_batch':number,'publications':{k:{x:v[x] for x in ['path','sha256']} for k,v in results.items()}}),flush=True)

def audit():
 issues=[];mapping=read(B/'source-map.json');additions=read(B/'additions.json');edits=read(B/'edits.json');base=read(B/'baseline-deletion-audit.json');build=read(B/'latest-build.json');captured=read(R/build['source_before'])
 malformed=source_text_issues(D)
 if malformed:issues.append('Malformed source text: '+json.dumps(malformed))
 audit_start_ledger=sha(B/'edits.json')
 audit_start_sources={str(p.relative_to(R)):sha(p) for p in S.rglob('*') if p.is_file()}
 initial={};changed_baseline=[]
 for target,row in mapping.items():
  original=R/row['original']
  if not original.is_file() or sha(original)!=row['sha256']:changed_baseline.append(row['original'])
  else:initial[target]=original.read_text() if original.suffix in {'.tex','.bib','.bst','.sty','.cls'} else None
 for row in additions:
  original=R/row['original']
  if sha(original)!=row['sha256']:changed_baseline.append(row['original'])
  initial[row['path']]=original.read_text() if original.suffix in {'.tex','.bib','.bst','.sty','.cls'} else None
 expected=dict(initial)
 for i,e in enumerate(edits,1):
  if e['file'] not in expected or expected[e['file']] is None:issues.append(f'Edit {i}: unknown text target');continue
  if expected[e['file']].count(e['before'])!=1:issues.append(f'Edit {i}: nonunique anchor');continue
  if not e.get('reason') or not e.get('substantive_destination'):issues.append(f'Edit {i}: missing disposition')
  expected[e['file']]=expected[e['file']].replace(e['before'],e['after'],1)
 for name,text in expected.items():
  if text is not None and (R/name).read_text()!=text:issues.append('Unrecorded source difference: '+name)
  if text is None:
   expected_hash=mapping[name]['sha256'] if name in mapping else next(row['sha256'] for row in additions if row['path']==name)
   if sha(R/name)!=expected_hash:issues.append('Changed preserved asset: '+name)
 if changed_baseline:issues.append('Protected baseline changed')
 for n,h in base['final_source_hashes'].items():
  if sha(R/n)!=h:issues.append('505-edit baseline source changed: '+n)
 for pub in base['publication'].values():
  if sha(R/pub['path'])!=pub['sha256']:issues.append('505-edit baseline PDF changed')
 for n,h in read(B/'state.json')['historical_protected'].items():
  if sha(R/n)!=h:issues.append('Historical programme changed: '+n)
 protected=read(R/'docs/writing-repair/2026-10-29/baseline.json')['protected']
 relocation_path=B/'protected-relocations.json'
 relocations=read(relocation_path)['relocations'] if relocation_path.exists() else []
 preserved_elsewhere=[];protected_bad=[]
 protected_map={x['path']:x for x in protected}
 if len({x['original'] for x in relocations})!=len(relocations):issues.append('Duplicate protected relocation')
 relocation_map={x['original']:x for x in relocations}
 for name,row in relocation_map.items():
  if name not in protected_map or row.get('expected_sha256')!=protected_map[name]['sha256']:
   issues.append('Relocation does not match protected original: '+name)
 for x in protected:
  path=R/x['path']
  if path.is_file() and sha(path)==x['sha256']:continue
  row=relocation_map.get(x['path']);valid=False
  if row:
   target=(R/row['preserved']).resolve();review=row.get('review_record',{});review_path=R/review.get('path','')
   valid=(target.is_relative_to(B.resolve()) and target.is_file() and sha(target)==x['sha256']
          and row.get('reason') and review_path.is_file() and sha(review_path)==review.get('sha256'))
  if valid:preserved_elsewhere.append(row)
  else:protected_bad.append(x['path'])
 if protected_bad:issues.append('Inherited protected identity changed')
 if sha(B/'edits.json')!=build['ledger_sha256']:issues.append('Audit ledger differs from compiled ledger')
 drift=[n for n,h in captured['files'].items() if sha(R/n)!=h]
 if drift:issues.append('Release source differs from compiled source')
 reverse={target:row['original'] for target,row in mapping.items()}
 def math(text):return Counter(re.sub(r'\s+',' ',m[0]) for m in MATH.finditer(text))
 def keys(text):return Counter(k.strip() for m in CITE.findall(text) for k in m.split(','))
 before_math=Counter();after_math=Counter();before_keys=Counter();after_keys=Counter();before_labels=set();after_labels=set();numeric_loss=[]
 for name,text in initial.items():
  if text is None or not name.endswith('.tex'):continue
  final=(R/name).read_text();before_math.update(math(text));after_math.update(math(final));before_keys.update(keys(text));after_keys.update(keys(final));before_labels.update(re.findall(r'\\label\{([^}]+)\}',text));after_labels.update(re.findall(r'\\label\{([^}]+)\}',final))
  # Informational per-file loss; the aggregate check guards retained numeric facts.
 before_text='\n'.join(t for n,t in initial.items() if t is not None and n.endswith('.tex'));after_text='\n'.join((R/n).read_text() for n,t in initial.items() if t is not None and n.endswith('.tex'))
 lost_math=dict(before_math-after_math);added_math=dict(after_math-before_math);lost_keys=sorted(set(before_keys)-set(after_keys));lost_labels=sorted(before_labels-after_labels)
 # Existing mathematics remains protected. New equations require exact,
 # independently hash-bound review records; a generic waiver is insufficient.
 from release_mathematical_review_20261029 import validate_additions
 math_review_path=B/'mathematical-addition-reviews.json'
 math_reviews=read(math_review_path)['reviews'] if math_review_path.exists() else []
 approved_math,math_issues=validate_additions(math_reviews,edits,R,MATH)
 issues.extend(math_issues)
 if lost_math:issues.append('Unreviewed mathematical removal')
 if added_math!=dict(approved_math):issues.append('Unreviewed mathematical occurrence change')
 if lost_keys or lost_labels:issues.append('Lost citation key or label')
 clean=lambda s:re.sub(r'\\(?:input|include|includegraphics|bibliography|bibliographystyle|label|ref|eqref|pageref)(?:\[[^\]]*\])?\{[^}]+\}','',s)
 number=lambda s:set(re.findall(r'\d+(?:[.,]\d+)*',clean(s)))
 numeric_loss=sorted(number(before_text)-number(after_text))
 if numeric_loss:issues.append('Unaccounted distinct numeric loss')
 publications={};input_reports={}
 for kind,row in build['publications'].items():
  stem=row['stem'];folder=R/row['folder'];pdf=R/row['path'];files=tree(D,D/(stem+'.tex'))
  baseline_stem='causal_banking_integrated_argument_2026-10-29' if kind=='full' else 'causal_banking_sponsor_integrated_2026-10-29'
  original_files=tree(R/'docs',R/'docs'/(baseline_stem+'.tex'))
  # Exact inherited occurrence order, with only declared additions removed.
  inherited=[str(p.relative_to(R)) for p in original_files[1:]];actual=[reverse[str(p.relative_to(R))] for p in files[1:] if str(p.relative_to(R)) in reverse]
  if inherited!=actual:issues.append(kind+' inherited input order/occurrences changed')
  input_reports[kind]={'inherited_occurrences':len(inherited),'preserved_in_order':inherited==actual,'added_occurrences':[str(p.relative_to(R)) for p in files if str(p.relative_to(R)) not in reverse]}
  compiled=set()
  for line in (folder/(stem+'.fls')).read_text().splitlines():
   if line.startswith('INPUT '):
    p=Path(line[6:]);compiled.add((p if p.is_absolute() else D/p).resolve())
  absent=[str(p.relative_to(R)) for p in files if p.resolve() not in compiled]
  if absent:issues.append(kind+' expected input not compiled')
  log=(folder/(stem+'.log')).read_text(errors='replace');warnings={w:len(re.findall(w,log,re.I)) for w in ['undefined','multiply defined','Overfull','Underfull','Label.*changed']}
  if any(v for k,v in warnings.items() if k!='Underfull'):issues.append(kind+' unresolved build warning')
  txt=folder/'rendered.txt';xml=folder/'geometry.xml';subprocess.run(['pdftotext','-layout',str(pdf),str(txt)],check=True,capture_output=True);subprocess.run(['pdftotext','-bbox',str(pdf),str(xml)],check=True,capture_output=True)
  cleaned=re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]','',xml.read_text());pages=[p for p in ET.fromstring(cleaned).iter() if p.tag.endswith('page')];outside=[];empty=[]
  for i,page in enumerate(pages,1):
   words=[w for w in page.iter() if w.tag.endswith('word')]
   if not words:empty.append(i)
   for w in words:
    v=w.attrib
    if float(v['xMin'])<0 or float(v['yMin'])<0 or float(v['xMax'])>float(page.get('width'))+.1 or float(v['yMax'])>float(page.get('height'))+.1:outside.append(i);break
  if outside or empty or '??' in txt.read_text():issues.append(kind+' text/geometry issue')
  if sha(pdf)!=row['sha256']:issues.append(kind+' publication changed since build')
  publications[kind]={'path':row['path'],'sha256':sha(pdf),'pages':len(pages),'warnings':warnings,'outside_pages':outside,'empty_pages':empty,'unresolved_markers':'??' in txt.read_text(),'missing_compiler_inputs':absent,'fresh_visual_acceptance':False}
 source_bindings=[]
 for x in read(B/'discovery-integration-verification.json')['preserved_evidence'].items():
  n,h=x;source_bindings.append({'path':n,'pass':sha(R/n)==h})
 if not all(x['pass'] for x in source_bindings):issues.append('Integrated evidence changed')
 # A long geometry pass must not certify a source edit made after its first read.
 audit_end_sources={str(p.relative_to(R)):sha(p) for p in S.rglob('*') if p.is_file()}
 audit_end_ledger=sha(B/'edits.json')
 stable_during_audit=(audit_start_sources==audit_end_sources and audit_start_ledger==audit_end_ledger)
 if not stable_during_audit:issues.append('Source or ledger changed during audit')
 if audit_end_sources!=captured['files'] or audit_end_ledger!=build['ledger_sha256']:
  issues.append('Final audit bytes differ from compiled source or ledger')
 report={'status':'pass' if not issues else 'fail','issues':issues,'edits':len(edits),'ledger_sha256':sha(B/'edits.json'),'baseline_edits':505,'baseline_unchanged':not changed_baseline,'protected_identities':len(protected),'changed_protected':protected_bad,'exact_replay':not any('anchor' in i or 'difference' in i for i in issues),'input_reports':input_reports,'math_removed':lost_math,'math_added':added_math,'missing_citation_keys':lost_keys,'missing_labels':lost_labels,'distinct_numeric_loss':numeric_loss,'citation_keys':len(after_keys),'final_source_hashes':{str(p.relative_to(R)):sha(p) for p in S.rglob('*') if p.is_file()},'source_edits_after_build':drift,'publication':publications,'checks_after_final_edit':not drift and build['ledger_sha256']==sha(B/'edits.json'),'new_evidence_bindings':source_bindings,'fresh_visual_acceptance':False,'independent_acceptance':False,'release_accepted':False,'meaning':'Preservation and publication verification of the current candidate; author/source/visual/external release gates remain distinct.'}
 report['sources_stable_during_audit']=stable_during_audit
 report['source_text_integrity']={'status':'pass' if not malformed else 'fail','findings':malformed,'scope':'Control bytes and the observed escaped-reference failure; no general prose-quality or visual certification.'}
 report['protected_preserved_elsewhere']=preserved_elsewhere
 report['protected_relocations']={'path':str(relocation_path.relative_to(R)),'sha256':sha(relocation_path)} if relocation_path.exists() else None
 report['reviewed_math_additions']=dict(approved_math)
 report['mathematical_addition_review']={'path':str(math_review_path.relative_to(R)),'sha256':sha(math_review_path)} if math_review_path.exists() else None
 report['checks_after_final_edit']=report['checks_after_final_edit'] and stable_during_audit
 save(B/'deletion-audit.json',report);save(R/build['folder']/'deletion-audit.json',report)
 lines=['# Release candidate exact edit ledger','','All edits apply to the separately preserved successor. Baseline 505-edit reader and original scientific study remain unchanged.','']
 for i,e in enumerate(edits,1):lines += [f'## Edit {i}',e['file'],'',e['reason'],'','Substantive destination: '+e['substantive_destination'],'','Before:','~~~text',e['before'],'~~~','After:','~~~text',e['after'],'~~~','']
 (B/'full-deletion-ledger.md').write_text('\n'.join(lines))
 print(json.dumps({k:v for k,v in report.items() if k not in ['final_source_hashes','new_evidence_bindings']},indent=2),flush=True)
 if issues:raise SystemExit(1)

def main():
 parser=argparse.ArgumentParser();parser.add_argument('action',choices=['build','audit']);args=parser.parse_args();globals()[args.action]()
if __name__=='__main__':main()

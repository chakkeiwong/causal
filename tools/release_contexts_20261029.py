"""Bind release contextual review extracts to an exact edit-ledger revision.

The 39-edit expanded snapshot is retained. Later exact edits are replayed in
its source segments, then every substantive segment is matched back to current
source bytes. This prepares review material; it never certifies that it was read.
"""
from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parents[1]
B=R/'docs/release/2026-10-29'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ledger=json.loads((B/'edits.json').read_text())
 old=json.loads((B/'review-context-expanded.json').read_text())
 out=B/f'context-review-{len(ledger):03d}'
 if out.exists():raise SystemExit('Review snapshot already exists; preserve it and use its manifest.')
 issues=[];unmatched=[];ancillary=[]
 for i,e in enumerate(ledger[39:],40):
  if e['file'].endswith(('.bib','.bst')) or e['file'].endswith('/sponsor-body.tex'):
   # Bibliographies, their style and the separately compiled sponsor are not in this reader
   # snapshot. Reconstruct the entire file from its preserved baseline before
   # recording the exact scope exception. Sponsor reading remains separate.
   mapping=json.loads((B/'source-map.json').read_text())
   original=R/mapping[e['file']]['original']
   assert digest(original)==mapping[e['file']]['sha256']
   expected=original.read_text()
   for change in ledger:
    if change['file']==e['file']:
     assert expected.count(change['before'])==1
     expected=expected.replace(change['before'],change['after'],1)
   assert expected==(R/e['file']).read_text()
   ancillary.append({'edit':i,'file':e['file'],'sha256':digest(R/e['file']),'status':'exact_replay_verified_outside_prose_snapshot'})
   continue
  hits=[s for c in old['chapters'] for s in c['segments'] if s['file']==e['file'] and e['before'] in s['text']]
  # Input commands are expanded out of the snapshot. An insertion immediately
  # before one belongs at the end of its unique preceding source segment.
  if not hits and re.fullmatch(r'\\input\{[^}]+\}',e['before']) and e['after'].endswith(e['before']):
   added=e['after'][:-len(e['before'])]
   actual=(R/e['file']).read_text()
   preceding=[s for c in old['chapters'] for s in c['segments']
              if s['file']==e['file'] and s['text'].strip()
              and actual.count(s['text']+added+e['before'])==1]
   if len(preceding)==1:
    preceding[0]['text']+=added
    continue
  if len(hits)!=1:
   unmatched.append({'edit':i,'file':e['file'],'matches':len(hits)})
   continue
  hits[0]['text']=hits[0]['text'].replace(e['before'],e['after'],1)
 for c in old['chapters']:
  for s in c['segments']:
   if not s['text'].strip():continue
   actual=(R/s['file']).read_text();pos=actual.find(s['text'])
   if pos<0:issues.append(s['file'])
   else:s['start']=pos
 if issues or unmatched:raise SystemExit(json.dumps({'issues':issues,'unmatched_edits':unmatched},indent=2))
 out.mkdir();manifest=[]
 for idx,c in enumerate(old['chapters']):
  segments=[s for s in c['segments'] if s['text'].strip()]
  text='\n\n'.join('% SOURCE '+s['file']+' CHAR '+str(s['start'])+'\n'+s['text'] for s in segments)+'\n'
  name=f"chapter-{c['number']:03d}.tex" if c.get('number') else f'front-{idx:03d}.tex'
  p=out/name;p.write_text(text)
  manifest.append({'chapter':c.get('number',0),'title':c['title'],'extract':str(p.relative_to(R)),'sha256':digest(p),'lines':len(text.splitlines()),'words':len(text.split()),'source_bindings':{s['file']:digest(R/s['file']) for s in segments},'segments':[{'file':s['file'],'start':s['start'],'characters':len(s['text']),'sha256':hashlib.sha256(s['text'].encode()).hexdigest()} for s in segments]})
 receipt={'ledger_sha256':digest(B/'edits.json'),'edits':len(ledger),'basis':'Preserved39-edit expanded snapshot with exact successor edit replay and source-segment matching','chapters':manifest,'ancillary_edits':ancillary,'read_acceptance':False}
 (out/'manifest.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps({'output':str(out.relative_to(R)),'chapters':len(manifest),'edits':len(ledger),'matching_issues':issues,'unmatched_edits':unmatched}))
if __name__=='__main__':main()

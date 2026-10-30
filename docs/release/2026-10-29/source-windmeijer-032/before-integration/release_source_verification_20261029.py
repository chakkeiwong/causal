"""Bind every release citation to retained audit records and inspectable originals."""
from pathlib import Path
from collections import Counter,defaultdict
import hashlib,json,re,subprocess

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/release/2026-10-29'
SOURCE=OUT/'source/docs'
AUDITS=[
 'docs/program/execution/2026-10-29/panel-runtime-reader-v2/reader/source-audit.json',
 'docs/scientific-synthesis/2026-10-29/source-audit.json',
 'docs/scientific-gap-closure/2026-10-29/source-audit.json',
 'docs/scientific-gap-closure/2026-10-29/frontier-source-audit.json',
 'docs/writing-repair/2026-10-29/additional-source-support.json',
 'docs/discovery-repair/2026-10-29/source-audit.json',
 'docs/release/2026-10-29/source-delegates-015/source-audit.json',
 'docs/release/2026-10-29/source-flexbcf-016/source-audit.json',
 'docs/release/2026-10-29/source-flexpaper-017/source-audit.json',
 'docs/release/2026-10-29/source-closure-018/source-audit.json',
 'docs/release/2026-10-29/source-dbn-019/source-audit.json',
 'docs/release/2026-10-29/source-survival-022/source-audit.json',
 'docs/release/2026-10-29/source-ife-023/source-audit.json',
 'docs/release/2026-10-29/source-pygformula-025/source-audit.json']

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def walk(value):
    if isinstance(value,dict):
        yield value
        for child in value.values():yield from walk(child)
    elif isinstance(value,list):
        for child in value:yield from walk(child)

def main():
    keys=set();occurrences=defaultdict(list);issues=[]
    for path in SOURCE.rglob('*.tex'):
        for match in re.finditer(r'\\cite\w*\*?(?:\[[^\]]*\]){0,2}\{([^}]+)\}',path.read_text()):
            for key in match[1].split(','):
                key=key.strip();keys.add(key);occurrences[key].append(str(path.relative_to(ROOT)))
    records={};record_audits={};audit_bindings={};checked={};bad=[]
    for name in AUDITS:
        path=ROOT/name;audit=json.loads(path.read_text());audit_bindings[name]=sha(path)
        for row in audit.get('sources',[]):
            for field in ['integrated_citation_key','id','citation','citation_key']:
                if isinstance(row.get(field),str):records[row[field]]=row;record_audits[row[field]]=name
        for row in walk(audit):
            name=row.get('path',row.get('local_path',row.get('local_copy')));digest=row.get('sha256')
            if not isinstance(name,str) or not isinstance(digest,str) or len(digest)!=64:continue
            path=Path(name) if name.startswith('/') else ROOT/name;identity=(str(path),digest)
            if identity not in checked:
                good=path.is_file() and sha(path)==digest;checked[identity]=good
                if not good:bad.append(dict(path=name,expected=digest))
    missing=sorted(keys-records.keys())
    if missing:issues.append('Citation keys without audit records')
    if bad:issues.append('Source identity binding failures')
    entries=[];schema=[];papers={}
    for key in sorted(keys & records.keys()):
        row=records[key];kind=row.get('kind',row.get('classification','unspecified'))
        local=[];anchors=[]
        for child in walk(row):
            for field in ['inspected_anchors','anchors','inspected','anchor']:
                if child.get(field):anchors.append(dict(field=field,value=child[field]))
            name=child.get('path',child.get('local_path',child.get('local_copy')));digest=child.get('sha256')
            if isinstance(name,str) and isinstance(digest,str) and len(digest)==64:local.append(dict(path=name,sha256=digest))
        identity=row.get('source_identity',row.get('source_identities',row.get('url')))
        if not identity and str(kind).startswith('project') and local:identity='Project-authored local artifact: '+local[0]['path']
        version=row.get('version_date',row.get('version_status',row.get('arxiv_version',row.get('updated',row.get('published')))))
        if not version and row.get('commit') and row.get('commit_date'):
            version='commit '+row['commit']+'; '+row['commit_date']
        claims=row.get('supported_claims',row.get('claims'))
        absent=[name for name,value in [('identity',identity),('version/date',version),('local hashed copy',local),('inspected anchors',anchors),('supported claims',claims)] if not value]
        if absent:schema.append(dict(citation_key=key,missing=absent,audit=record_audits[key]))
        entry=dict(citation_key=key,kind=kind,audit=record_audits[key],audit_sha256=audit_bindings[record_audits[key]],source_identity=identity,version_date=version,local_bindings=local,anchor_records=anchors,supported_claims=claims,manuscript_files=sorted(set(occurrences[key])),limitations={k:row[k] for k in ['limits','limitations','cutoff_limit','cutoff_status','adverse_findings_and_limits','scope'] if k in row})
        entries.append(entry)
        if kind=='paper' or (kind=='unspecified' and any(x['path'].startswith('docs/papers/') and x['path'].endswith('.pdf') for x in local)):
            pdfs=[x for x in local if x['path'].startswith('docs/papers/') and x['path'].endswith('.pdf')]
            if not pdfs:schema.append(dict(citation_key=key,missing=['genuine PDF path under docs/papers'],audit=record_audits[key]))
            for info in pdfs:
                path=ROOT/info['path']
                if info['path'] in papers:continue
                proc=subprocess.run(['pdfinfo',str(path)],text=True,capture_output=True)
                pages=re.search(r'^Pages:\s+(\d+)',proc.stdout,re.M)
                good=path.read_bytes().startswith(b'%PDF-') and proc.returncode==0 and bool(pages)
                named=bool(re.search(r' .+\(\d{4}\)\.pdf$',path.name))
                papers[info['path']]=dict(sha256=info['sha256'],valid_pdf=good,pages=int(pages[1]) if pages else None,naming_pattern=named)
                if not good or not named:issues.append('Scholarly PDF identity or naming issue: '+info['path'])
    if schema:issues.append('Traceability schema requires contextual reconciliation')
    supplementary=[]
    supplement=OUT/'supplemental-source-support.json'
    if supplement.exists():
        audit_bindings[str(supplement.relative_to(ROOT))]=sha(supplement)
        for row in json.loads(supplement.read_text())['sources']:
            key=row['citation_key']
            absent=[field for field in ['source_identity','version_date','local_bindings',
                    'inspected_anchors','supported_claims','scope_limits'] if not row.get(field)]
            if key not in keys or absent:
                issues.append('Invalid supplemental source record: '+key)
            primary=ROOT/row['primary_audit']
            if not primary.is_file() or sha(primary)!=row['primary_audit_sha256']:
                issues.append('Supplement primary-audit identity mismatch: '+key)
            for binding in row['local_bindings']:
                path=ROOT/binding['path']
                if not path.is_file() or sha(path)!=binding['sha256']:
                    issues.append('Supplement local-source identity mismatch: '+binding['path'])
            supplementary.append(row)
    build=json.loads((OUT/'latest-build.json').read_text())
    report=dict(status='pass' if not issues else 'review_required',issues=issues,citation_keys=len(keys),missing_citations=missing,source_bindings_checked=len(checked),source_binding_failures=bad,audit_bindings=audit_bindings,record_count=len(entries),kind_counts=dict(Counter(x['kind'] for x in entries)),scholarly_pdf_count=len(papers),scholarly_pdfs=papers,schema_findings=schema,records=entries,supplementary_reinspections=supplementary,ledger_sha256=sha(OUT/'edits.json'),build_batch=build['batch'],scope='Mechanical verification and preserved claim/anchor navigation, with separately attributed supplemental reinspections. This does not re-read every original or certify each scientific claim, cutoff entitlement or independent acceptance.')
    (OUT/'source-verification.json').write_text(json.dumps(report,indent=2)+chr(10))
    print(json.dumps({k:v for k,v in report.items() if k not in ['records','scholarly_pdfs','supplementary_reinspections']},indent=2))
    if issues:raise SystemExit(1)
if __name__=='__main__':main()

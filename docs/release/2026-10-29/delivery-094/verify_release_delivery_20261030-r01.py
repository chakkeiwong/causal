"""Verify delivery identity and scope; do not confer editorial acceptance."""
import argparse
import hashlib
import json
from pathlib import Path
import re

R = Path(__file__).resolve().parents[1]
B = R / 'docs/release/2026-10-29'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def read(p):
    return json.loads(p.read_text())

def verify(manifest):
    m=read(manifest); issues=[]; counts={}
    def require(condition,message):
        if not condition: issues.append(message)
    for path,h in m['identity_files'].items():
        p=R/path
        require(p.is_file(),f'Missing delivery identity: {path}')
        if p.is_file(): require(sha(p)==h,f'Changed delivery identity: {path}')
    counts['delivery_files']=len(m['identity_files'])
    a=read(B/'deletion-audit.json');cur=read(B/'review-currency-current.json');rev=read(B/'review-scope-current.json')
    require(a['status']=='pass' and a['edits']==292,'Current preservation not passing for292 edits')
    require(a['ledger_sha256']==sha(B/'edits.json')==m['ledger_sha256'],'Ledger identity disagrees')
    for k in ['math_removed','missing_citation_keys','missing_labels','distinct_numeric_loss','changed_protected']:
        require(not a[k],f'Preservation loss: {k}')
    require(a['checks_after_final_edit'],'Audit precedes final edit')
    require(a['protected_identities']==1607,'Protected identity count differs')
    require(a['input_reports']['full']['inherited_occurrences']==458 and a['input_reports']['full']['preserved_in_order'],'Inherited compilation order differs')
    for name,pub in a['publication'].items():
        require(pub['sha256']==m['publications'][name]['sha256']==sha(R/pub['path']),f'{name} PDF mismatch')
        require(not any(pub['warnings'].values()) and not pub['empty_pages'] and not pub['outside_pages'] and not pub['unresolved_markers'],f'{name} publication checks fail')
    require(cur['status']=='pass' and cur['numbered_chapters']==101 and cur['source_segments_checked']==523,'Context currency differs')
    for path,h in rev['basis'].items():
        require((R/path).is_file() and sha(R/path)==h,f'Current review basis changed: {path}')
    counts['current_review_basis']=len(rev['basis'])
    require(rev['portable_package_current'] and rev['numerical_package_current'],'Current review points to stale packages')
    proof=read(B/'package-verification-batch-086-r01.json');nr=read(B/'numerical-portability-batch-086-r01/result.json')
    require(proof['status']==nr['status']=='pass','Relocation did not pass')
    require(proof['package_revision']==nr['package_revision']==1,'Wrong package revision')
    for root,checksum in [(R/proof['package'],'SHA256SUMS')]:
        n=0
        for line in (root/checksum).read_text().splitlines():
            h,path=line.split('  ',1);p=root/path;n+=1
            require(p.is_file() and sha(p)==h,f'Frozen manuscript package changed: {path}')
        counts['manuscript_package_files']=n
    nm=read(R/nr['package']/'manifest.json')
    require(sha(R/nr['package']/'manifest.json')==nr['manifest_sha256'],'Numerical manifest mismatch')
    for path,h in nm['files'].items():
        p=R/nr['package']/path
        require(p.is_file() and sha(p)==h,f'Frozen numerical package changed: {path}')
    counts['numerical_package_files']=len(nm['files'])
    require(len(nm['check_groups'])==68,'Numerical group count differs')
    require(nm['reader_sha256']==m['publications']['full']['sha256'],'Numerical package reader mismatch')
    adversarial=read(B/'portability-batch-086-r01/adversarial-preservation.json')
    require(len(adversarial)==5 and all(x['returncode']!=0 for x in adversarial),'Preservation rejection tests did not pass')
    counts['preservation_rejection_tests']=len(adversarial)
    require(len(nr['tests'])==11,'Numerical test count differs')
    counts['numerical_cases']=len(nr['tests'])
    for test in nr['tests']:
        require(test['returncode']==0 if test['case']=='complete' else test['returncode']!=0,f'Unexpected numerical test outcome: {test["case"]}')
    source=read(B/'source-verification.json')
    require(source['status']=='pass' and source['build_batch']==86 and source['ledger_sha256']==m['ledger_sha256'],'Source receipt is stale')
    require(source['citation_keys']==1512 and source['source_bindings_checked']==10421 and source['scholarly_pdf_count']==294,'Source census differs')
    unique_sources={}
    for record in source['records']+source['supplementary_reinspections']:
        for binding in record['local_bindings']:
            path=binding['path'];h=binding['sha256']
            require(path not in unique_sources or unique_sources[path]==h,f'Conflicting source identity: {path}')
            unique_sources[path]=h
    for path,h in {**unique_sources,**source['audit_bindings']}.items():
        require((R/path).is_file() and sha(R/path)==h,f'Source original/audit changed: {path}')
    counts['unique_source_files']=len(unique_sources)
    counts['source_audit_files']=len(source['audit_bindings'])
    inv=read(B/'remaining-inventory.json')
    require(inv['frontier_counts']=={'inspected':91,'unread':22} and len(inv['frontier_unread'])==22,'Frontier residuals differ')
    require(len(inv['release_blockers'])==2,'Publication blockers differ')
    state=read(B/'state.json')
    for path,h in state['historical_protected'].items():
        require(sha(R/path)==h,f'Protected historical control changed: {path}')
    require(not m['release_accepted'] and not m['fresh_visual_acceptance'] and not m['independent_acceptance'],'Unsupported acceptance flag')
    for k in ['release_accepted','fresh_visual_acceptance','independent_acceptance']:
        require(not state[k],f'Unsupported live acceptance: {k}')
    counts['historical_controls']=len(state['historical_protected'])
    closure=read(B/'final-readiness-093/review-binding-closure.json')
    for row in closure['resolved']:
        ident=row['retained_identity']
        p=R/ident['path'] if 'path' in ident else R/proof['package']/ident['package_path']
        require(p.is_file() and sha(p)==row['expected_sha256'],f'Unresolved historical review: {row["recorded_path"]}')
        if 'sha256' in ident: require(ident['sha256']==row['expected_sha256'],f'Historical recorded hash differs: {row["recorded_path"]}')
    counts['historical_review_resolutions']=len(closure['resolved'])
    preview=read(B/'final-readiness-093/visual-handoff/manifest.json')
    require(preview['status']=='prepared_not_inspected' and preview['images_forwarded']==0,'Visual preparation misrepresented')
    nav=read(B/'final-readiness-093/pdf-navigation/navigation-verification.json')
    require(nav['status']=='pass' and len(nav['chapter_navigation'])==101,'Chapter navigation incomplete')
    require(not nav['referenced_labels_with_page_mismatch'],'Referenced navigation mismatch')
    counts['chapter_destinations']=len(nav['chapter_navigation'])
    return {'status':'pass' if not issues else 'fail','manifest':str(manifest.relative_to(R)),'manifest_sha256':sha(manifest),'counts':counts,'issues':issues,'scope':'Final identity,declared-scope and control-consistency verification. No new numerical reconstruction,primary-source reading,visual inspection or independent acceptance.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--manifest',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    result=verify(a.manifest.resolve());a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
    raise SystemExit(0 if result['status']=='pass' else 1)

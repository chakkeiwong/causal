from pathlib import Path
import hashlib
import importlib.util
import json
import re
from urllib.parse import urlsplit,unquote

R=Path(__file__).resolve().parents[1]
D=R/'docs/release/2026-10-30/publication-acceptance-001'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p): return json.loads(p.read_text())

def verify():
    state=load(D/'state.json');manifest=load(D/'manifest.json');issues=[]
    def check(ok,why):
        if not ok: issues.append(why)
    for path,h in manifest['files'].items():
        p=R/path;check(p.is_file() and sha(p)==h,'Changed acceptance evidence: '+path)
    oldpath=R/state['candidate_manifest'];old=load(oldpath)
    check(sha(oldpath)==state['candidate_manifest_sha256'],'Changed candidate manifest')
    spec=importlib.util.spec_from_file_location('old_delivery_verifier',R/'tools/verify_release_delivery_20261030.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    previous=module.verify(oldpath)
    expected={'Live control differs from delivery: '+p for p in state['before_controls']}
    check(set(previous['issues'])==expected,'Unexpected predecessor verification issue')
    for path,record in state['before_controls'].items():
        p=R/record['path']
        check(p.is_file() and sha(p)==record['sha256']==old['control_snapshots'][path]['sha256'],'Lost prior entrypoint: '+path)
    links=[]
    for name in list(state['before_controls'])+[state['programme'],str((D/'decision.md').relative_to(R))]:
        p=R/name;s=p.read_text()
        if '<!-- publication-acceptance:start -->' in s:
            s=s.split('<!-- publication-acceptance:start -->',1)[1].split('<!-- publication-acceptance:end -->',1)[0]
        markdown_pattern = re.escape('](') + '([^)]*)' + re.escape(')')
        for href in re.findall(markdown_pattern,s)+re.findall(r"href=['\"]([^'\"]+)['\"]",s):
            parsed=urlsplit(href)
            if parsed.scheme or not parsed.path:continue
            target=(p.parent/unquote(parsed.path)).resolve();links.append({'source':name,'href':href,'exists':target.exists()})
            check(target.exists(),'Broken current acceptance link: '+name+' -> '+href)
    search=load(D/'review-evidence-search.json')
    check(not search['parse_issues'] and not search['exact_candidate_reviews'],'Review evidence search changed')
    review=load(D/'author-critical-review.json')
    for rec in review['extracts']:check(sha(R/rec['path'])==rec['sha256'],'Changed reviewed extract: '+rec['path'])
    check(review['manuscript_changes']==review['deletions']==0,'Unaccounted manuscript edit')
    independent=load(D/'independent-ai-review/review.json')
    check(independent['decision']=='accept' and independent['blocking_findings']==0 and not independent['required_manuscript_revisions'],'Reviewer does not support acceptance')
    check(independent['reviewer']['independent_of_edits'] and bool(independent['reviewer']['ai_provider_limitation']),'Reviewer independence or AI limits omitted')
    check(sha(D/'independent-ai-review/review.md')==independent['review_md_sha256'],'Independent review text changed')
    check(sha(D/'independent-ai-review/review.json')==state['reviewer_report']['sha256'],'Independent review binding differs')
    check('IR-01 is resolved' in (D/'independent-ai-review/errata-verification.md').read_text(),'Erratum not confirmed by reviewer')
    findings=load(D/'findings-disposition.json')
    check(findings['unresolved_blocking_findings']==0 and findings['required_manuscript_revisions']==0,'Unresolved blocking finding')
    check(any(x['id']=='IR-01' and x['status']=='resolved_by_publication_errata' for x in findings['findings']),'Source locator correction missing')
    visual=independent['visual_review']
    check(visual['status']=='accept_sampled_visual_presentation' and not visual['every_page_inspected'],'Visual scope misrepresented')
    check(visual['preview_count']==len(visual['previews'])==6 and visual['combined_image_url_chars']<2000000,'Visual review exceeds declared budget')
    for item in visual['previews']:
        check(item['visual_status']=='inspected_pass_sample_only' and bool(item['observation']),'Visual observation absent')
        check(sha(R/item['preview'])==item['sha256'],'Inspected image changed')
    for item in independent['source_checks']:check(sha(R/item['source'])==item['sha256'],'Reviewer primary source changed')
    for key,item in state['publication_copies'].items():
        check(sha(R/item['path'])==item['sha256']==independent['pdfs'][key]['sha256']==sha(R/item['byte_identical_reviewed_candidate']),'Publication copy differs from reviewed PDF')
    check(all(state[k] for k in ['release_accepted','fresh_visual_acceptance','independent_acceptance']),'Acceptance disposition inconsistent')
    check(not any(state[k] for k in ['human_peer_review','external_X01_acceptance','bank_acceptance','all_pages_visually_reviewed']),'Unsupported external or exhaustive acceptance')
    check(state['status']=='publication_accepted_in_independent_ai_review_scope','Incorrect accepted scope')
    preservation=load(D/'preservation-check.json')
    check(preservation['status']=='pass' and preservation['manuscript_edits_this_continuation']==preservation['deletions_this_continuation']==0,'Preservation check incomplete')
    for filename in ['historical-check.stdout.json','scientific-check.stdout.json']:
        check(load(D/filename)['status']=='pass','Programme check failed: '+filename)
    result={'status':'fail' if issues else 'pass','scope':'Identity, preservation, actual separately attributed AI-review evidence, resolved findings, sampled visual observations and current publication controls. Validates evidence consistency; does not independently certify all mathematics or human/institutional acceptance.','manifest':str((D/'manifest.json').relative_to(R)),'manifest_sha256':sha(D/'manifest.json'),'files_checked':len(manifest['files']),'local_links_checked':len(links),'predecessor_counts':previous['counts'],'expected_live_control_successions':len(expected),'issues':issues,'links':links,'publication_accepted':True,'acceptance_scope':state['independent_acceptance_scope'],'sampled_visual_pages':6}
    (D/'verification.json').write_text(json.dumps(result,indent=2)+chr(10))
    print(json.dumps({k:v for k,v in result.items() if k!='links'}))
    return not issues

if __name__=='__main__': raise SystemExit(0 if verify() else 1)

"""Preserve failed build and create a line-break-only successor."""
import json
from pathlib import Path
from prepare_openai_publication_20261028 import ROOT,T,replace,save,ref
from prepare_followup_program_20261028 import write
DAY=ROOT/'docs/program/execution/2026-10-28'

def main():
    old=DAY/'boundary-profile-review-v1';new=DAY/'boundary-profile-review-v2';assert not new.exists();new.mkdir()
    write(old/'reader-build-consumed.json',dict(actual_exit_code=1,session_id=66854,failure='50.83766pt overfull hbox from unbroken server commit identifier; no canonical publication occurred',log=ref(old/'reader-build.log','Actual failed build'),next_action='Create preserving successor with explicit allowable line break in commit identifier.'))
    for name in ['source-audit.json','exact-results.json','mathematical-review.json','sponsor-addition.md']:(new/name).write_bytes((old/name).read_bytes())
    text=(old/'development.tex').read_text();needle='d3c846f8b0279e79b0e3a960a7575fde6920e9df';assert text.count(needle)==1
    (new/'development.tex').write_text(text.replace(needle,needle[:20]+r'\allowbreak{}'+needle[20:]))
    for name in ['copyedit-review.json','plan-review.json','review.json']:
        obj=json.loads((old/name).read_text());obj['evidence']=[ref(new/Path(x['path']).name,x.get('anchor','Reviewed successor')) if Path(x['path']).parent==Path(str(old.relative_to(ROOT))) and (new/Path(x['path']).name).exists() else x for x in obj['evidence']]
        obj['layout_repair']=dict(change='Allow a line break in printed commit hash; no claim or identity change',failure=ref(old/'reader-build-consumed.json','Preserved failure'))
        write(new/name,obj)
    mapping={'boundary-profile-review-v1':'boundary-profile-review-v2','boundary-profile-reader-v1':'boundary-profile-reader-v2','sponsor-boundary-profile-v1':'sponsor-boundary-profile-v2','causal_proposal_boundary_profile_reviewed_v1_2026-10-28':'causal_proposal_boundary_profile_reviewed_v2_2026-10-28','sponsor_proposal_boundary_profile_reviewed_2026-10-28':'sponsor_proposal_boundary_profile_reviewed_v2_2026-10-28'}
    for kind in ['build','publish']:
      for doc in ['reader','sponsor']:mapping[f'{kind}_boundary_profile_{doc}_20261028']=f'{kind}_boundary_profile_{doc}_v2_20261028'
    for kind in ['build','publish']:
      for doc in ['reader','sponsor']:save(f'{kind}_boundary_profile_{doc}_v2_20261028.py',replace((T/f'{kind}_boundary_profile_{doc}_20261028.py').read_text(),mapping))
    print('Failed attempt preserved; four successor scripts and line-break-only source prepared.')

if __name__=='__main__':main()

"""Preserve failed source/build and create an explicitly corrected successor."""
import json
from pathlib import Path
import review_panel_runtime_contracts_20261029 as review
from publish_latent_r_review_v2_20261013 import ref,write
ROOT=Path(__file__).resolve().parents[1];DAY=ROOT/'docs/program/execution/2026-10-29';TOOLS=ROOT/'tools'


def main():
    old=DAY/'panel-runtime-semantics-v1';new=DAY/'panel-runtime-semantics-v2';assert not new.exists();new.mkdir()
    for name in ['source-plan.json','dispatch-source-plan.json','additional-source-plan.json','exact-results.json','constructed-r-exit.json','constructed-r-result.txt','sponsor-addition.md']:
        (new/name).write_bytes((old/name).read_bytes())
    text=(old/'development.tex').read_text();assert text.count('bind_rows')==1
    (new/'development.tex').write_text(text.replace('bind_rows',r'\texttt{bind\_rows}'))
    failure=DAY/'panel-runtime-publication-v1/reader-build-exit.json';assert json.loads(failure.read_text())['actual_exit_code']==1
    write(new/'repair-review.json',dict(status='reviewed_correction',cause='Unescaped bind_rows identifier caused LaTeX Missing$ on first pass; no PDF produced.',repair='Escape only identifier in new immutable source and publish newv2 artifacts; preserve failedv1inputs/logs.',
        evidence=[ref(failure,'Actual build failure'),ref(old/'review.json','Original source review'),ref(old/'development.tex','Original text'),ref(new/'development.tex','Corrected text'),ref(Path(__file__),'Repair logic')],awards_acceptance=False))
    write(new/'plan-review.json',dict(status='reviewed',steps=['Preserve failedv1 source and compilation.','Escape one identifier; authenticate unchanged claims and references.','Compile and verify v2 preserving paired successor.'],evidence=[ref(new/'repair-review.json','Specific correction'),ref(old/'plan-review.json','Original reviewed scope')],awards_acceptance=False))
    review.BASE=new;review.main()
    mappings={
        'build_panel_runtime_reader_20261029.py':'build_panel_runtime_reader_v2_20261029.py',
        'publish_panel_runtime_reader_20261029.py':'publish_panel_runtime_reader_v2_20261029.py',
        'build_panel_runtime_sponsor_20261029.py':'build_panel_runtime_sponsor_v2_20261029.py',
        'publish_panel_runtime_sponsor_20261029.py':'publish_panel_runtime_sponsor_v2_20261029.py',
        'review_panel_runtime_chapters_20261029.py':'review_panel_runtime_chapters_v2_20261029.py',
        'refresh_panel_runtime_program_20261029.py':'refresh_panel_runtime_program_v2_20261029.py',
        'execute_panel_runtime_publication_20261029.py':'execute_panel_runtime_publication_v2_20261029.py',
        'continue_panel_runtime_publication_20261029.py':'continue_panel_runtime_publication_v2_20261029.py',
        'finish_panel_runtime_publication_20261029.py':'finish_panel_runtime_publication_v2_20261029.py',
    }
    for source,dest in mappings.items():
        s=(TOOLS/source).read_text()
        for a,b in mappings.items():s=s.replace(a.removesuffix('.py'),b.removesuffix('.py'))
        for stem in ['panel-runtime-reader','sponsor-panel-runtime','panel-runtime-semantics','panel-runtime-chapters','program-refresh-panel-runtime','panel-runtime-publication']:
            s=s.replace(stem+'-v1',stem+'-v2')
        s=s.replace('panel_runtime_reviewed_v1_2026-10-29','panel_runtime_reviewed_v2_2026-10-29')
        p=TOOLS/dest;assert not p.exists();p.write_text(s)
    from run_followup_program_20261028 import append
    q=DAY/'followup-runtime-v15';p=q/'repair-checkpoint.json'
    write(p,dict(task='PANEL.RUNTIME.PUBLICATION',awards_acceptance=False,next_action='Use runtime publicationv2tools; v1compile failure retained, corrected sourcev2review passes.',evidence=[ref(new/'repair-review.json','Reviewed narrow correction'),ref(new/'review.json','Revalidated source claims')]))
    append('checkpoint','PANEL.RUNTIME.PUBLICATION',str(p.relative_to(ROOT)),ROOT,q)
    print('Corrected immutable runtime source and publicationv2tools prepared.')


if __name__=='__main__':main()

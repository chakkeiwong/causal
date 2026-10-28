"""Create explicit runtime publication successors without changing bound predecessors."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
TOOLS=ROOT/'tools'


def main():
    s=(TOOLS/'refresh_panel_inference_program_20261029.py').read_text()
    s=s.replace('panel-inference-reader','panel-runtime-reader').replace('sponsor-panel-inference','sponsor-panel-runtime')
    s=s.replace('panel-inference-contracts','panel-runtime-semantics').replace('program-refresh-panel-inference','program-refresh-panel-runtime')
    s=s.replace("prior=PRIOR_DAY/'program-refresh-panel-estimators-v1/remaining-operations.json'","prior=DAY/'program-refresh-panel-inference-v1/remaining-operations.json'")
    s=s.replace("ref(PRIOR_DAY/'panel-estimator-delivery-v1/push-verification.json'","ref(DAY/'panel-inference-delivery-v2/push-verification.json'")
    s=s.replace('760468e0ef5a9445fb3b7f48dd0a41b7c6033c2c','24fe7658044ebfa28b9cd726aca4a5da19143891')
    s=s.replace('continuation-handoff-v3','continuation-handoff-v4')
    mapping={'1,451':'1,453','1,449':'1,451','1,126':'1,130','1,122':'1,126'}
    s=re.sub('|'.join(mapping),lambda m:mapping[m.group()],s)
    s=s.replace('Selected constructor, tests and numerical delegates','Selected runtime sources and conditional witnesses')
    start=s.index("corrected_continuation='");end=s.index("')",start)
    s=s[:start]+"corrected_continuation='Retain previous panel reviews and22selected runtime file inspections plus1acquired-only baseQR file. Exact packed-bit moments and constructed installedR4.1.2 covariance fixture pass; native defaultLINPACK reachability,full header/RNG law,vctrs/custom methods and complete dependency profile remain open. Resolve exact upstream object editions,originals and rights before native calibration."+s[end:]
    start=s.index('The new addition reviews');end=s.index("'''",start)
    s=s[:start]+'''The new addition inspects 22 of 23 acquired runtime files. Development R 4.7.0,
patched-branch R 4.6.1 and installed R 4.1.2 remain distinct. A constructed
installed-R covariance fixture yields 1/4 versus 1 after ordering correction;
conditional packed-bit moments pass exact enumeration. These are not native
parglm/fastdid/BMisc qualification or coverage results.
'''+s[end:]
    start=s.index('Next pin R stats');end=s.index('Other software/reuse',start)
    s=s[:start]+'''Next qualify full header/RNG inclusion and actual finite-state sampling law;
establish default-LINPACK pivot reachability and rank-deficient covariance semantics;
pin vctrs and external reconstruction registrations, then test mixed-level results.
Resolve upstream object editions, original-paper omissions and transitive rights.
Use exact public profiles with complete failure and cost denominators before
native calibration claims. Source-review completion is not product acceptance.

'''+s[end:]
    p=TOOLS/'refresh_panel_runtime_program_20261029.py';assert not p.exists();p.write_text(s)
    s=(TOOLS/'finish_panel_inference_publication_20261029.py').read_text()
    s=s.replace('PANEL.INFERENCE.PUBLICATION','PANEL.RUNTIME.PUBLICATION').replace('panel-inference','panel-runtime')
    s=s.replace('panel-runtime-contracts-v1','panel-runtime-semantics-v1').replace("'reader-finalize'","'reader-build'")
    a=s.index('    failed=json.loads');b=s.index('    reader=json.loads',a);s=s[:a]+s[b:]
    s=s.replace('continuation-handoff-v3','continuation-handoff-v4').replace('1449reader and1122sponsor','1451reader and1126sponsor')
    s=s.replace(' Label-report failure retained and repaired.',' Full runtime limits retained.')
    p=TOOLS/'finish_panel_runtime_publication_20261029.py';assert not p.exists();p.write_text(s)
    print('Created runtime master refresh and finite publication completion successors.')


if __name__=='__main__':main()

"""Prepare reviewed finite work packets without changing historical obligations."""
import json,subprocess
from pathlib import Path
from run_followup_program_20261028 import ROOT,BASE,load,view


def ref(p,anchor):
    import hashlib
    return dict(path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),anchor=anchor)


def write(p,d):
    assert not p.exists(),p;p.write_text(json.dumps(d,indent=2)+chr(10))


def main():
    assert not BASE.exists();BASE.mkdir()
    source=ROOT/'docs/program/execution/2026-10-28/program-refresh-delegate-contract-v1'
    assert (source/'remaining-operations.json').exists()
    report=subprocess.check_output(['python3','tools/test_followup_program_20261028.py'],cwd=ROOT,text=True)
    test=json.loads(report);assert test['status']=='pass';write(BASE/'test-report.json',test)
    tasks=[]
    specs=[
      ('GAP.ROUTES',[], 'Reconcile all150nonpassing obligations into precise successor routes,local blockers and later qualification without changing historical outcomes.', ['All150ids retained exactly once with bound predecessor action.','Proposal research and later native/bank qualification are separated; blocked routes remain local.'], 'gap-routes.json'),
      ('L6.PROFILES',[], 'Review bounded named service/model/deployment and migration profiles against acquired evidence; record exact missing originals and permitted next routes.', ['All six named provider/client families and migration leads have explicit source/service/artifact boundaries.','No client source license is treated as service/model entitlement; no new uninspected capability or price claim.'], 'l6-profiles.json'),
      ('L1.ESSENTIALITY',[], 'Compare the14task census matrix and31unread original identities to actual chapter claims; distinguish direct gaps,edition differences and adjacent leads.', ['All14tasks and31unread identities accounted for; title metadata alone does not establish dispensability.','Exact source/edition restrictions retained; scoped current-claim support and full-frontier coverage distinguished.'], 'l1-essentiality.json'),
      ('SOFTWARE.TAILS',[], 'Resolve the exact source/search/rights worklist behind98inconclusive software cells and six unresolved reuse decisions; retain explicit acquisition limits.', ['All98inconclusive software cells and six unresolved reuse decisions traced to current artifacts.','Existing acquired/inspected work is not reset; next permitted route or concrete local dependency is recorded.'], 'software-tails.json'),
      ('FOLLOWUP.DISPATCH',['GAP.ROUTES','L6.PROFILES','L1.ESSENTIALITY','SOFTWARE.TAILS'], 'Review the completed work packets and install bounded next executable source/review tasks; do not stop at this phase boundary.', ['Every resulting ready action has an owner,exact input,output and acceptance contract or a specific local blocker.','Original acceptance outcomes remain unchanged and no global blockage inferred from one route.'], 'next-contracts-review.json'),
    ]
    for key,deps,action,acceptance,out in specs:
        tasks.append(dict(id=key,depends=deps,scope='Proposal successor preparation and evidence review; no qualification awarded',action=action,acceptance=acceptance,outputs=[str((BASE/out).relative_to(ROOT))]))
    evidence=[ref(source/'remaining-operations.json','All150unresolved obligations'),ref(source/'program-review.json','Current verified reconciliation'),ref(ROOT/'tools/run_followup_program_20261028.py','New separate work queue'),ref(ROOT/'tools/test_followup_program_20261028.py','Independent-work/custody regression tests'),ref(BASE/'test-report.json','Observed tests')]
    contract=dict(schema_version=1,awards_acceptance=False,canonical_obligations=376,tasks=tasks,evidence=evidence,cutoff='2026-10-07T15:59:59Z',policy=['No alteration of prior operation contracts or outcomes.','Task dependency means performed reviewed output,not capability pass.','Original controller prerequisites still govern any actual chapter/operation acceptance.','No unattended worker or concurrent canonical mutation.','No phase boundary is a permission or completion gate.'])
    write(BASE/'contracts.json',contract)
    write(BASE/'plan-review.json',dict(status='pass',findings=['Original ready count zero is explained by exclusion of recorded results.','Four independent packets have no mutual dependencies; blocked or inconclusive work cannot strand independent packets.','Custody,sequence,exact outputs and criterion completeness are enforced.','The extension cannot award acceptance; canonical controller checks remain mandatory.'],evidence=evidence+[ref(BASE/'contracts.json','Reviewed work contracts')],limitations=['Queue schedules active-agent work; does not execute autonomous research.','Broader original-operation successors still need their explicit contract review.']))
    print(json.dumps(view(load()),indent=2))


if __name__=='__main__':main()

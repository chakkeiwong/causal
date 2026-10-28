"""Resume scoped delivery after preserving and repairing two mutable EOFs."""
import json,subprocess
from pathlib import Path
import recover_fixture_java_delivery_20261028 as delivery
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write
ROOT=delivery.ROOT
BASE=ROOT/'docs/program/execution/2026-10-28/panel-design-delivery-v2'
PRIOR=BASE.with_name('panel-design-delivery-v1')


def main():
    assert not BASE.exists()
    old=json.loads((PRIOR/'delivery-plan.json').read_text());verify_bindings(old)
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==old['parent']
    events=[json.loads(s) for s in (PRIOR/'delivery-sequence.jsonl').read_text().splitlines()]
    assert [(e['step'],e['actual_exit_code']) for e in events]==[('stage-publication',0),('authored-whitespace-check',2)]
    failure=(PRIOR/'authored-whitespace-check.log').read_text().splitlines()
    assert failure==['docs/program/execution/current-program.md:101: new blank line at EOF.','docs/program/master-live.md:63: new blank line at EOF.']
    BASE.mkdir();repairs=[];changed={}
    for rel in ['docs/program/execution/current-program.md','docs/program/master-live.md']:
        p=ROOT/rel;snapshot=BASE/('before-'+p.name);snapshot.write_bytes(p.read_bytes())
        before=ref(p,'Preserved pre-repair mutable bytes')
        p.write_text(p.read_text().rstrip()+chr(10))
        after=ref(p,'Only final blank line removed')
        repairs.append(dict(original_path=before['path'],original_sha256=before['sha256'],historical_copy=ref(snapshot,'Exact original delivery-plan bytes'),replacement=after))
        changed[rel]=after
    paths=[changed.get(x['path'],x) for x in old['paths']]
    paths += [ref(Path(__file__),'Exact narrow recovery tool')]
    paths += [ref(p,'Preserved failed delivery record') for p in PRIOR.iterdir() if p.is_file()]
    paths += [ref(p,'Preserved pre-repair mutable text') for p in BASE.glob('before-*')]
    plan=dict(parent=old['parent'],paths=paths,repairs=repairs,
        original_plan=ref(PRIOR/'delivery-plan.json','Immutable predecessor with historical live-file bindings'),
        scope='Only two live EOF fixes; all original publication and canonical acceptance bytes preserved.',
        historical_binding_policy='The two original live-file bindings refer to exact before-* snapshots; never claim they match the normalized live files.',
        visual_acceptance=False,final_acceptance=False)
    write(BASE/'delivery-plan.json',plan)
    for item in paths:verify_bindings(item)
    delivery.BASE=BASE
    delivery.step('stage-normalized-live-files',['git','add','-f','--',*changed, str(Path(__file__).relative_to(ROOT)),str(PRIOR.relative_to(ROOT)),str((BASE/'delivery-plan.json').relative_to(ROOT)),*[str(p.relative_to(ROOT)) for p in BASE.glob('before-*')]])
    delivery.step('authored-whitespace-check',['git','diff','--cached','--check','--','tools','docs/program/master-live.md','docs/program/execution/current-program.md','docs/mission-control.md'])
    staged=set(subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=ROOT).decode().split(chr(0)))-{''}
    allowed={x['path'] for x in paths}|{str((BASE/'delivery-plan.json').relative_to(ROOT))}
    assert staged<=allowed,sorted(staged-allowed)
    dirty=set(subprocess.check_output(['git','diff','--name-only','-z'],cwd=ROOT).decode().split(chr(0)))-{''}
    assert not dirty&allowed
    write(BASE/'staged-review.json',dict(status='pass',staged_count=len(staged),exact_worktree_versions=True,
        evidence=[ref(BASE/'delivery-plan.json','Narrow successor delivery'),ref(BASE/'authored-whitespace-check.log','Successful real check')],
        original_failure_preserved=True,visual_acceptance=False,final_acceptance=False))
    delivery.step('stage-delivery-records',['git','add','-f','--',str(BASE.relative_to(ROOT))])
    delivery.step('git-commit',['git','-c','user.name=Codex','-c','user.email=codex@users.noreply.github.com','commit','-m','Recover panel research and integrate baselines, multiple events and stacked weights'])
    delivery.step('git-push',['git','push'])
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    remote=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT,text=True).strip()
    assert head==remote
    write(BASE/'push-verification.json',dict(status='pass',commit=head,origin_main=remote,visual_acceptance=False,final_acceptance=False))
    print(json.dumps(dict(pushed=head)),flush=True)


if __name__=='__main__':main()

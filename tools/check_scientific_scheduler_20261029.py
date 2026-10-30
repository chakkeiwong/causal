"""Focused scientific scheduling regressions: unrelated blockers and dependency cycles."""
from pathlib import Path
import copy
import json
from scientific_program import eligible_tasks,task_issues
ROOT=Path(__file__).resolve().parents[1]
def task(id,status='ready',deps=None,blockers=None):
    return dict(id=id,stream='S01',question='Which evidence changes the decision?',action='Execute scoped test',required_result='Checked comparison',status=status,depends_on=deps or [],blockers=blockers or [],evidence=['docs/program/master-live.md'],priority=1)
def main():
    base=dict(items=[dict(id='S01')],tasks=[task('blocked','blocked',blockers=['External adjudicator']),task('independent'),task('waiting',deps=['blocked']),task('complete','complete'),task('dependent',deps=['complete'])])
    assert {x['id'] for x in eligible_tasks(base)}=={'independent','dependent'}
    assert not task_issues(base)
    bad=copy.deepcopy(base);bad['tasks'][1]['depends_on']=['waiting'];bad['tasks'][2]['depends_on']=['independent']
    assert any('cycle' in x for x in task_issues(bad))
    missing=copy.deepcopy(base);missing['tasks'][1]['depends_on']=['absent']
    assert any('unknown dependency' in x for x in task_issues(missing))
    evidence=copy.deepcopy(base);evidence['tasks'][3]['evidence']=[]
    assert any('lacks evidence' in x for x in task_issues(evidence))
    report=dict(status='pass',cases=['Independent work bypasses unrelated blocked task','Completed dependency enables work','Cycles rejected','Unknown dependency rejected','Completion without evidence rejected'])
    (ROOT/'docs/scientific-gap-closure/2026-10-29/scheduler-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()

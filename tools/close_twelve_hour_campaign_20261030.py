"""Record completed timebox without changing the accepted publication overlay."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil
R=Path(__file__).resolve().parents[1]
O=R/'docs/twelve-hour-closure/2026-10-29'
A=R/'docs/release/2026-10-30/publication-acceptance-001'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(p):return dict(path=str(p.relative_to(R)),sha256=sha(p))
def save(p,x):p.write_text(json.dumps(x,indent=2)+chr(10))
def main():
    now=datetime.now(timezone.utc).isoformat();end=O/'completion.json';assert not end.exists()
    state=read(A/'state.json');assert state['status']=='publication_accepted_in_independent_ai_review_scope'
    for v in state['publication_copies'].values():assert sha(R/v['path'])==v['sha256']
    focused=read(O/'partial-publication/revision-2/publication-1/verification.json');assert focused['status']=='pass'
    corrected=read(O/'partial-recovery-corrected-summary.json');assert corrected['release_reconstruction_agrees']
    assert read(O/'partial-net-decision-check.json')['status']=='pass'
    review=dict(recorded_utc=now,status='complete_in_declared_author_scope',
      main_publication=state['publication_copies']['reader'],focused_reading=focused,
      integrated_section='14.5, physical PDF pages109–114',
      source_ledgers=[bind(O/('partial-'+n+'.json'))for n in ['source-support','citation-metadata','backward-snowball','forward-snowball','claim-support','omissions-risk']],
      mathematical_review=['Binary sharp bounds attained by unresolved-arm completions; invitation q positive and fixed completion law required.',
        'Inverse-invitation endpoints unbiased; range1/q and independent summands give whole-set Hoeffding bound via two adverse tails.',
        'No normal-band finite-sample guarantee and no transfer to unstable outcomes or unbounded longitudinal rewards.',
        'Gamma27/76 is historical mean drift, not the package nonresponse-mixture delta.'],
      numerical_evidence=[bind(O/'partial-recovery-attempt-1/independent-check.json'),bind(O/'partial-recovery-corrected-summary.json'),bind(O/'partial-net-decision-check.json'),bind(R/'docs/release/2026-10-29/partial-recovery-073/exact-witnesses.json')],
      visual=dict(revision1_pdf=bind(R/'docs/causal_banking_selective_recovery_2026-10-30.pdf'),revision1_pages=list(range(1,9)),integrated_pages=list(range(109,115)),
        observations='Inspected equations,tables,figure,citations and page transitions. No clipping or overlap detected in viewed pages.',
        revision2='Rendered text,reference and all-page bounds verified. No fresh image inspection; inherited visual observations are not relabelled as a revision2 verdict.',
        tool_use_failure='Closeout forwarded multiple images/contact sheets before reading the parent AGENTS image restrictions. This exceeded the six-preview rule. No further images were requested after discovery; future recovery must read parent instructions first.'),
      failures_and_repairs=['One summary-writing command had an escaped-newline syntax error before mutation; corrected command wrote separate derived summaries.',
        'Initial large patch had an invalid hunk and made no file change; raw-template patch succeeded.',
        'Geometry parser encountered PDF control characters; filtered invalid XML control characters while preserving raw extraction.',
        'Revision1 used the earlier release treatment; revision2 extracts frozen batch086 final text and retains independently checked net-benefit counts. Both PDFs preserved.'],
      limits=['No native attrition run','No bank data or prices','No exhaustive source-survey claim','Accepted main reader review is separately attributed; focused extract does not inherit independent acceptance automatically.'])
    save(O/'partial-author-review.json',review)
    report=bind(O/'final-report.md')
    completion=dict(status='timebox_complete_with_residual_gaps',started_utc='2026-10-29T15:00:01Z',deadline_utc='2026-10-30T03:00:01Z',closeout_completed_utc=now,
      deadline_overrun_disclosed=True,reason='Already-underway study and publication reconciliation finished after deadline; no new simulation campaign launched in final closeout.',
      main_publication=state['publication_copies']['reader'],sponsor=state['publication_copies']['sponsor'],focused_reading=focused,
      acceptance_decision=bind(A/'decision.md'),acceptance_scope=state['publication_acceptance_scope'],
      remaining_counts=read(R/'docs/scientific-gap-closure/2026-10-29/remaining-inventory.json')['current_frontier_counts'],
      final_report=report,partial_review=bind(O/'partial-author-review.json'),
      all_research_gaps_closed=False,bank_product_qualified=False,external_human_acceptance=False,
      publication_sources_changed=False,commit_or_push=False,next='No further automatic campaign. Follow the concrete scoped next actions in final-report.md; preserve the accepted reader and existing source/experiment identities.')
    save(end,completion)
    cp=O/'checkpoint.json';shutil.copyfile(cp,O/'checkpoint-before-closeout.json');c=read(cp)
    c.update(status='timebox_complete_with_residual_gaps',updated_utc=now,last_completed='Selective-recovery study reconciled with accepted integrated publication; focused extract and final gap report delivered.',next=completion['next'],
      completion=bind(end),publications={'full':completion['main_publication'],'sponsor':completion['sponsor'],'short':focused},
      active_work=None,completed_work={'partial_recovery':bind(O/'partial-author-review.json')})
    c['do_not_repeat'].append('Completed partial-recovery2000datasets/8000ratecells;derived empty-set correction and financial thresholds verified without rerunning simulations.')
    save(cp,c)
    pp=R/'docs/program/scientific-priorities.json';shutil.copyfile(pp,O/'priorities-before-closeout.json');p=read(pp);a=p['active_twelve_hour_campaign']
    a.update(status='timebox_complete_with_residual_gaps',completed_utc=now,last_completed=c['last_completed'],last_evidence=str(end.relative_to(R)),reader=completion['main_publication'],short_study=focused,frontier_current=completion['remaining_counts'],next=completion['next'],final_report=report)
    save(pp,p)
    plan=R/'docs/program/twelve-hour-closure-2026-10-29.md';shutil.copyfile(plan,O/'plan-before-closeout.md')
    old=plan.read_text();heading,rest=old.split(chr(10),1)
    plan.write_text(heading+chr(10)+'''
## Terminal status: completed timebox, residual gaps retained

The authorized twelve-hour window ended at30October2026,03:00:01UTC
(11:00:01Asia/Shanghai). Final closeout finished after that deadline.
The integrated monograph is now the accepted publication copy linked in the
[final report](../twelve-hour-closure/2026-10-29/final-report.md).
Acceptance is scoped independent AI publication review, not human or bank
qualification. The partial-recovery study is complete; the22 unread frontier
originals and other scientific/prototype obligations remain explicit.
No further research campaign is automatically active. The original plan below
is retained as the execution contract. See the final report for results,
evidence, actual failures and concrete next actions.

'''+rest)
    rp=O/'README.md';shutil.copyfile(rp,O/'README-before-closeout.md')
    rp.write_text('''# Completed twelve-hour campaign

The current main reader is the [published monograph](../../causal_banking_publication_2026-10-30.pdf), with its [sponsor](../../causal_banking_sponsor_publication_2026-10-30.pdf) and [errata](../../release/2026-10-30/publication-acceptance-001/errata.md).

[Final results and remaining gaps](final-report.md) · [Completion record](completion.json) · [Eight-page recovery extract](../../causal_banking_selective_recovery_v2_2026-10-30.pdf).

The timebox and closeout are complete. The scoped AI publication acceptance does not establish a generally qualified product. Earlier entries below preserve the progression and their historical counts/statuses; they are not current continuation instructions.

'''+rp.read_text())
    print(json.dumps(dict(status=completion['status'],main=completion['main_publication'],focused=focused['path'],report=report['path'],accepted_publication_unchanged=True)))
if __name__=='__main__':main()

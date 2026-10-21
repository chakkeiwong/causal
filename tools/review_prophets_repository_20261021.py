#!/usr/bin/env python3
"""Record pinned source inspection and a bounded saved-result reconciliation."""
import json
from pathlib import Path
import prophets_repository_reference_20261021 as exact
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT,BASE,FILES=exact.ROOT,exact.BASE,exact.FILES
LIMITS=[
 'Static inspection and arithmetic over saved public results; no downloaded code or model execution.',
 'Selected commit predates cutoff but is not authenticated as the exact experiment runner revision.',
 'Stored-label accuracy is distinct from scientific reference correctness.',
 'SC chain votes, error annotations, provider request records and total costs remain incomplete.',
 'No independent, rendered visual, bank or runtime acceptance; overall census stays57 inspected/56 unread.']


def main():
    assert not (BASE/'source-audit.json').exists()
    result=exact.calculate()
    write(BASE/'exact-results.json',result)
    selection=json.loads((BASE/'selected-files.json').read_text())
    descriptions={
      0:'Full MIT grant and2025 Rahul Shrestha copyright; inherited-data/dependency rights separate.',
      1:'Paper identity, prompt references, root license and pip requirements instruction; example paths are not all consistent with tree.',
      2:'Conda osx-arm64 environment export, Python3.12 and DoWhy0.8; not a pip requirements specification.',
      3:'Entire runner: provider client plumbing, four-parameter helper/five-argument call, PoT REPL, last-token labels and recorded reasoning.',
      4:'Entire prompt module; causal prompt asserts identifiable answer; PoT illustrative data generator omits its common parent from displayed graph and contains non-Python explanatory lines.',
      5:'Entire utility module; Python-fence extraction, last yes/no token, all-row and rung scoring.',
      6:'All notebook code cells: fixed-seed sampling, greedy tree search, self-contained-world instruction, selected partial run and alternate denominator functions.',
      7:'All notebook code cells: fixed-seed sample, REPL demonstration, partial GPT-4o-mini run starting at19; not a frozen complete RQ3 replay.',
      8:'All notebook code cells: selection seed25, model calls, saved pickle paths and inconsistent selected column/model calls; outputs not executed.',
      9:'All1000 CSV records parsed: IDs, labels, query/rung counts, eight method predictions and reasoning availability; D.3 question2883 isolated.',
      10:'All1000 CSV records parsed: same IDs/labels and eight method predictions; per-question comparison and missing chain histories.',
      11:'All1000 CSV records parsed: same IDs/labels and eight method predictions; per-question comparison and missing chain histories.'}
    inspected=[]
    for i,entry in enumerate(result['authenticated_files']):
        p=ROOT/entry['local_path']
        anchor='Whole CSV; columns question_id,answer,query_type,rung and all8 method answer/reasoning pairs' if i>=9 else 'Whole selected text or notebook code cells; original bytes preserved'
        inspected.append(dict(upstream_path=entry['upstream_path'],git_blob=entry['git_blob'],
            local_copy=ref(p,anchor),finding=descriptions[i]))
    claims=[
      'Twelve selected files authenticate by byte length, SHA-256 and Git blob SHA1 against the complete pinned tree.',
      'Three result CSVs contain the same1000 unique question IDs and labels; all24 Table4 subset averages reproduce exactly against stored labels.',
      'Sample counts have138 ETT questions, not the printed137; rung counts are405 association,197 intervention,398 counterfactual.',
      'Question2883 matches AppendixD.3 facts; its unrounded formula gives -0.11217602178843015, matching stored target to1e-15. The verbal coding/notation remains inconsistent.',
      'SC5/SC10 reasoning columns are empty in every selected table; vote distributions and paper error annotations remain unreconciled.',
      'The self-consistency helper declares four arguments but the caller passes five; the helper also omits the client in its generate_completion call.',
      'Requirements is an osx-arm64 Conda export, whereas the README recommends pip -r; environment reconstruction remains unqualified.',
      'Prompt illustration generates taking-drugs and cholesterol independently conditional on assignment but displays only taking-drugs to cholesterol; it adds assumptions and uses the wrong displayed graph for that generator.',
      'Selected PoT runner passes generated text to PythonREPL; code sanitization alone is not evidence of the proposed restricted execution contract.',
      'Root MIT text is complete; inherited data/dependencies/provider terms and precise experimental revision remain separate obligations.']
    write(BASE/'omissions-register.json',dict(global_blocker=None,items=[
      dict(item='Reference truth',next_action='Inspect original CLADDER generator, labels and polarity for question2883; reconcile survival/death and counterfactual notation before relabeling.'),
      dict(item='Self-consistency votes and error categories',next_action='Recover per-chain records and question-level error annotations; selected CSVs cannot explain995/999 vote totals or60/prose50 categories.'),
      dict(item='Exact experiment revision',next_action='Bind runner commit, model snapshot, requests, seeds and outputs before claiming experiment replay; notebook fragments alone are insufficient.'),
      dict(item='Rights and environment',next_action='Review inherited dataset/dependency/provider rights and prepare a supported dependency specification before executable adoption.'),
      dict(item='Implementation',next_action='Repair call/client plumbing, parsing, assumptions and constrained runtime in an isolated prototype; qualify against public known-law and refusal cases.'),
      dict(item='Public proposal coverage',next_action='Continue56 unread originals and complementary searches; this follow-up adds no inspected-paper count.')],no_source_waivers=True))
    sources=[dict(integrated_citation_key='exec21_prophets_repo',kind='software_source',
        title='Causal reasoning repository: pinned prompts, runners and RQ3 result records',
        author='Rahul Shrestha and causal-reasoning contributors',year=2025,
        source_identity='github.com/rahulbshrestha/causal-reasoning@'+result['commit'],
        version_date='Commit23 March2025; acquired21 October2026; cutoff7 October2026',
        local_copy=ref(BASE/'selected-files.json','Pinned complete-tree selection'),
        inspected_anchors=inspected,supported_claims=claims,limitations=LIMITS),
      dict(integrated_citation_key='exec21_prophets_repo_reference',kind='project_derivation',
        title='Saved-result reconciliation and exact generator comparison for causal programs of thought',
        author='Causal banking proposal project',year=2026,source_identity='tools/prophets_repository_reference_20261021.py',
        version_date='21 October2026',local_copy=ref(ROOT/'tools/prophets_repository_reference_20261021.py','Static CSV/AST inspection and exact authored formula'),
        inspected_anchors=[ref(BASE/'exact-results.json','All method scores, pairs, counts and source identities')],
        supported_claims=['All24 Table4 subset averages reproduce against saved labels.',
          'Program/baseline discordances are141 improvements/59 regressions,152/73 and182/79 across variants.',
          'Literal prompt generator under independent noises has zero treatment effect but observational difference6/793.',
          'Exact raw D.3 probability functional agrees with stored groundtruth while coding/notation remains open.'],limitations=LIMITS)]
    write(BASE/'source-audit.json',dict(sources=sources,cutoff='2026-10-07'))
    write(BASE/'conversion-contract.json',dict(status='reference_only_not_runtime_qualified',integration_allowed=False,
        decision='Retain prompts and saved records as research references; reject unchanged executable adoption.',
        reasons=['Runner and environment defects prevent an honest immediate-replay claim.',
          'Known-law assumption and graph elicitation need explicit separate contracts.',
          'Static references remain useful for paired public evaluation after rights and truth review.'],
        required_before_execution=['Exact runner/model/environment identity and rights.',
          'Correct client plumbing, strict parsers, recorded invalid outcomes and explicit target assumptions.',
          'Restricted tool environment with independent formula checks, timeout and resource limits.',
          'Paired held-out public cases, reference adjudication and full costs.'],
        evidence=[ref(BASE/'exact-results.json','Source and saved-result findings')]))
    write(BASE/'plan-review.json',dict(status='pass',findings=claims,limitations=LIMITS,
        evidence=[ref(BASE/'plan.json','Reviewed acquisition scope'),ref(BASE/'selected-files.json','Pinned selection'),
          ref(BASE/'source-audit.json','Inspected source'),ref(BASE/'exact-results.json','Reproduced results')]))
    write(BASE/'review.json',dict(status='pass_for_scoped_static_review',findings=claims,limitations=LIMITS,
        reviewer=dict(name='Codex author/coordinator',kind='author'),model_execution=False,upstream_code_execution=False,
        evidence=[ref(BASE/n,'Reviewed bounded findings') for n in ['source-audit.json','exact-results.json','omissions-register.json','conversion-contract.json','plan-review.json']]))
    for n in ['source-audit.json','review.json']:verify_bindings(json.loads((BASE/n).read_text()))
    print(json.dumps(dict(authenticated_files=12,subset_averages_reproduced=24,unique_questions=1000,unchanged_census='57/56',runtime_admitted=False)))


if __name__=='__main__':main()

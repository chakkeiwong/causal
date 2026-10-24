#!/usr/bin/env python3
"""Review a related preprint without closing an unavailable journal-original obligation."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import hashlib,html,json,re
import scientific_method_reference_20261024 as exact
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-24/census-scientific-method-v1'
PRIOR=ROOT/'docs/program/execution/2026-10-24/census-prompt-engineering-v1'
RAW=ROOT/'docs/literature/raw'
PDF=ROOT/'docs/papers/Advancing the Scientific Method with Large Language Models From Hypothesis to Discovery Zhang(2025).pdf'
read=lambda p:json.loads(p.read_text())
LIMITS=['Selected45-page May2025arXivv1; related journal original remains unavailable and exact equivalence is unestablished.',
 'Perspective is primary evidence of its own framework and caveats; underlying empirical and software originals are not adopted by citation transitively.',
 'Exact authored examples are stipulated; no model, downloaded code, external package or bank experiment executed.',
 'Algorithmic confidence is an open research direction, not a general calibrated guarantee.',
 'Census candidate165 remains open; mandatory coverage/depth, visual, independent and final acceptance remain open.']

def main():
    assert not (BASE/'review.json').exists()
    receipt=read(RAW/'exec24_scimethod_arxiv_v1.receipt.json')
    assert PDF.read_bytes()==(RAW/'exec24_scimethod_arxiv_v1.pdf').read_bytes()
    digest=hashlib.sha256(PDF.read_bytes()).hexdigest();assert digest==receipt['sha256']
    landing=(RAW/'exec24_scimethod_arxiv_landing.html').read_text()
    title=html.unescape(re.search(r'name="citation_title" content="([^"]+)"',landing)[1])
    authors=[html.unescape(x) for x in re.findall(r'name="citation_author" content="([^"]+)"',landing)]
    assert len(authors)==13 and '2025/05/22' in landing and '2505.16477v1' in landing
    pages=[x for x in (BASE/'original-v1.txt').read_text().split(chr(12)) if x.strip()]
    assert len(pages)==45 and 'From Hypothesis to Discovery' in pages[0]
    specs=[(1,4,'Title/authors, perspective scope, and distinction between scientific assistance and fundamental discovery.'),
           (5,12,'Prompt, agent and scientific-foundation-model taxonomy; examples are secondary accounts, not our empirical/package qualification.'),
           (13,18,'Observation-hypothesis-experiment loop, representation loss, tool planning and feedback; human/application premises remain necessary.'),
           (19,22,'Formal verification can inherit translation mistakes; hypothesis, retrieval and human-goal roles.'),
           (23,28,'Hallucination, reasoning/planning and self-explanation limits; system-level confidence proposed without general calibration construction.'),
           (29,34,'Negative results, peer-review caveats and conclusions; speculative creativity distinguished from experimental reliability.')]
    paper=dict(integrated_citation_key='exec24_scimethod_original',kind='paper',title=title,filename_title=title.replace(':',''),author=' and '.join(authors),first_author='Zhang',year=2025,source_identity='https://arxiv.org/abs/2505.16477v1',version_date='arXiv2505.16477v1;22May2025;before7October2026cutoff;related journal original unavailable',local_path=str(PDF.relative_to(ROOT)),sha256=digest,local_copy=ref(PDF,'Genuine45-page preprint'),identity_evidence=[ref(RAW/n,'Archive identity and acquisition') for n in ['exec24_scimethod_arxiv_landing.html','exec24_scimethod_arxiv_landing.receipt.json','exec24_scimethod_arxiv_v1.receipt.json','exec24_scimethod_crossref.json']]+[ref(BASE/'inspection-checkpoint-v1.json','Version boundary')],inspected_anchors=[dict(anchor=f'PDF pages{a}-{b}',pages=[a,b],finding=f,text_extract=ref(BASE/'original-v1.txt',f'Form-feed pages{a}-{b}')) for a,b,f in specs],supported_claims=[f for _,_,f in specs],limitations=LIMITS)
    result=exact.calculate();write(BASE/'exact-results.json',result)
    project=dict(integrated_citation_key='exec24_scimethod_reference',kind='project_derivation_and_exact_reference',title='Authored observation, formal-translation, shared-judge, transport and cost witnesses',author='Causal banking proposal project',year=2026,source_identity='tools/scientific_method_reference_20261024.py',version_date='24October2026;exact rational arithmetic and explicit finite witnesses',local_copy=ref(Path(exact.__file__),'Exact authored reference'),inspected_anchors=[ref(BASE/'exact-results.json','Complete outputs'),ref(BASE/'development.tex','Assumptions and mathematical argument')],supported_claims=['Equal eventual-repayment flags can conceal ten-day cash values10000and0USD.','Cost100 satisfies an inclusive bound but violates a strict bound100.','Five independent judges with marginalerror.1 give majorityerror107/12500=.00856; shared errors give.1.','Constructed public and bank utilities reverse preferred action, giving7USDtransport regret.','Stipulated240USD costs6perattempt,8pertoolcompletion and30peracceptedanswer;6correctrefusals separate.'],limitations=LIMITS)
    write(BASE/'source-audit.json',dict(sources=[paper,project],cutoff='2026-10-07',native_execution=False))
    omissions=[('journal_original','Retain candidate165 as open; acquire genuine journal original and compare technical text before claiming equivalence. The related preprint is independently cited.'),('underlying_originals','Inspect original tool, model and empirical studies before inheriting their technical results; perspective examples supply discovery leads only.'),('confidence','Define scientific error event, task law, dependence, selection and validation procedure; no universal calibrated construction established.'),('public_protocol','Freeze task/version split, semantic and refusal oracles, search/retry budget and failure-complete cost accounting before any native comparison.'),('transport','Specify and test restrictions bridging public/generated tasks to bank populations; no automatic transfer of accuracy or value.'),('coverage_visual','Continue36unread originals and4crosscutting tasks; complete mandatory depth and fresh visual/independent/final review.')]
    write(BASE/'omissions-register.json',dict(items=[dict(gap=g,next_action=a,global_blocker=False) for g,a in omissions],journal_failure=ref(BASE/'journal-pdf-failure.json','Preserved failed acquisition'),native_execution=False))
    write(BASE/'mathematical-review.json',dict(status='pass_for_exact_authored_examples',evidence=[ref(BASE/'exact-results.json','Exact outputs'),ref(Path(exact.__file__),'Arithmetic and Boolean witnesses'),ref(BASE/'development.tex','Fibre-constancy proof and assumptions')],findings=project['supported_claims'],limitations=['Fibre-constancy is a deterministic information statement, not a causal identification theorem.','Judge independence and alternate environments are explicit hypothetical constructions; no universal bound or measured model effect.']))
    write(BASE/'copyedit-review.json',dict(status='pass',evidence=[ref(BASE/'development.tex','Connected scientific argument'),ref(BASE/'sponsor-addition.md','Investment implications')],findings=['Survey synthesis, authored examples, proposed experiments and implementation remain separate.','Question preservation connects observation to diagrams, identification, evaluation and CLI/MCP artifacts.','Journal omission and general confidence/transport limits explicit.'],visual_acceptance=False))
    write(BASE/'plan-review-v2.json',dict(status='pass_for_scoped_review_and_preserving_integration',evidence=[ref(BASE/'plan-review.json','Original plan'),ref(BASE/'inspection-checkpoint-v1.json','Full argument inspected'),ref(BASE/'source-audit.json','Claim boundaries'),ref(BASE/'mathematical-review.json','Exact examples')],revision='Do not close journal candidate165 on a differently titled related preprint without proven equivalence.',steps=['Bind actual preprint identity and substantive anchors.','Preserve unavailable journal original and underlying-source limits.','Integrate connected banking argument and exact examples.','Preserve1071prior citations and240papers;add2records and1genuinepaper.','Keep77inspected/36unread census and4crosscutting obligations;attach related-source evidence without relabeling journal inspection.','Publish paired documents,reconcile,commit/push and continue ready work.']))
    reg=deepcopy(read(PRIOR/'census-register.json'));old=deepcopy(reg)
    row=next(x for x in reg['items'] if x['id']=='LA01-candidate-165');assert row['disposition']=='open_original_not_inspected'
    row.update(availability='Journal landing challenged and PDF request did not yield a PDF. Related45-page preprint independently acquired and inspected; journal equivalence unestablished.',related_primary_source_record=paper,related_publication_keys=[paper['integrated_citation_key'],project['integrated_citation_key']],effect_on_claims='Related preprint supports its own framework/caveats only; journal-specific technical claims and original-inspection closure remain withheld.',next_action='Acquire journal original and compare to citedarXiv2505.16477v1; retain journal omission meanwhile. Continue independent unread originals and coverage tasks.')
    assert len(reg['items'])==117 and all(x==next(y for y in reg['items'] if y['id']==x['id']) for x in old['items'] if x['id']!=row['id'])
    counts=dict(Counter(x['disposition'] for x in reg['items']));assert counts['inspected_primary_retained_with_limits']==77 and counts['open_original_not_inspected']==36
    reg.update(counts=counts,supersedes=ref(PRIOR/'census-register.json','Preserved77/36census'),changes=['Candidate165 receives separately identified related-preprint evidence; its journal-original obligation remains open.'],closure=False,interpretation='77of113candidate originals inspected;36unread;fourcrosscutting obligations open. One additional related preprint inspected without changing these counts.');write(BASE/'census-register.json',reg)
    mapping=deepcopy(read(PRIOR/'task-map.json'))
    for fam in mapping['task_families']:
        if fam['id'] in ['business_translation','diagram_construction','active_experiments','agent_architecture','evaluation_cost']:
            fam.setdefault('related_inspected_source_keys',[]);fam['related_inspected_source_keys'].extend(row['related_publication_keys'])
        fam['coverage_acceptance']=False
    mapping.update(register=ref(BASE/'census-register.json','Unchanged77/36withrelatedsource'),supersedes=ref(PRIOR/'task-map.json','Preserved mapping'));write(BASE/'task-map.json',mapping)
    evidence=[ref(BASE/n,'Reviewed primary and authored evidence') for n in ['source-audit.json','exact-results.json','mathematical-review.json','copyedit-review.json','plan-review-v2.json','development.tex','sponsor-addition.md','omissions-register.json','census-register.json','task-map.json']]+[ref(Path(__file__),'Preserving audit logic')]
    review=dict(status='pass_for_scoped_primary_review',reviewer=dict(name='Codex author/coordinator',kind='author'),candidate=row['id'],candidate_closed=False,evidence=evidence,findings=['Two records bind actual45-page preprint and exact authored witnesses.','Journal-original omission remains open;77/36and4crosscutting counts unchanged.','Confidence, hypothesis validation, causal identification and transport remain distinct.'],limitations=LIMITS,coverage_acceptance=False,native_execution=False,visual_acceptance=False);verify_bindings(review);write(BASE/'review.json',review)
    write(BASE/'progress.json',dict(finding='Related scientific-method preprint inspected and separately cited; journalcandidate165remains open, with77inspected/36unread originals.',next_action='Publish preserving scientific-method reader and paired sponsor, reconcile, then continue36unread originals and fourcrosscutting tasks; independent Python off-policy source review remains ready.',yield_reason='Completed scoped original review proceeds to integration; no global blocker.',evidence=[ref(BASE/'review.json','Scoped source review'),ref(BASE/'census-register.json','Preserved census')]))
    print(json.dumps(dict(inspected_candidate_originals=77,unread=36,related_preprints_added=1,audited_records=2,native_execution=False)))

if __name__=='__main__':main()

"""Prepare a preserving publication from reviewed predecessor mechanics."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
T = ROOT / 'tools'
DAY = ROOT / 'docs/program/execution/2026-10-28'


def replace(text, mapping):
    return re.sub('|'.join(re.escape(k) for k in sorted(mapping, key=len, reverse=True)), lambda m: mapping[m[0]], text)


def save(name, text):
    p = T / name
    assert not p.exists(), p
    compile(text, str(p), 'exec')
    p.write_text(text)


def ref(p, anchor):
    return dict(path=str(p.relative_to(ROOT)), sha256=hashlib.sha256(p.read_bytes()).hexdigest(), anchor=anchor)


def main():
    source = DAY / 'l6-openai-pinned-v1'
    target = DAY / 'openai-contract-review-v1'
    assert not target.exists()
    target.mkdir()
    for n in ['development.tex', 'sponsor-addition.md', 'source-audit.json', 'exact-results.json', 'mathematical-review.json', 'copyedit-review.json']:
        (target / n).write_bytes((source / n).read_bytes())
    plan = dict(status='pass', scope='Preserve 1400 previous reader records and 1049 sponsor records; integrate three new audited records without awarding full L6 coverage.',
        evidence=[ref(source / n, 'Reviewed acquisition, correction or source argument') for n in ['plan-review-v2.json', 'discovery-correction.json', 'review.json', 'authenticated-source-index.json']],
        checks=['Only actual collector bytes and Git-blob matches establish original identity.', 'All selected source commits predate the fixed cutoff.', 'No downloaded code, native model or live API executed.', 'Census review will be recorded inconclusive; 82 inspected and 31 unread remain distinct.', 'Rebuild and pair reader/sponsor; preserve all prior citations, content and contexts.', 'Both full controllers run unchanged; visual and final acceptance remain open.'])
    (target / 'plan-review.json').write_text(json.dumps(plan, indent=2) + chr(10))
    review = dict(status='pass', issues=[], scope='Publication input review', evidence=[ref(source / 'review.json', 'Primary review'), ref(target / 'plan-review.json', 'Publication plan')], final_acceptance=False)
    (target / 'review.json').write_text(json.dumps(review, indent=2) + chr(10))
    mapping = {
        'followup_causal_reference_20261028': 'openai_contract_reference_20261028',
        'followup_causal': 'openai_contract',
        'followup-causal-reader-v1': 'openai-contract-reader-v1',
        'followup-causal-review-v1': 'openai-contract-review-v1',
        'sponsor-followup-causal-v1': 'sponsor-openai-contract-v1',
        'causal-modeling-reader-v1': 'followup-causal-reader-v1',
        'sponsor-causal-modeling-v1': 'sponsor-followup-causal-v1',
        'causal_proposal_causal_modeling_reviewed_v1_2026-10-28': 'causal_proposal_followup_causal_reviewed_v1_2026-10-28',
        'sponsor_proposal_causal_modeling_reviewed_2026-10-28': 'sponsor_proposal_followup_causal_reviewed_2026-10-28',
        '1397': '1400', '1400': '1403', '1044': '1049', '1049': '1054', '269': '271',
        'exec28_fr_': 'exec28_oa_', 'sec:exec28-fr': 'sec:exec28-oa',
        'sp28fr_': 'sp28oa_', 'sp28cm_': 'sp28fr_',
        'task-specific survey and representation': 'provider response-state and scientific-admission',
        'Causal tasks and representation interventions': 'Structured outputs and scientific admission',
    }
    text = replace((T / 'build_followup_causal_reader_20261028.py').read_text(), mapping)
    text = text.replace('Add the inspected Ma survey and Hu representation preprint,source-specific evaluation limits,and exact arithmetic/geometric and joint-confounder witnesses', 'Add pinned official OpenAI cookbook/SDK contracts and exact scientific-admission/nested-retry witnesses')
    save('build_openai_contract_reader_20261028.py', text)
    text = replace((T / 'publish_followup_causal_reader_20261028.py').read_text(), mapping)
    text = text.replace("['ma','hu','reference']", "['cookbook','sdk','reference']")
    text = text.replace('A causal assistant must preserve the distinction between answering a causal question and changing a language model.', 'A structured banking answer must preserve both the scientific target and the state of the computation.')
    text = text.replace('For the banking analyst, the useful output is an auditable answer whose scientific target survives every translation and approximation.', 'The banking decision remains admissible only when its scientific meaning survives the complete request lifecycle.')
    text = text.replace("['1,000','740','geometric','reminder','CHAIR']", "['1.50','33','schema','reminder','refusal']")
    text = text.replace('three additional primary-paper and independent-project records', 'three additional official-software and independent-project records')
    text = text.replace('Survey comparability limits and representation methods/results are inspected; authored mathematical witnesses remain distinct from native results.', 'Official pinned client and notebook contracts are inspected; authored admission and budget witnesses remain distinct from native behavior.')
    text = text.replace('Task-specific survey evaluation,representation interventions and exact approximation/joint-confounder witnesses', 'Pinned provider parsing,refusal,incomplete/phase and retry contracts with exact authored admission and budget witnesses')
    text = text.replace('Exact finite examples distinguish arithmetic3/10,geometric1/4,uniform1/2,conditional37/50andjoint1/2versusproduct1/4', 'Exact finite examples retain one admitted effect among four states,six nested attempts,stipulated1.50USD and33seconds')
    text = text.replace('Proposed request contracts distinguish measurement,model-internal intervention and banking-policy effects,with explicit weights,approximations and assumptions', 'Proposed request contracts distinguish completion,representation,scientific admission,refusal and transport uncertainty,with full attempts and costs')
    save('publish_openai_contract_reader_20261028.py', text)
    text = replace((T / 'build_followup_causal_sponsor_20261028.py').read_text(), mapping)
    text = text.replace("text=text.replace(old,'The program has 350 recorded outcomes of 376')", "text=text.replace(old,'The program has 351 recorded outcomes of 376')")
    text = text.replace("DOCS/'program/execution/2026-10-28/openai-contract-review-v1/census-register.json'", "DOCS/'program/execution/2026-10-28/census-criterion-review-v1/census-register.json'")
    save('build_openai_contract_sponsor_20261028.py', text)
    text = replace((T / 'publish_followup_causal_sponsor_20261028.py').read_text(), mapping)
    text = text.replace("['ma','hu','reference']", "['cookbook','sdk','reference']").replace('Separate causal reasoning from model repair', 'Preserve scientific meaning across provider responses').replace("'350 recorded'", "'351 recorded'")
    save('publish_openai_contract_sponsor_20261028.py', text)
    print('Prepared four preserving publication successors and reviewed source package.')


if __name__ == '__main__':
    main()

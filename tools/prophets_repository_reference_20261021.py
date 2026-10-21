#!/usr/bin/env python3
"""Inspect saved CSV/text/JSON as data; never import or execute upstream code."""
import ast
from collections import Counter
import csv
from decimal import Decimal
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'docs/program/execution/2026-10-21/prophets-repository-v1'
FILES = BASE/'acquisition/files-network'


def calculate():
    selection = json.loads((BASE/'selected-files.json').read_text())
    bindings = []
    for i, entry in enumerate(selection['selected']):
        suffix = entry['path'].rsplit('.', 1)[-1] if '.' in entry['path'] else 'txt'
        path = FILES/f'file-{i:02}.{suffix}'
        data = path.read_bytes()
        receipt = json.loads((FILES/f'file-{i:02}.receipt.json').read_text())
        git_blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert len(data) == entry['size'] == receipt['bytes']
        assert git_blob == entry['sha']
        assert hashlib.sha256(data).hexdigest() == receipt['sha256']
        assert receipt['status'] == 'complete_public_original'
        bindings.append(dict(upstream_path=entry['path'], local_path=str(path.relative_to(ROOT)),
            sha256=receipt['sha256'], git_blob=git_blob, bytes=len(data)))

    csv.field_size_limit(4*1024*1024)
    tables, rows_by_variant = {}, {}
    methods = ['gpt-4o', 'gpt-4o-zeroshot', 'gpt-4o-ccot',
        'gpt-4o-sc-3-chains', 'gpt-4o-sc-5-chains', 'gpt-4o-sc-10-chains',
        'gpt-4o-tot', 'gpt-4o-pot']
    published = {
        'commonsensical': [84.3,85.3,81.1,83.0,82.7,83.5,87.5,92.5],
        'anti_commonsense': [82.4,83.7,80.2,82.3,81.2,80.3,86.5,90.3],
        'nonsense': [79.3,80.7,77.4,81.3,80.8,82.3,85.3,89.6]}
    for i, variant in [(9,'commonsensical'), (10,'anti_commonsense'), (11,'nonsense')]:
        with (FILES/f'file-{i:02}.csv').open(newline='') as stream:
            rows = list(csv.DictReader(stream))
        ids = [r['question_id'] for r in rows]
        assert len(rows) == len(set(ids)) == 1000
        assert all(r['answer'] in ('yes','no') for r in rows)
        rows_by_variant[variant] = rows
        stats = {}
        for method, reported in zip(methods, published[variant]):
            correct = sum(r[method] == r['answer'] for r in rows)
            percentage = Decimal(correct)/10
            assert percentage == Decimal(str(reported)), (variant,method,percentage,reported)
            per_rung = {}
            for rung in ['1','2','3']:
                subset = [r for r in rows if r['rung']==rung]
                per_rung[rung] = dict(correct=sum(r[method]==r['answer'] for r in subset),total=len(subset))
            stats[method] = dict(correct=correct,total=1000,percentage=str(percentage),
                invalid_answers=dict(Counter(r[method] for r in rows if r[method] not in ('yes','no'))),
                reasoning_present=sum(bool(r[method+'_reasoning']) for r in rows),per_rung=per_rung)
        paired = Counter(('baseline_correct' if r['gpt-4o']==r['answer'] else 'baseline_wrong')+
            '_'+('program_correct' if r['gpt-4o-pot']==r['answer'] else 'program_wrong') for r in rows)
        tables[variant] = dict(rows=1000,unique_question_ids=1000,
            query_counts=dict(Counter(r['query_type'] for r in rows)),
            rung_counts=dict(Counter(r['rung'] for r in rows)),methods=stats,
            baseline_program_pairs=dict(paired))
    original = rows_by_variant['commonsensical']
    for variant,rows in rows_by_variant.items():
        assert [r['question_id'] for r in rows]==[r['question_id'] for r in original]
        for before,after in zip(original,rows):
            assert all(before[k]==after[k] for k in ['answer','rung','query_type','groundtruth','desc_id'])
        assert tables[variant]['query_counts']['ett']==138

    d3 = next(r for r in original if r['question_id']=='2883')
    given = ast.literal_eval(d3['given_info'])  # literal data only, no code evaluation
    probabilities = given['p(Y | X, V2)']; mediator = given['p(V2 | X)']
    effect = (Decimal(str(probabilities[0][1]))-Decimal(str(probabilities[0][0])))*(
        Decimal(str(mediator[1]))-Decimal(str(mediator[0])))
    assert abs(effect-Decimal(d3['groundtruth'])) < Decimal('1e-15')

    # Exact project derivation from the *illustrated* independent-draw generator.
    # This does not execute that generator or claim a native model result.
    p_take = (F(79,100)+F(43,100))/2
    y_take = (F(79,100)*F(54,100)+F(43,100)*F(52,100))/(2*p_take)
    y_not = (F(21,100)*F(54,100)+F(57,100)*F(52,100))/(2*(1-p_take))
    assert y_take-y_not == F(6,793)
    module = ast.parse((FILES/'file-03.py').read_text())
    helper = next(n for n in module.body if isinstance(n,ast.FunctionDef) and n.name=='cot_self_consistency')
    callers = [n for n in ast.walk(module) if isinstance(n,ast.Call) and
        isinstance(n.func,ast.Name) and n.func.id=='cot_self_consistency']
    assert len(helper.args.args)==4 and len(callers)==1 and len(callers[0].args)==5
    return dict(scope='Static source and saved-result audit; no upstream execution, new model trials or independent truth validation.',
        commit=selection['commit'],tree=selection['tree'],authenticated_files=bindings,
        tables=tables,all_24_table4_subset_averages_match=True,all_variants_same_1000_question_ids=True,
        sampled_ett_count=138,paper_sampled_ett_count=137,
        d3=dict(question_id='2883',desc_id=d3['desc_id'],info=d3['info'],question=d3['question'],
            answer=d3['answer'],stored_groundtruth=d3['groundtruth'],computed_from_unrounded_probabilities=str(effect),
            given_info=given,formal_form=d3['formal_form'],estimand=d3['estimand'],stored_reasoning=d3['reasoning'],
            disposition='Numerical stored target reconciles with step4; death/survival coding and displayed notation remain unresolved.'),
        prompt_generator=dict(scope='Authored calculation conditional on independent Bernoulli noises in the displayed generator.',
            action='taking all drugs',outcome='low cholesterol',common_parent='assigned drug',
            observational_difference=str(y_take-y_not),interventional_difference='0',
            omitted_parent='The displayed two-node graph omits assigned drug, which drives both generated variables.',
            native_execution=False),
        self_consistency_call=dict(helper_parameters=len(helper.args.args),caller_positional_arguments=len(callers[0].args),
            helper_line=helper.lineno,caller_line=callers[0].lineno,scope='Selected source mismatch; experiment runner revision remains unknown.'),
        remaining=['SC5/SC10 reasoning columns are empty; chain-vote distributions cannot be reconstructed from selected CSVs.',
            'No question-level error-category annotations in selected files resolve Table10 60/prose50.',
            'Result files do not bind provider revision, complete request logs, random seeds, token/cost records or exact runner revision.',
            'Root MIT grant does not settle inherited CLADDER, dependency, model or service rights.',
            'Do not equate correctness against stored labels with scientific reference truth.'])


if __name__=='__main__':
    print(json.dumps(calculate(),indent=2))

#!/usr/bin/env python3
"""Preserving comparison validator for current and legacy authenticated audits."""
import argparse
import importlib
import json
from pathlib import Path
from fractions import Fraction
import re

import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = controller.base.core.ROOT
run = controller.base
read = lambda p: json.loads(p.read_text())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('specification')
    args = parser.parse_args()
    specification = ROOT / args.specification
    spec = read(specification)
    base = specification.parent
    state = run.core.read(ROOT, run.core.STATE)
    graph, merged, _ = run.combined(ROOT, state)
    node = run.ledger.operation(graph, spec['operation'])
    assert node['id'].startswith('SW.COMP.') and len(node['criteria']) == 2
    assert node['id'] not in merged['execution_program']['results']
    assert not run.ledger.blockers(merged, node)
    active = state['execution_runtime']['active']
    assert active is None or active['operation'] == node['id']
    assert run.same_reader(state['reader'], spec['reader'])
    verify_bindings(spec)
    manuscript = ROOT / spec['manuscript']['path']
    text = manuscript.read_text()
    keys = {k.strip() for group in re.findall(r'\\citep?\{([^}]+)\}', text) for k in group.split(',')}
    audit_path = ROOT / spec['reader_audit']['path']
    inherited = {s['integrated_citation_key']: s for s in read(audit_path)['sources']}
    assert keys and keys <= inherited.keys()
    sources = [inherited[key] for key in sorted(keys)]
    for source in sources:
        verify_bindings(source)
        paper = source.get('kind') == 'paper' and source.get('url') and source.get('inspected')
        assert (source.get('source_identity') or paper) and source.get('version_date')
        if paper:
            original = run.core.safe(ROOT, source['local_path'])
            assert original.parent == ROOT / 'docs/papers' and original.suffix == '.pdf'
            assert run.core.sha(original) == source['sha256']
            assert original.name == f"{source['filename_title']} {source['first_author']}({source['year']}).pdf"
        # Earlier authenticated records keep inspected anchors on each primary copy.
        nested = [r for r in source.get('records', [])
                  if r.get('role') == 'inspected_primary_technical_text'
                  and r.get('source_identity') and r.get('local_copy', {}).get('anchor')
                  and r.get('local_copy', {}).get('sha256')]
        project = (source.get('kind') == 'project_analysis'
                   and source.get('code', {}).get('sha256')
                   and source.get('code', {}).get('anchor')
                   and source.get('local_copy', {}).get('anchor')
                   and source.get('local_copy', {}).get('sha256'))
        assert source.get('inspected_anchors') or source.get('anchors') or nested or project or paper
    assert len(spec['criterion_findings']) == 2
    assert all(spec['criterion_findings']) and spec['limitations']
    for anchor in spec['integrated_locations']:
        content = (ROOT / anchor['path']).read_text()
        assert anchor['literal'] in content
    results = []
    for oracle in spec['oracles']:
        module = importlib.import_module(oracle['module'])
        assert Path(module.__file__).resolve() == (ROOT / oracle['code']['path']).resolve()
        def encode_rational(value):
            if isinstance(value, Fraction):
                return str(value)
            raise TypeError(type(value).__name__)
        result = json.loads(json.dumps(module.calculate(), default=encode_rational))
        expected = read(ROOT / oracle['expected']['path'])
        if oracle.get('expected_embeds_code'):
            embedded = expected.pop('code')
            assert embedded['path'] == oracle['code']['path']
            assert embedded['sha256'] == oracle['code']['sha256']
        assert result == expected, oracle['module']
        results.append(dict(module=oracle['module'], exact_replay='pass', code=oracle['code'],
                            expected=oracle['expected']))
    assert results
    output = ROOT / node['outputs'][0]
    assert not output.exists()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(manuscript.read_bytes())
    write(base / 'source-audit.json', dict(cutoff='2026-10-07', sources=sources,
        inherited_audit=spec['reader_audit'], new_technical_sources=False,
        limitations=spec['limitations']))
    write(base / 'oracle-replay.json', dict(status='pass', results=results,
        native_execution=False, empirical_coverage=False))
    evidence = [ref(specification, 'Individually authored criterion review and exact source locations'),
        ref(manuscript, 'Connected scientific comparison'), ref(output, 'Contracted comparison'),
        ref(base / 'source-audit.json', 'Unaltered authenticated source records'),
        ref(base / 'oracle-replay.json', 'Replayed exact authored banking constructions'),
        ref(Path(__file__), 'Comparison validation; no automatic capability inference')]
    evidence += spec['evidence']
    review = dict(status='pass_for_scoped_scientific_comparison',
        reviewer=dict(name='Codex author/coordinator', kind='author'),
        operation=node['id'], scope=spec['scope'], evidence=evidence,
        findings=spec['criterion_findings'], limitations=spec['limitations'],
        integrated_locations=spec['integrated_locations'], reviewed_reader=state['reader'],
        source_coverage_complete=False, integration_allowed=False, native_execution=False,
        visual_acceptance=False, proposal_accepted=False)
    verify_bindings(review)
    write(base / 'review.json', review)
    receipt = run.ledger.receipt_template(node)
    receipt.update(outcome='pass', execution='performed', scope=spec['scope'],
        reviewer=review['reviewer'], limitations=spec['limitations'],
        original_gap_qualification=False, capabilities=[], nonexecution_reason='',
        revisit_trigger=spec['revisit_trigger'], outputs=[ref(output, 'Required comparison')],
        criteria=[dict(index=i, verdict='pass', finding=finding,
            evidence=evidence + [ref(base / 'review.json', 'Individual author review')])
            for i, finding in enumerate(spec['criterion_findings'])])
    run.validate_receipt(ROOT, merged, node, receipt, len(state['execution_program']['turns']))
    write(base / 'operation-receipt.json', receipt)
    print(json.dumps(dict(operation=node['id'], source_records=len(sources),
        exact_replays=len(results), outcome='pass', coverage_complete=False)))


if __name__ == '__main__':
    main()

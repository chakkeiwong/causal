#!/usr/bin/env python3
"""Preserve the first release; repair newline/formfeed anchor offsets in a successor."""
import json
from pathlib import Path
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/'docs/program/execution/2026-10-22/bayesian-commercial-v1'
BASE=ROOT/'docs/program/execution/2026-10-22/bayesian-commercial-v2'
read=lambda p:json.loads(p.read_text())


def main():
    assert not BASE.exists();BASE.mkdir()
    audit=read(OLD/'source-audit.json');verify_bindings(audit)
    checks=[]
    for source in audit['sources']:
        if source['kind']!='official_documentation':continue
        body=(ROOT/source['text_copy']['path']).read_text()
        lines=body.split('\n')
        for anchor in source['inspected_anchors']:
            bounds=anchor['anchor'].replace('extracted lines','').split('-')
            lo,hi=map(int,bounds)
            anchor['inspected_text']='\n'.join(lines[lo-1:hi])+'\n'
            anchor['physical_page']='\n'.join(lines[:lo-1]).count(chr(12))+1
            anchor['anchor']=f'newline-delimited extracted lines {lo}-{hi}; formfeeds retained within lines'
        combined=' '.join(a['inspected_text'] for a in source['inspected_anchors'])
        required={
            'exec22_state_stata_sspace':['maximum likelihood','time-invariant','refining step','uncorrelated','robust'],
            'exec22_state_stata_sspace_post':['estimation error','all sample','contemporaneous','prediction sample'],
            'exec22_state_stata_bayesmh':['proper posterior','frequency weight','MCSE','pseudoconvergence','functions','prior']
        }[source['integrated_citation_key']]
        for token in required:assert token in combined,token
        checks.append(dict(source=source['integrated_citation_key'],anchors=len(source['inspected_anchors']),required_tokens=required))
    write(BASE/'source-audit.json',audit)
    for name in ['development.tex','sponsor-addition.md','plan.md','plan-review.json','inherited-source-review.json',
        'exact-results.json','comparison-review.json','omissions-register.json','conversion-contract.json',
        'candidate-register.json','search-coverage.json']:
        (BASE/name).write_bytes((OLD/name).read_bytes())
    write(BASE/'anchor-repair-review.json',dict(status='pass',reviewer=dict(name='Codex author/coordinator',kind='author'),
        preserved_failure=ref(OLD/'anchor-failure.json','Observed newline/formfeed mismatch'),
        prior_audit=ref(OLD/'source-audit.json','Preserved original defective snippets'),
        corrected_audit=ref(BASE/'source-audit.json','Same source identities/bytes/claims; corrected inspected anchors'),
        checks=checks,source_identity_changes=False,scientific_claim_changes=False,
        evidence=[ref(Path(__file__),'Newline-only repair and claim-token checks')],
        limitation='This repair corrects saved anchors only; no new native, independent, visual or market-completion acceptance.'))
    prior=read(OLD/'review.json')
    successor=dict(prior)
    successor['scope']='Preserving successor to commercial state coverage, with repaired technical anchors'
    successor['evidence']=prior['evidence']+[ref(BASE/'source-audit.json','Corrected authoritative technical anchors'),
        ref(BASE/'anchor-repair-review.json','Reviewed saved-anchor repair')]
    successor['supersedes_anchor_evidence']=ref(OLD/'source-audit.json','Historical saved-anchor defect; source bytes and claims unchanged')
    write(BASE/'review.json',successor)
    write(BASE/'operation-followup.json',dict(operation='SW.CELL.bayesian_scm_state.commercial',outcome='inconclusive',
        previous_receipt=ref(OLD/'operation-receipt.json','Historical outcome preserved'),
        current_review=ref(BASE/'review.json','Corrected evidence successor'),
        failure=ref(OLD/'anchor-failure.json','Failure retained'),
        next_action='Complete the explicit market/edition/rights and missing-original obligations; use corrected source anchors.'))
    print(json.dumps(dict(status='pass',corrected_sources=len(checks),science_changed=False)))


if __name__=='__main__':main()

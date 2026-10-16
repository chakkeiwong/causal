#!/usr/bin/env python3
"""Preserve the S5 revision and bind the added covariance/coupling references."""
import json
from pathlib import Path

import s5_examples_20261017 as examples
import s5_covariance_20261017 as joint
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT, WORK = examples.ROOT, examples.BASE
BASE = WORK / 'revision-v2'


def read(path):
    return json.loads(path.read_text())


def main():
    for path in [WORK/'publication-v1/prepared-inputs.json', WORK/'primary-review.json',
                 WORK/'mathematics-review.json', WORK/'source-audit.json']:
        verify_bindings(read(path))
    exact = read(WORK/'exact-results.json')
    covariance = read(WORK/'covariance-results.json')
    assert examples.calculate() == exact and examples.separate(exact)['status'] == 'pass'
    assert joint.calculate() == covariance and joint.separate(covariance)['status'] == 'pass'
    chapter = (BASE/'chapter.tex').read_text()
    assert not [c for c in chapter if ord(c) < 32 and c not in '\n\t']
    assert chapter.count(r'\chapter{') == 1
    claims = [
        'Whole-subject two-period event vector mean and covariance follow both nine-path enumeration and separate indicator identities.',
        'The monetary variance is c^T Sigma c; dropping covariance overstates variance in the constructed law and has no universal direction.',
        'For equal starting laws, a fixed common policy/reward and uniform transition TV budgets, first-split recursion gives q=1-product(1-epsilon).',
        'A two-state absorbing-divergence witness attains the running plus terminal envelope jointly; tighter and additive totals are60 and61.2USD for stipulated budgets.'
    ]
    evidence = [ref(p,a) for p,a in [
        (WORK/'covariance-results.json','Exact covariance and tight/additive transition references'),
        (ROOT/'tools/s5_covariance_20261017.py','Separate indicator and first-split calculations'),
        (WORK/'exact-results.json','Original eight exact authored families'),
        (WORK/'draft-review-v1.json','Preserved first-draft revision findings'),
        (WORK/'publication-v1/prepared-inputs.json','Restored initial builder identity; no compiled v1 reader'),
        (BASE/'chapter.tex','Revised source, including all first-draft semantic and TeX repairs'),
        (Path(__file__),'Revision evidence binding')]]
    limits = [
        'Author review only; no independent review, upstream estimator execution or empirical qualification study.',
        'Fixed-law independent trajectories differ from a fitted observational causal estimator.',
        'Uniform TV budgets, common rewards and independent subjects are stipulated restrictions; predictive MSE does not establish them.',
        'Previous version/date, cutoff, complete-census, rights and bank-qualification limits remain.',
        'Visual acceptance remains false; no image forwarding in this continuation.'
    ]
    write(BASE/'mathematics-review.json',dict(status='pass',reviewer=dict(name='Codex author/coordinator',kind='author'),
        checks=joint.separate(covariance),original_checks=examples.separate(exact),
        findings=claims,evidence=evidence,limitations=limits,visual_acceptance=False))
    source=dict(integrated_citation_key='exec17_s5_joint_error',
        title='Joint competing-event reward covariance and sharp sequential coupling envelope',
        author='Causal banking proposal',kind='project_derivation',year=2026,
        source_identity='Project-authored finite history law and conditional kernel/reward proof',
        version_date='2026-10-17; recovered S5 successor',
        local_copy=ref(WORK/'covariance-results.json','Exact vector moments and coupling witness'),
        inspected_anchors=claims,supported_claims=claims,
        records=evidence+[ref(BASE/'mathematics-review.json','Separate author identities and proof review')],
        limitations=limits)
    write(BASE/'source-audit.json',dict(sources=[source],cutoff='2026-10-07'))
    print(json.dumps(dict(original_families=8,new_families=2,source_records_added=1,
        revision='pass_for_compilation',visual_acceptance=False)))


if __name__=='__main__':
    main()

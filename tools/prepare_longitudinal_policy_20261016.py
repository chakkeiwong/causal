#!/usr/bin/env python3
"""Prepare immutable author review, task synthesis and three citation records."""
import json
from pathlib import Path
import subprocess
import review_longitudinal_policy_20261016 as work
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT, BASE = work.ROOT, work.BASE


def main():
    primary = json.loads((BASE/'source-review.json').read_text())
    omissions = json.loads((BASE/'omissions-register.json').read_text())
    verify_bindings(primary); verify_bindings(omissions)
    assert work.exact() == json.loads((BASE/'exact-results.json').read_text())
    assert len(primary['records']) == 22 and len(primary['papers']) == 6
    write(BASE/'authoring-failure.json', {
        'stage': 'First tool call to create development.template',
        'observed_error': 'TypeError: String.raw(...) is not a function',
        'cause': 'LaTeX double-backtick quotation terminated the JavaScript template literal.',
        'effect': 'Tool evaluation failed before any patch; no manuscript artifact was created by the failed call.',
        'repair': 'Used ordinary CVAE wording and reapplied the patch successfully.',
        'source_extraction_note': 'pdftotext emitted one font-type mismatch warning; all selected nonempty text extracts were inspected.'})
    contract = {
        'status': 'proposed_not_implemented', 'integration_allowed': False,
        'scientific_request': {
            'population': 'Eligible accounts at first servicing decision;sampling frame and exclusions explicit',
            'unit': 'Account,with household/branch/calendar dependence declared',
            'target': 'Fixed-policy30-day expected net cash recovery and contrast with a frozen comparator',
            'history': 'Only information available before each decision;event/availability/decision clocks retained',
            'policy': 'History-conditioned action rule at every stage;finite messages or a versioned text-generation kernel',
            'outcome': 'Cash units,contact costs,horizon,absorbing events and missing outcomes explicit',
            'premises': ['Consistency including text-version mixture','Sequential exchangeability',
                         'Policy-support positivity','Justified assignment,retention and observation laws'],
            'estimation': 'Forward g-computation compared with independent backward recursion;qualified weighting/augmentation alternatives',
            'uncertainty': 'Sampling,nuisance,MonteCarlo,policy-selection and identification uncertainty distinguished'
        },
        'transport': 'Same scientific request and evidence identities through proposed CLI/MCP;no implicit policy changes',
        'outcomes': ['invalid_chronology','unsupported_backend','unresolved_identification',
                     'failed_support_or_diagnostics','computed_under_stated_assumptions'],
        'remedies': [
            {'finding': 'Fixed action vectors do not implement adaptive history feedback',
             'repair': 'Call frozen policy on every newly simulated history;compare with finite enumeration and backward recursion.'},
            {'finding': 'Treatment versions and local derivatives have different decision meaning',
             'repair': 'Bind text kernel and finite action;state extra assumptions before converting local effects to net decisions.'},
            {'finding': 'Unpinned model,CUDA import and option spelling',
             'repair': 'Explicit artifact acquisition,revision/device/config validation and resolved dependencies;test offline import before any upstream trial.'},
            {'finding': 'Rows may share participants and calendar dependence',
             'repair': 'Split at declared independent unit;hold out deployment calendar and keep policy-learning data separate.'},
            {'finding': 'Representation and last-state law are specific model choices',
             'repair': 'Bind actual loss,K L coefficient,scaling and noise law;test transition/representation sensitivity without asserting causal sufficiency.'},
            {'finding': 'No observed redistribution or code reuse grant',
             'repair': 'Use independent generated references;obtain applicable terms before copying into an adapter.'}
        ],
        'prototype': {
            'status': 'design_only',
            'generated_cases': ['Adaptive versus independent-action rollout','Missing retention','Unsupported action histories',
                                'Changed message mixture','Late-arriving state','Derivative reported as finite gain'],
            'reference': ref(BASE/'exact-results.json','Executed exact authored baseline'),
            'public_options': ['UCI credit histories for clocks/covariates with generated actions/responses',
                              'Freddie/Fannie mortgage clocks conditional on permitted access;not full action truth'],
            'baselines': ['Deterministic analyst workflow with same facts','Scripted assistant and frozen estimator',
                          'Optional later frozen live-model assistance under a registered protocol'],
            'acceptance': 'Predeclare target,status,unit and numerical tolerance per case;all attempts remain in denominator;no live/model accuracy inference from exact references',
            'costs': ['Formulation/review','Rights and environment closure','Embeddings','Nuisance fits',
                      'Trajectory simulation','Diagnostics/failures','Maintenance after revisions'],
            'later': 'Justify expensive bank measurement only when useful public/generated prototype evidence supports resolving an actual decision uncertainty'
        },
        'remaining_research': ['Representation sufficiency','Hidden longitudinal confounding',
                               'Uncertainty after adaptive policy selection','Useful precision under weak support',
                               'Nonignorable loss and transport to bank populations'],
        'omissions': ref(BASE/'omissions-register.json','Uninspected original,noisy search,rights and scope limits')
    }
    write(BASE/'proposed-contract.json', contract)
    template = BASE/'development.template'
    text = template.read_text().replace('§', chr(92))
    development = BASE/'development.tex'
    with development.open('x') as stream: stream.write(text)
    work.OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    assert not work.OUTPUT.exists()
    subprocess.run(['pandoc','--from=latex','--to=markdown','--wrap=auto',
                    str(development),'-o',str(work.OUTPUT)], check=True, timeout=30)
    with work.OUTPUT.open('a') as stream:
        stream.write('\n\nThis is a bounded proposal synthesis. The associated source review, original-file hashes, '
                     'candidate omissions, exact references and proposed contract are in '
                     'docs/program/execution/2026-10-16/longitudinal-policy/. No prototype or live-model performance is claimed.\n')
    def source(key, title, kind, path, claims, records, year=2026):
        return {'integrated_citation_key': key, 'title': title,
            'author': 'XMUBQ/dtr-text' if kind == 'software_primary_sources' else 'Causal banking proposal',
            'kind': kind, 'year': year,
            'source_identity': 'https://github.com/XMUBQ/dtr-text' if kind == 'software_primary_sources' else 'Project-authored proposal evidence',
            'version_date': work.PIN+';2024-06-24;inspected2026-10-16' if year == 2024 else '2026-10-16',
            'local_copy': ref(path, title), 'inspected_anchors': claims,
            'supported_claims': claims, 'records': records, 'limitations': work.LIMITS}
    sources = [
        source('exec16_longpolicy_code','CausalCollab pinned caller,representation,state-generation and output paths',
            'software_primary_sources', BASE/'source-review.json', primary['findings'], primary['records'], 2024),
        source('exec16_longpolicy_oracle','Exact text-version,adaptive-servicing,support and clock references',
            'project_derivation', BASE/'exact-results.json',
            ['Stipulated97/67USD version mixture;94.8/87.6USD policy conversion;positive derivative with finite loss',
             'Independent finite enumeration and backward formulas;support planning,clock exclusion and source loop count'],
            [{'local_copy': ref(ROOT/'tools/review_longitudinal_policy_20261016.py','Reproducible exact function')},
             {'local_copy': ref(BASE/'independent-arithmetic-review.json','Alternative arithmetic checks')}]),
        source('exec16_longpolicy_design','Proposed longitudinal assistance contract and public-evidence comparison',
            'project_design', BASE/'proposed-contract.json',
            ['Typed proposed requests/failures,public/generated prototype,matched baseline/full costs and unresolved research',
             'Design only;no integration permission,live-model accuracy or bank truth'],
            [{'local_copy': ref(BASE/'omissions-register.json','Coverage and candidate decisions')},
             {'local_copy': ref(BASE/'plan.md','Reviewed task scope and independence of eligible work')}])
    ]
    write(BASE/'source-audit.json', {'sources': sources, 'cutoff': '2026-10-07',
        'prior': ref(work.PRIOR,'646 inherited citation records'),
        'primary_rereads': ref(BASE/'source-review.json','Six genuine primary papers and22 original blobs')})
    evidence = [ref(p, anchor) for p, anchor in [
        (BASE/'source-review.json','Primary papers and pinned implementation paths'),
        (BASE/'exact-results.json','Six exact reference families'),
        (BASE/'independent-arithmetic-review.json','Independent formula checks'),
        (BASE/'omissions-register.json','Search limits,missing original and rights'),
        (BASE/'proposed-contract.json','Concrete engineering remedies and proposed evidence'),
        (BASE/'source-audit.json','Three traceable citation additions'),
        (BASE/'authoring-failure.json','Preserved tool error and repair'),
        (work.OUTPUT,'Connected task synthesis'), (template,'Authored manuscript argument'),
        (Path(__file__),'Preparation and criterion review')]]
    for row in evidence: verify_bindings(row)
    findings = [
        'Six primary papers distinguish text-version ISE,workflow assistance,active strategy learning,open-loop models and two-wave discovery. Favorable/adverse results and22 pinned source blobs support specific reuse remedies. Candidate122 and nonexhaustive search remain explicit.',
        'Fixed30-day net servicing target,three clocks,assignment/retention laws and formal recursion connect to independently reproduced version,feedback,locality,support and clock examples.',
        'Literature,static code,executed exact arithmetic and a proposed public/generated prototype retain separate status;no live-model performance,upstream runtime or bank truth is asserted.'
    ]
    write(BASE/'author-review.json', {'status':'pass', 'reviewer':work.REVIEWER,
        'scope':'Bounded proposal synthesis and author review;not census completion or capability qualification',
        'findings':findings, 'evidence':evidence, 'limitations':work.LIMITS,
        'integration_allowed':False,'visual_acceptance':False,
        'plan_review': ['No expensive bank evidence is required to finish this proposal synthesis.',
                        'Independent generated cases proceed despite dataset/license/search omissions.',
                        'Adaptive histories and text versions are required before a static implementation can answer the banking target.'],
        'depth_credit':'No automatic new chapter-depth credit;prior policy exposition is reused by reference.'})
    print(json.dumps({'synthesis':str(work.OUTPUT.relative_to(ROOT)), 'new_citations':3,
                      'author_review':'pass', 'integration_allowed':False}))


if __name__ == '__main__': main()

#!/usr/bin/env python3
"""Publish the reviewed proposal scope and versioned public-data readers atomically."""
import argparse
import copy
import json

import build_integrated_monograph_v12 as shared
import causal_program_v14 as ledger
import master_control as core
import proposal_program as proposal

ROOT = core.ROOT
BASE = ROOT / proposal.BASE


def ref(path, anchor):
    return shared.ref(ROOT / path if isinstance(path, str) else path, anchor)


def prepare():
    state = copy.deepcopy(core.read(ROOT, proposal.BASE + '/predecessor-state.json'))
    book = core.read(ROOT, proposal.BASE + '/reader/build-report.json')
    survey = core.read(ROOT, proposal.BASE + '/survey-reader/build-report.json')
    for r in [book, survey]:
        shared.verify_refs(r)
        shared.verify_refs(core.read(ROOT, r['source_audit']['path']))
    source_review = {'status': 'pass', 'issues': [], 'reviewer': {'name': 'Current coordinator', 'kind': 'author'},
                    'scope': 'Dataset identity, reported counts, claim types, source anchors and explicit access/causal limitations; not final manuscript or bank acceptance.',
                    'evidence': [ref(BASE / 'review.md', 'Scientific/access/scope review'),
                                 ref(BASE / 'source-audit.json', 'Every new citation'), book['source_audit'],
                                 ref(BASE / 'bank-profile.json', 'Actual descriptive inspection')]}
    core.write(BASE / 'source-review.json', source_review)
    audit = core.read(ROOT, book['source_audit']['path'])
    release = {'kind': 'working_monograph', 'final_acceptance': False,
               'pdf': book['pdf'], 'pages': book['pages'],
               'supersedes': {k: state['reader'][k] for k in ('path', 'sha256')},
               'build_report': ref(BASE / 'reader/build-report.json', 'Versioned integrated book'),
               'source_review': ref(BASE / 'source-review.json', 'Author claim/source review'),
               'text_layout': ref(BASE / 'reader/text-layout-review.json', 'Text and bounds only; not visual acceptance'),
               'source_artifacts': audit['tex_files'] + [audit['dataset_bibliography'], book['builder']]}
    core.write(BASE / 'working-release.json', release)
    binding = ref(BASE / 'working-release.json', 'Proposal/public-data book delivery')
    ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: book['pdf'][k] for k in ('path', 'sha256')}
    state['reader'].update(pages=book['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'] += [dict(state['reader']),
                            {**{k: survey['pdf'][k] for k in ('path', 'sha256')},
                             'status': str(survey['pages']) + '-page public-data survey; source/text/bounds checked; visual review pending'}]
    paths = {'plan': 'docs/program/master-program-proposal.md',
             'scope': proposal.BASE + '/proposal-scope.json',
             'survey': proposal.BASE + '/survey.md',
             'survey_pdf': survey['pdf']['path'],
             'dataset_register': proposal.BASE + '/dataset-register.json',
             'source_audit': proposal.BASE + '/source-audit.json',
             'omissions': proposal.BASE + '/omissions.json',
             'profile': proposal.BASE + '/bank-profile.json',
             'review': proposal.BASE + '/review.md',
             'source_review': proposal.BASE + '/source-review.json',
             'controller': 'tools/proposal_program.py', 'installer': 'tools/install_proposal_scope.py',
             'tests': 'tests/test_proposal_program.py',
             'profile_code': 'tools/profile_public_bank_data.py',
             'source_preparer': 'tools/prepare_public_data_survey.py',
             'collector': 'tools/public_dataset_sources.py',
             'frozen_original_collector': 'tools/public_sources.py',
             'builder': 'tools/build_public_data_reader.py',
             'survey_build': proposal.BASE + '/survey-reader/build-report.json',
             'survey_layout': proposal.BASE + '/survey-reader/text-layout-review.json',
             'working_release': proposal.BASE + '/working-release.json'}
    state['proposal_program'] = {'revision': '15.0-proposal-public-evidence-scope',
                                'predecessor': ref(BASE / 'predecessor-state.json', 'Preserved complete V14 state'),
                                'documents': {k: ref(v, 'Reviewed proposal ' + k) for k, v in paths.items()}}
    state['mission'] = core.read(ROOT, paths['scope'])['mission']
    issues = proposal.validate_state(ROOT, state)
    if issues:
        raise ValueError('; '.join(issues))
    core.write(BASE / 'candidate-state.json', state)
    print(json.dumps({'status': 'prepared', 'pages': book['pages'], 'proposal_accepted': False, 'product_accepted': False}))


def publish():
    state = core.read(ROOT, proposal.BASE + '/candidate-state.json')
    before = core.sha(ROOT / core.STATE)
    if before != state['proposal_program']['predecessor']['sha256']:
        raise ValueError('Canonical state changed; reconcile before publishing')
    report = core.read(ROOT, proposal.BASE + '/verification.json')
    shared.verify_refs(report)
    if report['status'] != 'pass' or report['tests_passed'] < 12 or report['blocking_issues']:
        raise ValueError('Passing exact-candidate verification required')
    if report['candidate_state']['sha256'] != core.sha(BASE / 'candidate-state.json'):
        raise ValueError('Verification belongs to another candidate')
    state['proposal_program']['documents']['verification'] = ref(BASE / 'verification.json', 'Exact-candidate verification')
    core.validate_state = proposal.validate_state
    core.render = proposal.render
    core.commit_state(ROOT, before, state, {'action': 'install_proposal_public_evidence_scope',
        'reason': 'Explicit user correction: proposal first; costly authentic bank experiments after demonstrated prototype merit.',
        'new_dataset_families_surveyed': 24, 'new_descriptive_profiles': 1,
        'new_fitted_causal_studies': 0, 'authentic_inputs_received': [],
        'proposal_acceptance': False, 'product_acceptance': False,
        'reader': state['reader'], 'preserved_execution_revision': state['revision']})
    print(json.dumps({'status': 'published', 'reader': state['reader'],
                      'scope_revision': state['proposal_program']['revision'], 'next': proposal.overview(state, ledger.graph_for(ROOT, state))['next']}))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('command', choices=['prepare', 'publish'])
    args = p.parse_args()
    prepare() if args.command == 'prepare' else publish()

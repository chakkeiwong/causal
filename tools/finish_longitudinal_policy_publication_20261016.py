#!/usr/bin/env python3
"""Admit the existing reviewed release with canonical reader metadata."""
import publish_longitudinal_policy_20261016 as prior
from pathlib import Path


def main():
    root, base = prior.ROOT, prior.BASE
    state = prior.core.read(root, prior.core.STATE)
    before = prior.core.sha(root/prior.core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path'] == str(prior.build.OLD.with_suffix('.pdf').relative_to(root))
    binding = prior.ref(base/'working-release.json','Reviewed longitudinal working successor')
    manifest = prior.run.ledger.validate_working_release(root,binding)
    canonical_status = state['reader']['status']
    assert canonical_status == 'Working monograph; not I02 acceptance'
    repair = base/'publication-repair.json'
    prior.write(repair,{
        'observed_failure':'State admission rejected: Current reader differs from its preserved working-delivery chain.',
        'cause':'Publisher omitted the space after the semicolon in the canonical reader status.',
        'effect':'Canonical state and previous reader remained unchanged;reviewed release manifest already existed.',
        'repair':'Reuse the exact canonical status from the predecessor. Preserve failed publisher,PDF,review and manifest;no validator or scientific criterion changes.',
        'optional_inspection_failure':'PyMuPDF/fitz was unavailable. Used existing pdftotext output to inspect physical pages509,512,513;no image review claimed.',
        'evidence':[binding,prior.ref(root/'tools/publish_longitudinal_policy_20261016.py','Preserved failed publisher'),
                    prior.ref(root/'tools/causal_program_v14.py','Exact reader metadata reconstruction'),
                    prior.ref(Path(__file__),'Successor metadata repair')],
        'next_action':'RenewQ2-Q4 for the published reader and continue the next eligible operation.'})
    state['execution_program']['working_releases'].append(binding)
    state['reader']={k:manifest['pdf'][k] for k in ['path','sha256']}
    state['reader'].update(pages=manifest['pages'],status=canonical_status)
    state['deliveries'].append(dict(state['reader']))
    prior.run.commit(root,before,state,{'action':'publish_longitudinal_policy_reader',
        'manifest':binding,'repair':prior.ref(repair,'Canonical metadata correction'),'final_acceptance':False})
    print('Published reviewed827-page longitudinal reader;canonical metadata restored.')


if __name__=='__main__': main()

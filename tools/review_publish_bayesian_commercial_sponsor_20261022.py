#!/usr/bin/env python3
"""Review preserving sponsor content and publish only after paired-reader renewal."""
import json
from pathlib import Path
import re
import build_bayesian_commercial_sponsor_20261022 as build
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run,core,ROOT,BASE=build.run,build.core,build.ROOT,build.BASE
read=lambda p:json.loads(p.read_text())


def sections(text):
    parts=re.split(r'(?m)^(#{1,2} .+)$',text)
    assert len({parts[i] for i in range(1,len(parts),2)})==len(parts)//2
    return {parts[i]:parts[i+1] for i in range(1,len(parts),2)}


def main():
    report,audit,progress=[read(BASE/n) for n in ['build-report.json','source-audit.json','progress-evidence.json']]
    for record in [report,audit,progress,read(BASE/'plan-review.json')]:verify_bindings(record)
    assert report['cited_records']==len(audit['sources'])
    assert not report['empty_pages'] and not report['text_bounds_issues']
    assert all('Underfull' in w for w in report['warnings'])
    assert not report['visual_acceptance'] and not report['final_proposal_acceptance']
    assert read(BASE/'economics-results.json')==build.engine.economics.calculate()
    prior=read(build.PRIOR/'source-audit.json')
    before={s['integrated_citation_key']:s for s in prior['sources']}
    after={s['integrated_citation_key']:s for s in audit['sources']}
    assert all(after[k]==v for k,v in before.items())
    required={r['integrated_citation_key'] for r in read(build.reader.BASE/'source-audit.json')['sources']} | {'sp22bs_reader','sp22bs_progress'}
    assert required<=after.keys()-before.keys()
    current=(BASE/'proposal.md').read_text();original=(build.PRIOR/'proposal.md').read_text()
    pages=progress['reader']['pages'];assert current==build.manuscript(pages)
    old_sections,new_sections=sections(original),sections(current)
    changed={'# The decision this proposal supports','# What remains before a complete proposal'}
    for heading,content in old_sections.items():
        if heading not in changed:assert new_sections[heading]==content,heading
    assert set(new_sections)-set(old_sections)=={'## Hidden-state tools need a causal and information contract'}
    cited={k.strip() for group in re.findall(build.engine.shared.CITE,current) for k in group.split(',')}
    assert cited==after.keys()
    text=' '.join((BASE/'reader.txt').read_text().split())
    records=len(read(build.reader.OUT/'source-audit.json')['sources'])
    c=progress['software_cells']
    for token in [f'{pages:,} pages',f'{records} audited','217 genuine',f'{c["open"]} open',
        f'{c["inconclusive"]} inconclusive','87 open','57 inspected','56 unread','USD 5,200','USD 36,000',
        'gsynth','fect','USD -4.4','Shrestha','90.8%','82.0%','twenty-four','2883','6/793',
        'USD -100','USD 500','USD -40','USD 440','USD 15','USD -10','0.18','frequency']:
        assert token.lower() in text.lower(),token
    assert c=={'pass':2,'inconclusive':37,'open':63,'total':102}
    assert progress['reuse_decisions']=={'pass':25,'inconclusive':3,'open':87,'total':115}
    state=core.read(ROOT,core.STATE)
    assert state['execution_runtime']['active'] is None
    assert run.same_reader(state['reader'],report['paired_monograph']) and run.same_reader(state['reader'],progress['reader'])
    status=run.status(ROOT,state)
    assert status['recorded_proposal_operations']==180
    assert {q['id']:q['status'] for q in status['proposal_gaps']}==dict(Q1='open',Q2='pass',Q3='pass',Q4='pass',Q5='open')
    evidence=[ref(BASE/n,'Reviewed sponsor evidence') for n in ['plan-review.json','source-audit.json','build-report.json',
        'economics-results.json','proposal.md','reader.txt','progress-evidence.json']]+[ref(Path(__file__),'Exact preservation and pairing'),
        ref(build.reader.BASE/'anchor-repair-review.json','Corrected manual anchors in paired reader')]
    findings=[f'All {len(before)} prior citation identities survive; {len(after)} cited records are audited.',
        'All earlier substantive sections survive; reader and software coverage fields are current.',
        'Commercial strengths, identification ambiguity, information clocks, uncertainty and export requirements are explained.',
        'Previous economics survive; new amounts are hypothetical specified-law calculations, not measured bank value.',
        'Coverage remains2 pass/37 inconclusive/63 open;180 outcomes are recorded, not full program acceptance.']
    limits=['Author source, arithmetic and text-layout review; no independent or rendered visual acceptance.',
        'Mandatory repairs, Q1/Q5 and final acceptance remain open.',
        'No native runtime, rights, actual costs or bank return is claimed.']
    write(BASE/'author-review.json',dict(status='pass',issues=[],reviewer=dict(name='Codex author/coordinator',kind='author'),
        scope='Preserving Bayesian/state sponsor and exact-reader review',sponsor=report['reader_copy'],
        paired_monograph=report['paired_monograph'],findings=findings,evidence=evidence,limitations=limits,
        visual_acceptance=False,final_acceptance=False))
    manifest=dict(kind='working_sponsor',pdf=report['reader_copy'],pages=report['pages'],paired_monograph=report['paired_monograph'],
        predecessor=ref(build.PRIOR/'reader/sponsor-proposal.pdf','Preserved sponsor'),
        predecessor_release=ref(build.PRIOR/'working-release.json','Preserved release'),
        predecessor_operation=state['execution_program']['results']['RELEASE.SPONSOR'],
        build=ref(BASE/'build-report.json','Dynamically counted build'),review=ref(BASE/'author-review.json','Exact-reader review'),
        evidence=evidence,final_acceptance=False,visual_acceptance=False)
    verify_bindings(manifest);write(BASE/'working-release.json',manifest)
    digest=core.sha(ROOT/core.STATE)
    delivery={k:report['reader_copy'][k] for k in ['path','sha256']}
    delivery.update(pages=report['pages'],kind='working_sponsor',status='Working sponsor; exact-reader review, visual/final acceptance open',
        paired_monograph=report['paired_monograph'],release=ref(BASE/'working-release.json','Preserving commercial state sponsor'))
    assert not any(item['path']==delivery['path'] for item in state['deliveries'])
    state['deliveries'].append(delivery)
    run.commit(ROOT,digest,state,dict(action='publish_bayesian_commercial_sponsor',release=delivery['release'],
        prior_operation_preserved=True,final_acceptance=False))
    print(json.dumps(dict(published=delivery['path'],pages=report['pages'],records=len(after),
        paired_monograph=state['reader']['path'],review='pass',visual_acceptance=False,final_acceptance=False)))


if __name__=='__main__':main()

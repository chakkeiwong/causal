#!/usr/bin/env python3
"""Bounded six-family commercial-host synthetic-control documentary review."""
import json,hashlib
from pathlib import Path
import run_program_reviews_v2 as extension
import synthetic_control_contract_reference_20261019 as exact
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write
run=extension.base;core=run.core;ROOT=core.ROOT;RAW=ROOT/'docs/literature/raw'
BASE=ROOT/'docs/program/execution/2026-10-19/commercial-synthetic-controls-v1'
OP='SW.CELL.synthetic_controls.commercial';OUTPUT=ROOT/f'docs/program/comprehensive-v14/work/{OP}/coverage-review.json'
REVIEWER=dict(name='Codex author/coordinator',kind='author');read=lambda p:json.loads(p.read_text())


def main():
    assert not OUTPUT.exists() and not (BASE/'source-audit.json').exists()
    c=read(RAW/'exec19_synth_stata_cutoff.json')[0];pin=c['sha'];t=read(RAW/'exec19_synth_stata_tree.json')
    assert pin=='ae99fd1ed100e8f5ea38386f18f02e61a90956e6' and c['commit']['committer']['date']=='2026-04-30T15:57:51Z'
    assert t['sha']==c['commit']['tree']['sha'] and not t['truncated']
    blobs={r['path']:r['sha'] for r in t['tree'] if r['type']=='blob'}
    rows=read(BASE/'pinned-acquisition-manifest.json')['files']+read(BASE/'contract-acquisition-manifest.json')['files']
    ranges=[[(1,145)],[(28,54),(107,150),(157,187),(264,328)],[(1,40),(54,78),(134,184),(540,605),(665,685),(890,929)],[(1,39)],[(1,35)],[(1,80)],[(1,154)],[(1,55)],[(1,42)],[(1,28)],[(1,112)],[(1,60)]]
    records=[];extracts=[]
    for row,rs in zip(rows,ranges):
        p=RAW/(row['id']+'.txt');rc=RAW/(row['id']+'.receipt.json');r=read(rc);data=p.read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();url=f'https://raw.githubusercontent.com/j-hai/synth-stata/{pin}/{row["path"]}'
        assert r['status']=='saved' and r['url']==url and r['sha256']==core.sha(p) and blobs[row['path']]==blob
        lines=data.decode().splitlines();anchors=[f'lines{lo}-{min(hi,len(lines))}' for lo,hi in rs]
        records.append(dict(source_identity=url,version_date='Historical30April2026commit; '+pin,local_copy=ref(p,'; '.join(anchors)),git_blob_sha1=blob,receipt=ref(rc,'Bounded original acquisition'),inspected_anchors=anchors,executed=False))
        extracts.append(dict(path=row['path'],ranges=[dict(start=lo,end=min(hi,len(lines)),text='\n'.join(f'{i+1}: {lines[i]}' for i in range(lo-1,min(hi,len(lines))))) for lo,hi in rs]))
    claims=['The selected community Synth-for-Stata source identifies version0.0.8 and a Stata13.0 command version declaration; it is not a verified proprietary vendor-native synthetic-control implementation.',
        'Donors default to all panel units except the treated unit; explicitly supplied donor lists require at least two units. Scientific eligibility and spillover exclusion remain caller obligations.',
        'Predictor means ignore missing entries, with all-missing predictor checks. Predictor-specific dates can override the general period; this is not a common balanced measurement window by default.',
        'Default predictor and MSPE periods precede treatment, but explicitly supplied MSPE periods are checked for membership in observed dates rather than for being before treatment.',
        'Help specifies margin0.05 and sigf7; selected command defaults are margin0.005 and sigf12. The mismatch must be retained rather than silently choosing one.',
        'The selected C wrapper assigns pr_loqo status, stores primal weights and returns0 without branching on that status; the header distinguishes optimal, suboptimal, iteration-limit and infeasible states.',
        'RMSPE is computed before a roundmat call alters wsol. The compiled Mata routine body is not inspected, so exact rounding behavior remains unknown.',
        'The nested loss helper maximizes negative squared error. Choosing the larger log objective in allopt is consistent with that sign; a comment saying lower loss does not establish a reversed comparison bug.',
        'README declares GPL>=2, while bundled pr_loqo source/header retains proprietary and commercial-use restriction notices. This is unresolved distribution-rights evidence, not permission to reuse or a legal determination.',
        'Selected returns expose weights, predictor balance, trajectories and RMSPE. General help language about placebo/permutation inference does not qualify a matched inference protocol here.',
        'Upstream integration scripts and saved numerical baselines are inspected author artifacts, not rerun results or independent validation.'
    ]
    limits=['Only a community estimator inside one commercial host has inspected technical originals; EViews, SAS, IBM, MathWorks and hosted-front-end coverage remain unresolved.',
        'Four requested vendor/archive routes were rejected by the fixed collector allowlist; those are acquisition failures, not source absence or a reason to relax policy.',
        'Built-in web search returned no usable text; inherited metadata query returns two unrelated/domain-mismatched leads, not market completeness.',
        'No Stata runtime, plugin binary or compiled Mata library is executed or authenticated against source; tests remain inspected specifications.',
        'README licensing statement and conflicting component notices need authoritative distribution-specific clarification; no redistribution or commercial-use approval granted.',
        'No authentic price, entitlement, support agreement, runtime comparison or bank causal-effect claim.',
        'Authored finite arithmetic is not a calibrated placebo test or an identified real portfolio effect.']
    write(BASE/'inspected-extracts.json',dict(records=extracts,native_execution=False))
    source=dict(integrated_citation_key='exec19_synth_stata_source',kind='software_primary_sources',title='Synth for Stata0.0.8: selected historical command, help, optimizer interface and notices',author='Abadie, Alberto and Diamond, Alexis and Hainmueller, Jens and contributors',year=2026,source_identity='https://github.com/j-hai/synth-stata',version_date='Commit30April2026; '+pin,local_copy=ref(RAW/'exec19_synth_stata_source_0.txt','Pinned README'),records=records,identity_evidence=[ref(RAW/'exec19_synth_stata_cutoff.json','Selected pre-cutoff commit'),ref(RAW/'exec19_synth_stata_tree.json','Exact complete tree')],inspected_anchors=[dict(anchor=x,inspection='Selected primary technical/source/notice text') for x in claims],supported_claims=claims,limitations=limits)
    reference=dict(integrated_citation_key='exec19_synth_contract_reference',kind='project_authored_exact_reference',title='Exact regional-portfolio donor contamination and postoutcome-selection example',author='Causal banking proposal project',year=2026,source_identity='tools/synthetic_control_contract_reference_20261019.py',version_date='2026-10-19',local_copy=ref(ROOT/'tools/synthetic_control_contract_reference_20261019.py','Exact finite arithmetic'),inspected_anchors=[dict(anchor='calculate()',inspection='Executed rational reference')],supported_claims=['Half-half donors give stipulated20thousandUSD gap; donor contamination reduces it to10 and postoutcome weight selection to0.','Rank-count fractions1/5 and1/2 differ with retained denominator; no calibration claimed.'],limitations=['Authored assumptions; no vendor, bank or inference trial.'])
    audit=dict(sources=[source,reference],records=records,cutoff='2026-10-07',limitations=limits);write(BASE/'source-audit.json',audit);write(BASE/'exact-results.json',exact.calculate())
    failed=[ref(RAW/f'exec19_synth_{name}.receipt.json','Actual rejected acquisition route') for name in ['ssc_help','ssc_code','eviews_addins','sas_rwe']]
    contract=dict(status='proposed_not_implemented',requirements=['Explicit treated/donor identity, eligibility, no-interference restrictions and outcome measurement clock.','Separate predictor, tuning and display periods; prevent postoutcome tuning unless the declared design justifies it.','Retain missingness and effective windows per predictor/unit, all attempts and donor exclusions.','Return optimizer status, constraints/residuals, objective sign, starts, precision and pre/post rounding weights distinctly.','Specify placebo eligible universe, inclusion of treated unit, pre-fit rule, tail direction, exchangeability/null law and denominator.','Distinguish native vendor command, community code, commercial host, compiled plugin and hosted frontend rights and capabilities.','Use explicit unsupported/failure results until a matched common-service implementation is demonstrated.'])
    write(BASE/'conversion-contract.json',contract)
    candidates=[]
    for family in ['Stata','EViews','SAS','IBM','MathWorks','Commercial hosted open-source frontends']:
        candidates.append(dict(family=family,status='selected_community_source_inspected' if family=='Stata' else 'relevant_primary_not_inspected',aliases=['Synth for Stata','synth','Stata commercial host'] if family=='Stata' else [family],documented_scope=claims if family=='Stata' else [],proposal_route='Compare a separately licensed community estimator in its commercial host; defer integration' if family=='Stata' else 'Find matched dated primary estimator/host documents before comparison',absence_claim=False,price=None,native_execution=False,rights_qualified=False))
    omissions=dict(status='open',vendors=candidates,failed_acquisitions=failed,remaining=['Dated native proprietary alternatives and exact editions','Authoritative resolution of component notices','Compiled Mata rounding and plugin binary/source correspondence','Matched donor/placebo inference protocol and source theorem anchors','Public prices, entitlement and support scope'],next_action='Continue each missing vendor route independently using permitted official originals; do not infer synthetic-control estimators from regression menus or synthetic-data marketing.')
    write(BASE/'omissions-register.json',omissions)
    evidence=[ref(BASE/n,'Reviewed bounded evidence') for n in ['plan-review.json','search-review.json','source-audit.json','inspected-extracts.json','exact-results.json','conversion-contract.json','omissions-register.json']]+[ref(Path(__file__),'Source authentication and criterion review')]
    out=dict(operation_id=OP,status='inconclusive',reviewer=REVIEWER,scope='Six-family documentary commercial-host synthetic-control survey; one community implementation inspected',cutoff='2026-10-07',selected_commit=pin,candidates=candidates,evidence=evidence,claims=claims,limitations=limits,integration_allowed=False,capabilities=[],revisit_trigger='Obtain matched historical technical originals for five uninspected families and resolve source/host/plugin rights, binary correspondence, estimator and placebo contracts; licensed execution is later prototype work.')
    write(OUTPUT,out);write(BASE/'review.json',dict(status='inconclusive',reviewer=REVIEWER,output=ref(OUTPUT,'Bounded six-family coverage'),evidence=evidence,findings=claims,limitations=limits))
    s=core.read(ROOT,core.STATE);assert s['execution_runtime']['active']['operation']==OP;g,_,_=run.combined(ROOT,s);receipt=run.ledger.receipt_template(run.ledger.operation(g,OP))
    findings=[('inconclusive','Six families retained; five lack inspected matching originals and search is not saturated.'),('pass','Twelve pinned original texts authenticated; supported technical claims, notice conflicts and exact project reference are separately scoped.'),('pass','Omissions, acquisition failures and commercial-host/community distinction are explicit; no absence or rights waiver.')]
    receipt.update(outcome='inconclusive',execution='performed',scope=out['scope'],reviewer=REVIEWER,capabilities=[],outputs=[ref(OUTPUT,'Contracted commercial synthetic-control review')],limitations=limits,nonexecution_reason='',revisit_trigger=out['revisit_trigger'],criteria=[dict(index=i,verdict=v,finding=f,evidence=evidence+[ref(BASE/'review.json','Author criterion review')]) for i,(v,f) in enumerate(findings)])
    write(BASE/'operation-receipt.json',receipt);verify_bindings([audit,out,receipt]);print(json.dumps(dict(operation=OP,outcome='inconclusive',families=6,selected_source_blobs=12,native_execution=False)))


if __name__=='__main__':main()

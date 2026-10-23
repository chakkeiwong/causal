#!/usr/bin/env python3
"""Preserve initial source review and bind each source to a complete cutoff tree."""
import copy, hashlib, json
from pathlib import Path
import workflow_contract_reference_20261024 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'docs/program/execution/2026-10-24/workflow-contracts-v3';RAW=ROOT/'docs/literature/raw'
read=lambda p:json.loads(p.read_text())

def main():
    assert not (BASE/'source-audit-qualified.json').exists()
    identity={}
    for prefix,commit_suffix in [('exec24_workflow3_sassamples','cutoff'),('exec24_workflow3_dataiku','cutoff'),
        ('exec24_workflow3_requests','cutoff'),('exec24_workflow3_urllib3','cutoff'),
        ('exec24_workflow3_requests231','commit'),('exec24_workflow3_urllib126','commit'),
        ('exec24_workflow3_domino','cutoff_retry1'),('exec24_workflow3_positcpp','cutoff'),('exec23_workflow_dominopy','cutoff')]:
        cp=RAW/(prefix+'_'+commit_suffix+'.json');tp=RAW/(prefix+'_tree.json')
        c,t=read(cp),read(tp);c=c[0] if isinstance(c,list) else c
        assert not t['truncated'] and t['sha']==c['commit']['tree']['sha']
        assert c['commit']['committer']['date']<'2026-10-07T16:00:00Z'
        for p in [cp,tp]:
            r=read(p.with_suffix('.receipt.json'));assert r['status']=='saved' and r['sha256']==hashlib.sha256(p.read_bytes()).hexdigest()
        identity[c['sha']]=(c,t,[ref(cp,'Cutoff commit and date'),ref(tp,'Complete authenticated tree')])
    audit=copy.deepcopy(read(BASE/'source-audit.json'));verify_bindings(audit)
    checked=[]
    for source in audit['sources']:
        for record in source.get('records',[]):
            url=record['source_identity'];tail=url.split('raw.githubusercontent.com/',1)[1];parts=tail.split('/');commit=parts[2];path='/'.join(parts[3:]);c,t,evidence=identity[commit]
            entry=next(x for x in t['tree'] if x['path']==path);b=(ROOT/record['local_copy']['path']).read_bytes()
            assert entry['sha']==record['git_blob_sha1'] and entry['size']==len(b)
            record['identity_evidence']=evidence;record['version_date']=c['commit']['committer']['date']+'; '+commit
            checked.append(record['local_copy'])
    audit.update(predecessor=ref(BASE/'source-audit.json','Preserved initial span review'),identity_reviewer=ref(Path(__file__),'Complete tree/date qualification'))
    write(BASE/'source-audit-qualified.json',audit)
    write(BASE/'identity-review.json',dict(status='pass',issues=[],source_audit=ref(BASE/'source-audit-qualified.json','Qualified source identities'),inspected_files=len(checked),records=checked,cutoff='2026-10-07'))
    result=exact.calculate();assert result['total_cost_usd']==12 and result['acceptance_per_request']=='1/4' and result['acceptance_per_started']=='1/3'
    assert result['three_backoff_sleeps_seconds']=='331/500' and result['three_two_second_requests_plus_sleep_seconds']=='3331/500'
    assert read(BASE/'exact-results.json')==result
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_exact_accounting',issues=[],evidence=[ref(Path(exact.__file__),'Exact rational reference'),ref(BASE/'exact-results.json','Exact results'),ref(BASE/'development.tex','Connected argument')],findings=['Requested and started denominators are distinct; costs retain all requested attempts.','Sleep caps do not bound request duration or an unbounded number of polls.','Terminal state and exit code do not substitute for request-bound scientific acceptance.'],native_execution=False))
    write(BASE/'copyedit-review.json',dict(status='pass',issues=[],evidence=[ref(BASE/'development.tex','Reviewed manuscript'),ref(BASE/'sponsor-addition.md','Sponsor treatment')],findings=['Static source behavior, intended server contracts, authored examples and native measurements remain distinct.','Historical document versions and client versions are not described as current server releases.','No unsupported schema, rights, full coverage or native integration claim.'],visual_acceptance=False))
    review=dict(status='pass_for_scoped_contract_review_with_limits',reviewer=dict(name='Codex author/coordinator',kind='author'),evidence=[ref(BASE/n,'Reviewed grouped comparison') for n in ['review.json','identity-review.json','source-audit-qualified.json','mathematical-review.json','copyedit-review.json','development.tex','sponsor-addition.md','search-screening.json','omissions-register.json','conversion-contract.json']],whole_cell_complete=False,integration_allowed=False,native_execution=False,visual_acceptance=False)
    verify_bindings(review);write(BASE/'review-v2.json',review)
    state=controller.base.core.read(ROOT,controller.base.core.STATE);graph,_,_=controller.base.combined(ROOT,state);node=controller.base.ledger.operation(graph,'SW.CELL.computation_workflow.commercial')
    assert node['id'] not in state['execution_runtime']['results']
    evidence=[ref(BASE/n,'Reviewed commercial workflow evidence') for n in ['review-v2.json','source-audit-qualified.json','search-screening.json','omissions-register.json','conversion-contract.json','mathematical-review.json','development.tex']]
    path=ROOT/node['outputs'][0];assert not path.exists();path.parent.mkdir(parents=True,exist_ok=True)
    action='Resolve immutable supported Dataiku DSS server and SAS normative workflow contracts, Domino v4/jobs terminal/error schemas and exact lock, Posit supported product/backend profile, and earlier market/source tails. Public client evidence is integrated; native qualification, rights and prices remain separate.'
    write(path,dict(operation=node['id'],status='inconclusive',scope='Four bounded commercial workflow profiles; not exhaustive market coverage',reviewer=dict(name='Codex author/coordinator',kind='author'),evidence=evidence,next_action=action,whole_cell_complete=False,integration_allowed=False,capabilities=[],native_execution=False))
    receipt=controller.base.ledger.receipt_template(node);receipt.update(outcome='inconclusive',execution='performed',scope='Source-grounded workflow contracts; incomplete supported-server and market coverage',reviewer=dict(name='Codex author/coordinator',kind='author'),limitations=read(BASE/'review.json')['limitations'],outputs=[ref(path,'Bounded commercial coverage disposition')],nonexecution_reason='',revisit_trigger=action,criteria=[dict(index=0,verdict='inconclusive',finding='Bounded candidate searches and pinned originals improve four profiles but do not complete historical server schemas or the full candidate census.',evidence=evidence),dict(index=1,verdict='pass',finding='Technical claims bind primary bytes, complete cutoff trees, dates, hashes and inspected anchors; no metadata-only technical or scholarly claims.',evidence=evidence),dict(index=2,verdict='pass',finding='Alternatives, temporal omissions, rights and native boundaries remain explicit; no unavailable-original waiver.',evidence=evidence)])
    write(BASE/'operation-receipt.json',receipt)
    print(json.dumps(dict(identity_review='pass',inspected_files=len(checked),receipt='inconclusive',source_records=5)))
if __name__=='__main__':main()

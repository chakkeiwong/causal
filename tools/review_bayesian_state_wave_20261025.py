#!/usr/bin/env python3
"""Review pinned Bayesian source contracts and separate language-cell outcomes."""
import argparse
import hashlib
import json
from pathlib import Path
import bayesian_state_wave_reference_20261025 as exact
from bayesian_state_wave_anchors_20261025 import ANCHORS, REUSE, NEW_GROUPS
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings

run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-25/bayesian-state-wave-v1'
RAW=ROOT/'docs/literature/raw'
PRIOR=ROOT/'docs/program/execution/2026-10-25/other-transport-missingness-reader-v1/reader/source-audit.json'
read=lambda p:json.loads(p.read_text())
LIMITS=[
    'Five selected source repositories and four bounded discovery queries do not establish ecosystem saturation.',
    'Previously reviewed source records retain their original dates, scope and limits; not newly acquired evidence.',
    'Keanu is a historical2021source; separate Stan/RStan pins do not establish compatible distributed artifacts.',
    'No downloaded implementation executed; exact authored examples are not measured native failure rates.',
    'Complete dependencies, native qualification, artifact rights, owners and full costs remain open.',
    'Package-mentioned scholarly works remain leads; no new paper admitted without genuine original.',
    'Q1/Q5, mandatory coverage/depth and fresh visual/independent/final acceptance remain open.',
]
NEXT='Complete residual candidate/delegate inspection and register model-specific public trials for intervention, information clocks, posterior/predictive laws, diagnostics, failures, retained draws, restart custody and total costs; no universal hidden-state identification claim.'
DECISIONS={
    'R':['Conditionally use RStan with exact StanHeaders/runtime pairing and named diagnostic formulas.','Conditionally use NIMBLE with explicit sampled/predictive nodes, chain initialization and continuation contracts.','Retain bnlearn and bssm as distinct graph/state alternatives; no umbrella Bayesian causal admission.'],
    'Python':['Reuse existing PyMC/NumPyro evidence for typed model-surgery and predictive contracts.','Use Dynamax/PyDLM only with declared action/observation factorization and filtering/smoothing clocks.','Prefer pinned process workers to broad ports; native and full ecosystem qualification remain open.'],
    'Java':['Retain historical Keanu as conditional reference with observation versus intervention, adaptation and sample-budget contracts.','Compare Tetrad graph operations and JDemetra+ state propagation in their distinct roles.','Keep Smile Java distinct from BayesFusion SMILE; no support/entitlement transfer.'],
    'Cxx':['Conditionally use Stan services with log/draw/diagnostic validation, not return-code-only acceptance.','Retain libDAI/OpenGM factor and optimization roles; conditioning/MAP are not causal surgery/posterior paths.','Compare bssm/structural kernels with model-specific uncertainty and clock qualification.'],
    'other_relevant':['Conditionally use Turing with supported Gibbs blocks, correct conditional callbacks and particle contracts.','Retain StateSpaceModels.jl/gretl fitted-state roles without unsupported Bayesian model-averaging claims.','Other languages and complete numerical delegates remain open; do not infer absence.'],
}


def prepare():
    assert not (BASE/'review.json').exists()
    pins=read(BASE/'pins.json')
    selected=read(BASE/'selected-paths.json')+read(BASE/'delegate-paths.json')
    assert len(selected)==57
    originals=[];identities=[]
    for group,pin in pins.items():
        cp=RAW/f'exec25_bsw_{group}_commit.json';tp=RAW/f'exec25_bsw_{group}_tree.json'
        for p in [cp,tp]:assert core.sha(p)==read(p.with_suffix('.receipt.json'))['sha256']
        commit=read(cp)[0];tree=read(tp)
        assert commit['sha']==pin['sha'] and commit['commit']['committer']['date']==pin['date']<='2026-10-07T15:59:59Z'
        assert tree['sha']==pin['tree_sha'] and not tree['truncated']
        blobs={x['path']:x['sha'] for x in tree['tree'] if x['type']=='blob'}
        identities.extend([ref(cp,'Pinned identity'),ref(tp,'Complete selected tree')])
        for item in [x for x in selected if x['group']==group]:
            p=RAW/(item['id']+'.txt');rp=p.with_suffix('.receipt.json');r=read(rp);data=p.read_bytes()
            assert r['status']=='saved' and core.sha(p)==r['sha256']
            assert r['url']=='https://raw.githubusercontent.com/'+pin['repository']+'/'+pin['sha']+'/'+item['upstream_path']
            blob=hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()
            assert blob==blobs[item['upstream_path']]==item['git_blob']
            originals.append(dict(**item,local_copy=ref(p,'Authentic original'),receipt=ref(rp,'Public receipt')))
    write(BASE/'authenticated-originals-v2.json',dict(count=57,groups=5,originals=originals,identities=identities,native_execution=False,predecessor=ref(BASE/'authenticated-originals.json','First51originals preserved')))
    fragments=[];sources=[]
    for group,checks in ANCHORS.items():
        pin=pins[group];evidence=[ref(RAW/f'exec25_bsw_{group}_commit.json','Pinned identity')];anchors=[];claims=[]
        for suffix,lo,hi,token,finding in checks:
            p=RAW/f'exec25_bsw_{group}_{suffix}.txt';lines=p.read_text().splitlines();hi=min(hi,len(lines));excerpt=chr(10).join(lines[lo-1:hi]);assert token in excerpt,(group,suffix,token)
            binding=ref(p,f'Lines{lo}-{hi}: {finding}');evidence.append(binding);anchors.append(dict(path=binding['path'],line_spans=[[lo,hi]],finding=finding));claims.append(finding);fragments.append(dict(group=group,source=binding,first_line=lo,last_line=hi,text=excerpt))
        sources.append(dict(integrated_citation_key='exec25_bsw_'+group,kind='software',title=group+' pinned Bayesian computation and state-worker contracts',author=pin['repository']+' contributors',year=int(pin['date'][:4]),source_identity='https://github.com/'+pin['repository']+'/tree/'+pin['sha'],version_date=pin['date']+';'+pin['sha'],local_copy=evidence[1],evidence=evidence,inspected_anchors=anchors,supported_claims=claims,limitations=LIMITS,native_execution=False))
    write(BASE/'inspected-extracts.json',dict(count=len(fragments),anchors=fragments))
    write(BASE/'exact-results.json',exact.calculate())
    prior=read(PRIOR);verify_bindings(prior);entries={s['integrated_citation_key']:s for s in prior['sources']};keys=set(sum(REUSE.values(),[]));assert keys<=entries.keys()
    inherited=[entries[k] for k in sorted(keys)];sources+=inherited
    write(BASE/'reused-evidence.json',dict(records=len(inherited),by_language=REUSE,source_audit=ref(PRIOR,'Unchanged predecessor identities'),limitations='Retain original scope/date/primary bindings; no claim of new acquisition or native qualification.'))
    queries=[];leads={}
    for p in sorted(RAW.glob('exec25_bsw_search_*.json')):
        if p.name.endswith('.receipt.json'):continue
        receipt=read(p.with_suffix('.receipt.json'));assert receipt['status']=='saved' and receipt['sha256']==core.sha(p);d=read(p)
        queries.append(dict(source=ref(p,'Discovery only; not historical search reconstruction'),total=d['total_count'],returned=len(d['items']),unreturned=max(0,d['total_count']-len(d['items'])),incomplete=d['incomplete_results']))
        for x in d['items']:leads[x['full_name']]=dict(repository=x['full_name'],status='uninspected_discovery')
    assert len(queries)==4
    write(BASE/'search-screening.json',dict(cutoff='2026-10-07',queries=queries,unique_leads=len(leads),leads=list(leads.values()),absence_claim=False,saturation_claim=False))
    write(BASE/'dependency-license-review.json',dict(status='not_complete_clearance',evidence=[ref(BASE/'authenticated-originals-v2.json','Exact original declarations')],findings=['Stan/NIMBLE BSD-style; RStan GPL>=3; StanHeaders distinct BSD3; Keanu/Turing MIT.','Separate version pins and compatibility ranges are not complete installed dependency custody.','No native integration or distribution clearance.']))
    tests=['Enumerate observationally equivalent structural models and preserve model sensitivity.','Compare filtering/smoothing under separate event,availability and decision clocks.','Check conjugate posterior and predictive moments,not just estimates.','Qualify missing diagnostics,empty outputs,partial path failures,adaptation removal and exact draw budgets.','Check intervention versus conditioning,factor order and predicted-variable regeneration.','Test trapped Gibbs supports and user conditional-law correctness with finite oracles.','Preserve particle weight ESS,genealogy and log-normalizer calibration as distinct quantities.','Bind exact artifacts,rights,RNG/model state and full cost before native admission.']
    write(BASE/'qualification-plan.json',dict(status='proposed_not_executed',owner='Scientific, numerical, integration and operations owners to be appointed',tests=tests,independent_branches=True,native_execution=False,bank_trials_required_now=False))
    write(BASE/'omissions-register.json',dict(global_blocker=False,known_routes=tests,uninspected=['Residual discovery candidates and other languages.','Full Stan Math/compiler,AdvancedHMC,DynamicPPL,AbstractMCMC,Libtask,numerical and JVM delegates.','Installed release artifacts,whole-dependency rights,native experiments and complete costs.','Package-mentioned scholarly originals not admitted by this review.'],unknown_universal_repairs=['Observational equivalence cannot be resolved by more draws alone.','Unrestricted latent-state identification and arbitrary cross-world dependence need additional information or assumptions.','Universal dependent-data uncertainty calibration is not supplied by a sampler.'],next_action=NEXT))
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_witnesses',evidence=[ref(Path(exact.__file__),'Exact project calculations'),ref(BASE/'exact-results.json','Replayed results'),ref(BASE/'inspected-extracts.json','Implementation contracts')],findings=['Model odds3/2 remain3/2 under equal observed likelihoods.','Filtering3/4versus smoothing9/10gives currentUSD-25versus future-informedUSD50; illustrative10000decision lossUSD250000.','Beta8,7moments and two-trial predictive variance119/225versus plug-in112/225.','Energy ratios3/100and9/4differ under the selected formulas.','Eleven transitions,two drops,thinningfour retainthree positions; particle ESS50/41is not genealogy.'],native_execution=False))
    for language in REUSE:
        folder=BASE/language;folder.mkdir()
        write(folder/'comparison-review.json',dict(operation='SW.CELL.bayesian_scm_state.'+language,status='inconclusive',selected_new_groups=NEW_GROUPS[language],reused_records=REUSE[language],decisions=DECISIONS[language],limitations=LIMITS,next_action=NEXT))
    evidence=[ref(BASE/n,'Reviewed comparison') for n in ['authenticated-originals-v2.json','inspected-extracts.json','reused-evidence.json','search-screening.json','dependency-license-review.json','mathematical-review.json','qualification-plan.json','omissions-register.json']]
    sources.append(dict(integrated_citation_key='exec25_bsw_choice',kind='project_evidence_not_scholarly_paper',title='Authored five-language Bayesian SCM and hidden-state comparison and public qualification',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='25October2026; cutoff7October2026; no native execution',local_copy=ref(BASE/'mathematical-review.json','Exact authored witnesses'),evidence=evidence+[ref(Path(exact.__file__),'Authored reference')],inspected_anchors=[dict(anchor='Model ambiguity,information clocks,uncertainty,diagnostics,failures and language choices',inspection='Author inspection')],supported_claims=['57authentic originals and preserved primary audits support bounded five-language decisions.','Exact public laws motivate implementation qualification before bank experiments.'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,new_records=6,reused_records=len(inherited),new_scholarly_pdfs=0,evidence=evidence,native_execution=False))
    write(BASE/'plan-review-v2.json',dict(status='pass_for_bounded_source_work',evidence=evidence+[ref(BASE/'plan.md','Initial plan')],checks=['Scientific identification separate from numerical posterior quality.','Direct reuse,adapter,port and reject choices are candidate-specific.','Five source cells independent; one preserving publication after consumed predecessor.','No source claim exceeds selected primary branches; missing delegates remain explicit.']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_argument',evidence=[ref(BASE/'development.tex','Cross-language scholarly argument'),ref(BASE/'sponsor-addition.md','Connected sponsor investment case')],findings=['Explained notation,assumptions,exact banking examples and substantive alternatives.','Historical pins,source/runtime scope and license distinctions retained.','No false native,visual or final acceptance.'],visual_acceptance=False))
    evidence += [ref(BASE/n,'Reviewed integration') for n in ['source-audit.json','plan-review-v2.json','copyedit-review.json','development.tex','sponsor-addition.md']]+[ref(Path(__file__),'Reviewer'),ref(ROOT/'tools/bayesian_state_wave_anchors_20261025.py','Inspected spans')]
    verify_bindings(dict(evidence=evidence))
    write(BASE/'review.json',dict(status='pass_for_bounded_source_work',operation_outcome='inconclusive',evidence=evidence,technical_anchors=len(fragments),originals=57,scholarly_originals=0,language_cells=list(REUSE),limitations=LIMITS,native_execution=False))
    print(json.dumps(dict(review='pass',outcomes='five_inconclusive',originals=57,anchors=len(fragments),new_records=6,reused_records=len(inherited))))


def receipt(language):
    verify_bindings(read(BASE/'review.json'));assert exact.calculate()==read(BASE/'exact-results.json')
    op='SW.CELL.bayesian_scm_state.'+language;state=core.read(ROOT,core.STATE);graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,op);folder=BASE/language;output=ROOT/node['outputs'][0]
    assert not output.exists();write(output,read(folder/'comparison-review.json'))
    evidence=[ref(BASE/n,'Reviewed coverage') for n in ['review.json','source-audit.json','search-screening.json','omissions-register.json']]+[ref(folder/'comparison-review.json','Language-specific decisions')]
    findings=['Bounded selected sources inspected;ecosystem,artifact and native coverage remain incomplete.','Authentic pinned originals and unchanged prior records ground selected claims; exact authored examples reproduce.','Conditional direct use,adapter,port and rejection choices retain scientific,rights and cost qualification.']
    result=run.ledger.receipt_template(node);result.update(outcome='inconclusive',execution='performed',scope=language+' Bayesian SCM and state primary-source comparison',reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(output,'Bounded coverage')],criteria=[dict(index=i,verdict='inconclusive' if i==0 else 'pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=NEXT)
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(folder/'operation-receipt.json',result);print(language+' Bayesian/state coverage receipt prepared.')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);p.add_argument('language',nargs='?',choices=list(REUSE));a=p.parse_args()
    if a.command=='prepare':prepare()
    else:assert a.language;receipt(a.language)

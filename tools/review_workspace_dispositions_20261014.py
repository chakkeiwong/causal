#!/usr/bin/env python3
"""Refresh proposal integration dispositions; never import or write siblings."""
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import tomllib

import build_integrated_monograph_v12 as shared
import master_control as core
import run_program as run
import workspace_inventory_v12 as inventory

ROOT = core.ROOT
BASE = ROOT/'docs/program/execution/2026-10-14/workspace-dispositions'
OLD = ROOT/'docs/program/repair-v12/work/IN01'
PRIOR = ROOT/'docs/program/execution/2026-10-13/workspace'
OP = 'IN.REQ.all_workspace_repos_disposition'
OUTPUT = ROOT/'docs/program/comprehensive-v14/work'/OP/'requirement-review.json'
ref = shared.ref


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False, allow_nan=False)
        stream.write('\n')


def main():
    assert not OUTPUT.exists() and not (BASE/'inventory.json').exists()
    previous = json.loads((OLD/'workspace-inventory.json').read_text())
    annotations = json.loads((OLD/'annotations.json').read_text())
    annotations['hponas'].update(
        reason='Current README reports retained finite local qualification and later development repairs awaiting affected-source qualification. It separates declared evaluation from legacy_unqualified examples. These are upstream declarations, not reproduced causal-consumer acceptance.',
        next_action='Use an isolated Python 3.12+ process with a frozen objective/data/protocol and protected final evaluation; qualify target and uncertainty semantics separately.')
    annotations['MOONeural'].update(
        reason='Current README says delivery 0.1.27 while pyproject declares 0.1.28. Task-specific solver losses/acceptance limits and caller-owned evaluation remain explicit; a solver does not identify a causal target.',
        next_action='Resolve source/version identity for the chosen adapter, rights and a concrete nuisance/solver role; retain separate loss constraints and independent final evaluation.')
    annotations['causal'].update(
        reason='The local reference runtime has preserved library/CLI/stdio evidence for nine bounded operations; problem.formulate, graph.discover and design.evaluate remain unimplemented. Historical runtime evidence is not general product qualification.',
        integration_state='local_reference_demonstrated_selected_scope',
        next_action='Reuse the admitted causal-side operations and preserve unsupported requests, target identity, assumption provenance, missing methods and later consumer conformance.')
    annotations['MacroFinance']['next_action']='Resolve the facade constant pointing to /home/ubuntu/python/BayesFilter against this workspace; bind the selected model/revision and BayesFilter runtime authority before an isolated causal-side contract trial.'
    annotations['humanvoice']['reason']='Current README describes separate child-manuscript editing with retained-concept controls and bounded internal results. Its own declarations do not establish causal scientific review or a right to rewrite frozen proposal evidence.'
    dirs = sorted(p for p in ROOT.parent.iterdir() if p.is_dir())
    assert {p.name for p in dirs} == set(annotations), 'Review added or missing directories first'
    old_hashes = {s['source_identity']:s['sha256'] for s in previous['sources']}
    rows, sources, missing, drift = [], [], [], []
    now = datetime.now(timezone.utc).isoformat()
    for directory in dirs:
        name = directory.name
        row = {'name':name, **annotations[name], 'path':str(directory),
               'observed_at':now, 'sibling_execution_in_this_review':False,
               'consumer_acceptance':False, 'source_ids':[], 'declared_console_scripts':{}}
        if name == '.local':
            row['inspection']='Directory identity only; contents excluded'
            rows.append(row)
            continue
        row['repository_revision'] = inventory.git(directory,'rev-parse','HEAD')
        row['git_common_dir'] = inventory.git(directory,'rev-parse','--path-format=absolute','--git-common-dir')
        row['revision_scope']='HEAD plus selected working-file hashes; no clean-tree assumption'
        for relative in ['AGENTS.md','README.md','pyproject.toml']+inventory.SELECTED.get(name,[]):
            path = directory/relative
            if not path.is_file():
                missing.append({'directory':name,'selected_path':relative,'claim':'Absent selected path, not absence of a capability'})
                continue
            anchors = ['Dated inventory scope; inherited selected anchors retained when bytes unchanged']
            claims = ['Selected local identity, declared role and scope only; no execution or independent acceptance']
            if relative == 'pyproject.toml':
                meta = tomllib.loads(path.read_text()).get('project',{})
                row['package_metadata'] = {k:meta.get(k) for k in ['name','version','requires-python','license']}
                row['declared_console_scripts'] = meta.get('scripts',{})
                anchors = ['[project] and [project.scripts]']
                claims = ['Declared dependency/runtime and launcher metadata only']
            elif path.suffix == '.py':
                row.setdefault('source_interfaces',[]).append({'path':relative,**inventory.source_structure(path)})
                anchors = ['AST top-level classes, functions and annotated fields; no import']
            elif relative == 'README.md':
                anchors = ['Opening product/status paragraphs and selected usage, runtime, limitation and license passages']
            elif relative == 'AGENTS.md':
                anchors = ['Read-only boundaries and project ownership; unrelated campaigns not resumed']
            else:
                anchors = ['Complete selected license/notice text; rights not transferred by inventory']
            item = inventory.observe(path,anchors,claims)
            item.update(repository_revision=row['repository_revision'],
                        version_date='Working files observed 2026-10-14; post-cutoff environment delta, not backdated literature')
            prior = old_hashes.get(str(path))
            item['inherited_identity_unchanged'] = prior == item['sha256']
            if prior and prior != item['sha256']:
                drift.append({'source_identity':str(path),'prior_sha256':prior,'current_sha256':item['sha256']})
            sources.append(item)
            row['source_ids'].append(str(path))
        if name == 'dsge_hmc':
            row['nested_checkouts'] = [{'name':n,'revision':inventory.git(directory/n,'rev-parse','HEAD')}
                                      for n in ['main-baseline','original-main','sgu-neural-training-plan']]
        rows.append(row)
    unstable = [x['source_identity'] for x in sources if inventory.digest(Path(x['source_identity'])) != x['sha256']]
    assert not unstable, unstable
    current = {'operation':OP,'observed_at':now,'literature_cutoff':'2026-10-07',
               'cutoff_limit':'This is a separately labeled current local environment observation.',
               'directories':rows,'sources':sources,'changed_from_IN01':drift,
               'selected_paths_not_found':missing,'sibling_writes':0,'sibling_code_executions':0,
               'source_copy_policy':'Local originals retained in place; no sibling implementations copied or redistributed',
               'historical_inventory':ref(OLD/'workspace-inventory.json','18-directory predecessor'),
               'collector':ref(Path(__file__),'Bounded read-only collector and exact local replay')}
    write(BASE/'inventory.json',current)
    # Exact examples execute only project-authored mathematics inside causal.
    replays = []
    for tool, filename in [('workspace_examples_20261013.py','examples.json'),
                           ('workspace_composition_20261013.py','composition.json'),
                           ('workspace_approximation_20261013.py','approximation.json')]:
        target=BASE/filename
        p=subprocess.run([sys.executable,str(ROOT/'tools'/tool),'--output',str(target)],
                         cwd=ROOT,capture_output=True,text=True,timeout=25)
        assert p.returncode==0,p.stderr
        assert json.loads(target.read_text())==json.loads((PRIOR/filename).read_text()),filename
        replays.append(ref(target,'Fresh exact local replay equals preserved reference'))
    primary = json.loads((PRIOR/'primary-inspection.json').read_text())
    for item in primary['sources']:
        assert inventory.digest(Path(item['source_identity']))==item['sha256']
    transport=json.loads((ROOT/'docs/program/repair-v12/work/IN04/transport-checks.json').read_text())
    faults=json.loads((ROOT/'docs/program/repair-v12/work/IN04/fault-trials.json').read_text())
    assert transport['status']=='pass' and transport['scientific_cases']==11
    assert all(c['status']=='pass' for c in faults['cases'])
    metadata={r['name']:r.get('package_metadata',{}) for r in rows}
    assert '<3.12' in metadata['cardnpv']['requires-python']
    assert '>=3.12' in metadata['hponas']['requires-python']
    obligations = {
      'BayesFilter':['Bind target/model/data coordinates and approximation semantics; reject unqualified error certification.','Causal-side serialization/parity fixture, exact backend/version, provider owner and actual target-runtime outcome.'],
      'DynareMCP':['Separate normalized structural model/timing artifacts from transport replies.','Current stdio/CLI transport conformance, model restrictions and owner-selected version.'],
      'FinMarketing':['Preserve entity/source owner/permission, target kind and lexicographic availability-cutoff-decision clocks.','Roundtrip source/schema fixture plus negative stale-feature, population/target mismatch and missing authority cases.'],
      'MOONeural':['Resolve README 0.1.27 versus metadata 0.1.28; freeze solver target and independent evaluation.','Task-specific constraint accuracy and rate/error argument, dependency rights and separate runtime.'],
      'MacroFinance':['Preserve positive dollar-scarcity basis convention, units/horizon, conditional model and numerical authority.','Resolve historical absolute import path, canonical revision, model assumptions and selected provider conformance.'],
      'MacroFinance-ccma-g-v7-neutra-r9':['Retain distinct HEAD and shared family identity.','Select intended model/revision before a separate scoped contract trial.'],
      'MacroFinance-dz5-neutra':['Retain distinct HEAD and shared family identity.','Select intended model/revision before a separate scoped contract trial.'],
      'MathDevMCP':['Carry located mathematical obligations and evidence without promoting a symbolic response to proof.','Pinned protocol/schema and dependency/controlled-use terms; independent substantive review.'],
      'SMEwallet':['Map declared accounting primitives to a named intervention and estimand before implementation.','Owner-selected current model specification and actual consumer surface; primitive formulas are not an estimator.'],
      'cardnpv':['Retain historical-minus-perfect target, declared finite horizon and continuation status.','Reject conversion of negated perfect-execution gap into a feasible policy effect; qualify serializer with true consumer.'],
      'causal':['Preserve nine admitted local reference operations and semantic refusals; unimplemented methods remain explicit.','Broader estimator/adapters, new transport versions, target platform and external consumer acceptance remain open.'],
      'dataml':['Preserve origin linkage, sampling/inclusion, observation/availability clocks and owner declarations.','Actual export/schema/version agreement and acceptance by observation owner; generated identity cannot establish truth.'],
      'dsge_hmc':['Treat as a container with three recorded nested revisions.','Choose canonical model/source before an API claim; no automatic adoption of archived computation.'],
      'hponas':['Keep objective/model/data/protocol declaration, search budget and protected final evaluation.','Isolated Python3.12+ boundary; select a supported learner family and qualify post-selection inference separately.'],
      'humanvoice':['Only a separate manuscript child with full claim/equation/citation retention; frozen evidence untouched.','Editorial handoff after scientific content, exact claim regression and named reader acceptance; not scientific independence.'],
      'research-assistant':['Read-only navigation and custody of real primary PDFs; summaries cannot replace inspected originals.','Actual schema/transport conformance and citation identity/anchor checks for the selected source workflow.'],
      'claudecodex':['Exclude agent policy installers from the causal runtime.','No runtime qualification proposed; shared policy changes remain outside this program.'],
      '.local':['Exclude ambient environment contents from product integration.','No integration proposed; only directory identity recorded.']}
    acceptance=[{'directory':r['name'],'disposition':r['disposition'],
                 'semantic_contract':obligations[r['name']][0],
                 'remaining_case_and_owner_input':obligations[r['name']][1],
                 'actual_consumer_acceptance':False} for r in rows]
    local = {'status':'pass','scope':'Current source disposition, inherited actual local evidence and fresh exact examples only',
             'actual_inherited':{'scientific_transport_cases':11,'fault_cases':len(faults['cases']),
                 'protocol':transport['protocol'],'reexecuted_this_review':False,
                 'evidence':[ref(ROOT/'docs/program/repair-v12/work/IN04/receipt.json','Preserved bounded runtime scope'),
                             ref(ROOT/'docs/program/repair-v12/work/IN04/transport-checks.json','Actual library/CLI/stdio outcomes'),
                             ref(ROOT/'docs/program/repair-v12/work/IN04/fault-trials.json','Actual local fault cases')]},
             'exact_reexecuted':replays,'static_sibling_interfaces':ref(BASE/'inventory.json','Current18-directory source observations'),
             'current_primary_contracts':ref(PRIOR/'primary-inspection.json','Four unchanged key sources; exact anchors reread'),
             'environment_conflict':{'cardnpv':metadata['cardnpv']['requires-python'],'hponas':metadata['hponas']['requires-python'],
                 'common_interpreter':'Empty declared intersection; propose separate pinned environments and serialized target-preserving artifacts'},
             'semantic_refusals':['Do not turn card historical-minus-perfect value into a feasible policy contrast.',
                 'Reject features available after cutoff or at an unadmitted decision sequence.',
                 'Retain graph-equivalence effect sets; no causal effect from a correlation alone.',
                 'Unknown/zero inclusion and unverified origin truth cannot be corrected by a transport.',
                 'Do not pool conditional populations, overlapping interventions or internal transfers naively.',
                 'A conditional numerical error bound does not supply statistical identification or confidence.'],
             'actual_sibling_trials':0,'mock_consumer_trials':0,'synthetic_examples':'Project-authored finite laws only',
             'remaining_cases':acceptance}
    write(BASE/'evidence-and-acceptance.json',local)
    limits=['Proposal requirement author review; no independent or institutional acceptance.',
            'Selected source/metadata inspection is not exhaustive call-chain or runtime qualification.',
            'External originals are mutable; recheck hashes and copying rights before implementation.',
            'Public/generated evidence is appropriate for this proposal; expensive authentic bank tests are later conditional work.',
            'All actual inherited runtime claims retain their frozen environment, protocol and limited method scope.']
    review={'operation_id':OP,'status':'pass','reviewer':{'name':'Codex author/coordinator','kind':'author'},
            'scope':'All18workspace directory dispositions and concrete target-preserving acceptance cases, with no sibling changes',
            'directory_count':len(rows),'source_count':len(sources),'changed_sources':len(drift),
            'findings':['All18directory identities remain; every directory has a current disposition and next acceptance case.',
                        'Current HPO-NAS declarations replace the obsolete Tier0-blocked wording; upstream qualification is not transferred.',
                        'MOONeural version mismatch and MacroFinance historical import path remain explicit unresolved interface inputs.',
                        'CardNPV and HPO-NAS have incompatible declared in-process Python ranges; isolated exchange is the proposed boundary.',
                        'Exact funding, servicing, graph, observation, clock, accounting, population and numerical-approximation references replay unchanged.'],
            'evidence':[ref(BASE/'inventory.json','Current inventory and nine-source drift'),
                        ref(BASE/'evidence-and-acceptance.json','Execution labels and all remaining cases')]+replays,
            'limitations':limits,'original_gap_qualification':False,'consumer_acceptance':False}
    write(OUTPUT,review)
    state=core.read(ROOT,core.STATE); graph,_,_=run.combined(ROOT,state)
    receipt=run.ledger.receipt_template(run.ledger.operation(graph,OP))
    receipt.update(outcome='pass',execution='performed',scope=review['scope'],reviewer=review['reviewer'],
                   limitations=limits,outputs=[ref(OUTPUT,'Reviewed requirement outcome')],nonexecution_reason='',revisit_trigger='',
                   criteria=[{'index':0,'verdict':'pass','finding':'Every directory has a current dated source disposition and explicit local/external acceptance case; incompatible environments, owner inputs and deferred/excluded projects are retained.',
                              'evidence':[ref(BASE/'inventory.json','Current18-directory inventory'),ref(BASE/'evidence-and-acceptance.json','Per-directory contracts and remaining cases')]},
                             {'index':1,'verdict':'pass','finding':'Three exact reference families replay identically; inherited actual local transport/fault evidence is separated from static sibling inspection and proposed integrations. Semantic refusals and owner inputs are explicit.',
                              'evidence':[ref(BASE/'evidence-and-acceptance.json','Evidence labels and limitations')]+replays}])
    write(BASE/'operation-receipt.json',receipt)
    print(json.dumps({'directories':len(rows),'source_records':len(sources),'drift':len(drift),'exact_replays':3,'sibling_writes':0,'outcome':'proposal_requirement_pass'}))


if __name__=='__main__':
    main()

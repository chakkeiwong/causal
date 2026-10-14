"""Offline proposal-to-fixed-tool reference controller (LA05).

The trusted caller supplies grants; this module is not a bank authentication
service or an LLM backend. Retrieved bytes and proposals cannot grant tools.
Only a narrow, explicit static ATE projection is implemented. Full declarations
are retained even when no numerical operation can answer them.
"""
from copy import deepcopy
from dataclasses import asdict, dataclass, field
import hashlib
import json
from pathlib import Path
import re

from .artifacts_v12 import ROOT, atomic, bounded_read, digest, encode, local_root
from .operation_contract_v12 import context_digest, finite_json, validate_response
from .problem_contract_v12 import declaration_digest, review_problem
from .runtime_v12 import Runtime, execution_identity, locked

OPERATIONS = frozenset({'graph.review', 'graph.discover', 'identify.effect', 'estimate.effect'})
MAX_PROPOSAL = 500_000


@dataclass(frozen=True)
class ReviewGrant:
    """Trusted local caller input, never parsed from a model response.

Binding a digest prevents silent revision changes, but is not a signature or
proof that an assumption is true. External authentication is out of scope.
"""
    declaration_sha256: str
    operations: tuple[str, ...]
    sampling: dict
    reviewer: str
    numerical_inputs: dict = field(default_factory=dict)


def validate_proposal(proposal):
    finite_json(proposal)
    if not isinstance(proposal, dict) or set(proposal) != {
            'schema_version', 'problem', 'diagram', 'operations', 'model_record'}:
        raise ValueError('Proposal fields must match the fixed envelope; no commands or permission grants')
    if proposal['schema_version'] != 'causalbank.agent-proposal/1':
        raise ValueError('Unsupported proposal version')
    if len(encode(proposal)) > MAX_PROPOSAL:
        raise ValueError('Proposal exceeds bounded input size')
    ops = proposal['operations']
    if (not isinstance(ops, list) or not ops or any(not isinstance(op, str) for op in ops)
            or len(set(ops)) != len(ops) or not set(ops) <= OPERATIONS):
        raise ValueError('Only distinct fixed causal operations can be proposed')
    if not isinstance(proposal['problem'],dict) or not isinstance(proposal['diagram'],dict):
        raise ValueError('Problem and diagram must be typed objects')
    record = proposal['model_record']
    if not isinstance(record, dict) or set(record) != {
            'mode', 'provider', 'model', 'revision', 'prompt', 'prompt_sha256', 'parameters', 'usage'}:
        raise ValueError('Incomplete or extended model record')
    if record['mode'] not in {'offline_fixture', 'recorded_model_output'}:
        raise ValueError('Live model calls are unavailable in this controller')
    if any(not isinstance(record[k], str) or not record[k] for k in ['provider', 'model', 'revision']):
        raise ValueError('Model identity fields must be nonempty strings')
    if (not isinstance(record['parameters'], dict) or not isinstance(record['prompt_sha256'],str)
            or not re.fullmatch(r'[0-9a-f]{64}', record['prompt_sha256'])):
        raise ValueError('Model parameters and exact prompt hash required')
    if (not isinstance(record['prompt'],str) or
            hashlib.sha256(record['prompt'].encode()).hexdigest() != record['prompt_sha256']):
        raise ValueError('Prompt bytes do not match their recorded identity')
    if record['usage'] is not None:
        raise ValueError('Imported usage is unverified; keep it unavailable in this offline prototype')
    if (not isinstance(proposal['diagram'].get('models'),list)
            or not isinstance(proposal['problem'].get('evidence'),list)):
        raise ValueError('Graph models and evidence must be arrays')
    if len(proposal['diagram']['models']) > 16 or len(proposal['problem']['evidence']) > 32:
        raise ValueError('Prototype graph/source count bound exceeded')


def verify_sources(problem):
    """Check bounded local bytes; do not execute or follow instructions in them."""
    verified = []
    for source in problem['evidence']:
        path = ROOT / source['local_path']
        if not path.is_relative_to(ROOT/'docs') or path != path.resolve():
            raise ValueError('Evidence must be a nonsymlink local docs path')
        data = bounded_read(path, 16 * 1024 * 1024)
        if hashlib.sha256(data).hexdigest() != source['sha256']:
            raise ValueError('Evidence bytes changed: ' + source['id'])
        verified.append(deepcopy(source))
    return verified


def _selected(problem):
    return next(t for t in problem['estimand_alternatives'] if t['id'] == problem['resolution']['selected_id'])


def project_context(problem, model, sampling, declaration_ref, source_refs):
    """Explicit supported mapping; unsupported semantics never become an ATE."""
    t = _selected(problem)
    if (t['family'] != 'ATE' or t['target_measure']['kind'] != 'population_uniform'
            or t['population_condition'] or t['horizon']['start'] != 0):
        raise ValueError('Only unconditional static population ATE with horizon origin zero is mapped')
    for regime, value in [('intervention', 1), ('comparator', 0)]:
        r = t[regime]
        if (r['kind'] != 'static' or len(r['actions']) != 1
                or r['actions'][0]['variable'] != t['treatment']
                or isinstance(r['actions'][0]['value'], bool)
                or r['actions'][0]['value'] != value or r['actions'][0]['rule'] is not None):
            raise ValueError('Only static 1-versus-0 contrast on one action is mapped')
    if set(model['nodes']) != {v['id'] for v in problem['variables']}:
        raise ValueError('Graph must explicitly account for every declared variable in this projection')
    variables = []
    for v in problem['variables']:
        role = ('action' if v['id'] == t['treatment'] else 'outcome' if v['id'] == t['outcome']
                else 'latent' if v['measurement'] == 'latent' else
                'adjustment' if v['id'] in t['adjustment']['variables'] else 'observed')
        # Frozen per-operation schemas accept only these fields. The complete
        # clocks, measurement lineage and definitions remain in declaration_ref.
        variables.append({'id':v['id'], 'role':role, 'unit':v['unit']})
    outcome = next(v for v in problem['variables'] if v['id'] == t['outcome'])
    if t['loss']['unit'] != outcome['unit']:
        raise ValueError('Outcome and target loss units differ; no utility transformation is implemented')
    context = {
        'target':{'kind':'average_effect','treatment':t['treatment'],'outcome':t['outcome'],'contrast':'1-versus-0'},
        'population':{'definition':t['population'],'unit':problem['unit_of_analysis']},
        'variables':variables, 'intervention':{'kind':'set','value':t['treatment']+'=1 versus 0'},
        'horizon':{'value':t['horizon']['end'],'unit':problem['clock']['unit']},
        'units':[outcome['unit']], 'sign_convention':'intervention-minus-comparator',
        'observation_clock':{'event_time':'declared_event_time','available_time':'declared_available_time',
             'decision_time':'declared_decision_time','rule':'explicit_alternative',
             'alternative_justification':'Full LA02 numeric decision/information clocks are retained in source_evidence; LA02 declaration validator applied. No row-clock audit is inferred.'},
        'sampling':deepcopy(sampling),
        'assumptions':[{'id':a['id'],'statement':a['statement'],
                       'status':'contradicted' if a['status']=='contradicted' else 'declared',
                       'evidence':[source_refs[e] for e in a['evidence_refs']]} for a in problem['assumptions']],
        'graph':{'kind':model['kind'], 'edges':[{
            'left_node':e['left'],'right_node':e['right'],'left_mark':e['left_mark'],'right_mark':e['right_mark'],
            'evidence_type':'assumption', 'review_status':'declared',
            'evidence_refs':[source_refs[x] for x in e['evidence_refs']]} for e in model['edges']]},
        'source_evidence':[declaration_ref,*source_refs.values()]}
    # The projection never upgrades a synthetic or human declaration to truth.
    return context


class AgentWorkflow:
    def __init__(self, root=ROOT/'.runtime/agent-v12'):
        self.runtime = Runtime(root)
        self.store = self.runtime.store
        self.journal = local_root(self.runtime.root/'agent-journal')

    def prepare(self, proposal, grant, *, previous=None):
        """Validate and prepare immutable requests, without invoking a tool."""
        validate_proposal(proposal)
        problem, diagram = proposal['problem'], proposal['diagram']
        previous_diagram = None
        if previous is not None:
            validate_proposal(previous)
            previous_diagram = previous['diagram']
        review = review_problem(problem, diagram, previous_diagram=previous_diagram)
        base = {'status':'blocked','review':review,'requests':[],
                'qualification':'offline_semantics_only','model_record':deepcopy(proposal['model_record']),
                'proposal_sha256':digest(proposal),'previous_proposal_sha256':digest(previous) if previous else None}
        base['proposal_ref']=self.store.put(proposal,'causalbank.agent-proposal/1','agent_proposal')
        base['previous_proposal_ref']=(self.store.put(previous,'causalbank.agent-proposal/1','agent_proposal') if previous else None)
        if review['gate'] == 'invalid':
            return {**base,'status':'rejected','reason':'invalid_declaration'}
        try:
            sources = verify_sources(problem)
        except (ValueError, OSError) as exc:
            return {**base,'status':'rejected','reason':'source_integrity','detail':str(exc)}
        snapshot = self.store.put({'problem':problem,'diagram':diagram}, 'causalbank.declaration/1', 'causal_declaration')
        base['declaration_ref'] = snapshot
        if review['gate'] != 'ready_for_formal_analysis':
            return {**base,'reason':'unresolved_declaration'}
        if (not isinstance(grant, ReviewGrant) or not grant.reviewer
                or grant.declaration_sha256 != declaration_digest(problem, diagram)
                or not set(proposal['operations']) <= set(grant.operations)
                or not set(grant.operations) <= OPERATIONS):
            return {**base,'reason':'missing_or_mismatched_external_grant'}
        if (not isinstance(grant.sampling, dict) or set(grant.sampling) != {'law','unit','fold_unit'}
                or any(not isinstance(x,str) or not x for x in grant.sampling.values())
                or grant.sampling['unit'] != problem['unit_of_analysis']):
            return {**base,'status':'rejected','reason':'invalid_external_sampling_declaration'}
        source_refs = {s['id']:self.store.put(s, 'causalbank.source-record/1','source_evidence') for s in sources}
        targets = [m for m in diagram['models'] if problem['resolution']['selected_id'] in m['estimand_ids']]
        if len(targets)*len(proposal['operations'])>16:
            return {**base,'status':'unsupported','reason':'operation_count_bound'}
        plan = []
        for model in targets:
            try:
                context = project_context(problem, model, grant.sampling, snapshot, source_refs)
            except ValueError as exc:
                return {**base,'status':'unsupported','reason':'unmapped_target','detail':str(exc)}
            for operation in proposal['operations']:
                parameters = {'graph.review':{'review_kind':'syntax'},
                    'graph.discover':{'algorithm_id':'unconfigured','algorithm_version':'unavailable'},
                    'identify.effect':{'method_id':'backdoor'},
                    'estimate.effect':{'engine_id':'reference-moment-sets','estimator_id':'gaussian-residual-inversion'}}[operation]
                inputs = deepcopy(grant.numerical_inputs.get(model['id'], [])) if operation == 'estimate.effect' else []
                key = digest({'proposal':proposal, 'grant':asdict(grant), 'model':model['id'], 'operation':operation})
                request = {'schema_version':'causalbank.request/1.0.0','request_id':'agent-'+key[:24],
                    'operation':operation,'artifact_inputs':inputs,'parameters':parameters,
                    'scientific_context':context,'idempotency_key':'agent-'+key,
                    'budget':{'wall_seconds':10,'memory_bytes':1024**3,'max_output_bytes':500_000,'model_calls':0}}
                plan.append({'model_id':model['id'],'request':request})
        return {**base,'status':'prepared','requests':plan,'graph_candidates':len(targets)}

    def run(self, proposal, grant=None, *, previous=None, interrupt_after=None):
        """Execute or resume fixed tools; interrupt_after is a local fault fixture."""
        prepared = self.prepare(proposal, grant, previous=previous)
        if prepared['status'] != 'prepared':
            return prepared
        identity = {'proposal_sha256':digest(proposal), 'grant_sha256':digest(asdict(grant)),
                    'previous_sha256':digest(previous) if previous else None,
                    'requests_sha256':digest(prepared['requests']), 'runtime':execution_identity(),
                    'controller_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                    'declaration_validator_sha256':hashlib.sha256((ROOT/'src/causalbank/problem_contract_v12.py').read_bytes()).hexdigest(),
                    'declaration_schemas':{name:hashlib.sha256((ROOT/'docs/program/repair-v12/work/LA02'/name).read_bytes()).hexdigest()
                                           for name in ['problem-schema.json','diagram-schema.json']}}
        for step in prepared['requests']:
            self.runtime._verify_refs(step['request'],8*1024**2)
        key = digest(identity)
        path = self.journal/(key+'.json')
        with locked(self.journal/(key+'.lock')):
            if path.exists() or path.is_symlink():
                state = json.loads(bounded_read(path))
                if state['identity'] != identity or state['checkpoint_sha256'] != digest(state['results']):
                    raise ValueError('Journal identity or result hash changed')
                if not isinstance(state['results'],list) or len(state['results'])>len(prepared['requests']):
                    raise ValueError('Journal is not a prefix of the planned operations')
                for step, saved in zip(prepared['requests'],state['results']):
                    if saved['model_id'] != step['model_id']:
                        raise ValueError('Journal graph identity changed')
                    validate_response(step['request'],saved['response'])
                    self.runtime._verify_refs(saved['response'],8*1024**2)
            else:
                state = {'identity':identity,'results':[],'checkpoint_sha256':digest([]),'complete':False}
                atomic(path,state)
            for step in prepared['requests'][len(state['results']):]:
                response = self.runtime.invoke(step['request'])
                state['results'].append({'model_id':step['model_id'],'response':response})
                state['checkpoint_sha256']=digest(state['results'])
                atomic(path,state)
                if interrupt_after == len(state['results']):
                    raise InterruptedError('Injected local interruption after durable tool result')
            state['complete']=True
            atomic(path,state)
            responses = state['results']
        dispositions = [r['response']['disposition'] for r in responses]
        status = ('ambiguous' if prepared['graph_candidates']>1 else
                  'unsupported' if all(d=='unsupported' for d in dispositions) else
                  'completed_with_limits' if any(d!='computed' for d in dispositions) else 'completed')
        record = {**prepared,'status':status,'results':responses,'journal_identity':key,
                  'usage':{'live_model_calls':0,'model_tokens':None,'model_cost':None},
                  'qualification':'Local fixed-tool semantics only; no live-model quality, bank truth or policy authorization',
                  'report':{'target_id':proposal['problem']['resolution']['selected_id'],
                     'graph_candidate_count':prepared['graph_candidates'],
                     'dispositions':dispositions,'unresolved':prepared['review']['obligations'],
                     'bank_action_authorized':False}}
        record['result_ref']=self.store.put(record,'causalbank.agent-result/1','agent_result')
        return record

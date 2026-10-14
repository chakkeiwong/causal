#!/usr/bin/env python3
"""Record a prospective evaluation and unavailable inputs, without a trial."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT/'docs/program/repair-v12/work/LA06'


def ref(path,anchor):
    return {'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'anchor':anchor}


def save(name,value):
    (WORK/name).write_text(json.dumps(value,indent=2)+'\n')


def prepare():
    WORK.mkdir(parents=True,exist_ok=True)
    requirements=[
      {'id':'model_backend','observed':'LA05 has no live provider adapter; its validated modes are offline_fixture and recorded_model_output.',
       'evidence':ref(ROOT/'src/causalbank/agent_workflow_v12.py','validate_proposal live-mode rejection and exact model record'),
       'needed':'Named provider/model revision, backend implementation, terms/custody review, generation settings and permitted endpoint.',
       'resume':'Implement the selected adapter separately, qualify transport/custody/timeouts and freeze exact model/version evidence.'},
      {'id':'budget_prices','observed':'LA05 exports zero live calls and unavailable tokens/cost. No priced model-comparison budget is supplied in that contract.',
       'evidence':ref(ROOT/'docs/program/repair-v12/work/LA05/prototype-evidence.json','Offline execution scope and zero live calls'),
       'needed':'Dated actual input/output/cache/tool prices, all-method request limits, approved currency ceiling and overrun rule.',
       'resume':'Bind a priced budget to the protocol. Stop before requests when required pricing is unknown; do not assume zero cost.'},
      {'id':'heldout_cases','observed':'Existing LA02 cases and LA05 fixtures have already been authored, inspected and used for implementation tests.',
       'evidence':ref(ROOT/'docs/program/repair-v12/work/LA02/casebook.json','Four exposed development fixtures'),
       'needed':'Independent held-out mechanism manifest plus original benchmark bytes and verified label semantics; development examples excluded.',
       'resume':'Acquire/generate a sealed test set through an independent custodian, verify truth/generator assumptions and freeze before study registration.'},
      {'id':'expert_adjudication','observed':'The master program lists independent review and bank truth as required roles; no accepted evidence supplies those inputs.',
       'evidence':ref(ROOT/'docs/program/master/external-inputs.md','Independent reviewers, bank scientific owners and authentic input contracts'),
       'needed':'Named independent business/diagram adjudicators, task rubric, conflict resolution, assessor blinding and signed judgments.',
       'resume':'Enroll reviewers and resolve target/diagram disagreements without revealing method identity; retain unresolved labels.'},
      {'id':'numerical_baselines','observed':'The frozen local service advertises no discovery backend and only a supplied-DAG back-door and moment-inversion subset.',
       'evidence':ref(ROOT/'src/causalbank/operation_service_v12.py','SUPPORTED and explicit unsupported operations'),
       'needed':'Pinned, licensed numerical discovery/identification/longitudinal baselines qualified through SW07/IN03 for selected regimes.',
       'resume':'Complete candidate adoption and adapter tests; exclude unsupported cells explicitly and preserve full coverage obligations.'},
    ]
    save('unavailability.json',{'status':'unavailable','observed_date':'2026-10-12','requirements':requirements,
      'boundary':'No credentials were read, no endpoints probed and no provider-wide claim of unavailability is made. These are missing inputs to this program, not a claim that the market lacks usable models.'})
    protocol={
      'task_id':'LA06','status':'reviewed_prospective_design_not_registered',
      'final_evaluation_authorized_to_start':False,'registration':None,
      'reason':'Exact backend, independent holdout/adjudication, qualified baselines and priced budget must be bound before final registration.',
      'primary_question':'Does assistance improve correct, usable causal decisions at a declared total cost relative to a fixed numerical/analyst workflow?',
      'methods':[
       {'id':'data_only','spec':'Prespecified numerical baseline using identical observed data and allowed metadata; no language prior.'},
       {'id':'llm_only','spec':'Frozen prompt and schema; supplied data summaries permitted exactly as declared; no numerical discovery-tool loop.'},
       {'id':'retrieval','spec':'Same model with frozen primary-text corpus, top-k and retrieval rule; all retrieved bytes retained.'},
       {'id':'hybrid','spec':'Same numerical baseline plus explicitly typed model proposals/constraints; all adaptation and stopping rules frozen.'},
       {'id':'expert_assisted','spec':'Structured ordinary expert workflow and a separately timed expert-plus-model arm; expert time and information explicitly matched.'}],
      'strata':['independent sufficient DAG','latent ADMG/PAG','time-series with known lag/clock','treatment-confounder feedback',
                'panel/quasi-experimental assignment','proxy/linkage/selection','weak/nonidentifying effect','business target and monetary loss ambiguity'],
      'planning_allocation':{'independent_mechanisms':400,'per_stratum':50,
        'label_evidence_conditions':['ordinary labels and relevant evidence','unfamiliar labels','misleading or irrelevant retrieved evidence','numeric/text conflict'],
        'stochastic_repetitions':3,'unit_of_analysis':'Mechanism, with variants and repetitions nested; never count repeated prompts as independent worlds.',
        'precision_limit':'N=400 is a planning allocation, not a demonstrated power result. Worst-case normal half-width for one Bernoulli proportion is about 0.049; paired differences can be less precise. Final precision/power and cost design requires a separate development pilot excluded from the final test.',
        'final_sample_size':None},
      'information_matching':'Same observed data, target and permissible scientific metadata per matched cell; knowledge and tool differences explicitly defined by arm. Report both natural workflow and matched compute/time budget comparisons.',
      'freeze_required':['independent test identities and original byte hashes','source applicability/adjudication labels and uncertainty',
         'model/provider revision, actual generation settings, seed support and prompts','retriever/corpus/ranker/chunking identities',
         'numerical algorithms, versions, hyperparameters and scientific assumptions','method-specific tools and maximum calls/iterations',
         'tokens, wall time, expert time and currency budgets including retries','development/test split, all stopping/selection rules and analysis script'],
      'contamination_control':['Exclude LA02/LA05 exposed fixtures from final quality estimation.',
         'Cross label novelty with mechanism novelty; a renamed public graph is not an independent unseen mechanism.',
         'Keep mechanism families split between development and test; cluster dependence in inference.',
         'Quarantine CLadder IV-as-population-ATE cells pending generator/assumption verification.',
         'Verify CausalDS target/observation and missing-identification metadata before using scorer labels.',
         'No prompt/retriever/prior-strength tuning on test outcomes; changes create a new registered revision.'],
      'metrics':{
        'problem':'Correct population/unit/actions/comparator/horizon/target measure/availability clocks; critical semantic errors and unresolved owner questions separately.',
        'evidence':'Supported claim precision, applicability and contradiction/missing-source handling against independent judgments.',
        'graph':'Adjacency and endpoint precision/recall against the declared identifiable equivalence class; orientation informativeness separately. Do not penalize justified circles as missing truth or reward an unsupported fully directed graph.',
        'identification':'Correct functional/target or valid set/refusal under the stated class; separate unsupported backend, invalid output, explicit abstention and scientific nonidentification.',
        'effect':'Bias/error only for identified scalar targets; coverage and set topology, all-request availability, finite width conditional on availability, whole-line and empty-set rates reported separately.',
        'interval_loss':'For finite single intervals only: (u-l)+2/alpha*(l-theta)*1(theta<l)+2/alpha*(theta-u)*1(theta>u). Preserve raw uncapped scores. For unions use coverage and Lebesgue length, retaining infinite length; no midpoint or interval-score substitution.',
        'decision':'Known-SCM expected loss under the actual feasible policy; authentic bank value remains a separate external trial.',
        'cost':'Calls, input/output/cache tokens, numerical CPU/wall/memory, retrieval, tool retries, expert review/rework and actual dated prices. Unknown components stay missing.',
        'failures':'All planned requests enter denominators: computed, ambiguous, abstained, malformed, unsupported, timed out, refused and unavailable.'},
      'analysis':'Paired comparisons by independent mechanism with nested stochastic repeats/label variants; mechanism-level bootstrap or a justified finite-sample alternative specified before registration. Report uncertainty for each outcome and multiplicity policy; no global winner from one graph score.',
      'qualification_rule':'No positive model/capability claim without prespecified target-error limits, effect/set calibration and availability, evidence-grounded interpretation and full cost limits. Numeric acceptance thresholds remain unset until decision loss and review budget are supplied.',
      'next_registration_command':'python3 tools/causal_program_v12.py register LA06 --protocol PATH (use the final completed protocol and controller format; this design is not registration)',
      'development_evidence':[ref(ROOT/'docs/program/repair-v12/work/LA05/receipt.json','80 local conformance tests and six paths; not final empirical evidence'),
                               ref(ROOT/'docs/program/repair-v12/work/LA03/response-count-derivation.json','Exact analytical response-null counterexample, not a model run')]
    }
    save('protocol.json',protocol)
    save('results.json',{'status':'unavailable','final_evaluations_run':0,'model_quality_results':[],
      'live_model_calls':0,'model_tokens':None,'model_cost':None,'expert_scores':None,
      'local_conformance':'LA05 is separately completed. Its authored fixtures are development evidence and have not been relabeled as a benchmark.',
      'qualification':'none','unavailability':ref(WORK/'unavailability.json','Missing inputs and exact resumption steps')})
    save('journal.json',{'status':'no_final_experiment_started','events':[
      {'event':'reviewed_local_baseline','evidence':ref(ROOT/'docs/program/repair-v12/work/LA05/verification.json','80 conformance checks')},
      {'event':'identified_missing_final_study_inputs','evidence':ref(WORK/'unavailability.json','Five prerequisite classes')},
      {'event':'wrote_prospective_design','evidence':ref(WORK/'protocol.json','Not registered; final size/models/budgets unresolved')},
      {'event':'withheld_final_evaluation','reason':'Do not fabricate unavailable backend, independent labels, holdout or spending authority.'}]})
    print(json.dumps({'final_evaluations_run':0,'missing_prerequisite_classes':len(requirements),'protocol_status':protocol['status']}))


if __name__=='__main__':
    prepare()

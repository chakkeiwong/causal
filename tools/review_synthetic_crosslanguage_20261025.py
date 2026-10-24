#!/usr/bin/env python3
"""Review original source contracts without executing acquired implementations."""
import argparse
import json
from pathlib import Path
import synthetic_crosslanguage_reference_20261025 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings

run=controller.base; core=run.core; ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-25/synthetic-crosslanguage-v1'
RAW=ROOT/'docs/literature/raw'
read=lambda p:json.loads(p.read_text())
OPS={
 'Java': ('Tencent Java gateway availability boundary',
          'Inspect concrete JVM estimator and engine originals, Maven interfaces and remaining leads; qualify a versioned worker bridge before any Java synthetic-control capability claim.'),
 'Cxx': ('R-facing C++ kernels, diagnostics and Bayesian/network boundaries',
         'Complete C++ numerical and R-wrapper delegates, network/Stan models and file-level rights; expose solver routes, retained populations and full failure counts before public native qualification.'),
 'other_relevant': ('Selected Julia interface, lifecycle and inference population',
                    'Inspect six additional Julia leads and other languages; resolve TreatmentPanels/JuMP/HiGHS artifacts and test panel mutation, zero effects, stopping reasons and every placebo identity.')
}
LIMITS=[
 'Bounded selected sources and 43 discovery leads; search metadata is not technical evidence, saturation or proof of absence.',
 'No acquired code, installed package or upstream test executed; conditional source findings and authored witnesses are not native failures.',
 'Rcpp or generated Stan language classification does not establish a standalone C++ estimator; a Java gateway does not establish estimator availability.',
 'Package and file notices, dependencies and distribution rights remain unresolved; no legal clearance.',
 'Counterfactual stability, assignment law, unknown network truth and arbitrary dependence have no automatic software repair.',
 'Visual, independent, bank and final acceptance remain open.'
]

def prepare():
    assert not (BASE/'review.json').exists()
    validation=read(BASE/'git-byte-validation.json')
    assert validation['status']=='pass' and validation['count']==44
    verify_bindings(validation)
    for row in validation['originals']:
        assert core.sha(ROOT/row['local_path'])==row['sha256']
    write(BASE/'exact-results.json',exact.calculate())
    groups=read(BASE/'source-spec.json');sources=[];primary=[]
    for key,(title,repo,version,checks) in groups.items():
        evidence=[];anchors=[];claims=[]
        for filename,lo,hi,tokens,finding in checks:
            p=RAW/filename;fragment='\n'.join(p.read_text().splitlines()[lo-1:hi])
            assert all(t in fragment for t in tokens),(filename,lo,hi)
            binding=ref(p,f'Lines {lo}-{hi}: {finding}')
            evidence.append(binding);anchors.append(dict(path=binding['path'],line_spans=[[lo,hi]],finding=finding));claims.append(finding)
        primary.append(dict(group=key,evidence=evidence,inspected_anchors=anchors,supported_claims=claims))
        sources.append(dict(integrated_citation_key='exec25_synthcross_'+key,kind='software',title=title,author=repo+' contributors',year=int(version.split(';')[1][-4:]),source_identity='https://github.com/'+repo+'/tree/'+version.split(';')[-1],version_date=version,local_copy=evidence[0],evidence=evidence,inspected_anchors=anchors,supported_claims=claims,limitations=LIMITS,native_execution=False))
    write(BASE/'primary-review.json',dict(status='pass_for_selected_anchors',groups=primary,evidence=[ref(BASE/'git-byte-validation.json','44 authenticated originals')],native_execution=False))
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_exact_witnesses',evidence=[ref(Path(exact.__file__),'Independent rational and label-only oracle'),ref(BASE/'exact-results.json','Reproduced exact values')],checks=['All zero-prefit simplex optima can extrapolate to different post-period contrasts.','Four-label source-loop replay selects A,B,D; stipulated variances are52/3 and35/3.','Observed inclusive rank1/3 differs from all-request bounds1/5 to3/5.','Missing network entry survives this local na.rm sum guard only; no whole-program runtime conclusion.','Zero-effect predicate and hypothetical costs reproduced; no calibration or native execution claim.']))
    for key,(title,next_action) in OPS.items():
        write(BASE/('comparison-'+key+'.json'),dict(operation='SW.CELL.synthetic_controls.'+key,status='inconclusive',scope=title,registered_candidates=[],selected_groups={'Java':['tencent'],'Cxx':['core','helpers','nasc','bsynth'],'other_relevant':['julia']}[key],limitations=LIMITS,next_action=next_action,evidence=[ref(BASE/'primary-review.json','Selected original contracts'),ref(BASE/'search-screening.json','Explicit search boundaries')]))
    write(BASE/'dependency-license-review.json',dict(status='not_complete_clearance',evidence=[ref(BASE/'primary-review.json','Inspected notices and interface boundaries')],findings=['SynthControl MIT; resolved TreatmentPanels/JuMP/HiGHS remains open.','coresynth MIT with RcppArmadillo interface; complete installed artifacts open.','SynthHelpers GPL-2 declaration; copied implementation provenance and complete terms require review.','nasc MIT with R/Stan dependencies; scientific model review open.','bsynth Apache metadata/R header and GPL-3-or-later Stan include retained without legal conclusion.','Tencent root BSD-3 does not override nested component terms.'],integration_allowed=False))
    write(BASE/'qualification-plan.json',dict(status='proposed_not_executed',fixtures=['Zero effect with no requested SE and explicit successful lifecycle state','Full identity trace through mutable panel reordering and each donor placebo','Tied/nonunique prefit optima; post-period target and solver-route agreement','Numerical fallback, feasibility, tolerance and terminal status','Every requested/failed/pruned/usable placebo and statistical selection law','Finite network entries, dimensions, isolated nodes, identity and missing ties','Unique date keys, draw identifiers and posterior model meanings','Versioned worker bridge, full dependency rights and total request costs'],owners=['Scientific author','Adapter owner','Environment/rights owner','Evaluation reviewer'],native_execution=False))
    write(BASE/'omissions-register.json',dict(global_blocker=False,evidence=[ref(BASE/'search-screening.json','Bounded discovery and uninspected candidates')],known_routes=['Inspect remaining candidates/delegates and exact installed artifacts.','Prepare public lifecycle/population/solver/interface fixtures before bank trials.','Resolve contradictory file notices with authentic distribution evidence.'],unknown_universal_repairs=['True untreated paths and unknown spillovers require added information or restrictions.','Arbitrary dependence and unverified assignment laws are not repaired by a language choice.'],next_actions={key:value[1] for key,value in OPS.items()}))
    sources.append(dict(integrated_citation_key='exec25_synthcross_choice',kind='project_evidence_not_scholarly_paper',title='Authored cross-language synthetic-control comparison and public qualification witnesses',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='25 October 2026; cutoff 7 October 2026; no native execution',local_copy=ref(BASE/'mathematical-review.json','Authored exact witnesses'),evidence=[ref(BASE/n,'Reviewed comparison boundaries') for n in ['search-screening.json','dependency-license-review.json','qualification-plan.json','omissions-register.json']]+[ref(BASE/('comparison-'+key+'.json'),'Separate language decision') for key in OPS],inspected_anchors=[dict(anchor='Targets, solver and interface boundaries, populations, rights and cost denominators',inspection='Author inspection')],supported_claims=['Selected comparison and exact authored witnesses','Three incomplete language coverage decisions and concrete next tests'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,new_records=7,new_scholarly_pdfs=0,native_execution=False));verify_bindings(read(BASE/'source-audit.json'))
    write(BASE/'plan-review-v2.json',dict(status='pass_for_inconclusive_source_work',evidence=[ref(BASE/n,'Reviewed plan against acquired evidence') for n in ['plan.md','plan-review.json','query-correction.json','primary-review.json','mathematical-review.json','dependency-license-review.json','qualification-plan.json','omissions-register.json']],findings=['Three operations reviewed separately and integrated in one wave.','44 originals authenticated; 30 exact anchor ranges; 43 leads retain bounded search limitations.','No standalone API, native failure, legal clearance, absence proof or scientific qualification inferred.','Canonical publication waits for completed Python delivery.']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_argument',evidence=[ref(BASE/'development.tex','Banking target, notation, alternatives and limitations'),ref(BASE/'sponsor-addition.md','Investment rationale')],findings=['Actual exports and runtime boundaries distinguished from repository language.','Conditional static findings, exact authored examples and proposed tests separated.','Uncertainty population, diagnostic loss and nonunique optima connected to decision target.'],visual_acceptance=False))
    names=['git-byte-validation.json','primary-review.json','search-screening.json','mathematical-review.json','exact-results.json','source-audit.json','dependency-license-review.json','qualification-plan.json','omissions-register.json','plan-review-v2.json','copyedit-review.json','development.tex','sponsor-addition.md']
    review=dict(status='pass_for_selected_source_work',operation_outcomes={key:'inconclusive' for key in OPS},evidence=[ref(BASE/n,'Reviewed source comparison') for n in names]+[ref(Path(__file__),'Review logic')],findings=['Six source groups and one authored comparison record; no new scholarly work admitted.','Three distinct language dispositions remain inconclusive.'],limitations=LIMITS,native_execution=False)
    verify_bindings(review);write(BASE/'review.json',review)
    print(json.dumps(dict(review='pass_for_selected_source_work',originals=44,new_records=7,operations=3)))

def receipt(key):
    op='SW.CELL.synthetic_controls.'+key;state=core.read(ROOT,core.STATE)
    assert state['execution_runtime']['active']['operation']==op
    verify_bindings(read(BASE/'review.json'));graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,op)
    value=read(BASE/('comparison-'+key+'.json'));value['evidence'].append(ref(BASE/'review.json','Selected source review'));output=ROOT/node['outputs'][0];write(output,value)
    evidence=[ref(BASE/n,'Reviewed bounded coverage') for n in ['review.json','search-screening.json','source-audit.json','omissions-register.json']]
    findings=['Declared candidates and bounded searches retained; technical and ecosystem coverage incomplete.','Selected technical claims bind authentic bytes, cutoff identities and inspected anchors.','Alternatives, source rights, uninspected candidates and exact next actions remain explicit.']
    result=run.ledger.receipt_template(node);result.update(outcome='inconclusive',execution='performed',scope=OPS[key][0],reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(output,'Separate bounded coverage')],criteria=[dict(index=i,verdict='inconclusive' if i==0 else 'pass',finding=finding,evidence=evidence) for i,finding in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=OPS[key][1])
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/('operation-receipt-'+key+'.json'),result)
    print(json.dumps(dict(receipt=op,outcome='inconclusive')))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);p.add_argument('key',nargs='?',choices=list(OPS));a=p.parse_args()
    if a.command=='prepare':prepare()
    else:receipt(a.key)

#!/usr/bin/env python3
"""Authenticate medflex contracts and record a scoped reference disposition."""
import argparse, hashlib, json
from pathlib import Path
import medflex_reference_20261023 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-23/medflex-reuse-v1';RAW=ROOT/'docs/literature/raw'
read=lambda p:json.loads(p.read_text())
REVIEWER=dict(name='Codex author/coordinator',kind='author')
LIMITS=['Selected cutoff sources and project-owned exact examples only; no downloaded code executed.',
 'GPL-2 declaration and separately identified local license text do not clear the full artifact, datasets or transitive dependency rights.',
 'No native conformance, empirical coverage, general mediation identification, measured banking economics or integration permission.']
SPANS={
 'R/neModel.R': [([140,164],'Bootstrap interval defaults and confidence-interval delegates.'),([203,237],'Documented full bootstrap refitting, robust branch and original-mediator exclusion.'),([329,384],'Defaults, mediator rejection and imputation-structure warning.'),([386,425],'Original-row bootstrap, working-model refitting, positional expansion mapping and optional exposure refit.'),([429,544],'GLM/family restrictions, subject-level score aggregation, off-diagonal nuisance derivatives and sandwich covariance.')],
 'R/neImpute.R': [([39,84],'Formula variable order, exposure nodes and default quantile limits.'),([174,278],'Prediction-based expansion, swapped observed/hypothetical exposure roles, impData class and refresh path.')],
 'R/neWeight.R': [([157,166],'Joint-mediator request warning and forced one-mediator path.'),([175,278],'Exposure expansion and direct mediator-density ratio; weightData class and refresh path.'),([288,328],'Formula order and continuous-node design.')],
 'R/terms-expand.R': [([1,24],'Documentation reverses weightData/impData descriptions and uses length(data) for row count.'),([28,113],'Expansion identity from original row names, factor levels, numeric quantile/random nodes and merged data.')],
 'R/utils.R': [([13,25],'Original data recovered by evaluating stored call in globalenv.'),([40,59],'Observed/hypothetical design alignment.'),([61,115],'Weighting path, pointer validation, optional exposure denominator and suppressed final GLM warnings.')],
 'man/expData.Rd': [([1,34],'Expansion documentation and reversed class descriptions; implementation and adapter fixture must resolve the discrepancy.')],
 'man/neImpute.Rd': [([1,36],'Imputation generic and declared impData return class.')],
 'man/neWeight.Rd': [([1,37],'Weighting generic and declared weightData return class.')],
 'DESCRIPTION': [([1,46],'Version0.6-11, named maintainers, GPL-2 declaration, R/dependency requirements and publication date.')],
 'man/neModel.Rd': [([54,86],'Natural-effect fit, full bootstrap, robust standard errors and mediator exclusion documented.')]
}

def audit():
 assert not (BASE/'source-audit.json').exists()
 commit=read(RAW/'v12_sw2_cran_cutoff_medflex.json')[0];tree=read(RAW/'exec23_medflex_canonical_tree.json')
 assert commit['sha']=='8699ea24da75a8e0c2830edb8c1a55ddc50a5bd2'
 assert tree['sha']==commit['commit']['tree']['sha']=='5ae7ee71883d04ca2d3c047a5f4ca8c93bec36ce' and not tree['truncated']
 assert commit['commit']['committer']['date']<'2026-10-07T15:59:59Z'
 entries={e['path']:e for e in tree['tree']}
 requests=[(r['id'],r['source_path']) for r in read(BASE/'source-manifest.json')['requests']]
 requests += [('v12_sw2_description_medflex','DESCRIPTION'),('v12_sw2_manual_medflex_1','man/neModel.Rd')]
 records=[]
 for key,path in requests:
  p=RAW/(key+'.txt');data=p.read_bytes();receipt=read(RAW/(key+'.receipt.json'))
  blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
  url='https://raw.githubusercontent.com/cran/medflex/'+commit['sha']+'/'+path
  assert blob==entries[path]['sha'] and len(data)==entries[path]['size']
  assert receipt['status']=='saved' and receipt['url']==url and receipt['sha256']==core.sha(p)
  lines=data.decode().splitlines()
  assert all(1<=lo<=hi<=len(lines) for (lo,hi),_ in SPANS[path]),(path,len(lines))
  records.append(dict(upstream_path=path,source_identity=url,version_date=commit['commit']['committer']['date'],
   local_copy=ref(p,'; '.join(s for _,s in SPANS[path])),receipt=ref(RAW/(key+'.receipt.json'),'Acquisition identity'),git_blob_sha1=blob,
   inspected_anchors=[dict(lines=span,finding=claim) for span,claim in SPANS[path]],supported_claims=[claim for _,claim in SPANS[path]],executed=False))
 assert len(records)==10
 one=(RAW/'exec23_medflex_1.txt').read_text();impute=(RAW/'exec23_medflex_2.txt').read_text();weight=(RAW/'exec23_medflex_3.txt').read_text();utils=(RAW/'exec23_medflex_5.txt').read_text()
 assert 'boot::boot(data = extrData(fit)' in one and 'bootExpFit <- eval(as.call(call1))' in one and 'bootxFit <- eval(as.call(call3))' in one
 assert 'aggregate(estEqList[[1]], by = list(as.numeric(expData$id)), FUN = mean)' in one
 assert '"expData", "impData"' in impute and '"expData", "weightData"' in weight
 assert 'suppressWarnings(do.call("glm", args))' in utils and 'envir = globalenv()' in utils
 static=dict(native_execution=False,full_working_model_refit_present=True,original_subject_score_aggregation=True,
  documented_classes_reversed=True,implementation_classes=dict(neImpute='impData',neWeight='weightData'),
  final_glm_warnings_suppressed=True,original_data_call_uses_global_environment=True,
  limits=['Static contracts, not observed runtime failures.','Bootstrap index mapping needs ordering, equal expansion count and missingness conformance.'])
 write(BASE/'static-contract-check.json',static)
 write(BASE/'exact-results.json',exact.calculate())
 identity=dict(repository='cran/medflex',version='0.6-11',commit=commit['sha'],tree=tree['sha'],date=commit['commit']['committer']['date'],source_blobs=10,
  evidence=[ref(RAW/'v12_sw2_cran_cutoff_medflex.json','Cutoff-selected commit'),ref(RAW/'exec23_medflex_canonical_tree.json','Complete canonical tree')],
  maintenance='Named maintainer and dated CRAN publication; no support promise or complete release-history claim.')
 write(BASE/'identity.json',identity)
 license_path=ROOT/'docs/program/execution/2026-10-23/sensitivity-reuse-v1/GPL-2.txt'
 source=dict(integrated_citation_key='exec23_medflex_sources',kind='software_primary_sources',title='medflex0.6-11 natural-effect expansion, full refitting and joint-score contracts',
  author='Johan Steen and medflex contributors',year=2026,source_identity='https://github.com/cran/medflex/tree/'+commit['sha'],version_date='0.6-11; '+identity['date'],
  local_copy=records[0]['local_copy'],identity=identity,records=records,inspected_anchors=[dict(path=r['upstream_path'],anchors=r['inspected_anchors']) for r in records],
  supported_claims=[claim for spans in SPANS.values() for _,claim in spans],
  license_declaration=ref(RAW/'v12_sw2_description_medflex.txt','GPL-2 package metadata'),license_text=ref(license_path,'Separate local GPL-2 text; not retrieved from medflex artifact'),
  license_custody=ref(license_path.with_name('license-text-custody.json'),'Local operating-system text custody'),limitations=LIMITS)
 project=dict(integrated_citation_key='exec23_medflex_reference',kind='project_derivation_and_exact_reference',title='Exact natural-effect decomposition and expansion-covariance examples',
  author='Causal banking proposal project',year=2026,source_identity='tools/medflex_reference_20261023.py',version_date='23 October2026; independently authored',
  local_copy=ref(Path(exact.__file__),'calculate()'),inspected_anchors=['calculate()'],supported_claims=['Stipulated nested means give direct/indirect14/5+18/5 or2+22/5, total32/5.',
  'Duplicated rows halve an illustrative mean-score variance from1/2 to1/4; joint nuisance propagation gives7 versus1.',
  'Stipulated total-policy net14 differs from direct-component calculation-22; no measured ROI or implementation claim.'],limitations=LIMITS)
 write(BASE/'source-audit.json',dict(sources=[source,project],cutoff='2026-10-07',native_execution=False))
 omissions=dict(items=[dict(gap='Complete runtime, dependencies and delivery rights',next_action='Bind a selected full release, resolved R environment and original dependency/data notices before actual integration.'),
  dict(gap='Native bootstrap/order/NA and warning behavior',next_action='Run registered fresh-process fixtures with original IDs, row permutations, missingness, denominator failures and full model diagnostics in an authorized environment.'),
  dict(gap='General mediation identification and dependent sampling',next_action='Acquire and inspect original methodological papers and justify the declared cross-world law and sampling regime before theorem-level or bank claims.'),
  dict(gap='Broader learner and family support',next_action='Qualify each selected learner/family, bootstrap dispatch and robust-branch restriction separately.')],limitations=LIMITS)
 write(BASE/'omissions-register.json',omissions)
 write(BASE/'plan-review.json',dict(status='pass_for_scoped_reference',evidence=[ref(BASE/n,'Reviewed plan or check') for n in ['plan.md','static-contract-check.json','exact-results.json','preparation-corrections.md']],
  findings=['Ten source/documentation blobs authenticate; canonical tree queried explicitly instead of assuming the prior tree-response SHA was a tree.',
   'Full refitting, expansion identity and nuisance covariance stay in the contract.','Documentation discrepancies, warning suppression and environment dependence are bounded static observations.',
   'Reference-only decision distinguishes integration, porting and arbitrary identification.'],native_execution=False))
 evidence=[ref(BASE/n,'Reviewed contract evidence') for n in ['source-audit.json','identity.json','static-contract-check.json','exact-results.json','omissions-register.json','plan-review.json','development.tex']]
 evidence += [ref(Path(__file__),'Audit and decision construction'),ref(Path(exact.__file__),'Independent exact examples')]
 review=dict(status='pass_for_reference_disposition',reviewer=REVIEWER,evidence=evidence,findings=['Ten immutable blobs authenticated.',
  'Natural-effect target, full bootstrap, covariance and repeated-row contracts are explicit.','No upstream code executed and no new scholarly theorem is attributed to unread originals.'],limitations=LIMITS)
 verify_bindings(review);write(BASE/'review.json',review)
 print(json.dumps(dict(source_blobs=10,source_records=2,decision='reference',native_execution=False)))

def receipt():
 op='SW.DECISION.seed_056';state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==op
 verify_bindings(read(BASE/'review.json'))
 evidence=[ref(BASE/n,'Reviewed source decision') for n in ['source-audit.json','identity.json','review.json','plan-review.json','static-contract-check.json','exact-results.json','omissions-register.json','development.tex']]
 evidence += [ref(Path(__file__),'Receipt construction')]
 output=ROOT/f'docs/program/comprehensive-v14/work/{op}/decision.json'
 decision=dict(operation_id=op,status='pass',decision='reference',decision_scope='Source-qualified proposal reference; no native adapter approval',identity=read(BASE/'identity.json'),
  reason='Retain explicit natural-effect expansion and full uncertainty propagation; qualify a narrow isolated R profile before runtime integration.',
  target_and_uncertainty='Declared nested mean and contrast on a specified link/response scale; full working-model refitting or restricted joint-score sandwich, original-subject unit.',
  license=dict(declaration='GPL-2',evidence=ref(RAW/'v12_sw2_description_medflex.txt','License/dependency declarations'),text=ref(ROOT/'docs/program/execution/2026-10-23/sensitivity-reuse-v1/GPL-2.txt','Separately identified local text'),transitive_clearance=False),
  dependencies=dict(declared=['R>=3.1.2','multcomp>=1.3-6','boot>=1.3-8','car>=2.0-21','Matrix>=1.1-4','graphics>=3.1.2','sandwich>=2.3-2','stats>=3.1.2','utils>=3.1.2'],suggested=['arm','gam','glmnet','mice','mitools','rpart','SuperLearner','VGAM'],environment_locked=False),
  conversion_contract=['Preserve formula variable order, factors, mediator count, original IDs, row clock, exposure copies, target and scale.',
   'Retain expansion attributes, full refit calls and environment-bound data; verify row permutation, NA and constant replication assumptions.',
   'Retain working models, nuisance covariance, bootstrap seed/backend and interval type; refuse unsupported robust families and dependent sampling.',
   'Inspect finite weights, denominators, convergence and returned objects despite suppressed final GLM warnings; do not silently clip or reinterpret.'],
  alternatives=[dict(route='Full package adoption',decision='defer',reason='Broad dispatch and unresolved complete runtime/rights exceed selected contract.'),
   dict(route='Isolated R worker',decision='conditional future prototype',reason='Preserves upstream semantics if a complete frozen environment and narrow conformance regime are established.'),
   dict(route='Port to Python/Java/C++',decision='reject for current scope',reason='No measured advantage justifies reproducing formulas, expansion, bootstrap, family dispatch and maintenance.'),
   dict(route='Independent exact reference',decision='retain',reason='Check targets and covariance without claiming a complete estimator.'),
   dict(route='General identification or longitudinal replacement',decision='reject',reason='Natural-effect code does not supply the missing scientific or sampling assumptions.')],
  costs_to_measure=['Environment and rights custody','Data/call conversion and warning capture','Full bootstrap compute and fixture replay','Scientific mediation review','Version maintenance'],
  owner_obligations=dict(scientific='Nested target, cross-world interpretation, model adequacy and sampling law',maintainer='Pinned release, conversion and native conformance',operator='Actual deployment rights, custody and resource budget'),
  revisit_trigger='Complete release/environment/rights plus registered native tests; changed target, source, sampling law or delivery requires new review.',
  evidence=evidence,reviewer=REVIEWER,limitations=LIMITS,integration_allowed=False,runtime_qualification=False,capabilities=[])
 write(output,decision)
 graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,op);r=run.ledger.receipt_template(node)
 findings=['Concrete cutoff identity, license declaration/text, dependencies and maintenance limits recorded.','Target/uncertainty, conversion, failures, alternatives, costs, owners and revisit trigger are explicit.','Reference-only decision grants no integration capability and separates exact examples from native execution.']
 r.update(outcome='pass',execution='performed',scope=decision['decision_scope'],reviewer=REVIEWER,outputs=[ref(output,'Contracted reference decision')],criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=decision['revisit_trigger'])
 run.validate_receipt(ROOT,merged,node,r,len(state['execution_program']['turns']));verify_bindings(r);write(BASE/'operation-receipt.json',r)
 print(json.dumps(dict(operation=op,decision='reference',integration_allowed=False)))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['audit','receipt']);globals()[p.parse_args().command]()

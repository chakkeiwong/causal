#!/usr/bin/env python3
"""Current evidence gate: recheck saved outcomes, do not replace stale hashes."""
import ast
import json
import zipfile
from closure_common import ROOT,save,digest
from closure_linkage_study import projection_summary
from causalbank.linkage_sets import decode_set


def normalized_kernel(source):
    module=ast.parse(source);function=next(x for x in module.body if isinstance(x,ast.FunctionDef) and x.name=='fit_linked')
    class Normalize(ast.NodeTransformer):
        def visit_Assign(self,node):
            if isinstance(node.value,ast.Call) and isinstance(node.value.func,ast.Name) and node.value.func.id=='funding_inference':return None
            if len(node.targets)==1 and isinstance(node.targets[0],ast.Name) and node.targets[0].id=='result' and isinstance(node.value,ast.Dict):return ast.Return(value=node.value)
            return self.generic_visit(node)
        def visit_Return(self,node):
            if isinstance(node.value,ast.Name) and node.value.id=='result':return None
            return self.generic_visit(node)
    # In both versions discard the projection return after comparing its full
    # preceding computation. Preserve all original return dictionaries.
    return ast.dump(Normalize().visit(function),include_attributes=False)


def main():
    issues=[];inputs=['tools/closure_verify.py','tools/closure_common.py','tools/closure_linkage_study.py']
    checks=['docs/reviews/closure-contract-checks.json','docs/reviews/closure-linkage-checks.json',
            'docs/reviews/closure-restart-checks.json','docs/reviews/closure-journeys.json',
            'docs/reviews/linkage-scientific-checks.json','docs/reconstruction/checks.json']
    studies=['docs/studies/closure-linkage-results.json','docs/studies/closure-nonlinear-results.json',
             'docs/studies/closure-nonlinear-followup-results.json','docs/studies/closure-discovery-results.json',
             'docs/studies/closure-learning-results.json','docs/studies/closure-workload-results.json']
    receipts=checks+studies+['docs/literature/closure-runtime-audit.json','docs/literature/closure-source-review.json']
    for name in receipts:
        result=json.loads((ROOT/name).read_text());inputs.append(name)
        if name in checks and result.get('status')!='pass':issues.append('Failed executed check: '+name)
        for path,expected in result.get('input_sha256',{}).items():
            if digest(path)!=expected:issues.append('Stale executed input: '+name+' / '+path)
            inputs.append(path)
    linkage=json.loads((ROOT/studies[0]).read_text());truth=json.loads((ROOT/'docs/studies/linkage-projection-results.json').read_text())['financial_truth']
    for family,target in [('fresh',1.2),('retrospective',truth)]:
        for case in linkage[family]:
            if projection_summary(case['runs'],target)!=case['summary']:issues.append('Projection summary mismatch: '+family)
    for case in linkage['persistent']:
        for method,summary in case['summary'].items():
            count=sum(r['methods'][method]['interval'][0]<=case['truth']<=r['methods'][method]['interval'][1] for r in case['runs'])
            if count!=summary['coverage']['count'] or len(case['runs'])!=summary['coverage']['requests']:issues.append('Persistent count mismatch')
    nonlinear=json.loads((ROOT/studies[1]).read_text())
    if not all(nonlinear['numerical']['checks'].values()):issues.append('Nonlinear numerical reference failed')
    for case in nonlinear['results']:
        available=[r for r in case['runs'] if r['status']=='computed'];count=sum(r['interval'][0]<=case['truth']<=r['interval'][1] for r in available)
        if len(available)!=case['summary']['available'] or count!=case['summary']['coverage_all']['count']:issues.append('Nonlinear count mismatch')
    follow=json.loads((ROOT/studies[2]).read_text())
    for case in follow['results']:
        for method,summary in case['summary'].items():
            available=[r['methods'][method] for r in case['runs'] if r['methods'][method]['status']=='computed']
            count=sum(r['interval'][0]<=follow['truth']<=r['interval'][1] for r in available)
            if len(available)!=summary['available'] or count!=summary['coverage_all']['count']:issues.append('Follow-up count mismatch')
    discovery=json.loads((ROOT/studies[3]).read_text())
    if not all(discovery['checks'].values()):issues.append('Graph witness checks failed')
    for case in discovery['results']:
        for method,summary in case['summary'].items():
            count=sum(any(a<=case['truth']<=b for a,b in decode_set(r['methods'][method]['set'])) for r in case['runs'])
            if count!=summary['coverage']['count']:issues.append('Graph coverage count mismatch')
    learning=json.loads((ROOT/studies[4]).read_text())
    if not all(learning['rejection_checks'].values()):issues.append('Learner rejection checks failed')
    for case in learning['results']:
        for method,summary in case['summary'].items():
            count=sum(r['methods'][method]['interval'][0]<=case['truth']<=r['methods'][method]['interval'][1] for r in case['runs'])
            if count!=summary['coverage']['count']:issues.append('Learning count mismatch')
    workload=json.loads((ROOT/studies[5]).read_text());rows=workload['runs']
    if len(rows)!=32:issues.append('Incomplete workload suite')
    for kind,size,repeat in {(r['kind'],r['size'],r['repeat']) for r in rows}:
        pair=[r for r in rows if (r['kind'],r['size'],r['repeat'])==(kind,size,repeat)]
        if len(pair)!=2 or pair[0]['output_sha256']!=pair[1]['output_sha256']:issues.append('Matched workload outputs differ')
    preservation=json.loads((ROOT/'docs/program/history/v6.1-preservation-receipt.json').read_text())
    if digest(preservation['archive'])!=preservation['sha256']:issues.append('V6.1 archive changed')
    with zipfile.ZipFile(ROOT/preservation['archive']) as archive:
        prior=json.loads(archive.read('docs/program/reconstruction-delivery-manifest.json'));bound={r['path']:r for r in prior['artifacts']}
        old=archive.read('src/causalbank/dynamic_product.py').decode()
        numeric_equivalence=normalized_kernel(old)==normalized_kernel((ROOT/'src/causalbank/dynamic_product.py').read_text())
    if not numeric_equivalence:issues.append('Legacy numeric AST changed beyond metadata-only repair')
    # Retain unchanged scientific evidence at its original byte identity.
    # Current checks cover changed public code; old study hashes stay historical.
    claims=json.loads((ROOT/'docs/literature/reconstruction-claims.json').read_text());artifact_status=[]
    for claim in claims:
        for path in claim.get('artifacts',[]):
            actual=digest(path);inputs.append(path)
            if not claim['id'].startswith('C-G') and path in bound:
                unchanged=actual==bound[path]['sha256'];artifact_status.append(dict(claim=claim['id'],path=path,unchanged_v61=unchanged))
                if not unchanged and path not in ('src/causalbank/dynamic_product.py','docs/reviews/linkage-scientific-checks.json'):
                    issues.append('Changed inherited scientific artifact needs replay: '+path)
    inputs+=['docs/literature/reconstruction-claims.json','docs/literature/sources.json','docs/program/history/v6.1-preservation-receipt.json',preservation['archive'],'src/causalbank/dynamic_product.py']
    result=dict(status='pass' if not issues else 'fail',issues=issues,
                verification=dict(retained_summary_replays='all six study families',matched_complete_workloads=len(rows),legacy_numeric_ast_equivalence=numeric_equivalence,inherited_artifacts=artifact_status),
                scope='Author evidence replay and current executed input identities. Negative scientific outcomes remain negative; passing identity checks do not qualify arbitrary models or bank use.')
    save('docs/reviews/closure-verification.json',result,inputs)
    print(json.dumps({'status':result['status'],'issues':issues,'legacy_numeric_ast_equivalence':numeric_equivalence,'matched_workloads':len(rows)},indent=2));raise SystemExit(bool(issues))


if __name__=='__main__':main()

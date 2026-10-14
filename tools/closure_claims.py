#!/usr/bin/env python3
"""Register the new source and six reconstructed evidence chains."""
import json
from closure_common import ROOT,digest

def main():
    path=ROOT/'docs/literature/sources.json';sources=json.loads(path.read_text());audit=json.loads((ROOT/'docs/literature/closure-runtime-audit.json').read_text())
    local='docs/literature/runtime/closure/jax-derivative-contract.txt'
    record=dict(id='jaxruntime2026',title='JAX 0.11.1 installed derivative API and inspected source',authors='{{JAX contributors}}',year=2026,kind='documentation',url='https://github.com/jax-ml/jax',local_path=local,sha256=digest(local),
                version_status='Installed JAX and jaxlib 0.11.1 observed 10 October 2026; release status at the 7 October literature cutoff is not inferred',accessed='2026-10-10',
                inspected=['Local API source: jit line 171, grad line 426, jacrev line 791, hessian line 861; preserved derivative docstrings inspected'],
                claims=['The operations stage/differentiate a pure discretized array objective. The nonlinear study checks likelihood, score and value separately.'],
                limits='Runtime operation evidence only; no literature-currentness, identification, quadrature certification or arbitrary resampling-gradient qualification.',
                artifacts=[dict(path=p,sha256=h) for p,h in audit['input_sha256'].items() if p.startswith('docs/literature/runtime/')],qualification_record='docs/literature/closure-runtime-audit.json')
    if not any(s['id']==record['id'] for s in sources):sources.append(record)
    path.write_text(json.dumps(sources,indent=2,ensure_ascii=False)+'\n')
    bib=ROOT/'docs/causal_banking_refs.bib'
    if '@misc{jaxruntime2026,' not in bib.read_text():
        with bib.open('a') as output:output.write('\n@misc{jaxruntime2026,\n  author = {{JAX contributors}},\n  title = {JAX 0.11.1 installed derivative API and inspected source},\n  year = {2026},\n  note = {Installed operation observed 10 October 2026; local source, metadata, inspected anchors and hashes in the runtime audit. Cutoff release status not inferred}\n}\n')
    claims=json.loads((ROOT/'docs/literature/reconstruction-claims.json').read_text())
    added=[
      ('C-G1','c7:journeys','Versioned explicit inference and both public consumers retain qualifications with exact legacy numeric equivalence.',[],['docs/reviews/closure-contract-checks.json','docs/reviews/closure-journeys.json','src/causalbank/dynamic_product.py','src/causalbank/closure_journeys.py']),
      ('C-G2','c7:joint-projection','Global analytic ellipsoid outer projection compares useful precision and retains singular failures; undercoverage diagnostics distinguish primitive response and audit contributions.',['newey1986','staiger1994'],['docs/studies/closure-linkage-results.json','docs/reviews/closure-linkage-checks.json','src/causalbank/ellipsoid_linkage.py']),
      ('C-G3','c7:nonlinear','Accurate labelled audits identify a selected nonlinear family; observed/audit likelihood, score and fixed-policy value are fitted with retained boundary failures and a registered stable-domain/audit follow-up.',['sarkka2013','pearl2009','jaxruntime2026'],['docs/studies/closure-nonlinear-results.json','docs/studies/closure-nonlinear-followup-results.json','src/causalbank/nonlinear_audited.py','src/causalbank/nonlinear_stability.py']),
      ('C-G4','c7:latent-confidence','Finite Gaussian episode covariance inclusion projects conservatively over a latent structural class, preserves observational witnesses, and distinguishes validated encouragement from false exclusions.',['pearl2009'],['docs/studies/closure-discovery-results.json','src/causalbank/latent_temporal_sets.py']),
      ('C-G5','c7:persistent-audits','Known-inclusion persistent-pair audits identify a focal outcome moment with pair-level uncertainty and separately identified label-error correction.',['slawski2025','guha2022'],['docs/studies/closure-linkage-results.json','docs/reviews/closure-linkage-checks.json','src/causalbank/persistent_audits.py']),
      ('C-G6','c7:restartable','Bounded dependent sparse inference, clock-checked streamed materialization and atomic score restarts preserve the experiment; complete matched local workloads do not establish multi-host speedups or analyst savings.',['dml2018'],['docs/studies/closure-learning-results.json','docs/reviews/closure-restart-checks.json','docs/studies/closure-workload-results.json','src/causalbank/blocked_learning.py','src/causalbank/checkpoint_scores.py'])]
    claims=[c for c in claims if not c['id'].startswith('C-G')]
    claims += [dict(id=i,manuscript_anchor=a,claim=c,sources=s,artifacts=e,evidence_class='project_derivation_with_primary_source_limits_and_retained_synthetic_local_evidence') for i,a,c,s,e in added]
    (ROOT/'docs/literature/reconstruction-claims.json').write_text(json.dumps(claims,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'registered_sources':len(sources),'claim_groups':len(claims)}))


if __name__=='__main__':main()

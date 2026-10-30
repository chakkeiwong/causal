"""Single-use, ledgered survival delegate integration; no upstream execution."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import re
from release_candidate_20261029 import MATH
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/release/2026-10-29'
OUT=BASE/'source-survival-022'
SOURCE=BASE/'source/docs/writing-repair/2026-10-29'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ledger=json.loads((BASE/'edits.json').read_text())
    assert len(ledger)==91,'Single-use integration; do not rerun.'
    assert not (OUT/'source-audit.json').exists()
    changes={}
    def edit(p,before,after,reason,destination):
        old,current=changes.get(p,(p.read_text(),p.read_text()))
        assert current.count(before)==1,before[:100]
        changes[p]=(old,current.replace(before,after,1))
        ledger.append(dict(file=str(p.relative_to(ROOT)),before=before,after=after,reason=reason,substantive_destination=destination))
    p=SOURCE/'src/4576dc3f2d02826a.tex'
    edit(p,'Delegated SurvivalBase and\nSurvivalDistributions behaviour remains a separate inspection obligation.',
         'The selected SurvivalBase and SurvivalDistributions delegates are examined\nbelow. Their observation and distribution contracts qualify this candidate\nfurther; they do not resolve the preceding boundary discrepancy.',
         'Replace the selected-dependency omission with its substantive comparison, retaining the unresolved scalar/vector discrepancy.',
         'The original six-family comparison, all mathematics and adverse findings remain; selected dependency evidence follows before the Rust discussion.')
    anchor=r'\subsection{Rust causal labels require method-level inspection}'
    extra=(OUT/'addition.tex').read_text()+'\n'
    edit(p,anchor,extra+anchor,
         'Add primary-source dependency contracts, exact entry and identifiability derivations, monetary consequences and serious alternatives.',
         'New developed subsections precede the original Rust comparison; all original Julia/Rust findings and numerical examples remain in the manuscript.')
    bib=SOURCE/'references-0.bib';tail=bib.read_text()[-180:]
    entries=r'''
@misc{rel22survbase,
 author={{JuliaSurv contributors}},
 title={{SurvivalBase.jl}: selected formula and observation contracts},
 year={2026},
 note={Version 0.1.0; commit d43e1f9ee4a2c96325140d8fabb0ba02b7f4cc70, 26 June. Primary source inspection; no native execution},
 url={https://github.com/JuliaSurv/SurvivalBase.jl}
}
@misc{rel22survdist,
 author={{JuliaSurv contributors}},
 title={{SurvivalDistributions.jl}: selected distributions, domains and tails},
 year={2026},
 note={Version 0.1.1; commit 54f8bd703573940c934bc1ce1c21da5e657482d7, 1 July. Primary source inspection; no native execution},
 url={https://github.com/JuliaSurv/SurvivalDistributions.jl}
}
@misc{rel22survcaller,
 author={{JuliaSurv contributors}},
 title={{SurvivalModels.jl}: general-hazard likelihood, inference and prediction caller},
 year={2026},
 note={Version 0.1.6; commit 3a9f953120296b0ca9602a96d83cd8e25b63fe2d, 25 August. Selected caller inspection; not a resolved installation},
 url={https://github.com/JuliaSurv/SurvivalModels.jl}
}
@misc{rel22survwitness,
 author={{Causal Banking Research Project}},
 title={Exact survival contracts: entry, parameter redundancy, units, tails and monetary outputs},
 year={2026},
 note={Project-authored derivations and independent reconstruction, 29 October; no bank data or downloaded-package execution}
}
'''
    edit(bib,tail,tail+entries,'Add traceable identities for selected delegates, caller and project laws.','All inherited references remain; four new entries support the added comparison.')
    authenticated=json.loads((OUT/'authenticated-files.json').read_text());pins=json.loads((OUT/'pins.json').read_text())
    findings={
      'base':[('src/Surv.jl',[(1,39,'Right-censored time/status term and two-column response.')]),('src/Strata.jl',[(1,37,'Estimator-specific stratification marker.')]),('README.md',[(15,20,'Explicit right-censoring scope and planned extensions.')])],
      'dist':[('src/utilities.jl',[(1,31,'Hazard/cumulative hazard and origin-based censored likelihood.')]),('src/distros/LogLogistic.jl',[(16,42,'Location/scale representation.')]),('src/distros/PiecewiseConstantHazardDistribution.jl',[(1,60,'Last-hazard continuation, finite quantile endpoint, inconsistent D/L names.')]),('src/distros/AbstractHazardDistribution.jl',[(1,14,'Unbound numerical helper calls in selected module.')]),('src/SurvivalDistributions.jl',[(1,29,'Complete imports and includes.')])],
      'parent':[('src/Parametric/GeneralHazard.jl',[(1,31,'Time/hazard multipliers, likelihood and exponentiation of every baseline parameter.'),(207,255,'Minimizer and objective storage, active coefficient blocks.'),(298,330,'Coefficient representation and observed Hessian inversion.'),(690,718,'Time/status formula response.'),(743,846,'Cumulative-hazard output and own-time/common-time predictions.'),(882,888,'Inverse-CDF simulation with supplied RNG.')]),('src/SurvivalModels.jl',[(1,17,'Public module and exports.')])]
    }
    claims={
      'base':['Right-censored exit/status formula does not carry delayed entry or interval endpoints.','Version and direct MIT notice.'],
      'dist':['Log-logistic location and scale representation.','Piecewise tail/quantile mismatch and unbound D/L names.','Generic helpers not bound by selected module.','Version and direct MIT notice; no assertion that all families fail.'],
      'parent':['Time/cumulative-hazard composition and right-censored origin likelihood.','Every baseline fit parameter exponentiated; active-block selection does not diagnose all baseline/design redundancy.','Inverse observed Hessian and minimizer/objective storage without a convergence field.','Expected prediction is cumulative hazard; default own-time differs from common future horizon.']}
    sources=[]
    for group,key in [('base','rel22survbase'),('dist','rel22survdist'),('parent','rel22survcaller')]:
        rows=[x for x in authenticated if x['group']==group];anchors=[];bindings=[]
        for row in rows:
            q=ROOT/row['local'];bindings.append(dict(path=row['local'],sha256=sha(q)))
            receipt=q.with_suffix('.receipt.json')
            if receipt.exists():bindings.append(dict(path=str(receipt.relative_to(ROOT)),sha256=sha(receipt)))
            for upstream,segments in findings[group]:
                if upstream!=row['upstream_path']:continue
                lines=q.read_text().splitlines()
                for first,last,finding in segments:
                    last=min(last,len(lines));anchors.append(dict(path=row['local'],sha256=sha(q),lines=[first,last],text='\n'.join(lines[first-1:last]),finding=finding))
        if group=='parent':
            repo='JuliaSurv/SurvivalModels.jl';commit='3a9f953120296b0ca9602a96d83cd8e25b63fe2d';date='2026-08-25';version='0.1.6'
            more=['docs/literature/raw/exec24_survivalother_juliamodels_'+part for part in ['src_00.txt','src_01.txt','cutoff.json','tree.json']]
        else:
            pin=pins[group];repo=pin['repo'];commit=pin['sha'];date=pin['commit_date'];version='0.1.0' if group=='base' else '0.1.1'
            more=['docs/literature/raw/rel22_'+group+'_'+part+'.json' for part in ['repo','cutoff','tree']]
        for name in more:bindings.append(dict(path=name,sha256=sha(ROOT/name)))
        sources.append(dict(citation_key=key,kind='implementation',source_identity='https://github.com/'+repo+'/tree/'+commit,
                            version_date=f'{version}; {commit}; {date}; retrieved 2026-10-29; pre-2026-10-07 cutoff.',
                            local_bindings=bindings,inspected_anchors=anchors,supported_claims=claims[group],
                            limitations=['Static selected-source inspection; no vendor execution, native qualification, bank validation or transitive rights clearance.','Separate selected snapshots do not prove a resolved installed environment.','Package-mentioned papers remain unadmitted discovery leads.']))
    witness=OUT/'exact-witnesses.json';generator=ROOT/'tools/release_survival_witnesses_20261029.py'
    sources.append(dict(citation_key='rel22survwitness',kind='project_derivation',source_identity=str(generator.relative_to(ROOT)),version_date='2026-10-29 exact project laws',
                        local_bindings=[dict(path=str(q.relative_to(ROOT)),sha256=sha(q)) for q in [witness,generator]],
                        inspected_anchors=['main(): delayed-entry exposure; equal Weibull hazards and cumulative hazards; exponential AH cancellation; location unit change; tail inversion and receipt integration; hazard/probability conversion.'],
                        supported_claims=['Conditional-entry rates1/3 vs1/11 and losses28.35 vs8.69.','Shared-covariate Weibull GH identifies(k-1)alpha+beta, with exact equal-law pairs.','Baseline-only positive-location fitting changes admitted log-logistic laws with time units.','Tail quantile5log10 vs finite-loop1; full/restricted receipt totals500 vs90.63.','Cumulative hazard2 means probability1-exp(-2) and loss86.47, not200.'],
                        limitations=['Stipulated laws and static arithmetic; no empirical or native execution results.','Entry/censoring and cashflow assumptions do not identify a causal payment-holiday effect.']))
    audit=dict(cutoff='2026-10-07',sources=sources,scope='Named dependency/source closure; no exhaustive survey or new scholarly admission.')
    ap=OUT/'source-audit.json';at=json.dumps(audit,indent=2)+'\n'
    rp=BASE/'mathematical-addition-reviews.json';reviews=json.loads(rp.read_text());e=ledger[92]
    occ=lambda s:Counter(re.sub(r'\s+',' ',m[0]) for m in MATH.finditer(s));assert not occ(e['before'])-occ(e['after'])
    reviews['reviews'].append(dict(scope='Additive entry likelihood, model identification and valuation derivations.',
      edits=[dict(edit=93,file=e['file'],before_sha256=hashlib.sha256(e['before'].encode()).hexdigest(),after_sha256=hashlib.sha256(e['after'].encode()).hexdigest())],
      allowed_added=dict(occ(e['after'])-occ(e['before'])),allowed_removed={},status='reviewed_additions_only',
      derivation='Condition event/censor likelihood on survival to entry and differentiate exponential log likelihood. Integrate time-rescaled hazard, substitute Weibull cumulative hazard and isolate shared coefficient combination. Transform log-time location under days=30*months. Invert constant-hazard tail, integrate survival and convert H to1-exp(-H).',
      reviewed_assumptions=['Independent entry/censoring conditional on covariates; positive exposure and exponential illustrative law.','Shared scalar covariate and Weibull baseline; parametric redundancy distinct from causal identification.','Baseline-only log-logistic counterexample without covariates.','Positive terminal hazard continues forever; no discounting, competing event or costs in receipt illustration.','Project arithmetic and source tracing only; no native execution or bank outcome.'],
      witness=dict(path=str(witness.relative_to(ROOT)),sha256=sha(witness)),source_audit=dict(path=str(ap.relative_to(ROOT)),sha256=hashlib.sha256(at.encode()).hexdigest()),fresh_visual_acceptance=False,independent_acceptance=False))
    backup=OUT/'before';backup.mkdir(exist_ok=False)
    for q,(old,new) in changes.items():assert q.read_text()==old;(backup/q.name).write_text(old)
    for name in ['edits.json','mathematical-addition-reviews.json']:(backup/name).write_bytes((BASE/name).read_bytes())
    ap.write_text(at)
    for q,(old,new) in changes.items():q.write_text(new)
    (BASE/'edits.json').write_text(json.dumps(ledger,indent=2)+'\n');rp.write_text(json.dumps(reviews,indent=2)+'\n')
    print(json.dumps(dict(edits=len(ledger),source_audit_sha256=sha(ap),witness_sha256=sha(witness))))

if __name__=='__main__':main()

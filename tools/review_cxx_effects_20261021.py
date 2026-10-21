"""Bounded source inspection of native heterogeneous-effect lineages."""
import hashlib
import json
from pathlib import Path
import shutil
import cxx_effects_reference_20261021 as exact
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write
run=extension.base
core=run.core
ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-20/cxx-effects-v1'
OP='SW.CELL.effects_heterogeneity.Cxx'
REVIEWER=dict(name='Codex author/coordinator',kind='author')
read=lambda p:json.loads(p.read_text())
LIMITS=[
 'Bounded four-lineage source comparison; 18 discovery hits are not an exhaustive census.',
 'Pinned commit identities precede 7October2026; post-cutoff discovery is not evidence of complete historical availability.',
 'Source inspection and authored examples do not execute or qualify upstream libraries.',
 'License declarations are recorded; complete dependency rights and deployment obligations remain unreviewed.',
 'Posterior draws, little-bag variance and repeat-sampling calibration remain different statements.',
 'No runtime integration, vendor/LLM execution, measured bank value or independent acceptance is granted.',
 'Mandatory repairs, Q1/Q5, rendered visual review and final proposal acceptance remain open.']

def excerpt(path,ranges):
    lines=path.read_text().splitlines(keepends=True)
    result=[]
    for lo,hi in ranges:
        assert 1<=lo<=hi<=len(lines),(str(path),lo,hi,len(lines))
        result.append(dict(anchor=f'lines {lo}-{hi}',inspected_text=''.join(lines[lo-1:hi])))
    return result

def main():
    assert not (BASE/'source-audit.json').exists()
    state=core.read(ROOT,core.STATE)
    assert state['execution_runtime']['active']['operation']==OP
    write(BASE/'exact-results.json',exact.calculate())
    authenticated=read(BASE/'alternative-authenticated-sources.json')['sources']
    grf=read(BASE/'grf-authenticated-sources.json')
    authenticated += [dict(s,family='grf',commit=grf['commit']) for s in grf['sources']]
    for s in authenticated:
        b=(ROOT/s['local_path']).read_bytes()
        assert hashlib.sha256(b).hexdigest()==s['sha256']
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==s['git_blob_sha1']
    selections={
      'grf':{0:[(1,18)],1:[(1,30)],2:[(44,65),(85,150)],7:[(1,65),(154,235),(276,325)],10:[(50,118)],11:[(40,125)]},
      'bcf':{0:[(1,31)],2:[(84,138),(216,270),(282,330),(664,710),(760,794)],3:[(369,389),(880,911)]},
      'xbcf':{0:[(1,13)],1:[(1,30)],2:[(115,170),(189,227)],4:[(10,81),(85,120)],5:[(392,480),(516,577)],7:[(33,126)]},
      'flexbcf':{0:[(1,13)],1:[(1,17)],2:[(1,66)],3:[(35,54),(230,310)],4:[(89,133)],5:[(88,141)]}}
    versions={'grf':'2.6.1; commit30April2026; GPL>=3',
      'bcf':'2.0.2; commit26September2023; GPL3 declaration',
      'xbcf':'0.1.2 declared; commit25June2024; Apache2.0 declared',
      'flexbcf':'1.0.3; commit1December2025; GPL>=3 declaration'}
    claims={
      'grf':['Binary unconfounded CATE differs from the continuous-treatment covariance/variance slope.',
        'Wrapper fits or accepts aligned nuisance predictions and residualizes; honest trees and cluster weighting affect learning.',
        'Native moment ratio and little-bag group variance require denominator/group diagnostics; its Bayes variance correction is not a BCF posterior.',
        'Earlier R-first native boundary decision is preserved; source inspection grants no new route.'],
      'bcf':['Separate prognostic and treatment ensembles use a supplied propensity feature; include_pi controls placement.',
        'w specifies likelihood precision sigma^2/w, distinct from a target-population average.',
        'Tree-file persistence, row order, outcome standardization and draw-wise b1-b0 restoration are observable wrapper semantics.',
        'Prediction wrapper requires both treatment labels and serialized samples; source hardcodes one chain executor core.'],
      'xbcf':['Separate native prognostic/treatment updates and optional scale updates produce joint draws; categorical ordering and supplied propensity provenance need preservation.',
        'Selected R combined predictor references z without a formal argument and obj before local assignment; static hazards require isolated reconciliation, not claimed observed runtime failures.',
        'Selected Python zero-variance branch constructs ValueError without raising it, and adjusted fitted draws are assigned inside standardize_target; paths require prototype tests.',
        'Prediction restores each draw by outcome SD and treatment-scale contrast, then averages post-burnin draws.'],
      'flexbcf':['README explicitly distinguishes its prior and treatment-recoding behavior from bcf; it is not an identical implementation.',
        'Wrapper transposes design matrices and standardizes outcome; native trainer uses separate prognostic/all-unit and treatment design sizes.',
        'Native SATT helper averages supplied rows within each common draw before quantiles; its name does not select treated rows.',
        'Weighted helper divides by sum of supplied weights; callers, denominator and row-selection guards require further trace.']}
    sources=[]
    for family,indices in selections.items():
        records=[]
        for index,ranges in indices.items():
            p=ROOT/f'docs/literature/raw/exec20_cxx_effects_{family}_{index:02}.txt'
            a=next(s for s in authenticated if s['local_path']==str(p.relative_to(ROOT)))
            receipt=p.with_suffix('.receipt.json');r=read(receipt)
            assert r['sha256']==core.sha(p) and r['status']=='saved'
            records.append(dict(role='inspected_primary_technical_text',source_identity=r['url'],
                local_copy=ref(p,a['path']),receipt=ref(receipt,'Original fixed HTTPS acquisition'),
                git_blob_sha1=a['git_blob_sha1'],commit=a['commit'],inspected_anchors=excerpt(p,ranges)))
        sources.append(dict(integrated_citation_key='exec21_cxx_'+family,kind='software',
            title=family+' pinned native heterogeneous-effect source review',author=family+' contributors',year=2026,
            source_identity=records[0]['source_identity'],version_date=versions[family],
            records=records,inspected_anchors=[dict(anchor=r['local_copy']['anchor'],ranges=r['inspected_anchors']) for r in records],
            supported_claims=claims[family],limitations=LIMITS))
    title='Bayesian regression tree models for causal inference regularization confounding and heterogeneous effects'
    paper=ROOT/'docs/papers'/f'{title} Hahn(2019).pdf'
    raw=ROOT/'docs/literature/raw/exec20_bcf_article_v4.pdf'
    assert raw.read_bytes().startswith(b'%PDF-') and not paper.exists()
    shutil.copyfile(raw,paper)
    text=BASE/'bcf-paper.txt'
    anchors=excerpt(text,[(175,230),(440,580),(580,735),(820,920),(950,1015),(1386,1470)])
    for anchor in anchors:
        lo=int(anchor['anchor'].split()[1].split('-')[0])
        anchor['physical_page']=''.join(text.read_text().splitlines(keepends=True)[:lo-1]).count(chr(12))+1
    sources.append(dict(integrated_citation_key='exec21_cxx_hahn',kind='paper',title=title,
        author='Hahn, P. Richard and Murray, Jared S. and Carvalho, Carlos M.',first_author='Hahn',year=2019,
        source_identity='https://arxiv.org/abs/1706.09523v4',version_date='arXiv1706.09523v4;13November2019;33pages, not asserted identical to2020 journal version',
        local_copy=ref(paper,'Genuine original preprint, unchanged bytes'),local_path=str(paper.relative_to(ROOT)),sha256=core.sha(paper),
        text_copy=ref(text,'Inert extraction'),inspected_anchors=anchors,
        supported_claims=['SUTVA,ignorability,overlap and an additive Gaussian likelihood frame the BCF response-surface decomposition.',
          'Separate priors and propensity-as-feature address regularization-induced confounding; paper does not claim double robustness.',
          'Purpose-built simulations and retrospective ACIC2016 comparisons are conditional historical evidence, not this project reproduction.',
          'Reported ACIC nominal95% intervals achieve BCF82%,ps-BART88%,BART81%,CausalRF58%; no uniform coverage theorem is supplied.'],
        limitations=LIMITS+['Linked references and related papers are not imported as inspected evidence.']))
    sources.append(dict(integrated_citation_key='exec21_cxx_reference',kind='project_derivation',
        title='Exact native-effect target, weighting, posterior aggregation and shrinkage witnesses',
        author='Causal banking proposal project',year=2026,source_identity='tools/cxx_effects_reference_20261021.py',
        version_date='21October2026',local_copy=ref(ROOT/'tools/cxx_effects_reference_20261021.py','Rational finite-law constructions'),
        inspected_anchors=[ref(BASE/'exact-results.json','All reproduced witnesses')],supported_claims=[
          'Covariance slope0 differs from finite dose contrast1.',
          'Equal-population effect2 differs from precision-weighted26/5; assumed cost3 reverses margin sign.',
          'Joint-draw portfolio is always2 although marginal supports are[-2,6].',
          'Draw-wise scale restoration produces5,40 and mean22.5; omitted contrast gives15.',
          'Positive overlap and true effect0 coexist with a penalized regression coefficient1 under declared shrinkage.'],limitations=exact.calculate()['limits']))
    write(BASE/'source-audit.json',dict(sources=sources,cutoff='2026-10-07',review_date='2026-10-21',
        authenticated_acquired_blobs=len(authenticated),inspected_blobs=sum(len(s.get('records',[])) for s in sources),limitations=LIMITS))
    hits=read(ROOT/'docs/literature/raw/exec20_cxx_effects_search.json')['items']
    candidates=[dict(name=s['name'],repository=s['repository'],commit=s['commit'],status='selected_primary_sources_inspected',
        recommendation='qualified_process_adapter_candidate; no native admission',integration_allowed=False) for s in read(BASE/'alternative-identities.json')['candidates']]
    candidates.insert(0,dict(name='grf',commit=grf['commit'],status='selected_primary_sources_inspected',
        recommendation='preserve prior R-first boundary decision SW.DECISION.seed_080',integration_allowed=False))
    leads=[dict(repository=r['full_name'],status='uninspected_discovery_lead',historical_cutoff_verified=False,
        alias_review='CRAN mirror candidate; do not count separately' if r['full_name'].startswith('cran/') else 'lineage and originality unresolved')
        for r in hits if r['full_name'] not in [c.get('repository') for c in candidates]]
    write(BASE/'candidate-register.json',dict(candidates=candidates,other_hits=leads,market_census_complete=False,
        query='causal forest language:C++',search_evidence=ref(ROOT/'docs/literature/raw/exec20_cxx_effects_search.json','18 bounded repository hits')))
    write(BASE/'omissions-register.json',dict(global_blocker=False,uninspected_candidates=leads,remaining=[
        'Complementary uplift,multitreatment,survival,dose-response and language/package searches; exact alias/cutoff reconciliation.',
        'XBCF and flexBCF dedicated method originals and paper discussion; no borrowed theorem before authentic inspection.',
        'Trace flexBCF public callers and training order; verify target cohort, empty draws, weights and category guards.',
        'Full dependency/licensing/deployment review; static wrapper hazards and serialization/restart behavior.',
        'Predeclared public-data/generated-law native comparison after environment and rights qualification.'],
        failures=[ref(BASE/'bcf-publisher-nonpdf.receipt.json','Publisher returned non-PDF; genuine arXivv4 used with version limit')]))
    write(BASE/'plan-review.json',dict(status='pass',reviewer=REVIEWER,evidence=[ref(BASE/'plan.md','Recovered plan')],
        refinements=['Keep target, prior, draw semantics and deployment distinct.',
          'Record adverse paper evidence and static hazards without runtime defect claims.',
          'Use exact public witnesses and retain incomplete census; no scope-based waiver of coverage.']))
    write(BASE/'conversion-contract.json',dict(status='proposed_not_implemented',integration_allowed=False,
        inputs=['Outcome and action clocks; binary contrast or continuous slope/dose pair; graph and ignorability assertions',
          'Separate likelihood precision, sampling/cluster weights and target-cohort weights',
          'Covariate names/order/types, nuisance provenance, folds and training identities',
          'Pinned source/environment, priors, chains, burnin, thinning, random seeds and file dependencies'],
        outputs=['Typed estimand, scale, target population and support/refusal diagnostics',
          'Native draw orientation normalized with unit/chain/draw IDs; common draws retained across units',
          'Posterior credible interval versus sampling confidence interval; separate Monte Carlo diagnostics',
          'Same semantics through library,CLI,MCP; no LLM relabeling a failed or unsupported target'],
        public_experiments=['Exact target/scale/order/weight parity; constant outcomes,empty cohorts,zero weights and unsupported actions',
          'Known-law overlap and targeted-selection strata; original coverage failures remain in denominator',
          'Dependence,unmeasured confounding and misspecified propensity stress cells',
          'Persistence/restart,cancellation,thread and memory measurements only after scoped native qualification']))
    evidence=[ref(BASE/n,'Bounded C++ coverage evidence') for n in ['source-audit.json','exact-results.json','candidate-register.json','omissions-register.json','plan-review.json','conversion-contract.json']]
    evidence += [ref(Path(__file__),'Source inspection and exact author review')]
    findings=[('inconclusive','Four authenticated lineages compared; full language/capability census and complementary source searches remain open.'),
      ('pass','Pinned primary sources, genuine BCFv4 and exact authored constructions have hashes, inspected anchors and scoped claims.'),
      ('pass','Known source hazards, historical adverse results, missing method originals, rights and runtime qualification remain explicit without absence claims.')]
    output=ROOT/f'docs/program/comprehensive-v14/work/{OP}/coverage-review.json'
    write(output,dict(operation_id=OP,status='inconclusive',reviewer=REVIEWER,evidence=evidence,limitations=LIMITS,capabilities=[],integration_allowed=False,
        criteria=[dict(index=i,verdict=v,finding=f) for i,(v,f) in enumerate(findings)]))
    write(BASE/'review.json',dict(status='inconclusive',output=ref(output,'Bounded proposal coverage'),evidence=evidence,limitations=LIMITS))
    graph,_,_=run.combined(ROOT,state);receipt=run.ledger.receipt_template(run.ledger.operation(graph,OP))
    receipt.update(outcome='inconclusive',execution='performed',scope='Bounded native heterogeneous-effects proposal comparison',
        reviewer=REVIEWER,capabilities=[],outputs=[ref(output,'Coverage disposition')],limitations=LIMITS,nonexecution_reason='',
        revisit_trigger='Complete complementary census, originals, caller contracts and rights before native prototype qualification.',
        criteria=[dict(index=i,verdict=v,finding=f,evidence=evidence) for i,(v,f) in enumerate(findings)])
    write(BASE/'operation-receipt.json',receipt);verify_bindings(read(BASE/'source-audit.json'))
    print(json.dumps(dict(outcome='inconclusive',sources=len(sources),paper=str(paper.relative_to(ROOT)),inspected_blobs=sum(len(s.get('records',[])) for s in sources))))

if __name__=='__main__':main()

from pathlib import Path
from hashlib import sha256
import json
import shutil

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/scientific-gap-closure/2026-10-29'

def ref(path,anchor):
    return dict(path=path,sha256=sha256((ROOT/path).read_bytes()).hexdigest(),anchor=anchor)

def main():
    papers=[dict(key='gap29dehejia',raw='gap29_nsw_jasa',year=1999,
      title='Causal Effects in Nonexperimental Studies: Reevaluating the Evaluation of Training Programs',
      authors='Rajeev H. Dehejia and Sadek Wahba',
      file='Causal Effects in Nonexperimental Studies Reevaluating the Evaluation of Training Programs Dehejia(1999).pdf',
      version='Author-hosted scan of published JASA 94(448), 1053-1062',
      anchors=['Physical PDF p.2 / printed 1053: identity',
               'Physical PDF p.3 / printed 1054 section 2.1: randomisation, cohort and subset-selection assumptions',
               'Physical PDF p.4 / printed 1055 Table 1 and section 2.2: 185/260 subset and composition'],
      claims=['The retained male subset has 185 treated and 260 controls.',
              'Preserving randomisation after selecting RE74 requires independence from pre-intervention covariates.',
              'The subset target differs from the full experiment.']),
      dict(key='gap29lin',raw='gap29_lin',year=2013,
      title='Agnostic Notes on Regression Adjustments to Experimental Data: Reexamining Freedmans Critique',authors='Winston Lin',
      file='Agnostic Notes on Regression Adjustments to Experimental Data Reexamining Freedmans Critique Lin(2013).pdf',
      version='arXiv:1208.2301v2, 19 April 2013; published electronic reprint',
      anchors=['PDF pp.3-4 sections 2.1-2.2: fixed-size randomisation, finite-population target and interacted estimator',
               'PDF pp.7-9 conditions 1-3, theorem 1 and corollary 1.1: fixed-dimensional asymptotic precision',
               'PDF pp.12-14 section 5 and theorem 2: sandwich covariance, asymptotic conservatism, HC2 identity and finite-sample cautions'],
      claims=['Interacted adjustment and its uncertainty require the stated design and regularity conditions.',
              'Asymptotic non-worsening precision does not order realised standard errors in one dataset.',
              'No exact finite-sample coverage guarantee is supplied for this NSW sample.']),
      dict(key='gap29matching',raw='gap29_matching_original',year=2002,
      title='Propensity Score-Matching Methods for Nonexperimental Causal Studies',authors='Rajeev H. Dehejia and Sadek Wahba',
      file='Propensity Score-Matching Methods for Nonexperimental Causal Studies Dehejia(2002).pdf',
      version='Author-hosted published Review of Economics and Statistics 84, 151-161',
      anchors=['Physical PDF p.1: title, authors, published identity and related-data purpose'],
      claims=['Attribution and identity only; no matching theorem or performance claim used'])]
    sources=[]
    for p in papers:
        dest=ROOT/'docs/papers'/p['file'];raw=ROOT/'docs/literature/raw'/(p['raw']+'.pdf')
        if not dest.exists():shutil.copyfile(raw,dest)
        assert dest.read_bytes()==raw.read_bytes()
        receipt=json.loads(raw.with_suffix('.receipt.json').read_text())
        sources.append(dict(integrated_citation_key=p['key'],kind='paper',title=p['title'],authors=p['authors'],year=p['year'],
          local_path=str(dest.relative_to(ROOT)),sha256=sha256(dest.read_bytes()).hexdigest(),source_identity=receipt['url'],
          version_date=p['version'],accessed_utc=receipt['accessed_utc'],inspected_anchors=p['anchors'],supported_claims=p['claims'],
          cutoff='2026-10-07; publication predates cutoff, access date is later',
          citation_count='not available',venue_metric='not used as evidence',
          correction_check='Author page flags PSID3 Hispanic mean; not used in experimental-only calculation' if p['year']==1999 else 'Identity records and available update fields inspected; bounded check only',
          retraction_status='No signal in inspected records; not comprehensive clearance'))
    sources.append(dict(integrated_citation_key='gap29data',kind='documentation',title='NSW experimental data and author archive documentation',
      authors='Rajeev H. Dehejia',version_date='Retrieved 29 October 2026; exact pre-cutoff page bytes unestablished',
      source_identity='https://users.nber.org/~rdehejia/nswdata2.html',
      local_copy=ref('docs/literature/raw/gap29_nsw_original_page.html','Data Use and Citation; NSW Dehejia-Wahba sample; Correction'),
      data=[ref('docs/literature/raw/gap29_nsw_'+a+'.txt','Documented experimental '+a+' rows') for a in ['treated','control']],
      inspected_anchors=['Data Use and Citation: CC BY-NC 2.0 and three requested attributions',
                         '185/260 sample and ten-column order','PSID3 Hispanic mean correction'],
      supported_claims=['Data identity, field order, target subset and current stated terms'],
      limits=['No commercial-use or redistribution authority inferred','Original assignment logs unavailable']))
    sources.append(dict(integrated_citation_key='gap29r',kind='software',title='R stats linear-model fitting',authors='R Core Team',
      version_date='Installed R/stats 4.1.2',source_identity='/usr/lib/R/library/stats',
      local_copy=ref('docs/scientific-gap-closure/2026-10-29/r-stats-description.txt','Installed stats DESCRIPTION'),
      artifacts=[ref('docs/scientific-gap-closure/2026-10-29/'+p,a) for p,a in [
        ('r-functions-inspected.txt','lm -> model.matrix -> lm.fit -> C_Cdqrls; hatvalues implementation'),
        ('r-lm-help-readable.txt','Arguments method; Details'),('r-copyright.txt','Distribution-specific notices'),('r-session.txt','Runtime identity')]],
      supported_claims=['Observed QR-based lm calculation; HC2 implemented explicitly in project R code'],
      limits=['No causal-package, adapter or full transitive runtime qualification']))
    inherited=json.loads((ROOT/'docs/scientific-synthesis/2026-10-29/source-audit.json').read_text())
    sources.append(next(s for s in inherited['sources'] if s.get('integrated_citation_key')=='exec13_census_text_review_arxiv'))
    audit=dict(date='2026-10-29',cutoff='2026-10-07',sources=sources,
      inherited_audit=ref('docs/scientific-synthesis/2026-10-29/source-audit.json','Existing inspected sources, unchanged'),
      source_support='Paper claims tied to listed anchors; numerical findings are project calculations',
      citation_venue_metadata='Counts unavailable; not a ranking or correctness claim',
      forward_snowball='Author publication page and Crossref identity/update records inspected; comprehensive forward citation search not completed',
      backward_snowball=[dict(candidate='LaLonde 1986',role='Foundational and required data attribution',action='Original not acquired; no direct technical claim'),
        dict(candidate='Dehejia and Wahba 2002',role='Related data attribution',action='Authentic published PDF retained; no matching comparison in this batch'),
        dict(candidate='Freedman 2008',role='Critique discussed by Lin',action='Not independently used for theorem support'),
        dict(candidate='Smith and Todd 2005',role='Observational-matching competitor on author page',action='Inspect before extending to nonexperimental matching claims')],
      quarantined_sources=[],
      scope='Bounded experimental-subset analysis and measurement derivation; not a completed survey',
      project_evidence=[ref('docs/scientific-gap-closure/2026-10-29/'+p,'Executed result or frozen study specification') for p in
                        ['study-plan.json','study-results.json','r-verification.json','interface-results.json','measurement-results.json',
                         'servicing-plan.json','servicing-results.json','servicing-verification.json',
                         'funding-plan.json','funding-results.json','funding-verification.json',
                         'observation-plan.json','observation-results.json','additional-numerical-verification.json',
                         'policy-uncertainty-plan.json','policy-uncertainty-results.json','new-results-verification.json']])
    (OUT/'source-audit.json').write_text(json.dumps(audit,indent=2)+chr(10))
    omissions=dict(items=[dict(title='Evaluating the Econometric Evaluations of Training Programs',author='Robert LaLonde',year=1986,
       status='original_not_acquired',reason='Author-hosted guessed route returned HTTP 404. Do not cite as inspected; no substitute summary.',
       evidence=ref('docs/literature/raw/gap29_lalonde_original.receipt.json','Failed public GET'),
       action='Locate a legitimate authentic original before broader redistribution requiring all requested citations or a direct technical citation.')],
       frontier_census='Historical 82 inspected/31 unread; public-study batch alone adds no frontier original. See frontier-source-audit.json for the current 85/28 follow-up.',
       unknowns=['Full original assignment/selection history','Data commercial-use rights','Comprehensive forward citation and correction clearance'])
    (OUT/'source-omissions.json').write_text(json.dumps(omissions,indent=2)+chr(10))
    (OUT/'ATTRIBUTION.md').write_text('NSW author archive: Rajeev H. Dehejia. Current page states CC BY-NC 2.0. Local methodological research only; no commercial redistribution permission inferred. The archive requests attribution to LaLonde (1986), Dehejia and Wahba (1999), and Dehejia and Wahba (2002). The latter two authentic papers are retained; the LaLonde original remains an explicit source omission, not a direct scholarly citation or technical support. The edited analysis export preserves numerical records and adds headers. Author source bytes remain unchanged.'+chr(10))
    bib=r'''@article{gap29dehejia,author={Dehejia, Rajeev H. and Wahba, Sadek},
 title={Causal Effects in Nonexperimental Studies: Reevaluating the Evaluation of Training Programs},
 journal={Journal of the American Statistical Association},year={1999},volume={94},number={448},pages={1053--1062}}
@article{gap29lin,author={Lin, Winston},
 title={Agnostic Notes on Regression Adjustments to Experimental Data: Reexamining Freedman's Critique},
 journal={The Annals of Applied Statistics},year={2013},volume={7},number={1},pages={295--318}}
@article{gap29matching,author={Dehejia, Rajeev H. and Wahba, Sadek},title={Propensity Score-Matching Methods for Nonexperimental Causal Studies},
 journal={The Review of Economics and Statistics},year={2002},volume={84},number={1},pages={151--161}}
@misc{gap29data,author={Dehejia, Rajeev H.},title={NSW Experimental Data and Archive Documentation},year={2026},
 note={Author archive, accessed 29 October 2026. Historical study and current use terms distinguished.}}
@manual{gap29r,author={{R Core Team}},title={R stats Linear-Model Fitting},year={2021},
 note={Installed R and stats 4.1.2. Local help, implementation and runtime inspected.}}
'''
    (OUT/'refs.bib').write_text(bib)
    print(json.dumps(dict(sources=len(sources),papers=3,frontier_count_unchanged=True)))

if __name__=='__main__':main()

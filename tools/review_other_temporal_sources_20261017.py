#!/usr/bin/env python3
"""Bounded original-source review for Julia/Rust/MATLAB temporal discovery."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'docs/program/execution/2026-10-17/other-temporal'
RAW = ROOT/'docs/literature/raw'
PRIOR = ROOT/'docs/program/execution/2026-10-17/variable-ontology/publication/reader/source-audit.json'
OP = 'SW.CELL.discovery_temporal_interventional.other_relevant'
OUTPUT = ROOT/'docs/program/comprehensive-v14/work'/OP/'coverage-review.json'
REVIEWER = {'name': 'Codex author/coordinator', 'kind': 'author', 'role': 'Author primary-source and mathematical review',
            'independent': False}
LIMITS = [
    'Bounded cutoff-compatible searches and selected technical paths; no exhaustive ecosystem or absence assertion.',
    'Static originals and exact authored examples; no downloaded engine, licensed MATLAB, GPU or live-model execution.',
    'Complete package/dependency rights, temporal test calibration and target-preserving adapters remain unqualified.',
    'No general latent-graph identification, bank validation, independent review, adoption or ROI claim.',
    'Rendered visual acceptance remains open under the inherited exhausted image allowance; other work continues.'
]
PAPERS = [
    {'key': 'mvgc_paper', 'stem': 'mvgc-paper',
     'title': 'The MVGC Multivariate Granger Causality Toolbox: A New Approach to Granger-causal Inference',
     'filename_title': 'The MVGC Multivariate Granger Causality Toolbox A New Approach to Granger-causal Inference',
     'first_author': 'Barnett', 'author': 'Lionel Barnett and Anil K. Seth', 'year': 2014,
     'version_date': 'Preprint submitted to Journal of Neuroscience Methods, 2014-01-03; pinned repository original',
     'raw': 'exec17_other_temporal_follow_mvgc_1.pdf'},
    {'key': 'cdnod_paper', 'stem': 'cdnod-paper',
     'title': 'Causal Discovery from Heterogeneous/Nonstationary Data',
     'filename_title': 'Causal Discovery from Heterogeneous Nonstationary Data',
     'first_author': 'Huang',
     'author': 'Biwei Huang and Kun Zhang and Jiji Zhang and Joseph Ramsey and Ruben Sanchez-Romero and Clark Glymour and Bernhard Schölkopf',
     'year': 2020, 'version_date': 'JMLR 21 (2020), 1-53; published May 2020',
     'raw': 'exec17_other_temporal_cdnod_paper.pdf'}
]


def read(path):
    return json.loads(path.read_text())


def extract():
    records = []
    for paper in PAPERS:
        raw = RAW/paper['raw']; data = raw.read_bytes()
        receipt = raw.with_suffix('.receipt.json'); r = read(receipt)
        assert data.startswith(b'%PDF-') and r['sha256'] == hashlib.sha256(data).hexdigest()
        subprocess.run(['pdfinfo', str(raw)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=20)
        target = ROOT/'docs/papers'/f'{paper["filename_title"]} {paper["first_author"]}({paper["year"]}).pdf'
        assert not target.exists(); shutil.copyfile(raw, target)
        text = BASE/(paper['stem']+'.txt'); assert not text.exists()
        subprocess.run(['pdftotext', '-layout', str(raw), str(text)], check=True, timeout=25)
        records.append(dict(paper, local_copy=ref(target, 'Genuine original PDF'),
            retrieval=ref(receipt, 'Actual collector receipt'), source_identity=r['url'],
            extracted_text=ref(text, 'Paginated original primary text')))
    write(BASE/'paper-acquisition.json', {'papers': records, 'accessed_utc': datetime.now(timezone.utc).isoformat()})
    print(json.dumps({'genuine_papers': len(records)}))


# Selected paths only. These ranges are retained with actual original excerpts;
# a package-wide claim cannot be inferred from a README or these excerpts.
INSPECTIONS = {
    'associations_0': ([(17,45)], 'Shannon transfer entropy is conditional mutual information of source past and target future given target past and optional conditioning past.'),
    'associations_1': ([(1,115)], 'The embedding declaration distinguishes nonpositive source/target-past lags and positive prediction lags, measured in sample steps.'),
    'associations_2': ([(1,45)], 'The selected surrogate path returns count(null >= observed)/B without adding one.'),
    'associations_3': ([(57,116)], 'The final information statistic conditions on (T,C), while this transfer-entropy-specific local permutation helper chooses neighbours in C alone. This requires path-specific qualification, not an executed failure assertion.'),
    'associations_4': ([(1,85)], 'CCM configures reconstruction dimension, a default negative embedding lag and a temporal exclusion window; cross-map prediction correlation is not a bank do-effect.'),
    'associations_5': ([(45,85)], 'The selected cross-map calculation correlates actual and predicted target values.'),
    'associations_6': ([(1,60)], 'Project version4.7.1 and Julia compatibility^1.10.11; declared dependencies require their own rights/runtime review.'),
    'extra_associations_0': ([(1,35),(115,160)], 'Manual lag lengths and uniqueness are checked; joint embeddings are constructed. A multidimensional TODO is retained rather than assumed implemented.'),
    'varlingam_0': ([(1,105),(350,430),(470,500)], 'VAR residuals feed DirectLiNGAM. Actual lag helper uses (I-B0)M, despite an inverse comment at its call. Edge significant means an absolute coefficient threshold, default0.05; the sample-size multiplier is a heuristic.'),
    'varlingam_1': ([(1,100)], 'Cargo version0.1.0, MIT OR Apache-2.0 declaration, numerical/parallel/Python dependencies; no complete dependency qualification.'),
    'extra_varlingam_0': ([(1,103)], 'The selected VAR design uses raw lagged columns without an intercept or internal demeaning; information criteria use a pooled isotropic residual-variance likelihood approximation.'),
    'extra_varlingam_1': ([(1,25),(100,160)], 'Python interfaces are registered in source; advertised bootstrap, RCD, scalable interfaces and speedups are not inspected performance evidence.'),
    'bnt_0': ([(1,60)], 'A caller supplies intra/inter-slice adjacency, node sizes and parameter classes; acyclicity is checked. This is a supplied DBN constructor.'),
    'bnt_1': ([(1,13)], 'The file do_intervention.m declares mutilate_bnet, removes incoming arcs and installs root_CPD. The filename/function mismatch remains a runtime qualification question.'),
    'bnt_2': ([(1,65)], 'Topology unrolling repeats the supplied intra/inter-slice graph; it does not infer it from data.'),
    'bnt_3': ([(1,70)], 'Ordinary forward sampling skips supplied evidence cells. Without a separate conditioning procedure, clamping cells is not general posterior sampling given evidence.'),
    'follow_bnt_0': ([(1,36)], 'A root CPD requires no parents and is assumed observed/clamped; its constructor stores the supplied value.'),
    'follow_bnt_1': ([(1,12)], 'Root-CPD sample_node returns CPD.val exactly.'),
    'mvgc_0': ([(1,90)], 'README describes MVGC1 v1.3 March2022 and a newer state-space path; the latter is not inspected or executed here.'),
    'mvgc_1': ([(1,24)], 'The original license notice explicitly grants GPLv3-or-later; metadata NOASSERTION is not a contrary license finding.'),
    'mvgc_2': ([(1,55),(110,150)], 'Input axes are variables, observations and trials. The selected estimator demeans and forms within-trial lag designs for OLS/LWR.'),
    'mvgc_3': ([(150,230)], 'Spectral radius, positive residual covariance and Lyapunov/autocovariance diagnostics expose stability and truncation failures; they do not prove causal assumptions.'),
    'mvgc_4': ([(1,90)], 'Pairwise conditional GC uses target row/source column and log reduced/full prediction-error variance; diagonal is unavailable.'),
    'mvgc_5': ([(1,115)], 'The p-value interface calls the theoretical GC distribution and preserves unavailable diagonal/NaN entries; model/calibration premises remain necessary.'),
    'mvgc_6': ([(1,155)], 'Bonferroni, Holm and FDR variants adjust supplied p-values; correction cannot validate an invalid input null law.'),
    'follow_mvgc_0': ([(90,150)], 'Default F form applies to univariate target, chi-square to multivariate target; effective observations N(m-p). Noncentral F is explicitly experimental.'),
    'follow_mvgc_1': ([], 'Genuine Barnett and Seth preprint; paper-specific paginated anchors are recorded separately.'),
    'trentool_0': ([(1,25)], 'README v3.4.2 declares MATLAB and CUDA C/C++ components, FieldTrip and TSTOOL; it is a neural-series workflow, not established bank effect software.'),
    'trentool_1': ([(1,20)], 'The repository includes GNU GPL version3 text. Individual source headers grant GNU GPL without an explicit version; complete distributed-component rights remain unqualified.'),
    'trentool_2': ([(1,25),(30,125)], 'Configuration distinguishes sampling Hz, seconds, prediction milliseconds and embedding delays in autocorrelation-time units; trial, Ragwitz and GPU constraints require preservation.'),
    'trentool_3': ([(1,25),(70,105),(315,350)], 'Selected surrogate choices and default alpha0.05/FDR/one-tail/shift-test settings are implementation choices, not a proof of temporal exchangeability.'),
    'trentool_4': ([(225,270)], 'One-tail permutation fraction counts strict null>observed and clamps zero to1/B. Two-tail code uses the smaller tail against alpha/2. It is not the Associations raw-zero convention.'),
    'cdnod_0': ([(1,80)], 'README documents nonstationary/heterogeneous discovery; its graph encoding must be read with the actual entrypoint.'),
    'cdnod_1': ([(1,80)], 'Original repository usage instructions and source identity; no top-level redistribution permission established by these inspected bytes.'),
    'cdnod_2': ([(1,95)], 'Example uses variables and domain/time context and calls nonsta_cd_new; a time index alone is not a randomized treatment.'),
    'cdnod_3': ([(1,95)], 'Example supplied to the same-row discovery entrypoint; no dedicated Algorithm5 lag assembly is established on this inspected path.'),
    'cdnod_4': ([(1,95)], 'Example demonstrates changing modules and direction inference in its supplied construction, not bank validation.'),
    'follow_cdnod_0': ([(1,82),(100,135),(145,180)], 'The entrypoint appends/standardizes context, calls CI tests and orients g(i,j)=1,g(j,i)=0. Unresolved edges start with -1 both ways. Header reserves rights; explicit lag assembly/time-tier constraints are not present in this inspected entrypoint.'),
    'follow_cdnod_1': ([(1,35),(65,110)], 'Kernel bandwidth/regularization defaults and standardization are explicit; final direction statistic is not a p-value. Dense kernel computations need resource limits.'),
    'follow_cdnod_2': ([(1,120)], 'The selected changing-module visualization uses kernel PCA; its components are not validated bank latent causes.')
}

PACKAGE_NAMES = {
    'associations': 'Associations.jl (formerly CausalityTools.jl)',
    'varlingam': 'varlingam-rs', 'bnt': 'MATLAB Bayes Net Toolbox',
    'mvgc': 'MVGC1', 'trentool': 'TRENTOOL3', 'cdnod': 'CD-NOD MATLAB'
}


def source(key, title, author, path, kind, claims, records, identity=None, version='2026-10-17'):
    return {'integrated_citation_key': 'exec17_temporal_'+key,
        'title': title, 'author': author, 'kind': kind, 'year': 2026,
        'source_identity': identity or 'Project-authored proposal reference',
        'version_date': version, 'cutoff': '2026-10-07',
        'local_copy': ref(path, title), 'inspected_anchors': claims,
        'supported_claims': claims, 'records': records, 'limitations': LIMITS}


def review():
    acquisition = read(BASE/'acquisition-verification-v2.json')
    verify_bindings(acquisition); assert acquisition['status'] == 'pass'
    assert len(acquisition['records']) == 40
    prior = read(PRIOR); verify_bindings(prior)
    inherited = {s['integrated_citation_key']:s for s in prior['sources']}
    originals, packages = [], {}
    for row in acquisition['records']:
        short = row['id'].removeprefix('exec17_other_temporal_')
        spans, claim = INSPECTIONS[short]
        raw = ROOT/row['local_copy']['path']; data = raw.read_bytes()
        assert len(data) == row['expected_bytes']
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest() == row['blob_sha1']
        receipt = read(ROOT/row['retrieval']['path'])
        assert receipt['sha256'] == hashlib.sha256(data).hexdigest()
        assert receipt['url'] == row['url'] and row['pin']['date'][:10] <= '2026-10-07'
        encoding = 'not_text'
        lines = []
        if row['extension'] != 'pdf':
            try:
                lines = data.decode('utf-8').splitlines()
                encoding = 'utf-8'
            except UnicodeDecodeError:
                # Preserve every byte; only ASCII code/technical anchors are
                # interpreted for legacy files with undecodable comment bytes.
                lines = data.decode('latin-1').splitlines()
                encoding = 'latin-1 byte-preserving fallback; non-ASCII prose not used'
        anchors = []
        for a,b in spans:
            assert 1 <= a <= len(lines), (short,a,len(lines))
            end = min(b,len(lines))
            anchors.append({'anchor':f'lines {a}-{end}', 'excerpt':'\n'.join(lines[a-1:end])})
        if row['extension'] == 'pdf':
            anchors = [{'anchor':'Sections2.1-2.3,3.3; genuine paginated original',
                        'extracted_text':ref(BASE/'mvgc-paper.txt','Inspected preprint text')}]
        record = dict(row, inspected_anchors=anchors, supported_claims=[claim], excerpt_encoding=encoding,
                      role='inspected_primary_technical_text')
        originals.append(record); packages.setdefault(row['package'],[]).append(record)
    assert set(INSPECTIONS) == {r['id'].removeprefix('exec17_other_temporal_') for r in originals}
    extra = []
    for family, n in [('associations',1),('varlingam',1),('bnt',1)]:
        path = RAW/f'exec13_other_file_{family}_{n}.txt'
        lines = path.read_text().splitlines()
        extra.append({'family':family,'local_copy':ref(path,'Inherited original license text'),
            'inherited_audit':inherited['exec13_other_'+family],
            'inspected_anchors':[{'anchor':f'lines1-{min(len(lines),30)}',
                'excerpt':'\n'.join(lines[:30])}],
            'supported_claims':[{'associations':'MIT notice; complete dependencies remain separate.',
                'varlingam':'Cargo MIT OR Apache-2.0 declaration and saved license original; full rights qualification remains separate.',
                'bnt':'GNU Library GPL version2 text; complete component and distribution qualification remains separate.'}[family]]})
    paper_rows = []
    page_claims = {
        'mvgc_paper': [(1,'Title, authors and 2014-01-03 preprint identity'),
            (2,'Section2: predictive definition; VAR coefficients need not represent a generating causal mechanism.'),
            (3,'Section2.1: covariance stationarity, stable VAR and nonsingular spectrum.'),
            (4,'Sections2.2-2.3: reduced/full prediction error and conditional multivariate GC.'),
            (14,'Section3.3: collinearity, nonstationarity, long memory, moving average and independent-trial cautions.'),
            (15,'Section3.3: heteroscedasticity can invalidate standard statistical tests.')],
        'cdnod_paper': [(1,'JMLR21(2020) original identity'),
            (8,'Assumption1: confounders are domain functions or smooth time functions, fixed within instance; not arbitrary latent confounding.'),
            (9,'Independent disturbances/mechanism parameters, augmented Markov/faithfulness and no-selection premises.'),
            (22,'Additional orientation assumptions and equivalence-class limits.'),
            (25,'Section6.1 explicitly develops lagged extension using m(P+1) columns and no-future-to-past restriction.'),
            (26,'Lagged common causes needed for contemporaneous skeleton; certain stationary-confounded changing-module alternatives remain indistinguishable.'),
            (27,'Algorithm5 is an explicit time-varying instantaneous/lagged skeleton algorithm.'),
            (29,'Section7 connects mechanism changes to soft interventions; this does not certify an observed bank regime as randomized.')]
    }
    for paper in read(BASE/'paper-acquisition.json')['papers']:
        verify_bindings(paper)
        pages = (ROOT/paper['extracted_text']['path']).read_text().split('\f')
        anchors = []
        for number,claim in page_claims[paper['key']]:
            anchors.append({'anchor':f'Physical PDF page {number}', 'finding':claim,
                'extracted_text':paper['extracted_text'], 'page_text':pages[number-1]})
        s = {k:v for k,v in paper.items() if k not in ['key','stem','raw']}
        s.update(integrated_citation_key='exec17_temporal_'+paper['key'], kind='paper',
            local_path=paper['local_copy']['path'],sha256=paper['local_copy']['sha256'],
            inspected_anchors=anchors,supported_claims=[x['finding'] for x in anchors],
            cutoff='2026-10-07',limitations=LIMITS)
        paper_rows.append(s)
    hyvarinen = inherited['hyvarinen2010']
    hytext = ROOT/hyvarinen['text_path']
    primary = {'status':'pass_for_bounded_static_synthesis','reviewer':REVIEWER,
        'originals':originals,'inherited_license_originals':extra,'new_papers':paper_rows,
        'inherited_structural_var':hyvarinen,
        'inherited_structural_var_text':ref(hytext,'Sections2-2.3, printed1711-1713'),
        'runtime_execution':'No downloaded package, MATLAB/GPU or live-model execution',
        'limitations':LIMITS}
    verify_bindings(primary); write(BASE/'source-review.json',primary)
    sources = list(paper_rows)
    for family,records in packages.items():
        pin=records[0]['pin']
        claims=[c for r in records for c in r['supported_claims']]
        rights=[r for r in extra if r['family']==family]
        sources.append(source(family,PACKAGE_NAMES[family]+' temporal source comparison',
            pin['repository'],ROOT/records[0]['local_copy']['path'],'software_primary_sources',
            claims,records+rights,'https://github.com/'+pin['repository'],
            'Pinned '+pin['sha']+'; '+pin['date']+'; accessed2026-10-17'))
    write(BASE/'technical-source-audit.json',{'sources':sources,'prior':ref(PRIOR,'686 preserved source records'),
        'new_records':8,'new_scholarly_pdfs':2})
    print(json.dumps({'originals':len(originals),'families':len(packages),'new_genuine_papers':2,'technical_review':'saved'}))


def register():
    # Preserve every returned search row, including repeated identities. Bounded
    # pagination and creation dates do not establish complete cutoff coverage.
    selected = {'edy-os/varlingam-rs':'varlingam',
        'Biwei-Huang/Causal-Discovery-from-Nonstationary-Heterogeneous-Data':'cdnod',
        'trentool/TRENTOOL3':'trentool'}
    queries, rows = [], []
    for i in range(6):
        path = RAW/f'exec17_other_temporal_search_{i}.json'
        receipt_path = RAW/f'exec17_other_temporal_search_{i}.receipt.json'
        data,receipt = read(path),read(receipt_path)
        assert receipt['sha256'] == hashlib.sha256(path.read_bytes()).hexdigest()
        queries.append({'index':i,'url':receipt['url'],'total_count':data['total_count'],
            'returned':len(data['items']),'incomplete_results':data['incomplete_results'],
            'local_copy':ref(path,'Original returned search metadata; not technical evidence'),
            'retrieval':ref(receipt_path,'Exact query and receipt')})
        for position,item in enumerate(data['items'],1):
            name=item['full_name'];family=selected.get(name)
            if name=='treeshin/MVGC1':
                disposition='possible_copy_or_related_variant_not_verified'
                reason='Canonical lcbarnett/MVGC1 inspected separately; equality of this repository is not established.'
            elif family:
                disposition='selected_primary_paths_inspected'
                reason='Bounded original-source comparison; no whole-engine qualification.'
            else:
                disposition='uninspected_candidate_deferred'
                reason='Metadata lead only; no rejection or temporal-capability/absence conclusion.'
            rows.append({'query_index':i,'position':position,'candidate':name,
                'url':item['html_url'],'created_at':item['created_at'],
                'default_branch':item['default_branch'],'family':family,
                'disposition':disposition,'reason':reason})
    assert len(rows)==43 and all(not q['incomplete_results'] for q in queries)
    aliases=[{'family':k,'names':([v,'CausalityTools.jl'] if k=='associations' else [v]),
              'selection':'Inherited identity/manual canonical lead plus bounded searches',
              'technical_evidence':ref(BASE/'source-review.json',k)}
             for k,v in PACKAGE_NAMES.items()]
    write(BASE/'candidate-register.json',{'cutoff':'2026-10-07 Asia/Shanghai',
        'stopping_rule':'Six saved GitHub queries, at most first10 results each; no pagination. Plus inherited canonical leads and first10/35 OpenAlex matches.',
        'queries':queries,'returned_entries':rows,'aliases':aliases,
        'inherited_search':read(BASE/'inherited-search.json'),
        'coverage_outcome':'inconclusive','limits':[
            'Creation cutoff is a discovery filter; current search ranking and metadata need not reconstruct historical search results.',
            'Only selected technical revisions are pinned before cutoff.',
            'Finite queries omit terminology, languages, repositories and later result pages; no ecosystem absence claim.',
            'Aliases and copies are not merged without technical identity evidence.']})
    gaps = [
        ('search','Uninspected43-row leads and later pages, MVGC2, kernel/multiscale/PTE variants and JavaScript tooling.',
         'Run successor bounded queries/pagination and inspect original technical/license paths; retain all candidate dispositions.'),
        ('associations_null','Conditional neighbour set differs from final conditioning set on the selected helper; surrogate validity and multidimensional path incomplete.',
         'Before adapting, define complete null/clock/conditioning law, compare helper paths, qualify any correction against generated null/alternative cases.'),
        ('varlingam_runtime','Intercept/centering, isotropic order criterion, coefficient flags and inherited entropy-cache question; bootstrap/scalable paths uninspected.',
         'Use independently computed centered VAR and full-covariance criteria; inspect residual estimator/cache and Python boundary; register equivalence and fresh stability tests.'),
        ('bnt_call','Supplied graph and intervention/sampling semantics; filename/function mismatch unresolved.',
         'Resolve actual callable path in a permitted MATLAB environment, enumerate a small supplied model and compare conditioning with surgery; inspect engine evidence handling.'),
        ('mvgc_scope','Newer state-space path and dependent calendar/asymptotic calibration not inspected or qualified.',
         'Pin/inspect state-space sources; use whole-calendar/trial generators, stable and misspecified VARs, preserved failures and finite null calibration.'),
        ('trentool_scope','GPL component details, MATLAB/GPU dependencies, time-unit conversion and surrogate/multiple-test calibration unqualified.',
         'Complete permitted distribution inventory, predeclare sampling/embedding/surrogates, compare frozen CPU/GPU numerical outputs and all-request calibration.'),
        ('cdnod_bridge','Paper Algorithm5 lag extension is real; selected entrypoint has no dedicated lag/time-tier assembly. Top-level code rights unresolved.',
         'Obtain explicit code permission or use paper-only mathematical reference; inspect/implement an original typed lag construction with temporal constraints and exact endpoint oracle.'),
        ('rights','Complete component/dependency/data terms and distribution choices remain open for all families.',
         'Prepare per-component inventory before any download execution, adaptation, port or redistribution. No integration permission is awarded here.'),
        ('identification','Unknown latent confounding, regime meaning and observationally equivalent structures can leave intervention effects unidentified.',
         'State restricted assumptions and effect sets; obtain justified exogenous variation or a permitted public experiment only where necessary. More metadata cannot resolve equivalent laws.'),
        ('visual','Inherited six-image allowance exhausted.',
         'Use a fresh session for rendered review; continue text/source/math and other independent proposal work now.')
    ]
    write(BASE/'omissions-register.json',{'scope':'Concrete unresolved sources, rights, implementation and research questions',
        'items':[{'id':k,'gap':g,'route':r,'blocks':'Its own capability/coverage claim only'} for k,g,r in gaps],
        'evidence':[ref(BASE/'candidate-register.json','Every saved query row and alias'),
                    ref(BASE/'source-review.json','Inspected originals and exact limitations')],
        'no_essential_source_waiver':True,'integration_allowed':False})
    print(json.dumps({'saved_search_entries':len(rows),'queries':6,'omissions':len(gaps),'coverage':'inconclusive'}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('command', choices=['extract','review','register'])
    args = parser.parse_args(); {'extract': extract,'review':review,'register':register}[args.command]()

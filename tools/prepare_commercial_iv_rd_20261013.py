#!/usr/bin/env python3
"""Bind inspected vendor text, omissions and exact examples for the IV/RD reader."""
from datetime import datetime, timezone
import json
from pathlib import Path

import build_integrated_monograph_v12 as shared
import commercial_iv_rd_examples_20261013 as examples
import master_control as core
from publish_latent_r_review_v2_20261013 import verify_bindings, write

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/commercial-iv-rd'
ref = shared.ref


def main():
    completions = {}
    for p in sorted(BASE.glob('acquisition-completion-*.json')):
        for r in json.loads(p.read_text()):
            assert r['status'] == 'fulfilled'
            completions[r['value']['session']] = r['value']
    acquisition = []
    for p in sorted(BASE.glob('acquisition-0[1-7].json')):
        for r in json.loads(p.read_text()):
            assert r['status'] == 'fulfilled'
            row = r['value']
            result = completions[row['session_id']] if row.get('session_id') else row
            raw = BASE / (row['id'] + '.' + row['extension'])
            item = {k: row[k] for k in ['id', 'url', 'extension']}
            item.update(exit_code=result['exit_code'], observed_result=result['output'],
                status='saved' if result['exit_code'] == 0 else 'unavailable',
                command_record=ref(p, 'Preserved bounded public acquisition command result'),
                headers=ref(BASE / (row['id']+'.headers'), 'Preserved HTTP headers'))
            if raw.exists():
                item['local_copy'] = ref(raw, 'Authentic acquired bytes' if result['exit_code'] == 0 else 'Incomplete bytes excluded from technical evidence')
                item['bytes'] = raw.stat().st_size
                item['local_write_utc'] = datetime.fromtimestamp(raw.stat().st_mtime, timezone.utc).isoformat()
                if row['extension'] == 'pdf' and result['exit_code'] == 0:
                    assert raw.read_bytes().startswith(b'%PDF-')
            acquisition.append(item)
    acquisition.append({'id':'limdep_retry','url':'https://www.limdep.com/products/limdep/features.php',
        'extension':'html','status':'unavailable','exit_code':7,
        'observed_result':completions[84999]['output'],
        'execution':'Approved escalation retry after network failure; same no-route error.',
        'headers':ref(BASE/'limdep_retry.headers','No HTTP response from retry')})
    write(BASE/'acquisition-review.json', {'requests':acquisition,'cutoff':'2026-10-07',
        'access_date':'2026-10-13', 'runtime_executed':False,
        'transfers':'25-second and 12-MiB bounds, public HTTPS GET only; failed/partial files excluded.',
        'normalization_repairs':'The initial inline extraction had a Python string syntax error and no output. A successor script found bs4 unavailable and used the existing stdlib Document parser. No acquired bytes changed.'})
    by_id = {r['id']:r for r in acquisition}
    specs = [
        ('stata','StataCorp','Instrumental-variables estimation and weak-instrument postestimation',2026,
         'Mutable official manual acquired 2026-10-13; Stata 19 and Stata 18 StataNow feature identities separately inspected; exact cutoff bytes unresolved',
         [('stata_iv','lines1–116: estimators and covariance controls'),('stata_post','lines185–201,295–350,716–848,915–957: tests, grids, topology and stored results'),
          ('stata19_feature','title and weak-instrument feature description'),('stata18now','lines160–173: StataNow-specific feature list')],
         ['Documented AR/CLR test inversion and one-endogenous-regressor confidence-set scope.',
          'Adaptive grids, simulation controls, unconventional topology, empty-set distinction and stored output are explicit.',
          'No vendor runtime, universal finite calibration or all Stata 18 builds claimed.']),
        ('eviews','EViews','IV Diagnostics and Tests',2025,
         'Official help last updated 12 March 2025; acquired 2026-10-13; exact edition/update unresolved',
         [('eviews_iv','lines9–12,14–23,34–54,69–70: diagnostics, rank drops and applicability qualification')],
         ['Instrument summary, orthogonality, endogeneity and weak-instrument diagnostic roles differ.',
          'Cragg–Donald applicability is qualified; image-only formulas are not inferred.']),
        ('sas','SAS Institute','SAS/ETS 14.1 SYSLIN instruments, estimators and 2SLS example',2015,
         'Edition 14.1 HTML documentation; acquired 2026-10-13; later 15.1 partial PDF excluded',
         [('sas_syslin_overview','Overview and listed estimator/input/output methods'),
          ('sas_syslin_methods','Single Equation Estimation Methods and Choosing a Method: orthogonality, relevance and system assumptions'),
          ('sas_syslin_instruments','INSTRUMENTS Statement: all listed variables enter each first stage'),
          ('sas_syslin_2sls','First example, FIRST option, ENDOGENOUS statement and ANOVA/R-square caveat')],
         ['SYSLIN supplies systems and single-equation IV alternatives, conditional on scientific premises.',
          'Instrument and endogenous declarations, outputs and diagnostics need explicit translation.']),
        ('spss','IBM','SPSS Statistics 30 Two-Stage Least-Squares Regression',2026,
         'Version 30.0.0 official procedure page acquired 2026-10-13; exact update date unresolved; incomplete v19 PDF excluded',
         [('spss30_iv','lines21–34,44–63: outputs, assumptions, edition requirement and instrument-list semantics')],
         ['2SLS requires Standard edition or Regression option according to inspected text.',
          'Instrument/explanatory lists and model-based outputs do not verify identification or general robustness.']),
        ('rats','Estima','RATS 11 User’s Guide: instrumental variables',2025,
         'Version 11 guide, copyright 2025; acquired 2026-10-13; exact cutoff bytes unresolved',
         [('rats11','title/copyright; Section2.5 printed UG48–50, extracted2533–2630: instrument list, INST and covariance semantics')],
         ['Documented regression/system IV paths use explicit instrument lists, including an explicit constant.',
          'Covariance options and scientific moment assumptions remain part of the target operation.']),
        ('jmp','JMP Statistical Discovery','JMP 19 Multivariate Methods: model-implied instrumental variables',2025,
         'September 2025 edition; acquired 2026-10-13; intended installed entitlement still unverified',
         [('jmp19','title/copyright; printed195,206,225–227; extracted6749–6767,7166–7172,7775–7850: MIIV-2SLS and equation diagnostics')],
         ['SEM documents MIIV-2SLS, equation-level Sargan tests and instrument lists.',
          'Supplied-model instruments and local misspecification claims are not unrestricted causal discovery or immunity to invalid instruments.']),
        ('rdrobust','RD Packages developers','Pinned Stata rdrobust help, source and license',2026,
         'Commit 7df239395c4afce2a58e22ef16a5817341683955, committed 2026-10-07T22:36:54Z; version11.1.1 dated2026-10-01; UTC end-of-day cutoff query',
         [('rdrobust_help','lines1–58,81–107,120–185: RD targets, bandwidths, masspoints and covariance'),
          ('rdrobust_ado','lines5–10,488–526: version, unique-score counts and degenerate fuzzy first stage'),
          ('rdrobust_license_md','Full license declaration'),('rdrobust_cutoff','Commit identity/date only; not technical claims')],
         ['Upstream package is distinct from its commercial Stata host; documented robust bias correction is not a weak-IV guarantee.',
          'Mass-point handling, first-stage guard and output choices require preservation; GPL3 declaration retained.']),
        ('rddensity','RD Packages developers','Pinned Stata rddensity help and license',2026,
         'Commit e59c0ae59f82ace535cc7a4b2d68068ef05f1fb8, committed2026-09-24T17:18:10Z; acquired2026-10-13',
         [('rddensity_help','lines98–178: density/manipulation, binomial, graphics dependency, masspoints and statistics'),
          ('rddensity_license','Full license declaration'),('rddensity_cutoff','Commit identity/date only')],
         ['Documented manipulation diagnostics and dependencies do not certify causal validity.',
          'GPL3 declaration is separate from host execution rights.']),
        ('license','StataCorp','Stata license options',2026,
         'Mutable official license-options page acquired2026-10-13; service embedding and price not determined',
         [('stata_license','lines168–185,231–269: identified user and concurrent-network distinctions')],
         ['Named-user and concurrent-network routes differ; neither page reading nor local package license confers deployment rights.'])]
    sources = []
    for ident, author, title, year, version, anchors, claims in specs:
        items = []
        for name, anchor in anchors:
            row = by_id[name]
            assert row['status'] == 'saved', name
            raw = ROOT/row['local_copy']['path']
            text = BASE/(name+'.txt')
            if not text.exists():
                text = raw
            items.append({'source_identity':row['url'],'local_copy':ref(raw,anchor),
                'text_copy':ref(text,anchor),'inspected_anchor':anchor})
        sources.append({'integrated_citation_key':'exec13_ivrd_'+ident,'kind':'software_primary_sources',
            'title':title,'author':author,'year':year,'source_identity':items[0]['source_identity'],
            'version_date':version,'local_copy':items[0]['local_copy'],'additional_sources':items,
            'anchors':[a for _,a in anchors],'claims':claims,
            'limits':'Documented or static-source behavior only; no native run, measured performance, blanket absence claim or deployment acceptance.'})
    omissions = [
        {'candidate':'MATLAB / System Identification Toolbox / ivx / iv4','reason':'Both essential official pages returned403; capability and license comparison unresolved.','revisit':'Obtain edition-matched original technical text and the intended toolbox license.'},
        {'candidate':'OxMetrics / PcGive / IVE','reason':'Attempted official manual and index routes returned404; prior temporal study also retained unavailable originals.','revisit':'Locate current authoritative edition manual and IV/covariance/export sections.'},
        {'candidate':'LIMDEP / NLOGIT','reason':'Official feature route has no route to host, including escalated retry.','revisit':'Accessible original vendor technical manual and actual edition/rights record.'},
        {'candidate':'Later SAS/ETS 15.1 and SPSS19 PDF downloads','reason':'Transfers timed out and retained partial bytes; excluded from evidence. Complete SAS14.1 HTML and SPSS30 procedure text used instead.','revisit':'Only acquire later complete versions when that edition is in scope.'},
        {'candidate':'rdlocrand / rdmulti / rdpower / lpdensity / ivreg2 / weakiv / rivtest','reason':'Adjacent package families and community extensions are outside this bounded direct-source comparison. No feature absence or equivalence inferred.','revisit':'Separate pinned source/license/technical reviews; do not use mere mentions for claims.'},
        {'candidate':'Scholarly works referenced inside vendor and package manuals','reason':'Not newly cited as scholarly originals in this addition; software feature documentation is not promoted to their theorem proofs.','revisit':'Obtain and inspect correctly named real scholarly PDFs before adding scholarly claims.'}]
    write(BASE/'omissions-register.json', {'items':omissions,'essential_commercial_candidates_unresolved':3,
        'whole_cell_qualified':False,'unsupported_absence_claims':False})
    candidates = [
        ('Stata / StataNow / ivregress / estat weakrobust','Primary technical text inspected','Propose licensed adapter; preserve every interval component, grid and simulation boundary; no vendor port.'),
        ('SAS / SAS-ETS / SYSLIN','Edition14.1 primary text inspected','Propose equation-system export with all instrument declarations; later editions not inferred.'),
        ('EViews / TSLS / LIML / GMM','Primary diagnostics text inspected','Retain diagnostic applicability; do not relabel rank diagnostics as robust test inversion.'),
        ('IBM SPSS Statistics / Regression / 2SLS','Version30 procedure text inspected','Guided supplied-model path; explicit lists and covariance assumptions.'),
        ('RATS / INSTRUMENTS / INST','Version11 technical guide inspected','Scripted adapter candidate; explicitly include constants and intended covariance.'),
        ('JMP / JMP Pro / MIIV-2SLS','Version19 SEM technical guide inspected; installed entitlement unresolved','Keep supplied-model instrument identity and equation diagnostics; no general discovery claim.'),
        ('MATLAB / ivx / iv4','Essential primary source unavailable','Retain unresolved; no absence claim.'),
        ('OxMetrics / PcGive / IVE','Essential primary source unavailable','Retain unresolved; no absence claim.'),
        ('LIMDEP / NLOGIT','Essential primary source unavailable','Retain unresolved; no absence claim.')]
    search = {'cutoff':'2026-10-07','access_date':'2026-10-13','scope':'Nine named commercial families and two direct RD companions',
        'routes':[{'route':'Saved cutoff scholarly-metadata query','finding':'One off-topic big-data survey; it establishes no software capability.',
          'evidence':ref(ROOT/'docs/literature/raw/v12_sw_cell_iv_rd_design_commercial.json','Single metadata discovery result')},
          {'route':'Named vendor manual/API traversal and upstream cutoff commit/tree inspection',
           'finding':'Six commercial technical sources plus pinned upstream help/source acquired; all failed routes retained.',
           'evidence':ref(BASE/'acquisition-review.json','Every bounded source request and actual outcome')}],
        'stopping_rule':'Nine seeded families, selected IV postestimation pages and two direct RD companion packages; one official fallback per unavailable candidate, except required same-URL sandbox escalation retry. Adjacent extension leads retained as omissions.',
        'search_limit':'No exhaustive global census. A failed metadata query is explicitly uninformative. UTC end-of-day is used for GitHub cutoff queries; mutable acquired bytes do not establish exact historical availability.',
        'candidates':[{'candidate':a,'evidence_state':b,'decision':c} for a,b,c in candidates],
        'evidence':[ref(BASE/'plan-review.json','Reviewed bounded acquisition and comparison plan'),
                    ref(BASE/'omissions-register.json','Unresolved source, edition, rights and extension limits')]}
    write(BASE/'candidate-register.json',search)
    assert examples.calculate() == json.loads((BASE/'exact-results.json').read_text())
    for ident,title,path,anchor,claims in [
        ('exact','Exact eligibility, invalid-instrument, coarse-score and weak-set constructions',BASE/'exact-results.json',
         'Complete rational examples, sixteen-state moments and101 direct rectangle membership checks',
         ['The exclusion/direct-effect examples preserve exactly the claimed summaries, with stipulated USD40 cost.',
          'Proportional direct instrument effects satisfy both population moments at the wrong causal coefficient.',
          'Smooth response functions with identical discrete-score observations give opposite cutoff effects.',
          'A narrow grid can miss a nonempty disconnected ratio set; no vendor runtime or confidence coverage inferred.']),
        ('survey','Bounded commercial IV and RD source comparison and omissions',BASE/'candidate-register.json',
         'All nine candidate families, two search routes, exclusions and acquisition evidence',
         ['Six acquired commercial families and three unresolved essential-source candidates remain explicit.',
          'Proposed capability comparison does not confer licensed runtime, complete coverage or bank acceptance.']),
        ('dependent','Independent-pilot study feasibility and conservative precision planning',ROOT/'docs/program/execution/2026-10-13/dependent-design/design-review.md',
         'Restricted proof, failed predecessor, calibrated-noise floor, centered-width and exact-binomial screen review',
         ['New deterministic calculations do not approve a final qualification study.',
          'Centering moments, known bounds and oracle means are explicit planning concessions.',
          'Exact-binomial screen power and raw availability are separate from nominal confidence and useful precision.'])]:
        extra = ([ref(ROOT/'tools/commercial_iv_rd_examples_20261013.py','Exact generated law enumeration')]
                 if ident=='exact' else [ref(BASE/'acquisition-review.json','All source requests'),ref(BASE/'omissions-register.json','Unavailable primary material')]
                 if ident=='survey' else [ref(ROOT/'docs/program/execution/2026-10-13/dependent-design/calculations.json','Deterministic law, width and exact-binomial calculations'),
                   ref(ROOT/'docs/program/comprehensive-v14/work/SCI.DESIGN.R05S/successor-review.json','Recorded negative final-study candidate')])
        sources.append({'integrated_citation_key':'exec13_ivrd_'+ident,'kind':'project_derivation_and_review',
            'title':title,'author':'Causal banking research proposal project','year':2026,
            'source_identity':str(path.relative_to(ROOT)),'version_date':'Authored/reviewed2026-10-13; project evidence, no post-cutoff scholarly citation',
            'local_copy':ref(path,anchor),'additional_sources':extra,'anchors':[anchor],'claims':claims,
            'limits':'Author review and generated examples; no independent acceptance or actual bank/vendor performance.'})
    audit={'cutoff':'2026-10-07','sources':sources}
    verify_bindings(audit)
    write(BASE/'source-audit.json',audit)
    review={'status':'pass','issues':[],'reviewer':{'name':'Codex author/coordinator','kind':'author'},
        'scope':'Supported manuscript claims, source identities, exact examples and scoped negative study design',
        'findings':['Stata already documents five weak-IV set forms; no novelty or competitor absence claim is invented.',
            'Grid-induced emptiness, Monte Carlo critical values and one-endogenous-regressor inversion limits are preserved.',
            'Six commercial paths have distinct instrument/covariance/edition roles; three essential originals remain unresolved.',
            'RD host licensing, GPL3 upstream declaration, bias correction, weak first stages and missing score support remain distinct.',
            'Complier identity is conditional on the explicitly stipulated common limiting potential-outcome population.',
            'Exact examples check all finite statements; mathematical and USD planning assumptions are labeled.',
            'Dependent-design rejection is confined to final-study approval; old failures and proposal development route remain.'],
        'evidence':[ref(BASE/p,'Reviewed manuscript or source/evidence record') for p in
            ['comparison.tex','dependent-feasibility.tex','source-audit.json','candidate-register.json','omissions-register.json','exact-results.json']],
        'preflight_repair':'Removed an unused erroneous cubic probe after its assertion failed; no result had been saved. The retained discrete-support counterexample uses the independently checked quadratic factor.',
        'commercial_cell_complete':False,'visual_acceptance':False,'independent_review':False,'vendor_execution':False}
    write(BASE/'manuscript-review.json',review)
    (BASE/'refs.bib').write_text('\n'.join('@misc{'+s['integrated_citation_key']+',\n author={{'+shared.escape(s['author'])+'}},\n title={'+shared.escape(s['title'])+'},\n year={'+str(s['year'])+'},\n note={'+shared.escape(s['version_date'])+'}\n}\n' for s in sources))
    print(json.dumps({'sources':len(sources),'commercial_families_inspected':6,'essential_candidates_unresolved':3,
        'exact_replay':'pass','native_execution':False}))


if __name__ == '__main__':
    main()

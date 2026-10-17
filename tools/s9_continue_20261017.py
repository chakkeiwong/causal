#!/usr/bin/env python3
"""Finish S9 evidence, preserving build and source identities across successors."""
import argparse
import hashlib
import itertools
import json
import re
from pathlib import Path

import build_integrated_monograph_v12 as shared
import build_java_temporal_engine_20261016 as engine
import audit_reader_traceability_v2_20261013 as trace
import s9_port_references_20261017 as references
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
BASE = DOCS / 'program/execution/2026-10-17/s9'
PRIOR = DOCS / 'program/execution/2026-10-17/s8/publication-v3/reader/source-audit.json'
OLD = DOCS / 'causal_proposal_commercial_gap_reviewed_v3_2026-10-17.tex'
OLD_PDF = OLD.with_suffix('.pdf')
NAME = 'causal_proposal_language_reuse_reviewed_2026-10-17'
DRIVER = DOCS / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
PUB = BASE / 'publication-v1'
OUT = PUB / 'reader'
CHAPTER = BASE / 'development.tex'
CONTRACT_CHAPTER = DOCS / 'program/comprehensive-v14/work/TEXT.DRAFT.S9/chapter.tex'
INSERT = r'\input{program/execution/2026-10-17/s9/development.tex}'
NEW_KEYS = {'exec17_s9_route_decisions', 'exec17_s9_bank_oracle', 'exec17_s9_admission'}


def read(path):
    return json.loads(Path(path).read_text())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def put(path, value):
    write(Path(path), value)


def checked_source(path, anchor):
    return ref(ROOT / path, anchor)


def exact_extension():
    source = references.calculate()
    # Nine endpoint-mark pairs have only four arrow-presence signatures under
    # a conversion that tests arrowheads and forgets circle versus tail.
    marks = ('circle', 'tail', 'arrow')
    pairs = list(itertools.product(marks, repeat=2))
    signature = lambda pair: (pair[0] == 'arrow', pair[1] == 'arrow')
    signatures = sorted({signature(pair) for pair in pairs})
    groups = {}
    for pair in pairs:
        groups.setdefault(str(signature(pair)), []).append(list(pair))
    labels = ['A@t1', 'A@t2', 'B@t1', 'B@t2']
    lagged = [{'current': labels[i], 'previous': labels[i-1],
               'within_subject': labels[i].split('@')[0] == labels[i-1].split('@')[0]}
              for i in range(1, len(labels))]
    value = dict(
        inherited_exact_references=source,
        graph_mark_enumeration=dict(input_pairs=len(pairs),
            arrow_presence_signatures=len(signatures), collapsed_pairs=groups,
            distinct_pairs_lost=len(pairs)-len(signatures),
            scope='Authored encoding counterexample for arrow-presence-only conversion; not an upstream call.'),
        panel_clock_counterexample=dict(rows=labels, one_row_lag=lagged,
            cross_subject_pairs=sum(not x['within_subject'] for x in lagged),
            scope='Authored row-index example; not a test of the upstream routine.'),
        limitations=['All values are exact finite authored counterexamples.',
                     'No upstream R, Python, Java or C++ runtime or cross-language binding was executed.',
                     'Source inspection covers named paths and versions only; not complete package or legal review.'])
    return value


def route_ledger():
    return dict(status='prospective_source_bounded_route_decisions', cutoff='2026-10-07',
      decisions=[
       dict(id='R-pcalg', source='pcalg 2.7-12, pinned CRAN mirror commit 930fe476875ddc00528dbaacb6f48f2791ab12e3',
        action='ADOPT through a pinned native R worker for selected observational FCI/RFCI profiles; no reimplementation first.',
        reason='Source exposes search cap, NAdelete, >= alpha, selected endpoint conversion, R dependency and license declarations.',
        admission='Retain CI status, threshold, conditioning trace, search limits, endpoint class and explicit unsupported graph refusals.',
        reject_or_defer='Do not call it universal FCI, port its branch path without trace evidence, or assume imports and rights are closed.'),
       dict(id='R-rCausalMGM', source='rCausalMGM 1.0.1, CRAN commit 9e0101244c379a33a1329dfdcb6b9ffcb01fb0d4',
        action='ADOPT only as a distinct mixed-data R profile behind the Rcpp wrapper.',
        reason='Pinned docs describe mixed input, orientation choices and row deletion under missingness; C++ implementation is R-hosted.',
        admission='Begin with explicit complete-case profile; record dropped rows and test family; separately assess MAR/MNAR target consequences.',
        reject_or_defer='Reject as a standalone C++ core or drop-in pcalg equivalent; no missing-data claim without new evidence.'),
       dict(id='R-C++-MIIC', source='miic 2.0.4, pinned commit 9bb87a2ac02041f81ee63a57c3ec25e99bb25609',
        action='ADOPT as a separate discovery-family comparator through its R package; do not port from wrapper evidence alone.',
        reason='Distinct information-theoretic, latent and stationary temporal modes, C++14 compilation, Rcpp/OpenMP build, GPL >=2 declaration.',
        admission='Match the named mode, data regime, output meaning, orientation confidence and temporal stationarity; retain source diagnostics.',
        reject_or_defer='Reject translation of a latent flag into a generic PAG or graph into an effect; direct native C++ packaging remains uninspected.'),
       dict(id='Python-CausalML', source='CausalML 0.17.0 declared; inspected commit 49283de921ba66379bab71305d471de6ce893d34',
        action='ADOPT in Python for a selected binary T-learner profile; wrapper preserves original fit objects and bootstrap.',
        reason='One shared control fit, sorted treatment labels, row-index resampling and separately controlled learner randomness are source-visible.',
        admission='Pass action labels, target rows, fit identities, row/cluster sampling unit, index RNG and learner RNG as distinct fields.',
        reject_or_defer='Defer multi-arm or clustered uncertainty claims until separately qualified; direct requirements are not a resolved lock.'),
       dict(id='Java-Tetrad', source='Tetrad 7.6.11-SNAPSHOT at pinned commit b89afaf952a4fd647df0d85b08102250106c6764',
        action='ADOPT original JVM library for selected graph/search paths if its dependency and GPL obligations fit.',
        reason='Graph objects preserve endpoint types, but node lookup is identity-sensitive; selected core POM targets Java 21.',
        admission='Pin artifact, JDK, graph node map, endpoint vocabulary and the chosen search/options; run exact round-trip fixtures.',
        reject_or_defer='Do not treat newer nonstandard Python/R wrappers requiring JDK 25 as the same artifact or qualification.'),
       dict(id='C++-aGrUM', source='aGrUM pinned commit 2ec71906f4108684c5cfb96d1d44f2925e16a32e',
        action='ADOPT as an independent native C++ FCI/PAG comparator, not as a pcalg port.',
        reason='Possible-D-Sep, filtering, endpoint access and graph conversion have source-specific paths; dual LGPL-3-or-later/MIT statement has third-party caveats.',
        admission='Build only after dependency/rights inventory; compare graph-class outputs, node names, marks, missing-data behavior and diagnostics.',
        reject_or_defer='No runtime, binding, complete dependency-license or parity evidence; do not claim a cleared deployable product.'),
       dict(id='Universal-rewrite', source='Proposed one-language rewrite of every selected package',
        action='REJECT as the current default architecture; retain narrow ports only after measured constraint.',
        reason='Method families, endpoint conventions, clocks, RNG coupling, missingness and license/dependency models differ.',
        admission='Require a failing native-worker need, bounded equivalence domain, exact fixtures, resource benchmark, ownership and maintenance case.',
        reject_or_defer='An attractive common API or matching graph name is not an evidence-based reason to reimplement.')],
      limitations=['Routes are proposals based on inspected pinned originals, not executable code or accepted integration.',
                   'No legal opinion, resolved transitive dependency lock, package installation or bank deployment review.',
                   'No finding of absence is made outside selected inspected source paths.'])


def admission_protocol():
    return dict(status='prospective_protocol', request_fields=[
      'target population, action or graph question, outcome and units',
      'information cutoff, observation clock, subject key, row and inferential sampling unit',
      'variable ontology, missingness action, identification assumptions and requested result type',
      'method options, package identity, source version, dependency/environment digest',
      'random stream ownership, resampling indices, learner RNG and shared-fit identity',
      'endpoint vocabulary, node identifiers, temporal row map and resource/time bound'],
      response_fields=['request digest, explicit status and refusal reason',
      'target identity and point/identified-set/graph-class output',
      'uncertainty type and sampling law; diagnostics and effective controls',
      'source/runtime identity, fit and node maps, omitted rows and failed replicates'],
      gates=[
       dict(level=1,name='schema and clock',criterion='Required units, keys, temporal order and target are complete; unsupported fields refuse.'),
       dict(level=2,name='representation and branch fixtures',criterion='Exact graph marks, node permutations, threshold ties, missing tests and row maps pass.'),
       dict(level=3,name='numerical domain',criterion='Predeclared tolerance and decision-boundary consequences pass on admitted cases.'),
       dict(level=4,name='joint randomness',criterion='Coupled inputs or a predeclared joint-law comparison; no seed-equality shortcut.'),
       dict(level=5,name='operational qualification',criterion='Pinned build, dependency and rights inventory, resource limits, restart and assigned-request failures recorded.')],
      limitations=['Passing a lower level does not imply a higher level.',
                   'Protocol is prospective; no worker currently passes these gates by inclusion here.'])


def complete_source_review():
    required=['exec13_latentr_primary','exec14_causalml_primary','exec14_java_latent_sources',
              'exec14_native_agrum','exec14_native_miic','exec14_native_rcmgm',
              'exec13_pcalg_reuse_primary','exec13_tetrad_reuse_primary','exec15_javatemporal_tetrad']
    prior=read(PRIOR)['sources']
    integrated={x['integrated_citation_key']:x for x in prior}
    refs={
     'pcalg': [('exec13_pcalg_reuse_primary','docs/literature/raw/exec13_pcalg_description.txt','DESCRIPTION: version, R, License, Imports, LinkingTo','Pinned package constraints and source dependencies.'),
               ('exec13_latentr_primary','docs/literature/raw/exec13_latentr_r_pdsep.txt','FCI possible-D-Sep source and missing-test branch','Search cap, missing-test substitution and threshold comparison.' )],
     'CausalML': [('exec14_causalml_primary','docs/literature/raw/exec14_causalml_pyproject.txt','project version, Python constraint and direct requirements','Declared version, Python floor and direct requirement list.'),
                  ('exec14_causalml_primary','docs/literature/raw/exec14_causalml_license.txt','root Apache-2.0 notice','Root package license declaration; dependencies remain separate.')],
     'Tetrad': [('exec13_tetrad_reuse_primary','docs/literature/raw/v12_exec13_java_tetrad_libpom.txt','library POM: release 21 and dependencies','Pinned library Java release and declared Maven dependencies.'),
                ('exec13_tetrad_reuse_primary','docs/program/repair-v12/work/SW01/extracted/pinned-tetrad-LICENSE.txt','pinned root GPL text and distribution terms','Pinned root GPL text; no complete dependency-rights conclusion.')],
     'MIIC': [('exec14_native_miic','docs/literature/raw/exec14_cxx_latent_miic_r_description.txt','DESCRIPTION: version, GPL, Imports, LinkingTo','R package version, declared GPL, imports and Rcpp linking.'),
              ('exec14_native_miic','docs/literature/raw/exec14_cxx_latent_miic_r_readme.txt','Prerequisites and C++14 build declaration','R/C++ wrapper and source build compiler prerequisite.'),
              ('exec14_native_miic','docs/literature/raw/exec14_cxx_latent_miic_r_makevars.txt','OpenMP compiler/link flags','Package build delegates OpenMP flags through R.')],
     'rCausalMGM': [('exec14_native_rcmgm','docs/literature/raw/exec13_cxx_lead_4_source_0.txt','DESCRIPTION: version, GPL-3, Imports, LinkingTo','Rcpp-hosted package and declared dependencies/license.'),
                    ('exec14_native_rcmgm','docs/literature/raw/exec14_cxx_latent_rcmgm_fci_api.txt','fciStable public arguments, missing-row behavior and return','Documented FCI-Stable profile and complete-case row drop.')],
     'aGrUM': [('exec14_native_agrum','docs/program/execution/2026-10-14/cxx-latent/primary-review.json','Pinned source paths, PAG behavior, endpoint and license findings','Pinned native-source review and explicit separate third-party terms.'),
               ('exec14_native_agrum','docs/literature/raw/exec14_cxx_latent_fci_cpp.txt','FCI implementation traversal and filter','Source-level traversal and candidate filtering.')],
     'temporal': [('exec15_javatemporal_tetrad','docs/literature/raw/exec15_javatemporal_tetrad_1.txt','Tetrad positional lag source lines375-448','Row-position lag construction and lack of subject/time arguments in this method.')]
    }
    package_sources={}; audit_index={x['integrated_citation_key']:x for x in prior}
    def upstream_identity(key,path):
        receipt=ROOT/(path+'.receipt.json')
        if receipt.is_file():
            item=read(receipt)
            if item.get('url'):return item['url']
        source=audit_index[key]
        if source.get('local_copy',{}).get('path')==path:return source.get('source_identity',source.get('url'))
        stack=list(source.get('records',[]))
        while stack:
            item=stack.pop()
            if not isinstance(item,dict):continue
            lc=item.get('local_copy')
            if isinstance(lc,dict) and lc.get('path')==path:
                return item.get('source_identity',source.get('source_identity',source.get('url')))
            stack.extend(v for v in item.values() if isinstance(v,(dict,list)))
        return source.get('source_identity',source.get('url'))
    for k in required:
        if k not in integrated: raise ValueError('Missing carried primary audit: '+k)
        verify_bindings(integrated[k])
    for name,items in refs.items():
        package_sources[name]=[]
        for key,path,anchor,claim in items:
            package_sources[name].append(dict(source_identity=upstream_identity(key,path),
                version_date=audit_index[key].get('version_date',audit_index[key].get('version_status')),
                local_copy=ref(ROOT/path,anchor),inspected_anchors=[anchor],supported_claims=[claim],
                source_audit_record=ref(BASE/'primary-review.json','Pinned source identity and version record for '+key)))
    return dict(status='pass_for_bounded_source_decisions',cutoff='2026-10-07',
      reviewed_packages=package_sources,
      package_audit_records=[integrated[k] for k in required],
      decisions=route_ledger()['decisions'],
      findings=['Exact source-version and endpoint semantics inform only named profiles.',
                'R wrappers over C++ are not assumed to provide a standalone C++ API.',
                'Direct requirements, root license declarations and compiler targets are not complete resolved deployment inventories.',
                'Temporal lag-by-row is admitted only where physical/subject clock matches; stacked-account example must refuse.',
                'No upstream installation, cross-language runtime, prototype or bank trial was executed.'],
      evidence=[ref(BASE/'primary-review.json','Eight initial inspected source excerpts; superseded by this completed bounded review'),
               ref(BASE/'plan.md','Reviewed S9 plan'),ref(Path(__file__),'Exact package inventory and route review')],
      limitations=route_ledger()['limitations'])


def prepare():
    assert not PUB.exists() and not DRIVER.exists() and not PDF.exists()
    assert not CONTRACT_CHAPTER.exists()
    CONTRACT_CHAPTER.parent.mkdir(parents=True, exist_ok=True)
    CONTRACT_CHAPTER.write_text(CHAPTER.read_text())
    PUB.mkdir(parents=True)
    value=exact_extension();write(BASE/'semantic-results.json',value)
    assert references.calculate()==read(BASE/'exact-results.json')
    assert references.separate(read(BASE/'exact-results.json'))['status']=='pass'
    decisions=route_ledger();write(BASE/'route-decisions.json',decisions)
    protocol=admission_protocol();write(BASE/'admission-protocol.json',protocol)
    source_review=complete_source_review();write(BASE/'completed-source-review.json',source_review)
    limits=['Author review only; no independent or institutional acceptance.',
            'No package was installed or executed; no bridge or port is built.',
            'Direct/transitive dependency, rights, platform and bank-truth inputs remain incomplete.',
            'Finite examples are authored references, not upstream benchmark or calibration.',
            'Literature cutoff 2026-10-07; acquired copies after cutoff establish pinned bytes, not later historical vendor state.',
            'Visual acceptance remains false under the exhausted image allowance.']
    new=[
      dict(integrated_citation_key='exec17_s9_route_decisions',title='Source-bounded R, Python, Java and C++ reuse/port decisions',author='Causal banking proposal',kind='project_design',year=2026,
        source_identity='Project-authored package route ledger, bounded by pinned primary source inspections',version_date='2026-10-17; literature cutoff 2026-10-07',
        local_copy=ref(BASE/'route-decisions.json','Seven package and architecture route decisions'),
        inspected_anchors=['R-pcalg','R-rCausalMGM','R-C++-MIIC','Python-CausalML','Java-Tetrad','C++-aGrUM','Universal-rewrite'],
        supported_claims=['Proposes native-language reuse for named profiles and a measured-need condition for ports.',
                          'Separates Rcpp-wrapped C++ sources from a standalone native-library claim.',
                          'Does not claim package runtime, rights clearance or bank qualification.'],
        records=[ref(BASE/'completed-source-review.json','Hash-bound package source and bounded route review'),ref(BASE/'plan.md','Reviewed scope')],limitations=limits),
      dict(integrated_citation_key='exec17_s9_bank_oracle',title='Exact finite bank-contrast and representation counterexamples',author='Causal banking proposal',kind='project_derivation',year=2026,
        source_identity='Authored Rademacher shared-fit law, finite endpoint encoding count and ordered-panel counterexample',version_date='2026-10-17',
        local_copy=ref(BASE/'semantic-results.json','Exact finite references; upstream_execution=false'),
        inspected_anchors=['inherited_exact_references.shared_control','inherited_exact_references.split_control','graph_mark_enumeration','panel_clock_counterexample'],
        supported_claims=['The stipulated shared-control contrast variance is2 while independently refitted controls give4; positive contrast probabilities are1/4 and5/16.',
                          'Nine endpoint mark pairs collapse to four arrow-presence signatures in the authored lossy map.',
                          'A one-row lag over rows A:t1,A:t2,B:t1,B:t2 includes one cross-subject pair.'],
        records=[ref(ROOT/'tools/s9_port_references_20261017.py','Original exact shared-control and row/cluster enumeration'),ref(Path(__file__),'Independent graph encoding and panel-clock calculation')],limitations=limits),
      dict(integrated_citation_key='exec17_s9_admission',title='Prospective cross-language worker admission contract',author='Causal banking proposal',kind='project_design',year=2026,
        source_identity='Project-authored request/response contract and five-level conformance protocol',version_date='2026-10-17',
        local_copy=ref(BASE/'admission-protocol.json','Request, response, refusal and staged admission criteria'),
        inspected_anchors=['request_fields','response_fields','gates','limitations'],
        supported_claims=['Scientific target, observation clock, sampling unit and randomness identity are explicit transport fields.',
                          'Representation, numerical, stochastic and operational tests are separate conformance levels.',
                          'Protocol remains prospective and no worker passes by appearing in the chapter.'],
        records=[ref(BASE/'completed-source-review.json','Bounded original-source review'),ref(BASE/'plan.md','Reviewed S9 scope')],limitations=limits)]
    write(BASE/'source-audit.json',dict(sources=new,cutoff='2026-10-07',prior=ref(PRIOR,'Preserved726 audited source records')))
    bib=[]
    for s in new:
        bib.append('@misc{'+s['integrated_citation_key']+',\n author={{Causal banking proposal}},\n title={'+s['title']+'},\n year={2026},\n note={Project-authored; see bound audit record}\n}\n')
    (PUB/'refs.bib').write_text('\n'.join(bib))
    (PUB/'source-audit.json').write_text(json.dumps({'sources':new,'cutoff':'2026-10-07','prior':ref(PRIOR,'Preserved726 audited source records')},indent=2)+'\n')
    prior=read(PRIOR); index={s['integrated_citation_key']:s for s in prior['sources']}
    cited={k.strip() for g in re.findall(r'\\cite\w*\*?(?:\[[^\]]*\])*\{([^}]+)\}',CHAPTER.read_text()) for k in g.split(',')}
    assert cited <= set(index)|NEW_KEYS, sorted(cited-(set(index)|NEW_KEYS))
    assert NEW_KEYS==cited-set(index)
    old=OLD.read_text();marker=r'\input{program/execution/2026-10-17/s8/publication-v3/chapter.tex}'
    assert old.count(marker)==1
    driver=old.replace(marker,marker+'\n'+INSERT)
    driver=re.sub(r'\\bibliography\{([^}]+)\}',lambda m:r'\bibliography{'+m.group(1)+',program/execution/2026-10-17/s9/publication-v1/refs}',driver)
    DRIVER.write_text(driver)
    write(PUB/'prepared-inputs.json',dict(inputs=[ref(OLD,'Canonical S8 v3 preserving reader driver'),ref(PRIOR,'726-record canonical source audit'),
        ref(CHAPTER,'Expanded S9 chapter'),ref(CONTRACT_CHAPTER,'Contracted TEXT.DRAFT.S9 logical output'),ref(BASE/'plan.md','Reviewed execution plan'),ref(BASE/'primary-review.json','Initial eight excerpt review'),
        ref(BASE/'completed-source-review.json','Completed package decisions and audit'),ref(BASE/'route-decisions.json','Route ledger'),
        ref(BASE/'semantic-results.json','Finite authored references'),ref(BASE/'admission-protocol.json','Prospective conformance contract'),
        ref(BASE/'source-audit.json','Three new project records'),ref(Path(__file__),'Preserving build/preparation script')],
        generated=[ref(DRIVER,'Preserving S9 successor'),ref(PUB/'refs.bib','Three project references')],
        transform='Insert one S9 chapter after S8 and append a bibliography namespace; predecessor manuscript and records remain preserved.',
        expected_prior_records=726,added_records=3,visual_acceptance=False))
    engine.BASE=PUB;engine.OUT=OUT;engine.OLD=OLD;engine.NAME=NAME;engine.DRIVER=DRIVER;engine.PDF=PDF;engine.PRIOR_AUDIT=PRIOR
    print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)),added_records=3,expected_total=729),indent=2))


def build():
    assert PUB.is_dir() and not OUT.exists() and not PDF.exists()
    verify_bindings(read(PUB/'prepared-inputs.json'))
    engine.BASE=PUB;engine.OUT=OUT;engine.OLD=OLD;engine.NAME=NAME;engine.DRIVER=DRIVER;engine.PDF=PDF;engine.PRIOR_AUDIT=PRIOR
    engine.build()
    report=read(OUT/'build-report.json')
    assert report['cited_records']==729 and report['pages']>998
    assert not [x for x in report['warnings'] if 'Underfull' not in x]
    idx=trace.audit(DRIVER,OUT/'source-audit.json')
    write(PUB/'traceability-review.json',idx)
    assert idx['status']=='pass' and not idx['issues'] and idx['scholarly_pdfs']==188
    reader=(OUT/'reader.txt').read_text()
    assert 'Reusing causal software across languages without changing the question' in reader
    for n in range(1,4): assert f'({26}.{n})' in reader or f'({27}.{n})' in reader or f'({28}.{n})' in reader
    build_contract=dict(status='pass',reviewer={'name':'Codex author/coordinator','kind':'author'},reader=report['pdf'],
        pages=report['pages'],cited_records=report['cited_records'],prior_records_preserved=726,new_project_records=3,
        exact_equations='Compiled S9 equation labels and all-page text bounds checked by builder.',
        scholarly_pdfs=idx['scholarly_pdfs'],material_warnings=[],visual_acceptance=False,
        limitations=read(BASE/'completed-source-review.json')['limitations'])
    write(PUB/'build-review.json',build_contract)
    print(json.dumps({k:report[k] for k in ['pages','cited_records','warnings','added_sections']},indent=2))


def main():
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','build'])
    a=p.parse_args();{'prepare':prepare,'build':build}[a.command]()


if __name__=='__main__':main()

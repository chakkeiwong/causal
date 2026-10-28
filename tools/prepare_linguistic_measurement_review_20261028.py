"""Retain genuine original, precise source anchors and independently checked argument."""
import hashlib
import json
from pathlib import Path
import linguistic_measurement_reference_20261028 as exact
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings
ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-28/linguistic-measurement-v1'
CHAIN = ROOT / 'docs/program/execution/2026-10-28/longitudinal-backward-chain-v1'
RUNTIME = ROOT / 'docs/program/execution/2026-10-25/runtime-artifact-gaps-v1'
RAW = ROOT / 'docs/literature/raw'
read = lambda p: json.loads(p.read_text())


def main():
    assert BASE.is_dir() and not (BASE / 'source-audit.json').exists()
    for p in [CHAIN / 'metadata-review.json', RUNTIME / 'review.json']:
        verify_bindings(read(p))
    pdf = RAW / 'exec28_lbc_pryzant_v1.pdf'
    receipt = read(RAW / 'exec28_lbc_pryzant_v1.receipt.json')
    assert receipt['status'] == 'saved' and receipt['sha256'] == hashlib.sha256(pdf.read_bytes()).hexdigest()
    assert receipt['sha256'] == '88b0109a76b5fd36bc0260075e74d9c27492b55c0fa550f75d7b82ef5ad59072'
    named = ROOT / 'docs/papers/Causal Effects of Linguistic Properties Pryzant(2020).pdf'
    assert not named.exists()
    named.write_bytes(pdf.read_bytes())
    pages = (CHAIN / 'pryzant-v1.txt').read_text().split(chr(12))
    assert len(pages) == 14 and '24 Oct 2020' in pages[0]
    assert 'sign is homogeneous' in pages[3] and 'Theorem 4.' in pages[10]
    anchors = []
    (BASE / 'inspected').mkdir()
    findings = {1:'Title, five authors and arXiv v1 first-page date.',
                2:'Separate writer intent, reader perception, proxy label and text.',
                3:'Theorem 1 backdoor and intent/perception agreement; conditional proxy errors in Theorem 2.',
                4:'Explicit better-than-chance and homogeneous-effect-sign qualifications; text adjustment.',
                5:'Text representation and semi-synthetic evaluation construction.',
                6:'Semi-synthetic sensitivity and observational CFPB design introduction.',
                7:'CFPB response threshold, outcome matching, selected extremes, 4000 complaints and estimates.',
                11:'Appendix A outcome-sufficient component, overlap and consistent regression assumptions.'}
    for page, finding in findings.items():
        path = BASE / 'inspected' / f'pryzant-page-{page}.txt'
        path.write_text(pages[page-1])
        anchors.append(dict(pdf_page=page, finding=finding, extract=ref(path,'Inspected physical-page extracted primary text')))
    paper = dict(integrated_citation_key='exec28_lm_pryzant',kind='paper',
        title='Causal Effects of Linguistic Properties',filename_title='Causal Effects of Linguistic Properties',
        first_author='Pryzant',author='Reid Pryzant and Dallas Card and Dan Jurafsky and Victor Veitch and Dhanya Sridhar',
        year=2020,pages=13,source_identity='https://arxiv.org/abs/2010.12919v1',
        version_date='arXiv:2010.12919v1; first-page 24 October 2020; retained PDF metadata creation 27 August 2021',
        accessed_utc=receipt['accessed_utc'],cutoff='2026-10-07',
        cutoff_basis='First-page preprint stamp and archive history predate cutoff; exact historic byte identity and conference equivalence are not asserted.',
        local_path=str(named.relative_to(ROOT)),sha256=receipt['sha256'],
        local_copy=ref(pdf,'Authentic fetched preprint; identical to named scholarly PDF'),
        acquisition_receipt=ref(RAW/'exec28_lbc_pryzant_v1.receipt.json','Fixed-collector acquisition'),
        identity_page=ref(RAW/'exec28_lbc_pryzant_identity.html','Archive version history'),
        identity_receipt=ref(RAW/'exec28_lbc_pryzant_identity.receipt.json','Archive retrieval'),
        extracted_text=ref(CHAIN/'pryzant-v1.txt','Primary text; not substitute for original'),
        inspected_anchors=anchors,supported_claims=list(findings.values()),
        limits='Selected preprint inspected; theorem notation mixes perception/proxy symbols. No corrected theorem, conference equivalence, native TextCause reproduction or bank truth inferred.',
        execution='literature_inspection_only_no_local_replication')
    artifacts = dict(integrated_citation_key='exec28_lm_artifacts',kind='software_primary_sources',
        title='Pinned LLM-CD, LLM-and-SCD and LCM component and model-artifact inspection',
        author='tyMadara, mas-takayama and kougioulis contributors',year=2026,
        source_identity='https://github.com/tyMadara/LLM-CD ; https://github.com/mas-takayama/LLM-and-SCD ; https://github.com/kougioulis/LCM',
        version_date='Pinned commits 8ea28948affdab88bee91a8b7858e89dc9424ffe; 5aaeaea89e71e2cff443289e473c06d2f79172c5; b6d386913bb63e16b79439204ce06fd215baafd6; all before client cutoff',
        local_copy=ref(RUNTIME/'primary-source-records.json','Exact source bytes, commit identities, retrieval receipts and full-tree inventories'),
        inspected_anchors=['Complete tree root/component notice paths','Pinned requirements and project manifest','LCM named weights and loader failure branches'],
        supported_claims=['No root notices in two specific pinned trees; nested notice has component scope.',
                          'LCM code notice is distinct from exact externally linked model bytes, provenance and terms.',
                          'Loader returns None on missing/exceptional loads and sets weights_only=False; static inspection only.'],
        evidence=[ref(RUNTIME/'review.json','Completed source review'),ref(RUNTIME/'remaining-artifact-register.json','Component-specific unresolved items')],
        records=read(RUNTIME/'primary-source-records.json'),limitations=['No legal clearance, execution or native integration claimed.'])
    write(BASE/'exact-results.json',exact.calculate())
    project = dict(integrated_citation_key='exec28_lm_reference',kind='project_evidence_not_scholarly_paper',
        title='Exact heterogeneous linguistic-measurement witness',author='Causal banking proposal project',year=2026,
        source_identity='tools/linguistic_measurement_reference_20261028.py',version_date='28 October 2026; exact rational enumeration and independent conditional-mean algebra',
        local_copy=ref(Path(exact.__file__),'Independently authored finite model'),
        inspected_anchors=['calculate: full joint enumeration and stratum conditional means','Algebra equality and exact expected outcomes'],
        supported_claims=['77.5 percent proxy accuracy coexists with true effect USD5 and proxy contrast minus USD4 when stratum effects have opposite signs.'],
        evidence=[ref(BASE/'exact-results.json','Exact fractions, cells and assertions')],
        limitations=['Stochastic-proxy model with adjustment strata; not the deterministic full-text setting, source theorem refutation, empirical TextCause failure or bank evidence.'])
    write(BASE/'source-audit.json',dict(sources=[paper,artifacts,project],cutoff='2026-10-07',visual_acceptance=False))
    write(BASE/'omissions-register.json',dict(omissions=read(CHAIN/'metadata-review.json')['omissions'],
        evidence=[ref(CHAIN/'metadata-review.json','Bounded metadata-only routes')],
        source_search_complete=False,remaining_census_originals=31,conference_equivalence=False))
    write(BASE/'plan-review.json',dict(status='pass',scope='Connected linguistic measurement, sequential policy translation and artifact-specific adoption argument',
        evidence=[ref(BASE/'development.tex','Reviewed planned manuscript'),ref(BASE/'source-audit.json','Primary claims'),ref(BASE/'omissions-register.json','Unadmitted originals'),ref(Path(__file__),'Source retention and checks')],
        checks=['Preserve every predecessor source, citation context and content input.',
                'Retain source homogeneous-sign qualifier; do not label project witness a counterexample to its conditional result.',
                'Separate writer intent, perception, proxy and executable editing policy; chronological and support assumptions remain explicit.',
                'Treat exact enumeration as stipulated economics, not empirical calibration or performance.',
                'Keep three runtime artifact inventories distinct from scientific source access and global blockers.',
                'Compile paired documents, verify sources/arithmetic/all-page text, refresh exact-reader reviews and canonical continuation.',
                'Preserve failures, run both full controllers, audit staged custody, commit/push and consume exit before next publication.'],
        reviewed_risks=['Preprint/version metadata discrepancy disclosed.','No deterministic-proxy positivity theorem inferred.','No new census row closed by an adjacent backward reference.','Visual allowance remains exhausted.'],
        final_acceptance=False))
    write(BASE/'mathematical-review.json',dict(status='pass_for_scoped_project_argument',issues=[],
        evidence=[ref(Path(exact.__file__),'Exact model'),ref(BASE/'exact-results.json','Enumerated output'),ref(BASE/'development.tex','Assumptions and independent derivation')],
        findings=['Eight joint cells normalize exactly; each stratum has proxy support one half.',
                  'Enumeration and separate algebra agree on contrasts2,-10; trueATE5,proxyATE-4,accuracy31/40.',
                  'Source sign-preservation requires its explicit conditional assumptions; heterogeneous-sign witness does not meet them.',
                  'Sequential g-formula is an assumed finite-history design under consistency, sequential exchangeability, support and fixed policy; no universal semantic theorem.'],
        native_execution=False,empirical_coverage=False))
    write(BASE/'copyedit-review.json',dict(status='pass',evidence=[ref(BASE/'development.tex','Connected product narrative'),ref(BASE/'sponsor-addition.md','Sponsor implications')],
        findings=['Notation and intervention timing explicit.','Negative proxy sign is qualified as an authored measurement example.','Source omissions and process records kept outside product narrative.','Public-data prototype costs remain to be measured.'],rendered_review=False))
    write(BASE/'review.json',dict(status='pass_for_primary_review_and_authored_argument',
        evidence=[ref(BASE/n,'Reviewed evidence') for n in ['plan-review.json','source-audit.json','mathematical-review.json','copyedit-review.json','omissions-register.json','exact-results.json']],
        new_scholarly_originals=1,census_dispositions_changed=0,native_admission=False,visual_acceptance=False,final_acceptance=False))
    verify_bindings(read(BASE/'review.json'))
    print(json.dumps(dict(review='pass',new_sources=3,new_scholarly_pdfs=1,census_dispositions_changed=0)))


if __name__ == '__main__':
    main()

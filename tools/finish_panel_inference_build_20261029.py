"""Resume completed compilation after a stale expected-label assertion."""
import hashlib,json,re,subprocess
from pathlib import Path
import build_panel_inference_reader_20261029 as build
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write


def main():
    build.configure();engine=build.engine
    BASE,OUT,ROOT=build.BASE,build.OUT,build.ROOT
    failed=ROOT/'docs/program/execution/2026-10-29/panel-inference-publication-v1/reader-build-exit.json'
    receipt=json.loads(failed.read_text());verify_bindings(receipt);assert receipt['actual_exit_code']==1
    log=(OUT/(build.NAME+'.log')).read_text(errors='replace')
    for token in ['undefined citations','undefined references','multiply defined','Missing character','Overfull','Label(s) may have changed','Rerun to get']:
        assert token not in log,token
    assert build.PDF.read_bytes()==(OUT/(build.NAME+'.pdf')).read_bytes()
    before=hashlib.sha256(build.PDF.read_bytes()).hexdigest()
    prepared=json.loads((BASE/'prepared-inputs.json').read_text());verify_bindings(prepared)
    assert build.DRIVER.read_text()==build.expected_driver()
    assert build.exact.calculate()==json.loads((BASE/'exact-results.json').read_text())
    audit=json.loads((OUT/'source-audit.json').read_text());verify_bindings(audit)
    files=engine.shared.scan(build.DRIVER);joined='\n'.join(t for _,t in files)
    labels=re.findall(engine.shared.LABEL,joined);assert len(labels)==len(set(labels))
    cited={k.strip() for g in re.findall(engine.shared.CITE,joined) for k in g.split(',')}
    assert cited==engine.sources().keys() and len(cited)==1451
    label='sec:exec29-panel-inference-contracts'
    aux=(OUT/(build.NAME+'.aux')).read_text()
    match=re.search(r'\\newlabel\{'+re.escape(label)+r'\}\{\{([^}]+)\}\{(\d+)\}',aux);assert match
    pages=int(re.search(r'(?m)^Pages:\s+(\d+)',subprocess.check_output(['pdfinfo',str(build.PDF)],text=True,timeout=15)).group(1))
    write(BASE/'build-repair.json',dict(status='performed',cause='Successor expected exec28 label but manuscript has correct exec29 label.',
        repair='Verify actual compiled label and finish reports without modifying or recompiling preserved source or PDF.',
        evidence=[ref(failed,'Observed failure'),ref(Path(__file__),'Performed repair'),ref(OUT/(build.NAME+'.aux'),'Actual compiled label')],pdf_unchanged_sha256=before))
    write(OUT/'build-report.json',dict(status='compiled_source_and_text_checked_working_draft',pages=pages,pdf=ref(build.PDF,'Panel inference working successor'),
        driver=ref(build.DRIVER,'Preserving driver'),builder=ref(Path(__file__),'Post-compilation completion'),predecessor_pdf=ref(build.OLD.with_suffix('.pdf'),'Preserved predecessor'),
        source_audit=ref(OUT/'source-audit.json','1451 audited records'),cited_records=1451,added_anchors={label:dict(number=match.group(1),printed_page=int(match.group(2)))},
        warnings=[line for line in log.splitlines() if any(t in line for t in ['Warning','Overfull','Underfull','Missing character'])],
        repair=ref(BASE/'build-repair.json','Preserved failure and corrected expected label'),final_acceptance=False,mandatory_repairs_closed=[],visual_acceptance=False,
        visual_review='Pending fresh image allowance; inherited allowance exhausted'))
    engine.layout.OUT=OUT;engine.layout.main()
    assert json.loads((OUT/'text-layout-review.json').read_text())['status']=='pass'
    index=engine.trace.audit(build.DRIVER,OUT/'source-audit.json');write(BASE/'traceability-review.json',index)
    assert index['status']=='pass' and not index['issues'] and index['scholarly_pdfs']==277
    assert hashlib.sha256(build.PDF.read_bytes()).hexdigest()==before
    print(json.dumps(dict(pages=pages,records=1451,scholarly_pdfs=277,repair='pass',recompiled=False)))


if __name__=='__main__':main()

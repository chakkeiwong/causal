#!/usr/bin/env python3
"""Preflight the exact publication plan without mutating canonical state."""
import ast,json,re,tempfile
from pathlib import Path
import build_data_workflow_wave_sponsor_20261025 as previous
import build_agent_evaluation_surveys_sponsor_20261025 as current
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-25/agent-evaluation-surveys-v1'
SOURCE=BASE.parent/'census-observation-workflow-v1'
read=lambda p:json.loads(p.read_text())

def main():
    assert not BASE.exists();BASE.mkdir()
    prior_text=previous.manuscript(1716)
    with tempfile.TemporaryDirectory(prefix='survey-sponsor-preflight-') as directory:
        temporary=Path(directory);(temporary/'proposal.md').write_text(prior_text)
        original=current.PRIOR;current.PRIOR=temporary
        try:text=current.manuscript(1719)
        finally:current.PRIOR=original
    cite=lambda t:{k.strip() for g in re.findall(current.engine.shared.CITE,t) for k in g.split(',')}
    old,new=cite(prior_text),cite(text)
    assert len(old)==1026 and len(new)==1031 and old<=new
    assert new-old=={'exec25_cow_chemistry','exec25_cow_vulnerability','exec25_cow_reference','sp25aes_reader','sp25aes_progress'}
    for token in ['1,719 pages','1390 audited citation records','267 genuine scholarly PDFs','350 recorded outcomes','98 inconclusive and 1 open cells','82 inspected','31 unread']:
        assert token in text,token
    (BASE/'expected-sponsor.md').write_text(text)
    preflight=dict(status='pass_for_preserving_manuscript',prior_records=1026,expected_records=1031,expected_monograph_pages=1719,expected_papers=267,evidence=[ref(BASE/'expected-sponsor.md','Expected complete sponsor'),ref(current.READER_BASE/'release-source-review.json','1390-record preserving reader'),ref(Path(current.__file__),'Exact sponsor builder')],limitations=['Actual sponsor rendering and canonical snapshot are checked during publication.','Related preprints do not close distinct original-source obligations.'])
    verify_bindings(preflight);write(BASE/'sponsor-preflight.json',preflight)
    stems=['reconcile_agent_evaluation_surveys','execute_agent_evaluation_surveys_publication','deliver_agent_evaluation_surveys_publication','build_agent_evaluation_surveys_sponsor','publish_agent_evaluation_surveys_sponsor','refresh_agent_evaluation_surveys_program','build_agent_evaluation_surveys_reader_v2','publish_agent_evaluation_surveys_reader_v2','run_with_verified_hash_cache']
    scripts=[ROOT/'tools'/(n+'_20261025.py') for n in stems]+[Path(__file__)]
    for p in scripts:ast.parse(p.read_text())
    evidence=[ref(p,'Reviewed serial script') for p in scripts]+[ref(BASE/'sponsor-preflight.json','Exact citation and manuscript preflight'),ref(SOURCE/'review.json','Audited genuine source and project examples'),ref(SOURCE/'layout-repair.json','Preserved failed layout and whitespace-only successor'),ref(ROOT/'docs/program/execution/2026-10-25/hash-cache-repair-v1/review.json','First-read bytes and metadata-checked process-local reuse')]
    plan=dict(status='pass_for_serial_publication_after_consumed_predecessor',reviewer=dict(name='Codex author/coordinator',kind='author'),evidence=evidence,
        steps=['Consume data-workflow delivery exit and verify HEAD/origin before canonical changes.','Publish reviewed 1719-page reader preserving1387 records,all contexts and408content inputs.','Save LL.CENSUS start/yield with82/31 unchanged and four crosscutting tasks.','Build and review exact paired sponsor1031records;renew Q2-Q4 for exact bytes.','Reconcile all376 obligations;run both unmodified full controller checks.','Commit,push,consume delivery and continue benchmark-oracle work.'],
        expected=dict(recorded=350,operations=376,nonpassing=150,software=dict(pass_count=3,inconclusive=98,open=1),census=dict(inspected=82,unread=31,crosscutting=4),reader_citations=1390,scholarly_pdfs=267,sponsor_citations=1031),
        checks=['Canonical phases serialize; predecessor success is checked explicitly.','Process-local cache rehashes changed identities; final controllers are not patched.','No blanket operation closure from source acquisition or page counts.','Source-route denials and failed layout remain immutable.','Scoped staging recursively checks local evidence custody.','Visual,independent,native,bank and final acceptance remain open.'],
        global_blocker=None,phase_boundaries_are_stopping_points=False)
    verify_bindings(plan);write(BASE/'publication-plan-review.json',plan)
    print(json.dumps(dict(plan='reviewed',sponsor_records=1031,reader_pages=1719,original_obligations_closed=0)))

if __name__=='__main__':main()

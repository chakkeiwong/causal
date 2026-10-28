#!/usr/bin/env python3
"""Bind reviewed scripts and exact sponsor preflight before canonical changes."""
import ast,json,re,tempfile
from pathlib import Path
import build_benchmark_oracles_sponsor_20261025 as sponsor
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-25/benchmark-oracles-v1'
read=lambda p:json.loads(p.read_text())

def main():
    assert not (BASE/'publication-plan-review.json').exists()
    previous=BASE.parent/'agent-evaluation-surveys-v1/expected-sponsor.md'
    with tempfile.TemporaryDirectory(prefix='benchmark-sponsor-preflight-') as directory:
        temporary=Path(directory);(temporary/'proposal.md').write_bytes(previous.read_bytes())
        original=sponsor.PRIOR;sponsor.PRIOR=temporary
        try:text=sponsor.manuscript(1723)
        finally:sponsor.PRIOR=original
    cite=lambda t:{k.strip() for g in re.findall(sponsor.engine.shared.CITE,t) for k in g.split(',')}
    old,new=cite(previous.read_text()),cite(text)
    assert len(old)==1031 and len(new)==1035 and old<=new
    assert new-old=={'exec25_bor_sources','exec25_bor_reference','sp25bor_reader','sp25bor_progress'}
    for token in ['1,723 pages','1392 audited citation records','267 genuine scholarly PDFs','350 recorded outcomes','98 inconclusive and 1 open cells','82 inspected','31 unread']:
        assert token in text,token
    (BASE/'expected-sponsor.md').write_text(text)
    preflight=dict(status='pass_for_preserving_manuscript',prior_records=1031,expected_records=1035,expected_monograph_pages=1723,expected_papers=267,evidence=[ref(BASE/'expected-sponsor.md','Complete expected sponsor'),ref(sponsor.READER_BASE/'release-source-review.json','1392-record preserving reader'),ref(Path(sponsor.__file__),'Exact preserving builder')],limitations=['Actual sponsor render and canonical snapshot are checked during publication.','Native and independent benchmark qualification remain open.'])
    verify_bindings(preflight);write(BASE/'sponsor-preflight.json',preflight)
    stems=['reconcile_benchmark_oracles','execute_benchmark_oracles_publication','deliver_benchmark_oracles_publication','build_benchmark_oracles_sponsor','publish_benchmark_oracles_sponsor','refresh_benchmark_oracles_program','build_benchmark_oracles_reader','publish_benchmark_oracles_reader','run_with_verified_hash_cache']
    scripts=[ROOT/'tools'/(n+'_20261025.py') for n in stems]+[Path(__file__)]
    for p in scripts:ast.parse(p.read_text())
    evidence=[ref(p,'Reviewed serial script') for p in scripts]+[ref(BASE/'sponsor-preflight.json','Complete manuscript and citation preflight'),ref(BASE/'review.json','Pinned source and independent witness audit'),ref(BASE/'qualification-design.json','Native qualification criteria'),ref(BASE/'generator-repair.json','Preserved generation failure and corrected successor'),ref(ROOT/'docs/program/execution/2026-10-25/hash-cache-repair-v1/review.json','Validated first-byte-read process-local hashing')]
    plan=dict(status='pass_for_serial_publication_after_consumed_predecessor',reviewer=dict(name='Codex author/coordinator',kind='author'),evidence=evidence,
        steps=['Consume and verify agent-survey publication delivery.','Publish1723-page preserving reader;1390previous records and409compiled inputs unchanged.','Record durable census progress without closing native or original-source obligations.','Build paired1035-record sponsor and renew exact-byte Q2-Q4.','Reconcile376obligations and run both unmodified full controllers.','Commit,push,consume delivery and continue independent runtime-rights review.'],
        expected=dict(recorded=350,operations=376,nonpassing=150,software=dict(pass_count=3,inconclusive=98,open=1),census=dict(inspected=82,unread=31,crosscutting=4),reader_citations=1392,scholarly_pdfs=267,sponsor_citations=1035),
        checks=['No canonical mutations overlap predecessor publication.','Scientific witnesses are independent code and not native benchmark results.','Full generator and parser paths remain unqualified.','Source records and citation contexts are preserved exactly.','Source and financial/arithmetic examples are traceable and reproducible.','Final controller checks do not use the hash-cache wrapper.','No page,count or inconclusive-outcome completion inference.','Scoped staging checks all bound local evidence; visual and final acceptance stay open.'],global_blocker=None,phase_boundaries_are_stopping_points=False)
    verify_bindings(plan);write(BASE/'publication-plan-review.json',plan)
    print(json.dumps(dict(plan='reviewed',sponsor_records=1035,reader_pages=1723,native_qualification=False)))

if __name__=='__main__':main()

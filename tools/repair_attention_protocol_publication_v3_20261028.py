"""Preserve the failed edition and prepare a citation-consistent successor."""
import ast
import json
import re
from pathlib import Path

from prepare_followup_program_20261028 import ROOT, ref, write
from publish_latent_r_review_v2_20261013 import verify_bindings

DAY = ROOT / 'docs/program/execution/2026-10-28'
TOOLS = ROOT / 'tools'
SOURCE = DAY / 'attention-protocol-review-v4'
DEST = DAY / 'attention-protocol-review-v5'
FAILED = DAY / 'attention-protocol-reader-v1'


def replace_once(text, old, new):
    assert text.count(old) == 1, (old, text.count(old))
    return text.replace(old, new)


def script(old, new, changes):
    text = (TOOLS / old).read_text()
    for before, after in changes:
        assert before in text, before
        text = text.replace(before, after)
    ast.parse(text)
    path = TOOLS / new
    assert not path.exists(), path
    path.write_text(text)
    return path


def main():
    assert not DEST.exists()
    failure = FAILED / 'reader'
    logs = sorted(failure.glob('*.log')) + sorted(failure.glob('*.blg'))
    assert logs and 'exec28_at_contract_fixture' in (failure / 'bibtex-pass.log').read_text()
    write(FAILED / 'build-failure.json', dict(
        status='failed_attempt_preserved',
        failure='The source text cited exec28_at_contract_fixture, an unregistered alias. The registered exec28_at_protocol_reference already audits the public fixture and exact derivations.',
        effect='No publication or canonical reader changed. All failed-edition logs and generated files remain in place.',
        evidence=[ref(p, 'Observed failed build') for p in logs],
        additional_preflight_findings=[
            'The generated reader verifier expected exec28_ap_* instead of the audited exec28_at_* keys.',
            'The source lacked the generated verifier opening and closing anchors.',
            'The sponsor builder incorrectly expected the new citation count in the predecessor and duplicated old pairing citations.',
            'The sponsor verifier expected both previously inherited sources and a wrong new prefix in its addition set.',
            'Several inherited review findings described the previous attention supplement instead of this protocol delta.',
        ],
        next_action='Prepare a new source package, reader, sponsor and review scripts; preflight actual citations before compiling.'))

    DEST.mkdir()
    for name in ['source-audit.json', 'exact-results.json', 'protocol-exact-results.json', 'mathematical-review.json']:
        (DEST / name).write_bytes((SOURCE / name).read_bytes())
    text = (SOURCE / 'development.tex').read_text()
    text = replace_once(text, r'\citep{exec28_at_protocol_reference,exec28_at_contract_fixture}', r'\citep{exec28_at_protocol_reference}')
    text = replace_once(text,
        'The primary method description and the code path are different evidence. This supplement traces\n'
        'the selected temporal and event-discovery delegates far enough to state what their current\n'
        'proposal can compare, and what a public qualification would have to measure.',
        'A precise temporal/evaluation contract keeps a predictive graph separate from banking intervention evidence.\n'
        'The primary method description and the code path are different evidence. Tracing the selected\n'
        'temporal and event-discovery delegates determines which predictions are comparable and what\n'
        'a public qualification must measure.')
    text += '\nA temporal discovery result is admissible only when its observation window, graph truth access and failure denominator are explicit.\n'
    (DEST / 'development.tex').write_text(text)
    sponsor = (SOURCE / 'sponsor-addition.md').read_text().replace('exec28_at_contract_fixture', 'exec28_at_protocol_reference')
    (DEST / 'sponsor-addition.md').write_text(sponsor)
    write(DEST / 'copyedit-review.json', dict(status='pass',
        evidence=[ref(DEST / n, 'Corrected connected argument') for n in ['development.tex', 'sponsor-addition.md']],
        findings=['The public fixture uses its registered project reference; no new source or unsupported claim is introduced.',
                  'Opening and closing statements now delimit the actual protocol argument.',
                  'Source-derived findings, authored fixtures and proposed native experiments remain explicit.']))
    write(DEST / 'plan-review.json', dict(status='pass',
        evidence=[ref(SOURCE / 'review.json', 'Preserved source review'),
                  ref(FAILED / 'build-failure.json', 'Observed failure and full preflight repair')],
        checks=['Preserve all 1430 predecessor reader and 1089 sponsor citation records and prior compiled content.',
                'Add only the three audited exec28_at_* records and the two exact sponsor pairing references.',
                'Verify citations and source keys before compiling; retain all strict source, layout and controller checks.',
                'No native, complete census, full software coverage, visual or final acceptance is awarded.']))
    write(DEST / 'review.json', dict(status='pass', issues=[],
        evidence=[ref(DEST / n, 'Reviewed corrected source package') for n in [
            'source-audit.json', 'exact-results.json', 'protocol-exact-results.json',
            'mathematical-review.json', 'copyedit-review.json', 'plan-review.json',
            'development.tex', 'sponsor-addition.md']],
        native_execution=False, visual_acceptance=False, final_acceptance=False))
    verify_bindings(json.loads((DEST / 'review.json').read_text()))

    created = []
    created.append(script('build_attention_protocol_reader_v4_20261028.py',
        'build_attention_protocol_reader_v5_20261028.py', [
            ('attention-protocol-reader-v1', 'attention-protocol-reader-v2'),
            ('attention-protocol-review-v4', 'attention-protocol-review-v5'),
            ('causal_proposal_attention_protocol_reviewed_v1_2026-10-28', 'causal_proposal_attention_protocol_reviewed_v2_2026-10-28')]))
    created.append(script('publish_attention_protocol_reader_v3_20261028.py',
        'publish_attention_protocol_reader_v4_20261028.py', [
            ('build_attention_protocol_reader_v4_20261028', 'build_attention_protocol_reader_v5_20261028'),
            ("{'exec28_ap_'+k", "{'exec28_at_'+k"),
            ('three additional primary-paper,software and independent-project records', 'three additional software and authored-project records'),
            ('Exact finite witness preserves a marginal while covariance changes1/4to-1/4,predictor loss0to1,and temporal agreement2/3to0; stipulated intervention effect remains0; no native behavior or bank performance claimed.',
             'Prior mathematical arguments are preserved; exact temporal support is lags 0-7 for non-targets and 1-8 for the shifted target, threshold ties differ by comparator, and zero-valid results remain unavailable. These are source-derived and authored fixtures, not native performance.'),
            ('Proposed request contracts distinguish completion,representation,scientific admission,refusal and transport uncertainty,with full attempts and costs; no native capability.',
             'Prior integration contracts are preserved; the public protocol separates training, validation and held-out graph identities, truth access, effective configuration and complete failure denominators. No native adapter is qualified.'),
            ('Attention discovery assumptions,permutation-law qualification,oracle/split/empty-denominator contracts and conditional source reuse; all previous content preserved.',
             'Exact TCDF temporal support and TACD split, truth-access, device and scoring findings; public contract fixtures; all previous content preserved.')]))
    created.append(script('build_attention_protocol_sponsor_v3_20261028.py',
        'build_attention_protocol_sponsor_v4_20261028.py', [
            ('build_attention_protocol_reader_v4_20261028', 'build_attention_protocol_reader_v5_20261028'),
            ('sponsor-attention-protocol-v1', 'sponsor-attention-protocol-v2'),
            ('sponsor_proposal_attention_protocol_reviewed_2026-10-28.pdf', 'sponsor_proposal_attention_protocol_reviewed_v2_2026-10-28.pdf'),
            ("assert text.count('1433 audited citation records')==1", "assert text.count('1430 audited citation records')==1"),
            (".replace('1433 audited citation records','1433 audited citation records')", ".replace('1430 audited citation records','1433 audited citation records')"),
            ("text=text.replace(marker,marker+',sp28at_reader,sp28at_progress')", "text=text.replace(marker,marker+',sp28ap_reader,sp28ap_progress')"),
            ("'1080 preserved identities'", "'1089 preserved identities'"),
            ('citations=1089,paired_pages=pages', 'citations=len(sources),paired_pages=pages')]))
    created.append(script('publish_attention_protocol_sponsor_v3_20261028.py',
        'publish_attention_protocol_sponsor_v4_20261028.py', [
            ('build_attention_protocol_sponsor_v3_20261028', 'build_attention_protocol_sponsor_v4_20261028'),
            ('sponsor-attention-protocol-v1', 'sponsor-attention-protocol-v2'),
            ('attention-protocol-reader-v1', 'attention-protocol-reader-v2'),
            ("{'exec28_at_'+k for k in ['liu','ct','camcns','tacd','tcdf','cdt','reference']}|{'exec28_ap_'+k for k in ['tcdf_temporal','tacd_protocol','protocol_reference']}",
             "{'exec28_at_'+k for k in ['tcdf_temporal','tacd_protocol','protocol_reference']}")]))
    created.append(script('review_attention_protocol_chapters_v3_20261028.py',
        'review_attention_protocol_chapters_v4_20261028.py', [
            ('attention-protocol-reader-v1', 'attention-protocol-reader-v2'),
            ('attention-protocol-chapters-v1', 'attention-protocol-chapters-v2'),
            ('attention_discovery_delta', 'attention_protocol_delta'),
            ('Prior L1/L6 content preserved; one new primary attention discovery preprint and selected source/evaluation findings are added without changing LLM census counts.',
             'Prior L1/L6 content and source identities preserved; exact temporal/evaluation delegates and authored public fixtures add no new LLM scholarly original and do not change census counts.')]))

    import build_attention_protocol_reader_v5_20261028 as build
    build.prepare()
    build.configure()
    entries = build.engine.sources()
    files = build.engine.shared.scan(build.DRIVER)
    cited = {key.strip() for _, content in files for group in re.findall(build.engine.shared.CITE, content) for key in group.split(',')}
    assert cited == entries.keys() and len(cited) == 1433
    assert entries.keys() - {s['integrated_citation_key'] for s in json.loads(build.PRIOR.read_text())['sources']} == {
        'exec28_at_tcdf_temporal', 'exec28_at_tacd_protocol', 'exec28_at_protocol_reference'}
    write(DEST / 'publication-preflight.json', dict(status='pass', cited_records=len(cited),
        preserved_reader_records=1430, expected_sponsor_records=1094,
        evidence=[ref(p, 'Immutable corrected publication successor') for p in created] + [
            ref(build.BASE / 'prepared-inputs.json', 'Prepared successor inputs'),
            ref(FAILED / 'build-failure.json', 'Failed edition preserved')],
        findings=['Actual compiled citation set equals audited source set before LaTeX compilation.',
                  'Only three registered protocol records are new; all inherited identities remain unchanged.',
                  'Sponsor pairing citations are new and all 1089 predecessor citations remain required.']))
    print(json.dumps(dict(preflight='pass', reader_records=1433, expected_sponsor_records=1094)))


if __name__ == '__main__':
    main()

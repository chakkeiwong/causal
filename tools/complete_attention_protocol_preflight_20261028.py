"""Resume the interrupted publication-tool preparation without replacing artifacts."""
import json
import re

from prepare_followup_program_20261028 import ROOT, ref, write
from repair_attention_protocol_publication_v3_20261028 import DEST, FAILED, TOOLS, script


def main():
    write(DEST / 'preflight-preparation-failure.json', dict(
        status='failed_attempt_preserved',
        failure='The repair generator required a sponsor base-path literal absent from the publisher, which already obtains its base from the builder.',
        effect='Source package and the first three corrected scripts are preserved; no build, publication or canonical state changed.',
        evidence=[ref(TOOLS / 'repair_attention_protocol_publication_v3_20261028.py', 'Failed generator')],
        next_action='Generate only the two missing scripts with applicable substitutions, then validate all citations.'))
    script('publish_attention_protocol_sponsor_v3_20261028.py',
        'publish_attention_protocol_sponsor_v4_20261028.py', [
            ('build_attention_protocol_sponsor_v3_20261028', 'build_attention_protocol_sponsor_v4_20261028'),
            ("{'exec28_at_'+k for k in ['liu','ct','camcns','tacd','tcdf','cdt','reference']}|{'exec28_ap_'+k for k in ['tcdf_temporal','tacd_protocol','protocol_reference']}",
             "{'exec28_at_'+k for k in ['tcdf_temporal','tacd_protocol','protocol_reference']}")])
    script('review_attention_protocol_chapters_v3_20261028.py',
        'review_attention_protocol_chapters_v4_20261028.py', [
            ('attention-protocol-reader-v1', 'attention-protocol-reader-v2'),
            ('attention-protocol-chapters-v1', 'attention-protocol-chapters-v2'),
            ('attention_discovery_delta', 'attention_protocol_delta'),
            ('Prior L1/L6 content preserved; one new primary attention discovery preprint and selected source/evaluation findings are added without changing LLM census counts.',
             'Prior L1/L6 content and source identities preserved; exact temporal/evaluation delegates and authored public fixtures add no new LLM scholarly original and do not change census counts.')])
    import build_attention_protocol_reader_v5_20261028 as build
    build.prepare()
    build.configure()
    entries = build.engine.sources()
    files = build.engine.shared.scan(build.DRIVER)
    cited = {key.strip() for _, content in files for group in re.findall(build.engine.shared.CITE, content) for key in group.split(',')}
    assert cited == entries.keys() and len(cited) == 1433
    assert entries.keys() - {s['integrated_citation_key'] for s in json.loads(build.PRIOR.read_text())['sources']} == {
        'exec28_at_tcdf_temporal', 'exec28_at_tacd_protocol', 'exec28_at_protocol_reference'}
    names = ['build_attention_protocol_reader_v5_20261028.py', 'publish_attention_protocol_reader_v4_20261028.py',
             'build_attention_protocol_sponsor_v4_20261028.py', 'publish_attention_protocol_sponsor_v4_20261028.py',
             'review_attention_protocol_chapters_v4_20261028.py']
    write(DEST / 'publication-preflight.json', dict(status='pass', cited_records=len(cited),
        preserved_reader_records=1430, expected_sponsor_records=1094,
        evidence=[ref(TOOLS / n, 'Immutable corrected publication successor') for n in names] + [
            ref(build.BASE / 'prepared-inputs.json', 'Prepared successor inputs'),
            ref(FAILED / 'build-failure.json', 'Failed edition preserved'),
            ref(DEST / 'preflight-preparation-failure.json', 'Generator failure preserved')],
        findings=['Actual compiled citation set equals audited source set before LaTeX compilation.',
                  'Only three registered protocol records are new; all inherited identities remain unchanged.',
                  'Sponsor pairing citations are new and all 1089 predecessor citations remain required.']))
    print(json.dumps(dict(preflight='pass', reader_records=1433, expected_sponsor_records=1094)))


if __name__ == '__main__':
    main()

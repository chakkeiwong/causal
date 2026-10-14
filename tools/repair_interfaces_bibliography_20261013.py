#!/usr/bin/env python3
"""Preserve a real BibTeX failure and check an extended alphabetic suffix style."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-13/interfaces'


def ref(p, anchor):
    return {'path': str(p.relative_to(ROOT)), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'anchor': anchor}


def main():
    failed = BASE / 'build-failure-01'
    assert not failed.exists()
    (BASE / 'reader').rename(failed)
    original = Path('/usr/share/texlive/texmf-dist/bibtex/bst/natbib/plainnat.bst').read_text()
    (BASE / 'plainnat-upstream.bst').write_text(original)
    addition = '''% Causal proposal project modification, 2026-10-13.
% Renamed causalplainnat.bst; preserve original LPPL/copyright below.
% Only duplicate-author/year suffix conversion changes: a..z, aa..az, ba, ...
% Original authors are not responsible for this modification.
'''
    helper = '''INTEGERS { suffix.number suffix.remainder suffix.quotient }
STRINGS { suffix.text }

FUNCTION {extended.extra.label}
{ last.extra.num "a" chr.to.int$ - #1 + 'suffix.number :=
  "" 'suffix.text :=
  { suffix.number #0 > }
  { suffix.number #1 - 'suffix.remainder :=
    #0 'suffix.quotient :=
    { suffix.remainder #25 > }
    { suffix.remainder #26 - 'suffix.remainder :=
      suffix.quotient #1 + 'suffix.quotient :=
    }
    while$
    suffix.remainder "a" chr.to.int$ + int.to.chr$
    suffix.text * 'suffix.text :=
    suffix.quotient 'suffix.number :=
  }
  while$
  suffix.text
}

'''
    marker = 'FUNCTION {forward.pass}'
    assert original.count(marker) == 1
    changed = original.replace(marker, helper + marker, 1)
    old = "last.extra.num int.to.chr$ 'extra.label :="
    assert changed.count(old) == 1
    changed = changed.replace(old, "extended.extra.label 'extra.label :=", 1)
    (BASE / 'causalplainnat.bst').write_text(addition + changed)

    out = BASE / 'bibliography-check'
    out.mkdir()
    bib = ''.join('@misc{t%04d, author={{Fixture Consortium}}, title={Item %04d}, year={2000}}\n' % (i, i)
                  for i in range(1, 704))
    bib += '@misc{unique, author={{Unique Author}}, title={Single work}, year={2000}}\n'
    (out / 'fixture.bib').write_text(bib)
    (out / 'fixture.aux').write_text('\\relax\n\\citation{*}\n\\bibstyle{causalplainnat}\n\\bibdata{fixture}\n')
    env = {**os.environ, 'BSTINPUTS': str(BASE) + ':'}
    proc = subprocess.run(['bibtex', 'fixture'], cwd=out, env=env, text=True, capture_output=True, timeout=20)
    (out / 'bibtex.log').write_text(proc.stdout + proc.stderr)
    assert proc.returncode == 0
    entries = dict((key, label) for label, key in re.findall(r'\\bibitem\[(.*?)\]\{([^{}]+)\}',
                   (out / 'fixture.bbl').read_text(), re.S))

    def expected(n):
        value = ''
        while n:
            n, r = divmod(n-1, 26)
            value = chr(97+r) + value
        return value

    observed = {}
    for i in range(1, 704):
        label = entries['t%04d' % i]
        match = re.search(r'\\natexlab\{([a-z]+)\}', label)
        assert match and match.group(1) == expected(i), (i, label)
        if i in {1, 2, 26, 27, 52, 53, 702, 703}:
            observed[i] = match.group(1)
    assert len(entries) == 704 and 'natexlab' not in entries['unique']
    report = {'status': 'pass', 'duplicate_entries_checked': 703, 'unique_entry_has_no_suffix': True,
              'boundary_suffixes': observed, 'independent_reference': 'Python integer divmod bijective base 26',
              'evidence': [ref(out / n, 'Actual BibTeX fixture and output') for n in
                           ['fixture.bib', 'fixture.aux', 'fixture.bbl', 'bibtex.log']]}
    (BASE / 'bibliography-test.json').write_text(json.dumps(report, indent=2) + '\n')
    repair = {
        'observed_failure': 'plainnat converts 27th same-author/year suffix to ASCII opening brace; malformed natexlab causes fatal runaway bibitem argument.',
        'failure_evidence': [ref(failed / n, 'Preserved first build failure') for n in
                             ['pass-2.log', 'causal_proposal_interfaces_2026-10-13.bbl']],
        'repair': 'Rename and preserve LPPL plainnat derivative; extend only duplicate-author/year suffixes to a..z, aa..zz, aaa... . Author identities and years unchanged.',
        'sources': [ref(BASE / 'plainnat-upstream.bst', 'Installed plainnat source, copyright/LPPL header and forward/reverse passes'),
                    ref(BASE / 'causalplainnat.bst', 'Renamed local derivative; suffix conversion only'),
                    ref(Path(__file__), 'Reproducible style transformation and meaningful boundary fixture')],
        'verification': ref(BASE / 'bibliography-test.json', '703 duplicate identities plus unique-author control'),
        'book_recompile_pending': True}
    (BASE / 'build-repair.json').write_text(json.dumps(repair, indent=2) + '\n')
    print(json.dumps({'repair': 'extended alphabetic year suffixes', 'checks': report['boundary_suffixes'],
                      'entries_checked': 704}))


if __name__ == '__main__':
    main()

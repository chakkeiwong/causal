#!/usr/bin/env python3
"""Bind the primary passages actually inspected for the C construction."""
import json
from closure_common import ROOT, digest, save

READS = {
 'slawski2025': ('docs/literature/text/slawski2025.txt',220,267,
                 'Section 2.1, Audit Sample, assumptions (i) and (ii)',
                 'The source assumes independent membership and accurate audit labels. Our known unequal-inclusion pair estimator is a project derivation, not a claim inherited from this paper.'),
 'sarkka2013': ('docs/literature/text/sarkka2013.txt',9396,9470,
                'Theorem 12.1, equations (12.5)–(12.8), printed p.176; Chapter 6 example p.106 and Chapter 7 pp.116–117 also inspected',
                'Recursive marginal likelihood and numerical Gaussian/particle alternatives. Private logger, audit identification and joint-score calculation are project extensions.'),
 'dml2018': ('docs/reviews/dynamic-source-excerpts/dml2018.txt',1250,1328,
             'Assumptions 3.1–3.2 and equations (3.7)–(3.8), pp.25–26',
             'Orthogonality, score nondegeneracy and nuisance-rate conditions. The source does not automatically validate dependent sparse learners; temporal coupling is reconstructed in our dependent-learning chapter.'),
 'pearl2009': ('docs/literature/text/pearl2009.txt',730,796,
               'Theorem 1 and Corollary 1, equations (15)–(17), pp.110–111',
               'Structural factorization and replacement of intervention factors. Gaussian covariance confidence, latent witnesses and the conservative graph union are project derivations.')}


def main():
    sources={r['id']:r for r in json.loads((ROOT/'docs/literature/sources.json').read_text())}
    rows=[];inputs=['tools/closure_source_review.py','tools/closure_common.py','docs/literature/sources.json']
    for key,(text,start,end,anchors,support) in READS.items():
        source=sources[key]
        assert digest(source['local_path'])==source['sha256']
        assert (ROOT/source['local_path']).read_bytes().startswith(b'%PDF-')
        excerpt='\n'.join((ROOT/text).read_text().split('\n')[start-1:end])
        path=f'docs/reviews/closure-source-{key}.txt';(ROOT/path).write_text(excerpt+'\n')
        rows.append({k:source[k] for k in ('id','title','authors','year','url','local_path','sha256','version_status')} |
                    dict(inspected_anchors=anchors,supported_claim=support,excerpt=path,excerpt_sha256=digest(path)))
        inputs += [source['local_path'],path]
    result=dict(status='pass',date='2026-10-10',publication_cutoff='2026-10-07',sources=rows,
                source_search='No new newest-source claim or new acquisition. Existing cutoff and omissions remain in force.',
                scope='Targeted primary-source inspection and claim limits; not independent review.')
    save('docs/literature/closure-source-review.json',result,inputs)
    print(json.dumps({'status':'pass','inspected_sources':len(rows)}))


if __name__=='__main__':main()

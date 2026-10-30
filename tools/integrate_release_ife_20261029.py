"""Single-use, ledgered uncertainty-delegate integration."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import re
from release_candidate_20261029 import MATH

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'docs/release/2026-10-29'
OUT = BASE/'source-ife-023'
SOURCE = BASE/'source/docs/writing-repair/2026-10-29'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def binding(p):
    return dict(path=str(p.relative_to(ROOT)), sha256=sha(p))


def main():
    ledger = json.loads((BASE/'edits.json').read_text())
    assert len(ledger) == 98, 'Single-use integration; do not rerun.'
    assert not (OUT/'source-audit.json').exists()
    changes = {}
    def edit(p, before, after, reason, destination):
        old, current = changes.get(p, (p.read_text(), p.read_text()))
        assert current.count(before) == 1
        changes[p] = (old, current.replace(before, after, 1))
        ledger.append(dict(file=str(p.relative_to(ROOT)), before=before, after=after,
                           reason=reason, substantive_destination=destination))
    p = SOURCE/'src/d2347a0ffab006bb.tex'
    edit(p, 'two estimated policies also needs their covariance. Variance and contrast\nsemantics delegated to \\texttt{ife}, full survival handling, learner internals\nand parallel random-number behavior remain unqualified.',
         'two estimated policies also needs their covariance. The selected variance\nand contrast delegate is examined below, including centering, sampling units\nand output scale. Full survival handling, learner internals and parallel\nrandom-number behavior remain unqualified.',
         'Replace the named unresolved delegate with its bounded primary-source comparison.',
         'All original policy laws, values, fold and numerical findings remain; selected delegate findings follow in the same section.')
    anchor = 'longitudinal reference while keeping adoption and coverage as later claims.\n'
    edit(p, anchor, anchor+'\n'+(OUT/'addition.tex').read_text(),
         'Develop the uncertainty contract through exact centering, weighting, clustering and contrast examples.',
         'Two new subsections extend the original lmtp treatment; no original science, adverse finding or alternative is removed.')
    bib = SOURCE/'references-0.bib'
    tail = bib.read_text()[-180:]
    extra = r'''
@misc{rel23ife,
 author={Williams, Nicholas and contributors},
 title={{ife}: selected influence-function arithmetic and uncertainty contracts},
 year={2026},
 note={Version 0.2.5; commit dc43de2b030ebd9ae48e725002556bf2b9b9ac00, 1 July. Static primary-source inspection, not native qualification},
 url={https://github.com/nt-williams/ife}
}
@misc{rel23ifecaller,
 author={Williams, Nicholas and Diaz, Ivan and contributors},
 title={{lmtp}: selected pseudo-outcome, contrast and uncertainty-scale callers},
 year={2026},
 note={Version 1.5.4; commit f04a2b47f46debc515ce4ae778e05ebfde922c44, 6 May. Separate source snapshots do not establish a resolved dependency environment},
 url={https://github.com/nt-williams/lmtp}
}
@misc{rel23ifewitness,
 author={{Causal Banking Research Project}},
 title={Exact uncertainty contracts: centered weighted means, unequal clusters and paired contrast scales},
 year={2026},
 note={Project derivations and independent exact reconstruction, 29 October. No downloaded-code execution, empirical coverage study or bank observations}
}
'''
    edit(bib, tail, tail+extra, 'Add authenticated delegate/caller and exact-project identities.',
         'All earlier bibliography entries remain; three additional records support the new treatment.')
    selected = json.loads((OUT/'authenticated-files.json').read_text())
    callers = json.loads((OUT/'authenticated-caller-files.json').read_text())
    tree = json.loads((ROOT/'docs/literature/raw/rel23_lmtp_tree.json').read_text())
    bypath = {x['path']:x for x in tree['tree']}
    for upstream, local in [('R/theta.R','exec22_lmtp_theta.txt'),('R/eif.R','exec22_lmtp_eif.txt'),('R/Task.R','exec22_lmtp_task.txt')]:
        q = ROOT/'docs/literature/raw'/local
        data = q.read_bytes()
        blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert blob == bypath[upstream]['sha'] and len(data) == bypath[upstream]['size']
        callers.append(dict(path=upstream, local_path=str(q.relative_to(ROOT)), sha256=sha(q),
                            receipt=str(q.with_suffix('.receipt.json').relative_to(ROOT))))
    anchor_specs = {
        'R/influence_func_estimand.R':[(38,41,'Symmetric interval on current object scale.'),(61,66,'Documented individual and cluster variance convention.'),(84,135,'Stores supplied influence values without centering; validation.'),(150,229,'Paired arithmetic, derivatives, critical values and denominator/log guards.'),(138,147,'Fixed95% print label.')],
        'R/std_error.R':[(1,15,'Weights before sample variance; cluster sums and K/n scaling; single-cluster fallback.')],
        'R/helpers.R':[(1,14,'Equality checks on vector length, weights and IDs.')],
        'R/ife.R':[(1,8,'Constructor default critical value and positional IDs.')],
        'R/tidy.R':[(7,15,'Delegate output uses current object scale.')],
        'README.md':[(54,65,'Documented uncentered example.'),(87,94,'Exponentiation of log confidence endpoints.')],
        'NEWS.md':[(1,25,'Version-specific clustering and arithmetic changes.')],
        'DESCRIPTION':[(1,28,'Version0.2.5 and declared dependencies/terms.')],
        'LICENSE.md':[(1,8,'Direct GPLv3 text identity.')],
        'tests/testthat/test-std_error.R':[(4,22,'Tests document sample-variance divisor and single-cluster fallback.'),(44,58,'Unequal-cluster test supplies centered influence values.'),(78,94,'Weighted test supplies centered values.')]
    }
    caller_specs = {
        'R/theta.R':[(1,25,'Uncentered pseudo-outcome and estimate rescaled then passed to ife.')],
        'R/eif.R':[(1,12,'Residual sum plus initial shifted prediction, without estimate subtraction.')],
        'R/Task.R':[(54,60,'Affine rescaling.'),(178,190,'Mean-normalized supplied weights.')],
        'R/contrasts.R':[(19,56,'Paired contrast, log-scale uncertainty, point/endpoints exponentiated with std.error unchanged.')],
        'R/print.R':[(10,20,'Multiple-comparison warning on print.')],
        'R/tidy.R':[(21,22,'Forwarding estimate to ife tidy.')]
    }
    sources = []
    for key, rows, specs, repo, pin, version in [
        ('rel23ife',selected,anchor_specs,'nt-williams/ife','dc43de2b030ebd9ae48e725002556bf2b9b9ac00','0.2.5;2026-07-01'),
        ('rel23ifecaller',callers,caller_specs,'nt-williams/lmtp','f04a2b47f46debc515ce4ae778e05ebfde922c44','1.5.4;2026-05-06')]:
        bindings = []
        anchors = []
        for row in rows:
            q = ROOT/row['local_path']
            assert sha(q) == row['sha256']
            bindings.append(binding(q))
            if row.get('receipt'): bindings.append(binding(ROOT/row['receipt']))
            lines = q.read_text().splitlines()
            for first,last,finding in specs.get(row['path'],[]):
                last = min(last,len(lines))
                anchors.append(dict(path=row['local_path'],sha256=sha(q),lines=[first,last],
                                    text='\n'.join(lines[first-1:last]),finding=finding))
        identity_files = ['rel23_ife_repo.json','rel23_ife_cutoff.json','rel23_ife_tree.json'] if key=='rel23ife' else ['rel23_lmtp_tree.json']
        bindings.extend(binding(ROOT/'docs/literature/raw'/name) for name in identity_files)
        sources.append(dict(citation_key=key, kind='implementation',source_identity=f'https://github.com/{repo}/tree/{pin}',
                            version_date=version+'; '+pin+'; retrieved2026-10-29; client cutoff2026-10-07',
                            local_bindings=bindings,inspected_anchors=anchors,supported_claims=[x['finding'] for x in anchors],
                            limitations=['Static source inspection only; no downloaded code or upstream tests executed.',
                                         'Separate selected revisions do not prove a resolved installed environment or CRAN artifact equality.',
                                         'Numerical variance delegate, dependency behavior, native admission and empirical calibration remain unqualified.',
                                         'Papers named in package documentation are discovery leads only; no scholarly admission or technical theorem attributed to them.']))
    witness = OUT/'exact-witnesses.json'
    generator = ROOT/'tools/release_ife_witnesses_20261029.py'
    sources.append(dict(citation_key='rel23ifewitness',kind='project_derivation',source_identity=str(generator.relative_to(ROOT)),
                        version_date='2026-10-29 exact project constructions',local_bindings=[binding(witness),binding(generator)],
                        inspected_anchors=['main(): weighted-ratio derivative and origin shift; constant reward contrast; unequal-cluster aggregation; paired row identity; transformed interval scales.'],
                        supported_claims=['Weighted ratio influence must center before unequal weighting.',
                                          'Exact variance101/192 vs149/48 and14983/16 after known offset.',
                                          'Constant reward difference has zero influence; uncentered weighting gives1/3.',
                                          'Unequal-cluster centered variance1/4 vs1 and2601 after offset.',
                                          'Log standard error0.2 differs from ratio-scale0.3; endpoint transformations differ.'],
                        limitations=['Finite authored arithmetic, not upstream runtime, empirical coverage or bank outcomes.',
                                     'Sampling and nuisance conditions must be supplied separately; two clusters illustrate an identity, not reliable asymptotics.']))
    ap = OUT/'source-audit.json'
    audit_text = json.dumps(dict(cutoff='2026-10-07',sources=sources,scope='Selected uncertainty delegate and caller closure; no exhaustive census or new scholarly source.'),indent=2)+'\n'
    rp = BASE/'mathematical-addition-reviews.json'
    reviews = json.loads(rp.read_text())
    e = ledger[99]
    occurrences = lambda text:Counter(re.sub(r'\s+',' ',m[0]) for m in MATH.finditer(text))
    assert not occurrences(e['before'])-occurrences(e['after'])
    reviews['reviews'].append(dict(scope='Additive weighted-ratio, cluster and contrast uncertainty derivations.',
        edits=[dict(edit=100,file=e['file'],before_sha256=hashlib.sha256(e['before'].encode()).hexdigest(),after_sha256=hashlib.sha256(e['after'].encode()).hexdigest())],
        allowed_added=dict(occurrences(e['after'])-occurrences(e['before'])),allowed_removed={},status='reviewed_additions_only',
        derivation='Differentiate weighted numerator/denominator, center before weights, group independent-cluster sums and scale K/n. Compare exact variance under known location shifts and constant reward increments. Apply chain rule to log-ratio and exponentiate interval endpoints.',
        reviewed_assumptions=['Nonnegative weights with positive finite mean; finite second moments and declared independent observations or clusters.',
                              'Fitted pseudo-outcomes additionally need identifying and nuisance conditions; no coverage established by arithmetic.',
                              'Known deterministic reward shifts are not claims of constant causal effects.',
                              'Sample variance divisor n-1 is explicit; no downloaded numerical delegate execution.'],
        witness=binding(witness),source_audit=dict(path=str(ap.relative_to(ROOT)),sha256=hashlib.sha256(audit_text.encode()).hexdigest()),
        fresh_visual_acceptance=False,independent_acceptance=False))
    before = OUT/'before'
    before.mkdir(exist_ok=False)
    for q,(old,new) in changes.items():
        assert q.read_text()==old
        (before/q.name).write_text(old)
    for name in ['edits.json','mathematical-addition-reviews.json']:
        (before/name).write_bytes((BASE/name).read_bytes())
    ap.write_text(audit_text)
    for q,(_,new) in changes.items(): q.write_text(new)
    (BASE/'edits.json').write_text(json.dumps(ledger,indent=2)+'\n')
    rp.write_text(json.dumps(reviews,indent=2)+'\n')
    print(json.dumps(dict(edits=len(ledger),source_audit_sha256=sha(ap),witness_sha256=sha(witness))))


if __name__ == '__main__':
    main()

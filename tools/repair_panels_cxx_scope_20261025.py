#!/usr/bin/env python3
"""Preserving pre-publication correction for the kernel's short-panel lag cap."""
import json
from pathlib import Path
import panels_cxx_reference_v2_20261025 as exact
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/'docs/program/execution/2026-10-25/panels-cxx-v1'
BASE=OLD.parent/'panels-cxx-v2'
read=lambda p:json.loads(p.read_text())

def main():
    assert not BASE.exists();verify_bindings(read(OLD/'review.json'));BASE.mkdir()
    for name in ['sponsor-addition.md','comparison-review.json','conversion-contract.json',
                 'dependency-license-review.json','omissions-register.json','identity-review.json',
                 'search-screening.json']:
        (BASE/name).write_bytes((OLD/name).read_bytes())
    text=(OLD/'development.tex').read_text()
    marker='This is an authored witness about interface normalization, not a package'+chr(10)+'measurement.'
    assert text.count(marker)==1
    replacement=r'''This is an authored witness about interface normalization, not a package
measurement. In fact, the selected kernel caps its weight count at $T-1$
after dropping a trailing zero. With two periods this leaves only lag zero,
so the lag-one algebra above must not be reported as that native return.
Appending a third, zero-score period retains the same sum of squares and
lag-one product while allowing the lag-one loop under the inspected cap.
Both short-panel and zero-padded cases belong in the public test inventory.
\citep{exec25_panelcxx_fixest,exec25_panelcxx_reference}'''
    text=text.replace(marker,replacement);(BASE/'development.tex').write_text(text)
    write(BASE/'exact-results.json',exact.calculate())
    findings=read(OLD/'mathematical-review.json')['findings']+['Two-period kernel weight cap leaves lag zero only;41is a lag-one algebraic witness,not the two-period native output. Three-period zero padding retains lag-one41under the inspected bound.']
    evidence=[ref(OLD/'review.json','Preserved first review'),ref(OLD/'development.tex','Preserved first argument'),ref(ROOT/'docs/literature/raw/exec25_panelcxx_fixest_2.txt','Weight count at lines143-149 and lag loop'),ref(Path(exact.original.__file__),'Original arithmetic'),ref(Path(exact.__file__),'Explicit short-panel successor'),ref(BASE/'exact-results.json','Exact distinctions'),ref(BASE/'development.tex','Corrected argument'),ref(Path(__file__),'Preserving repair')]
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_witnesses',evidence=evidence,findings=findings,native_execution=False,native_reachability_proved=False))
    audit=read(OLD/'source-audit.json')
    source=next(s for s in audit['sources'] if s['integrated_citation_key']=='exec25_panelcxx_reference')
    source['local_copy']=ref(BASE/'mathematical-review.json','Exact examples with short-panel limit');source['supported_claims']=findings
    kernel=next(s for s in audit['sources'] if s['integrated_citation_key']=='exec25_panelcxx_fixest')
    kernel['supported_claims'].append('Kernel caps weight count atT-1;two-period input excludes lag1. Distinguish intended normalization witness from native output.')
    kernel['inspected_anchors'].append(dict(local_copy=ref(ROOT/'docs/literature/raw/exec25_panelcxx_fixest_2.txt','Short-panel bound'),lines=[143,149],finding=kernel['supported_claims'][-1]))
    write(BASE/'source-audit.json',audit)
    write(BASE/'plan-review.json',dict(status='pass',evidence=evidence,checks=['Preserve original source and review without alteration.','Inspect loop bound and caller before attributing an algebraic value to a package.','Keep all seven new records and inherited sources;no native capability.','Integrate successor,record inconclusive coverage,complete paired publication and all controller checks.']))
    write(BASE/'copyedit-review.json',dict(status='pass',evidence=evidence,findings=['Explicitly separate two-period kernel bound from general lag-one normalization.','Prior covariance reachability,native,rights and coverage limitations retained.'],visual_acceptance=False))
    prior=read(OLD/'review.json');prior['evidence']+=evidence+[ref(BASE/n,'Corrected review dependency') for n in ['source-audit.json','mathematical-review.json','plan-review.json','copyedit-review.json']]
    prior['findings']=findings;prior['supersedes']=ref(OLD/'review.json','Preserved bounded review');write(BASE/'review.json',prior)
    print('Preserving short-panel qualification repair completed.')

if __name__=='__main__':main()

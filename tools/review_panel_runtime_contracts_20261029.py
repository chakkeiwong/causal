"""Bind runtime source claims and performed authored fixtures without native promotion."""
import hashlib,json
from pathlib import Path
import panel_runtime_reference_20261029 as exact
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'docs/program/execution/2026-10-29/panel-runtime-semantics-v1';RAW=ROOT/'docs/literature/raw'
read=lambda p:json.loads(p.read_text())
ANCHORS={
 'exec29_runtime_rstats_0':[(1,1,'Development branch reports4.7.0 unstable')],
 'exec29_runtime_rstats_1':[(729,765,'Selected development summary covariance and pivot route')],
 'exec29_runtime_rstats_2':[(20,63,'Selected development explicit GLM summary and aliased covariance route')],
 'exec29_runtime_rstats_3':[],
 'exec29_runtime_rcpp_0':[(1,4,'Selected Rcpp version'),(30,36,'Declared constraints and licence; not complete rights acceptance')],
 'exec29_runtime_rcpp_1':[(22,28,'Conditional sampling include guard'),(335,350,'Size-one integer empirical sampler'),(395,434,'One-based default and dispatch')],
 'exec29_runtime_dplyr_0':[(1,4,'Selected dplyr version'),(19,27,'Declared terms and dependency constraints')],
 'exec29_runtime_dplyr_1':[(30,94,'First-input template and post-vctrs reconstruction')],
 'exec29_runtime_dplyr_2':[(195,220,'Reconstruction dispatch and data-frame method')],
 'exec29_runtime_dplyr_3':[(1,139,'Default reconstruction copies template attributes except names and row names')],
 'exec29_runtime_tibble_0':[(1,3,'Selected tibble version'),(15,23,'Declared terms and dependencies')],
 'exec29_dispatch_rstats_0':[(480,485,'Development qr.lm returns stored QR')],
 'exec29_dispatch_dplyr_0':[(1,481,'Selected registrations: data.frame,grouped_df,rowwise_df reconstruction; no nonabsdid method in this namespace')],
 'exec29_dispatch_tibble_0':[(1,112,'No dplyr reconstruction method in selected namespace')],
 'exec29_dispatch_tibble_1':[(422,424,'Subset restoration delegate only; not row-binding qualification')],
 'exec29_runtime_armadillo_0':[(1,6,'Selected Armadillo bridge version'),(29,42,'Declared C++14,licence distinction and Rcpp constraint')],
 'exec29_runtime_armadillo_1':[(21,39,'Header includes forward configuration then Rcpp')],
 'exec29_runtime_armadillo_2':[(24,51,'Forward configuration and RNG alternative; complete inclusion path remains open')],
 'exec29_runtime_armadillo_3':[(27,80,'Separate opt-in extension namespace and call signature')],
 'exec29_runtime_r46_0':[(1,1,'Branch reports4.6.1 Patched; not binary-release identity')],
 'exec29_runtime_r46_1':[(687,723,'Patched-branch summary covariance in pivot order')],
 'exec29_runtime_r46_2':[(20,63,'Patched-branch GLM summary and aliased covariance route')],
 'exec29_runtime_r46_3':[(457,462,'Patched-branch qr.lm returns stored QR')],
}


def main():
    assert not (BASE/'review.json').exists()
    rows=[]
    for name in ['source-plan.json','dispatch-source-plan.json','additional-source-plan.json']:
        for p in read(BASE/name)['sources']:
            f=RAW/(p['id']+'.txt');receipt=RAW/(p['id']+'.receipt.json');data=f.read_bytes();r=read(receipt)
            assert hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()==p['git_blob_sha1']
            assert hashlib.sha256(data).hexdigest()==r['sha256'] and r['url']==p['url']
            lines=data.decode().splitlines();anchors=[]
            for a,b,finding in ANCHORS[p['id']]:
                assert 1<=a<=b<=len(lines),(p['id'],a,b,len(lines))
                anchors.append(dict(lines=[a,b],finding=finding,excerpt_sha256=hashlib.sha256(chr(10).join(lines[a-1:b]).encode()).hexdigest()))
            rows.append(dict(candidate=p['candidate'],source_identity=p['url'],version_date=p['date']+'; '+p['commit'],
                local_copy=ref(f,'Exact primary bytes'),acquisition_receipt=ref(receipt,'Observed response'),git_blob_sha1=p['git_blob_sha1'],
                inspected_anchors=anchors,supported_claims=[a['finding'] for a in anchors],inspection_status='selected_ranges_inspected' if anchors else 'acquired_only',native_execution=False))
    assert len(rows)==23
    assert exact.calculate()==read(BASE/'exact-results.json')
    sources=[dict(integrated_citation_key='exec29_panel_runtime_sources',kind='software_primary_sources',title='Pinned R, Rcpp, Armadillo and result reconstruction source contracts',author='Selected R ecosystem contributors',year=2026,source_identity='Selected fixed cutoff repository files',version_date='Pre-cutoff source candidates; inspected29October2026',local_copy=rows[0]['local_copy'],records=rows,
        inspected_anchors=[dict(anchor='Selected per-file line ranges and excerpt digests',inspection='Primary source comparison')],supported_claims=['Selected covariance dispatch/order, version, sampling and reconstruction behavior.'],limits=['R4.7development and4.6.1Patched sources are candidates; installed fixture uses4.1.2.','Acquired base QR file uninspected; other file tails and full header/vctrs/native paths remain open.']),
        dict(integrated_citation_key='exec29_panel_runtime_reference',kind='project_reference_not_external_paper',title='Conditional packed-bit moments and constructed covariance-order witnesses',author='Causal banking proposal project',year=2026,source_identity='Independent exact Python reference and authored installed-R constructed-object fixture',version_date='29October2026; performed on installedR4.1.2',local_copy=ref(Path(exact.__file__),'Independent exact reference'),results=ref(BASE/'exact-results.json','Exact fractions and small-bit enumeration'),constructed_fixture=ref(ROOT/'tools/panel_runtime_constructed_fixture_20261029.R','Authored fixture'),execution=ref(BASE/'constructed-r-exit.json','Actual exit0 and outputs'),
        inspected_anchors=[dict(anchor='calculate and constructedRscript',inspection='Exact conditional moments and covariance-order invariants')],supported_claims=['Under ideal uniform positive31-bit integers mean1/(2^31-1), cross-moment -1/(2^31-1).','Constructed nontrivial pivot gives positional quadratic1/4 versus aligned1.'],limits=['No native parglm/fastdid/BMisc execution; no default-solver reachability or coverage claim.'])]
    audit=dict(sources=sources,cutoff='2026-10-07',native_package_execution=False);verify_bindings(audit);write(BASE/'source-audit.json',audit)
    evidence=[ref(BASE/n,'Performed source or connected argument') for n in ['source-audit.json','exact-results.json','constructed-r-exit.json','development.tex','sponsor-addition.md','plan-review.json']]+[ref(Path(__file__),'Exact source audit')]
    write(BASE/'mathematical-review.json',dict(status='pass_for_scoped_project_derivations',issues=[],evidence=evidence,findings=['Counting excludes only the zero bit pattern; exact enumeration checks2through8bits.','Covariance permutation uses a declared coherent triangular factor and original coefficient order.','Native pivot reachability, PRNG law and coverage remain separate.'],native_package_execution=False,empirical_coverage=False))
    write(BASE/'copyedit-review.json',dict(status='pass_for_source_text',evidence=evidence,rendered_review=False,findings=['Connected runtime/target argument with explicit banking and CLI/MCP implications.','Development source,patched branch and installed runtime are distinguished.','No agent-written substitute original or inferred native acceptance.']))
    actions=['Qualify full preprocessor/header chain and actual PRNG; retain ideal-uniform calculations as conditional.','Prove or test pivot reachability in exact defaultLINPACK path; compare aliases and full influence calculations.','Pin vctrs and external reconstruction registrations; run mixed-level objects in declared native profile.','Resolve exact upstream DCDH/fect/PanelMatch versions and authentic omitted originals.','Complete transitive rights and fixed public profile before native package/calibration claims.','Continue independent coverage/depth and31unread frontier originals; fresh visual and final acceptance remain open.']
    write(BASE/'remaining-obligations.json',dict(status='open_local_continuations',actions=actions,canonical_gaps_closed=[],evidence=evidence))
    write(BASE/'review.json',dict(status='pass_for_bounded_source_addition',acquired_files=23,inspected_files=22,source_records=2,evidence=evidence+[ref(BASE/'mathematical-review.json','Derivation review'),ref(BASE/'remaining-obligations.json','Open routes')],native_package_execution=False,visual_acceptance=False,final_acceptance=False))
    print(json.dumps(dict(acquired_files=23,inspected_files=22,source_records=2,reference='pass',constructed_R_fixture='pass',native_package_execution=False)))


if __name__=='__main__':main()

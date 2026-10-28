"""Review selected originals and identities; preserve precise source limitations."""
import hashlib,json,shutil,subprocess
from pathlib import Path
import panel_design_reference_20261028 as exact
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-28/panel-originals-v1'
RAW=ROOT/'docs/literature/raw'
read=lambda p:json.loads(p.read_text())


def main():
    assert not (BASE/'source-audit.json').exists()
    sources=[]
    configs=[
        ('roth','exec28_panel_roth_v2','Interpreting Event-Studies from Recent Difference-in-Differences Methods','Jonathan Roth','Roth',2026,
         'https://arxiv.org/pdf/2401.12309v2','2401.12309v2; submitted 2026-01-16; cover 2026-01-21',
         [(2,9,'Common-adoption diagnostic and exact pre/post baseline formulas'),(10,12,'Symmetric baselines, separate diagnostic/estimation uses and valid-assumption scope'),(15,15,'In-sample attenuation in the common-adoption example')],
         ['Nonstaggered baseline changes explain apparent kinks and jumps under a linear violated trend.','Universal and mean-base comparisons have different diagnostic interpretations.'],
         ['No visual figure review; package environment reported by the paper is 31 October 2025; 2024 source script is not that environment.']),
        ('tsai','exec28_panel_tsai_v3','Difference-in-Differences with Multiple Events','Lin-Tung Tsai','Tsai',2025,
         'https://arxiv.org/pdf/2409.05184v3','2409.05184v3; submitted 2025-01-21; cover 2025-01-22',
         [(3,6,'Absorbing treatments, iid units, no anticipation, parallel trends, overlap and omitted-event decomposition'),(8,17,'Combined versus target effects, second-stage assumptions, aggregation and inference'),(26,27,'Homogeneous omitted-event algebra'),(30,31,'First-stage comparison/subsample proof'),(34,36,'Appendix explicit anchor and two event-order derivations')],
         ['First stage identifies combined effects with controls not yet exposed to either event.','Separate effect identification needs event-order-specific support and treatment-effect restrictions.','Same-date events lack the one-effect base period in this design.'],
         ['Equation 11 target-time entry conflicts with Appendix equation 17 anchor; neighboring event-order prose and availability notation also require clarification.','Only selected proofs reviewed; no whole-theorem certification or native equivalence.','Conditional trends do not license an unadjusted unconditional contrast.','No unrestricted cross-unit dependence or interaction identification is claimed.']),
        ('wing','exec28_panel_stacked_original','Stacked Difference-in-Differences','Coady Wing and Seth M. Freedman and Alex Hollingsworth','Wing',2024,
         'https://www.nber.org/system/files/working_papers/w32054/w32054.pdf','NBER w32054; January 2024 cover; mutable endpoint acquired 2026-10-28',
         [(1,3,'Identity, abstract and repository association'),(8,10,'Group-time identification and composition problem'),(12,20,'Trimmed targets, explicit sample shares and corrective weights'),(21,23,'Aggregation and clustering assumptions; limited Monte Carlo')],
         ['Basic pooled stack weights treatment and control trends differently.','Corrective control weights align cohort shares for the specified balanced target.','Common event windows and repeated-unit dependence are separate issues.'],
         ['Cover date is not proof of historical byte identity for a mutable endpoint.','Not every stacked fixed-effect specification is the basic pooled estimator.','No complete Monte Carlo replication or bank uncertainty qualification.'])]
    for key,stem,title,author,surname,year,url,version,anchors,claims,limits in configs:
        raw=RAW/(stem+'.pdf');receipt=read(RAW/(stem+'.receipt.json'))
        assert raw.read_bytes().startswith(b'%PDF-') and hashlib.sha256(raw.read_bytes()).hexdigest()==receipt['sha256']
        dest=ROOT/'docs/papers'/f'{title} {surname}({year}).pdf'
        if dest.exists():assert dest.read_bytes()==raw.read_bytes()
        else:shutil.copyfile(raw,dest)
        inspected=[]
        for a,b,finding in anchors:
            target=BASE/f'{key}-pages-{a}-{b}.txt'
            subprocess.run(['pdftotext','-layout','-f',str(a),'-l',str(b),str(raw),str(target)],check=True)
            inspected.append(dict(anchor=f'Physical PDF pages {a}-{b}',finding=finding,extraction=ref(target,'Inspected primary text, not a replacement PDF')))
        sources.append(dict(integrated_citation_key='exec28_panel_'+key,kind='paper',title=title,filename_title=title,
            author=author,first_author=surname,year=year,source_identity=url,version_date=version,local_path=str(dest.relative_to(ROOT)),
            sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),local_copy=ref(dest,'Genuine retained original'),
            acquisition_receipt=ref(RAW/(stem+'.receipt.json'),'Observed original acquisition'),inspected_anchors=inspected,
            supported_claims=claims,limits=limits))
    identities=read(BASE/'identity-review.json')['repositories']
    spec={'nonabsdid':[(0,[(1,48,'Version 0.4.1, delegate/package list, URL and license declaration')]),(1,[(1,2,'Copyright holder notice')])],
        'pampe':[(0,[(1,16,'Version 1.1.2, leaps dependency, GPL-2 declaration')]),(1,[(1,105,'API, donor layout, subset selection, placebo options and model-size discussion')])],
        'stacked':[(0,[(1,3,'R/Stata walkthrough association')]),(1,[(92,143,'R stack membership, date encoding and feasible window'),(407,443,'R shares and corrective weights'),(450,470,'Stata row-index sums require balance'),(508,536,'Weighted regression and original-state clustering')])],
        'events':[(0,[(1,148,'Unpinned package imports, linear violated-trend example and estimator calls')]),(1,[(1,21,'MIT notice and retention condition')])],
        'fastdid':[(0,[(1,36,'Version 1.0.7, date, author, URL, dependencies and license declaration')]),(1,[(1,68,'Paper association, multiple-event documentation and unverified performance claim')]),(2,[(1,2,'Copyright holder notice')])]}
    records=[];decisions=[]
    actions={
        'nonabsdid':'Inspect nabs_event_study, effect_cells, preflight and each DIDmultiplegtDYN/PanelMatch/fect/fixest delegate; adopt presentation conventions only after target distinctions survive.',
        'pampe':'Inspect pampe, regsubsets2aic and robustness plus exact leaps version; obtain original method/package papers through an authentic permitted route.',
        'stacked':'Check balanced/unbalanced cohorts, date=1/TRUE inclusion, Stata triangular count sums, package locks and rights; port algebra only after target and weight checks.',
        'events':'Pin imports matching intended paper edition; preserve normalization and compare estimator targets before native replay.',
        'fastdid':'Resolve paper/README edition difference; inspect double_did, estimate_gtatt, aggregate_gt, validate and tests; check both event orders, equal timing, support and bootstrap.'}
    for row in identities:
        key=row['candidate'];tree=read(RAW/f'exec28_panel_{key}_tree.json');assert tree['truncated'] is False
        lookup={x['path']:x for x in tree['tree']}
        selected=[]
        for j,anchors in spec[key]:
            stem=f'exec28_panel_{key}_identity_{j}';p=RAW/(stem+'.txt');receipt=read(RAW/(stem+'.receipt.json'))
            path=receipt['url'].split(row['commit']+'/',1)[1];data=p.read_bytes()
            blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            assert blob==lookup[path]['sha'] and hashlib.sha256(data).hexdigest()==receipt['sha256']
            lines=data.decode().splitlines();aa=[]
            for a,b,finding in anchors:
                b=min(b,len(lines));assert b>=a
                excerpt=chr(10).join(lines[a-1:b]).encode()
                aa.append(dict(lines=[a,b],finding=finding,excerpt_sha256=hashlib.sha256(excerpt).hexdigest()))
            records.append(dict(candidate=key,source_identity=receipt['url'],version_date=row['date']+'; '+row['commit'],
                upstream_path=path,local_copy=ref(p,'Inspected pinned primary file'),acquisition_receipt=ref(RAW/(stem+'.receipt.json'),'Saved pinned public source'),
                git_blob_sha1=blob,inspected_anchors=aa,supported_claims=[a['finding'] for a in aa],native_execution=False))
            selected.append(path)
        decisions.append(dict(candidate=key,repository=row['repository'],commit=row['commit'],date=row['date'],selected_files=selected,
            tree=ref(RAW/f'exec28_panel_{key}_tree.json','Complete pinned navigation tree, not technical acceptance'),
            next_action=actions[key],native_execution=False,rights_acceptance=False))
    software= dict(integrated_citation_key='exec28_panel_software',kind='software_primary_sources',
        title='Pinned panel software identities and selected example/manual contracts',author='Panel package and example contributors',year=2026,
        source_identity='Five exact cutoff repositories: nonabsdid, pampe, stacked-did-weights, HetEventStudies and fastdid',
        version_date='Per-record pinned commits before 2026-10-07; inspected 2026-10-28',records=records,
        local_copy=records[0]['local_copy'],inspected_anchors=[dict(anchor='Per-record exact lines and blob identities',inspection='Author primary text inspection')],
        supported_claims=['Five exact candidate identities and eleven selected originals are distinguished from native qualification.','Conditional reuse alternatives and specific delegate/edition/rights obligations.'],
        limits=['Metadata supports identity and declared scope; selected example code supports only the inspected construction.','No acquired execution, performance benchmark or complete dependency rights review.'])
    sources.append(software)
    write(BASE/'exact-results.json',exact.calculate())
    sources.append(dict(integrated_citation_key='exec28_panel_reference',kind='project_reference_not_external_paper',
        title='Exact synthetic banking panel baselines, event orders and stack weights',author='Causal banking proposal project',year=2026,
        source_identity='tools/panel_design_reference_20261028.py',version_date='28 October 2026; exact authored reference',
        local_copy=ref(Path(exact.__file__),'Independent Fraction arithmetic'),results=ref(BASE/'exact-results.json','Exact outputs'),
        inspected_anchors=[dict(anchor='calculate(): normalization, stacked aggregate and row-level means, multiple-event cancellation and anchors',inspection='Algebra and exact replay')],
        supported_claims=['Specified artificial examples yield false trend/weight signals and conditional corrected values.'],limits=['Not native execution, measured customer economics or empirical uncertainty calibration.']))
    write(BASE/'software-identity-review.json',dict(status='pass_for_bounded_identity_and_selected_source_review',candidates=decisions,records=records,native_execution=False,awards_acceptance=False))
    write(BASE/'omissions-register.json',dict(status='open_local_obligations',items=[
        dict(id='TSAI.EDITION',reason='Selected v3 main/appendix and event-order inconsistencies; README dates cited work 2026.',next_action=actions['fastdid']),
        dict(id='PAMPE.ORIGINAL',reason='R Journal host outside fixed collector allowlist; authentic package/method originals not admitted here.',next_action='Find authentic permitted original route or narrowly authorized collector addition; no summary substitute.'),
        dict(id='SYNTH.ORIGINAL',reason='Original JSS paper remains a separate lead despite retained package source.',next_action='Acquire DOI 10.18637/jss.v042.i13 original and reconcile selected source version.'),
        dict(id='TREND.WEIGHTING',reason='Ahlfeldt original DOI 10.1093/cesifo/ify013 not inspected in this packet.',next_action='Acquire original through permitted primary route and inspect target/weights.'),
        dict(id='PINNED.DELEGATES',reason='Five candidates not natively or comprehensively qualified.',next_action='Execute candidate-specific delegate actions in software-identity-review.json.'),
        dict(id='VISUAL',reason='Inherited six-image allowance exhausted.',next_action='Fresh session for rendered visual review; keep source and independent tasks eligible.')],final_acceptance=False))
    audit=dict(sources=sources,cutoff='2026-10-07',inspection_date='2026-10-28',identity=ref(BASE/'identity-review.json','Version histories and cutoff commits'))
    verify_bindings(audit);write(BASE/'source-audit.json',audit)
    evidence=[ref(BASE/n,'Reviewed panel source or argument') for n in ['source-audit.json','software-identity-review.json','exact-results.json','development.tex','sponsor-addition.md','omissions-register.json','plan-review.json']]
    evidence += [ref(Path(__file__),'Performed source review'),ref(Path(exact.__file__),'Independent arithmetic')]
    write(BASE/'mathematical-review.json',dict(status='pass_for_scoped_project_derivations',issues=[],evidence=evidence,
        findings=['Verified differing baseline formulas under zero effect and linear violated trends.','Derived both event-order formulas with explicit support and restrictions from Appendix A.4.','Preserved equation11/17 inconsistency instead of silently equating expressions.','Unconditional contrast requires unconditional trends; conditional adjustment caveat explicit.','Stack trend mismatch 65 and corrective weights checked by aggregate and row-level arithmetic.','Covariance, overlap and estimated weights remain part of inference, not established by arithmetic.'],
        all_source_theorems_independently_verified=False,native_execution=False,empirical_coverage=False))
    write(BASE/'copyedit-review.json',dict(status='pass_for_source_text',evidence=evidence,
        findings=['Connected bank decision, notation, assumptions, alternatives and monetary examples.','All numerical banking examples explicitly synthetic.','Documentation scope, proof argument, authored calculation and native behavior distinguished.','No process-log narrative or wholesale acceptance claim.'],rendered_review=False))
    write(BASE/'review.json',dict(status='pass_for_bounded_proposal_addition',evidence=evidence+[ref(BASE/'mathematical-review.json','Mathematical review'),ref(BASE/'copyedit-review.json','Copyedit review')],
        original_papers=3,pinned_original_files=len(records),canonical_gaps_closed=[],native_execution=False,visual_acceptance=False,final_acceptance=False))
    print(json.dumps(dict(papers=3,pinned_files=len(records),audited_additions=len(sources),mathematical_review='pass_with_explicit_source_limits')))


if __name__=='__main__':main()

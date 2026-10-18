#!/usr/bin/env python3
"""Review selected Java identification sources without claiming full coverage."""
import hashlib
import json
from pathlib import Path
import run_program_reviews_v2 as extension
import java_identification_reference_20261019 as exact
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run=extension.base
core=run.core
ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-19/java-identification-v1'
RAW=ROOT/'docs/literature/raw'
OP='SW.CELL.identification_counterfactual.Java'
OUTPUT=ROOT/f'docs/program/comprehensive-v14/work/{OP}/coverage-review.json'
REVIEWER=dict(name='Codex author/coordinator',kind='author')


def read(p):return json.loads(p.read_text())


def main():
    assert not OUTPUT.exists()
    state=core.read(ROOT,core.STATE)
    assert state['execution_runtime']['active']['operation']==OP
    assert read(BASE/'plan-review.json')['status']=='pass_to_execute'
    manifest=read(BASE/'acquisition-manifest.json');pin=manifest['selected_commit']
    tree=read(RAW/'v12_sw2_tetrad_tree.json')
    commit=read(RAW/'v12_sw_cutoff_commit_tetrad.json')[0]
    assert pin==commit['sha'] and not tree['truncated'] and len(tree['tree'])==4200
    blobs={r['path']:r['sha'] for r in tree['tree'] if r['type']=='blob'}
    files=manifest['files']+read(BASE/'dependency-acquisition-manifest.json')['files']
    ranges=[[(35,42),(150,165),(175,200),(211,265),(290,355),(480,520),(535,560),(855,965),(970,998)],
        [(29,88)],[(35,95)],[(68,82),(120,166)],[(100,145),(170,205),(418,460)],
        [(43,55),(110,150),(305,348),(525,570)],[(215,235),(260,290)],[(970,1030)],[(205,235),(305,330),(365,379)]]
    records=[];extracts=[]
    for row,sections in zip(files,ranges):
        path=RAW/(row['id']+'.txt');receipt_path=RAW/(row['id']+'.receipt.json')
        data=path.read_bytes();receipt=read(receipt_path)
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        url=f'https://raw.githubusercontent.com/cmu-phil/tetrad/{pin}/{row["path"]}'
        assert receipt['status']=='saved' and receipt['url']==url and receipt['sha256']==core.sha(path)
        assert blob==blobs[row['path']]==row['git_blob_sha1']
        anchor='; '.join(f'lines{a}-{b}' for a,b in sections)
        records.append(dict(role='inspected_primary_technical_text',source_identity=url,
            version_date=manifest['commit_date']+'; '+pin,local_copy=ref(path,anchor),
            receipt=ref(receipt_path,'Authentic bounded primary acquisition'),git_blob_sha1=blob,
            inspected_anchors=[anchor],executed=False))
        lines=data.decode().splitlines()
        extracts.append(dict(source=row['path'],local_copy=ref(path,anchor),sections=[
            dict(start=a,end=b,text='\n'.join(f'{i+1}: {lines[i]}' for i in range(a-1,min(b,len(lines))))) for a,b in sections]))
    assert len(records)==9
    write(BASE/'inspected-extracts.json',dict(records=extracts,native_execution=False))
    claims=[
        'Identifiability implements ManipulatingBayesUpdater and evaluates a c-component/Q-expression route using an observational joint-probability object; it is a distinct interface from IDA.',
        'The public parameter type is BayesIm, but no-evidence and QList evaluation paths cast to MlBayesImObs; a generic parameter signature is not sufficient subtype qualification.',
        'Evidence.getVariablesInEvidence selects singleton categories without checking manipulation flags; Identifiability treats these variables as interventions, while createManipulatedGraph checks flags.',
        'An unsuccessful recursive identify branch returns null and the public joint marginal returns -1; internal consistency failures throw. Probability zero and one also have explicit valid branches.',
        'QList evaluates reciprocal denominators without a local zero guard; the selected observed-probability setter permits NaN. Numerical support and finite outputs require explicit validation.',
        'getUpdatedBayesIm returns null; the wrapper formats numeric marginals and does not provide a typed scientific status certificate in the inspected path.',
        'PdagPagIda documentation mentions PAGs, but its selected constructor admits only legal DAG/PDAG inputs and continuous data, with a comment disabling rPAG-IDA.',
        'An optimal-adjustment exception can append zero, while an outer exception logs and omits a candidate; these are not proof of a zero effect or exhaustive candidate set.',
        'Selected IDA distance functions compare to the interval hull and return trueEffect when effects are empty; neither is a general finite-set distance or calibrated confidence set.'
    ]
    limits=[
        'Nine selected originals at one pre-cutoff revision do not establish complete Java software-market or package-interface coverage.',
        'The source header names a Tian/Pearl2002 report, but its proof PDF was not inspected in this tranche. No theorem, completeness or general latent-ID guarantee is attributed to it.',
        'No Java compilation, Tetrad runtime, downloaded tests, sibling execution or native failure reproduction occurred.',
        'Static paths distinguish risks and intended semantics; graph-method implementation and probability-storage validation remain further inspection obligations.',
        'A PAG-related class name or documentation cannot override the inspected constructor guard; no unsupported graph-class admission is granted.',
        'The authored mechanisms and costs are exact illustrations, not a sharp identified set, empirical model performance or bank ROI.',
        'No software, license, adapter, runtime, deployment or scientific capability is awarded.'
    ]
    source=dict(integrated_citation_key='exec19_javaid_source',kind='software_primary_sources',
        title='Tetrad selected Java identification, evidence, Q-expression and IDA interfaces',author='Tetrad contributors',year=2026,
        source_identity='https://github.com/cmu-phil/tetrad',version_date='7.6.11-SNAPSHOT; '+manifest['commit_date']+'; '+pin,
        local_copy=records[0]['local_copy'],records=records,
        identity_evidence=[ref(RAW/'v12_sw_cutoff_commit_tetrad.json','Preserved cutoff commit identity'),
            ref(RAW/'v12_sw2_tetrad_tree.json','Complete4200-entry selected tree and blob identities')],
        inspected_anchors=[dict(anchor=c,inspection='Selected original source-code path') for c in claims],
        supported_claims=claims,limitations=limits)
    results=exact.calculate();write(BASE/'exact-results.json',results)
    reference=dict(integrated_citation_key='exec19_javaid_reference',kind='project_authored_exact_reference',
        title='Exact lending identification witnesses and intervention-versus-counterfactual reference',
        author='Causal banking proposal project',year=2026,source_identity='tools/java_identification_reference_20261019.py',
        version_date='2026-10-19',local_copy=ref(ROOT/'tools/java_identification_reference_20261019.py','calculate: exact probability enumeration'),
        inspected_anchors=[dict(anchor='calculate()',inspection='Exact positive observed-law and potential-outcome enumeration')],
        supported_claims=['Same positive observed joint law permits intervention effects0 and1/2; assumed net values-20 and80USD.',
            'Same observed and marginal intervention laws permit conditional counterfactual risks0 and1 under different couplings.',
            'Hull distance0 differs from finite-set distance2 for candidates{-2,2} and target0.'],limitations=limits[-2:])
    write(BASE/'source-audit.json',dict(sources=[source,reference],cutoff='2026-10-07',records=records,
        supported_claims=claims,native_execution=False))
    omissions=[dict(item='Other Java candidate and alias coverage',status='open',route='Repeat bounded primary discovery; verify language, ownership and relevant query interfaces before excluding alternatives.'),
        dict(item='Tian/Pearl report named in source header',status='not_inspected_not_cited_as_theorem',route='Acquire genuine correctly named PDF and inspect exact algorithm assumptions before any completeness claim.'),
        dict(item='Graph legality and probability storage helpers',status='not_fully_inspected',route='Inspect Paths legal-PDAG/PAG tests, StoredCellProbsObs support behavior and relevant native tests.'),
        dict(item='General conditional ID, cross-world queries and partial identification',status='not_established',route='Find actual APIs and algorithm contracts; absence in selected files is not package-wide absence.'),
        dict(item='Native subtype, flag, sentinel and numerical behavior',status='not_executed',route='Run a reviewed pinned build against typed adverse references only after executable admission.'),
        dict(item='Complete distribution and rights',status='deferred',route='Bind actual Java dependencies and applicable notices; existing PC reuse choice does not admit these interfaces.')]
    write(BASE/'omissions-register.json',dict(items=omissions,global_blocker=None))
    contract=dict(status='proposed_not_implemented',requirements=[
        'Separate observational evidence, intervention assignments and cross-world conditioning in the request schema.',
        'Initial Identifiability candidate profile permits validated singleton interventions only; reject mixed ordinary-evidence requests until the flag mismatch is resolved.',
        'Validate graph class, node/category bijection, compatible observed JPD subtype, normalized finite support and intervention membership.',
        'Treat probability -1 as a failed algorithm result, null updated model as unavailable, exceptions as failures and nonfinite arithmetic as numerical/support failure.',
        'Do not clamp a negative probability sentinel to zero; signed causal contrasts have a separate type.',
        'Preserve all candidate attempts and skipped/error branches. Exception-added zero cannot be certified as a scientific zero.',
        'Separate a finite effect list, interval hull and confidence set. Empty candidate output is unknown/failed, not identified zero.',
        'Report identified only after verified algorithm/graph premises and completed evaluation; report not_identified only with an applicable reviewed certificate; otherwise unknown or execution_error.',
        'No PAG or cross-world capability follows from names or generic updater documentation.'],integration_allowed=False)
    write(BASE/'conversion-contract.json',contract)
    evidence=[ref(BASE/n,'Scoped source and semantic evidence') for n in ['plan.md','plan-review.json','discovery-search.json',
        'acquisition-manifest.json','dependency-acquisition-manifest.json','source-audit.json','inspected-extracts.json',
        'exact-results.json','omissions-register.json','conversion-contract.json']]
    evidence += [ref(Path(__file__),'Exact review construction')]
    findings=[dict(index=0,verdict='inconclusive',finding='Inherited Tetrad candidate and interfaces are inspected; other Java candidate discovery remains incomplete and empty search responses establish no absence.'),
        dict(index=1,verdict='pass',finding='Nine primary files match pinned Git blobs and acquisition hashes; claims stay within inspected code and exact authored references, without borrowing an uninspected theorem.'),
        dict(index=2,verdict='pass',finding='Alternative query semantics, engine profiles, proof/helper/native gaps and search omissions are explicit; no essential source is waived.')]
    trigger='Resolve other Java candidate coverage and inspect the named algorithm original plus graph/probability helpers; test flag/subtype/sentinel/nonfinite paths in a separately admitted native prototype. Preserve typed identification/unknown/error distinctions.'
    output=dict(operation_id=OP,status='inconclusive',scope='Tetrad Java identification and effect-candidate source comparison',
        reviewer=REVIEWER,cutoff='2026-10-07',candidate_ids=['inherited:tetrad'],selected_revision=pin,
        aliases=['Tetrad','tetrad-lib','IdentifiabilityWrapper GUI'],interfaces=['Identifiability','Ida','PdagPagIda'],
        documented_findings=claims,alternatives=['Reviewed symbolic ID engines in R/Python have distinct graph and proof contracts.',
            'Supplied-model Bayesian updating, observational identification and cross-world counterfactuals are separate operations.',
            'Transparent authored positive-law witnesses remain the proposed small-case oracle.'],
        evidence=evidence,limitations=limits,criteria=findings,revisit_trigger=trigger,
        integration_allowed=False,capabilities=[],coverage_complete=False,bank_inputs_required=False)
    write(OUTPUT,output)
    write(BASE/'review.json',dict(status='inconclusive_for_coverage_pass_for_bounded_source_claims',reviewer=REVIEWER,
        reviewed_output=ref(OUTPUT,'Bounded coverage result'),findings=findings,evidence=evidence,limitations=limits))
    graph,_,_=run.combined(ROOT,state);receipt=run.ledger.receipt_template(run.ledger.operation(graph,OP))
    receipt.update(outcome='inconclusive',execution='performed',scope=output['scope'],reviewer=REVIEWER,
        capabilities=[],outputs=[ref(OUTPUT,'Contracted Java coverage review')],limitations=limits,
        nonexecution_reason='',revisit_trigger=trigger,criteria=[dict(c,evidence=evidence+[ref(BASE/'review.json','Author review')]) for c in findings])
    write(BASE/'operation-receipt.json',receipt);verify_bindings([output,receipt])
    print(json.dumps(dict(operation=OP,outcome='inconclusive',primary_files=9,exact_reference='pass',native_Java_execution=False)))


if __name__=='__main__':main()

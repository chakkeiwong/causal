#!/usr/bin/env python3
"""Audit latest cutoff LLAMIA original and preserve a scoped census successor."""
import json
from collections import Counter
from copy import deepcopy
from pathlib import Path
import collaboration_reference_20261024 as exact
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-24/census-language-collaboration-v1'
PRIOR = ROOT / 'docs/program/execution/2026-10-23/census-recon-memory-v1'
RAW = ROOT / 'docs/literature/raw'
TITLE = 'Exploring Collaboration between a language and a non-language agent'
PDF = ROOT / ('docs/papers/' + TITLE + ' S I(2026).pdf')
LIMITS = [
    'Selected primary text, raw extraction and authored arithmetic inspected; no downloaded code, training, upstream tests or live models executed.',
    'Reported empirical results remain unverified. Contradictory tables and contracts require experiment identities and author artifacts; no fabrication allegation.',
    'The latest version listed before the client cutoff is v2, 2 September 2026. v1 acquisition is retained without substituting it for v2.',
    'No new image previews; extraction warnings and exhausted visual allowance leave visual acceptance open.',
    'Chess and Go representation experiments do not qualify bank intervention identification, uncertainty, operating reliability or adoption.',
]
read = lambda p: json.loads(p.read_text())


def main():
    assert not (BASE / 'review.json').exists()
    raw = RAW / 'exec24_census_collaboration_pdf_v2.pdf'
    receipt = read(raw.with_suffix('.receipt.json'))
    assert receipt['status'] == 'saved' and raw.read_bytes().startswith(b'%PDF-')
    import hashlib
    assert hashlib.sha256(raw.read_bytes()).hexdigest() == receipt['sha256']
    assert not PDF.exists()
    PDF.write_bytes(raw.read_bytes())
    html = (RAW / 'exec24_census_collaboration_abs_v2.html').read_text()
    assert '2 Sep 2026 04:33:39' in html and 'Harini' in html
    text = (BASE / 'original-v2.txt').read_text()
    pages = text.split(chr(12))
    assert len([x for x in pages if x.strip()]) == 46
    rawtext = (BASE / 'original-v2-raw.txt').read_text().split(chr(12))
    checks = [(27, '57 54 60 57'), (28, '44.0 ±1.2 56.6 ±1.4 50.3'),
              (30, '91.5 0.67 ±0.02'), (31, '53 ±1 49 ±1 71 ±2 52 ±2 45.8')]
    for page, token in checks:
        assert token in ' '.join(rawtext[page - 1].split()), (page, token)
    specs = [
        (1, 9, 'Six chess task scores and reported gains motivate interface research; the abstract-wide superiority wording is narrower than the MAIA expert comparison in Tables14/18.'),
        (4, 6, 'Frozen specialist activations pass through a learned32-token projector; both variants receive verbal outputs. The projector and LLM are jointly trained in Stage2; empirical ablation is not a universal text impossibility theorem.'),
        (17, 19, 'Table2 training overhead at8B is12%, not within approximately6% at every scale. Table3 calls times return tokens excludes other prompt/output/context and training costs.5M pairs,32GPUs and training steps need exact elapsed/GPU-hour accounting.'),
        (20, 23, 'Data protocol reports100 commentary games and5000 puzzles; FEN disjointness and low-view selection have distinct leakage limits. Community-interest labels are not causal effects or intrinsic utility.'),
        (24, 25, 'Text/template/probe baselines are selected implementations. The observed failure of a limited probe or top-k summary does not prove impossibility of a sufficient typed text channel.'),
        (27, 31, 'Table14 Wild14B mean57 disagrees with headline49; Table15 rationale50.3 disagrees with45.8; Table17 difficulty0.67 disagrees with0.71. Raw and layout extraction agree; no corrected performance value is chosen.'),
        (29, 30, 'Table16 describes approximately300 games and Table17 approximately1000 puzzles, unlike100/5000 protocol counts. Table17 retains XX.X for one solved result. Exact evaluated row sets and run IDs are required.'),
        (31, 35, 'Interface and architecture ablations are reported. The paper explicitly acknowledges architecture, size and projector compatibility confounds; a ratio of correlations is not a ratio of decision benefit.'),
        (36, 41, 'Twelve screened raters and15 positions form180 crossed judgments.130/180 and130/162 reproduce72.2% and80.2% with different tie denominators. Pooled ratio differs from average per-rater ratios when ties vary.'),
        (42, 43, 'Stage2 description includes500K human-move-labelled examples despite earlier no-human-move-supervision language. Reward target, teacher policy and sampling clocks need explicit reconciliation.'),
        (44, 46, 'J.3 excludes read-only get_policy from re-encoding, but J.4.3 says get_policy injects fresh32-token state. Sequential mutations and parallel reads need state-version binding; prompt forbids refusal, unsuitable for automatic adoption in bank inference.'),
        (46, 46, 'Internal-activation access is required; closed specialist access is a stated limitation. A standard text tool result alone is not a demonstrated embedding-injection interface.'),
    ]
    source = dict(integrated_citation_key='exec24_collaboration_original', kind='paper',
        title=TITLE, filename_title=TITLE, author='Harini S I and Somesh Singh and Yaman K Singla and Rajiv Ratn Shah and David Doermann and Balaji Krishnamurthy',
        first_author='S I', year=2026, source_identity='https://arxiv.org/abs/2609.00474v2',
        version_date='v2; 2 September 2026 04:33:39 UTC; latest listed version before 2026-10-07 cutoff',
        local_path=str(PDF.relative_to(ROOT)), sha256=receipt['sha256'], local_copy=ref(PDF,'Genuine46-page v2 original'),
        identity_evidence=[ref(RAW / n,'Original acquisition and archive identity') for n in ['exec24_census_collaboration_abs_v2.html','exec24_census_collaboration_abs_v2.receipt.json','exec24_census_collaboration_pdf_v2.receipt.json']],
        inspected_anchors=[dict(anchor=f'PDF pages {a}-{b}',pages=[a,b],finding=f,text_extract=ref(BASE/'original-v2.txt',f'Form-feed pages {a}-{b}')) for a,b,f in specs],
        supported_claims=[f for _,_,f in specs], limitations=LIMITS)
    project = dict(integrated_citation_key='exec24_collaboration_reference',kind='project_derivation_and_exact_reference',
        title='Authored interface sufficiency, table arithmetic and crossed-rating reference',author='Causal banking proposal project',year=2026,
        source_identity='tools/collaboration_reference_20261024.py',version_date='24 October 2026; exact stipulated examples',
        local_copy=ref(ROOT/'tools/collaboration_reference_20261024.py','calculate'),inspected_anchors=['calculate: exact arithmetic, binary state/action law, crossed rater-position variance'],
        supported_claims=['Selected published table entries disagree; no empirical value is repaired by arithmetic.',
            'A stipulated binary bank state gives USD100 expected savings with a sufficient typed bit or full state, versus0 with a constant summary.',
            'For12 raters and15 positions with independent unit-variance random effects, mean variance is3/20 versus erroneous iid1/90.',
            'Tool-return token totals and all-judgment versus non-tie denominators have distinct interpretations.'],limitations=LIMITS)
    write(BASE/'source-audit.json',dict(sources=[source,project],cutoff='2026-10-07',native_execution=False))
    assert exact.calculate()==read(BASE/'exact-results.json')
    write(BASE/'plan-review.json',dict(status='pass',evidence=[ref(BASE/'source-audit.json','Versioned originals and authored checks')],
        steps=['Inspect latest cutoff original and preserve both versions.','Reconcile method, denominators, metrics, costs, training target and state-refresh rules.','Develop a sufficient typed-interface banking counterexample and public trial design.','Integrate preserving reader/sponsor successors, renew exact-reader checks, and retain all unresolved gates.'],
        risks=['Do not silently select one contradictory result.','Text losslessness is only a decision-specific existence example, not an efficiency claim.','Do not make API injection or bank causal-identification claims from chess performance.']))
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_checks',evidence=[ref(BASE/'source-audit.json','Primary definitions'),ref(BASE/'exact-results.json','Exact rational arithmetic')],
        findings=['8B overhead is3/25; averages57 and50.3 differ from reported headline49 and45.8.','Binary state is stipulated identified input: +/-USD200 action advantages produce USD100 value of sufficient information, no bank empirical claim.','Crossed-effects variance sums rater and position components; repeated judgments do not create180 independent people.','Finite representation may be serialized; this proves existence, not bounded-context learnability or compression efficiency.']))
    omissions = [
        ('Exact experiments','Obtain frozen run/checkpoint IDs, row manifests, evaluated denominators, seeds, code and author reconciliation for Tables14-18 and the100/300 and5000/1000 counts.'),
        ('Native interface','Resolve get_policy versus mutation refresh; specify hidden layer, checkpoint, pooling, precision, projector and state/version custody; register conformance before executing downloaded code.'),
        ('Training/economics','Resolve human-move reward and no-supervision wording, reference/old projector likelihoods, zero-variance groups and full training/inference metering.'),
        ('Public comparison','Compare top-k prose, complete typed records, latent-only, text-plus-latent, shuffled/missing state and no-specialist under fixed tasks and split custody.'),
        ('Uncertainty/rights','Obtain game/player and rater/position sampling records, repeated-seed variability, judge identities and corpus/model/dependency licenses.'),
        ('Visual/external','Fresh image allowance, independent review and later authentic bank validation remain open; none blocks source work.'),
    ]
    write(BASE/'omissions-register.json',dict(items=[dict(gap=g,next_action=a) for g,a in omissions],global_blocker=None))
    write(BASE/'copyedit-review.json',dict(status='pass',evidence=[ref(BASE/'development.tex','Connected banking argument'),ref(BASE/'sponsor-addition.md','Sponsor decision')],
        findings=['Clearly distinguish reported observations, unresolved inconsistencies and authored examples.','Preserve useful latent-interface hypothesis without promising text impossibility, native integration or bank validity.'],visual_acceptance=False))
    register=deepcopy(read(PRIOR/'census-register.json'));old=deepcopy(register)
    row=next(x for x in register['items'] if x['id']=='LA01-candidate-164');assert row['disposition']=='open_original_not_inspected'
    row.update(prior_disposition=row['disposition'],disposition='inspected_primary_retained_with_limits',technical_source_review_open=False,
        source_key=source['integrated_citation_key'],primary_source_record=source,publication_keys=[source['integrated_citation_key'],project['integrated_citation_key']],
        task_families=['agent_architecture','estimation_validation','evaluation_cost','data_code'],mapping_basis='Non-language specialist interface, state custody and empirical evaluation; not causal discovery qualification.',
        availability='Genuine46-page v2 original acquired; v1 preserved; raw and layout text inspected; visual acceptance open.',
        effect_on_claims='Retain a prospective latent-interface experiment; withhold performance ranking, universal verbalization and cost-neutrality claims.',
        next_action='Reconcile primary table/harness/training contracts, acquire exact released artifacts and register matched typed-versus-latent experiments.')
    assert all(x==next(y for y in register['items'] if x['id']==y['id']) for x in old['items'] if x['id']!=row['id'])
    counts=dict(Counter(x['disposition'] for x in register['items']));assert counts['inspected_primary_retained_with_limits']==73 and counts['open_original_not_inspected']==40
    register.update(counts=counts,supersedes=ref(PRIOR/'census-register.json','Preserved72/41 baseline'),changes=['Only candidate164 changes;113 identities and all other dispositions preserved.'],closure=False,interpretation='73 of113 originals inspected;40 unread;four crosscutting obligations remain.')
    write(BASE/'census-register.json',register)
    mapping=deepcopy(read(PRIOR/'task-map.json'))
    for family in mapping['task_families']:
        if row['id'] in family.get('uninspected_candidate_ids',[]):family['uninspected_candidate_ids'].remove(row['id'])
        if family['id'] in row['task_families']:
            for field,vals in [('inspected_candidate_ids',[row['id']]),('inspected_source_keys',row['publication_keys'])]:
                family.setdefault(field,[]);family[field].extend(x for x in vals if x not in family[field])
        family['coverage_acceptance']=False
    mapping.update(register=ref(BASE/'census-register.json','73/40 successor'),supersedes=ref(PRIOR/'task-map.json','Preserved mapping'));write(BASE/'task-map.json',mapping)
    evidence=[ref(BASE/n,'Reviewed source, arithmetic and bounded proposal') for n in ['source-audit.json','plan-review.json','mathematical-review.json','copyedit-review.json','exact-results.json','development.tex','sponsor-addition.md','omissions-register.json','census-register.json','task-map.json','version-changes.json']]+[ref(Path(__file__),'Preserving audit logic')]
    review=dict(status='pass_for_scoped_adverse_source_review',reviewer=dict(name='Codex author/coordinator',kind='author'),candidate='LA01-candidate-164',evidence=evidence,
        findings=['Latest cutoff v2 source inspected; no empirical ranking or native result reproduced.','Useful interface hypothesis retained with table, training, refresh, cost and sampling contradictions explicit.','Sufficient typed text is a substantive comparator; truth and identification remain separately declared.','Only candidate164 advances;73 inspected/40 unread with four crosscutting tasks open.'],limitations=LIMITS,coverage_acceptance=False,native_execution=False,visual_acceptance=False)
    verify_bindings(review);write(BASE/'review.json',review)
    write(BASE/'progress.json',dict(finding='Candidate164 v2 inspected; typed-interface alternative, empirical inconsistencies and crossed uncertainty developed. Census73/40; no coverage closure.',
        next_action='Integrate the collaboration review into preserving monograph and sponsor successors and renew exact-reader checks; continue40 unread originals and four crosscutting tasks. No native, visual or final acceptance.',
        yield_reason='Release operation for exact-byte publication while preserving scoped progress; not a global stop.',evidence=[ref(BASE/'review.json','Scoped review'),ref(BASE/'census-register.json','73/40 census')]))
    print(json.dumps(dict(inspected=73,unread=40,scholarly_pages=46,coverage_closed=False)))


if __name__=='__main__':main()

#!/usr/bin/env python3
"""Review pinned native latent-discovery sources; never execute upstream code."""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
import hashlib
import json
from pathlib import Path

import run_program as control

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'docs/literature/raw'
BASE = ROOT / 'docs/program/execution/2026-10-14/cxx-latent'
OP = 'SW.CELL.discovery_latent.Cxx'
OUTPUT = ROOT / f'docs/program/comprehensive-v14/work/{OP}/coverage-review.json'


def ref(path, anchor):
    return {'path': str(path.relative_to(ROOT)),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'anchor': anchor}


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False, allow_nan=False)
        stream.write('\n')


def exact():
    # A project-level representation oracle, not execution of PAG::toMixedGraph.
    groups = defaultdict(list)
    rows = []
    for left, right in product(['circle', 'tail', 'arrow'], repeat=2):
        converted = ('two_arcs' if left == right == 'arrow' else
                     'x_to_y' if right == 'arrow' else
                     'y_to_x' if left == 'arrow' else 'undirected')
        groups[converted].append([left, right])
        rows.append({'left': left, 'right': right, 'generic_conversion': converted})
    assert len(rows) == 9 and sorted(map(len, groups.values())) == [1, 2, 2, 4]
    assert ['circle', 'arrow'] in groups['x_to_y'] and ['tail', 'arrow'] in groups['x_to_y']
    observed = []
    for u, v in product([0, 1], repeat=2):
        mass = F(1, 2) * (F(3, 4) if v == 0 else F(1, 4))
        observed.append({'offer': u, 'recovery_USD': 100 + 20*u + 5*v, 'mass': str(mass)})
    assert sum(F(r['mass']) for r in observed) == 1
    # Same observed law: A=U and Y=100+20U+5V, versus randomized A and Y=100+20A+5V.
    effects = [F(0), F(20)]
    net = [e-F(8) for e in effects]
    assert net == [F(-8), F(12)]
    return {'kind': 'exact_project_algebra', 'upstream_execution': False,
            'endpoint_pairs': rows, 'generic_conversion_classes': dict(groups),
            'serialized_pair_count': 9, 'distinct_generic_outputs': 4,
            'validity_limit': 'Nine local endpoint combinations are a representation check, not nine globally valid PAGs.',
            'borrower_example': {'law': 'U~Bernoulli(1/2), V~Bernoulli(1/4), independent; independent accounts.',
                'observed_distribution_both_worlds': observed,
                'hidden_risk_world': 'A=U; Y=100+20U+5V. Intervention replaces only A equation.',
                'direct_world': 'A~Bernoulli(1/2), independent V; Y=100+20A+5V.',
                'ATE_USD': list(map(str, effects)), 'offer_cost_USD': '8',
                'net_offer_value_USD': list(map(str, net)),
                'limit': 'Stipulated observational equivalence; no bank data, estimated model or discovered graph.'}}


def inspect(repo, pin, tree_file, head_file, selections):
    tree = json.loads((RAW/tree_file).read_text())
    head = json.loads((RAW/head_file).read_text())
    head = head[0] if isinstance(head, list) else head
    assert head['sha'] == tree['sha'] == pin and tree['truncated'] is False
    date = head['commit']['committer']['date']
    assert date[:10] <= '2026-10-07'
    indexed = {r['path']: r for r in tree['tree']}
    records = []
    for key, upstream, anchor, claims in selections:
        path = RAW/(key+'.txt')
        receipt_path = RAW/(key+'.receipt.json')
        receipt = json.loads(receipt_path.read_text())
        data = path.read_bytes()
        blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        url = f'https://raw.githubusercontent.com/{repo}/{pin}/{upstream}'
        assert receipt['url'] == url and receipt['status'] == 'saved'
        assert receipt['sha256'] == hashlib.sha256(data).hexdigest()
        assert indexed[upstream]['sha'] == blob, upstream
        records.append({'source_identity': url, 'revision': pin, 'source_date': date,
            'acquired_utc': receipt['accessed_utc'], 'local_copy': ref(path, anchor),
            'acquisition_receipt': ref(receipt_path, 'Original HTTPS acquisition'),
            'git_blob_sha1': blob, 'tree_identity_verified': True,
            'inspected_anchors': [anchor], 'supported_claims': claims})
    return {'repository': repo, 'revision': pin, 'source_date': date,
            'tree': ref(RAW/tree_file, 'Complete pinned tree; selected blob identities verified'),
            'head': ref(RAW/head_file, 'Identity and cutoff only'), 'records': records,
            'upstream_execution': False}


def main():
    assert not OUTPUT.exists() and not (BASE/'operation-receipt.json').exists()
    prefix = 'exec14_cxx_latent_'
    agrum = inspect('agrumery/aGrUM', '2ec71906f4108684c5cfb96d1d44f2925e16a32e',
        'v12_sw2_tree_agrum.json', 'v12_sw_cutoff_commit_agrum.json', [
        (prefix+'fci_h', 'src/agrum/BN/learning/FCI.h', 'lines 1-34 and FCI class/options',
         ['Selected file declares LGPL-3.0-or-later OR MIT; source includes FCI parameters and native PAG interface.']),
        (prefix+'fci_cpp', 'src/agrum/BN/learning/FCI.cpp', 'lines 248-347, 818-876',
         ['Possible-D-Sep traversal has a semidirected-path filter and starts subset sizes at two; theorem/engine qualification is not established by comments.',
          'learnPAG performs skeleton, collider, possible-D-Sep and R1-R10 phases; generic bridge converts and resolves double-headed arcs.']),
        (prefix+'pag_h', 'src/agrum/base/graphs/PAG.h', 'lines 59-145',
         ['markAt(src,dst) denotes the mark at dst. Circle, tail and arrowhead are distinct.']),
        (prefix+'pag_cpp', 'src/agrum/base/graphs/PAG.cpp', 'lines 179-201',
         ['toMixedGraph tests only arrowheads; circle/tail pairs collide, and bidirected edges become two arcs.']),
        (prefix+'miic_cpp', 'src/agrum/BN/learning/Miic.cpp', 'lines 143-163, 315-350, 674-684',
         ['Native MIIC uses mixed graphs and an additional latent-couple list; it is not the FCI native PAG route.']),
        (prefix+'simplemiic_cpp', 'src/agrum/BN/learning/SimpleMiic.cpp', 'lines 98-106, 214-292, 613-654, 818-823',
         ['SimpleMiic has mixed/PDAG/completion paths and a latent-couple accessor; no latent bank state is recovered here.']),
        (prefix+'fci_test', 'src/testunits/module_BN/FCITestSuite.h', 'lines 298-355, 423-437, 532-610',
         ['Upstream fixture source includes PAG shape, latent-list and possible-D-Sep tests; none was executed in this review.']),
        ('exec13_cxx_agrum_ibase_cpp', 'src/agrum/BN/learning/BNLearnUtils/IBNLearner.cpp', 'lines 933-954',
         ['learnPAG requires FCI and rejects missing values in the selected BNLearner route.']),
        ('exec13_cxx_agrum_constraint', 'src/agrum/BN/learning/ConstraintBasedLearning.cpp', 'lines 204-247',
         ['Double-headed resolver can erase one arc or, in its fallback, both arcs. It is not an endpoint-preserving serializer.'])])
    miic = inspect('miicTeam/miic_R_package', '9bb87a2ac02041f81ee63a57c3ec25e99bb25609',
        prefix+'miic_r_tree.json', prefix+'miic_r_commit.json', [
        (prefix+'miic_r_readme', 'README.md', 'Prerequisites, Installation, License; lines 10-26',
         ['R/C++ package, documented C++14 compiler requirement, declared temporal and latent modes; prose is not a reliability guarantee.']),
        (prefix+'miic_r_description', 'DESCRIPTION', 'Version, License, Imports and LinkingTo fields',
         ['Version 2.0.4, GPL >=2 declaration; Rcpp linking and ppcor/scales/stats imports.']),
        (prefix+'miic_r_license', 'LICENSE', 'GPL version 3 header and complete license text',
         ['GPL-3 full text is bundled; reconcile with README GPL-2|GPL-3 and DESCRIPTION >=2 before redistribution.']),
        (prefix+'miic_r_makevars', 'src/Makevars', 'complete two OpenMP assignments',
         ['OpenMP flags are delegated to R; this file does not by itself establish a compiler standard or passing build.']),
        (prefix+'miic_r_api', 'man/miic.Rd', 'lines 172-214, 431-559',
         ['Latent default is orientation, not yes; output keeps adjacency codes, endpoint scores, cycle/consensus fields and confidence ratio.',
          'Documentation labels probability-matrix entries as the row endpoint; preserve this convention question pending wrapper trace.']),
        (prefix+'miic_r_orientation', 'src/orientation.cpp', 'lines 32-48, 66-80, 198-214',
         ['Orientation acceptance is (1-p)/p < threshold; native edge(x,y).proba_head receives x2y.']),
        (prefix+'miic_r_parse', 'R/parseResults.R', 'lines 238-256, 284-359',
         ['Summary p_x2y indexes matrix[x,y], unlike the manual row-endpoint reading; causality labels are gated by latent and not propagation.']),
        (prefix+'miic_r_reconstruct', 'src/reconstruct.cpp', 'lines 29-59, 84-157',
         ['Rcpp native reconstruction has explicit interrupted results, iteration/cycle status and multiple raw outputs.']),
        (prefix+'miic_r_utilities', 'src/utilities.cpp', 'lines 189-232',
         ['Native adjacency/probability serializers flatten at Y+X*n; a later R matrix-construction step is required to settle exported direction.']),
        (prefix+'miic_r_structure', 'src/structure.h', 'lines 239-253',
         ['Native edge stores orientation probability separately from connection status.'])])
    rcmgm = inspect('cran/rCausalMGM', '9e0101244c379a33a1329dfdcb6b9ffcb01fb0d4',
        'exec13_cxx_lead_4_tree.json', 'exec13_cxx_lead_4_commit.json', [
        (prefix+'rcmgm_fci_api', 'man/fciStable.Rd', 'complete interface and return contract',
         ['Documented FCI-Stable returns PAG; mixed input types, missing-row deletion, initial skeleton, four orientation rules and possible-D-Sep switch are material.']),
        (prefix+'rcmgm_fci', 'src/Fci.cpp', 'lines 67-184, 239-256',
         ['Source resets circles, prunes with RFCI R0, optionally performs possible-D-Sep, and delegates final orientations.']),
        (prefix+'rcmgm_edge', 'src/inc/Edge.hpp', 'lines 6-16, 58-79',
         ['Two endpoint fields include circle/tail/arrow and extra star/null states that need explicit rejection or representation.']),
        (prefix+'rcmgm_graph', 'src/EdgeListGraph.cpp', 'lines 365-402, 1687-1740',
         ['R graph list keeps edge strings, algorithm/type and ambiguous triples; selected parser accepts only specific endpoint spellings and splits nodes on spaces.']),
        (prefix+'rcmgm_r_export', 'R/RcppExports.R', 'lines 454-477',
         ['R fciStable delegates native call with explicit defaults; no external execution follows from source inspection.']),
        ('exec13_cxx_lead_4_source_0', 'DESCRIPTION', 'version, License, Imports, LinkingTo',
         ['Version 1.0.1 declares GPL-3 and Rcpp/Armadillo/Thread/BH dependencies; full derivative notice closure remains separate.'])])
    packages = [agrum, miic, rcmgm]
    queries = []
    hits = []
    for name in ['fci', 'miic']:
        p = RAW/(prefix+'search_'+name+'.json')
        data = json.loads(p.read_text())
        receipt = json.loads(p.with_name(p.stem+'.receipt.json').read_text())
        queries.append({'url': receipt['url'], 'accessed_utc': receipt['accessed_utc'],
                        'total_count': data['total_count'], 'returned': len(data['items']),
                        'incomplete_results': data['incomplete_results'], 'bound': 30,
                        'response': ref(p, 'All returned discovery identities, not capability evidence')})
        hits += data['items']
    dispositions = {
        'miicTeam/MIIC': 'Relevant archived alias; pinned README redirects to miicTeam/miic_R_package, reviewed here.',
        'FoofooTheGuy/Miichanic_Plugin': 'Discovery metadata describes a Mii Maker plugin; out of causal scope, no technical claim.',
        'MissingNo42/MiiCraft': 'Discovery metadata describes Minecraft for Wii; out of causal scope.',
        'Kiratopat-s/MIIC1222': 'Pinned labfinal/final.cpp defines string/sort exercises; out of causal scope.',
        'Kiratopat-s/MIIC1225': 'Discovery metadata describes operating-systems coursework; out of causal scope.',
        'Asterki/miichi': 'Discovery metadata describes a walking-cat controller; out of causal scope.',
        'sguo1129/miica_mss': 'Discovery metadata describes a Landsat algorithm; out of causal scope.',
        'snvasuncion/MiiCard': 'Pinned README is a Flutter starter; out of causal scope.'}
    assert set(dispositions) == {x['full_name'] for x in hits}
    oa = json.loads((RAW/'v12_sw_cell_discovery_latent_cpp.json').read_text())
    leads = [{'id': x['id'], 'title': x['title'], 'date': x['publication_date'], 'doi': x.get('doi'),
              'disposition': 'uninspected_methodology_lead_not_cited',
              'next': 'Acquire genuine original and locate a pinned implementation before assigning native capability.'} for x in oa['results']]
    omissions = [
        {'id': 'MIIC-original-methods', 'gap': 'Selected API/source inspected; linked 2017/2024 methodological originals not locally acquired for this review.',
         'impact': 'No consistency, calibration, scale or missingness-detection theorem accepted from README/manual claims.',
         'next': 'Acquire and inspect genuine originals for DOI 10.1371/journal.pcbi.1005662 and 10.1016/j.isci.2024.109736 with named PDFs and hashes.'},
        {'id': 'MIIC-endpoint-export', 'gap': 'Manual row-endpoint language and summary p_x2y indexing need final R matrix reshaping trace.',
         'impact': 'Executable conversion admission withheld.',
         'next': 'Inspect R/miic.reconstruct.R plus utilities; freeze a two-node asymmetric endpoint fixture and then execute the pinned wrapper.'},
        {'id': 'native-FCI-qualification', 'gap': 'Selected source phases are not proof of algorithmic completeness or finite-sample graph coverage.',
         'impact': 'No FCI engine qualification or causal-effect interval claim.',
         'next': 'Compare possible-D-Sep and orientation implementations against primary theory and independent tiny oracle graphs, including selection and bounded-search cases.'},
        {'id': 'distribution-rights-runtime', 'gap': 'Selected declarations do not close file/dependency rights, build or wrapper behavior.',
         'impact': 'No executable native or R adapter admitted.',
         'next': 'Resolve notices/derivatives, pin dependency environment and run export, missingness, interruption and numerical fixtures.'},
        {'id': 'bounded-search', 'gap': 'Ten of 82 OpenAlex records and two finite GitHub query routes; no saturation or complete historical index.',
         'impact': 'Whole-cell completeness remains inconclusive.',
         'next': 'Triage original leads and alias references; extend relevant native package searches and document a justified coverage stopping rule.'}]
    write(BASE/'primary-review.json', {'cutoff': '2026-10-07', 'acquired_after_cutoff': True,
        'packages': packages, 'supported_scope': 'Pinned static source capabilities and limits only',
        'no_new_scholarly_citations': True, 'upstream_execution': False})
    write(BASE/'exact-oracle.json', exact())
    write(BASE/'candidate-register.json', {'cutoff': '2026-10-07', 'queries': queries,
        'operational_stopping_rule': 'Two finite repository queries, all returned identities, known native alternatives, one-hop MIIC successor and selected delegated source paths; not preregistered or exhaustive.',
        'index_limit': 'Current metadata filtered by creation date; commit pins separately bound technical claims. Zero FCI hits do not imply absence.',
        'query_candidates': [{'repository': x['full_name'], 'description': x.get('description'), 'disposition': dispositions[x['full_name']]} for x in hits],
        'known_native_candidates': [{'repository': p['repository'], 'pin': p['revision']} for p in packages],
        'aliases': {'aGrUM/pyAgrum': 'One native engine with bindings; FCI, Miic and SimpleMiic are distinct paths.',
            'miicTeam/MIIC -> miicTeam/miic_R_package': 'Legacy source redirects to R/C++ successor; no equality to aGrUM MIIC assumed.',
            'cran/rCausalMGM': 'Pinned CRAN mirror; upstream derivative and release equivalence remain separate.',
            'pcalg': 'Existing R FCI/RFCI alternative; native dependencies do not count as a new independent engine.'},
        'alias_evidence': [ref(BASE/'miic-readme.txt', 'Decoded pinned original redirects to successor'),
                          ref(RAW/(prefix+'miic_readme.json'), 'Unmodified GitHub contents response'),
                          ref(RAW/(prefix+'ambiguous_course_final.txt'), 'Sorting/string exercise'),
                          ref(BASE/'miicard-readme.txt', 'Decoded pinned Flutter README')],
        'inherited_native_candidates': ref(ROOT/'docs/program/execution/2026-10-13/cxx-discovery/candidate-register.json', '17 prior native/hosted/inference leads; no new latent capability inferred for uninspected paths'),
        'openalex_response': ref(RAW/'v12_sw_cell_discovery_latent_cpp.json', 'First ten of 82 metadata results'),
        'uninspected_scholarly_leads': leads, 'full_cell_coverage_accepted': False})
    write(BASE/'omissions-register.json', {'items': omissions, 'essential_source_waiver': False,
        'other_leads': leads, 'unavailable_original_substituted': False})
    contract = {'status': 'proposed_not_implemented', 'first_choice': 'aGrUM native FCI learnPAG with explicit endpoint serializer',
        'alternatives': ['rCausalMGM FCI-Stable through its R contract', 'MIIC R/C++ through a distinct MIIC graph/score contract', 'Existing pcalg R FCI/RFCI path'],
        'not_selected': {'PAG::toMixedGraph': 'Lossy endpoint representation; subsequent double-head resolution discards additional information.',
            'direct_MIIC_port': 'No demonstrated deployment need justifies owning its R preprocessing, code semantics and GPL obligations.',
            'generic_DAG_completion': 'Chooses unsupported orientation and cannot establish an intervention target.'},
        'required_context': ['Pinned engine and environment', 'variable ID and data-column mapping', 'graph kind and per-node endpoint marks',
            'CI method, thresholds, conditioning/path bounds and prior constraints', 'sampling unit, observation clock and selection/missingness assumptions',
            'all unavailable/interrupted results and raw graph before conversion'],
        'failure_rules': ['Reject unknown node IDs, duplicate edges and unsupported endpoint tokens.',
            'Keep circle distinct from tail; never map bidirected edges to a two-cycle in a DAG.',
            'Keep MIIC scores and consensus cycles; do not label them confidence intervals for effects or FCI-PAG probabilities.',
            'Do not silently delete missing rows; require an explicit complete-case target and selection justification or refuse.',
            'Require graph/effect identification after discovery; refuse unsupported effect or precision claims.'],
        'oracles': ['Nine local mark-pair round trips and graph/node permutation invariance',
            'Named selection, latent-confounding, collision and bounded-search cases',
            'Asymmetric MIIC matrix fixture and rCausalMGM string round-trip including unsupported marks',
            'Retained cancellation, empty/partial results, row selection and resource caps'],
        'integration_allowed': False, 'runtime_qualified': False,
        'bank_example': ref(BASE/'exact-oracle.json', 'Equal observation laws; causal effects 0 and 20, net values -8 and 12')}
    write(BASE/'conversion-contract.json', contract)
    evidence = [ref(BASE/'candidate-register.json', 'Candidate and alias census with bounds'),
        ref(BASE/'primary-review.json', 'Pinned original bytes and inspected source claims'),
        ref(BASE/'omissions-register.json', 'Essential sources and exact continuation'),
        ref(BASE/'conversion-contract.json', 'Proposed lossless boundary and alternatives'),
        ref(BASE/'exact-oracle.json', 'Representation and hidden-risk reference'),
        ref(Path(__file__), 'Source custody and exact reproduction')]
    findings = ['All eight new repository hits, relevant successor, three native candidates, inherited alternatives and ten scholarly leads are identified; comprehensive lead/alias closure is still open.',
        'Twenty-five selected primary blobs match pinned tree identities; claims are static-source observations. No new scholarly technical claim relies on metadata.',
        'Omissions, source needs, alternatives, lossy conversion and exact next actions are retained; no essential-source waiver or executable admission.']
    count = sum(len(p['records']) for p in packages)
    findings[1] = findings[1].replace('Twenty-five', str(count))
    write(BASE/'author-review.json', {'outcome': 'inconclusive', 'reviewer': {'name': 'Codex author/coordinator', 'kind': 'author'},
        'findings': findings, 'source_blobs': count, 'evidence': evidence,
        'plan_review': ['Follow the archived MIIC alias before selecting a package.',
            'Include inherited native R backends; language-filter search alone misses candidates.',
            'Keep endpoint serialization separate from scientific graph validity and interval qualification.',
            'Do not use missing originals or runtime work to block independent proposal writing.'],
        'full_cell_coverage_accepted': False})
    review = {'operation': OP, 'outcome': 'inconclusive', 'execution': 'performed',
        'scope': 'Expanded source-grounded native latent-discovery comparison and proposed conversion contract',
        'evidence': evidence, 'review': ref(BASE/'author-review.json', 'Criterion review'),
        'runtime_qualified': False, 'full_cell_coverage_accepted': False,
        'next_action': 'Resolve MIIC primary-method and matrix-export issues, complete relevant native lead/alias triage, then review a successor; independent lanes continue.'}
    write(OUTPUT, review)
    graph, _, _ = control.combined(ROOT, control.core.read(ROOT, control.core.STATE))
    node = control.ledger.operation(graph, OP)
    receipt = control.ledger.receipt_template(node)
    receipt.update(outcome='inconclusive', execution='performed', scope=review['scope'],
        reviewer={'name': 'Codex author/coordinator', 'kind': 'author'},
        limitations=['Full native-latent coverage and methodological original review remain open.',
                    'No upstream engine, actual integration, effect-interval or bank validation executed.'],
        outputs=[ref(OUTPUT, 'Bounded inconclusive coverage review')],
        revisit_trigger=review['next_action'], nonexecution_reason='')
    for c, finding, verdict in zip(receipt['criteria'], findings, ['inconclusive', 'pass', 'pass']):
        c.update(verdict=verdict, finding=finding, evidence=evidence[:5])
    write(BASE/'operation-receipt.json', receipt)
    print(json.dumps({'outcome': 'inconclusive', 'native_candidates': len(packages), 'source_blobs': count,
                      'representation_oracle': 'pass', 'integration_allowed': False}))


if __name__ == '__main__':
    main()

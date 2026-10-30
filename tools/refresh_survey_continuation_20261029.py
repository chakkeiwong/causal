"""Apply the observed survey delta after the earlier scientific finalizer."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PREFIX = 'docs/scientific-gap-closure/2026-10-29/'

def apply_state(state):
    audit = ROOT / (PREFIX+'survey-source-audit.json')
    if not audit.exists():
        return
    json.loads(audit.read_text())
    additions = [PREFIX+'survey-source-audit.json', PREFIX+'survey-continuation-results.json']
    for task in state['tasks']:
        if task['id'] == 'SOFTWARE-CONSEQUENTIAL':
            task['action'] = ('Pinned did DESCRIPTION now matches the selected API commit; DoubleML, did and causaleffect have explicit conditional proposal roles. Digital Worker Factory/System of Work is the named current commercial comparator. Continue the exact essential candidate omissions and versioned commercial method questions; complete distributions and native qualification remain prototype work.')
            task['evidence'] = list(dict.fromkeys(task['evidence']+additions))
        if task['id'] == 'FRONTIER-ORIGINALS':
            task['action'] = ('85 inspected/28 unread remain. New eScholarship routes returned403, Unisabana returned a challenge, and two UAH PDF routes timed out/disconnected. UAH identity alone is not technical support. Continue other distinct complete originals; do not repeat these requests or the truncated UPM copies unchanged.')
            task['evidence'] = list(dict.fromkeys(task['evidence']+[PREFIX+'survey-source-audit.json']))
    for item in state['items']:
        if item['id'] == 'S01':
            item['latest_progress'] = 'Conditional estimator/identification reuse made explicit; did same-commit metadata resolved; named current commercial service comparison added. Historical coverage outcomes retained.'
            item['evidence'] = list(dict.fromkeys(item['evidence']+additions))
    state['survey_continuation'] = dict(plan='docs/program/survey-continuation-2026-10-29.md', results=PREFIX+'survey-continuation-results.json', scientific_changes=4, new_scholarly_originals=0, complete_survey=False)
    pub = ROOT/(PREFIX+'survey-continuation/publication-verification.json')
    if pub.exists():
        state['survey_continuation']['publication'] = str(pub.relative_to(ROOT))
        state['survey_continuation']['documents'] = json.loads(pub.read_text())['documents']
    state['remaining_inventory'] = PREFIX+'survey-continuation/remaining-inventory.json'
    state['approval_scope']['survey_collector'] = 'tools/survey_sources_20261029.py fetch'
    state['approval_scope']['survey_installed'] = 'security/survey-installation-20261029.json'

def apply_inventory(inv):
    if not (ROOT/(PREFIX+'survey-source-audit.json')).exists():
        return
    actions = {
        'inherited_doubleml': 'Conditional selected original Python model, with explicit target and score; full native distribution and matched adverse tests are prototype evidence. No port justified by the inspected material.',
        'inherited_did': 'Same-commit DESCRIPTION now acquired and matches earlier bytes. Conditional original R procedure; specify cohort, time, weights and uncertainty. Full dependency rights and native qualification remain later.',
        'seed_048': 'Use as a bounded symbolic identification reference. Retain source date discrepancy and graph/query semantics; structured failure and native estimation integration remain prototype tests.',
        'seed_088': 'Official current panel methods inspected. Obtain dated release/edition and applicable terms; do not call all MATLAB sources unavailable.',
        'seed_089': 'Named current commercial comparator: Digital Worker Factory with System of Work. Advertising inspected; obtain versioned causal technical specification, comparative evidence and terms. Dara remains a separate source identity.',
        'seed_092': 'Official GUI9.8 decision-information manual and public licence terms inspected. Exact historical version date, order-specific rights and native qualification remain unresolved.'}
    for row in inv['unresolved_reuse_decisions']:
        key=row['id'].split('.')[-1]
        if key in actions:
            row['current_proposal_action']=actions[key]
            row['current_evidence']=PREFIX+'survey-source-audit.json'
            row['historical_status_preserved']=True
    inv['survey_continuation']=PREFIX+'survey-continuation-results.json'
    inv['current_frontier_counts']={'inspected':85,'unread':28}


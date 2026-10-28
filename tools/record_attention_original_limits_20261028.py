"""Record finite original-source routes and local acquisition limits honestly."""
import json
from pathlib import Path
from record_attention_installer_recovery_20261028 import original,start
from prepare_followup_program_20261028 import ROOT,ref,write
from run_followup_program_v2_20261028 import selected
from run_followup_program_20261028 import append,load


def main():
    base=selected();assert base.name=='followup-runtime-v5' and load(ROOT,base)['active'] is None
    names=['original-acquisition-plan.json','original-followup-plan.json'];evidence=[ref(base/n,'Finite original-identity acquisition plan') for n in names]
    start(base,'ATTENTION.ORIGINALS','attention-originals',evidence)
    records=[];failures=[];queries=[]
    raw=ROOT/'docs/literature/raw'
    for name in names:
        for req in json.loads((base/name).read_text())['requests']:
            rp=raw/(req['id']+'.receipt.json');receipt=json.loads(rp.read_text());assert receipt['url']==req['url']
            if receipt['status']=='saved':
                record=original(req);record['claim_scope']='Discovery and edition/access identity only; no primary technical support.';records.append(record)
                if 'search/repositories' in req['url']:
                    d=json.loads((raw/(req['id']+'.json')).read_text());queries.append(dict(query=req.get('query'),total=d['total_count'],returned=len(d['items']),identities=[x['full_name'] for x in d['items']]))
            else:
                assert receipt['status']=='failed';failures.append(dict(source_identity=req['url'],error=receipt['error'],receipt=ref(rp,'Observed collector failure')))
    candidates=[]
    for i in range(2):
        oa=json.loads((raw/f'exec28_attention_original_oa_{i}.json').read_text())
        cr=json.loads((raw/f'exec28_attention_original_crossref_{i}.json').read_text())['message']
        s2=json.loads((raw/f'exec28_attention_original_s2_{i}.json').read_text())
        candidates.append(dict(title=oa['title'],doi=oa['doi'],year=oa['publication_year'],
            first_author=cr['author'][0]['family'],metadata_identities=[oa['id'],s2['paperId']],
            routes=[dict(landing=x.get('landing_page_url'),pdf=x.get('pdf_url')) for x in oa['locations']],
            original_acquired=False,technical_claims_supported=False,
            disposition=('Known publisher/author-institution routes use hosts outside the unchanged fixed collector; matching original not obtained.' if i==0 else 'Metadata identifies SIAM2023 edition; no open PDF or arXiv identity supplied. Exact-title discovery is rate-limited,not proof of absence.'),
            next_action=('Use an explicitly approved publisher/institution route or a verified lawful permitted-host original; inspect exact PDF before scholarly citation.' if i==0 else 'Resume bounded author/preprint/repository identity search when rate limit clears or a lawful original is provided; verify edition before inspection.')))
    omissions=base/'original-omissions-successor.json'
    write(omissions,dict(status='local_access_limits_preserved',candidates=candidates,failures=failures,
        predecessor=ref(base.parent/'followup-runtime-v4/attention-omissions.json','Earlier two omissions retained'),
        no_substitute_original=True,scope='Finite routes only; not global or permanent unavailability.'))
    out=base/'attention-originals.json'
    write(out,dict(status='performed_inconclusive',cutoff='2026-10-07T15:59:59Z',metadata_records=records,
        failed_routes=failures,queries=queries,omissions=ref(omissions,'Edition identities and precise local routes'),
        findings=['Eight saved metadata originals establish identity/access leads only; no new scholarly PDF acquired.','Two exact-title arXiv requests returned429 and GARL repository query returned403; retain requests as failed,not zero-result searches.','Exact Yang-title GitHub query returned0; TCDF/Nauta README query returned20of25repository metadata matches; no saturation or technical claims.','Liu2026 original was already acquired and integrated in predecessor; no duplicate review or census closure awarded.'],
        evidence=evidence+[ref(Path(__file__),'Source-limit reconciliation')],native_execution=False,full_coverage='inconclusive'))
    receipt=base/'attention-originals-receipt.json'
    write(receipt,dict(task='ATTENTION.ORIGINALS',awards_acceptance=False,execution='performed',outcome='inconclusive',
        outputs=[ref(out,'Finite performed original-source search')],evidence=evidence,
        criteria=[dict(index=0,verdict='inconclusive',finding='Both named editions identified; genuine originals still unavailable through performed routes; local host/rate limits preserved.'),dict(index=1,verdict='pass',finding='No metadata-only technical claims,substitute papers or unmatched-edition coverage awarded.')],
        next_action='Continue independent temporal/protocol integration; revisit only named original routes when host permission,rate-limit recovery or exact original identity changes.'))
    append('record','ATTENTION.ORIGINALS',str(receipt.relative_to(ROOT)),ROOT,base)
    print(json.dumps(dict(status='recorded_inconclusive',saved_metadata=len(records),failed_routes=len(failures),states=load(ROOT,base)['states'])))


if __name__=='__main__':main()

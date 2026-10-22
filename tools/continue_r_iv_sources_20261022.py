#!/usr/bin/env python3
"""Register a second bounded batch, derived only from observed source identities."""
import json
from prepare_r_iv_rd_20261022 import BASE, RAW, MANIFEST, write


def main():
    aer=json.loads((RAW/'exec22_riv_aer_cutoff.json').read_text())[0]['sha']
    rd=json.loads((RAW/'exec22_riv_rdrobust_history.json').read_text())[0]['sha']
    requests=[
        dict(id='exec22_riv_aer_tree',url=f'https://api.github.com/repos/cran/AER/git/trees/{aer}?recursive=1',extension='json'),
        dict(id='exec22_riv_aer_description',url=f'https://raw.githubusercontent.com/cran/AER/{aer}/DESCRIPTION',extension='txt'),
        dict(id='exec22_riv_rd411_tree',url=f'https://api.github.com/repos/cran/rdrobust/git/trees/{rd}?recursive=1',extension='json'),
        dict(id='exec22_riv_rd411_description',url=f'https://raw.githubusercontent.com/cran/rdrobust/{rd}/DESCRIPTION',extension='txt'),
        dict(id='exec22_riv_econometrics_view',url='https://cran.r-project.org/web/views/Econometrics.html',extension='html')]
    for name in ['AR','CLR']:
        requests.append(dict(id='exec22_riv_ivmodel_'+name.lower()+'_source',
            url='https://raw.githubusercontent.com/cran/ivmodel/975e89dba107e2b41822cdd680dc33eab09b2c2d/R/'+name+'.r',extension='txt'))
    value=dict(requests=requests)
    write(BASE/'technical-manifest.json',value)
    MANIFEST.write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps(dict(requests=len(requests),AER=aer,rdrobust_postcutoff=rd)))


if __name__=='__main__':main()

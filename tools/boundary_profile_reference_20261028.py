"""Authored finite interface witnesses; no external package is executed."""
def calculate():
    labels=['z','a'];matrix=[[0,1],[0,0]]
    def edges(names):return [[names[i],names[j]] for i,row in enumerate(matrix) for j,value in enumerate(row) if value]
    cases=[
        dict(name='complete',events=[{'done':False},{'done':True,'done_reason':'stop'}],valid=True,identified=True),
        dict(name='midstream_error',events=[{'done':False},{'error':'failure'}],valid=True,identified=True),
        dict(name='truncated',events=[{'done':False}],valid=True,identified=True),
        dict(name='unload',events=[{'done':True,'done_reason':'unload'}],valid=True,identified=True),
        dict(name='invalid',events=[{'done':True,'done_reason':'stop'}],valid=False,identified=True),
        dict(name='nonidentified',events=[{'done':True,'done_reason':'stop'}],valid=True,identified=False),
    ]
    for c in cases:
        c['http_status']=200
        c['admit']=bool(c['events'] and c['events'][-1].get('done') and c['events'][-1].get('done_reason')=='stop' and not any('error' in e for e in c['events']) and c['valid'] and c['identified'])
    assert edges(labels)==[['z','a']] and edges(sorted(labels))==[['a','z']]
    assert [c['name'] for c in cases if c['admit']]==['complete']
    return dict(scope='Authored exact conversion and admission witnesses; not native outcomes',columns=labels,matrix=matrix,correct_edges=edges(labels),labels_only_sorted_edges=edges(sorted(labels)),streams=cases,admitted=1,rejected=5,native_execution=False)

if __name__=='__main__':
    import json
    print(json.dumps(calculate(),indent=2))

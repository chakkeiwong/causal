#!/usr/bin/env python3
"""Preserve installed runtime identities and inspected derivative semantics."""
import importlib
import importlib.metadata
import inspect
import json
from pathlib import Path
import shutil
import jax
from closure_common import ROOT,save,digest


def main():
    target=ROOT/'docs/literature/runtime/closure';target.mkdir(exist_ok=True)
    rows=[];inputs=['tools/closure_runtime_audit.py','tools/closure_common.py']
    for package in ('jax','jaxlib','numpy','scipy','scikit-learn','threadpoolctl'):
        distribution=importlib.metadata.distribution(package);entries=[]
        for item in distribution.files or []:
            if item.name in ('METADATA','LICENSE','LICENSE.txt','LICENSE.rst'):
                original=Path(distribution.locate_file(item));copy=target/(package+'-'+str(item).replace('/','_'))
                shutil.copyfile(original,copy);path=str(copy.relative_to(ROOT));entries.append(dict(path=path,sha256=digest(path),original=str(original)));inputs.append(path)
        rows.append(dict(identity=package,version=distribution.version,accessed='2026-10-10',local_copies=entries))
    api=importlib.import_module('jax._src.api');original=Path(api.__file__);copy=target/'jax-api.py';shutil.copyfile(original,copy);path=str(copy.relative_to(ROOT));inputs.append(path)
    source=copy.read_text();assert 'def grad(' in source and 'def jit(' in source and 'def jacrev(' in source
    anchors={name:source[:source.index('def '+name+'(')].count('\n')+1 for name in ('jit','grad','jacrev','hessian')}
    inspection='\n\n'.join(inspect.getdoc(getattr(jax,name))[:3500] for name in ('jit','grad','jacrev','hessian'))
    excerpt=target/'jax-derivative-contract.txt';excerpt.write_text(inspection+'\n');inputs.append(str(excerpt.relative_to(ROOT)))
    save('docs/literature/closure-runtime-audit.json',dict(status='pass',runtime=rows,
         inspected_api=dict(path=path,sha256=digest(path),original=str(original),anchors=anchors,
                            supported_claim='JIT stages a pure array computation; grad/jacrev/hessian differentiate that discretized objective. They do not certify quadrature accuracy, derivative validity through resampling or statistical identification.'),
         qualification='Installed versions observed on 10 October; separate from current-source survey cutoff 7 October. Numerical finite differences and Gaussian reduction validate selected operations, not library authority alone.'),inputs)
    print(json.dumps({'status':'pass','versions':{r['identity']:r['version'] for r in rows},'anchors':anchors}))


if __name__=='__main__':main()

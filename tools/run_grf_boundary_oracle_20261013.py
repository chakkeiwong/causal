#!/usr/bin/env python3
"""Compile only our arithmetic reference and compare independent exact formulas."""
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'docs/program/execution/2026-10-13/grf-cxx'


def ref(p, anchor):
    return {'path': str(p.relative_to(ROOT)), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'anchor': anchor}


def main():
    source = ROOT/'tools/grf_boundary_oracle_20261013.cpp'
    binary = BASE/'boundary-oracle'
    args = ['c++','-std=c++17','-O2','-Wall','-Wextra','-Werror',str(source),'-o',str(binary)]
    p = subprocess.run(args, capture_output=True, text=True, timeout=40)
    (BASE/'compile.log').write_text(p.stdout+p.stderr)
    assert p.returncode == 0, 'Compilation failed; see compile.log'
    output = subprocess.check_output([str(binary)],text=True,timeout=5)
    observed = json.loads(output)
    oracle = BASE/'oracle-results.json'
    oracle.write_text(json.dumps(observed,indent=2)+'\n')
    scores = [F(10),F(10)]+[F(40)]*4
    mean = sum(scores)/6
    iid = sum((v-mean)**2 for v in scores)/30
    sums = [sum(v-mean for v in scores[:2]),sum(v-mean for v in scores[2:])]
    cluster_var = sum(v*v for v in sums)*F(2,36)
    # Independently expand the usual two-outcome-regression AIPW expression.
    dr=[]
    for y,a,m,e,tau in [(0,0,1,F(1,4),2),(1,0,1,F(1,2),2),(3,1,2,F(1,2),2),(5,1,2,F(3,4),2)]:
        mu0,mu1=m-e*tau,m+(1-e)*tau
        dr.append(mu1-mu0+F(a)*(y-mu1)/e-F(1-a)*(y-mu0)/(1-e))
    expected={'person_mean':mean,'cluster_mean':F(25),'iid_variance':iid,
              'cluster_variance':cluster_var,'equal_cluster_variance':F(225),
              'aipw_mean':sum(dr)/4,'local_slope':F(3),'column_major_value':F(20),
              'wrong_row_major_value':F(3),'rejections':F(5)}
    for k,v in expected.items():
        assert math.isclose(observed[k],float(v),rel_tol=1e-13,abs_tol=1e-13),(k,observed[k],v)
    compiler=subprocess.check_output(['c++','--version'],text=True,timeout=5).splitlines()[0]
    review={'status':'pass','scope':'Project C++ arithmetic and exact Python references; no grf package/core execution',
            'compiler':compiler,'flags':args[1:6],
            'source':ref(source,'Compiled project-only deterministic oracle'),
            'review_code':ref(Path(__file__),'Independent exact expectations and two-outcome score expansion'),
            'binary':ref(binary,'Local oracle executable, not a grf adapter'),
            'results':ref(oracle,'Observed deterministic outputs'),
            'compile_log':ref(BASE/'compile.log','Compiler diagnostics'),
            'exact_expected':{k:str(v) for k,v in expected.items()},
            'inference_limits':['Two-cluster example illustrates formula and target differences, not coverage.',
                                'Five rejection examples validate this reference only.',
                                'Weak denominator threshold is a declared numerical rule, not a proof of overlap.']}
    (BASE/'reproduction-review.json').write_text(json.dumps(review,indent=2)+'\n')
    print(json.dumps({'status':'pass','comparisons':len(expected),'rejections':observed['rejections'],
                      'person_mean':observed['person_mean'],'cluster_mean':observed['cluster_mean']}))


if __name__ == '__main__':
    main()

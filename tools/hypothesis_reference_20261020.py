"""Authored checks: descriptive counts, printed ANOVA identities, and graph witness."""
from fractions import Fraction as F
from pathlib import Path
import json
from scipy.stats import f
import mpmath as mp

def calculate():
    sf=float(f.sf(5.25,3,116))
    z=mp.mpf(116)/(116+mp.mpf(3)*mp.mpf('5.25'))
    other=float(mp.betainc(mp.mpf(116)/2,mp.mpf(3)/2,0,z,regularized=True))
    assert abs(sf-other)<1e-14
    r2=F('84.1611')*3/(F('84.1611')*3+1652)
    a={'Z','P'};b={'Z','P'};j=F(len(a&b),len(a|b))
    assert j==1 and F(156,238)+F(51,238)+F(31,238)==1
    return dict(reported_count_checks=dict(causal_label_precision=str(F(156,238)),
        relation_exists=str(F(207,238)),correlation_given_causal=str(F(51,238)),
        nonexistent_given_causal=str(F(31,238)),source_concentration=str(F(35797,43312))),
        printed_anova_checks=dict(F=5.25,df=[3,116],reported_p=0.553,
            independently_evaluated_upper_tail=sf,independent_beta_tail=other,
            semantic_F='84.1611',semantic_df=[3,1652],reported_R2='0.8696',ordinary_R2=str(r2)),
        graph_witness=dict(edges=[['Z','A'],['Z','B'],['A','P'],['B','P']],
            laws=['A=Z+Ea','B=Z+Eb','P=A+B+Ep'],errors='Independent zero-mean errors and Z',
            undirected_neighbors_A=sorted(a),undirected_neighbors_B=sorted(b),jaccard=str(j),
            intervention_derivative_B_wrt_A='0',assumed_value=100,assumed_cost=20,
            invalid_similarity_probability_margin=str(j*100-20),true_incremental_margin=-20),
        limitations=['Project arithmetic and constructed structural law; no reproduction of paper raw data.',
            'ANOVA identities are conditional on the ordinary stated model and printed degrees of freedom.',
            'Jaccard witness does not assert the uninspected native implementation uses this neighbor convention.',
            'No causal calibration, native execution, live model or measured bank return.'])

if __name__=='__main__':
    out=Path(__file__).resolve().parents[1]/'docs/program/execution/2026-10-20/census-hypothesis-v1/exact-results.json'
    assert not out.exists()
    out.write_text(json.dumps(calculate(),indent=2)+'\n')
    print(json.dumps(calculate()))


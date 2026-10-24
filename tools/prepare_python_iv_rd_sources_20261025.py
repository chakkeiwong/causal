#!/usr/bin/env python3
"""Build exact source anchors after preserving the first range-end failure."""
from pathlib import Path
import json
from publish_latent_r_review_v2_20261013 import ref,write
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'docs/program/execution/2026-10-25/python-iv-rd-completion-v1';RAW=ROOT/'docs/literature/raw'
G={
'causalpy':('CausalPy IV/RD design, likelihood and cutoff-contrast contracts','pymc-labs/CausalPy','1.0.0rc1;6 October 2026;f17b30ff1d33b065119acac83122abe79210fda3',[
('causalpy_src_0',143,197,['self.get_2SLS_fit()','if priors is None'],'Deterministic reference fits and data-centered default priors.'),
('causalpy_src_0',199,220,['self.instruments_formula','self.labels_instruments'],'Separate formula matrices and row-identity boundary.'),
('causalpy_src_0',297,369,['Treatment term','def get_2SLS_fit','sk_lin_reg()'],'Treatment checks and point-reference fitting; no exclusion proof.'),
('docs/program/execution/2026-10-14/causalpy-reuse/causalpy__pymc_models.py',1662,1750,['pm.Bernoulli','rho_clipped','pm.MvNormal','LKJCholeskyCov'],'Separate continuous and binary likelihoods, priors and latent coupling.'),
('causalpy_src_1',164,201,['mask &=','self.donut_hole','build_formula_matrices'],'Bandwidth/donut filtering and design construction.'),
('causalpy_src_1',231,291,['self.treatment_threshold - self.epsilon','self.treatment_threshold + self.epsilon','discontinuity_at_threshold'],'Finite-epsilon conditional expectation contrast.'),
('causalpy_src_1',295,338,['_is_variable_dummy_coded','donut_hole','np.greater_equal'],'Input guards and treatment direction; assignment validity separate.')]),
'rdrobust':('rdrobust Python 2.1.1 target, robust-row and fuzzy-ratio contracts','rdpackages/rdrobust','2.1.1;6 October 2026;fa3fea8260d41fe25964af8119e65d151c4841c5',[
('rdrobust_src_0',1,12,['GNU General Public License version 3'],'Original GPL notice; installed/dependency terms separate.'),
('rdrobust_src_1',1,35,['version = 2.1.1','license = GPL-3.0-only','scipy'],'Version and dependency metadata.'),
('rdrobust_src_2',295,307,['q must be strictly greater than p','deriv>p'],'Polynomial, bias and derivative specification guard.'),
('rdrobust_src_2',463,543,['weights must include','less_c = x<c','Not enough distinct','Fuzzy RD: first-stage'],'Weight/cutoff/distinct-score and fully degenerate treatment checks.'),
('rdrobust_src_2',1017,1030,['tau_cl = tau_Y_cl/tau_T_cl','tau_bc = tau_cl','tau_T_cl**2'],'Fuzzy ratio and bias correction depend on first-stage denominator.'),
('rdrobust_src_2',1124,1183,['tau = np.array([tau_cl, tau_bc, tau_bc])','se  = np.array([se_tau_cl,se_tau_cl,se_tau_rb])','Conventional','Robust'],'Exact estimate/SE row pairing and normal-reference calculation.')]),
'rdd':('rdd 0.0.3 separate trimming and unfitted common-slope WLS reference','evan-magnusson/rdd','0.0.3;17 August 2019;7a354a2bc485a029cfc0c3ceba4fcdfb55750946',[
('rdd_src_0',1,21,['Permission is hereby granted'],'Original MIT notice.'),
('rdd_src_1',1,25,["version='0.0.3'","'statsmodels'"],'Version and runtime dependency.'),
('rdd_src_2',79,143,['def truncated_data','data_new =','def rdd','TREATED','smf.wls','return rdd_model'],'Separate trimming, common-slope default and unfitted WLS object.')]),
'ivmodels':('ivmodels 0.10.0 coefficient-null inversion and confidence-set geometry','mlondschien/ivmodels','0.10.0;6 July 2026;43d3b02036ca0dc679bba91b8d202c2b82270e25',[
('ivmodels_src_0',1,16,['BSD 3-clause','Redistribution'],'Original BSD notice.'),
('ivmodels_src_1',1,25,['version = "0.10.0"','glum','scipy'],'Version and unresolved dependencies.'),
('ivmodels_src_2',188,239,['residuals = y - X @ beta','dfd =','scipy.stats.chi2.sf','scipy.stats.f.sf'],'Coefficient-null residual test and explicit critical values.'),
('ivmodels_src_2',319,377,['Test inversion','S_proj','A = S_proj.T','return Quadric'],'Subvector branch, quadratic inversion and projection.'),
('ivmodels_src_4',42,71,['np.linalg.solve','np.linalg.eigh','is_empty','is_bounded'],'Direct-solve center; singular parameterizations require qualification.'),
('ivmodels_delegate_0',1,70,['union of','ConfidenceSet([])','(-np.inf, np.inf)','boundary[1], np.inf'],'Union, empty and unbounded confidence-set representation.'),
('ivmodels_delegate_1',28,89,['Shape mismatch','scipy.linalg.lstsq','lapack_driver="gelsy"'],'Shape preservation and projection solver; rank qualification separate.')]),
'pyfixest':('pyfixest rank, solver and missing-permission-document followup','py-econometrics/pyfixest','repository revision;6 October 2026;45d52b6e368cefc7321239921f2547b4e08c8f20',[
('pyfixest_src_0',1,3,['_find_collinear_variables_rs'],'Actual Rust-backed binding.'),
('pyfixest_src_1',1,18,['SPDX-License-Identifier: MIT','docs/THIRD_PARTY_PERMISSIONS.md'],'Header asserts permission; named primary document unresolved.'),
('pyfixest_src_1',60,120,['original column ordering','if tol <= 0.0','if r_jj < tol'],'Ordered Gram threshold and local positive-only tolerance guard.'),
('pyfixest_src_2',35,48,['np.linalg.lstsq','assume_a="pos"','lsqr(tZX, rhs)[0]'],'Branches extract solutions; adapter must preserve additional diagnostics.')])}

def main():
    assert not (BASE/'source-spec.json').exists();spec={}
    for key,(title,repo,version,checks) in G.items():
        rows=[]
        for stem,lo,hi,tokens,finding in checks:
            filename=stem if stem.startswith('docs/') else 'exec25_pyrdiv_'+stem+'.txt'
            p=ROOT/filename if filename.startswith('docs/') else RAW/filename
            lines=p.read_text().splitlines();fragment='\n'.join(lines[lo-1:hi]);assert all(t in fragment for t in tokens),(filename,lo,hi,[t for t in tokens if t not in fragment])
            rows.append([filename,lo,min(hi,len(lines)),tokens,finding])
        spec[key]=[title,repo,version,rows]
    write(BASE/'source-spec.json',spec)
    leads={};queries=[]
    for key in ['rd','iv']:
        p=RAW/('exec25_pyrdiv_search_'+key+'.json');d=json.loads(p.read_text());queries.append(dict(kind=key,total=d['total_count'],returned=len(d['items']),incomplete_results=d['incomplete_results'],original=ref(p,'Discovery metadata only')))
        for x in d['items']:leads.setdefault(x['full_name'],dict(name=x['full_name'],description=x.get('description'),status='discovery_only_uninspected'))
    for key in ['bashtage/linearmodels','evan-magnusson/rdd','mlondschien/ivmodels']:
        if key in leads:leads[key]['status']='selected_or_inherited_primary_review'
    write(BASE/'search-screening.json',dict(cutoff='2026-10-07',queries=queries,unique_leads=len(leads),leads=list(leads.values()),additional_named_candidates=['rdpackages/rdrobust','pymc-labs/CausalPy','py-econometrics/pyfixest'],scope='Two first-page searches and retained chains; unreturned pages and nonlinear IV alternatives open',saturation_claim=False,absence_claim=False))
    print(json.dumps(dict(groups=len(spec),anchors=sum(len(x[3]) for x in spec.values()),unique_leads=len(leads))))
if __name__=='__main__':main()

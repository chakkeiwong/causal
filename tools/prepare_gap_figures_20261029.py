from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/scientific-gap-closure/2026-10-29'
s=json.loads((OUT/'study-results.json').read_text())
labels=['Difference in means','Common-slope adjustment','Fully interacted adjustment']
fig,ax=plt.subplots(figsize=(8.1,3.7))
for j,m in enumerate(s['methods']):
    b=m['estimate'];lo,hi=m['interval']
    ax.errorbar(b,2-j,xerr=[[b-lo],[hi-b]],fmt='o',capsize=5,color='#17324D',lw=2)
ax.set_yticks([2,1,0],labels)
ax.axvline(0,color='grey',lw=1)
ax.axvline(1000,color='#9E4F20',ls='--',lw=1.4,label='Illustrative cost: 1,000')
ax.set_xlabel('1978 earnings contrast, archived dollar units')
ax.set_ylim(-.6,2.7);ax.grid(axis='x',alpha=.2);ax.legend(loc='upper right',frameon=False)
fig.tight_layout();fig.savefig(OUT/'decision-intervals.pdf');fig.savefig(OUT/'decision-intervals.png',dpi=130);plt.close(fig)
fig,ax=plt.subplots(figsize=(8.1,4.1))
m=np.arange(1,31)
for rho in [0,.2,.5,.9]:
    se=rho+(1-rho)/m;beta=-.2+se/(1+2*se)
    ax.plot(m,beta,label=f'Error correlation {rho:g}',lw=2)
ax.axhline(0,color='grey',lw=1);ax.axhline(-.2,color='black',ls=':',label='True effect -0.2')
ax.set_xlabel('Number of readings');ax.set_ylabel('Population adjusted coefficient')
ax.legend(frameon=True,facecolor='white',framealpha=1,fontsize=9,loc='lower left');ax.grid(alpha=.15);fig.tight_layout()
fig.savefig(OUT/'measurement-floor.pdf');fig.savefig(OUT/'measurement-floor.png',dpi=130);plt.close(fig)
rows=[]
for label,m in zip(labels,s['methods']):
    rows.append(f"{label} & {m['estimate']:,.0f} & {m['standard_error']:,.0f} & [{m['interval'][0]:,.0f}, {m['interval'][1]:,.0f}] " + chr(92)*2)
table=r'''
\begin{table}[htbp]
\centering\small
\begin{tabular}{lrrl}
\toprule
Estimator & Estimate & Std. error & Approx. 95\% interval \\
\midrule
'''+chr(10).join(rows)+r'''
\bottomrule
\end{tabular}
\caption{New calculations on the 445 retained experimental observations.
Intervals use normal critical values and HC2 covariance, equivalent to
separate-arm variance for the unadjusted estimator. This single dataset
establishes neither finite-sample coverage nor estimator superiority.}
\end{table}
'''
(OUT/'public-results-table.tex').write_text(table)
print('Two figures and one results table saved')

policy=json.loads((OUT/'policy-uncertainty-results.json').read_text())
verification=json.loads((OUT/'new-results-verification.json').read_text())
fig,ax=plt.subplots(figsize=(8.1,4.1))
cases=['baseline','future_dependent_dropout','omitted_state_predictor']
for j,(method,label,color) in enumerate([('gcomp_bootstrap','Fitted transition + bootstrap','#17324D'),('prefix_ipw','Prefix weighting','#9E4F20')]):
    for i,case in enumerate(cases):
        r=next(r for r in policy['scenarios'] if r['scenario']==case and r['policy']=='selected_threshold' and r['target']=='improvement' and r['method']==method)
        v=next(r for r in verification['policy-uncertainty']['coverage_checks'] if all(r[k]==value for k,value in dict(scenario=case,policy='selected_threshold',target='improvement',method=method).items()))
        p=r['coverage'];lo,hi=v['coverage_wilson']
        ax.errorbar(i+(j-.5)*.14,p,yerr=[[p-lo],[hi-p]],fmt='o',capsize=4,color=color,label=label if i==0 else None)
ax.axhline(.95,color='gray',ls='--',label='Nominal coverage')
ax.set_xticks(range(3),['Baseline','Future-dependent\ndropout','Omitted state\npredictor'])
ax.set_ylabel('Coverage of policy improvement');ax.set_ylim(-.03,1.12)
ax.legend(fontsize=9,loc='lower left',framealpha=1);ax.grid(axis='y',alpha=.15)
fig.tight_layout();fig.savefig(OUT/'policy-coverage.pdf');fig.savefig(OUT/'policy-coverage.png',dpi=120);plt.close(fig)

obs=json.loads((OUT/'observation-results.json').read_text())
fig,ax=plt.subplots(figsize=(8.1,3.8))
for method,label,color in [('fuzzy','Fuzzy matching','#17324D'),('conditional_candidates','Candidate ranges','#518571'),('corruption_aware','Corruption-budget envelope','#9E4F20')]:
    rs=[r for r in obs['scenarios'] if r['scenario']=='outcome_dependent' and r['method']==method]
    ax.plot([r['rate']*100 for r in rs],[r['mean_width'] for r in rs],marker='o',lw=2,label=label,color=color)
ax.set_xlabel('Corrupted outcome records (%)');ax.set_ylabel('Average population interval width')
ax.legend(loc='upper left',framealpha=1,fontsize=9);ax.grid(alpha=.15)
fig.tight_layout();fig.savefig(OUT/'linkage-width.pdf');fig.savefig(OUT/'linkage-width.png',dpi=120);plt.close(fig)
print('Policy coverage and linkage uncertainty figures saved')

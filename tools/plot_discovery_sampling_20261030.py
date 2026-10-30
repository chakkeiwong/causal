"""Render retained sampling comparisons; do not regenerate experiments."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

O=Path(__file__).resolve().parents[1]/'docs/twelve-hour-closure/2026-10-29'
a=json.loads((O/'discovery-sampling-attempt-1/results.json').read_text())
b=json.loads((O/'discovery-timing-attempt-1/results.json').read_text())
F=O/'sampling-figures';F.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,axes=plt.subplots(3,1,figsize=(6.4,7.7),sharex=True,sharey=True)
titles={'strong':'Larger baseline coefficients','weak':'Smaller baseline coefficients','cancellation':'Exact cancellation'}
for ax,name in zip(axes,titles):
    first=[next(x for x in a['summaries'] if x['mechanism']==name and x['n']==n and x['alpha']==.05 and x['method']=='full') for n in [100,500,2000]]
    known=[next(x for x in a['references'] if x['mechanism']==name and x['n']==n and x['method']=='all_baseline') for n in [100,500,2000]]
    def line(items,color,marker,label,key,band):
        y=np.array([x[key] if isinstance(x[key],float) else x[key]['estimate'] for x in items]);bounds=np.array([x[band] if band else x[key]['wilson95'] for x in items]);error=np.vstack([y-bounds[:,0],bounds[:,1]-y]);error=np.maximum(error,0)
        ax.errorbar([0,1,2],100*y,yerr=100*error,color=color,marker=marker,capsize=3,label=label,lw=1.8)
    line(first,'#b44f30','o','Graph-selected controls','coverage',None)
    if name!='cancellation':
        timing=[next(x for x in b['summaries'] if x['mechanism']==name and x['n']==n and x['alpha']==.05 and x['method']=='full') for n in [100,500,2000]]
        line(timing,'#2b7791','s','Exclude later score from search','coverage','coverage_wilson95')
    line(known,'#247348','^','All baseline controls','coverage','wilson95')
    ax.axhline(95,color='#777777',linestyle='--',lw=.9);ax.set_title(titles[name]);ax.set_xticks([0,1,2],['100','500','2,000']);ax.set_ylim(-5,105);ax.grid(axis='y',alpha=.16)
axes[1].set_ylabel('Intervals covering the true effect (%)');axes[-1].set_xlabel('Observations per sample')
handles,labels=axes[0].get_legend_handles_labels();fig.legend(handles,labels,loc='lower center',ncol=1,bbox_to_anchor=(.5,-.015),frameon=False);fig.tight_layout(rect=(0,.11,1,1));fig.savefig(F/'coverage.pdf',bbox_inches='tight');fig.savefig(F/'coverage.png',dpi=150,bbox_inches='tight');plt.close(fig)
fig,axes=plt.subplots(1,2,figsize=(9,3.5),sharey=True)
for ax,name in zip(axes,['strong','weak']):
    for data,color,label,timing in [(a['summaries'],'#b44f30','Search includes later score',False),(b['summaries'],'#2b7791','Search excludes later score',True)]:
        y=[]
        for n in [100,500,2000]:
            x=next(x for x in data if x['mechanism']==name and x['n']==n and x['alpha']==.05 and x['method']=='full');y.append(100*(1-x['error_rate'] if timing else 1-x['proportions']['wrong_skeleton']['estimate']))
        ax.plot([0,1,2],y,'o-',color=color,label=label)
    ax.set_title(titles[name]);ax.set_xticks([0,1,2],['100','500','2,000']);ax.set_xlabel('Observations per sample');ax.set_ylim(-5,105);ax.grid(axis='y',alpha=.16)
axes[0].set_ylabel('Exact skeleton recovery (%)');fig.legend(*axes[0].get_legend_handles_labels(),loc='lower center',ncol=2,bbox_to_anchor=(.5,-.03),frameon=False);fig.tight_layout(rect=(0,.10,1,1));fig.savefig(F/'skeleton.pdf',bbox_inches='tight');fig.savefig(F/'skeleton.png',dpi=150,bbox_inches='tight');plt.close(fig)
rows=[r'\begin{longtable}{llrrrrr}',r'\toprule',r'Mechanism & Search & $n$ & $\alpha$ & Wrong & Unfinished & Coverage\\',r'\midrule\endhead']
for x in a['summaries']:
    rows.append(f"{x['mechanism']} & {x['method']} & {x['n']} & {x['alpha']:.2f} & {x['counts']['wrong_skeleton']} & {x['counts']['incomplete']} & {100*x['coverage']['estimate']:.1f}\\%"+r'\\')
rows += [r'\bottomrule\end{longtable}']
(O/'sampling-complete-table.tex').write_text(chr(10).join(rows)+chr(10))
print(json.dumps({'figures':[str(x.relative_to(O)) for x in F.glob('*.pdf')],'table_rows':len(a['summaries'])}))

from pathlib import Path
import os,json,csv,numpy as np
os.environ.setdefault('MPLCONFIGDIR','/tmp/causal-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
O=Path(__file__).resolve().parents[1]/'docs/twelve-hour-closure/2026-10-29'
F=O/'outcome-figures';F.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
basic=json.loads((O/'outcome-audit-attempt-2/future/result.json').read_text())
aug=json.loads((O/'outcome-audit-precision-attempt-1/future/result.json').read_text())
a={r['method']:r for r in basic['summaries'] if r['target']=='gain'}
b={r['method']:r for r in aug['summaries'] if r['target']=='gain'}
fig,axs=plt.subplots(1,2,figsize=(9.5,3.8),layout='constrained')
for source,prefix,label,color in [(a,'audit_','Reward weighting','#a45b28'),(b,'augmented_audit_','Pilot-assisted score','#24628a')]:
 rs=[source[prefix+f'{q:g}'] for q in [.05,.1,.25,.5,1.]]
 x=[r.get('mean_audits',r.get('mean_evaluation_audits')) for r in rs]
 axs[0].plot(x,[r['mean_width'] for r in rs],'o-',label=label,color=color)
 axs[1].plot(x,[100*r['positive_lower_rate'] for r in rs],'o-',label=label,color=color)
axs[0].axhline(.7525801777763024,color='.5',linestyle='--',linewidth=1,label='True gain (reference)')
axs[0].set(ylabel='Mean 95% interval width (reward units)',xlabel='Completed evaluation follow-ups')
axs[1].set(ylabel='Positive lower bound (%)',xlabel='Completed evaluation follow-ups',ylim=(0,50))
axs[0].legend(frameon=False,fontsize=8);axs[1].legend(frameon=False,fontsize=8)
fig.savefig(F/'precision.pdf');plt.close(fig)
names=['augmented_routine_g','augmented_audit_0.05','augmented_audit_0.25','constant_audit_0.25','augmented_full']
labels=['Assumed routine model','5% random recovery','25% random recovery','25%, constant model','Full-history diagnostic']
fig,axs=plt.subplots(1,2,figsize=(9.5,4),layout='constrained');y=np.arange(len(names))
axs[0].errorbar([b[m]['bias'] for m in names],y,xerr=[1.96*b[m]['bias_mcse'] for m in names],fmt='o',color='#24628a',capsize=3)
axs[0].set_yticks(y,labels);axs[0].invert_yaxis();axs[0].axvline(0,color='.5',linestyle='--');axs[0].set_xlabel('Bias and 95% Monte Carlo interval')
axs[1].errorbar([100*b[m]['coverage'] for m in names],y,xerr=[196*b[m]['coverage_mcse'] for m in names],fmt='o',color='#24628a',capsize=3)
axs[1].set_yticks(y,[]);axs[1].invert_yaxis();axs[1].axvline(95,color='.5',linestyle='--');axs[1].set(xlabel='Coverage and Monte Carlo interval (%)',xlim=(50,100))
fig.savefig(F/'bias-coverage.pdf');plt.close(fig)
print('Created two source-linked figures.')

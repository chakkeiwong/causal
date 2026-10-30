"""Plot exact project examples; no experimental claims about external models."""
from pathlib import Path
import json
import os
os.environ.setdefault('MPLCONFIGDIR', '/tmp/causal-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

root=Path(__file__).resolve().parents[1]
out=root/'docs/twelve-hour-closure/2026-10-29'
d=json.loads((out/'graph-confidence-attempt-1/result.json').read_text())
folder=out/'graph-figures';folder.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,
                     'axes.spines.right':False,'axes.titleweight':'bold'})
fig,axs=plt.subplots(1,3,figsize=(11,3.0),layout='constrained')
ax=axs[0];pmax=d['bound']['pmax']
ax.hlines(0,0,pmax,color='#4d779c',lw=9,alpha=.45)
ax.scatter([.1,pmax],[0,0],color=['#203e56','#b84c35'],s=45,zorder=3)
ax.annotate('Feasible success = 0.10',(.1,0),(.03,.55),arrowprops={'arrowstyle':'-','color':'#777'},fontsize=8)
ax.annotate('Success cap = 0.495',(pmax,0),(.18,-.65),arrowprops={'arrowstyle':'-','color':'#777'},fontsize=8)
ax.set(xlim=(-.03,1.03),ylim=(-1,1),yticks=[],xlabel='Probability of success',title='1. A cap is not an estimate')
ax=axs[1];ax.bar([0,1],[.8,36/61],width=.55,color=['#b84c35','#4d779c'])
ax.set(xticks=[0,1],xticklabels=['Assigned','After rejecting\ncycles'],ylim=(0,1),ylabel='Arrow probability',title='2. Joint consistency matters')
for x,y,s in [(0,.8,'0.800'),(1,36/61,'0.590')]:ax.text(x,y+.035,s,ha='center')
ax.text(.5,.93,'Cycle probability: 0.512',ha='center',transform=ax.transAxes,fontsize=8)
ax=axs[2];sample=d['sampling']['qr_checks'][0];crit=d['sampling']['critical']
lo,hi=sample['slope']-crit*sample['se'],sample['slope']+crit*sample['se']
ax.hlines(1,lo,hi,color='#b84c35',lw=5);ax.hlines(0,lo,hi,color='#4d779c',lw=5)
ax.scatter([0],[0],color='#4d779c',s=50,zorder=4)
for val in [0,.6]:ax.axvline(val,color='#888',lw=.7,ls=':')
ax.set(xlim=(-.08,.8),ylim=(-.6,1.65),yticks=[0,1],yticklabels=['Both graphs','One graph'],xlabel='Effect of a one-unit change',title='3. Preserve the effect ambiguity')
ax.text(0,1.4,'World 2',ha='center',fontsize=8);ax.text(.6,1.4,'World 1',ha='center',fontsize=8)
fig.savefig(folder/'uncertainty.pdf',bbox_inches='tight')
fig.savefig(folder/'uncertainty.png',dpi=160,bbox_inches='tight')
print(str(folder/'uncertainty.pdf'))

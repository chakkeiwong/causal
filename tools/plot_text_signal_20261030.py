"""Render the specified economic graph, without estimating new results."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

O=Path(__file__).resolve().parents[1]/'docs/twelve-hour-closure/2026-10-29/text-figures'
O.mkdir(exist_ok=True)
fig,ax=plt.subplots(figsize=(8.4,4.4));ax.set_xlim(0,10);ax.set_ylim(0,5);ax.axis('off')
pos={'U':(5,4.1),'A':(2.1,2.2),'R':(5,2.2),'Y':(8,2.2)}
labels={'U':'Baseline risk U','A':'Relief A','R':'Baseline description R','Y':'Later default Y'}
for key,(x,y) in pos.items():
 ax.text(x,y,labels[key],ha='center',va='center',fontsize=11,bbox=dict(boxstyle='round,pad=.55',facecolor='#f3f5f7',edgecolor='#334d66'))
for a,b in [('U','A'),('U','R'),('U','Y')]:
 x,y=pos[a];xx,yy=pos[b];ax.annotate('',(xx,yy+.35),(x,y-.3),arrowprops=dict(arrowstyle='->',color='#334d66',lw=1.6))
ax.annotate('',(7.7,1.83),(2.4,1.83),arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=.28',color='#ac5035',lw=1.6))
ax.text(5,.82,'Policy effect: 0 or -5 percentage points',ha='center',fontsize=10,color='#903b25')
ax.add_patch(FancyBboxPatch((.8,1.62),5.7,1.2,boxstyle='round,pad=.15',fill=False,ls='--',lw=1.2,edgecolor='#557b65'))
ax.text(1.75,3.04,'Text W = (A, R)',ha='center',fontsize=9,color='#355c44')
fig.tight_layout();fig.savefig(O/'decision.pdf',bbox_inches='tight');fig.savefig(O/'decision.png',dpi=180,bbox_inches='tight');plt.close(fig)
print('Rendered declared economic graph')

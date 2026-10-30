"""Reproduce the declared trace and exact Poisson waiting figure."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
O=Path(__file__).resolve().parents[1]/'docs/twelve-hour-closure/2026-10-29/energy-figures'
O.mkdir(exist_ok=True)
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
fig,ax=plt.subplots(1,2,figsize=(9,3.25))
t=np.arange(7);p=np.array([100,100,10,10,10,100,100]);active=np.array([1,1,0,0,0,1,1],bool)
ax[0].plot(t,p,'o-',label='All samples: 330 J',color='#1b536b')
ax[0].plot(t[active],p[active],'s--',label='Remove idle samples: 600 J',color='#b33d3d')
ax[0].fill_between(t,p,alpha=.15,color='#1b536b')
ax[0].set(xlabel='Elapsed seconds',ylabel='Power (watts)',ylim=(0,125),title='A declared synthetic power trace')
ax[0].legend(loc='lower center',fontsize=8)
r=np.logspace(0,np.log10(60),200)
for b,c in [(4,'#1b536b'),(20,'#b33d3d')]:ax[1].plot(r,(b-1)*30/r,label=f'Batch of {b}',color=c)
ax[1].set(xlabel='Requests per minute',ylabel='Mean collection delay (seconds)',xscale='log',yscale='log',title='Waiting for enough requests')
ax[1].set_xticks([1,10,60],['1','10','60']);ax[1].legend();fig.tight_layout()
fig.savefig(O/'energy-waiting.pdf');fig.savefig(O/'energy-waiting.png',dpi=160)

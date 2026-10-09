import sys,numpy as np,openpyxl
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt,matplotlib.gridspec as gridspec
from scipy.interpolate import PchipInterpolator
wb=openpyxl.load_workbook(sys.argv[1],data_only=True)
def block(ws,start):
    t=[];cols=[[],[],[]]
    for r in range(start,start+43):
        row=[ws.cell(r,c).value for c in range(1,5)]
        t.append(row[0]);[cols[j].append(row[j+1]) for j in range(3)]
    return np.array(t,float),[np.array(c,float) for c in cols]
COLORS=['#4472C4','#ED7D31','#70AD47']
plt.rcParams.update({'font.family':'serif','font.serif':['Times New Roman','Times','DejaVu Serif'],'font.size':21,'axes.labelsize':23,'axes.linewidth':1.1,'xtick.labelsize':21,'ytick.labelsize':21,'figure.dpi':300,'savefig.dpi':300,'mathtext.fontset':'dejavuserif'})
LAB={'kf':[r'$k_f$ = 4.0×10$^4$',r'$k_f$ = 3.0×10$^5$',r'$k_f$ = 1.0×10$^6$'],
     'kd':[r'$k_d$ = 2.0×10$^7$',r'$k_d$ = 1.0×10$^8$',r'$k_d$ = 4.0×10$^8$'],
     'ko':[r'$k_{ORR}$ = 16',r'$k_{ORR}$ = 80',r'$k_{ORR}$ = 400']}
ROWS=[('Figure 4a-c','Mass Loss (%)',(0,0.7),'upper left'),('Figure 4d-f',r'Saturation, F/F$_{max}$ (%)',(0,50),'upper left'),('Figure 4g-i',r'Interface O$_2$ (mg L$^{-1}$)',(0,3.9),'lower left')]
fig=plt.figure(figsize=(18,14))
gs=gridspec.GridSpec(3,3,figure=fig,left=0.08,right=0.97,top=0.95,bottom=0.07,wspace=0.25,hspace=0.35)
tf=np.linspace(0,168,400);letters=iter('abcdefghi')
for r,(sheet,yl,ylim,loc) in enumerate(ROWS):
    ws=wb[sheet]
    for c,(key,start) in enumerate((('kf',7),('kd',52),('ko',97))):
        t,cols=block(ws,start)
        ax=fig.add_subplot(gs[r,c])
        for y,col,lab in zip(cols,COLORS,LAB[key]):
            ax.plot(tf,PchipInterpolator(t,y)(tf),color=col,lw=2.0,label=lab)
        for sp in ax.spines.values(): sp.set_visible(True);sp.set_linewidth(1.1)
        ax.set_xlabel('Time (hours)');ax.set_ylabel(yl,fontsize=19 if r==1 else None);ax.set_xlim(0,168);ax.set_ylim(*ylim)
        lg=ax.legend(loc=loc,frameon=True,edgecolor='#AAAAAA',framealpha=0.95,fontsize=14,handlelength=1.5,handletextpad=0.3,borderpad=0.25,labelspacing=0.12);lg.get_frame().set_linewidth(0.7)
        ax.annotate(f'({next(letters)})',xy=(0,1),xycoords='axes fraction',xytext=(-68,25),textcoords='offset points',fontsize=27,fontweight='bold',va='top',ha='left',annotation_clip=False)
        if r==0: ax.set_title([r'$k_f$ sweep',r'$k_d$ sweep',r'$k_{ORR}$ sweep'][c],fontsize=20,fontweight='bold',pad=10)
fig.savefig(sys.argv[2],format='png',bbox_inches='tight',dpi=200)

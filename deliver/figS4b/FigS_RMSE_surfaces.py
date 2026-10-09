"""RMSE response surfaces of the BO calibration (32 evaluations, optimization_runs_v4.csv).
Each panel: RMSE vs two parameters (log10 axes), surface = smoothed thin-plate-spline interpolant (shown only within 0.22 normalised-log units of an evaluated point) of the 32 evaluations
projected onto the parameter pair, for the 28 evaluations with k_ORR <= 200 mm/h (the third parameter is not held fixed); black dots = evaluated points."""
import csv, os, numpy as np, matplotlib.pyplot as plt
from matplotlib import cm
from scipy.interpolate import RBFInterpolator
B=os.path.dirname(os.path.abspath(__file__))
R=list(csv.DictReader(open(os.path.join(B,'optimization_runs_v4.csv'))))
kf=np.array([float(r['k1_kf']) for r in R]);kd=np.array([float(r['k2_kd']) for r in R]);ko=np.array([float(r['k_ORR']) for r in R]);z=np.array([float(r['RMSE']) for r in R])
M=ko<=200   # keep the evaluations inside the k_ORR range of Table S5 (10-200 mm/h); 4 points (210-710) lie outside and are not drawn
kf,kd,ko,z=kf[M],kd[M],ko[M],z[M]
P={'kf':(np.log10(kf),r'$k_f$ (h$^{-1}$)'),'kd':(np.log10(kd),r'$k_d$ (mm$^6$ g$^{-2}$ h$^{-1}$)'),'ko':(np.log10(ko),r'$k_{ORR}$ (mm h$^{-1}$)')}
plt.rcParams.update({'font.size':13,'axes.labelsize':16,'axes.titlesize':18,'axes.titleweight':'bold','figure.dpi':300,'savefig.dpi':300})
def tl(a):
    t=np.arange(np.ceil(a.min()),np.floor(a.max())+1);return t,[r'$10^{%d}$'%v for v in t]
def panel(a,b,title,name):
    xa,la=P[a];xb,lb=P[b]
    n=lambda v:(v-v.min())/(v.max()-v.min())
    pts=np.c_[n(xa),n(xb)]
    f=RBFInterpolator(pts,z,kernel='thin_plate_spline',smoothing=2e-2)
    g=np.linspace(0,1,60);G1,G2=np.meshgrid(g,g)
    Z=np.clip(f(np.c_[G1.ravel(),G2.ravel()]).reshape(G1.shape),z.min(),z.max())
    from scipy.spatial import cKDTree
    d,_=cKDTree(pts).query(np.c_[G1.ravel(),G2.ravel()]);Z=np.where(d.reshape(G1.shape)<0.22,Z,np.nan)
    X=xa.min()+G1*(xa.max()-xa.min());Y=xb.min()+G2*(xb.max()-xb.min())
    fig=plt.figure(figsize=(9,7.5));ax=fig.add_subplot(111,projection='3d')
    s=ax.plot_surface(X,Y,Z,cmap='jet',edgecolor='k',linewidth=0.3,vmin=z.min(),vmax=z.max())
    ax.scatter(xa,xb,z,c='k',s=14,depthshade=False)
    i=int(np.argmin(z));ax.scatter([xa[i]],[xb[i]],[z[i]],marker='*',s=260,c='gold',edgecolor='k',depthshade=False,zorder=10)
    ax.view_init(elev=28,azim=-55);ax.set_xlabel(la,labelpad=14);ax.set_ylabel(lb,labelpad=14);ax.set_zlabel('RMSE (%)',labelpad=10,fontweight='bold')
    t,l=tl(xa);ax.set_xticks(t);ax.set_xticklabels(l);t,l=tl(xb);ax.set_yticks(t);ax.set_yticklabels(l)
    ax.set_title(title,pad=10);fig.colorbar(s,ax=ax,shrink=0.55,pad=0.08,label='RMSE (%)')
    fig.savefig(os.path.join(B,name+'.png'),bbox_inches='tight');fig.savefig(os.path.join(B,name+'.pdf'),bbox_inches='tight');plt.close(fig)
panel('kd','ko',r'RMSE vs. $k_d$ and $k_{ORR}$','FigS_RMSE_kd_kORR')
panel('kf','ko',r'RMSE vs. $k_f$ and $k_{ORR}$','FigS_RMSE_kf_kORR')
panel('kf','kd',r'RMSE vs. $k_f$ and $k_d$','FigS_RMSE_kf_kd')

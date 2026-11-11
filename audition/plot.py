import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from ovm import *
fonts=[f.name for f in font_manager.fontManager.ttflist if "Noto" in f.name and ("CJK" in f.name or "TC" in f.name)]
if fonts: plt.rcParams["font.family"]=fonts[0]
N,b=22,2.0
fig,axs=plt.subplots(1,3,figsize=(13,5.2),sharey=True,dpi=150)
for ax,a in zip(axs,(2.4,1.5,1.0)):
    x,v,L=uniform(N,b)
    s=simulate(x,v,a,L,0.05,700,every=0.1,brake=(0,10,11)); s=[r for r in s if r[0]>=400]
    ts=[t for t,_,_ in s for _ in range(N)]
    xs=[xi for _,xx,_ in s for xi in xx]
    vs=[vi for _,_,vv in s for vi in vv]
    sc=ax.scatter(xs,ts,c=vs,s=0.6,cmap="turbo_r",vmin=0,vmax=2)
    seg=[];
    for t,xx,_ in s:
        if seg and xx[0]<seg[-1][0]: ax.plot(*zip(*seg),color="k",lw=1.4); seg=[]
        seg.append((xx[0],t))
    ax.plot(*zip(*seg),color="k",lw=1.4)
    tag="穩定" if a>critical_a(b,N) else "不穩定"
    ax.set_title(f"a={a}（{tag}，分界{critical_a(b,N):.3f}）")
    ax.set_xlabel("環上位置")
axs[0].set_ylabel("時間（往上）")
fig.colorbar(sc,ax=axs,label="車速（藍=快，紅=慢）",shrink=0.85)
fig.suptitle("第0台車在t=10踩一下煞車，之後22台車的速度（t=400～700），黑線是第0台車自己的軌跡",y=0.98)
fig.savefig("timespace.png",bbox_inches="tight")
print("fonts",fonts[:1])

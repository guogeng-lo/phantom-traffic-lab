import math
from ovm import *
N,b=22,2.0
for a in (1.0,1.5):
    rs=[(k,mode_rate(a,b,2*math.pi*k/N)) for k in range(1,12)]
    print(a,"fastest mode",max(rs,key=lambda r:r[1]), "k=1",rs[0][1])
# noise growth at a=1.0 unperturbed
x,v,L=uniform(N,b)
s=simulate(x,v,1.0,L,0.05,350,every=5)
for t,xx,_ in s[::10]: print(t, amplitude(xx,L))
print("fit 100-300", fit_rate(s,L,100,300))
# jam depth vs a
for a in (1.0,1.2,1.5,1.8):
    x,v,L=uniform(N,b)
    s=simulate(x,v,a,L,0.1,4000,every=1.0,brake=(0,10,11))
    tail=[vv for t,_,vv in s if t>=3500]
    print("a",a,"min",round(min(min(q) for q in tail),3),"max",round(max(max(q) for q in tail),3))

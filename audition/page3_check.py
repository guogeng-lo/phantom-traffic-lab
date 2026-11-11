import math
from ovm import *
L=44.0
print(" N     b    V(b)  V'(b)  a_c(N)   a=1.0理論  a=1.0模擬")
for N in (12,16,20,22,26,30,36,44,55):
    b=L/N
    ac=dV(b)*(1+math.cos(2*math.pi/N))
    # 模擬：k=1擾動，量成長率（線性區）
    x=[i*b for i in range(N)]; v=[V(b)]*N
    x=[(xi+1e-5*math.cos(2*math.pi*i/N))%L for i,xi in enumerate(x)]
    s=simulate(x,v,1.0,L,0.05,200,every=1.0)
    r=fit_rate(s,L,40,200)
    print(f"{N:3d} {b:5.2f} {V(b):6.3f} {dV(b):6.3f} {ac:6.3f}   {'不穩定' if 1.0<ac else '穩定':4s}   {r:+.2e}")

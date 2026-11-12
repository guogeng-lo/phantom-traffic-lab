"""M2、M5a、M6沒通過之後的診斷（2026-11-12）。這不是測試，不判通過；只是找出沒通過的原因。

看過M1～M7的結果之後才寫的，用來提出修改標準的建議給使用者決定。
"""
import cmath
import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from ovm import DT, V, Ring, mode_ring, theory_sigma  # noqa: E402


def mode_amps(r, ks):
    N, b = r.N, r.L / r.N
    h = r.headways(r.x)
    return {k: abs(sum((h[n] - b) * cmath.exp(-2j * math.pi * k * n / N) for n in range(N))) / N for k in ks}


def m2_floor():
    print("## M2：強烈衰減的N，k=1的波掉到多小")
    for N in (10, 12, 14, 15):
        r = mode_ring(N, 44.0, 1.0)
        marks = {}
        while r.t < 2100 - 1e-9:
            r.step()
            for T in (100, 500, 1000, 1500, 2100):
                if abs(r.t - T) < DT / 2:
                    marks[T] = r.k1_amplitude()
        print(f"    N={N} 理論σ {theory_sigma(1.0, 44 / N, N):+.3e}；k=1的波：" +
              "、".join(f"t={T}: {a:.1e}" for T, a in marks.items()))


def m2_contamination():
    print("## M2：N=28～32，量到t_end時其他的波有多大")
    for N in (27, 28, 30, 32, 34):
        r = mode_ring(N, 44.0, 1.0)
        while r.t < 2100 - 1e-9:
            r.step()
            if r.k1_amplitude() > 1e-3:
                break
        amps = mode_amps(r, range(1, 6))
        rates = {k: theory_sigma(1.0, 44 / N, N, k) for k in range(1, 6)}
        print(f"    N={N} t_end={r.t:.0f}：" + "、".join(f"k={k} 振幅{amps[k]:.1e}（σ{rates[k]:+.3f}）" for k in amps))


def m5a_growth():
    print("## M5a：完全均勻、不點的時候，偏差怎麼長大")
    r = Ring(22, 44.0, 1.0)
    vb = V(2.0)
    for T in (50, 100, 200, 300, 400, 436.5, 500):
        while r.t < T - 1e-9:
            r.step()
        print(f"    t={T}：最大速度偏差 {max(abs(v - vb) for v in r.v):.1e}")
    print(f"    理論σ（k=1～4）：" + "、".join(f"k={k} {theory_sigma(1.0, 2.0, 22, k):+.4f}" for k in range(1, 5)))


def m6_minspeed():
    print("## M6：塞車剛形成之後，最低車速的變化（M5b選出的煞車β=0.25、τ=0.5）")
    r = Ring(22, 44.0, 1.0)
    r.brake = (0, 20.0, 0.5, 0.25)
    out = []
    while r.t < 620 - 1e-9:
        r.step()
        if abs(r.t / 5 - round(r.t / 5)) < 1e-9 and r.t >= 100:
            out.append((r.t, min(r.v), sum(1 for v in r.v if v < 0.1)))
    for t, vmin, n in out[:30:2] + out[30::20]:
        print(f"    t={t:.0f}：最低車速 {vmin:.3f}，車速<0.1的車 {n} 台")


if __name__ == "__main__":
    m2_floor()
    m2_contamination()
    m5a_growth()
    m6_minspeed()

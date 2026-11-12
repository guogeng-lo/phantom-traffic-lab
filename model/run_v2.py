"""照model/CRITERIA.md的「第2版修改」執行M2v2、M5a v2、M6v2。

這支程式不改核心求解器：只用model/ovm.py的Ring（RK4、時間步長都沒動），新的量法和展示方式寫在這裡。
用法：python3 model/run_v2.py [M2v2 M5av2 M6v2]   （不給就全部跑）
結束代碼：有任何一項沒通過或無法判定就是1。
"""
import cmath
import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from ovm import DT, V, Ring, fit_slope, mode_ring, theory_sigma  # noqa: E402

JAM_V = 0.1
results = []


def report(name, ok, detail):
    results.append((name, ok))
    tag = {True: "通過", False: "沒通過", None: "記錄", "undecided": "無法判定"}[ok]
    print(f"[{tag}] {name}：{detail}", flush=True)


def tol(sig):
    return 2e-5 + 0.02 * abs(sig)


def run_until(r, t_end, every, f):
    rec = int(round(every / DT))
    s = 0
    while r.t < t_end - 1e-9:
        r.step()
        s += 1
        if s % rec == 0 and f(r) is False:
            break


# ---------------- M2v2 ----------------
def mode_table(N):
    ks = range(1, N // 2 + 1)
    return {k: [cmath.exp(-2j * math.pi * k * n / N) for n in range(N)] for k in ks}


def measure_v2(N, L, a, eps=1e-6):
    r = mode_ring(N, L, a, eps)
    b = L / N
    table = mode_table(N)
    pts, reason = [], "t = 2100"
    s = 0
    rec = int(round(1.0 / DT))
    while r.t < 2100 - 1e-9:
        r.step()
        s += 1
        if s % rec:
            continue
        h = r.headways(r.x)
        d = [hn - b for hn in h]
        amps = {k: abs(sum(dn * e for dn, e in zip(d, row))) / N for k, row in table.items()}
        a1 = amps[1]
        others = [amps[k] for k in amps if k != 1]
        if a1 > 1e-3:
            reason = "k=1 > 1e−3"
            break
        if a1 < 1e-10:
            reason = "k=1 < 1e−10"
            break
        if others and max(others) > 0.1 * a1:
            kmax = max((k for k in amps if k != 1), key=lambda k: amps[k])
            reason = f"k={kmax} > 0.1×k=1"
            break
        if r.t >= 100 - 1e-9:
            pts.append((r.t, math.log(a1)))
    stop = r.t
    length = (pts[-1][0] - pts[0][0]) if len(pts) >= 2 else 0.0
    sig = fit_slope(pts) if len(pts) >= 2 else float("nan")
    return sig, stop, length, reason, r


def m2v2():
    L, a = 44.0, 1.0
    rows, undecided, bad, unstable = [], [], [], []
    for N in range(3, 61):
        sm, stop, length, reason, r = measure_v2(N, L, a)
        st = theory_sigma(a, L / N, N)
        if length < 200:
            verdict = "數值無法判定"
            undecided.append(N)
        elif abs(st) < 1e-8:
            verdict = "相符（只比差距）" if abs(sm - st) <= tol(st) and r.sane() else "不符"
        else:
            verdict = "相符" if ((sm > 0) == (st > 0) and abs(sm - st) <= tol(st) and r.sane()) else "不符"
        if verdict == "不符":
            bad.append(N)
        if length >= 200 and abs(st) >= 1e-8 and sm > 0:
            unstable.append(N)
        print(f"    N={N:2d} b={L / N:.3f} σ_meas {sm:+.4e} 理論 {st:+.4e} 差 {sm - st:+.2e} "
              f"有效長度 {length:6.0f} 停止 t={stop:6.0f}（{reason}） {verdict}", flush=True)
    exact = unstable == list(range(16, 40))
    detail = (f"σ_meas > 0的N（理論|σ| ≥ 1e−8）：{min(unstable)}～{max(unstable)}（{'剛好16～39' if exact else '不是剛好16～39'}）；"
              f"不符：{bad or '沒有'}；數值無法判定：{undecided or '沒有'}")
    if undecided:
        report("M2v2 車數掃描", "undecided", detail)
    else:
        report("M2v2 車數掃描", not bad and exact, detail)


# ---------------- M5a v2 ----------------
def analytic(N, L, t):
    b = L / N
    vb = V(b)
    return [n * b + vb * t for n in range(N)], [vb] * N


class ClickDemo:
    """第2頁的展示：點擊之前用解析解；點擊那一刻用當下的解析解當RK4的初始狀態，同時開始煞車。
    內部Ring的時間從0開始，顯示用的時間是 t_click + ring.t，所以時間是接續的。"""
    def __init__(self, N, L, a):
        self.N, self.L, self.a = N, L, a
        self.ring, self.t_click = None, None

    def state(self, t):
        if self.ring is None:
            return analytic(self.N, self.L, t)
        return self.ring.x, self.ring.v

    def click(self, t0, car, tau, beta):
        x, v = analytic(self.N, self.L, t0)
        self.ring = Ring(self.N, self.L, self.a, x=x, v=v)
        self.ring.brake = (car, 0.0, tau, beta)
        self.t_click = t0

    def time(self):
        return self.t_click + self.ring.t


def m5a_v2():
    N, L, a, b = 22, 44.0, 1.0, 2.0
    vb = V(b)
    beta, tau = 0.25, 0.5
    # 1. 點擊之前
    worst_v = worst_h = 0.0
    t = 0.0
    while t <= 3000 + 1e-9:
        x, v = analytic(N, L, t)
        h = [x[n + 1] - x[n] for n in range(N - 1)] + [x[0] + L - x[N - 1]]
        worst_v = max(worst_v, max(abs(q - vb) for q in v))
        worst_h = max(worst_h, max(abs(q - b) for q in h))
        t += 0.5
    ok1 = worst_v <= 1e-12 and worst_h <= 1e-12
    report("M5a v2-1 點擊之前（解析解，t = 0～3000）", ok1, f"車速最大偏差 {worst_v:.1e}，車距最大偏差 {worst_h:.1e}（容許 1e−12）")
    # 2. 切換的連續性
    t0 = 20.0
    demo = ClickDemo(N, L, a)
    xa, va = analytic(N, L, t0)
    demo.click(t0, 0, tau, beta)
    dx = max(abs(p - q) for p, q in zip(demo.ring.x, xa))
    dv = max(abs(p - q) for p, q in zip(demo.ring.v, va))
    dt_ = abs(demo.time() - t0)
    ok2 = dx <= 1e-12 and dv <= 1e-12 and dt_ <= 1e-12
    report("M5a v2-2 切換的連續性", ok2, f"位置差 {dx:.1e}，速度差 {dv:.1e}，時間差 {dt_:.1e}（容許 1e−12）")
    # 3. 跟第1次M5b一致
    orig = Ring(N, L, a)
    orig.brake = (0, t0, tau, beta)
    o = {"jam": None, "vmin": vb, "x100": None}

    def fo(r):
        if r.t <= t0 + tau + 1:
            o["vmin"] = min(o["vmin"], r.v[0])
        if o["jam"] is None and min(r.v) < JAM_V:
            o["jam"] = r.t - t0
        if o["x100"] is None and r.t >= t0 + 100 - 1e-9:
            o["x100"] = r.x[:]
    run_until(orig, 600.0, 0.05, fo)
    d = {"jam": None, "vmin": vb, "x100": None}

    def fd(r):
        tt = t0 + r.t
        if tt <= t0 + tau + 1:
            d["vmin"] = min(d["vmin"], r.v[0])
        if d["jam"] is None and min(r.v) < JAM_V:
            d["jam"] = tt - t0
        if d["x100"] is None and tt >= t0 + 100 - 1e-9:
            d["x100"] = r.x[:]
    run_until(demo.ring, 600.0 - t0, 0.05, fd)
    djam = abs(o["jam"] - d["jam"])
    dvmin = abs(o["vmin"] - d["vmin"])
    dx100 = max(abs(p - q) for p, q in zip(o["x100"], d["x100"]))
    ok3 = djam <= 0.1 and dvmin <= 1e-6 and dx100 <= 1e-6 and orig.sane() and demo.ring.sane()
    report("M5a v2-3 跟第1次M5b一致", ok3,
           f"點之後形成塞車：原做法 {o['jam']:.2f}、新做法 {d['jam']:.2f}，差 {djam:.2f}（容許 0.1）；"
           f"被點那台最低速度差 {dvmin:.1e}（容許 1e−6）；t0+100位置最大差 {dx100:.1e}（容許 1e−6）")
    # 4. 很晚才點
    t0 = 500.0
    demo = ClickDemo(N, L, a)
    demo.click(t0, 0, tau, beta)
    late = {"jam": None}

    def fl(r):
        if late["jam"] is None and min(r.v) < JAM_V:
            late["jam"] = r.t
    run_until(demo.ring, 200.0, 0.05, fl)
    ok4 = late["jam"] is not None and late["jam"] <= 200 and demo.ring.sane() and ok1
    when = "沒有形成塞車" if late["jam"] is None else f"{late['jam']:.2f} 形成塞車"
    report("M5a v2-4 很晚才點（t0 = 500）", ok4,
           f"點之後 {when}（要 ≤ 200）；點之前完全均勻（同第1點）；S {'OK' if demo.ring.sane() else '失敗'}")


# ---------------- M6v2 ----------------
def clusters(v):
    """車速 < 0.1的車，依環道前後順序分成相鄰的群。第N−1台跟第0台相鄰。"""
    N = len(v)
    slow = [v[n] < JAM_V for n in range(N)]
    if all(slow):
        return [list(range(N))]
    start = next(n for n in range(N) if not slow[n])
    groups, cur = [], []
    for i in range(1, N + 1):
        n = (start + i) % N
        if slow[n]:
            cur.append(n)
        elif cur:
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    return groups


def track_wave(ss, N, L):
    def center(group, x, ref):
        ds = [((x[n] % L - ref + L / 2) % L) - L / 2 for n in group]
        return ref + sum(ds) / len(ds)

    track, last_group, last_pos, last_t, unwrapped = [], None, None, None, None
    for t, x, v in ss:
        gs = clusters(v)
        if last_group is None:
            big = [g for g in gs if len(g) >= 3]
            if not big:
                continue
            g = max(big, key=len)
            pos = center(g, x, x[g[0]] % L)
            unwrapped = pos
            last_group, last_pos, last_t = set(g), pos % L, t
            track.append((t, unwrapped))
            continue
        cand = [(len(set(g) & last_group), g) for g in gs]
        cand = [c for c in cand if c[0] > 0]
        if cand:
            g = max(cand, key=lambda c: c[0])[1]
        else:
            near = []
            if t - last_t <= 5 + 1e-9:
                for g in gs:
                    c = center(g, x, last_pos)
                    if abs(c - last_pos) <= 2.0:
                        near.append((abs(c - last_pos), g))
            if near:
                g = min(near)[1]
            elif t - last_t > 5 + 1e-9:
                break
            else:
                continue
        pos = center(g, x, last_pos)
        unwrapped += pos - last_pos
        last_group, last_pos, last_t = set(g), pos % L, t
        track.append((t, unwrapped))
    return track


def m6v2():
    N, L, a = 22, 44.0, 1.0
    beta, tau, t0 = 0.25, 0.5, 20.0
    r = Ring(N, L, a)
    r.brake = (0, t0, tau, beta)
    while r.t < t0 - 1e-9:
        r.step()
    samples = [(r.t, r.x[:], r.v[:])]

    def f(rr):
        samples.append((rr.t, rr.x[:], rr.v[:]))
    run_until(r, t0 + 600, 0.05, f)
    out = {}
    for step, label in ((10, "0.5"), (1, "0.05")):
        ss = samples[::step]
        mismatch = 0
        for n in range(N):
            for (_, xa, _), (_, xb, _) in zip(ss, ss[1:]):
                pa, pb = xa[n] % L, xb[n] % L
                breaks = (pa - pb) > L / 2
                lap = math.floor(xb[n] / L) != math.floor(xa[n] / L)
                if breaks != lap or (not breaks and abs(pb - pa) > L / 2):
                    mismatch += 1
        tr = track_wave(ss, N, L)
        dur = tr[-1][0] - tr[0][0] if len(tr) >= 2 else 0.0
        c = fit_slope(tr) if len(tr) >= 2 and dur >= 50 else float("nan")
        mean_v = sum(sum(v) / N for _, _, v in ss) / len(ss)
        out[label] = (mismatch, dur, c, mean_v, tr[0][0] if tr else None, tr[-1][0] if tr else None)
        print(f"    取樣Δt_s={label}：跨越起點不一致 {mismatch} 處；軌跡從t={out[label][4]}到{out[label][5]}，長 {dur:.1f}；"
              f"波速c = {c:+.4f}；車平均速度 {mean_v:.4f}", flush=True)
    m05, m005 = out["0.5"], out["0.05"]
    if m05[1] < 50 or m005[1] < 50:
        report("M6v2 時空圖", "undecided", f"軌跡長度 {m05[1]:.1f}／{m005[1]:.1f}，短於50，無法可靠量測，不報波速方向")
        return
    rel = abs(m05[2] - m005[2]) / abs(m005[2])
    ok = m05[0] == 0 and m005[0] == 0 and m05[2] < 0 and m05[3] > 0 and rel <= 0.05 and r.sane()
    report("M6v2 時空圖", ok,
           f"跨越起點不一致 {m05[0]}/{m005[0]}；波速 c = {m05[2]:+.4f}（0.5取樣）、{m005[2]:+.4f}（0.05取樣），差 {rel:.2%}（容許5%）；"
           f"車平均速度 {m05[3]:.4f}；軌跡 {m05[1]:.0f}／{m005[1]:.0f}；S {'OK' if r.sane() else '失敗'}")


def main():
    want = set(sys.argv[1:]) or {"M2v2", "M5av2", "M6v2"}
    print(f"dt = {DT}；標準見model/CRITERIA.md的「第2版修改」；核心求解器（model/ovm.py的Ring）沒有改", flush=True)
    if "M5av2" in want:
        m5a_v2()
    if "M6v2" in want:
        m6v2()
    if "M2v2" in want:
        m2v2()
    fails = [n for n, ok in results if ok is False]
    und = [n for n, ok in results if ok == "undecided"]
    print(f"\n通過 {sum(1 for _, ok in results if ok is True)} 項，沒通過 {len(fails)} 項，無法判定 {len(und)} 項。")
    if fails:
        print("沒通過：" + "、".join(fails))
    if und:
        print("無法判定：" + "、".join(und))
    return 1 if fails or und else 0


if __name__ == "__main__":
    sys.exit(main())

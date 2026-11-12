"""照model/CRITERIA.md執行M1～M7，印出設定、量到的值、通過或沒通過。

用法：python3 model/run_core.py [M1 M2 ...]   （不給就全部跑；M2要跑幾分鐘）
結束代碼：有任何一項沒通過就是1。只記錄、不判通過的項目（M5a的記錄、M5d、M7的逐台）不影響結束代碼。
"""
import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from ovm import DT, V, Ring, critical_a, measure_sigma, theory_sigma  # noqa: E402

JAM_V = 0.1
UNIFORM_DEV = 0.01
results = []


def report(name, ok, detail):
    results.append((name, ok))
    tag = "通過" if ok is True else ("沒通過" if ok is False else "記錄")
    print(f"[{tag}] {name}：{detail}", flush=True)


def tol(sig):
    return 2e-5 + 0.02 * abs(sig)


def run_until(r, t_end, every=None, on_sample=None):
    rec = int(round(every / DT)) if every else None
    s = 0
    while r.t < t_end - 1e-9:
        r.step()
        s += 1
        if rec and s % rec == 0 and on_sample:
            if on_sample(r) is False:
                break
    return r


def first_jam_time(r, t_end, every=0.5):
    hit = [None]

    def f(rr):
        if hit[0] is None and min(rr.v) < JAM_V:
            hit[0] = rr.t
    run_until(r, t_end, every, f)
    return hit[0]


# ---------------- M1 ----------------
def m1():
    N, L, b = 22, 44.0, 2.0
    lo, hi = 1.90, 2.00
    s_lo = measure_sigma(N, L, lo)[0]
    s_hi = measure_sigma(N, L, hi)[0]
    ok_bracket = s_lo > 0 > s_hi
    while hi - lo > 1e-5:
        mid = (lo + hi) / 2
        s = measure_sigma(N, L, mid)[0]
        if s > 0:
            lo = mid
        else:
            hi = mid
    a_meas = (lo + hi) / 2
    a_th = critical_a(b, N)
    report("M1 分界a", ok_bracket and abs(a_meas - 1.959493) <= 5e-4,
           f"量到 {a_meas:.6f}，公式 {a_th:.6f}，差 {a_meas - a_th:+.2e}（容許 5e-4）")
    for a in (1.90, 1.94, 1.95, 1.97, 1.98, 2.00, 2.20):
        sm, t_end, r = measure_sigma(N, L, a)
        st = theory_sigma(a, b, N)
        ok = (sm > 0) == (st > 0) and abs(sm - st) <= tol(st) and r.sane()
        report(f"M1 分界附近 a={a:.2f}", ok,
               f"σ_meas {sm:+.4e}，理論 {st:+.4e}，差 {sm - st:+.2e}（容許 {tol(st):.2e}），量到t={t_end:.0f}，S {'OK' if r.sane() else '失敗'}")


# ---------------- M2 ----------------
def m2():
    L, a = 44.0, 1.0
    bad, unstable = [], []
    for N in range(3, 61):
        sm, t_end, r = measure_sigma(N, L, a)
        st = theory_sigma(a, L / N, N)
        ok = (sm > 0) == (st > 0) and abs(sm - st) <= tol(st) and r.sane()
        if sm > 0:
            unstable.append(N)
        if not ok:
            bad.append(N)
        print(f"    N={N:2d} b={L / N:.3f} σ_meas {sm:+.4e} 理論 {st:+.4e} 差 {sm - st:+.2e} "
              f"{'OK' if ok else '不符'} t_end={t_end:.0f}", flush=True)
    rng = f"{min(unstable)}～{max(unstable)}" if unstable else "沒有"
    contiguous = unstable == list(range(16, 40))
    report("M2 車數掃描", not bad and contiguous,
           f"σ_meas > 0的N：{rng}（{len(unstable)}個，{'剛好是16～39' if contiguous else '不是剛好16～39'}）；跟理論不符的N：{bad or '沒有'}")


# ---------------- M3 ----------------
def m3():
    N, L, a = 44, 44.0, 1.0
    r = Ring(N, L, a)
    target = 0.2024334241
    worst = [0.0]

    def f(rr):
        worst[0] = max(worst[0], max(abs(v - target) for v in rr.v))
    run_until(r, 1000.0, 1.0, f)
    report("M3 44台均勻速度", worst[0] <= 1e-9 and r.sane(),
           f"V(1) = {V(1.0):.10f}；t ≤ 1000所有車速跟0.2024334241最大差 {worst[0]:.2e}（容許 1e-9）")
    sm, t_end, r2 = measure_sigma(N, L, a)
    st = theory_sigma(a, 1.0, N)
    report("M3 44台加小擾動", sm < 0 and abs(sm - st) <= tol(st) and r2.sane(),
           f"σ_meas {sm:+.4e}，理論 {st:+.4e}，差 {sm - st:+.2e}（容許 {tol(st):.2e}）")


# ---------------- M4 ----------------
def m4():
    N, L, a, b = 22, 44.0, 1.0, 2.0
    times = {}
    all_sane = True
    for eps in (0.01, 0.05, 0.1, 0.2):
        x = [n * b for n in range(N)]
        x[0] += eps
        r = Ring(N, L, a, x=x)
        tj = first_jam_time(r, 1000.0)
        times[eps] = tj
        all_sane &= r.sane()
        report(f"M4 ε={eps}", None, f"第一次有塞車 t_jam = {tj if tj is None else round(tj, 1)}；S {'OK' if r.sane() else '失敗'}")
    report("M4 ε=0.1在1000內形成塞車且全部通過S", times[0.1] is not None and all_sane, f"t_jam(0.1) = {times[0.1]}")
    if times[0.1] is not None and 60 <= times[0.1] <= 300:
        pick = 0.1
    else:
        ok = [e for e, t in times.items() if t is not None and 60 <= t <= 300]
        pick = max(ok) if ok else None
    report("M4 第1頁用的ε", None, f"{pick}（規則：0.1的t_jam在[60, 300]就用0.1，否則在範圍內的取最大）")
    return pick


# ---------------- M5 ----------------
def m5():
    N, L, b = 22, 44.0, 2.0
    # M5a
    r = Ring(N, L, 1.0)
    vb = V(b)
    lost = [None]

    def f(rr):
        if lost[0] is None and max(abs(v - vb) for v in rr.v) >= UNIFORM_DEV:
            lost[0] = rr.t
    run_until(r, 3000.0, 0.5, f)
    report("M5a 沒點時t ≤ 600一直均勻", (lost[0] is None or lost[0] > 600) and r.sane(),
           f"第一次不再均勻的時間：{'3000以內沒有' if lost[0] is None else round(lost[0], 1)}")
    # M5b
    t0 = 20.0
    combos = []
    for beta in (0.25, 0.5, 1.0):
        for tau in (0.5, 1.0, 2.0):
            r = Ring(N, L, 1.0)
            r.brake = (0, t0, tau, beta)
            vmin0, box = [vb], [None]

            def h(rr):
                if rr.t <= t0 + tau + 1:
                    vmin0[0] = min(vmin0[0], rr.v[0])
                if box[0] is None and min(rr.v) < JAM_V:
                    box[0] = rr.t
            run_until(r, 600.0, 0.05, h)
            tj = box[0]
            dt_jam = None if tj is None else tj - t0
            sane = r.sane()
            combos.append((beta, tau, dt_jam, sane))
            report(f"M5b β={beta} τ={tau}", None,
                   f"點之後 {'沒有形成塞車' if dt_jam is None else f'{dt_jam:.1f} 形成塞車'}；被點那台的最低速度 {vmin0[0]:.3f}；S {'OK' if sane else '失敗'}")
    ok = [c for c in combos if c[2] is not None and c[2] <= 200 and c[3]]
    ok.sort(key=lambda c: (c[0] * c[1], c[1]))
    pick = (ok[0][0], ok[0][1]) if ok else None
    report("M5b 第2頁用的煞車", pick is not None, f"β, τ = {pick}（規則：200以內形成塞車且通過S的組合裡，β·τ最小，同分選τ短的）")
    if pick is None:
        return None
    beta, tau = pick
    # M5c
    for a in (2.2, 2.5, 3.0):
        r = Ring(N, L, a)
        r.brake = (0, t0, tau, beta)
        jam = [False]

        def j(rr):
            if min(rr.v) < JAM_V:
                jam[0] = True
        run_until(r, t0 + 300, 0.5, j)
        A = r.max_dev()
        report(f"M5c a={a}", (not jam[0]) and A < 0.01 and r.sane(),
               f"{'有' if jam[0] else '沒有'}塞車，A(t0+300) = {A:.2e}（要 < 0.01）")
    # M5d
    for a in (1.90, 1.94, 1.98, 2.02, 2.05, 2.10):
        for mult in (1, 3):
            r = Ring(N, L, a)
            r.brake = (0, t0, tau, beta * mult)
            jam = [None]
            A300 = [None]

            def k(rr):
                if jam[0] is None and min(rr.v) < JAM_V:
                    jam[0] = rr.t
                if A300[0] is None and rr.t >= t0 + 300 - 1e-9:
                    A300[0] = rr.max_dev()
            run_until(r, t0 + 1500, 0.5, k)
            report(f"M5d a={a:.2f} 煞車×{mult}", None if r.sane() else False,
                   f"{'沒有塞車' if jam[0] is None else f'點之後 {jam[0] - t0:.0f} 形成塞車'}；A(t0+300) = {A300[0]:.3e}，A(t0+1500) = {r.max_dev():.3e}；"
                   f"理論σ {theory_sigma(a, b, N):+.2e}；S {'OK' if r.sane() else '失敗'}")
    return pick


# ---------------- M6 ----------------
def m6(pick):
    N, L, a, b = 22, 44.0, 1.0, 2.0
    beta, tau = pick
    t0 = 20.0
    r = Ring(N, L, a)
    r.brake = (0, t0, tau, beta)
    run_until(r, t0)
    samples = []   # 每0.05記一次，0.5的取樣用每10筆取1筆

    def f(rr):
        samples.append((rr.t, rr.x[:], rr.v[:]))
    samples.append((r.t, r.x[:], r.v[:]))
    run_until(r, t0 + 600, 0.05, f)
    sane = r.sane()

    def check(step, label):
        ss = samples[::step]
        # 跨越起點：斷開 ⇔ 圈數改變
        mismatch = 0
        for n in range(N):
            for (_, xa, _), (_, xb, _) in zip(ss, ss[1:]):
                pa, pb = xa[n] % L, xb[n] % L
                breaks = (pa - pb) > L / 2
                lap = math.floor(xb[n] / L) != math.floor(xa[n] / L)
                if breaks != lap:
                    mismatch += 1
                if not breaks and abs(pb - pa) > L / 2:
                    mismatch += 1
        # 追同一團塞車
        track, prev, start = [], None, None
        for t, x, v in ss:
            jam_cars = [n for n in range(N) if v[n] < 0.1]
            if prev is None:
                if not jam_cars:
                    continue
                n0 = min(jam_cars, key=lambda n: v[n])
                prev, unwrapped, start = x[n0] % L, x[n0] % L, t
                track.append((t, unwrapped))
                continue
            if not jam_cars:
                break
            ds = [((x[n] % L - prev + L / 2) % L) - L / 2 for n in jam_cars]
            d = min(ds, key=abs)
            unwrapped += d
            prev = (prev + d) % L
            track.append((t, unwrapped))
        dur = track[-1][0] - track[0][0] if track else 0
        if len(track) >= 2:
            n_ = len(track)
            mt = sum(p[0] for p in track) / n_
            my = sum(p[1] for p in track) / n_
            c = sum((p[0] - mt) * (p[1] - my) for p in track) / sum((p[0] - mt) ** 2 for p in track)
        else:
            c = float("nan")
        mean_v = sum(sum(v) / N for _, _, v in ss) / len(ss)
        print(f"    取樣{label}：跨越起點不一致 {mismatch} 處；塞車軌跡長 {dur:.1f}（從t={start}），波速c = {c:+.4f}，車平均速度 {mean_v:.4f}", flush=True)
        return mismatch, dur, c, mean_v

    m05 = check(10, "Δt_s=0.5")
    m005 = check(1, "Δt_s=0.05")
    rel = abs(m05[2] - m005[2]) / abs(m005[2]) if m005[2] == m005[2] and m005[2] != 0 else float("inf")
    ok = (m05[0] == 0 and m005[0] == 0 and m05[1] >= 50 and m05[2] < 0 and m05[3] > 0 and rel <= 0.05 and sane)
    report("M6 時空圖", ok,
           f"跨越起點不一致 {m05[0]}/{m005[0]}；波速 c = {m05[2]:+.4f}（0.5取樣）、{m005[2]:+.4f}（0.05取樣），差 {rel:.2%}（容許5%）；"
           f"車平均速度 {m05[3]:.4f}；軌跡 {m05[1]:.0f}（要 ≥ 50）；S {'OK' if sane else '失敗'}")


# ---------------- M7 ----------------
def m7(pick):
    N, L, b = 22, 44.0, 2.0
    beta, tau = pick
    t0 = 20.0
    for a, want in ((1.0, "grow"), (2.5, "decay")):
        r = Ring(N, L, a)
        r.brake = (0, t0, tau, beta)
        A5 = [None]
        mins = [V(b)] * N

        def f(rr):
            if A5[0] is None and rr.t >= t0 + 5 - 1e-9:
                A5[0] = rr.max_dev()
            if t0 <= rr.t <= t0 + 100 + 1e-9:
                for n in range(N):
                    mins[n] = min(mins[n], rr.v[n])
        run_until(r, t0 + 200, 0.05, f)
        A200 = r.max_dev()
        ok = (A200 > 2 * A5[0]) if want == "grow" else (A200 < 0.5 * A5[0])
        report(f"M7 a={a}", ok and r.sane(),
               f"A(t0+5) = {A5[0]:.3e}，A(t0+200) = {A200:.3e}，比值 {A200 / A5[0]:.2f}（{'要 > 2' if want == 'grow' else '要 < 0.5'}）")
        follow = [mins[(0 - j) % N] for j in range(1, N)]
        lower = sum(1 for p, q in zip([mins[0]] + follow, follow) if q < p)
        report(f"M7 a={a} 逐台", None,
               "被點那台後面第1～21台在[t0, t0+100]的最低速度：" + "、".join(f"{m:.3f}" for m in follow) +
               f"；比前一台低的有 {lower} 台（共21台）")


def main():
    want = set(sys.argv[1:]) or {"M1", "M2", "M3", "M4", "M5", "M6", "M7"}
    print(f"dt = {DT}，V(h) = tanh(h−2)+tanh2；標準見model/CRITERIA.md", flush=True)
    if "M1" in want:
        m1()
    if "M2" in want:
        m2()
    if "M3" in want:
        m3()
    if "M4" in want:
        m4()
    pick = None
    if want & {"M5", "M6", "M7"}:
        pick = m5()
    if pick is not None and "M6" in want:
        m6(pick)
    if pick is not None and "M7" in want:
        m7(pick)
    fails = [n for n, ok in results if ok is False]
    print(f"\n通過 {sum(1 for _, ok in results if ok is True)} 項，沒通過 {len(fails)} 項，只記錄 {sum(1 for _, ok in results if ok is None)} 項。")
    if fails:
        print("沒通過：" + "、".join(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

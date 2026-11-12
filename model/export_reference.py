"""用Python參考模型算對答案用的參考答案，存成web/reference/parity-ref.json。項目和設定照web/PARITY.md（J1～J10）。

用法：python3 model/export_reference.py
這支程式只是把既有的Python參考模型（ovm.py、run_v2.py、run_v3_m2.py的規則、explore_smoothing.py）跑一遍、存結果，不改任何模型。
"""
import json
import math
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from ovm import DT, V, Ring, fit_slope, theory_sigma  # noqa: E402
from run_v2 import ClickDemo, measure_v2, tol, track_wave  # noqa: E402
import explore_smoothing as sm  # noqa: E402

N, L = 22, 44.0
BETA, TAU = 0.25, 0.5


def sample_every(r, s_end, every=0.5, rec_fn=None):
    out = [rec_fn(r)]
    k = int(round(every / DT))
    steps = 0
    while r.t < s_end - 1e-9:
        r.step()
        steps += 1
        if steps % k == 0:
            out.append(rec_fn(r))
    return out


def j1():
    rows = []
    for t0, tau in ((0, 0.5), (20, 0.5), (19.95, 0.5), (500, 0.5), (0.07, 0.5), (20, 0.33)):
        r = Ring(N, L, 1.0)
        r.brake = (0, t0, tau, BETA)
        try:
            w = r.brake_window()
            rows.append({"t0": t0, "tau": tau, "k0": w[1], "k1": w[2]})
        except ValueError:
            rows.append({"t0": t0, "tau": tau, "error": True})
    return rows


def first_jam_step(r, max_steps):
    for _ in range(max_steps):
        r.step()
        if min(r.v) < 0.1:
            return r._steps
    return None


def j2_j3():
    rows = []
    for tc, car in ((0, 0), (20, 0), (123.45, 7), (500, 21), (3000, 13)):
        d = ClickDemo(N, L, 1.0)
        d.click(tc, car, TAU, BETA)
        traj = sample_every(d.ring, 400.0, 0.5, lambda r: [r.x[:], r.v[:]])
        d2 = ClickDemo(N, L, 1.0)
        d2.click(tc, car, TAU, BETA)
        jam = first_jam_step(d2.ring, 10000)
        rows.append({"tc": tc, "car": car, "traj": traj, "jamStep": jam, "sane": d.ring.sane()})
    return rows


def j4():
    rows = []
    for eps in (0.01, 0.1, 0.2):
        x = [n * 2.0 for n in range(N)]
        x[0] += eps
        r = Ring(N, L, 1.0, x=x)
        jam = None
        while r.t < 1000 - 1e-9:
            r.step()
            if jam is None and min(r.v) < 0.1:
                jam = r._steps
            if r._steps == 3000:
                state = [r.x[:], r.v[:]]
            if jam is not None and r._steps >= 3000:
                break
        rows.append({"eps": eps, "jamStep": jam, "state150": state, "sane": r.sane()})
    return rows


def j5():
    rows = []
    for a in (1.0, 2.5):
        d = ClickDemo(N, L, a)
        d.click(20.0, 0, TAU, BETA)
        followers = [(0 - j) % N for j in (1, 5, 10, 15)]
        traj = sample_every(d.ring, 100.0, 0.5, lambda r: [r.v[n] for n in followers])
        d2 = ClickDemo(N, L, a)
        d2.click(20.0, 0, TAU, BETA)
        A = {}
        while d2.ring.t < 200 - 1e-9:
            d2.ring.step()
            if d2.ring._steps in (100, 4000):
                A[str(d2.ring._steps)] = d2.ring.max_dev()
        rows.append({"a": a, "followers": followers, "speeds": traj, "A5": A["100"], "A200": A["4000"], "sane": d2.ring.sane()})
    return rows


def j6():
    rows = []
    for a in (1.0, 1.90, 1.98, 2.2, 2.5, 3.0):
        d = ClickDemo(N, L, a)
        d.click(20.0, 0, TAU, BETA)
        row = {"a": a}
        if a == 1.0:
            row["jamStep"] = first_jam_step(d.ring, 40000)
        else:
            end = 1500 if a in (1.90, 1.98) else 300
            while d.ring.t < end - 1e-9:
                d.ring.step()
                if d.ring._steps == 6000:
                    row["A300"] = d.ring.max_dev()
            if end == 1500:
                row["A1500"] = d.ring.max_dev()
        row["sane"] = d.ring.sane()
        rows.append(row)
    return rows


def j7():
    a = 1.0
    rows = []
    for n in range(3, 61):
        st = theory_sigma(a, L / n, n)
        sig, stop, length, reason, r = measure_v2(n, L, a)
        runs = [{"eps": 1e-6, "sigma": sig, "stop": stop, "length": length, "reason": reason, "sane": r.sane()}]
        if length < 200:
            verdicts = []
            for eps in (1e-7, 1e-8):
                s2, stop2, len2, rs2, r2 = measure_v2(n, L, a, eps)
                runs.append({"eps": eps, "sigma": s2, "stop": stop2, "length": len2, "reason": rs2, "sane": r2.sane()})
                enough = len2 >= 200
                match = (s2 > 0) == (st > 0) and abs(s2 - st) <= tol(st) and r2.sane()
                verdicts.append((enough, match))
            sufficient = [m for e, m in verdicts if e]
            verdict = "數值無法判定" if not sufficient else ("相符" if all(sufficient) else "不符")
        elif abs(st) < 1e-8:
            verdict = "相符（只比差距）" if abs(sig - st) <= tol(st) and r.sane() else "不符"
        else:
            verdict = "相符" if ((sig > 0) == (st > 0) and abs(sig - st) <= tol(st) and r.sane()) else "不符"
        rows.append({"N": n, "theory": st, "runs": runs, "verdict": verdict})
        print(f"  J7 N={n}: {verdict}", flush=True)
    return rows


def j8():
    t0 = 20.0
    r = Ring(N, L, 1.0)
    r.brake = (0, t0, TAU, BETA)
    while r.t < t0 - 1e-9:
        r.step()
    samples = [(r.t, r.x[:], r.v[:])]
    k = int(round(0.5 / DT))
    steps = 0
    while r.t < t0 + 600 - 1e-9:
        r.step()
        steps += 1
        if steps % k == 0:
            samples.append((r.t, r.x[:], r.v[:]))
    tr = track_wave(samples, N, L)
    c = fit_slope(tr)
    mean_v = sum(sum(v) / N for _, _, v in samples) / len(samples)
    return {"trackStart": tr[0][0], "trackEnd": tr[-1][0], "trackLen": len(tr), "c": c, "meanV": mean_v, "sane": r.sane()}


def j9():
    eps = 0.1
    cases = {"R0": None, "R1": sm.AvgRule(), "R2": sm.ClampRule(), "R3": sm.TargetRule(V(2.0))}
    for mult in (0.9, 1.0, 1.05, 1.1, 1.2):
        cases[f"U{mult}"] = sm.TargetRule(V(2.0) * mult)
    return {k: sm.run(rule, eps) for k, rule in cases.items()}


def main():
    t = time.time()
    out = {"source": "model/export_reference.py（Python參考模型）", "DT": DT,
           "J1": j1(), "J2": j2_j3(), "J4": j4(), "J5": j5(), "J6": j6(), "J8": j8(), "J9": j9()}
    print("J1～J6、J8、J9完成", flush=True)
    out["J7"] = j7()
    dest = HERE.parent / "web" / "reference" / "parity-ref.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":"), allow_nan=True), encoding="utf-8")
    print(f"已寫入 {dest.relative_to(HERE.parent)}，{dest.stat().st_size // 1024} KB，{time.time() - t:.0f} 秒")


if __name__ == "__main__":
    main()

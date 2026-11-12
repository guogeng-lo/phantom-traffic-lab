"""照model/CRITERIA.md的M8、M9探索平滑車規則。這是探索，不擋核心頁面；結果好壞都照實記錄。

這裡的平滑車規則都是我們自己設計的，不是Stern 2018的控制器。
用法：python3 model/explore_smoothing.py
"""
import collections
import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from ovm import DT, V, Ring  # noqa: E402

N, L, A = 22, 44.0, 1.0
T_SWITCH, T_END, W0, W1 = 300.0, 1500.0, 1000.0, 1500.0


def pick_eps():
    """跟run_core.m4同一條規則選ε（不印出逐項結果）。"""
    times = {}
    for eps in (0.01, 0.05, 0.1, 0.2):
        x = [n * 2.0 for n in range(N)]
        x[0] += eps
        r = Ring(N, L, A, x=x)
        tj = None
        while r.t < 1000 - 1e-9:
            r.step()
            if tj is None and min(r.v) < 0.1:
                tj = r.t
                break
        times[eps] = tj
    if times[0.1] is not None and 60 <= times[0.1] <= 300:
        return 0.1
    ok = [e for e, t in times.items() if t is not None and 60 <= t <= 300]
    return max(ok) if ok else None


class AvgRule:
    """R1：a_s·(min(U_avg, V(h)) − v)，U_avg是自己過去50時間單位的平均速度。"""
    def __init__(self, a_s=1.0, window=50.0):
        self.a_s, self.buf = a_s, collections.deque(maxlen=int(round(window / DT)))

    def observe(self, ring, n):
        self.buf.append(ring.v[n])

    def __call__(self, ring, n, x, v, h):
        u = sum(self.buf) / len(self.buf) if self.buf else v[n]
        return self.a_s * (min(u, V(h[n])) - v[n])


class ClampRule:
    """R2：照原本的模型，但加速度限制在±c。"""
    def __init__(self, c=0.05):
        self.c = c

    def observe(self, ring, n):
        pass

    def __call__(self, ring, n, x, v, h):
        acc = ring.a * (V(h[n]) - v[n])
        return max(-self.c, min(self.c, acc))


class TargetRule:
    """R3：a_s·(min(U, V(h)) − v)，U是固定的目標速度。"""
    def __init__(self, U, a_s=1.0):
        self.U, self.a_s = U, a_s

    def observe(self, ring, n):
        pass

    def __call__(self, ring, n, x, v, h):
        return self.a_s * (min(self.U, V(h[n])) - v[n])


def run(rule, eps):
    x = [n * 2.0 for n in range(N)]
    x[0] += eps
    r = Ring(N, L, A, x=x)
    speeds, jam_samples, samples = [], 0, 0
    rec = int(round(0.5 / DT))
    s = 0
    while r.t < T_END - 1e-9:
        if rule is not None and r.t >= T_SWITCH - 1e-9 and r.smooth is None:
            r.smooth = (0, rule)
        r.step()
        s += 1
        if r.smooth is not None:
            rule.observe(r, 0)
        elif rule is not None and isinstance(rule, AvgRule):
            rule.observe(r, 0)   # 換成平滑車之前，先記下它自己的速度，切換時才有過去50的平均
        if s % rec == 0 and W0 - 1e-9 <= r.t <= W1 + 1e-9:
            speeds.extend(r.v)
            samples += 1
            jam_samples += min(r.v) < 0.1
    m = sum(speeds) / len(speeds)
    std = math.sqrt(sum((q - m) ** 2 for q in speeds) / len(speeds))
    return {"std": std, "vmin": min(speeds), "jam_frac": jam_samples / samples, "mean": m, "sane": r.sane(),
            "min_h": r.min_h}


def fmt(name, res):
    return (f"{name}：車速標準差 {res['std']:.4f}，最低車速 {res['vmin']:.4f}，有塞車的時間比例 {res['jam_frac']:.0%}，"
            f"平均車速 {res['mean']:.4f}，最小車距 {res['min_h']:.3f}，S {'OK' if res['sane'] else '失敗'}")


def main():
    eps = pick_eps()
    print(f"M8、M9：N={N}、L={L:g}、a={A:g}；初始偏移ε={eps}（M4的規則）；t={T_SWITCH:g}把第0台換成平滑車；比較區間[{W0:g}, {W1:g}]")
    print("這些規則都是我們設計的，不是Stern 2018的控制器。\n")
    base = run(None, eps)
    print("[記錄] " + fmt("R0 基準（不換）", base))
    rules = [("R1 自己過去50的平均速度", AvgRule()), ("R2 加速度限制±0.05", ClampRule()),
             ("R3 固定目標速度U=V(2)", TargetRule(V(2.0)))]
    for name, rule in rules:
        res = run(rule, eps)
        effective = res["std"] <= 0.5 * base["std"] and res["vmin"] >= 0.1 and res["sane"]
        teaching = base["jam_frac"] > 0 and res["jam_frac"] == 0
        print(f"[{'有效' if effective else '無效'}{'、有教學價值' if effective and teaching else ''}] " + fmt(name, res)
              + f"；標準差是R0的 {res['std'] / base['std']:.0%}")
    print("\nM9：R3改變目標速度U（不預設結果）")
    for mult in (0.9, 1.0, 1.05, 1.1, 1.2):
        res = run(TargetRule(V(2.0) * mult), eps)
        print("[記錄] " + fmt(f"U = V(2)×{mult}", res) + f"；標準差是R0的 {res['std'] / base['std']:.0%}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

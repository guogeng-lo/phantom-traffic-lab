"""幽靈塞車試鏡：A穩定性、B數值正確性、C可觀察性。

執行：python3 test_ovm.py
每一項印出 預期／實際／PASS或FAIL，最後印總結。只用標準函式庫。
"""
import math
from ovm import (V, dV, uniform, mode_perturb, simulate, amplitude, fit_rate,
                 mode_rate, critical_a, headways)

N, B = 22, 2.0          # 22台車，均勻車距2（無因次），V'(2)=1，正好是最敏感的地方
TH = 2 * math.pi / N    # 最長的波 k=1
results = []


def check(name, ok, expect, actual):
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    print(f"    預期：{expect}")
    print(f"    實際：{actual}")


def rate_at(a, b=B, dt=0.05, t1=50, t2=250):
    x, v, L = uniform(N, b)
    x = mode_perturb(x, N, b, 1, 1e-4)
    s = simulate(x, v, a, L, dt, t2, every=1.0)
    return fit_rate(s, L, t1, t2)


print("=== A 穩定性 ===")

# A1 沒有擾動就維持均勻（穩定區）
x, v, L = uniform(N, B)
s = simulate(x, v, 2.4, L, 0.05, 1000, every=10)
mx = max(amplitude(xx, L) for _, xx, _ in s)
check("A1 穩定區（a=2.4）沒有擾動，跑到t=1000車距一直均勻", mx < 1e-9,
      "車距標準差一直 < 1e-9", f"最大 {mx:.2e}")

# A1b 不穩定區沒有擾動：理論上也是均勻的，但這是不穩定的平衡，電腦的捨入誤差會被放大。
# 第1次執行時這裡用「t≤300 < 1e-9」當標準，失敗了：放大最快的不是k=1，見CHECKLOG.md。
# 改成：捨入誤差的成長率要對上「所有波裡放大最快的那個」。
x, v, L = uniform(N, B)
s = simulate(x, v, 1.0, L, 0.05, 300, every=5)
m = fit_rate(s, L, 100, 300)
kf, pf = max(((k, mode_rate(1.0, B, 2 * math.pi * k / N)) for k in range(1, N // 2 + 1)),
             key=lambda r: r[1])
check("A1b 不穩定區（a=1.0）沒有擾動：捨入誤差照「最快的波」放大",
      abs(m - pf) <= 0.05 * pf,
      f"跟理論最快的波 k={kf}（成長率 {pf:.4f}）差 ≤5%",
      f"{m:.4f}（差 {abs(m - pf) / pf:.1%}）；同條件下k=1只有 {mode_rate(1.0, B, TH):.4f}")

# A1c 單獨激發k=3，確認它真的比k=1快、而且對上理論
x, v, L = uniform(N, B)
x = mode_perturb(x, N, B, 3, 1e-6)
s = simulate(x, v, 1.0, L, 0.05, 150, every=1.0)
m = fit_rate(s, L, 30, 150)
p = mode_rate(1.0, B, 2 * math.pi * 3 / N)
check("A1c a=1.0 只激發k=3：成長率對上理論", abs(m - p) <= 0.01 * p,
      f"{p:.6f}，差 ≤1%", f"{m:.6f}（差 {abs(m - p) / p:.2e}）")

# A2 穩定區：k=1擾動衰減，衰減率對上線性理論
for a in (2.4, 3.0):
    m, p = rate_at(a), mode_rate(a, B, TH)
    check(f"A2 穩定區 a={a}：擾動衰減，速率對上理論",
          m < 0 and abs(m - p) <= 0.01 * abs(p),
          f"負的，跟理論 {p:.6f} 差 ≤1%", f"{m:.6f}（差 {abs(m - p) / abs(p):.2e}）")

# A3 不穩定區：同樣的擾動放大，成長率對上線性理論
for a in (1.0, 1.5):
    m, p = rate_at(a), mode_rate(a, B, TH)
    check(f"A3 不穩定區 a={a}：擾動放大，速率對上理論",
          m > 0 and abs(m - p) <= 0.01 * abs(p),
          f"正的，跟理論 {p:.6f} 差 ≤1%", f"{m:.6f}（差 {abs(m - p) / abs(p):.2e}）")

# A4 從模擬找出分界，跟公式比
for b in (2.0, 2.5):
    ac = critical_a(b, N)
    lo, hi = ac - 0.02, ac + 0.02
    rlo, rhi = rate_at(lo, b, t2=400), rate_at(hi, b, t2=400)
    est = lo + (hi - lo) * rlo / (rlo - rhi)   # 成長率對a線性內插找零點
    check(f"A4 b={b}：模擬算出的分界 vs 公式 V'(b)(1+cos(2π/22))",
          rlo > 0 > rhi and abs(est - ac) < 1e-3,
          f"{ac:.5f}（論文的無限長公式 2V'(b) = {2 * dV(b):.5f}）",
          f"{est:.5f}（a={lo:.3f}成長率 {rlo:+.2e}，a={hi:.3f}成長率 {rhi:+.2e}）")

# A4b 22台車的分界不是剛好a/2：a=1.98時無限長公式說不穩定，但22台的環其實穩定
m = rate_at(1.98, t2=400)
check("A4b a=1.98（2V'=2 和 22台分界1.9595之間）：有限環應該穩定",
      m < 0, "成長率是負的（照無限長公式會以為是正的）", f"{m:+.2e}")

# A5 比較像真的情況：一台車踩一下煞車
def brake_run(a, t_end=3000, dt=0.1):
    x, v, L = uniform(N, B)
    s = simulate(x, v, a, L, dt, t_end, every=1.0, brake=(0, 10.0, 11.0))
    return s, L

for a, want in ((2.4, "衰減"), (1.5, "放大")):
    s, L = brake_run(a)
    a0 = max(amplitude(xx, L) for t, xx, _ in s if 10 <= t <= 40)
    a_end = amplitude(s[-1][1], L)
    ok = a_end < a0 * 0.1 if want == "衰減" else a_end > a0 * 10
    check(f"A5 a={a}：第0台車在t=10踩煞車1個時間單位，最後要{want}", ok,
          "最後車距波動 < 一開始的1/10" if want == "衰減" else "最後車距波動 > 一開始的10倍",
          f"一開始 {a0:.3e}，t=3000 {a_end:.3e}")

print("\n=== B 數值正確性 ===")

s, L = brake_run(1.5, t_end=3000, dt=0.1)
min_h = min(min(headways(xx, L)) for _, xx, _ in s)
max_err = max(abs(sum(headways(xx, L)) - L) for _, xx, _ in s)
check("B1 塞車全程：車距都 > 0、車距總和 = 環長（沒有撞車、超車）",
      min_h > 0 and max_err < 1e-9, "最小車距 > 0，總和誤差 < 1e-9",
      f"最小車距 {min_h:.4f}，總和誤差 {max_err:.1e}")

r = [rate_at(1.5, dt=d) for d in (0.2, 0.1, 0.05)]
spread = (max(r) - min(r)) / abs(r[-1])
check("B2 時間步長 0.2/0.1/0.05，成長率一致", spread < 1e-4,
      "相對差 < 1e-4", f"{r[0]:.8f} / {r[1]:.8f} / {r[2]:.8f}（相對差 {spread:.1e}）")

def jam_stats(dt):
    s, L = brake_run(1.5, t_end=3000, dt=dt)
    tail = [vv for t, _, vv in s if t >= 2500]
    return min(min(v) for v in tail), max(max(v) for v in tail)

(a1, b1), (a2, b2) = jam_stats(0.1), jam_stats(0.05)
check("B3 時間步長 0.1/0.05，塞車成形後的最低、最高車速一致",
      abs(a1 - a2) < 0.01 and abs(b1 - b2) < 0.01, "兩者差 < 0.01",
      f"最低 {a1:.4f}/{a2:.4f}，最高 {b1:.4f}/{b2:.4f}")

print("\n=== C 可觀察性 ===")

# 第1次執行時C1只看a=1.5、門檻「最低 < 0.2倍均勻車速」是隨便定的，失敗了（最低0.253）。
# a=1.5離分界1.96很近，塞車本來就淺。改成掃a，檢查兩件有根據的事：
# 離分界越遠塞得越深（最低車速隨a變小而下降），以及最深的那組要有車幾乎停下。
depth = []
for a in (1.0, 1.2, 1.5, 1.8):
    s, L = brake_run(a, t_end=4000, dt=0.1)
    tail = [vv for t, _, vv in s if t >= 3500]
    depth.append((a, min(min(q) for q in tail), max(max(q) for q in tail)))
mono = all(depth[i][1] < depth[i + 1][1] for i in range(len(depth) - 1))
txt = "；".join(f"a={a} 最低{lo:.3f} 最高{hi:.3f}" for a, lo, hi in depth)
check("C1 離分界越遠塞得越深，a=1.0 有車幾乎停下",
      mono and depth[0][1] < 0.1 * V(B),
      f"最低車速隨a增加而上升；a=1.0最低 < {0.1 * V(B):.3f}（均勻車速的1/10）", txt)

s, L = brake_run(1.5, t_end=3000, dt=0.1)
tail = [(t, xx, vv) for t, xx, vv in s if t >= 2500]

# 追蹤最慢那台車的位置，看塞車波往哪個方向走
def slowest_pos(xx, vv):
    i = min(range(N), key=lambda k: vv[k])
    return xx[i]

pos = [(t, slowest_pos(xx, vv)) for t, xx, vv in tail]
# 用相鄰兩點的位移（考慮繞圈）算平均速度
moves = []
for (t0, p0), (t1, p1) in zip(pos, pos[1:]):
    d = (p1 - p0 + L / 2) % L - L / 2
    moves.append(d / (t1 - t0))
moves.sort()
wave = moves[len(moves) // 2]
mean_v = sum(sum(vv) / N for _, _, vv in tail) / len(tail)
check("C2 塞車波往後走（跟車流方向相反），車子本身往前",
      wave < 0 < mean_v, "塞車波速度 < 0 < 車流平均速度",
      f"塞車波 {wave:.3f}（中位數），車流平均 {mean_v:.3f}")

print(f"\n共{len(results)}項，失敗{results.count(False)}項。")

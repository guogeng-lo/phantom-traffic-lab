"""Bando等人1995年的最佳速度模型（OVM），環狀道路，只用Python標準函式庫。

dv_n/dt = a [V(h_n) - v_n]，h_n是第n台車到前車的車距。
V(h) = tanh(h - 2) + tanh(2)，用Bando論文的無因次單位。
車子的位置每一步都對環長L取餘數（跟之後動畫的做法一樣），
車距用 (前車位置 - 自己位置) mod L 算，所以如果有車超車或撞車，
車距總和就不會剛好等於L，測試抓得到。
"""
import cmath
import math


def V(h):
    return math.tanh(h - 2.0) + math.tanh(2.0)


def dV(h):
    return 1.0 / math.cosh(h - 2.0) ** 2


def headways(x, L):
    n = len(x)
    return [(x[(i + 1) % n] - x[i]) % L for i in range(n)]


def deriv(x, v, a, L):
    h = headways(x, L)
    return v[:], [a * (V(h[i]) - v[i]) for i in range(len(x))]


def rk4_step(x, v, a, L, dt):
    k1x, k1v = deriv(x, v, a, L)
    x2 = [(xi + 0.5 * dt * k) % L for xi, k in zip(x, k1x)]
    v2 = [vi + 0.5 * dt * k for vi, k in zip(v, k1v)]
    k2x, k2v = deriv(x2, v2, a, L)
    x3 = [(xi + 0.5 * dt * k) % L for xi, k in zip(x, k2x)]
    v3 = [vi + 0.5 * dt * k for vi, k in zip(v, k2v)]
    k3x, k3v = deriv(x3, v3, a, L)
    x4 = [(xi + dt * k) % L for xi, k in zip(x, k3x)]
    v4 = [vi + dt * k for vi, k in zip(v, k3v)]
    k4x, k4v = deriv(x4, v4, a, L)
    xn = [(xi + dt / 6 * (p + 2 * q + 2 * r + s)) % L
          for xi, p, q, r, s in zip(x, k1x, k2x, k3x, k4x)]
    vn = [vi + dt / 6 * (p + 2 * q + 2 * r + s)
          for vi, p, q, r, s in zip(v, k1v, k2v, k3v, k4v)]
    return xn, vn


def uniform(N, b):
    L = N * b
    return [i * b for i in range(N)], [V(b)] * N, L


def mode_perturb(x, N, b, k, eps):
    L = N * b
    return [(xi + eps * math.cos(2 * math.pi * k * i / N)) % L for i, xi in enumerate(x)]


def simulate(x, v, a, L, dt, t_end, every=1.0, brake=None):
    """brake=(car, t0, t1)：這段時間把那台車的加速度換成強制減速-0.5（模擬踩一下煞車）。"""
    out = []
    t = 0.0
    steps = int(round(t_end / dt))
    rec = max(1, int(round(every / dt)))
    for s in range(steps + 1):
        if s % rec == 0:
            out.append((t, x[:], v[:]))
        if s == steps:
            break
        if brake and brake[1] <= t < brake[2]:
            c = brake[0]
            # 踩煞車：這一步把那台車的速度往下拉，其餘照模型
            x, v = rk4_step(x, v, a, L, dt)
            v[c] = max(0.0, v[c] - 0.5 * dt)
        else:
            x, v = rk4_step(x, v, a, L, dt)
        t += dt
    return out


def amplitude(x, L):
    h = headways(x, L)
    m = sum(h) / len(h)
    return math.sqrt(sum((hi - m) ** 2 for hi in h) / len(h))


def fit_rate(samples, L, t1, t2):
    """對ln(車距標準差)做線性回歸，斜率就是成長率（負的就是衰減率）。"""
    pts = [(t, math.log(amplitude(x, L))) for t, x, _ in samples if t1 <= t <= t2]
    n = len(pts)
    mt = sum(p[0] for p in pts) / n
    my = sum(p[1] for p in pts) / n
    num = sum((p[0] - mt) * (p[1] - my) for p in pts)
    den = sum((p[0] - mt) ** 2 for p in pts)
    return num / den


# ---- 線性理論 ----
# 把 y_n = e^{i θ n + z t} 代進線性化方程式：z^2 + a z - a V'(b) (e^{iθ} - 1) = 0

def mode_rate(a, b, theta):
    c = a * a + 4 * a * dV(b) * (cmath.exp(1j * theta) - 1)
    r = cmath.sqrt(c)
    return max(((-a + r) / 2).real, ((-a - r) / 2).real)


def critical_a(b, N):
    """有限N台車：a往下調時，最先變不穩定的是最長的波（k=1），界線是 a = V'(b) (1 + cos(2π/N))。
    N→∞時變成 a = 2V'(b)，也就是論文的 V'(b) > a/2。
    注意：「最先變不穩定」不等於「放大最快」，a離分界越遠，放大最快的波越短（a=1.0時是k=3）。"""
    return dV(b) * (1 + math.cos(2 * math.pi / N))

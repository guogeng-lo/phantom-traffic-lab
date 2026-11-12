"""正式參考模型：Bando等人1995年的最佳速度模型（OVM），環狀道路。只用Python標準函式庫。

dv_n/dt = a[V(h_n) - v_n] + f_n(t)
V(h) = tanh(h - 2) + tanh(2)                    （Bando式(1)、(24)，無因次）
h_n = x_{n+1} - x_n，最後一台的前車是第0台（車距加L）

跟audition/ovm.py不同的地方：
- 位置用不取餘數的累積位置，畫圖時才對L取餘數。
- 煞車寫在微分方程式裡（f_n(t) = -β），跟RK4一起積分，不是每一步之後硬改速度。
- 煞車用整數步數判定（2026-11-12第3版標準）：(車, t0, τ, β)換算成開始步t0/dt、步數τ/dt，
  兩個都要是整數，否則報錯。一個煞車步裡RK4的四次評估都加煞車，其他步都不加。
  不用浮點時間比大小，避免像第399步最後一個子步算成20.000000000000004而提早生效。
- 每一步都做物理檢查（車距 > 0、車速 >= -1e-9、車距總和 = L）。
- 可以把某一台車換成平滑車（M8、M9用）。
測試標準在model/CRITERIA.md，寫程式之前就commit了。
"""
import cmath
import math

TANH2 = math.tanh(2.0)
DT = 0.05


def V(h):
    return math.tanh(h - 2.0) + TANH2


def dV(h):
    return 1.0 / math.cosh(h - 2.0) ** 2


def theory_sigma(a, b, N, k=1):
    """Bando式(10)：z^2 + a z - a V'(b)(e^{iα} - 1) = 0，α = 2πk/N，回傳實部最大的根的實部。"""
    alpha = 2 * math.pi * k / N
    c = -a * dV(b) * (cmath.exp(1j * alpha) - 1)
    d = cmath.sqrt(a * a - 4 * c)
    return max(((-a + d) / 2).real, ((-a - d) / 2).real)


def critical_a(b, N):
    """有限N台車的分界（ours-finite-n-threshold）：a = V'(b)(1 + cos(2π/N))。"""
    return dV(b) * (1 + math.cos(2 * math.pi / N))


class Ring:
    def __init__(self, N, L, a, x=None, v=None):
        self.N, self.L, self.a = N, L, a
        b = L / N
        self.x = list(x) if x is not None else [n * b for n in range(N)]
        self.v = list(v) if v is not None else [V(b)] * N
        self.t = 0.0
        self._steps = 0
        self.brake = None          # (車, 開始時間t0, 持續時間τ, 減速β)；t0/dt、τ/dt都要是整數
        self.smooth = None         # (車, 規則函式)：規則函式(ring, n, x, v, h) -> 加速度
        self.min_h = min(self.headways(self.x))
        self.min_v = min(self.v)
        self.max_sum_err = 0.0

    def headways(self, x):
        N, L = self.N, self.L
        return [x[n + 1] - x[n] for n in range(N - 1)] + [x[0] + L - x[N - 1]]

    def brake_window(self):
        """煞車換算成(車, 開始步, 結束步（不含）, β)；沒有煞車回傳None。"""
        if self.brake is None:
            return None
        n, t0, tau, beta = self.brake
        k0, m = t0 / DT, tau / DT
        if abs(k0 - round(k0)) > 1e-9 or abs(m - round(m)) > 1e-9:
            raise ValueError(f"煞車的開始時間{t0}和持續時間{tau}都要是dt={DT}的整數倍")
        return n, int(round(k0)), int(round(k0)) + int(round(m)), beta

    def accel(self, x, v, braking):
        h = self.headways(x)
        a = self.a
        acc = [a * (V(h[n]) - v[n]) for n in range(self.N)]
        if self.smooth is not None:
            n, rule = self.smooth
            acc[n] = rule(self, n, x, v, h)
        if braking is not None:
            n, beta = braking
            acc[n] -= beta
        return acc

    def step(self, dt=DT):
        x, v = self.x, self.v
        w = self.brake_window()
        braking = (w[0], w[3]) if w is not None and w[1] <= self._steps < w[2] else None
        k1x, k1v = v, self.accel(x, v, braking)
        x2 = [xi + 0.5 * dt * k for xi, k in zip(x, k1x)]
        v2 = [vi + 0.5 * dt * k for vi, k in zip(v, k1v)]
        k2x, k2v = v2, self.accel(x2, v2, braking)
        x3 = [xi + 0.5 * dt * k for xi, k in zip(x, k2x)]
        v3 = [vi + 0.5 * dt * k for vi, k in zip(v, k2v)]
        k3x, k3v = v3, self.accel(x3, v3, braking)
        x4 = [xi + dt * k for xi, k in zip(x, k3x)]
        v4 = [vi + dt * k for vi, k in zip(v, k3v)]
        k4x, k4v = v4, self.accel(x4, v4, braking)
        self.x = [xi + dt / 6 * (p + 2 * q + 2 * r + s) for xi, p, q, r, s in zip(x, k1x, k2x, k3x, k4x)]
        self.v = [vi + dt / 6 * (p + 2 * q + 2 * r + s) for vi, p, q, r, s in zip(v, k1v, k2v, k3v, k4v)]
        # 步數乘dt算時間，避免一直加0.05累積誤差
        self._steps += 1
        self.t = self._steps * dt
        h = self.headways(self.x)
        self.min_h = min(self.min_h, min(h))
        self.min_v = min(self.min_v, min(self.v))
        self.max_sum_err = max(self.max_sum_err, abs(sum(h) - self.L))

    def sane(self):
        """共同的物理檢查S1～S3。"""
        return self.min_h > 0 and self.min_v >= -1e-9 and self.max_sum_err <= 1e-9

    def k1_amplitude(self):
        N, b = self.N, self.L / self.N
        h = self.headways(self.x)
        s = sum((h[n] - b) * cmath.exp(-2j * math.pi * n / N) for n in range(N))
        return abs(s) / N

    def max_dev(self):
        vb = V(self.L / self.N)
        return max(abs(vi - vb) for vi in self.v)


def mode_ring(N, L, a, eps=1e-6):
    """位置加上 eps·cos(2πn/N) 的k=1小擾動，速度不動。"""
    b = L / N
    x = [n * b + eps * math.cos(2 * math.pi * n / N) for n in range(N)]
    return Ring(N, L, a, x=x)


def fit_slope(pts):
    n = len(pts)
    mt = sum(p[0] for p in pts) / n
    my = sum(p[1] for p in pts) / n
    num = sum((p[0] - mt) * (p[1] - my) for p in pts)
    den = sum((p[0] - mt) ** 2 for p in pts)
    return num / den


def measure_sigma(N, L, a, t_start=100.0, t_max=2100.0, cap=1e-3, every=1.0):
    """M1、M2、M3的量法：對ln(k=1的波)在[t_start, T_end]做線性回歸。
    T_end = t_max，或k=1的波第一次超過cap的時間，取比較早的。回傳(σ_meas, T_end, ring)。"""
    r = mode_ring(N, L, a)
    rec = int(round(every / DT))
    pts, s = [], 0
    while r.t < t_max - 1e-9:
        r.step()
        s += 1
        if s % rec == 0:
            amp = r.k1_amplitude()
            if amp > cap:
                break
            if r.t >= t_start - 1e-9:
                pts.append((r.t, math.log(amp)))
    return fit_slope(pts), r.t, r

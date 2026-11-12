/* 瀏覽器版求解器：model/ovm.py第3版（和run_v2.py、explore_smoothing.py用到的部分）逐行對應的JavaScript版本。
 * 同一個檔案在Node（對答案測試）和瀏覽器（簡報）都能用。對答案的標準在web/PARITY.md，寫這個檔案之前就commit了。
 * 不能為了效能改DT、減少RK4的評估次數或換積分法（PARITY.md的J12）。
 *
 * Python的%是取「跟除數同號」的餘數，JavaScript的%不是；這裡一律用pmod()。
 */
(function (root) {
  "use strict";
  const TANH2 = Math.tanh(2.0);
  const DT = 0.05;
  const JAM_V = 0.1;

  const V = h => Math.tanh(h - 2.0) + TANH2;
  const dV = h => 1.0 / Math.cosh(h - 2.0) ** 2;
  const pmod = (a, m) => { const r = a % m; return r < 0 ? r + m : r === 0 ? 0 : r; };  // 跟Python的%一樣：結果跟除數同號，−0當0

  // ---------- 複數（只用在理論成長率和波的振幅） ----------
  const cmul = (a, b) => [a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]];
  function csqrt(z) {  // 主值，跟cmath.sqrt一樣
    const [x, y] = z, r = Math.hypot(x, y);
    if (r === 0) return [0, y];
    let re = Math.sqrt((r + Math.abs(x)) / 2), im = y / (2 * re);
    if (x < 0) { const t = re; re = Math.abs(im); im = y < 0 || Object.is(y, -0) ? -t : t; }
    return [re, im];
  }

  /** Bando式(10)：z² + az − aV'(b)(e^{iα} − 1) = 0，α = 2πk/N，回傳實部最大的根的實部。 */
  function theorySigma(a, b, N, k = 1) {
    const alpha = 2 * Math.PI * k / N;
    const e = [Math.cos(alpha) - 1, Math.sin(alpha)];
    const f = -a * dV(b);
    const c = [f * e[0], f * e[1]];
    const d = csqrt([a * a - 4 * c[0], -4 * c[1]]);
    return Math.max((-a + d[0]) / 2, (-a - d[0]) / 2);
  }
  const criticalA = (b, N) => dV(b) * (1 + Math.cos(2 * Math.PI / N));

  class Ring {
    constructor(N, L, a, x = null, v = null) {
      this.N = N; this.L = L; this.a = a;
      const b = L / N;
      this.x = x ? Float64Array.from(x) : Float64Array.from({ length: N }, (_, n) => n * b);
      this.v = v ? Float64Array.from(v) : new Float64Array(N).fill(V(b));
      this.t = 0.0;
      this._steps = 0;
      this.brake = null;   // [車, t0, τ, β]
      this.smooth = null;  // [車, 規則]，規則.accel(ring, n, x, v, h)
      this._h = new Float64Array(N);
      this.minH = Math.min(...this.headways(this.x));
      this.minV = Math.min(...this.v);
      this.maxSumErr = 0.0;
    }
    headways(x, out) {
      const N = this.N, L = this.L, h = out || new Float64Array(N);
      for (let n = 0; n < N - 1; n++) h[n] = x[n + 1] - x[n];
      h[N - 1] = x[0] + L - x[N - 1];
      return h;
    }
    brakeWindow() {
      if (!this.brake) return null;
      const [n, t0, tau, beta] = this.brake, k0 = t0 / DT, m = tau / DT;
      if (Math.abs(k0 - Math.round(k0)) > 1e-9 || Math.abs(m - Math.round(m)) > 1e-9)
        throw new Error(`煞車的開始時間${t0}和持續時間${tau}都要是dt=${DT}的整數倍`);
      return [n, Math.round(k0), Math.round(k0) + Math.round(m), beta];
    }
    accel(x, v, braking, out) {
      const N = this.N, a = this.a, h = this.headways(x, this._h), acc = out;
      for (let n = 0; n < N; n++) acc[n] = a * (V(h[n]) - v[n]);
      if (this.smooth) { const [n, rule] = this.smooth; acc[n] = rule.accel(this, n, x, v, h); }
      if (braking) acc[braking[0]] -= braking[1];
      return acc;
    }
    step() {
      const dt = DT, N = this.N, x = this.x, v = this.v;
      const w = this.brakeWindow();
      const braking = w && w[1] <= this._steps && this._steps < w[2] ? [w[0], w[3]] : null;
      const k1v = this.accel(x, v, braking, new Float64Array(N)), k1x = v;
      const x2 = new Float64Array(N), v2 = new Float64Array(N);
      for (let n = 0; n < N; n++) { x2[n] = x[n] + 0.5 * dt * k1x[n]; v2[n] = v[n] + 0.5 * dt * k1v[n]; }
      const k2x = v2, k2v = this.accel(x2, v2, braking, new Float64Array(N));
      const x3 = new Float64Array(N), v3 = new Float64Array(N);
      for (let n = 0; n < N; n++) { x3[n] = x[n] + 0.5 * dt * k2x[n]; v3[n] = v[n] + 0.5 * dt * k2v[n]; }
      const k3x = v3, k3v = this.accel(x3, v3, braking, new Float64Array(N));
      const x4 = new Float64Array(N), v4 = new Float64Array(N);
      for (let n = 0; n < N; n++) { x4[n] = x[n] + dt * k3x[n]; v4[n] = v[n] + dt * k3v[n]; }
      const k4x = v4, k4v = this.accel(x4, v4, braking, new Float64Array(N));
      const nx = new Float64Array(N), nv = new Float64Array(N);
      for (let n = 0; n < N; n++) {
        nx[n] = x[n] + dt / 6 * (k1x[n] + 2 * k2x[n] + 2 * k3x[n] + k4x[n]);
        nv[n] = v[n] + dt / 6 * (k1v[n] + 2 * k2v[n] + 2 * k3v[n] + k4v[n]);
      }
      this.x = nx; this.v = nv;
      this._steps += 1;
      this.t = this._steps * dt;  // 步數乘dt算時間
      const h = this.headways(nx, this._h);
      let mh = Infinity, sum = 0, mv = Infinity;
      for (let n = 0; n < N; n++) { if (h[n] < mh) mh = h[n]; sum += h[n]; if (nv[n] < mv) mv = nv[n]; }
      if (mh < this.minH) this.minH = mh;
      if (mv < this.minV) this.minV = mv;
      const e = Math.abs(sum - this.L); if (e > this.maxSumErr) this.maxSumErr = e;
    }
    sane() { return this.minH > 0 && this.minV >= -1e-9 && this.maxSumErr <= 1e-9; }
    maxDev() { const vb = V(this.L / this.N); let m = 0; for (const q of this.v) { const d = Math.abs(q - vb); if (d > m) m = d; } return m; }
    minSpeed() { let m = Infinity; for (const q of this.v) if (q < m) m = q; return m; }
  }

  const analytic = (N, L, t) => { const b = L / N, vb = V(b); return [Array.from({ length: N }, (_, n) => n * b + vb * t), new Array(N).fill(vb)]; };

  /** 第2頁的做法：點擊之前用解析解；點擊那一刻從當下的解析解開始RK4，同時開始煞車（內部時間從0開始）。 */
  class ClickDemo {
    constructor(N, L, a) { this.N = N; this.L = L; this.a = a; this.ring = null; this.tClick = null; }
    state(t) { return this.ring ? [this.ring.x, this.ring.v] : analytic(this.N, this.L, t); }
    click(t0, car, tau, beta) {
      const [x, v] = analytic(this.N, this.L, t0);
      this.ring = new Ring(this.N, this.L, this.a, x, v);
      this.ring.brake = [car, 0.0, tau, beta];
      this.tClick = t0;
    }
    time() { return this.tClick + this.ring.t; }
  }

  function modeRing(N, L, a, eps = 1e-6) {
    const b = L / N;
    return new Ring(N, L, a, Array.from({ length: N }, (_, n) => n * b + eps * Math.cos(2 * Math.PI * n / N)));
  }

  function fitSlope(pts) {
    const n = pts.length;
    let mt = 0, my = 0; for (const p of pts) mt += p[0]; mt /= n; for (const p of pts) my += p[1]; my /= n;
    let num = 0, den = 0; for (const p of pts) num += (p[0] - mt) * (p[1] - my); for (const p of pts) den += (p[0] - mt) ** 2;
    return num / den;
  }

  const tol = sig => 2e-5 + 0.02 * Math.abs(sig);

  /** run_v2.measure_v2：k=1的小擾動，每1.0量各波的振幅；停止條件和有效長度照model/CRITERIA.md第2版。onSample(t, a1)給畫面用。 */
  function measureV2(N, L, a, eps = 1e-6, onSample = null) {
    const r = modeRing(N, L, a, eps), b = L / N, K = Math.floor(N / 2);
    const table = [];
    for (let k = 1; k <= K; k++) { const row = []; for (let n = 0; n < N; n++) { const th = (-2 * Math.PI * k * n) / N; row.push([Math.cos(th), Math.sin(th)]); } table.push(row); }
    const pts = []; let reason = "t = 2100", s = 0; const rec = Math.round(1.0 / DT);
    const h = new Float64Array(N);
    while (r.t < 2100 - 1e-9) {
      r.step(); s += 1;
      if (s % rec) continue;
      r.headways(r.x, h);
      const amps = table.map(row => { let re = 0, im = 0; for (let n = 0; n < N; n++) { const d = h[n] - b; re += d * row[n][0]; im += d * row[n][1]; } return Math.hypot(re, im) / N; });
      const a1 = amps[0];
      if (onSample) onSample(r.t, a1);
      if (a1 > 1e-3) { reason = "k=1 > 1e−3"; break; }
      if (a1 < 1e-10) { reason = "k=1 < 1e−10"; break; }
      if (amps.length > 1) {
        let km = 2, mx = amps[1]; for (let i = 2; i < amps.length; i++) if (amps[i] > mx) { mx = amps[i]; km = i + 1; }
        if (mx > 0.1 * a1) { reason = `k=${km} > 0.1×k=1`; break; }
      }
      if (r.t >= 100 - 1e-9) pts.push([r.t, Math.log(a1)]);
    }
    const length = pts.length >= 2 ? pts[pts.length - 1][0] - pts[0][0] : 0.0;
    const sigma = pts.length >= 2 ? fitSlope(pts) : NaN;
    return { sigma, stop: r.t, length, reason, sane: r.sane() };
  }

  /** M2v2的判定，資料不足的再用1e−7、1e−8（model/run_v3_m2.py的規則）。 */
  function verdictN(N, L = 44.0, a = 1.0, onRun = null) {
    const st = theorySigma(a, L / N, N);
    const first = measureV2(N, L, a, 1e-6); const runs = [Object.assign({ eps: 1e-6 }, first)];
    if (onRun) onRun(runs[0]);
    let verdict;
    if (first.length < 200) {
      const vs = [];
      for (const eps of [1e-7, 1e-8]) {
        const m = measureV2(N, L, a, eps); runs.push(Object.assign({ eps }, m)); if (onRun) onRun(runs[runs.length - 1]);
        const enough = m.length >= 200, match = (m.sigma > 0) === (st > 0) && Math.abs(m.sigma - st) <= tol(st) && m.sane;
        vs.push([enough, match]);
      }
      const suff = vs.filter(q => q[0]).map(q => q[1]);
      verdict = suff.length === 0 ? "數值無法判定" : suff.every(Boolean) ? "相符" : "不符";
    } else if (Math.abs(st) < 1e-8) {
      verdict = Math.abs(first.sigma - st) <= tol(st) && first.sane ? "相符（只比差距）" : "不符";
    } else {
      verdict = (first.sigma > 0) === (st > 0) && Math.abs(first.sigma - st) <= tol(st) && first.sane ? "相符" : "不符";
    }
    return { N, theory: st, runs, verdict };
  }

  // ---------- 塞車團的追蹤（run_v2.clusters、track_wave；M6v2） ----------
  function clusters(v) {
    const N = v.length, slow = Array.from(v, q => q < JAM_V);
    if (slow.every(Boolean)) return [Array.from({ length: N }, (_, n) => n)];
    const start = slow.findIndex(s => !s);
    const groups = []; let cur = [];
    for (let i = 1; i <= N; i++) { const n = (start + i) % N; if (slow[n]) cur.push(n); else if (cur.length) { groups.push(cur); cur = []; } }
    if (cur.length) groups.push(cur);
    return groups;
  }
  const cmpList = (a, b) => { for (let i = 0; i < Math.min(a.length, b.length); i++) if (a[i] !== b[i]) return a[i] - b[i]; return a.length - b.length; };
  function trackWave(ss, N, L) {
    const center = (g, x, ref) => { let s = 0; for (const n of g) s += pmod(pmod(x[n], L) - ref + L / 2, L) - L / 2; return ref + s / g.length; };
    const track = []; let lastGroup = null, lastPos = null, lastT = null, unwrapped = null;
    for (const [t, x, v] of ss) {
      const gs = clusters(v);
      if (lastGroup === null) {
        const big = gs.filter(g => g.length >= 3); if (!big.length) continue;
        let g = big[0]; for (const q of big) if (q.length > g.length) g = q;
        const pos = center(g, x, pmod(x[g[0]], L)); unwrapped = pos;
        lastGroup = new Set(g); lastPos = pmod(pos, L); lastT = t; track.push([t, unwrapped]); continue;
      }
      let g = null, best = 0;
      for (const q of gs) { let c = 0; for (const n of q) if (lastGroup.has(n)) c++; if (c > 0 && c > best) { best = c; g = q; } }
      if (!g) {
        const near = [];
        if (t - lastT <= 5 + 1e-9) for (const q of gs) { const c = center(q, x, lastPos); if (Math.abs(c - lastPos) <= 2.0) near.push([Math.abs(c - lastPos), q]); }
        if (near.length) { near.sort((p, q) => p[0] - q[0] || cmpList(p[1], q[1])); g = near[0][1]; }
        else if (t - lastT > 5 + 1e-9) break;
        else continue;
      }
      const pos = center(g, x, lastPos);
      unwrapped += pos - lastPos;
      lastGroup = new Set(g); lastPos = pmod(pos, L); lastT = t; track.push([t, unwrapped]);
    }
    return track;
  }

  // ---------- 平滑車（explore_smoothing.py；都是我們設計的規則，不是Stern 2018的控制器） ----------
  class AvgRule {  // R1
    constructor(aS = 1.0, window = 50.0) { this.aS = aS; this.max = Math.round(window / DT); this.buf = []; }
    observe(ring, n) { this.buf.push(ring.v[n]); if (this.buf.length > this.max) this.buf.shift(); }
    accel(ring, n, x, v, h) { let u = v[n]; if (this.buf.length) { let s = 0; for (const q of this.buf) s += q; u = s / this.buf.length; } return this.aS * (Math.min(u, V(h[n])) - v[n]); }
  }
  class ClampRule {  // R2
    constructor(c = 0.05) { this.c = c; }
    observe() {}
    accel(ring, n, x, v, h) { const acc = ring.a * (V(h[n]) - v[n]); return Math.max(-this.c, Math.min(this.c, acc)); }
  }
  class TargetRule {  // R3
    constructor(U, aS = 1.0) { this.U = U; this.aS = aS; }
    observe() {}
    accel(ring, n, x, v, h) { return this.aS * (Math.min(this.U, V(h[n])) - v[n]); }
  }

  /** explore_smoothing.run：ε偏移開始，t=300換第0台，跑到1500，比較區間[1000, 1500]每0.5取樣。onStep(ring)給畫面用。 */
  function smoothingRun(rule, eps = 0.1, opts = {}) {
    const N = 22, L = 44.0, A = 1.0, T_SWITCH = 300.0, T_END = opts.tEnd || 1500.0, W0 = 1000.0, W1 = 1500.0;
    const x = Array.from({ length: N }, (_, n) => n * 2.0); x[0] += eps;
    const r = new Ring(N, L, A, x);
    const speeds = []; let jam = 0, samples = 0, s = 0; const rec = Math.round(0.5 / DT);
    while (r.t < T_END - 1e-9) {
      if (rule && r.t >= T_SWITCH - 1e-9 && !r.smooth) r.smooth = [0, rule];
      r.step(); s += 1;
      if (r.smooth) rule.observe(r, 0); else if (rule instanceof AvgRule) rule.observe(r, 0);
      if (s % rec === 0 && W0 - 1e-9 <= r.t && r.t <= W1 + 1e-9) { for (const q of r.v) speeds.push(q); samples += 1; if (r.minSpeed() < 0.1) jam += 1; }
      if (opts.onStep && opts.onStep(r) === false) break;
    }
    if (!speeds.length) return { ring: r };
    let m = 0; for (const q of speeds) m += q; m /= speeds.length;
    let ss = 0; for (const q of speeds) ss += (q - m) ** 2;
    let vmin = Infinity; for (const q of speeds) if (q < vmin) vmin = q;
    return { std: Math.sqrt(ss / speeds.length), vmin, jamFrac: jam / samples, mean: m, sane: r.sane(), minH: r.minH, ring: r };
  }

  const api = { DT, JAM_V, TANH2, V, dV, pmod, theorySigma, criticalA, Ring, analytic, ClickDemo, modeRing, fitSlope, tol,
    measureV2, verdictN, clusters, trackWave, AvgRule, ClampRule, TargetRule, smoothingRun };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.OVM = api;
})(typeof self !== "undefined" ? self : this);

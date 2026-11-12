// 節點7：瀏覽器求解器web/ovm.js跟Python參考模型對答案。項目和容許誤差照web/PARITY.md（J1～J10、J12），寫求解器之前就commit了。
// 參考答案：web/reference/parity-ref.json（python3 model/export_reference.py產生）
// 用法：node tests/test_js_parity.js        結束代碼：0全部通過；1有項目沒通過
"use strict";
const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..");
const O = require(path.join(ROOT, "web", "ovm.js"));
const REF = JSON.parse(fs.readFileSync(path.join(ROOT, "web", "reference", "parity-ref.json"), "utf8"));
const N = 22, L = 44.0, BETA = 0.25, TAU = 0.5;

let fails = 0;
const report = (id, ok, msg) => { if (!ok) fails += 1; console.log(`[${ok ? "通過" : "沒通過"}] ${id}：${msg}`); };
const maxAbs = (a, b) => { let m = 0; for (let i = 0; i < a.length; i++) { const d = Math.abs(a[i] - b[i]); if (!(d <= m)) m = d; } return m; };
const relDiff = (a, b) => Math.abs(a - b) / Math.max(Math.abs(b), 1e-300);
const sci = x => x.toExponential(2);

function sampleEvery(r, sEnd, every, rec) {
  const out = [rec(r)], k = Math.round(every / O.DT); let s = 0;
  while (r.t < sEnd - 1e-9) { r.step(); s += 1; if (s % k === 0) out.push(rec(r)); }
  return out;
}
function firstJamStep(r, maxSteps) { for (let i = 0; i < maxSteps; i++) { r.step(); if (r.minSpeed() < 0.1) return r._steps; } return null; }

// J1
for (const row of REF.J1) {
  const r = new O.Ring(N, L, 1.0); r.brake = [0, row.t0, row.tau, BETA];
  let got; try { const w = r.brakeWindow(); got = { k0: w[1], k1: w[2] }; } catch (e) { got = { error: true }; }
  const ok = row.error ? !!got.error : (got.k0 === row.k0 && got.k1 === row.k1);
  report(`J1 煞車步數 (t0=${row.t0}, τ=${row.tau})`, ok, row.error ? `Python報錯；JS ${got.error ? "也報錯" : "沒報錯"}` : `Python ${row.k0}～${row.k1}；JS ${got.k0}～${got.k1}`);
}

// J2、J3、J10
for (const row of REF.J2) {
  const d = new O.ClickDemo(N, L, 1.0); d.click(row.tc, row.car, TAU, BETA);
  const traj = sampleEvery(d.ring, 400.0, 0.5, r => [Array.from(r.x), Array.from(r.v)]);
  let mx = 0, mv = 0;
  for (let i = 0; i < row.traj.length; i++) { mx = Math.max(mx, maxAbs(traj[i][0], row.traj[i][0])); mv = Math.max(mv, maxAbs(traj[i][1], row.traj[i][1])); }
  report(`J2 第2頁點擊 (t_c=${row.tc}, 第${row.car}台)`, traj.length === row.traj.length && mx <= 1e-6 && mv <= 1e-6, `取樣 ${traj.length}/${row.traj.length} 個；位置最大差 ${sci(mx)}，車速最大差 ${sci(mv)}（容許1e−6）`);
  const d2 = new O.ClickDemo(N, L, 1.0); d2.click(row.tc, row.car, TAU, BETA);
  const js = firstJamStep(d2.ring, 10000);
  report(`J3 塞車形成 (t_c=${row.tc}, 第${row.car}台)`, js === row.jamStep, `Python第${row.jamStep}步（${(row.jamStep * O.DT).toFixed(2)}）；JS第${js}步`);
  report(`J10 物理檢查 J2 (t_c=${row.tc})`, d.ring.sane() === row.sane, `Python ${row.sane}；JS ${d.ring.sane()}`);
}

// J4
for (const row of REF.J4) {
  const x = Array.from({ length: N }, (_, n) => n * 2.0); x[0] += row.eps;
  const r = new O.Ring(N, L, 1.0, x); let jam = null, state = null;
  while (r.t < 1000 - 1e-9) { r.step(); if (jam === null && r.minSpeed() < 0.1) jam = r._steps; if (r._steps === 3000) state = [Array.from(r.x), Array.from(r.v)]; if (jam !== null && r._steps >= 3000) break; }
  const ds = Math.max(maxAbs(state[0], row.state150[0]), maxAbs(state[1], row.state150[1]));
  report(`J4 第1頁 ε=${row.eps}`, jam === row.jamStep && ds <= 1e-6, `塞車：Python第${row.jamStep}步（${(row.jamStep * O.DT).toFixed(2)}），JS第${jam}步；t=150狀態最大差 ${sci(ds)}`);
  report(`J10 物理檢查 J4 ε=${row.eps}`, r.sane() === row.sane, `Python ${row.sane}；JS ${r.sane()}`);
}

// J5
for (const row of REF.J5) {
  const d = new O.ClickDemo(N, L, row.a); d.click(20.0, 0, TAU, BETA);
  const sp = sampleEvery(d.ring, 100.0, 0.5, r => row.followers.map(n => r.v[n]));
  let m = 0; for (let i = 0; i < sp.length; i++) m = Math.max(m, maxAbs(sp[i], row.speeds[i]));
  const d2 = new O.ClickDemo(N, L, row.a); d2.click(20.0, 0, TAU, BETA); const A = {};
  while (d2.ring.t < 200 - 1e-9) { d2.ring.step(); if (d2.ring._steps === 100 || d2.ring._steps === 4000) A[d2.ring._steps] = d2.ring.maxDev(); }
  const r5 = relDiff(A[100], row.A5), r200 = relDiff(A[4000], row.A200);
  report(`J5 第4頁 a=${row.a}`, sp.length === row.speeds.length && m <= 1e-6 && r5 <= 1e-4 && r200 <= 1e-4,
    `四條線車速最大差 ${sci(m)}；擾動 點擊後5 Python ${sci(row.A5)} JS ${sci(A[100])}（相對差 ${sci(r5)}），點擊後200 Python ${sci(row.A200)} JS ${sci(A[4000])}（相對差 ${sci(r200)}）；比值 ${(A[4000] / A[100]).toFixed(2)}`);
  report(`J10 物理檢查 J5 a=${row.a}`, d2.ring.sane() === row.sane, `Python ${row.sane}；JS ${d2.ring.sane()}`);
}

// J6
for (const row of REF.J6) {
  const d = new O.ClickDemo(N, L, row.a); d.click(20.0, 0, TAU, BETA);
  if (row.a === 1.0) {
    const js = firstJamStep(d.ring, 40000);
    report(`J6 第5頁 a=1.0`, js === row.jamStep, `塞車：Python第${row.jamStep}步，JS第${js}步`);
  } else {
    const end = row.A1500 !== undefined ? 1500 : 300; let a300 = null;
    while (d.ring.t < end - 1e-9) { d.ring.step(); if (d.ring._steps === 6000) a300 = d.ring.maxDev(); }
    const parts = [`點擊後300 Python ${sci(row.A300)} JS ${sci(a300)}（相對差 ${sci(relDiff(a300, row.A300))}）`];
    let ok = relDiff(a300, row.A300) <= 1e-4;
    if (end === 1500) { const a15 = d.ring.maxDev(); ok = ok && relDiff(a15, row.A1500) <= 1e-4; parts.push(`點擊後1500 Python ${sci(row.A1500)} JS ${sci(a15)}（相對差 ${sci(relDiff(a15, row.A1500))}）`); }
    report(`J6 第5頁 a=${row.a}`, ok, parts.join("；"));
  }
  report(`J10 物理檢查 J6 a=${row.a}`, d.ring.sane() === row.sane, `Python ${row.sane}；JS ${d.ring.sane()}`);
}

// J8
{
  const t0 = 20.0, r = new O.Ring(N, L, 1.0); r.brake = [0, t0, TAU, BETA];
  while (r.t < t0 - 1e-9) r.step();
  const ss = [[r.t, Array.from(r.x), Array.from(r.v)]]; let s = 0; const k = Math.round(0.5 / O.DT);
  while (r.t < t0 + 600 - 1e-9) { r.step(); s += 1; if (s % k === 0) ss.push([r.t, Array.from(r.x), Array.from(r.v)]); }
  const tr = O.trackWave(ss, N, L), c = O.fitSlope(tr);
  let mean = 0; for (const [, , v] of ss) { let q = 0; for (const z of v) q += z; mean += q / N; } mean /= ss.length;
  const R = REF.J8;
  const ok = tr[0][0] === R.trackStart && tr[tr.length - 1][0] === R.trackEnd && tr.length === R.trackLen && Math.abs(c - R.c) <= 1e-6 && Math.abs(mean - R.meanV) <= 1e-6;
  report("J8 第3頁波速（M6v2）", ok, `追蹤 Python ${R.trackStart}～${R.trackEnd}（${R.trackLen}點），JS ${tr[0][0]}～${tr[tr.length - 1][0]}（${tr.length}點）；波速 Python ${R.c.toFixed(6)} JS ${c.toFixed(6)}（差 ${sci(Math.abs(c - R.c))}）；平均車速 Python ${R.meanV.toFixed(6)} JS ${mean.toFixed(6)}`);
  report("J10 物理檢查 J8", r.sane() === R.sane, `Python ${R.sane}；JS ${r.sane()}`);
}

// J9
{
  const V2 = O.V(2.0);
  const mk = { R0: () => null, R1: () => new O.AvgRule(), R2: () => new O.ClampRule(), R3: () => new O.TargetRule(V2) };
  // Python的鍵是"U1.0"這種寫法，直接從鍵取倍數（第1次執行時這裡寫成`U${m}`，1.0變成"U1"對不到，測試程式自己當掉）
  for (const key of Object.keys(REF.J9)) if (key.startsWith("U")) { const m = parseFloat(key.slice(1)); mk[key] = () => new O.TargetRule(V2 * m); }
  for (const key of Object.keys(REF.J9)) {
    const P = REF.J9[key], J = O.smoothingRun(mk[key](), 0.1);
    const d = Math.max(Math.abs(J.std - P.std), Math.abs(J.vmin - P.vmin), Math.abs(J.mean - P.mean), Math.abs(J.minH - P.min_h));
    report(`J9 第8頁 ${key}`, d <= 1e-6 && J.jamFrac === P.jam_frac && J.sane === P.sane,
      `標準差 Python ${P.std.toFixed(6)} JS ${J.std.toFixed(6)}；平均 ${P.mean.toFixed(6)}／${J.mean.toFixed(6)}；最低 ${P.vmin.toFixed(6)}／${J.vmin.toFixed(6)}；最小車距 ${P.min_h.toFixed(6)}／${J.minH.toFixed(6)}；最大差 ${sci(d)}；塞車比例 ${P.jam_frac}／${J.jamFrac}；物理檢查 ${P.sane}／${J.sane}`);
  }
}

// J7（最慢，放最後）
{
  let bad = 0;
  for (const row of REF.J7) {
    const J = O.verdictN(row.N, L, 1.0);
    const problems = [];
    if (Math.abs(J.theory - row.theory) > 1e-12) problems.push(`理論σ差 ${sci(Math.abs(J.theory - row.theory))}`);
    if (J.runs.length !== row.runs.length) problems.push(`跑的次數 Python ${row.runs.length} JS ${J.runs.length}`);
    for (let i = 0; i < Math.min(J.runs.length, row.runs.length); i++) {
      const p = row.runs[i], j = J.runs[i];
      const sd = Math.abs(j.sigma - p.sigma), noise = p.reason.startsWith("k=") && p.reason.includes("0.1×");
      if (!(sd <= 1e-9 + 1e-6 * Math.abs(p.sigma)) && !(Number.isNaN(p.sigma) && Number.isNaN(j.sigma))) problems.push(`ε=${p.eps} σ差 ${sci(sd)}`);
      if (j.reason !== p.reason) problems.push(`ε=${p.eps} 停止原因 Python「${p.reason}」JS「${j.reason}」`);
      const ld = Math.abs(j.length - p.length);
      if (noise ? ld > 2 : ld !== 0) problems.push(`ε=${p.eps} 有效長度 Python ${p.length} JS ${j.length}`);
    }
    if (J.verdict !== row.verdict) problems.push(`判定 Python「${row.verdict}」JS「${J.verdict}」`);
    const ok = problems.length === 0; if (!ok) bad += 1;
    report(`J7 第6頁 N=${row.N}`, ok, ok ? `${J.verdict}；σ_meas ${J.runs[0].sigma.toExponential(4)}，有效長度 ${J.runs[0].length.toFixed(0)}（${J.runs[0].reason}）` : problems.join("；"));
  }
  console.log(`J7 合計：58個N，不一致 ${bad} 個`);
}

// J12
{
  const src = fs.readdirSync(path.join(ROOT, "web")).filter(f => f.endsWith(".js") && f !== "ovm.js").map(f => [f, fs.readFileSync(path.join(ROOT, "web", f), "utf8")]);
  const calls = src.flatMap(([f, t]) => (t.match(/\.step\(\s*[^)\s]/g) || []).map(m => `${f}: ${m}`));
  report("J12 不能偷改精度", O.DT === 0.05 && calls.length === 0, `DT = ${O.DT}；web/裡帶參數的step(呼叫：${calls.length ? calls.join("、") : "沒有"}`);
}

console.log(`\n沒通過 ${fails} 項。`);
process.exit(fails ? 1 : 0);

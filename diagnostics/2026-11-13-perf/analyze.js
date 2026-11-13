/* 分析診斷結果（不重新量測）。用法：node analyze.js <診斷輸出資料夾>
 * 1. A1、A2的分布。2. A3 trace：只算沒有上層的頂層工作當總時間，self time分成幾類。
 * 3. Lighthouse trace：每次最長的頂層工作，裡面的self time前幾名，比較B0和其他次。 */
const fs = require("fs"), path = require("path"), zlib = require("zlib");
const D = process.argv[2];
const C = require("./common");
const CAT = name => /^(FunctionCall|EvaluateScript|v8\.|V8\.|TimerFire|FireAnimationFrame|MinorGC|MajorGC|BlinkGC|v8)/.test(name) ? "JavaScript（含GC、編譯）"
  : /Canvas|canvas/.test(name) ? "畫布（canvas）"
  : /Layout|layout|RecalcStyle|UpdateLayoutTree|Shape|PrePaint|UpdateLifecycle|StyleRecalc|HitTest/.test(name) ? "Rendering（樣式、版面配置、文字排版）"
  : /Paint|paint|LayerTreeHost|Commit|Composite|Raster|raster|UpdateLayer|Layer/.test(name) ? "Painting／合成（含圖層更新）"
  : /ParseHTML|ParseAuthorStyleSheet|ResourceSendRequest|ResourceReceive|ResourceFinish/.test(name) ? "載入、解析"
  : "其他";
function mainThread(ev, url) {
  const names = new Map(); ev.filter(e => e.ph === "M" && e.name === "thread_name").forEach(e => names.set(`${e.pid}:${e.tid}`, e.args.name));
  const keys = [...names.entries()].filter(([, v]) => v === "CrRendererMain").map(([k]) => k);
  const cnt = new Map(); ev.forEach(e => { const k = `${e.pid}:${e.tid}`; if (keys.includes(k) && e.ph === "X") cnt.set(k, (cnt.get(k) || 0) + 1); });
  const key = [...cnt.entries()].sort((a, b) => b[1] - a[1])[0][0];
  return ev.filter(e => `${e.pid}:${e.tid}` === key && e.ph === "X" && e.dur != null).sort((a, b) => a.ts - b.ts || b.dur - a.dur);
}
function tree(xs) {   // 建父子關係，算self time
  const stack = [], tops = [];
  for (const e of xs) {
    while (stack.length && stack[stack.length - 1].ts + stack[stack.length - 1].dur <= e.ts) stack.pop();
    const p = stack[stack.length - 1];
    e._kids = []; e._child = 0;
    if (p) { p._child += e.dur; p._kids.push(e); } else tops.push(e);
    stack.push(e);
  }
  return tops;
}
function selfIn(root) { const m = new Map(); (function walk(e) { m.set(e.name, (m.get(e.name) || 0) + Math.max(0, e.dur - e._child)); e._kids.forEach(walk); })(root); return m; }
const load = f => JSON.parse(zlib.gunzipSync(fs.readFileSync(path.join(D, f))).toString());
const ms = us => +(us / 1000).toFixed(1);
const out = {};

// 1. 分布
const A1 = JSON.parse(fs.readFileSync(path.join(D, "A1.json"))), A2 = JSON.parse(fs.readFileSync(path.join(D, "A2.json")));
out.cpu = {};
for (const n of [1, 2, 5]) {
  const g = (rows, kind) => rows.filter(r => r.page === n && r.kind === kind);
  out.cpu[`p${n}`] = { A1冷: C.stats(g(A1.rows, "冷").map(r => r.busy)), A1熱: C.stats(g(A1.rows, "熱").map(r => r.busy)), A2冷: C.stats(g(A2.rows, "冷").map(r => r.busy)),
    A1冷JS: C.stats(g(A1.rows, "冷").map(r => r.js)), A1熱JS: C.stats(g(A1.rows, "熱").map(r => r.js)), 模型時間: [...A1.rows, ...A2.rows].filter(r => r.page === n).map(r => r.modelAdvance),
    A1版面配置: C.stats(A1.rows.filter(r => r.page === n).map(r => r.layout)) };
}
const all = [...A1.rows, ...A2.rows].map(r => r.busy);
out.cpu.全部 = C.stats(all);
out.cpu.依輪次 = [1, 2, 3, 4, 5].map(r => ({ 輪: r, 忙碌: A1.rows.filter(x => x.rep === r).map(x => x.busy), JS: A1.rows.filter(x => x.rep === r).map(x => x.js), 負載: A1.rows.filter(x => x.rep === r).map(x => x.loadavg.split(" ")[0]) }));

// 2. A3 trace
out.trace = {};
for (const n of [1, 2, 5]) {
  const ev = load(`trace-p${n}.json.gz`).traceEvents || load(`trace-p${n}.json.gz`);
  const xs = mainThread(ev), tops = tree(xs);
  const t0 = Math.min(...xs.map(e => e.ts)), t1 = Math.max(...xs.map(e => e.ts + e.dur));
  const busy = tops.reduce((a, e) => a + e.dur, 0), self = new Map();
  tops.forEach(t => selfIn(t).forEach((v, k) => self.set(k, (self.get(k) || 0) + v)));
  const cats = new Map(); self.forEach((v, k) => cats.set(CAT(k), (cats.get(CAT(k)) || 0) + v));
  out.trace[`p${n}`] = { 時間窗ms: ms(t1 - t0), 頂層工作ms: ms(busy), 忙碌比例: +(busy / (t1 - t0) * 100).toFixed(1),
    分類: [...cats.entries()].sort((a, b) => b[1] - a[1]).map(([k, v]) => [k, ms(v), +(v / busy * 100).toFixed(1) + "%"]),
    前12名: [...self.entries()].sort((a, b) => b[1] - a[1]).slice(0, 12).map(([k, v]) => [k, ms(v)]) };
  // DoUpdateLayers裡面有什麼（如果有子事件）
  const dul = xs.filter(e => e.name === "LayerTreeHost::DoUpdateLayers");
  const kids = new Map(); dul.forEach(e => e._kids.forEach(k => kids.set(k.name, (kids.get(k.name) || 0) + k.dur)));
  out.trace[`p${n}`].DoUpdateLayers = { 次數: dul.length, 平均ms: ms(dul.reduce((a, e) => a + e.dur, 0) / Math.max(1, dul.length)), 子事件: [...kids.entries()].sort((a, b) => b[1] - a[1]).slice(0, 6).map(([k, v]) => [k, ms(v)]) };
  // 每一格（FireAnimationFrame或BeginMainThreadFrame）的頂層工作數
  out.trace[`p${n}`].動畫格數 = xs.filter(e => e.name === "FireAnimationFrame").length;
}

// 3. Lighthouse trace：最長的頂層工作
out.lighthouse = [];
for (const f of fs.readdirSync(D).filter(f => /\.trace\.json\.gz$/.test(f) && !f.startsWith("trace-")).sort()) {
  const j = load(f), ev = j.traceEvents || j, xs = mainThread(ev), tops = tree(xs);
  const sorted = [...tops].sort((a, b) => b.dur - a.dur), top = sorted[0], self = selfIn(top);
  const cats = new Map(); self.forEach((v, k) => cats.set(CAT(k), (cats.get(CAT(k)) || 0) + v));
  const sumF = f.replace(/-\d+-0\.trace\.json\.gz$/, "-summary.json"), idx = +f.match(/-(\d+)-0\.trace/)[1];
  const row = JSON.parse(fs.readFileSync(path.join(D, sumF))).find(r => r.i === idx);
  out.lighthouse.push({ 檔案: f, TBT: row.tbt, 分數: row.score, 負載: row.loadBefore, 最長頂層工作ms: ms(top.dur), 超過50ms的頂層工作: tops.filter(t => t.dur > 50000).length,
    分類: [...cats.entries()].sort((a, b) => b[1] - a[1]).map(([k, v]) => [k, ms(v)]), 前8名: [...self.entries()].sort((a, b) => b[1] - a[1]).slice(0, 8).map(([k, v]) => [k, ms(v)]) });
}
fs.writeFileSync(path.join(D, "analysis.json"), JSON.stringify(out, null, 1));
console.log(JSON.stringify(out, null, 1));

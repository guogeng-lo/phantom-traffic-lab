/* A3. Performance trace：第1、2、5頁各1次（冷，同A1的條件），錄6秒，統計renderer主執行緒每種工作的self time。
 * 用法：node trace.js <輸出資料夾> */
const { chromium } = require("playwright"); const zlib = require("zlib"); const path = require("path");
const C = require("./common");
const outDir = process.argv[2];
function analyze(trace) {
  const ev = trace.traceEvents || trace;
  const names = new Map(); ev.filter(e => e.ph === "M" && e.name === "thread_name").forEach(e => names.set(`${e.pid}:${e.tid}`, e.args.name));
  const mainKey = [...names.entries()].filter(([, v]) => v === "CrRendererMain").map(([k]) => k);
  // 找事件最多的那個renderer主執行緒（簡報的分頁）
  const count = k => ev.filter(e => `${e.pid}:${e.tid}` === k && e.ph === "X").length;
  const key = mainKey.sort((a, b) => count(b) - count(a))[0];
  const xs = ev.filter(e => `${e.pid}:${e.tid}` === key && e.ph === "X" && e.dur != null).sort((a, b) => a.ts - b.ts || b.dur - a.dur);
  // self time：事件時間減掉包在裡面的子事件
  const self = new Map(), stack = [];
  for (const e of xs) {
    while (stack.length && stack[stack.length - 1].ts + stack[stack.length - 1].dur <= e.ts) stack.pop();
    const parent = stack[stack.length - 1];
    if (parent) parent._child = (parent._child || 0) + e.dur;
    stack.push(e);
  }
  for (const e of xs) self.set(e.name, (self.get(e.name) || 0) + (e.dur - (e._child || 0)));
  const top = xs.filter(e => e.name === "RunTask" || e.name === "ThreadControllerImpl::RunTask");
  const t0 = xs.length ? xs[0].ts : 0, t1 = xs.length ? Math.max(...xs.map(e => e.ts + e.dur)) : 0;
  const busy = top.reduce((a, e) => a + e.dur, 0);
  return { span: (t1 - t0) / 1000, busyTopLevelMs: busy / 1000, self: [...self.entries()].sort((a, b) => b[1] - a[1]).slice(0, 25).map(([k, v]) => [k, +(v / 1000).toFixed(1)]) };
}
(async () => {
  const { srv, url } = await C.serve(); const res = {};
  for (const n of [1, 2, 5]) {
    const browser = await chromium.launch(), ctx = await browser.newContext(C.MOBILE), page = await ctx.newPage(); await C.blockExternal(page);
    await page.goto(url + `#p${n}`); await page.waitForTimeout(500); await C.setup(page, n); await page.waitForTimeout(300);
    const cdp = await ctx.newCDPSession(page); await cdp.send("Emulation.setCPUThrottlingRate", { rate: 4 });
    await browser.startTracing(page, { categories: ["devtools.timeline", "disabled-by-default-devtools.timeline", "toplevel", "blink", "cc", "gpu", "v8", "disabled-by-default-devtools.timeline.frame"] });
    await page.waitForTimeout(6000);
    const buf = await browser.stopTracing();
    require("fs").writeFileSync(path.join(outDir, `trace-p${n}.json.gz`), zlib.gzipSync(buf));
    res[`p${n}`] = analyze(JSON.parse(buf.toString()));
    console.log(`p${n}：主執行緒頂層工作${res[`p${n}`].busyTopLevelMs.toFixed(0)} ms／${res[`p${n}`].span.toFixed(0)} ms；self time前幾名：` + res[`p${n}`].self.slice(0, 8).map(([k, v]) => `${k} ${v}`).join("、"));
    await browser.close();
  }
  require("fs").writeFileSync(path.join(outDir, "trace-summary.json"), JSON.stringify(res, null, 1)); srv.close();
})().catch(e => { console.error("診斷程式出錯：", e); process.exit(2); });

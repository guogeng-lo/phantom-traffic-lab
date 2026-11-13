/* B. Lighthouse診斷。用法：node lh.js <組別> <次數> <輸出資料夾> [--port=9222]
 * 條件跟tests/perf_mobile.js一樣（手機、模擬慢速4G、CPU慢4倍、#p1、只量performance）。
 * 每次存完整結果（gzip）和trace（--save-assets），另外摘要：分數、LCP、TBT、CLS、FCP、long-tasks、主執行緒工作分類。 */
const { execFile } = require("child_process"); const fs = require("fs"); const path = require("path"); const zlib = require("zlib");
const { chromium } = require("playwright");
const C = require("./common");
const [group, times, outDir, portArg] = process.argv.slice(2);
(async () => {
  const { srv, url } = await C.serve(); const env = Object.assign({}, process.env, { CHROME_PATH: chromium.executablePath() }); const rows = [];
  for (let i = 1; i <= +times; i++) {
    const e0 = C.env(`${group}#${i}前`), base = path.join(outDir, `${group}-${i}`);
    const args = [require.resolve("lighthouse/cli/index.js"), url + "#p1", "--only-categories=performance", "--output=json", `--output-path=${base}.json`, "--save-assets", "--quiet"];
    if (portArg) args.push(portArg); else args.push("--chrome-flags=--headless=new --no-sandbox");
    const t0 = Date.now();
    await new Promise((res, rej) => execFile(process.execPath, args, { env, timeout: 300000 }, err => err ? rej(err) : res()));
    const d = JSON.parse(fs.readFileSync(`${base}.json`, "utf8")), A = d.audits;
    const lt = (A["long-tasks"].details || { items: [] }).items.map(x => ({ url: x.url, start: Math.round(x.startTime), dur: Math.round(x.duration) }));
    const mw = (A["mainthread-work-breakdown"].details || { items: [] }).items.map(x => [x.groupLabel || x.group, Math.round(x.duration)]);
    const row = { group, i, wallS: (Date.now() - t0) / 1000, score: d.categories.performance.score, lcp: Math.round(A["largest-contentful-paint"].numericValue), tbt: Math.round(A["total-blocking-time"].numericValue),
      cls: A["cumulative-layout-shift"].numericValue, fcp: Math.round(A["first-contentful-paint"].numericValue), longTasks: lt, mainthread: mw, loadBefore: e0.loadavg, topBefore: e0.top };
    rows.push(row);
    for (const f of fs.readdirSync(outDir).filter(f => f.startsWith(`${group}-${i}`) && !f.endsWith(".gz"))) { const p = path.join(outDir, f); fs.writeFileSync(p + ".gz", zlib.gzipSync(fs.readFileSync(p))); fs.unlinkSync(p); }
    console.log(`${group} 第${i}次：效能${row.score} TBT ${row.tbt} ms LCP ${row.lcp} ms 負載${row.loadBefore}${row.tbt > 1000 ? "　← 異常" : ""}；長任務：${lt.map(x => `${x.dur}ms@${x.start}(${x.url.split("/").pop() || x.url})`).join("、") || "無"}`);
  }
  fs.writeFileSync(path.join(outDir, `${group}-summary.json`), JSON.stringify(rows, null, 1)); srv.close();
})().catch(e => { console.error("診斷程式出錯：", e); process.exit(2); });

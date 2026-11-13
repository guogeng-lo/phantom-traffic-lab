/* 節點7：手機效能。標準在跑之前寫在這裡（下面的LIMITS），沒過就改程式，不改標準；要改標準先問使用者。
 * 用法：node tests/perf_mobile.js
 * 1. Lighthouse（手機設定：模擬慢速4G、CPU慢4倍）量第1頁的載入：效能分數、LCP、TBT、CLS。
 *    固定條件下連續、各自獨立跑5次（每次新開瀏覽器），每個指標取5次的中位數跟門檻比；5次的原始數字全部印出來。
 *    單次TBT超過1000 ms的另外標成「異常」，不能因為中位數通過就忽略；異常出現2次以上，整項算沒通過，要調查。
 *    （2026-11-13使用者授權：原本只跑1次。第2輪同一版本出現過0.74／TBT 1,240 ms，之後3次都是0.99，
 *     單次結果不穩定。門檻不變。見runs/2026-11-13-n7-standard-lighthouse.md）
 * 2. 動畫和圖表的CPU負擔：Chromium開手機畫面（375×812、裝置像素比3），CPU慢4倍，每個會動的頁面跑6秒，
 *    用CDP的Performance.getMetrics量主執行緒忙碌的比例；同時確認模型時間照每秒6個模型時間前進（沒有因為效能偷少算）。
 * 3. 不在畫面上的東西不能算：第1頁捲到看不到、換到沒有動畫的第7頁時，主執行緒要幾乎沒事。
 * 4. 頁面裡的求解器DT還是0.05（PARITY.md的J12，在瀏覽器裡再確認一次）。 */
const path = require("path");
const { execFile } = require("child_process");
const { chromium } = require("playwright");
const { serve, blockExternal } = require("./site_server");

const LIMITS = {
  lhScore: 0.9,          // Lighthouse效能分數「良好」的下限
  lcpMs: 2500, tbtMs: 200, cls: 0.1,   // Core Web Vitals「良好」的門檻（TBT用Lighthouse的良好門檻）
  busy: 0.6,             // 動畫頁：CPU慢4倍時，主執行緒忙碌比例上限（留四成給讀者的操作）
  idleBusy: 0.08,        // 沒有動畫或看不到時的上限
  rate: 0.9,             // 模型時間至少要走到「每秒6個模型時間×秒數」的90%
  lhRuns: 5,             // Lighthouse跑幾次，取中位數
  tbtOutlierMs: 1000,    // 單次TBT超過這個值標成異常
  maxOutliers: 1         // 異常超過這個次數，整項算沒通過
};
let fails = 0;
const say = (ok, msg) => { if (!ok) fails++; console.log(`${ok ? "通過" : "沒通過"}｜${msg}`); };

(async () => {
  const { srv, url } = await serve();
  console.log("## 標準", JSON.stringify(LIMITS));

  // ---- 1. Lighthouse：5次取中位數 ----
  const fs = require("fs");
  const env = Object.assign({}, process.env, { CHROME_PATH: chromium.executablePath() });
  const runs = [];
  for (let i = 1; i <= LIMITS.lhRuns; i++) {
    const out = path.join(require("os").tmpdir(), `lh-${process.pid}-${i}.json`);
    try {
      // 用非同步的execFile：本機伺服器跑在同一個程式裡，同步等待會讓伺服器沒辦法回應
      await new Promise((res, rej) => execFile(process.execPath, [require.resolve("lighthouse/cli/index.js"), url + "#p1", "--only-categories=performance", "--output=json", `--output-path=${out}`,
        "--chrome-flags=--headless=new --no-sandbox", "--quiet"], { env, timeout: 300000 }, err => err ? rej(err) : res()));
      const d = JSON.parse(fs.readFileSync(out, "utf8")), A = d.audits;
      const r = { score: d.categories.performance.score, lcp: A["largest-contentful-paint"].numericValue, tbt: A["total-blocking-time"].numericValue, cls: A["cumulative-layout-shift"].numericValue, fcp: A["first-contentful-paint"].numericValue };
      runs.push(r);
      if (i === 1) console.log(`  Lighthouse ${d.lighthouseVersion}，${d.configSettings.formFactor}，CPU慢${d.configSettings.throttling.cpuSlowdownMultiplier}倍`);
      console.log(`  第${i}次：效能${r.score}、LCP ${(r.lcp / 1000).toFixed(2)} s、TBT ${Math.round(r.tbt)} ms、CLS ${r.cls.toFixed(3)}、FCP ${(r.fcp / 1000).toFixed(2)} s${r.tbt > LIMITS.tbtOutlierMs ? "　← 異常（TBT超過1000 ms）" : ""}`);
    } catch (e) { console.log(`  第${i}次：Lighthouse沒有跑完：${String(e.message).split("\n")[0]}`); }
  }
  say(runs.length === LIMITS.lhRuns, `Lighthouse跑完${runs.length}／${LIMITS.lhRuns}次`);
  if (runs.length) {
    const med = k => { const v = runs.map(r => r[k]).sort((a, b) => a - b), m = v.length >> 1; return v.length % 2 ? v[m] : (v[m - 1] + v[m]) / 2; };
    say(med("score") >= LIMITS.lhScore, `Lighthouse效能分數中位數 ${med("score")}（要≥${LIMITS.lhScore}）`);
    say(med("lcp") <= LIMITS.lcpMs, `LCP中位數 ${(med("lcp") / 1000).toFixed(2)} s（要≤${LIMITS.lcpMs / 1000} s）`);
    say(med("tbt") <= LIMITS.tbtMs, `TBT中位數 ${Math.round(med("tbt"))} ms（要≤${LIMITS.tbtMs} ms）`);
    say(med("cls") <= LIMITS.cls, `CLS中位數 ${med("cls").toFixed(3)}（要≤${LIMITS.cls}）`);
    const out = runs.filter(r => r.tbt > LIMITS.tbtOutlierMs).length;
    say(out <= LIMITS.maxOutliers, `TBT異常（單次超過${LIMITS.tbtOutlierMs} ms）${out}次（超過${LIMITS.maxOutliers}次算反覆出現，要調查）`);
  }

  // ---- 2、3. 動畫的CPU負擔 ----
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 375, height: 812 }, deviceScaleFactor: 3, isMobile: true, hasTouch: true });
  const page = await ctx.newPage(); await blockExternal(page);
  await page.goto(url + "#p1"); await page.waitForTimeout(500);
  const cdp = await ctx.newCDPSession(page);
  await cdp.send("Performance.enable"); await cdp.send("Emulation.setCPUThrottlingRate", { rate: 4 });
  const metrics = async () => Object.fromEntries((await cdp.send("Performance.getMetrics")).metrics.map(m => [m.name, m.value]));
  async function measure(label, secs, prep, limit, after) {
    if (prep) await prep();
    await page.waitForTimeout(300);
    const before = after ? await after() : null, m0 = await metrics();
    await page.waitForTimeout(secs * 1000);
    const m1 = await metrics(), dur = m1.Timestamp - m0.Timestamp, busy = (m1.TaskDuration - m0.TaskDuration) / dur;
    say(busy <= limit, `${label}：主執行緒忙碌 ${(busy * 100).toFixed(0)}%（要≤${limit * 100}%；JS ${((m1.ScriptDuration - m0.ScriptDuration) / dur * 100).toFixed(0)}%）`);
    if (after) { const t1 = await after(); return [before, t1, dur]; }
  }
  const clock = n => async () => parseFloat(await page.locator(`#p${n} .clock b`).first().textContent());
  const go = n => async () => { await page.evaluate(n => window.__deck.go(n), n); };
  // 第1頁：自動播放
  const [a1, b1, d1] = await measure("第1頁環道自動播放", 6, null, LIMITS.busy, clock(1));
  say(b1 - a1 >= 6 * d1 * LIMITS.rate, `第1頁：模型時間在${d1.toFixed(1)}秒內走了${(b1 - a1).toFixed(1)}（每秒6個模型時間應該是${(6 * d1).toFixed(1)}）`);
  await measure("第1頁捲到看不到環道", 4, async () => { await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight)); }, LIMITS.idleBusy);
  // 第2頁：點一台車之後
  await measure("第2頁點車之後播放", 6, async () => { await go(2)(); await page.locator("#p2 canvas.ring").focus(); await page.keyboard.press("Enter"); }, LIMITS.busy);
  // 第3頁：疊上全部的車之後（時間游標在動）
  await measure("第3頁時空圖（全部的車、游標在動）", 6, async () => { await go(3)(); await page.waitForFunction(() => !document.querySelector("#p3 .placard .btns button").disabled, null, { timeout: 60000 });
    await page.locator("#p3").getByRole("button", { name: "疊上其他車" }).click(); await page.locator("#p3 canvas.chart").scrollIntoViewIfNeeded(); }, LIMITS.busy);
  // 第4頁：兩張圖邊算邊畫
  await measure("第4頁兩張圖邊算邊畫", 5, async () => { await go(4)(); await page.locator("#p4").getByRole("button", { name: "開始" }).click(); }, LIMITS.busy);
  // 第5頁：a=1點車之後播放
  await measure("第5頁點車之後播放", 6, async () => { await go(5)(); await page.locator("#p5").getByRole("button", { name: "看調多快" }).click(); await page.locator("#p5 canvas.ring").focus(); await page.keyboard.press("Enter"); }, LIMITS.busy);
  // 第6頁：單一車數的環道動畫（全部跑一次在背景執行緒，不算在主執行緒）
  await measure("第6頁環道動畫＋背景計算全部車數", 6, async () => { await go(6)(); await page.locator("#p6").getByRole("button", { name: "中間那段" }).click(); await page.locator("#p6").getByRole("button", { name: "把3到60台全部跑一次" }).click(); }, LIMITS.busy);
  console.log(`  （第6頁的背景計算用${await page.evaluate(() => window.__deck.engine.mode === "worker" ? "Web Worker" : "主執行緒（Worker開不起來）")}）`);
  // 第7頁：沒有動畫
  await measure("第7頁（沒有動畫）", 4, go(7), LIMITS.idleBusy);
  // ---- 4. DT ----
  const dt = await page.evaluate(() => window.OVM.DT);
  say(dt === 0.05, `頁面裡的求解器DT = ${dt}（要是0.05，不能為了效能放大）`);
  await browser.close(); srv.close();
  console.log(`\n沒通過${fails}項。`);
  process.exit(fails ? 1 : 0);
})().catch(e => { console.error("測試程式出錯：", e); process.exit(2); });

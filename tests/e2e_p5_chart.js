/* 第3輪之後的限定效能修補：第5頁擾動圖的重畫（標準見runs/2026-11-13-n7-perf-patch-authorization.md）。
 * 用法：node tests/e2e_p5_chart.js
 * 桌機1280和手機375各跑一次，用正常動態（不是減少動態），才看得到播放中的重畫。
 * 量重畫次數：包住擾動圖畫布的getContext，每次重畫都會呼叫一次。
 * 「畫面是不是最新的」：先把畫布存成圖，再觸發一次視窗resize（頁面會把目前這頁強制重畫），兩張圖要逐像素一樣。 */
const { chromium } = require("playwright");
const { serve, blockExternal } = require("./site_server");

let fails = 0;
const say = (ok, m, got) => { if (!ok) fails++; console.log(`${ok ? "通過" : "沒通過"}｜${m}${got !== undefined ? `｜實際：${got}` : ""}`); };

async function one(browser, url, label, opt) {
  console.log(`\n## ${label}`);
  const ctx = await browser.newContext(opt), page = await ctx.newPage(); await blockExternal(page);
  const errs = []; page.on("pageerror", e => errs.push(String(e)));
  page.on("console", m => { if (m.type() === "error" && !/ERR_FAILED|net::/.test(m.text())) errs.push(m.text()); });
  await page.goto(url + "#p5"); await page.waitForTimeout(400);
  const s = page.locator("#p5");
  await s.getByRole("button", { name: "看調多快" }).click();
  await page.evaluate(() => { const cv = document.querySelector("#p5 canvas.chart"), g = cv.getContext.bind(cv); window.__paints = 0; cv.getContext = (...a) => { window.__paints++; return g(...a); }; });
  const paints = () => page.evaluate(() => window.__paints);
  const snap = () => page.evaluate(() => document.querySelector("#p5 canvas.chart").toDataURL());
  const clock = async () => parseFloat(await s.locator(".clock b").textContent());
  // 「畫面是最新的」：現在的圖 vs 強制重畫後的圖
  async function fresh(name) {
    await page.waitForTimeout(300);
    const a = await snap(); const p0 = await paints();
    await page.evaluate(() => window.dispatchEvent(new Event("resize"))); await page.waitForTimeout(300);
    const b = await snap(), p1 = await paints();
    say(p1 > p0 && a === b, `${name}：畫面上的擾動圖跟強制重畫的結果一樣`, `${p1 > p0 ? "有強制重畫" : "沒有重畫"}、${a === b ? "逐像素一樣" : "不一樣"}`);
  }
  // 1、2. 播放中（a=1，點第0台）
  await s.locator("canvas.ring").focus(); await page.keyboard.press("Enter");
  await page.waitForTimeout(500);
  const c0 = await clock(), p0 = await paints();
  await page.waitForTimeout(3000);
  const c1 = await clock(), p1 = await paints();
  const newPts = Math.floor((c1 - c0) / 0.5) + 1;
  say(p1 - p0 <= newPts + 2 && p1 - p0 >= 1, "播放中：3秒內擾動圖重畫的次數不超過新增的資料點數＋2", `重畫${p1 - p0}次，新增資料點約${newPts}個`);
  say(c1 - c0 >= 16.2, "播放中：環道照每秒6個模型時間前進", `3秒走了${(c1 - c0).toFixed(1)}`);
  // 3、4. 暫停
  await s.getByRole("button", { name: "暫停", exact: true }).click();
  await page.waitForTimeout(300);
  const q0 = await paints(); await page.waitForTimeout(1500); const q1 = await paints();
  say(q1 === q0, "暫停1.5秒：擾動圖不重畫", `重畫${q1 - q0}次`);
  await fresh("暫停時");
  // 4. 完成
  await s.getByRole("button", { name: "快轉", exact: true }).click();
  await page.waitForFunction(() => document.querySelector("#p5 .placard .say").textContent.includes("塞住了"), null, { timeout: 60000 });
  await fresh("完成（塞住了）時");
  // 4. 重設
  await s.getByRole("button", { name: "重來", exact: true }).click();
  await fresh("按「重來」之後");
  // 4. 換a
  await s.locator("#p5a").fill("3");
  await fresh("換成a=2.2之後");
  // 5. 改變寬度
  const r0 = await paints();
  const w2 = label.includes("手機") ? 320 : 900;
  await page.setViewportSize({ width: w2, height: 800 }); await page.waitForTimeout(600);
  const r1 = await paints();
  const size = await page.evaluate(() => { const cv = document.querySelector("#p5 canvas.chart"); return [cv.width, Math.round(cv.clientWidth * Math.min(2, devicePixelRatio || 1))]; });
  say(r1 > r0 && size[0] === size[1], "改變視窗寬度：擾動圖重畫，畫布寬度跟新的寬度一致", `重畫${r1 - r0}次，畫布${size[0]}px、應該${size[1]}px`);
  await fresh("改變寬度之後");
  say(errs.length === 0, "沒有JavaScript錯誤", errs.join(" / ") || "0個");
  await ctx.close();
}

(async () => {
  const { srv, url } = await serve();
  const browser = await chromium.launch();
  await one(browser, url, "桌機1280", { viewport: { width: 1280, height: 900 } });
  await one(browser, url, "手機375", { viewport: { width: 375, height: 812 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
  await browser.close(); srv.close();
  console.log(`\n沒通過${fails}項。`);
  process.exit(fails ? 1 : 0);
})().catch(e => { console.error("測試程式出錯：", e); process.exit(2); });

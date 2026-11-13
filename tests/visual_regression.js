/* 節點7：桌機（1280×900）和手機（375×812）的視覺回歸截圖。
 * 用法：node tests/visual_regression.js <輸出資料夾>
 *       python3 tests/compare_shots.py tests/visual-baseline <輸出資料夾>
 * 每一頁先操作到固定的狀態（模擬跑完、題目答完），再截整頁。用「減少動態」模式，讓動畫不受截圖時間影響。
 * 基準截圖在這個容器的Chromium和字型下產生；換電腦或字型，基準要重做（重做要寫進紀錄）。 */
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");
const { serve, blockExternal } = require("./site_server");

const OUT = path.resolve(process.argv[2] || "shots");
fs.mkdirSync(OUT, { recursive: true });

async function states(page, n) {
  const s = page.locator(`#p${n}`), wait = (f, t = 120000) => page.waitForFunction(f, null, { timeout: t });
  const press = name => s.getByRole("button", { name, exact: true }).click();
  if (n === 1) await press("快轉到有車幾乎停住");
  if (n === 2) { await s.locator("canvas.ring").focus(); await page.keyboard.press("Enter"); await press("快轉到有車幾乎停住"); await page.waitForTimeout(1200); }
  if (n === 3) { await wait(() => !document.querySelector("#p3 .placard .btns button").disabled); await press("疊上其他車"); await press("往左，跟車子反方向"); }
  if (n === 4) { await press("開始"); await wait(() => document.querySelector("#p4 .say").textContent.includes("畫完了")); }
  if (n === 5) { await press("看調多快"); await s.locator("canvas.ring").focus(); await page.keyboard.press("Enter"); await press("快轉"); await wait(() => document.querySelector("#p5 .placard .say").textContent.includes("塞住了")); }
  if (n === 6) { await press("中間那段"); await press("跑這個車數"); await wait(() => document.querySelector("#p6 .placard .say").textContent.startsWith("22台："));
    await press("把3到60台全部跑一次"); await wait(() => document.querySelector("#p6 .progress").textContent.includes("算完了"), 300000);
    await page.evaluate(() => { document.querySelector("#p6 .progress").textContent = "（截圖時把花了幾秒的文字固定住）"; }); }
  if (n === 8) { await press("固定目標速度"); await wait(() => document.querySelector("#p8 .sim-box .say").textContent.includes("跑完了"));
    await press("不一定，可能更大"); await press("跑這個值"); await wait(() => document.querySelectorAll("#p8 .sim-box")[1].querySelector(".say").textContent.includes("跑完了")); }
  if (n === 9) await s.locator("details.card9 summary").first().click();
  if (n === 10) for (let q = 1; q <= 3; q++) { await s.locator(`.quiz[data-quiz="${q}"] .opt[data-right="1"]`).click(); await s.locator(`.quiz[data-quiz="${q}"]`).getByRole("button", { name: q < 3 ? "下一題" : "看延伸閱讀" }).click(); }
}

module.exports = { states };
if (require.main === module) (async () => {
  const { srv, url } = await serve();
  const browser = await chromium.launch();
  for (const [tag, opt] of [["desktop", { viewport: { width: 1280, height: 900 } }], ["m375", { viewport: { width: 375, height: 812 }, isMobile: true, hasTouch: true }]]) {
    const ctx = await browser.newContext(Object.assign({ reducedMotion: "reduce", deviceScaleFactor: 1 }, opt));
    for (let n = 1; n <= 10; n++) {
      const page = await ctx.newPage(); await blockExternal(page);
      await page.goto(url + `#p${n}`); await page.waitForTimeout(300);
      await states(page, n); await page.waitForTimeout(400);
      // 黏在下方的換頁列會跟著整頁截圖跑到中間，截圖時先拿掉
      await page.addStyleTag({ content: ".pager{position:static!important}" });
      await page.evaluate(() => window.scrollTo(0, 0)); await page.waitForTimeout(200);
      const f = path.join(OUT, `${tag}-p${String(n).padStart(2, "0")}.png`);
      await page.screenshot({ path: f, fullPage: true, animations: "disabled", caret: "hide" });
      console.log(`已截圖 ${path.basename(f)}`);
      await page.close();
    }
    await ctx.close();
  }
  await browser.close(); srv.close();
})().catch(e => { console.error("截圖程式出錯：", e); process.exit(2); });

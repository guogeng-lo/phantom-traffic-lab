/* 節點7第3輪（N7-15）：不同寬度下的版面。
 * 用法：node tests/layout_widths.js
 * 寬度：320（WCAG重排的最小寬度）、640（1280寬的桌機放大200%）、768（平板直放）。375和1280在e2e_flow.js測。
 * 每一頁先操作到全部打開的狀態（跟視覺回歸同一套操作），再檢查：
 *   1. 整頁沒有超出畫面寬度（document的scrollWidth不大於畫面寬度）。
 *   2. 按鈕、表格格子、結果列、展開區標題、滑桿數值裡的字沒有超出自己的框。
 * 截圖存到指定的資料夾給人看，不當基準。 */
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");
const { serve, blockExternal } = require("./site_server");
const { states } = require("./visual_regression");

const OUT = process.argv[2] ? path.resolve(process.argv[2]) : null;
if (OUT) fs.mkdirSync(OUT, { recursive: true });
let fails = 0;
const say = (ok, m) => { if (!ok) fails++; console.log(`${ok ? "通過" : "沒通過"}｜${m}`); };

(async () => {
  const { srv, url } = await serve();
  const browser = await chromium.launch();
  for (const [w, h, mobile, label] of [[320, 700, true, "320寬（手機最窄）"], [640, 450, false, "640寬（1280放大200%）"], [768, 1024, true, "768寬（平板）"]]) {
    console.log(`\n## ${label}`);
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, isMobile: mobile, hasTouch: mobile, reducedMotion: "reduce", deviceScaleFactor: 1 });
    for (let n = 1; n <= 10; n++) {
      const page = await ctx.newPage(); await blockExternal(page);
      await page.goto(url + `#p${n}`); await page.waitForTimeout(300);
      await states(page, n); await page.waitForTimeout(300);
      const r = await page.evaluate(n => {
        const sw = document.documentElement.scrollWidth, vw = window.innerWidth;
        const spill = [...document.querySelectorAll(`#p${n} button, #p${n} td, #p${n} th, #p${n} dd, #p${n} dt, #p${n} summary, #p${n} output, .pager button, .top summary`)]
          .filter(e => e.checkVisibility() && e.scrollWidth > e.clientWidth + 1).map(e => `${e.tagName.toLowerCase()}「${e.textContent.trim().slice(0, 10)}」`);
        return { sw, vw, spill };
      }, n);
      say(r.sw <= w && r.spill.length === 0, `第${n}頁：整頁寬${r.sw}px（畫面${w}px）${r.spill.length ? "；文字溢出：" + r.spill.slice(0, 4).join("、") : "，沒有文字溢出"}`);
      if (OUT) await page.screenshot({ path: path.join(OUT, `w${w}-p${String(n).padStart(2, "0")}.png`), fullPage: true });
      await page.close();
    }
    await ctx.close();
  }
  await browser.close(); srv.close();
  console.log(`\n沒通過${fails}項。`);
  process.exit(fails ? 1 : 0);
})().catch(e => { console.error("測試程式出錯：", e); process.exit(2); });

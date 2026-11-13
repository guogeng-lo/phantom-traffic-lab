/* 節點8最後一批限定範圍的排版修正（紀錄：runs/2026-11-13-n8-layout-fixes.md）。
 * 用法：node tests/n8_layout_fixes.js [截圖資料夾]     （SITE_URL=網址 可改測正式網址）
 * 寬度：320、375、390、430（手機觸控）、1280（桌機）。
 *   1. 第7頁：三張實驗卡，標題後面的內文不以「：」開頭；標題還是「年份，地點」。
 *   2. 第3頁時空圖：直的軸標題跟左邊的刻度數字之間至少6px；軸上的字都在畫布裡。
 *   3. 每一頁：底部「第N頁／共10頁」只有一行；「上一頁」「下一頁」字沒有斷行、至少44px高、互不重疊、在畫面裡。
 *   4. 第3頁三張讀圖卡：說明文字沒有任何一行只剩一個字。
 *   5. 第6頁擾動圖：最右邊的刻度離畫布右邊至少6px；所有刻度字都在畫布裡、彼此不重疊。
 * 圖表的字畫在canvas上，看不到DOM，所以先攔下fillText，記下每個字的實際範圍（含旋轉、裝置像素比）。 */
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");
const { serve, blockExternal } = require("./site_server");
const { states } = require("./visual_regression");

const OUT = process.argv[2] ? path.resolve(process.argv[2]) : null;
if (OUT) fs.mkdirSync(OUT, { recursive: true });
let fails = 0;
const say = (ok, m) => { if (!ok) fails++; console.log(`${ok ? "通過" : "沒通過"}｜${m}`); };

// 在頁面載入前攔下canvas畫字：每個畫布記一份清單，整張塗白（重畫）時清空
const HOOK = () => {
  const P = CanvasRenderingContext2D.prototype, fillText = P.fillText, fillRect = P.fillRect;
  P.fillRect = function (x, y, w, h) { if (x === 0 && y === 0 && w >= this.canvas.clientWidth - 1) this.canvas.__texts = []; return fillRect.apply(this, arguments); };
  P.fillText = function (t, x, y) {
    const cv = this.canvas, m = this.getTransform(), k = cv.clientWidth / cv.width, w = this.measureText(t).width, f = parseFloat((this.font.match(/(\d+(\.\d+)?)px/) || [0, 14])[1]);
    const x0 = this.textAlign === "right" || this.textAlign === "end" ? x - w : this.textAlign === "center" ? x - w / 2 : x;
    const y0 = this.textBaseline === "middle" ? y - f / 2 : this.textBaseline === "top" ? y : y - f * 0.8;
    const pts = [[x0, y0], [x0 + w, y0], [x0, y0 + f], [x0 + w, y0 + f]].map(([a, b]) => [(m.a * a + m.c * b + m.e) * k, (m.b * a + m.d * b + m.f) * k]);
    const xs = pts.map(p => p[0]), ys = pts.map(p => p[1]);
    (cv.__texts = cv.__texts || []).push({ t: String(t), l: Math.min(...xs), r: Math.max(...xs), top: Math.min(...ys), bot: Math.max(...ys), rot: Math.abs(m.b) > 1e-6 });
    return fillText.apply(this, arguments);
  };
};

(async () => {
  const { srv, url } = await serve();
  const browser = await chromium.launch();
  for (const [w, h, mobile] of [[320, 700, true], [375, 812, true], [390, 844, true], [430, 932, true], [1280, 900, false]]) {
    console.log(`\n## ${w}寬`);
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, isMobile: mobile, hasTouch: mobile, reducedMotion: "reduce", deviceScaleFactor: OUT ? 2 : 1 });
    await ctx.addInitScript(HOOK);
    const open = async n => { const p = await ctx.newPage(); await blockExternal(p); await p.goto(url + `#p${n}`); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400); return p; };

    // 1. 第7頁
    let p = await open(7);
    const cards = await p.evaluate(() => [...document.querySelectorAll("#p7 .exp-grid li")].map(li => {
      const s = li.querySelector("strong"), rest = li.textContent.slice(li.textContent.indexOf(s.textContent) + s.textContent.length).trim();
      return { title: s.textContent.trim(), head: rest.slice(0, 12) };
    }));
    say(cards.length === 3, `第7頁：實驗卡${cards.length}張（應該3張）`);
    for (const c of cards) say(/^\d{4}年，/.test(c.title) && !/^[：:]/.test(c.head), `第7頁「${c.title}」：內文開頭是「${c.head}…」`);
    if (OUT) await p.locator("#p7 .exp-grid").screenshot({ path: path.join(OUT, `w${w}-p7-cards.png`) });
    await p.close();

    // 2.、4. 第3頁
    p = await open(3); await states(p, 3); await p.waitForTimeout(400);
    const p3 = await p.evaluate(() => {
      const cv = document.querySelector("#p3 canvas.chart"), T = cv.__texts || [], W = cv.clientWidth, H = cv.clientHeight;
      const title = T.find(x => x.t.startsWith("模型時間")), ticks = T.filter(x => /^\d+$/.test(x.t) && !x.rot && x.r < W * 0.3 && x.top > 60);
      const outside = T.filter(x => x.l < -0.5 || x.r > W + 0.5 || x.top < -0.5 || x.bot > H + 0.5).map(x => x.t);
      // 讀圖卡：每一行有幾個字
      const orphans = [];
      for (const fc of document.querySelectorAll("#p3 .guide figcaption")) for (const node of [fc.firstChild, fc.querySelector("span").firstChild]) {
        const s = node.textContent, lines = new Map();
        for (let i = 0; i < s.length; i++) { const g = document.createRange(); g.setStart(node, i); g.setEnd(node, i + 1); const r = g.getClientRects()[0]; if (!r) continue; const key = Math.round(r.top); lines.set(key, (lines.get(key) || "") + s[i]); }
        for (const line of lines.values()) if (line.trim().length === 1) orphans.push(`「${s}」的「${line}」`);
      }
      return { gap: title && ticks.length ? Math.min(...ticks.map(x => x.l)) - title.r : null, nt: ticks.length, outside, orphans };
    });
    say(p3.gap !== null && p3.gap >= 6, `第3頁：縱軸標題跟刻度數字的距離${p3.gap === null ? "量不到" : p3.gap.toFixed(1) + "px"}（至少6px，刻度${p3.nt}個）`);
    say(p3.outside.length === 0, `第3頁：圖上的字${p3.outside.length ? "超出畫布：" + p3.outside.join("、") : "都在畫布裡"}`);
    say(p3.orphans.length === 0, `第3頁讀圖卡：${p3.orphans.length ? "一行只剩一個字：" + p3.orphans.join("、") : "沒有一行只剩一個字"}`);
    if (OUT) { await p.locator("#p3 .guide").screenshot({ path: path.join(OUT, `w${w}-p3-guide.png`) }); await p.locator("#p3 canvas.chart").screenshot({ path: path.join(OUT, `w${w}-p3-chart.png`) }); }
    await p.close();

    // 5. 第6頁
    p = await open(6); await states(p, 6); await p.waitForTimeout(400);
    const p6 = await p.evaluate(() => {
      const cv = [...document.querySelectorAll("#p6 canvas")].find(c => (c.__texts || []).some(x => x.t === "2100"));
      if (!cv) return null;
      const T = cv.__texts, W = cv.clientWidth, H = cv.clientHeight, last = T.find(x => x.t === "2100");
      const outside = T.filter(x => x.l < -0.5 || x.r > W + 0.5 || x.top < -0.5 || x.bot > H + 0.5).map(x => x.t);
      const ticks = T.filter(x => ["0", "700", "1400", "2100"].includes(x.t)), hit = [];
      for (let i = 0; i < ticks.length; i++) for (let j = i + 1; j < ticks.length; j++) { const a = ticks[i], b = ticks[j]; if (a.l < b.r && b.l < a.r && a.top < b.bot && b.top < a.bot) hit.push(`${a.t}和${b.t}`); }
      return { right: W - last.r, outside, hit, n: ticks.length };
    });
    say(!!p6 && p6.right >= 6, `第6頁：「2100」離畫布右邊${p6 ? p6.right.toFixed(1) + "px" : "量不到"}（至少6px）`);
    say(!!p6 && p6.outside.length === 0 && p6.hit.length === 0 && p6.n === 4, `第6頁：橫軸刻度${p6 ? p6.n : 0}個；${p6 && p6.outside.length ? "超出畫布：" + p6.outside.join("、") : "都在畫布裡"}；${p6 && p6.hit.length ? "重疊：" + p6.hit.join("、") : "沒有重疊"}`);
    if (OUT) await p.locator("#p6 canvas.chart").first().screenshot({ path: path.join(OUT, `w${w}-p6-chart.png`) });
    await p.close();

    // 3. 每一頁的底部頁碼
    p = await open(1);
    for (let n = 1; n <= 10; n++) {
      if (n > 1) { await p.evaluate(n => { location.hash = `#p${n}`; }, n); await p.waitForTimeout(250); }
      const r = await p.evaluate(() => {
        const wh = document.querySelector(".pager .where"), btns = [...document.querySelectorAll(".pager .nav-btn")], vw = document.documentElement.clientWidth;
        const lh = parseFloat(getComputedStyle(wh).lineHeight) || parseFloat(getComputedStyle(wh).fontSize) * 1.3;
        const show = wh.checkVisibility(), R = wh.getBoundingClientRect(), probs = [];
        if (show && R.height > lh * 1.5) probs.push(`「${wh.textContent}」斷成${Math.round(R.height / lh)}行`);
        for (const b of btns) { const q = b.getBoundingClientRect(), bl = parseFloat(getComputedStyle(b).lineHeight) || 24;
          if (q.height < 44) probs.push(`「${b.textContent}」高${q.height}px`);
          if (b.scrollWidth > b.clientWidth + 1) probs.push(`「${b.textContent}」字超出按鈕`);
          const g = document.createRange(); g.selectNodeContents(b); if (g.getClientRects().length > 1) probs.push(`「${b.textContent}」斷行`);
          if (q.left < 0 || q.right > vw) probs.push(`「${b.textContent}」超出畫面`);
          if (show && q.left < R.right && R.left < q.right && q.top < R.bottom && R.top < q.bottom) probs.push(`「${b.textContent}」跟頁碼重疊`); }
        if (btns.length === 2) { const a = btns[0].getBoundingClientRect(), b = btns[1].getBoundingClientRect(); if (a.right > b.left) probs.push("兩個按鈕重疊"); }
        if (document.documentElement.scrollWidth > vw) probs.push(`整頁寬${document.documentElement.scrollWidth}px`);
        return { txt: show ? wh.textContent : "（這個寬度用圓點，不顯示文字）", probs };
      });
      say(r.probs.length === 0, `第${n}頁底部：${r.txt}${r.probs.length ? "：" + r.probs.join("；") : ""}`);
      if (OUT && (n === 3 || n === 10)) await p.locator(".pager").screenshot({ path: path.join(OUT, `w${w}-pager-p${n}.png`) });
    }
    await p.close();
    await ctx.close();
  }
  await browser.close(); srv.close();
  console.log(`\n沒通過${fails}項。`);
  process.exit(fails ? 1 : 0);
})().catch(e => { console.error("測試程式出錯：", e); process.exit(2); });

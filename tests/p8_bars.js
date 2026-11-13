/* 節點8：第8頁三組長條圖的標籤（9筆資料）在各種寬度都完整看得到。
 * 起因：使用者在真實Android手機（Brave）上看到B、C的百分比被截斷、數字和長條擠在一起
 * （紀錄：runs/2026-11-13-n8-p8-bars.md）。
 *
 * 用法：
 *   node tests/p8_bars.js                     # 測本機docs/（擋外部字型，跟其他測試一樣）
 *   node tests/p8_bars.js --url <網址>         # 測正式網址（不擋外部請求；字型檔能不能載入看網路環境）
 *   node tests/p8_bars.js [--url <網址>] --shots <資料夾>   # 另外存每種寬度的長條圖截圖
 *
 * 寬度：320、375、390、430、768（手機觸控），640（1280寬放大200%），1280（桌機）。
 * 每一筆資料檢查：
 *   1. 剛好一個看得到的標籤，文字跟這一筆的無障礙名稱裡的數字一樣（例如「少了80.8%」）。
 *   2. 用文字本身的範圍量（不是框），整段字都在長條圖的卡片裡、也在畫面裡，沒有被任何上層元素裁掉。
 *   3. 字和長條：白字一定整段在長條裡面；不是白字就不能壓到任何長條。
 *      左右用文字範圍（行框寬度）；上下用字形實際的墨跡範圍（2026-11-13授權修正：圓體的行框比字形高，
 *      行框會超出22px高的長條，但字本身沒有。見runs/2026-11-13-n8-p8-bars-measure-authorization.md）。
 *   4. 標籤不能跟其他標籤、A／B／C字母重疊。
 *   5. 減少的長條在中線左邊、增加的在右邊（方向的意思還在）。
 * 另外：整頁沒有橫向捲動。 */
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");
const { serve, blockExternal } = require("./site_server");

const arg = k => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : null; };
const REMOTE = arg("--url"), SHOTS = arg("--shots") ? path.resolve(arg("--shots")) : null;
if (SHOTS) fs.mkdirSync(SHOTS, { recursive: true });
let fails = 0;
const say = (ok, m) => { if (!ok) fails++; console.log(`${ok ? "通過" : "沒通過"}｜${m}`); };

const WIDTHS = [
  [320, 700, true, "320寬（手機最窄）"], [375, 812, true, "375寬"], [390, 844, true, "390寬"], [430, 932, true, "430寬"],
  [640, 450, false, "640寬（1280放大200%）"], [768, 1024, true, "768寬（平板）"], [1280, 900, false, "1280寬（桌機）"],
];

(async () => {
  let srv = null, url = REMOTE;
  if (!url) ({ srv, url } = await serve());
  console.log(`測試對象：${REMOTE ? url : "本機docs/"}`);
  const browser = await chromium.launch();
  for (const [w, h, mobile, label] of WIDTHS) {
    console.log(`\n## ${label}`);
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, isMobile: mobile, hasTouch: mobile, reducedMotion: "reduce", deviceScaleFactor: SHOTS ? 2 : 1 });
    const page = await ctx.newPage();
    if (!REMOTE) await blockExternal(page);
    await page.goto(url + "#p8", { waitUntil: "load" });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForSelector("#p8 .bars .bar-row");
    await page.waitForTimeout(300);
    const r = await page.evaluate(() => {
      const box = document.querySelector("#p8 .bars"), B = box.getBoundingClientRect();
      const vw = document.documentElement.clientWidth, sw = document.documentElement.scrollWidth;
      const hit = (a, b) => a.left < b.right - 0.5 && b.left < a.right - 0.5 && a.top < b.bottom - 0.5 && b.top < a.bottom - 0.5;
      const inside = (a, b) => a.left >= b.left - 0.5 && a.right <= b.right + 0.5 && a.top >= b.top - 0.5 && a.bottom <= b.bottom + 0.5;
      const textRect = e => { const g = document.createRange(); g.selectNodeContents(e); return g.getBoundingClientRect(); };
      // 往上找會裁切的祖先（overflow不是visible），整段字要在它們的範圍裡
      const clipped = (e, t) => { for (let p = e.parentElement; p && p !== document.body; p = p.parentElement) {
        const s = getComputedStyle(p); if ((s.overflowX !== "visible" || s.overflowY !== "visible") && !inside(t, p.getBoundingClientRect())) return p.className || p.tagName; } return null; };
      // 上下方向的墨跡範圍：同字型量字形離基線多高、多低，基線＝行框頂端＋字型的上緣高度
      const cvs = document.createElement("canvas").getContext("2d");
      const ink = (e, t) => { const s = getComputedStyle(e); cvs.font = `${s.fontStyle} ${s.fontWeight} ${s.fontSize} ${s.fontFamily}`;
        const m = cvs.measureText(e.textContent), base = t.top + m.fontBoundingBoxAscent;
        return { left: t.left, right: t.right, top: base - m.actualBoundingBoxAscent, bottom: base + m.actualBoundingBoxDescent, lineH: t.bottom - t.top, inkH: m.actualBoundingBoxAscent + m.actualBoundingBoxDescent, fontH: m.fontBoundingBoxAscent + m.fontBoundingBoxDescent }; };
      const white = e => { const c = getComputedStyle(e).color.match(/\d+(\.\d+)?/g).map(Number); return c[0] > 240 && c[1] > 240 && c[2] > 240; };
      const rows = [...box.querySelectorAll(".bar-row")];
      const axis = box.querySelector(".bar-l").getBoundingClientRect().right; // 中線（減少在左、增加在右）
      const out = [], labels = [], metrics = [];
      rows.forEach((row, ri) => {
        const name = row.getAttribute("aria-label"), want = (name.match(/[少多]了[\d.]+%/) || [""])[0];
        const cands = [...row.querySelectorAll("*")].filter(e => e.checkVisibility() && [...e.childNodes].some(n => n.nodeType === 3 && /[少多]了[\d.]+%/.test(n.textContent)));
        const letter = [...row.querySelectorAll("*")].find(e => e.checkVisibility() && /^(實驗)?[ABC]$/.test(e.textContent.trim()));
        const bars = [...row.querySelectorAll("i")].filter(e => e.checkVisibility() && e.getBoundingClientRect().width > 0);
        const probs = [];
        if (cands.length !== 1) probs.push(`看得到的標籤有${cands.length}個`);
        const lab = cands[0];
        if (lab) {
          const t = textRect(lab), txt = lab.textContent;
          if (!txt.includes(want)) probs.push(`文字「${txt}」不是「${want}」`);
          if (!inside(t, B)) probs.push(`字超出卡片（字${Math.round(t.left)}～${Math.round(t.right)}，卡片${Math.round(B.left)}～${Math.round(B.right)}）`);
          if (t.left < -0.5 || t.right > vw + 0.5) probs.push("字超出畫面");
          const c = clipped(lab, t); if (c) probs.push(`字被「${c}」裁掉`);
          const g = ink(lab, t); metrics.push({ name, lineH: +g.lineH.toFixed(1), fontH: +g.fontH.toFixed(1), inkH: +g.inkH.toFixed(1) });
          for (const b of bars) { const br = b.getBoundingClientRect();
            if (white(lab) && !inside(g, br)) probs.push("白字有一部分在長條外面（白底上看不到）");
            if (!white(lab) && hit(g, br)) probs.push("深色字壓到長條"); }
          if (white(lab) && !bars.some(b => inside(g, b.getBoundingClientRect()))) probs.push("白字不在長條裡");
          if (letter && letter !== lab && hit(t, letter.getBoundingClientRect())) probs.push("字跟A／B／C重疊");
          labels.push({ ri, t });
        }
        for (const b of bars) { const br = b.getBoundingClientRect(), neg = want.startsWith("少");
          if (neg ? br.right > axis + 1.5 : br.left < axis - 1.5) probs.push(`${neg ? "減少" : "增加"}的長條方向不對`); }
        if (!bars.length) probs.push("看不到長條");
        out.push({ name, probs });
      });
      for (let i = 0; i < labels.length; i++) for (let j = i + 1; j < labels.length; j++)
        if (hit(labels[i].t, labels[j].t)) out[labels[i].ri].probs.push(`跟第${labels[j].ri + 1}筆的標籤重疊`);
      return { vw, sw, rows: out, metrics };
    });
    say(r.rows.length === 9, `資料筆數：${r.rows.length}（應該9筆）`);
    say(r.sw <= r.vw, `整頁寬${r.sw}px（畫面${r.vw}px）`);
    const mh = r.metrics.map(m => m.lineH), ih = r.metrics.map(m => m.inkH);
    console.log(`（量法）文字行框高${Math.min(...mh)}～${Math.max(...mh)}px，字型上下緣${r.metrics[0].fontH}px，字形墨跡高${Math.min(...ih)}～${Math.max(...ih)}px`);
    for (const x of r.rows) say(x.probs.length === 0, `${x.name}${x.probs.length ? "：" + x.probs.join("；") : ""}`);
    if (SHOTS) await page.locator("#p8 .bars").screenshot({ path: path.join(SHOTS, `p8-bars-w${w}.png`) });
    await ctx.close();
  }
  await browser.close(); if (srv) srv.close();
  console.log(`\n沒通過${fails}項。`);
  process.exit(fails ? 1 : 0);
})().catch(e => { console.error("測試程式出錯：", e); process.exit(2); });

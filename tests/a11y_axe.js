/* 節點7：無障礙檢查。axe-core（WCAG 2.0／2.1／2.2 A和AA的規則，加上best-practice）＋三項自己寫的檢查：
 *   1. 鍵盤：每個按鈕、連結、滑桿、展開區都能用Tab走到，而且有看得到的焦點框。
 *   2. 觸控：手機上按鈕、滑桿、展開區至少44×44 CSS像素；所有可點的東西至少24×24（文字裡的連結除外，WCAG 2.5.8的例外）。
 *   3. 名稱：每個按鈕都有讀得出來的名稱（axe也會查，這裡再列出名稱給人看）。
 * 用法：node tests/a11y_axe.js
 * 每一頁查兩種狀態：剛進來（鎖著、文字還沒出現）和操作完（解鎖、結果和說明都出現）。 */
const path = require("path");
const { chromium } = require("playwright");
const { serve, blockExternal } = require("./site_server");
const AXE = require.resolve("axe-core/axe.min.js");

let fails = 0;
const say = (ok, msg) => { if (!ok) fails++; console.log(`${ok ? "通過" : "沒通過"}｜${msg}`); };

async function operate(page, n) {   // 把每一頁操作到「全部打開」的狀態（用減少動態，不必等動畫）
  const s = page.locator(`#p${n}`), wait = (f, t = 300000) => page.waitForFunction(f, null, { timeout: t });
  const press = name => s.getByRole("button", { name, exact: true }).click();
  if (n === 1) await press("快轉到有車幾乎停住");
  if (n === 2) { await s.locator("canvas.ring").focus(); await page.keyboard.press("Enter"); await press("快轉到有車幾乎停住"); }
  if (n === 3) { await wait(() => !document.querySelector("#p3 .placard .btns button").disabled); await press("疊上其他車"); await press("往左，跟車子反方向"); }
  if (n === 4) { await press("開始"); await wait(() => document.querySelector("#p4 .say").textContent.includes("畫完了")); }
  if (n === 5) { await press("看調多快"); for (const i of [0, 3]) { await s.locator("#p5a").fill(String(i)); await s.locator("canvas.ring").focus(); await page.keyboard.press("Enter");
    const ff = s.getByRole("button", { name: "快轉", exact: true }); if (await ff.isEnabled()) await ff.click(); await wait(() => /塞住了|0.01以下/.test(document.querySelector("#p5 .placard .say").textContent)); } await press("揭曉"); }
  if (n === 6) { await press("中間那段"); await press("跑這個車數"); await press("把3到60台全部跑一次"); await wait(() => document.querySelector("#p6 .progress").textContent.includes("算完了")); }
  if (n === 8) { await press("固定目標速度"); await wait(() => document.querySelector("#p8 .sim-box .say").textContent.includes("跑完了"));
    await press("不一定，可能更大"); for (const i of [1, 2]) { await s.locator("#p8u").fill(String(i)); await s.locator("#p8u").dispatchEvent("change");
      await wait(() => document.querySelectorAll("#p8 .sim-box")[1].querySelector(".say").textContent.includes("跑完了")); } await press("揭曉"); }
  if (n === 9) for (const d of await s.locator("details.card9 summary").all()) await d.click();
  if (n === 10) for (let q = 1; q <= 3; q++) { await s.locator(`.quiz[data-quiz="${q}"] .opt[data-right="1"]`).click(); await s.locator(`.quiz[data-quiz="${q}"]`).getByRole("button", { name: q < 3 ? "下一題" : "看延伸閱讀" }).click(); }
  for (const d of await s.locator("details.adv > summary, details.src > summary").all()) await d.click();
}

async function custom(page, n, mobile, label) {
  const r = await page.evaluate(({ n, mobile }) => {
    const sel = `#p${n} button, #p${n} a[href], #p${n} input, #p${n} summary, #p${n} canvas[tabindex], .pager button:not([disabled]), .top summary`;
    const els = [...document.querySelectorAll(sel)].filter(e => e.checkVisibility({ contentVisibilityAuto: true, visibilityProperty: true }));   // 收起來的<details>裡面的東西不算
    const small = [], unnamed = [];
    for (const e of els) {
      const b = e.getBoundingClientRect(), inline = e.tagName === "A" && e.closest("p, li") && !e.classList.contains("paper") && !e.closest(".back-links");
      const min = e.matches(".dot") ? 24 : mobile && !inline && e.tagName !== "A" ? 44 : 24;
      if (!inline && (b.width < min - 0.5 || b.height < min - 0.5)) small.push(`${e.tagName.toLowerCase()}「${(e.getAttribute("aria-label") || e.textContent).trim().slice(0, 12)}」${Math.round(b.width)}×${Math.round(b.height)}（要${min}）`);
      const name = (e.getAttribute("aria-label") || e.textContent || "").trim();
      if (e.tagName !== "INPUT" && !name) unnamed.push(e.outerHTML.slice(0, 60));
      if (e.tagName === "INPUT" && !(e.labels && e.labels.length)) unnamed.push(e.outerHTML.slice(0, 60));
    }
    return { count: els.length, small, unnamed };
  }, { n, mobile });
  say(r.small.length === 0, `${label}：可點範圍（${r.count}個控制項）${r.small.length ? "：" + r.small.join("、") : ""}`);
  say(r.unnamed.length === 0, `${label}：控制項都有名稱${r.unnamed.length ? "：" + r.unnamed.join(" / ") : ""}`);
  // 鍵盤：從頁面最上面一直按Tab，記下每一個拿到焦點的東西，確認本頁的控制項都走得到、焦點框看得到
  const reach = await page.evaluate(n => { document.activeElement && document.activeElement.blur(); window.scrollTo(0, 0); return [...document.querySelectorAll(`#p${n} button, #p${n} a[href], #p${n} input, #p${n} summary, #p${n} canvas[tabindex]`)].filter(e => e.checkVisibility({ contentVisibilityAuto: true, visibilityProperty: true }) && !e.disabled).length; }, n);
  await page.locator("body").focus().catch(() => {});
  await page.evaluate(() => { const b = document.querySelector(".brand"); b.tabIndex = -1; b.focus(); b.removeAttribute("tabindex"); });
  const seen = new Set(), noRing = [];
  for (let i = 0; i < 400; i++) {
    await page.keyboard.press("Tab");
    const f = await page.evaluate(n => { const e = document.activeElement; if (!e || e === document.body) return null;
      const cs = getComputedStyle(e), ring = (cs.outlineStyle !== "none" && parseFloat(cs.outlineWidth) >= 2) || cs.boxShadow !== "none";
      if (!e.dataset.k) e.dataset.k = Math.random().toString(36).slice(2);
      return { k: e.dataset.k, inPage: !!e.closest(`#p${n}`), ring, name: (e.getAttribute("aria-label") || e.textContent || e.tagName).trim().slice(0, 14) }; }, n);
    if (!f) continue;
    if (seen.has(f.k)) break;
    seen.add(f.k); if (!f.ring) noRing.push(f.name);
    if (f.inPage) seen.add("in:" + f.k);
  }
  const inPage = [...seen].filter(k => k.startsWith("in:")).length;
  say(inPage >= reach, `${label}：鍵盤Tab走得到本頁的${reach}個控制項（走到${inPage}個）`);
  say(noRing.length === 0, `${label}：拿到焦點時都有焦點框${noRing.length ? "：缺" + noRing.join("、") : ""}`);
}

(async () => {
  const { srv, url } = await serve();
  const browser = await chromium.launch();
  for (const [tag, opt, mobile] of [["桌機1280", { viewport: { width: 1280, height: 900 } }, false], ["手機375", { viewport: { width: 375, height: 812 }, isMobile: true, hasTouch: true }, true]]) {
    console.log(`\n## ${tag}`);
    const ctx = await browser.newContext(Object.assign({ reducedMotion: "reduce" }, opt));
    for (let n = 1; n <= 10; n++) {
      const page = await ctx.newPage(); await blockExternal(page);
      await page.goto(url + `#p${n}`); await page.waitForTimeout(300);
      for (const state of ["剛進來", "操作完"]) {
        if (state === "操作完") await operate(page, n);
        await page.addScriptTag({ path: AXE });
        const res = await page.evaluate(async () => window.axe.run(document, { runOnly: { type: "tag", values: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"] }, resultTypes: ["violations"] }));
        const v = res.violations.map(x => `${x.id}（${x.impact}，${x.nodes.length}處：${x.nodes.slice(0, 2).map(nd => nd.target.join(" ")).join("；")}）`);
        say(v.length === 0, `第${n}頁${state}：axe-core ${res.testEngine.version}${v.length ? "：" + v.join(" / ") : "沒有違規"}`);
        await custom(page, n, mobile, `第${n}頁${state}`);
      }
      await page.close();
    }
    await ctx.close();
  }
  await browser.close(); srv.close();
  console.log(`\n沒通過${fails}項。`);
  process.exit(fails ? 1 : 0);
})().catch(e => { console.error("測試程式出錯：", e); process.exit(2); });

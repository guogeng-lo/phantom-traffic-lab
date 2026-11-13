/* 節點7：簡報被嵌在別的網頁裡（沙盒iframe、about:srcdoc）時也要能用。
 * 起因：使用者在Claude的預覽面板打開docs/index.html，按「下一頁」時history.pushState丟出SecurityError，整個換頁失效。
 * 用法：node tests/e2e_embedded.js
 * 三種情況都在<iframe sandbox="allow-scripts" srcdoc=...>裡跑（跟預覽面板一樣：沒有allow-same-origin，網址是about:srcdoc）：
 *   A. 照原樣
 *   B. Worker一建立就丟錯（模擬瀏覽器不准）
 *   C. Worker建立成功、但載入失敗（onerror），已經送出去的計算要改在主執行緒重算
 * 每種情況都檢查：沒有JavaScript錯誤、下一頁／上一頁／鍵盤／目錄換頁、第2頁點車、第6頁單一車數算得出來、第10頁「答案在」連結。 */
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

const HTML = fs.readFileSync(path.join(__dirname, "..", "docs", "index.html"), "utf8");
const INJECT = {
  A: "",
  B: "<script>window.Worker=function(){throw new Error(\"測試：不准建立Worker\")};</script>",
  C: "<script>window.Worker=class{constructor(){setTimeout(()=>{if(this.onerror)this.onerror(new Event(\"error\"));},50);}postMessage(){}terminate(){}};</script>"
};
let fails = 0;
const say = (ok, m, got) => { if (!ok) fails++; console.log(`${ok ? "通過" : "沒通過"}｜${m}${got !== undefined ? `｜實際：${got}` : ""}`); };

(async () => {
  const browser = await chromium.launch();
  for (const [k, inj] of Object.entries(INJECT)) {
    console.log(`\n## 情況${k}${k === "A" ? "：照原樣" : k === "B" ? "：Worker一建立就丟錯" : "：Worker載入失敗"}`);
    const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    await page.route(/^https?:\/\//, r => r.abort());   // 外部字型連不到，條件固定
    const errs = [];
    page.on("pageerror", e => errs.push(String(e)));
    page.on("console", m => { if (m.type() === "error" && !/ERR_FAILED|net::/.test(m.text())) errs.push(m.text()); });
    await page.setContent('<iframe id="f" sandbox="allow-scripts" style="width:1240px;height:860px;border:0"></iframe>');
    await page.evaluate(h => { document.getElementById("f").srcdoc = h; }, HTML.replace("<head>", "<head>" + inj));
    await page.waitForFunction(() => document.getElementById("f").contentWindow !== null);
    let f = null;
    for (let i = 0; i < 50 && !f; i++) { f = page.frames().find(x => x.url() === "about:srcdoc"); if (!f) await page.waitForTimeout(100); }
    await f.waitForSelector("#p1:not([hidden])");
    const cur = async () => (await f.locator("section.page:not([hidden])").getAttribute("id"));
    say(f.url() === "about:srcdoc", "在about:srcdoc裡（沙盒、沒有同源）", f.url());
    await f.getByRole("button", { name: "下一頁" }).click();
    say(await cur() === "p2", "「下一頁」換到第2頁", await cur());
    await f.getByRole("button", { name: "上一頁" }).click();
    say(await cur() === "p1", "「上一頁」回到第1頁", await cur());
    await f.locator("body").press("ArrowRight");
    say(await cur() === "p2", "鍵盤→換頁", await cur());
    await f.locator(".toc summary").click(); await f.locator("#toc a").nth(6).click();
    say(await cur() === "p7", "目錄連結換到第7頁（不會把iframe導到別的網址）", await cur());
    say(f.url() === "about:srcdoc", "點完頁內連結之後iframe還在原地", f.url());
    await f.locator(".toc summary").click(); await f.locator("#toc a").nth(1).click();
    await f.locator("#p2 canvas.ring").focus(); await f.locator("#p2 canvas.ring").press("Enter");
    say((await f.locator("#p2 .say").first().textContent()).includes("你剛剛讓這台車慢了一下"), "第2頁點車");
    await f.locator(".toc summary").click(); await f.locator("#toc a").nth(5).click();
    await f.getByRole("button", { name: "中間那段" }).click();
    await f.locator("#p6n").fill("10");
    await f.getByRole("button", { name: "跑這個車數" }).click();
    const done = await f.waitForFunction(() => document.querySelector("#p6 .placard .say").textContent.startsWith("10台："), null, { timeout: 60000 }).then(() => true, () => false);
    const mode = await f.evaluate(() => window.__deck.engine.mode);
    say(done, `第6頁單一車數算得出來（計算在${mode === "worker" ? "Web Worker" : "主執行緒"}）`, await f.locator("#p6 .placard .say").textContent());
    if (k !== "A") say(mode === "main", "Worker不能用時改在主執行緒算", mode);
    await f.locator(".toc summary").click(); await f.locator("#toc a").nth(9).click();
    await f.locator('.quiz[data-quiz="1"] .opt').first().click();
    await f.locator('.quiz[data-quiz="1"] .back-links a').first().click();
    say(await cur() === "p1", "第10頁「答案在」連結回到第1頁", await cur());
    say(errs.length === 0, "沒有JavaScript錯誤", errs.join(" / ") || "0個");
    await page.close();
  }
  await browser.close();
  console.log(`\n沒通過${fails}項。`);
  process.exit(fails ? 1 : 0);
})().catch(e => { console.error("測試程式出錯：", e); process.exit(2); });

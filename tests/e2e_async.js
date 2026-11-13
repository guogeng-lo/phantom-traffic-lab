/* 節點7第3輪：非同步計算的回歸測試（N7-01、N7-02、N7-03、N7-04、N7-17）。
 * 用法：node tests/e2e_async.js
 * 標準在正式執行前寫在這裡：
 * 第6頁「全部跑一次」，在三種情況下跑（A：Worker正常；B：Worker一建立就丟錯；C：Worker建立後載入失敗）：
 *   1. Worker不能用（B、C）時，按下去先說明「可能卡頓」並讓讀者選要不要跑；選「先不要」就什麼都不算。
 *   2. 按「停止」之後，2秒內進度不再增加；已經算完的格子保留。
 *   3. 跑到一半離開第6頁，進度不再增加；回來之後可以「繼續」，最後58格都算完。
 *   4. 每一個車數只算一次（繼續的時候不重算已經算完的）。
 *   5. 最後58格跟逐頁稿一致（16～20、22～39放大；21無法判定；3只比差距；其他不放大）。
 *   6. 沒有JavaScript錯誤。
 *   另外記錄（不當標準，只報告）：Worker不能用時，主執行緒最長停頓多久。這是這個測試環境的數字，不代表所有手機。
 * 第8頁（情況A）：
 *   7. 「不換」的對照（R0）整頁只算一次，不管先按哪個、連按幾次。
 *   8. 同一個目標速度只算一次（連按「跑這個值」、來回切換都不重算）。
 *   9. 快速切換0.9→1.2→0.9→1.0時，最後畫面顯示的是1.0倍的結果（舊的結果不會蓋掉）。
 *  10. 第三題一開始就看得到兩個待辦（先跑1.0倍、再跑一個大於1.0倍）；只跑1.2倍時揭曉鈕不出現、第二項打勾；兩項都做了才出現。
 *  11. 快轉／播放動畫是兩個互斥的按鈕，aria-pressed跟畫面一致。 */
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

const HTML = fs.readFileSync(path.join(__dirname, "..", "docs", "index.html"), "utf8");
const SPY = "<script>window.__lt=[];try{new PerformanceObserver(l=>{for(const e of l.getEntries())window.__lt.push(Math.round(e.duration));}).observe({type:\"longtask\",buffered:true});}catch(e){}</script>";
const INJECT = {
  A: SPY,
  B: SPY + "<script>window.Worker=function(){throw new Error(\"測試：不准建立Worker\")};</script>",
  C: SPY + "<script>window.Worker=class{constructor(){setTimeout(()=>{if(this.onerror)this.onerror(new Event(\"error\"));},50);}postMessage(){}terminate(){}};</script>"
};
const SHORT = { timeout: 3000 };
let fails = 0;
const say = (ok, m, got) => { if (!ok) fails++; console.log(`${ok ? "通過" : "沒通過"}｜${m}${got !== undefined ? `｜實際：${got}` : ""}`); };
const want = k => k === 3 ? "c-gap" : k === 21 ? "c-na" : (k >= 16 && k <= 39 ? "c-up" : "c-down");

async function open(browser, inj) {
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  await page.route(/^https?:\/\//, r => r.abort());
  const errs = [];
  page.on("pageerror", e => errs.push(String(e)));
  page.on("console", m => { if (m.type() === "error" && !/ERR_FAILED|net::/.test(m.text())) errs.push(m.text()); });
  await page.setContent('<iframe id="f" sandbox="allow-scripts" style="width:1240px;height:860px;border:0"></iframe>');
  await page.evaluate(h => { document.getElementById("f").srcdoc = h; }, HTML.replace("<head>", "<head>" + inj));
  let f = null;
  for (let i = 0; i < 50 && !f; i++) { f = page.frames().find(x => x.url() === "about:srcdoc"); if (!f) await page.waitForTimeout(100); }
  await f.waitForSelector("#p1:not([hidden])");
  // 記下每一次送出的計算（只是旁聽，原封不動交給原本的函式）
  await f.evaluate(() => { const e = window.__deck.engine, r = e.run.bind(e); window.__calls = []; e.run = (m, ...rest) => { window.__calls.push(m.cmd + (m.N != null ? ":" + m.N : "") + (m.kind ? ":" + m.kind : "") + (m.mult != null ? ":" + m.mult : "")); return r(m, ...rest); }; });
  return { page, f, errs };
}
const tryClick = async (loc) => { try { await loc.click(SHORT); return true; } catch (e) { return false; } };
const done = f => f.evaluate(() => document.querySelectorAll('#p6 .strip td[data-n]:not(.c-wait)').length);

async function sweepCase(browser, k) {
  console.log(`\n## 第6頁，情況${k}${k === "A" ? "：Worker正常" : k === "B" ? "：Worker一建立就丟錯" : "：Worker載入失敗"}`);
  const { page, f, errs } = await open(browser, INJECT[k]);
  await f.evaluate(() => window.__deck.go(6));
  await f.getByRole("button", { name: "中間那段" }).click();
  await page.waitForTimeout(300);
  const bAll = f.locator("#p6").getByRole("button", { name: /全部跑一次|繼續跑/ });
  await bAll.click();
  if (k !== "A") {
    const warn = f.locator("#p6").getByText(/卡頓/);
    say(await warn.isVisible().catch(() => false), "Worker不能用：按下去先說明可能卡頓");
    const no = await tryClick(f.locator("#p6").getByRole("button", { name: "先不要" }));
    await page.waitForTimeout(800);
    say(no && await done(f) === 0, "選「先不要」就不算", `${await done(f)}格`);
    await bAll.click().catch(() => {});
    await tryClick(f.locator("#p6").getByRole("button", { name: "照樣全部跑" }));
  }
  await f.waitForFunction(() => document.querySelectorAll('#p6 .strip td[data-n]:not(.c-wait)').length >= 5, null, { timeout: 60000 }).catch(() => {});
  const stopped = await tryClick(f.locator("#p6").getByRole("button", { name: "停止" }));
  await page.waitForTimeout(2000); const s1 = await done(f); await page.waitForTimeout(3000); const s2 = await done(f);
  say(stopped && s1 === s2 && s1 >= 5, "按「停止」之後不再增加，已算完的保留", `停止後2秒${s1}格、再3秒${s2}格`);
  // 繼續，跑到一半離開
  await tryClick(f.locator("#p6").getByRole("button", { name: /繼續跑/ }));
  await page.waitForTimeout(1500);
  await f.evaluate(() => window.__deck.go(7));
  await page.waitForTimeout(2000); const l1 = await done(f); await page.waitForTimeout(3000); const l2 = await done(f);
  say(l1 === l2, "離開第6頁之後不再增加", `離開後2秒${l1}格、再3秒${l2}格`);
  await f.evaluate(() => window.__deck.go(6));
  const resumed = await tryClick(f.locator("#p6").getByRole("button", { name: /繼續跑/ }));
  if (k !== "A") await tryClick(f.locator("#p6").getByRole("button", { name: "照樣全部跑" }));
  const finished = await f.waitForFunction(() => document.querySelector("#p6 .progress").textContent.includes("算完了"), null, { timeout: 300000 }).then(() => true, () => false);
  say(resumed && finished, "回來之後可以繼續，最後算完");
  const calls = await f.evaluate(() => window.__calls.filter(c => c.startsWith("verdict:")));
  const per = {}; calls.forEach(c => { per[c] = (per[c] || 0) + 1; });
  const dup = Object.entries(per).filter(([, n]) => n > 1).map(([c, n]) => `${c.slice(8)}台×${n}`);
  say(Object.keys(per).length === 58 && dup.length === 0, "每個車數只算一次（繼續時不重算）", `${Object.keys(per).length}個車數${dup.length ? "；重算：" + dup.join("、") : ""}`);
  const cells = await f.evaluate(() => Object.fromEntries([...document.querySelectorAll("#p6 .strip td[data-n]")].map(td => [td.dataset.n, td.className.split(" ").find(c => c.startsWith("c-"))])));
  const bad = Object.keys(cells).filter(n => cells[n] !== want(+n));
  say(Object.keys(cells).length === 58 && bad.length === 0, "58格跟逐頁稿一致", bad.length ? bad.map(n => `${n}:${cells[n]}`).join(",") : "58格都一致");
  const lt = (await f.evaluate(() => window.__lt.slice())).sort((a, b) => b - a);
  console.log(`  （只報告，不當標準）引擎：${await f.evaluate(() => window.__deck.engine.mode)}；主執行緒停頓超過50 ms的${lt.length}次，最長${lt.slice(0, 3).join("、") || "0"} ms；超過500 ms的${lt.filter(x => x > 500).length}次。這是這個測試環境的數字，不代表所有手機。`);
  say(errs.length === 0, "沒有JavaScript錯誤", errs.join(" / ") || "0個");
  await page.close();
}

async function p8Case(browser) {
  console.log("\n## 第8頁（Worker正常）");
  const { page, f, errs } = await open(browser, INJECT.A);
  await f.evaluate(() => window.__deck.go(8));
  const s8 = f.locator("#p8"), q3 = s8.locator(".sim-box").nth(1);
  // 11. 快轉／播放動畫
  const ff = s8.getByRole("button", { name: "快轉", exact: true }).first(), play = s8.getByRole("button", { name: "播放動畫", exact: true }).first();
  const pressed = async () => [await ff.getAttribute("aria-pressed", SHORT).catch(() => null), await play.getAttribute("aria-pressed", SHORT).catch(() => null)].join("/");
  const p0 = await pressed(); await tryClick(play); const p1 = await pressed(); await tryClick(ff); const p2 = await pressed();
  say(p0 === "true/false" && p1 === "false/true" && p2 === "true/false", "快轉／播放動畫是兩個互斥按鈕，狀態跟aria-pressed一致", `${p0} → ${p1} → ${p2}`);
  // 7、8. 先按規則，馬上答第三題、連按跑這個值
  await s8.getByRole("button", { name: "固定目標速度", exact: true }).click();
  await s8.getByRole("button", { name: "不一定，可能更大" }).click();
  const run = s8.getByRole("button", { name: "跑這個值" });
  await tryClick(run); await tryClick(run); await tryClick(run);
  // 10. 待辦
  const todo = await q3.textContent();
  say(/先跑1\.0倍/.test(todo) && /大於1\.0倍/.test(todo), "第三題一開始就看得到兩個待辦", todo.match(/[①②][^①②]{0,30}/g)?.join(" ") || "找不到");
  await page.waitForTimeout(6000);
  // 只跑1.2倍的情況另開一個頁面測，這裡先測快速切換
  const slider = s8.locator("#p8u");
  for (const v of ["0", "4", "0", "1"]) { await slider.fill(v); await slider.dispatchEvent("change"); await page.waitForTimeout(80); }
  await f.waitForFunction(() => { const s = document.querySelectorAll("#p8 .sim-box")[1].querySelector(".say"); return s && s.textContent.includes("跑完了") && s.textContent.startsWith("1"); }, null, { timeout: 60000 }).catch(() => {});
  await page.waitForTimeout(6000);   // 等可能還在路上的舊結果回來，看它會不會蓋掉
  const shown = await q3.locator("dl.results").textContent().catch(() => ""), msg = await q3.locator(".say").textContent().catch(() => "");
  say(msg.startsWith("1.0倍") && shown.includes("42%"), "快速切換後，畫面是最後選的1.0倍的結果（舊結果沒有蓋掉）", `${msg}｜${shown.slice(0, 30)}`);
  const calls = await f.evaluate(() => window.__calls);
  const r0 = calls.filter(c => c === "smooth:R0").length, per = {};
  calls.filter(c => c.startsWith("smooth:R3")).forEach(c => { per[c] = (per[c] || 0) + 1; });
  say(r0 === 1, "「不換」的對照只算一次", `${r0}次`);
  const dup = Object.entries(per).filter(([, n]) => n > 1).map(([c, n]) => `${c.split(":")[2]}倍×${n}`);
  say(dup.length === 0, "同一個目標速度只算一次", Object.entries(per).map(([c, n]) => `${c.split(":")[2]}倍×${n}`).join("、"));
  say(errs.length === 0, "沒有JavaScript錯誤", errs.join(" / ") || "0個");
  await page.close();
  // 10（續）. 只跑1.2倍
  const o = await open(browser, INJECT.A);
  await o.f.evaluate(() => window.__deck.go(8));
  await o.f.locator("#p8").getByRole("button", { name: "不一定，可能更大" }).click();
  await o.f.locator("#p8u").fill("4"); await o.f.locator("#p8u").dispatchEvent("change");
  await o.f.waitForFunction(() => document.querySelectorAll("#p8 .sim-box")[1].querySelector(".say").textContent.includes("跑完了"), null, { timeout: 60000 }).catch(() => {});
  const rev1 = await o.f.locator("#p8").getByRole("button", { name: "揭曉", exact: true }).isVisible();
  const ticks = await o.f.evaluate(() => [...document.querySelectorAll("#p8 .todo li")].map(li => li.classList.contains("done") ? "✓" : "□").join(""));
  say(!rev1 && ticks === "□✓", "只跑1.2倍：揭曉鈕不出現，只有第二項打勾", `揭曉鈕${rev1 ? "出現" : "沒出現"}，待辦${ticks || "找不到"}`);
  await o.f.locator("#p8u").fill("1"); await o.f.locator("#p8u").dispatchEvent("change");
  await o.f.waitForFunction(() => document.querySelectorAll("#p8 .sim-box")[1].querySelector(".say").textContent.startsWith("1.0倍：跑完了"), null, { timeout: 60000 }).catch(() => {});
  const rev2 = await o.f.locator("#p8").getByRole("button", { name: "揭曉", exact: true }).isVisible();
  say(rev2, "兩項都做了，揭曉鈕出現");
  say(o.errs.length === 0, "沒有JavaScript錯誤（只跑1.2倍那頁）", o.errs.join(" / ") || "0個");
  await o.page.close();
}

(async () => {
  const browser = await chromium.launch();
  for (const k of ["A", "B", "C"]) await sweepCase(browser, k);
  await p8Case(browser);
  await browser.close();
  console.log(`\n沒通過${fails}項。`);
  process.exit(fails ? 1 : 0);
})().catch(e => { console.error("測試程式出錯：", e); process.exit(2); });

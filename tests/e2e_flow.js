/* 節點7：用Playwright在Chromium實際操作建好的簡報（docs/index.html）。
 * 用法：node tests/e2e_flow.js [--mobile]
 * 每一項印出「通過／沒通過」和實際讀到的值；有任何一項沒通過，結束代碼是1。
 * 這裡比的數字（例如第5頁a=2.2「擾動縮到0.01以下了」、第8頁「42%」）是逐頁稿和證據卡寫的結果，
 * 用來確認頁面在瀏覽器裡即時算出來的，跟審查過的文字一致；不是另外訂的標準。 */
const { chromium } = require("playwright");
const { serve, blockExternal } = require("./site_server");

const MOBILE = process.argv.includes("--mobile");
const results = [];
function check(name, ok, got) { results.push(ok); console.log(`${ok ? "通過" : "沒通過"}｜${name}${got !== undefined ? `｜實際：${got}` : ""}`); }

(async () => {
  const { srv, url } = await serve();
  const browser = await chromium.launch();
  const ctx = await browser.newContext(MOBILE ? { viewport: { width: 375, height: 812 }, isMobile: true, hasTouch: true, deviceScaleFactor: 1 } : { viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();
  await blockExternal(page);
  const errors = [];
  page.on("pageerror", e => { errors.push(String(e)); console.log("  （頁面錯誤）" + String(e)); });
  page.on("console", m => { if (m.type() === "error" && !/ERR_FAILED|net::/.test(m.text())) errors.push(m.text()); });
  const sec = n => page.locator(`#p${n}`);
  const visibleMain = async (n, i) => sec(n).locator(`.main > [data-i="${i}"]`).isVisible();
  const tap = async (loc) => MOBILE ? loc.tap() : loc.click();
  console.log(`# 節點7互動流程測試（${MOBILE ? "手機375×812、觸控" : "桌機1280×900、滑鼠"}）`);

  // ---- 第1頁 ----
  await page.goto(url + "#p1");
  check("第1頁：一開始第二段文字還沒出現", !(await visibleMain(1, 2)));
  await tap(sec(1).getByRole("button", { name: "快轉到有車幾乎停住" }));
  check("第1頁：有車幾乎停住後第二段出現", await visibleMain(1, 2));
  check("第1頁：停在模型時間92.0（ours-model-offset-jam，每0.5檢查一次）", (await sec(1).locator(".clock b").textContent()) === "92.0", await sec(1).locator(".clock b").textContent());
  await tap(sec(1).getByRole("button", { name: "重播" }));
  check("第1頁：重播從t=0重跑", parseFloat(await sec(1).locator(".clock b").textContent()) < 5, await sec(1).locator(".clock b").textContent());

  // ---- 換頁 ----
  await tap(page.getByRole("button", { name: "下一頁" }));
  check("換頁：「下一頁」到第2頁", await page.evaluate(() => window.__deck.page) === 2);
  check("換頁：網址變成#p2", page.url().endsWith("#p2"));

  // ---- 第2頁：點車 ----
  const ring2 = sec(2).locator("canvas.ring");
  const box = await ring2.boundingBox();
  if (MOBILE) await page.touchscreen.tap(box.x + box.width / 2, box.y + box.width / 2 - box.width * 0.41);
  else await page.mouse.click(box.x + box.width / 2, box.y + box.width / 2 - box.width * 0.41);
  const ck = await page.evaluate(() => window.__deck.shared.click);
  check("第2頁：點環道上的車會煞車", !!ck, JSON.stringify(ck));
  check("第2頁：顯示「你剛剛讓這台車慢了一下」", (await sec(2).locator(".say").first().textContent()).includes("你剛剛讓這台車慢了一下"));
  await tap(sec(2).getByRole("button", { name: "快轉到有車幾乎停住" }));
  const t2 = parseFloat(await sec(2).locator(".clock b").textContent());
  check("第2頁：點完89.3模型時間形成塞車（ours-model-click-brake；畫面時鐘只到小數一位，容許0.05的進位差）", Math.abs(t2 - ck.tc - 89.3) < 0.051, (t2 - ck.tc).toFixed(2));
  check("第2頁：第二段文字出現", await visibleMain(2, 2));
  await ring2.scrollIntoViewIfNeeded(); const box2 = await ring2.boundingBox();   // 按過快轉，頁面可能捲動了，重新量位置
  if (MOBILE) await page.touchscreen.tap(box2.x + box2.width / 2, box2.y + box2.width / 2 + box2.width * 0.41);
  else await page.mouse.click(box2.x + box2.width / 2, box2.y + box2.width / 2 + box2.width * 0.41);
  check("第2頁：點過之後不能再點別台", (await sec(2).locator(".say").first().textContent()).includes("已經點過一台了"));
  await tap(sec(2).getByRole("button", { name: "重來" }));
  check("第2頁：重來之後回到均勻車流", parseFloat(await sec(2).locator(".clock b").textContent()) < 5);
  await ring2.focus(); await page.keyboard.press("ArrowRight"); await page.keyboard.press("ArrowRight"); await page.keyboard.press("Enter");
  const ck2 = await page.evaluate(() => window.__deck.shared.click);
  check("第2頁：鍵盤（方向鍵＋Enter）可以點車", ck2 && ck2.car === 2, JSON.stringify(ck2));

  // ---- 第3頁：時空圖 ----
  await page.evaluate(() => window.__deck.go(3));
  check("第3頁：用的是第2頁的那一次點擊", (await sec(3).locator(".placard .fine").first().textContent()).includes("第2台車"));
  const bAll = sec(3).getByRole("button", { name: "疊上其他車" });
  await page.waitForFunction(() => !document.querySelector("#p3 .placard .btns button").disabled, null, { timeout: 30000 });
  check("第3頁：一台車穿過塞車後才能疊上其他車", await bAll.isEnabled());
  check("第3頁：還沒選答案前，第三段和揭曉的讀圖小圖都還沒出現", !(await visibleMain(3, 3)) && (await sec(3).locator(".guide figure").nth(2).textContent()).includes("帶子往哪邊斜"));
  await tap(bAll);
  await tap(sec(3).getByRole("button", { name: "往左，跟車子反方向" }));
  check("第3頁：選了之後第三段出現", await visibleMain(3, 3));
  check("第3頁：程式量到塞車團往後移（讀圖小圖改成往左下）", (await sec(3).locator(".guide figure").nth(2).textContent()).includes("往左下"), await sec(3).locator(".guide figure").nth(2).textContent());
  check("第3頁：知識和進階層在揭曉後出現", await sec(3).locator('[data-layer="know"]').isVisible());

  // ---- 第4頁 ----
  await page.evaluate(() => window.__deck.go(4));
  check("第4頁：按開始前第二段沒出現", !(await visibleMain(4, 2)));
  await tap(sec(4).getByRole("button", { name: "開始" }));
  await page.waitForFunction(() => document.querySelector("#p4 .say").textContent.includes("畫完了"), null, { timeout: 30000 });
  check("第4頁：畫完後第二段出現", await visibleMain(4, 2));
  // 畫布上真的有線：數兩張圖裡有顏色（不是白、灰）的像素
  const ink = await page.evaluate(() => [...document.querySelectorAll("#p4 canvas.chart")].map(cv => { const c = cv.getContext("2d"), d = c.getImageData(0, 0, cv.width, cv.height).data; let n = 0;
    for (let i = 0; i < d.length; i += 4) { const mx = Math.max(d[i], d[i + 1], d[i + 2]), mn = Math.min(d[i], d[i + 1], d[i + 2]); if (mx - mn > 60) n++; } return n; }));   // 只算彩色的線（藍、橘、紫），黑色的軸不算
  check("第4頁：兩張圖都畫出彩色的線", ink.every(n => n > 500), ink.join("、") + "個彩色像素");

  // ---- 第5頁：先猜、滑桿 ----
  await page.evaluate(() => window.__deck.go(5));
  check("第5頁：沒選之前滑桿鎖著", !(await sec(5).locator("#p5a").isVisible()));
  await tap(sec(5).getByRole("button", { name: "看調多快" }));
  check("第5頁：選了之後滑桿打開", await sec(5).locator("#p5a").isVisible());
  const ring5 = sec(5).locator("canvas.ring");
  async function runA(idx, expect) {
    await sec(5).locator("#p5a").fill(String(idx));
    await ring5.focus(); await page.keyboard.press("Enter");
    const ff = sec(5).getByRole("button", { name: "快轉", exact: true });
    if (await ff.isEnabled()) await ff.click().catch(() => {});
    await page.waitForFunction(() => /：/.test(document.querySelector("#p5 .placard .say").textContent) && !document.querySelector("#p5 .placard .say").textContent.includes("中"), null, { timeout: 60000 });
    const got = await sec(5).locator(".placard .say").textContent();
    check(`第5頁：${expect[0]}`, got.includes(expect[1]), got);
  }
  await runA(0, ["a=1.0 塞住了", "塞住了"]);
  check("第5頁：只跑一個a時還沒有揭曉按鈕", !(await sec(5).getByRole("button", { name: "揭曉", exact: true }).isVisible()));
  await runA(3, ["a=2.2 點完300內擾動縮到0.01以下", "擾動縮到0.01以下了"]);
  await runA(1, ["a=1.90 擾動慢慢變大、沒塞住", "還沒塞住，擾動在慢慢變大"]);
  await runA(2, ["a=1.98 擾動慢慢變小", "擾動在慢慢變小"]);
  await runA(4, ["a=2.5 擾動縮到0.01以下", "擾動縮到0.01以下了"]);
  await runA(5, ["a=3.0 擾動縮到0.01以下", "擾動縮到0.01以下了"]);
  await tap(sec(5).getByRole("button", { name: "揭曉", exact: true }));
  check("第5頁：跑過兩個以上的a、按揭曉後第二段出現", await visibleMain(5, 2));

  // ---- 第6頁 ----
  await page.evaluate(() => window.__deck.go(6));
  await tap(sec(6).getByRole("button", { name: "中間那段" }));
  await sec(6).locator("#p6n").fill("21");
  check("第6頁：車數21時顯示平均車距和均勻車流的速度", (await sec(6).locator(".placard .fine").first().textContent()).includes("44÷21"), await sec(6).locator(".placard .fine").first().textContent());
  await tap(sec(6).getByRole("button", { name: "跑這個車數" }));
  await page.waitForFunction(() => document.querySelector("#p6 .placard .say").textContent.startsWith("21台："), null, { timeout: 60000 });
  check("第6頁：單一車數的小圖跑完", true, await sec(6).locator(".placard .say").textContent());
  const t0 = Date.now();
  await tap(sec(6).getByRole("button", { name: "把3到60台全部跑一次" }));
  await page.waitForFunction(() => document.querySelector("#p6 .progress").textContent.includes("算完了"), null, { timeout: 300000 });
  const cells = await page.evaluate(() => { const out = {}; document.querySelectorAll("#p6 .strip table").forEach(tb => { const ks = [...tb.querySelectorAll("thead th")].slice(1).map(th => +th.textContent); const sim = [...tb.querySelectorAll("tbody tr:nth-child(2) td")]; const th = [...tb.querySelectorAll("tbody tr:nth-child(1) td")]; ks.forEach((k, i) => { out[k] = [th[i].className, sim[i].className]; }); }); return out; });
  console.log(`  （全部跑一次在這個瀏覽器花了${((Date.now() - t0) / 1000).toFixed(0)}秒；${await sec(6).locator(".progress").textContent()}）`);
  const want = k => k === 3 ? "c-gap" : k === 21 ? "c-na" : (k >= 16 && k <= 39 ? "c-up" : "c-down");
  const bad = Object.keys(cells).filter(k => cells[k][1] !== want(+k));
  check("第6頁：模擬列跟逐頁稿一致（16～20、22～39放大；21無法判定；3只比差距；其他不放大）", bad.length === 0 && Object.keys(cells).length === 58, bad.length ? bad.map(k => `${k}:${cells[k][1]}`).join(",") : "58格都一致");
  const badT = Object.keys(cells).filter(k => cells[k][0] !== (+k >= 16 && +k <= 39 ? "c-up" : "c-down"));
  check("第6頁：公式列是16到39台放大", badT.length === 0, badT.join(",") || "58格都一致");
  check("第6頁：算完後第二段出現", await visibleMain(6, 2));

  // ---- 第8頁 ----
  await page.evaluate(() => window.__deck.go(8));
  check("第8頁：長條圖有9條", (await sec(8).locator(".bar-row").count()) === 9);
  await tap(sec(8).getByRole("button", { name: "固定目標速度" }));
  await page.waitForFunction(() => document.querySelector("#p8 .sim-box .say").textContent.includes("跑完了"), null, { timeout: 60000 });
  const r3 = await sec(8).locator(".sim-box").first().locator("dl.results").textContent();
  check("第8頁：固定目標速度 42%、0.966→0.887、最小車距0.326、沒有撞車", ["42%", "0.966", "0.887", "0.326", "沒有撞車"].every(s => r3.includes(s)), r3);
  await tap(sec(8).getByRole("button", { name: "照自己過去的平均速度" }));
  await page.waitForFunction(() => document.querySelector("#p8 .sim-box .say").textContent.includes("平均速度」跑完了"), null, { timeout: 60000 });
  const r1 = await sec(8).locator(".sim-box").first().locator("dl.results").textContent();
  check("第8頁：照自己過去的平均速度 平均車速0.763、最小車距0.325", ["0.763", "0.325", "沒有撞車"].every(s => r1.includes(s)), r1);
  check("第8頁：第三題沒選之前滑桿鎖著", !(await sec(8).locator("#p8u").isVisible()));
  await tap(sec(8).getByRole("button", { name: "不一定，可能更大" }));
  const q3 = sec(8).locator(".sim-box").nth(1);
  const runU = async (i, pct) => { await sec(8).locator("#p8u").fill(String(i)); await sec(8).locator("#p8u").dispatchEvent("change");
    await page.waitForFunction(() => document.querySelectorAll("#p8 .sim-box")[1].querySelector(".say").textContent.includes("跑完了"), null, { timeout: 60000 });
    const got = await q3.locator("dl.results").textContent(); check(`第8頁第三題：${["0.9", "1.0", "1.05", "1.1", "1.2"][i]}倍 → ${pct}`, got.includes(pct), got); };
  await runU(1, "42%"); await runU(2, "49%"); await runU(3, "55%"); await runU(4, "63%");
  await runU(0, "0.868");
  await tap(sec(8).getByRole("button", { name: "揭曉", exact: true }));
  check("第8頁：揭曉後出現第三題的答案", await visibleMain(8, 9));

  // ---- 第9頁 ----
  await page.evaluate(() => window.__deck.go(9));
  const c9 = sec(9).locator("details.card9");
  check("第9頁：7張卡片，預設收起", (await c9.count()) === 7 && (await sec(9).locator("details.card9[open]").count()) === 0);
  await tap(c9.first().locator("summary"));
  check("第9頁：點了卡片會展開（不用懸停）", (await sec(9).locator("details.card9[open]").count()) === 1);

  // ---- 第10頁 ----
  await page.evaluate(() => window.__deck.go(10));
  check("第10頁：一次只顯示一題", (await sec(10).locator(".quiz:visible").count()) === 1);
  for (let q = 1; q <= 3; q++) {
    const quiz = sec(10).locator(`.quiz[data-quiz="${q}"]`);
    await tap(quiz.locator('.opt[data-right="0"]').first());
    check(`第10頁第${q}題：選錯顯示「再想想」和解釋`, (await quiz.locator(".verdict").textContent()) === "再想想" && await quiz.locator(".why").isVisible());
    await tap(quiz.locator('.opt[data-right="1"]'));
    check(`第10頁第${q}題：選對顯示「對」`, (await quiz.locator(".verdict").textContent()) === "對");
    check(`第10頁第${q}題：有「答案在第幾頁」的連結`, (await quiz.locator(".back-links a").count()) >= 1);
    await tap(quiz.getByRole("button", { name: q < 3 ? "下一題" : "看延伸閱讀" }));
  }
  check("第10頁：三題做完出現延伸閱讀", await sec(10).locator(".further").isVisible());
  await sec(10).locator('.quiz[data-quiz="1"] .back-links a').first().click();
  check("第10頁：答案連結回到第1頁", await page.evaluate(() => window.__deck.page) === 1);
  const stored = await page.evaluate(() => { try { return localStorage.length + sessionStorage.length; } catch (e) { return 0; } });
  check("沒有用localStorage或sessionStorage存資料", stored === 0, stored);

  // ---- 鍵盤換頁、返回鍵、直接開某頁 ----
  await page.locator("body").press("ArrowRight");
  check("鍵盤：→換到下一頁", await page.evaluate(() => window.__deck.page) === 2);
  await page.goBack();
  check("瀏覽器返回鍵回到上一頁", await page.evaluate(() => window.__deck.page) === 1, await page.evaluate(() => window.__deck.page));
  const p2 = await ctx.newPage(); await blockExternal(p2); await p2.goto(url + "#p7");
  check("直接開#p7就在第7頁", await p2.evaluate(() => window.__deck.page) === 7);
  check("第7頁：三個實驗各有論文連結", (await p2.locator("#p7 a.paper").count()) === 3);
  await p2.close();

  // ---- 互動做完之後（解鎖、圖表和結果條都出現了）再看一次每頁有沒有超出畫面寬度 ----
  const wide = [];
  for (let i = 1; i <= 10; i++) { await page.evaluate(i => window.__deck.go(i), i); await page.waitForTimeout(150);
    const sw = await page.evaluate(() => document.documentElement.scrollWidth); if (sw > (MOBILE ? 375 : 1280)) wide.push(`第${i}頁${sw}px`);
    // 文字溢出：按鈕、選項、表格格子、結果列裡的字超出自己的框
    const spill = await page.evaluate(i => [...document.querySelectorAll(`#p${i} button, #p${i} td, #p${i} th, #p${i} dd, #p${i} dt, #p${i} summary, #p${i} output, .pager button`)]
      .filter(e => e.checkVisibility() && e.scrollWidth > e.clientWidth + 1).map(e => `${e.tagName.toLowerCase()}「${e.textContent.trim().slice(0, 10)}」`), i);
    if (spill.length) wide.push(`第${i}頁文字溢出：${spill.slice(0, 4).join("、")}`); }
  check("互動之後每一頁都沒有超出畫面寬度、沒有文字溢出", wide.length === 0, wide.join("、") || "10頁都沒有");
  check("頁面沒有JavaScript錯誤", errors.length === 0, errors.join(" / ") || "0個");
  await browser.close(); srv.close();
  const nf = results.filter(x => !x).length;
  console.log(`\n共${results.length}項，沒通過${nf}項。`);
  process.exit(nf ? 1 : 0);
})().catch(e => { console.error("測試程式出錯：", e); process.exit(2); });

/* A. 動畫CPU診斷。用法：node cpu.js <組別> <輸出json>
 *  A1：第1、2、5頁，每頁5次，順序固定為「第1次：p1→p2→p5，第2次：p1→p2→p5……」。每一次都新開瀏覽器：
 *      先量「冷」（載入後0.5秒開始操作、0.3秒後量6秒），再重新整理、操作、先跑6秒不量（預熱），再量「熱」6秒。
 *  A2：緊接在Lighthouse 5次之後，第1、2、5頁各2次，只量「冷」。 */
const { chromium } = require("playwright");
const C = require("./common");
const [group, out] = process.argv.slice(2);
(async () => {
  const { srv, url } = await C.serve();
  const reps = group === "A1" ? 5 : 2, rows = [], envs = [C.env(group + "開始")];
  for (let r = 1; r <= reps; r++) for (const n of [1, 2, 5]) {
    const browser = await chromium.launch(), ctx = await browser.newContext(C.MOBILE), page = await ctx.newPage(); await C.blockExternal(page);
    await page.goto(url + `#p${n}`); await page.waitForTimeout(500); await C.setup(page, n); await page.waitForTimeout(300);
    const cold = await C.measure(ctx, page, n); rows.push(Object.assign({ group, rep: r, page: n, kind: "冷", loadavg: C.env("").loadavg }, cold));
    console.log(`${group} 第${r}次 p${n} 冷：忙碌${cold.busy}% JS${cold.js}% 模型時間+${cold.modelAdvance}（${cold.seconds}秒）`);
    if (group === "A1") {
      await page.reload(); await page.waitForTimeout(500); await C.setup(page, n); await page.waitForTimeout(6000);
      const hot = await C.measure(ctx, page, n); rows.push(Object.assign({ group, rep: r, page: n, kind: "熱", loadavg: C.env("").loadavg }, hot));
      console.log(`${group} 第${r}次 p${n} 熱：忙碌${hot.busy}% JS${hot.js}% 模型時間+${hot.modelAdvance}（${hot.seconds}秒）`);
    }
    await browser.close();
  }
  envs.push(C.env(group + "結束"));
  C.fs.writeFileSync(out, JSON.stringify({ group, envs, rows }, null, 1));
  srv.close();
})().catch(e => { console.error("診斷程式出錯：", e); process.exit(2); });

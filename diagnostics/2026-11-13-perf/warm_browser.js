/* B3用：開一個帶遠端除錯埠的Chromium（無頭），先載入簡報#p1兩次預熱，然後一直開著，讓Lighthouse用--port接上去。
 * 用法：node warm_browser.js <網址>（由run.sh在背景執行，跑完再關掉） */
const { chromium } = require("playwright");
(async () => {
  const b = await chromium.launch({ args: ["--remote-debugging-port=9222"] });
  const p = await b.newPage();
  for (let i = 0; i < 2; i++) { await p.goto(process.argv[2] + "#p1"); await p.waitForTimeout(3000); }
  await p.close(); console.log("預熱完成"); await new Promise(() => {});
})();

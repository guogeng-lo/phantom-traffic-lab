/* PARITY.md的J11：在Chromium打開建好的簡報（docs/index.html），用頁面裡的求解器跑J2的(20, 0)和J4的ε=0.1，
 * 跟Node跑web/ovm.js的結果比，每個值的差 ≤ 1e−12。另外確認頁面內嵌的求解器跟web/ovm.js是同一份檔案。
 * 用法：node tests/test_js_parity_browser.js */
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");
const { serve, blockExternal } = require("./site_server");
const O = require("../web/ovm.js");

const TOL = 1e-12;
function runJ2(O) {   // 第2頁：t=20點第0台，點擊後0到400，每0.5取樣位置和車速
  const d = new O.ClickDemo(22, 44.0, 1.0); d.click(20.0, 0, 0.5, 0.25);
  const out = [Array.from(d.ring.x).concat(Array.from(d.ring.v))];
  while (d.ring.t < 400 - 1e-9) { d.ring.step(); if (d.ring._steps % 10 === 0) out.push(Array.from(d.ring.x).concat(Array.from(d.ring.v))); }
  let jam = null; const d2 = new O.ClickDemo(22, 44.0, 1.0); d2.click(20.0, 0, 0.5, 0.25);
  for (let i = 0; i < 10000; i++) { d2.ring.step(); if (d2.ring.minSpeed() < 0.1) { jam = d2.ring._steps; break; } }
  return { traj: out, jam };
}
function runJ4(O) {   // 第1頁：ε=0.1，第一次車速低於0.1的步數，t=150的狀態
  const x = Array.from({ length: 22 }, (_, n) => n * 2.0); x[0] += 0.1;
  const r = new O.Ring(22, 44.0, 1.0, x); let jam = null, st = null;
  while (r.t < 1000 - 1e-9) { r.step(); if (jam === null && r.minSpeed() < 0.1) jam = r._steps; if (r._steps === 3000) st = Array.from(r.x).concat(Array.from(r.v)); if (jam !== null && r._steps >= 3000) break; }
  return { jam, st };
}

(async () => {
  const { srv, url } = await serve();
  const browser = await chromium.launch(); const page = await browser.newPage(); await blockExternal(page);
  await page.goto(url + "#p7");
  let fails = 0; const say = (ok, m) => { if (!ok) fails++; console.log(`${ok ? "通過" : "沒通過"}｜${m}`); };
  const embedded = await page.evaluate(() => document.getElementById("ovm-src").textContent.trim());
  say(embedded === fs.readFileSync(path.join(__dirname, "..", "web", "ovm.js"), "utf8").trim(), "頁面內嵌的求解器跟web/ovm.js一字不差");
  const fnSrc = `(${runJ2.toString()})`, fn4 = `(${runJ4.toString()})`;
  const b2 = await page.evaluate(src => eval(src)(window.OVM), fnSrc), n2 = runJ2(O);
  const b4 = await page.evaluate(src => eval(src)(window.OVM), fn4), n4 = runJ4(O);
  let m2 = 0; n2.traj.forEach((row, i) => row.forEach((v, j) => { m2 = Math.max(m2, Math.abs(v - b2.traj[i][j])); }));
  say(b2.traj.length === n2.traj.length && m2 <= TOL, `J11 J2(20, 0)：${n2.traj.length}個取樣，位置和車速的最大差 ${m2.toExponential(2)}（容許${TOL}）`);
  say(b2.jam === n2.jam, `J11 J2(20, 0)：塞車形成步數 瀏覽器${b2.jam}、Node ${n2.jam}`);
  let m4 = 0; n4.st.forEach((v, j) => { m4 = Math.max(m4, Math.abs(v - b4.st[j])); });
  say(m4 <= TOL, `J11 J4 ε=0.1：t=150狀態的最大差 ${m4.toExponential(2)}（容許${TOL}）`);
  say(b4.jam === n4.jam, `J11 J4 ε=0.1：塞車形成步數 瀏覽器${b4.jam}、Node ${n4.jam}`);
  console.log(`  （Chromium ${browser.version()}，Node ${process.version}）`);
  await browser.close(); srv.close();
  console.log(`\n沒通過${fails}項。`); process.exit(fails ? 1 : 0);
})().catch(e => { console.error("測試程式出錯：", e); process.exit(2); });

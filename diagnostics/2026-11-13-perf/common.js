/* 診斷共用（暫時性的診斷腳本，不是驗收測試）。量法跟tests/perf_mobile.js的動畫CPU項目一樣：
 * 375×812、DPR 3、isMobile、CPU慢4倍（CDP Emulation.setCPUThrottlingRate）、量6秒的Performance.getMetrics。 */
const fs = require("fs"), os = require("os"), { execSync } = require("child_process");
const { serve, blockExternal } = require("../../tests/site_server");
function env(label) {
  const sh = c => { try { return execSync(c, { encoding: "utf8" }).trim(); } catch (e) { return "（讀不到）"; } };
  return { label, time: new Date().toISOString(), loadavg: os.loadavg().map(x => x.toFixed(2)).join(" "), cpus: os.cpus().length, cpuModel: os.cpus()[0].model,
    cpuMax: sh("cat /sys/fs/cgroup/cpu.max 2>/dev/null || echo 沒有cpu.max（沒有cgroup CPU配額檔）"), memMB: Math.round(os.totalmem() / 1048576), freeMB: Math.round(os.freemem() / 1048576),
    uptimeS: Math.round(os.uptime()), top: sh("ps -eo pcpu,rss,comm --sort=-pcpu | head -6").split("\n").map(s => s.trim()) };
}
async function setup(page, n) {
  const s = page.locator(`#p${n}`);
  if (n === 2) { await s.locator("canvas.ring").focus(); await page.keyboard.press("Enter"); }
  if (n === 5) { await s.getByRole("button", { name: "看調多快" }).click(); await s.locator("canvas.ring").focus(); await page.keyboard.press("Enter"); }
}
async function measure(ctx, page, n, secs = 6) {
  const cdp = await ctx.newCDPSession(page);
  await cdp.send("Performance.enable"); await cdp.send("Emulation.setCPUThrottlingRate", { rate: 4 });
  const M = async () => Object.fromEntries((await cdp.send("Performance.getMetrics")).metrics.map(m => [m.name, m.value]));
  const clock = async () => parseFloat(await page.locator(`#p${n} .clock b`).first().textContent());
  const c0 = await clock(), m0 = await M();
  await page.waitForTimeout(secs * 1000);
  const m1 = await M(), c1 = await clock(), dur = m1.Timestamp - m0.Timestamp;
  return { busy: +((m1.TaskDuration - m0.TaskDuration) / dur * 100).toFixed(1), js: +((m1.ScriptDuration - m0.ScriptDuration) / dur * 100).toFixed(1),
    layout: +((m1.LayoutDuration - m0.LayoutDuration) / dur * 100).toFixed(1), style: +((m1.RecalcStyleDuration - m0.RecalcStyleDuration) / dur * 100).toFixed(1),
    seconds: +dur.toFixed(2), modelAdvance: +(c1 - c0).toFixed(1) };
}
const MOBILE = { viewport: { width: 375, height: 812 }, deviceScaleFactor: 3, isMobile: true, hasTouch: true };
function stats(v) { const s = [...v].sort((a, b) => a - b), n = s.length, mean = s.reduce((a, b) => a + b, 0) / n;
  return { n, min: s[0], max: s[n - 1], mean: +mean.toFixed(1), median: n % 2 ? s[n >> 1] : (s[n / 2 - 1] + s[n / 2]) / 2, over60: s.filter(x => x > 60).length, all: v }; }
module.exports = { env, setup, measure, MOBILE, stats, serve, blockExternal, fs };

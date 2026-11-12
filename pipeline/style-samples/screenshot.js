const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const url = 'file://' + require('path').resolve(__dirname, 'index.html');
  const errs = [];
  for (const [w, h, tag] of [[1366, 900, 'desk'], [375, 812, 'phone']]) {
    for (const k of ['a', 'b', 'c']) {
      const p = await b.newPage({ viewport: { width: w, height: h } });
      p.on('pageerror', e => errs.push(`${tag} ${k} ${e.message}`));
      await p.goto(url + '#' + k); await p.waitForTimeout(600);
      const cv = await p.$('[data-ring="2"]'); const bb = await cv.boundingBox();
      await p.mouse.click(bb.x + bb.width * 0.5, bb.y + bb.height * 0.1);
      await p.waitForFunction(() => document.querySelector('[data-say]').textContent.includes('最後有一段幾乎停住'), null, { timeout: 90000 });
      await p.waitForTimeout(1500);
      const sec = await p.$$('section.page'); await sec[0].screenshot({ path: `shots/${tag}-${k}-p2.png` });
      await p.click('[data-act="ts-one"]'); await p.waitForTimeout(2500);
      await sec[1].screenshot({ path: `shots/${tag}-${k}-p3-one.png` });
      await p.waitForFunction(() => !document.querySelector('[data-act="ts-all"]').disabled, null, { timeout: 90000 });
      await p.click('[data-act="ts-all"]'); await p.waitForTimeout(300);
      await p.click('[data-opt="left"]'); await p.waitForTimeout(600);
      await sec[1].screenshot({ path: `shots/${tag}-${k}-p3.png` });
      const ov = await p.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      if (ov > 0) errs.push(`${tag} ${k} horizontal overflow ${ov}px`);
      await p.close();
    }
  }
  console.log(errs.length ? errs.join('\n') : 'no page errors, no overflow');
  await b.close();
})();

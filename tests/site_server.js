/* 測試共用：在本機起一個靜態伺服器提供docs/（跟GitHub Pages一樣用http，不用file://），再開Chromium。 */
const http = require("http");
const fs = require("fs");
const path = require("path");

const DOCS = path.resolve(__dirname, "..", "docs");
const TYPES = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".css": "text/css", ".json": "application/json", ".png": "image/png" };

function serve() {
  return new Promise(res => {
    const srv = http.createServer((req, rsp) => {
      const u = decodeURIComponent(req.url.split("?")[0].split("#")[0]);
      const f = path.join(DOCS, u === "/" ? "index.html" : u);
      if (!f.startsWith(DOCS) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { rsp.writeHead(404); rsp.end(); return; }
      rsp.writeHead(200, { "Content-Type": TYPES[path.extname(f)] || "application/octet-stream" });
      fs.createReadStream(f).pipe(rsp);
    });
    srv.listen(0, "127.0.0.1", () => res({ srv, url: `http://127.0.0.1:${srv.address().port}/` }));
  });
}

/** 字型（Google Fonts）在測試環境連不到；擋掉外部請求，讓每次測試的條件一樣，也不會等到逾時。 */
async function blockExternal(page) {
  await page.route(/^https?:\/\/(?!127\.0\.0\.1)/, r => r.abort());
}

module.exports = { serve, blockExternal };

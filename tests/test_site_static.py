"""節點7：建好的簡報（docs/index.html）和網頁程式的靜態檢查。

用法：python3 tests/test_site_static.py
- 每一頁都有「出處和檢查」，而且至少列一張證據卡；列出的證據卡檔案真的存在。
- 連結：頁內連結（#p1～#p10）指得到；連到GitHub repo的連結，對應的檔案或資料夾在repo裡存在；外部連結是完整的https網址。
  （外部網站這裡連不到，實際打得開要在節點8用正式網址測。）
- 沒有只能懸停的操作：CSS沒有:hover，網頁程式沒有mouseover、mouseenter、hover的事件。
- 不存讀者的資料：網頁程式沒有localStorage、sessionStorage、IndexedDB、cookie、fetch、XMLHttpRequest、sendBeacon。
- 檢查結果不是寫死的：網頁程式和樣板裡沒有「通過」「PASS」這種字；出處裡的檢查結果只能來自build_site.py建置時實際執行的程式。
- 網頁程式不能改求解器的步長：web/裡沒有呼叫step(時傳參數（PARITY.md的J12，Node的對答案測試也會查）。
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO = "https://github.com/guogeng-lo/phantom-traffic-lab"
results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(f"{'通過' if ok else '沒通過'}｜{name}{'｜' + detail if detail else ''}")


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.stack, self.pages = set(), [], [], {}
        self.cur = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "section" and a.get("data-page"):
            self.cur = int(a["data-page"])
            self.pages[self.cur] = {"src": 0, "cards": []}
        if tag == "details" and "src" in (a.get("class") or "").split() and self.cur:
            self.pages[self.cur]["src"] += 1
        if tag == "a" and "href" in a:
            self.links.append(a["href"])
            m = re.match(re.escape(REPO) + r"/blob/main/wiki/cards/([a-z0-9-]+)\.md$", a["href"])
            if m and self.cur:
                self.pages[self.cur]["cards"].append(m.group(1))


def main():
    html = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    p = P()
    p.feed(html)
    check("簡報有10頁", sorted(p.pages) == list(range(1, 11)), str(sorted(p.pages)))
    for n in range(1, 11):
        pg = p.pages.get(n, {"src": 0, "cards": []})
        miss = [c for c in pg["cards"] if not (ROOT / "wiki" / "cards" / f"{c}.md").exists()]
        check(f"第{n}頁有出處，至少一張證據卡，卡片檔案都在", pg["src"] == 1 and len(pg["cards"]) >= 1 and not miss, f"{len(pg['cards'])}張" + (f"；找不到：{miss}" if miss else ""))
    # 第10頁的延伸閱讀和第7頁的論文連結是程式產生的；這裡把它們的網址也算進來
    js = (ROOT / "web" / "deck.js").read_text(encoding="utf-8")
    links = list(p.links) + [f"{REPO}/blob/main/wiki/index.md", f"{REPO}/tree/main/runs", REPO]
    bad = []
    for h in links:
        if h.startswith("#"):
            if h[1:] not in p.ids:
                bad.append(h)
        elif h.startswith(REPO):
            rest = h[len(REPO):]
            m = re.match(r"^/(blob|tree)/main/(.+)$", rest)
            if rest and not (m and (ROOT / m.group(2)).exists()):
                bad.append(h)
        elif not re.match(r"^https://[a-z0-9.-]+\.[a-z]{2,}/\S+$", h):
            bad.append(h)
    check("連結都指得到（頁內、repo裡的檔案、https網址的格式）", not bad, f"{len(links)}個連結" + (f"；有問題：{bad}" if bad else ""))
    import json
    data = re.search(r"window\.DECK_DATA = (\{.*?\});\n", html, re.S)
    srcs = json.loads(data.group(1))["sources"] if data else []
    badsrc = [s["id"] for s in srcs if not re.match(r"^https://[a-z0-9.-]+\.[a-z]{2,}/\S+$", s.get("url", ""))]
    check("六篇文獻都有https連結（DOI優先）", len(srcs) == 6 and not badsrc, f"{len(srcs)}篇" + (f"；有問題：{badsrc}" if badsrc else ""))
    css = (ROOT / "web" / "deck.css").read_text(encoding="utf-8")
    hov = re.findall(r":hover", css) + re.findall(r"mouseover|mouseenter|mouseleave|onhover|\"hover\"", js)
    check("沒有只能懸停的操作（CSS的:hover、滑鼠移入事件）", not hov, f"找到{hov}" if hov else "0處")
    store = re.findall(r"localStorage|sessionStorage|indexedDB|document\.cookie|fetch\(|XMLHttpRequest|sendBeacon", js)
    check("網頁程式不存、不送讀者的資料", not store, f"找到{store}" if store else "0處")
    tpl = (ROOT / "web" / "template.html").read_text(encoding="utf-8")
    # 「通過量」（車流量）是第8頁長條圖的名稱，不是檢查結果
    hard = [w for w in (r"通過(?!量)", r"PASS", r"Pass") if any(re.search(w, t) for t in (js, tpl, css))]
    check("網頁程式和樣板沒有寫死檢查結果", not hard, f"找到{hard}" if hard else "0處")
    calls = []
    for f in sorted((ROOT / "web").glob("*.js")):
        for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if re.search(r"\.step\(\s*[^)\s]", line):
                calls.append(f"{f.name}:{i}")
    check("web/裡沒有呼叫step(時傳參數", not calls, "、".join(calls) if calls else "0處")
    nf = results.count(False)
    print(f"\n共{len(results)}項，沒通過{nf}項。")
    return 1 if nf else 0


if __name__ == "__main__":
    sys.exit(main())

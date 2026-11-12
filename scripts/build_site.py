"""建置教學簡報：從逐頁稿、slide-map、證據卡和實際執行的檢查，產生單一HTML檔docs/index.html。

用法：python3 scripts/build_site.py            # 建置時會實際執行檢查程式，把結果寫進每頁的「出處」
      python3 scripts/build_site.py --no-checks # 只建置版面（開發用；出處的檢查狀態會顯示「這次建置沒有執行檢查」）

- 頁面的文字（主線、知識、進階）直接從pipeline/pages/pNN.md轉成HTML，不另外手寫，避免跟審查過的內容不一致。
- 「出處」由slide-map、證據卡和這次建置實際執行的檢查產生；不手寫檢查結果（AGENTS第0節第4條）。
  節點6的審查狀態：比對逐頁稿現在的SHA-256和runs/2026-11-12-n6-review-r4.md記錄的值，不同就顯示「已過期」。
- CSS、求解器（web/ovm.js）、互動程式（web/deck.js）都內嵌，輸出一個HTML檔。
"""
import argparse
import datetime
import hashlib
import html
import json
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from check_pages import split_sections  # noqa: E402
from check_slide_map import LINK, ROW  # noqa: E402
from check_wiki import parse  # noqa: E402

REPO = "https://github.com/guogeng-lo/phantom-traffic-lab"
TYPE = {"experiment": ("exp", "實驗"), "model_theory": ("mod", "模型"), "review": ("mod", "綜述"),
        "our_simulation": ("sim", "我們的模擬"), "our_derivation": ("der", "我們的推導"), "expression": ("pop", "科普")}
TAGS = {"實驗": "exp", "模型": "mod", "我們的模擬": "sim", "我們的推導": "der"}
SIM_PAGES = {1, 2, 3, 4, 5, 6, 8}


# ---------------- Markdown（逐頁稿只用到的一小部分） ----------------
def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r'<code class="f">\1</code>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"【(實驗|模型|我們的模擬|我們的推導)】", lambda m: f'<span class="tag {TAGS[m.group(1)]}">【{m.group(1)}】</span>', s)
    return s


def blocks(text):
    """切成段落和清單。回傳[("p", 文字) | ("ul"/"ol", [項目文字, ...])]；清單項目可以有縮排的第二段。"""
    out, lines, i = [], text.strip("\n").splitlines(), 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1
            continue
        m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", ln)
        if m and not m.group(1):
            kind = "ol" if m.group(2)[0].isdigit() else "ul"
            items = []
            while i < len(lines):
                m = re.match(r"^([-*]|\d+\.)\s+(.*)$", lines[i])
                if m:
                    items.append([m.group(2)])
                    i += 1
                elif lines[i].startswith("  ") and items:
                    items[-1].append(lines[i].strip())
                    i += 1
                elif not lines[i].strip() and i + 1 < len(lines) and (lines[i + 1].startswith("  ") or re.match(r"^([-*]|\d+\.)\s", lines[i + 1])):
                    items[-1].append("")
                    i += 1
                else:
                    break
            out.append((kind, items))
            continue
        para = [ln.strip()]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^([-*]|\d+\.)\s", lines[i]):
            para.append(lines[i].strip())
            i += 1
        out.append(("p", "".join(para)))
    return out


def item_html(parts, wrap_first=False):
    paras, cur = [], []
    for s in parts:
        if s == "":
            if cur:
                paras.append("".join(cur))
            cur = []
        else:
            cur.append(s)
    if cur:
        paras.append("".join(cur))
    return "".join(f"<p>{inline(p)}</p>" if k or wrap_first else inline(p) for k, p in enumerate(paras))


def render(text, cls=""):
    out, n = [], 0
    for kind, body in blocks(text):
        n += 1
        if kind == "p":
            out.append(f'<p data-i="{n}">{inline(body)}</p>')
        else:
            items = "".join(f"<li>{item_html(it)}</li>" for it in body)
            out.append(f'<{kind} data-i="{n}"{f" class={cls}" if cls else ""}>{items}</{kind}>')
    return "\n".join(out)


def render_quiz(text):
    """第10頁：題目、選項、揭曉。（正確）只用來標記答案，不顯示在選項上。"""
    out, q = [], 0
    bl = blocks(text)
    intro = []
    k = 0
    while k < len(bl) and not (bl[k][0] == "p" and bl[k][1].startswith("**第")):
        intro.append(f"<p>{inline(bl[k][1])}</p>")
        k += 1
    out.append("".join(intro))
    while k < len(bl):
        title = re.sub(r"^\*\*(.+)\*\*$", r"\1", bl[k][1])
        opts = bl[k + 1][1]
        reveal = bl[k + 2][1]
        q += 1
        btns = []
        for j, it in enumerate(opts):
            t = "".join(it)
            right = t.endswith("（正確）")
            t = t[:-4] if right else t
            t = t.strip("「」")
            btns.append(f'<button class="opt" type="button" data-q="{q}" data-right="{int(right)}">{inline(t)}</button>')
        reveal = re.sub(r"^揭曉：", "", reveal)
        out.append(f'<div class="quiz" data-quiz="{q}"><h3>{inline(title)}</h3><div class="opts">{"".join(btns)}</div>'
                   f'<p class="verdict" hidden></p><div class="why" hidden><p>{inline(reveal)}</p></div></div>')
        k += 3
    return "\n".join(out)


def render_cards9(text):
    """第9頁：編號清單的每一項變成一張可以展開的卡片。"""
    out = []
    for kind, body in blocks(text):
        if kind == "p":
            if "卡片內容" in body:
                continue
            out.append(f"<p>{inline(body)}</p>")
            continue
        for it in body:
            m = re.match(r"^\*\*(.+?)\*\*：(.*)$", it[0])
            title, first = (m.group(1), m.group(2)) if m else (it[0], "")
            out.append(f'<details class="card9"><summary>{inline(title)}</summary>{item_html([first] + it[1:], True)}</details>')
    return "\n".join(out)


# ---------------- 證據卡、slide-map、檢查 ----------------
def load_cards():
    cards = {}
    for p in sorted((ROOT / "wiki" / "cards").glob("*.md")):
        if p.name == "_template.md":
            continue
        meta, _ = parse(p)
        cards[p.stem] = meta
    return cards


def slide_cards():
    m = {}
    for line in (ROOT / "wiki" / "slide-map.md").read_text(encoding="utf-8").splitlines():
        r = ROW.match(line)
        if r:
            pg = int(r.group(1))
            for _, cid in LINK.findall(r.group(3)):
                m.setdefault(pg, [])
                if cid not in m[pg]:
                    m[pg].append(cid)
    return m


def run(cmd):
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    lines = [l for l in (r.stdout + r.stderr).strip().splitlines() if l.strip()]
    return r.returncode, (lines[-1] if lines else "")


def n6_status():
    rec = (ROOT / "runs" / "2026-11-12-n6-review-r4.md").read_text(encoding="utf-8")
    want = dict(re.findall(r"\| `(pipeline/pages/p\d\d\.md)` \| `([0-9a-f]{64})` \|", rec))
    stale = [f for f, h in want.items() if hashlib.sha256((ROOT / f).read_bytes()).hexdigest() != h]
    return want, stale


def checks(enabled):
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    today = datetime.date.today().isoformat()
    if not enabled:
        return {"commit": commit, "date": today, "items": None}
    items = []
    for name, cmd in (("證據卡格式檢查（scripts/check_wiki.py）", ["python3", "scripts/check_wiki.py"]),
                      ("頁面和證據卡對應（scripts/check_slide_map.py）", ["python3", "scripts/check_slide_map.py"]),
                      ("逐頁稿程式檢查（scripts/check_pages.py）", ["python3", "scripts/check_pages.py"]),
                      ("瀏覽器求解器跟Python對答案（tests/test_js_parity.js）", ["node", "tests/test_js_parity.js"])):
        code, last = run(cmd)
        items.append({"name": name, "ok": code == 0, "out": last, "sim": "parity" in " ".join(cmd)})
    want, stale = n6_status()
    return {"commit": commit, "date": today, "items": items, "n6_stale": stale, "n6_known": sorted(want)}


def source_box(pg, cards, smap, chk):
    rows = []
    for cid in smap.get(pg, []):
        meta = cards[cid]
        cls, label = TYPE.get(meta.get("type"), ("pop", meta.get("type", "")))
        rows.append(f'<li><span class="tag {cls}">【{label}】</span> <a href="{REPO}/blob/main/wiki/cards/{cid}.md" target="_blank" rel="noopener">{cid}</a>'
                    f'<span class="loc">{html.escape(meta.get("locator", ""))}</span></li>')
    if chk["items"] is None:
        status = '<p class="chk">這次建置沒有執行檢查，所以不顯示檢查結果。</p>'
    else:
        lis = []
        for it in chk["items"]:
            if it["sim"] and pg not in SIM_PAGES:
                continue
            lis.append(f'<li class="{"ok" if it["ok"] else "bad"}">{"通過" if it["ok"] else "沒通過"}：{html.escape(it["name"])}<span class="loc">{html.escape(it["out"])}</span></li>')
        rel = f"pipeline/pages/p{pg:02d}.md"
        if rel not in chk["n6_known"]:
            n6 = '<li class="bad">未檢查：逐頁稿獨立審查（節點6）沒有這一頁的紀錄</li>'
        elif rel in chk["n6_stale"]:
            n6 = '<li class="bad">已過期：逐頁稿在節點6審查之後改過，要重新審查</li>'
        else:
            n6 = '<li class="ok">通過：逐頁稿獨立審查（節點6第4輪，使用者授權的限定範圍複核）<span class="loc">逐頁稿的SHA-256跟審查紀錄一致</span></li>'
        lis.append(n6)
        status = f'<ul class="chk">{"".join(lis)}</ul><p class="chk-meta">以上是建置時（{chk["date"]}，commit {chk["commit"]}）實際執行的結果。網站不會自己更新；Wiki或程式改了要重新建置。</p>'
    return (f'<details class="src"><summary>出處和檢查</summary><div class="src-in"><h3>這一頁用到的證據卡</h3><ul class="cards">{"".join(rows)}</ul>'
            f'<h3>檢查狀態</h3>{status}</div></details>')


def page_html(pg, cards, smap, chk):
    path = ROOT / "pipeline" / "pages" / f"p{pg:02d}.md"
    text = path.read_text(encoding="utf-8")
    title = text.splitlines()[0].split("｜", 1)[1]
    sec = dict(split_sections(text))
    main = render_quiz(sec["主線"]) if pg == 10 else render(sec["主線"], "exp-grid" if pg == 7 else "")
    know = sec.get("知識", "").strip()
    adv = sec.get("進階", "").strip()
    know_html = "" if not know or know.startswith("（這頁沒有") else (render_cards9(know) if pg == 9 else render(know))
    adv_html = "" if not adv or adv.startswith("（這頁沒有") else render(adv)
    parts = [f'<section class="page" id="p{pg}" data-page="{pg}" aria-labelledby="h{pg}" hidden>',
             f'<header class="ph"><h2 id="h{pg}" tabindex="-1">{html.escape(title)}</h2></header>',
             f'<div class="stage" data-stage="{pg}"></div>',
             f'<div class="text main" data-layer="main">{main}</div>']
    if know_html:
        parts.append(f'<div class="text know" data-layer="know">{"" if pg == 9 else '<h3 class="layer">正式名稱</h3>'}{know_html}</div>')
    if adv_html:
        parts.append(f'<details class="adv" data-layer="adv"><summary>進階：模型、推導和量法</summary><div class="text">{adv_html}</div></details>')
    parts.append(source_box(pg, cards, smap, chk))
    parts.append("</section>")
    return "\n".join(parts), title


def sources_list():
    out = []
    for p in sorted((ROOT / "wiki" / "sources").glob("*.md")):
        if p.name == "_template.md":
            continue
        meta, _ = parse(p)
        doi = meta.get("doi", "無")
        out.append({"id": p.stem, "title": meta.get("title", ""), "year": meta.get("year", ""),
                    "url": f"https://doi.org/{doi}" if doi and doi != "無" else meta.get("url", "")})
    return out


def bars():
    """第8頁長條圖的數字：直接從逐頁稿的主線讀，不在程式裡另外寫一份。讀不到就讓建置失敗。"""
    text = (ROOT / "pipeline" / "pages" / "p08.md").read_text(encoding="utf-8")
    pats = {"std": r"車速起伏都變小：分別少了([\d.]+)%、([\d.]+)%、([\d.]+)%",
            "fuel": r"油耗都下降：分別少了([\d.]+)%、([\d.]+)%、([\d.]+)%",
            "flow": r"A、B兩場增加了([\d.]+)%和([\d.]+)%，C那一場反而少了([\d.]+)%"}
    out = {}
    for k, pat in pats.items():
        m = re.search(pat, text)
        if not m:
            sys.exit(f"build_site：第8頁讀不到長條圖的數字（{k}）")
        a, b, c = (float(g) for g in m.groups())
        out[k] = [-a, -b, -c] if k != "flow" else [a, b, -c]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-checks", action="store_true")
    args = ap.parse_args()
    cards, smap = load_cards(), slide_cards()
    chk = checks(not args.no_checks)
    pages, titles = [], []
    for pg in range(1, 11):
        h, t = page_html(pg, cards, smap, chk)
        pages.append(h)
        titles.append(t)
    tpl = (ROOT / "web" / "template.html").read_text(encoding="utf-8")
    out = (tpl.replace("{{CSS}}", (ROOT / "web" / "deck.css").read_text(encoding="utf-8"))
              .replace("{{PAGES}}", "\n".join(pages))
              .replace("{{TITLES}}", json.dumps(titles, ensure_ascii=False))
              .replace("{{SOURCES}}", json.dumps(sources_list(), ensure_ascii=False))
              .replace("{{BARS}}", json.dumps(bars()))
              .replace("{{REPO}}", REPO)
              .replace("{{OVM}}", (ROOT / "web" / "ovm.js").read_text(encoding="utf-8"))
              .replace("{{DECK}}", (ROOT / "web" / "deck.js").read_text(encoding="utf-8")))
    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)
    (docs / "index.html").write_text(out, encoding="utf-8", newline="\n")
    (docs / ".nojekyll").write_text("", encoding="utf-8")
    bad = [] if chk["items"] is None else [i["name"] for i in chk["items"] if not i["ok"]]
    print(f"已產生 docs/index.html（{len(out) // 1024} KB）；檢查：{'沒有執行' if chk['items'] is None else ('全部通過' if not bad else '沒通過：' + '、'.join(bad))}"
          f"{'' if chk['items'] is None else '；節點6已過期：' + (', '.join(chk['n6_stale']) or '沒有')}")


if __name__ == "__main__":
    main()

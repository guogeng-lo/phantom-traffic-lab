"""逐頁稿檢查（節點6送審前的程式檢查）。讀pipeline/pages/、pipeline/outline.md、wiki/slide-map.md、證據卡和wiki/glossary.md。

用法：python3 scripts/check_pages.py [--root 路徑]
結束代碼：0沒有錯誤；1有錯誤。

檢查的事：
P1 大綱的每一頁都有pipeline/pages/pNN.md，第一行是「# 第N頁｜標題」，標題跟大綱一樣。
P2 段落齊全、順序固定、每個只出現一次：畫面和互動、顯示設定、主線、知識、進階、數字從哪來、證據卡、要小心。
P3 「證據卡」段落：每一行是「- 【標示】卡片id、卡片id」；卡片要存在；標示要跟卡片類型對得上
   （【實驗】experiment、【模型】model_theory或review、【我們的推導】our_derivation、【我們的模擬】our_simulation）；
   這頁的卡片要跟wiki/slide-map.md這一頁所有列的卡片完全一樣（出處區是從slide-map產生的）。
P4 讀者看得到的文字（畫面和互動、主線、知識、進階）裡的每一個數字，都要列在「數字從哪來」表格的第一欄。
   （行首的清單編號「1. 」本來就不會被當成數字：數字後面緊接著句點的不算，規則跟check_slide_map.py一樣。）
   不算的：1900～2099的四位數（年份）、「第N頁」「第N題」這種頁面和題目編號、
   反引號裡的檔名和卡片id（只有英數、底線、點、斜線、連字號）、緊接在大寫英文字母後面的數字（例如RK4這種名稱）。
P5 「數字從哪來」表格的每一列：證據卡那一欄的卡片都要在這頁的證據卡裡，而且這一列的每一個數字，
   至少在其中一張卡（主張、條件、原文依據、限制）裡找得到；照數字的小數位數四捨五入比對，跟check_slide_map.py一樣。
   比check_slide_map.py多算「限制」，因為頁面要照實寫限制裡的數字（例如21台的量測長度）；slide-map的核心主張不能只靠限制，所以那邊不算。
   例外：證據卡那一欄寫「顯示設定」的列，是呈現方式的選擇（例如畫哪幾台車），不是證據；這種列的數字要出現在這頁的「顯示設定」段落裡。
P6 wiki/glossary.md有英文的術語，在逐頁稿裡第一次出現時（照第1頁主線、知識、進階，再第2頁……的順序），
   後面要緊接著「（英文）」，括號裡要包含術語表英文欄的其中一個寫法。
P7 讀者看得到的文字用了【實驗】【模型】【我們的推導】【我們的模擬】，這頁就要有那種類型的卡。
"""
import argparse
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_wiki import parse, sections  # noqa: E402
from check_slide_map import LINK, ROW, found, numbers  # noqa: E402

SECTIONS = ["畫面和互動", "顯示設定", "主線", "知識", "進階", "數字從哪來", "證據卡", "要小心"]
READER = ["畫面和互動", "主線", "知識", "進階"]
GLOSSARY_ORDER = ["主線", "知識", "進階"]
TAGS = {"實驗": {"experiment"}, "模型": {"model_theory", "review"},
        "我們的推導": {"our_derivation"}, "我們的模擬": {"our_simulation"}}
CARD_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)+")
PAGE_REF = re.compile(r"第[\d、，,～~\-]+[頁題]")
PATH_TICK = re.compile(r"`[A-Za-z0-9_./-]+`")
NAME_NUM = re.compile(r"(?<=[A-Z])\d+")


class Report:
    def __init__(self):
        self.errors = 0

    def err(self, where, msg):
        self.errors += 1
        print(f"[錯誤] {where}：{msg}")


def split_sections(text):
    """回傳[(標題, 內容)]，照出現順序；只認「## 」開頭的行。"""
    out, cur, buf = [], None, []
    for line in text.splitlines():
        if line.startswith("## "):
            if cur is not None:
                out.append((cur, "\n".join(buf)))
            cur, buf = line[3:].strip(), []
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        out.append((cur, "\n".join(buf)))
    return out


def reader_numbers(text):
    t = PATH_TICK.sub(" ", text)
    t = PAGE_REF.sub(" ", t)
    t = NAME_NUM.sub("", t)
    return numbers(t)


def table_rows(body):
    rows = []
    for line in body.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) < 3 or set(cells[0]) <= set("-: ") or cells[0] == "數字":
            continue
        rows.append(cells)
    return rows


def load_glossary(root):
    terms = []
    p = root / "wiki" / "glossary.md"
    for line in p.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) < 2 or cells[0] in ("中文", "") or set(cells[0]) <= set("-: "):
            continue
        eng = [e.strip() for e in cells[1].split(",") if e.strip() and e.strip() != "—"]
        if eng:
            terms.append((cells[0], eng))
    return terms


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=Path(__file__).resolve().parent.parent)
    root = Path(ap.parse_args().root).resolve()
    rep = Report()

    cards = {}
    for p in sorted((root / "wiki" / "cards").glob("*.md")):
        if p.name == "_template.md":
            continue
        meta, body = parse(p)
        secs = sections(body)
        text = " ".join([secs.get("主張", ""), meta.get("conditions", ""), secs.get("原文依據", ""), secs.get("限制", "")])
        cards[p.stem] = (meta.get("type"), numbers(text))

    outline = (root / "pipeline" / "outline.md").read_text(encoding="utf-8")
    titles = {int(n): t.strip() for n, t in re.findall(r"^### 第(\d+)頁｜(.+)$", outline, re.M)}

    smap = {}
    for line in (root / "wiki" / "slide-map.md").read_text(encoding="utf-8").splitlines():
        m = ROW.match(line)
        if m:
            smap.setdefault(int(m.group(1)), set()).update(t for _, t in LINK.findall(m.group(3)))

    glossary = load_glossary(root)
    seen_terms = set()

    for pg in sorted(titles):
        rel = f"pipeline/pages/p{pg:02d}.md"
        path = root / rel
        if not path.exists():
            rep.err(rel, f"大綱的第{pg}頁沒有逐頁稿")
            continue
        text = path.read_text(encoding="utf-8")
        first = text.splitlines()[0] if text else ""
        if first != f"# 第{pg}頁｜{titles[pg]}":
            rep.err(rel, f"第一行要是「# 第{pg}頁｜{titles[pg]}」")
        secs = split_sections(text)
        names = [n for n, _ in secs]
        for n in SECTIONS:
            c = names.count(n)
            if c == 0:
                rep.err(rel, f"缺少段落「## {n}」")
            elif c > 1:
                rep.err(rel, f"段落「## {n}」出現{c}次")
        present = [n for n in names if n in SECTIONS]
        if len(set(present)) == len(present) and present != [n for n in SECTIONS if n in present]:
            rep.err(rel, "段落的順序不對，要照：" + "、".join(SECTIONS))
        body = {n: b for n, b in secs}

        # P3
        page_cards, page_types = set(), set()
        for line in body.get("證據卡", "").splitlines():
            s = line.strip()
            if not s:
                continue
            m = re.match(r"^- 【([^】]+)】(.+)$", s)
            if not m:
                rep.err(rel, f"證據卡段落的這一行格式不對：{s}")
                continue
            tag = m.group(1)
            if tag not in TAGS:
                rep.err(rel, f"證據卡段落用了不認得的標示【{tag}】")
                continue
            for cid in re.split(r"[、,，\s]+", m.group(2).strip()):
                if not cid:
                    continue
                if cid not in cards:
                    rep.err(rel, f"證據卡 {cid} 不存在")
                    continue
                if cards[cid][0] not in TAGS[tag]:
                    rep.err(rel, f"證據卡 {cid} 的類型是{cards[cid][0]}，不能標【{tag}】")
                page_cards.add(cid)
                page_types.add(cards[cid][0])
        want = smap.get(pg, set())
        for cid in sorted(page_cards - want):
            rep.err(rel, f"證據卡 {cid} 在逐頁稿裡，但slide-map第{pg}頁沒有")
        for cid in sorted(want - page_cards):
            rep.err(rel, f"slide-map第{pg}頁有證據卡 {cid}，但逐頁稿沒有")

        # P4、P5
        listed = set()
        for cells in table_rows(body.get("數字從哪來", "")):
            nums = numbers(cells[0])
            listed.update(nums)
            if cells[2] == "顯示設定":
                shown = numbers(body.get("顯示設定", ""))
                for num in nums:
                    if num not in shown:
                        rep.err(rel, f"數字表把 {num} 標成顯示設定，但「顯示設定」段落裡沒有這個數字")
                continue
            row_cards = [c for c in re.split(r"[、,，\s]+", cells[2]) if c]
            for c in row_cards:
                if c not in page_cards:
                    rep.err(rel, f"數字表的「{cells[0]}」那一列用了證據卡 {c}，但這頁的證據卡沒有")
            pool = [x for c in row_cards if c in cards for x in cards[c][1]]
            for num in nums:
                if not found(num, pool):
                    rep.err(rel, f"數字 {num} 在數字表寫的證據卡裡找不到")
        for sec in READER:
            for num in reader_numbers(body.get(sec, "")):
                if num not in listed:
                    rep.err(rel, f"「{sec}」裡的數字 {num} 沒有列在數字從哪來")

        # P6
        for sec in GLOSSARY_ORDER:
            t = body.get(sec, "")
            for term, eng in glossary:
                if term in seen_terms:
                    continue
                i = t.find(term)
                if i < 0:
                    continue
                seen_terms.add(term)
                rest = t[i + len(term):]
                m = re.match(r"（([^）]*)）", rest)
                if not m or not any(e.lower() in m.group(1).lower() for e in eng):
                    rep.err(rel, f"術語「{term}」第一次出現（{sec}）要寫成「{term}（{eng[0]}）」")

        # P7
        reader = "\n".join(body.get(s, "") for s in READER)
        for tag, types in TAGS.items():
            if f"【{tag}】" in reader and not (page_types & types):
                rep.err(rel, f"文字用了【{tag}】，但這頁沒有那種類型的證據卡")

    print(f"\n逐頁稿 {len(titles)} 頁，錯誤 {rep.errors} 個。")
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())

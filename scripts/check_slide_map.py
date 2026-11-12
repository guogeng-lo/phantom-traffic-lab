"""節點5：頁面和證據卡對應檢查。讀wiki/slide-map.md、證據卡和pipeline/outline.md。

用法：python3 scripts/check_slide_map.py [--root 路徑]
結束代碼：0沒有錯誤；1有錯誤。

檢查的事：
C1 大綱裡的每一頁（pipeline/outline.md的「### 第N頁」），在slide-map至少有一列。
C2 每一列至少連到一張證據卡；連到的卡要存在；連結文字要跟連結的卡片id一樣。
C3 層次有「主線」的列，至少要有一張status是confirmed、而且type不是expression的卡（核心主張不能只靠pending或科普）。
C4 主張寫了「真實」「實驗」「真的人」，至少要連到一張experiment卡。
C5 只連到我們自己的卡（our_derivation、our_simulation）時，主張要寫明「模型」「模擬」或「我們」，不能看起來像真實道路的結果。
C6 主張寫了「模型」「模擬」，至少要連到一張model_theory、review或我們自己的卡。
C7 主張裡的每一個數字，都要在連到的卡片裡找得到（卡片的主張、條件、原文依據）。
   比對時照主張裡數字的小數位數四捨五入，例如主張寫1.96，卡片寫1.959494也算找到。
   1900～2099的四位數當成年份，不檢查。
"""
import argparse
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_wiki import parse, sections  # noqa: E402

ROW = re.compile(r"^\|\s*(\d+)\s*\|(.*)\|(.*)\|(.*)\|\s*$")
LINK = re.compile(r"\[([^\]]+)\]\(cards/([^)]+)\.md\)")
NUM = re.compile(r"(?<![\d.])\d+(?:\.\d+)?(?![\d.])")
OURS = {"our_derivation", "our_simulation"}


class Report:
    def __init__(self):
        self.errors = 0

    def err(self, where, msg):
        self.errors += 1
        print(f"[錯誤] {where}：{msg}")


def numbers(text):
    out = []
    for m in NUM.finditer(text):
        s = m.group(0)
        if "." not in s and len(s) == 4 and 1900 <= int(s) <= 2099:
            continue
        out.append(s)
    return out


def found(num, card_nums):
    d = len(num.split(".")[1]) if "." in num else 0
    x = float(num)
    for y in card_nums:
        yv = float(y)
        if round(yv, d) == x or abs(yv - x) < 1e-12:
            return True
    return False


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
        text = " ".join([secs.get("主張", ""), meta.get("conditions", ""), secs.get("原文依據", "")])
        cards[p.stem] = (meta, numbers(text))
    outline = (root / "pipeline" / "outline.md").read_text(encoding="utf-8")
    pages = sorted({int(n) for n in re.findall(r"^### 第(\d+)頁", outline, re.M)})
    rows = []
    for n, line in enumerate((root / "wiki" / "slide-map.md").read_text(encoding="utf-8").splitlines(), 1):
        m = ROW.match(line)
        if m:
            rows.append((n, int(m.group(1)), m.group(2).strip(), m.group(3).strip(), m.group(4).strip()))
    for pg in pages:
        if not any(r[1] == pg for r in rows):
            rep.err("wiki/slide-map.md", f"第{pg}頁沒有任何對照列")
    for n, pg, claim, cell, layer in rows:
        where = f"wiki/slide-map.md:{n}（第{pg}頁）"
        links = LINK.findall(cell)
        if not links:
            rep.err(where, "沒有連到任何證據卡")
            continue
        linked = []
        for text, target in links:
            if text != target:
                rep.err(where, f"連結文字「{text}」跟連到的卡片 {target} 不一樣")
            if target not in cards:
                rep.err(where, f"連結的卡片 {target} 不存在")
            else:
                linked.append(target)
        if not linked:
            continue
        types = {cards[c][0].get("type") for c in linked}
        if "主線" in layer and not any(cards[c][0].get("status") == "confirmed" and cards[c][0].get("type") != "expression"
                                     for c in linked):
            rep.err(where, "主線的主張至少要有一張confirmed、而且不是expression的卡")
        if re.search(r"真實|實驗|真的人", claim) and "experiment" not in types:
            rep.err(where, "寫了真實或實驗，卻沒有連到experiment卡")
        if types <= OURS and not re.search(r"模型|模擬|我們", claim):
            rep.err(where, "只連到我們自己的卡，主張要寫明是模型、模擬或我們的結果")
        if re.search(r"模型|模擬", claim) and not (types & ({"model_theory", "review"} | OURS)):
            rep.err(where, "寫了模型或模擬，卻沒有連到模型、綜述或我們的卡")
        pool = [x for c in linked for x in cards[c][1]]
        for num in numbers(claim):
            if not found(num, pool):
                rep.err(where, f"數字 {num} 在連到的卡片裡找不到")
    print(f"\n頁數 {len(pages)}，對照列 {len(rows)}，錯誤 {rep.errors} 個。")
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())

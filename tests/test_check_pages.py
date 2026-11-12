"""故意弄壞逐頁稿、slide-map和證據卡，確認scripts/check_pages.py擋得住。

用法：python3 tests/test_check_pages.py
判定方式跟tests/test_check_wiki.py一樣：預期錯誤時，「[錯誤]」那一行的訊息要以指定的字開頭。
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_check_wiki import judge  # noqa: E402

OUTLINE = "# 大綱\n\n### 第1頁｜一\n\n### 第2頁｜二\n"
GLOSSARY = ("# 術語\n\n| 中文 | 英文 | 其他常見譯名 | 出處或說明 |\n|---|---|---|---|\n"
            "| 塞車團 | jam cluster | — | 說明 |\n| 敏感度 | sensitivity | — | 說明 |\n| 平滑車 | — | — | 我們取的名字 |\n")


def card(cid, typ, claim, limits="限制。"):
    src = "runs/x.log" if typ.startswith("our_") else "demo2000"
    return (f"---\nid: {cid}\ntype: {typ}\nsource: {src}\nlocator: 第1頁\nconditions: 條件\nunits: 無因次\n"
            f"status: confirmed\nrelated: \n---\n\n## 主張\n\n{claim}\n\n## 原文依據\n\n依據。\n\n## 限制\n\n{limits}\n")


CARDS = {
    "exp-a": card("exp-a", "experiment", "真實環道上，22台車的塞車團約20 km/h往後。", limits="只有1場。"),
    "model-a": card("model-a", "model_theory", "模型的分界是1.959494。"),
    "ours-a": card("ours-a", "our_simulation", "我們的模擬量到1.959494。"),
    "der-a": card("der-a", "our_derivation", "公式是1.959493。"),
    "pop-a": card("pop-a", "expression", "科普的說法。"),
}


def L(c):
    return f"[{c}](cards/{c}.md)"


MAP = ("# 對照\n\n| 頁 | 核心主張 | 證據卡 | 層次 |\n|---|---|---|---|\n"
       f"| 1 | 真實環道實驗裡，22台車的塞車團約20 km/h往後 | {L('exp-a')} | 主線 |\n"
       f"| 1 | 模型裡的分界約1.96 | {L('model-a')} | 知識 |\n"
       f"| 2 | 我們的模擬量到分界約1.96 | {L('ours-a')}、{L('der-a')} | 主線 |\n")

P1 = """# 第1頁｜一

- **讀者看完能說出**：一件事。

## 畫面和互動

- 「點一下」看22台車。
1. 第一步看`model/ovm.py`和`runs/2026-11-12-x.md`。

## 顯示設定

- 每秒6個模型時間；畫後面第1、5台。

## 主線

【實驗】2008年的環道上有22台車，塞車團（jam cluster）往後約20 km/h（第2頁）。

## 知識

【模型】模型的分界約1.96，駕駛的這個數字叫敏感度（sensitivity）。

## 進階

用RK4算的。

## 數字從哪來

| 數字 | 用在 | 證據卡 |
|---|---|---|
| 22 | 車數 | exp-a |
| 20 | 波速 | exp-a |
| 1.96 | 分界 | model-a |

## 證據卡

- 【實驗】exp-a
- 【模型】model-a

## 要小心

- 沒有。
"""

P2 = """# 第2頁｜二

## 畫面和互動

- 沒有數字。

## 顯示設定

## 主線

【我們的模擬】我們量到1.959494，塞車團也往後，敏感度不變。

## 知識

## 進階

【我們的推導】公式是1.959493。

## 數字從哪來

| 數字 | 用在 | 證據卡 |
|---|---|---|
| 1.959494 | 量到的 | ours-a |
| 1.959493 | 公式 | der-a |

## 證據卡

- 【我們的模擬】ours-a
- 【我們的推導】der-a

## 要小心

"""


def make_site(tmp):
    (tmp / "scripts").mkdir()
    for s in ("check_pages.py", "check_slide_map.py", "check_wiki.py"):
        shutil.copy(ROOT / "scripts" / s, tmp / "scripts" / s)
    (tmp / "wiki" / "cards").mkdir(parents=True)
    (tmp / "pipeline" / "pages").mkdir(parents=True)
    for cid, text in CARDS.items():
        (tmp / "wiki" / "cards" / f"{cid}.md").write_text(text, encoding="utf-8")
    (tmp / "wiki" / "slide-map.md").write_text(MAP, encoding="utf-8")
    (tmp / "wiki" / "glossary.md").write_text(GLOSSARY, encoding="utf-8")
    (tmp / "pipeline" / "outline.md").write_text(OUTLINE, encoding="utf-8")
    (tmp / "pipeline" / "pages" / "p01.md").write_text(P1, encoding="utf-8")
    (tmp / "pipeline" / "pages" / "p02.md").write_text(P2, encoding="utf-8")


def edit(rel, old, new):
    def f(tmp):
        p = tmp / rel
        t = p.read_text(encoding="utf-8")
        assert old in t, old
        p.write_text(t.replace(old, new, 1), encoding="utf-8")
    return f


def p1(old, new):
    return edit("pipeline/pages/p01.md", old, new)


def remove(rel):
    return lambda tmp: (tmp / rel).unlink()


CASES = [
    ("正常的資料不報錯", lambda t: None, None),
    ("P1 大綱的第2頁沒有逐頁稿", remove("pipeline/pages/p02.md"), "大綱的第2頁沒有逐頁稿"),
    ("P1 標題跟大綱不一樣", p1("# 第1頁｜一", "# 第1頁｜一二"), "第一行要是「# 第1頁｜一」"),
    ("P2 少一個段落", p1("## 顯示設定\n", ""), "缺少段落「## 顯示設定」"),
    ("P2 段落重複", p1("## 要小心\n", "## 要小心\n\n## 要小心\n"), "段落「## 要小心」出現2次"),
    ("P2 段落順序錯", lambda t: (p1("## 主線\n", "## 暫存A\n")(t), p1("## 知識\n", "## 主線\n")(t), p1("## 暫存A\n", "## 知識\n")(t)),
     "段落的順序不對"),
    ("P3 證據卡不存在", p1("- 【模型】model-a", "- 【模型】model-a、ghost-a"), "證據卡 ghost-a 不存在"),
    ("P3 標示跟卡片類型不合", p1("- 【模型】model-a", "- 【模型】model-a、exp-a"), "證據卡 exp-a 的類型是experiment，不能標【模型】"),
    ("P3 不認得的標示", p1("- 【模型】model-a", "- 【模型】model-a\n- 【科普】pop-a"), "證據卡段落用了不認得的標示【科普】"),
    ("P3 逐頁稿多了slide-map沒有的卡", p1("- 【模型】model-a", "- 【模型】model-a\n- 【我們的推導】der-a"),
     "證據卡 der-a 在逐頁稿裡，但slide-map第1頁沒有"),
    ("P3 逐頁稿少了slide-map有的卡", edit("wiki/slide-map.md", "| 2 | 我們的模擬量到分界約1.96 |",
                                      f"| 1 | 模型裡的另一件事 | {L('ours-a')} | 知識 |\n| 2 | 我們的模擬量到分界約1.96 |"),
     "slide-map第1頁有證據卡 ours-a，但逐頁稿沒有"),
    ("P4 文字裡的數字沒有列在表格", p1("往後約20 km/h", "往後約20 km/h，團裡有5台"), "「主線」裡的數字 5 沒有列在數字從哪來"),
    ("P4 畫面和互動的數字也要列", p1("看22台車", "看23台車"), "「畫面和互動」裡的數字 23 沒有列在數字從哪來"),
    ("P4 對照：年份、第N頁、清單編號、反引號檔名、RK4都不算", lambda t: None, None),
    ("P4 對照：顯示設定的數字不用列", p1("每秒6個模型時間", "每秒7個模型時間"), None),
    ("P5 表格的數字在卡片裡找不到", p1("| 1.96 | 分界 | model-a |", "| 1.97 | 分界 | model-a |"),
     "數字 1.97 在數字表寫的證據卡裡找不到"),
    ("P5 1.960不能拿1.959494充數", p1("| 1.96 | 分界 | model-a |", "| 1.960 | 分界 | model-a |"),
     "數字 1.960 在數字表寫的證據卡裡找不到"),
    ("P5 數字只在別張卡裡也不算", p1("| 22 | 車數 | exp-a |", "| 22 | 車數 | model-a |"), "數字 22 在數字表寫的證據卡裡找不到"),
    ("P5 表格用了這頁沒有的卡", p1("| 1.96 | 分界 | model-a |", "| 1.96 | 分界 | ours-a |"),
     "數字表的「1.96」那一列用了證據卡 ours-a，但這頁的證據卡沒有"),
    ("P5 對照：限制裡的數字也算找到", p1("| 22 | 車數 | exp-a |", "| 22、1 | 車數、只有1場 | exp-a |"), None),
    ("P5 標成顯示設定的數字要在顯示設定段落裡", p1("| 22 | 車數 | exp-a |", "| 22 | 車數 | exp-a |\n| 9 | 畫第9台 | 顯示設定 |"),
     "數字表把 9 標成顯示設定，但「顯示設定」段落裡沒有這個數字"),
    ("P5 對照：顯示設定段落裡有的數字可以標顯示設定", p1("| 22 | 車數 | exp-a |", "| 22 | 車數 | exp-a |\n| 5 | 畫第5台 | 顯示設定 |"), None),
    ("P6 術語第一次出現沒有英文", p1("塞車團（jam cluster）往後", "塞車團往後"), "術語「塞車團」第一次出現（主線）要寫成「塞車團（jam cluster）」"),
    ("P6 括號裡的英文不對", p1("敏感度（sensitivity）", "敏感度（delay）"), "術語「敏感度」第一次出現（知識）要寫成「敏感度（sensitivity）」"),
    ("P6 第一次出現在後面的頁也要檢查", lambda t: (p1("塞車團（jam cluster）往後", "車往後")(t)),
     "術語「塞車團」第一次出現（主線）要寫成「塞車團（jam cluster）」"),
    ("P6 對照：第二次出現不用英文、沒有英文的術語不檢查", edit("pipeline/pages/p02.md", "敏感度不變", "敏感度不變，平滑車也一樣"), None),
    ("P7 用了【實驗】卻沒有實驗卡", edit("pipeline/pages/p02.md", "【我們的模擬】我們量到", "【實驗】實驗裡，我們量到"),
     "文字用了【實驗】，但這頁沒有那種類型的證據卡"),
]


def run(tmp):
    r = subprocess.run([sys.executable, "-B", str(tmp / "scripts" / "check_pages.py"), "--root", str(tmp)],
                       capture_output=True, text=True, encoding="utf-8")
    return r.returncode, r.stdout + r.stderr


def main():
    fails = 0
    for name, breaker, expect in CASES:
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            make_site(tmp)
            breaker(tmp)
            code, out = run(tmp)
            ok, want, got = judge(code, out, expect, {})
            fails += not ok
            print(f"[{'PASS' if ok else 'FAIL'}] {name}\n    預期：{want}\n    實際：{got}")
    print(f"\n共{len(CASES)}個情境，失敗{fails}個。")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

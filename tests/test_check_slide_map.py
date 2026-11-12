"""故意弄壞slide-map和證據卡，確認scripts/check_slide_map.py擋得住。

用法：python3 tests/test_check_slide_map.py
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


def card(cid, typ, status="confirmed", claim="一句話。", conditions="條件"):
    src = "runs/x.log" if typ.startswith("our_") else "demo2000"
    return (f"---\nid: {cid}\ntype: {typ}\nsource: {src}\nlocator: 第1頁\nconditions: {conditions}\nunits: 無因次\n"
            f"status: {status}\nrelated: \n---\n\n## 主張\n\n{claim}\n\n## 原文依據\n\n依據。\n\n## 限制\n\n限制。\n")


CARDS = {
    "exp-a": card("exp-a", "experiment", claim="真實環道上，22台車的塞車團約20 km/h往後。"),
    "model-a": card("model-a", "model_theory", claim="模型的分界是1.959494。"),
    "ours-a": card("ours-a", "our_simulation", claim="我們的模擬量到1.959494。"),
    "pop-a": card("pop-a", "expression", claim="科普的說法。"),
    "pend-a": card("pend-a", "experiment", status="pending", claim="還沒確認的實驗。"),
}


def L(c):
    return f"[{c}](cards/{c}.md)"


MAP = ("# 對照\n\n| 頁 | 核心主張 | 證據卡 | 層次 |\n|---|---|---|---|\n"
       f"| 1 | 真實環道實驗裡，22台車的塞車團約20 km/h往後 | {L('exp-a')} | 主線 |\n"
       f"| 2 | 模型裡的分界約1.96 | {L('model-a')}、{L('ours-a')} | 主線 |\n")


def make_site(tmp):
    (tmp / "scripts").mkdir()
    for s in ("check_slide_map.py", "check_wiki.py"):
        shutil.copy(ROOT / "scripts" / s, tmp / "scripts" / s)
    (tmp / "wiki" / "cards").mkdir(parents=True)
    (tmp / "pipeline").mkdir()
    for cid, text in CARDS.items():
        (tmp / "wiki" / "cards" / f"{cid}.md").write_text(text, encoding="utf-8")
    (tmp / "wiki" / "slide-map.md").write_text(MAP, encoding="utf-8")
    (tmp / "pipeline" / "outline.md").write_text(OUTLINE, encoding="utf-8")


def edit_map(old, new):
    def f(tmp):
        p = tmp / "wiki" / "slide-map.md"
        t = p.read_text(encoding="utf-8")
        assert old in t, old
        p.write_text(t.replace(old, new, 1), encoding="utf-8")
    return f


def add_row(row):
    def f(tmp):
        p = tmp / "wiki" / "slide-map.md"
        p.write_text(p.read_text(encoding="utf-8") + row + "\n", encoding="utf-8")
    return f


CASES = [
    ("正常的資料不報錯", lambda t: None, None),
    ("大綱的第2頁沒有對照列", edit_map(f"| 2 | 模型裡的分界約1.96 | {L('model-a')}、{L('ours-a')} | 主線 |\n", ""),
     "第2頁沒有任何對照列"),
    ("一列沒有連到卡", add_row("| 1 | 模型裡的另一件事 | 沿用前面的卡 | 主線 |"), "沒有連到任何證據卡"),
    ("連到不存在的卡", add_row(f"| 1 | 模型裡的另一件事 | {L('ghost')} | 主線 |"), "連結的卡片 ghost 不存在"),
    ("連結文字跟目標不一樣", add_row("| 2 | 模型裡的分界約1.96 | [model-a](cards/ours-a.md) | 主線 |"),
     "連結文字「model-a」跟連到的卡片 ours-a 不一樣"),
    ("主線只靠pending的卡", add_row(f"| 1 | 實驗裡的另一件事 | {L('pend-a')} | 主線 |"),
     "主線的主張至少要有一張confirmed、而且不是expression的卡"),
    ("主線只靠科普的卡", add_row(f"| 1 | 一般人常說的講法 | {L('pop-a')} | 主線 |"),
     "主線的主張至少要有一張confirmed、而且不是expression的卡"),
    ("知識層只靠科普的卡可以", add_row(f"| 1 | 一般人常說的講法 | {L('pop-a')} | 知識 |"), None),
    ("寫了真實卻沒有實驗卡", add_row(f"| 2 | 真實道路上的分界約1.96 | {L('model-a')} | 主線 |"),
     "寫了真實或實驗，卻沒有連到experiment卡"),
    ("寫了真的人卻沒有實驗卡", add_row(f"| 2 | 真的人開車的分界約1.96 | {L('model-a')} | 主線 |"),
     "寫了真實或實驗，卻沒有連到experiment卡"),
    ("只連到我們的卡卻沒寫是模擬", add_row(f"| 2 | 分界約1.96 | {L('ours-a')} | 主線 |"),
     "只連到我們自己的卡，主張要寫明是模型、模擬或我們的結果"),
    ("寫了模型卻只有實驗卡", add_row(f"| 1 | 模型裡的塞車團約20 km/h往後 | {L('exp-a')} | 主線 |"),
     "寫了模型或模擬，卻沒有連到模型、綜述或我們的卡"),
    ("主張的數字在卡片裡找不到", add_row(f"| 2 | 模型裡的分界約1.97 | {L('model-a')} | 主線 |"), "數字 1.97 在連到的卡片裡找不到"),
    ("數字只在沒連到的卡裡也不算", add_row(f"| 1 | 真實環道實驗裡分界約1.96 | {L('exp-a')} | 主線 |"),
     "數字 1.96 在連到的卡片裡找不到"),
    ("1.960不能拿1.959494充數（照小數位數四捨五入）", add_row(f"| 2 | 模型裡的分界約1.960 | {L('model-a')} | 主線 |"), "數字 1.960 在連到的卡片裡找不到"),
    ("年份不當成數字檢查", add_row(f"| 1 | 2008年的真實環道實驗裡塞車團約20 km/h往後 | {L('exp-a')} | 主線 |"), None),
    ("卡片條件裡的數字也算找到", lambda t: (
        (t / "wiki" / "cards" / "exp-a.md").write_text(card("exp-a", "experiment", claim="真實環道上塞車團往後。",
                                                              conditions="環長230 m、22台、約20 km/h"), encoding="utf-8")), None),
]


def run(tmp):
    r = subprocess.run([sys.executable, "-B", str(tmp / "scripts" / "check_slide_map.py"), "--root", str(tmp)],
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

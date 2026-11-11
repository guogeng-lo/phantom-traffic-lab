"""故意弄壞Wiki，確認check_wiki.py擋得住。

用法：python3 tests/test_check_wiki.py
每個情境印出 預期／實際。只用標準函式庫，在暫存資料夾裡跑，不會動到repo。
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "check_wiki.py"

SOURCE = """---
id: demo2000
kind: paper
authors: A. Author, B. Author
year: 2000
title: A demo paper
venue: Demo Journal 1(1)
doi: 10.1234/demo.2000
url: https://example.com/demo
read_status: 全文已讀
read_scope: 全文
independent: 是
---

## 這篇在做什麼
示範用。

## 研究條件
示範用。

## 主要結果
見cards/demo2000-claim.md。

## 限制
示範用。

## ingest紀錄
示範用。
"""

CARD = """---
id: demo2000-claim
type: experiment
source: demo2000
locator: p.3 圖2
conditions: 環狀道路
units: m
status: confirmed
related:
---

## 主張
2000年的實驗裡，22台車繞230m的環。

## 原文依據
> a short quote

## 限制
只有一次實驗。
"""

INDEX = "# 索引\n\n- sources/demo2000.md\n- cards/demo2000-claim.md\n"


def make_site(tmp):
    (tmp / "scripts").mkdir()
    shutil.copy(SCRIPT, tmp / "scripts" / "check_wiki.py")
    (tmp / "wiki" / "sources").mkdir(parents=True)
    (tmp / "wiki" / "cards").mkdir()
    (tmp / "wiki" / "sources" / "demo2000.md").write_text(SOURCE, encoding="utf-8")
    (tmp / "wiki" / "cards" / "demo2000-claim.md").write_text(CARD, encoding="utf-8")
    (tmp / "wiki" / "index.md").write_text(INDEX, encoding="utf-8")


def run(tmp):
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, "-B", str(tmp / "scripts" / "check_wiki.py"), "--root", str(tmp)],
                       capture_output=True, text=True, encoding="utf-8", env=env)
    return r.returncode, r.stdout


def edit(path, old, new):
    t = path.read_text(encoding="utf-8")
    assert old in t, f"測試寫錯了：{path.name} 裡找不到 {old!r}"
    path.write_text(t.replace(old, new, 1), encoding="utf-8")


def S(tmp):
    return tmp / "wiki" / "sources" / "demo2000.md"


def C(tmp):
    return tmp / "wiki" / "cards" / "demo2000-claim.md"


def add_popular(tmp):
    t = SOURCE.replace("demo2000", "news2001").replace("kind: paper", "kind: popular")
    (tmp / "wiki" / "sources" / "news2001.md").write_text(t, encoding="utf-8")
    edit(tmp / "wiki" / "index.md", "- cards", "- sources/news2001.md\n- cards")


CASES = [
    # (名稱, 怎麼弄壞, 預期要出現的字；None代表預期沒有錯誤)
    ("正常資料", lambda t: None, None),
    ("主張裡只有年份，units寫無數值", lambda t: (edit(C(t), "units: m", "units: 無數值"),
                                       edit(C(t), "22台車繞230m的環", "做了實驗")), None),
    ("文獻少一個欄位", lambda t: edit(S(t), "venue: Demo Journal 1(1)\n", ""), "缺少欄位 venue"),
    ("閱讀狀態亂寫", lambda t: edit(S(t), "read_status: 全文已讀", "read_status: 大概讀過"), "read_status 要是"),
    ("DOI格式錯", lambda t: edit(S(t), "doi: 10.1234/demo.2000", "doi: demo"), "doi 格式不對"),
    ("網址不是https", lambda t: edit(S(t), "https://example.com", "http://example.com"), "url 要用 https://"),
    ("文獻少段落", lambda t: edit(S(t), "## 限制\n示範用。\n", ""), "缺少段落「## 限制」"),
    ("證據卡的文獻不存在", lambda t: edit(C(t), "source: demo2000", "source: ghost1999"), "找不到"),
    ("文獻尚未查證，卡片卻是confirmed", lambda t: edit(S(t), "read_status: 全文已讀", "read_status: 尚未查證"),
     "不能是 confirmed"),
    ("只讀摘要，locator沒寫摘要", lambda t: edit(S(t), "read_status: 全文已讀", "read_status: 只讀摘要"),
     "locator 要寫「摘要」"),
    ("科普當成實驗證據", lambda t: (add_popular(t), edit(C(t), "source: demo2000", "source: news2001")),
     "科普或新聞只能當 expression"),
    ("expression引用論文", lambda t: edit(C(t), "type: experiment", "type: expression"),
     "expression 只能引用"),
    ("證據類型亂寫", lambda t: edit(C(t), "type: experiment", "type: guess"), "type 要是"),
    ("有數字但units寫無數值", lambda t: edit(C(t), "units: m", "units: 無數值"), "units 不能寫「無數值」"),
    ("英文原文引用太長", lambda t: edit(C(t), "> a short quote", "> " + "word " * 60), "超過 50"),
    ("證據卡少原文依據", lambda t: edit(C(t), "## 原文依據\n> a short quote\n", ""), "「## 原文依據」"),
    ("自己的模擬指向不存在的檔案", lambda t: (edit(C(t), "type: experiment", "type: our_simulation"),
                                     edit(C(t), "source: demo2000", "source: audition/nope.py")),
     "source 要是repo裡存在的檔案"),
    ("自己的模擬用..跳出repo", lambda t: (edit(C(t), "type: experiment", "type: our_simulation"),
                                    edit(C(t), "source: demo2000", "source: ../etc/passwd")),
     "source 要是repo裡存在的檔案"),
    ("related指到不存在的卡", lambda t: edit(C(t), "related:", "related: nope-card"), "related 的 nope-card 不存在"),
    ("卡片id跟檔名不同", lambda t: edit(C(t), "id: demo2000-claim", "id: other"), "跟檔名不一樣"),
    ("索引沒列卡片", lambda t: edit(t / "wiki" / "index.md", "- cards/demo2000-claim.md\n", ""), "沒有列出證據卡"),
    ("放了PDF", lambda t: (t / "raw.pdf").write_bytes(b"%PDF-1.4"), "PDF不能放進repo"),
    ("檔案裡有像學號的數字", lambda t: (t / "note.md").write_text("學號 412345678\n", encoding="utf-8"),  # privacy-scan: ignore
     "像學號"),
    ("檔案裡有個人信箱", lambda t: (t / "note.md").write_text("someone@gmail.com\n", encoding="utf-8"),  # privacy-scan: ignore
     "電子郵件"),
    ("檔案裡有本機路徑", lambda t: (t / "note.md").write_text("C:\\Users\\me\\a.pdf\n", encoding="utf-8"),  # privacy-scan: ignore
     "本機路徑"),
    ("檔案裡有金鑰", lambda t: (t / "note.md").write_text("key=sk-" + "a" * 30 + "\n", encoding="utf-8"),
     "金鑰或Token"),
]


def main():
    fails = 0
    for name, breaker, expect in CASES:
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            make_site(tmp)
            breaker(tmp)
            code, out = run(tmp)
            if expect is None:
                ok = code == 0
                want, got = "沒有錯誤", ("沒有錯誤" if code == 0 else out.strip())
            else:
                ok = code == 1 and expect in out
                errs = [l for l in out.splitlines() if l.startswith("[錯誤]")]
                want, got = f"錯誤裡有「{expect}」", "；".join(errs) or "沒有錯誤"
            fails += not ok
            print(f"[{'PASS' if ok else 'FAIL'}] {name}\n    預期：{want}\n    實際：{got}")
    print(f"\n共{len(CASES)}個情境，失敗{fails}個。")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

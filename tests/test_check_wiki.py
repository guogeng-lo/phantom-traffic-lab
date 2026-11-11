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


def run(tmp, *args):
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, "-B", str(tmp / "scripts" / "check_wiki.py"), "--root", str(tmp), *args],
                       capture_output=True, text=True, encoding="utf-8", env=env)
    return r.returncode, r.stdout


def git(tmp, *args):
    env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@example.com",
               GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@example.com")
    subprocess.run(["git", *args], cwd=tmp, env=env, check=True, capture_output=True)


def commit_all(tmp, msg):
    git(tmp, "add", "-A")
    git(tmp, "commit", "-q", "-m", msg)


def leak_then_remove(tmp):
    """先commit一個有金鑰的檔案，再刪掉commit：現在的檔案乾淨，但歷史裡還有。"""
    git(tmp, "init", "-q")
    (tmp / "note.md").write_text("key=sk-" + "b" * 30 + "\n", encoding="utf-8")
    commit_all(tmp, "leak")
    (tmp / "note.md").unlink()
    commit_all(tmp, "remove")


def our_card_to_ignored(tmp):
    git(tmp, "init", "-q")
    (tmp / ".gitignore").write_text("local/\n", encoding="utf-8")
    (tmp / "local").mkdir()
    (tmp / "local" / "sim.py").write_text("print(1)\n", encoding="utf-8")
    edit(C(tmp), "type: experiment", "type: our_simulation")
    edit(C(tmp), "source: demo2000", "source: local/sim.py")


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


# 第4個欄位是選項：args＝額外參數；warn＝預期只有警告（結束代碼0）且警告裡有這段字；
# out＝預期結束代碼0且輸出裡有這段字。沒有選項時：None代表預期沒有錯誤，字串代表錯誤裡要有這段字。
CASES = [
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
    ("檔案裡有手機號碼", lambda t: (t / "note.md").write_text("電話 0912-345-678\n", encoding="utf-8"),  # privacy-scan: ignore
     "手機號碼"),
    ("log裡的小數不能誤判成學號或電話", lambda t: (t / "run.log").write_text(
        "rate 1.412345678 / 0.0912345678\n", encoding="utf-8"), None),
    ("欄位重複", lambda t: edit(C(t), "status: confirmed", "status: confirmed\nstatus: pending"),
     "欄位 status 出現不只一次"),
    ("索引列了不存在的卡", lambda t: edit(t / "wiki" / "index.md", "- cards/demo2000-claim.md",
                                    "- cards/demo2000-claim.md\n- cards/deleted-card.md"),
     "cards/deleted-card.md 不存在"),
    ("有數字的主張，locator只寫全文", lambda t: edit(C(t), "locator: p.3 圖2", "locator: 全文"),
     "locator 要到頁碼"),
    ("自己的模擬指向不會上傳的檔案", our_card_to_ignored, "不會上傳的檔案"),
    ("歷史裡有金鑰：平常是警告", leak_then_remove, "金鑰或Token", {"warn": True}),
    ("歷史裡有金鑰：--strict是錯誤", leak_then_remove, "金鑰或Token", {"args": ["--strict"]}),
    ("歷史裡有PDF：--strict是錯誤", lambda t: (git(t, "init", "-q"), (t / "a.pdf").write_bytes(b"%PDF"),
                                         commit_all(t, "pdf"), (t / "a.pdf").unlink(), commit_all(t, "rm")),
     "出現過PDF：a.pdf", {"args": ["--strict"]}),
    ("有confirmed卡的論文才算進5篇", lambda t: None, "算進5篇的獨立論文 1 篇", {"out": True}),
    ("沒有confirmed卡的論文不算", lambda t: edit(C(t), "status: confirmed", "status: pending"),
     "算進5篇的獨立論文 0 篇", {"out": True}),
]


def main():
    fails = 0
    for case in CASES:
        name, breaker, expect = case[:3]
        opt = case[3] if len(case) > 3 else {}
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            make_site(tmp)
            breaker(tmp)
            code, out = run(tmp, *opt.get("args", []))
            if opt.get("warn"):
                warns = [l for l in out.splitlines() if l.startswith("[警告]") and expect in l]
                ok = code == 0 and bool(warns)
                want, got = f"沒有錯誤，警告裡有「{expect}」", out.strip().replace("\n", "；")
            elif opt.get("out"):
                ok = code == 0 and expect in out
                want, got = f"沒有錯誤，輸出裡有「{expect}」", out.strip().splitlines()[-2:]
            elif expect is None:
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

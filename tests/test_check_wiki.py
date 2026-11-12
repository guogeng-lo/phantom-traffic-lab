"""故意弄壞Wiki，確認check_wiki.py擋得住。

用法：python3 tests/test_check_wiki.py
每個情境印出 預期／實際。只用標準函式庫，在暫存資料夾裡跑，不會動到repo。
"""
import os
import shutil
import hashlib
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

INDEX_HEAD = "# 索引\n\n人工寫的導覽。\n\n"
sys.path.insert(0, str(SCRIPT.parent))
from check_wiki import INDEX_BEGIN, INDEX_END  # noqa: E402


def make_site(tmp):
    (tmp / "scripts").mkdir()
    shutil.copy(SCRIPT, tmp / "scripts" / "check_wiki.py")
    shutil.copy(SCRIPT.parent / "build_index.py", tmp / "scripts" / "build_index.py")
    (tmp / "wiki" / "sources").mkdir(parents=True)
    (tmp / "wiki" / "cards").mkdir()
    (tmp / "wiki" / "sources" / "demo2000.md").write_text(SOURCE, encoding="utf-8")
    (tmp / "wiki" / "cards" / "demo2000-claim.md").write_text(CARD, encoding="utf-8")
    (tmp / "wiki" / "index.md").write_text(INDEX_HEAD + INDEX_BEGIN + "\n" + INDEX_END + "\n", encoding="utf-8")
    rebuild(tmp)


def rebuild(tmp):
    """照規定的做法：改了文獻檔或證據卡之後重建索引。"""
    subprocess.run([sys.executable, "-B", str(tmp / "scripts" / "build_index.py"), "--root", str(tmp)],
                   check=True, capture_output=True)


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


# 雜湊值排除的測試用：假學號、假手機只在這兩行出現，其他地方用變數組字串。
# 假資料在執行時才組合，原始碼裡不出現完整的假學號、假手機、假信箱、假路徑（2026-11-12起不再用行內例外標記）
SID = "4" + "12345678"
PHONE = "09" + "12345678"
PHONE_DASH = "09" + "12-345-678"
GMAIL = "someone" + "@gmail.com"
WINPATH = "C:" + "\\Users\\me\\a.pdf"
SHA_TABLE = "| 檔案 | SHA-256 |\n|---|---|\n"


def fake_hash(inner="", n=64):
    """長得像SHA-256的十六進位字串，可以在中間夾一段數字。"""
    return ("ab" * 10 + inner).ljust(n, "c")[:n]


def note(text):
    return lambda t: (t / "note.md").write_text(text, encoding="utf-8")


def history_note(text):
    """先commit一個檔案，再刪掉：現在的檔案乾淨，只剩歷史裡有。"""
    def f(tmp):
        git(tmp, "init", "-q")
        (tmp / "note.md").write_text(text, encoding="utf-8")
        commit_all(tmp, "add")
        (tmp / "note.md").unlink()
        commit_all(tmp, "remove")
    return f


def history_versions(*texts):
    """同一個檔案依序commit好幾個版本，最後刪掉。後面版本的diff只看得到改動附近幾行。"""
    def f(tmp):
        git(tmp, "init", "-q")
        for i, text in enumerate(texts):
            (tmp / "note.md").write_text(text, encoding="utf-8")
            commit_all(tmp, f"v{i}")
        (tmp / "note.md").unlink()
        commit_all(tmp, "remove")
    return f


def broken_textconv(tmp):
    """模擬Git for Windows對PDF和md設了文字轉換、而且轉換程式會失敗的環境。"""
    git(tmp, "init", "-q")
    git(tmp, "config", "diff.boom.textconv", "false")
    (tmp / ".gitattributes").write_text("*.pdf diff=boom\n*.md diff=boom\n", encoding="utf-8")


def textconv_pdf(tmp):
    broken_textconv(tmp)
    (tmp / "a.pdf").write_bytes(b"%PDF")
    commit_all(tmp, "pdf")
    (tmp / "a.pdf").unlink()
    commit_all(tmp, "rm")


def textconv_key(tmp):
    broken_textconv(tmp)
    (tmp / "note.md").write_text("key=sk-" + "c" * 30 + "\n", encoding="utf-8")
    commit_all(tmp, "leak")
    (tmp / "note.md").unlink()
    commit_all(tmp, "remove")


def corrupt_history(tmp):
    """刪掉Git裡一個檔案內容的物件，讓git log -p失敗。"""
    git(tmp, "init", "-q")
    (tmp / "note.md").write_text("hello\n", encoding="utf-8")
    commit_all(tmp, "add")
    blob = subprocess.run(["git", "rev-parse", "HEAD:note.md"], cwd=tmp, capture_output=True,
                          text=True, check=True).stdout.strip()
    obj = tmp / ".git" / "objects" / blob[:2] / blob[2:]
    obj.chmod(0o644)
    obj.unlink()


def claim_add(tmp, text):
    edit(C(tmp), "22台車繞230m的環。", "22台車繞230m的環。" + text)
    rebuild(tmp)


def line_hash(line):
    return hashlib.sha256(line.encode("utf-8")).hexdigest()


def head(tmp):
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=tmp, capture_output=True, text=True, check=True).stdout.strip()


FAKE_KEY = "key=sk-" + "d" * 30
ALLOW = "scripts/privacy_allowlist.tsv"


def write_allow(tmp, rows_):
    (tmp / ALLOW).write_text("# commit\tpath\tsha256\trule\treason\n" + "".join("\t".join(r) + "\n" for r in rows_),
                             encoding="utf-8")


def allow_history(same_commit=True, same_path=True):
    """note.md加了一行假金鑰又刪掉，例外清單列那個commit、那個檔案、那一行的雜湊。"""
    def f(tmp):
        git(tmp, "init", "-q")
        (tmp / "note.md").write_text(FAKE_KEY + "\n", encoding="utf-8")
        commit_all(tmp, "add")
        first = head(tmp)
        (tmp / "note.md").unlink()
        commit_all(tmp, "remove")
        if not same_commit:  # 同樣內容在另一個commit又加一次，清單只列第一次
            (tmp / "note.md").write_text(FAKE_KEY + "\n", encoding="utf-8")
            commit_all(tmp, "again")
            (tmp / "note.md").unlink()
            commit_all(tmp, "remove again")
        write_allow(tmp, [(first, "note.md" if same_path else "other.md", line_hash(FAKE_KEY), "金鑰或Token", "測試用的假金鑰")])
    return f


def allow_current(tmp):
    git(tmp, "init", "-q")
    (tmp / "note.md").write_text(FAKE_KEY + "\n" + FAKE_KEY + "x\n", encoding="utf-8")
    commit_all(tmp, "add")
    write_allow(tmp, [(head(tmp), "note.md", line_hash(FAKE_KEY), "金鑰或Token", "測試用的假金鑰")])


def fenced(fence):
    return note(fence + "\n" + SHA_TABLE + f"| `a.md` | `{fake_hash(SID)}` |\n" + fence + "\n")


def broken_head(tmp):
    git(tmp, "init", "-q")
    (tmp / "note.md").write_text(FAKE_KEY + "\n", encoding="utf-8")
    commit_all(tmp, "add")
    (tmp / "note.md").unlink()
    commit_all(tmp, "remove")
    git(tmp, "branch", "keep")
    (tmp / ".git" / "HEAD").write_text("ref: refs/heads/nowhere\n", encoding="utf-8")


def merge_only(tmp):
    git(tmp, "init", "-q")
    git(tmp, "checkout", "-q", "-b", "main")
    commit_all(tmp, "base")
    git(tmp, "checkout", "-q", "-b", "side")
    (tmp / "b.md").write_text("b\n", encoding="utf-8")
    commit_all(tmp, "side")
    git(tmp, "checkout", "-q", "main")
    (tmp / "c.md").write_text("c\n", encoding="utf-8")
    commit_all(tmp, "main")
    subprocess.run(["git", "merge", "--no-ff", "--no-commit", "side"], cwd=tmp, capture_output=True)
    (tmp / "m.md").write_text(FAKE_KEY + "\n", encoding="utf-8")
    commit_all(tmp, "merge")
    (tmp / "m.md").unlink()
    commit_all(tmp, "remove")


def quoted(kind):
    def f(tmp):
        git(tmp, "init", "-q")
        git(tmp, "config", "core.quotePath", "true")
        if kind == "pdf":
            (tmp / "論文.pdf").write_bytes(b"%PDF")
            commit_all(tmp, "pdf")
            (tmp / "論文.pdf").unlink()
            commit_all(tmp, "rm")
        else:
            (tmp / "中文.md").write_text(FAKE_KEY + "\n", encoding="utf-8")
            commit_all(tmp, "add")
            if kind == "history":
                (tmp / "中文.md").unlink()
                commit_all(tmp, "rm")
    return f


def rows(n, cell=None):
    return "".join(f"| `f{i}.md` | `{cell or fake_hash()}` |\n" for i in range(n))


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
    rebuild(tmp)


# 第4個欄位是選項：args＝額外參數；warn＝預期只有警告（結束代碼0）且警告裡有這段字；
# out＝預期結束代碼0且輸出裡有這段字。沒有選項時：None代表預期沒有錯誤，字串代表錯誤裡要有這段字。
CASES = [
    ("正常資料", lambda t: None, None),
    ("主張裡只有年份，units寫無數值", lambda t: (edit(C(t), "units: m", "units: 無數值"),
                                       edit(C(t), "22台車繞230m的環", "做了實驗"), rebuild(t)), None),
    ("文獻少一個欄位", lambda t: edit(S(t), "venue: Demo Journal 1(1)\n", ""), "缺少欄位 venue"),
    ("閱讀狀態亂寫", lambda t: edit(S(t), "read_status: 全文已讀", "read_status: 大概讀過"), "read_status 要是"),
    ("DOI格式錯", lambda t: edit(S(t), "doi: 10.1234/demo.2000", "doi: demo"), "doi 格式不對"),
    ("網址不是https", lambda t: edit(S(t), "https://example.com", "http://example.com"), "url 要用 https://"),
    ("文獻少段落", lambda t: edit(S(t), "## 限制\n示範用。\n", ""), "缺少段落「## 限制」"),
    ("證據卡的文獻不存在", lambda t: edit(C(t), "source: demo2000", "source: ghost1999"), "source ghost1999 在 wiki/sources/ 裡找不到"),
    ("文獻尚未查證，卡片卻是confirmed", lambda t: edit(S(t), "read_status: 全文已讀", "read_status: 尚未查證"),
     "demo2000 還是「尚未查證」，卡片不能是 confirmed"),
    ("只讀摘要，locator沒寫摘要", lambda t: edit(S(t), "read_status: 全文已讀", "read_status: 只讀摘要"),
     "demo2000 只讀了摘要，locator 要寫「摘要」"),
    ("科普當成實驗證據", lambda t: (add_popular(t), edit(C(t), "source: demo2000", "source: news2001")),
     "科普或新聞只能當 expression"),
    ("expression引用論文", lambda t: edit(C(t), "type: experiment", "type: expression"),
     "expression 只能引用"),
    ("證據類型亂寫", lambda t: edit(C(t), "type: experiment", "type: guess"), "type 要是"),
    ("有數字但units寫無數值", lambda t: edit(C(t), "units: m", "units: 無數值"), "主張裡有數字，units 不能寫「無數值」"),
    ("英文原文引用太長", lambda t: edit(C(t), "> a short quote", "> " + "word " * 60), "英文原文引用 60 個字，超過 50"),
    ("證據卡少原文依據", lambda t: edit(C(t), "## 原文依據\n> a short quote\n", ""), "缺少段落或段落是空的「## 原文依據」"),
    ("自己的模擬指向不存在的檔案", lambda t: (edit(C(t), "type: experiment", "type: our_simulation"),
                                     edit(C(t), "source: demo2000", "source: audition/nope.py")),
     "source 要是repo裡存在的檔案"),
    ("自己的模擬用..跳出repo", lambda t: (edit(C(t), "type: experiment", "type: our_simulation"),
                                    edit(C(t), "source: demo2000", "source: ../etc/passwd")),
     "source 要是repo裡存在的檔案"),
    ("related指到不存在的卡", lambda t: edit(C(t), "related:", "related: nope-card"), "related 的 nope-card 不存在"),
    ("卡片id跟檔名不同", lambda t: edit(C(t), "id: demo2000-claim", "id: other"), "id other 跟檔名不一樣"),
    ("索引沒列卡片", lambda t: edit(t / "wiki" / "index.md", "(cards/demo2000-claim.md)", ""), "沒有列出證據卡"),
    ("放了PDF", lambda t: (t / "raw.pdf").write_bytes(b"%PDF-1.4"), "PDF不能放進repo"),
    ("檔案裡有像學號的數字", lambda t: (t / "note.md").write_text("學號 " + SID + "\n", encoding="utf-8"),
     "疑似像學號"),
    ("檔案裡有個人信箱", lambda t: (t / "note.md").write_text(GMAIL + "\n", encoding="utf-8"),
     "疑似電子郵件"),
    ("檔案裡有本機路徑", lambda t: (t / "note.md").write_text(WINPATH + "\n", encoding="utf-8"),
     "疑似本機路徑"),
    ("檔案裡有金鑰", lambda t: (t / "note.md").write_text("key=sk-" + "a" * 30 + "\n", encoding="utf-8"),
     "疑似金鑰或Token"),
    ("檔案裡有手機號碼", lambda t: (t / "note.md").write_text("電話 " + PHONE_DASH + "\n", encoding="utf-8"),
     "疑似手機號碼"),
    ("log裡的小數不能誤判成學號或電話", lambda t: (t / "run.log").write_text(
        "rate 1.412345678 / 0.0912345678\n", encoding="utf-8"), None),
    ("欄位重複", lambda t: edit(C(t), "status: confirmed", "status: confirmed\nstatus: pending"),
     "欄位 status 出現不只一次"),
    ("索引列了不存在的卡", lambda t: edit(t / "wiki" / "index.md", "人工寫的導覽。",
                                    "人工寫的導覽。見[舊卡](cards/deleted-card.md)。"),
     "列出的 cards/deleted-card.md 不存在"),
    ("有數字的主張，locator只寫全文", lambda t: edit(C(t), "locator: p.3 圖2", "locator: 全文"),
     "主張裡有數字，locator 要到頁碼"),
    ("自己的模擬指向不會上傳的檔案", our_card_to_ignored, "source local/sim.py 是不會上傳的檔案"),
    ("歷史裡有金鑰：平常是警告", leak_then_remove, "疑似金鑰或Token", {"warn": True}),
    ("歷史裡有金鑰：--strict是錯誤", leak_then_remove, "疑似金鑰或Token", {"args": ["--strict"]}),
    ("歷史裡有PDF：--strict是錯誤", lambda t: (git(t, "init", "-q"), (t / "a.pdf").write_bytes(b"%PDF"),
                                         commit_all(t, "pdf"), (t / "a.pdf").unlink(), commit_all(t, "rm")),
     "出現過PDF：a.pdf", {"args": ["--strict"]}),
    ("有confirmed卡的論文才算進5篇", lambda t: None, "算進5篇的獨立論文 1 篇", {"out": True}),
    ("沒有confirmed卡的論文不算", lambda t: (edit(C(t), "status: confirmed", "status: pending"), rebuild(t)),
     "算進5篇的獨立論文 0 篇", {"out": True}),
    # 以下是雜湊值排除（2026-11-11，看到n3-package-r2.md的SHA-256被誤判成學號之後才加的）
    ("SHA-256表格裡的雜湊值不算學號", note(SHA_TABLE + f"| `a.md` | `{fake_hash(SID)}` |\n"), None),
    ("SHA-256表格裡的雜湊值不算手機", note(SHA_TABLE + f"| `a.md` | `{fake_hash(PHONE)}` |\n"), None),
    ("SHA-256欄的雜湊後面接說明也排除",
     note("| 檔案 | SHA-256（第2輪後） |\n|---|---|\n" + f"| `a.md` | `{fake_hash(SID)}`（第2輪修改後） |\n"), None),
    ("同一行有SHA-256標記的雜湊值不算學號", note(f"PDF的SHA-256 `{fake_hash(SID)}`\n"), None),
    ("學號緊接中文照樣偵測", note(f"學號{SID}\n"), "疑似像學號的9位數字"),
    ("學號夾在英文字母中照樣偵測", note(f"id{SID}x\n"), "疑似像學號的9位數字"),
    ("沒有分隔的手機號碼照樣偵測", note(f"電話{PHONE}\n"), "疑似手機號碼"),
    ("一般句子裡的學號照樣偵測", note(f"請{SID}同學到辦公室\n"), "疑似像學號的9位數字"),
    ("沒有SHA-256標記的64位十六進位不放行", note(f"commit `{fake_hash(SID)}`\n"), "疑似像學號的9位數字"),
    ("SHA-256欄裡只有63位不放行", note(SHA_TABLE + f"| `a.md` | `{fake_hash(SID, 63)}` |\n"), "疑似像學號的9位數字"),
    ("SHA-256欄裡沒有反引號不放行", note(SHA_TABLE + f"| `a.md` | {fake_hash(SID)} |\n"), "疑似像學號的9位數字"),
    ("雜湊放在SHA-256以外的欄不放行",
     note("| 檔案 | SHA-256 | 備註 |\n|---|---|---|\n" + f"| `a.md` | `{fake_hash()}` | `{fake_hash(SID)}` |\n"),
     "疑似像學號的9位數字"),
    ("表格結束後的雜湊不放行", note(SHA_TABLE + f"| `a.md` | `{fake_hash()}` |\n\n`{fake_hash(SID)}`\n"),
     "疑似像學號的9位數字"),
    ("SHA-256表格同一列的學號照樣偵測",
     note(SHA_TABLE + f"| `a.md` | `{fake_hash()}` | 學號{SID} |\n"), "疑似像學號的9位數字"),
    ("SHA-256表格同一列的金鑰照樣偵測",
     note(SHA_TABLE + f"| `sk-{'a' * 30}` | `{fake_hash(SID)}` |\n"), "疑似金鑰或Token"),
    ("歷史裡SHA-256表格的雜湊不算學號（--strict）",
     history_note(SHA_TABLE + f"| `a.md` | `{fake_hash(SID)}` |\n"), None, {"args": ["--strict"]}),
    ("歷史裡沒有標記的雜湊照樣抓（--strict）",
     history_note(f"commit `{fake_hash(SID)}`\n"), "疑似像學號的9位數字", {"args": ["--strict"]}),
    # 以下是歷史掃描改讀完整檔案（2026-11-11，看到4462639的diff看不到表頭、雜湊被誤判之後才加的）
    ("歷史：SHA-256表格中間加一列，diff看不到表頭也排除（--strict）",
     history_versions(SHA_TABLE + rows(10), SHA_TABLE + rows(10) + f"| `x.md` | `{fake_hash(SID)}` |\n"),
     None, {"args": ["--strict"]}),
    ("歷史：SHA-256表格中間加的那列有金鑰照樣抓（--strict）",
     history_versions(SHA_TABLE + rows(10), SHA_TABLE + rows(10) + f"| `sk-{'a' * 30}` | `{fake_hash(SID)}` |\n"),
     "疑似金鑰或Token", {"args": ["--strict"]}),
    ("歷史：SHA-256表格中間加的那列有學號照樣抓（--strict）",
     history_versions(SHA_TABLE + rows(10), SHA_TABLE + rows(10) + f"| `學號{SID}` | `{fake_hash()}` |\n"),
     "疑似像學號的9位數字", {"args": ["--strict"]}),
    ("歷史：表格結束很久之後加的雜湊照樣抓（--strict）",
     history_versions(SHA_TABLE + rows(10) + "\n說明\n" * 5,
                      SHA_TABLE + rows(10) + "\n說明\n" * 5 + f"`{fake_hash(SID)}`\n"),
     "疑似像學號的9位數字", {"args": ["--strict"]}),
    ("歷史：沒有SHA-256欄的表格加雜湊照樣抓（--strict）",
     history_versions("| 檔案 | 備註 |\n|---|---|\n" + rows(10),
                      "| 檔案 | 備註 |\n|---|---|\n" + rows(10) + f"| `x.md` | `{fake_hash(SID)}` |\n"),
     "疑似像學號的9位數字", {"args": ["--strict"]}),
    # 以下是索引自動產生和同步檢查（2026-11-12，第2、3輪審查發現手寫的索引摘要沒跟著卡片更新之後才加的）
    ("改了卡片的主張沒重建索引要擋", lambda t: edit(C(t), "22台車繞230m的環", "22台車繞260m的環"), "跟文獻檔、證據卡不同步"),
    ("改了卡片的狀態沒重建索引要擋", lambda t: edit(C(t), "status: confirmed", "status: pending"), "跟文獻檔、證據卡不同步"),
    ("改了卡片的條件沒重建索引要擋", lambda t: edit(C(t), "conditions: 環狀道路", "conditions: 直線道路"), "跟文獻檔、證據卡不同步"),
    ("改了文獻的閱讀狀態沒重建索引要擋",
     lambda t: (edit(S(t), "read_status: 全文已讀", "read_status: 部分章節"), edit(S(t), "read_scope: 全文", "read_scope: 第1節")),
     "跟文獻檔、證據卡不同步"),
    ("新增卡片沒重建索引要擋",
     lambda t: (t / "wiki" / "cards" / "demo2000-second.md").write_text(CARD.replace("demo2000-claim", "demo2000-second"),
                                                                       encoding="utf-8"), "跟文獻檔、證據卡不同步"),
    ("手改自動產生的摘要要擋", lambda t: edit(t / "wiki" / "index.md", "22台車繞230m的環", "22台車繞環"), "跟文獻檔、證據卡不同步"),
    ("自動產生的標記被刪掉要擋",
     lambda t: edit(t / "wiki" / "index.md", "<!-- 自動產生結束 -->", ""), "找不到自動產生區塊的標記"),
    ("改了卡片也重建索引就通過", lambda t: (edit(C(t), "22台車繞230m的環", "22台車繞260m的環"), rebuild(t)), None),
    ("改人工寫的導覽不用重建", lambda t: edit(t / "wiki" / "index.md", "人工寫的導覽。", "人工寫的導覽，改過。"), None),
    ("主張裡的相對連結在索引裡改成從wiki出發",
     lambda t: (edit(C(t), "22台車繞230m的環。", "22台車繞230m的環，見[本卡](demo2000-claim.md)。"), rebuild(t),
                edit(t / "wiki" / "index.md", "見[本卡](cards/demo2000-claim.md)", "見[本卡](cards/demo2000-claim.md)")),
     None),
    # 以下是第4輪工程審查的反例（2026-11-12，看到審查結果之後才加的）
    ("偽表頭：資料列有SHA-256格，下一列同欄的雜湊不放行",
     note("| 值 | 說明 |\n|---|---|\n| SHA-256 | x |\n" + f"| `{fake_hash(SID)}` | y |\n"), "疑似像學號的9位數字"),
    ("表頭後面沒有分隔列，不算表格，不放行",
     note("| 檔案 | SHA-256 |\n" + f"| `a.md` | `{fake_hash(SID)}` |\n"), "疑似像學號的9位數字"),
    ("表頭寫SHA-256之外的字（SHA-256值或備註），不放行",
     note("| 檔案 | SHA-256值或備註 |\n|---|---|\n" + f"| `a.md` | `{fake_hash(SID)}` |\n"), "疑似像學號的9位數字"),
    ("資料列的格數跟表頭不同，不放行",
     note(SHA_TABLE + f"| `a.md` | `{fake_hash(SID)}` | 多一格 |\n"), "疑似像學號的9位數字"),
    ("SHA-256欄的雜湊後面接的不是括號說明，不放行",
     note(SHA_TABLE + f"| `a.md` | `{fake_hash(SID)}`附註 |\n"), "疑似像學號的9位數字"),
    ("NotSHA-256這種標記不放行", note(f"NotSHA-256 `{fake_hash(PHONE)}`\n"), "疑似手機號碼"),
    ("SHA-256-old這種標記不放行", note(f"SHA-256-old `{fake_hash(PHONE)}`\n"), "疑似手機號碼"),
    ("偽表頭那列同一行的信箱照樣抓",
     note("| 值 | 說明 |\n|---|---|\n| SHA-256 | " + GMAIL + " |\n"), "疑似電子郵件"),
    ("索引的起訖標記重複要擋",
     lambda t: (t / "wiki" / "index.md").write_text(
         (t / "wiki" / "index.md").read_text(encoding="utf-8") + INDEX_BEGIN + "\n過期內容\n" + INDEX_END + "\n",
         encoding="utf-8"), "找不到自動產生區塊的標記，或標記不合規定（標記要各出現一次"),
    ("索引的標記沒有獨立成行要擋", lambda t: edit(t / "wiki" / "index.md", INDEX_END, "結尾" + INDEX_END), "找不到自動產生區塊的標記，或標記不合規定（標記要各出現一次"),
    ("索引的結束標記在開始標記前面要擋",
     lambda t: (t / "wiki" / "index.md").write_text(
         INDEX_HEAD + INDEX_END + "\n" + INDEX_BEGIN + "\n", encoding="utf-8"), "找不到自動產生區塊的標記，或標記不合規定（標記要各出現一次"),
    ("卡片有兩個「## 主張」要擋",
     lambda t: edit(C(t), "## 主張\n", "## 主張\n插進來的另一段。\n\n## 主張\n"), "段落「## 主張」出現不只一次"),
    ("卡片有兩個「## 限制」要擋", lambda t: edit(C(t), "## 限制\n", "## 限制\n第一段。\n\n## 限制\n"),
     "段落「## 限制」出現不只一次"),
    ("主張裡的錨點連結在索引裡指回那張卡", lambda t: claim_add(t, "見[限制](#限制)。"), None,
     {"files": [("wiki/index.md", "見[限制](cards/demo2000-claim.md#限制)。", True)]}),
    ("主張裡行內程式碼的連結字樣不改", lambda t: claim_add(t, "寫法是`[x](y.md)`。"), None,
     {"files": [("wiki/index.md", "寫法是`[x](y.md)`。", True)]}),
    ("主張裡程式碼區塊的連結字樣不改", lambda t: claim_add(t, "\n\n```\n[x](y.md)\n```"), None,
     {"files": [("wiki/index.md", "```\n[x](y.md)\n```", True)]}),
    ("Git設了會失敗的textconv，歷史裡的PDF照樣報（--strict）", textconv_pdf, "出現過PDF：a.pdf",
     {"args": ["--strict"]}),
    ("Git設了會失敗的textconv，歷史裡的金鑰照樣抓（--strict）", textconv_key, "疑似金鑰或Token", {"args": ["--strict"]}),
    ("Git指令失敗要報錯，不能當成沒問題", corrupt_history, "Git指令失敗"),
    ("Git指令失敗在--strict也要報錯", corrupt_history, "Git指令失敗", {"args": ["--strict"]}),
    # 以下是固定反例清單（runs/2026-11-12-eng-acceptance-v2.md，在修程式之前先commit）
    ("F01 行內寫privacy-scan: ignore不再免檢", note(FAKE_KEY + "  # privacy-scan: ignore\n"), "疑似金鑰或Token"),
    ("F02 受控例外：commit、檔案、內容都對得上就不報（--strict）", allow_history(), None, {"args": ["--strict"]}),
    ("F03 受控例外：同樣內容在清單沒列的commit照樣報（--strict）", allow_history(same_commit=False), "疑似金鑰或Token",
     {"args": ["--strict"]}),
    ("F04 受控例外：清單列的是別的檔案就照樣報（--strict）", allow_history(same_path=False), "疑似金鑰或Token",
     {"args": ["--strict"]}),
    ("F05 受控例外：目前檔案只排除對得上的那一行", allow_current, "疑似金鑰或Token", {"absent": ["note.md:1："]}),
    ("F06 受控例外清單格式錯要擋", lambda t: (t / ALLOW).write_text("abc\tnote.md\n", encoding="utf-8"),
     "privacy_allowlist.tsv"),
    ("F07 三個反引號的程式碼區塊裡的假SHA-256表格不放行", fenced("```"), "疑似像學號的9位數字"),
    ("F08 三個波浪號的程式碼區塊裡的假SHA-256表格不放行", fenced("~~~"), "疑似像學號的9位數字"),
    ("F09 全形的ＮｏｔSHA-256不算標記", note(f"ＮｏｔSHA-256 `{fake_hash(PHONE)}`\n"), "疑似手機號碼"),
    ("F10 對照：中文接SHA-256標記照樣排除", note(f"這個PDF的SHA-256 `{fake_hash(PHONE)}`\n"), None),
    ("F11 學號後面接英文句點照樣偵測", note(f"id {SID}.\n"), "疑似像學號的9位數字"),
    ("F12 手機後面接英文句點照樣偵測", note(f"tel {PHONE}.\n"), "疑似手機號碼"),
    ("F13 對照：小數不算學號或手機", note("x = " + SID + ".5，y = 0." + PHONE + "\n"), None),
    ("F14 信箱網域example.com.invalid照樣偵測", note("a" + "@example.com.invalid\n"), "疑似電子郵件"),
    ("F15 對照：網域剛好是example.com或GitHub的noreply不算", note("a" + "@example.com、1+u" + "@users.noreply.github.com\n"),
     None),
    ("F16 Windows路徑寫小寫users照樣偵測", note("c:" + "\\users\\me\\a.txt\n"), "疑似本機路徑"),
    ("F17 金鑰緊接中文照樣偵測", note("金鑰" + FAKE_KEY[4:] + "\n"), "疑似金鑰或Token"),
    ("F18 座號緊接中文照樣偵測", note("座號" + "I3" + "A15號\n"), "疑似班級座號"),
    ("F19 對照：座號格式夾在英文型號中間不算", note("型號ABI" + "3A15X\n"), None),
    ("F21 「##  主張」多一個空格也算重複", lambda t: edit(C(t), "## 主張\n", "##  主張\n另一段。\n\n## 主張\n"),
     "段落「## 主張」出現不只一次"),
    ("F22 主張的程式碼區塊裡有「## example」不會截斷主張",
     lambda t: claim_add(t, "\n\n```\n## example\n```\n\n區塊後面的正文。"), None,
     {"files": [("wiki/index.md", "區塊後面的正文。", True)]}),
    ("F23 卡片有兩個「## 主張」時build_index.py --check也要失敗",
     lambda t: edit(C(t), "## 主張\n", "## 主張\n插進來的另一段。\n\n## 主張\n"), "段落「## 主張」出現不只一次",
     {"build_check": 1}),
    ("F24 帶title的錨點也指回那張卡", lambda t: claim_add(t, '見[限制](#限制 "提示")。'), None,
     {"files": [("wiki/index.md", '見[限制](cards/demo2000-claim.md#限制 "提示")。', True)]}),
    ("F25 雙反引號的程式碼不改", lambda t: claim_add(t, "寫法是``[x](y.md)``。"), None,
     {"files": [("wiki/index.md", "寫法是``[x](y.md)``。", True)]}),
    ("F26 波浪號程式碼區塊不改", lambda t: claim_add(t, "\n\n~~~\n[x](y.md)\n~~~"), None,
     {"files": [("wiki/index.md", "~~~\n[x](y.md)\n~~~", True)]}),
    ("F27 行內程式碼裡的連結字樣不當成連結檢查", lambda t: claim_add(t, "寫法是`[x](cards/absent.md)`。"), None),
    ("F28 HEAD壞掉但還有別的分支：報錯，而且照樣掃出歷史裡的金鑰（--strict）", broken_head, "HEAD無法解析",
     {"args": ["--strict"], "also": ["疑似金鑰或Token"]}),
    ("F28 HEAD壞掉但還有別的分支：一般模式也要報錯", broken_head, "HEAD無法解析"),
    ("F29 只在merge commit加的金鑰照樣抓（--strict）", merge_only, "疑似金鑰或Token", {"args": ["--strict"]}),
    ("F30 core.quotePath下中文檔名的PDF進過歷史照樣報（--strict）", quoted("pdf"), "出現過PDF：論文.pdf",
     {"args": ["--strict"]}),
    ("F31 core.quotePath下中文檔名的檔案裡的金鑰照樣抓", quoted("current"), "疑似金鑰或Token"),
    ("F32 core.quotePath下中文檔名的檔案進過歷史，金鑰照樣抓（--strict）", quoted("history"), "疑似金鑰或Token",
     {"args": ["--strict"]}),
    ("F33 對照：剛git init還沒有commit不報錯（--strict）", lambda t: git(t, "init", "-q"), None, {"args": ["--strict"]}),
]


def judge(code, out, expect, opt):
    """判斷一個情境過不過。預期錯誤時，「[錯誤]」那一行的訊息一定要以指定的字開頭，
    不能靠警告行或其他無關的錯誤湊出結束代碼1。（2026-11-12第4輪審查指出原本只在整份輸出找關鍵字。）"""
    lines = out.splitlines()
    errs = [l for l in lines if l.startswith("[錯誤]")]
    if opt.get("warn"):
        warns = [l for l in lines if l.startswith("[警告]") and expect in l]
        return code == 0 and not errs and bool(warns), f"沒有錯誤，警告裡有「{expect}」", out.strip().replace("\n", "；")
    if opt.get("out"):
        return code == 0 and not errs and expect in out, f"沒有錯誤，輸出裡有「{expect}」", lines[-2:]
    if expect is None:
        ok = code == 0 and not errs
        return ok, "沒有錯誤", ("沒有錯誤" if ok else out.strip())
    ok = code == 1 and any(error_message(l).startswith(expect) for l in errs)
    return ok, f"「[錯誤]」那一行的訊息以「{expect}」開頭", "；".join(errs) or out.strip() or "沒有錯誤"


def error_message(line):
    """「[錯誤] 位置：訊息」只取訊息。只比對訊息開頭，欄位內容剛好有同樣的字也騙不了。
    （2026-11-12工程審查指出：related欄位寫了「金鑰或Token」，舊判定會把「related 的 金鑰或Token 不存在」當成偵測到金鑰。）"""
    return line.split("：", 1)[1] if "：" in line else ""


# 檢查judge本身：故意給它會騙過舊寫法的輸出
JUDGE_CASES = [
    ("關鍵字只在警告行，另有無關錯誤：不能算通過",
     (1, "[警告] x：疑似金鑰或Token\n[錯誤] y：無關的錯誤\n", "疑似金鑰或Token", {}), False),
    ("訊息以預期的字開頭：算通過", (1, "[錯誤] note.md:1：疑似金鑰或Token\n", "疑似金鑰或Token", {}), True),
    ("F20 預期的字只出現在別的錯誤訊息中間（related欄位）：不能算通過",
     (1, "[錯誤] wiki/cards/x.md：related 的 金鑰或Token 不存在\n", "疑似金鑰或Token", {}), False),
    ("F20 預期的字出現在位置欄（檔名）裡：不能算通過",
     (1, "[錯誤] 疑似金鑰或Token.md：缺少欄位 venue\n", "疑似金鑰或Token", {}), False),
    ("結束代碼1但沒有任何錯誤行（例如程式當掉）：不能算通過",
     (1, "Traceback (most recent call last):\n  金鑰或Token\n", "疑似金鑰或Token", {}), False),
    ("預期沒有錯誤，卻有錯誤行：不能算通過", (0, "[錯誤] x：y\n", None, {}), False),
    ("預期只有警告，卻也有錯誤行：不能算通過", (0, "[錯誤] a\n[警告] b：金鑰或Token\n", "疑似金鑰或Token", {"warn": True}), False),
]


def main():
    fails = 0
    for name, args, want_ok in JUDGE_CASES:
        ok = judge(*args)[0] == want_ok
        fails += not ok
        print(f"[{'PASS' if ok else 'FAIL'}] 判定規則：{name}")
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        make_site(tmp)
        edit(C(tmp), "related:", "related: 疑似金鑰或Token")
        code, out = run(tmp)
        ok = code == 1 and judge(code, out, "疑似金鑰或Token", {})[0] is False
        fails += not ok
        print(f"[{'PASS' if ok else 'FAIL'}] 判定規則：F20 用實際檢查程式的輸出：卡片沒有金鑰、related寫了那幾個字，不能判成偵測到金鑰")
    for case in CASES:
        name, breaker, expect = case[:3]
        opt = case[3] if len(case) > 3 else {}
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            make_site(tmp)
            breaker(tmp)
            code, out = run(tmp, *opt.get("args", []))
            ok, want, got = judge(code, out, expect, opt)
            errs = [error_message(l) for l in out.splitlines() if l.startswith("[錯誤]")]
            for extra in opt.get("also", []):
                want = f"{want}；也要有以「{extra}」開頭的錯誤"
                if not any(e.startswith(extra) for e in errs):
                    ok, got = False, f"{got}；缺少「{extra}」"
            for bad in opt.get("absent", []):
                want = f"{want}；錯誤行裡不能有「{bad}」"
                if any(bad in l for l in out.splitlines() if l.startswith("[錯誤]")):
                    ok, got = False, f"{got}；錯誤行裡有「{bad}」"
            if "build_check" in opt:
                r = subprocess.run([sys.executable, "-B", str(tmp / "scripts" / "build_index.py"), "--root", str(tmp),
                                    "--check"], capture_output=True, text=True, encoding="utf-8")
                want = f"{want}；build_index.py --check結束代碼{opt['build_check']}"
                if r.returncode != opt["build_check"]:
                    ok, got = False, f"{got}；build_index.py --check結束代碼{r.returncode}"
            for rel, text, present in opt.get("files", []):
                content = (tmp / rel).read_text(encoding="utf-8")
                if (text in content) != present:
                    ok = False
                    got = f"{got}；{rel}裡{'找不到' if present else '不該有'}「{text}」"
                want = f"{want}；{rel}裡{'要有' if present else '不能有'}「{text}」"
            fails += not ok
            print(f"[{'PASS' if ok else 'FAIL'}] {name}\n    預期：{want}\n    實際：{got}")
    total = len(CASES) + len(JUDGE_CASES) + 1
    print(f"\n共{total}個情境（其中判定規則{len(JUDGE_CASES) + 1}個），失敗{fails}個。")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

"""檢查Wiki的文獻檔、證據卡、索引，並掃描個資和金鑰。

用法：python3 scripts/check_wiki.py [--root 路徑] [--strict]
錯誤數 > 0 時結束代碼是1。只用標準函式庫。
--strict：push前用。Git歷史裡的PDF和疑似個資也算錯誤（平常只算警告，
因為歷史要改只能改寫歷史，必須先問使用者）。
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True

KINDS = {"paper", "book", "data", "popular"}
READ = {"全文已讀", "部分章節", "只讀摘要", "尚未查證"}
TYPES = {"experiment", "model_theory", "review", "expression", "our_derivation", "our_simulation"}
OURS = {"our_derivation", "our_simulation"}
SOURCE_FIELDS = ["id", "kind", "authors", "year", "title", "venue", "doi", "url",
                 "read_status", "read_scope", "independent"]
SOURCE_SECTIONS = ["這篇在做什麼", "研究條件", "主要結果", "限制", "ingest紀錄"]
CARD_FIELDS = ["id", "type", "source", "locator", "conditions", "units", "status", "related"]
CARD_SECTIONS = ["主張", "原文依據", "限制"]
ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MIN_PAPERS = 5
MAX_QUOTE_WORDS = 50

# 個資和金鑰的樣式。這幾行本身會被掃到，所以行尾加了忽略標記。
PRIVACY = [
    (re.compile(r"(?<![\d.])4\d{8}(?![\d.])"), "像學號的9位數字"),  # privacy-scan: ignore
    (re.compile(r"(?<![\d.])09\d{2}[- ]?\d{3}[- ]?\d{3}(?![\d.])"), "手機號碼"),  # privacy-scan: ignore
    (re.compile(r"[A-Za-z0-9._%+-]+@(?!users\.noreply\.github\.com)(?!example\.com)[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), "電子郵件"),  # privacy-scan: ignore
    (re.compile(r"(/home/|/Users/|[A-Za-z]:\\Users|/tmp/claude|/mnt/user-data)"), "本機路徑"),  # privacy-scan: ignore
    (re.compile(r"\b(sk-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{20,}|gsk_[A-Za-z0-9]{20,}|AIza[0-9A-Za-z_-]{30,})"), "金鑰或Token"),  # privacy-scan: ignore
    (re.compile(r"\bI[1-4]A\d{2}\b"), "班級座號"),  # privacy-scan: ignore
]
IGNORE_MARK = "privacy-scan: ignore"
CJK = r"[一-鿿]"
SPACE_RE = re.compile(rf"{CJK} +[A-Za-z0-9]|[A-Za-z0-9] +{CJK}")


class Report:
    def __init__(self):
        self.errors, self.warnings = [], []

    def err(self, where, msg):
        self.errors.append(f"[錯誤] {where}：{msg}")

    def warn(self, where, msg):
        self.warnings.append(f"[警告] {where}：{msg}")


def parse(path):
    """讀開頭的 --- 區塊（每行 key: value），回傳 (欄位, 內文)。"""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end < 0:
        return None, text
    meta = {}
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            meta.setdefault("__bad__", []).append(line)
            continue
        k, v = line.split(":", 1)
        k = k.strip()
        if k in meta:
            meta.setdefault("__dup__", []).append(k)
        meta[k] = v.strip()
    return meta, text[end + 5:]


def sections(body):
    out, cur = {}, None
    for line in body.splitlines():
        m = re.match(r"^## (.+?)\s*$", line)
        if m:
            cur = m.group(1)
            out[cur] = []
        elif cur:
            out[cur].append(line)
    return {k: "\n".join(v).strip() for k, v in out.items()}


def check_fields(rep, where, meta, fields):
    if meta is None:
        rep.err(where, "開頭沒有 --- 欄位區塊")
        return False
    for bad in meta.get("__bad__", []):
        rep.err(where, f"欄位格式錯誤：{bad}")
    for dup in meta.get("__dup__", []):
        rep.err(where, f"欄位 {dup} 出現不只一次")
    for f in fields:
        if f not in meta:
            rep.err(where, f"缺少欄位 {f}")
        elif f != "related" and not meta[f]:
            rep.err(where, f"欄位 {f} 是空的")
    for f in meta:
        if f not in ("__bad__", "__dup__") and f not in fields:
            rep.err(where, f"不認得的欄位 {f}")
    return True


def check_sources(root, rep):
    sources = {}
    for p in sorted((root / "wiki" / "sources").glob("*.md")):
        if p.name == "_template.md":
            continue
        where = p.relative_to(root).as_posix()
        meta, body = parse(p)
        if not check_fields(rep, where, meta, SOURCE_FIELDS):
            continue
        if meta.get("id") != p.stem:
            rep.err(where, f"id {meta.get('id')} 跟檔名不一樣")
        if not ID_RE.match(p.stem):
            rep.err(where, "檔名只能用小寫英數和-")
        if meta.get("kind") not in KINDS:
            rep.err(where, f"kind 要是 {'、'.join(sorted(KINDS))} 之一")
        if meta.get("read_status") not in READ:
            rep.err(where, f"read_status 要是 {'、'.join(sorted(READ))} 之一")
        if meta.get("independent") not in ("是", "否"):
            rep.err(where, "independent 要是「是」或「否」")
        if not re.fullmatch(r"\d{4}", meta.get("year", "")):
            rep.err(where, "year 要是4位數年份")
        url = meta.get("url", "")
        if url and not url.startswith("https://"):
            rep.err(where, "url 要用 https://")
        doi = meta.get("doi", "")
        if doi and doi != "無" and not re.fullmatch(r"10\.\d{4,9}/\S+", doi):
            rep.err(where, "doi 格式不對（寫 10.xxxx/... 或「無」）")
        secs = sections(body)
        for s in SOURCE_SECTIONS:
            if s not in secs:
                rep.err(where, f"缺少段落「## {s}」")
        sources[p.stem] = meta
    return sources


def quote_words(text):
    lines = [l[1:] for l in text.splitlines() if l.startswith(">")]
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-]*", " ".join(lines)))


def check_cards(root, rep, sources, tracked):
    cards = {}
    paths = [p for p in sorted((root / "wiki" / "cards").glob("*.md")) if p.name != "_template.md"]
    for p in paths:
        where = p.relative_to(root).as_posix()
        meta, body = parse(p)
        if not check_fields(rep, where, meta, CARD_FIELDS):
            continue
        cards[p.stem] = (meta, body, where)
    for cid, (meta, body, where) in cards.items():
        if meta.get("id") != cid:
            rep.err(where, f"id {meta.get('id')} 跟檔名不一樣")
        if not ID_RE.match(cid):
            rep.err(where, "檔名只能用小寫英數和-")
        t, src, loc = meta.get("type"), meta.get("source", ""), meta.get("locator", "")
        if t not in TYPES:
            rep.err(where, f"type 要是 {'、'.join(sorted(TYPES))} 之一")
        if meta.get("status") not in ("confirmed", "pending"):
            rep.err(where, "status 要是 confirmed 或 pending")
        if t in OURS:
            f = root / src
            if not src or src.startswith("/") or ".." in src or not f.is_file():
                rep.err(where, f"source 要是repo裡存在的檔案（找不到 {src}）")
            elif f.resolve() not in tracked:
                rep.err(where, f"source {src} 是不會上傳的檔案，別人沒辦法核對")
        elif t in TYPES:
            s = sources.get(src)
            if s is None:
                rep.err(where, f"source {src} 在 wiki/sources/ 裡找不到")
            else:
                rs = s.get("read_status")
                if rs == "尚未查證" and meta.get("status") == "confirmed":
                    rep.err(where, f"{src} 還是「尚未查證」，卡片不能是 confirmed")
                if rs == "只讀摘要" and "摘要" not in loc:
                    rep.err(where, f"{src} 只讀了摘要，locator 要寫「摘要」")
                if t == "expression" and s.get("kind") != "popular":
                    rep.err(where, "expression 只能引用 kind: popular 的文獻")
                if t != "expression" and s.get("kind") == "popular":
                    rep.err(where, "科普或新聞只能當 expression，不能當研究證據")
        secs = sections(body)
        for s_ in CARD_SECTIONS:
            if s_ not in secs or not secs[s_]:
                rep.err(where, f"缺少段落或段落是空的「## {s_}」")
        claim = re.sub(r"(?<!\d)(19|20)\d{2}(?!\d)", "", secs.get("主張", ""))
        if re.search(r"\d", claim):
            if meta.get("units") == "無數值":
                rep.err(where, "主張裡有數字，units 不能寫「無數值」（要寫單位或「無因次」）")
            if t not in OURS and not re.search(r"\d|摘要", loc):
                rep.err(where, "主張裡有數字，locator 要到頁碼、章節、公式或圖表編號（或寫「摘要」）")
        w = quote_words(body)
        if w > MAX_QUOTE_WORDS:
            rep.err(where, f"英文原文引用 {w} 個字，超過 {MAX_QUOTE_WORDS}")
        for r in [x.strip() for x in meta.get("related", "").split(",") if x.strip()]:
            if r not in cards:
                rep.err(where, f"related 的 {r} 不存在")
    return cards


def check_index(root, rep, sources, cards):
    idx = root / "wiki" / "index.md"
    if not idx.is_file():
        rep.err("wiki/index.md", "檔案不存在")
        return
    text = idx.read_text(encoding="utf-8")
    for kind, name in re.findall(r"\b(sources|cards)/([a-z0-9-]+)\.md", text):
        if not (root / "wiki" / kind / f"{name}.md").is_file():
            rep.err("wiki/index.md", f"列出的 {kind}/{name}.md 不存在")
    for sid in sources:
        if f"sources/{sid}.md" not in text:
            rep.err("wiki/index.md", f"沒有列出文獻 {sid}")
    for cid in cards:
        if f"cards/{cid}.md" not in text:
            rep.err("wiki/index.md", f"沒有列出證據卡 {cid}")


def tracked_files(root):
    try:
        out = subprocess.run(["git", "ls-files", "-co", "--exclude-standard"], cwd=root,
                             capture_output=True, text=True, check=True).stdout
        return [root / l for l in out.splitlines() if l]
    except (OSError, subprocess.CalledProcessError):
        return [p for p in root.rglob("*") if p.is_file() and ".git" not in p.parts]


# SHA-256雜湊值是64位十六進位，裡面常會剛好有一段像學號或手機的數字。只在有明確標記時排除：
# 1. 同一行寫了「SHA-256」，後面緊接著用反引號包起來的64位小寫十六進位；或
# 2. 表格的表頭有一欄以「SHA-256」開頭，而且這一格以反引號包起來的64位小寫十六進位開頭。
# 排除只套用在學號和手機兩條規則，信箱、路徑、金鑰、座號照原本那一行檢查。
# （2026-11-11看到pipeline/review/n3-package-r2.md的雜湊被誤判成學號之後才加的，紀錄在
#  runs/2026-11-11-check-wiki-hash-exclusion.md。）
HASH_TOKEN = "`[0-9a-f]{64}`"
LABELED_HASH = re.compile(r"(SHA-256[:：]?\s*)" + HASH_TOKEN)
HASH_CELL = re.compile(r"^(\s*)" + HASH_TOKEN)
HASH_MASKED = {"像學號的9位數字", "手機號碼"}


def sha_column(line):
    """表格表頭裡以SHA-256開頭的那一欄，回傳它用「|」切開後的位置；不是這種表頭就回傳None。"""
    if not line.lstrip().startswith("|"):
        return None
    for i, cell in enumerate(line.split("|")):
        if cell.strip().startswith("SHA-256"):
            return i
    return None


class ShaTable:
    """一行一行讀，記住現在是不是在有SHA-256欄的表格裡。表格一結束（下一行不是「|」開頭）就失效。"""
    def __init__(self):
        self.col = None

    def feed(self, line):
        col = sha_column(line)
        if col is not None:
            self.col = col
        elif not line.lstrip().startswith("|"):
            self.col = None
        return self.col


def mask_hashes(line, sha_col=None):
    line = LABELED_HASH.sub(r"\1`<sha256>`", line)
    if sha_col is not None and line.lstrip().startswith("|"):
        cells = line.split("|")
        if sha_col < len(cells):
            cells[sha_col] = HASH_CELL.sub(r"\1`<sha256>`", cells[sha_col])
        line = "|".join(cells)
    return line


def scan_line(line, sha_col=None):
    if IGNORE_MARK in line:
        return []
    masked = mask_hashes(line, sha_col)
    return [name for pat, name in PRIVACY if pat.search(masked if name in HASH_MASKED else line)]


def check_history(root, rep, strict):
    """掃Git歷史裡加進去過的每一行，以及出現過的PDF。"""
    def git(*args):
        return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", check=True).stdout
    try:
        git("rev-parse", "--verify", "HEAD")
    except (OSError, subprocess.CalledProcessError):
        return
    report = rep.err if strict else rep.warn
    for name in sorted(set(git("log", "--all", "--name-only", "--format=").splitlines())):
        if name.lower().endswith(".pdf"):
            report("Git歷史", f"出現過PDF：{name}")
    commit, path, table = "", "", ShaTable()
    for line in git("log", "--all", "-p", "--no-color", "--format=commit %h").splitlines():
        if line.startswith("commit "):
            commit, table = line[7:], ShaTable()
        elif line.startswith("+++ "):
            path, table = (line[6:] if line.startswith("+++ b/") else line[4:]), ShaTable()
        elif line.startswith("@@"):
            table = ShaTable()  # 新的一段diff可能從檔案中間開始，看不到表頭就不排除
        elif line.startswith("+"):
            for name in scan_line(line[1:], table.feed(line[1:])):
                report(f"Git歷史 {commit} {path}", f"疑似{name}")
        elif line.startswith(" "):
            table.feed(line[1:])  # 沒改的上下文行也要追表頭，但它本身已經在別的commit掃過


def check_privacy(root, rep, tracked):
    for p in sorted(tracked):
        if not p.is_file():
            continue
        rel = p.relative_to(root).as_posix()
        if p.suffix.lower() == ".pdf":
            rep.err(rel, "PDF不能放進repo")
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        table = ShaTable()
        for n, line in enumerate(text.splitlines(), 1):
            for name in scan_line(line, table.feed(line)):
                rep.err(f"{rel}:{n}", f"疑似{name}")


def check_spacing(root, rep):
    for p in sorted((root / "wiki").rglob("*.md")):
        rel = p.relative_to(root).as_posix()
        lines = p.read_text(encoding="utf-8").splitlines()
        start = 0
        if lines and lines[0] == "---" and "---" in lines[1:]:
            start = lines.index("---", 1) + 1
        in_code = False
        for n, line in enumerate(lines[start:], start + 1):
            if line.startswith("```"):
                in_code = not in_code
            if in_code or line.startswith(">"):
                continue
            if SPACE_RE.search(re.sub(r"`[^`]*`", "", line)):
                rep.warn(f"{rel}:{n}", "中文和英文或數字之間有空格")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=Path(__file__).resolve().parent.parent)
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    rep = Report()
    tracked = {p.resolve() for p in tracked_files(root) if p.is_file()}
    sources = check_sources(root, rep)
    cards = check_cards(root, rep, sources, tracked)
    check_index(root, rep, sources, cards)
    check_privacy(root, rep, tracked)
    check_history(root, rep, args.strict)
    check_spacing(root, rep)
    used = {m.get("source") for m, _, _ in cards.values() if m.get("status") == "confirmed"}
    papers = [s for s, m in sources.items() if m.get("kind") == "paper" and m.get("independent") == "是"
              and m.get("read_status") in ("全文已讀", "部分章節") and s in used]
    if len(papers) < MIN_PAPERS:
        rep.warn("wiki/sources", f"實際讀過、而且有confirmed證據卡的獨立論文 {len(papers)} 篇，"
                                 f"還不到 {MIN_PAPERS} 篇")
    for line in rep.errors + rep.warnings:
        print(line)
    pending = sum(1 for m, _, _ in cards.values() if m.get("status") == "pending")
    print(f"\n文獻 {len(sources)} 篇（算進5篇的獨立論文 {len(papers)} 篇），"
          f"證據卡 {len(cards)} 張（pending {pending} 張）。")
    print(f"錯誤 {len(rep.errors)} 個，警告 {len(rep.warnings)} 個。")
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())

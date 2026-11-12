"""檢查Wiki的文獻檔、證據卡、索引，並掃描個資和金鑰。

用法：python3 scripts/check_wiki.py [--root 路徑] [--strict]
錯誤數 > 0 時結束代碼是1。只用標準函式庫。
--strict：push前用。Git歷史裡的PDF和疑似個資也算錯誤（平常只算警告，
因為歷史要改只能改寫歷史，必須先問使用者）。
"""
import argparse
import hashlib
import posixpath
import re
import subprocess
import sys
import unicodedata
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

# 個資和金鑰的樣式。2026-11-12起拿掉行內忽略標記（任何檔案都不能自己宣告免檢），
# 這裡的樣式字串用拼接寫，讓這個檔案本身不會被掃到。邊界都用ASCII英數判斷，
# 中文緊接著寫（例如「座號」後面直接接座號）也抓得到；學號、手機後面接英文句點也算，
# 只有句點後面還接數字（小數）才不算。見runs/2026-11-12-eng-acceptance-v2.md。
LOCAL_PATHS = ["/" + "home/", "/" + "Users/", "(?i:[a-z]:" + r"\\" + "users)", "/" + "tmp/claude", "/" + "mnt/user-data"]
PRIVACY = [
    (re.compile(r"(?<![\d.])4\d{8}(?!\d)(?!\.\d)"), "像學號的9位數字"),
    (re.compile(r"(?<![\d.])09\d{2}[- ]?\d{3}[- ]?\d{3}(?!\d)(?!\.\d)"), "手機號碼"),
    (re.compile(r"[A-Za-z0-9._%+-]+" + "@" + r"([A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,})"), "電子郵件"),
    (re.compile("(" + "|".join(LOCAL_PATHS) + ")"), "本機路徑"),
    (re.compile(r"(?<![A-Za-z0-9_-])(sk-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{20,}|gsk_[A-Za-z0-9]{20,}|AIza[0-9A-Za-z_-]{30,})"),
     "金鑰或Token"),
    (re.compile(r"(?<![A-Za-z0-9])I[1-4]A\d{2}(?!\d)"), "班級座號"),
]
# 信箱網域要完全等於這兩個才不算（example.com.invalid這種不算）
ALLOWED_EMAIL_DOMAINS = {"users.noreply.github.com", "example.com"}
ALLOWLIST = "scripts/privacy_allowlist.tsv"
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


FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
H2_RE = re.compile(r"^ {0,3}##[ \t]+(.+?)[ \t]*$")


def split_sections(body):
    """把內文切成 [(段落名稱, 內容行)]。程式碼區塊（```或~~~）裡長得像標題的行不算標題；
    標題名稱把多餘的空白合併，所以「##  主張」跟「## 主張」是同一個段落。"""
    out, fence = [], None
    for line in body.splitlines():
        m = FENCE_RE.match(line)
        if fence is None and m:
            fence = m.group(1)
        elif fence is not None and m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) \
                and not line.strip()[len(m.group(1)):].strip():
            fence = None
        elif fence is None:
            h = H2_RE.match(line)
            if h:
                out.append((" ".join(h.group(1).split()), []))
                continue
        if out:
            out[-1][1].append(line)
    return out


def duplicate_sections(body):
    seen, dups = set(), []
    for name, _ in split_sections(body):
        if name in seen and name not in dups:
            dups.append(name)
        seen.add(name)
    return dups


def dup_sections(rep, where, body):
    """同一個「## 」段落出現兩次，只會有一段進索引，所以直接報錯。"""
    for name in duplicate_sections(body):
        rep.err(where, f"段落「## {name}」出現不只一次")


def sections(body):
    out = {}
    for name, lines in split_sections(body):
        out.setdefault(name, "\n".join(lines).strip())
    return out


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
        dup_sections(rep, where, body)
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
        dup_sections(rep, where, body)
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
    expected = index_with_generated(text, render_index(root))
    if expected is None:
        rep.err("wiki/index.md", "找不到自動產生區塊的標記，或標記不合規定（標記要各出現一次、獨立成行，"
                                 "開始在結束前面）；請照原本的格式放回兩行標記，再跑 python3 scripts/build_index.py")
    elif expected != text:
        rep.err("wiki/index.md", "跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），"
                                 "請跑 python3 scripts/build_index.py")
    for kind, name in re.findall(r"\b(sources|cards)/([a-z0-9-]+)\.md", prose_only(text)):
        if not (root / "wiki" / kind / f"{name}.md").is_file():
            rep.err("wiki/index.md", f"列出的 {kind}/{name}.md 不存在")
    for sid in sources:
        if f"sources/{sid}.md" not in text:
            rep.err("wiki/index.md", f"沒有列出文獻 {sid}")
    for cid in cards:
        if f"cards/{cid}.md" not in text:
            rep.err("wiki/index.md", f"沒有列出證據卡 {cid}")


# index.md的文獻表和證據卡清單由scripts/build_index.py從文獻檔、證據卡產生（單一事實來源）。
# 兩個標記中間是產生的內容，外面的主題介紹和導覽人工寫。check_index會重新產生一次，跟檔案不同就報錯。
# （2026-11-12加的：第2、3輪審查發現手寫的索引摘要沒跟著卡片更新，見runs/2026-11-12-index-generation.md。）
INDEX_BEGIN = "<!-- 以下由scripts/build_index.py從wiki/sources和wiki/cards產生，不要手改；改了文獻檔或證據卡就重跑 -->"
INDEX_END = "<!-- 自動產生結束 -->"
OURS_GROUP = "我們自己的推導和模擬"


INLINE_CODE = re.compile(r"(?<!`)(`+)(?!`).*?(?<!`)\1(?!`)", re.S)
LINK_DEST = re.compile(r"\]\(\s*(<[^>\n]*>|[^()\s]+)((?:\s+(?:\"[^\"\n]*\"|'[^'\n]*'|\([^)\n]*\)))?)\s*\)")


def split_code(text):
    """把文字切成 [(是不是程式碼, 原文)]，接回去跟原文一模一樣。
    程式碼包括```或~~~的區塊（含區塊標記那兩行），以及任意長度反引號包起來的行內程式碼。"""
    out, prose, fence = [], [], None

    def flush():
        chunk = "".join(prose)
        prose.clear()
        pos = 0
        for m in INLINE_CODE.finditer(chunk):
            out.append((False, chunk[pos:m.start()]))
            out.append((True, m.group(0)))
            pos = m.end()
        out.append((False, chunk[pos:]))

    for line in text.splitlines(keepends=True):
        m = FENCE_RE.match(line)
        if fence is None and m:
            flush()
            fence = m.group(1)
            out.append((True, line))
        elif fence is not None:
            out.append((True, line))
            body = line.rstrip("\r\n")
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) and not body.strip()[len(m.group(1)):].strip():
                fence = None
        else:
            prose.append(line)
    flush()
    return [(c, s) for c, s in out if s]


def prose_only(text):
    return "".join(s for code, s in split_code(text) if not code)


def fix_links(text, card_name):
    """主張裡的相對連結是從cards/出發寫的，放進index.md要改成從wiki/出發；
    「#段落」這種卡片內的錨點（可以帶title）改成指回那張卡。程式碼（行內和區塊）裡的字不動。"""
    def fix_dest(dest):
        if re.match(r"^(https?:|mailto:|/)", dest):
            return dest
        if dest.startswith("#"):
            return f"cards/{card_name}{dest}"
        return posixpath.normpath(posixpath.join("cards", dest))

    def repl(m):
        dest, title = m.group(1), m.group(2)
        dest = f"<{fix_dest(dest[1:-1])}>" if dest.startswith("<") else fix_dest(dest)
        return f"]({dest}{title})"
    return "".join(s if code else LINK_DEST.sub(repl, s) for code, s in split_code(text))


def index_problems(root):
    """產生索引之前要先擋下的問題：證據卡有重複的段落時，主張只會收進一段。"""
    probs = []
    for p in sorted((root / "wiki" / "cards").glob("*.md")):
        if p.name == "_template.md":
            continue
        _, body = parse(p)
        for name in duplicate_sections(body):
            probs.append((p.relative_to(root).as_posix(), f"段落「## {name}」出現不只一次"))
    return probs


def render_index(root):
    wiki = root / "wiki"
    srcs, groups = [], {}
    for p in sorted((wiki / "sources").glob("*.md")):
        if p.name == "_template.md":
            continue
        meta, _ = parse(p)
        meta = meta or {}
        srcs.append(f"| {p.stem} | {meta.get('kind', '')} | {meta.get('read_status', '')} | "
                    f"[sources/{p.name}](sources/{p.name}) |")
    n_cards = 0
    for p in sorted((wiki / "cards").glob("*.md")):
        if p.name == "_template.md":
            continue
        meta, body = parse(p)
        meta = meta or {}
        n_cards += 1
        group = OURS_GROUP if meta.get("type", "").startswith("our_") else meta.get("source", "")
        claim = fix_links(sections(body).get("主張", ""), p.name)
        groups.setdefault(group, []).append(
            f"#### [{p.stem}](cards/{p.name})\n\n- 類型：{meta.get('type', '')}\n- 狀態：{meta.get('status', '')}\n"
            f"- 條件：{meta.get('conditions', '')}\n\n{claim}")
    out = [INDEX_BEGIN, "", "## 文獻", "", "| id | 種類 | 閱讀狀態 | 檔案 |", "|---|---|---|---|", *srcs, "",
           "## 證據卡", "", f"共{n_cards}張。每張的條件取自卡片的conditions欄位，主張直接取自卡片的「## 主張」，都沒有另外縮寫；原文依據和限制請點進卡片看。"]
    for g in sorted(k for k in groups if k != OURS_GROUP) + ([OURS_GROUP] if OURS_GROUP in groups else []):
        out += ["", f"### {g}"]
        for item in groups[g]:
            out += ["", item]
    out += ["", INDEX_END]
    return "\n".join(out)


def index_with_generated(text, generated):
    """把index.md裡兩個標記之間換成新產生的內容。標記要各出現一次、獨立成行、開始在結束前面，
    否則回傳None（重複的標記會讓第二份過期內容躲過比對）。"""
    lines = text.split("\n")
    begins = [i for i, l in enumerate(lines) if l == INDEX_BEGIN]
    ends = [i for i, l in enumerate(lines) if l == INDEX_END]
    if (text.count(INDEX_BEGIN), text.count(INDEX_END), len(begins), len(ends)) != (1, 1, 1, 1) or begins[0] > ends[0]:
        return None
    return "\n".join(lines[:begins[0]] + generated.split("\n") + lines[ends[0] + 1:])


def tracked_files(root):
    try:
        # -z加上core.quotePath=false：中文檔名照原文輸出，不會變成帶引號的跳脫字串而漏掃
        out = subprocess.run(["git", "-c", "core.quotePath=false", "ls-files", "-z", "-co", "--exclude-standard"],
                             cwd=root, capture_output=True, text=True, encoding="utf-8", check=True).stdout
        return [root / l for l in out.split("\0") if l]
    except (OSError, subprocess.CalledProcessError):
        return [p for p in root.rglob("*") if p.is_file() and ".git" not in p.parts]


# SHA-256雜湊值是64位十六進位，裡面常會剛好有一段像學號或手機的數字。只在有明確標記時排除：
# 1. 同一行寫了「SHA-256」，後面緊接著用反引號包起來的64位小寫十六進位；或
# 2. 表格的表頭有一欄以「SHA-256」開頭，而且這一格以反引號包起來的64位小寫十六進位開頭。
# 排除只套用在學號和手機兩條規則，信箱、路徑、金鑰、座號照原本那一行檢查。
# （2026-11-11看到pipeline/review/n3-package-r2.md的雜湊被誤判成學號之後才加的，紀錄在
#  runs/2026-11-11-check-wiki-hash-exclusion.md。掃Git歷史時用那個commit的完整檔案判斷表頭，
#  見runs/2026-11-11-check-wiki-history-fullfile.md。）
# 2026-11-12第4輪工程審查後收緊（runs/2026-11-12-eng-fixes-after-r4.md）：
# - 同一行的標記：「SHA-256」前面不能接任何文字的英數（含全形，例如ＮｏｔSHA-256），也不能接底線或連字號；
#   前面是中文、空白或標點才算（「PDF的SHA-256」算）。後面只能接冒號、空白，再接雜湊。
# - 程式碼區塊（```或~~~）裡的表格不算表格。
# - 表格：第一列是表頭、緊接著一列分隔列（|---|）、而且表頭剛好有一格是「SHA-256」或「SHA-256（說明）」，
#   才算有SHA-256欄的表格；資料列的格數要跟表頭一樣；那一格的內容只能是雜湊值，後面最多接一個全形括號說明。
HASH_TOKEN = "`[0-9a-f]{64}`"
HASH_RE = re.compile(HASH_TOKEN)
LABELED_HASH = re.compile(r"(SHA-256[:：]?\s*)" + HASH_TOKEN)
HASH_CELL = re.compile(r"^(\s*)" + HASH_TOKEN + r"((?:（[^（）]*）)?\s*)$")
SHA_HEADER_CELL = re.compile(r"^SHA-256(?:（[^（）]*）)?$")
SEPARATOR = re.compile(r"^\s*\|(?:\s*:?-{3,}:?\s*\|)+\s*$")
HASH_MASKED = {"像學號的9位數字", "手機號碼"}


def sha_column(line):
    """表頭列裡剛好有一格是「SHA-256」或「SHA-256（說明）」時，回傳那一格用「|」切開後的位置；否則None。"""
    if not line.lstrip().startswith("|"):
        return None
    hits = [i for i, cell in enumerate(line.split("|")) if SHA_HEADER_CELL.match(cell.strip())]
    return hits[0] if len(hits) == 1 else None


class ShaTable:
    """一行一行讀，判斷現在這一行是不是「有SHA-256欄的真表格」的資料列。
    表格從一串「|」開頭的行的第一列開始，第二列一定要是分隔列，表格一結束（下一行不是「|」開頭）就失效。
    程式碼區塊裡的行一律不算。"""
    def __init__(self):
        self.row = 0          # 目前是這個表格的第幾列（0代表不在表格裡）
        self.header_col = None
        self.ncells = 0
        self.col = None
        self.fence = None

    def feed(self, line):
        m = FENCE_RE.match(line)
        if self.fence is None and m:
            self.fence = m.group(1)
        elif self.fence is not None:
            if m and m.group(1)[0] == self.fence[0] and len(m.group(1)) >= len(self.fence) \
                    and not line.strip()[len(m.group(1)):].strip():
                self.fence = None
        if self.fence is not None or m:
            self.row, self.header_col, self.col = 0, None, None
            return None
        if not line.lstrip().startswith("|"):
            self.row, self.header_col, self.col = 0, None, None
            return None
        self.row += 1
        cells = len(line.split("|"))
        if self.row == 1:
            self.header_col, self.ncells, self.col = sha_column(line), cells, None
            return None
        if self.row == 2:
            if self.header_col is not None and SEPARATOR.match(line) and cells == self.ncells:
                self.col = self.header_col
            return None
        return self.col if cells == self.ncells else None


def label_ok(line, start):
    """「SHA-256」前一個字：沒有字、空白、標點或中文才算標記；任何文字的英數（含全形）、底線、連字號都不算。"""
    if start == 0:
        return True
    ch = line[start - 1]
    if ch in "_-":
        return False
    if ch.isalnum():
        return unicodedata.name(ch, "").startswith("CJK UNIFIED IDEOGRAPH")
    return True


def mask_hashes(line, sha_col=None):
    line = LABELED_HASH.sub(lambda m: m.group(1) + "`<sha256>`" if label_ok(line, m.start()) else m.group(0), line)
    if sha_col is not None and line.lstrip().startswith("|"):
        cells = line.split("|")
        if sha_col < len(cells):
            cells[sha_col] = HASH_CELL.sub(r"\1`<sha256>`\2", cells[sha_col])
        line = "|".join(cells)
    return line


def scan_line(line, sha_col=None):
    masked = mask_hashes(line, sha_col)
    found = []
    for pat, name in PRIVACY:
        text = masked if name in HASH_MASKED else line
        if name == "電子郵件":
            if any(m.group(1).lower() not in ALLOWED_EMAIL_DOMAINS for m in pat.finditer(text)):
                found.append(name)
        elif pat.search(text):
            found.append(name)
    return found


def line_hash(line):
    return hashlib.sha256(line.encode("utf-8")).hexdigest()


def load_allowlist(root, rep):
    """受控例外清單：每一行是 commit（40位）、路徑、那一行的SHA-256、規則名稱、原因，用tab分開。
    只排除清單上「那個commit、那個檔案、那一行內容、那條規則」的命中；目前檔案只要路徑、內容、規則對得上。
    清單只放雜湊，不放原文。格式錯就報錯，不會因此多排除任何東西。"""
    path = root / ALLOWLIST
    history, current = set(), set()
    if not path.is_file():
        return history, current
    names = {name for _, name in PRIVACY}
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.startswith("#"):
            continue
        f = line.split("\t")
        ok = (len(f) == 5 and re.fullmatch(r"[0-9a-f]{40}", f[0]) and f[1] and not f[1].startswith("/")
              and re.fullmatch(r"[0-9a-f]{64}", f[2]) and f[3] in names and f[4].strip())
        if not ok:
            rep.err(ALLOWLIST, f"privacy_allowlist.tsv第{n}行格式錯誤（要有commit、路徑、SHA-256、規則名稱、原因五欄）")
            continue
        history.add((f[0], f[1], f[2], f[3]))
        current.add((f[1], f[2], f[3]))
    return history, current


def check_history(root, rep, strict, allow=frozenset()):
    """掃Git歷史裡加進去過的每一行（包括merge commit對每個parent新增的行），以及出現過的PDF。"""
    def git(*args):
        # core.quotePath=false：中文檔名照原文輸出
        return subprocess.run(["git", "-c", "core.quotePath=false", *args], cwd=root, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", check=True).stdout

    def git_failed(args, e):
        detail = (getattr(e, "stderr", "") or str(e)).strip().splitlines()
        rep.err("Git歷史", f"Git指令失敗，歷史沒有檢查完（git {' '.join(args)}）：{detail[-1] if detail else e}")

    report = rep.err if strict else rep.warn
    try:
        inside = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], cwd=root, capture_output=True,
                                text=True).stdout.strip() == "true"
    except OSError as e:
        report("Git歷史", f"找不到git，沒辦法檢查歷史：{e}")
        return
    if not inside:
        if strict:
            rep.err("Git歷史", "這裡不是Git repo，--strict沒辦法檢查歷史")
        return
    args = ("for-each-ref", "--count=1", "--format=%(refname)")
    try:
        has_refs = bool(git(*args).strip())
    except (OSError, subprocess.CalledProcessError) as e:
        git_failed(args, e)
        return
    try:
        git("rev-parse", "--verify", "HEAD")
    except subprocess.CalledProcessError:
        if not has_refs:
            return  # 剛git init、還沒有任何commit，沒有歷史可以掃
        # HEAD壞了但還有其他分支或標籤：報錯，而且照樣掃全部歷史
        rep.err("Git歷史", "HEAD無法解析（指向不存在的分支，或參照壞掉），但repo裡還有其他參照；照樣掃描全部歷史")
    # 一律加--no-textconv：Git for Windows預設對PDF設了文字轉換（astextplain），轉換失敗會讓git log整個失敗
    args = ("log", "--all", "-z", "--no-textconv", "--name-only", "--format=")
    try:
        names = git(*args)
    except (OSError, subprocess.CalledProcessError) as e:
        git_failed(args, e)
        return
    for name in sorted({n.strip() for n in re.split(r"[\0\n]", names) if n.strip()}):
        if name.lower().endswith(".pdf"):
            report("Git歷史", f"出現過PDF：{name}")

    def sha_cols(commit, path):
        """讀這個commit裡這個檔案的完整內容，算出每一行是不是在SHA-256表格裡（行號從1開始）。
        讀不到（例如檔名有特殊字元）就全部當成不在表格裡，也就是不排除。"""
        try:
            text = git("cat-file", "-p", f"{commit}:{path}")  # cat-file不做文字轉換
        except subprocess.CalledProcessError:
            return {}
        table = ShaTable()
        return {n: table.feed(line) for n, line in enumerate(text.splitlines(), 1)}

    def flush(commit, path, added):
        # 只有新增的行裡有反引號包起來的64位十六進位，排除才可能有作用，這時才去讀完整檔案
        cols = sha_cols(commit, path) if any(HASH_RE.search(text) for _, text in added) else {}
        for n, text in added:
            for name in scan_line(text, cols.get(n)):
                if (commit, path, line_hash(text), name) in allow:
                    used.add((commit, path, line_hash(text), name))
                    continue
                report(f"Git歷史 {commit[:7]} {path}", f"疑似{name}")

    # 只掃每個commit新增的行，但表頭用那個commit的完整檔案判斷，不靠diff前後幾行的上下文。
    # 用@@標頭的行數判斷哪些行是內容，內容剛好以「+++」開頭也不會被當成檔名。
    commit, path, added, n, old_left, new_left, used = "", "", [], 0, 0, 0, set()
    # -m：merge commit也輸出它對每個parent的差異，只在merge時加進來的內容才掃得到
    args = ("log", "--all", "-p", "-m", "--no-color", "--no-textconv", "--format=commit %H")
    try:
        log = git(*args)
    except (OSError, subprocess.CalledProcessError) as e:
        git_failed(args, e)
        return
    for line in log.splitlines():
        if old_left > 0 or new_left > 0:
            if line.startswith("+"):
                added.append((n, line[1:]))
                n, new_left = n + 1, new_left - 1
            elif line.startswith("-"):
                old_left -= 1
            elif line.startswith(" ") or line == "":
                n, old_left, new_left = n + 1, old_left - 1, new_left - 1
            continue
        if line.startswith("commit "):
            flush(commit, path, added)
            commit, path, added = line.split()[1], "", []
        elif line.startswith("diff --git "):
            flush(commit, path, added)
            path, added = "", []
        elif line.startswith("+++ "):
            path = line[6:] if line.startswith("+++ b/") else line[4:]
        elif line.startswith("@@"):
            m = re.match(r"@@ -\d+(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", line)
            if m:
                old_left = int(m.group(1)) if m.group(1) is not None else 1
                n = int(m.group(2))
                new_left = int(m.group(3)) if m.group(3) is not None else 1
    flush(commit, path, added)
    return used


def check_privacy(root, rep, tracked, allow=frozenset()):
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
                if (rel, line_hash(line), name) in allow:
                    continue
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
    allow_hist, allow_cur = load_allowlist(root, rep)
    check_privacy(root, rep, tracked, allow_cur)
    used = check_history(root, rep, args.strict, allow_hist) or set()
    for entry in sorted(allow_hist - used):
        rep.warn(ALLOWLIST, f"例外清單有一筆沒用到（commit {entry[0][:7]}、{entry[1]}、{entry[3]}），可能已經不需要")
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

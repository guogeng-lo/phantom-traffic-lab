# 工程審查包：檢查程式和回歸測試（只審程式，不審文獻）

## 你的角色

你是獨立審查者。這份Wiki有兩支檢查程式：`scripts/check_wiki.py`（格式、索引同步、個資和金鑰掃描，包含Git歷史）和`scripts/build_index.py`（從證據卡產生索引）。上一次審查（附在最後）找到7項程式問題，整理的人先把反例寫成測試、在舊版重現，再修改程式。這次**只審程式碼和回歸測試**，不審論文、證據卡或科學內容，也不需要論文PDF。

請確認：

1. **7項問題都修好了**：SHA-256偽表頭、`NotSHA-256`這類偽標記、測試只在整份輸出找關鍵字、索引標記重複、證據卡有重複的`## 主張`、錨點和程式碼裡的連結、Git textconv和Git指令失敗的處理。
2. **反例測試有效**：每個新測試真的測到它名稱說的事；在舊版會失敗、在新版會通過（修改前後的實際輸出附在後面）。判定規則`judge()`會不會被騙。
3. **沒有引入新的重大漏判**：
   - 學號、手機、信箱、路徑、金鑰、座號的偵測，有沒有任何寫法能讓它漏掉（特別是SHA-256排除）。
   - 索引能不能在沒報錯的情況下跟證據卡不同步。
   - Git指令失敗時會不會被當成沒問題。
4. **能跑就跑**：如果你的環境能連到GitHub，請clone公開repo `guogeng-lo/phantom-traffic-lab`，checkout到commit `2cb460b`，跑：
   - `python3 tests/test_check_wiki.py`
   - `python3 scripts/build_index.py --check`
   - `python3 scripts/check_wiki.py --strict`
   - 貼上實際輸出和結束代碼。
   - 也歡迎自己寫反例去試。
   - 不能跑就寫「沒有執行」，不要推測結果。

## 請照這個格式回覆

第一部分，7項問題逐項：

| 問題 | 修好了嗎（修好／部分修好／沒修好） | 根據（程式位置、測試名稱或你實際跑的結果） |

第二部分，新發現的問題（沒有就寫「沒有」）：

| 問題 | 嚴重程度（重大：會讓個資或金鑰漏判、索引無聲不同步、Git失敗被當成沒問題、測試測不到宣稱的事／一般） | 重現方式 | 建議怎麼改 |

第三部分，你實際執行了什麼、結果和結束代碼。

第四部分，無法確認的地方。

最後一行寫：7項中修好幾項；新問題幾個（其中重大幾個）；有沒有重大問題：有／沒有。


## 這份審查包包含的檔案版本

| 檔案 | SHA-256 |
|---|---|
| `scripts/check_wiki.py` | `f1c25bf2216667ffe78770434b60357e3d0c217366696ef5c8f0fad3ce6caa31` |
| `scripts/build_index.py` | `1c70f28459a70bd68146620ff6622bab25202e7a122e0eedab6193505dd5f28f` |
| `tests/test_check_wiki.py` | `e71bbd5ddd99ea18c0ed6d24e6b8d5f3bf480498a7a8fa93238114ac01ceee4c` |
| `runs/2026-11-12-eng-fixes-after-r4.md` | `1763f3c63a6dc86623a9154f3f5092a2bbe2ed23b1f7184cdc58b4197cf97814` |
| `runs/logs/2026-11-12-eng-tests-before.log` | `7467a1b22b0b85c5d6e21d9083df5669579b8231a941172a541a2889734b6099` |
| `runs/logs/2026-11-12-eng-tests-after.log` | `c3d25cd43c7eff38ea64eb28461fc25514bd996014c4f77fb58c65fdc02528f2` |
| `runs/logs/2026-11-12-eng-judge-before.log` | `4658e95e7d1094492d5e3929812cf99a82c86810904ded078b0d67c0d3961f62` |
| `runs/logs/2026-11-12-eng-history-compare.log` | `f67a2f02e74fe73db4685738345031974fd6805bcf177d16ebde16e8c583c013` |
| `runs/logs/2026-11-12-eng-verify.log` | `f5f2874e505add071e768cd742692f6e83f9da9b4d2f606e58ea3cc75a7cfb31` |
| `runs/logs/2026-11-12-n3-r4-repro.log` | `fee1a600dc39740d2bc41fda0fd5c5587fd163dcb3735128396d6c0b36ff2a03` |


========== 程式或執行輸出：scripts/check_wiki.py ==========

```
"""檢查Wiki的文獻檔、證據卡、索引，並掃描個資和金鑰。

用法：python3 scripts/check_wiki.py [--root 路徑] [--strict]
錯誤數 > 0 時結束代碼是1。只用標準函式庫。
--strict：push前用。Git歷史裡的PDF和疑似個資也算錯誤（平常只算警告，
因為歷史要改只能改寫歷史，必須先問使用者）。
"""
import argparse
import posixpath
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


def dup_sections(rep, where, body):
    """同一個「## 」段落出現兩次，sections()只會留一段，索引會漏掉另一段，所以直接報錯。"""
    seen = set()
    for line in body.splitlines():
        m = re.match(r"^## (.+?)\s*$", line)
        if m:
            if m.group(1) in seen:
                rep.err(where, f"段落「## {m.group(1)}」出現不只一次")
            seen.add(m.group(1))


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
    for kind, name in re.findall(r"\b(sources|cards)/([a-z0-9-]+)\.md", text):
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


CODE = re.compile(r"(```.*?```|`[^`\n]*`)", re.S)


def fix_links(text, card_name):
    """主張裡的相對連結是從cards/出發寫的，放進index.md要改成從wiki/出發；
    「#段落」這種卡片內的錨點改成指回那張卡。程式碼（行內和區塊）裡的字不動。"""
    def repl(m):
        target = m.group(1)
        if re.match(r"^(https?:|mailto:|/)", target):
            return m.group(0)
        if target.startswith("#"):
            return f"](cards/{card_name}{target})"
        return f"]({posixpath.normpath(posixpath.join('cards', target))})"
    parts = CODE.split(text)
    return "".join(part if i % 2 else re.sub(r"\]\(([^)\s]+)\)", repl, part) for i, part in enumerate(parts))


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
#  runs/2026-11-11-check-wiki-hash-exclusion.md。掃Git歷史時用那個commit的完整檔案判斷表頭，
#  見runs/2026-11-11-check-wiki-history-fullfile.md。）
# 2026-11-12第4輪工程審查後收緊（runs/2026-11-12-eng-fixes-after-r4.md）：
# - 同一行的標記：「SHA-256」前後不能接英數、底線或連字號（NotSHA-256、SHA-256-old都不算）。
# - 表格：第一列是表頭、緊接著一列分隔列（|---|）、而且表頭剛好有一格是「SHA-256」或「SHA-256（說明）」，
#   才算有SHA-256欄的表格；資料列的格數要跟表頭一樣；那一格的內容只能是雜湊值，後面最多接一個全形括號說明。
HASH_TOKEN = "`[0-9a-f]{64}`"
HASH_RE = re.compile(HASH_TOKEN)
LABELED_HASH = re.compile(r"((?<![A-Za-z0-9_-])SHA-256(?![A-Za-z0-9_-])[:：]?\s*)" + HASH_TOKEN)
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
    表格從一串「|」開頭的行的第一列開始，第二列一定要是分隔列，表格一結束（下一行不是「|」開頭）就失效。"""
    def __init__(self):
        self.row = 0          # 目前是這個表格的第幾列（0代表不在表格裡）
        self.header_col = None
        self.ncells = 0
        self.col = None

    def feed(self, line):
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


def mask_hashes(line, sha_col=None):
    line = LABELED_HASH.sub(r"\1`<sha256>`", line)
    if sha_col is not None and line.lstrip().startswith("|"):
        cells = line.split("|")
        if sha_col < len(cells):
            cells[sha_col] = HASH_CELL.sub(r"\1`<sha256>`\2", cells[sha_col])
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
    try:
        git("rev-parse", "--verify", "HEAD")
    except subprocess.CalledProcessError:
        return  # 還沒有任何commit，沒有歷史可以掃
    # 一律加--no-textconv：Git for Windows預設對PDF設了文字轉換（astextplain），轉換失敗會讓git log整個失敗
    args = ("log", "--all", "--no-textconv", "--name-only", "--format=")
    try:
        names = git(*args)
    except (OSError, subprocess.CalledProcessError) as e:
        git_failed(args, e)
        return
    for name in sorted(set(names.splitlines())):
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
                report(f"Git歷史 {commit} {path}", f"疑似{name}")

    # 只掃每個commit新增的行，但表頭用那個commit的完整檔案判斷，不靠diff前後幾行的上下文。
    # 用@@標頭的行數判斷哪些行是內容，內容剛好以「+++」開頭也不會被當成檔名。
    commit, path, added, n, old_left, new_left = "", "", [], 0, 0, 0
    args = ("log", "--all", "-p", "--no-color", "--no-textconv", "--format=commit %h")
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
            commit, path, added = line[7:], "", []
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
```


========== 程式或執行輸出：scripts/build_index.py ==========

```
"""從文獻檔和證據卡產生wiki/index.md的文獻表和證據卡清單。

用法：
  python3 scripts/build_index.py           # 重寫index.md裡兩個標記之間的內容，標記外面的人工內容不動
  python3 scripts/build_index.py --check   # 只比對，不同步就印出來、結束代碼1（check_wiki.py也會做同樣的比對）
產生的內容：文獻的id、種類、閱讀狀態、連結；證據卡依文獻分組，每張的id、類型、狀態、主張全文、連結。
主張直接用卡片的「## 主張」，不另外縮寫。產生規則寫在check_wiki.py的render_index，兩邊用同一份。
"""
import argparse
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_wiki import index_with_generated, render_index  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=Path(__file__).resolve().parent.parent)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    idx = root / "wiki" / "index.md"
    text = idx.read_text(encoding="utf-8")
    new = index_with_generated(text, render_index(root))
    if new is None:
        print("[錯誤] wiki/index.md自動產生區塊的標記要各出現一次、獨立成行，開始在結束前面")
        return 1
    if args.check:
        same = new == text
        print("index.md跟文獻檔、證據卡同步" if same else "[錯誤] index.md跟文獻檔、證據卡不同步")
        return 0 if same else 1
    if new != text:
        idx.write_text(new, encoding="utf-8", newline="\n")
        print("已重建 wiki/index.md 的自動產生區塊")
    else:
        print("wiki/index.md 已經是最新的，沒有改")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```


========== 程式或執行輸出：tests/test_check_wiki.py ==========

```
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
SID = "412345678"  # privacy-scan: ignore
PHONE = "0912345678"  # privacy-scan: ignore
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
    ("索引沒列卡片", lambda t: edit(t / "wiki" / "index.md", "(cards/demo2000-claim.md)", ""), "沒有列出證據卡"),
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
    ("索引列了不存在的卡", lambda t: edit(t / "wiki" / "index.md", "人工寫的導覽。",
                                    "人工寫的導覽。見[舊卡](cards/deleted-card.md)。"),
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
    ("沒有confirmed卡的論文不算", lambda t: (edit(C(t), "status: confirmed", "status: pending"), rebuild(t)),
     "算進5篇的獨立論文 0 篇", {"out": True}),
    # 以下是雜湊值排除（2026-11-11，看到n3-package-r2.md的SHA-256被誤判成學號之後才加的）
    ("SHA-256表格裡的雜湊值不算學號", note(SHA_TABLE + f"| `a.md` | `{fake_hash(SID)}` |\n"), None),
    ("SHA-256表格裡的雜湊值不算手機", note(SHA_TABLE + f"| `a.md` | `{fake_hash(PHONE)}` |\n"), None),
    ("SHA-256欄的雜湊後面接說明也排除",
     note("| 檔案 | SHA-256（第2輪後） |\n|---|---|\n" + f"| `a.md` | `{fake_hash(SID)}`（第2輪修改後） |\n"), None),
    ("同一行有SHA-256標記的雜湊值不算學號", note(f"PDF的SHA-256 `{fake_hash(SID)}`\n"), None),
    ("學號緊接中文照樣偵測", note(f"學號{SID}\n"), "像學號的9位數字"),
    ("學號夾在英文字母中照樣偵測", note(f"id{SID}x\n"), "像學號的9位數字"),
    ("沒有分隔的手機號碼照樣偵測", note(f"電話{PHONE}\n"), "手機號碼"),
    ("一般句子裡的學號照樣偵測", note(f"請{SID}同學到辦公室\n"), "像學號的9位數字"),
    ("沒有SHA-256標記的64位十六進位不放行", note(f"commit `{fake_hash(SID)}`\n"), "像學號的9位數字"),
    ("SHA-256欄裡只有63位不放行", note(SHA_TABLE + f"| `a.md` | `{fake_hash(SID, 63)}` |\n"), "像學號的9位數字"),
    ("SHA-256欄裡沒有反引號不放行", note(SHA_TABLE + f"| `a.md` | {fake_hash(SID)} |\n"), "像學號的9位數字"),
    ("雜湊放在SHA-256以外的欄不放行",
     note("| 檔案 | SHA-256 | 備註 |\n|---|---|---|\n" + f"| `a.md` | `{fake_hash()}` | `{fake_hash(SID)}` |\n"),
     "像學號的9位數字"),
    ("表格結束後的雜湊不放行", note(SHA_TABLE + f"| `a.md` | `{fake_hash()}` |\n\n`{fake_hash(SID)}`\n"),
     "像學號的9位數字"),
    ("SHA-256表格同一列的學號照樣偵測",
     note(SHA_TABLE + f"| `a.md` | `{fake_hash()}` | 學號{SID} |\n"), "像學號的9位數字"),
    ("SHA-256表格同一列的金鑰照樣偵測",
     note(SHA_TABLE + f"| `sk-{'a' * 30}` | `{fake_hash(SID)}` |\n"), "金鑰或Token"),
    ("歷史裡SHA-256表格的雜湊不算學號（--strict）",
     history_note(SHA_TABLE + f"| `a.md` | `{fake_hash(SID)}` |\n"), None, {"args": ["--strict"]}),
    ("歷史裡沒有標記的雜湊照樣抓（--strict）",
     history_note(f"commit `{fake_hash(SID)}`\n"), "像學號的9位數字", {"args": ["--strict"]}),
    # 以下是歷史掃描改讀完整檔案（2026-11-11，看到4462639的diff看不到表頭、雜湊被誤判之後才加的）
    ("歷史：SHA-256表格中間加一列，diff看不到表頭也排除（--strict）",
     history_versions(SHA_TABLE + rows(10), SHA_TABLE + rows(10) + f"| `x.md` | `{fake_hash(SID)}` |\n"),
     None, {"args": ["--strict"]}),
    ("歷史：SHA-256表格中間加的那列有金鑰照樣抓（--strict）",
     history_versions(SHA_TABLE + rows(10), SHA_TABLE + rows(10) + f"| `sk-{'a' * 30}` | `{fake_hash(SID)}` |\n"),
     "金鑰或Token", {"args": ["--strict"]}),
    ("歷史：SHA-256表格中間加的那列有學號照樣抓（--strict）",
     history_versions(SHA_TABLE + rows(10), SHA_TABLE + rows(10) + f"| `學號{SID}` | `{fake_hash()}` |\n"),
     "像學號的9位數字", {"args": ["--strict"]}),
    ("歷史：表格結束很久之後加的雜湊照樣抓（--strict）",
     history_versions(SHA_TABLE + rows(10) + "\n說明\n" * 5,
                      SHA_TABLE + rows(10) + "\n說明\n" * 5 + f"`{fake_hash(SID)}`\n"),
     "像學號的9位數字", {"args": ["--strict"]}),
    ("歷史：沒有SHA-256欄的表格加雜湊照樣抓（--strict）",
     history_versions("| 檔案 | 備註 |\n|---|---|\n" + rows(10),
                      "| 檔案 | 備註 |\n|---|---|\n" + rows(10) + f"| `x.md` | `{fake_hash(SID)}` |\n"),
     "像學號的9位數字", {"args": ["--strict"]}),
    # 以下是索引自動產生和同步檢查（2026-11-12，第2、3輪審查發現手寫的索引摘要沒跟著卡片更新之後才加的）
    ("改了卡片的主張沒重建索引要擋", lambda t: edit(C(t), "22台車繞230m的環", "22台車繞260m的環"), "不同步"),
    ("改了卡片的狀態沒重建索引要擋", lambda t: edit(C(t), "status: confirmed", "status: pending"), "不同步"),
    ("改了卡片的條件沒重建索引要擋", lambda t: edit(C(t), "conditions: 環狀道路", "conditions: 直線道路"), "不同步"),
    ("改了文獻的閱讀狀態沒重建索引要擋",
     lambda t: (edit(S(t), "read_status: 全文已讀", "read_status: 部分章節"), edit(S(t), "read_scope: 全文", "read_scope: 第1節")),
     "不同步"),
    ("新增卡片沒重建索引要擋",
     lambda t: (t / "wiki" / "cards" / "demo2000-second.md").write_text(CARD.replace("demo2000-claim", "demo2000-second"),
                                                                       encoding="utf-8"), "不同步"),
    ("手改自動產生的摘要要擋", lambda t: edit(t / "wiki" / "index.md", "22台車繞230m的環", "22台車繞環"), "不同步"),
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
     note("| 值 | 說明 |\n|---|---|\n| SHA-256 | x |\n" + f"| `{fake_hash(SID)}` | y |\n"), "像學號的9位數字"),
    ("表頭後面沒有分隔列，不算表格，不放行",
     note("| 檔案 | SHA-256 |\n" + f"| `a.md` | `{fake_hash(SID)}` |\n"), "像學號的9位數字"),
    ("表頭寫SHA-256之外的字（SHA-256值或備註），不放行",
     note("| 檔案 | SHA-256值或備註 |\n|---|---|\n" + f"| `a.md` | `{fake_hash(SID)}` |\n"), "像學號的9位數字"),
    ("資料列的格數跟表頭不同，不放行",
     note(SHA_TABLE + f"| `a.md` | `{fake_hash(SID)}` | 多一格 |\n"), "像學號的9位數字"),
    ("SHA-256欄的雜湊後面接的不是括號說明，不放行",
     note(SHA_TABLE + f"| `a.md` | `{fake_hash(SID)}`附註 |\n"), "像學號的9位數字"),
    ("NotSHA-256這種標記不放行", note(f"NotSHA-256 `{fake_hash(PHONE)}`\n"), "手機號碼"),
    ("SHA-256-old這種標記不放行", note(f"SHA-256-old `{fake_hash(PHONE)}`\n"), "手機號碼"),
    ("偽表頭那列同一行的信箱照樣抓",
     note("| 值 | 說明 |\n|---|---|\n| SHA-256 | someone@gmail.com |\n"), "電子郵件"),  # privacy-scan: ignore
    ("索引的起訖標記重複要擋",
     lambda t: (t / "wiki" / "index.md").write_text(
         (t / "wiki" / "index.md").read_text(encoding="utf-8") + INDEX_BEGIN + "\n過期內容\n" + INDEX_END + "\n",
         encoding="utf-8"), "標記要各出現一次"),
    ("索引的標記沒有獨立成行要擋", lambda t: edit(t / "wiki" / "index.md", INDEX_END, "結尾" + INDEX_END), "標記要各出現一次"),
    ("索引的結束標記在開始標記前面要擋",
     lambda t: (t / "wiki" / "index.md").write_text(
         INDEX_HEAD + INDEX_END + "\n" + INDEX_BEGIN + "\n", encoding="utf-8"), "標記要各出現一次"),
    ("卡片有兩個「## 主張」要擋",
     lambda t: edit(C(t), "## 主張\n", "## 主張\n插進來的另一段。\n\n## 主張\n"), "「## 主張」出現不只一次"),
    ("卡片有兩個「## 限制」要擋", lambda t: edit(C(t), "## 限制\n", "## 限制\n第一段。\n\n## 限制\n"),
     "「## 限制」出現不只一次"),
    ("主張裡的錨點連結在索引裡指回那張卡", lambda t: claim_add(t, "見[限制](#限制)。"), None,
     {"files": [("wiki/index.md", "見[限制](cards/demo2000-claim.md#限制)。", True)]}),
    ("主張裡行內程式碼的連結字樣不改", lambda t: claim_add(t, "寫法是`[x](y.md)`。"), None,
     {"files": [("wiki/index.md", "寫法是`[x](y.md)`。", True)]}),
    ("主張裡程式碼區塊的連結字樣不改", lambda t: claim_add(t, "\n\n```\n[x](y.md)\n```"), None,
     {"files": [("wiki/index.md", "```\n[x](y.md)\n```", True)]}),
    ("Git設了會失敗的textconv，歷史裡的PDF照樣報（--strict）", textconv_pdf, "出現過PDF：a.pdf",
     {"args": ["--strict"]}),
    ("Git設了會失敗的textconv，歷史裡的金鑰照樣抓（--strict）", textconv_key, "金鑰或Token", {"args": ["--strict"]}),
    ("Git指令失敗要報錯，不能當成沒問題", corrupt_history, "Git指令失敗"),
    ("Git指令失敗在--strict也要報錯", corrupt_history, "Git指令失敗", {"args": ["--strict"]}),
]


def judge(code, out, expect, opt):
    """判斷一個情境過不過。預期錯誤時，指定的訊息一定要出現在「[錯誤]」那一行，
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
    ok = code == 1 and any(expect in l for l in errs)
    return ok, f"「[錯誤]」那一行裡有「{expect}」", "；".join(errs) or out.strip() or "沒有錯誤"


# 檢查judge本身：故意給它會騙過舊寫法的輸出
JUDGE_CASES = [
    ("關鍵字只在警告行，另有無關錯誤：不能算通過",
     (1, "[警告] x：疑似金鑰或Token\n[錯誤] y：無關的錯誤\n", "金鑰或Token", {}), False),
    ("關鍵字在錯誤行：算通過", (1, "[錯誤] note.md:1：疑似金鑰或Token\n", "金鑰或Token", {}), True),
    ("結束代碼1但沒有任何錯誤行（例如程式當掉）：不能算通過",
     (1, "Traceback (most recent call last):\n  金鑰或Token\n", "金鑰或Token", {}), False),
    ("預期沒有錯誤，卻有錯誤行：不能算通過", (0, "[錯誤] x：y\n", None, {}), False),
    ("預期只有警告，卻也有錯誤行：不能算通過", (0, "[錯誤] a\n[警告] b：金鑰或Token\n", "金鑰或Token", {"warn": True}), False),
]


def main():
    fails = 0
    for name, args, want_ok in JUDGE_CASES:
        ok = judge(*args)[0] == want_ok
        fails += not ok
        print(f"[{'PASS' if ok else 'FAIL'}] 判定規則：{name}")
    for case in CASES:
        name, breaker, expect = case[:3]
        opt = case[3] if len(case) > 3 else {}
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            make_site(tmp)
            breaker(tmp)
            code, out = run(tmp, *opt.get("args", []))
            ok, want, got = judge(code, out, expect, opt)
            for rel, text, present in opt.get("files", []):
                content = (tmp / rel).read_text(encoding="utf-8")
                if (text in content) != present:
                    ok = False
                    got = f"{got}；{rel}裡{'找不到' if present else '不該有'}「{text}」"
                want = f"{want}；{rel}裡{'要有' if present else '不能有'}「{text}」"
            fails += not ok
            print(f"[{'PASS' if ok else 'FAIL'}] {name}\n    預期：{want}\n    實際：{got}")
    total = len(CASES) + len(JUDGE_CASES)
    print(f"\n共{total}個情境（其中判定規則{len(JUDGE_CASES)}個），失敗{fails}個。")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
```


========== 程式或執行輸出：runs/2026-11-12-eng-fixes-after-r4.md ==========

```
# 工程修復：第4輪審查指出的7項程式問題

- **類別**：檢查程式修正、索引程式修正（不是Graph的節點，是節點3第4輪不通過後，使用者授權的「工程修復與回歸驗收」）
- **日期**：2026-11-12
- **依據**：`runs/2026-11-12-n3-review-r4.md`（第4輪不通過，紀錄保留不改），使用者第4輪後的決定第2～4點
- **改的檔案**：`scripts/check_wiki.py`、`scripts/build_index.py`（只改錯誤訊息）、`tests/test_check_wiki.py`
- **標準有沒有改**：有，全部是**看到第4輪審查結果之後才改的**。方向都是收緊：
  - SHA-256排除的條件變嚴。
  - 索引和卡片的格式要求變嚴。
  - 測試的判定變嚴。
  - 學號、手機、信箱、路徑、金鑰、座號的偵測規則本身都沒動。

## 做法

照使用者的要求：
1. 先把審查者的反例寫成測試。
2. 在舊版跑一次，留下結果。
3. 再改程式，重跑同一組測試。

### 修改前

- 測試：`共94個情境（其中判定規則5個），失敗18個。`，結束代碼1（`runs/logs/2026-11-12-eng-tests-before.log`）。
  - 失敗的18個全是這次新加的反例，代表測試真的測到問題。
  - 原本的71個在新的判定規則下也都通過。
- 新加的反例裡有兩個在舊版就通過，它們是確認不會漏報的對照組：
  - 「SHA-256-old這種標記不放行」
  - 「偽表頭那列同一行的信箱照樣抓」
- 判定規則：用舊的判定寫法（在整份輸出找關鍵字）去判5個判定規則情境，錯了4個（`runs/logs/2026-11-12-eng-judge-before.log`）。例如「關鍵字只在警告行、另有無關錯誤」，舊寫法會判成通過。

### 修改後

- 測試：`共94個情境（其中判定規則5個），失敗0個。`，結束代碼0（`runs/logs/2026-11-12-eng-tests-after.log`）。

## 7項問題怎麼修

| # | 問題 | 怎麼修 | 對應的反例測試 |
|---|---|---|---|
| 1 | SHA-256偽表頭 | 要是真的表格才算：第一列是表頭、第二列一定是分隔列（`\|---\|`）、表頭剛好有一格是「SHA-256」或「SHA-256（說明）」。資料列的格數要跟表頭一樣，那一格只能是雜湊值，後面最多接一個全形括號說明 | 偽表頭；表頭後沒有分隔列；表頭寫「SHA-256值或備註」；資料列格數不同；雜湊後面接的不是括號說明 |
| 2 | `NotSHA-256`標記 | 「SHA-256」前後不能接英數、底線或連字號 | NotSHA-256；SHA-256-old |
| 3 | 測試只在整份輸出找關鍵字 | 新增`judge()`：預期錯誤時，指定訊息一定要出現在`[錯誤]`那一行；預期沒錯誤時，不能有任何`[錯誤]`行；結束代碼1但沒有錯誤行（例如程式當掉）不算通過。另外加5個情境測`judge()`本身 | 5個判定規則情境 |
| 4 | 索引標記重複 | 兩個標記各只能出現一次、各自獨立成一行、開始在結束前面，否則`check_wiki.py`報錯，`build_index.py`也拒絕重建 | 標記重複；標記沒有獨立成行；結束在開始前面 |
| 5 | 卡片有兩個`## 主張` | 證據卡任何一個`## `段落重複都報錯 | 兩個主張；兩個限制 |
| 6 | 錨點和程式碼裡的連結 | `#段落`改成指回那張卡（`cards/<卡片>.md#段落`）；行內程式碼和程式碼區塊裡的字不動 | 錨點；行內程式碼；程式碼區塊 |
| 7 | Git textconv和Git失敗 | `git log`一律加`--no-textconv`，讀完整檔案改用不做文字轉換的`git cat-file -p`。Git指令失敗時報錯，一般模式和`--strict`都算錯誤，所以會擋commit也會擋push。`--strict`在不是Git repo的地方也報錯 | textconv壞掉時PDF照樣報；textconv壞掉時金鑰照樣抓；Git物件壞掉時報錯（一般模式、`--strict`各一個） |

Windows的textconv問題，我這裡沒有Windows。測試用Git設定一個一定會失敗的文字轉換（`diff.boom.textconv=false`），模擬審查者遇到的狀況。舊版在這個設定下會當掉，沒有報出PDF。

## 有沒有放寬原本的偵測

- 學號、手機、信箱、路徑、金鑰、座號的規則（`PRIVACY`）一字沒改。
- 原本的71個測試，在更嚴的判定規則下全部通過，包括這些「照樣偵測」的情境：
  - 學號
  - 手機
  - 信箱
  - 金鑰
  - 夾在英文字母中的學號
  - 63位字串
  - 沒有反引號
  - 沒有標記
- 歷史掃描新舊版對照（`runs/logs/2026-11-12-eng-history-compare.log`）：

  ```
  掃到的新增行數：old 13858 new 13858
  只在old出現 0 只在new出現 0
  在SHA-256表格欄裡的行數：old 255 new 233
  ```

  - 兩版掃的新增行完全相同。
  - 被當成在SHA-256欄裡的行變少了。舊版連表頭列和分隔列也算進去，新版只算資料列。範圍只有變小，沒有變大。
- 修改後的`--strict`：錯誤0，結束代碼0。repo裡原本用的格式都還認得，所以沒有新的誤報，例如：
  - `| 檔案 | SHA-256（第2輪後） |`
  - `` `雜湊`（第2輪修改後） ``

## 還做不到的

- 程式還是看不到圖片內容。截圖要人看過。
- SHA-256排除只有在「64位小寫十六進位、用反引號包起來」時才會發生。如果有人刻意做一個符合全部格式的假SHA-256表格，把學號藏在一個64位的十六進位字串裡，還是會被排除。這是使用者同意的設計，排除本來就以表格格式為準。
```


========== 程式或執行輸出：runs/logs/2026-11-12-eng-tests-before.log ==========

```
[PASS] 判定規則：關鍵字只在警告行，另有無關錯誤：不能算通過
[PASS] 判定規則：關鍵字在錯誤行：算通過
[PASS] 判定規則：結束代碼1但沒有任何錯誤行（例如程式當掉）：不能算通過
[PASS] 判定規則：預期沒有錯誤，卻有錯誤行：不能算通過
[PASS] 判定規則：預期只有警告，卻也有錯誤行：不能算通過
[PASS] 正常資料
    預期：沒有錯誤
    實際：沒有錯誤
[PASS] 主張裡只有年份，units寫無數值
    預期：沒有錯誤
    實際：沒有錯誤
[PASS] 文獻少一個欄位
    預期：「[錯誤]」那一行裡有「缺少欄位 venue」
    實際：[錯誤] wiki/sources/demo2000.md：缺少欄位 venue
[PASS] 閱讀狀態亂寫
    預期：「[錯誤]」那一行裡有「read_status 要是」
    實際：[錯誤] wiki/sources/demo2000.md：read_status 要是 全文已讀、只讀摘要、尚未查證、部分章節 之一；[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] DOI格式錯
    預期：「[錯誤]」那一行裡有「doi 格式不對」
    實際：[錯誤] wiki/sources/demo2000.md：doi 格式不對（寫 10.xxxx/... 或「無」）
[PASS] 網址不是https
    預期：「[錯誤]」那一行裡有「url 要用 https://」
    實際：[錯誤] wiki/sources/demo2000.md：url 要用 https://
[PASS] 文獻少段落
    預期：「[錯誤]」那一行裡有「缺少段落「## 限制」」
    實際：[錯誤] wiki/sources/demo2000.md：缺少段落「## 限制」
[PASS] 證據卡的文獻不存在
    預期：「[錯誤]」那一行裡有「找不到」
    實際：[錯誤] wiki/cards/demo2000-claim.md：source ghost1999 在 wiki/sources/ 裡找不到；[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 文獻尚未查證，卡片卻是confirmed
    預期：「[錯誤]」那一行裡有「不能是 confirmed」
    實際：[錯誤] wiki/cards/demo2000-claim.md：demo2000 還是「尚未查證」，卡片不能是 confirmed；[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 只讀摘要，locator沒寫摘要
    預期：「[錯誤]」那一行裡有「locator 要寫「摘要」」
    實際：[錯誤] wiki/cards/demo2000-claim.md：demo2000 只讀了摘要，locator 要寫「摘要」；[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 科普當成實驗證據
    預期：「[錯誤]」那一行裡有「科普或新聞只能當 expression」
    實際：[錯誤] wiki/cards/demo2000-claim.md：科普或新聞只能當 expression，不能當研究證據；[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] expression引用論文
    預期：「[錯誤]」那一行裡有「expression 只能引用」
    實際：[錯誤] wiki/cards/demo2000-claim.md：expression 只能引用 kind: popular 的文獻；[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 證據類型亂寫
    預期：「[錯誤]」那一行裡有「type 要是」
    實際：[錯誤] wiki/cards/demo2000-claim.md：type 要是 experiment、expression、model_theory、our_derivation、our_simulation、review 之一；[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 有數字但units寫無數值
    預期：「[錯誤]」那一行裡有「units 不能寫「無數值」」
    實際：[錯誤] wiki/cards/demo2000-claim.md：主張裡有數字，units 不能寫「無數值」（要寫單位或「無因次」）
[PASS] 英文原文引用太長
    預期：「[錯誤]」那一行裡有「超過 50」
    實際：[錯誤] wiki/cards/demo2000-claim.md：英文原文引用 60 個字，超過 50
[PASS] 證據卡少原文依據
    預期：「[錯誤]」那一行裡有「「## 原文依據」」
    實際：[錯誤] wiki/cards/demo2000-claim.md：缺少段落或段落是空的「## 原文依據」
[PASS] 自己的模擬指向不存在的檔案
    預期：「[錯誤]」那一行裡有「source 要是repo裡存在的檔案」
    實際：[錯誤] wiki/cards/demo2000-claim.md：source 要是repo裡存在的檔案（找不到 audition/nope.py）；[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 自己的模擬用..跳出repo
    預期：「[錯誤]」那一行裡有「source 要是repo裡存在的檔案」
    實際：[錯誤] wiki/cards/demo2000-claim.md：source 要是repo裡存在的檔案（找不到 ../etc/passwd）；[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] related指到不存在的卡
    預期：「[錯誤]」那一行裡有「related 的 nope-card 不存在」
    實際：[錯誤] wiki/cards/demo2000-claim.md：related 的 nope-card 不存在
[PASS] 卡片id跟檔名不同
    預期：「[錯誤]」那一行裡有「跟檔名不一樣」
    實際：[錯誤] wiki/cards/demo2000-claim.md：id other 跟檔名不一樣
[PASS] 索引沒列卡片
    預期：「[錯誤]」那一行裡有「沒有列出證據卡」
    實際：[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py；[錯誤] wiki/index.md：沒有列出證據卡 demo2000-claim
[PASS] 放了PDF
    預期：「[錯誤]」那一行裡有「PDF不能放進repo」
    實際：[錯誤] raw.pdf：PDF不能放進repo
[PASS] 檔案裡有像學號的數字
    預期：「[錯誤]」那一行裡有「像學號」
    實際：[錯誤] note.md:1：疑似像學號的9位數字
[PASS] 檔案裡有個人信箱
    預期：「[錯誤]」那一行裡有「電子郵件」
    實際：[錯誤] note.md:1：疑似電子郵件
[PASS] 檔案裡有本機路徑
    預期：「[錯誤]」那一行裡有「本機路徑」
    實際：[錯誤] note.md:1：疑似本機路徑
[PASS] 檔案裡有金鑰
    預期：「[錯誤]」那一行裡有「金鑰或Token」
    實際：[錯誤] note.md:1：疑似金鑰或Token
[PASS] 檔案裡有手機號碼
    預期：「[錯誤]」那一行裡有「手機號碼」
    實際：[錯誤] note.md:1：疑似手機號碼
[PASS] log裡的小數不能誤判成學號或電話
    預期：沒有錯誤
    實際：沒有錯誤
[PASS] 欄位重複
    預期：「[錯誤]」那一行裡有「欄位 status 出現不只一次」
    實際：[錯誤] wiki/cards/demo2000-claim.md：欄位 status 出現不只一次；[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 索引列了不存在的卡
    預期：「[錯誤]」那一行裡有「cards/deleted-card.md 不存在」
    實際：[錯誤] wiki/index.md：列出的 cards/deleted-card.md 不存在
[PASS] 有數字的主張，locator只寫全文
    預期：「[錯誤]」那一行裡有「locator 要到頁碼」
    實際：[錯誤] wiki/cards/demo2000-claim.md：主張裡有數字，locator 要到頁碼、章節、公式或圖表編號（或寫「摘要」）
[PASS] 自己的模擬指向不會上傳的檔案
    預期：「[錯誤]」那一行裡有「不會上傳的檔案」
    實際：[錯誤] wiki/cards/demo2000-claim.md：source local/sim.py 是不會上傳的檔案，別人沒辦法核對；[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 歷史裡有金鑰：平常是警告
    預期：沒有錯誤，警告裡有「金鑰或Token」
    實際：[警告] Git歷史 9c07708 note.md：疑似金鑰或Token；[警告] wiki/sources：實際讀過、而且有confirmed證據卡的獨立論文 1 篇，還不到 5 篇；；文獻 1 篇（算進5篇的獨立論文 1 篇），證據卡 1 張（pending 0 張）。；錯誤 0 個，警告 2 個。
[PASS] 歷史裡有金鑰：--strict是錯誤
    預期：「[錯誤]」那一行裡有「金鑰或Token」
    實際：[錯誤] Git歷史 07932b5 note.md：疑似金鑰或Token
[PASS] 歷史裡有PDF：--strict是錯誤
    預期：「[錯誤]」那一行裡有「出現過PDF：a.pdf」
    實際：[錯誤] Git歷史：出現過PDF：a.pdf
[PASS] 有confirmed卡的論文才算進5篇
    預期：沒有錯誤，輸出裡有「算進5篇的獨立論文 1 篇」
    實際：['文獻 1 篇（算進5篇的獨立論文 1 篇），證據卡 1 張（pending 0 張）。', '錯誤 0 個，警告 1 個。']
[PASS] 沒有confirmed卡的論文不算
    預期：沒有錯誤，輸出裡有「算進5篇的獨立論文 0 篇」
    實際：['文獻 1 篇（算進5篇的獨立論文 0 篇），證據卡 1 張（pending 1 張）。', '錯誤 0 個，警告 1 個。']
[PASS] SHA-256表格裡的雜湊值不算學號
    預期：沒有錯誤
    實際：沒有錯誤
[PASS] SHA-256表格裡的雜湊值不算手機
    預期：沒有錯誤
    實際：沒有錯誤
[PASS] SHA-256欄的雜湊後面接說明也排除
    預期：沒有錯誤
    實際：沒有錯誤
[PASS] 同一行有SHA-256標記的雜湊值不算學號
    預期：沒有錯誤
    實際：沒有錯誤
[PASS] 學號緊接中文照樣偵測
    預期：「[錯誤]」那一行裡有「像學號的9位數字」
    實際：[錯誤] note.md:1：疑似像學號的9位數字
[PASS] 學號夾在英文字母中照樣偵測
    預期：「[錯誤]」那一行裡有「像學號的9位數字」
    實際：[錯誤] note.md:1：疑似像學號的9位數字
[PASS] 沒有分隔的手機號碼照樣偵測
    預期：「[錯誤]」那一行裡有「手機號碼」
    實際：[錯誤] note.md:1：疑似手機號碼
[PASS] 一般句子裡的學號照樣偵測
    預期：「[錯誤]」那一行裡有「像學號的9位數字」
    實際：[錯誤] note.md:1：疑似像學號的9位數字
[PASS] 沒有SHA-256標記的64位十六進位不放行
    預期：「[錯誤]」那一行裡有「像學號的9位數字」
    實際：[錯誤] note.md:1：疑似像學號的9位數字
[PASS] SHA-256欄裡只有63位不放行
    預期：「[錯誤]」那一行裡有「像學號的9位數字」
    實際：[錯誤] note.md:3：疑似像學號的9位數字
[PASS] SHA-256欄裡沒有反引號不放行
    預期：「[錯誤]」那一行裡有「像學號的9位數字」
    實際：[錯誤] note.md:3：疑似像學號的9位數字
[PASS] 雜湊放在SHA-256以外的欄不放行
    預期：「[錯誤]」那一行裡有「像學號的9位數字」
    實際：[錯誤] note.md:3：疑似像學號的9位數字
[PASS] 表格結束後的雜湊不放行
    預期：「[錯誤]」那一行裡有「像學號的9位數字」
    實際：[錯誤] note.md:5：疑似像學號的9位數字
[PASS] SHA-256表格同一列的學號照樣偵測
    預期：「[錯誤]」那一行裡有「像學號的9位數字」
    實際：[錯誤] note.md:3：疑似像學號的9位數字
[PASS] SHA-256表格同一列的金鑰照樣偵測
    預期：「[錯誤]」那一行裡有「金鑰或Token」
    實際：[錯誤] note.md:3：疑似金鑰或Token
[PASS] 歷史裡SHA-256表格的雜湊不算學號（--strict）
    預期：沒有錯誤
    實際：沒有錯誤
[PASS] 歷史裡沒有標記的雜湊照樣抓（--strict）
    預期：「[錯誤]」那一行裡有「像學號的9位數字」
    實際：[錯誤] Git歷史 fdde6ef note.md：疑似像學號的9位數字
[PASS] 歷史：SHA-256表格中間加一列，diff看不到表頭也排除（--strict）
    預期：沒有錯誤
    實際：沒有錯誤
[PASS] 歷史：SHA-256表格中間加的那列有金鑰照樣抓（--strict）
    預期：「[錯誤]」那一行裡有「金鑰或Token」
    實際：[錯誤] Git歷史 46ddabb note.md：疑似金鑰或Token
[PASS] 歷史：SHA-256表格中間加的那列有學號照樣抓（--strict）
    預期：「[錯誤]」那一行裡有「像學號的9位數字」
    實際：[錯誤] Git歷史 e704b91 note.md：疑似像學號的9位數字
[PASS] 歷史：表格結束很久之後加的雜湊照樣抓（--strict）
    預期：「[錯誤]」那一行裡有「像學號的9位數字」
    實際：[錯誤] Git歷史 1fa3282 note.md：疑似像學號的9位數字
[PASS] 歷史：沒有SHA-256欄的表格加雜湊照樣抓（--strict）
    預期：「[錯誤]」那一行裡有「像學號的9位數字」
    實際：[錯誤] Git歷史 3a37528 note.md：疑似像學號的9位數字
[PASS] 改了卡片的主張沒重建索引要擋
    預期：「[錯誤]」那一行裡有「不同步」
    實際：[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 改了卡片的狀態沒重建索引要擋
    預期：「[錯誤]」那一行裡有「不同步」
    實際：[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 改了卡片的條件沒重建索引要擋
    預期：「[錯誤]」那一行裡有「不同步」
    實際：[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 改了文獻的閱讀狀態沒重建索引要擋
    預期：「[錯誤]」那一行裡有「不同步」
    實際：[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 新增卡片沒重建索引要擋
    預期：「[錯誤]」那一行裡有「不同步」
    實際：[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py；[錯誤] wiki/index.md：沒有列出證據卡 demo2000-second
[PASS] 手改自動產生的摘要要擋
    預期：「[錯誤]」那一行裡有「不同步」
    實際：[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 自動產生的標記被刪掉要擋
    預期：「[錯誤]」那一行裡有「找不到自動產生區塊的標記」
    實際：[錯誤] wiki/index.md：找不到自動產生區塊的標記，請照原本的格式放回兩行標記，再跑 python3 scripts/build_index.py
[PASS] 改了卡片也重建索引就通過
    預期：沒有錯誤
    實際：沒有錯誤
[PASS] 改人工寫的導覽不用重建
    預期：沒有錯誤
    實際：沒有錯誤
[PASS] 主張裡的相對連結在索引裡改成從wiki出發
    預期：沒有錯誤
    實際：沒有錯誤
[FAIL] 偽表頭：資料列有SHA-256格，下一列同欄的雜湊不放行
    預期：「[錯誤]」那一行裡有「像學號的9位數字」
    實際：[警告] wiki/sources：實際讀過、而且有confirmed證據卡的獨立論文 1 篇，還不到 5 篇

文獻 1 篇（算進5篇的獨立論文 1 篇），證據卡 1 張（pending 0 張）。
錯誤 0 個，警告 1 個。
[FAIL] 表頭後面沒有分隔列，不算表格，不放行
    預期：「[錯誤]」那一行裡有「像學號的9位數字」
    實際：[警告] wiki/sources：實際讀過、而且有confirmed證據卡的獨立論文 1 篇，還不到 5 篇

文獻 1 篇（算進5篇的獨立論文 1 篇），證據卡 1 張（pending 0 張）。
錯誤 0 個，警告 1 個。
[FAIL] 表頭寫SHA-256之外的字（SHA-256值或備註），不放行
    預期：「[錯誤]」那一行裡有「像學號的9位數字」
    實際：[警告] wiki/sources：實際讀過、而且有confirmed證據卡的獨立論文 1 篇，還不到 5 篇

文獻 1 篇（算進5篇的獨立論文 1 篇），證據卡 1 張（pending 0 張）。
錯誤 0 個，警告 1 個。
[FAIL] 資料列的格數跟表頭不同，不放行
    預期：「[錯誤]」那一行裡有「像學號的9位數字」
    實際：[警告] wiki/sources：實際讀過、而且有confirmed證據卡的獨立論文 1 篇，還不到 5 篇

文獻 1 篇（算進5篇的獨立論文 1 篇），證據卡 1 張（pending 0 張）。
錯誤 0 個，警告 1 個。
[FAIL] SHA-256欄的雜湊後面接的不是括號說明，不放行
    預期：「[錯誤]」那一行裡有「像學號的9位數字」
    實際：[警告] wiki/sources：實際讀過、而且有confirmed證據卡的獨立論文 1 篇，還不到 5 篇

文獻 1 篇（算進5篇的獨立論文 1 篇），證據卡 1 張（pending 0 張）。
錯誤 0 個，警告 1 個。
[FAIL] NotSHA-256這種標記不放行
    預期：「[錯誤]」那一行裡有「手機號碼」
    實際：[警告] wiki/sources：實際讀過、而且有confirmed證據卡的獨立論文 1 篇，還不到 5 篇

文獻 1 篇（算進5篇的獨立論文 1 篇），證據卡 1 張（pending 0 張）。
錯誤 0 個，警告 1 個。
[PASS] SHA-256-old這種標記不放行
    預期：「[錯誤]」那一行裡有「手機號碼」
    實際：[錯誤] note.md:1：疑似手機號碼
[PASS] 偽表頭那列同一行的信箱照樣抓
    預期：「[錯誤]」那一行裡有「電子郵件」
    實際：[錯誤] note.md:3：疑似電子郵件
[FAIL] 索引的起訖標記重複要擋
    預期：「[錯誤]」那一行裡有「標記要各出現一次」
    實際：[警告] wiki/sources：實際讀過、而且有confirmed證據卡的獨立論文 1 篇，還不到 5 篇

文獻 1 篇（算進5篇的獨立論文 1 篇），證據卡 1 張（pending 0 張）。
錯誤 0 個，警告 1 個。
[FAIL] 索引的標記沒有獨立成行要擋
    預期：「[錯誤]」那一行裡有「標記要各出現一次」
    實際：[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[FAIL] 索引的結束標記在開始標記前面要擋
    預期：「[錯誤]」那一行裡有「標記要各出現一次」
    實際：[錯誤] wiki/index.md：找不到自動產生區塊的標記，請照原本的格式放回兩行標記，再跑 python3 scripts/build_index.py；[錯誤] wiki/index.md：沒有列出文獻 demo2000；[錯誤] wiki/index.md：沒有列出證據卡 demo2000-claim
[FAIL] 卡片有兩個「## 主張」要擋
    預期：「[錯誤]」那一行裡有「「## 主張」出現不只一次」
    實際：[警告] wiki/sources：實際讀過、而且有confirmed證據卡的獨立論文 1 篇，還不到 5 篇

文獻 1 篇（算進5篇的獨立論文 1 篇），證據卡 1 張（pending 0 張）。
錯誤 0 個，警告 1 個。
[FAIL] 卡片有兩個「## 限制」要擋
    預期：「[錯誤]」那一行裡有「「## 限制」出現不只一次」
    實際：[警告] wiki/sources：實際讀過、而且有confirmed證據卡的獨立論文 1 篇，還不到 5 篇

文獻 1 篇（算進5篇的獨立論文 1 篇），證據卡 1 張（pending 0 張）。
錯誤 0 個，警告 1 個。
[FAIL] 主張裡的錨點連結在索引裡指回那張卡
    預期：沒有錯誤；wiki/index.md裡要有「見[限制](cards/demo2000-claim.md#限制)。」
    實際：沒有錯誤；wiki/index.md裡找不到「見[限制](cards/demo2000-claim.md#限制)。」
[FAIL] 主張裡行內程式碼的連結字樣不改
    預期：沒有錯誤；wiki/index.md裡要有「寫法是`[x](y.md)`。」
    實際：[錯誤] wiki/index.md：列出的 cards/y.md 不存在
[警告] wiki/sources：實際讀過、而且有confirmed證據卡的獨立論文 1 篇，還不到 5 篇

文獻 1 篇（算進5篇的獨立論文 1 篇），證據卡 1 張（pending 0 張）。
錯誤 1 個，警告 1 個。；wiki/index.md裡找不到「寫法是`[x](y.md)`。」
[FAIL] 主張裡程式碼區塊的連結字樣不改
    預期：沒有錯誤；wiki/index.md裡要有「```
[x](y.md)
```」
    實際：[錯誤] wiki/index.md：列出的 cards/y.md 不存在
[警告] wiki/sources：實際讀過、而且有confirmed證據卡的獨立論文 1 篇，還不到 5 篇

文獻 1 篇（算進5篇的獨立論文 1 篇），證據卡 1 張（pending 0 張）。
錯誤 1 個，警告 1 個。；wiki/index.md裡找不到「```
[x](y.md)
```」
[FAIL] Git設了會失敗的textconv，歷史裡的PDF照樣報（--strict）
    預期：「[錯誤]」那一行裡有「出現過PDF：a.pdf」
    實際：沒有錯誤
[FAIL] Git設了會失敗的textconv，歷史裡的金鑰照樣抓（--strict）
    預期：「[錯誤]」那一行裡有「金鑰或Token」
    實際：沒有錯誤
[FAIL] Git指令失敗要報錯，不能當成沒問題
    預期：「[錯誤]」那一行裡有「Git指令失敗」
    實際：沒有錯誤
[FAIL] Git指令失敗在--strict也要報錯
    預期：「[錯誤]」那一行裡有「Git指令失敗」
    實際：沒有錯誤

共94個情境（其中判定規則5個），失敗18個。
exit=1
```


========== 程式或執行輸出：runs/logs/2026-11-12-eng-tests-after.log ==========

```
[PASS] 判定規則：關鍵字只在警告行，另有無關錯誤：不能算通過
[PASS] 判定規則：關鍵字在錯誤行：算通過
[PASS] 判定規則：結束代碼1但沒有任何錯誤行（例如程式當掉）：不能算通過
[PASS] 判定規則：預期沒有錯誤，卻有錯誤行：不能算通過
[PASS] 判定規則：預期只有警告，卻也有錯誤行：不能算通過
[PASS] 正常資料
    預期：沒有錯誤
    實際：沒有錯誤
[PASS] 主張裡只有年份，units寫無數值
    預期：沒有錯誤
    實際：沒有錯誤
[PASS] 文獻少一個欄位
    預期：「[錯誤]」那一行裡有「缺少欄位 venue」
    實際：[錯誤] wiki/sources/demo2000.md：缺少欄位 venue
[PASS] 閱讀狀態亂寫
    預期：「[錯誤]」那一行裡有「read_status 要是」
    實際：[錯誤] wiki/sources/demo2000.md：read_status 要是 全文已讀、只讀摘要、尚未查證、部分章節 之一；[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] DOI格式錯
    預期：「[錯誤]」那一行裡有「doi 格式不對」
    實際：[錯誤] wiki/sources/demo2000.md：doi 格式不對（寫 10.xxxx/... 或「無」）
[PASS] 網址不是https
    預期：「[錯誤]」那一行裡有「url 要用 https://」
    實際：[錯誤] wiki/sources/demo2000.md：url 要用 https://
[PASS] 文獻少段落
    預期：「[錯誤]」那一行裡有「缺少段落「## 限制」」
    實際：[錯誤] wiki/sources/demo2000.md：缺少段落「## 限制」
[PASS] 證據卡的文獻不存在
    預期：「[錯誤]」那一行裡有「找不到」
    實際：[錯誤] wiki/cards/demo2000-claim.md：source ghost1999 在 wiki/sources/ 裡找不到；[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 文獻尚未查證，卡片卻是confirmed
    預期：「[錯誤]」那一行裡有「不能是 confirmed」
    實際：[錯誤] wiki/cards/demo2000-claim.md：demo2000 還是「尚未查證」，卡片不能是 confirmed；[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 只讀摘要，locator沒寫摘要
    預期：「[錯誤]」那一行裡有「locator 要寫「摘要」」
    實際：[錯誤] wiki/cards/demo2000-claim.md：demo2000 只讀了摘要，locator 要寫「摘要」；[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 科普當成實驗證據
    預期：「[錯誤]」那一行裡有「科普或新聞只能當 expression」
    實際：[錯誤] wiki/cards/demo2000-claim.md：科普或新聞只能當 expression，不能當研究證據；[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] expression引用論文
    預期：「[錯誤]」那一行裡有「expression 只能引用」
    實際：[錯誤] wiki/cards/demo2000-claim.md：expression 只能引用 kind: popular 的文獻；[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 證據類型亂寫
    預期：「[錯誤]」那一行裡有「type 要是」
    實際：[錯誤] wiki/cards/demo2000-claim.md：type 要是 experiment、expression、model_theory、our_derivation、our_simulation、review 之一；[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 有數字但units寫無數值
    預期：「[錯誤]」那一行裡有「units 不能寫「無數值」」
    實際：[錯誤] wiki/cards/demo2000-claim.md：主張裡有數字，units 不能寫「無數值」（要寫單位或「無因次」）
[PASS] 英文原文引用太長
    預期：「[錯誤]」那一行裡有「超過 50」
    實際：[錯誤] wiki/cards/demo2000-claim.md：英文原文引用 60 個字，超過 50
[PASS] 證據卡少原文依據
    預期：「[錯誤]」那一行裡有「「## 原文依據」」
    實際：[錯誤] wiki/cards/demo2000-claim.md：缺少段落或段落是空的「## 原文依據」
[PASS] 自己的模擬指向不存在的檔案
    預期：「[錯誤]」那一行裡有「source 要是repo裡存在的檔案」
    實際：[錯誤] wiki/cards/demo2000-claim.md：source 要是repo裡存在的檔案（找不到 audition/nope.py）；[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 自己的模擬用..跳出repo
    預期：「[錯誤]」那一行裡有「source 要是repo裡存在的檔案」
    實際：[錯誤] wiki/cards/demo2000-claim.md：source 要是repo裡存在的檔案（找不到 ../etc/passwd）；[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] related指到不存在的卡
    預期：「[錯誤]」那一行裡有「related 的 nope-card 不存在」
    實際：[錯誤] wiki/cards/demo2000-claim.md：related 的 nope-card 不存在
[PASS] 卡片id跟檔名不同
    預期：「[錯誤]」那一行裡有「跟檔名不一樣」
    實際：[錯誤] wiki/cards/demo2000-claim.md：id other 跟檔名不一樣
[PASS] 索引沒列卡片
    預期：「[錯誤]」那一行裡有「沒有列出證據卡」
    實際：[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py；[錯誤] wiki/index.md：沒有列出證據卡 demo2000-claim
[PASS] 放了PDF
    預期：「[錯誤]」那一行裡有「PDF不能放進repo」
    實際：[錯誤] raw.pdf：PDF不能放進repo
[PASS] 檔案裡有像學號的數字
    預期：「[錯誤]」那一行裡有「像學號」
    實際：[錯誤] note.md:1：疑似像學號的9位數字
[PASS] 檔案裡有個人信箱
    預期：「[錯誤]」那一行裡有「電子郵件」
    實際：[錯誤] note.md:1：疑似電子郵件
[PASS] 檔案裡有本機路徑
    預期：「[錯誤]」那一行裡有「本機路徑」
    實際：[錯誤] note.md:1：疑似本機路徑
[PASS] 檔案裡有金鑰
    預期：「[錯誤]」那一行裡有「金鑰或Token」
    實際：[錯誤] note.md:1：疑似金鑰或Token
[PASS] 檔案裡有手機號碼
    預期：「[錯誤]」那一行裡有「手機號碼」
    實際：[錯誤] note.md:1：疑似手機號碼
[PASS] log裡的小數不能誤判成學號或電話
    預期：沒有錯誤
    實際：沒有錯誤
[PASS] 欄位重複
    預期：「[錯誤]」那一行裡有「欄位 status 出現不只一次」
    實際：[錯誤] wiki/cards/demo2000-claim.md：欄位 status 出現不只一次；[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 索引列了不存在的卡
    預期：「[錯誤]」那一行裡有「cards/deleted-card.md 不存在」
    實際：[錯誤] wiki/index.md：列出的 cards/deleted-card.md 不存在
[PASS] 有數字的主張，locator只寫全文
    預期：「[錯誤]」那一行裡有「locator 要到頁碼」
    實際：[錯誤] wiki/cards/demo2000-claim.md：主張裡有數字，locator 要到頁碼、章節、公式或圖表編號（或寫「摘要」）
[PASS] 自己的模擬指向不會上傳的檔案
    預期：「[錯誤]」那一行裡有「不會上傳的檔案」
    實際：[錯誤] wiki/cards/demo2000-claim.md：source local/sim.py 是不會上傳的檔案，別人沒辦法核對；[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 歷史裡有金鑰：平常是警告
    預期：沒有錯誤，警告裡有「金鑰或Token」
    實際：[警告] Git歷史 c3fbda2 note.md：疑似金鑰或Token；[警告] wiki/sources：實際讀過、而且有confirmed證據卡的獨立論文 1 篇，還不到 5 篇；；文獻 1 篇（算進5篇的獨立論文 1 篇），證據卡 1 張（pending 0 張）。；錯誤 0 個，警告 2 個。
[PASS] 歷史裡有金鑰：--strict是錯誤
    預期：「[錯誤]」那一行裡有「金鑰或Token」
    實際：[錯誤] Git歷史 c3fbda2 note.md：疑似金鑰或Token
[PASS] 歷史裡有PDF：--strict是錯誤
    預期：「[錯誤]」那一行裡有「出現過PDF：a.pdf」
    實際：[錯誤] Git歷史：出現過PDF：a.pdf
[PASS] 有confirmed卡的論文才算進5篇
    預期：沒有錯誤，輸出裡有「算進5篇的獨立論文 1 篇」
    實際：['文獻 1 篇（算進5篇的獨立論文 1 篇），證據卡 1 張（pending 0 張）。', '錯誤 0 個，警告 1 個。']
[PASS] 沒有confirmed卡的論文不算
    預期：沒有錯誤，輸出裡有「算進5篇的獨立論文 0 篇」
    實際：['文獻 1 篇（算進5篇的獨立論文 0 篇），證據卡 1 張（pending 1 張）。', '錯誤 0 個，警告 1 個。']
[PASS] SHA-256表格裡的雜湊值不算學號
    預期：沒有錯誤
    實際：沒有錯誤
[PASS] SHA-256表格裡的雜湊值不算手機
    預期：沒有錯誤
    實際：沒有錯誤
[PASS] SHA-256欄的雜湊後面接說明也排除
    預期：沒有錯誤
    實際：沒有錯誤
[PASS] 同一行有SHA-256標記的雜湊值不算學號
    預期：沒有錯誤
    實際：沒有錯誤
[PASS] 學號緊接中文照樣偵測
    預期：「[錯誤]」那一行裡有「像學號的9位數字」
    實際：[錯誤] note.md:1：疑似像學號的9位數字
[PASS] 學號夾在英文字母中照樣偵測
    預期：「[錯誤]」那一行裡有「像學號的9位數字」
    實際：[錯誤] note.md:1：疑似像學號的9位數字
[PASS] 沒有分隔的手機號碼照樣偵測
    預期：「[錯誤]」那一行裡有「手機號碼」
    實際：[錯誤] note.md:1：疑似手機號碼
[PASS] 一般句子裡的學號照樣偵測
    預期：「[錯誤]」那一行裡有「像學號的9位數字」
    實際：[錯誤] note.md:1：疑似像學號的9位數字
[PASS] 沒有SHA-256標記的64位十六進位不放行
    預期：「[錯誤]」那一行裡有「像學號的9位數字」
    實際：[錯誤] note.md:1：疑似像學號的9位數字
[PASS] SHA-256欄裡只有63位不放行
    預期：「[錯誤]」那一行裡有「像學號的9位數字」
    實際：[錯誤] note.md:3：疑似像學號的9位數字
[PASS] SHA-256欄裡沒有反引號不放行
    預期：「[錯誤]」那一行裡有「像學號的9位數字」
    實際：[錯誤] note.md:3：疑似像學號的9位數字
[PASS] 雜湊放在SHA-256以外的欄不放行
    預期：「[錯誤]」那一行裡有「像學號的9位數字」
    實際：[錯誤] note.md:3：疑似像學號的9位數字
[PASS] 表格結束後的雜湊不放行
    預期：「[錯誤]」那一行裡有「像學號的9位數字」
    實際：[錯誤] note.md:5：疑似像學號的9位數字
[PASS] SHA-256表格同一列的學號照樣偵測
    預期：「[錯誤]」那一行裡有「像學號的9位數字」
    實際：[錯誤] note.md:3：疑似像學號的9位數字
[PASS] SHA-256表格同一列的金鑰照樣偵測
    預期：「[錯誤]」那一行裡有「金鑰或Token」
    實際：[錯誤] note.md:3：疑似金鑰或Token
[PASS] 歷史裡SHA-256表格的雜湊不算學號（--strict）
    預期：沒有錯誤
    實際：沒有錯誤
[PASS] 歷史裡沒有標記的雜湊照樣抓（--strict）
    預期：「[錯誤]」那一行裡有「像學號的9位數字」
    實際：[錯誤] Git歷史 8613c27 note.md：疑似像學號的9位數字
[PASS] 歷史：SHA-256表格中間加一列，diff看不到表頭也排除（--strict）
    預期：沒有錯誤
    實際：沒有錯誤
[PASS] 歷史：SHA-256表格中間加的那列有金鑰照樣抓（--strict）
    預期：「[錯誤]」那一行裡有「金鑰或Token」
    實際：[錯誤] Git歷史 549880a note.md：疑似金鑰或Token
[PASS] 歷史：SHA-256表格中間加的那列有學號照樣抓（--strict）
    預期：「[錯誤]」那一行裡有「像學號的9位數字」
    實際：[錯誤] Git歷史 09d7258 note.md：疑似像學號的9位數字
[PASS] 歷史：表格結束很久之後加的雜湊照樣抓（--strict）
    預期：「[錯誤]」那一行裡有「像學號的9位數字」
    實際：[錯誤] Git歷史 3a8ced0 note.md：疑似像學號的9位數字
[PASS] 歷史：沒有SHA-256欄的表格加雜湊照樣抓（--strict）
    預期：「[錯誤]」那一行裡有「像學號的9位數字」
    實際：[錯誤] Git歷史 4688372 note.md：疑似像學號的9位數字
[PASS] 改了卡片的主張沒重建索引要擋
    預期：「[錯誤]」那一行裡有「不同步」
    實際：[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 改了卡片的狀態沒重建索引要擋
    預期：「[錯誤]」那一行裡有「不同步」
    實際：[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 改了卡片的條件沒重建索引要擋
    預期：「[錯誤]」那一行裡有「不同步」
    實際：[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 改了文獻的閱讀狀態沒重建索引要擋
    預期：「[錯誤]」那一行裡有「不同步」
    實際：[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 新增卡片沒重建索引要擋
    預期：「[錯誤]」那一行裡有「不同步」
    實際：[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py；[錯誤] wiki/index.md：沒有列出證據卡 demo2000-second
[PASS] 手改自動產生的摘要要擋
    預期：「[錯誤]」那一行裡有「不同步」
    實際：[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 自動產生的標記被刪掉要擋
    預期：「[錯誤]」那一行裡有「找不到自動產生區塊的標記」
    實際：[錯誤] wiki/index.md：找不到自動產生區塊的標記，或標記不合規定（標記要各出現一次、獨立成行，開始在結束前面）；請照原本的格式放回兩行標記，再跑 python3 scripts/build_index.py
[PASS] 改了卡片也重建索引就通過
    預期：沒有錯誤
    實際：沒有錯誤
[PASS] 改人工寫的導覽不用重建
    預期：沒有錯誤
    實際：沒有錯誤
[PASS] 主張裡的相對連結在索引裡改成從wiki出發
    預期：沒有錯誤
    實際：沒有錯誤
[PASS] 偽表頭：資料列有SHA-256格，下一列同欄的雜湊不放行
    預期：「[錯誤]」那一行裡有「像學號的9位數字」
    實際：[錯誤] note.md:4：疑似像學號的9位數字
[PASS] 表頭後面沒有分隔列，不算表格，不放行
    預期：「[錯誤]」那一行裡有「像學號的9位數字」
    實際：[錯誤] note.md:2：疑似像學號的9位數字
[PASS] 表頭寫SHA-256之外的字（SHA-256值或備註），不放行
    預期：「[錯誤]」那一行裡有「像學號的9位數字」
    實際：[錯誤] note.md:3：疑似像學號的9位數字
[PASS] 資料列的格數跟表頭不同，不放行
    預期：「[錯誤]」那一行裡有「像學號的9位數字」
    實際：[錯誤] note.md:3：疑似像學號的9位數字
[PASS] SHA-256欄的雜湊後面接的不是括號說明，不放行
    預期：「[錯誤]」那一行裡有「像學號的9位數字」
    實際：[錯誤] note.md:3：疑似像學號的9位數字
[PASS] NotSHA-256這種標記不放行
    預期：「[錯誤]」那一行裡有「手機號碼」
    實際：[錯誤] note.md:1：疑似手機號碼
[PASS] SHA-256-old這種標記不放行
    預期：「[錯誤]」那一行裡有「手機號碼」
    實際：[錯誤] note.md:1：疑似手機號碼
[PASS] 偽表頭那列同一行的信箱照樣抓
    預期：「[錯誤]」那一行裡有「電子郵件」
    實際：[錯誤] note.md:3：疑似電子郵件
[PASS] 索引的起訖標記重複要擋
    預期：「[錯誤]」那一行裡有「標記要各出現一次」
    實際：[錯誤] wiki/index.md：找不到自動產生區塊的標記，或標記不合規定（標記要各出現一次、獨立成行，開始在結束前面）；請照原本的格式放回兩行標記，再跑 python3 scripts/build_index.py
[PASS] 索引的標記沒有獨立成行要擋
    預期：「[錯誤]」那一行裡有「標記要各出現一次」
    實際：[錯誤] wiki/index.md：找不到自動產生區塊的標記，或標記不合規定（標記要各出現一次、獨立成行，開始在結束前面）；請照原本的格式放回兩行標記，再跑 python3 scripts/build_index.py
[PASS] 索引的結束標記在開始標記前面要擋
    預期：「[錯誤]」那一行裡有「標記要各出現一次」
    實際：[錯誤] wiki/index.md：找不到自動產生區塊的標記，或標記不合規定（標記要各出現一次、獨立成行，開始在結束前面）；請照原本的格式放回兩行標記，再跑 python3 scripts/build_index.py；[錯誤] wiki/index.md：沒有列出文獻 demo2000；[錯誤] wiki/index.md：沒有列出證據卡 demo2000-claim
[PASS] 卡片有兩個「## 主張」要擋
    預期：「[錯誤]」那一行裡有「「## 主張」出現不只一次」
    實際：[錯誤] wiki/cards/demo2000-claim.md：段落「## 主張」出現不只一次
[PASS] 卡片有兩個「## 限制」要擋
    預期：「[錯誤]」那一行裡有「「## 限制」出現不只一次」
    實際：[錯誤] wiki/cards/demo2000-claim.md：段落「## 限制」出現不只一次
[PASS] 主張裡的錨點連結在索引裡指回那張卡
    預期：沒有錯誤；wiki/index.md裡要有「見[限制](cards/demo2000-claim.md#限制)。」
    實際：沒有錯誤
[PASS] 主張裡行內程式碼的連結字樣不改
    預期：沒有錯誤；wiki/index.md裡要有「寫法是`[x](y.md)`。」
    實際：沒有錯誤
[PASS] 主張裡程式碼區塊的連結字樣不改
    預期：沒有錯誤；wiki/index.md裡要有「```
[x](y.md)
```」
    實際：沒有錯誤
[PASS] Git設了會失敗的textconv，歷史裡的PDF照樣報（--strict）
    預期：「[錯誤]」那一行裡有「出現過PDF：a.pdf」
    實際：[錯誤] Git歷史：出現過PDF：a.pdf
[PASS] Git設了會失敗的textconv，歷史裡的金鑰照樣抓（--strict）
    預期：「[錯誤]」那一行裡有「金鑰或Token」
    實際：[錯誤] Git歷史 cf58e9a note.md：疑似金鑰或Token
[PASS] Git指令失敗要報錯，不能當成沒問題
    預期：「[錯誤]」那一行裡有「Git指令失敗」
    實際：[錯誤] Git歷史：Git指令失敗，歷史沒有檢查完（git log --all -p --no-color --no-textconv --format=commit %h）：fatal: unable to read ce013625030ba8dba906f756967f9e9ca394464a
[PASS] Git指令失敗在--strict也要報錯
    預期：「[錯誤]」那一行裡有「Git指令失敗」
    實際：[錯誤] Git歷史：Git指令失敗，歷史沒有檢查完（git log --all -p --no-color --no-textconv --format=commit %h）：fatal: unable to read ce013625030ba8dba906f756967f9e9ca394464a

共94個情境（其中判定規則5個），失敗0個。
exit=0
```


========== 程式或執行輸出：runs/logs/2026-11-12-eng-judge-before.log ==========

```
舊的判定寫法（第4輪前的tests/test_check_wiki.py）對判定規則情境的結果：
[FAIL] 關鍵字只在警告行，另有無關錯誤：不能算通過：應該False，舊寫法True
[PASS] 關鍵字在錯誤行：算通過：應該True，舊寫法True
[FAIL] 結束代碼1但沒有任何錯誤行（例如程式當掉）：不能算通過：應該False，舊寫法True
[FAIL] 預期沒有錯誤，卻有錯誤行：不能算通過：應該False，舊寫法True
[FAIL] 預期只有警告，卻也有錯誤行：不能算通過：應該False，舊寫法True
失敗4個
```


========== 程式或執行輸出：runs/logs/2026-11-12-eng-history-compare.log ==========

```
掃到的新增行數：old 13858 new 13858
只在old出現 0 只在new出現 0
在SHA-256表格欄裡的行數：old 255 new 233
```


========== 程式或執行輸出：runs/logs/2026-11-12-eng-verify.log ==========

```
# 工程修復後的完整驗證（commit 0afb1ed）

## 本機工作目錄

$ python3 tests/test_check_wiki.py
共94個情境（其中判定規則5個），失敗0個。
exit=0

$ python3 scripts/build_index.py --check
index.md跟文獻檔、證據卡同步
exit=0

$ python3 scripts/check_wiki.py --strict

文獻 6 篇（算進5篇的獨立論文 6 篇），證據卡 39 張（pending 0 張）。
錯誤 0 個，警告 0 個。
exit=0

$ python3 audition/test_ovm.py
輸出跟audition/run2.log逐字相同
exit=0

## 從GitHub乾淨clone（0afb1ed）

$ python3 tests/test_check_wiki.py
共94個情境（其中判定規則5個），失敗0個。
exit=0

$ python3 scripts/build_index.py --check
index.md跟文獻檔、證據卡同步
exit=0

$ python3 scripts/check_wiki.py --strict

文獻 6 篇（算進5篇的獨立論文 6 篇），證據卡 39 張（pending 0 張）。
錯誤 0 個，警告 0 個。
exit=0

$ python3 audition/test_ovm.py
輸出跟audition/run2.log逐字相同
exit=0

## 本機（有PDF）

$ python3 scripts/check_quotes.py
引用 31 段：逐字找到 22，OCR逐字 8，OCR近似 1，找不到 0，無法比對 0。
exit=0
```


========== 程式或執行輸出：runs/logs/2026-11-12-n3-r4-repro.log ==========

```
f1 資料列以SHA-256開頭被當表頭: [(4, '像學號的9位數字')]
   對照（同樣內容沒有那列）: [(3, '像學號的9位數字')]
f2 NotSHA-256標記: []
   對照（沒有標記）: [(1, '手機號碼')]
a  重複標記後還判定同步: True
b  重複## 主張只留最後一段: 作者做過不同車數的實驗，文中只提到23台的結果：也形成了塞車
c  錨點連結: 見[限制](#limits)，`[x](cards/y.md)`
f1' 資料列第1欄是SHA-256、雜湊在同一欄: []
    對照（沒有那列）: [(3, '像學號的9位數字')]
```


========== 上一輪的審查意見原文 ==========

## 第一部分｜第3輪的問題逐條回覆

依審查包列出的 6 條修正和 18 條索引不一致逐條判定。索引項目的「修好」指索引已補回原先遺漏的條件，或已和卡片、文獻檔一致。

| 卡片id或檔案 | 第3輪的問題 | 修好了嗎（修好／部分修好／沒修好） | 說明 |
|---|---|---|---|
| `stern2018-wave-returns` | A、B、C 的控制方式與調速混在一起 | 修好 | A 用 FollowerStopper，外部設定依序為 6.50、7.00、7.50、8.00，再降回 7.50 m/s。8.00 m/s 時復波，調回後波減弱。B 由受訓駕駛把目標從 14 提到 16 mph，後一段的車速標準差最低（1.19 m/s），恢復一般跟車後復波。C 用帶飽和限制的 PI 控制器自行決定目標，第一個波消除，第二個波減弱。見 Stern 第9–14頁、表1、表2、圖5。1705.01693v1(2) |
| `tadaki2013-critical-density` | 圖8近似自由流，卡片限制卻寫成「看不出塞車」 | 修好 | 已寫出 2030、2934 的定點通過資料為何近似自由流，並保留平均速度略低、波動較大兩項差異。見 Tadaki 第10頁圖8及正文。NewJPhys_15_103034(2) |
| `tadaki2013-density-dependence` | 把第一天 1625、1730 寫成完全未用於分析 | 修好 | 兩場有納入兩天的車速及波動比較，之後才排除於估計臨界密度的選定資料。附錄 C、E 仍有相關圖。見 Tadaki 第5–6頁、第8頁圖5、第17–19頁。NewJPhys_15_103034(2) |
| `orosz2010-ring-stability` | 把大 \(N\) 的整體穩定條件寫成所有波共用一條分界 | 修好 | 已交代固定均勻車距時，首個失穩模態 \(k=1\) 的波數趨近零，整體條件化為式（A8）。有限環道各模態仍按式（A6）判定，首失穩敘述也保留 \(N\ge3\)。見 Orosz 第4467、4475–4476頁。PTRSA2published(2) |
| `wiki/glossary.md`／相變 | 把作者提出的相變判斷寫成比喻 | 修好 | 已寫明 Sugiyama 以非平衡相變解釋穩定性改變，Tadaki 稱為動態相變，並保留「似乎是一階」。見 Sugiyama 第3、7頁及 Tadaki 第11頁。NewJPhys_10_033001(2) NewJPhys_15_103034(2) |
| `wiki/sources/sugiyama2008.md` | 把實驗設定、巡航速度和觀察值概括成影片與圖上的估計 | 修好 | 已區分 230 公尺及 22 台的實驗設定、約 30 km/h 的巡航速度及駕駛要求，以及觀察到的團外車速約 40 km/h、塞車團向後約 20 km/h。見 Sugiyama 第4–6頁、圖2及圖4。NewJPhys_10_033001(2) |
| 索引／`orosz2010-ring-stability` | 漏掉 \(N\ge3\) | 修好 | 主張保留 \(N\ge3\) 和偶數 \(N\) 時 \(k=N/2\) 無有限分界的例外。 |
| 索引／`stern2018-controllers` | 漏掉距離過近時以安全為先 | 修好 | 索引主張保留安全優先。 |
| 索引／`stern2018-results` | 漏掉比較基準、C 的時段與煞車指標定義 | 修好 | 條件列出首次出波且無控制的基準，A、B 各取最佳控制段，C 只有一段。主張採第4.1節定義的過度煞車事件。 |
| 索引／`nagel1992-real-units` | 把粗略的物理換算寫得像固定單位 | 修好 | 條件和主張保留估算性質，結論寫成時間步為秒量級。見 Nagel 第2227–2228頁第5節。ajp-jp1v2p2221(2) |
| 索引／`tadaki2013-density-dependence` | 把約 20 km/h 寫得像所有高密度場次都適用 | 修好 | 條件限定圖4的三場，主張把約 20 km/h 放在 30 台的場次，另述 34 台場次的現象。 |
| 索引／`tadaki2013-metastable` | 漏掉同一密度附近及三場基本圖的判讀依據 | 修好 | 主張寫明圖7(c)的三場與同一密度附近的兩類資料點。 |
| 索引／`tadaki2013-expressway-consistency` | 漏掉速度與車距的粗略換算 | 修好 | 索引保留速度約三倍、所需車距約三倍的比較方式。 |
| 索引／`tadaki2013-high-density` | 把單一 40 台場次概括為一般結果 | 修好 | 條件限定第一天 1940 場，主張指出不確定的是該場觀察是否對應模型預測。 |
| 索引／`bando1995-large-n-note` | 把環道週期邊界擴大到各種邊界條件 | 修好 | 索引和卡片都限定環狀道路的邊界條件。 |
| 索引／`bando1995-velocity-function` | 漏掉倒車發生在失穩情況下 | 修好 | 索引主張保留「在不穩定時」及作者對倒車的解讀。 |
| 索引／`bando1995-spontaneous-jam` | 漏掉產生五團塞車的參數與初始條件 | 修好 | 條件保留模型參數，主張列出近乎等距、首車前移 0.1、所有車初速為零。 |
| 索引／`bando1995-capacity` | 兩個約 0.48 缺少適用條件 | 修好 | 條件列出 \(N=100\)、\(L=200\)。主張分別交代塞車流的模擬估計與均勻流解的公式計算。 |
| 索引／`ours-finite-n-threshold` | 漏掉取大 \(N\) 極限時固定車距 \(b\) | 修好 | 主張寫明固定 \(b\)，增加車數時環長也增加。 |
| 索引／`ours-finite-n-simulation` | 把 22 台寫得像只有一個分界 | 修好 | 索引分別列出 \(b=2\) 和 \(b=2.5\) 的模擬值與公式值。 |
| 索引／`sugiyama2008-setup` | 「起步」容易讀成從靜止加速 | 修好 | 索引寫的是開始前已用約 30 km/h、近乎等距地繞圈。 |
| 索引／`sugiyama2008-23-vehicles` | 未明示相同的是塞車團的移動速度 | 部分修好 | 索引和卡片已一致，但**卡片主張**仍只寫「速度跟22台時一樣」。Sugiyama 第5頁第3段明指塞車團的移動速度。應在卡片補上主詞，再重建索引。NewJPhys_10_033001(2) |
| 索引／`sugiyama2008-fundamental-diagram` | 漏掉約 25 台/km 的量測範圍 | 修好 | 條件寫明單一地點、一個月，主張把數值限定在圖1的地點。 |
| 索引／`stern2018` | 索引的閱讀狀態多了預印本註記 | 修好 | 索引和文獻檔的 `read_status` 均為「全文已讀」。arXiv v1 與閱讀範圍記在 `read_scope`。 |

## 第二部分｜新發現的問題

| 卡片id或檔案 | 問題類型 | 嚴重程度（會誤導讀者／不精確／小問題） | 原文在哪裡 | 問題是什麼 | 建議怎麼改 |
|---|---|---|---|---|---|
| `stern2018-wave-returns` | 控制條件 | 不精確 | Stern 第7頁第3.3節、第10頁第4.2節、第13–14頁 | `conditions` 寫 C「沒有外部參數」。原文交代控制器有預設參數，實驗期間沒有調整外部參數，也不需要外部資訊。卡片主張的「實驗中沒有改任何外部參數」符合原文。1705.01693v1(2) | 將 `conditions` 改成「實驗C由帶飽和限制的 PI 控制器自行決定目標速度，控制期間未調整外部參數」。 |

## 第三部分｜自動產生的索引

審查包內的索引有 **39 張不同的卡片、6 筆文獻**。逐欄比對後，卡片的類型、狀態、條件、主張均與包內卡片一致，文獻的種類與閱讀狀態也均相符。現有主張中的卡片相對連結已正確改寫。人工介紹與導覽文字和自動區塊沒有矛盾。

| 產生或檢查方式 | 實測結果 | 建議怎麼改 |
|---|---|---|
| `index_with_generated()` 只定位第一組標記 | 在有效索引後附加第二組標記及過期主張，`check_wiki.py` 和 `build_index.py --check` 都回傳 `0`。讀者仍會看到第二份過期內容。 | 要求起訖標記各自獨立成行、各恰好出現一次，且順序正確。 |
| `sections()` 遇到重複的 `## 主張` 會覆蓋先前段落 | 在卡片原有主張之前插入另一段同名主張，索引漏掉新段落，兩支檢查仍都回傳 `0`。 | 檢查每張卡恰有一個 `## 主張`，重複時報錯。 |
| `fix_links()` 用正規表示式處理整段主張 | 測得 `[節名](#limits)` 複製到索引後仍指向索引內的錨點，行內程式碼裡形似連結的文字也會被改寫。包內這版索引沒有觸發這兩個情況。 | 將卡片內錨點轉成帶卡片路徑的連結，並跳過程式碼裡的連結字樣。 |

程式位置見審查包的 `sections()`、`fix_links()` 與 `index_with_generated()`。 

## 第四部分｜回歸測試

本機未能連上 GitHub 以 clone 並 checkout `5ab826c`。我用審查包附的三份原始碼執行可獨立運行的檢查，三份原始碼的 SHA-256 都與包內清單相符。

| 指令 | 實際結果 |
|---|---|
| `python3 tests/test_check_wiki.py` | 用本機 Python 3.10 執行。第一次 **69 個情境，失敗 1 個**，結束碼 `1`。僅對重跑程序設定 `GIT_ATTR_NOSYSTEM=1` 後，**69 個情境，失敗 0 個**，結束碼 `0`。 |
| `python3 scripts/check_wiki.py --strict` | **沒有執行**於指定 commit 的完整 repo。審查包自附的日誌記載 6 篇文獻、39 張卡、0 錯誤、0 警告。 |
| `python3 scripts/build_index.py --check` | 對審查包內的索引、文獻檔及卡片重建資料執行。輸出 `index.md跟文獻檔、證據卡同步`，結束碼 `0`。 |

「改了卡片的主張沒重建索引要擋」確實把 `230m` 改成 `260m`，兩次執行都收到 `wiki/index.md` 不同步的錯誤。第一次執行的失敗輸出如下。

```text
[FAIL] 歷史裡有PDF：--strict是錯誤
    預期：錯誤裡有「出現過PDF：a.pdf」
    實際：沒有錯誤
共69個情境，失敗1個。
```

| 測試或檢查問題 | 證據與影響 |
|---|---|
| Git 歷史檢查受系統的 PDF 文字轉換設定影響 | 單獨重跑失敗情境時，Git for Windows 嘗試啟動 `astextplain`，`git log -p` 回傳 `128`，檢查程式拋出例外，已記錄的 PDF 錯誤來不及印出。同一條 `git log` 加 `--no-textconv` 後回傳 `0`。建議歷史掃描明確關閉文字轉換，並在 Git 失敗時印出原因。 |
| SHA-256 排除會放過部分學號與手機樣式 | 實測一般表格的資料列以 `SHA-256` 開頭，便能被當成表頭，讓後一列測試用的學號樣式被遮蔽。`NotSHA-256` 後接測試字串也會遮蔽手機樣式。移除這些字樣後，兩者均可偵測。同一行的測試金鑰仍被抓到，程式也確實用原始行掃金鑰。建議驗證真正的表頭及獨立的標記，補上這兩個反例。 |
| 預期錯誤的測試在整份輸出搜尋關鍵字 | 測試要求結束碼為 `1`，但關鍵字可出現在任一行。指定訊息若只出現在警告，而另一項無關錯誤讓程式回傳 `1`，測試仍可能通過。應在 `[錯誤]` 行內比對指定訊息。n3-package-r4 |

## 第五部分｜無法確認的地方

- **bando.pdf 的掃描正文讀不到。** 相關索引判定以審查包內的卡片與索引為據。Bando 第1035–1042頁的原文、公式及模擬數值未能直接核對。
- **Stern B 場的 14 mph 有兩種標法。** PDF 第10、12頁寫 6.25 m/s，第11頁正文與表2寫 6.26 m/s。可確認目標從 14 調到 16 mph，無法由預印本確定兩種公制標法的差異是怎麼來的。1705.01693v1(2)
- **Sugiyama 第5頁腳註15沒有指名後續論文。** 無法確認它當時特指 Tadaki 2013。NewJPhys_10_033001(2)
- 無法確認指定 commit 的完整 repo 在 `--strict` 下的實際結果，也無法從審查包確認人工導覽中 `disputes.md`、`slide-map.md` 和 `derivations/finite-n-threshold.md` 三個目標在該 commit 能否開啟。

- 第3輪問題修好 23 條、部分修好 1 條、沒修好 0 條；新問題 1 條（其中會誤導讀者 0 條）；索引問題 3 條；測試問題 3 條。
- 有沒有重大問題（會誤導讀者、科學錯誤、沒修好、索引不同步、測試沒通過或測不到它宣稱的事）：有。

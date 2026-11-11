"""產生第3關（研究差異與忠實度審查）的審查包。

用法：
  python3 scripts/make_review_package.py                     # 第1輪：全部檔案，輸出pipeline/review/n3-package.md
  python3 scripts/make_review_package.py --since <commit> --previous <上一輪審查原文> --round 2
      # 第2輪以後：只放<commit>之後改過的Wiki檔案，加上上一輪的審查意見，請審查者確認有沒有修好
審查包只放審查標準、文獻檔、證據卡、研究差異和推導文件，不放我們的ingest紀錄和自己的看法，
避免審查的AI被生成者的判斷影響。每個輸入檔的SHA-256寫在檔頭，之後Wiki改了，就知道這份審查過期了。
第2輪以後的審查包另外附上沒改過的證據卡的開頭欄位和「主張」、沒改過的文獻檔開頭欄位，
只給審查者核對index.md和證據卡是否一致（第3輪起加的，因為第2輪發現索引摘要沒跟著卡片更新）。
"""
import argparse
import hashlib
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "pipeline" / "review" / "n3-package.md"

PDFS = """## 上傳的PDF和對應的文獻id

| 文獻id | 檔案 | 注意 |
|---|---|---|
| bando1995 | bando.pdf | 掃描檔，頁碼看頁首的1035～1042 |
| sugiyama2008 | NewJPhys_10_033001.pdf | 前面多兩頁（典藏庫封面和出版商的頁面），頁碼看頁首的1～7 |
| nagel1992 | ajp-jp1v2p2221.pdf | 掃描檔，頁碼2221～2229 |
| tadaki2013 | NewJPhys_15_103034.pdf | 前面多兩頁，頁碼看頁首 |
| stern2018 | 1705.01693v1.pdf | arXiv預印本，頁碼就是PDF頁碼 |
| orosz2010 | PTRSA2published.pdf | 頁碼4455～4479；Wiki只讀了部分章節，見文獻檔的read_scope |

"""

CRITERIA_RAW = """# 審查包：幽靈塞車Wiki的研究差異與忠實度審查

## 你的角色

你是獨立審查者。這份Wiki是另一個AI依6篇論文整理的，整理的人沒有參與這次審查。請對照我同時上傳的論文PDF，檢查證據卡有沒有讀錯原文。你的意見不會被直接採用，有爭議的地方我們會再回原文核對，所以請只寫你在PDF裡確認得到的事，不確定就寫不確定。

{pdfs}## 要檢查的五件事

1. **忠實度**：每張卡的「主張」和「原文依據」有沒有讀錯、誇大、或漏掉會改變意思的條件。數字、單位、頁碼、圖表和式子編號對不對。
2. **證據類型**：`type`有沒有放錯。experiment是論文裡真實車輛的實驗或觀測；model_theory是論文裡的模型、推導或電腦模擬；review是綜述的整理；our_derivation、our_simulation是我們自己的。特別注意：有沒有把模型或模擬的結果寫得像真實道路已經證實。
3. **條件能不能比**：卡片之間或`disputes.md`裡拿來比較的東西，條件（車數、環長、密度單位、有沒有因次、實驗或模型）是不是真的能比。
4. **研究差異的分類**：`disputes.md`每一條的分類（1假設或方法不同、2條件不同、3結論真的衝突、4資料不足）和「目前判斷」合不合理，有沒有被強行統一或選邊。
5. **我們自己的推導**：`derivations/finite-n-threshold.md`從Bando 1995式(9)(11)和Orosz 2010附錄A推出22台車分界的過程，代換和適用條件有沒有錯。

不用檢查中文文筆，也不用提新的研究方向。

## 請照這個格式回覆

第一部分，有問題的卡片，一張一列（沒問題的不用列）：

| 卡片id | 問題類型（忠實度／證據類型／條件比較／分類／推導） | 嚴重程度（會誤導讀者／不精確／小問題） | 原文在哪裡（頁、段、式、圖） | 問題是什麼 | 建議怎麼改 |

第二部分，`disputes.md`各條的意見。

第三部分，推導文件的意見。

第四部分，你沒辦法確認的地方（例如掃描檔看不清楚、PDF裡找不到），列出來就好，不要猜。

最後一行寫：總共檢查了幾張卡、有問題的幾張。
"""

CRITERIA = CRITERIA_RAW.replace("{pdfs}", PDFS)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


RECHECK = """# 審查包（第{round}輪）：確認上一輪的問題有沒有修好

## 你的角色

你是獨立審查者。上一輪你（或另一個審查者）對這份Wiki提出了意見，原文附在最後。整理的人逐條回到論文核對後修改了下面這些檔案。請對照同樣的6篇論文PDF，確認：

1. 上一輪列出的每一個問題，有沒有修好。
2. 修改有沒有引入新的錯誤（讀錯原文、數字或頁碼錯、把模型講成實驗、語氣過度）。整理的人有時也會改上一輪沒指出的地方，這些一樣要檢查。
3. `wiki/index.md`跟證據卡是否一致：索引裡每一列的類型、狀態和摘要，跟那張卡的`type`、`status`和「主張」有沒有不一樣，摘要有沒有比主張講得更強、或漏掉會改變意思的條件；文獻那張表的種類和閱讀狀態，跟文獻檔的`kind`、`read_status`是否相同。全部列都要看，不只這輪改過的。

這份審查包只完整放改過的檔案。沒改過的檔案上一輪已經看過，忠實度不用重看；最後的附錄只放它們的開頭欄位和「主張」，用來做第3項的核對。

{pdfs}
## 請照這個格式回覆

第一部分，上一輪的問題逐條回覆，一張卡一列：

| 卡片id或檔案 | 上一輪的問題 | 修好了嗎（修好／部分修好／沒修好） | 說明 |

第二部分，新發現的問題（沒有就寫「沒有」），格式跟上一輪的第一部分一樣：

| 卡片id | 問題類型 | 嚴重程度 | 原文在哪裡 | 問題是什麼 | 建議怎麼改 |

第三部分，`index.md`和證據卡不一致的地方（沒有就寫「沒有」）：

| 卡片id或文獻id | 索引寫的 | 卡片或文獻檔寫的 | 問題是什麼 |

第四部分，無法確認的地方。

最後一行寫：上一輪問題修好幾條、部分修好幾條、沒修好幾條；新問題幾條；索引不一致幾條。
"""


LIMITED = """# 審查包（第{round}輪，限定範圍）：第3輪問題的修正、自動產生的索引、檢查程式

## 你的角色

你是獨立審查者。這份Wiki的第3關（研究差異與忠實度審查）原本最多3輪，第3輪沒有通過；使用者另外授權這一輪限定範圍的複核，不是重新開始。第3輪的審查意見原文附在最後。請對照6篇論文PDF和這份審查包，只檢查下面四件事，不用重審其他沒改過的內容：

1. **第3輪的6條修正**有沒有修好：`stern2018-wave-returns`、`tadaki2013-critical-density`、`tadaki2013-density-dependence`、`orosz2010-ring-stability`、`glossary.md`的「相變」、`sources/sugiyama2008.md`的限制。特別看`stern2018-wave-returns`裡實驗A、B、C的控制方式和速度調整，是否分開而且跟原文一致。
2. **自動產生的`wiki/index.md`**：文獻表和39張證據卡的清單，現在由程式從文獻檔、證據卡產生（每張放類型、狀態、條件欄位原文和主張全文，不再另寫摘要）。請確認：
   - 39張都在，類型、狀態、條件、主張跟附錄裡的卡片一致，文獻的種類和閱讀狀態跟文獻檔一致。
   - 第3輪第三部分列的18條索引不一致，現在各自是否已解決。如果是卡片主張本身就缺條件，請標明是卡片的問題。
   - 開頭的介紹和導覽是人工寫的，也看一下有沒有跟自動產生的內容矛盾。
3. **這些修改有沒有引入新的錯誤**：讀錯原文、數字或頁碼錯、把模型講成實驗、語氣過度。
4. **相關程式的回歸測試**：審查包附了`scripts/check_wiki.py`、`scripts/build_index.py`、`tests/test_check_wiki.py`的原始碼和最近一次實際執行的輸出。請看：
   - 測試情境是否真的測到它名稱說的事（例如「改了卡片沒重建索引要擋」是不是真的會失敗）。
   - 學號、手機、金鑰等個資檢查有沒有因為SHA-256雜湊值的排除而變鬆。
   - 索引同步檢查有沒有漏洞。
   - 如果你的環境能連到GitHub，可以clone公開repo `guogeng-lo/phantom-traffic-lab`，checkout到commit `{commit}`，跑 `python3 tests/test_check_wiki.py`、`python3 scripts/check_wiki.py --strict`、`python3 scripts/build_index.py --check`，貼上實際結果；論文PDF不在repo裡，`check_quotes.py`不用跑。不能跑就寫「沒有執行」，不要推測結果。

{pdfs}

## 請照這個格式回覆

第一部分，第3輪的問題逐條回覆（6條修正和18條索引不一致，一條一列）：

| 卡片id或檔案 | 第3輪的問題 | 修好了嗎（修好／部分修好／沒修好） | 說明 |

第二部分，新發現的問題（沒有就寫「沒有」）：

| 卡片id或檔案 | 問題類型 | 嚴重程度（會誤導讀者／不精確／小問題） | 原文在哪裡 | 問題是什麼 | 建議怎麼改 |

第三部分，自動產生的索引：不一致或產生方式有問題的地方（沒有就寫「沒有」）。

第四部分，回歸測試：有沒有執行、實際結果、測試有沒有漏洞。

第五部分，無法確認的地方。

最後兩行寫：
- 第3輪問題修好幾條、部分修好幾條、沒修好幾條；新問題幾條（其中會誤導讀者幾條）；索引問題幾條；測試問題幾條。
- 有沒有重大問題（會誤導讀者、科學錯誤、沒修好、索引不同步、測試沒通過或測不到它宣稱的事）：有／沒有。
"""


ENGINEERING = """# 工程審查包：檢查程式和回歸測試（只審程式，不審文獻）

## 你的角色

你是獨立審查者。這份Wiki有兩支檢查程式：`scripts/check_wiki.py`（格式、索引同步、個資和金鑰掃描，包含Git歷史）和`scripts/build_index.py`（從證據卡產生索引）。上一次審查（附在最後）找到7項程式問題，整理的人先把反例寫成測試、在舊版重現，再修改程式。這次**只審程式碼和回歸測試**，不審論文、證據卡或科學內容，也不需要論文PDF。

請確認：

1. **7項問題都修好了**：SHA-256偽表頭、`NotSHA-256`這類偽標記、測試只在整份輸出找關鍵字、索引標記重複、證據卡有重複的`## 主張`、錨點和程式碼裡的連結、Git textconv和Git指令失敗的處理。
2. **反例測試有效**：每個新測試真的測到它名稱說的事；在舊版會失敗、在新版會通過（修改前後的實際輸出附在後面）。判定規則`judge()`會不會被騙。
3. **沒有引入新的重大漏判**：
   - 學號、手機、信箱、路徑、金鑰、座號的偵測，有沒有任何寫法能讓它漏掉（特別是SHA-256排除）。
   - 索引能不能在沒報錯的情況下跟證據卡不同步。
   - Git指令失敗時會不會被當成沒問題。
4. **能跑就跑**：如果你的環境能連到GitHub，請clone公開repo `guogeng-lo/phantom-traffic-lab`，checkout到commit `{commit}`，跑：
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
"""


def changed_since(commit):
    out = subprocess.run(["git", "diff", "--name-only", commit, "--", "wiki"], cwd=ROOT,
                         capture_output=True, text=True, check=True).stdout.split()
    return sorted(ROOT / f for f in out if f.endswith(".md") and not f.endswith("_template.md")
                  and (ROOT / f).is_file())


def summary_only(p):
    """只留開頭欄位和「## 主張」那一段（文獻檔只留開頭欄位）。"""
    text = p.read_text(encoding="utf-8")
    head_end = text.index("\n---", 4) + 4
    keep = text[:head_end].strip()
    if "/cards/" in p.as_posix() and "## 主張" in text:
        claim = text.split("## 主張", 1)[1].split("\n## ", 1)[0].strip()
        keep += "\n\n## 主張\n\n" + claim
    return keep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since")
    ap.add_argument("--previous")
    ap.add_argument("--round", type=int, default=1)
    ap.add_argument("--limited", action="store_true", help="限定範圍的複核（第3關第4輪）")
    ap.add_argument("--engineering", action="store_true", help="只審程式和測試，不放Wiki檔案")
    ap.add_argument("--extra", nargs="*", default=[], help="另外附上的程式或執行輸出（原文照放）")
    args = ap.parse_args()
    wiki = ROOT / "wiki"
    if args.engineering:
        files, appendix = [], []
        commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True,
                                text=True, check=True).stdout.strip()
        head = ENGINEERING.replace("{commit}", commit)
        out_path = ROOT / "pipeline" / "review" / "n3-engineering-review.md"
    elif args.since:
        files = changed_since(args.since)
        template = LIMITED if args.limited else RECHECK
        commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True,
                                text=True, check=True).stdout.strip()
        head = template.replace("{round}", str(args.round)).replace("{pdfs}", PDFS).replace("{commit}", commit)
        changed = set(files)
        appendix = sorted(p for d in ("sources", "cards") for p in (wiki / d).glob("*.md")
                          if p.name != "_template.md" and p not in changed)
        out_path = ROOT / "pipeline" / "review" / f"n3-package-r{args.round}.md"
    else:
        # index.md也要放：它的每張卡摘要是卡片主張的縮寫，卡片改了它常常沒跟著改（第2輪審查才發現）
        files = [wiki / "index.md", wiki / "glossary.md", wiki / "disputes.md", wiki / "derivations" / "finite-n-threshold.md"]
        files += sorted(p for p in (wiki / "sources").glob("*.md") if p.name != "_template.md")
        files += sorted(p for p in (wiki / "cards").glob("*.md") if p.name != "_template.md")
        head = CRITERIA
        out_path = OUT
        appendix = []
    out = [head, "\n## 這份審查包包含的檔案版本\n", "| 檔案 | SHA-256 |", "|---|---|"]
    extra = [ROOT / e for e in args.extra]
    out += [f"| `{p.relative_to(ROOT).as_posix()}` | `{sha(p)}` |" for p in files + appendix + extra]
    if files:
        out.append("\n# 以下是要審查的Wiki內容\n")
    for p in files:
        out.append(f"\n\n========== 檔案：{p.relative_to(ROOT).as_posix()} ==========\n")
        out.append(p.read_text(encoding="utf-8").strip())
    if appendix:
        out.append("\n\n========== 附錄：沒改過的檔案，只放開頭欄位和主張（只用來核對index.md） ==========\n")
        for p in appendix:
            out.append(f"\n\n---------- {p.relative_to(ROOT).as_posix()} ----------\n")
            out.append(summary_only(p))
    for p in extra:
        out.append(f"\n\n========== 程式或執行輸出：{p.relative_to(ROOT).as_posix()} ==========\n")
        out.append("```\n" + p.read_text(encoding="utf-8").strip() + "\n```")
    if args.previous:
        out.append("\n\n========== 上一輪的審查意見原文 ==========\n")
        out.append((ROOT / args.previous).read_text(encoding="utf-8").strip())
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
    n_cards = sum(1 for p in files if "/cards/" in p.as_posix())
    print(f"已產生 {out_path.relative_to(ROOT).as_posix()}：完整檔案 {len(files)} 個（其中證據卡 {n_cards} 張），"
          f"附錄 {len(appendix)} 個，程式或輸出 {len(extra)} 個，{out_path.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()

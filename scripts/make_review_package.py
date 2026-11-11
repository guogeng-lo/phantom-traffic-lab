"""產生第3關（研究差異與忠實度審查）的審查包。

用法：python3 scripts/make_review_package.py
輸出：pipeline/review/n3-package.md
審查包只放審查標準、文獻檔、證據卡、研究差異和推導文件，不放我們的ingest紀錄和自己的看法，
避免審查的AI被生成者的判斷影響。每個輸入檔的SHA-256寫在檔頭，之後Wiki改了，就知道這份審查過期了。
"""
import hashlib
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "pipeline" / "review" / "n3-package.md"

CRITERIA = """# 審查包：幽靈塞車Wiki的研究差異與忠實度審查

## 你的角色

你是獨立審查者。這份Wiki是另一個AI依6篇論文整理的，整理的人沒有參與這次審查。請對照我同時上傳的論文PDF，檢查證據卡有沒有讀錯原文。你的意見不會被直接採用，有爭議的地方我們會再回原文核對，所以請只寫你在PDF裡確認得到的事，不確定就寫不確定。

## 上傳的PDF和對應的文獻id

| 文獻id | 檔案 | 注意 |
|---|---|---|
| bando1995 | bando.pdf | 掃描檔，頁碼看頁首的1035～1042 |
| sugiyama2008 | NewJPhys_10_033001.pdf | 前面多一張典藏庫封面，頁碼看頁首的1～7 |
| nagel1992 | ajp-jp1v2p2221.pdf | 掃描檔，頁碼2221～2229 |
| tadaki2013 | NewJPhys_15_103034.pdf | 前面多兩頁，頁碼看頁首 |
| stern2018 | 1705.01693v1.pdf | arXiv預印本，頁碼就是PDF頁碼 |
| orosz2010 | PTRSA2published.pdf | 頁碼4455～4479；Wiki只讀了部分章節，見文獻檔的read_scope |

## 要檢查的五件事

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


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    wiki = ROOT / "wiki"
    files = [wiki / "glossary.md", wiki / "disputes.md", wiki / "derivations" / "finite-n-threshold.md"]
    files += sorted(p for p in (wiki / "sources").glob("*.md") if p.name != "_template.md")
    files += sorted(p for p in (wiki / "cards").glob("*.md") if p.name != "_template.md")
    out = [CRITERIA, "\n## 這份審查包包含的檔案版本\n", "| 檔案 | SHA-256 |", "|---|---|"]
    out += [f"| `{p.relative_to(ROOT).as_posix()}` | `{sha(p)}` |" for p in files]
    out.append("\n# 以下是要審查的Wiki內容\n")
    for p in files:
        out.append(f"\n\n========== 檔案：{p.relative_to(ROOT).as_posix()} ==========\n")
        out.append(p.read_text(encoding="utf-8").strip())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
    n_cards = sum(1 for p in files if "/cards/" in p.as_posix())
    print(f"已產生 {OUT.relative_to(ROOT).as_posix()}：{len(files)} 個檔案，其中證據卡 {n_cards} 張，"
          f"{OUT.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()

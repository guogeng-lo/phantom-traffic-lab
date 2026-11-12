"""產生節點6（逐頁稿審查）的審查包。

用法：
  python3 scripts/make_page_review_package.py                                   # 第1輪，輸出pipeline/review/n6-package-r1.md
  python3 scripts/make_page_review_package.py --round 2 --previous <上一輪審查原文>  # 第2輪以後，附上上一輪的審查意見
  python3 scripts/make_page_review_package.py --round 4 --previous <上一輪審查原文> --limited --since <commit>
      # 使用者授權的限定範圍複核：多放pipeline/review/n6-criteria-r4.md和<commit>之後逐頁稿的修改前後對照

審查包放：判定標準（pipeline/review/n6-criteria.md原文）、逐頁稿的共同規則、十頁逐頁稿、
逐頁稿用到的全部證據卡全文、術語表、slide-map。
不放我們的執行紀錄和對審查結果的看法，避免審查的AI被生成者的判斷影響。
逐頁稿「要小心」裡寫了要審查確認的句子，程式會挑出來列成一張清單，請審查者逐條回答。
每個輸入檔的SHA-256寫在審查包裡，之後檔案改了，就知道這份審查過期了。
"""
import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_pages import split_sections  # noqa: E402

HEAD = """# 審查包（節點6，第{round}輪）：幽靈塞車教學簡報的逐頁稿

## 你的角色

你是獨立審查者。這份教學簡報是給**完全沒有交通流背景的一般人**自己看、自己操作的，不會有人講解。逐頁稿是另一個AI依證據卡寫的，寫的人沒有參與這次審查。你的意見不會被直接採用，我們會回到證據卡和原始文獻核對，所以請只寫你在證據卡裡確認得到的事，不確定就寫不確定。

這份審查包的組成：
1. 判定標準（我們在送審之前寫好、commit的，下面原文照放）。
2. 逐頁稿的共同規則（`pipeline/pages/README.md`）。
3. 十頁逐頁稿。每頁的「主線」「知識」「進階」就是讀者會看到的文字；「畫面和互動」是畫面規格，裡面「」括起來的是讀者看得到的字；「顯示設定」「數字從哪來」「要小心」是給審查和建置的人看的。
4. 逐頁稿用到的全部證據卡全文、術語表和頁面對照表（`wiki/slide-map.md`）。

證據卡的類型：experiment是論文裡真的車、真的路；model_theory是論文裡的模型或推導；review是綜述的整理；our_derivation是我們自己的推導；our_simulation是我們自己的模擬或測試。

程式已經檢查過：每頁的段落齊全、證據卡跟頁面對照表一致、頁面上的每個數字都在「數字從哪來」裡、而且在寫的那張卡裡找得到。**程式只比對數字有沒有出現，不判斷是不是同一件事的數字**，所以數字和條件配對錯了，還是要你看。

{previous_note}
"""

FORMAT = """
## 請照這個格式回覆

第一部分，有問題的地方，一處一列（沒問題的不用列）：

| 頁 | 段落 | 問題類型（超出證據／扭曲原意／誤導／數字或條件配錯／標示錯） | 嚴重程度（會誤導讀者／不精確／小問題） | 頁面原文（短句） | 證據卡怎麼說（卡片id和段落） | 建議怎麼改 |

第二部分，下面「請逐條回答」清單裡的每一條：可以／不可以／不確定，加上理由。

第三部分，三個學習目標：一般讀者照這十頁讀完，能不能用自己的話說出「沒有事故為什麼也會塞車」「為什麼車往前開，塞車波卻往後傳」「什麼條件下小變化會放大」？哪一頁最可能讓人卡住或誤會？（簡短就好）

第四部分，你沒辦法確認的地方，列出來就好，不要猜。

{recheck_format}最後兩行寫：
- 總共幾條問題，其中會誤導讀者幾條、不精確幾條、小問題幾條。
- 有沒有「會誤導讀者」的問題：有／沒有。
"""

RECHECK_NOTE = """這是第{round}輪。上一輪的審查意見原文附在最後。寫逐頁稿的人逐條核對後改了一些地方。請確認上一輪的每一條有沒有改好，也檢查修改有沒有引入新的問題。"""

LIMITED_NOTE = """這是第{round}輪，是使用者在第3輪不通過之後**授權的限定範圍複核**，不是重新開始。範圍和判定寫在下面的「第{round}輪的範圍和判定標準」（送審前commit）。上一輪的審查意見原文附在最後，這一輪的修改前後對照（git diff）也附在後面。

請只做兩件事：
1. 上一輪第一部分列的每一條，有沒有改好。
2. 這些修改有沒有引入新的錯誤或誤導。沒有修改的文字不用重審；但如果你發現**修改直接造成**的新重大錯誤，一定要指出。"""

LIMITED_FORMAT = """
## 請照這個格式回覆

第零部分，上一輪的問題逐條回覆：

| 頁 | 上一輪的問題 | 改好了嗎（改好／部分改好／沒改好） | 說明 |

第一部分，修改直接造成的新問題（沒有就寫「沒有」）：

| 頁 | 段落 | 問題類型 | 嚴重程度（會誤導讀者／不精確／小問題） | 頁面原文（短句） | 證據卡怎麼說 | 建議怎麼改 |

第二部分，你沒辦法確認的地方，列出來就好，不要猜。

最後兩行寫：
- 上一輪問題改好幾條、部分改好幾條、沒改好幾條；新問題幾條（其中會誤導讀者幾條）。
- 照「第{round}輪的範圍和判定標準」，這一輪通過還是不通過。
"""

RECHECK_FORMAT = """另外，第零部分（放在最前面），上一輪的問題逐條回覆：

| 頁 | 上一輪的問題 | 改好了嗎（改好／部分改好／沒改好） | 說明 |

"""


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def page_cards(text):
    body = dict(split_sections(text))
    ids = []
    for line in body.get("證據卡", "").splitlines():
        m = re.match(r"^- 【[^】]+】(.+)$", line.strip())
        if m:
            ids += [c for c in re.split(r"[、,，\s]+", m.group(1).strip()) if c]
    return ids


def to_confirm(pages):
    """「要小心」裡提到審查要確認的句子。"""
    out = []
    for p in pages:
        body = dict(split_sections(p.read_text(encoding="utf-8")))
        for line in body.get("要小心", "").splitlines():
            if re.search(r"審查(時|一起|確認)|要在逐頁稿審查", line):
                out.append(f"- {p.stem}：{line.strip()[2:] if line.strip().startswith('- ') else line.strip()}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--round", type=int, default=1)
    ap.add_argument("--previous")
    ap.add_argument("--limited", action="store_true", help="使用者授權的限定範圍複核")
    ap.add_argument("--since", help="--limited時：從這個commit之後的逐頁稿修改做前後對照")
    args = ap.parse_args()
    if args.limited and not (args.since and args.previous):
        sys.exit("--limited要同時給--since和--previous")
    if args.round > 1 and not args.previous:
        sys.exit("第2輪以後要用--previous附上上一輪的審查原文")

    criteria = ROOT / "pipeline" / "review" / "n6-criteria.md"
    readme = ROOT / "pipeline" / "pages" / "README.md"
    pages = sorted((ROOT / "pipeline" / "pages").glob("p[0-9][0-9].md"))
    ids = []
    for p in pages:
        for c in page_cards(p.read_text(encoding="utf-8")):
            if c not in ids:
                ids.append(c)
    cards = [ROOT / "wiki" / "cards" / f"{c}.md" for c in sorted(ids)]
    missing = [c for c in cards if not c.exists()]
    if missing:
        sys.exit("找不到證據卡：" + "、".join(c.stem for c in missing) + "（先跑scripts/check_pages.py）")
    others = [ROOT / "wiki" / "glossary.md", ROOT / "wiki" / "slide-map.md"]
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True,
                            text=True, check=True).stdout.strip()

    if args.limited:
        note = LIMITED_NOTE.replace("{round}", str(args.round))
    else:
        note = RECHECK_NOTE.replace("{round}", str(args.round)) if args.round > 1 else ""
    out = [HEAD.replace("{round}", str(args.round)).replace("{previous_note}", note)]
    if args.limited:
        out.append(LIMITED_FORMAT.replace("{round}", str(args.round)))
        scope = ROOT / "pipeline" / "review" / f"n6-criteria-r{args.round}.md"
        out.append(f"\n## 第{args.round}輪的範圍和判定標準\n")
        out.append(scope.read_text(encoding="utf-8").strip())
        diff = subprocess.run(["git", "-c", "core.quotePath=false", "diff", "--no-color", args.since, "--", "pipeline/pages"],
                              cwd=ROOT, capture_output=True, text=True, check=True).stdout
        out.append(f"\n## 這一輪的修改前後對照（`git diff {args.since} -- pipeline/pages`）\n")
        out.append("```diff\n" + diff.strip() + "\n```")
    else:
        out.append(FORMAT.replace("{recheck_format}", RECHECK_FORMAT if args.round > 1 else ""))
        out.append("\n## 請逐條回答\n\n逐頁稿的「要小心」裡，寫的人標了要在審查時確認的地方：\n")
        out += to_confirm(pages) or ["（沒有）"]
    out.append(f"\n## 這份審查包包含的檔案版本\n\n產生時的commit：`{commit}`（公開repo `guogeng-lo/phantom-traffic-lab`）\n")
    out += ["| 檔案 | SHA-256 |", "|---|---|"]
    files = [criteria, readme] + pages + cards + others
    if args.limited:
        files.insert(1, ROOT / "pipeline" / "review" / f"n6-criteria-r{args.round}.md")
    out += [f"| `{p.relative_to(ROOT).as_posix()}` | `{sha(p)}` |" for p in files]
    for title, group in (("判定標準", [criteria]), ("逐頁稿的共同規則", [readme]), ("逐頁稿", pages),
                         ("證據卡", cards), ("術語表和頁面對照表", others)):
        out.append(f"\n\n# {title}\n")
        for p in group:
            out.append(f"\n========== 檔案：{p.relative_to(ROOT).as_posix()} ==========\n")
            out.append(p.read_text(encoding="utf-8").strip())
    if args.previous:
        out.append("\n\n========== 上一輪的審查意見原文 ==========\n")
        out.append((ROOT / args.previous).read_text(encoding="utf-8").strip())
    out_path = ROOT / "pipeline" / "review" / f"n6-package-r{args.round}.md"
    out_path.write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
    print(f"已產生 {out_path.relative_to(ROOT).as_posix()}：逐頁稿 {len(pages)} 頁，證據卡 {len(cards)} 張，"
          f"要逐條回答 {len(to_confirm(pages))} 條，{out_path.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()

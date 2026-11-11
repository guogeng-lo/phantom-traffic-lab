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
